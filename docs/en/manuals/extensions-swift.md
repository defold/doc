---
title: Using Swift in iOS and macOS native extensions
brief: This manual explains how to write the code of a native extension in Swift for iOS and macOS builds.
---

# Swift in native extensions

Many Apple APIs, such as StoreKit 2 or CryptoKit, are only available from Swift. A native extension can include its own Swift source files next to its Objective-C++ files. The build server compiles them together with the rest of the extension and links the result into the engine. This is separate from [Swift packages](/manuals/extensions-spm) and [CocoaPods](/manuals/extensions-cocoapods), which provide ready-made dependencies.

Swift code is compiled for macOS (`arm64` and `x86_64`) and for iOS (devices and the simulator). Swift files are ignored when building for other platforms.


## Adding Swift sources

Put the `.swift` files in the `src` folder of the extension, next to the C++ and Objective-C++ files:

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Swift files in `commonsrc` or `pluginsrc` are not supported and fail the build.

All Swift files of an extension are compiled together as one Swift module. The name of the module is the `name` from `ext.manifest`, where every character other than a letter, a digit or an underscore is replaced with `_` (`My-Extension` becomes `My_Extension`). The Swift language mode is Swift 5.


## Calling Swift from Objective-C++

The entry point of an extension is still a C++ function registered with `DM_DECLARE_EXTENSION`, so an extension needs at least one `.cpp` or `.mm` file. Swift is called from this file through the generated `<Module>-Swift.h` header.

Only classes, protocols and methods marked with `@objc` are visible from Objective-C. Mark the classes `public` and derive them from `NSObject`:

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

#if defined(DM_PLATFORM_IOS) || defined(DM_PLATFORM_OSX)
#import <Foundation/Foundation.h>
#import "MyExtension-Swift.h"
#endif

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
#if defined(DM_PLATFORM_IOS) || defined(DM_PLATFORM_OSX)
    MyExtensionGreeter* greeter = [[MyExtensionGreeter alloc] init];
    dmLogInfo("%s", [[greeter message] UTF8String]);
#endif
    return dmExtension::RESULT_OK;
}

DM_DECLARE_EXTENSION(MyExtension, "MyExtension", AppInitializeMyExtension, 0, 0, 0, 0, 0)
```

* The generated header imports `Foundation`. Types from other frameworks are only forward declared in it. Import the header of the framework (for example `UIKit`) in the `.mm` file before you call methods that use those types.
* `throws` functions are exposed as methods with an `NSError **` parameter, and `async` functions as methods with a completion handler.
* Swift-only features, such as generics, enums with associated values and structs, are not visible from Objective-C. Wrap them in an `@objc` class.
* Guard the include with `DM_PLATFORM_IOS` or `DM_PLATFORM_OSX`, as the header only exists when building for these platforms.


## Calling Objective-C from Swift

To use Objective-C or C declarations from Swift, add a bridging header named `<Module>-Bridging-Header.h` to the `src` folder, for example `src/MyExtension-Bridging-Header.h`:

```cpp
#import "mynative.h"
```

If the header exists, it is imported into the Swift module automatically. Headers it includes are searched in the `include` folder of the extension and in the folders listed in `additionalSwiftIncludePaths` (see below).

Apple frameworks, such as `Foundation`, `UIKit` or `StoreKit`, are imported from Swift with a normal `import`. The frameworks listed in `frameworks` and `weakFrameworks` of the `ext.manifest` are linked as usual. Most system frameworks are linked automatically when the Swift code imports them.


## Using Swift packages from Swift

The products of the [Swift packages](/manuals/extensions-spm) that the extension declares in `SwiftPackages.json` are available to its Swift code. Import the module in a Swift file:

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

The Objective-C headers of a package can be imported in the bridging header, in the same way as from an `.mm` file:

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

Declare the package in the `SwiftPackages.json` of the extension that uses it. The build server builds the packages first and then the Swift code of the extension. CocoaPods dependencies are not yet available from Swift code, use them from the Objective-C++ file.


## Compiler options

Options for the Swift compiler are set in the `ext.manifest` file, in the same `context` as the options for the C++ compiler:

```yaml
name: MyExtension

platforms:
    ios:
        context:
            defines: ["MY_DEFINE"]
            swiftFlags: ["-strict-concurrency=complete"]
            additionalSwiftIncludePaths: ["vendor/headers"]
            additionalFrameworkSearchPaths: ["vendor/frameworks"]
    osx:
        context:
            defines: ["MY_DEFINE"]
```

* `defines` - The defines set for C++ are passed to Swift as conditional compilation names, so `#if MY_DEFINE` works in Swift. The value of a define, such as `MY_DEFINE=1`, is dropped, as Swift only supports names.
* `swiftFlags` - Additional flags for the Swift compiler. Each flag and each value is a separate list item. The flags are filtered by an allow list, and all other flags fail the build with an `Invalid flag - 'swiftFlags'` error. The allowed flags are:
  * `-enable-upcoming-feature <Feature>` - Enable an upcoming language feature, for example `["-enable-upcoming-feature", "ExistentialAny"]`.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize` and `-Onone` - The optimization level. The default is `-O`.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - Folders that the Swift compiler searches for headers and modules, in addition to the `include` folder of the extension.
* `additionalFrameworkSearchPaths` - Folders that are searched for frameworks, in addition to the `lib/<platform>` folder of the extension. This is not specific to Swift: the folders are used by the Swift compiler, by the C++ and Objective-C++ compiler for the sources of the extension, and by the linker.

The paths are relative to the extension folder, must stay inside of it, and may only contain letters, digits and `._+-/`.

The Swift keys of the `ios` platform apply to both devices and the simulator. A build server that predates Swift support rejects them with a `Manifest context variable unsupported` error, and the project then fails to build until the Defold version and the build server are updated.


## Minimum OS versions

The Swift runtime is not included in the application. It is loaded from the operating system, and the Swift code is built for the minimum iOS and macOS versions the engine supports. Use an `#available` check before calling APIs that are newer than that.


## Limitations

* An extension still needs a C++ or Objective-C++ file with `DM_DECLARE_EXTENSION`. Swift code cannot yet register the extension or call the Defold SDK (`dmsdk`) itself. A build with only `.swift` files fails to link with an undefined symbol error named after the extension.
* Swift code can use [Swift packages](/manuals/extensions-spm), but not CocoaPods dependencies. Use pods from the Objective-C++ file and pass what is needed to the Swift code.
* Only the Swift 5 language mode is supported. C++ interoperability is not enabled.
* Swift sources are supported by Defold versions that include this feature. A build server with an older SDK fails with a `Swift sources are not supported by this Defold SDK version` error.


## Troubleshooting

`no such module 'Name'`
: The module is not a product of a package declared in a `SwiftPackages.json`. Check that `products` lists a product that provides the module, as described in the [Swift Package Manager manual](/manuals/extensions-spm).

`Swift sources are only supported in the 'src' folder`
: Move the `.swift` files into the `src` folder of the extension.

`'MyExtension-Swift.h' file not found`
: The module name is built from `name` in `ext.manifest`. Check the name in the `#import` line, and that the class is marked `public` and `@objc`.

`Undefined symbols ... _MyExtension`
: The extension has no `DM_DECLARE_EXTENSION`. Add a `.mm` file that registers the extension as described above.

`Invalid flag - 'swiftFlags'`
: The flag is not on the allow list. Remove it or use one of the listed flags.
