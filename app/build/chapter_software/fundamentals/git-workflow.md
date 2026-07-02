# Git 基本工作流

## 我们希望你形成的习惯

日常开发里最重要的不是“会很多 Git 命令”，而是形成稳定习惯：

- 改东西前先看 `git status`
- 拉最新代码前先把本地未提交改动整理好
- 新功能和较大修复尽量开分支
- 提交信息要能让后来者一眼看懂

如果你喜欢 GUI，可以用 `Fork` 之类的工具；但背后的命令行逻辑仍然要懂。

## 每天最常用的一套命令

```powershell
git status
git fetch
git pull --rebase --autostash
```

`git pull --rebase --autostash` 在我们这里很重要，因为它能：

- 先自动暂存你的未提交改动
- 把本地提交线性地接到远端最新提交之后
- 再把你的改动恢复回来

这通常比直接无脑 merge 更干净。

## 新功能的推荐流程

```powershell
git switch -c feat/your-topic
git add .
git commit -m "feat: add power curve editor docs"
git push -u origin feat/your-topic
```

如果只是小修复，也可以直接在常用开发分支上完成，但前提是团队协作方式允许。

## `merge`、`rebase`、`cherry-pick` 怎么理解

### `merge`

- 适合把两条分支合并到一起。
- 优点是历史真实完整。
- 缺点是多人频繁 merge 时图会比较乱。

### `rebase`

- 适合把“我的提交”重新接到“别人最新提交”后面。
- 优点是历史更线性，阅读舒服。
- 风险是会改写提交历史，所以不要随意 rebase 已经被多人依赖的公共分支历史。

### `cherry-pick`

- 适合“我只想拿对方的一两个提交，不想整个合并过去”。
- 常见于热修复、临时回迁、跨分支摘取小功能。

## 提交信息建议

推荐简洁、可搜索、可分组的格式：

```text
feat: migrate software wiki to Python-C++ architecture
fix: correct role match explanation
docs: update launch.json debugging guide
refactor: archive old lua wiki pages
```

好处是：

- `git log --oneline` 一眼就能扫过去
- 后续查历史非常省时间

## 冲突时先做什么

先不要慌着“全部接受 theirs / ours”，先做三件事：

1. 看冲突文件到底是不是你真的理解的模块。
2. 看两边改的是“同一逻辑”还是“只是相邻行”。
3. 解决后重新运行最小验证，不要只凭直觉结束。

Git 冲突本身并不可怕，可怕的是在不理解语义的前提下机械点按钮。

## 一个特别常见的坑

不要把下面这些东西随手提交进去：

- 本地临时日志
- IDE 个人缓存
- 自动生成但不该入库的中间文件
- 自己电脑特有的绝对路径配置

在提交前，`git status` 是你最后一道防线。
