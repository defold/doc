---
title: Defold 中的性能分析
brief: 本手册解释了 Defold 中存在的性能分析工具。
---

# 性能分析

Defold 包含一组与引擎和构建流程集成的性能分析工具。这些工具旨在帮助发现性能和内存使用方面的问题。内置的性能分析器仅在调试版本中可用。Defold 中使用的帧性能分析器是 [Celtoys 的 Remotery 性能分析器](https://github.com/Celtoys/Remotery)。

## 运行时可视化性能分析器

调试版本具有运行时可视化性能分析器，显示实时信息并渲染在运行应用程序的顶部：

```lua
function on_reload(self)
    -- 在热重载时切换可视化性能分析器。
    profiler.enable_ui(true)
end
```

![Visual profiler](images/profiling/visual_profiler.png)

可视化性能分析器提供了许多不同的功能，可用于改变可视化性能分析器呈现其数据的方式：

```lua

profiler.set_ui_mode()
profiler.set_ui_view_mode()
profiler.view_recorded_frame()
```

有关性能分析器功能的更多信息，请参阅[性能分析器 API 参考](/ref/stable/profiler/)。

## Web 性能分析器

运行游戏的调试版本时，可以通过浏览器访问基于 Web 的交互式性能分析器。

### 帧性能分析器
帧性能分析器允许您在游戏运行时对其进行采样，并详细分析各个帧。要访问性能分析器：

1. 在目标设备上启动您的游戏。
2. 选择 <kbd> Debug ▸ Open Web Profiler</kbd> 菜单。

帧性能分析器分为几个部分，都提供对运行游戏的不同视图。按右上角的暂停按钮可以暂时停止性能分析器更新视图。

![Web profiler](images/profiling/webprofiler_page.png)

::: sidenote
当您同时使用多个目标时，可以通过更改页面顶部的连接地址字段以匹配目标启动时控制台中显示的 Remotery 性能分析器 URL 来手动切换它们：

```
INFO:ENGINE: Defold Engine 1.3.4 (80b1b73)
INFO:DLIB: Initialized Remotery (ws://127.0.0.1:17815/rmt)
INFO:ENGINE: Loading data from: build/default
```
:::

采样时间轴
: 采样时间轴将显示在引擎中捕获的数据帧，每个线程一个水平时间轴。Main 是运行所有游戏逻辑和大部分引擎代码的主线程。Remotery 用于性能分析器本身，Sound 用于声音混合和播放线程。您可以放大和缩小（使用鼠标滚轮）并选择单个帧以在帧数据视图中查看帧的详细信息。

  ![Sample Timeline](images/profiling/webprofiler_sample_timeline.png)


帧数据
: 帧数据视图是一个表格，其中当前选定帧的所有数据都被分解为详细信息。您可以查看在每个引擎作用域中花费了多少毫秒。

  ![Frame data](images/profiling/webprofiler_frame_data.png)


全局属性
: 全局属性视图显示一个计数器表。它们使您可以轻松地，例如，跟踪绘制调用的数量或特定类型组件的数量。

  ![Global Properties](images/profiling/webprofiler_global_properties.png)


### 资源性能分析器
资源性能分析器允许您在游戏运行时检查它并详细分析资源使用情况。要访问性能分析器：

1. 在目标设备上启动您的游戏。
2. 打开浏览器并浏览到 http://localhost:8002

资源性能分析器分为 2 个部分，一个显示游戏中当前实例化的集合、游戏对象和组件的层次视图，另一个显示所有当前加载的资源。

![Resource profiler](images/profiling/webprofiler_resources_page.png)

集合视图
: 集合视图显示游戏中当前实例化的所有游戏对象和组件的层次列表，以及它们来自哪个集合。当您需要深入了解并了解在任何给定时间在游戏中实例化了什么以及对象来自何处时，这是一个非常有用的工具。

资源视图
: 资源视图显示当前加载到内存中的所有资源、它们的大小以及对每个资源的引用数量。当您需要了解在任何给定时间加载到内存中的内容时，这对于优化应用程序中的内存使用非常有用。


## 构建报告

打包游戏时，可以选择创建构建报告。这对于了解游戏包中所有资产的大小非常有用。只需在打包游戏时勾选*生成构建报告*复选框。

![build report](images/profiling/build_report.png)

构建器将在游戏包旁边生成一个名为"report.html"的文件。在 Web 浏览器中打开该文件以检查报告：

![build report](images/profiling/build_report_html.png)

*概述*根据资源类型提供项目大小的整体视觉分解。

*资源*显示您可以按大小、压缩比、加密、类型和目录名称排序的资源的详细列表。使用"搜索"字段过滤显示的资源条目。

*结构*部分显示基于资源在项目文件结构中组织的大小。条目根据文件和目录内容的相对大小从绿色（轻）到蓝色（重）进行颜色编码。


## 外部工具

除了内置工具外，还有各种免费的高质量跟踪和性能分析工具可用。以下是其中的一些选择：

ProFi (Lua)
: 我们不提供任何内置的 Lua 性能分析器，但有足够容易使用的外部库。要找出您的脚本在哪里花费时间，可以在代码中自己插入时间测量，或者使用像 [ProFi](https://github.com/jgrahamc/ProFi) 这样的 Lua 性能分析库。

  请注意，纯 Lua 性能分析器会为它们安装的每个钩子增加相当多的开销。因此，您应该对从这样的工具获得的计时配置文件持谨慎态度。不过，计数配置文件是足够准确的。

Instruments (macOS and iOS)
: 这是 Xcode 的一部分的性能分析器和可视化工具。它允许您跟踪和检查一个或多个应用程序或进程的行为，检查设备特定功能（如 Wi-Fi 和蓝牙）等等。

  ![instruments](images/profiling/instruments.png)

OpenGL 性能分析器 (macOS)
: 您可以从 Apple 下载的"Xcode 附加工具"包的一部分（在 Xcode 菜单中选择 <kbd>Xcode ▸ Open Developer Tool ▸ More Developer Tools...</kbd>）。

  此工具允许您检查正在运行的 Defold 应用程序并查看它如何使用 OpenGL。它允许您跟踪 OpenGL 函数调用，在 OpenGL 函数上设置断点，调查应用程序资源（纹理、程序、着色器等），查看缓冲区内容，并检查 OpenGL 状态的其他方面。

  ![opengl profiler](images/profiling/opengl.png)

Android 性能分析器 (Android)
: https://developer.android.com/studio/profile/android-profiler.html

  一组性能分析工具，可捕获游戏 CPU、内存和网络活动的实时数据。您可以执行基于采样的代码执行方法跟踪，捕获堆转储，查看内存分配，并检查网络传输文件的详细信息。使用该工具需要您在"AndroidManifest.xml"中设置 `android:debuggable="true"`。

  ![android profiler](images/profiling/android_profiler.png)

  注意：从 Android Studio 4.1 开始，也可以[在不启动 Android Studio 的情况下运行性能分析工具](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers)。

Graphics API 调试器 (Android)
: https://github.com/google/gapid

  这是一组工具，允许您检查、调整和重放从应用程序到图形驱动程序的调用。要使用该工具需要您在"AndroidManifest.xml"中设置 `android:debuggable="true"`。

  ![graphics api debugger](images/profiling/gapid.png)
