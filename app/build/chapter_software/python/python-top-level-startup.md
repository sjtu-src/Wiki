# *Python 作为顶层启动 Medusa

这一页属于进阶内容，因为它默认你已经知道系统的普通主线是怎么跑的。只有在这个前提下，你才会真正体会到 Python 顶层模式的价值：它不是为了“换一种启动姿势”，而是为了让你在日常开发里更方便地调 Python、连 C++、做实验和写工具。

## 什么时候值得优先用这种模式

如果你当前主要在改：

- `SelectPlay.py`
- `Config.py`
- `Play/Normal/*`
- `Play/RefPlay/*`
- `Play/Test/*`
- `RoleMatch_LuaStyle/*`

那么 Python 顶层模式通常会比传统 `Medusa.exe` 顶层更顺手。因为你可以直接在 Python 主循环里断点、改参数、看状态机切换，也更容易跟 VS Code 里的 `debugpy` 联动。

反过来说，如果你此刻只是在排查纯 C++ 底层路径规划、运动控制或 Qt 相关问题，那它就不一定是最优入口。

## 启动前最容易忽视的两件事

第一件事，是解释器必须对。当前项目要求的环境并不是你系统里随便一个 Python，而是 `ZBin/PythonScripts/.venv` 这套受 `uv` 管理的环境。`pyproject.toml` 里也明确写了 Python 版本和依赖，例如 `debugpy`、`munkres`、`pybind11`、`pybind11-stubgen`、`litgen` 等都在这里集中管理。

第二件事，是当前工作目录必须是 `ZBin/`。这一点千万别嫌啰嗦，因为 `main.py`、`CppPackage/__init__.py`、`zss.ini`、各种相对路径资源，默认都是按 `ZBin` 作为工作根来算的。

!!! warning "最常见的启动坑"
    不是脚本写错，也不是 pybind 坏了，而是你从错误目录启动了 Python，导致 `zss.ini`、`CppPackage.pyd`、`MedusaCore.dll`、参数文件和工具资源都找偏了。

## 基本启动命令

在 `ZBin/` 目录下，最常用的启动方式是：

```powershell
python PythonScripts/main.py --team blue --side right --sim
python PythonScripts/main.py --team yellow --side left
```

当前 `main.py` 支持的主要参数包括：

- `--team` / `-t`：`blue` 或 `yellow`
- `--side` / `--positive-side` / `-s`：`left` 或 `right`
- `--sim` / `--simulation`：是否仿真
- `--test-mode`：是否直接进入 Test Mode

这些参数最终会被写回 `zss.ini`，这样 Python 层和 C++ 层就能共享同一份启动状态。

## `main.py` 真正做了什么

`main.py` 的代码不长，但它做的事情非常像一层“Python 版系统启动器”。

它先解析命令行参数，然后通过 `_update_config_file()` 把队伍颜色、正方向、仿真开关等信息写进 `zss.ini`。接着，它创建 `CppPackage.SystemRunner.Instance()`，并调用 `systemRunner.init()` 完成底层 C++ 模块初始化。等这些都完成后，才进入真正的循环：

```python
systemRunner.preDecision()
SelectPlay.SelectPlay()
systemRunner.postDecision()
```

看到这里时，最好把这三行翻译成一句人话：

> 前半帧先让 C++ 更新视觉和环境，再让 Python 决定这帧任务，最后回到 C++ 做任务规划和发包。

## `SystemRunner` 在这里扮演什么角色

`SystemRunner` 的意义，在于把传统 `runLoop()` 那种“一整帧全包在 C++ 里”的流程，拆成更适合 Python 顶层插入的两段。

- `init()`：做底层初始化，相当于传统主流程里 while 循环之前的大部分准备工作；
- `preDecision()`：做本帧开始前的视觉更新和任务清理；
- `postDecision()`：做本帧后半段的 Skill 规划、发包和 debug 输出。

如果你只是把它看成“某个 pybind 包出来的类”，会低估它的重要性。更准确的说法是：它是 Python 顶层模式下，连接整个 C++ Core 生命周期的总开关。

## 为什么 `CppPackage/__init__.py` 也很关键

很多人会把 `CppPackage/__init__.py` 当成普通包初始化文件，但它这里有个很实用的工作：在 Windows 下先把 `ZBin/` 加进 DLL 搜索路径，然后再导入真正的 `CppPackage.pyd`。没有这一步，`import CppPackage` 往往会因为找不到 `MedusaCore.dll` 或其他依赖而直接失败。

所以 Python 顶层模式并不是“脚本直接调用某个 pyd”那么简单，而是靠：

- 工作目录对齐；
- `.venv` 解释器对齐；
- DLL 路径对齐；
- `zss.ini` 配置对齐；

这四件事一起才能稳定跑起来。

## 一个最小可运行骨架

如果你现在想验证的不是完整比赛逻辑，而只是“Python 能不能带着 C++ 跑起来”，那么脑子里可以先保留这样一个最小骨架：

```python
import CppPackage as C

systemRunner = C.SystemRunner.Instance()
systemRunner.init()

import InitAllModules
import SelectPlay

while True:
    systemRunner.preDecision()
    SelectPlay.SelectPlay()
    systemRunner.postDecision()
```

当然，真实 `main.py` 比这还多了参数解析、测试模式和退出处理，但核心骨架就是这样。

## 这一模式为什么特别适合调试

最大的原因不是“Python 更高级”，而是你现在可以把断点直接打在顶层脚本上，而不必每次都从 `Client -> Medusa.exe -> Python attach` 那条传统链进去。对日常开发来说，这会明显降低调试摩擦。

比如你想查：

- 为什么 `SelectPlay` 没切到预期脚本；
- 为什么某个 Test 脚本没拿到正确角色号；
- 为什么 `Skill.py` 传给 C++ 的参数不对；

用 Python 顶层模式通常会快很多。

## 但它不是万能入口

也要实事求是地说，这一模式并不适合所有问题。假如你现在在追：

- 纯 C++ 底层性能问题；
- `Client` 调 `Medusa.exe` 时才出现的兼容性问题；
- Qt 或线程相关的传统入口行为；

那么回到 C++ 顶层模式往往更直接。

所以真正成熟的使用方式不是“以后都只用 Python 顶层”，而是知道：**什么时候该用它，什么时候该回传统入口。**
