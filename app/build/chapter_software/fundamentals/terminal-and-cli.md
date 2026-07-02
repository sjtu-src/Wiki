# Terminal 与 CLI

## 为什么软件组成员必须会命令行

在 SRC 的软件开发里，命令行不是可选项，而是基础设施：

- 你要用 `git` 同步和整理代码。
- 你要用 `uv` 管理 Python 环境。
- 你要用 `cmake` / VS Code CMake Tools 生成和编译工程。
- 你要在 `ZBin` 目录下直接启动 `main.py`，否则很多相对路径会错。

GUI 工具当然可以用，但只会点按钮很容易在出问题时不知道系统到底做了什么。

## 你最应该记住的几个工作目录

| 目录 | 作用 |
| --- | --- |
| 仓库根目录 `MilkTest/` | CMake 工程根目录 |
| `MilkTest/ZBin/` | 运行时根目录；很多配置和相对路径都从这里算 |
| `MilkTest/ZBin/PythonScripts/` | Python 顶层代码、`pyproject.toml`、`.venv` |
| `MilkTest/build/` | Visual Studio / CMake 的输出目录 |

最常见的错误之一，就是在错误目录下运行程序。

## 本项目里最常用的命令

### `git`

```powershell
git status
git fetch
git pull --rebase --autostash
git switch -c your-branch
git add .
git commit -m "feat: ..."
git push
```

### `uv`

在 `ZBin/PythonScripts/` 下：

```powershell
uv sync
uv run python test.py
```

如果你在别的目录下乱装 Python 包，最后大概率会出现：

- VS Code 看到的解释器不是项目解释器
- `CppPackage.pyd` 编译用的 Python 版本和运行时版本不一致
- `debugpy` / `PySide6` / `pybind11-stubgen` 装到了错误环境

### `cmake`

常见流程是：

```powershell
cmake --preset Release
cmake --build --preset Release
```

实际开发时，很多人会直接用 VS Code 的 CMake 插件和 Visual Studio 生成器；但理解这两条命令仍然很重要。

## 什么是环境变量

你可以把环境变量理解成“进程启动时会继承的一组全局配置”，其中最常见的是：

- `PATH`：系统去哪里找可执行文件和 DLL
- `PYTHONPATH`：Python 去哪里找模块

本项目里尤其容易遇到的是 **DLL 搜索路径** 问题。

例如 `ZBin/PythonScripts/CppPackage/__init__.py` 会主动调用 `os.add_dll_directory(...)`，就是因为：

- `CppPackage.pyd` 本质上是 Python 侧加载的本地二进制模块；
- 它还依赖 `MedusaCore.dll`、Qt DLL、`python312.dll` 等一整串运行库；
- 如果这些 DLL 不在可搜索路径里，`import CppPackage` 就会失败。

## Windows 和 Linux 的心智差别

大体上可以这样记：

- Windows 更容易“点开就跑”，但路径、DLL 和解释器混用问题更多。
- Linux / WSL 更适合自动化和脚本化，但本项目当前主开发链路还是 Windows。

所以我们的建议不是“只会 GUI 就行”，而是：

- 在 Windows 上把 CLI 用顺；
- 能明确区分“编译目录”“运行目录”“Python 虚拟环境目录”；
- 出问题时先看路径、进程、解释器，而不是先怀疑算法。
