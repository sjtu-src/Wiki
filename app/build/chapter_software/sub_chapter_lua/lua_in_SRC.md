# SRC系统中lua

## 状态机

!!! question "什么是状态机"
    状态机用来描述系统在面对不同情况下的行为.状态机的组成包括 **当前状态** 、**输出事件** 、**状态转移** 等.

    状态机的设计遵循以下步骤
    
    1. 定义状态：确定系统需要的所有状态
    
    2. 定义转换：确定状态之间的转换规则，包括触发转换的事件和条件
    
    3. 设计状态转移图：使用图形化的方式表示状态和转换，这有助于理解和设计状态机
    
    4. 实现状态机：根据设计的状态转移图，使用编程语言或硬件描述语言实现状态机

举个例子:
```mermaid
graph RL
node([状态机示意图])
style node fill:#f9f,stroke:#333,stroke-width:4px
S[睡觉];E[吃饭];L[上课];
S -- 上课铃响 --> L;
L -- 困且枯燥 --> S;
E -- 上课铃响 --> L;
L -- 饭到了且下课了 --> E;
S -- 肚子饿 --> E;
E -- 吃饱喝足 --> S;
```

- 三个状态:睡觉,吃饭,上课
- 对应三个输出事件:闭眼,心率降低,呼吸拉长; 牙齿咬合,舌头搅拌,消化系统活跃; 发呆,游离,打哈欠
- 四个状态转移:睡觉->上课,上课->睡觉,吃饭->上课,上课->吃饭,睡觉->吃饭,吃饭->睡觉
- 状态转移条件:上课铃响,肚子饿,饭到了且下课了,困且枯燥...
-------
## 用lua写状态机

1. 进入一个状态，
   
2. 从World Model中获取信息，判断下一步进入哪个状态

3. 动作分配

4. 匹配规则

一个例子：
```lua
-- 在实现中，每个状态都是一个Lua的table类型变量，
-- 包括switch，match，Kicker、Goalie（各个角色）这些键
["run1"] = {
    -- 状态的跳转函数
    switch = function ()
        -- 从World Model中获取信息，判断下一步进入哪个状态
        if player.toTargetDist("Kicker") < 20 then
            return "run2"
        end
    end,
    -- 分配任务，调用封装的SKill
    Kicker = task.goCmuRush(TargetPos1, 0),
    -- 匹配规则，这样写就是不匹配
    match = ""
},
```

!!! success "巧用bufcnt实现状态机跳转"
    bufcnt相比其他的状态跳转如if,else,switch case等,可以实现更加复杂的跳转逻辑

    bufcnt(cond, buf, cnt)
    
    其中cond为跳转条件,buf为满足的cond的持续帧数,当满足cond时间超过buf后返回true
    
    当一直没有切换状态的时间超过buf后也返回true
    ```lua
    switch = function ()
    	if bufcnt(player.toTargetDist("Kicker") < distThreshold , 300, 1000) then
    		return "run2";
    	end
    end,
    ```
-------
## 匹配规则
- 由于在机器人足球比赛中,以多智能体的形式执行动作,因此匹配动作的执行者非常重要

- 目前的匹配机制以离任务点的距离来作优先级进行区分

- 以下是可使用的球员角色
![role](lua_in_SRC.assets\role.png)

**三种匹配机制**:

一对括号内的任务点为“一组”(1)，按组依次匹配组内的最优任务点执行车辆
    { .annotate }

1.  详情参见RoleMatch.lua

------
- []: Real Time，实时最优匹配

- (): Once，进入状态后匹配一次

- {}: Never，除非该状态为进入脚本初状态才会匹配一次
![match](lua_in_SRC.assets\match.png)

-------

## 部分常用函数讲解
**用于判断状态跳转**

- 球的信息(详情可见ssl\worldmodel\ball.lua)
    ```lua
    --位置
    ball.pos()
    ball.posX()
    ball.posY()
    ---速度 
    ball.vel()
    ball.velX()
    ball.velY()
    --距离
    ball.toPlayerHeadDist() 球到某球员的距离
    ball.toPlayerHeadDir() 球到某球员的方向
    --其他
    ball.antiYPos(p) 将 p 点的 Y 坐标取为负值
    ball.syntYPos(p) 将 p 点的 Y 坐标取为正值
    ball.refAntiYPos(p) 在定位球中使用的反向点
    ball.refSyntYPos(p) 在定位球中使用的同向点v
    ```

- 机器人的信息(详情可见ssl\worldmodel\player.lua)
    ```lua
    --位置及朝向
    player.pos()
    player.posX()
    player.posY()
    player.dir() 
    player.vel()
    --速度
    player.vel()
    player.velDir()
    player.velMod()
    --距离
    player.toBallDist()
    player.toBallDir()
    player.toTargetDist()
    palyer.toPointDist()
    --机器人是否拿到球了(返回值越大越可能拿到球了)
    world:getBallPossession(true, gRoleNum["Kicker"])
    ```
    **用于分配的任务**

- 机器人可执行的动作(详情可见ssl\worldmodel\task.lua)
    ```lua
    task.chaseNew() --智能射门
    task.goCmuRush(p, d, a, f) --智能跑位（p 为要走的点, d 默认为射门朝向, a 为加速度, f 为相关的 flag）
    task.getball(p) --拿球（p 为拿球后朝向的最终点）
    task.staticGetBall(p) --静态拿球 (更加稳地拿球,但响应地拿球速度也更慢)
    task.pass(role, power) --传球（role 为接球车和某个点，power 为力度）
    task.passToDir(dir, c)
    task.passToPos(p, c)
    task.chipPass(p, c) --挑传
    task.flatPass(role, power) --平传
    task.receivePass(p) --接传 (p 参数可以传入球员名称)
    ```
------

## 一个完整的例子

---以UniTest_Run.lua为例
```lua
local TargetPos1  = CGeoPoint:new_local(400, 120)
local TargetPos2  = CGeoPoint:new_local(400,-140)
local TargetPos3  = CGeoPoint:new_local(400,70)
local TargetPos4  = CGeoPoint:new_local(400,0)
local TargetPos5  = CGeoPoint:new_local(400, 70)
local TargetPos6  = CGeoPoint:new_local(400, 140)


local TargetPos7  = CGeoPoint:new_local(-400, 120)
local TargetPos8  = CGeoPoint:new_local(-400,-140)
local TargetPos9  = CGeoPoint:new_local(-400,70)
local TargetPos10 = CGeoPoint:new_local(-400,0)
local TargetPos11 = CGeoPoint:new_local(-400, 70)
local TargetPos12 = CGeoPoint:new_local(-400, 140)

local distThreshold = 10
--定义一些可能要用到的值,包括距离阈值,跑位点等

gPlayTable.CreatePlay{

    firstState = "run1",
    --设定初始状态
    ["run1"] = {
        switch = function()
            if bufcnt(player.toTargetDist("Leader") < distThreshold , 150, 1000) then
                return "run2";
            end
            --当bufcnt返回true时跳转到run2,否则循环执行run1(类似arduino的loop)
        end,
        Leader = task.goCmuRush(TargetPos1),
	    Assister = task.goCmuRush(TargetPos7),
	    Middle = task.goCmuRush(TargetPos2),
        Special = task.goCmuRush(TargetPos8),
	    Defender = task.goCmuRush(TargetPos3),
	    Hawk = task.goCmuRush(TargetPos9),
        -- 执行跑点任务
        match = "{LA}{M}{S}{D}{H}"
        --匹配规则,其中Leader和Assister一组匹配,选择出两个机器人分别为Leader和Assiter使得机器人目前位置到角色的任务点的距离最小
    },

    ["run2"] = {
        switch = function()
            if bufcnt(player.toTargetDist("Leader") < distThreshold , 150) then
                return "run1";
            end
        end,
        Leader = task.goCmuRush(TargetPos7),
	    Assister = task.goCmuRush(TargetPos1),
	    Middle = task.goCmuRush(TargetPos8),
        Special = task.goCmuRush(TargetPos2),
	    Defender = task.goCmuRush(TargetPos9),
	    Hawk = task.goCmuRush(TargetPos3),
        match = "{L}{A}{M}{S}{D}{H}"
    },
    --可以直接简单理解为格式,其中name对应文件名
    name = "UnitTest_Run",
    applicable ={
        exp = "a",
        a = true
    },
    attribute = "attack",
    timeout = 99999
    }
    --脚本实现了机器人在两个点之间折返跑的效果
```

<!-- ## lua作顶层

- 裁判盒相应指令与文档调用的关系 -->
