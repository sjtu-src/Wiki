# 编写新的 Test / Strategy 脚本

这一页专门回答一个很实际的问题：当你已经看懂现有框架后，如果想自己加一份新的脚本，应该放在哪里、按什么结构写、最后又怎么注册到系统里？

这里故意把 `Test` 和正式 `Strategy` 放在同一页讲，是因为它们底层用的是同一套状态机和 Skill 框架；真正不同的，主要是“脚本放在哪个目录”和“谁来选中它”。

## 第一步先别写代码，先决定它属于哪一类

当前 `Play/` 目录按触发场景分成三类：

- `Play/Test/`：调试、实验、Benchmark、单项验证；
- `Play/Normal/`：正常比赛主战术；
- `Play/RefPlay/`：裁判盒驱动的脚本。

这个分类非常重要，因为它决定了后面谁会调用你的脚本。

如果你只是想验证某个 Skill、某个跑位、某种配合关系是否可行，优先写进 `Play/Test/`。这样最灵活，也最不容易误伤比赛主线。

如果你想写的是“常规比赛时默认使用的一套 11v11 策略”，就应该放进 `Play/Normal/`。

如果你写的是“我方开球”“对方点球”“GameStop 摆阵”这种由裁判盒消息直接触发的逻辑，那它就属于 `Play/RefPlay/`。

## 一个最小 Test 脚本长什么样

`Play/Test/Test_Run11.py` 是非常好的入门模板。它清楚地展示了最基本的写法：先写若干 `State`，再用 `@declare_state_machine(...)` 把它们组装成一个状态机类。

你完全可以用下面这个骨架起步：

```python
from typing import override

from Geometry import *
from RoleMatch_LuaStyle.State import State
from RoleMatch_LuaStyle.StateMachine import declare_state_machine, StateMachine
from RoleMatch_LuaStyle.Task import Task
from RoleMatch_LuaStyle.Skills import Skill


class DemoState(State):
    @override
    def getMatchString(self) -> str:
        return "[LA]"

    @override
    def getTasks(self) -> "dict[str, Task]":
        return {
            "L": Task(Skill.RushTo(CGeoPoint(1000, 0), 0)),
            "A": Task(Skill.RushTo(CGeoPoint(0, 1000), 0)),
            "G": Task(Skill.Goalie()),
        }

    @override
    def transFunction(self) -> str:
        return ""


@declare_state_machine(DemoState)
class Test_Demo(StateMachine):
    pass
```

这段骨架的意义不在于“功能强”，而在于它清楚展示了最小必要结构：状态、任务字典、匹配规则和状态机声明。

## 正式 Strategy 和 Test 的写法，本质上没有换框架

很多新人会以为 Test 和正式比赛脚本是两套体系，其实不是。无论你写的是 `Test_Run11` 这种实验脚本，还是 `NormalPlayMessi_11vs11_new` 这种正式主战术，底层都还是：

- `State`
- `Task`
- `matchStr`
- `StateMachine`

真正的区别更多在于：

- Test 脚本往往会固定车号、固定目标点，更强调“验证一个点”；
- 正式 Strategy 更依赖 `messiDecision`、`defenceSequence`、裁判消息和角色稳定性，更强调“整队在比赛中的持续运行”。

所以写新脚本时，不要先想着“我要不要换一种框架”，而是先想“我现在是在做验证，还是在做比赛主线”。

## 脚本写完之后，怎么让系统真的跑到它

这一步才是很多人最容易卡住的地方。文件写好只是第一半，后面还有“把它注册到顶层调度里”这一半。

### 如果是 Test 脚本

最直接的方式，是在 `Config.py` 里：

1. `import` 你的新脚本类；
2. 把 `testStrategy` 改成它。

例如：

```python
from Play.Test.Test_Demo import Test_Demo

testStrategy = GameStrategy(Test_Demo())
```

然后在启动时打开 `Global.isTestMode`，或者直接使用 `main.py --test-mode` 之类入口，让 `SelectPlay.py` 优先走 Test 路由。

### 如果是新的 NormalPlay

你需要在 `Config.py` 里：

1. `import` 你的 `Play/Normal/*.py` 中的状态机类；
2. 在 `Global.gameStrategies` 里把 `NormalPlay` 指向新的实例，或者新增一个新 key。

例如：

```python
from Play.Normal.MyNewNormalPlay import MyNewNormalPlay

Global.gameStrategies["NormalPlay"] = GameStrategy(MyNewNormalPlay())
```

如果你只是想短期切换默认主战术，这已经够了。

### 如果是新的 RefPlay

这一步比前两种稍微多一层，因为 RefPlay 不只是注册，还要能被裁判盒消息映射到。

你通常需要：

1. 在 `Config.py` 里导入并注册一个新 key；
2. 在 `GameControl/Referee.py` 里，把某种裁判消息映射到这个 key。

比如现在 `OurBallPlacement -> BallPlace`、`TheirKickOff -> KickOffDef` 就是这样做的。如果你新增了新的裁判脚本，但忘了补 `Referee.py`，那系统即使知道这个类存在，也不会自动跑到它。

## `Config.py` 注册的其实不只是“文件名”

这一点一定要注意。`Config.py` 里注册的通常不是字符串文件名，而是已经实例化好的状态机对象，或者 `GameStrategy(...)` 包装后的对象。也就是说，注册动作本质上是在告诉系统：

> 这个名字对应的，不是一份源码文件，而是一套已经可以 `runStrategy()` 的顶层策略实例。

所以当你读 `Global.gameStrategies["NormalPlay"] = GameStrategy(...)` 时，脑子里不要把它想成“配置文件字符串映射”，而要把它想成“真正要跑的对象注册表”。

## 新脚本第一次起步时，建议用这条最小路线

如果你想尽快验证一份新脚本能不能通，最推荐的路径通常是：

1. 先写到 `Play/Test/`；
2. 状态数量尽量少，先一个状态也行；
3. 先只放 2 到 3 个角色，别一上来就全队铺满；
4. 在 `Config.py` 里把 `testStrategy` 指向它；
5. 用 Python 顶层模式跑起来，先看任务能否正常下发；
6. 再逐步增加角色、状态和复杂匹配。

这样做的好处是你能很快区分：问题是出在框架没接通，还是出在战术逻辑本身太复杂。

## 正式写比赛脚本时，几个经验很有用

第一个经验，是优先显式表达角色意图。不要一上来就搞一堆隐式副作用和跨模块共享变量，先把 `L/A/B/G` 这些角色在状态里写清楚。

第二个经验，是先把 `matchStr` 想清楚，再写复杂 Skill。很多时候不是 Skill 不对，而是角色漂移太厉害导致整套逻辑根本不稳定。

第三个经验，是先做“能稳定跑”的版本，再做“很聪明”的版本。尤其在 Test 脚本里，这点非常重要。一个最小但稳定的脚本，往往比一个一上来就追求复杂联动却满是隐患的脚本更有价值。

## 这一页想让你建立的工作流感

写新脚本这件事，最好在脑子里一直翻译成下面这句话：

> 先决定脚本属于 Test、Normal 还是 RefPlay；再按 `State -> Task -> StateMachine` 的框架把它写出来；最后把它注册到 `Config.py` 和必要的顶层映射里。

只要这条流程顺了，后面不管你是想加一个简单 Test，还是逐步做成新的比赛主战术，都会有很明确的下手路径。
