## 基本原理：
通过计算球员对球“势能”的大小，形成我方球员和对方球员的两个势能列表，由小到大排列，列表第一项，即最小的那个对应的车的编号即为BestPlayer,并在每一次视觉循环时更新一次  
输入:   
      ourPalyer   - 我方球员位置  
      otherPlayer - 对方球员位置  
      ball        - 球的位置  
      biases      - 各个影响因素的参数    
输出:  
      result      - 双方最佳的拿球队员  
      Potentials  - 我方&对方5个车的potential  
## 需要考虑的因素：
biases(0)  -   DistBallToPlayer   离球的距离,越近越好  
biases(1)  -   shootAngleDiff     跟球到对方球门的角度，相差越小越好  
biases(2)  -   ClearPah           球和车直接是否有对方车  
biases(3)  -   anglePlayerToBall  车的方向和车到球的方向的角度，相差越小越好  
biases(4)  -   LastBallPlayer     上一周期的拿球队员  
## 六个重要函数： (详细函数参数见后说明） 
1.  double distBallToPlayer() 返回球员到球的距离的“修正值”
2.  double shootAngle()  返回球员与门和与球员球的夹角的一半的sin值*相关系数
3.  double clearPath() 判断敌方车对我方是否形成阻挡(我方车与球之间是否有敌方车）
4.  double theirclearPath() 判断我方对敌方是否形成阻挡
5.  double anglePlayertoBall() 车和球之间的角度因素
6.  double velBallToPlayer() 相对速度因素
## 执行步骤：（在每一次视觉循环里）
1.  更新门将信息（判断门将是否出禁区，是否换车）  
2.  更新球信息（球的位置、球员据球最远距离（作为maxdist为后面函数提供参数）、哪方在控球、）
3.  更新我方球员情况（是否换车，是否还在场上，**计算势能列表**)  
_Potentials[i-1][6](i-1表示第i台车，共有7个参数）=distFactor*_Potentials[i-1][1]+velFactor*_Potentials[i-1][5];(distFactor&velFactor为修正参数）  
_Potentials[i-1[1]=distBallToPlayer(playerToKickPos,biases,MaxToBallDist);  
_Potentials[i-1][5] = velBallToPlayer(pVision->OurPlayer(i),pVision->Ball(),biases,MaxToBallDist);  
_Potentials[i-1][2]到_Potentials[i-1][4]:0  
_Potentials[i-1][0]=_Potentials[i-1][6] **本周期计算出的最终第i台车的势能**  
迭代：最终_Potentials[i-1][0]=0.75* 本周期势能+0.25* 上周期势能  
4.  更新我方最优球员情况（根据步骤3判断最优球员是否发生变化）  
5.  &6.  对对方球员执行3.4步相同操作
## 源码展示：distBallToPlayer 与velBallToPlayer
```cpp
double CBestPlayer::distBallToPlayer(CVector playerToBall,const double *biases,double maxDist)
{
	//计算距离的影响
	double DistPlayerToBall = playerToBall.mod();			//c  0~1
	return (biases[0] * DistPlayerToBall / (maxDist+1.0));	//--Potential
}
```
```cpp
double CBestPlayer::velBallToPlayer(const PlayerVisionT& player,const MobileVisionT& ball,const double *biases,double maxDist)
{
	/// 限制球速大小为8m/s
	double limited_ball_speed = 800;
	if (! ball.Valid()) {
		limited_ball_speed = 50;
	}
	CVector applicable_ball_vel = ball.Vel();
	if (ball.Vel().mod() > limited_ball_speed) {
		applicable_ball_vel = Utils::Polar2Vector(limited_ball_speed,ball.Vel().dir());
	}

	double maxProjDist=80;
	CGeoLine ballVelLine=CGeoLine(ball.Pos(),ball.Pos()+applicable_ball_vel);
	CGeoPoint proj=ballVelLine.projection(player.Pos());
	double dist=player.Pos().dist(proj);
	if (ball.Vel().mod()<30||!ball.Valid()){
		dist = player.Pos().dist(ball.RawPos());
	}
	dist=min(dist,maxProjDist);
	dist=max(dist,10.0);

	/// 考虑球靠近球员还是远离球员
	const double own_vel_alpha = 0;
	CVector playerToBall = ball.RawPos() - player.RawPos();	
	CVector diffVel = applicable_ball_vel - player.Vel()*own_vel_alpha;
	double angleDiff = Utils::Normalize(diffVel.dir() - playerToBall.dir());
	// 计算值
	double ballMovingCost = diffVel.mod() * cos(angleDiff);
	//ballMovingCost += diffVel.mod() * fabs(sin(Param::Math::PI-fabs(angleDiff)));

	
	if (ballMovingCost >= maxDist) {
		ballMovingCost = maxDist;
	} else if (ballMovingCost <= -maxDist) {
		ballMovingCost = -maxDist;
	}

	double ballFactor = (ballMovingCost) / (maxDist+1.0);
	//double finalBallFactor=0.5* ballFactor+0.5;

	double yDistFactor=0.5;
	if (ball.Vel().mod()>600){
		yDistFactor=1.3;
	}else if (ball.Vel().mod()>400){
		yDistFactor=1.1;
	}else if (ball.Vel().mod()>350){
		yDistFactor=1;
	}else if (ball.Vel().mod()>280){
		yDistFactor=0.8;
	}else if (ball.Vel().mod()>220){
		yDistFactor=0.65;
	}else if (ball.Vel().mod()>160){
		yDistFactor=0.45;
	}else if (ball.Vel().mod()>100){
		yDistFactor=0.3;
	}else{
		yDistFactor=0.1;
	}

	double finalBallFactor = 0.5 * ballFactor + yDistFactor*dist/maxProjDist;
	//if (VERBOSE_MODE) cout << "ballMovingCost: " << ballMovingCost <<" "<<"ballFactor: "<<ballFactor <<endl;
	if (ball.Vel().mod()<70){
		return 0;
	}else{
		return biases[0] * finalBallFactor;
	}
}
//biases[5]列表是一个参数列表，在此cpp里规定为 { 0.7, 0.0, 0.15, 0.0, 0.15 }
```
## 评价：
此cpp计算势能时还是只考虑了距离和相对速度，没有将其他因素计算在内，可能是在实践中效果不好；但是在更新门将和球信息这块做得很好


