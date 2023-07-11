
GitHelper.bat是在 rbk/batchs 路径下的自动运行脚本，辅助使用git进行版本管理

# 为什么需要GitHelper?

Git作为代码版本管理控制系统，主要追踪的是代码的变化，因此不少非代码文件是我们不需要git进行追踪的，例如*.exe*文件。此时我们将其加入*.gitignore*文件中，git就会直接“看不见”这个文件。

与此同时，还有一类用户配置类的文件。我们想要git看见这个文件，但又不想git追踪它的变化。例如，对*config.lua*这个文件来说，*gNormalPlay*这种运行脚本的设置就和我们提交到git上的重点（新功能、优化、bug修复）没有太大关系。如果把这些的修改也放进git里面，一方面在分支合并时容易创造冲突，另一方面对后人进行代码维护也会造成不便。但我们并不能简单将它放进*.gitignore*文件中：如果在现在直接添加，git会以为你将这个文件删掉了，那么在其他人进行clone的时候这个文件就会缺失。同时如果lua层面开发了新的skill，也需要在config.lua中进行修改。

因此，我找到了一条命令参数：--skip-worktree。这个参数，以我现在的理解解释的话，就是**仅保留在本地，忽略本地对某文件进行改动的标志（flag）**。仅保留在本地，说明这个命令**对远端仓库没有影响**。作为一个标志，它随时可以标记或取消，**并且重复进行标记并不会产生任何影响**。唯一不方便的是，它每次敲起来非常繁琐。延续上文*config.lua*的例子，这条命令会长这样：

```
$ git update-index --skip-worktree ./bin/rbk.cfg
```

这还只是一个文件。在目前架构中，起“配置文件”作用的总共有5项，手动操作的繁琐程度可想而知。因此，我写了这个GitHelper脚本进行傻瓜式操作的管理。

# 用了这个命令到底会发生什么？

## 场景一：我对skill进行了优化，因此修改了config.lua的gNormalPlay项

这样的修改和我工作重点完全无关。因此使用GitHelper忽略后，git将不会将你对config.lua文件的修改进行任何记录。

## 场景二：我研发了新skill，因此修改了config.lua的gskill项

这里的修改就是和我工作重点息息相关的了。因此，我需要先用GitHelper重新追踪该文件。这么做之后git将像普通文件一样对待它，将它的所有修改纳入版本管理。

## 场景三：别人对config.lua进行修改（并上传到远端仓库）

按习惯来说，一般我会在工作前执行一次`git pull`看看有没有新的变化。假设今天我们忘了，于是在完成工作之后我们尝试上传代码：

```
$ git push
To github.com:SY-LG/test_skip.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:SY-LG/test_skip.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

哦，原来是其他人上传了新代码，那就pull一下先

```
$ git pull
remote: Enumerating objects: 7, done.
remote: Counting objects: 100% (7/7), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 4 (delta 0), reused 4 (delta 0), pack-reused 0
Unpacking objects: 100% (4/4), 337 bytes | 42.00 KiB/s, done.
From github.com:SY-LG/test_skip
   5a6a323..fa137fa  main       -> origin/main
error: Your local changes to the following files would be overwritten by merge:
        config.txt
Please commit your changes or stash them before you merge.
Aborting
```

于是这里就有提示了：我之前设置“忽略”的文件*config.txt*被远端仓库修改了，为保证我的工作进度不丢失，git取消了这一次pull命令。那怎么办呢？

如果我们的修改确实不需要保存的话，可以通过git命令或者gui工具将修改删掉。

```
$ git checkout -- config.txt
```

如果确实需要保存的话，就先将之前的忽略标志变为追踪（示例中使用原始命令，对应GitHelper中的追踪选项），并提交修改，最后重新pull

```
$ git update-index --no-skip-worktree config.txt

$ git add config.txt

$ git commit -m "Changes that need to be saved"

$ git pull
Auto-merging config.txt
CONFLICT (content): Merge conflict in config.txt
Auto-merging test.txt
CONFLICT (content): Merge conflict in test.txt
Automatic merge failed; fix conflicts and then commit the result.
```

这是常见情况，pull之后产生融合冲突。这往往由同时对一个地方的修改引起。例如，进行上述操作后config.txt中可能会这么显示：

```
IS_TEST_MODE = true
<<<<<<< HEAD
gTestPlay = "Test_ChaseKick"
=======
gTestPlay = "Test_Goalie"
>>>>>>> dev
```

在这个文件中我在HEAD（当前版本）和dev分支的版本中进行了不同的修改，因此git不知道该如何将二者进行融合，因此产生了冲突。（与之相对的，如果我只在其中一个版本中添加了一行新内容，git就会自动将这个变化添加到融合后的版本中）。git会将冲突的地方标出，通过<和>指出两个版本的区别，并需要我们手动去确定最终内容（也即，删掉<<<===>>>并保留我们想要的那一行）。冲突解决后，我们就可以重新进行add、commit和push了。

# 怎么使用GitHelper？

在rbk文件夹下打开batches文件夹并找到*GitHelper.bat*，双击打开，按照提示操作即可。在我写的版本中，输入1对应忽略所有配置文件的更改，2对应重新追踪所有配置文件的修改，3对应自定义每个配置文件的追踪或修改（每一项手动选择）。输入命令后回车即可。