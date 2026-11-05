---
title: iOS と macOS のビルドで Swift Package Manager の依存関係を使う
brief: このマニュアルでは、Swift Package Manager を使って iOS と macOS のビルドの依存関係を解決する方法を説明します。
---

# Swift Package Manager {#swift-package-manager}

[Swift Package Manager](https://www.swift.org/documentation/package-manager/) は、Swift と Xcode に組み込まれた依存関係マネージャーです。多くの iOS および macOS の SDK が Swift パッケージとして配布されており、CocoaPods では公開されなくなったものもあります。Defold はエンジンのビルドに Xcode を使いませんが、ビルドサーバーは Xcode を使って、拡張が依存する Swift パッケージをダウンロードしてビルドします。その結果は、[CocoaPods の依存関係](/manuals/extensions-cocoapods)と同じ方法でエンジンにリンクします。

CocoaPods と Swift パッケージは、同じプロジェクト内、さらには同じ拡張内でも併用できます。


## 依存関係の宣言 {#declaring-dependencies}

ネイティブ拡張では、`manifests/ios` と `manifests/osx` フォルダーに `SwiftPackages.json` ファイルを含め、拡張が依存する Swift パッケージを指定できます。例:

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

ファイルは通常の JSON です。`Package.swift` を自分で書く必要はありません。すべての拡張の `SwiftPackages.json` ファイルから、ビルドサーバーが生成します。

ファイルには、次のフィールドがあります。

* `platform` - 必須です。`manifests/ios/SwiftPackages.json` では `"ios"`、`manifests/osx/SwiftPackages.json` では `"osx"` を指定します。
* `minVersion` - 任意です。パッケージのビルド対象となる iOS または macOS の最小バージョンです。例: `"15.0"`。すべての拡張の値とエンジンがサポートする最小バージョンのうち、最も高い値を、パッケージのビルドとエンジンのリンクの両方で使います。
* `wrapperType` - 任意です。`"static"`（デフォルト）または `"dynamic"` を指定します。後述の[静的リンクと動的リンク](#static-and-dynamic-linking)を参照してください。
* `packages` - 必須です。パッケージのリストです。各パッケージには、次のフィールドがあります。
  * `url` - パッケージの git リポジトリの `https://` URL です。認証情報、独自のポート、クエリー文字列を含む URL や、`ssh` URL は受け付けないため、リポジトリは公開アクセスできる必要があります。
  * `products` - エンジンにリンクするパッケージのプロダクトです。パッケージの `Package.swift` の `products` セクションにあるライブラリプロダクトを指定します。プロダクト名は、パッケージ名やインポートするモジュール名と同じとは限りません。
  * バージョン要件を次からちょうど1つ指定します。
    * `version` - 指定したバージョンそのものです。例: `"12.16.0"`。
    * `from` - 指定したバージョン以降で、メジャーバージョンが同じものです。たとえば `"9.0.0"` は最新の `9.x.x` リリースに解決されます。
    * `branch` - ブランチの最新コミットです。例: `"main"`。
    * `revision` - 40文字の完全なコミットハッシュで指定する、特定のコミットです。

ビルドサーバーは、すべての拡張から `SwiftPackages.json` ファイルを集め、パッケージ自体の依存関係を含むすべての依存関係を解決し、ネイティブコードのビルド時に含めます。


## 拡張のコードからパッケージを使う {#using-packages-from-extension-code}

プロダクトのヘッダーは、拡張のソースコードから利用できます。Objective-C++（`.mm`）ソースファイルから使います。次の例は、アプリケーションの起動時に [Sentry](https://github.com/getsentry/sentry-cocoa) SDK を起動します。

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

* Objective-C のヘッダーは `#import <Module/Header.h>` としてインポートします。`Module` は、そのヘッダーを提供するモジュールの名前です。
* Swift で実装したクラスは、生成される `<Module/Module-Swift.h>` ヘッダーで宣言されます。このヘッダーに含まれるのは、モジュールが Objective-C に公開するクラスとメソッド（Swift で `@objc` が付いたもの）のみです。生成されたヘッダーはそれらの型を使うため、その前に `UIKit`（macOS では `AppKit`）をインポートします。


## 複数の拡張の依存関係 {#dependencies-of-several-extensions}

プロジェクト内の複数の拡張が Swift パッケージを使う場合、そのプラットフォームのすべての `SwiftPackages.json` ファイルを、単一のパッケージグラフにまとめます。

* 同じ URL のパッケージは統合され、要求されたプロダクトもまとめられます。
* 複数の拡張で共有するパッケージは、すべてで同じバージョン要件を指定する必要があります。たとえば一方で `"version": "12.16.0"`、他方で `"from": "12.0.0"` のように要件が異なると、`Conflicting requirements for Swift package` エラーでビルドに失敗します。
* 最も高い `minVersion` を使います。
* `wrapperType` を設定するすべての拡張は、同じ値を指定する必要があります。

プロジェクトには、CocoaPods を使う拡張と Swift パッケージを使う拡張を混在させることもできます。どちらも依存関係を解決し、エンジンにリンクします。ただし、同じ SDK を両方から取得してはいけません。一方の拡張が `Podfile` から Firebase を取得し、もう一方が `SwiftPackages.json` から取得すると、重複シンボルのエラーでエンジンのリンクに失敗します。SDK を共有する拡張は、同じ依存関係マネージャーを使ってください。


## パッケージのバージョンの固定 {#locking-package-versions}

ビルドが成功すると、ビルドサーバーは、パッケージの依存関係を含むグラフ内のすべてのパッケージの正確なバージョンとコミットを列挙した `Package.resolved` ファイルを返します。これは、`build/arm64-ios/Package.resolved` など、プロジェクトのビルドフォルダーに配置されます。

パッケージのバージョンを固定するには、このファイルを拡張内の `SwiftPackages.json` の隣にコピーします（例: `manifests/ios/Package.resolved`）。以降、ビルドサーバーは `SwiftPackages.json` の要件を満たす限り、固定されたバージョンを使います。ビルドも速くなります。`Package.resolved` がない場合、ビルドサーバーはパッケージの依存関係を段階的に検出するため、依存関係の多いパッケージでは長い時間がかかる場合があります。

複数の拡張が同じプラットフォームの `Package.resolved` を含む場合、使われるのはそのうち1つだけです。


## 静的リンクと動的リンク {#static-and-dynamic-linking}

デフォルトでは、すべての Swift パッケージを単一の静的ライブラリにまとめ、エンジンの実行ファイルにリンクします。

一部の SDK は静的ライブラリにまとめられず、重複シンボルのエラーでエンジンのリンクに失敗します。この場合は、`SwiftPackages.json` で `"wrapperType": "dynamic"` を設定します。パッケージは動的フレームワークとしてビルドされ、アプリケーションバンドルに埋め込まれます。


## リソースとプライバシーマニフェスト {#resources-and-privacy-manifests}

パッケージのリソースバンドルとプライバシーマニフェスト（`PrivacyInfo.xcprivacy`）は、CocoaPods の依存関係と同じ方法でアプリケーションバンドルに含まれます。


## CocoaPods からの移行 {#migrating-from-cocoapods}

多くの SDK は、pod と Swift パッケージの両方で公開されています。拡張を `Podfile` から `SwiftPackages.json` に移行するには、次のようにします。

1. SDK のドキュメントで Swift パッケージの git リポジトリを探します。pod と同じリポジトリである場合が多いです。
2. パッケージの `Package.swift` でプロダクト名を確認します。pod 名とプロダクト名は異なる場合が多いです。
3. `Podfile` を `SwiftPackages.json` に置き換えます。`Podfile` の `platform :ios` のバージョンは `minVersion` になります。
4. 拡張の `#import` 行が、引き続きプロダクトのモジュール名と一致していることを確認します。

たとえば、次の `Podfile` は:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

次の `SwiftPackages.json` になります。

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

この場合、モジュール名は変わらないため、`#import <FBSDKCoreKit/FBSDKCoreKit.h>` はどちらでも動作します。


## 制限 {#limitations}

* `https://` で公開アクセスできるパッケージリポジトリのみをサポートします。Swift パッケージレジストリには対応しません。
* パッケージの `Package.swift` ファイルとプラグインは、ビルドサーバー上でネットワークアクセスなしで実行されます。パッケージをビルドする前に、ビルドサーバー自身がパッケージとそのバイナリフレームワークをダウンロードします。
* アセットカタログ（`.xcassets`）を含むパッケージを iOS 向けにビルドするには、Xcode 27 以降を使用するビルドサーバーが必要です。それ以前の Xcode では、該当するパッケージ名を示すエラーでビルドに失敗します。
* プロジェクトの `SwiftPackages.json` ファイルで宣言できるのは、プラットフォームごとに最大32パッケージ、64プロダクトです。


## トラブルシューティング {#troubleshooting}

`'Module/Header.h' file not found` または未定義シンボル
: `SwiftPackages.json` の `products` が `Package.swift` のプロダクト名であり、そのいずれかにヘッダーが属することを確認します。Swift Package Manager に対応しないビルドサーバーは `SwiftPackages.json` を無視するため、同じように拡張のコンパイルやリンクに失敗します。

`The Swift package graph did not resolve within the ... time budget`
: ロックファイルなしで検出するには、パッケージの依存関係が多すぎます。[パッケージのバージョンの固定](#locking-package-versions)に従い、`SwiftPackages.json` の隣に `Package.resolved` を追加します。ビルドが完了していないため、たとえば同じパッケージを Xcode プロジェクトに追加し、ローカルでファイルを作成します。Xcode は `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved` に保存します。


## ローカルビルドサーバー {#local-build-server}

Swift パッケージは macOS のビルドサーバーでビルドします。[ローカルビルドサーバー](/manuals/extender-local-setup)で使うには、完全な Xcode のインストール（Command Line Tools だけでは不十分です）、[XcodeGen](https://github.com/yonaskolb/XcodeGen)、および `extender.spm.enabled` 設定による Swift Package Manager サポートの有効化が必要です。詳細は [GitHub のビルドサーバードキュメント](https://github.com/defold/extender)を参照してください。
