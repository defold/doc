---
title: 打包应用程序
brief: 本手册介绍了如何创建应用程序包.
---

# 打包应用程序

在开发应用程序时，您应该养成在目标平台上尽可能频繁地测试游戏的习惯。您应该这样做是为了在开发过程的早期阶段发现性能问题，这些问题在此时更容易解决。还建议在所有目标平台上进行测试，以发现着色器等方面的差异。在移动设备上开发时，您可以选择使用[移动开发应用](/manuals/dev-app/)将内容推送到应用程序，而不必进行完整的打包和卸载/安装循环。

您可以在Defold编辑器本身中为Defold支持的所有平台创建应用程序包，无需任何外部工具。您也可以使用我们的命令行工具从命令行打包。如果您的项目包含一个或多个[原生扩展](/manuals/extensions)，应用程序打包需要网络连接。

## 从编辑器中打包

您可以通过项目菜单和Bundle选项创建应用程序包：

![](images/bundling/bundle_menu.png)

选择任何菜单选项都会为该特定平台打开Bundle对话框。

### 构建报告

打包游戏时，有一个选项可以创建构建报告。这对于了解构成游戏包的所有资源的大小非常有用。只需在打包游戏时勾选*Generate build report*复选框即可。

![build report](images/profiling/build_report.png)

要了解更多关于构建报告的信息，请参考[性能分析手册](/manuals/profiling/#build-reports)。


### Android

创建Android应用程序包（.apk文件）的文档记录在[Android手册](/manuals/android/#creating-an-android-application-bundle)中。

### iOS

创建iOS应用程序包（.ipa文件）的文档记录在[iOS手册](/manuals/ios/#creating-an-ios-application-bundle)中。

### macOS

创建macOS应用程序包（.app文件）的文档记录在[macOS手册](/manuals/macos)中。

### Linux

创建Linux应用程序包不需要特定设置，也不需要在*game.project*[项目设置文件](/manuals/project-settings/#linux)中进行可选的平台特定配置。

### Windows

创建Windows应用程序包（.exe文件）的文档记录在[Windows手册](/manuals/windows)中。

### HTML5

创建HTML5应用程序包以及可选设置的文档记录在[HTML5手册](/manuals/html5/#creating-html5-bundle)中。

#### Facebook Instant Games

可以为Facebook Instant Games创建一个特殊版本的HTML5应用程序包。这个过程在[Facebook Instant Games手册](/manuals/instant-games/)中有详细说明。

## 从命令行打包

编辑器使用我们的命令行工具[Bob](/manuals/bob/)来打包应用程序。

在进行应用程序的日常开发时，您可能会在Defold编辑器内进行构建和打包。在其他情况下，您可能希望自动生成应用程序包，例如在发布新版本时为所有目标进行批量构建，或者创建最新版本游戏的夜间构建，也许在CI环境中。应用程序的构建和打包可以在正常编辑器工作流程之外使用[Bob命令行工具](/manuals/bob/)完成。

## 包布局

逻辑包布局结构如下：

![](images/bundling/bundle_schematic_01.png)

包被输出到一个文件夹中。根据平台的不同，该文件夹也可能被zip归档到`.apk`或`.ipa`中。
文件夹的内容取决于平台。

除了可执行文件外，我们的打包过程还会收集平台所需的资源（例如Android的.xml资源文件）。

使用[bundle_resources](https://defold.com/manuals/project-settings/#bundle-resources)设置，您可以配置应原样放置在包中的资源。
您可以按平台控制这一点。

游戏资源位于`game.arcd`文件中，它们使用LZ4压缩单独压缩。
使用[custom_resources](https://defold.com/manuals/project-settings/#custom-resources)设置，您可以配置应放置（并压缩）在`game.arcd`中的资源。
这些资源可以通过[`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource)函数访问。

## Release 与 Debug

创建应用程序包时，您可以选择创建debug或release包。这两种包之间的差异很小，但重要的是要记住：

* Release构建不包含[性能分析器](/manuals/profiling)
* Release构建不包含[屏幕录制器](/ref/stable/sys/#start_record)
* Release构建不显示任何对`print()`的调用的输出或任何原生扩展的输出
* Release构建在`sys.get_engine_info()`中将`is_debug`值设置为`false`
* Release构建在调用`tostring()`时不会对`hash`值进行反向查找。这在实践中意味着，对于类型为`url`或`hash`的值的`tostring()`将返回其数字表示，而不是原始字符串（`'hash: [/camera_001]'`对比`'hash: [11844936738040519888 (unknown)]'`）
* Release构建不支持来自编辑器的[热重载](/manuals/hot-reload)和类似功能的targeting



