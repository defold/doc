---
title: 优化 Defold 游戏的大小
brief: 本手册描述了如何优化 Defold 游戏的大小。
---

# 优化游戏大小

您的游戏大小可能是网络和移动平台等的关键成功因素，而在桌面和控制台平台上，磁盘空间便宜且通常充足，因此重要性较低。

### iOS 和 Android
Apple 和 Google 已经定义了通过移动网络（而不是通过 Wifi 下载）下载时的应用程序大小限制。对于 Android，使用[应用捆绑包](https://developer.android.com/guide/app-bundle#size_restrictions)发布的应用程序的此限制为 200 MB。对于 iOS，如果应用程序大于 200 MB，用户将收到警告，但仍可以继续下载。

::: sidenote
根据 2017 年的一项研究，"APK 大小每增加 6 MB，我们看到安装转化率下降 1%。"（[来源](https://medium.com/googleplaydev/shrinking-apks-growing-installs-5d3fcba23ce2)）
:::

### HTML5
Poki 和许多其他网络游戏平台建议初始下载不应超过 5 MB。

Facebook 建议Facebook即时游戏应在不到 5 秒内启动，最好少于 3 秒。这对实际应用程序大小意味着什么没有明确定义，但我们讨论的是高达 20 MB 的大小。

可玩广告通常限制在 2 到 5 MB 之间，具体取决于广告网络。

## 大小优化策略
您可以通过两种方式优化应用程序大小；通过减小引擎的大小和/或通过减小游戏资源的大小。

为了更好地了解构成应用程序大小的因素，您可以在打包时[生成构建报告](/manuals/bundling/#build-reports)。通常，声音和图形是占用任何游戏大小的大部分。

::: important
Defold 在构建和打包您的应用程序时将创建一个依赖树。构建系统将从 *game.project* 文件中指定的引导集合开始，并检查每个引用的集合、游戏对象和组件，以构建正在使用的资源列表。只有这些资源将被包含在最终的应用程序包中。任何未直接引用的内容都将被排除。虽然知道未使用的资源不会被包含是好事，但您作为开发人员仍需要考虑最终应用程序中的内容以及单个资源的大小和应用程序包的总大小。
:::

## 优化引擎大小
减小引擎大小的一种快速方法是移除您不使用的引擎中的功能。这是通过[应用程序清单文件](https://defold.com/manuals/app-manifest/)完成的，您可以在其中移除不需要的引擎组件。例如：

* 物理 - 如果您的游戏不使用 Box2D 或 Bullet3D 物理，则强烈建议移除物理引擎
* LiveUpdate - 如果您的游戏不使用 LiveUpdate，则可以移除它
* 图像加载器 - 如果您的游戏不使用 `image.load()` 手动加载和解码图像
* BasisU - 如果您的游戏纹理较少，请比较不使用 BasisU（通过应用程序清单移除）和纹理压缩的构建大小与使用 BasisU 和压缩纹理的构建大小。对于纹理有限的游戏，减少二进制大小并跳过纹理压缩可能更有益。此外，不使用转码器可以降低运行游戏所需的内存量。

## 优化资源大小
在资源大小优化方面，最大的收益通常是通过减小声音和纹理的大小来获得的。

### 优化声音
Defold 支持这些格式：
* .wav
* .ogg
* .opus

声音文件必须使用 16 位采样。
我们的声音解码器将根据当前声音设备需要向上/向下缩放声音采样率。

像音效这样的较短声音通常压缩得更厉害，而音乐文件的压缩较少。
Defold 不进行压缩，因此开发人员必须针对每种音频格式专门处理压缩。

您可以使用外部声音编辑器软件（或使用例如 [ffmpeg](https://ffmpeg.org) 的命令行）编辑声音以降低质量或在格式之间转换。还可以考虑将声音从立体声转换为单声道以进一步减小内容的大小。

### 优化纹理
在优化游戏使用的纹理方面，您有几种选择，但首先要做的是检查添加到图集或用作瓦片源的图像的大小。您永远不应该在图像上使用比游戏中实际需要的更大的尺寸。导入大图像并将它们缩小到适当的大小是对纹理内存的浪费，应该避免。首先使用外部图像编辑软件将图像的大小调整为游戏中实际需要的大小。对于背景图像之类的东西，使用小图像并将其放大到所需的大小可能也是可以的。一旦您将图像缩小到正确的大小并添加到图集或用于瓦片源中，您还需要考虑图集本身的大小。可以使用的最大图集大小因平台和图形硬件而异。

::: sidenote
[这个论坛帖子](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl)提供了有关如何使用脚本或第三方软件调整多个图像大小的几个技巧。
:::

* HTML5 上报告给 [Web3D 调查项目](https://web3dsurvey.com/webgl/parameters/MAX_TEXTURE_SIZE) 的最大纹理大小
* iOS 上的最大纹理大小：
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* Android 上的最大纹理大小差异很大，但通常所有合理新的设备都至少支持 4096x4096。

如果图集太大，您需要将其拆分为几个较小的图集，使用多页图集或使用纹理配置文件缩放整个图集。Defold 中的纹理配置文件系统不仅允许您缩放整个图集，还允许应用压缩算法以减少磁盘上图集的大小。您可以[在手册中阅读有关纹理配置文件的更多信息](/manuals/texture-profiles/)。如果您不知道使用什么，请尝试从这些设置开始作为进一步自定义的起点：

* mipmaps: false
* premultiply_alpha: true
* format: TEXTURE_FORMAT_RGBA
* compression_level: NORMAL
* compression_type: COMPRESSION_TYPE_BASIS_UASTC

::: sidenote
您可以阅读有关如何优化和管理纹理的更多信息，请参阅[此论坛帖子](https://forum.defold.com/t/texture-management-in-defold/8921)。
:::

### 优化字体
如果您指定将要使用的符号并在[字符](/manuals/font/#properties)中设置它，而不是使用"所有字符"复选框，那么您的字体大小将会更小。

### 排除内容以按需下载
减少初始应用程序大小的另一种方法是从应用程序包中排除部分游戏内容并按需下载。Defold 提供了一个名为 Live Update 的系统，用于排除内容以按需下载。

排除的内容可以是整个关卡，也可以是可解锁的角色、皮肤、武器或车辆。如果您的游戏有很多内容，请组织加载过程，使引导集合和第一个关卡集合包含该关卡所需的最低限度资源。您可以通过使用启用了"排除"复选框的集合代理或工厂来实现这一点。根据玩家的进度分割资源。这种方法确保了高效的资源加载并保持初始内存使用量低。在[Live Update 手册](/manuals/live-update/)中了解更多信息。

## Android 特定的大小优化
Android 构建必须支持 32 位和 64 位 CPU 架构。当您为 [Android 打包](/manuals/android)时，您可以指定要包含的 CPU 架构：

![签名 Android 捆绑包](images/android/sign_bundle.png)

Google Play 支持每个游戏发布[多个 APK](https://developer.android.com/google/play/publishing/multiple-apks)，这意味着您可以通过生成两个 APK（每个 CPU 架构一个）并将两者都上传到 Google Play 来减小应用程序大小。

您还可以利用 [APK 扩展文件](https://developer.android.com/google/play/expansion-files)和[Live Update 内容](/manuals/live-update)的组合，这要归功于[资源门户中的 APKX 扩展](https://defold.com/assets/apkx/)。