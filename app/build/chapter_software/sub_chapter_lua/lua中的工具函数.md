# lua中的工具函数
本部分主要介绍worldmodel文件夹里lua文件包含的内容这部分包含了在opponent，play，skill的各个脚本中都可以调用的一些工具性函数，包括：

* ball.lua：与球有关的函数，可提供包括但不限于球的坐标，速度，到车距离，运动方向等等

* combo.lua：对task.lua更高一层的抽象,包括一些通过标志位决定的task和一些组合的task

* cond.lua：TODO （由名字看大概是判断各种状态？？比如匹配的决定什么的）例如isGameOn()判断比赛是否开始；

* cp.lua：与挑射有关的函数，可提供不同的挑射力度

* dir.lua：与角度有关的函数，可提供包括但不限于球与球门连线的角度，球车连线角度，车与球门连线的角度等等

* enemy.lua：与敌方车辆有关的函数，可提供包括但不限于敌方的坐标，速度，到我方车辆的距离，运动方向等等

* flag.lua：各种状态标签，用于控制车的运动，例如nothing(无特殊要求)dodge_ball(避球)
avoid_shoot_line(避开射门线)placer_to_ball_dis(放球车到球距离)等等

* kick.lua：与踢球有关的函数，用于判定是挑球还是平射等等

* kp.lua：与平射有关的函数，可提供不同的平射力度

* param.lua：与场地有关的参数，如球员数、场地的长宽、球门的长宽深等等

* player.lua：与我方车辆有关的函数，可提供包括但不限于我方的坐标，速度，到我方车辆的距离，运动方向等等

* pos.lua：与坐标有关的函数，提供各种坐标，如踢球点等等

* pre.lua：与精度有关的坐标，可能在临界情况判定或踢球角度校准中用到

* task.lua：与车所执行的任务有关的函数，包含了在opponent，play，skill的各个脚本中车辆调用的task函数，如射门、传球、防守、盯人等等

这里简单介绍一下task中函数的基本架构，以传球函数pass()为例：
```lua
function pass(role, power) --函数名
	local idir,ikp
  --这一段决定车的朝向
	if type(role) == "string" then 
		idir = ball.toPlayerHeadDir(role)
	elseif type(role) == "function" then
		idir = ball.toFuncDir(role)
	elseif type(role) == "userdata" then
		idir = player.antiYDir(role)
	end

  --这一段决定踢球的力度
	if power == nil then
		ikp =  kp.toTarget(role)
	else
		ikp = kp.specified(power)
	end

  --在此处调用Skill中的ChaseKickV2函数，传入两个参数pos和dir，其中pos代表匹配时的任务点（参见前文play小节关于匹配的说明），dir代表车的朝向
	local mexe, mpos = ChaseKickV2{pos = ball.pos, dir = idir}
  --返回部分依次包括{mexe, mpos, 平射/挑射，车的朝向，精度，平射力度，挑射力度，任务标签}，前两项为必填项，后面的参数可省略（此处若省略则需要全部省略）。
	return {mexe, mpos, kick.auto(role), idir, pre.middle, ikp, cp.toPlayer(role), flag.nothing}
end
```

下面列举一些常用的task：

### 防守型

```lua
--防守时反踢
task.defendKick()
--退回禁区附近防守
task.sideBack()
task.leftBack()
task.rightBack()
--守门
task.golieNew()
--盯人，First/Second代表离球最近的第一/二辆敌方车
task.marking("First"/"Second"/...)
--在禁区边线附近防守，车头一直朝向球
task.defendMiddle()
```


### 进攻型
```lua
--跑位函数，CGeoPoint为要走的点, dir默认为射门朝向, ACC为加速度, flag为相关的任务标签。
task.goCumRush(CGeoPoint, dir, ACC, flag)
--去拿球，拿到球后往球门射一脚。
task.chase()
task.chaseNew()--智能射门
--静态拿球，比较稳，但拿球速度也慢，去CGeoPoint拿球,anti若为false,则不将点进行反向，f为传入的flag。
task.staticGetBall(CGeoPoint, anti, f)
--去pos拿球。
task.getball(pos)
--挑传到CGeoPoint，力度为power，flag为相关的任务标签。
task.chipPass(CGeoPoint, power,_,_, flag)
--平传给role，力度为power。
task.flatPass(role, power)
--传球给role，力度为power。role为接球车或某个点。
task.pass(role, power)
--向dir方向传球，力度为power。
task.passToDir(dir, power)
--传球到CGeoPoint，力度为power，精度为precision。
task.passToPos(CGeoPoint, power, precision)
--接role传来的球，在CGeoPoint接球。
task.receive(role, CGeoPoint)
task.receivePass(role, CGeoPoint)
```