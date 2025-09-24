---
title: 在 iOS 和 macOS 构建中使用 CocoaPods 依赖
brief: 本手册介绍了如何在 iOS 和 macOS 构建中使用 CocoaPods 解析依赖。
---

# CocoaPods

[CocoaPods](https://cocoapods.org/) 是 Swift 和 Objective-C Cocoa 项目的依赖管理器。CocoaPods 通常用于管理和集成 Xcode 项目中的依赖。Defold 在为 iOS 和 macOS 构建时不使用 Xcode，但它仍然使用 Cocoapods 在构建服务器上解析依赖。

## 解析依赖

原生扩展可以在 `manifests/ios` 和 `manifests/osx` 文件夹中包含 `Podfile` 文件来指定扩展依赖。例如：

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

构建服务器将收集所有扩展中的 `Podfile` 文件，并使用这些文件解析所有依赖，并在构建原生代码时包含它们。

示例：

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)