# config.lua

!!! abstract
	config.lua作为特殊的lua文件,是整个框架的 **核心**

可以理解为控制台。

```lua
IS_SIMULATION = CGetIsSimulation() --判断是否为仿真模式
IS_YELLOW = CGetIsYellow() --判断是否为黄方

IS_TEST_MODE = false --判断是否为test模式
--这里是一些常用的测试脚本
-- Test_Run Test_Break Test_ChaseNew Test_GetBall
-- Test_Run Test_Run6 Test_Speed
-- Test_Goalie Test_PassEachOther Test_NormalPass
-- Test_AdvanceV4 Test_MultiBack Test_GoSupport Test_ChaseKickV3

--在IS_TEST_MODE下调用下面规定的脚本
if not IS_YELLOW then
	gTestPlay = "Nor_bus" --蓝方调用此脚本
else
	gTestPlay = "Nor_bus" --黄方调用此脚本
end

-- PureDefence8 NormalKick
--在非test mode下调用下面规定的脚本
if not IS_YELLOW then
	OPPONENT_NAME = "NormalKick_show" --蓝方调用此脚本
else
	OPPONENT_NAME =  "NormalKick_show" --黄方调用此脚本
end

--在脚本中未规定匹配时固定名字匹配的车号，详见下文有关匹配的小节
gRoleFixNum = {
	Goalie   = {0},
	Kicker   = {1},
	Tier	 = {2},
	Receiver = {3}
}
--下面四个table储存了所有play和skill的脚本的名字，方便查找调用
gSkill = {
    ...
}

gRefPlayTable = {
	...
}

gNorPlayTable = {
	...
}

gTestPlayTable = {
	...
}
```