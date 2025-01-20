# lua中的工具函数
本部分主要介绍worldmodel文件夹和utils文件夹里的lua文件包含的内容。这部分包含了在opponent，play，skill的各个脚本中都可以调用的一些工具性函数。

注：此处仅介绍lua脚本中现在还在使用的工具函数，对于一些远古的废弃函数，读者可以自行学习。

## Utils
### bit

bit.lua文件定义了一个名为`bit`的表（在Lua中类似类的概念），它实现了一些基本的位操作功能，包括二进制和十进制之间的转换，以及常见的位逻辑运算（如与、或、异或、非）和位移操作（左移、右移）。

#### 代码细节解释

1. 初始化`bit.data32`
   - 在这段代码开始部分：

   ```lua
   bit = {data32 = {}}
   for i = 1,32 do
       bit.data32[i]=2^(32 - i)
   end
   ```

   - 这里创建了一个名为`bit`的表，其中包含一个名为`data32`的子表。这个子表用于后续的二进制到十进制转换。通过循环，计算并存储了从`2^31`到`2^0`的值到`bit.data32`表中。这些值将在二进制到十进制转换时作为权重使用。

2. `d2b`函数（十进制到二进制转换）
   - 代码如下：

   ```lua
   function bit:d2b(arg)
       local tr = {}
       for i = 1,32 do
           if arg >= self.data32[i] then
               tr[i]=1
               arg = arg - self.data32[i]
           else
               tr[i]=0
           end
       end
       return tr
   end
   ```

   - 这个函数接受一个十进制数`arg`作为参数。它通过与`bit.data32`中的值进行比较，将十进制数转换为一个32位的二进制表示形式存储在表`tr`中。如果`arg`大于等于当前的权重值（`self.data32[i]`），则相应位设为1，并从`arg`中减去该权重值；否则设为0。

3. `b2d`函数（二进制到十进制转换）
   - 代码如下：

   ```lua
   function bit:b2d(arg)
       local nr = 0
       for i = 1,32 do
           if arg[i]==1 then
               nr = nr + 2^(32 - i)
           end
       end
       return nr
   end
   ```

   - 这个函数接受一个表示二进制数的表`arg`作为参数。它通过遍历这个表，如果表中的元素为1，则将对应的权重值（`2^(32 - i)`）累加到`nr`中，最后返回转换后的十进制数。

4. `_xor`函数（异或操作）
   - 代码如下：

   ```lua
   function bit:_xor(a,b)
       local op1 = self:d2b(a)
       local op2 = self:d2b(b)
       local r = {}

       for i = 1,32 do
           if op1[i]==op2[i] then
               r[i]=0
           else
               r[i]=1
           end
       end
       return self:b2d(r)
   end
   ```

   - 这个函数接受两个十进制数`a`和`b`作为参数。首先将`a`和`b`转换为二进制形式（使用`d2b`函数），然后对这两个二进制数的每一位进行异或操作（如果对应位相同则结果为0，不同则为1），最后将得到的二进制结果转换回十进制数并返回。

5. `_and`函数（与操作）
   - 代码如下：

   ```lua
   function bit:_and(a,b)
       local op1 = self:d2b(a)
       local op2 = self:d2b(b)
       local r = {}

       for i = 1,32 do
           if op1[i]==1 and op2[i]==1 then
               r[i]=1
           else
               r[i]=0
           end
       end
       return self:b2d(r)
   end
   ```

   - 这个函数接受两个十进制数`a`和`b`作为参数。将`a`和`b`转换为二进制后，对每一位进行与操作（只有当两位都为1时结果为1），最后将二进制结果转换回十进制数返回。

6. `_or`函数（或操作）
   - 代码如下：

   ```lua
   function bit:_or(a,b)
       local op1 = self:d2b(a)
       local op2 = self:d2b(b)
       local r = {}

       for i = 1,32 do
           if op1[i]==1 or op2[i]==1 then
               r[i]=1
           else
               r[i]=0
           end
       end
       return self:b2d(r)
   end
   ```

   - 这个函数接受两个十进制数`a`和`b`作为参数。将`a`和`b`转换为二进制后，对每一位进行或操作（只要有一位为1结果就为1），最后将二进制结果转换回十进制数返回。

7. `_not`函数（非操作）
   - 代码如下：

   ```lua
   function bit:_not(a)
       local op1 = self:d2b(a)
       local r = {}

       for i = 1,32 do
           if op1[i]==1 then
               r[i]=0
           else
               r[i]=1
           end
       end
       return self:b2d(r)
   end
   ```

   - 这个函数接受一个十进制数`a`作为参数。将`a`转换为二进制后，对每一位进行非操作（1变为0，0变为1），然后将二进制结果转换回十进制数返回。

8. `_rshift`函数（右移操作）
   - 代码如下：

   ```lua
   function bit:_rshift(a,n)
       local op1 = self:d2b(a)
       local r = self:d2b(0)

       if n < 32 and n > 0 then
           for i = 1,n do
               for i = 31,1, - 1 do
                   op1[i + 1]=op1[i]
               end
               op1[1]=0
           end
           r = op1
       end
       return self:b2d(r)
   end
   ```

   - 这个函数接受一个十进制数`a`和一个位移量`n`作为参数。将`a`转换为二进制后，循环`n`次，每次将二进制数的每一位向右移动一位（最左边的位补0），最后将得到的二进制结果转换回十进制数返回。

9. `_lshift`函数（左移操作）
   - 代码如下：

   ```lua
   function bit:_lshift(a,n)
       local op1 = self:d2b(a)
       local r = self:d2b(0)

       if n < 32 and n > 0 then
           for i = 1,n do
               for i = 1,31 do
                   op1[i]=op1[i + 1]
               end
               op1[32]=0
           end
           r = op1
       end
       return self:b2d(r)
   end
   ```

   - 这个函数接受一个十进制数`a`和一个位移量`n`作为参数。将`a`转换为二进制后，循环`n`次，每次将二进制数的每一位向左移动一位（最右边的位补0），最后将得到的二进制结果转换回十进制数返回。

10. `print`函数
   - 代码如下：

   ```lua
   function bit:print(ta)
       local sr = ""
       for i = 1,32 do
           sr = sr..ta[i]
       end
       print(sr)
   end
   ```

   - 这个函数接受一个表示二进制数的表`ta`作为参数。它将表中的元素连接成一个字符串，并打印这个字符串，从而以二进制形式输出这个数。

### bufcunt
bufcunt.lua里定义了常用状态跳转函数bufcunt，一下是详细代码

```lua
function bufcnt( cond, buf, cnt )
	--cond为状态跳转条件，buf为cond满足的持续时间，cnt为若场上无变化情况下可保持此状态的最长时间
	if buf == "normal" then
		buf = 6
	elseif buf == "slow" then
		buf = 10
	elseif buf == "fast" then
		buf = 1
	end
	--注意buf不一定为"normal","slow","fast"，也可以为数字如20。单位是帧数

	if CTimeOut(cond, buf, cnt) == 1 then --调用C++函数判断是否跳转状态
		return true
	else
		return false
	end
end
```

### file

file.lua文件主要定义了一些用于文件操作和打印表结构的函数。它包含了文件的打开、写入、关闭操作以及一个能够递归打印表结构（包括嵌套表）的函数，并且还将这个打印表结构的函数赋值给`table.print`以便于使用。

#### 代码细节解释

1. **`open`函数**
   - 代码如下：

   ```lua
   function open(file_name, mode)
       -- local recFile
       -- return function()
           recFile = io.open(file_name, mode)
           return recFile
       -- end
   end
   ```

   - 这个函数用于打开一个文件。它接受文件名`file_name`和打开模式`mode`作为参数。函数内部直接使用`io.open`来打开文件，并返回打开后的文件句柄。原本代码中有一个函数嵌套的结构，但注释掉了多余部分，实际功能就是直接打开文件并返回文件句柄。如果打开文件失败，将会返回`nil`以及错误信息（这是`io.open`的默认行为）。

2. **`write`函数**
   - 代码如下：

   ```lua
   function write(rec_file, fmt,...)
       rec_file:write(string.format(fmt,...))
   end
   ```

   - 这个函数用于向已打开的文件写入内容。它接受文件句柄`rec_file`、格式化字符串`fmt`以及可变参数`...`。首先使用`string.format`根据给定的格式化字符串和参数生成要写入的字符串，然后通过文件句柄的`write`方法将内容写入文件。

3. **`close`函数**
   - 代码如下：

   ```lua
   function close(rec_file)
       rec_file:close()
   end
   ```

   - 这个函数用于关闭已打开的文件。它接受文件句柄`rec_file`作为参数，并调用文件句柄的`close`方法来关闭文件，释放相关资源。

4. **`print_r`函数（用于打印表结构）**
   - 代码如下：

   ```lua
   function print_r ( t )  
       local print_r_cache={}
       local function sub_print_r(t,indent)
           if (print_r_cache[tostring(t)]) then
               print(indent.."*"..tostring(t))
           else
               print_r_cache[tostring(t)]=true
               if (type(t)=="table") then
                   for pos,val in pairs(t) do
                       if (type(val)=="table") then
                           print(indent.."["..pos.."] => "..tostring(t).." {")
                           sub_print_r(val,indent..string.rep(" ",string.len(pos)+8))
                           print(indent..string.rep(" ",string.len(pos)+6).."}")
                       elseif (type(val)=="string") then
                           print(indent.."["..pos..'] => "'..val..'"')
                       else
                           print(indent.."["..pos.."] => "..tostring(val))
                       end
                   end
               else
                   print(indent..tostring(t))
               end
           }
       end
       if (type(t)=="table") then
           print(tostring(t).." {")
           sub_print_r(t,"  ")
           print("}")
       else
           sub_print_r(t,"  ")
       end
       print()
   end
   ```

   - 这个函数用于递归地打印表结构。
     - 首先，它创建了一个空表`print_r_cache`用于缓存已经处理过的表的字符串表示，避免循环引用时无限递归。
     - 然后定义了内部函数`sub_print_r`，这个函数接受一个表`t`和缩进字符串`indent`作为参数。如果表的字符串表示已经在缓存中，则只打印一个带`*`标记的表的字符串表示，表示已经处理过。否则，将表的字符串表示添加到缓存中。如果表是一个普通表，就遍历表中的键值对。如果值是一个表，则递归调用`sub_print_r`来打印嵌套表，并添加适当的缩进和括号来表示表的结构；如果值是一个字符串，则打印带有双引号的字符串；否则直接打印值的字符串表示。
     - 最后，在`print_r`函数中，如果传入的参数是一个表，则先打印表的开始括号，然后调用`sub_print_r`来处理表内容，最后打印表的结束括号并换行；如果传入的不是表，则直接调用`sub_print_r`进行处理并换行。

5. **`table.print`的赋值**
   - 代码如下：

   ```lua
   table.print = print_r
   ```

   - 这行代码将`print_r`函数赋值给`table.print`，使得可以通过`table.print`来调用这个用于打印表结构的函数，这是一种方便的命名约定，让使用者可以更直观地知道这个函数是用于打印表的。

## worldmodel
此处仅对worldmodel中的lua文件进行简单介绍，详细部分请查阅2.2.6.1-2.2.6.3小节

* ball.lua：与球有关的函数，可提供包括但不限于球的坐标，速度，到车距离，运动方向等等

* combo.lua：对task.lua更高一层的抽象,包括一些通过标志位决定的task和一些组合的task

目前combo只开发了multiback，故在此处作简单介绍，不再另开小节

```lua
function multiBack(n)
  if n == 1 then
  	return task.multiBack(1,1)
  else
    taskTable={}
    for i=1,n do
      table.insert(taskTable,task.multiBack(n,i))
    end
    return taskTable
  end
end
```

multiback在使用时用作`Engineer_Finisher_Crosser = combo.multiback(3)`，即把此处生成的table中的元素传给三个球员，进行任务分配。

* cond.lua：一系列判断场上各种状态的函数

* cp.lua：与挑射有关的函数，可提供不同的挑射力度。包括：

```lua
function specified(p) --返回p的精确值
function full() --全力，返回500
function touch() --touch力度，返回480
function slight() --轻踢，返回180
function middle() --中等力度，返回220
function normal() --正常力度，返回240
-- 纯闭包函数，这个函数只是用在开射门的条件中
-- role1 为接球车
function toPlayer(role1) --返回传球给role1的力度

function toTarget(p) --返回传球到p处的力度
	return function()
		local tmpP
		if type(p) == "function" then
			tmpP = p()
		elseif type(p) == "userdata" then
			tmpP = p
		end

		local dist = ball.toPointDist(tmpP)
		if IS_SIMULATION then --在仿真状态下返回dist
			return dist
		else --在实车状态下返回0.6*dist-38
			dist = dist * 0.6 - 38
			-- dist = dist * 0.4857 - 16.19
			if dist <= 60 then
				dist = 60
			end
			return dist
		end
	end
end

```

* dir.lua：与角度有关的函数，可提供包括但不限于球与球门连线的角度，球车连线角度，车与球门连线的角度等等

* enemy.lua：与敌方车辆有关的函数，可提供包括但不限于敌方的坐标，速度，到我方车辆的距离，运动方向等等

* flag.lua：各种状态标签，用于控制车的运动，例如nothing(无特殊要求)dodge_ball(避球)avoid_shoot_line(避开射门线)placer_to_ball_dis(放球车到球距离)等等

* kick.lua：与踢球有关的函数，用于判定是挑球还是平射等等

* kp.lua：与平射有关的函数，可提供不同的平射力度，包括：

```lua
function specified(p)--返回p的精确值
function full()--全力，返回500
function touch()--touch力度，返回500
-- 当t有三种输入(userdate/point、role、function)，返回挑传到target的力度
function toTarget(p)
	return function(role)
		local target
		if type(p) == "function" then
			target = p()
		elseif type(p) == "userdata" then
			target = p
		else
			target = player.pos(p)
		end

		if IS_SIMULATION then
			local pw=player.toPointDist(role, target)*1.2 + 150
			if pw>650 then
				pw=650
			end
			return pw
		else
			local pw = player.toPointDist(role, target) * 1.5714 + 42.857
			if gCurrentPlay == "Nor_PassAndShoot" then
				pw = pw - 100
			else
				pw = pw - 50
			end

			if pw < 250 then    --50 --> 250 Modified by Soap, 2015/4/11
				pw = 250 					--50 --> 250 Modified by Soap, 2015/4/11
			elseif pw > 600 then
				pw = 600
			end
			return pw
			-- local pw = -0.0068*dist*dist + 5.5774*dist - 287.8
		end
	end
end

--同样返回传球到p的力度，与上面函数有不同的力度最大/最小处理，此处限制实车力度最小为50，最大为500，不限制仿真力度。
function toTargetNormalPlay(p)
	return function(role)
		local target
		if type(p) == "function" then
			target = p()
		elseif type(p) == "userdata" then
			target = p
		else
			target = player.pos(p)
		end

		if IS_SIMULATION then
			return player.toPointDist(role, target)*1.2 + 150
		else
			local pw = player.toPointDist(role, target) * 1.5 + 42.857
			if pw < 50 then
				pw = 50
			elseif pw > 500 then
				pw = 500
			end
			return pw
		end
	end
end
```

* param.lua：与场地有关的参数，如球员数、场地的长宽、球门的长宽深等等

```lua
maxPlayer   = CGetFieldParam("MAX_PLAYER") -- 8
pitchLength = CGetFieldParam("PITCH_LENGTH") -- 1200
pitchWidth  = CGetFieldParam("PITCH_WIDTH") -- 900
goalWidth = CGetFieldParam("GOAL_WIDTH") -- 120
goalDepth = CGetFieldParam("GOAL_DEPTH") -- 20
freeKickAvoidBallDist = CGetFieldParam("FREE_KICK_AVOID_BALL_DIST") -- 55
playerRadius	= CGetFieldParam("PLAYER_SIZE") -- 9
penaltyWidth    = CGetFieldParam("PENALTY_AREA_WIDTH") -- 240	-- 195
penaltyDepth	= CGetFieldParam("PENALTY_AREA_DEPTH") -- 120	-- 85
penaltyRadius	= CGetFieldParam("PENALTY_AREA_R") -- 85	-- 85
penaltySegment	= CGetFieldParam("PENALTY_AREA_L") -- 35	--
playerFrontToCenter = CGetFieldParam("PLAYER_FRONT_TO_CENTER") -- 7.6
lengthRatio	= 1
widthRatio	= 1
```

* player.lua：与我方车辆有关的函数，可提供包括但不限于我方的坐标，速度，到我方车辆的距离，运动方向等等

* pos.lua：与坐标有关的函数，提供各种坐标，如踢球点等等

* pre.lua：与精度有关的坐标，可能在临界情况判定或踢球角度校准中用到，包括

```lua
function specified(p)--把p转化为弧度制
function high() --高精度，pi/180
function middlehigh() --较高精度，pi/60
function middle() --中精度，pi/36
function low() --低精度，7pi/180
function fieldDefender() --返回防守清球时的角度精度
```

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