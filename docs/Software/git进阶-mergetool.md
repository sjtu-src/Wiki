# git进阶-mergetool

在git merge产生冲突的时候，使用传统IDE和编辑器（例如Visual Studio和Sublime Text）去手动定位到冲突位置并解决并不是一件轻松的事情，而通过配置mergetool可以快速解决conflict。Sublime Merge的部件smerge就是mergetool的一种，下面以此举例进行演示。

## 安装与配置

### 下载与安装

访问[官网](https://www.sublimemerge.com/)可以下载安装免费的永久体验版

### 配置全局变量(windows)

将Sublime Merge文件夹添加至Path环境变量

### git配置

在cmd或bash中输入以下命令：

```
git config mergetool.smerge.cmd 'smerge mergetool "$BASE" "$LOCAL" "$REMOTE" -o "$MERGED"'
git config mergetool.smerge.trustExitCode true
git config merge.tool smerge
```

注：

1.   这段命令只对当前git仓库生效。若想全局生效，可在每句后加入`--global`命令。**global选项对第三句不完全起作用，详见下文**

2.   Git文档中对前两句的解释如下：

     When *git mergetool* is invoked with this tool (either through the `-t` or `--tool` option or the `merge.tool` configuration variable) the configured command line will be invoked with `$BASE` set to the name of a temporary file containing the common base for the merge, if available; `$LOCAL` set to the name of a temporary file containing the contents of the file on the current branch; `$REMOTE` set to the name of a temporary file containing the contents of the file to be merged, and `$MERGED` set to the name of the file to which the merge tool should write the result of the merge resolution.

     If the custom merge tool correctly indicates the success of a merge resolution with its exit code, then the configuration variable `mergetool.<tool>.trustExitCode` can be set to `true`. Otherwise, *git mergetool* will prompt the user to indicate the success of the resolution after the custom tool has exited.

### 不保存备份文件

git在使用mergetool时会默认产生原冲突的备份文件（以便恢复），并且此文件在conflict解决后不会消失，将会污染commit history。因此需要进行设置：

```
git config mergetool.keepBackup false
```

同上，视需求可加入`--global`命令。

### 使用mergetool

即使之前在其他仓库配置过，对每个仓库，也都建议使用

```
git config merge.tool smerge
```

配置一遍再使用

```
$ git mergetool
```

-----对git不熟悉的话可直接看到下一环节-----

否则，git会显示：

```
This message is displayed because 'merge.tool' is not configured.
See 'git mergetool --tool-help' or 'git help config' for more details.
'git mergetool' will now attempt to use one of the following tools:
opendiff kdiff3 tkdiff xxdiff meld tortoisemerge gvimdiff diffuse diffmerge ecmerge p4merge araxis bc codecompare smerge emerge vimdiff nvimdiff
```

如果当前确实处于merging状态*（且已经将smerge设置为全局的mergetool？未充分测试，不确定）*，git会提示选择

```
Hit return to start merge resolution tool (smerge):
```

此时直接回车也可以使用smerge，**但是，上文配置的“不保存备份文件”将不起作用，需要merge之后手动删除，因此非常不建议这么做**

注：这里git的行为比较迷惑，笔者未完全理解，请求大佬们解惑

## 使用演示

### 仓库初始化

```
$ mkdir demo_mergetool
$ cd demo_mergetool
$ git init
$ touch file.txt
$ git add file.txt
$ git commit -m "create file.txt"
```

使用bash shell指令（cmd无touch创建文件指令）演示，部分输出略去，下同

### 创造冲突

```
$ git switch -c branch1
```

此时将file.txt内容更改为"branch1"并commit。然后切换回master：

```
$ git switch master
```

将file.txt内容更改为"master"并commit。merge：

```
$ git merge branch1
Auto-merging file.txt
CONFLICT (content): Merge conflict in file.txt
Automatic merge failed; fix conflicts and then commit the result.
```

### 解决冲突

```
$ git mergetool
```

此时将会弹出Sublime Merge的界面

![](uploads/other/mergetool/1.png)

左侧为原本所在分支的内容，右侧为merge的分支的内容；左右、上下同步滚动。此时修复冲突即可。

### 快捷键

运用快捷键可以大幅提升效率。鼠标悬停于对应按钮上方也可以查看说明以及快捷键。

-   Ctrl+Shift+N: 光标定位到前一个冲突点（到尽头之后会停在第一个冲突点）
-   Ctrl+N: 光标定位到后一个冲突点（到尽头之后会停在最后一个冲突点）
-   Ctrl+S: 保存（并退出）Sublime Merge，若有多个冲突文件则修复下一个文件的conflict。
-   Ctrl+Shift+\[: 使用/不使用左侧代码（更改状态）
-   Ctrl+Shift+\]: 使用/不使用右侧代码（更改状态）

例如，在上述例子中，敲击Ctrl+Shift+\[+\]即可得：

![](uploads/other/mergetool/2.png)

此时Ctrl+S保存退出，按照正常步骤进行add, commit即可完成merge操作。
