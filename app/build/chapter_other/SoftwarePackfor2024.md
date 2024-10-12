# 2024软件包说明
!!! abstract
    本文档主要用于说明2024年上海交通大学SRC赛队校内赛的软件包的安装与使用说明



## falcon界面启动

解压后,bin文件夹下的Client.exe即为启动器,单击后即可启动falcon界面

![屏幕截图 2024-10-12 111329](SoftwarePackfor2024.assets\屏幕截图 2024-10-12 111329.png)

后续会出现终端界面,当出现``go on`` ``true``后会打开falcon主界面

![屏幕截图 2024-10-12 111626](SoftwarePackfor2024.assets\屏幕截图 2024-10-12 111626.png)

大体上与当前赛队成员使用的falcon功能相近,想要详细了解可以参考:

[falcon编译](https://sjtu-src.github.io/Wiki/chapter_universal_build/falcon/){ .md-button .md-button--primary}

这里只讲讲校内赛需要的一些功能:

1. 点击插头键,以及simulator的启动按钮,主界面上将出现22辆小车(11y and 11b)
2. 点击页面上方的formation,再点击load中的4v4,即进入4v4的队形
3. 再点击simulator下的controller中的蓝方,黄方启动按钮,双方即可开始行动,再次点击即为关闭

## 裁判盒说明

机器人启动后,即可用裁判盒开始控制比赛

点击侧边栏的referee box,进入裁判盒界面

![屏幕截图 2024-10-12 113243](SoftwarePackfor2024.assets\屏幕截图 2024-10-12 113243.png)

下面讲讲校内赛中裁判盒的使用:

- 点击send后,机器人开始接受裁判盒信息;点击stop后,机器人停止接受裁判盒信息
- 点击stop后,机器人进入stop阶段,此时类似于开球或者定位球时的准备阶段,机器人进行跑位,不进行其他动作
- 接下来如果进行定位球(初赛),即点击directkick,机器人即开始定位球攻防(黄方进攻则点击黄方的directkick,蓝方进攻则点击蓝方的directkick)

## 脚本说明

推荐参赛队伍使用sublime作为text editor,使用vscode需要自行安装插件

脚本位于``bin\lua_scripts\ssl\play\Ref\Gamecode``文件夹下

![屏幕截图 2024-10-12 114630](SoftwarePackfor2024.assets\屏幕截图 2024-10-12 114630.png)

初赛目前需要使用到的是``Ref_Def.lua, Ref_Kick.lua, Ref_Stop.lua``,分别对应的是定位球防守, 定位球进攻,Stop阶段所进行的脚本,另外的``Ref_Nor_4.lua``是复赛时常规4v4的脚本.



## 特别说明

![屏幕截图 2024-10-12 115215](SoftwarePackfor2024.assets\屏幕截图 2024-10-12 115215.png)

脚本对战的时候,双方ssl文件夹分别命名为自身队伍名字,并在falcon右下角的``Settings\Name\AlertNames``中进行更改!

![屏幕截图 2024-10-12 115411](SoftwarePackfor2024.assets\屏幕截图 2024-10-12 115411.png)

controller中新增的按钮FULL/HALF/ZERO分别代表门将全速,半速,零速,更改时需重新启动蓝黄双方!

!!! warning
    一旦不重新启动,门将的设置将不会生效!