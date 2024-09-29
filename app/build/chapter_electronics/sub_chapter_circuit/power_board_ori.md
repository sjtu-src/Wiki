# 功率板

## 一、概述

- 功率板的主要作用：通过升压模块将 $16V$ 电压升高至 $220V$，进而给电磁铁供电，并接受控制板的踢球信号控制电磁铁踢球。
  
- 两个 $2200 \mu F$ 的大电容可以实现对能量的储存，储存的的能量在踢球时通过极短的时间释放，从而驱动电磁铁踢球。
  
## 二、功率板原理图及PCB设计文件

目前有老功率板与新功率板两版设计，两版原理相同，新功率板在老功率板基础上进行了一定优化和删减。两版原理图及PCB设计文件如下：

- 老功率板原理图：[交大云盘](https://jbox.sjtu.edu.cn/l/y1gkPk)
- 新功率板原理图：[交大云盘](https://jbox.sjtu.edu.cn/l/r1TiNZ)
- 老功率板PCB设计（Altium Designer）：[交大云盘](https://jbox.sjtu.edu.cn/l/D1rCPL)
- 新功率板PCB设计（嘉立创）：[交大云盘](https://jbox.sjtu.edu.cn/l/51VMpd)

## 三、功率板原理图解析

### 1、充电使能电路

<div align="center">
    <img src="https://github.com/Gnitnaux/POWBRD/blob/master/%E5%85%85%E7%94%B5%E4%BD%BF%E8%83%BD%E7%94%B5%E8%B7%AF.png?raw=true" alt="充电使能电路" width="500">
</div>

- 充电使能电路主要有两大作用：
  * 保护功率板  
  * 方便功率板的维修

- 其中核心芯片为CD4072BM96，由该芯片引脚符号即可得知其主要功能。该芯片主要进行逻辑运算：左侧“J=A+B+C+D"表示J输出为A、B、C、D四个输入的逻辑之和，右侧K同理。此外SHOOT、CHIP分别为控制板提供的平射和挑射信号的反向信号，在正常情况下为低电平，因此正常情况下K引脚，即BOOST_EN引脚为低电平，该信号传递至升压电路允许升压，同时LED灯亮表示升压正常。而当功率表某些部分出现异常或是踢球时，该芯片进行逻辑运算输出BOOST_EN为高电平，传递至升压电路阻值升压，从而起到保护电路的作用。

- 在维修功率板时，该芯片可作为检测的第一步，即用万用表测量各引脚电压，通过异常向其他部分排查，而且LED1的状态也可指示升压的正常与否，方便了功率板的维修。

- 要注意**该芯片的质量会直接影响功率板的工作状态**，在开发阶段进行测试时由于采购到了质量较差的该元件出现了种种问题，在元器件采购时需格外注意该芯片的质量。



### 2、水泥电阻放电电路

<div align="center">
    <img src="https://github.com/Gnitnaux/POWBRD/blob/master/%E6%B0%B4%E6%B3%A5%E7%94%B5%E9%98%BB%E6%94%BE%E7%94%B5%E7%94%B5%E8%B7%AF.png?raw=true" alt="水泥电阻放电电路" width="500">
</div>

- 该电路起作用的场合为关闭电源时。EL357N(A)(TA)-G为光耦二极管，通过电路符号可以看出左侧1、2引脚控制内部发光二极管，若二极管发光，则3、4导通，否则关断。在正常工作时，3、4导通，此时Q3关断，电流通过 $510k\Omega$ 电阻缓慢流向地。在关闭开关时，3、4关断，此时Q3导通，电容中的能量流经R16、R44两个水泥电阻后释放，此时可以感受到水泥电阻温度有明显的升高。

- 在老功率板的使用中，**Q3是经常损坏的元件**，除元件质量问题外，在关闭电源瞬间的浪涌电流也可能对其造成一定的影响。因此在新功率板设计中加入了磁珠U6来抑制浪涌电流。

- U5只能耐受 $110\degree C$ 的温度，因此在更换该元件时**不能使用热风枪进行吹焊**。


### 3、踢球电路

<div align="center">
    <img src="https://github.com/Gnitnaux/POWBRD/blob/master/%E8%B8%A2%E7%90%83%E7%94%B5%E8%B7%AF.png?raw=true" alt="踢球电路" width="500">
</div>

- 踢球电路的原理较为简单，SN74LVC2G04DCKR为集成的两个非门，主要作用是将1、3引脚的信号取反。之后通过MC34152DG（大功率MOS管芯片）后转为两个MOS管（SGL160N60UFDTU）的驱动信号。正常情况下，MOS管关断，VCOIL与COIL_CHIP/COIL_SHOOT之间连接的电磁铁在整流二极管SBR40U300CTB作用下仅有几伏压降，电磁铁不工作。

- 踢球时（以挑射为例），控制板传来信号使CHIP_IN为低电平，反向后CHIP为高电平，此时MOS管导通，COIL_CHIP接地，电磁铁两端此时形成 $200V$ 电压，大电容储存的电能短时间内释放给电磁铁，从而驱动电磁铁工作。

### 4、升压电路

<div align="center">
    <img src="https://github.com/Gnitnaux/POWBRD/blob/master/%E5%8D%87%E5%8E%8B%E7%94%B5%E8%B7%AF.png?raw=true" alt="升压电路" width="500">
</div>

- 升压电路是功率板的核心，主要基于BOOST电路的原理（[基本原理可参考该链接](https://zhuanlan.zhihu.com/p/633235266)），其核心芯片为UC3843（[芯片手册](https://atta.szlcsc.com/upload/public/pdf/source/20160416/1460799393893.pdf)）

- 引脚说明：
  * 引脚1（COMP）： 误差放大器补偿引脚。该引脚通常通过一个电阻和电容连接到地，用于设置误差放大器的频率响应。
  * 引脚2（VFB）： 反馈电压输入引脚。该引脚接收来自输出电压分压器的反馈信号，用于调节输出电压。
  * 引脚3（ISENSE）： 电流检测输入引脚。该引脚用于检测开关管的电流，实现过流保护和电流模式控制。
  * 引脚4（RT/CT）： 振荡器定时电阻和电容引脚。通过连接一个电阻和一个电容到地，可以设置振荡器的频率，从而决定开关电源的工作频率。
  * 引脚5（GND）： 地引脚。所有电压都是相对于这个引脚来测量的。
  * 引脚6（OUT）： 输出驱动引脚。该引脚提供一个驱动信号，用于控制开关管的导通和关断。
  * 引脚7（VCC）： 电源电压引脚。该引脚接收工作电压，通常为10-30V。
  * 引脚8（VREF）： 基准电压输出引脚。该引脚提供一个稳定的5V基准电压，可用于内部电路或外部电路。
  
- BOOST_EN为来自充电使能电路的控制信号，不允许升压时为高，Q7导通，此时COMP为低电平，导致升压电路停止工作。允许升压时，Q7关断，芯片内部进行着较为复杂的工作，但总体上的工作原理很清晰：R38、R39为两个反馈电阻，其分压得到的信号反馈给VFB引脚。在芯片内部，VFB与 $2.5V$ 进行比较，若VFB小于 $2.5V$, 则OUT输出占空比增大，不断升压，直到VFB等于 $2.5V$，此时升压完毕，VCAP已达到200V。

- 值得注意的是，**Q6也是极易损坏的元件**，在维修功率板时也需十分注意。

- 经测量，功率板在正常升压时OUT引脚的输出频率 $28.09\ kHz$，占空比 $9.2$%
  
## 四、功率板对踢球力度的控制

实现对踢球力度的控制在比赛过程中极为重要，通过控制板给与功率板不同的力度信号，并用示波器测量该信号，测试结果如下：

<div align="center">
    <img src="https://github.com/Gnitnaux/POWBRD/blob/master/%E6%8E%A7%E5%88%B6%E6%9D%BF%E8%B8%A2%E7%90%83%E4%BF%A1%E5%8F%B7%E6%B5%8B%E8%AF%95/control_board_force_40.jpg?raw=true" alt="力度40" width="200">
    <img src="https://github.com/Gnitnaux/POWBRD/blob/master/%E6%8E%A7%E5%88%B6%E6%9D%BF%E8%B8%A2%E7%90%83%E4%BF%A1%E5%8F%B7%E6%B5%8B%E8%AF%95/control_board_force_80.jpg?raw=true" alt="力度80" width="200">
    <img src="https://github.com/Gnitnaux/POWBRD/blob/master/%E6%8E%A7%E5%88%B6%E6%9D%BF%E8%B8%A2%E7%90%83%E4%BF%A1%E5%8F%B7%E6%B5%8B%E8%AF%95/control_board_force_100.jpg?raw=true" alt="力度100" width="200">
</div>

进一步定量测试，有如下结果：

| 踢球力度 | 127    | 100  | 80  | 60  | 40  |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **脉冲宽度** | $12.6ms$ | $10ms$ | $8ms$ | $6ms$ | $4ms$ |

可见踢球力度是通过踢球信号的脉冲时间来控制的，且踢球力度与信号脉冲时间成正比。

## 五、电磁铁放电的电路模型

为进一步了解电磁铁放电时的工作状态，特建立以下电路模型来描述电磁铁放电时的响应。其中，电磁铁等效为电感模型。

<div align="center">
    <img src="https://github.com/Gnitnaux/POWBRD/blob/master/%E6%94%BE%E7%94%B5%E7%94%B5%E8%B7%AF%E6%A8%A1%E5%9E%8B.jpg?raw=true" alt="电路模型" width="500">
</div>

可用如下微分方程描述该电路模型：

$$
\begin{cases}
	&i_1 = -4.40044 \times 10^{-3}\ \frac{du_1}{dt}\\
	&i_2 = i_3 + i_4\\
    &u_2 = 5.1 \times 10^3\ i_3\\
    &i_4 = 10^{-8}\ \frac{du_2}{dt}\\
    &u_1 = u_2+430\times 10^3\ i_4\\
    &u_1 = 510\times10^3\ i_6\\
    &i_1 = i_2 + i_5 + i_6\\
    &u_1 = R\cdot i_5 + L\cdot \frac{di_5}{dt} + 2.6
\end{cases}
$$

以上微分方程组经过数学化简可转化为差分方程形式，进而可以使用MATLAB进行运算，拟合出放电电流随放电时间的关系。为弄清不同匝数电磁铁对应的放电曲线，还需进一步分析：

通过阻抗法进行测量，老电磁铁（500匝）电感值为 $0.0175H$，利用电流传感器测量老电磁铁在老功率板下的放电电流，得其为 $11.7A$。由此设置电路模型中 &L& 参数为 $0.0175H$ 并不断调整电路模型中的R参数，使得电流峰值为 $11.7A$，得到 $R=17.5\Omega$

用 $N$ 来表示电磁铁匝数，根据电阻及电磁铁的物理学模型，有

$$
R_L\propto N
$$

$$
L\propto N^2
$$

于是又如下MATLAB代码进行模型计算及数据可视化：

```matlab
N = [500, 450, 400, 350, 300, 250, 200, 150, 100];  
colors = lines(length(N)); 
  
figure; 
hold on;
  
for j = 1:length(N)
    u1 = 214; u2 = 2.58;  
    i2 = 0.00049; i3 = 0.00049; i4 = 0; i5 = 0; i6 = 0.00042;  
    i1 = i2 + i5 + i6;  
    t = 0:0.0000005:0.0127; 
    I = zeros(size(t)); % 初始化I数组  
    L = 0.0175 * N(j) * N(j) / 250000;  % 以500匝电磁铁的电感为基准，算出不同匝数下的电感
    R = 0.5 + N(j) * 17 / 500*64/25; %假设电阻丝及走线电阻为0.5欧，电磁铁电阻以500匝电阻17欧算
    for i = 1:length(t)  
        dt = 0.0000005;
  
        du1 = i1 * dt / (-4.40044 / 1000);
        di5 = (u1 - R * i5 - 2.6) * dt / L;
        du2 = i4 * 100000000 * dt;
        di3 = du2 / 5100;
        di2 = (du1 - du2) / 430000;
        di4 = di2 - di3;
        di6 = du1/510000;
        di1 = di5 + di2 + di6;
        i1 = i1 + di1;
        i2 = i2 + di2;
        i3 = i3 + di3;
        i4 = i4 + di4;
        i5 = i5 + di5;
        i6 = i6 + di6;
        u1 = u1 + du1;
        u2 = u2 + du2;
  
        I(i) = i5;  
    end  
  
    plot(t, I, 'LineWidth', 1.7, 'Color', colors(j,:));  
end  
  
plot(t, 15*ones(size(t)), '--k', 'LineWidth', 1.5);
  
xlabel('$t(s)$','Interpreter','latex');  
ylabel('$I(A)$','Interpreter','latex');  
title('Change of current with time at different turns', 'Interpreter','latex');  
legend(arrayfun(@(x) sprintf('N = %d', N(x)), 1:length(N), 'UniformOutput', false), 'Location', 'best'); % 添加图例，包括参考线  
hold off;  
```

运行结果如下：
<div align="center">
    <img src="https://github.com/Gnitnaux/POWBRD/blob/master/%E7%94%B5%E8%B7%AF%E6%A8%A1%E5%9E%8B%E5%8F%AF%E8%A7%86%E5%8C%96.png?raw=true" alt="电路可视化" width="500">
</div>

图中可见在不损坏保险丝的前提下，匝数在400匝以上均是安全的。考虑到部分物理量测量误差的影响，因此新一代电磁铁计划采用350匝。