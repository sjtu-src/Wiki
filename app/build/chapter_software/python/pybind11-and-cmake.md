# Pybind11 + CMake

这一页讲的是当前 Python-C++ 架构最关键的“桥”。

## `CppPackage` 是什么

对 Python 开发者来说，`CppPackage` 就是：

> 访问 C++ Core 能力的统一入口。

你在 Python 里看到的这些东西，大多都来自它：

- `CppPackage.SystemRunner`
- `CppPackage.VisionModule`
- `CppPackage.TaskMediator`
- `CppPackage.makeItRushTo(...)`
- `CppPackage.CGeoPoint`

## 当前的包形态

仓库采用的是：

- 一个大的 `CppPackage.pyd`
- 一个对应的 `CppPackage.pyi`
- Python 侧用 `CppPackage/__init__.py` 处理 DLL 搜索路径

这意味着当前推荐认知是：

- **对外只暴露一个顶层包 `CppPackage`**
- 不要指望按多级本地二进制包去 import

这也是当前仓库里“单层包”设计的核心原因。

## 绑定代码在哪里

主要在：

```text
Medusa/src/Pybind11Module/
```

常见子目录包括：

- `Geometry/`
- `Vision/`
- `WorldModel/`
- `Utils/`
- `Strategy/Skill/`
- `System/`

`pybind_CppPackage.cpp` 最终把这些模块统一注册成 `CppPackage`。

## CMake 在这里扮演什么角色

当前 `CMakeLists.txt` 里做了几件很关键的事：

1. 把 Python 和 pybind11 显式绑定到 `ZBin/PythonScripts/.venv`
2. 构建 `MedusaCore.dll`
3. 构建 `CppPackage.pyd`
4. 生成 `CppPackage.pyi`
5. 把运行所需文件复制到 `ZBin`

因此这不是“额外加一层类型提示”的小工具链，而是整个 Python-C++ 架构的编译基础设施。

## `.pyi` 为什么重要

`CppPackage.pyd` 是二进制模块，本身不提供良好的 IDE 类型提示。  
所以项目会通过 `pybind11_stubgen` 生成：

```text
CppPackage.pyi
```

它的价值非常大：

- 自动补全更可靠
- 类型和参数签名更清楚
- 新人写 Python 脚本时少很多猜测

## 如果你要新增一个绑定，大概步骤是什么

1. 找到对应的 C++ 能力应该放在哪个 pybind 子目录
2. 在 `Pybind11Module/...` 里补充声明和注册
3. 保证它依赖的 C++ 符号在 `MedusaCore.dll` 中正确导出
4. 重新构建 `PybindAll`
5. 检查 `CppPackage.pyi` 是否更新

## 当前这套体系里最常见的坑

### 1. Python 版本不一致

编译 `pyd` 用的 Python，和运行脚本用的 Python，必须是同一个版本体系。

### 2. DLL 搜索路径错误

这会导致：

```python
import CppPackage
```

直接失败。

### 3. `slots` 宏冲突

Qt 的 `slots` 宏和 Python / pybind 头文件里的命名冲突，是这个项目里的经典坑。  
当前代码里已经有相应处理方式，但你新增绑定时仍然要有这个意识。

### 4. 把头文件内联实现当成可共享单例

像 `TaskMediator`、`TaskFactoryV2` 这种涉及共享状态的对象，如果处理不当，会出现“看似同名，实际不是同一份实例”的问题。  
这也是当前工程把一些原本 head-only 的单例写法改成显式实现的原因。

## 一个很重要的开发观念

如果你只是写战术，不一定需要理解所有 pybind 细节；  
但如果你想把某个 C++ 能力变成 Python 一等公民，那你迟早要理解：

- `MedusaCore.dll`
- `CppPackage.pyd`
- `CppPackage.pyi`
- `PybindAll`

它们是一整套，不是彼此独立的几个文件。
