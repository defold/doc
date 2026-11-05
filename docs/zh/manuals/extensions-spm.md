---
title: 在 iOS 和 macOS 构建中使用 Swift Package Manager 依赖
brief: 本手册说明如何使用 Swift Package Manager 解析 iOS 和 macOS 构建中的依赖。
---

# Swift Package Manager

[Swift Package Manager](https://www.swift.org/documentation/package-manager/) 是 Swift 和 Xcode 内置的依赖管理器。许多 iOS 和 macOS SDK 以 Swift 包形式发布，其中一些已不再发布为 CocoaPods。Defold 构建引擎时不使用 Xcode，但构建服务器使用 Xcode 下载和构建扩展依赖的 Swift 包，随后以与 [CocoaPods 依赖](/manuals/extensions-cocoapods)相同的方式将结果链接到引擎中。

CocoaPods 和 Swift 包可以在同一项目中使用，甚至可以在同一扩展中使用。


## 声明依赖 {#declaring-dependencies}

原生扩展可以在 `manifests/ios` 和 `manifests/osx` 目录中包含 `SwiftPackages.json` 文件，指定该扩展依赖的 Swift 包。例如：

```json
{
  "platform": "ios",
  "minVersion": "15.0",
  "packages": [
    {
      "url": "https://github.com/firebase/firebase-ios-sdk.git",
      "version": "12.16.0",
      "products": ["FirebaseCore", "FirebaseInstallations"]
    }
  ]
}
```

该文件采用普通 JSON 格式。无需自行编写 `Package.swift` 文件；构建服务器会根据所有扩展的 `SwiftPackages.json` 文件生成它。

文件包含以下字段：

* `platform` - 必填。在 `manifests/ios/SwiftPackages.json` 中为 `"ios"`，在 `manifests/osx/SwiftPackages.json` 中为 `"osx"`。
* `minVersion` - 可选。构建这些包时使用的最低 iOS 或 macOS 版本，例如 `"15.0"`。构建包和链接引擎时，都会采用所有扩展的要求及引擎支持的最低版本中的最大值。
* `wrapperType` - 可选。可设为 `"static"`（默认值）或 `"dynamic"`。请参阅下方的[静态与动态链接](#static-and-dynamic-linking)。
* `packages` - 必填。包列表。每个包包含以下字段：
  * `url` - 包的 git 仓库的 `https://` URL。不接受包含凭据、自定义端口或查询字符串的 URL，也不接受 `ssh` URL，因此仓库必须公开可访问。
  * `products` - 要链接到引擎的包产物。它们是包的 `Package.swift` 文件中 `products` 部分列出的库产物。产物名称不一定与包名称或导入的模块名称相同。
  * 恰好一项版本要求：
    * `version` - 指定的精确版本，例如 `"12.16.0"`。
    * `from` - 此版本或主版本号相同的更新版本。例如，`"9.0.0"` 会解析为最新的 `9.x.x` 版本。
    * `branch` - 某个分支上的最新提交，例如 `"main"`。
    * `revision` - 指定的提交，使用完整的 40 字符提交哈希。

构建服务器会收集所有扩展的 `SwiftPackages.json` 文件，用它们解析全部依赖（包括包自身的依赖），并在构建原生代码时包含这些依赖。


## 在扩展代码中使用包 {#using-packages-from-extension-code}

扩展源代码可以使用这些产物的头文件。请在 Objective-C++（`.mm`）源文件中使用它们。此示例在应用启动时启动 [Sentry](https://github.com/getsentry/sentry-cocoa) SDK：

`manifests/ios/SwiftPackages.json`:

```json
{
  "platform": "ios",
  "minVersion": "15.0",
  "packages": [
    {
      "url": "https://github.com/getsentry/sentry-cocoa.git",
      "from": "9.0.0",
      "products": ["Sentry"]
    }
  ]
}
```

`src/myextension.mm`:

```cpp
#include <dmsdk/sdk.h>

#if defined(DM_PLATFORM_IOS)
#import <UIKit/UIKit.h>
#import <Sentry/Sentry.h>
#import <Sentry/Sentry-Swift.h>
#endif

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
#if defined(DM_PLATFORM_IOS)
    [SentrySDK startWithConfigureOptions:^(SentryOptions* options) {
        options.dsn = @"https://examplePublicKey@o0.ingest.sentry.io/0";
    }];
#endif
    return dmExtension::RESULT_OK;
}
```

* Objective-C 头文件以 `#import <Module/Header.h>` 的形式导入，其中 `Module` 是提供头文件的模块名称。
* 使用 Swift 实现的类在生成的 `<Module/Module-Swift.h>` 头文件中声明。它只包含模块向 Objective-C 暴露的类和方法（在 Swift 中标记为 `@objc`）。请先导入 `UIKit`（macOS 上为 `AppKit`），因为生成的头文件会使用其中的类型。


## 多个扩展的依赖 {#dependencies-of-several-extensions}

项目中的多个扩展使用 Swift 包时，该平台的全部 `SwiftPackages.json` 文件会合并为单个包依赖图：

* URL 相同的包会合并，请求的产物也会合并。
* 多个扩展共用的包，必须在所有扩展中使用相同的版本要求。如果要求不同，例如一个扩展使用 `"version": "12.16.0"`，另一个使用 `"from": "12.0.0"`，构建会失败并报告 `Conflicting requirements for Swift package` 错误。
* 使用最大的 `minVersion`。
* 所有设置了 `wrapperType` 的扩展必须使用相同的值。

项目也可以混合使用依赖 CocoaPods 和依赖 Swift 包的扩展。两种依赖都会被解析并链接到引擎中。但是，同一个 SDK 不能同时来自两者：如果一个扩展从 `Podfile` 获取 Firebase，另一个从 `SwiftPackages.json` 获取 Firebase，引擎会因重复符号错误而链接失败。共用 SDK 的扩展应使用相同的依赖管理器。


## 锁定包版本 {#locking-package-versions}

构建成功后，构建服务器会返回 `Package.resolved` 文件，列出依赖图中每个包的精确版本和提交，包括包的依赖。该文件位于项目的构建目录，例如 `build/arm64-ios/Package.resolved`。

将此文件复制到扩展中，与 `SwiftPackages.json` 放在一起（例如 `manifests/ios/Package.resolved`），即可锁定包版本。只要锁定的版本符合 `SwiftPackages.json` 中的要求，构建服务器就会使用它们。这也能加快构建：如果没有 `Package.resolved` 文件，构建服务器必须逐步发现包依赖；对依赖较多的包而言，这可能耗费很长时间。

如果多个扩展为同一平台提供了 `Package.resolved` 文件，只会使用其中一个。


## 静态与动态链接 {#static-and-dynamic-linking}

默认情况下，所有 Swift 包会合并为一个静态库，再链接到引擎可执行文件中。

某些 SDK 无法合并为静态库，此时引擎会因重复符号错误而链接失败。遇到这种情况，请在 `SwiftPackages.json` 中设置 `"wrapperType": "dynamic"`。这些包随后会构建为动态框架，并嵌入应用包中。


## 资源与隐私清单 {#resources-and-privacy-manifests}

包的资源包和隐私清单（`PrivacyInfo.xcprivacy`）会以与 CocoaPods 依赖相同的方式包含在应用包中。


## 从 CocoaPods 迁移 {#migrating-from-cocoapods}

许多 SDK 同时以 pod 和 Swift 包的形式发布。将扩展从 `Podfile` 迁移到 `SwiftPackages.json` 文件时：

1. 在 SDK 文档中查找 Swift 包的 git 仓库。它通常与 pod 的仓库相同。
2. 在包的 `Package.swift` 文件中查找产物名称。Pod 名称和产物名称往往不同。
3. 用 `SwiftPackages.json` 文件替换 `Podfile`。将 `Podfile` 中的 `platform :ios` 版本设为 `minVersion`。
4. 确保扩展中的 `#import` 语句仍然匹配这些产物的模块名称。

例如，这个 `Podfile`：

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

会变为这个 `SwiftPackages.json`：

```json
{
  "platform": "ios",
  "minVersion": "12.0",
  "packages": [
    {
      "url": "https://github.com/facebook/facebook-ios-sdk.git",
      "version": "17.0.0",
      "products": ["FacebookCore", "FacebookLogin", "FacebookShare", "FacebookGamingServices"]
    }
  ]
}
```

在这个例子中，模块名称不变，因此 `#import <FBSDKCoreKit/FBSDKCoreKit.h>` 对两种方式都有效。


## 限制 {#limitations}

* 仅支持通过 `https://` 公开可访问的包仓库。不支持 Swift 包注册表。
* 包的 `Package.swift` 文件和插件在构建服务器上运行时无法访问网络。构建服务器会在构建这些包之前，自行下载包和其二进制框架。
* 为 iOS 构建包含资源目录（`.xcassets`）的包，需要使用 Xcode 27 或更高版本的构建服务器。较早的 Xcode 会导致构建失败，并报告包含这些包名称的错误。
* 项目的 `SwiftPackages.json` 文件在每个平台最多可声明 32 个包和 64 个产物。


## 故障排查 {#troubleshooting}

`'Module/Header.h' file not found` 或未定义符号
: 检查 `SwiftPackages.json` 中的 `products` 是否为 `Package.swift` 中的产物名称，以及头文件是否属于其中某个产物。不支持 Swift Package Manager 的构建服务器会忽略 `SwiftPackages.json`，扩展随后也会以相同方式编译或链接失败。

`The Swift package graph did not resolve within the ... time budget`
: 包的依赖太多，无法在没有锁定文件的情况下完成发现。按照[锁定包版本](#locking-package-versions)中的说明，在 `SwiftPackages.json` 旁添加 `Package.resolved` 文件。由于构建未完成，请在本地创建此文件，例如将相同的包添加到 Xcode 项目中。Xcode 将文件存储在 `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`。


## 本地构建服务器 {#local-build-server}

Swift 包由 macOS 构建服务器构建。要通过[本地构建服务器](/manuals/extender-local-setup)使用 Swift 包，需要完整的 Xcode 安装（仅有 Command Line Tools 不够）、[XcodeGen](https://github.com/yonaskolb/XcodeGen)，并通过 `extender.spm.enabled` 设置启用 Swift Package Manager 支持。更多信息请参阅 [GitHub 上的构建服务器文档](https://github.com/defold/extender)。
