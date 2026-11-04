---
title: Using Swift Package Manager dependencies in iOS and macOS builds
brief: This manual explains how to use Swift Package Manager to resolve dependencies in iOS and macOS builds.
---

# Swift Package Manager

[Swift Package Manager](https://www.swift.org/documentation/package-manager/) is the dependency manager built into Swift and Xcode. Many iOS and macOS SDKs are distributed as Swift packages, and some of them are no longer published as CocoaPods. Defold does not use Xcode when building the engine, but the build server uses Xcode to download and build the Swift packages an extension depends on. The result is then linked into the engine the same way as [CocoaPods dependencies](/manuals/extensions-cocoapods).

CocoaPods and Swift packages can be used in the same project, and even in the same extension.


## Declaring dependencies

Native extensions can include a `SwiftPackages.json` file in the `manifests/ios` and `manifests/osx` folders to specify the Swift packages the extension depends on. Example:

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

The file is plain JSON. You do not write a `Package.swift` file yourself, the build server generates one from the `SwiftPackages.json` files of all extensions.

The file contains the following fields:

* `platform` - Required. `"ios"` in `manifests/ios/SwiftPackages.json` and `"osx"` in `manifests/osx/SwiftPackages.json`.
* `minVersion` - Optional. The minimum iOS or macOS version the packages are built for, for example `"15.0"`. The highest value of all extensions and the minimum version supported by the engine is used, both when building the packages and when linking the engine.
* `wrapperType` - Optional. `"static"` (default) or `"dynamic"`. See [Static and dynamic linking](#static-and-dynamic-linking) below.
* `packages` - Required. A list of packages. Each package has the following fields:
  * `url` - The `https://` URL of the git repository of the package. URLs with credentials, a custom port or a query string, as well as `ssh` URLs, are not accepted, so the repository must be publicly accessible.
  * `products` - The products of the package to link with the engine. These are the library products listed in the `products` section of the `Package.swift` file of the package. A product name is not necessarily the same as the name of the package or the name of the module you import.
  * Exactly one version requirement:
    * `version` - This exact version, for example `"12.16.0"`.
    * `from` - This version or any later version with the same major version. For example `"9.0.0"` resolves to the latest `9.x.x` release.
    * `branch` - The latest commit on a branch, for example `"main"`.
    * `revision` - A specific commit, given as the full 40 character commit hash.

The build server collects the `SwiftPackages.json` files from all the extensions and uses these to resolve all dependencies, including the dependencies of the packages themselves, and includes them when building the native code.


## Using packages from extension code

The headers of the products are available to the source code of the extension. Use them from Objective-C++ (`.mm`) source files. This example starts the [Sentry](https://github.com/getsentry/sentry-cocoa) SDK when the application starts:

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

* Objective-C headers are imported as `#import <Module/Header.h>`, where `Module` is the name of the module that provides them.
* Classes implemented in Swift are declared in the generated `<Module/Module-Swift.h>` header. It only contains the classes and methods that the module exposes to Objective-C (marked with `@objc` in Swift). Import `UIKit` (or `AppKit` on macOS) before it, since the generated header uses their types.


## Dependencies of several extensions

When several extensions in a project use Swift packages, all their `SwiftPackages.json` files for the platform are combined into a single package graph:

* Packages with the same URL are merged, and the requested products are combined.
* A package shared by several extensions must have the same version requirement in all of them. Different requirements, for example `"version": "12.16.0"` in one extension and `"from": "12.0.0"` in another, fail the build with a `Conflicting requirements for Swift package` error.
* The highest `minVersion` is used.
* All extensions that set `wrapperType` must set the same value.

A project can also mix extensions using CocoaPods and extensions using Swift packages. Both are resolved and linked with the engine. The same SDK must however not come from both: if one extension gets Firebase from a `Podfile` and another one from a `SwiftPackages.json`, the engine fails to link with duplicate symbol errors. Extensions that share an SDK should use the same dependency manager.


## Locking package versions

When the build succeeds, the build server returns a `Package.resolved` file listing the exact version and commit of every package in the graph, including the dependencies of the packages. It is placed in the build folder of the project, for example `build/arm64-ios/Package.resolved`.

Copy this file into the extension, next to `SwiftPackages.json` (for example `manifests/ios/Package.resolved`), to lock the package versions. The build server then uses the locked versions as long as they match the requirements in `SwiftPackages.json`. It also makes the build faster: without a `Package.resolved` file the build server discovers the dependencies of the packages step by step, which can take a long time for packages with many dependencies.

If several extensions include a `Package.resolved` file for the same platform, only one of them is used.


## Static and dynamic linking

By default all Swift packages are combined into one static library which is linked into the engine executable.

Some SDKs cannot be combined into a static library, and the engine then fails to link with duplicate symbol errors. In this case set `"wrapperType": "dynamic"` in `SwiftPackages.json`. The packages are then built into a dynamic framework, which is embedded in the application bundle.


## Resources and privacy manifests

Resource bundles and privacy manifests (`PrivacyInfo.xcprivacy`) of the packages are included in the application bundle in the same way as for CocoaPods dependencies.


## Migrating from CocoaPods

Many SDKs are published both as a pod and as a Swift package. To move an extension from a `Podfile` to a `SwiftPackages.json` file:

1. Find the git repository of the Swift package in the documentation of the SDK. It is often the same repository as the pod.
2. Find the product names in the `Package.swift` file of the package. Pod names and product names are often different.
3. Replace the `Podfile` with a `SwiftPackages.json` file. The `platform :ios` version of the `Podfile` becomes `minVersion`.
4. Make sure the `#import` lines of the extension still match the module names of the products.

For example, this `Podfile`:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

becomes this `SwiftPackages.json`:

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

In this case the modules keep their names, so `#import <FBSDKCoreKit/FBSDKCoreKit.h>` works with both.


## Limitations

* Only package repositories that are publicly accessible over `https://` are supported. Swift package registries are not supported.
* The `Package.swift` files and plugins of the packages run without network access on the build server. The build server downloads the packages and their binary frameworks itself before the packages are built.
* Building packages that contain asset catalogs (`.xcassets`) for iOS requires a build server that uses Xcode 27 or later. With an earlier version of Xcode the build fails with an error that names these packages.
* The `SwiftPackages.json` files of a project can declare at most 32 packages and 64 products per platform.


## Troubleshooting

`'Module/Header.h' file not found` or undefined symbols
: Check that the `products` in `SwiftPackages.json` are product names from `Package.swift` and that the header belongs to one of them. A build server that does not support Swift Package Manager ignores `SwiftPackages.json`, and the extension then fails to compile or link in the same way.

`The Swift package graph did not resolve within the ... time budget`
: The packages have too many dependencies to be discovered without a lock file. Add a `Package.resolved` file next to `SwiftPackages.json` as described in [Locking package versions](#locking-package-versions). Since the build did not complete, create the file locally, for example by adding the same packages to an Xcode project. Xcode stores the file in `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`.


## Local build server

Swift packages are built by the macOS build server. To use Swift packages with a [local build server](/manuals/extender-local-setup), it needs a full Xcode installation (the Command Line Tools alone are not enough), [XcodeGen](https://github.com/yonaskolb/XcodeGen), and Swift Package Manager support enabled with the `extender.spm.enabled` setting. Refer to the [build server documentation on GitHub](https://github.com/defold/extender) for more information.
