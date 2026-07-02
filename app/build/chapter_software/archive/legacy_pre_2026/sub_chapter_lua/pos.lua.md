<!-- 不要使用一级标题！这样才能自动生成一级标题 -->
pos.lua脚本包含了一系列在比赛过程中可能会使用的特殊点的计算函数，例如support任务车辆的站位等。以下是对各个函数的解析：

* `ourGoal()`函数：返回己方球门的坐标。

```lua
function ourGoal()
	return CGeoPoint:new_local(-param.pitchLength / 2.0, 0)
end
```

* `refStopAroundBall()`函数：在stop状态中若要让机器人执行对球周围一圈区域的封锁，可以使用该函数，返回各车辆在场上的站位坐标。

```lua
function refStopAroundBall()
	local BLOCK_DIST = param.freeKickAvoidBallDist + param.playerRadius
	local AWAY_DIST = 2.5 + param.playerRadius
	local BLOCK_ANGLE = math.asin(AWAY_DIST / BLOCK_DIST)*2
	local factor = ball.antiY

	local SIDE_POS = function()
		return ball.pos() + Utils.Polar2Vector(BLOCK_DIST, dir.ballToOurGoal() + factor()*BLOCK_ANGLE + math.pi * 90 / 180)
	end

	local INTER_POS = function()
		return ball.pos() + Utils.Polar2Vector(BLOCK_DIST, dir.ballToOurGoal() - factor()*BLOCK_ANGLE - math.pi * 90 / 180)
	end

	local MIDDLE_POS = function()
		return ball.pos() + Utils.Polar2Vector(BLOCK_DIST, dir.ballToOurGoal())
	end

	local SIDE2_POS = function()
		return ball.pos() + Utils.Polar2Vector(BLOCK_DIST, dir.ballToOurGoal() + 2*factor()*BLOCK_ANGLE)
	end

	local INTER2_POS = function()
		return ball.pos() + Utils.Polar2Vector(BLOCK_DIST, dir.ballToOurGoal() - 2*factor()*BLOCK_ANGLE)
	end

	return SIDE_POS, MIDDLE_POS, INTER_POS, SIDE2_POS, INTER2_POS
end
```

* `playerBest()`函数：返回最佳接球机器人的坐标。

```lua
function playerBest()
	local robotNum = bestPlayer:getOurBestPlayer()
	if robotNum >=0 and robotNum < param.maxPlayer then
		return player.pos(robotNum)
	else
		return ball.pos()
	end
end
```

* `defendFrontPos(p)`函数：返回最佳的正面防守对方持球车辆的站位坐标。

```lua
function defendFrontPos(p)
	return function ()
		return DefendUtils.getMiddleDefender(p)
	end
end
```

* `multiBackPos`函数：返回执行multiback任务的机器人的站位坐标。

```lua
function multiBackPos(guardNum, index)
	return function()
		return guardPos:backPos(guardNum, index)
	end
end
```

* `antiYDir(p)`函数：返回球到指定点p及其对称点中y坐标小于0的那一个的方向

```lua
function antiYDir(p)
	return function (role)
		if type(p) == "userdata" then
			return (ball.antiYPos(p)() - player.pos(role)):dir()
		end
	end
end
```

