# CUDA 与进阶扩展

这一页是进阶内容。  
如果你还没把 `DecisionModule -> Play -> Skill -> Action` 主链走通，先不用急着看这一层。

## CUDA 模块在仓库里的位置

可选 GPU 模块位于：

```text
Medusa/src/CUDAModule/
```

根 CMake 里通过：

```text
option(USE_CUDA "Enable CUDA support" OFF)
```

控制是否启用。

## 当前它主要做什么

从代码结构上看，`CUDAModule` 主要围绕：

- 最佳传球点
- 最佳射门点
- 一些候选点评估

做 GPU 加速尝试。

在 `runLoop()` / `SystemRunner::init()` 里也能看到：

- 如果启用 CUDA，就初始化 `ZCUDAModule`
- 否则走 `ZGetBestUtils` 和 `ZBestPosCalculate`

## 对新人而言应该如何理解它

最实用的理解是：

- 这不是当前入门主线
- 它属于“为了更快地做大规模候选点评估而存在的加速模块”
- 它和普通 Play / Skill 开发是弱耦合的

也就是说，大部分日常战术开发并不需要先掌握 CUDA。

## 当前状态的一个现实提醒

仓库里的 CUDA 模块更像“可选高级实验层”，而不是所有功能都完全依赖它的基础设施。  
例如代码中也能看到一些 `todo`、条件编译和保底分支。

所以如果你想动它，建议先确认三件事：

1. 当前编译链是否真的启用了 `USE_CUDA`
2. 你的修改是“核心比赛依赖”，还是“可选加速增强”
3. 有没有同等功能的 CPU 回退路径

## 其它值得知道的进阶扩展点

除了 CUDA，当前系统还有两类很重要的进阶扩展方向：

- `Pybind11Module/`：给 Python 暴露更多 C++ 能力
- `PhysicalModel/` 与 Python 力度模型：把球模型和数据拟合工具接进战术层

如果你的目标是“让高层脚本更好用”，通常先看 pybind；  
如果你的目标是“让某类评估更快”，再考虑 CUDA 或更底层的数值优化。
