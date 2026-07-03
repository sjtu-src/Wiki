# Skill.py 与任务包装

`RoleMatch_LuaStyle/Skills/Skill.py` 是当前 Python 战术层里非常值得理解的一层。它看起来像一堆零散函数，但它真正做的事情，其实是把“Python 战术意图”翻译成“C++ 能执行的任务入口”。

## 先说一句最准确的话

`Skill.py` 里的函数，通常并不是直接执行某个动作，而是返回一对东西：

1. `skill_cpp(executor)`：真正把任务送进 C++ 的函数；
2. `matchPos(executor)`：角色匹配时要用的参考位置。

所以当你写：

```python
Task(Skill.RushTo(target, angle))
```

你拿到的并不是“已经开始跑的机器人命令”，而是一个**任务工厂**。真正执行要等角色匹配完成、框架把真实车号 `executor` 分下来之后，才会发生。

## 为什么这一层存在得这么必要

因为 Python 顶层战术和 C++ Core 的关注点完全不同。

Python 层想表达的是：

- 这个角色要去哪个点；
- 到点时身体大概朝哪个方向；
- 是否需要吸球；
- 这个任务匹配时应该参考哪里；
- 这个角色是否应该注册成 `leader`、`goalie`、`back` 等身份。

而 C++ 层真正需要的是：

- `executor` 车号；
- 一份 `TaskT` 参数包；
- 一个具体的 `makeIt...` 入口；
- 以及本帧在 `TaskMediator` 里的角色标签。

`Skill.py` 正是负责把前者整理成后者的那一层。

## 读 `Skill.py` 时，先抓它的共同结构

绝大多数包装函数都长得很像。以 `RushTo` 为例，它大体会做三件事：

1. 先把 Python 战术层想表达的参数收进闭包里；
2. 在 `skill_cpp(executor)` 中把这些参数翻译成对 `CppPackage.makeIt...` 的调用；
3. 在 `matchPos(executor)` 中返回一个用于 Munkres 匹配的参考点。

这个结构看懂以后，后面再看 `Goalie`、`WBack`、`WMarking`、`Shoot`、`GoAndTurnKick` 这些函数，就不会觉得它们只是“风格不同的普通函数”，而会意识到它们都在做同一类工作。

## 一个简单例子：`SimpleGoTo`

`SimpleGoTo(point, angle=0, flag=0)` 是最直观的包装之一。它基本没有复杂角色语义，就是：

- `skill_cpp(executor)` 里调用 `CppPackage.makeItSimpleGoTo(executor, point, angle, flag)`；
- `matchPos(executor)` 直接返回 `point`。

这种包装很适合入门，因为它几乎没有“延迟参数”“角色注册”“多阶段逻辑”这些干扰项。

## 一个更典型的例子：`Goalie`

`Goalie()` 就比 `SimpleGoTo()` 更接近真实比赛语义了。它不仅会调用 `CppPackage.makeItGoalie(...)`，还会先做：

```python
taskMediator.registerRole(executor, "goalie")
CppPackage.TaskMediator.Instance().registerRole(executor, "goalie")
```

这两步的意义是把“这台车本帧是守门员”这个身份同时告诉 Python 和 C++ 两侧。这样到了 C++ 底层，`SmartGotoPositionV4`、禁区逻辑、能力上限选择等模块，才能正确识别它的特殊身份。

也就是说，`Skill.py` 不只是转发参数，它还在帮系统同步角色语义。

## `matchPos` 为什么不是附带小功能

很多人第一次写新 Skill 时，只盯着 `skill_cpp()`，会下意识觉得 `matchPos()` 随便返回个点也无所谓。但实际上它会直接影响 Munkres 的分配结果。

比如：

- `RushTo(...)` 往往把目标点本身当作 `matchPos`；
- `WMarking(...)` 会通过 C++ 侧函数动态算出更合适的盯人参考点；
- `Goalie()` 一般返回己方球门；
- `Crossover(...)` 这种更复杂的任务，匹配参考点甚至可能来自 `WeBestGetBallPosition(...)`。

所以 `matchPos` 不是锦上添花，而是角色匹配语义的一部分。一个包装函数如果 `matchPos` 设计得很随意，脚本表面上也许能跑，但整队角色分配会变得很奇怪。

## 为什么很多函数会支持 `callable` 参数

`RushTo`、`Shoot`、`StaticGetBallV4` 这类函数里，经常会允许你传一个闭包进来，而不是立即求值的常数。例如朝向参数 `angle`、`direction` 有时会传入一个依赖真实 `executor` 的函数。

这背后的理由跟状态机框架是一致的：在还没完成角色匹配之前，很多值本来就不应该被算死。于是包装层会把这类参数延后到 `skill_cpp(executor)` 真正执行时再解包，这样语义才对。

## `Skill.py` 里常见的几类包装

从使用场景看，当前包装大致可以分成几类：

### 1. 纯跑位 / 站位类

例如：

- `SimpleGoTo`
- `RushTo`
- `RushToV4`
- `SmartGoTo`

这类包装通常重点在目标点、目标朝向、速度和标志位。

### 2. 防守职责类

例如：

- `WBack`
- `WBackSide`
- `WMarking`
- `WDrag`

它们除了要把参数传给 C++，往往还会通过 `registerRole()` 告诉系统“这台车现在是 back / marking / drag 角色”。

### 3. 处理球类

例如：

- `Shoot`
- `GoAndTurnKick`
- `TurnAndShoot`
- `GetBallV4/V5`
- `StaticGetBallV4`

这类包装最容易引入延迟参数、吸球逻辑、自动算力度或精度控制。

## `Shoot()` 这类函数为什么看上去很“聪明”

像 `Shoot()` 这种包装，已经不只是简单转发参数了。它会先根据当前场上状态决定：

- 是否已经对准射门方向；
- 是否该打开 dribble；
- 是该平射还是挑射；
- 如果没传力度，是否用 `PowerCalculator.evalPower(...)` 自动估计。

也就是说，某些 Python 包装本身已经带有明显的“轻逻辑层”意味。它们并没有取代 C++ Skill，但确实会在把任务交下去之前，先做一些更贴近战术语义的处理。

## 写新的 Python 包装时，建议按这个模板思考

如果你准备把一个 C++ 能力包装成 `Skill.py` 里的新函数，推荐按下面这个顺序想：

1. Python 使用者最希望怎么调用它；
2. `matchPos` 应该返回什么，才能让 Munkres 分配得合理；
3. 这个角色是否需要在 `TaskMediator` 里注册身份；
4. 参数里哪些可以立即算，哪些应该延迟到拿到 `executor` 后再算；
5. 最终该调用哪个 `CppPackage.makeIt...` 接口。

可以先从一个很小的骨架开始：

```python
def MySkill(target, flag=0):
    def skill_cpp(executor: int):
        return CppPackage.makeItMySkill(executor, target, flag)

    def matchPos(executor: int):
        return target

    return skill_cpp, matchPos
```

然后再逐步加入更复杂的角色注册、延迟参数和辅助逻辑。

## 写这层代码时最容易踩的坑

第一个坑，是在函数默认参数里直接放运行时依赖值。`Skill.py` 文件开头其实已经特地提醒过：Python 默认参数是在函数定义时求值一次，不像 C++ 一样是每次调用重新求值。所以那些依赖球位置、朝向、动态决策结果的默认值，最好在函数体里再算。

第二个坑，是只写 `skill_cpp` 不认真设计 `matchPos`。这样最典型的结果就是底层 Skill 没毛病，但 Munkres 分配出来的执行者总感觉“不对劲”。

第三个坑，是忘了这层包装最终是要跟 `Task.py`、`State.py` 和 `TaskMediator` 协作的。`Skill.py` 不是独立工具箱，它是当前整个顶层战术框架的一部分。

## 这一页的落点

读完这一页后，你最好能把 `Skill.py` 里的函数理解成一句非常具体的话：

> 它们不是普通辅助函数，而是“把 Python 战术意图包装成标准任务接口，再把它送进 C++ Core”的翻译层。

带着这个视角回去看源码，你会发现 `Skill.py` 的很多设计看起来就顺理成章了。
