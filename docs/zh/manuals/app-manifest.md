---
title: App manifest
brief: 本教程介绍了如何使用应用清单来去掉引擎的特性.
---

# App manifest

应用清单控制为引擎加入或去掉功能特性. 推荐为引擎去掉不用的特性因为可以减小游戏包体.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

## Physics

控制使用哪个物理引擎, 或者选择 None 来完全去掉物理引擎.


## Exclude Record

从引擎中去掉视频录制功能 (参见手册 [`start_record`](https://defold.com/ref/stable/sys/#start_record) 消息).


## Exclude Profiler

从引擎中去掉分析器. 分析器用来收集性能和使用计数器. 参见 [分析器教程](/manuals/profiling/).


## Exclude Sound

从引擎中去掉所有声音播放功能.


## Exclude Input

从引擎中去掉所有输入处理.


## Exclude Live Update

从引擎中去掉 [热更新功能](/manuals/live-update).


## Exclude Basis Universal

从引擎中去掉基础通用 [纹理压缩库](/manuals/texture-profiles).


## Use Android Support Lib

使用安卓支持库而不使用 Android X. [更多详情参见这里](https://defold.com/manuals/android/#using-androidx).


## Graphics

选择使用的图形后端.

* OpenGL - 只包含 OpenGL.
* Vulkan - 只包含 Vulkan.
* OpenGL and Vulkan - 同时包含 OpenGL 和 Vulkan. Vulkan 是默认的, Vulkan 不可以时使用 OpenGL.
