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

Keep all Swift files in `src`. A macOS or iOS build fails if it finds a Swift file in `commonsrc` or `pluginsrc`.

All Swift files of an extension are compiled together as one Swift module. The name of the module is the `name` from `ext.manifest`, where every character other than a letter, a digit or an underscore is replaced with `_` (`My-Extension` becomes `My_Extension`). The Swift language mode is Swift 5.

The name of the module must differ from the modules that the code imports. An extension named `StoreKit` can't `import StoreKit`, as the compiler takes the import for the module itself.


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

* The generated header imports `Foundation`. Types from other frameworks are only forward declared in it. Import the header of the framework (for example `UIKit`) in the `.mm` file before you call methods that use those types.
* `throws` functions are exposed as methods with an `NSError **` parameter, and `async` functions as methods with a completion handler.
* Swift-only features, such as generics, enums with associated values and structs, are not visible from Objective-C. Wrap them in an `@objc` class.
* `.mm` files are only compiled for iOS and macOS, so an extension with only `.mm` and `.swift` files fails on other platforms with `Extension has no source!`. To also build the extension for other platforms, put `DM_DECLARE_EXTENSION` in a `.cpp` file and call the `.mm` file from it inside a `DM_PLATFORM_IOS` or `DM_PLATFORM_OSX` guard.


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

Declare the package in the `SwiftPackages.json` of the extension that uses it. The build server builds the packages first and then the Swift code of the extension. If a package needs a newer OS than the minimum version of the engine, set it as `minVersion` in the `SwiftPackages.json`, and the Swift code of the extension is built for that version too. Using CocoaPods dependencies from Swift code is not supported. Use them from the Objective-C++ file and pass what is needed to the Swift code.


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
* `swiftFlags` - Additional flags for the Swift compiler. Each flag and each value is a separate list item. The flags are filtered by an allow list, and all other flags fail the build with an `Invalid flag - 'swiftFlags'` error. A value with whitespace, a backslash or template syntax, or one that names a response file, fails with an `invalid 'swiftFlags' value` error instead. The allowed flags are:
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

The Swift runtime is part of every iOS and macOS version that Defold supports. The Swift code is built for the minimum iOS or macOS version of the build, and the application uses the Swift runtime of the operating system. Use an `#available` check before calling APIs that are newer than the minimum version.

A few parts of the runtime are part of the operating system only from a later version. For example, `MutableSpan` and related types are part of iOS 26 and macOS 26. If the minimum version is older and your Swift code or a dynamic framework of a package uses such a feature, the application may need an extra library to run on those devices. You don't have to do anything for this: the build server finds the libraries that the engine and the dynamic libraries embedded with it use, as Xcode does, and adds them to the application. On iOS they are placed in the `Frameworks` folder of the application and are signed together with the rest of its code.

The minimum version of a build is the one that the engine supports, which is set by the Defold version and the build server. A `minVersion` in a `SwiftPackages.json` raises it for the packages, the Swift code and the link of the engine, as described in the [Swift Package Manager manual](/manuals/extensions-spm). It can't be lowered.


## Limitations

* An extension still needs a C++ or Objective-C++ file with `DM_DECLARE_EXTENSION`. Swift code cannot yet register the extension or call the Defold SDK (`dmsdk`) itself. A build with only `.swift` files fails to link with an undefined symbol error named after the extension.
* Using CocoaPods dependencies from Swift code is not supported. Use them from the Objective-C++ file and pass what is needed to the Swift code.
* A target of a Swift package with its own `module.modulemap` can't be imported from Swift code, and neither can a Swift target that depends on one. The build fails with a `no such module` or `missing required module` error.
* Only the Swift 5 language mode is supported. C++ interoperability is not enabled.
* Swift sources are supported by Defold versions that include this feature. A build server with an older SDK fails with a `Swift sources are not supported by this Defold SDK version` error.
* Swift sources are not compiled when building the `library` artifact (`--build-artifacts library` in [Bob](/manuals/bob)), so an Objective-C++ file that imports `<Module>-Swift.h` fails to compile there.


## Troubleshooting

`no such module 'Name'`
: The module is not a product of a package declared in a `SwiftPackages.json`. Check that `products` lists a product that provides the module, as described in the [Swift Package Manager manual](/manuals/extensions-spm). A target with its own `module.modulemap` also gives this error, as listed in the limitations above.

`Swift sources are only supported in the 'src' folder`
: Move the `.swift` files into the `src` folder of the extension.

`'MyExtension-Swift.h' file not found`
: The module name is built from `name` in `ext.manifest`. Check the name in the `#import` line.

`unknown type name 'MyExtensionGreeter'`
: The class is missing from the generated header. Check that it is marked `public` and `@objc`, derives from `NSObject`, and that the `.mm` file uses the name from `@objc(...)`.

`cannot find 'AppStore' in scope` together with `file 'A.swift' is part of module 'StoreKit'; ignoring import`
: The extension has the same name as a module it imports. Rename the extension in `ext.manifest`.

`Undefined symbols ... _MyExtension`
: The extension has no `DM_DECLARE_EXTENSION`. Add a `.mm` file that registers the extension as described above.

`Invalid flag - 'swiftFlags'`
: The flag is not on the allow list. Remove it or use one of the listed flags.

`invalid 'swiftFlags' value`
: The value has whitespace, a backslash or template syntax, or names a response file. Put each flag and each value in its own list item.
