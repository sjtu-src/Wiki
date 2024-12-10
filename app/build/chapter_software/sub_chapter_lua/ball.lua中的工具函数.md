ball.lua脚本包含了一系列与球有关的函数，用于计算球的位置、速度、方向以及与球员和球门的距离等信息。以下是对各个函数：

* `pos()`函数：返回球在场上的坐标。
```lua
function pos()
	return vision:Ball():Pos()
end
```

* `posX()`函数：返回球在场上的x坐标值。
```lua
function posX()
	return vision:Ball():X()
end
```

* `posY()`函数：返回球在场上的y坐标值。
```lua
function posY()
	return vision:Ball():Y()
end
```

* `vel()`函数：返回球的速度（一个向量）
```lua
function vel()
	return vision:Ball():Vel()
end
```

* `velX()`函数：返回球速的x分量。（有方向，朝x正向为正）
```lua
function velX()
	return vision:Ball():VelX()
end
```

* `velY()`函数：返回球速的y分量。（有方向，朝y正向为正）
```lua
function velY()
	return vision:Ball():VelY()
end
```

* `velDir()`函数：返回球速的方向。
```lua
function velDir()
	return vision:Ball():Vel():dir()
end
```

* `velMod()`函数：返回球在场上的速率。
```lua
function velMod()
	return vision:Ball():Vel():mod()
end
```

* `valid()`函数：返回是否能在场上看到球。
```lua
function valid()
	return vision:Ball():Valid()
end
```

* `toPlayerDir(role)`函数：返回球到角色为role的球员的方向。
```lua
function toPlayerDir(role)
	return (player.pos(role)- pos()):dir()
end
```

* `toEnemyDir(role)`函数：返回球到车号/角色为role的敌方球员的方向。
```lua
function toEnemyDir(role)
	return (enemy.pos(role)-pos()):dir()
end
```

* `toPlayerHeadDir(recver)`函数：返回球到角色为recver的接球球员头部的方向。
```lua
function toPlayerHeadDir(recver)
	return function (passer)
		local tmpPlayerHead = player.pos(recver) + Utils.Polar2Vector(10, player.dir(recver)) --此处加上一个从recver中心到recver头部的向量：Utils.Polar2Vector(10, player.dir(recver)
		return (tmpPlayerHead - player.pos(passer)):dir()
	end
end
```

* `toPlayerHeadDist(role)`函数：返回球到角色为role的球员头部的距离。
```lua
function toPlayerHeadDist(role)
	local tmpPlayerHead = player.pos(role) + Utils.Polar2Vector(10, player.dir(role))
	return (ball.pos() - tmpPlayerHead):mod()
end
```

* `toPlayerDist(role)`函数：返回球到角色为role的指定球员中心的距离。
```lua
function toPlayerDist(role)
	return (player.pos(role)- pos()):mod()
end
```

* `toEnemyDist(role)`函数：返回球到角色为role的指定敌方球员的距离。
```lua
function toEnemyDist(role)
	return (enemy.pos(role) - pos()):mod()
end
```

* `toTheirGoalDist()`函数：返回球到对方球门的距离。
```lua
function toTheirGoalDist()
	return pos():dist(CGeoPoint:new_local(param.pitchLength / 2.0, 0))
end
```

* `toTheirGoalDir()`函数：返回球到对方球门的方向。
```lua
function toTheirGoalDir()
	return (CGeoPoint:new_local(param.pitchLength / 2.0,0) - ball.pos()):dir()
end
```

* `toOurGoalDist()`函数：返回球到我方球门的距离。
```lua
function toOurGoalDist()
	return pos():dist(CGeoPoint:new_local(-param.pitchLength / 2.0, 0))
end
```

* `toOurGoalPostDistSum()`函数：返回球到我方球门两个门柱距离之和。
```lua
function toOurGoalPostDistSum()
	local dist1 = pos():dist(CGeoPoint:new_local(-param.pitchLength / 2.0, -param.goalWidth / 2.0))
	local dist2 = pos():dist(CGeoPoint:new_local(-param.pitchLength / 2.0, param.goalWidth / 2.0))
    return (dist1 + dist2)
end
```

* `toOurGoalDir()`函数：返回球到我方球门的方向。
```lua
function toOurGoalDir()
	return (CGeoPoint:new_local(-param.pitchLength / 2.0, 0) - ball.pos()):dir()
end
```

* `toPointDir(p)`函数：返回球到指定点p的方向。
```lua
function toPointDir(p)
	return function ()
		return (p - pos()):dir()
	end
end
```

* `toPointDist(p)`函数：返回球到指定点p的距离。
```lua
function toPointDist(p)
	return pos():dist(p)
end
```

* `antiY()`函数：根据球的y坐标返回-1或1。若y>0，返回-1；若y<0，返回1
```lua
function antiY()
	if posY() > 0 then
		return -1
	else
		return 1
	end
end
```

* `syntY()`函数：返回antiY()的相反数。
```lua
function syntY()
	return -1*antiY()
end
```

* `antiYPos(p)`函数：返回指定点p及其对称点中y坐标小于0的那一个
```lua
function antiYPos(p)
	return function ()
		if type(p) == "function" then
			return CGeoPoint(p():x(), antiY()*p():y())
		else
			return CGeoPoint(p:x(), antiY()*p:y())
		end
	end
end
```

* `syntYPos(p)`函数：返回指定点p及其对称点中y坐标大于0的那一个
```lua
function syntYPos(p)
	return function ()
		return CGeoPoint(p:x(), syntY()*p:y())
	end
end
```

* `toFuncDir(f)`函数：返回球到指定函数f的返回点的方向。
```lua
function toFuncDir(f)
	return function ()
		return (f() - pos()):dir()
	end
end
```

* `antiYDir(p)`函数：返回球到指定点p及其对称点中y坐标小于0的那一个的方向
```lua
function antiYDir(p)
	return function ()
		if type(p) == "userdata" then
			return (antiYPos(p)() - pos()):dir()
		elseif type(p) == "number" then
			return ball.antiY()*p
		elseif type(p) == "function" then
			return (antiYPos(p())() - pos()):dir()
		end
	end
end
```

* `syntYDir(p)`函数：返回球到指定点p及其对称点中y坐标大于0的那一个的方向
```lua
function syntYDir(p)
	return function ()
		if type(p) == "userdata" then
			return (syntYPos(p)() - pos()):dir()
		elseif type(p) == "number" then
			return ball.syntY()*p
		end
	end
end
```

* `toBestEnemyDist()`函数：返回球到最近敌方球员的距离。
```lua
function toBestEnemyDist()
	local enemyNum = defenceInfoNew:getBestBallChaser()
	if Utils.PlayerNumValid(enemyNum) then --如果场上有这辆敌方车
		return toEnemyDist(enemyNum)
	else
		return 1000
	end
```

* `enemyDistMinusPlayerDist(role)`函数：返回球到最近敌方球员与到指定球员role的距离的差值。
```lua
function enemyDistMinusPlayerDist(role)
	return toBestEnemyDist() - toPlayerDist(role)
end
```

* `goRush()`函数：定位球时返回一个指定的点，用于冲向该点。
```lua
function goRush()
	return function ()
		-- changed to Brazil by zhyaic
		return CGeoPoint:new_local(refPosX() - 100, 150 * refAntiY())
	end
end
```

* `backDir(p, anti)`函数：返回球到指定点的方向。根据anti的bool值来决定是否对结果执行anti处理（即类似之前antiYDir的那种处理）
```lua
function backDir(p, anti)
	return function ()
		local idir
		if type(p) == "function" then
			idir = p()
		elseif type(p) == "number" then
			idir = p
		elseif type(p) == "userdata" then
			if anti == false then
				idir = Utils.Normalize((p - ball.pos()):dir())
			else
				local targetP = CGeoPoint:new_local(p:x(), ball.antiY()*p:y())
				idir = Utils.Normalize((targetP - ball.pos()):dir())
			end
		elseif type(p) == "string" then
			idir = Utils.Normalize((player.pos(p) - ball.pos()):dir())
		end

		if type(idir) == "userdata" then
			if anti == false then
				idir = Utils.Normalize((idir - ball.pos()):dir())
			else
				local temP = CGeoPoint:new_local(idir:x(), ball.antiY()*idir:y())
				idir = Utils.Normalize((temP - ball.pos()):dir())
			end
		end
		return idir
	end
end
```
* `backPos(p, d, s, anti)`函数：返回球相对于指定点p进行横向、纵向偏移后的坐标，d为纵向偏移量，s为横向偏移量。
```lua
function backPos(p, d, s, anti)
	return function ()
		local idir = backDir(p, anti)()
		if d == nil then
			d = 18
		end

		local ipos
		if s == nil then
			s = 0
		end
		local shiftVec = Utils.Polar2Vector(s, idir):rotate(syntY()*math.pi/2)--横向偏移向量
		local ipos = ball.pos() + shiftVec + Utils.Polar2Vector(d, Utils.Normalize(idir + math.pi)) --Utils.Polar2Vector(d, Utils.Normalize(idir + math.pi))为纵向偏移方向
		return ipos
	end
end
```

* 初始化gRefMsg
```lua
gRefMsg = {
	-- 上一次定位球的Cycle
	lastCycle = 0,
	-- 本次定位球开始时球的X位置
	ballX     = 0,
	-- 本次定位球开始时球的Y位置
	ballY     = 0,
	-- 本次定位球的antiY参数
	antiY     = 1,
	-- 本次定位球是不是我方的球
	isOurBall = false
}
```

* `updateRefMsg()`函数：当有裁判盒信息切换时进行更新的信息。
```lua
function updateRefMsg()
	if (vision:Cycle() - gRefMsg.lastCycle) > 6 then --更新球信息
		gRefMsg.ballX = posX()
		gRefMsg.ballY = posY()
		gRefMsg.antiY = antiY()
		gRefMsg.isOurBall = world:IsOurBallByAutoReferee()
	else --若球有明显移动，更新球信息
		if math.abs(gRefMsg.ballX - posX()) > 10 then
			gRefMsg.ballX = posX()
		end
		if math.abs(gRefMsg.ballY - posY()) > 10 then
			gRefMsg.ballY = posY()
		end
		gRefMsg.antiY = antiY()
	end
    --更新cycle值
	gRefMsg.lastCycle = vision:Cycle()
end
```

* `refPosX()`函数：返回球时球的x坐标。
```lua
function refPosX()
	return gRefMsg.ballX
end
```

* `refPosY()`函数：返回定位球时球的的y坐标。
```lua
function refPosY()
	return gRefMsg.ballY
end

```

* `refAntiY()`函数：返回定位球时的antiY参数。
```lua
function refAntiY()
	return gRefMsg.antiY
end
```

* `refAntiYPos(p)`函数：返回指定点在定位球中使用的反向点(参考之前的antiY操作)
```lua
function refAntiYPos(p)
	return function ()
		return CGeoPoint(p:x(), gRefMsg.antiY*p:y())
	end
end
```

* `refSyntYPos(p)`函数：返回指定点在定位球中使用的同向点
```lua
function refSyntYPos(p)
	return function ()
		return CGeoPoint(p:x(), -1*gRefMsg.antiY*p:y())
	end
end
```

* `refAntiYDir(p)`函数：指定方向在定位球中使用的反向朝向
```lua
function refAntiYDir(p)
	return function ()
		return gRefMsg.antiY*p
	end
end
```

* `refSyntYDir(p)`函数：指定方向在定位球中使用的同向朝向
```lua
function refSyntYDir(p)
	return function ()
		if type(p) == "function" then
			return -1*gRefMsg.antiY*p()
		else
			return -1*gRefMsg.antiY*p
		end
	end
end
```

* `refIsOurBall(p)`函数：返回是否我方开定位球
```lua
function refIsOurBall(p)
	return gRefMsg.isOurBall
end
```

* `supportPassPos(num)`函数：返回在num区域一个用于传球的最佳点。
```lua
function supportPassPos(num)
	return function ()
		--local passPos = bestAlg:getBestPointFromArea(num)
		local areaNum = num
		if type(areaNum) == "function" then
			areaNum = areaNum()
		end
		local passPos = bestAlg:getBestPointFromArea(areaNum)
		return passPos
	end
end
```

* `LWPassPos()`函数：返回一个用于左路传球的最佳点。
```lua
function LWPassPos()
	return function ()
		local passPos = bestAlg:getBestPointFromArea(0)
		return passPos
	end
end
```

* `MWPassPos()`函数：返回一个用于中路传球的最佳点。
```lua
function MWPassPos()
	return function ()
		local passPos = bestAlg:getBestPointFromArea(1)
		return passPos
	end
end
```

* `RWPassPos()`函数：返回一个用于右路传球的最佳点。
```lua
function RWPassPos()
	return function ()
		local passPos = bestAlg:getBestPointFromArea(2)
		return passPos
	end
end
```

* `LMPassPos()`函数：返回一个用于左中场传球的最佳点。
```lua
function LMPassPos()
	return function ()
		local passPos = bestAlg:getBestPointFromArea(3)
		return passPos
	end
end
```

* `MMPassPos()`函数：返回一个用于中中场传球的最佳点。
```lua
function MMPassPos()
	return function ()
		local passPos = bestAlg:getBestPointFromArea(4)
		return passPos
	end
end
```

* `RMPassPos()`函数：返回一个用于右中场传球的最佳点。
```lua
function RMPassPos()
	return function ()
		local passPos = bestAlg:getBestPointFromArea(5)
		return passPos
	end
end
```

* `isMovingTo(role)`函数：返回球是否朝着指定角色运动。
```lua
function isMovingTo(role)
	if ball.valid() and ball.velMod() > 1 and math.abs(Utils.Normalize(ball.velDir() - ball.toPlayerDir(role))) < math.pi / 9 then
		return true
	end
	return false
end
```

* `placementPos()`函数：返回球的放置位置。
```lua
function placementPos()
    return vision:getBallPlacementPosition()
end
```

* `readyplacementPos()`函数：返回一个放置球时车准备的位置。
```lua
function readyplacementPos() 
        return function ()
               --放球点在左上
               if ball.posX() > ball.placementPos():x() and  ball.posY() >ball.placementPos():y() and ball.posX()-ball.placementPos():x()> ball.posY()-ball.placementPos():y()  then
		         if ball.placementPos():y()+250<450 then
		           return CGeoPoint(ball.placementPos():x(), ball.placementPos():y()+250)
		         else 
		           return CGeoPoint(ball.placementPos():x(), ball.placementPos():y()-250)
		         end
               end
               if ball.posX() > ball.placementPos():x() and  ball.posY() >ball.placementPos():y() and ball.posX()-ball.placementPos():x()<= ball.posY()-ball.placementPos():y()  then
		         if ball.placementPos():x()+250<600 then
		           return CGeoPoint(ball.placementPos():x()+250, ball.placementPos():y())
		         else
		           return CGeoPoint(ball.placementPos():x()-250, ball.placementPos():y())
		         end
               end
               --放球点在右上
               if ball.posX() <= ball.placementPos():x() and  ball.posY() >ball.placementPos():y() and ball.placementPos():x()-ball.posX()> ball.posY()-ball.placementPos():y()  then
		          if ball.placementPos():y()+250<450 then 
		            return CGeoPoint(ball.placementPos():x(), ball.placementPos():y()+250)
		          else 
		          	return CGeoPoint(ball.placementPos():x(), ball.placementPos():y()-250)
		          end
               end
               if ball.posX() <= ball.placementPos():x() and  ball.posY() >ball.placementPos():y() and ball.placementPos():x()-ball.posX()<= ball.posY()-ball.placementPos():y()  then
		          if ball.placementPos():x()-250>-600 then
		            return CGeoPoint(ball.placementPos():x()-250, ball.placementPos():y())
		          else
		          	return CGeoPoint(ball.placementPos():x()+250, ball.placementPos():y())
		          end
               end
               --放球点在左下
               if ball.posX() > ball.placementPos():x() and  ball.posY() <=ball.placementPos():y() and ball.posX()-ball.placementPos():x()> ball.placementPos():y()-ball.posY()  then
		         if ball.placementPos():y()-250>-450 then 
		            return CGeoPoint(ball.placementPos():x(), ball.placementPos():y()-250)
		         else 
		         	return CGeoPoint(ball.placementPos():x(), ball.placementPos():y()+250)
		         end
               end
               if ball.posX() > ball.placementPos():x() and  ball.posY() <=ball.placementPos():y() and ball.posX()-ball.placementPos():x()<= ball.placementPos():y()-ball.posY()  then
		         if ball.placementPos():x()+250<600 then
		            return CGeoPoint(ball.placementPos():x()+250, ball.placementPos():y())
		         else
		         	return CGeoPoint(ball.placementPos():x()-250, ball.placementPos():y())
		         end
               end
               --放球点在右下
               if ball.posX() <= ball.placementPos():x() and  ball.posY() <=ball.placementPos():y() and ball.posX()-ball.placementPos():x()> ball.placementPos():y()-ball.posY()  then
		         if  ball.placementPos():y()-250>-450 then
 		           return CGeoPoint(ball.placementPos():x(), ball.placementPos():y()-250)
 		         else
 		           return CGeoPoint(ball.placementPos():x(), ball.placementPos():y()+250)
 		         end
               end
               if ball.posX() <= ball.placementPos():x() and  ball.posY() <=ball.placementPos():y() and ball.posX()-ball.placementPos():x()<= ball.placementPos():y()-ball.posY()  then
		         if ball.placementPos():x()-250>-600 then
		           return CGeoPoint(ball.placementPos():x()-250, ball.placementPos():y())
		         else
		           return CGeoPoint(ball.placementPos():x()+250, ball.placementPos():y())
		         end
               end
        end
end
```