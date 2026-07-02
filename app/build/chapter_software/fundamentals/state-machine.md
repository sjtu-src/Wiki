# 状态机

## 先说结论

SRC 现在的软件里，状态机不是“一个课本概念”，而是 **顶层战术的主组织方式**。

Python 层最重要的几个目录：

- `Play/`
- `RoleMatch_LuaStyle/State.py`
- `RoleMatch_LuaStyle/StateMachine.py`

它们共同决定了“这一帧球队处于什么战术状态、每台车拿到什么任务、下一帧怎么跳转”。

## 一个状态机在这里长什么样

最核心的抽象有三个：

- `Task`：一个角色当前要执行的任务
- `State`：某个战术状态下，所有角色任务的定义
- `StateMachine`：负责在状态之间切换

每个 `State` 主要回答三件事：

1. `getTasks()`：这一状态下各角色应该做什么
2. `getMatchString()`：这些角色怎么进行角色匹配
3. `transFunction()`：下一帧是否切换状态，切到哪一个

## 在本项目里的运行顺序

以 `State.run()` 为核心，一帧里大体会做：

1. 生成任务表 `tasks`
2. 根据 `matchStr` 和 Munkres 算法给角色分配真实车号
3. 对需要延迟求值的任务做解包
4. 执行每个任务，把底层 Skill 下发到 C++
5. 记录调试信息和上一次匹配位置
6. 调用 `transFunction()` 决定下一个状态

这也是为什么状态机不是“只管跳转”，它实际上把 **任务生成、角色匹配、调试显示、状态切换** 都串在了一起。

## `transFunction()` 返回值怎么理解

常见返回情况有三种：

- 返回另一个状态名：发生状态切换
- 返回空字符串：留在当前状态
- 返回 `exit`：常见于某些 RefPlay，表示这个脚本应当退出

这套约定在 `RoleMatch_LuaStyle/StateMachine.py` 里有明确实现。

## 例子：为什么 `GameStop` 很适合写成状态机

`Play/RefPlay/GameStop.py` 就是个很典型的例子：

- `Stop` 状态：先让所有角色停下来
- `Run` 状态：按裁判盒约束和场上位置重新分配 stop 站位
- `play_switch()`：决定什么时候继续维持、什么时候退出

如果不用状态机，这种逻辑很容易变成一个充满 `if/else` 的大函数。

## 例子：为什么 `Messi_11vs11_new` 也适合写成状态机

`Play/Normal/NormalPlayMessi_11vs11_new.py` 里，最核心的是两个状态：

- `GetBall`
- `Pass`

看起来只有两个状态，但每个状态内部都会：

- 根据 `messiDecision` 和 `defenceSequence` 生成任务
- 重新组织角色匹配字符串
- 控制 leader / receiver / back / marking / goalie 的分工

所以这里的“状态少”不代表“逻辑简单”。

## 写状态机时最容易踩的坑

### 1. 误把“角色名”和“真实车号”当成一回事

`A/B/C/.../G/L` 这些是角色名，不是车号。

真正车号通常要等角色匹配完成后，才能从：

- `task.num`
- `Global.getRoleNumber(roleName)`

里拿到。

### 2. 过早求值

如果任务里依赖“另一个角色当前的真实位置/车号”，就不能在任务刚创建时立刻求值，否则会发生：

- 还没匹配好角色
- 你却已经把错误的车号写死了

这也是 `Task` 里会有延迟计算和 `achedMatchPos` 缓存的原因。

### 3. 隐式复用上一个状态的任务

当前实现的设计取向是：

> 每个状态尽量显式地把这一帧要做的事说清楚，而不是偷偷沿用上一次残留任务。

这样虽然写起来更啰嗦一些，但长期维护更安全。
