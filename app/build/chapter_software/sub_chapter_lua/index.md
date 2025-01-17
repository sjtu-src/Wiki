# Introduction
首先，我们简单介绍一下lua部分的大致框架
![index](lua_in_SRC.assets\index.png)

[2.2.1小节](https://sjtu-src.github.io/Wiki/chapter_software/sub_chapter_lua/lua%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95/)会简单介绍lua的基本语法，属于开始学习前的预备知识

[2.2.2小节](https://sjtu-src.github.io/Wiki/chapter_software/sub_chapter_lua/config/)从config————lua部分的“控制台”————开始介绍，这一部分属于特殊的lua文件，控制代码运行时的脚本选择

[2.2.3小节](https://sjtu-src.github.io/Wiki/chapter_software/sub_chapter_lua/%E8%84%9A%E6%9C%AC%E9%80%89%E6%8B%A9/)介绍开始运行代码后执行的第一个步骤————脚本选择，即由config控制的内容

[2.2.4小节](https://sjtu-src.github.io/Wiki/chapter_software/sub_chapter_lua/%E8%84%9A%E6%9C%AC%E8%BF%90%E8%A1%8C/)承接上一节，介绍脚本运行环节，包括一些初始化和任务分配工作

[2.2.5小节](https://sjtu-src.github.io/Wiki/chapter_software/sub_chapter_lua/lua_in_SRC/)承接上一节，介绍了具体会执行的任务脚本的编写，这一部分为lua部分的主要内容

[2.2.6小节](https://sjtu-src.github.io/Wiki/chapter_software/sub_chapter_lua/lua%E4%B8%AD%E7%9A%84skill/)介绍了lua中的skill脚本，它们承接cpp代码，并在task中被调用

2.2.7小节介绍了lua部分常用的各种工具函数，它们常在2.2.5小节中所介绍的脚本中被调用，其中task.lua会调用2.2.6小节中所述的skill脚本

[2.2.8小节](https://sjtu-src.github.io/Wiki/chapter_software/sub_chapter_lua/Rolematch%E6%A8%A1%E5%9D%97/)介绍了任务匹配的相关代码，这一部分在2.2.4小节所述的脚本运行中被调用和执行

[2.2.9小节](https://sjtu-src.github.io/Wiki/chapter_software/sub_chapter_lua/%E5%85%B6%E5%AE%83/)与其它小节联系较少，主要介绍了lua中debug函数的用法，用于辅助脚本编写
