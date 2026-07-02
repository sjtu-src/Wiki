# 状态机与角色匹配

这一页是 Python 层里最核心的实现机制说明。

## 你真正应该读的文件

核心入口有四个：

- `RoleMatch_LuaStyle/Task.py`
- `RoleMatch_LuaStyle/State.py`
- `RoleMatch_LuaStyle/StateMachine.py`
- `Algorithm/munkre.py`

绝大多数 NormalPlay / RefPlay，本质上都在调用这套框架。

## `Task` 是什么

`Task` 不是“底层机器人命令”，而是 Python 层对一个角色任务的包装。

它通常包含：

- 一个 Skill 工厂或闭包
- 匹配位置 `matchPos`
- 可选固定车号 `fixedNumber`
- 调试描述

最重要的一点是：

> `Task` 既参与角色匹配，也参与真正执行。

## 为什么 `Task` 里会有“延迟求值”

很多任务会依赖：

- 另一个角色当前车号
- 另一个角色本帧位置
- 匹配完成后的真实 executor

这时就不能在 `Task` 创建的那一刻把所有参数算死。  
所以框架允许你传：

- `lambda: ...`
- `lambda runner: ...`

等延迟求值形式。

## `State` 负责什么

每个 `State` 负责三件事：

1. 生成任务表
2. 给出匹配规则字符串
3. 决定下一状态

`State.run()` 里最关键的一步，是先用当前 `matchPos` 跑匹配，再去真正展开延迟任务。

这也是为什么框架里会维护缓存的 `achedMatchPos`。

## 角色名和车号的关系

当前主流角色名通常是：

- `A/B/C/...`
- `G`：守门员
- `L`：很多脚本里会拿来表示 leader 或关键角色

这些都只是 **角色槽位**，不是固定车号。

真正的车号分配结果，会落在：

- `task.num`
- `Global.roleNumberStructTable`
- `Global.lastRoleNumberStructTable`

上。

## `matchStr` 的设计意义

`matchStr` 不是装饰，而是在表达“哪些角色身份要尽量稳定，哪些角色允许实时漂移”。

这对足球场景很重要，因为：

- 有些角色必须连续，比如 leader / receiver
- 有些角色只要站位合理就行
- 有些角色在状态切换时才应该重分配

如果你把所有角色都做成每帧实时匹配，往往会出现：

- 角色抖动
- 状态机语义不稳定
- 同一意图在场上不断换车执行

## `Global.py` 在这套系统里的角色

`Global.py` 不是“随便放全局变量”的文件，而是角色匹配体系的核心状态中心之一。

它管理的关键内容包括：

- `isYellow / isRight / isSimulation`
- `gameStrategies`
- `currentPlayName / lastPlayName`
- `roleNumberStructTable`
- `goalieNumber`
- 调试与力度模型相关配置

所以你改 `Global` 时要非常清楚自己是在改：

- 启动配置
- 运行时状态
- 还是跨模块共享规则

## 写战术时的经验建议

### 优先显式表达角色意图

宁可让 `getTasks()` 长一点，也尽量把：

- 谁是 leader
- 谁负责 back
- 谁负责 marking

写得明确。

### 尽量把“匹配规则”和“状态跳转规则”分开想

匹配回答的是“谁来做”，状态机回答的是“现在该做什么”。

这两个问题关联很强，但不是同一个问题。

### 先跑通一条最小链路，再复杂化

先写出：

- 一个状态
- 两三个角色
- 一个清晰 `matchStr`
- 一个稳定的 `transFunction()`

再慢慢扩展到完整 11v11，会比一开始就把全部角色和状态堆满靠谱很多。
