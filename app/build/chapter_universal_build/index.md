---
icon: material/router-wireless
---

# 实车调试流程



## 涉及软件
!!! success
    软件运行的基本原理分为视觉处理、局势判断、生成判罚

    - 视觉处理：接收裸视觉，经过卡尔曼滤波等处理得出更为准确的位置、速度信息
    - 局势判断：接收裁判指令（Halt、Stop……），结合视觉得出当前场上形势
    - 根据规则判断有无犯规行为

- rbk(core)：控制程序，负责决策，判断场上局势，发布运动指令
- owl2：可视化工具，处理视觉以得到更为准确的位姿，同时显示辅助调试的信息
- grSim(src-simulation)：仿真器，可提供仿真环境下的相机视觉（裸视觉）、机器人反馈等信息
- ssl-vision：视觉机，官方推荐使用，在实车模式中提供相机视觉
- 裁判盒：发送裁判指令（Halt、Stop……），包括owl2自带的和GC

## 调试流程

``` mermaid
graph LR
  A(启动视觉机) --> B{外部软硬件准备};
  C(机器人拨码) --> B;
  D(裁判盒) -->|可选| B;
  E(内部代码就位) --> F(启动 core 控制机器人)
  B --> F
  click A 视觉机.md
```



[:fontawesome-solid-circle-info:{ .lg .middle} 了解更多](https://sjtu-src.github.io/Wiki){ .md-button .md-button--primary}