# 本项目的开发环境

## 当前推荐栈

结合当前仓库配置，软件层推荐环境是：

- Windows 11
- VS Code
- MSVC / Visual Studio 2022
- Qt 6.9+
- CMake
- `uv` 管理的 Python 3.12.10 环境
- `Pybind11` 作为 Python-C++ 绑定工具

关键事实只有一句：

> Python 相关工作统一围绕 `ZBin/PythonScripts/pyproject.toml` 和 `ZBin/PythonScripts/.venv` 展开。

## 第一步：同步 Python 环境

进入 `ZBin/PythonScripts/`：

```powershell
cd ZBin\PythonScripts
uv sync
```

当前 `pyproject.toml` 里已经声明了常用依赖，例如：

- `debugpy`
- `munkres`
- `PySide6`
- `pybind11`
- `pybind11-stubgen`

不要把这套环境散落到系统 Python、conda base、其它软件自带 Python 里。

## 第二步：让 VS Code 选对解释器

在 VS Code 里执行：

```text
Ctrl+Shift+P -> Python: Select Interpreter
```

选择：

```text
ZBin/PythonScripts/.venv/Scripts/python.exe
```

如果解释器选错，会直接影响：

- Python 调试
- `debugpy`
- `pybind11_stubgen`
- `PySide6` 工具脚本
- 运行时 `import CppPackage`

## 第三步：理解 CMake 的关键约束

当前根 `CMakeLists.txt` 明确把 Python 和 pybind11 指向项目 `.venv`：

- `pybind11_DIR = ZBin/PythonScripts/.venv/...`
- `Python_EXECUTABLE = ZBin/PythonScripts/.venv/Scripts/python.exe`

这意味着：

- 编译 `CppPackage.pyd` 用的 Python 版本，应该和你运行 Python 顶层时用的是同一个版本。
- 如果你手动把解释器切成别的 Python，最常见后果就是 `import CppPackage` 崩掉。

## 第四步：第一次编译时建议关注什么

对新人最重要的构建目标有两个：

- `Medusa`：生成 `Medusa.exe`
- `PybindAll`：生成 `CppPackage.pyd` 和 `CppPackage.pyi`

如果 `CppPackage.pyi` 没生成出来，IDE 类型提示会差很多，但真正影响运行的往往还是：

- `CppPackage.pyd`
- `MedusaCore.dll`
- 相关 Qt / Python DLL 是否都在 `ZBin/`

## 运行时为什么一定强调 `ZBin`

当前工程里很多配置、参数和相对路径都默认以 `ZBin` 为根目录，例如：

- `zss.ini`
- `params/`
- `PythonScripts/`
- `data/power_curve/`

所以无论是 Python 顶层启动，还是某些工具脚本，**都优先从 `ZBin` 作为当前工作目录运行**。

## 一个最小可工作的心智模型

你可以把整套环境理解成三层：

1. 编译层：`CMake + MSVC + Qt + pybind11`
2. 运行层：`ZBin/` 下的 exe / dll / pyd / ini / data
3. 脚本层：`PythonScripts/` 下的 Play、RoleMatch、WorldModel、工具脚本

只要这三层的路径和版本统一，后面很多“玄学问题”都会自动消失。
