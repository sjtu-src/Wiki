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