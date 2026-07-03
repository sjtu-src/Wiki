# VS Code 调试工作流

当前仓库的 `.vscode/launch.json` 已经把几种最常用的调试入口准备好了。真正的关键不是记住配置名字，而是知道：**我现在是在调顶层 Python，还是在调传统 C++ 入口；我想看的是单边逻辑，还是整条 Python-C++ 链。**

## 最常用的一条：`Python 调试main.py`

这是日常开发最推荐先上的入口。它会直接启动 `ZBin/PythonScripts/main.py`，并把工作目录设成 `ZBin/`。如果你现在主要在改：

- `SelectPlay.py`
- `Config.py`
- `Play/*`
- `RoleMatch_LuaStyle/*`

那这条通常就是第一选择。

它的最大好处是：你不需要先穿过 `Client -> Medusa.exe` 那条更传统的入口，就能直接在 Python 顶层主循环里打断点。对改战术、看状态机和查角色匹配来说，这会省很多时间。

## 想连 C++ 一起看时，用 compound

当前工作区已经配好一个很实用的 compound：

```text
Python顶层 + C++ 联合调试
```

它的思路其实很自然：先用 `Python 调试main.py` 启动加载了 `CppPackage.pyd` 和 `MedusaCore.dll` 的 `python.exe` 进程，再用 `C++ (Windows) 附加` 挂到这个进程上。注意，这里附加的不是 `Medusa.exe`，而是那只已经把 Core 加载进来的 Python 进程。

这条工作流特别适合下面这种场景：

> 你想从 `Play` 或 `Skill.py` 的高层逻辑出发，一路追到 `pybind_Skill.cpp`、再追到真正的 C++ Skill `plan()`。

## 什么时候该回到传统 C++ 顶层

仓库里也保留了经典路线：

- `Launch C++ EXE with Python debugpy`
- `Python Attach (debugpy 5678)`

这条路更适合你在下面这些情况下使用：

- 问题只会在 `Medusa.exe` 传统入口下复现；
- 你想看 `Client -> Medusa.exe` 这条老工作流；
- 你确实需要复现更接近比赛时的入口形式。

它的代价是调试动作稍多一些，因为 Python 侧需要显式打开 `debugpy.listen(5678)` 并等待 attach。不过仓库里已经预留了相关注释模板，所以并不是从零开始折腾。

## `当前文件调试` 不是主线，但也很有用

`Python 调试程序: 当前文件` 这个配置很适合跑一些单独的小脚本，比如工具脚本、数据处理脚本、GUI 辅助模块或小实验。但它并不适合替代完整比赛主循环，因为它默认不会自动给你拉起整个 `SystemRunner -> SelectPlay -> postDecision` 这套流程。

所以更合适的用法是：把它当作“单脚本实验台”，而不是“比赛系统总入口”。

## 平时怎么选最省力

如果你现在在改战术脚本、状态机或 `Skill.py` 包装层，通常先选 `Python 调试main.py`。如果你已经知道这次排查一定会追进 C++ 底层，那就直接上 compound。只有当你明确需要复现传统入口问题时，才优先回到 `Launch C++ EXE with Python debugpy`。

这个顺序看起来像经验主义，但实际上很省时间。因为大部分日常问题，根本不需要先把整条老入口链都拉起来。

## 如果断点怎么都进不去，先别急着怀疑 VS Code

绝大多数所谓“调试器坏了”的问题，最后都能回到下面这几项对齐检查：

1. VS Code 当前 Python 解释器是不是 `ZBin/PythonScripts/.venv`；
2. 当前工作目录是不是 `ZBin`；
3. 你现在调的是 Python 顶层模式，还是 C++ 顶层模式；
4. 你附加到的进程到底是不是那只真正加载了 Core 的进程。

!!! tip "一个非常实用的判断"
    如果你走的是 Python 顶层联合调试，C++ 应该附加到 `python.exe`；如果你走的是传统入口联合调试，C++ 本体才会是 `Medusa.exe`。

只要这几件事在脑子里一直很清楚，调试这件事就不会显得神秘。
