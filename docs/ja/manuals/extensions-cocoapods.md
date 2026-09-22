---
title: iOS および macOS ビルドで CocoaPods の依存関係を使用する
brief: このマニュアルでは、CocoaPods を使用して iOS および macOS ビルドの依存関係を解決する方法を説明します。
---

# CocoaPods

[CocoaPods](https://cocoapods.org/) は、Swift および Objective-C の Cocoa プロジェクト向けの依存関係マネージャーです。CocoaPods は通常、Xcode プロジェクトの依存関係を管理し、統合するために使用されます。Defold では iOS および macOS 向けのビルドに Xcode を使用しませんが、ビルドサーバーでの依存関係の解決には Cocoapods を使用します。


## 依存関係の解決 {#resolving-dependencies}

ネイティブ拡張（native extension）では、`manifests/ios` および `manifests/osx` フォルダーに `Podfile` ファイルを含めて、拡張の依存関係を指定できます。例:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

ビルドサーバーは、すべての拡張から `Podfile` ファイルを収集し、それらを使用してすべての依存関係を解決し、ネイティブコードのビルド時に組み込みます。

例:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)
