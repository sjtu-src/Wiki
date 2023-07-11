
本篇文章介绍如何在Win 10系统上配置JAVA环境，以支持Tigers-AutoRef在仿真模式下使用

## 配置流程

+ 下载64位windows系统下的jdk安装包 jdk-11.0.11_windows-x64_bin.zip
+ 具体版本查看AutoRef的README，这里以11.0.11版本为例

- 进入计算机，选择属性、高级系统设置、高级、环境变量
- 编辑系统变量，新建 JAVA_HOME 变量，变量名填写jdk的解压文件位置
- 注：文件地址需填至bin文件夹的上一级     
    
![system](uploads/yujiazousjtu@sjtu.edu.cn/AutoRef/system.png)

- 编辑用户变量，编辑Path变量，新建 %JAVA_HOME%\bin;
- 注：最后的分号“;”必要
- 新建CLASSPATH变量，变量值如下填写，注意变量值中的“."和”;“

![user](uploads/yujiazousjtu@sjtu.edu.cn/AutoRef/user.png)

- 确认保存后退出，打开命令行，输出 java -version，如显示版本信息，则配置成功

## 软件对接

仿真模式下，owl2作为视觉信息、裁判指令的中转站，对接rbk、grSim、Tigers-AutoRef和GC

### 模式选择

- 开启owl2内裁判盒，点击使Manual切换为Auto
- 共有两种自动模式，以下方指令按键是否显示区分
    - 若显示，则只与AutoRef对接，裁判指令由内置裁判盒发送
    - 否则，裁判指令由GC发送，AutoRef配合形成完整的自动裁判系统

![refbox](uploads/yujiazousjtu@sjtu.edu.cn/AutoRef/refbox.png)

### 参数配置

- 与rbk、grSim的对接与一般情况相同
- 与AutoRef对接，需要转发裸视觉和裁判指令，具体端口在./config/cfg.ini中设置
    - 其中refereePortToAutoRef指向特一端口发送裁判指令，VisionAutoRef是向特一端口发送裸视觉，注意和AutoRef接收端一致
- 与GC对接，只需接收裁判指令，并完成以上对rbk、AutoRef的转发
    - refereePortFromGC指绑定接收裁判指令的端口，GC_Port是向特一端口发送队伍注册信息，仿真中用不上
- 该文件中还有关于ip地址的配置，一般不需要更改
- 改动后记得重启owl2或使用快捷键“r”，使新参数生效

![cfg.ini](uploads/yujiazousjtu@sjtu.edu.cn/AutoRef/cfg.ini.png)
