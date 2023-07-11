---
layout: default 
title: Advance
---

> Tyh 22.10

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
```

### 状态机设计

第一个swtich作为状态分配，第二个switch作为状态执行。

1. GET：拿球状态，主要内容为GetBall和RecivePass
2. KICK：射门状态，内含Getball和ShootBall
3. PASS：传球状态，内含FLAT、CHIP、Getball
4. JUSTCHIPPASS：后场解围，内含CHIP、Getball
5. BREAKSHOOT：Break射门技术，背身拿球时采用Getball调整朝向
6. BREAKPASS：Break传球技术

 老版advance中对于normalpush的设计引用了太多的pullcnt等参数设计，然而在实际比赛上如果对手采用lose就getball的策略，那么normalpush和lightkick等状态设计是不可靠的，故舍弃。

### GET

1. 如果有球，在前场时优先考虑射门，其次考虑可能有的break，最后考虑传球
   射门采用tendToShoot判断，传球采用CanSupport判断
2. 如果无球，考虑防守与进攻两种情景
   -  防守进行ChaseKick
   -  进攻时考虑球是否传向我自己，采用isPassBalltoMe判断。

### KICK

1. 采用isDirOK判断此时朝向是否正确
2. 朝向在误差范围内采用ShootBallV2
3. 朝向不可接受采用GetBallV3进行调整

### PASS

1. 优先考虑平传球，仍然采用isDirOK的判断方法，同KICK
2. 否则考虑挑球，仍然采用isDirOK的判断方法，同KICK

### 补充内容与部分思路

1. 所有射门角度计算采用KickDirection中的getPointShootDir
2. 所有踢球方式采用ShootBallV2
3. 所有跑位方式采用GetBallV3

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