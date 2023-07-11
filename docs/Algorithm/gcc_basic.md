```Makefile
Demo: Display.cpp
    g++ -g -o Display Display.cpp -I../../../include -Wl, -rpath=$(MVCAM_COMMON_RUNENV)/64 -L$(MVCAM_COMMON_RUNENV)/64 -lX11, -lMvCameraControl 
Clean: 
    rm Display -rf
```
海康相机sdk里面的demo。`-I`指定`include`路径，`-L`链接的路径,`-lX11`为build时候需要链接的库`libX11.lib`，`-rpath`运行程序时候需要找的链接库的路径