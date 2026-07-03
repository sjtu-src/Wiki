# `Config.py`、`SelectPlay.py` 与 `gameStrategies`

如果说 `SelectPlay.py` 是顶层路由器，那么 `Config.py` 就是它背后的路由表。很多新人刚接触这套代码时，会先去翻 `Play/` 目录里的具体脚本，结果越翻越容易糊涂，因为你会看到好多 `NormalPlay`、`RefPlay`、`Test` 文件，却不知道系统到底是怎么“选中它们”的。理解这页之后，这件事就会清楚很多。

## `InitAllModules.py` 负责把舞台先搭好

Python 层真正开始工作前，首先会跑 `InitAllModules.py`。这个脚本只执行一次，但作用很重：它会把 `.venv` 的包路径、`zss.ini` 里的配置、`Global` 里的启动参数，以及 `Geometry / Vision / WorldModel / Utils / Config / SelectPlay` 这些关键模块全都拉起来。

你可以把它理解成 Python 版的“总初始化入口”。它不负责每帧做决策，但它决定了后面的决策模块能不能正常工作。如果这里路径、解释器或者配置没对齐，后面很多看似奇怪的错误其实都是从这里埋下的。

## `SelectPlay.py` 每帧到底在决定什么

`SelectPlay.SelectPlay()` 的逻辑并不复杂，但它的位置极其关键。它每帧都会先读取当前裁判盒消息，然后按下面这个顺序做判断：

1. 如果 `Global.isTestMode` 为真，直接进入 `testStrategy`；
2. 否则，如果当前裁判消息属于 RefPlay 范围，交给 `GameControl/Referee.py` 去映射；
3. 如果某个 RefPlay 还没跑完，即使裁判消息已经切回普通状态，也允许它再续跑一段；
4. 如果前面都不是，就回到 `Global.gameStrategies["NormalPlay"]`。

所以这份文件本质上不是“写战术”的地方，而是“决定当前到底该用哪套战术”的地方。你如果把它看成顶层 dispatch，就会很自然。

## `ResetPlay()` 为什么不是可有可无的小函数

很多人第一次看 `SelectPlay.py` 会觉得 `ResetPlay()` 只是做点清理工作，但它其实是整套系统稳定性的关键。因为 Play 一旦切换，必须把上一套脚本在世界模型里留下的跨帧状态清掉，比如：

- `worldModel.SPlayFSMSwitchClearAll(True)` 相关缓存；
- `Global` 里的角色号表；
- 防守模块里的标记信息；
- 各类 buffer condition 和计时器。

不做这一步，最常见的后果不是直接报错，而是出现那种最烦人的“看起来像随机 bug”的现象：脚本明明已经切了，可场上角色还带着上一套战术的身份和历史状态在跑。

## `Config.py` 负责“注册这套系统有哪些可用策略”

当前 `Config.py` 的作用很像以前的 `Config.lua`，但它现在承担的事情更清楚也更集中：

- 设置顶层全局开关；
- 指定默认 NormalPlay；
- 注册所有 RefPlay 的策略对象；
- 指定 Test 模式入口；
- 固定守门员或其他默认角色号。

这里面最核心的数据结构就是 `Global.gameStrategies`。你可以把它看成一张“字符串名称 -> 真实策略对象”的映射表。`SelectPlay.py`、`GameControl/Referee.py` 以及其他顶层流程，最终都会回到这张表里找对象并调用 `runStrategy()`。

## `GameStrategy` 这个小包装类在干什么

`Config.py` 里先定义了一个 `GameStrategy` 类，它表面上很轻量，但作用很实用。它允许你给蓝方和黄方分别指定不同策略对象：

```python
GameStrategy(blueTeamStrategy, yellowTeamStrategy)
```

如果只传一个对象，那蓝黄双方默认共用同一套策略。`runStrategy()` 内部再根据 `Global.isYellow` 选择究竟跑哪一个实例。

这层包装的意义是：你在注册策略时不必把“颜色选择”逻辑散落到各个 Play 里，而是统一留在这一层处理。对长期维护来说，这个边界非常舒服。

## `Global.gameStrategies` 里每个条目大概都是什么意思

下面这张表对应的是当前 `Config.py` 里能直接看到的主策略条目。它不是把源码逐行翻译成中文，而是帮你建立“这些 key 在系统里分别扮演什么角色”的直觉。

| key | 当前默认脚本 | 主要用途 |
| --- | --- | --- |
| `NormalPlay` | `Messi_11vs11_new()` | 常规比赛主战术，裁判盒不接管时的默认入口 |
| `KickOff` | `RefPlay.KickOff()` | 我方开球或接近开球状态 |
| `KickOffDef` | `RefPlay.KickOffDefend()` | 对方开球时的防守脚本 |
| `FreeKick` | `RefPlay.DirectKick_2025_Middle()` | 通用定位球入口，当前偏向我方执行型脚本 |
| `FreeKickDef` | `RefPlay.FreeKickDefend()` | 定位球防守入口 |
| `ourDirectKick` | `RefPlay.DirectKick_2025_Middle()` | 我方直接任意球 |
| `ourIndirectKick` | `RefPlay.DirectKick_2025_Middle()` | 我方间接任意球 |
| `theirDirectKick` | `RefPlay.FreeKickDefend()` | 对方直接任意球防守 |
| `theirIndirectKick` | `RefPlay.FreeKickDefend()` | 对方间接任意球防守 |
| `PenaltyKick` | `RefPlay.PenaltyKickV3_CornerKick()` | 我方点球脚本 |
| `theirPenaltyKick` | `RefPlay.PenaltyDefend()` | 对方点球防守 |
| `BallPlace` | `RefPlay.BallPlace()` | 我方摆球 |
| `TheirBallPlace` | `RefPlay.TheirBallPlace()` | 对方摆球时的站位与避让 |
| `TimeOut` | `RefPlay.OurTimeout()` | 我方暂停 |
| `GameStop` | `RefPlay.GameStop()` | stop 状态下的停球与重摆阵 |
| `GameHalt` | `RefPlay.GameHalt()` | halt 状态下的彻底停机 |
| `IfHalfField` | `False` | 顶层配置开关，不是一个状态机脚本 |
| `USE_ZPASS` | `False` | 顶层配置开关，不是一个状态机脚本 |

这里有两个容易忽视的小点。

第一，`GameControl/Referee.py` 里真正接收到的裁判盒消息，并不总和 `gameStrategies` 里的 key 同名。例如 `OurBallPlacement` 最终会映射到 `BallPlace`，`TheirKickOff` 会映射到 `KickOffDef`。所以如果你新增一个 RefPlay，不只要在 `Config.py` 注册，还要看是否需要补 `Referee.py` 的映射。

第二，表里不只有“真策略”，还混着少数布尔配置，例如 `IfHalfField` 和 `USE_ZPASS`。因此读这张表时不要默认每个 key 都是状态机类实例。

## Test 模式和 Normal / RefPlay 是并行入口，不是附属功能

`Config.py` 里除了 `Global.gameStrategies` 之外，还有一行经常被忽视：

```python
testStrategy = GameStrategy(Test_Run11())
```

这意味着 Test 模式不是临时 if 一下某个脚本路径，而是跟 NormalPlay / RefPlay 一样，被当作一条正式入口维护。只要 `Global.isTestMode = True`，`SelectPlay.py` 就会优先走这里。

这设计很实用，因为它让 Test 脚本也能共享同一套状态机框架、同一套 `Skill.py` 包装和同一套 C++ Core，而不是另起炉灶写一套“只给测试用”的简化体系。

## `Play/` 目录怎么理解才不容易迷路

当前主线可以简单分成三类：

- `Play/Normal/`：正常比赛主战术；
- `Play/RefPlay/`：由裁判盒消息触发的脚本；
- `Play/Test/`：开发、实验、Benchmark 和单项验证脚本。

这三类不是按“重要程度”分的，而是按“触发场景”分的。`Test` 不代表不重要，`RefPlay` 也不代表只是附属逻辑。它们都在同一个顶层调度框架里，只是入口条件不同。

## 什么时候改 `Config.py`，什么时候直接改 `Play`

这个判断标准其实很简单：如果你改的是“这套系统应该选谁”，就去改 `Config.py`；如果你改的是“某套具体战术自己该怎么做”，就去改 `Play/*.py`。

适合改 `Config.py` 的典型场景有：

- 切换当前默认 `NormalPlay`；
- 换一个 `testStrategy`；
- 新增一个可被顶层调度选中的策略名；
- 固定守门员或其他默认角色编号。

适合直接改 `Play` 的典型场景有：

- 修改某个状态里的任务逻辑；
- 增加或删除状态；
- 改角色匹配规则；
- 调整某个 RefPlay 的退出条件或站位生成方式。

## 读这套顶层分发代码时，建议先建立一个很实用的脑图

建议你把这部分代码一直翻译成下面这句口语：

> `Config.py` 先告诉系统“我有哪些策略可以选”；`SelectPlay.py` 每帧再根据测试模式、裁判盒和运行状态决定“这一帧该选谁”。

当你能这样去看时，`Global.gameStrategies`、`testStrategy`、`runRefPlay()` 这些东西就不会再像零散配置，而会变成一张很好理解的调度地图。
