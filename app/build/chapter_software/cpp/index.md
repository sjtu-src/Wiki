# C++ Core

如果把 Python 看成“战术指挥层”，那 C++ 就是整个系统的 **实时内核**。

新人看 C++ 层时，最容易迷路的原因是文件太多。  
建议先建立下面这张地图：

| 模块 | 目录 | 主要职责 |
| --- | --- | --- |
| 程序入口 | `Medusa/src/Main/` | 启动、主循环、Decision、Action、TaskMediator |
| 视觉 | `Medusa/src/Vision/` | 接收视觉、预测、裁判盒状态、世界模型基础输入 |
| 策略 Skill | `Medusa/src/Strategy/skill/` | 各类底层技能的 `plan()` 逻辑 |
| 运动控制 | `Medusa/src/MotionControl/` | 轨迹、控制模型 |
| 路径规划 | `Medusa/src/PathPlan/` | 避障、RRT 等路径规划 |
| 点位/辅助决策 | `Medusa/src/Algorithm/`、`PointCalculation/` | 传球点、进攻/防守信息等 |
| Python 绑定 | `Medusa/src/Pybind11Module/` | 暴露给 `CppPackage` 的接口 |
| 可选 CUDA | `Medusa/src/CUDAModule/` | GPU 加速实验模块 |

建议先看：

1. `运行骨架`
2. `DecisionModule 与 TaskMediator`
3. `视觉、运动与 Skill`
4. 最后再看 CUDA 和其它扩展
