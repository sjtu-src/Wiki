# *Pybind11、CMake 与 C++ Skill 绑定

这一页属于进阶内容，因为它讨论的不是“如何写战术”，而是更底层的一件事：

> 当你在 C++ 里写了一个新能力，怎样把它变成 Python 层真正好用、可补全、可维护的一等公民？

这件事一旦搞明白，你会对当前整套 Python-C++ 架构的边界有非常扎实的理解。

## `CppPackage` 不是“某个普通模块”，而是整座桥

对 Python 开发者来说，`CppPackage` 就是访问 C++ Core 的统一入口。你在 Python 里看到的这些对象和函数：

- `CppPackage.SystemRunner`
- `CppPackage.VisionModule`
- `CppPackage.TaskMediator`
- `CppPackage.CGeoPoint`
- `CppPackage.makeItRushTo(...)`

本质上都来自同一个二进制扩展模块：`CppPackage.pyd`。

当前仓库采用的是“一个顶层二进制包 + 一个同名 `.pyi` + 一个 Python 包壳”的组织方式：

- `CppPackage.pyd`：真正的 pybind11 扩展；
- `CppPackage.pyi`：给 IDE 用的类型提示；
- `CppPackage/__init__.py`：补 DLL 搜索路径，再转发导入。

所以平时请把它当成**统一入口**来理解，而不要期待它像普通 Python 包那样按多级目录拆成很多二进制子包。

## 绑定代码在仓库里的哪一层

当前绑定代码主要集中在：

```text
Medusa/src/Pybind11Module/
```

其中最常见的子目录包括：

- `Geometry/`
- `Vision/`
- `WorldModel/`
- `Utils/`
- `Strategy/Skill/`
- `System/`

最终由 `pybind_CppPackage.cpp` 统一把这些注册函数组装成一个 `PYBIND11_MODULE(CppPackage, m)`。所以如果你新增了某个绑定文件，却忘了让上层注册函数真的调到它，最后 Python 里是看不到的。

## CMake 在这里不是配角，而是总装线

当前这套架构里，CMake 真正在做的是整条编译链的装配工作。它要负责：

1. 找到 `ZBin/PythonScripts/.venv` 这套 Python 环境；
2. 构建 `MedusaCore.dll`；
3. 构建 `CppPackage.pyd`；
4. 运行 `pybind11-stubgen` 生成 `CppPackage.pyi`；
5. 把运行时需要的二进制和脚本放到 `ZBin` 的正确位置。

所以不要把 pybind 绑定理解成“顺手写个包装函数”。它背后是一整套由 CMake 串起来的构建和部署流程。

## `.pyi` 为什么在这个项目里特别重要

`CppPackage.pyd` 是二进制模块，本身不适合给 IDE 做参数提示和静态补全。当前工程通过 `pybind11-stubgen` 生成的 `CppPackage.pyi`，会把大量接口签名同步出来。

这件事的价值远比“补全好看一点”更大。因为一旦 Python 顶层越来越重，大家写 `Skill.py`、`Play/*.py` 时对接口签名的依赖会越来越强。如果没有 `.pyi`，很多参数只能靠记忆、猜测或者到 pybind 源码里现翻，维护成本会明显上升。

## 新增一个 C++ Skill 后，通常要经过哪几层

下面这条链，建议你背下来。它几乎就是“让一个 C++ 能力进入 Python 生态”的标准路径。

1. 在 `Medusa/src/Strategy/skill/` 里实现或修改真实 C++ Skill；
2. 通过 `TaskFactoryV2` / `PlayerRole` 或相关接口，确保 C++ 内部能创建并调用它；
3. 在 `Medusa/src/Pybind11Module/` 里增加 pybind 包装函数和 `m.def(...)` 注册；
4. 重新构建，生成新的 `CppPackage.pyd` 和 `CppPackage.pyi`；
5. 如果你希望 Python 侧更易用，再去 `RoleMatch_LuaStyle/Skills/Skill.py` 加一层更符合项目习惯的包装。

只要其中一层漏了，这条链就不完整。

## 真正实用的做法：先判断你要绑定的是哪一类能力

新增绑定时，先别急着上手写 `m.def(...)`。更好的第一步是先判断：你要暴露给 Python 的到底是哪一类东西。

### 第一类：直接暴露一个已有的查询或工具接口

比如某个世界模型查询函数、某个单例对象的方法、某个 Geometry 工具。这类绑定通常比较直接，更多是在做类型转换、返回策略和模块组织。

### 第二类：暴露一个“可被 Python 当作 Skill 调用”的任务入口

这类最常见，也最容易踩坑。因为 Python 层真正想要的通常不是“某个 C++ 类本身”，而是一个像 `makeItRushTo(...)`、`makeItWBack(...)`、`makeItTurnAndShoot(...)` 这样的任务入口。此时 pybind 文件里往往要自己手动：

- 新建 `TaskT playerTask`；
- 填 `executor / player.pos / player.angle / flag / needdribble / ball.Sender / extraTaskParams`；
- 再交给 `TaskFactoryV2` 去创建真正的 C++ Skill；
- 最后注册到 `TaskMediator`。

也就是说，这一层并不只是“自动导出 C++ 符号”，而是在主动把 Python 参数翻译成项目内部的任务结构。

## 一个典型绑定函数长什么样

以 `pybind_Skill.cpp` 里的 `makeItRushTo` 为例，它的套路很标准：

```cpp
void makeItRushTo(const int executor, const CGeoPoint &target, const double angle, ...)
{
    TaskT playerTask;
    playerTask.executor = executor;
    playerTask.player.pos = target;
    playerTask.player.angle = angle;
    ...

    CPlayerTask *pTask = TaskFactoryV2::Instance()->SmartGotoPosition(playerTask);
    TaskMediator::Instance()->setPlayerTask(executor, pTask, 1);
}
```

然后在 `register_skill(...)` 里再加一条：

```cpp
m.def("makeItRushTo", makeItRushTo, ...);
```

这就是 Python 里 `CppPackage.makeItRushTo(...)` 的来源。

## 如果你要新增一个 C++ Skill，推荐按这个顺序做

### 第 1 步：先把 C++ 内部能力做扎实

先确认这个 Skill 在纯 C++ 体系里能被创建、能被 `plan()`、能通过 `setSubTask()` 正常下钻。也就是说，先把它当成一个 C++ Skill 写对，而不是一上来就想着 Python 怎么调。

### 第 2 步：决定参数该怎么落进 `TaskT`

这是最关键的一步。你要提前想清楚：

- 目标点放 `player.pos` 吗？
- 朝向放 `player.angle` 吗？
- 传球者编号或防守编号是不是要用 `ball.Sender`？
- 是不是需要 `extraTaskParams` 来存额外模式？

很多 binding 写坏，不是 pybind 语法错，而是 `TaskT` 字段设计错了。

### 第 3 步：在 pybind 层写包装函数和注册

如果是 Skill 相关入口，通常放在：

```text
Medusa/src/Pybind11Module/Strategy/Skill/pybind_Skill.cpp
```

如果是全新类别的能力，也可以新建绑定文件，然后在对应上层注册函数里接进去。

### 第 4 步：必要时补 `Skill.py` 包装层

很多时候，直接在 Python 里裸调 `CppPackage.makeIt...` 不够优雅，也不符合当前项目的任务接口约定。此时就应该再去 `RoleMatch_LuaStyle/Skills/Skill.py` 写一层包装，把它变成返回 `(skill_cpp, matchPos)` 的标准形式。

### 第 5 步：重新构建并检查 `.pyi`

构建成功之后，别只看 `.pyd` 有没有生成。一定要顺手确认：

- `CppPackage.pyi` 有没有更新；
- Python 里是否能正确补全新接口；
- 默认参数、类型签名和名称是否符合预期。

## `litgen_online` 能帮什么，不能帮什么

仓库里已经专门放了一个工具目录：

```text
ZBin/PythonScripts/litgen_online/
```

这里的 notebook 和说明，主要是为了借助 litgen 生成 pybind 代码骨架。这个工具很好用，尤其在你要绑定一批查询接口、结构体、普通函数时，会明显节省时间。

但要注意，它生成的是“骨架”，不是最终可直接交付的项目代码。当前项目里很多 Skill 绑定都有自己的工程约束，litgen 不会替你自动处理：

- `TaskT` 的参数打包；
- `TaskMediator` 注册；
- 自定义默认参数和 `py::arg(...)` 命名；
- `py::return_value_policy::reference` / `py::nodelete` 这类生命周期问题；
- Qt / pybind11 / 宏定义之间的工程细节；
- 生成后还要接入当前 `register_*` 体系。

所以更实际的建议是：

!!! tip "推荐使用方式"
    可以先用 `litgen_online` 或 AI 帮你生成第一版绑定骨架，但一定要把它当成草稿。最后定稿时，仍然要回到当前仓库的 `pybind_Skill.cpp`、`pybind_CppPackage.cpp`、`TaskT` 和 CMake 体系里逐项校对。

## 一个经常被忽视但非常重要的点：导出边界

当前工程里，`MedusaCore.dll` 和 `CppPackage.pyd` 共享大量底层能力。如果某个函数、类或单例本来只在一个编译单元里可见，你直接在 pybind 里 include 进去，并不代表它就天然能跨 DLL 正常共享状态。

这也是为什么仓库里反复强调像 `TaskMediator`、`TaskFactoryV2` 这类共享状态对象，不能草率地保持成“看似 header-only 的单例写法”，而要显式实现并导出。否则 Python 和 exe 侧很可能看见的不是同一份实例。

## 这一页想让你带走的核心观念

如果你只是改战术，不一定非得马上精通所有 pybind 细节；但只要你想把一个新的 C++ 能力平稳交给 Python 层使用，就一定要把下面这几个名字看成同一套体系：

- `MedusaCore.dll`
- `CppPackage.pyd`
- `CppPackage.pyi`
- `Pybind11Module/`
- `TaskT`
- `TaskMediator`
- CMake 构建与拷贝流程

它们不是几个互相独立的文件，而是一条真正把 C++ 能力送到 Python 手里的装配链。
