player.lua脚本包含了一系列与我方车辆有关的函数，包括但不限于我方的坐标，速度，到我方车辆的距离，运动方向等等。以下是对各个函数的详细解释：

* `instance(role)`函数：返回该role在场上的实体，用于参数调用。
```lua
function instance(role)
	local realIns
	if type(role) == "string" then
		realIns = vision:OurPlayer(gRoleNum[role])
	elseif type(role) == "number" then
--	and	role >= 1 and role <= param.maxPlayer then
		realIns = vision:OurPlayer(role)
	else
		print("Invalid role in player.instance!!!")
	end
	return realIns
end
```

* `num(role)`函数：返回role所代表的车辆编号。
```lua
function num(role)
	local retNum
	if type(role) == "string" then
		retNum = gRoleNum[role]
	elseif type(role) == "number" then
		retNum = role
	else
		print("Invalid role in player.instance!!!")
	end
	return retNum
end
```

* `pos(role)`函数：返回role在场上的坐标值。也可以通过调用`posX(role)`与`posY(role)`直接获取坐标X, Y值。
```lua
function pos(role)
	return instance(role):Pos()
end
```

* `vel()`函数：返回车辆的速度（一个向量）
```lua
function vel(role)
	return instance(role):Vel()
end
```
* `dir()`函数：返回车辆的朝向（一个向量）
```lua
function dir(role)
	return instance(role):Dir()
end
```

* `velDir()`函数：返回车辆的速度方向。
```lua
function velDir(role)
	return vel(role):dir()
end
```

* `velMod()`函数：返回车辆在场上的速率。
```lua
function velMod(role)
	return vel(role):mod()
end
```

* `valid()`函数：返回是否能在场上看到该车辆。
```lua
function valid(role)
	return instance(role):Valid()
end
```

* `toBallDist(role)`函数：返回该车辆到球的距离。
```lua
function toBallDist(role)
	return pos(role):dist(ball.pos())
end
```

* `toBallDir(role)`函数：返回该车辆到球的方向。
```lua
function toBallDir(role)
	return (ball.pos() - pos(role)):dir()
end
```

* `toTheirGoalDist(role)`函数：返回该车辆到对方球门中心的距离。
```lua
function toTheirGoalDist(role)
	return pos(role):dist(CGeoPoint:new_local(param.pitchLength / 2.0, 0))
end
```

* `toOurGoalDist(role)`函数：返回该车辆到己方球门中心的距离。
```lua
function toOurGoalDist(role)
	return pos(role):dist(CGeoPoint:new_local(param.pitchLength / 2.0, 0))
end
```

* `toPlayerDir(role1, role2)`函数：返回从车辆role1到车辆role2的方向。
```lua
function toPlayerDir(role1, role2)
	if role2 == nil then
		return function(role2)
			return (player.pos(role1) - player.pos(role2)):dir()
		end
	else
		return (player.pos(role2) - player.pos(role1)):dir()
	end
end
```

* `toPlayerHeadDir(role1, role2)`函数：返回从车辆role1头部到车辆role2头部的方向。
```lua
function toPlayerHeadDir(role1, role2)
	if role2 == nil then
		return function(role2)
			local tmpPlayerHead = player.pos(role1) + Utils.Polar2Vector(8, player.dir(role1))
			return (tmpPlayerHead - player.pos(role2)):dir()
		end
	else
		local tmpPlayerHead = player.pos(role2) + Utils.Polar2Vector(8, player.dir(role2))
		return (tmpPlayerHead - player.pos(role1)):dir()
	end
end
```

* `kickBall(role)`函数：返回该role是否已踢出球的bool值。
```lua
function kickBall(role)
	return world:IsBallKicked(num(role))
end
```

* `toShootOrRobot(role1)`函数：返回向role2传球的方向或者是射门的方向（射门效果已禁用）。
```lua
function toShootOrRobot(role1)
	return function(role2)
		local shootDir = ( CGeoPoint:new_local(param.pitchLength / 2.0, 0) - pos(role2) ):dir()
		local faceDir
		if toBallDist(role1) > 50 then
			faceDir = (ball.pos() - pos(role2)):dir()
		else
			faceDir = (pos(role1) - pos(role2)):dir()
		end
		return faceDir
		--if math.abs(Utils.Normalize(shootDir - faceDir)) > math.pi * 65 / 180 then
		--	return faceDir
		--else
		--	return shootDir
		--end
	end
end
```

* `waitAdvancePos(role)`函数：返回advance函数中若射门线被封堵时第一接球手所处的位置。
```lua
function waitAdvancePos(role)
	return function (role2)
		local ballPos=CGeoPoint:new_local(ball.posX(),ball.posY())
		if NormalPlayUtils.isEnemyBlockShootLine(ballPos,ball.toTheirGoalDir(),50) then
			return firstPassPos(role)
		else

			return ballPos
		end

	end
end
```

* `canBreak(role)`函数：若该role在前往target点时会被敌方车辆阻截，则返回false，若不会受到阻碍则返回true。
```lua
function canBreak(role)
	for i=1,6 do
		if enemy.valid(i) then
			local breakSeg = CGeoSegment:new_local(player.pos(role), gRolePos[role])
			local projP = breakSeg:projection(enemy.pos(i))
			if breakSeg:IsPointOnLineOnSegment(projP) then
				if enemy.pos(i):dist(projP) < 40 then
					return false
				end
			end
		end
	end

	return true
end
```

* `isMarked(role)`函数：若该role已站好防守站位，即盯防某一对方球员防止其正对球门空当，则判断为true，反之则false。
```lua
function isMarked(role)
	local closestDist = 9999
	for i=1,6 do
		if enemy.valid(i) then
			local dir1 = player.toPointDir(CGeoPoint:new_local(param.pitchLength / 2.0, 0),role)
			local dirDiff = Utils.Normalize( dir1- player.toPointDir(enemy.pos(i),role))
			if math.abs(dirDiff) < math.pi/2 then
				local tmpDist = player.toPointDist(role,enemy.pos(i))
				if tmpDist < closestDist then
					closestDist = tmpDist
				end
			end
		end
	end

	if closestDist < 30 then
		return true
	end
	return false
end
```

* `canFlatPassTo(role1, role2)`函数：判断从role1到role2平传球路径中是否会被敌方阻截，若不会有被阻截风险则返回true，反之则false。
```lua
function canFlatPassTo(role1, role2)
	local p1 = player.pos(role1)
	local p2 = player.pos(role2)
	local seg = CGeoSegment:new_local(p1, p2)
	for i = 0, param.maxPlayer-1 do
		if enemy.valid(i) then
			local dist = seg:projection(enemy.pos(i)):dist(enemy.pos(i))
			local isprjon = seg:IsPointOnLineOnSegment(seg:projection(enemy.pos(i)))
			if dist < 15 and isprjon then
				return false
			end
		end
	end

	return true
end
```

* `canDirectShoot(role1, d)`函数：判断从role1往前射出d距离的球是否会被敌方阻截，若不会有被阻截风险则返回true，反之则false。
```lua
function canDirectShoot(role1, d)
	if d == nil then
		d = 70
	end
	local p1 = player.pos(role1)
	local p2 = player.pos(role1) + Utils.Polar2Vector(d,player.dir(role1))
	local seg = CGeoSegment:new_local(p1, p2)
	for i = 0, param.maxPlayer-1 do
		if enemy.valid(i) then
			local dist = seg:projection(enemy.pos(i)):dist(enemy.pos(i))
			local isprjon = seg:IsPointOnLineOnSegment(seg:projection(enemy.pos(i)))
			if dist < 12 and isprjon then
				return false
			end
		end
	end

	return true
end
```

* `canChipPassTo(role1, role2)`函数：判断从role1到role2挑传球路径中是否会被敌方阻截，若不会有被阻截风险则返回true，反之则false。
```lua
function canChipPassTo(role1, role2)
	local p1 = player.pos(role1)
	local p2 = player.pos(role2)
	for i = 0, param.maxPlayer-1 do
		if enemy.valid(i) then
			local dist1 = enemy.pos(i):dist(p1)
			local dist2 = enemy.pos(i):dist(p2)
			if dist1 < 30 or dist2 < 30 then
				return false
			end
		end
	end

	return true
end
```

* `isBallPassed(role1,role2)`函数：判断球是否已经正确传给role2，若是则返回true，反之则false；衡量标准为射出的球速与方向是否正确。
```lua
function isBallPassed(role1,role2)
	local p1 = player.pos(role1)
	local p2 = player.pos(role2)
	local ptrDir = ( p2 - p1 ):dir()
	if (math.abs(Utils.Normalize(ball.velDir() - ptrDir)) < math.pi / 18) and
	   (ball.velMod() > 80) then
		return true
	else
		return false
	end
end
```

* `passIntercept(role)`函数：判断role是否需要上前接球以防止被敌方阻截，衡量标准为role到球的距离，球方向偏移，以及球速。
```lua
function passIntercept(role)
	local receiver = player.pos(role)
	local ptrDir = ( receiver - ball.pos()):dir()
	if ball.toPointDist(receiver) >50 then
		if math.abs(Utils.Normalize(ball.velDir() - ptrDir)) > math.pi / 10 or
			ball.velMod() < 120 then
			return true
		else
			return false
		end
	else
		return false
	end
end
```