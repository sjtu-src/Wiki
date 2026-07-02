# Python 作为顶层启动

这一模式非常适合：

- 快速调试战术
- 联合调试 Python 与 C++
- 直接写实验脚本
- 做工具化开发

## 启动前提

请先确认两件事：

1. Python 解释器是 `ZBin/PythonScripts/.venv/Scripts/python.exe`
2. 当前工作目录是 `ZBin/`

第二点非常重要，因为当前很多相对路径都默认从 `ZBin` 开始计算。

## 基本启动命令

在 `ZBin/` 下运行：

```powershell
python PythonScripts/main.py --team blue --side right --sim
python PythonScripts/main.py --team blue --side right
```

当前参数主要包括：

- `--team`：`blue` 或 `yellow`
- `--side` / `--positive-side`：`left` 或 `right`
- `--sim` / `--simulation`：是否仿真

## `main.py` 实际做了什么

它的大体流程是：

1. 解析命令行参数
2. 把关键参数写回 `zss.ini`
3. 创建 `CppPackage.SystemRunner.Instance()`
4. 调用 `systemRunner.init()`
5. 循环执行：

```python
systemRunner.preDecision()
SelectPlay.SelectPlay()
systemRunner.postDecision()
```

## 为什么会强调“必须从 `ZBin` 启动”

因为当前 Python 顶层并不只是普通脚本，它还要和 C++ 核心共享：

- `zss.ini`
- `params/`
- `CppPackage.pyd`
- `MedusaCore.dll`
- 若干工具数据文件

如果当前工作目录不对，常见结果包括：

- 参数读错
- 路径找不到
- `import CppPackage` 失败
- 某些 Skill 内部读取配置异常

## 一个最小可运行的骨架

如果你只是想快速验证视觉更新和 Python-C++ 交互，可以把主循环理解成：

```python
systemRunner = CppPackage.SystemRunner.Instance()
systemRunner.init()

import InitAllModules
import SelectPlay

while True:
    systemRunner.preDecision()
    SelectPlay.SelectPlay()
    systemRunner.postDecision()
```

## 什么时候优先用这种模式

推荐场景：

- 需要频繁改 Python Play
- 想把调试断点打在 Python 顶层
- 想做更快的实验和验证

不那么推荐的场景：

- 你当前只是在排查纯 C++ 底层问题
- 你需要复现完全等同于 `Client -> Medusa.exe` 的传统调用路径

两种模式都很重要，但 Python 顶层通常更适合日常开发。
