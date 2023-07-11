
## 综述

- 可视化的软件需要两个基本元素，一个是用于显示的界面，另一个则是要实现一些具体的功能
- 我们采用qml设计界面，功能基本都由C++实现。那么想在qml中调用C++编写的程序，就需要在两者之间建立接口
- 一点小建议：
    - 感觉学习最好先看界面部分，因为软件界面毕竟大家都见过了，代码可以对应上特定的按键，比较易懂
    - 自己写的话，也应该先把界面的框架搭好，再着手写C++接口和函数，如果前后倒置，就算写出来也不好检验

## 界面

- 比较简单的界面用一个.qml文件就够，直接调用Qt中自带的标准元件
- 如果需要自己定义元件，就在相同路径下建立新文件，语法都相同，就是多个标准元件的组合

### 必要部分

1. import相当于C++里的include，引用需要的库，一般形式是**import 库名 版本号**，或者**import 库名 版本号 as 别名**，后者是为了使用其中定义的类
    - import QtQuick 2.6
    - import Main 1.0 as Main
2.
```qml
ApplicationWindow{ // 每个软件必有的，建立一个app窗口
  id:window; // 别名，方便调用窗口内的变量、函数
  visible:true; // 必须为true，否则窗口不可见
  width: 500; // 窗口的宽度（横向长度）
  height: 700; // 窗口的高度（纵向长度）
  color: "#333" // 窗口的背景颜色

  Main.Test { id:test } //别名，方便调用库内的类

  Button{ // 窗口内显示的自定义内容
    id : clickButton;
    text : "Click";
    onClicked: clickEvent();
    function clickEvent(){
      test.clickEvent();
    }
  }
}
```

### 自定义部分

1. 这个语言的逻辑大致就是这样，有一些控件负责“圈地”，如Column、Rectangle、Grid等等，他们覆盖一定的区域，并规定该区域内的排列方式，如Column里的控件成行式排列，而Grid里的呈矩阵分布。他们覆盖的区域大小、颜色等特征，就由其中的width、height、color提供，这个与以上的ApplicationWindow中相同。各个控件可能还有特殊的性质，不过看名称就比较明了了。这些可以提供定值，也可以是可变量
2. 另外一类控键就来完成特定的功能，如按键Button、文本Text、下拉栏ComboBox。他们的括号里也有若干性质，作用同上。现在的代码里控件使用得挺全面了，以后想要加什么找到以前的仿写就行，下面介绍几个代表性控件：
   - 按键Button里面一般会有onClicked，就是它被点击触发的事件，可以是qml里面写的函数，也可以调用C++里的函数。其他控件里一般onXXX的形式都是定义这种触发事件的
   - 并不是所有的控件都会显示，如Timer，他就是个计数器，interval设置其周期，一个周期会触发一次，执行onTriggered{ …… }。开启和关闭都有特定函数 timer.start() 和 timer.stop()
   - Repeater，一个神奇的控件，其括号内的布局会同时显示多个，具体数量通过model定义。当然，多个样式相同的布局在程序内部是有区分的，会自动从0开始顺序分配一个index。但是Repeater及外围似乎无法读取index，则无法区别调用其中的控件，所以需要index的功能要在Repeater中定义
3. 控件间逻辑，以几个例子演示讲解
    - 想要将一个Button加入Grid里，就直接写入其括号内就行
      - Grid{
          ……
          Button{
            ……
          }
        }
    - 一个区域内的多个控件在代码里是并列关系，界面上的显示形式就是按照区域的规定，顺序分布
      - Grid{
          ……
          Text{
            ……
          }
          Button{
            ……
          }
        }
    - 有时也会有多级包含关系，如下就是在Rectangle上建立个Grid，再在Grid里搞个Button
      - Rectangle{
          ……
          Grid{
            ……
            Button{
              ……
            }
          }
        }
4. id是所用控件的共同性质，可写可不写，但注意一个文件内不要重复。有用的时候无非就是，一个控件想用另一个的性质，如宽度，可以用xxx(id).width来调取。当然，如果它俩属于包含关系，被包含的一方可以用parent称呼上一级控件，多级包含就是parent.parent.……
5. 想要自己定义一个变量，property 变量类型 变量名 : 变量值，如：
   - property bool isSimulation : true;
   - property int itemWidth : width - 2*padding;
   - 可以看到赋值可以赋定值，也可以是其他变量/控件特性的计算结果
6. qml里定义函数，语法是 function 函数名 {……}。内部与C++语法相似，可以有return，也可以使用if、while等语句

## 接口

- 先看类的定义
- 需要注意在qml里引用的类需要继承QObject，引用的函数前要加**Q_INVOKABLE**，放在public里，如:
```C++
header：
  #include <QObject>
  class CTest : public QObject
  {
	Q_OBJECT
  public:
	CTest(QObject *parent = 0);
	Q_INVOKABLE void clickEvent();
  };
cpp： 
  CTest::CTest(QObject *parent):QObject(parent){}
  void CTest::clickEvent(){
	qDebug()<<"click";
}
```
- 然后要调用**qmlRegister()**，注册在qml里的库以及库中的类，并关联C++中的类
- 可以看到qmlRegisterType里总共4个参数，第一个参数指的是QML中import后的内容，相当于库名，第二个第三个参数分别是主次版本号，第四个指的是QML中类的名字
- 注意，第四个QML的类名首字母一定要大写，要不然会报错，而且是那种你找不到的……
```C++
  void qmlRegister(){
    qmlRegisterType<CTest>("Main", 1, 0, "Test");
  }
```
- 到了qml里
```qml  
  import Main 1.0 as Main
  Main.Test { id : test; } // 必须有
```
- 然后就可以在qml中调用C++中定义的函数，如
```qml
  test.clickEvent();
```    
- 需要提醒：
  - 在实践中发现qml里的if语句似乎不能直接接受C++函数的返回值，需要先把返回值赋给变量
  - C++类中的变量也可以直接在qml里调用，但需要定义回调函数，且需要使用qmlRegisterSingletonType()。有兴趣的同学可以自学，或是参考Owl2里的rec_slider.h

## 相关资料

- [参考教程](https://blog.csdn.net/baidu_39502417/article/details/122296553)
