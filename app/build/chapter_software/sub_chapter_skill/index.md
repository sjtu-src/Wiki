# 如何写一个skill

## 1. 什么是skill

Skill 是可以在Lua状态机层，被某辆车使用的函数。如 `task.staticGetBall(ball.pos())` 的就是一个skill。

```lua
["chase"] = { -- 状态机内的一个状态
    switch = function ()
        if world:getBallPossession(true, gRoleNum["Kicker"]) > 0.3 then
            return "break";
        end
    end,
    
    Kicker = task.staticGetBall(ball.pos()), -- task.staticGetBall 是一个 skill
    match = ""
},
```

Skill 是最常见的策略函数。一个完整的 Skill 有能力具体地描述小车一段时间内所有的行为，可以处理场地环境信息，其他车辆（我方和敌方）和球的运动状态信息。写好 Skill 是掌握 SRC 软件开发的基础。

## 2. Skill 的基本结构

完成 Skill 的编写，需要了解的基本结构包括：

- Lua 层：状态机分派任务，决定哪一个 Skill 被执行。
- C++ 层：实现 Skill 的具体功能，主要承担具体计算和控制的任务。

下文将分两层详细的介绍 Skill 的编写方法。

## 3 Lua 层

Lua层主要承担最顶层状态机的功能，并可通过一系列脚本筛选并调用 Lua skills。

- 所有决策相关脚本位置: bin/base/lua_scripts/ssl
- 重要脚本：Config.lua, SelectPlay.lua

### 3.1 Lua 结构 & 创建Skill的流程

![lua_structure](index.assets/lua_diagram.png)

下文将举例说明如何在 Lua 层完成 Skill 的注册和测试代码编写。

#### 3.1.1 bin/base/lua_scripts/ssl/play/ 内的新文件创建

```lua

--bin/base/lua_scripts/ssl/play/Test_ChaseKick.lua 古老的追踢代码

local ALL_AVOID = flag.dodge_ball + flag.avoid_stop_ball_circle + flag.avoid_shoot_line
local ALL_NOT_AVOID = flag.not_avoid_their_vehicle + flag.not_avoid_our_vehicle + flag.not_dodge_penalty
local FLAG = ALL_AVOID + flag.dribbling

local distThreshold = 50

--本质上就是一个表
gPlayTable.CreatePlay{

firstState = "chase", -- 初始状态

["chase"] = { -- 一个状态机
    switch = function ()
        if world:getBallPossession(true, gRoleNum["Kicker"]) > 0.3 then
        --if bufcnt(world:getBallToucher() == gRoleNum["Kicker"], 5) then
        --if bufcnt(robotSensor:IsInfraredOn(1), 5)then
            return "break";
        end
    end,
    
    Kicker = task.staticGetBall(ball.pos()),
    match = ""
},
["break"] = {
    switch = function ()
        if world:getBallPossession(true, gRoleNum["Kicker"]) == 0 then
        --if bufcnt(world:getBallToucher() ~= gRoleNum["Kicker"], 10) then
        --if bufcnt(not robotSensor:IsInfraredOn(1), 10)then
            return "chase";
        end
    end,
    Kicker = task.testBreak(CGeoPoint:new_local(param.pitchLength / 2, 0)),
    match = ""
},

name = "Test_ChaseKick",
applicable ={
    exp = "a",
    a = true
},
attribute = "attack",
timeout = 99999

}

```

#### 3.1.2 task.lua 内的新函数

```lua
function chase()
    local mexe, mpos = ChaseKick{dir = dir.chase}--调用skill部分
    return {mexe, mpos, kick.flat, dir.chase, pre.middle, kp.full(), cp.full(), flag.nothing}
end
```

#### 3.1.3 bin/base/lua_scripts/ssl/skill/ 内的新文件创建

```lua

function ChaseKick(task) --bin/base/lua_scripts/ssl/skill/ChaseKick.lua
    local mdir
    local mflag = task.flag or 0 --flag是形如 8'b00001010 的二进制码
    execute = function(runner)
        if type(task.dir) == "function" then
            mdir = task.dir(runner)
        else
            mdir = task.dir
        end
        return CChaseKick(runner, mdir, mflag) -- 在这里调用c++的部分，也就是LuaModule.cpp工厂的一个类
    end

    matchPos = function()
        return ball.pos()
    end

    return execute, matchPos --最终传给用来匹配车号的Lua脚本
end

gSkillTable.CreateSkill{
    name = "ChaseKick",
    execute = function (self)
        print("This is in skill"..self.name)
    end
}。-- 同时在gskilltable注册
```
