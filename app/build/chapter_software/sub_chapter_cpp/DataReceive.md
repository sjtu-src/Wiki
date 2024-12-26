
# 信息处理
## 初始化与信息获取
信息的获取主要是在CDataReceiver4rbk类和CRobotSensor类中完成的，初始化时，会启动三个线程，一个用于接收 referee 信息，一个用于接收 vision 信息, 另外一个用于获取机器人信息。
!!! tip "多线程"
    多线程的目的是为了提高程序运行的效率，避免阻塞主线程，同时保证信息的实时性。在falcon中使用了非常多的线程，包括vision、referee、场势计算等，这些线程的运行是相互独立的，不会相互影响。
### Vision & Referee
```cpp
//仅展示核心代码,详情见DataReceiver4rbk.cpp
    referee_thread = new std::thread([=] {receiveRefMsgs();}); //创建新线程
    referee_thread->detach(); \
    //detach 方法将线程与当前执行的代码脱离开，使得线程在后台独立执行，调用 detach 后线程不再与主线程关联。
    receive_vision_thread = new std::thread([=] {receiveVision();}); 
    receive_vision_thread->detach();
```
此时,referee_thread 和 receive_vision_thread 已经在后台独立运行,调用```receiveRefMsgs()```和```receiveVision()```函数,从而不断获取 referee 和 vision 信息。

由于接受信息的方式大同小异,我们以 Vision 信息为例,展示其具体实现。
```cpp
void CDataReceiver4rbk::receiveVision() {
    // 定义一个QByteArray类型的buffer用于存储接收到的数据
    QByteArray buffer;
    // 无限循环，持续接收数据
    while (true) {
        // 每次循环开始时，线程休眠2毫秒，避免CPU资源占用过高
        std::this_thread::sleep_for(std::chrono::milliseconds(2));
        // 检查UDP套接字是否处于绑定状态，并且是否有待处理的数据报
        while (receive_vision_socket->state() == QUdpSocket::BoundState && receive_vision_socket->hasPendingDatagrams()) {
            // 调整buffer的大小以适应待处理的数据报的大小
            buffer.resize(receive_vision_socket->pendingDatagramSize());
            // 从UDP套接字读取数据报，存储到buffer中
            receive_vision_socket->readDatagram(buffer.data(), buffer.size());
            // 锁定互斥锁，确保数据解析的线程安全
            receive_vision_mutex.lock();
            // 使用ParseFromArray方法解析buffer中的数据到rec_vision对象
            rec_vision.ParseFromArray(buffer, buffer.size());
            // 解锁互斥锁，释放资源
            receive_vision_mutex.unlock();
            // 触发visionEvent事件，通知其他部分有新的视觉数据可用
            visionEvent.Signal();
        }
    }
}
```
### RobotStatus
```cpp
// 仅展示核心代码,详情见RobotSensor.cpp
    // 创建一个新的QUdpSocket对象，用于处理UDP通信
    robot_status_socket = new QUdpSocket();
    // 绑定该UDP套接字到所有可用的IPv4地址，并指定端口号
    // QUdpSocket::ShareAddress允许与其他套接字共享相同的地址和端口
    robot_status_socket->bind(QHostAddress::AnyIPv4, port, QUdpSocket::ShareAddress);
    // 创建一个新的线程，用于接收机器人状态信息
    robot_status_thread = new std::thread([=] {receiveRobotStatus();});
    // 将新创建的线程从主线程中分离，使其独立运行
    robot_status_thread->detach();
```
此时robot_status_thread 已经在后台独立运行,调用```receiveRobotStatus()```函数,从而不断获取机器人状态信息。需要注意的是与vision和referee信息不同的是，机器人状态信息是直接通过机器人得到的,而vision和referee信息是通过client接收到的。

??? summary 
    此时获得的所有信息都是client或机器人发来的原始数据.分别保存在```rec_vision,ssl_referee```,```robot_status```对象中,需要经过处理才能得到我们想要的数据。

## 信息维护

每一帧会调用```getGameInfo```,将rawdata处理写入info,以便其他模块使用。info (1)是一个结构体，包含了当前帧的所有信息，包括 referee 信息、vision 信息、机器人状态信息等。
{ .annotate }

1.  见server.h![](data_receive.assets\image-20241223213932021.png)

```cpp
bool CDataReceiver4rbk::getGameInfo(const COptionModule *pOption,GameInfoT& info){
    visionEvent.Wait();
    //get rawvision into visualinfo
	if (!rawVision2VisualInfo(pOption,info)){
		return false;
    }
    getNewRefMsgs(info);

	return true;
}
```
### SetNewVision
主要实现位于VisionModule.cpp中的SetNewVision中
!!! danger "两个VisionModule"
    在falcon中,有VisionModule.cpp和visionmodule.cpp两个VisionModule,前者位于client路径下,是用于处理摄像头直接发来的信息(origin),将其处理并呈现在client中FilterB和FilterY.包括对球的处理(dealball),对机器人的处理(dealrobot).后者位于core下,是用于策略框架进行决策所需的视觉信息的处理,包括对球,机器人的位置,速度等信息.
    ``` mermaid
    graph LR
       A{视觉机数据} -->|client| B{visionmodule};
       B -->D(dealball);
       B --> E(dealrobot);
       D --> |merge,choose...|F(球的真身)-->|core|C{VisionModule};
       E --> |merge,chosse...|G(机器人的真身)-->|core|C;
    ```
=== "记录调试信息"
    - 根据选边将原始信息进行反向,确保从我方视角制定策略时,我方始终处于左半区域,笛卡尔坐标定义<x y theta>,降低后续策略的复杂度
    ```cpp
    const bool invert = !(_pOption->MySide() == Param::Field::POS_SIDE_LEFT);
    ```

=== "位置预测"

    - 容错和滤波处理：由于原始数据包含测量噪声，有时还有信息不全和错误的情况发生，所以需要先进行滤波和容错处理。这里采用的kalman 滤波算法。(迁移至client)
    - 预测：由于摄像机硬件和图像处理费时的原因，视觉信息存在 100ms 左右的延时。所以必须进行预测才能得到机器人和球的真实位置。这里总共尝试过基于神经网络的预测模型和线性预测模型。(迁移至client)
    - 碰撞模型：在球被机器人挡住时，采用基于碰撞模型的算法对球的位置进行估计。(迁移至client)
    - 最后根据下位机的红外信息对机器人位置进行进一步修正。
    ```cpp
    _ballPredictor.updateVision(vInfo, invert); // 球的预测
    
    // 机器人的预测
    for (int i = 0; i < Param::Field::MAX_PLAYER; ++ i) {
    	const VehicleInfoT& ourPlayer = vInfo.player[i];
    	const VehicleInfoT& theirPlayer = vInfo.player[i+Param::Field::MAX_PLAYER];
    	_ourPlayerPredictor[i].updateVision(vInfo.cycle, ourPlayer, thisBall, invert);
    	_theirPlayerPredictor[i].updateVision(vInfo.cycle, theirPlayer, thisBall, invert);
    }
    ```
    球,机器人处理后的数据写入到```CBallPredictor```和```CRobotPredictor```的```_vision```中,接口为```_ballPredictor.getResult(_timeCycle),_ourPlayerPredictor[num].getResult(_timeCycle);```.
    最后封装为喜闻乐见的```pVision->ball,pVision->player```.

=== "更新决策信息"

    ```cpp
    // 球状态模块更新状态
    BallStatus::Instance()->UpdateBallStatus(this);
    
    // 更新敌我双方对于球的势能，越小越有利于拿球，贝叶斯滤波中有使用
    BestPlayer::Instance()->update(this); // 暂时去不掉，缺少OurBestPalyer的替换
    
    // 更新贝叶斯滤波器，评估目前比赛攻防形式
    
    // 更新防守信息
    DefenceInfo::Instance()->updateDefenceInfo(this);
    DefenceInfoNew::Instance()->updateDefenceInfoNew(this);
    ```
    其中```DefenceInfo```和```BestPlayer```已集成至```DefenceInfoNew```中

=== "更新裁判盒信息"
	- 检查球是否被踢出
    - 根据裁判盒指令(ref_mode)和球是否被踢出(_ballKicked)综合得出当前的gameState,并写入到core里的_refereeMsg中,用于后续策略决策
	```cpp
    CheckKickoffStatus(vInfo);
	int ref_mode = vInfo.mode;
    int next_ref_mode = vInfo.next_mode;
	// 更新裁判盒信息，一般当且仅当比赛模式为停球状态时，判断球是否被踢出
    if (ref_mode >= PMStop && ref_mode < PMNone) {
        _gameState.transition(playModePair[ref_mode].ch, _ballKicked);
        _next_gameState.transition(playModePair[next_ref_mode].ch, _ballKicked);
	}

	//更新裁判盒信息
	UpdateRefereeMsg();
	```
	
	!!! tip
	    需要注意的是除_refereeMsg外,_ourGoal,_Goalie等可直接由裁判盒指令得到的信息在```SetRefRecvMsg```中已经被更新.
	    ![image-20241224222411979](data_receive.assets\image-20241224222411979.png)

## 信息发送
### sendAction
主要实现位于ActionModule.cpp中的sendAction中

- 第一步: 遍历小车，获取赋予的任务
```cpp
	for (int vecNum = 0; vecNum < Param::Field::MAX_PLAYER; ++ vecNum) {
		rbk::protocol::Message_SSL_Command* ssl_cmd = nullptr;

		CPlayerTask* pTask = TaskMediator::Instance()->getPlayerTask(vecNum);
		
        pCmd = pTask->execute(_pVision); 
        //获取当前任务 
```
这里```playerTask```具体见DecisionModule,最后结果是任务层层调用执行，得到最终的指令：```<vx vy w> + <kick dribble>```,封存在```pTask->excute(_pVision)```中.
- 第二步: 跑,踢指令生成

```cpp
	// 跑：有效的运动指令
    if (pCmd) {
        dribble = pCmd->dribble() > 0;
        // 下发运动 <vx vy w>
        if(ssl_cmd == nullptr){
            ssl_cmd = cmds.add_command();
            ssl_cmd->set_robot_id(vInfo.player[pCmd->number()].ID);
        }

        ((CPlayerSpeedV2*)pCmd)->setSpeedtoSSLCmd(ssl_cmd);
        // 记录指令
        _pVision->SetPlayerCommand(pCmd->number(), pCmd);
    }
```
运动指令和踢控指令生成大同小异,这里以运动指令为例.

ssl_cmd是对每个机器人来说,解析pCmd后得到的指令,具体见```CPlayerSpeedV2::setSpeedtoSSLCmd``` (1) ,最后将ssl_cmd写入到cmds中.
{ .annotate }

1.  见server.h![image-20241226220517788](data_receive.assets\image-20241226220517788.png)

最后记录本周期我方机器人执行的指令，保存到历史堆栈里.

- 第三步: 指令下发
```cpp
	sendToOwl(cmds);

	// 清除上一周期的射门指令
	KickStatus::Instance()->clearAll();
	// 清除上一周期的控球指令
	DribbleStatus::Instance()->clearDribbleCommand();
```
每个机器人的ssl_cmd都写入到cmds中,最后通过```sendToOwl(cmds)```将cmds发送至client,由client统一发包给下位机.


!!! summary
    ![core](data_receive.assets\core.png)