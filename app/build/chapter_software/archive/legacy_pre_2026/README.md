# Legacy 说明

这个目录保存的是 2026 版重构之前的软件章节旧文档。

保留它们的原因只有一个：当你需要追溯历史设计、理解旧 Lua 时代脚本、或者寻找某些已经迁移掉的术语时，可以回来查。

但在日常开发里，请优先阅读新版 `chapter_software/` 主线文档。当前维护的主架构已经是：

- `Medusa.exe` / `MedusaCore.dll`
- `ZBin/PythonScripts`
- `Pybind11` 暴露出的 `CppPackage`

如果你发现这里的旧文档和当前代码冲突，以 **当前代码** 为准。
