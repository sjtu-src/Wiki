简单介绍一下`Lua C++ Binding`：

## 步骤一

用VS2010打开`robokit_ssl2017_Company\build\RoboKit.sln`，再打开插件`SSLStrategy`下的`VisionModule.h`，然后在该类里面添加一个函数，如下图红框所示。完成后需要重新生成该插件。

![Visionmudole](uploads/e384387c85a13d2e5d3e869de3975c02/Visionmudole.jpg)



## 步骤二

该插件重新生成后，打开`robokit_ssl2017_Company\plugins\SSLStragegy\src\LuaMudole`文件夹，找到并打开`visionmodule.pkg`（该文件告知`tolua++`要为LUA提供哪些函数），然后添加相应的函数，如下图所示：

![pkg](uploads/805419d41fc553d8ee16ab1703014fec/pkg.jpg)



接着，在`LuaMudole`文件夹下，找到并运行`test.bat`文件以生成`tolua源文件`，结果如下图所示：

![tolua](uploads/75ed824dd2567d0a10458c0aca0fdf4a/tolua.jpg)



然后在`LuaModule`文件夹下，`tolua++`会自动生成`lua_zeus.cpp`，结果如下图所示：

> tolua++是tolua的扩展版本。tolua是一个工具，它使LUA和C/ C++结合起来更加容易。它生成绑定C/ C++代码。tolua++提供了额外的功能，是为C++设计的。

![lua_zeus1](uploads/6bd4f5eae8172ee3c380b3d065a10140/lua_zeus1.jpg)

![lz2](uploads/a1d3f5c385a07ef827a265b559a4e19f/lz2.jpg)



## 步骤三（测试）

- 先观察`ball.lua`是怎么调用C++的，如下图所示：

![ball_lua](uploads/e24da97c0af00990eda71394d7ab68f7/ball_lua.jpg)

当我们在Lua程序里调用`pos()`函数时，其实最终调用的是`vision:Ball():X()`，其中vision是类`CVisionModule`的一个对象；

--- 

- 新建一个play：`Test.lua`，分别调用`vision:Ball():X()`和`vision:printNum()`，如下图所示：

![test](uploads/6a0e9d08875c97b2216214798f94bb84/test.jpg)

其中，第一个红框部分打印出球的x坐标，第二个红框部分打印出传入的一个数50，测试结果如下：
![teset_result](uploads/05980f324d6315e5bcd271f2c3b5a5fe/teset_result.jpg)


# 参考资料：

可以动手试一试：[toLua++ example](http://usefulgamedev.weebly.com/tolua-example.html)

