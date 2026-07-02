---
layout: default 
title: Advance

---

> Tyh 22.10
> wjr 24.10

## 初始工作

### Lua层面参数管理

三个参数：(const int num, const int flags, const int tendemNum)
分别对应executor  player.flag  ball.receiver
其中对于ball.receiver而言，设计思路来源于六人脚本中的Special:  goLWPassPos

1. 得到Special位置 进行receiver
2. 在当前版本的Advance中并没有使用这一参数
3. 因此目前实际使用到的参数仅仅只有`num` `flags`

### cpp层面参数管理

cpp中值得作为策略调整的参数已经移至ini：

```c++
	NowIsShoot = 0; /*Shoot持续化变量*/
	KICK_DIST = paramManager->KICK_DIST;  /*射门允许范围 越高越容易射门*/
	WantToLessShoot = paramManager->WantToLessShoot; /*射门倾向，越低越容易射门 最低为0 最高为5*/
	RELIEF_DIST = paramManager->RELIEF_DIST;  /*GET中紧急状况下的RELIEF判断距离*/
	OPP_HAS_BALL_DIST = paramManager->OPP_HAS_BALL_DIST; /*判断敌方是否有球的距离 需要调整*/
	CanPassToWingDist = paramManager->CanPassToWingDist; /*Advance能够传给边锋的临界距离*/
	CanWingShootDist = paramManager->CanWingShootDist; /*边锋能够射门的临界距离*/
	SHOOT_PRECISION = paramManager->SHOOT_PRECISION;	/*允许射门最小精度角分母，越大越慢越精确 最低为7最高17*/
	GetBallBias = paramManager->AdGetBallBias;	/*AdvanceGetball的偏差*/
	BalltoMeVelTime = paramManager->BalltoMeVelTime; /*Advance传球给我主动去接的临界时间*/
	/*射门力度参数*/
    ADV_FPASSPOWER_Alpha = paramManager->ADV_FPASSPOWER;
    ADV_CPASSPOWER_Alpha = paramManager->ADV_CPASSPOWER;
    // max:600 350
	RELIEF_POWER = paramManager->RELIEF_POWER;
    BACK_POWER = paramManager->BACK_POWER;
	Advance_DEBUG_ENGINE = paramManager->Advance_DEBUG_ENGINE;

	Intercept = paramManager->INTERCEPT;//是否打开getball的拦截球功能（可能导致碰撞）。一般关闭，该功能目前不完善。
	//touch参数
	Touch_Get_Bias_Angle = paramManager->TOUCH_GET_BIAS_ANGLE;
	Touch_Angel = paramManager->TOUCH_ANGEL;//可以touch的角度阈值
	Touch_Vel = paramManager->TOUCH_VEL;
	//break开关
	BreakOn = paramManager->BREAK_OPEN;//是否允许使用break。0为关闭，1为开启BREAKING，2为开启BREAKING和BREAKSHOOT。一般设置为2。
	//我方半场CHIP解围开关
	ChipOn = paramManager->CHIPRELIEF_OPEN;//0为关闭，1为开启。打开后，我方半场双方均离球很近时，会使用CHIP解围；关闭后，会使用GET或BREAKING。一般设置为1。
```

点球参数：

```
	Penalty = task().player.isPenalty;//判断当前是否为点球，通过外部传入
	useChip = paramManager->USE_CHIP;//射门是否使用挑射
	Pushout_power = paramManager->PUSHOUT_POWER;//带球时每次推球力度
	ChipDist = paramManager->CHIP_DIST;//敌方球员到球距离小于ChipDist时，直接挑射
	EndPushX = paramManager->END_PUSH_X;//自身位置的x坐标超过EndPushX时不再推球，进行射门
	Penalty_chipPower_percent = paramManager->PENALTY_CHIPPOWER_PERCENT;//挑射力度百分比，100为原力度（根据距离计算得到）
	useWait = paramManager->USE_WAIT;//在射门前停顿并射门（增加射门稳定性）
	waitTime = paramManager->WAIT_TIME;//停顿的帧数
	PenaltyTime = paramManager->PENALTY_TIME;//点球允许的总时间，超过时间会直接进入射门状态。建议设置短于真实允许的时间。
```

### 状态机设计

(plan函数中)第一个swtich作为状态分配，第二个switch作为状态执行。

状态转移思路：只有GET状态可以转移到其他状态，其他状态只能保持当前状态或转移到GET。

以下为所有状态，代码中的状态执行部分均有注释解释其功能。

1. GET：拿球状态，主要调用GetBall。
2. KICK：射门状态，内含Getball和ShootBall
3. PASS：传球状态，内含FLAT、CHIP、Getball
4. JUSTCHIPPASS：后场解围，内含CHIP、Getball
5. BREAKSHOOT：Break射门技术，背身拿球时采用Getball调整朝向
6. BREAKPASS：Break传球技术
7. PUSHOUT：推球状态。不断小力向前推球并跟上。目前不再使用，实战作用小且不稳定，仅作为备选状态。
8. CHASEKICK：追球射门。直接调用ChaseKickV2，目前不使用。
9. TOUCH：Touch射门。Touch时机器人提前等在球的路径上，碰到球后不吸球直接踢出，速度快。最适用于角球传球射门。
10. WAIT：原地吸球等待。点球时使用的状态。

注：Break为一个吸球移动的skill。Break进攻效果好，但踢出的球精度不高，且吸球移动时可能丢球。

老版advance中对于normalpush的设计引用了太多的pullcnt等参数设计，然而在实际比赛上如果对手采用lose就getball的策略，那么normalpush和lightkick等状态设计是不可靠的，故舍弃。

常规模式思路：参考Get的状态转移，代码中主要为GenerateNextState()函数，函数中分区域（MeIsInWhichArea）来判断应该转移到什么状态。
点球模式思路：一直PUSHOUT直到敌方靠近或位置较前时CHIP或KICK射门。设置了计时器，超时则直接射门。Penalty=1时为点球模式。

### GET

1. 如果有球，在前场时优先考虑射门，其次考虑可能有的break，最后考虑传球
   射门采用tendToShoot判断，传球采用CanSupport判断
2. 如果无球，考虑防守与常规两种情景
   -  防守进行ChaseKick
   -  否则调用Getball，Getball中会区分各种其他情景

### KICK

1. 采用isDirOK判断此时朝向是否正确
2. 朝向在误差范围内采用ShootBallV2
3. 朝向不可接受采用Getball进行调整

### PASS

1. 优先考虑平传球，仍然采用isDirOK的判断方法，同KICK
2. 否则考虑挑球，仍然采用isDirOK的判断方法，同KICK

### BREAKSHOOT

吸住球移动一小段距离后射门。

1. 若多人拦截且有合适support队员，传球
2. 否则调用break

### BREAKING

吸球移动进行突破、传球

1. 若敌方距离很远，向球门方向推球。不常见。
2. 突破敌方车辆后，挑传给support队员。

### TOUCH

首先调整位置，移动到接球点并面向球门。然后调用touch打门。

### 补充内容与部分思路

1. 所有射门角度计算采用KickDirection中的getPointShootDir
2. 所有踢球方式采用JustKick
3. 所有跑位方式采用GetBallV5(NoneTrajGetBall)

#### tendToShoot

计算敌人与踢球路径距离判断是否能够阻挡

具体方法为首先生成射门点与射门方向，同时计算所有敌人到直线距离与阈值进行判断

#### CanSupportKick

通过`GPU`算点生成点位，考虑传球角度是否过大、传球距离是否过大，接球车是否离地方球门过远

同时此处不考虑敌方能否拦截球

#### toChipOrToFlat

通过判断敌方能够拦截球选择平传还是挑传

#### isDirOK

采用比较当前误差与先前误差、理想情景的方法
敌人getball + 离球门足够近时适当放宽精度限制，增添快速出球判断
新增误差允许时的出球判断
因为存在ReceivePass，考虑传球精度可以适当比射门精度低

#### GenerateBreakPoint

Break拉球射门时自身自带速度，即已知射门点，自身速度与自身方位，需要得到射门方向与射门力度

采取工程化的修正

#### GetPassPower

已知距离求得所需力度

#### PassDirInside

`GPU`算点得到若干`support`点位，考虑一下因素判断应当传给哪个`Support`点位

- 是否有人在传球点附近
- 我到该点的距离
- 该点到球门的距离
- 敌人到该点射门线的距离
- 我传给该点所需要调整的`Dir`大小

其中部分因素的影响设置为：如果满足某个阈值才能够作为传球点

随后枚举可能的传球点，优先考虑区域1和区域4的点位。