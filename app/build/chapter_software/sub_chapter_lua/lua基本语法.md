# Lua

## 什么是lua

Lua:simple-lua:{ .lua .lg.middle} 是一种轻量级的脚本语言，由巴西里约热内卢天主教大学的Roberto Ierusalimschy、Waldemar Celes 和 Luiz Henrique de Figueiredo三位研究员于1993年设计。Lua 被设计为简单、高效且可扩展，它广泛应用于嵌入式系统、游戏开发、网络编程和各种应用程序的脚本编写。

<div class="grid cards" markdown>
-    **语言特点** 


    ---
    
    - **轻量级**：Lua 的体积小，易于嵌入其他应用程序。
    
    - **简洁**：语法简洁，易于学习和使用。
    
    - **可扩展性**：Lua 提供了丰富的API，方便与其他语言（如C/C++）进行交互。
    
    - **跨平台**：支持多种操作系统，包括Windows、Linux、macOS等。
    
    - **多范式**：支持过程式编程、面向对象编程和数据驱动编程。

-    **语法结构**

    ---
    - **变量**：使用 `local` 关键字声明局部变量，或直接声明全局变量。
    - **控制结构**：包括 `if`、`then`、`else`、`end`（条件语句），`while`、`do`、`end`（循环），`for`、`in`、`do`、`end`（迭代）等。
    - **函数**：使用 `function` 关键字定义函数，支持闭包和匿名函数。
    - **表（Table）**：Lua 的基本数据结构，类似于其他语言中的数组或字典。
    - **模块**：Lua 使用模块系统来组织代码，使用 `require` 函数加载模块。


-    **标准库**

    ---
    
    - **基础库**：提供内存分配、数学函数、表操作等基础功能。
    - **字符串库**：提供字符串处理功能，如模式匹配、字符串格式化等。
    - **表库**：提供表的迭代、排序等操作。
    - **IO库**：提供文件和输入输出操作。
    - **数学库**：提供更高级的数学运算功能。
    - **调试库**：提供调试支持，如钩子、调用栈信息等。

-    **应用场景**

    ---
    
    - **嵌入式系统**：由于其轻量级和易于集成的特性，Lua 常用于嵌入式系统。
    - **游戏开发**：Lua 在游戏开发中广泛用于脚本编写，如《魔兽世界》等。
    - **Web开发**：Lua 可以用于Web服务器端脚本，如OpenResty。
    - **科学计算**：LuaJIT（Lua的一个扩展）提供了JIT编译，适用于需要高性能计算的场景。

</div>
!!! abstract
    lua是什么？

    —— 轻量、动态语言，适合作为顶层策略控制
    
    学什么？
    
    —— 基础语法，条件与循环，函数，数组与表
    
    学习目标？
    
    —— 能大概看懂并仿写
    
    怎么学？
    
    —— [菜鸟教程(教程主要参考资料)](https://www.runoob.com/lua/lua-tutorial.html)，[B站视频](https://www.bilibili.com/video/BV1Yb411J7Lk/?p=1)，[在线运行网站](https://c.runoob.com/compile/66/)

## 基础

```lua
a="World"
-- 全局变量
local b=1
-- 局部变量，一般不这么用
print('Hello',a,b,[[!]])
--[[
  猜一猜：
  为什么这里写东西不报错？
  猜不出来也没关系！
]]
```

1.   一行一句话
2.   print输出
3.   变量的定义和赋值（弱类型、全局和局部）
4.   注释

## 条件与循环

```lua
a=11
while b==nil do
    local a=4
    if a> 5 then
        a=nil
    else
        b=14
        print(a)
    end
end
print(a)
```

1.   基本语法
2.   true, false, nil
3.   注意a的值（局部变量）

## 函数

```lua
function foo(a,b,c)
    return b,c,a
end
print(foo(1,2,3))
```

1.   基本语法
2.   多返回值

## 数组与表

### 数组

```lua
array={1,1}
for i=3,10 do
    array[i]=array[i-2]+array[i-1]
    print(array[i])
end
```

1.   基本语法
2.   关键：索引与值

### 表：很自由的结构

```lua
Config={}
Config["name"]="SYLG"
Config[-1]=1919810
Config.say=function()
    print(string.format("%s is %d years old",Config.name,Config[-1]))
end
Config["say"]()

Config.SubConfig={h="hello",w="world"}
print(Config["SubConfig"]["h"],Config["SubConfig"]["w"])
Config.SubConfig={}
print(Config["SubConfig"]["h"],Config["SubConfig"]["w"])
```

1.   数组就是一种表
2.   索引和值不再局限
3.   三种索引方式