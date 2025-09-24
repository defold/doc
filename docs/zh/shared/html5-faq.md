#### Q: 为什么我的 HTML5 应用程序在 Chrome 中启动画面处冻结？

A: 在某些情况下，无法从本地文件系统在浏览器中本地运行游戏。从编辑器运行时，游戏会从本地 Web 服务器提供。例如，您可以在 Python 中使用 `SimpleHTTPServer`：

```sh
$ python -m SimpleHTTPServer [port]
```


#### Q: 为什么我的游戏在加载时因出现"意外的数据大小"错误而崩溃？

A: 当您使用 Windows 进行构建并将其提交到 Git 时，通常会发生这种情况。如果您的 Git 中行尾配置不正确，它将会更改您的行尾，从而也会更改数据大小。请按照以下说明解决问题：[https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings](https://docs.github.com/en/free-pro-team@latest/github/using-git/configuring-git-to-handle-line-endings)
