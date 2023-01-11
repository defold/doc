---
title: Defold 性能分析
brief: 本教程介绍了 Defold 内置的性能分析工具.
---

# 性能分析

Defold 引擎内置了性能分析工具. 这些工具用来分析查找性能和内存占用的问题. 内置分析器只在打包 debug 版应用中可用. Defold 的逐帧分析使用了 [Celtoys 出品的远程分析器](https://github.com/Celtoys/Remotery).

## 运行时可视分析器

Debug 应用包含运行时可视分析工具可以在应用最上层把分析信息显示出来:

```lua
function on_reload(self)
    -- 热重载时打开分析表.
    profiler.enable_ui(true)
end
```

![Visual profiler](images/profiling/visual_profiler.png)

此分析器提供了一些函数用来改变其数据显示方式:

```lua

profiler.set_ui_mode()
profiler.set_ui_view_mode()
profiler.view_recorded_frame()
```

详情请见 [分析器 API 文档](/ref/stable/profiler/).

## 网页版分析器

运行debug版游戏时, 可以用浏览器访问一个基于网页的分析器.

### 逐帧分析器
逐帧分析器可以对正在运行中的游戏进行采样然后逐帧进行分析. 访问分析器的方法

1. 在目标设备上启动游戏.
2. 选择菜单 <kbd> Debug ▸ Open Web Profiler</kbd>.

逐帧分析器分为若干视图. 每个视图给出当前运行游戏某个方面的数据.
点击右上角的暂停按钮可暂停视图数据的更新.

![Web profiler](images/profiling/webprofiler_page.png)

::: sidenote
同时使用多个目标设备时, 可以随时手动切换. 方法是修改页面上方 Connection Address 框内的地址来匹配控制台输出的远程分析器 URL:

```
INFO:ENGINE: Defold Engine 1.3.4 (80b1b73)
INFO:DLIB: Initialized Remotery (ws://127.0.0.1:17815/rmt)
INFO:ENGINE: Loading data from: build/default
```
:::

Sample Timeline
: 采样时间轴显示出引擎采样数据的帧, 一个进程对应一个横向时间轴. Main 表示游戏逻辑和引擎代码运行的主线程. Remotery 表示分析器自身. Sound 表示混音和播放进程. 可以放大缩小 (用鼠标滚轮) 并选择某一帧来分析在 Frame Data view 中所展示的该帧的详细数据.

  ![Frames overview](images/profiling/webprofiler_frames_overview.png)

Frame Data
: 帧数据显示了当前选择帧的所有详细数据表格. 这里还可以看到每个游戏循环耗费的毫秒数.

  ![Frame data](images/profiling/webprofiler_frame_data.png)

Global Properties
: 全局属性视图显示了一组计数器. 可以方便地跟踪 draw call 数或者某一类型的组件数等.

  ![Global Properties](images/profiling/webprofiler_global_properties.png)


### 资源分析器
资源分析器可以检查并详细分析当前运行游戏的资源使用情况. 访问分析器的方法:

1. 在目标设备上启动游戏.
2. 打开浏览器并访问 http://localhost:8002

资源分析图表分为2个部分, 一个是集合层级关系, 显示了游戏中所有对象和组件实例, 另一个展示了加载的各种资源.

![Resource profiler](images/profiling/webprofiler_resources_page.png)

Collection view
: 集合视图展示了游戏里各个集合下所实例化出的各个游戏对象和组件的层级关系. 便于查找实例化对象与其原型的对应关系.

Resources view
: 资源视图展示了当前内存中加载的各种资源, 每个资源的空间占用和引用计数. 便于了解资源加载和优化内存使用.

## 编译报告

编译游戏时有个选项可以生成编译报告. 通过报告可以整体把握游戏包中各个资源的空间占用情况. 编译游戏时开启 *Generate build report* 选项即可.

![build report](images/profiling/build_report.png){srcset="images/profiling/build_report@2x.png 2x"}

游戏编译完成后将生成 "report.html" 文件. 用浏览器打开这个文件进行查阅:

![build report](images/profiling/build_report_html.png){srcset="images/profiling/build_report_html@2x.png 2x"}

*Overview* 按资源类别给出空间占用饼图.

*Resources* 给出更详细的数据表格可以用来按照大小, 压缩比, 加密与否, 类别和目录进行排序. 使用 "search" 框还可以对这些数据进行过滤.

*Structure* 基于项目结构给出空间占用树状图. 基于资源文件和目录从绿色 (占用小) 过渡到蓝色 (占用大).

## 外部工具

除了内置工具, 还有许多免费高效的分析跟踪工具. 举例如下:

ProFi (Lua)
: 内置工具里没有针对 Lua 的分析器但是使用外部工具可以做到这一点. 要测量脚本执行时间, 要么在代码里自己编写时间测试代码, 要么使用 ProFi 之类的 Lua 库.

  https://github.com/jgrahamc/ProFi

  注意纯 Lua 分析器使用时会为代码执行增加一些负担. 这可能会造成测量结果不准确. 虽然计数器工具还是蛮准确的.

Instruments (macOS and iOS)
: Xcode 包含一个性能分析可视化工具. 使用它可以跟踪检查一个或多个应用或进程的行为, 测试设备功能 (比如 Wi-Fi 和 Bluetooth) 等等.

  ![instruments](images/profiling/instruments.png){srcset="images/profiling/instruments@2x.png 2x"}

OpenGL 分析器 (macOS)
: 可以将 OpenGL 分析器作为 "Additional Tools for Xcode" 下载下来 (Xcode 菜单选择 <kbd>Xcode ▸ Open Developer Tool ▸ More Developer Tools...</kbd>).

  此工具可以用来分析运行中的 Defold 应用如何使用 OpenGL. 可以用来跟踪 OpenGL 函数调用, 在 OpenGL 函数上打断点, 调查应用资源 (纹理, 程序, 着色器之类的), 查看缓存内容, 以及 OpenGL 的各方面状态.

  ![opengl profiler](images/profiling/opengl.png){srcset="images/profiling/opengl@2x.png 2x"}

Android 分析器 (Android)
: https://developer.android.com/studio/profile/android-profiler.html

  Android 分析器是一组能够试试捕捉游戏 CPU, 内存及网络使用情况的工具. 可以基于取样跟踪代码执行, 堆栈使用, 内存分配及网络文件传输. 要使用这个工具需要在 "AndroidManifest.xml" 里设置 `android:debuggable="true"`.

  ![android profiler](images/profiling/android_profiler.png)

  注意: 從 Android Studio 版本 4.1 開始, 也可以 [不用運行 Android Studio 而直接進行分析](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers).

图像 API 调试器 (Android)
: https://github.com/google/gapid

  这组工具可以用来查看, 微调和重放从程序到显卡驱动的功能调用. 要使用这个工具需要在 "AndroidManifest.xml" 里设置 `android:debuggable="true"`.

  ![graphics api debugger](images/profiling/gapid.png)
