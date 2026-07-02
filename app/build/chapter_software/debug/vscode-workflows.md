# VS Code 调试工作流

当前仓库的 `.vscode/launch.json` 已经准备了几套常用配置。  
关键是你要理解它们分别对应什么场景。

## 工作流 1：Python 顶层启动

最直接的入口是：

- `Python 调试main.py`

它会：

- 启动 `ZBin/PythonScripts/main.py`
- 以 `ZBin/` 为工作目录
- 适合调试 Python 顶层主循环

如果你当前主要在改：

- `SelectPlay.py`
- `Config.py`
- `Play/*`
- `RoleMatch_LuaStyle/*`

这通常是第一选择。

## 工作流 2：Python 顶层 + C++ 联合调试

当前已经有一个 compound：

- `Python顶层 + C++ 联合调试`

它的思路是：

1. 用 `Python 调试main.py` 启动 `python.exe`
2. 再用 `C++ (Windows) 附加` 连接到这个 Python 进程

注意这里附加的不是 `Medusa.exe`，而是 **加载了 `CppPackage.pyd` / `MedusaCore.dll` 的 `python.exe` 进程**。

适合场景：

- Python 脚本和 C++ Skill 两边都要看
- 想追踪 `Skill.py -> CppPackage -> C++ task plan()` 全链路

## 工作流 3：C++ 顶层启动 + Python attach

当前也保留了传统方式：

- `Launch C++ EXE with Python debugpy`
- `Python Attach (debugpy 5678)`

这种方式适合：

- 你想从 `Medusa.exe` 传统入口复现问题
- 但同时又想断到 Python 层

前提是 Python 侧代码里需要显式打开 `debugpy.listen(5678)` 并等待 attach。  
当前项目里已经在若干文件里预留了相应注释模板。

## 工作流 4：当前脚本单独调试

还有一个通用配置：

- `Python 调试程序: 当前文件`

适合：

- 某个工具脚本
- 某个数据处理脚本
- 单独跑一个小实验

但它不适合直接替代完整比赛主循环调试。

## 推荐你平时怎么选

### 改战术脚本

优先：

- `Python 调试main.py`
- 或 `Python顶层 + C++ 联合调试`

### 查传统入口问题

优先：

- `Launch C++ EXE with Python debugpy`

### 查纯 C++ 底层执行

优先：

- C++ 启动 / 附加
- 然后只在必要时再把 Python 连进来

## 一个很关键的排障顺序

如果断点怎么都进不去，先查下面四件事：

1. VS Code 当前 Python 解释器是否是 `.venv`
2. 当前工作目录是不是 `ZBin`
3. 调的是 Python 顶层流程还是 C++ 顶层流程
4. 你附加到的进程是不是对的

很多所谓“调试器坏了”，其实都是这四件事里有一件没对齐。
