# 力度模型与数据驱动工具

## 当前推荐入口

现在高层脚本里统一通过：

```python
from WorldModel.PowerCalculator import evalPower, P
```

来计算力度。

不要在新代码里继续分散地：

- 到处手写距离到力度的映射
- 绕过统一入口直接乱调底层接口

## 为什么要统一到 `PowerCalculator`

因为当前系统已经同时支持多种后端：

- 旧式物理模型 / 距离映射
- 新的曲线后端

如果所有脚本都各算各的，后面就很难整体校准和切换。

## 当前两类主要后端

### `legacy`

更接近旧逻辑：

- 可以按距离线性映射
- 也可以走 C++ `PhysicalModel.evalPowerA2B`

### `curve`

这是当前更值得关注的新主线：

- 用 JSON 配置平射 / 挑射曲线
- `Low / Normal / High` 三档独立可调
- 运行时支持热重载
- 有独立 GUI 编辑器

## 这和 2026 TDP 的关系

2026 TDP 在软件部分强调了 **data-driven ball dynamics model**。  
在当前代码里，这个方向具体落成了两类能力：

- C++ 层的 `PhysicalModel`
- Python 层更易于实验和调整的曲线后端

可以把它理解成：

- C++ 模型更偏底层能力
- Python 曲线工具更偏实战调参与工程落地

## 曲线后端的关键文件

最值得优先看的几个文件：

- `WorldModel/PowerCalculator.py`
- `WorldModel/PowerCurveBackend.py`
- `tools/power_curve_editor.py`
- `Doc/Plan/PythonPowerCurveGUI.md`

## GUI 工具能做什么

当前已经有独立的曲线编辑器，用于：

- 编辑 flat / chip 两套曲线
- 分别设置 `Low / Normal / High`
- 调整上下限截断
- 保存 JSON
- 运行时热更新

启动方式是在 `ZBin` 下：

```powershell
.\PythonScripts\.venv\Scripts\python.exe PythonScripts/tools/power_curve_editor.py --curve-file data/power_curve/active_curve.json
```

## 运行时热更新的意义

这件事很实用，因为它让我们可以：

- 不改主战术逻辑
- 不重启整套流程
- 只改曲线文件
- 直接观察力度行为变化

对于比赛临场调参尤其有价值。

## 写战术时怎么选用

通常可以这样用：

```python
power = evalPower(Ball.pos(), target_pos, P.NORMAL)
```

经验上：

- 传球多用 `LOW` / `NORMAL`
- 射门通常直接走更激进的档位或显式满力
- 新逻辑优先复用统一入口，不要分散维护“第二套力度系统”

## 一个务实建议

力度问题表面上像“只是一个数”，实际上经常横跨：

- 球模型
- 电控车状态
- 比赛规则上限
- 脚本意图
- 调试工具

所以建议把它当成“独立子系统”来维护，而不是在脚本里顺手塞几个 magic number。
