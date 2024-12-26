# 开始的开始—ssl_strategy
当启动core,进入```ssl_strategy.cpp```,它负责初始化整个程序,并启动各个模块.
## init

![image-20241213202921893](ssl_strategy.assets\image-20241213202921893.png)

对各个模块进行初始化,包括视觉模块,传感模块,决策模块,动作模块等.关于单例模式,请参考[这里]([2.1.2  单例与指针 - SJTU-SRC Wiki](https://sjtu-src.github.io/Wiki/chapter_software/sub_chapter_cpp/单例与指针/))

- 首先通过```optionModule```向```client```获取信息包括是否为仿真模式(IS_SIMULATION),以及选边信息(option)
- 然后根据```option```初始化VisionModule,初始化gameState
- DecisionModule和ActionModule初始化.需要注意的是在```CDecisionModule```模块初始化时,lua层也进行初始化.
    ```cpp
    CDecisionModule::CDecisionModule(const COptionModule* pOption, CVisionModule* pVision): _pOption(pOption),_pVision(pVision)
    {		
            if(USE_LUA_SCRIPTS){
                //LuaModule::Instance()->RunScript("../lua_scripts/test/Init.lua");
                LuaModule::Instance()->RunScript("../lua_scripts/ssl/StartZeus.lua");
            }
    }
    //StartZeus.lua即lua层入口
    ```
- 建立从```client```获取信息线程(```DataReceiver4rbk```)和机器人通讯线程(```RobotSensor```).
??? tip "ActionModule初始化"
    - 在ActionModule中,需要建立向机器人发送指令的信息流通渠道,因此需要一套通讯协议,在falcon中,使用的是protobuf,protobuf是一种通讯协议，用于在不同的软件之间通讯，protobuf可以被转化为多种语言的文件用于编译
    - udp协议,是一种网络协议，用于在网络上传输数据，udp协议是一种无连接的协议，即发送数据时不需要建立连接，直接发送数据包，接收数据时也不需要建立连接，直接接收数据包。
    - protobuf与udp的结合使用，可以实现在网络上传输protobuf格式的数据，protobuf格式的数据是一种二进制格式的数据，可以减少传输的数据量，提高传输的效率。如果将信息传输比作送快递,udp和tcp就相当于顺丰和中通,proto是快递箱，规定了内容的形状.[参考](https://blog.csdn.net/jiushimanya/article/details/82684525)
    -![image-20241223202853801](ssl_strategy.assets\image-20241223202853801.png)



## loop

如果我们将整个系统借助arduino的理解方式,可以将上一部分理解为```setup()```,负责初始化.而接下来要介绍的相当于```loop```函数,整个系统大部分功能在此循环执行.

![image-20241213205103055](ssl_strategy.assets\image-20241213205103055.png)

每一帧会进行的步骤包括：

1. **更新比赛所需要的gameInfo**:gameInfo主要包括视觉信息和裁判信息,包括球的位置、球的速度、球员的位置、方向速度等视觉信息和进球数、门将id等裁判盒信息。
2. **DoDecision**:根据gameInfo进行任务的产生与分配。
3. **sendAction**:将生成的task分配给小车,生成动作指令。
4. **GDebugEngine::Instance()->send**:根据双方选边,将各自的debug信息打印在canvas上。接着清除该帧的debug信息,以免造成视觉障碍。

通过以上步骤,系统可以在每一帧都进行有效的循环执行,确保比赛策略的实时更新和执行。

