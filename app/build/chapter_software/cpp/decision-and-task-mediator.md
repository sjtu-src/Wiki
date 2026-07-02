# DecisionModule 与 TaskMediator

这两个类几乎是理解 C++ Core 的必经之路。

## `CDecisionModule` 在做什么

`DecisionModule` 不负责所有细节计算，但它负责把一帧决策过程组织起来。

在当前实现中，它至少负责三类事：

1. 管理脚本语言入口（Lua 或 Python）
2. 控制“生成任务”和“规划任务”的时序
3. 作为视觉与动作层之间的中间调度者

## 初始化时发生了什么

`DecisionModule` 构造时会读取：

```text
ScriptLanguage/CurrentScriptLanguage
```

然后决定：

- 如果是 `LUA`，走旧脚本入口
- 如果是 `PYTHON`，执行 `InitAllModules.py` 并 import `SelectPlay`

当前默认主线已经是 Python。

## 一帧里最重要的两个动作

### `GenerateTasks()`

这一阶段回答的是：

> 顶层到底想让每台车干什么？

在 Python 主线下，本质上就是让 `SelectPlay.py` 和具体 Play 脚本把任务塞进 `TaskMediator`。

### `PlanTasks()`

这一阶段回答的是：

> 已经分好的这些任务，如何递归展开成真正能执行的底层控制任务？

它会：

- 读取 `TaskMediator` 中每台车当前任务
- 按任务优先级排序
- 依次调用各个 `CPlayerTask::plan()`

也就是说，高层任务“被创建出来”还不够，还必须经过 C++ Skill 的进一步规划。

## `TaskMediator` 到底是什么

最直接的理解方式是：

> `TaskMediator` 是“本帧任务中心”和“角色标签中心”。

它主要承担：

- 记录每台车当前被分配到的 `CPlayerTask`
- 记录优先级
- 记录 goalie / back / marking / advancer 等角色标签
- 提供统一接口给各模块查询当前任务状态

这也是为什么很多模块都会 include `TaskMediator.h`。

## 为什么很多 Skill 逻辑都依赖它

例如在 `SmartGotoPositionV4` 或防守相关 Skill 里，经常要区分：

- 这台车是不是守门员
- 是不是后卫
- 当前是不是某个特殊角色

这些判断不适合每个模块自己维护一份，所以会统一从 `TaskMediator` 查。

## `PlayerRole::makeIt...` 与 `TaskFactoryV2`

从 Python 或更高层看，常见调用姿势是：

- `CppPackage.makeItRushTo(...)`
- `CppPackage.makeItWBack(...)`
- `CppPackage.makeItCrossover(...)`

但在 C++ 内部，真正创建任务的核心通常是：

- `PlayerRole::makeIt...`
- `TaskFactoryV2::...`

可以把这条链理解成：

```text
Python / 顶层脚本
    -> pybind 中介函数
    -> TaskT 参数封装
    -> TaskFactoryV2 创建 CPlayerTask
    -> TaskMediator 保存
```

## 为什么这套结构对 Python-C++ 混合架构很关键

因为 Python 顶层并不直接参与底层 task 对象的生命周期管理。  
Python 更多是在“描述任务”，真正把任务放进系统、排序、规划、执行，仍然由 C++ 完成。

这让架构边界非常清楚：

- Python 负责表达高层意图
- C++ 负责把意图变成高实时执行逻辑

## 读代码时的一个实用技巧

当你看到一个 Python 技能函数，例如 `Skill.RushTo(...)`，可以顺着下面这条链去追：

1. `RoleMatch_LuaStyle/Skills/Skill.py`
2. `CppPackage.makeIt...`
3. `Pybind11Module/Strategy/Skill/pybind_Skill.cpp`
4. `PlayerRole::makeIt...` / `TaskFactoryV2`
5. 具体 Skill 的 `plan()`

这是理解“Python 任务最终怎么在 C++ 里落地”的最快路径。
