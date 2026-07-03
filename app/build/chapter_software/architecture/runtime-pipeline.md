# 运行时主流程

这一页想回答的只有一个问题：

> 从程序启动，到机器人真的收到一帧控制指令，中间到底经历了什么？

很多人刚看这个仓库时，会把不同层的名字拆开记：`main.cpp`、`DecisionModule.cpp`、`SelectPlay.py`、`Skill.py`、`TaskMediator`……结果越看越碎。更好的方式，是把它们当成一条连续的时间线。下面我们就按“启动”到“单帧执行”这条时间线来走。

## 先看传统主线：C++ 顶层模式

如果你是从 `Medusa.exe` 启动系统，那么主线代码主要在：

- `Medusa/src/Main/main.cpp`
- `Medusa/src/Main/zeus_main.cpp`
- `Medusa/src/Main/DecisionModule.cpp`

`main.cpp` 其实不长，但角色非常关键。它会先创建 `pybind11::scoped_interpreter`，也就是把 Python 解释器嵌进当前进程；然后启动 Qt 事件循环；再开线程跑 `runLoop()`。这一步很多人第一次读时会愣住，因为它意味着哪怕你觉得自己走的是“纯 C++ 顶层”，Python 解释器其实也已经在进程里了。

接下来 `runLoop()` 会一路把系统常驻模块拉起来：参数系统、视觉模块、决策模块、动作模块、裁判盒接口，以及若干点位计算或可选 CUDA 模块。等这一堆东西初始化完，循环才真正开始：

```text
vision->setNewVision()
decision->DoDecision(false)
action->sendAction()
debug send
```

这四行就是比赛过程中最值得记在脑子里的“节拍器”。

## 真正的一帧，核心发生在 `DoDecision()`

`DecisionModule.cpp` 里的 `DoDecision()` 是整条链的分水岭。翻成自然语言，它每一帧大致做的是：

1. 等视觉线程把本帧数据准备好；
2. 清掉上一帧留在 `TaskMediator` 里的旧任务；
3. 更新各类中间决策模块和最佳点位计算；
4. 生成本帧高层任务；
5. 把这些任务继续规划到底层可执行 Skill；
6. 通知动作层可以取走结果并发包。

这里最容易被低估的是第 4 步和第 5 步的区别。

`GenerateTasks()` 回答的是“这帧想让哪台车做什么”；`PlanTasks()` 回答的是“这些高层任务怎么不断细化，最后变成真正可执行的控制任务”。如果你把这两步混在一起，后面看 `Skill.py` 和 `CPlayerTask::plan()` 时就会很容易迷糊。

## Python 是在什么时候插进来的

在当前主线里，Python 主要是在 `GenerateTasks()` 这一步介入。`DoTeamMode()` 会根据脚本语言配置决定是跑旧 Lua，还是调用 Python 的 `SelectPlay.SelectPlay()`。现在默认当然是 Python。

这意味着一帧中间其实会经历这样一段过程：

```text
C++ 进入 DecisionModule
    -> 调用 Python 的 SelectPlay.py
    -> Python 侧生成 Task 并通过 CppPackage.makeIt... 把任务写回 C++
    -> C++ 再继续 PlanTasks()
```

所以“Python 负责战术”“C++ 负责执行”这句话，并不是抽象口号，而是这段时序在代码里的真实体现。

## 再看另一条线：Python 作为顶层入口

如果你直接在 `ZBin/` 下运行：

```powershell
python PythonScripts/main.py --team blue --side right --sim
```

那么系统会换一种组织方式。`main.py` 会先解析参数并写回 `zss.ini`，然后拿到 `CppPackage.SystemRunner.Instance()`，再调用 `init()` 完成底层初始化。之后主循环就变成：

```python
systemRunner.preDecision()
SelectPlay.SelectPlay()
systemRunner.postDecision()
```

这里的 `SystemRunner` 本质上是在做一件很聪明的事：它把原本 C++ 顶层循环中的“一整帧”拆成了前半段和后半段，好让 Python 可以很自然地插在中间。于是你会得到这样一条更适合日常调试的链：

- `preDecision()`：更新视觉、清空旧任务、做本帧前置准备；
- `SelectPlay.SelectPlay()`：在 Python 层断点、改单帧逻辑、看状态机；
- `postDecision()`：回到 C++，继续递归规划 Skill、发包、发调试信息。

## 为什么 `preDecision()` 和 `postDecision()` 必须成对

这点值得单独强调，因为很多实验脚本会在这里踩坑。

`preDecision()` 不是“随便调一下更新世界模型”的便捷函数，它是完整帧流程的前半段。`postDecision()` 也不是“可有可无地补个发包”，它承担了后半帧的任务规划和执行。如果你只调前者不调后者，系统就会停在“已经知道这一帧看见了什么，但还没有把任务规划下去”的中间态；如果你只调后者不调前者，则可能在用旧视觉、旧任务状态继续往下跑。

!!! warning "日常开发里最容易忽略的一件事"
    Python 顶层模式看起来像普通脚本循环，但它本质上仍然是在驱动同一个 C++ Core。不要把 `preDecision()` / `postDecision()` 当成随便拆开的辅助接口。

## 真正值得你在调试里盯住的断点位置

如果你想完整走一遍“一帧从哪来，到哪去”，一个很高效的断点路线是：

1. `main.cpp` 或 `PythonScripts/main.py`
2. `zeus_main.cpp` / `SystemRunner`
3. `DecisionModule::DoDecision()`
4. `SelectPlay.SelectPlay()`
5. 某个具体 `Play` 的 `planTasks()`
6. `State.run()`
7. `Skill.py` 里的某个包装函数
8. `pybind_Skill.cpp` 里的对应 `makeIt...`
9. C++ 里真正的 Skill `plan()`

你一旦这样完整走过一遍，后面再看到仓库里那些看似分散的模块名，就不会再觉得它们是彼此独立的代码片段，而会自然把它们放回“这一帧的时间顺序”里。
