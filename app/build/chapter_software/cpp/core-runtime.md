# 运行骨架

## `main.cpp`

`Medusa/src/Main/main.cpp` 的职责很简单：

- 初始化嵌入式 Python 解释器
- 启动 Qt 事件循环
- 开线程执行 `runLoop()`

这一步说明了一个很重要的事实：

> 当前 exe 入口本身就是为 Python-C++ 混合架构准备的，而不是纯 C++ 独立程序。

## `zeus_main.cpp`

这里是真正的主循环骨架，主要包括两部分：

### 1. `runLoop()`

传统 C++ 顶层入口使用它：

- 初始化视觉、决策、动作和其它单例
- 循环执行 `setNewVision -> DoDecision -> sendAction`

### 2. `SystemRunner`

Python 顶层入口使用它：

- `init()`：做一遍和 `runLoop()` 开头类似的初始化
- `preDecision()`：更新视觉、清空上一帧任务
- `postDecision()`：规划任务并发送命令

可以把 `SystemRunner` 理解成“把原本一整个 `runLoop()` 拆成了 Python 可控的两段”。

## `ActionModule`

`ActionModule` 的职责相对稳定：

- 从 `TaskMediator` 取出本帧每台车最终的底层任务
- 转换成真实的机器人控制命令
- 通过无线层发送出去

所以在整体链路里，`ActionModule` 更像是“最后的执行出口”。

## 为什么要保留 `MedusaCore.dll`

当前的设计不是所有逻辑都塞在 exe 里，而是把绝大多数核心代码放进 `MedusaCore.dll`。

这样做带来的直接好处是：

- `Medusa.exe` 可以复用这些逻辑
- `CppPackage.pyd` 也可以复用这些逻辑
- Python 顶层与 C++ 顶层不会各自维护一份分叉实现

对开发者而言，最重要的结论是：

> 真正值得重点看的“核心逻辑”，通常不在 exe 壳子里，而在 `MedusaCore` 参与编译的源码里。

## 读这一层代码时的建议

如果你当前的目标是“理解架构”，不要先陷在每个 Skill 的数学细节里。  
先把这些结构记住：

- 入口：`main.cpp`
- 主循环：`runLoop()` 或 `SystemRunner`
- 决策核心：`CDecisionModule`
- 任务存储：`TaskMediator`
- 执行出口：`CActionModule`

这几个点串起来后，再去深挖单个模块会轻松很多。
