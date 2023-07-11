# 基本元素
## Rectangle
**绘制矩形**
- height,width
- border：.width, .color
- radius
## Item
**可视元素基类，也可用于分组**
# 基本属性
- id：用于引用（anchor），具有唯一性
- 信号处理器：on{signal}
# 布局
## 绝对坐标(类似absolute)
- x,y（相对window）
- width
- height

## 锚布局(anchor,类似relative)
**anchor实为item指令集**
- horizontalCenter：水平居中（相对锚点）
- verticalCenter：垂直居中（相对锚点）
- top,bottom,left,right：上下左右与锚点对齐（贴贴）
- margins（topMargin and so on)：上下左右留白
- fill：充满
- centerln：居中放置在控件内部
## 定位器
### Row
**一行之中布局**
- spacing：间距
- layoutDirection：从左向右，从右向左
### Column
**一列之中，与row相似**
### Grid（表格布局）
- rows,columns：设定行列数
- rowSpacing,columnSpacing：设定行列间距
- flow：默认左到右，可以上到下
### Flow
**与Grid相似，无固定行列数，根据子item大小折行**
## 布局管理器
### layout布局
- alignment：对齐方式