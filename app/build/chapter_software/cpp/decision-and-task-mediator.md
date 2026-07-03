# DecisionModule 与 TaskMediator

如果你问“C++ Core 里哪两个名字最值得先搞懂”，`DecisionModule` 和 `TaskMediator` 基本就是标准答案。前者决定一帧决策流程怎么排布，后者决定这一帧的任务和角色身份放在哪里、由谁来读。

## `CDecisionModule` 的职责不是“算所有东西”，而是“把一帧组织好”

`DecisionModule` 自己并不直接承担所有底层计算，它更像是一个导演：负责安排谁先上场、谁后上场、什么时候轮到 Python 决策、什么时候轮到 C++ 继续细化任务。

从当前实现看，它至少承担三类职责：

1. 管理脚本语言入口，是走旧 Lua 还是当前 Python；
2. 把“生成高层任务”和“规划底层任务”这两段时序分开；
3. 作为视觉层和动作层之间的中间调度者。

这也是为什么它虽然代码量不算整个仓库里最多，却几乎处在每条主链路的中心。

## 初始化阶段，它先决定这一套系统今天说哪门语言

`DecisionModule` 构造时会读取：

```text
ScriptLanguage/CurrentScriptLanguage
```

如果配置是 `LUA`，它会走旧脚本入口；如果是 `PYTHON`，它会初始化嵌入式 Python 解释器、执行 `InitAllModules.py`，并只 import 一次 `SelectPlay` 模块。当前主线当然是 Python，所以你在日常开发里更多会看到后一条路径。

这里有个很值得记住的点：**Python 顶层并不是另外起了一个平行系统，而是被嵌进了同一个 C++ 决策流程里。**

## 一帧里最关键的分界线：`GenerateTasks()` 和 `PlanTasks()`

理解 `DecisionModule` 最有效的方法，就是先把这一帧拆成两个问题。

第一个问题是：

> 顶层现在到底想让哪几台车做什么？

这是 `GenerateTasks()` 负责的。在 Python 主线下，它的真实含义就是：调用 `SelectPlay.py` 和具体 Play 脚本，让 Python 把这一帧的任务通过 `CppPackage.makeIt...` 重新写回 C++。

第二个问题是：

> 这些已经选好的高层任务，接下来怎么一步步细化，直到变成真正的执行命令？

这就是 `PlanTasks()` 负责的部分。

很多人第一次看代码时，会下意识把这两步当成“一个大决策函数里的两个普通阶段”，但其实它们对应的是完全不同的层级。前者更接近战术选择，后者更接近执行规划。

## `PlanTasks()` 真正在做什么

`PlanTasks()` 的逻辑其实很耐看。它先把 `TaskMediator` 里已经注册好的任务取出来，再按优先级做排序，最后依次调用每个任务的 `plan()`。这意味着它做的不是“重新生成任务”，而是对现有任务做递归下钻。

它的工作顺序大致可以翻译成：

1. 遍历所有车号；
2. 找出本帧确实已经分配了任务的那些执行者；
3. 读取每个任务在 `TaskMediator` 里记录的优先级；
4. 先高优先级、后低优先级地调用 `plan()`。

这个排序并不是装饰性的。因为有些 Skill 会占用关键球权、关键空间，先规划谁、后规划谁，确实会影响最终效果。也正因为如此，`TaskMediator` 不只记录“有没有任务”，还要记录“任务优先级”。

## `TaskMediator` 最好被理解成什么

最直白的理解方式是：

> `TaskMediator` 是“本帧任务中心”加“角色标签中心”。

它至少负责四件事：

- 存每台车当前的 `CPlayerTask*`；
- 存这个任务的优先级；
- 存守门员、后卫、leader、marking 等角色标签；
- 给下游模块提供统一查询接口。

这也是为什么它在仓库里被这么多模块 include。因为一旦进入底层 Skill、路径规划、运动控制这条链，大家都需要一个共享的地方来问：“当前这台车是谁？它这帧被分到了什么身份？”

## 为什么 `registerRole()` 这么重要

你在 Python 的 `Skill.py` 里经常会看到类似：

```python
taskMediator.registerRole(executor, "leader")
CppPackage.TaskMediator.Instance().registerRole(executor, "leader")
```

别把它当成单纯的调试注释。它真正的意义是把“这台车这帧的身份”同步给整个 C++ Core。后面 `SmartGotoPositionV4` 之类的模块会根据这些角色标签，决定：

- 这台车是不是守门员；
- 是不是后卫；
- 能不能采用某些特殊的速度上限；
- 在禁区、摆球区、stop 球圈附近应该套哪种约束。

所以 `TaskMediator` 不是一个被动仓库，而是角色语义在 C++ 侧的共享源头。

## `TaskMediator` 里保存的内容会在每帧开始时清空

这一点必须知道。`DecisionModule::DoDecision()` 一开始就会调用：

```cpp
TaskMediator::Instance()->cleanOldTasks();
```

这意味着 `TaskMediator` 存的是**本帧任务状态**，而不是一个长期数据库。跨帧需要保留的东西，通常要回到 `Global`、状态机上下文或其他专门的缓存结构里管理。否则你很容易误以为“上一帧的任务应该还在”，结果读到的是空任务。

## `PlayerRole::makeIt...`、`TaskFactoryV2` 和 pybind 之间的关系

从 Python 顶层看，你平时更常见的调用姿势是：

- `CppPackage.makeItRushTo(...)`
- `CppPackage.makeItWBack(...)`
- `CppPackage.makeItCrossover(...)`

但在 C++ 内部，这条链通常会继续变成：

```text
Python / 顶层脚本
    -> pybind 包装函数
    -> TaskT 参数封装
    -> TaskFactoryV2 创建 CPlayerTask
    -> TaskMediator 保存
    -> DecisionModule::PlanTasks() 调 plan()
```

所以 `TaskMediator` 在这条链上既是“落点”，也是“中转站”。高层任务先落到这里，之后 `DecisionModule` 再从这里把任务取走，送进递归的 Skill 规划过程。

## 这套结构为什么对 Python-C++ 混合架构特别重要

原因其实很朴素。Python 顶层的强项是表达高层意图，而不是管理底层 `CPlayerTask` 对象的生命周期。当前架构让 Python 在自己擅长的层级表达任务，再由 C++ 接管对象创建、优先级排序、递归规划和最终执行，这样边界就非常清晰。

换句话说，Python 负责说“我要这个角色干这件事”，C++ 负责回答“好，那我现在把这件事规划到底层，让它真能跑起来”。`DecisionModule` 和 `TaskMediator` 就是这次交接里最关键的两个节点。

## 顺着代码追一条完整链，会非常有帮助

以后当你看到一个 Python 包装函数，例如 `Skill.RushTo(...)`，可以刻意顺着下面这条链追一次：

1. `RoleMatch_LuaStyle/Skills/Skill.py`
2. `CppPackage.makeIt...`
3. `Pybind11Module/Strategy/Skill/pybind_Skill.cpp`
4. `TaskFactoryV2` / `PlayerRole::makeIt...`
5. `TaskMediator::setPlayerTask(...)`
6. `DecisionModule::PlanTasks()`
7. 对应 C++ Skill 的 `plan()`

一旦你这样完整走通过一次，再回来看这两个类，很多原本抽象的描述都会变得特别具体。
