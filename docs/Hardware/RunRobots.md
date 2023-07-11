
在硬件层面介绍下如何让小车跑起来

## 启动机器人

### 正确拨码

![code](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/code.png)

- 拨码盘从左到右依次为通讯频率、机器人号码和模式
- 所有拨码为二进制编码，右侧为低位，左侧为高位，拨动开关在下为0，在上为1，如上图中均为0
- 通讯频率范围0~9，具体的物理意义参考[发射机原理说明](https://gitlab.com/src-ssl/src/-/wikis/Hardware/发射机原理说明)
- 机器人号码范围0~11，是现有通讯协议中定义的
- 模式一般为0，若有其他需求请查阅[机器人模式说明](https://gitlab.com/src-ssl/src/-/wikis/Hardware/机器人模式说明)
- 注：此处的编码数值只在机器人启动时读取，所以需要更改时需要重启机器人

### 安装电池

![battery](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/battery.png)

- 电池主体应放在上图蓝框内，连线与红框中的接口相连
- 请注意电池连线与接口两侧不同，一端为弧形，一端为矩形，对应插入，千万不要硬插

### 打开电源

![open](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/open.png)

- 由上图红框内开关开启机器人电源，通电后应有一声蜂鸣器响声，控制板亮起蓝色LED灯，功率板亮起绿灯
- 注意，机器人上电后，不要触碰绿色的功率板，下图推荐两处安全抓握部位

![catch](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/catch.png)

## 关闭机器人

- 开关同上
- 将使用过的电池放于场边充电。充电器接口与电池接口相同，框内红灯表示电池正在充电，绿灯表示已充好，请拔下并放于指定位置

![charge](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/charge.png)

## 连接机器人

### 配置驱动

- 如果是第一次使用，先安装[USB转串口驱动](https://jbox.sjtu.edu.cn/l/W1zzCb)
  - 提取码：src
    
![drive](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/drive.png)

- 根据自己电脑的位数点击运行相应的 exe 文件

![drive1](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/drive1.png)

- 接受协议之后点击“下一页”，即可完成安装，但有些电脑需要重启才正式生效

![drive2](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/drive2.png)

![drive3](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/drive3.png)

### 连接设备

- 连接发射机（USB），此时发射机上的灯左右闪烁，说明在正常搜索连接

![connect](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/connect.png)

- 打开 Cray，Ports 选择连接发射机的串口，Frequency 选择机器人上的
FREQ 拨码数值，点击 Connect，激活发射机开始工作，发射机前灯应全部亮
  
![connect1](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/connect1.png)

- 连接成功时机器人控制板上会有黄色LED灯闪烁，即可开始遥控
- 注：通过Cray更改发射机频率时，如果发射机两个灯常亮，这个时候发射机内部的频率是已经设定好了的，更改频率然后重新连接发射机是不会起到任何效果的。需要重新插拔发射机，再设置一遍

## 控制机器人

- 使用rbk请提前关闭Cray
- 因为要用视觉，给机器人带上顶盖，但需要与号码拨码 NUM 数值对应

![robotID](uploads/yujiazousjtu@sjtu.edu.cn/RunRobots/robotID.png)

- 为了更好地识别机器人的位姿，顶盖前沿需要与机器人的嘴平行，上表面基本与地面平行，必要时可以用螺丝在边沿固定
- 最后运行rbk，机器人执行脚本中规定的动作

