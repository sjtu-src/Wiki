# Decoda

- Decoda还蛮有用的，能找到一些一不小心犯的很蠢的错误，比如这次比赛前找到了个变量在作用域外没有定义过的错误...
- [下载地址](https://jbox.sjtu.edu.cn/l/n1JPeI)
- 安装极为简单，运行可执行文件，同意协议后一路`Next`，最后选择合适的安装路径，点击`Install`下载
  
![Install_Decoda](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/Install_Decoda.png)

- 运行安装路径下的`Decoda.exe`，点击`Debug`、`Start Debugging`

![Decoda](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/Decoda.png)

- 在下图弹窗内设置，需要设置：
  - Debugging/Command : 在右侧的`...`处选择`rbk.exe`的路径
  - Debugging/Working : 完成上一步后，自动设置好`rbk.exe`的工作目录
  - Debugging/Command : 设置可执行文件的运行参数，暂时还没有用到
    
![Settings](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/Settings.png)

# VSCode + EmmyLua

电脑上需要安装好Java，参考[Windows Java 安装](https://java.com/en/download/help/windows_manual_download.xml#download]) ，安装好后重启电脑。

这个可以调试单独的Lua项目，也可以和attach到`rbk.exe`上调试，具体可查看[视频](https://www.bilibili.com/video/av48929259?from=search&seid=15939880355023659900)
