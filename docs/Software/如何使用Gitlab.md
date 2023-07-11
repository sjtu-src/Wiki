
Gitlab是我们重要的仓库，存放各版本的代码和文档等资源，各成员需熟悉其操作，以更好地进行团队编辑

## Gitlab

### repo

- 以owl2为例，介绍下主要的功能

![repo](uploads/yujiazousjtu@sjtu.edu.cn/Software/repo.png)

1. 切换分支（branches）、标签（tag），标签是确定版本的代码
2. 新增文件、分支、标签
    - 以分支为例，主要需要设置两点：分支名称和继承的原分支，继承的原分支内容会作为新分支的初始内容
    - 然后点击`Create branch`完成创建
    
![create_branch](uploads/yujiazousjtu@sjtu.edu.cn/Software/create_branch.png)   

3. 查看该分支的修改历史，如果该分支是继承了另一分支，那么也有原分支的历史记录，每一行详细列出提交修改的时间、作者，右侧有版本号和该版本的具体代码

![history](uploads/yujiazousjtu@sjtu.edu.cn/Software/history.png)

4. 下载源码，压缩包形式，不能修改后上传
5. 克隆源码，文件目录形似，修改后可直接上传
6. 最近一次提交的修改（commit），点击进入可以看详细信息，有所有经过修改的文件，绿色为新增内容，红色是删除部分
   
![commit](uploads/yujiazousjtu@sjtu.edu.cn/Software/commit.png)

7. 展示代码的详细信息，包括代码的内容、最近一次提交的修改及其时间

### wiki

- wiki用于展示队内的资源和文档，集中放置于SRC仓库内，也就是你现在看的地方
- 大致与上述相同，不过多论述了

![wiki](uploads/yujiazousjtu@sjtu.edu.cn/Software/wiki.png)

1. 查看该页面的修改历史
2. 新建页面，唯一不同的是命名，命名格式为 类别/文件名，若有多个类别以此类推
3. 克隆wiki的仓库，文件目录的形式，修改后可直接上传，比较方便整理结构
   - git clone git@gitlab.com:src-ssl/src.wiki.git
   - cd src.wiki
4. 在Gitlab上编辑该页面，一般是markdown语言
5. 显示所有的文档，按照首字母顺序排列，Home中有更为方便浏览的wiki目录
6. 当文档数量过多，无法完全显示出来时，通过这个浏览所有文档

