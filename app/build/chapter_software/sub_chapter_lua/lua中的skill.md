# lua中的skill
本文主要介绍lua中的skill脚本，这些脚本一般在task.lua中被调用，自身调用C++中的skil，在task.lua中组成机器人在场上需要执行的task任务，这些task任务会在前文提到的test或Ref等等脚本中被分配给机器人在场上执行。这些skill脚本也是lua的最底层，与C++部分衔接

## 脚本介绍

```lua
function AdvanceBallV4(task) --函数名
	local mpos --匹配的坐标
	local mflag     = task.flag or 0 --任务标签，flag.lua里的
	local mrole     = task.srole or "" 
	local tandem = function () --可能的函数
		return gRoleNum["Special"]
	end

	execute = function(runner)
		if runner >= 0 and runner < param.maxPlayer then
			...
		else
			print("Error runner in AdvanceBall", runner)
		end
		local tandemNum    = tandem() and tandem() or 0
		return CAdvanceBallV4(runner, mflag, tandemNum)  --调用C++中的底层skill
	end

	matchPos = function()
		if type(task.pos) == "function" then
			mpos = task.pos()
		else
			mpos = task.pos
		end
		return mpos
	end
	return execute, matchPos
end

gSkillTable.CreateSkill{
	name = "AdvanceBallV4", --skill名
	execute = function (self)
		print("This is in skill"..self.name)
	end
}
```
