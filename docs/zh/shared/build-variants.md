## Build variants

打包游戏时, 需要选择你想用的引擎类型. 有三个基本类型可以选择:

  * Debug
  * Release
  * Headless

这些类型即是 `Build variants`

::: sidenote
使用 <kbd>Project ▸ Build</kbd> 时使用的是 debug 版引擎.
:::

### Debug

此版本通常在游戏开发阶段使用, 因为它具有许多有用的调试功能:

* 分析器 - 用于收集性能和使用计数器. 如何使用分析器参见 [分析器教程](/manuals/profiling/).
* 日志 - 日志开启后引擎会记录系统信息, 警告和错误. 引擎也会通过 Lua `print()` 功能, 原生扩展使用 `dmLogInfo()`, `dmLogError()` 之类的功能记录日志. 如何阅读日志参见 [游戏和系统日志教程](https://defold.com/manuals/debugging-game-and-system-logs/).
* 热重载 - 热重载是一个强大的功能, 能让开发者在游戏运行时重新载入资源. 如何使用热重载参见 [热重载教程](https://defold.com/manuals/hot-reload/).
* 引擎服务 - 游戏的调试版本可以连结一些开启的 TCP 端口和服务并与之交互. 这些服务包括热重载功能, 远程日志存取和上述的分析器功能, 以及其他一些各种各样的服务. 关于引擎服务参见 [开发者教程](https://github.com/defold/defold/blob/dev/engine/docs/DEBUG_PORTS_AND_SERVICES.md).

### Release

此版本移除调试功能. 准备发布到应用商店时使用此版本. 基于以下原因不推荐发布包含调试功能的游戏:

* 调试功能会使包体略微变大, [我们应该尽量使发布游戏包体最小](https://defold.com/manuals/optimization/#optimize-application-size).
* 调试功能也会占用一点 CPU 时长. 这可能使用户的老机型卡顿. 在手机上增加 CPU 使用也会造成过热和电池消耗.
* 调试功能可能会给用户暴露不应暴露的信息, 无论从安全, 作弊还是欺诈角度.

### Headless

此版本没有图像和声音. 也就是说它可以 CI 服务器上进行 unit/smoke 测试, 甚至可以在云端作为服务器程序使用.
