---
title: 如何获得帮助
brief: 本教程介绍了使用 Defold 遇到麻烦时该如何寻求帮助.
---

# 获得帮助

如果你使用 Defold 时遇到了麻烦请联系我们以便解决或绕过问题! 有许多途径可以讨论和汇报问题. 依个人喜好选择:

## 在论坛里提交问题

在我们的 [论坛](https://www.defold.com/forum) 上提交问题是一个好方法. 依据你的问题的类型可以在 [Questions](https://forum.defold.com/c/questions) 或者 [Bugs](https://forum.defold.com/c/bugs) 类目下发帖. 提交问题的时候请尽附加可能多的信息. 记得发问之前在论坛 [搜索](https://forum.defold.com/search) 一下相关内容, 也许论坛上已经存在你的问题的解决方案了. 提问时请填写以下信息:

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

* **日志 (可选)** - 请附加相关日志 (引擎或者编辑器的). 编辑器日志位于:
  - Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  - macOS: `/Users/ **Your Username** /Library/Application Support/` 或者 `~/Library/Application Support/Defold`
  - Linux: `~/.Defold`

  Android 的引擎日志可以通过使用 `adb` (Android Debug Bridge) 命令行工具获取. 关于 `adb` 命令行工具详情请见 [Android 教程](/manuals/android/#android-debug-bridge).

  iOS 的引擎日志可以通过使用 XCode 和设备模拟器菜单项获取.

  HTML5 的引擎日志可以通过使用浏览器开发者控制台获取:
  - Chrome: 菜单 > 更多工具 > 开发者工具
  - Firefox: 工具 > web 开发者 > Web 控制台
  - Safari: 开发 > 显示 JavaScript 控制台

  桌面应用的引擎日志通过使用终端运行Defold应用获取.

  你还可以把引擎日志写入一个文件便于存取. 详情请见 [调试教程](/manuals/debugging/#提取日志文件).

* **问题复现小项目 (可选)** - 请附加一个可以再现问题的最小项目包. 这可以对别人研究修复问题提供极大帮助. 如果你把项目打成zip包请去掉其中的 `.git`, `.internal` 和 `build` 文件夹.

* **绕过方法 (可选)** - 如果你找到了可以绕过问题的方案, 也请附加上.

* **屏幕截图 (可选)** - 如果可以, 附加屏幕截图有助于描述出现的问题.

* **其他 (可选)** - 还可以加入其他问题相关上下文信息.


## 从编辑器里汇报问题

编辑器提供了一个汇报错误的方便的方法. 选择 <kbd>Help->Report Issue</kbd> 菜单项来汇报错误.

![](images/getting_help/report_issue.png)

选择此菜单项会在 GitHub 上提交一个 issue tracker. 请把尽量多的信息填入报表. 注意此种方法需要你有 GitHub 账号.


## 在 Slack 上讨论问题

如果在使用 Defold 时遇到困难你可以尝试在 [Slack](https://www.defold.com/slack/) 上提出问题. 虽然我们推荐复杂问题应该在论坛上深入讨论. 而且注意 Slack 上不支持错误报告.
