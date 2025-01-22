cond.lua 主要定义了一些函数，用于判断场上的状况

## 裁判盒指令状态判断

* ourBallPlace():判断是否是我方放球

```lua
function ourBallPlace()
	return vision:GetCurrentRefereeMsg() == "OurBallPlacement"
end
```

* theirBallPlace():判断是否为敌方放球

```lua
function theirBallPlace()
	return vision:GetCurrentRefereeMsg() == "TheirBallPlacement"
end
```

* isGameOn():判断比赛是否开始

```lua
function isGameOn()
	return vision:gameState():gameOn()
end
```

* isNormalStart():判断裁判盒是否发出normal start的指令

```lua
function isNormalStart()
	return vision:gameState():canEitherKickBall()
end
```

## 其它状态判断

* bestPlayerChanged(): 判断最佳追求手是否改变

```lua
function bestPlayerChanged()
	return world:IsBestPlayerChanged()
end
```

* canShootOnBallPos(role): 判断角色为role的球员是否可以射门

```lua
function canShootOnBallPos(role)
	return world:canShootOnBallPos(vision:Cycle(),gRoleNum[role])
end
```

* getOpponentScript(str, script, MaxRandom)函数的目的是根据给定的区域`str`、脚本`script`和最大随机数`MaxRandom`来获取对手脚本相关的信息。它会根据`script`的类型（是表还是字符串）进行不同的操作。

  * **当`script`为表时**
    * 首先，通过`table.getn(script)`获取表`script`中的元素个数`totalNum`。
    * 然后，使用`math.random(1,totalNum * 10000) % totalNum+1`生成一个随机数`randNum`，这个随机数的范围是1到`totalNum`。这里先将`math.random`的范围扩大到`1`到`totalNum * 10000`，然后再取模`totalNum`并加1，是为了让随机数的分布更均匀（相比于直接使用`math.random(1,totalNum)`）。
    * 接着，它会检查`script[randNum]`的类型。如果`script[randNum]`是字符串，就直接返回`script[randNum]`；否则，返回`str`和`script[randNum]`连接后的结果。
  * **当`script`为字符串时**
    * 如果`script`等于`"random"`，则生成一个1到`MaxRandom`之间的随机数`randNum`，然后返回`str`和`randNum`连接后的结果，并打印出`randNum`以及`str`和`randNum`连接后的结果。
    * 如果`script`不等于`"random"`，则直接返回`script`，这里表示使用固定的模式打定位球。
  * **当`script`为其他类型时**
    * 会打印出`Error in getOpponentScript`和`str`，表示在获取对手脚本时发生了错误。

```lua
-- str 为所在的区域
-- script 为所使用的脚本
-- MaxRandom 为最大的随机数
function getOpponentScript(str, script, MaxRandom)
	if type(script) == "table" then
		local totalNum = table.getn(script)
		local randNum = math.random(1,totalNum * 10000) % totalNum + 1
		print("randNum "..randNum.." "..str..script[randNum])
		if (type(script[randNum]) == "string") then
			return script[randNum]
		else
			return str..script[randNum]
		end
	elseif type(script) == "string" then
		if script == "random" then
			local randNum = math.random(1,MaxRandom)
			print("randNum",str..randNum)
			return str..randNum
		else
			-- 使用固定的模式打定位球
			return script
		end
	else
		print("Error in getOpponentScript "..str)
	end	
end
```
