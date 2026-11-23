---
title: 在 iOS 和 macOS 原生扩展中使用 Swift
brief: 本手册说明如何用 Swift 为 iOS 和 macOS 编写原生扩展代码。
---

# 在原生扩展中使用 Swift {#swift-in-native-extensions}

许多 Apple API（如 StoreKit 2 和 CryptoKit）只能在 Swift 中使用。原生扩展可以把自己的 Swift 源文件与 Objective-C++ 文件放在一起。构建服务器会将这些文件与扩展的其余代码一起编译，再将结果链接到引擎中。扩展也可以通过 [Swift 包](/manuals/extensions-spm)和 [CocoaPods](/manuals/extensions-cocoapods)引入现成的依赖，这与编译扩展自身的 Swift 源文件是两种独立的机制。

为 macOS（`arm64` 和 `x86_64`）以及 iOS（真机和模拟器）构建时，构建服务器会编译 Swift 代码。为其他平台构建时，服务器会忽略 Swift 文件。


## 添加 Swift 源文件 {#adding-swift-sources}

将 `.swift` 文件放在扩展的 `src` 文件夹中，与 C++ 和 Objective-C++ 文件放在一起。

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

所有 Swift 文件都必须放在 `src` 中。如果在 `commonsrc` 或 `pluginsrc` 中发现 Swift 文件，macOS 或 iOS 构建就会失败。

扩展的所有 Swift 文件会一起编译成一个 Swift 模块。模块名称取自 `ext.manifest` 中的 `name`，其中除了字母、数字和下划线以外，每个字符都会被替换为 `_`（例如 `My-Extension` 会变成 `My_Extension`）。编译时使用 Swift 5 语言模式。

模块不能与代码导入的模块同名。例如，名为 `StoreKit` 的扩展不能使用 `import StoreKit`，因为编译器会将其视为导入模块自身。


## 从 Objective-C++ 调用 Swift {#calling-swift-from-objective-c}

扩展的入口点仍是通过 `DM_DECLARE_EXTENSION` 注册的 C++ 函数，因此扩展至少需要一个 `.cpp` 或 `.mm` 文件。在该文件中，可以通过自动生成的 `<Module>-Swift.h` 头文件调用 Swift 代码。

Objective-C 只能访问标记为 `@objc` 的类、协议和方法。请将类声明为 `public`，并让它继承 `NSObject`。

`src/Greeter.swift`:

```swift
import Foundation

@objc(MyExtensionGreeter)
public class Greeter: NSObject {
    @objc public func message() -> String {
        return "Hello from Swift"
    }
}
```

`src/myextension.mm`:

```cpp
#include <dmsdk/sdk.h>
#import <Foundation/Foundation.h>
#import "MyExtension-Swift.h"

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    MyExtensionGreeter* greeter = [[MyExtensionGreeter alloc] init];
    dmLogInfo("%s", [[greeter message] UTF8String]);
    return dmExtension::RESULT_OK;
}

DM_DECLARE_EXTENSION(MyExtension, "MyExtension", AppInitializeMyExtension, 0, 0, 0, 0, 0)
```

* 生成的头文件会导入 `Foundation`。对于其他框架的类型，该头文件只提供前向声明。在调用使用这些类型的方法之前，请在 `.mm` 文件中导入相应框架（如 `UIKit`）的头文件。
* 在 Objective-C 中，`throws` 函数对应带有 `NSError **` 参数的方法，`async` 函数对应带有完成回调的方法。
* Objective-C 无法访问 Swift 特有的功能，如泛型、带关联值的枚举和结构体。可以将它们封装在标记为 `@objc` 的类中。
* 只有为 iOS 和 macOS 构建时才会编译 `.mm` 文件。因此，如果扩展只有 `.mm` 和 `.swift` 文件，为其他平台构建时就会失败并报告 `Extension has no source!` 错误。要让扩展也能为其他平台构建，请将 `DM_DECLARE_EXTENSION` 放在 `.cpp` 文件中，并在该文件中使用 `DM_PLATFORM_IOS` 或 `DM_PLATFORM_OSX` 判断目标平台，仅在对应平台上调用 `.mm` 文件中的代码。


## 从 Swift 调用 Objective-C {#calling-objective-c-from-swift}

要在 Swift 中使用 Objective-C 或 C 声明，请在 `src` 文件夹中添加名为 `<Module>-Bridging-Header.h` 的桥接头文件，例如 `src/MyExtension-Bridging-Header.h`。

```cpp
#import "mynative.h"
```

如果桥接头文件存在，构建时会自动将它导入 Swift 模块。编译器会在扩展的 `include` 文件夹和 `additionalSwiftIncludePaths` 列出的文件夹中查找它所包含的头文件（见下文）。

在 Swift 中，可以使用普通的 `import` 语句导入 Apple 框架，如 `Foundation`、`UIKit` 或 `StoreKit`。构建时会照常链接 `ext.manifest` 的 `frameworks` 和 `weakFrameworks` 中列出的框架。大多数系统框架只要在 Swift 代码中导入就会自动链接。


## 在 Swift 中使用 Swift 包 {#using-swift-packages-from-swift}

扩展可以在 Swift 代码中使用其 `SwiftPackages.json` 所声明的 [Swift 包](/manuals/extensions-spm)的产物。在 Swift 文件中导入相应的模块即可。

```swift
import Foundation
import Sentry

@objc(MyExtensionCrashReporter)
public class CrashReporter: NSObject {
    @objc public func start(dsn: String) {
        SentrySDK.start { options in
            options.dsn = dsn
        }
    }
}
```

可以在桥接头文件中导入包的 Objective-C 头文件，方式与在 `.mm` 文件中导入相同。

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

请在扩展自己的 `SwiftPackages.json` 中声明它使用的包。构建服务器先构建包，再编译扩展的 Swift 代码。如果包要求的操作系统版本高于引擎支持的最低版本，请将包要求的版本写入 `SwiftPackages.json` 的 `minVersion`。这样，扩展的 Swift 代码也会以该版本为目标进行编译。Swift 代码不支持直接使用 CocoaPods 依赖。请在 Objective-C++ 文件中使用这些依赖，再将所需内容传给 Swift 代码。


## 编译器选项 {#compiler-options}

在 `ext.manifest` 文件中，将 Swift 编译器选项与 C++ 编译器选项写在同一个 `context` 下。

```yaml
name: MyExtension

platforms:
    ios:
        context:
            defines: ["MY_DEFINE"]
            swiftFlags: ["-strict-concurrency=complete"]
            additionalSwiftIncludePaths: ["include/vendor/headers"]
            additionalFrameworkSearchPaths: ["lib/ios/vendor/frameworks"]
    osx:
        context:
            defines: ["MY_DEFINE"]
```

* `defines` - 为 C++ 设置的宏定义会以条件编译标识符的形式传给 Swift，因此可以在 Swift 中使用 `#if MY_DEFINE`。Swift 只支持名称，像 `MY_DEFINE=1` 这样的定义只会保留名称，其值会被丢弃。
* `swiftFlags` - 传递给 Swift 编译器的额外标志。每个标志和每个值都必须单独作为一个列表项。标志按白名单过滤，如果使用了未列出的标志，构建会失败并报告 `Invalid flag - 'swiftFlags'` 错误。如果值包含空白字符、反斜杠或模板语法，或者指定了响应文件，则会报告 `invalid 'swiftFlags' value` 错误。允许使用以下标志。
  * `-enable-upcoming-feature <Feature>` - 启用即将推出的语言特性，例如 `["-enable-upcoming-feature", "ExistentialAny"]`。
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`、`-Osize` 和 `-Onone` - 设置优化级别。默认值为 `-O`。
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - 除了扩展的 `include` 文件夹，Swift 编译器还会在这些文件夹中查找头文件和模块。
* `additionalFrameworkSearchPaths` - 除了扩展的 `lib/<platform>` 文件夹，构建时还会在这些文件夹中查找框架。Swift 编译器、编译扩展源文件的 C++ 和 Objective-C++ 编译器，以及链接器都会使用这些路径。

这些路径相对于扩展目录，必须指向该目录内的位置，并且只能包含字母、数字和 `._+-/` 中的字符。构建时只会将扩展的 `include`、`src`、`commonsrc`、`pluginsrc`、`lib/<platform>`、`manifests/<platform>` 和 `res/<platform>` 文件夹发送到构建服务器，因此路径必须指向其中一个文件夹内的位置。其他文件夹（例如扩展根目录下的 `vendor` 文件夹）中的文件在构建时不可用。

`ios` 平台的 Swift 配置键同时适用于真机和模拟器。尚不支持 Swift 的旧版构建服务器会拒绝这些键，并报告 `Manifest context variable unsupported` 错误。此时项目会构建失败，更新 Defold 和构建服务器后才能构建。


## 最低操作系统版本 {#minimum-os-versions}

Defold 支持的每个 iOS 和 macOS 版本都包含 Swift 运行时。编译 Swift 代码时，会以本次构建指定的最低 iOS 或 macOS 版本为目标，应用运行时使用操作系统自带的 Swift 运行时。调用最低版本之后才引入的 API 之前，请使用 `#available` 检查其可用性。

运行时的少数组件从较新的操作系统版本起才随系统提供。例如，从 iOS 26 和 macOS 26 起，系统才自带 `MutableSpan` 及相关类型。如果最低版本较早，而扩展的 Swift 代码或某个包的动态框架用到了这类功能，应用在旧系统设备上运行时可能需要额外的库。无需手动添加这些库。构建服务器会像 Xcode 一样，找出引擎及其随附的动态库所依赖的库，并将它们添加到应用中。在 iOS 上，这些库会放入应用的 `Frameworks` 文件夹，并与应用的其余代码一起签名。

构建采用引擎支持的最低系统版本，该版本由 Defold 版本和构建服务器决定。如 [Swift Package Manager 手册](/manuals/extensions-spm)所述，在 `SwiftPackages.json` 中设置 `minVersion` 可以提高构建包、编译 Swift 代码和链接引擎时采用的最低版本。此设置不能降低最低版本。


## 限制 {#limitations}

* 扩展仍然需要一个包含 `DM_DECLARE_EXTENSION` 的 C++ 或 Objective-C++ 文件。Swift 代码无法注册扩展，也无法调用 Defold SDK（`dmsdk`）的 C++ API，请在 Objective-C++ 文件中调用该 API。桥接头文件可以包含与 C 兼容的 `dmsdk` 头文件，例如 `dmsdk/dlib/hash.h`。如果扩展只有 `.swift` 文件，链接就会失败，并报告一个与扩展同名的未定义符号。
* Swift 代码不支持直接使用 CocoaPods 依赖。请在 Objective-C++ 文件中使用这些依赖，再将所需内容传给 Swift 代码。
* 仅支持 Swift 5 语言模式。未启用与 C++ 的互操作。
* 从 Defold 1.14.2 起支持 Swift 源文件。如果构建服务器使用更早版本的 SDK，构建会失败并报告 `Swift sources are not supported by this Defold SDK version` 错误。
* 构建 `library` 产物时（在 [Bob](/manuals/bob) 中使用 `--build-artifacts library`），不会编译 Swift 源文件，因此导入 `<Module>-Swift.h` 的 Objective-C++ 文件会编译失败。


## 故障排查 {#troubleshooting}

`no such module 'Name'`
: `SwiftPackages.json` 中声明的包都没有提供该模块。请按 [Swift Package Manager 手册](/manuals/extensions-spm)中的说明，检查 `products` 是否列出了提供该模块的产物。

`Swift sources are only supported in the 'src' folder`
: 将 `.swift` 文件移到扩展的 `src` 文件夹中。

`'MyExtension-Swift.h' file not found`
: 模块名称取自 `ext.manifest` 中的 `name`。请检查 `#import` 行中的名称。

`unknown type name 'MyExtensionGreeter'`
: 生成的头文件中没有这个类。请确认该类标记为 `public` 和 `@objc`，继承自 `NSObject`，并检查 `.mm` 文件是否使用了 `@objc(...)` 中的名称。

`cannot find 'AppStore' in scope` 和 `file 'A.swift' is part of module 'StoreKit'; ignoring import` 同时出现
: 扩展与它导入的一个模块同名。请在 `ext.manifest` 中重命名扩展。

`Undefined symbols ... _MyExtension`
: 扩展缺少 `DM_DECLARE_EXTENSION`。请按上文所述，添加一个用于注册扩展的 `.mm` 文件。

`Invalid flag - 'swiftFlags'`
: 该标志不在白名单中。请移除它或改用列出的标志。

`invalid 'swiftFlags' value`
: 值中包含空白字符、反斜杠或模板语法，或者该值指定了响应文件。请将每个标志和每个值分别写成独立的列表项。
