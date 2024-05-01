## Build variants

When you bundle a game, you need to choose what type of engine you wish to use. You have three basic options:

  * Debug
  * Release
  * Headless

These different versions are also referred to as `Build variants`

::: sidenote
When you choose <kbd>Project ▸ Build</kbd> you'll always get the debug version.
:::


### Debug

This type of executable is typically used during development of a game as it has several useful debugging features included:

* Profiler - Used for gathering performance and usage counters. Learn how to use the profiler in the [Profiling manual](/manuals/profiling/).
* Logging - The engine will log system information, warnings and errors when logging is enabled. The engine will also output logs from the Lua `print()` function and from native extensions logging using `dmLogInfo()`, `dmLogError()` and so on. Learn how to read these logs in the [Game and System Logs manual](https://defold.com/manuals/debugging-game-and-system-logs/).
* Hot reload - Hot-reload is a powerful feature which lets a developer reload resource while the game is running. Learn how to use this in the [Hot-Reload manual](https://defold.com/manuals/hot-reload/).
* Engine services - It is possible to connect to and interact with a debug version of a game through a number of different open TCP ports and services. The services include the hot-reload feature, remote log access and the profiler mentioned above, but also other services to remotely interact with the engine. Learn more about the engine services [in the developer documentation](https://github.com/defold/defold/blob/dev/engine/docs/DEBUG_PORTS_AND_SERVICES.md).


### Release

This variant has the debugging features disabled. This options should be chosen when the game is ready to be released to the app store or in other ways shared with players. It is not recommended to release a game with the debugging features enabled for a number of reasons:

* The debugging features take up a little bit of size in the binary, and [it is a best practice to try to keep the binary size of a released game as small as possible](https://defold.com/manuals/optimization/#optimize-application-size).
* The debugging features takes a little bit of CPU time as well. This can impact the performance of the game if a user has a low-end hardware. On mobile phones the increased CPU usage will also contribute to heating and battery drain.
* The debugging features may expose information about the game that is not intended for the eyes of the players, either from a security, cheating or fraud perspective.


### Headless

This executable runs without any graphics and sound. It means that you can run the game unit/smoke tests on a CI server, or even have it as a game server in the cloud.