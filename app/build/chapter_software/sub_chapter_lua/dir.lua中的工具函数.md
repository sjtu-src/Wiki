ball.lua定义了多个函数来处理各种角度信息，如球员射门、控球、防守等操作相关的方向计算等。

1. `specified(num)`:将某个角度值转换为弧度
```lua
function specified(num)
	return function()
		return num * math.pi / 180
	end
end
```

2. `ballToOurGoal()`:计算球到己方球门的方向向量。
```lua
function ballToOurGoal()
	return (pos.ourGoal() - ball.pos()):dir()
end
```

3. `posToTheirGoal(p)`:接受一个位置参数 `p`，计算从该位置到对方球门的方向向量
```lua
function posToTheirGoal(p)
	return (pos.theirGoal() - p):dir()
end
```

4. `theirGoalToBall()`:计算从对方球门到球的方向向量
```lua
function  theirGoalToBall()
	return (ball.pos() - pos.theirGoal()):dir()
end
```

5. `ourGoalToBall()`:计算从己方球门到球的方向向量
```lua
function ourGoalToBall()
	return (ball.pos() - pos.ourGoal()):dir()
end
```

6. `playerToBall(role)`:如果传入的角色 `role` 为 `nil`，会打印错误信息。否则，计算从球员（由 `role` 指定）到球的方向向量
```lua
function playerToBall(role)
	if role == nil then
		print("Invalid Role in ourPlayerToBall: ", role)
	end
	return (ball.pos() - player.pos(role)):dir()
end
```

7. `ballToPlayer(role)`:计算从球员到球的方向向量。如果传入的 `role` 为 `nil`，会打印错误信息。
```lua
function ballToPlayer(role)
	if role == nil then
		print("Invalid Role in ourPlayerToBall: ", role)
	end
	return (player.pos(role) - ball.pos()):dir()
end
```

8. `ourPlayerToPlayer(role1,role2)`计算`role1`到`role2`的方向向量。
```lua
function ourPlayerToPlayer(role1, role2)
	if role2 == nil then
		return function(role2)
			return (player.pos(role1) - player.pos(role2)):dir()
		end
	else
		return (player.pos(role2) - player.pos(role1)):dir()
	end
end
```

9. `shoot()`:用于返回射门方向
   - 内部定义了两个局部数组 `lastCycle` 和 `lastDir`，用于记录每个球员的上一次循环和方向信息，初始化所有元素为0。
   - 返回一个内部函数，这个内部函数根据传入的角色 `role` 类型进行处理，先把role转化为车号，如果角色类型合法，并且满足一定的条件（到球的距离大于50或者循环次数大于6次），则重新计算射门方向，更新相关的记录数组，并返回最后的射门方向。
```lua
function shoot()
	local lastCycle = {}
	local lastDir = {}

	for i = 0, param.maxPlayer do
		lastCycle[i] = 0
		lastDir[i] = 0
	end

	return function (role)
		if type(role) == "string" then
			role = gRoleNum[role]
		elseif type(role) == "number" and
			role >= 0 and role < param.maxPlayer then
			role = role
		else
			print("Error role in dir.shoot")
		end
		
		if vision:Cycle() - lastCycle[role] > 6 or player.toBallDist(role) > 50 then
			kickDirection:GenerateShootDir(role, player.pos(role))
			lastDir[role] = kickDirection:getRealKickDir()
		end
		lastCycle[role] = vision:Cycle()
		return lastDir[role]
	end
end
```

10. `evaluateTouch(p)`:用于返回touch方向
   - 与 `shoot` 函数类似，内部也有 `lastCycle` 和 `lastDir` 数组。
   - 返回的内部函数根据传入的角色 `role` 类型进行处理，计算球员触球相关的评估方向。
   - 若p不为nil，则可向p点返回touch角度，否则返回向敌方球门的touch角度。如果满足到球的距离大于50或者循环次数大于6次，会根据不同情况重新计算原始方向`tmpRawDir`，然后根据与球方向的夹角的大小对方向进行调整，并返回`lastDir[role]`。
```lua
function evaluateTouch(p)
	local lastCycle = {}
	local lastDir = {}

	for i = 0, param.maxPlayer do
		lastCycle[i] = 0
		lastDir[i] = 0
	end

	return function (role)
		if type(role) == "string" then
			role = gRoleNum[role]
		elseif type(role) == "number" and
			role >= 0 and role < param.maxPlayer then
			role = role
		else
			print("Error role in dir.shoot")
		end
		if vision:Cycle() - lastCycle[role] > 6 or player.toBallDist(role) > 50 then
			local tmpRawDir
			if p == nil then
				kickDirection:GenerateShootDir(role, player.pos(role))
				tmpRawDir = kickDirection:getRawKickDir()
			else
				if type(p) == "function" then
					p = p()
				end
				tmpRawDir = player.toPointDir(p,role)
			end

			local tmpTotalAngle = (tmpRawDir - player.toBallDir(role))*180/math.pi
			local tmpAbsValue = math.abs(tmpTotalAngle)
			local tmpEvaluateValue = 0.0008*tmpAbsValue*tmpAbsValue + 0.1145*tmpAbsValue
			if tmpTotalAngle <= 0 then
				lastDir[role] = tmpRawDir + tmpEvaluateValue*math.pi/180
			else
				lastDir[role] = tmpRawDir - tmpEvaluateValue*math.pi/180
			end

		end
		lastCycle[role] = vision:Cycle()
		return lastDir[role]
	end
end
```

11. `compensate(p)`:
   - 内部同样有 `lastCycle` 和 `lastDir` 数组。
   - 返回一个内部函数，该函数根据传入的目标点 `p`和角色 `role`，计算补偿后的方向。如果满足到球的距离大于50或者循环次数大于6次，会调用 `CCalCompensateDir` 函数来计算补偿方向。
```lua
function compensate(p)
	local lastCycle = {}
	local lastDir = {}

	for i = 0, param.maxPlayer do
		lastCycle[i] = 0
		lastDir[i] = 0
	end

	return function (role)
		local ipos
		if type(p) == "function" then
			ipos = p()
		else
			ipos = p
		end

		if vision:Cycle() - lastCycle[role] > 6 or player.toBallDist(role) > 50 then
			lastDir[role] = CCalCompensateDir(player.num(role), ipos:x(), ipos:y())
		end
		lastCycle[role] = vision:Cycle()
		return lastDir[role]
	end
end
```

12. `nocompensation(p)` 函数**
   - 内部定义了一个方向数组 `dir`。
   - 返回的内部函数根据传入的目标点 `p`和角色 `role`，计算没有角度补偿的射门方向，即简单地计算目标点与球员位置的方向向量。
```lua
function nocompensation(p)
	local dir = {0,0,0,0,0,0}

	return function (role)
		local ipos
		if type(p) == "function" then
			ipos = p()
		else
			ipos = p
		end
		dir[role] = (p - player.pos(role)):dir()
		return dir[role]
	end
end
```

13. `chase()`
   - 为角色 `role` 生成射门方向（调用 `kickDirection:GenerateShootDir`），并返回原始的射门方向（调用 `kickDirection:getRawKickDir`）
```lua
function chase(role)
	kickDirection:GenerateShootDir(player.num(role), player.pos(role))
	return kickDirection:getRawKickDir()
end
```

14. `backBall(p)`
   - 返回一个匿名函数，这个匿名函数计算将球回传的方向。它根据传入的点 `p` 创建一个新的目标点 `targetP`，根据球的y坐标计算`tatgetP`的坐标，并计算从球到这个目标点的方向向量。
```lua
function backBall(p)
	return function ()
		local targetP = CGeoPoint:new_local(p:x(), ball.antiY()*p:y())
		return  Utils.Normalize((targetP - ball.pos()):dir())
	end
end

```

15. `fakeDown(p)`
   - 内部定义了一个变量 `factor`，根据球的 `y` 坐标位置确定 `factor` 的值。
   - 返回一个匿名函数，这个匿名函数根据传入的点 `p` 创建一个目标点 `targetP`，然后计算一个旋转后的方向向量并返回其方向。
```lua
function fakeDown(p)
	local factor

	return function ()
		if ball.posY() > 10 then
			factor = -1
		else
			factor = 1
		end

		local targetP = CGeoPoint:new_local(p:x(), factor * p:y())
		local faceVec = (targetP - ball.pos()):rotate(factor * math.pi * 120 / 180)
		return faceVec:dir()
	end
end
```

16. `defendBackClear()`
   - 内部定义了一些变量，如 `targetdir`、`angle_left` 和 `angle_right` 等，用于确定防守清球的方向。
   - 返回一个匿名函数，这个匿名函数根据球在球场上的位置（特别是在球门附近的位置）计算防守清球的方向。
```lua
function defendBackClear()
	local targetdir = 0
	local angle_left = 0
	local angle_right = 0
	local NearGoalDist = -param.pitchLength/2 + 10
	return function()
		if ball.posY() >= -param.goalWidth/2 and ball.posY() <= param.goalWidth/2 then --若球在球门正前方
        --处理angle_left和angle_right，最后返回0
			if ball.posX() > NearGoalDist then
				angle_left = -math.pi/2
				angle_right = math.pi/2
			else
				angle_left = -math.pi/3
				angle_right = math.pi/3
			end
        --若球在球门前方偏外侧，处理angle_left和angle_right，最后返回正负pi/6
		elseif ball.posY()<-param.goalWidth/2 then
			angle_left = - math.pi*2/3
			angle_right = math.pi/2
		elseif ball.posY()>param.goalWidth/2 then
			angle_left = -math.pi/2
			angle_right = math.pi*2/3
		end
		return (angle_left+angle_right)/2
	end
end
```

17. `defendMiddleClear(role)`
   - 内部定义了一些变量，如 `angle_left` 和 `angle_right` 等。
   - 返回一个匿名函数，这个匿名函数根据球在球场上的位置（特别是在己方半场较后的位置）以及角色 `role`计算防守清球的方向。
```lua
function defendMiddleClear(role)
	local angle_left = 0
	local angle_right = 0
	local NearGoalDist = -param.pitchLength/2+10
	local temp = 0

	return function()
		if ball.posX()<-140 then --若球x坐标小于-140，位于球场靠后位置
			if ball.posY() > -param.goalWidth/2 and ball.posY() < param.goalWidth/2 then --若球在球门正前方，返回0
				if ball.posX()>NearGoalDist then
					angle_left = -math.pi/3
					angle_right = math.pi/3
				else
					angle_left = -math.pi/4
					angle_right = math.pi/4
				end
            --若球在球门斜前方，返回正负pi/6
			elseif ball.posY() < -param.goalWidth then
				angle_left = -math.pi*2/3
				angle_right = math.pi/3
			elseif ball.posY() > param.goalWidth then
				angle_left = -math.pi/3
				angle_right = math.pi*2/3
			end
			temp = (angle_left +angle_right)/2*180/math.pi
			return (angle_left +angle_right)/2
		else --否则返回球员role到球的角度
			temp = player.toBallDir(role)*180/math.pi
			return player.toBallDir(role)
		end
	end
end
```

18. `backSmartGotoDir()`:
   - 根据对手最佳追球者 `oppnum` 的位置以及球是否在己方禁区等情况，计算防守球员回防的方向向量。
```lua
function backSmartGotoDir()
	local oppnum = defenceInfoNew:getBestBallChaser()
	if Utils.InOurPenaltyArea(ball.pos(),5) and enemy.posX(oppnum)<0 then
		return (enemy.pos(oppnum) - pos.ourGoal()):dir()
	else
		return (ball.pos()- pos.ourGoal()):dir()
	end
end
```

19. `sideBackDir()`
   - 计算从侧边后卫位置到己方球门的方向向量。
```lua
function sideBackDir()
	return (pos.sideBackPos()- pos.ourGoal()):dir()
end
```