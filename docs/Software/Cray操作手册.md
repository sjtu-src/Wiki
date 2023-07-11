
介绍一下Cray的功能和操作

## 关于软件

- Cray是我们的遥控软件，可以在没有视觉的情况下，控制机器人完成基础动作（移动、踢球、吸球……）
- 借助其能够与机器人通讯的条件，在其中嵌入了一些远程调试功能（PID调试、射门力度拟合……）
- [Cray源码仓库](https://gitlab.com/src-ssl/cray)

## 基础操作

![Cray](uploads/yujiazousjtu@sjtu.edu.cn/Comm/Cray.png)

1. 发射机连接的串口，打开软件前先连接好发射机，软件启动时会更新串口信息，如果有多个，需要选择实际连接的，如果都不生效甚至没有，请检查发射机的连接情况，或是有没有安装USB转串口驱动，或者更换串口，最后重启软件
2. 发射机通讯频率，0~9，请将此频率与小车所选择的频率选择一致
3. 连接按钮，与发射机建立连接并激活其工作状态，完成连接后12所示的start按钮就会亮起生效
4. 需要控制的机器人号码，0~11，即机器人的拨码开关数值
5. 小车前进方向速度控制，快捷键W/S，每次按下会增加或减少前进方向的速度数值，最大值不超过MaxVel
6. 小车旋转方向速度控制，快捷键方向键左右，每次按下会增加或减少旋转方向的速度数值，最大值不超过MaxVelR
7. 小车左右方向速度控制，快捷键A/D，每次按下，会增加或减少左右方向的速度数值，最大值不超过MaxVel
8. 吸球等级，0~3，数值越大吸球力度越大
9. 切换踢球方式，快捷键方向键向上，flat即平射，chip即挑射
10.	踢球，快捷键E，是否踢球，激活一次自动恢复为false
11.	吸球，快捷键Q，是否吸球
12.	start按钮，按下后，发射机就会开始向小车发包
- 其他按键：
  - Stop：急停按钮，快捷键空格
  - MaxVel：向前后左右速度的最大值，最大为511，即5.11m/s
  - MaxVelR：旋转速度的最大值，最大为511
  - KickPower：调整踢球力度的数值，最大为127
  - 这些最大值的设置与通讯协议有关
- 速度的方向与按键的对应关系如下图所示：
  
![direction](uploads/yujiazousjtu@sjtu.edu.cn/Comm/direction.png)

- 踢球测试前需要合理放置球，最好是放于嘴的正中间，且需要在吸球装置中被检测到，此时会有一红色LED亮起。建议放置好了开启吸球固定，再踢球

![infrared](uploads/yujiazousjtu@sjtu.edu.cn/Comm/infrared.png)

## 远程调试

// TODO 在完善及实车测试后补充

### PID调节

![pid](uploads/yujiazousjtu@sjtu.edu.cn/Software/pid.png)

Cray里面调试pid的模块，选中pid mode，开启start开始发送指令，在运动的时候也可以修改四个轮子的pid参数。同时，机器人需要调成mode 5

### 射门力度拟合

## 最新功能

### 轮速显示

![wheelSpeed](uploads/yujiazousjtu@sjtu.edu.cn/Software/wheelSpeed.png)

- 点击Record开始录制，录制结束再次点击Record，然后点击Display显示刚刚录制的内容
- wheel 1~4 分别对应左前、右前、右后、左后轮
- 常见问题及解决：
  - 记录不了数据，重新插拔发射机
  - 记录到的数据不连续，正常情况，重新记录即可（画出的线本身就是虚线）
  
## 相关资料

+ [远古版Cray讲解](https://pan.baidu.com/s/17l6cx670jdmvCnHI137KEg)  
提取码:t1qb



