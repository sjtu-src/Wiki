
# 若电脑不支持cuda

电脑不支持cuda的话只能使用CPU版本，按照正常的方法配置VS，然后打开SSLStrategy\src\ssl\gpuBestAlgThread.cpp，将has_GPU的值修改为false，具体如下图所示：
需要修改的变量
```
#define has_GPU false
```
最终如下图所示：
![9](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/9.jpg)

然后直接编译即可

在此种情况下task.goLWPassPos等函数可以调用，但只能跑定点

# 若电脑支持cuda

## C++代码设置

按照正常的方法配置VS，然后打开SSLStrategy\src\ssl\gpuBestAlgThread.cpp，将has_GPU的值修改为false，具体如下图所示：
需要修改的变量
```
#define has_GPU true
```
最终如下图所示：
![10](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/10.jpg)

然后按照下方教程安装cuda并配置VS后即可编译

在配置了cuda后仍可将has_GPU修改为false从而调用CPU版本

## 下载CUDA

- ~~最保险，可使用v11.0版本的cuda~~若使用VS2022，建议安装CUDA12
- 安装教程网上多的是，不再赘述了
- [CUDA下载官网](https://developer.download.nvidia.com/compute/cuda/12.0.1/local_installers/cuda_12.0.1_528.33_windows.exe)
- [交大云盘备份](https://jbox.sjtu.edu.cn/l/k1G4BM)

## VS配置

- 之前必要的步骤还是有的~~记得换成vs15工具集~~(falcon可在较新的工具集上编译，包括但不限于142，143)但是注意cmake版本不能太高，建议使用3.22
  - [rbk的编译与调试(1)](https://jbox.sjtu.edu.cn/l/d1qgbA)
  - [rbk的编译与调试(2)](https://jbox.sjtu.edu.cn/l/f1SKBa)

若增加了新的cu文件：
- 写好的.cu文件直接和调用它的.cpp文件放到同一目录下即可

VS配置过程：
- 注意，接下来的操作中的项目仅指含有CUDA文件的项目(SSLStrategy)，不需要所有项目都配置  
1. 右键项目属性->VC++目录->包含目录，将安装好CUDA中include加入包含目录中，将下方这两个路径加入
    - C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.0\include
    - ~~C:\ProgramData\NVIDIA Corporation\CUDA Samples\v11.0\common\inc~~实测12.0没有也不需要samples
    - 具体视自己电脑上的安装路径调整

![1](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/1.png) 

步骤2与步骤3两个设置是Visual Studio的设置，不更换VS的情况下设置一次后就不用再重新设置
2. 点击上方菜单栏工具->选项->文本编辑器->文件扩展名，在扩展名栏中输入.cu，并选择编辑器为：Microsoft Visual C++

![2](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/2.png)    

3. 工具–>选项–>项目和解决方案–>VC++项目设置，添加要包括的扩展名".cu"

![3](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/3.png)

4. 右键打开的项目–>生成依赖项–>生成自定义–>勾选CUDA v12.0
- 如果这里找不到CUDA12.0，得重新安装CUDA，注意一定要安装Visual Studio Integration

![4](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/4.png)

5.之后设置cuda的编译器，否则无法执行cuda，cuda文件右击->属性->配置属性->常规->项类型->CUDA C/C++

![5](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/5.png)

6.配置cuda的lib，项目右击->属性->链接器->输入->附加依赖项中填入:cudart_static.lib与cublas.lib

![7](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/7.png)
![8](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/8.png)

- 之后编译可能会发生错误，如：
  - The CUDA Toolkit v10.0 directory ‘’ does not exist. Please verify the CUDA Toolkit is installed properly or define the CudaToolkitDir property to resolve this error. nbody C:\Program Files (x86)\MSBuild\Microsoft.Cpp\v4.0\V140\BuildCustomizations\CUDA 10.0.targets 536
- 右键项目属性->配置属性->CUDA C/C++->Common，在CUDA Toolkit Custom Dir处填入如下路径即可
  - C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.0
- 如果是.cu文件中显示错误，不用管，正常编译即可

![6](uploads/yujiazousjtu@sjtu.edu.cn/Algorithm/6.png)

## 参考博客

- [CUDA下载安装](https://zhuanlan.zhihu.com/p/416712347)
- [检验CUDA是否安装成功](https://blog.csdn.net/qq_36455412/article/details/124081733)  
- [CUDA工程环境搭建](https://blog.csdn.net/weixin_41336841/article/details/118313452)
- [C++项目中添加CUDA](https://blog.csdn.net/windxgz/article/details/108795892)
- [编译报错解决](https://blog.csdn.net/weixin_43091087/article/details/86064429?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-86064429-blog-121697156.t5_landing_title_tags_v3&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-86064429-blog-121697156.t5_landing_title_tags_v3&utm_relevant_index=1)
