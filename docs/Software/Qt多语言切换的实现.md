
## 问题及解决

- 之前的 **Cray** 等软件发现克隆到本地或修改代码后的第一次编译会莫名飘红失败，第二次就顺利通过，主要原因是 **.pro** 文件中有如下指令：
  - win32 {
    - RC_ICONS = logo.ico
    - system(lrelease t1_zh.ts)
    - copyToDestdir($$PWD/t1_zh.qm)
  - }
- 其中 **system(lrelease t1_zh.ts)** 是使用 **lrelease** 工具发布翻译文件的二进制文件，这样在程序运行时载入会大大的加快速度。
- **copyToDestdir($$PWD/t1_zh.qm)** 是将生成的 **.qm** 文件复制到 **.exe** 文件同目录下。
- 之前的需要两次编译的问题是因为代码修改后第一次编译需要按 **.pro** 执行，因 **copyToDestdir($$PWD/t1_zh.qm)** 缺少 **.qm** 而失败，第二次编译认为代码无更改，不再执行 **.pro**，成功。
- 将 **.ts** 文件转化为 **.qm** 文件，可以使用 **Qt** 工具 **Linguist** 完成。
- 之前从 **gitlab** 里 **clone** 下来的源码里就有 **.ts** 文件，**clone** 下来的缺少 **.qm** 文件，现在把 **.qm** 添加到源码中，就可以一次编译成功了。只要翻译不变，就不需要重新生成 **.qm** 文件。
- 另外，文件改名为 **zh_CN**，意思是符合中国中文规范。
- 这两个文件的功能是语言转化（翻译），之后我们的软件开源工作可能能用上。
- Reference
- [1](https://blog.csdn.net/chase_hung/article/details/90106533)
- [2](https://www.likecs.com/show-125381.html)
- [3](https://juejin.cn/post/6844903876257120263)
- [4](https://blog.csdn.net/iriczhao/article/details/121453722)