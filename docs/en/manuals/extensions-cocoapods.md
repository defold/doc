---
title: Using CocoaPods dependencies in iOS and macOS builds
brief: This manual explains how to use CocoaPods to resolve dependencies in iOS and macOS builds.
---

# CocoaPods

[CocoaPods](https://cocoapods.org/) is a dependency manager for Swift and Objective-C Cocoa projects. CocoaPods is typically used to manage and integrate dependencies in Xcode projects. Defold does not use Xcode when building for iOS and macOS, but it still uses Cocoapods to resolve dependencies on the build server.


## Resolving dependencies

Native extensions can include a `Podfile` file in the `manifests/ios` and `manifests/osx` folders to specify the extension dependencies. Example:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

The build server will collect the `Podfile` files from all the extensions and use these to resolve all dependencies and include them when building the native code.

Examples:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)