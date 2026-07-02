# 视觉、运动控制与 Skill

## 视觉模块：系统感知入口

`Medusa/src/Vision/VisionModule.h` 对它自己的描述非常准确：

- 接收原始视觉数据
- 做滤波与预测
- 维护球和机器人的世界状态
- 处理裁判盒信息
- 结合下位机反馈修正状态

在高层开发时，你可以把 `VisionModule` 当成：

> “这一帧全场状态的权威来源”

Python 侧大部分 `Vision` 包装，也都是在围绕它工作。

## 视觉层给上层提供了什么

对战术最常用的信息包括：

- `ourPlayer(i)` / `theirPlayer(i)`
- `ball()`
- `getCycle()`
- `getCurrentRefereeMsg()`
- `getBallPlacementPosition()`

这些接口最终也通过 pybind 暴露到了 `CppPackage.VisionModule`。

## Skill 为什么大多写在 C++

因为很多底层行为需要同时满足：

- 高频执行
- 复杂几何与约束处理
- 多障碍避障
- 对实时性敏感

所以 Python 层通常负责“选择哪种 Skill”，而不是自己计算所有细节。

## 一个最值得重点读的 Skill：`SmartGotoPositionV4`

如果你只打算认真读一个底层 Skill，推荐先看：

```text
Medusa/src/Strategy/skill/SmartGotoPositionV4.cpp
```

它基本能体现本队底层技能的典型风格：

- 先读任务参数
- 根据角色类型调整能力上限
- 处理禁区、停球圈、摆球区等规则约束
- 构造障碍物
- 调用路径规划器
- 生成中间点和目标速度
- 最终下发子任务

## 它和运动控制 / 路径规划是什么关系

可以粗略理解为三层：

1. **Skill 层**：决定“我要去哪、按什么规则去”
2. **路径规划层**：决定“避开障碍后走哪条路”
3. **运动控制层**：决定“沿这条路具体怎么加速、转向、跟踪”

在当前代码里，你会看到：

- `Strategy/skill/SmartGotoPositionV4.cpp`
- `PathPlan/RRTPathPlanner...`
- `MotionControl/ControlModel.*`
- `MotionControl/CMmotion.*`

它们共同完成“从战术目标点到实际速度指令”的转换。

## 运动控制层该怎么看

第一次读不建议直接扎进所有数学推导。  
先建立下面的理解：

- `MotionControl/` 负责轨迹和控制模型
- `PathPlan/` 负责空间层面的避障与中间点
- Skill 的 `plan()` 把战术语义翻译成这些模块能处理的参数

也就是说，Skill 更像“上游业务逻辑”，运动控制更像“下游执行引擎”。

## 盯人、防守、接球类 Skill 的共同特点

像这些 Skill：

- `WMarking`
- `WBack`
- `ZAttackV2`
- `Crossover`
- `GetBallV4/V5`

虽然目标不同，但基本都会依赖：

- 当前球和机器人状态
- `TaskMediator` 里的角色标签
- 若干点位计算模块
- 相同的底层运动/避障框架

所以读一个 Skill 时，最好同时关注：

- 它“为什么被选中”
- 它“拿到了哪些输入”
- 它“最后把哪些子任务往下交”

不要只盯着局部公式。
