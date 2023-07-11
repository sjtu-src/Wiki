### 写在前面

- 世界赛TDP，全名Team Description Paper，是每年时间赛前参赛队伍必须提交的论文
- 论文重点描述队伍在过去的一年内的技术发展，要求描述详细，复现性高，有极高的参考价值
- 世界赛的所有TDP可以在官网上查到，[TDP](https://ssl.robocup.org/team-description-papers/) 链接
- 部分有队员看过，感觉有价值的已经存到云盘，也可以从上面下载，[云盘](https://jbox.sjtu.edu.cn/l/eHE7uQ) 链接，进去找“内部学习资料/robocup小型组论文”即可
- 下面介绍一些有价值的TDP，欢迎大家补充

### ZJUNlict

- 浙大的TDP，价值爆满
- 因为我们的软硬件系统都是从浙大继承过来的，看他们历年的TDP有助于我们更加了解目前的系统，一些琢磨不透的工程处理也许可以从中找到答案，一些我们尚不了解的模块也可以作为第一手资料开始学习。总之，对于我们的传承和重构，都有重要意义
- 之后的目标是整理浙大历年的TDP，搞清楚软件系统的发展脉络，更加熟悉各模块准备重构，并收录专业解释用于编纂教材
- 硬件部分，看的较少，价值待定

#### 2009

- 视觉部分不要看了，当时还没有SSL-Vision，现在不需要自己写标定、识别的算法了

+ AI结构：play/subplay/agent/skill
+ 重要引用：Bruce J.R. Browning B. Skills tactics and plans for multi-robot control in adversarial
environments. Journal of System and Control Engineering, 2005.
  
![Decision2009Text](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/Decision2009Text.png)

![Decision2009](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/Decision2009.png)

+ 系统延时测量实验，测量从视觉图像捕捉到机器人接到运动指令之间的延时
+ 方法是给机器人发速度，数值呈正弦函数变化，看机器人走到最远距离和发出0指令之间的时间
+ 重要引用： Yonghai Wu Yu Sheng. Motion prediction in a high-speed, dynamic environment. Proceedings of 17th IEEE International Conference on Tools with Artificial Intelligence (ICTAI), 2005

- 挑球轨迹跟踪，落点估计

+ 路径规划，A*算法
+ 训练神经网络处理速度指令，以适应硬件性能

- Skill方面，GetBall的雏形，和现在比较像的是都是绕到球后面拿球，有large/smallAngle的雏形

![GetBall](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/GetBall.png)

- 开始半智能算点，算力不够（毕竟当时还用Win XP），考虑的因素较少、条件限制太死，搜索的范围也较小

#### 2011

- 开始使用SSL-Vision，新添WorldModel，包括视觉及传感器输入、历史决策信息和延时补偿
- 更加详细地说明AI结构，playBook/play/subplay/agent/skill，每个play中的任务是固定的（比如一个车固定向底线跑，然后把球传给他，他再传中），其中的subplay主要分进攻和防守两种，所以新添playBook来完成切换play的作用，丰富决策
- agent层里面使用状态机处理复杂动作，根据现在的状态调用合适的skill，例如传球给队友，需要先后调用拿球、转向和踢球的skill，期间还要判断能不能传出、多大力传出的问题，所以skill层就是些再基础不过的动作，例如跑点和踢球，不再判断状态，只负责执行

![Decision2011](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/Decision2011.png)

+ 引入贝叶斯理论分析比赛局势，判断进攻还是防守，输出结果更加平稳，结合了历史信息也使得对于一些队伍的战术更有针对性
+ 引用：Sebastian Thrun, Wolfram Burgard, Dieter Fox, Probabilistic Robotics, The MIT
Press

#### 2012

- 重构AI框架，去除了subPlay，play逐渐接近现在的脚本，包括有限状态机、跳转条件、分配角色和任务，各部分都有可调用的脚本，不单单是C++
- 充分利用WorldModel，特别是脚本里的状态判断交给WorldModel计算，再返回结果，现在lua里也好像有这种写法  
- 重要引用：Brett Browning, James Bruce, Michael Bowling and Manuela Veloso, STP: Skills,
tactics and plays for multi-robot control in adversarial environments

![Decision2012](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/Decision2012.png)

+ 其他部分之前几年的TDP都有提到，唯一的改进是智能算点开始采用CUDA，以一定精度在矩形内取点计算分数

#### 2013

- 出现了极为经典的AI框架图，其中PlayBook、Play和Agent层都用脚本语言LUA
- Play中的角色分配开始采用RoleMatch，使用Munkres算法分组顺序匹配角色，以到目标点的距离为标准，分有三种匹配模式
- 重要引用：Munkres, J.: Algorithms for the assignment and transportation problems. Journal of the Society for Industrial & Applied Mathematics 5(1), 32–38 (1957)  
- 感觉当时的Agent层和现在的Skill层更像，多种条件之间相互跳转，有三种跳转方式（顺序、计数器、优先级）
- Control Module开始使用RRT和Bang-Bang Control，加入了DMPs
- 重要引用：
  - Bruce, J., Veloso, M.: Real-time randomized path planning for robot navigation.In: IEEE/RSJ International Conference on Intelligent Robots and Systems 2002, vol. 3, pp. 2383–2388. IEEE (2002)
  - Sonneborn, L., Van Vleck, F.: The Bang-Bang Principle for Linear Control Systems. Journal of the Society for Industrial & Applied Mathematics, Series A: Control 2(2), 151–159 (1964)
  - Ijspeert, A.J., Nakanishi, J., Schaal, S.: Movement imitation with nonlinear dynamical systems in humanoid robots. In: International Conference on Robotics and Automation, pp. 1398–1403. IEEE, Washington, DC (2002)  
  - Park, D., Hoffmann, H., Pastor, P., Schaal, S.: Movement reproduction and obstacle avoidance with dynamic movement primitives and potential fields. In: IEEE-RAS International Conference on Humanoid Robotics (2008)
  - Kober, J., M¨ulling, K., Kr¨omer, O., Lampert, C.H., Sch¨olkopf, B., Peters, J.: Movement templates for learning of hitting and batting. In: IEEE International Conference on Robotics and Automation 2010, pp. 1–6 (2010)
  - Pastor, P., Hoffmann, H., Asfour, T., Schaal, S.: Learning and generalization of motor skills by learning from demonstration. In: Proc. of the International Conference on Robotics and Automation (2009)

![Decision2013](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/Decision2013.png)

#### 2014

- 介绍了Defence Strategy，基本思路沿用至今，如下图，defendKick、Marking经典防守Skill从此诞生

![DefenceStrategy](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/DefenceStrategy.png)

- 也提到了一个区域联防的概念，大概就是梳理Marking站位，使得一个进攻车摆脱防守后另一个车能快速补位

#### 2015

- 又一次比较系统地介绍了AI框架，说明了各部分的功能和定位，如下图，部分结构我们现在还有(Play/Skill/ControlModule/WorldModule)，主要区别在于我们不使用贝叶斯理论选择脚本，目前也把Agent和Skill两层合并，对Agent感兴趣可以去看看cond.lua，其实我们现在就是把决策树也做到了C++里，成为了更复杂的Skill，如Advance系列

![OldStructure](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/OldStructure.png)

- 也说了Defence Strategy，和上一年的差不多

- 新添一个Log分析的工具

#### 2016

- 新的Normalplay写法，不再使用有限状态机，而是评估场势、生成进攻或防守阵型，并用贝叶斯理论从中选择最合适的执行（我们从未使用过这种方法），里面提到了learning module，但并未介绍
- 开始简化上述提到的软件结构，主要研究Play-Skill结构

![NormalPlay2016](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/NormalPlay2016.png)

- 参数动态调整模块，利用真实达到和预期的数值之间的差值计算补偿

#### 2017

- 主要是视觉模块，包括挑球轨迹跟踪、球碰撞模型等

#### 2018

+ 重构视觉模块，思路与现在基本一致

- 新的运动控制算法，我们研究好现在用的之后可以看看这个

+ 参数动态调整模块的更新，补偿调整接球角度

- 重构或者说是更细化地讲解NormalPlay，JugdeModule和DecisionModule，基本思路沿用2016年的，根据场势确定进攻球员数量、生成阵型并执行
- 策略以球为主，场势估计关注球的控制权、位置，Skill分配也是先保证getBall，其他车跑合适的接球点
- 持球车(Advance)的决策倾向于转移球，除了Pass和Shoot外，添加了Light Kick or Chip，防止被对方怼住

![PassStrategy](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/PassStrategy.png)

#### 2019

- 对于SSL-Vision的改进方案

+ 通过路径规划、轨迹生成算法的改进，可以比较精准预测车到点的时间，以此规划拦截球的点位和优化Marking

#### 2020

- 建模球的运动模型，结合接球车的到点时间计算合适的传球力度

+ 优化传球射门决策，将场地分为多个区域来协调阵型，面向持球车的传球方向来计算点的价值，新添Break和摆脱防守的Skill增加传接球灵活度
+ 优化定位球策略，将计算放到了BallPlacement阶段

### CMU

- 五届冠军得主，历史排名第一的队伍，拥有充分可以挖掘的空间
- 他们的STP(SKill/Tactics/Play)结构和我们的很像，并且从15年就已提出了区域算点的算法，很符合我们的发展方向

### Skuba

- 泰国球队，历史第四队伍，唯一一个四连冠壮举
- 可惜他们14年就不打了，策略并未同步大场多车情况，但他们的车硬件很不错，可以快速拿球爆射

### TIGERS

- 德国球队，后起之秀，硬件方面的设计可以多参考些
- 目前传球较好的队伍之一，17～19年的TDP，详细介绍了他们的好的传球点位的判断方法和"One Strategy, One Score"

### Parsian

- 伊朗球队，开源grSim的队伍，亮点在于用Ros搭建系统

### ERForce

* 德国球队，我们17年世界赛的决赛对手，不过近几年表现一般，他们的仿真器设计可以参考下，较grSim占用资源较少

### RoboFEI

* 巴西球队，有一个自动调整PID参数的系统设计