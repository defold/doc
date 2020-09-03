---
title: 如何获得帮助
brief: 本教程介绍了使用 Defold 遇到麻烦时该如何寻求帮助.
---

# 获得帮助

如果你使用 Defold 时遇到了麻烦请联系我们以便解决或绕过问题! 有许多途径可以讨论和汇报问题. 依个人喜好选择:

## 在论坛里提交问题

在我们的 [论坛](https://forum.defold.com) 上提交问题是一个好方法. 依据你的问题的类型可以在 [Questions](https://forum.defold.com/c/questions) 或者 [Bugs](https://forum.defold.com/c/bugs) 类目下发帖. 提交问题的时候请尽附加可能多的信息. 记得发问之前在论坛 [搜索](https://forum.defold.com/search) 一下相关内容, 也许论坛上已经存在你的问题的解决方案了. 提问时请填写以下信息:

* **问题的描述 (必须)** - 问题的简短描述.

* **问题的复现 (必须)** - 复现问题的步骤:
  1. 进入 '...'
  2. 点击 '....'
  3. 滑动到 '....'
  4. 错误出现

* **期望行为 (必须)** - 期望实现的行为的简短描述.

* **Defold 版本 (必须)** - 版本 [例如 1.2.155]. 最好再加上引擎和编辑器的 SHA1, 可以从 <kbd>Help->About</kbd> 菜单项里看到.

* **操作平台 (必须)** - 在哪个操作平台上出现的问题?
  - 平台: [比如 iOS, Android, Windows, macOS, Linux, HTML5]
  - 系统: [比如 iOS8.1, Windows 10, High Sierra]
  - 设备: [比如 iPhone6]

* **详细系统信息 (可选)** - 有关错误出现系统平台的详细信息.
  - HTML5: 提供关于 WebGL 的详细信息, 参考网站 https://webglreport.com/?v=1

* **日志 (可选)** - 请附带相关 (云编译服务器, 引擎和编辑器) 日志. 参考 [下面关于日志文件获取的章节](#log-files).

* **问题复现小项目 (可选)** - 请附加一个可以再现问题的最小项目包. 这可以对别人研究修复问题提供极大帮助. 如果你把项目打成zip包请去掉其中的 `.git`, `.internal` 和 `build` 文件夹.

* **绕过方法 (可选)** - 如果你找到了可以绕过问题的方案, 也请附加上.

* **屏幕截图 (可选)** - 如果可以, 附加屏幕截图有助于描述出现的问题.

* **其他 (可选)** - 还可以加入其他问题相关上下文信息.


## 从编辑器里汇报问题

编辑器提供了一个汇报错误的方便的方法. 选择 <kbd>Help->Report Issue</kbd> 菜单项来汇报错误.

![](images/getting_help/report_issue.png)

这样就会在 GitHub 上生成一个错误报告. 请尽量详述错误的相关信息. 参考 [下面关于日志文件获取的章节](#log-files).

::: 注意
报告之前确保你已经拥有 GitHub 账户.
:::


## 在 Slack 上讨论问题

如果在使用 Defold 时遇到困难你可以尝试在 [Slack](https://www.defold.com/slack/) 上提出问题. 虽然我们推荐复杂问题应该在论坛上深入讨论. 而且注意 Slack 上不支持错误报告.


# 日志文件

游戏引擎, 编辑器和云编译服务器都有日志系统, 这对于定位调试错误十分有利. 报告错误时请务必带上日志文件.

## 引擎日志
- Android: 可以使用 `adb` (Android Debug Bridge) 命令获取. 有关 `adb` 命令详情请见 [Android 教程](/manuals/android/#android-debug-bridge).
- iOS: 可以使用 XCode 的设备和模拟器菜单项获取.
- HTML5: 浏览器控制台会输出日志:
  - Chrome: 菜单 > 更多工具 > 开发者工具
  - Firefox: 工具 > 网络开发者 > 网络控制台
  - Safari: 开发 > 显示 JavaScript 控制台
- Desktop: 如果从终端/命令控制台启动 Defold 程序的话, 就可以在上面看到输出的日志了.

有个功能就是程序崩溃时把相关信息写入一个日志文件中去. 详情请见 [调试教程](/manuals/debugging/#extracting-the-logtxt-file).

## 编辑器日志
- Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
- macOS: `/Users/ **Your Username** /Library/Application Support/` 或者 `~/Library/Application Support/Defold`
- Linux: `~/.Defold`

## 云编译服务器日志
使用原生扩展时才会有编译服务器日志. 编译时其日志文件 (`log.txt`) 与自定义引擎一起下载并保存在 `.internal/%platform%/build.zip` 文件中.
