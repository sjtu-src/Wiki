# 运行时主流程

这一页讲最关键的一件事：

> 从程序启动，到机器人收到指令，一帧里到底发生了什么？

## C++ 顶层模式

如果是 `Medusa.exe` 作为顶层入口，主流程在：

- `Medusa/src/Main/main.cpp`
- `Medusa/src/Main/zeus_main.cpp`
- `Medusa/src/Main/DecisionModule.cpp`

### 启动阶段

`main.cpp` 做的事很少，但很关键：

1. 创建 `pybind11::scoped_interpreter`
2. 启动 Qt 事件循环
3. 开线程执行 `runLoop()`

这意味着哪怕是“C++ 顶层模式”，Python 解释器也已经先在进程里启动了。

### `runLoop()` 初始化

`zeus_main.cpp` 里的 `runLoop()` 会依次初始化：

1. 单例和参数系统
2. `COptionModule`
3. `CVisionModule`
4. `CDecisionModule`
5. `CActionModule`
6. 裁判盒接口
7. `ZGetBestUtils` / `ZBestPosCalculate`，或可选的 `ZCUDAModule`

然后进入无限循环：

```text
vision->setNewVision()
decision->DoDecision(false)
action->sendAction()
debug send
```

## `DoDecision()` 一帧里做什么

`DecisionModule.cpp` 里一帧的核心顺序是：

1. `vision_to_decision.Wait()`
2. `TaskMediator::cleanOldTasks()`
3. `calculateModuleRun()`
4. `GenerateTasks()`
5. `PlanTasks()`
6. 通知 Action 层可以发包

其中最容易忽略的两步是：

- `calculateModuleRun()`：先更新大量中间决策模块和点位计算模块
- `PlanTasks()`：把已经分配好的高层任务进一步递归规划成底层可执行任务

## Python 是在哪一步介入的

在 `GenerateTasks()` 里，`DoTeamMode()` 会根据配置的脚本语言决定：

- 跑 Lua
- 还是调用 Python 的 `SelectPlay.SelectPlay()`

当前主线默认就是 Python：

- `DecisionModule` 初始化时执行 `InitAllModules.py`
- 只 import 一次 `SelectPlay`
- 每一帧反复调用 `selectPlayModule.attr("SelectPlay")()`

## Python 顶层模式

如果直接运行：

```powershell
cd ZBin
python PythonScripts/main.py --team blue --side right --sim
```

那么主流程会改成：

1. Python 改写 `zss.ini` 中的关键启动参数
2. `CppPackage.SystemRunner.Instance().init()`
3. 循环里执行：

```python
systemRunner.preDecision()
SelectPlay.SelectPlay()
systemRunner.postDecision()
```

这里的 `SystemRunner` 本质上就是把 `runLoop()` 拆成了“前半帧”和“后半帧”：

- `preDecision()`：更新视觉、清空旧任务
- Python 中间层：决定本帧任务
- `postDecision()`：规划任务、发包、发送 debug

## 为什么 `preDecision()` 和 `postDecision()` 必须成对

这是 Python 顶层模式里最重要的约束之一。

原因是：

- `preDecision()` 只做了前半帧的准备工作
- 真正的任务规划和发包在 `postDecision()` 里

如果你漏掉其中一个，系统状态就会不一致，轻则本帧不动，重则调试行为完全失真。

## 推荐的读源码顺序

第一次顺着主流程看代码，建议按下面顺序：

1. `main.cpp`
2. `zeus_main.cpp`
3. `DecisionModule.cpp`
4. `InitAllModules.py`
5. `SelectPlay.py`
6. 一个具体 `Play`
7. `RoleMatch_LuaStyle/State.py`
8. `RoleMatch_LuaStyle/Skills/Skill.py`
9. `Pybind11Module/Strategy/Skill/pybind_Skill.cpp`
10. 对应的 C++ Skill 源码

这样你能完整走通一条“从顶层决策到真实执行”的链路。
