enemy.lua脚本包含了一系列与敌方车辆有关的函数，包括但不限于我方的坐标，速度，到我方车辆的距离，运动方向等等。以下是对各个函数的详细解释：

* `instance(role)`函数：返回该敌方role在场上的实体，用于参数调用。
```lua
function instance(role)
	if type(role) == "number" then
		return vision:TheirPlayer(role)
	else
		print("Invalid role in enemy.instance!!!")
	end
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

* `oppoNum()`函数：用于获取对方车辆的数量。
```lua
function oppoNum()
	return defenceInfo:getOppoNum()
end
```

* `attackNum()`函数：用于获取对方车辆在进攻时投入的数量。
```lua
function attackNum()
	return defenceInfo:getAttackNum()
end
```

* `hasReceiver()`函数：用于判断对方车辆中是否有receiver角色。
```lua
function hasReceiver()
	return CEnemyHasReceiver()
end
```

* `best()`函数：用于返回对方车辆中最佳的球追逐者，即最有可能造成威胁的车辆。
```lua
function best()
	return defenceInfoNew:getBestBallChaser()
end
```

* `nearest()`函数：用于返回对方车辆中距离球最近的车辆的位置与方向。
```lua
function nearest()
	local nearDist = 99999
	local nearNum = 0
	for i=1,6 do
		local theDist = enemy.pos(i):dist(ball.pos())
		if enemy.valid(i) and nearDist > theDist then
			nearDist = theDist
			nearNum = i
		end
	end
	return pos(nearNum), dir(nearNum)
end
```