# `Config.py`、`SelectPlay.py` 与 Play 组织方式

## `InitAllModules.py` 负责“一次性初始化”

这个脚本在系统启动时只执行一次，主要做：

- 把项目 `.venv` 的 site-packages 放进 `sys.path`
- 读取 `zss.ini`
- 初始化 `Global` 中的启动参数
- import `Geometry`、`Vision`、`WorldModel`、`Utils`
- import `Config`
- 最后 import `SelectPlay`

你可以把它理解成 Python 侧的 `StartZeus`。

## `Config.py` 负责“注册可用脚本”

`Config.py` 在当前架构里最像原来的 `Config.lua`：

- 设置全局开关
- 选择 NormalPlay
- 注册 RefPlay
- 指定测试脚本
- 固定守门员车号等默认角色规则

其中最重要的是 `Global.gameStrategies` 这张表。

它把字符串名称映射到真实的策略对象，例如：

- `NormalPlay`
- `KickOff`
- `FreeKick`
- `GameStop`
- `BallPlace`

## `SelectPlay.py` 是每帧入口

它每帧都会做这几件事：

1. 读取当前裁判盒消息
2. 判断是否进入 Test Mode
3. 判断是否该跑 RefPlay
4. 否则进入 NormalPlay
5. 在 Play 切换时执行 `ResetPlay()`

所以它本质上是一个 **顶层路由器**。

## `ResetPlay()` 为什么很重要

切换 Play 时，不只是换个脚本名这么简单。  
还需要把很多跨帧状态清掉，例如：

- `worldModel.SPlayFSMSwitchClearAll(True)`
- 角色号表
- 防守信息
- 各种 buffer / timer

如果切换 Play 时不重置这些状态，最容易出现的结果就是：

- 新脚本读到了旧脚本残留状态
- 表现看起来像“随机 bug”

## `Play/` 目录该怎么理解

当前主线可以粗分为三类：

- `Play/Normal/`：正常比赛主战术
- `Play/RefPlay/`：裁判盒相关战术
- `Play/Test/`：实验和测试脚本

这三类不是按“重要程度”分的，而是按“使用场景”分的。

## 一个正常主战术的例子

`Play/Normal/NormalPlayMessi_11vs11_new.py` 是当前很值得认真读的例子。

它会结合：

- `messiDecision`
- `defenceSequence`
- `Task`
- `State`
- `matchStr`

动态组织：

- leader
- receiver
- back
- marking
- goalie

它能很好体现“Python 层到底在管什么”。

## 一个裁判盒脚本的例子

`Play/RefPlay/GameStop.py` 很适合入门 RefPlay：

- 结构清晰
- 状态数量少
- 和裁判盒消息关系直接
- 同时能看到 stop 站位、角色匹配和退出逻辑

## 什么时候改 `Config.py`，什么时候直接改 `Play`

### 改 `Config.py`

适合：

- 切换当前默认 NormalPlay
- 调整测试入口
- 注册新的脚本名字
- 设置默认固定角色号

### 直接改 `Play`

适合：

- 修改某套具体战术逻辑
- 增加状态机状态
- 调整角色匹配规则
- 修改某个裁判盒脚本

简单说：

- `Config.py` 负责“选择用谁”
- `Play/*.py` 负责“具体怎么做”
