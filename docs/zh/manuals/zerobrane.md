---
title: 使用 ZeroBrane Studio 进行调试
brief: 本手册介绍了如何使用 ZeroBrane Studio 在 Defold 中调试 Lua 代码。
---

# 使用 ZeroBrane Studio 调试 Lua 脚本

Defold 包含一个内置调试器，但也可以将免费开源的 Lua IDE _ZeroBrane Studio_ 作为外部调试器运行。要使用调试功能，需要安装 ZeroBrane Studio。该程序是跨平台的，可以在 macOS 和 Windows 上运行。

从 http://studio.zerobrane.com 下载 "ZeroBrane Studio"。

## ZeroBrane 配置

为了让 ZeroBrane 找到您项目中的文件，您需要将其指向 Defold 项目目录的位置。找出此位置的一个便捷方法是使用 Defold 项目根目录中文件的 <kbd>在桌面中显示</kbd> 选项。

1. 右键点击 *game.project*
2. 选择 <kbd>在桌面中显示</kbd>

![Show in Finder](images/zerobrane/show_in_desktop.png)

## 设置 ZeroBrane

要设置 ZeroBrane，请选择 <kbd>项目 ▸ 项目目录 ▸ 选择...</kbd>：

![Set up](images/zerobrane/setup.png)

一旦设置完成以匹配当前的 Defold 项目目录，就应该能够在 ZeroBrane 中看到 Defold 项目的目录树，并导航和打开文件。

文档后面部分可以找到其他推荐但非必需的配置更改。

## 启动调试服务器

在开始调试会话之前，需要启动 ZeroBrane 内置的调试服务器。启动它的菜单选项可以在 <kbd>项目</kbd> 菜单下找到。只需选择 <kbd>项目 ▸ 启动调试器服务器</kbd>：

![Start debugger](images/zerobrane/startdebug.png)

## 将应用程序连接到调试器

调试可以在 Defold 应用程序生命周期的任何时刻开始，但需要从 Lua 脚本中主动启动。启动调试会话的 Lua 代码如下所示：

::: sidenote
如果您的游戏在调用 `dbg.start()` 时退出，可能是因为 ZeroBrane 检测到问题并向游戏发送了退出命令。由于某种原因，ZeroBrane 需要打开一个文件才能开始调试会话，否则它将输出：
"Can't start debugging without an opened file or with the current file not being saved 'untitled.lua')."
在 ZeroBrane 中，打开您添加了 `dbg.start()` 的文件以修复此错误。
:::

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start()
```

通过将上述代码插入应用程序，它将连接到 ZeroBrane 的调试服务器（默认通过 "localhost"）并在下一个要执行的语句处暂停。

```txt
Debugger server started at localhost:8172.
Mapped remote request for '/' to '/Users/my_user/Documents/Projects/Defold_project/'.
Debugging session started in '/Users/my_user/Documents/Projects/Defold_project'.
```

现在可以使用 ZeroBrane 中提供的调试功能；您可以单步执行、检查、添加和删除断点等。

::: sidenote
调试仅在启动调试的 lua 上下文中启用。在 *game.project* 中启用 "shared_state" 意味着无论您从哪里启动，都可以调试整个应用程序。
:::

![Stepping](images/zerobrane/code.png)

如果连接尝试失败（可能是因为调试服务器未运行），您的应用程序将在连接尝试完成后继续正常运行。

## 远程调试

由于调试是通过常规网络连接（TCP）进行的，这允许进行远程调试。这意味着当您的应用程序在移动设备上运行时，也可以对其进行调试。

唯一需要更改的是启动调试的命令。默认情况下，`start()` 将尝试连接到 localhost，但对于远程调试，我们需要手动指定 ZeroBrane 调试服务器的地址，如下所示：

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start("192.168.5.101")
```

这也意味着确保从远程设备有网络连接非常重要，并且任何防火墙或类似软件都允许通过端口 8172 的 TCP 连接。否则，当应用程序尝试连接到您的调试服务器时，可能会卡住。

## 其他推荐的 ZeroBrane 设置

可以使 ZeroBrane 在调试期间自动打开 Lua 脚本文件。这使得可以单步执行到其他源文件中的函数，而无需手动打开它们。

第一步是访问编辑器配置文件。建议您更改该文件的用户版本。

- 选择 <kbd>编辑 ▸ 首选项 ▸ 设置：用户</kbd>
- 将以下内容添加到配置文件中：

  ```txt
  - to automatically open files requested during debugging
  editor.autoactivate = true
  ```

- 重启 ZeroBrane

![Other recommended settings](images/zerobrane/otherrecommended.png)