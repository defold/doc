---
title: 原生扩展 - 扩展清单
brief: 本手册描述了扩展清单及其与应用清单和引擎清单的关联方式。
---

# 扩展、应用和引擎清单文件

扩展清单是一个配置文件，包含用于构建单个扩展的标志和定义。此配置与应用级配置和Defold引擎本身的基础级配置相结合。

## 应用清单

应用清单（文件扩展名`.appmanifest`）是关于如何在构建服务器上构建游戏的应用级配置。应用清单允许您移除引擎中不使用的部分。如果您不需要物理引擎，可以从可执行文件中移除它以减小其大小。了解如何排除未使用的功能，请参阅[应用清单手册](/manuals/app-manifest)。

## 引擎清单

Defold引擎有一个构建清单（`build.yml`），它包含在引擎和Defold SDK的每个版本中。该清单控制使用哪些SDK版本，运行哪些编译器、链接器和其他工具，以及向这些工具传递哪些默认构建和链接标志。该清单可以在GitHub上的share/extender/build_input.yml中找到[在GitHub上](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml)。

## 扩展清单

另一方面，扩展清单（`ext.manifest`）是专门针对扩展的配置文件。扩展清单控制扩展的源代码如何编译和链接，以及包含哪些额外的库。

这三种不同的清单文件都共享相同的语法，以便它们可以合并并完全控制扩展和游戏的构建方式。

对于每个构建的扩展，清单按以下方式合并：

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

这允许用户覆盖引擎的默认行为以及每个扩展的行为。而且，在最终的链接阶段，我们将应用清单与defold清单合并：

	manifest = merge(game.appmanifest, build.yml)


### ext.manifest文件

除了扩展名称外，清单文件还可以包含特定于平台的编译标志、链接标志、库和框架。如果*ext.manifest*文件不包含"platforms"部分，或者列表中缺少某个平台，您为其打包的平台仍将构建，但不会设置任何额外的标志。

以下是一个示例：

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    armv7-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### 允许的键

特定于平台的编译标志允许的键有：

* `frameworks` - 构建时要包含的Apple框架（iOS和macOS）
* `weakFrameworks` - 构建时可选包含的Apple框架（iOS和macOS）
* `flags` - 应传递给编译器的标志
* `linkFlags` - 应传递给链接器的标志
* `libs` - 链接时要包含的额外库
* `defines` - 构建时要设置的定义
* `aaptExtraPackages` - 应生成的额外包名（Android）
* `aaptExcludePackages` - 要排除的包的正则表达式（或确切名称）（Android）
* `aaptExcludeResourceDirs` - 要排除的资源目录的正则表达式（或确切名称）（Android）
* `excludeLibs`, `excludeJars`, `excludeSymbols` - 这些标志用于移除平台上下文中先前定义的内容。

对于所有关键字，我们应用白名单过滤器。这是为了避免非法路径处理和访问构建上传文件夹之外的文件。