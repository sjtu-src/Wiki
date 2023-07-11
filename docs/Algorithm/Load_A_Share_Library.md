# Load a Share Library
这个真是血泪的教训。。。。  
只有折腾过很多很多次，被搞的头大才会想着：啊！！！我一定要好好学一下如何加载库
## 0.0 背景 加载一个动态库的场景
1. 在build的时候，需要去找动态库在哪里  
2. 在run的时候，程序需要去找动态库在哪里  

千万注意上面上的二个真滴是不同情况。

## 1.0 专有名词
区别下面几个名词，有些名词是有问题的
> hello.dll hello.lib libhello.lib libhello.so libhello.so.1.1 libhello.a hello.a hello.so 

## 2.0 运行库加载搜索
[Run Path](https://gitlab.kitware.com/cmake/community/wikis/doc/cmake/RPATH-handling)

## 3.0 解决方法
1. 最粗暴的方法，设置`LD_LIBRARY_PATH`， 但是每次都要搞一次麻烦啊  
2. 把一些库放在`/usr/lib`之类肯定会去搜索的下面，但是有游戏额东西不想共享出来啊
3. 用`rpath`来指定run的情况，编译的时候直接link过去
## 4.0 Demo and exepriments
强推！[Building C++ shared libraries in Qt Creator (cross-platform)](https://blog.g3rt.nl/building-cpp-shared-libraries-qt-creator.html)  
强推！[Building and using shared libraries in Linux](https://blog.g3rt.nl/building-using-shared-libraries-linux.html)   
[Linux 动态加载机理 官方](http://man7.org/linux/man-pages/man8/ld.so.8.html)  
[Program Library HOWTO](http://tldp.org/HOWTO/Program-Library-HOWTO/shared-libraries.html)