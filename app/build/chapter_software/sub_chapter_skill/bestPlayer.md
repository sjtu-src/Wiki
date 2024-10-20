---
layout: default 
title: Best Player

---

> gsh 24.10

## 用途和使用方法

筛选出能够最快速度到达球的车，主要用于防守。

调用时，可以直接在Lua的状态机层调用`task.advance()`, 便可在防守时直接使用bestPlayer计算得出的车,作为advace的一部份。

```Lua
["SW"] = {
    switch = SwitchBallArea,
    Leader = task.advance(), // 球在己方半场时，让BestPlayer成为Leader
    Assister = task.support("Leader",0),
    Middle = task.marking("First"),
    Special = task.leftBack(),
    Defender = task.rightBack(),
    Goalie = task.goalieNew(),
    match = "[L][DS][AM]"
},
```

或者可以在Lua脚本中直接调用`getOurBestChaser()`，返回值为车的编号。（老版的bestPlayer可用`bestPlayer:getOurBestPlayer()`调用）

```Lua
    local robotNum = defenceInfoNew:getOurBestChaser() 
```

## 基本原理

假设球匀速直线运动，车匀最大加速度加速，求得当前车速、球速下，开始加速追球所需的最短时间，再根据相应算法求得最佳车辆。（球的运动已有建模，这里假设匀直为简化计算）

## 变量

1. 车辆加速度

    加速度由参数库`ParamManager`中的`MAX_TRANSLATION_ACC`决定。

    ```cpp
        double MAX_TRANSLATION_ACC = paramManager->MAX_TRANSLATION_ACC;
    ```

2. 确定度
    用来决定是否应当切换为另一个车，防止精度不足时的在两辆车之间的来回切换。目前这个参数并没有移植到外部，需要手动调整。

    ```cpp
        const double certainty = 0.8;//值越低，越不容易切换
    ```

## 实现方法

1. 时间求解：二维运算解得四次方程，取最小正实根。

    ```cpp
    // p，p0 是机器人和球的初始位置，v和v0是机器人和球的速度，a_max是机器人最大加速度
    // v0_double是球的速度的模
    // 追上时纵坐标为0，p.y + v.y*t + 0.5*a.y*t^2 = 0
    // 横坐标为m, p.x + v.x*t + 0.5*a.x*t^2= v0 * t
    //|a|^2= a_max^2
    //  -0.25a * t^4 + (v.x^2 + v.y^2 - 2 v.x * v0 + v0^2) * t^2 - 2 * (p.x * v.x + p.y * v.y ) * t + p.x^2 + p.y^2 = 0
    //
    // 费拉里法计算t
    std::complex<double> t_complex[4];
    Ferrari(t_complex,
            -0.25 * a_max * a_max,
            0,
            (v.x() - v0_double) * (v.x() - v0_double) + v.y() * v.y(),
            2 * (p.x() * (v.x() - v0_double) - p.y() * v.y()),
            p.x() * p.x() + p.y() * p.y());
    ```

    （费拉里法解四次方程比较繁琐，但适用于所有小于等于四次的方程求解，如需复用，可参考`Core/src/ssl/defenceNew/ChaseTime.cpp`中`std::complex<double> Ferrari(...)`）

2. 最优成员筛选。在已知当前所有车到达球最短时间的情况下，对上一轮判断出的最优车辆的时间乘以确定度，保证不会频繁切换。

    ```cpp
    for (const auto &pair : chaseTimeList)
    {
        double nextValue = pair.first == bestChaser ? pair.second * certainty : pair.second; // 如果是上一轮的最优车辆，乘以确定度
        if (nextValue < min_value)
        {
            min_value = nextValue;
            bestNum = pair.first;// 记录本轮最优车辆
        }
    }
    ```

### 结构

#### 类名

`CChaseTimeCalculator`

#### 主要函数

1. `std::complex<double> Ferrari(...)`

    用于解四次方程，返回四个根。

2. `int getOurBestChaser()`

    返回最佳车辆的编号，对外接口。

3. `int CChaseTimeCalculator::ourBestChaser(const CVisionModule *pVision)`

    循环核心，每帧调用，计算出最佳车辆。
