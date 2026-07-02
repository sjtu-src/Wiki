# `Global`、`Vision`、`WorldModel` 与常用工具

## 这一层解决的是什么问题

写战术时，你几乎每几行就会需要：

- 球和机器人的位置
- 某个角色到球的方向
- 某个条件是否成立
- 某个目标点在哪里
- 应该给多少力度

这些东西如果全都直接调用 C++ 原始接口，战术脚本会很难读。  
所以 Python 层专门做了一层常用包装。

## `Vision/`

这是最常用的感知包装层之一，核心职责是把：

- `CppPackage.VisionModule`
- 各种 `ourPlayer / theirPlayer / ball`

包装成更适合 Python 战术脚本直接调用的形式。

常见用法包括：

- `Ball.pos()`
- `Player.Pos(role)`
- `Player.toBallDir(role)`
- `vision.getCycle()`

## `WorldModel/`

这一层更偏“战术工具箱”，常见子模块有：

- `Positions.py`：常用点位
- `Directions.py`：方向计算
- `Conditions.py`：条件判断
- `Flags.py`：任务标志位
- `PowerCalculator.py`：统一力度入口

最值得记住的一条规则是：

> 写高层脚本时，优先用 `WorldModel` 里整理好的接口，而不是每次都从零拼几何逻辑。

## `Global.py`

除了角色匹配状态，`Global.py` 还承担了很多“全局配置中心”的角色，例如：

- `isTestMode`
- `isDebugMode`
- `powerBackend`
- `powerCurveFile`
- `goalieNumber`

因此它有两个特点：

- 很方便
- 很容易被滥用

建议是：把真正稳定的全局配置放这里，把只对单一战术局部生效的变量留在 Play 自己内部。

## `BufferedCondition`

很多场上条件不适合看“一帧真或假”，而更适合看：

- 连续若干帧是否成立
- 某个条件是否维持了一段时间

`Utils/BufferedCondition.py` 就是为这种需求准备的。  
它能显著减少因为单帧噪声导致的状态机抖动。

## 哪些接口是主线，哪些更像兼容层

当前推荐主线：

- `Vision.*`
- `WorldModel.Positions / Directions / Conditions`
- `PowerCalculator.evalPower()`

仍然保留但带有迁移兼容意味的内容：

- 一些旧 Lua 同名别名
- `KickPower_*` / `ChipPower_*` 兼容接口
- 带有历史命名痕迹的 wrapper

如果你在写新代码，优先选择新的统一入口。

## 一个实用建议

当你觉得某个脚本里几何计算越来越乱时，先别急着继续堆逻辑。  
先想一件事：

> 这是不是应该被提炼到 `WorldModel/` 里，成为一个可复用的战术工具函数？

这样后面整套脚本都会更容易维护。
