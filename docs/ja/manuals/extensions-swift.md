---
title: iOS と macOS のネイティブ拡張で Swift を使う
brief: このマニュアルでは、iOS および macOS 向けのネイティブ拡張のコードを Swift で書く方法を説明します。
---

# ネイティブ拡張で Swift を使う {#swift-in-native-extensions}

StoreKit 2 や CryptoKit など、Apple の API には Swift からしか使えないものが数多くあります。ネイティブ拡張（native extension）には、Objective-C++ ファイルと一緒に、独自の Swift ソースファイルを含めることができます。ビルドサーバーはこれらのファイルを拡張の残りのコードとともにコンパイルし、その結果をエンジンにリンクします。この方法とは別に、[Swift パッケージ](/manuals/extensions-spm)や [CocoaPods](/manuals/extensions-cocoapods)を使って、既存のライブラリを依存関係として組み込むこともできます。

Swift コードは、macOS（`arm64` と `x86_64`）および iOS（実機とシミュレーター）向けにコンパイルされます。他のプラットフォーム向けのビルドでは、Swift ファイルは無視されます。


## Swift ソースファイルの追加 {#adding-swift-sources}

`.swift` ファイルは、C++ や Objective-C++ のファイルと同じく、拡張の `src` フォルダーに配置します。

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Swift ファイルはすべて `src` に置きます。`commonsrc` または `pluginsrc` に Swift ファイルがあると、macOS または iOS 向けのビルドに失敗します。

拡張の Swift ファイルはすべてまとめて1つの Swift モジュールとしてコンパイルされます。モジュール名には `ext.manifest` の `name` を使い、英字、数字、アンダースコア以外の文字をすべて `_` に置き換えます（`My-Extension` は `My_Extension` になります）。Swift の言語モードは Swift 5 です。

拡張のモジュール名は、コードがインポートするモジュールの名前と異なる必要があります。たとえば、`StoreKit` という名前の拡張では `import StoreKit` を使えません。コンパイラーがモジュール自身のインポートと解釈するためです。


## Objective-C++ から Swift を呼び出す {#calling-swift-from-objective-c}

拡張のエントリーポイントは、これまでどおり `DM_DECLARE_EXTENSION` で登録する C++ 関数です。このため、拡張には`.cpp` ファイルか `.mm` ファイルが少なくとも1つ必要です。このファイルから、自動生成される `<Module>-Swift.h` ヘッダーを介して Swift コードを呼び出します。

Objective-C から参照できるのは、`@objc` を付けたクラス、プロトコル、メソッドだけです。クラスは `public` として宣言し、`NSObject` を継承します。

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

* 生成されたヘッダーは `Foundation` をインポートします。他のフレームワークの型については前方宣言しか含まれません。そのような型を使うメソッドを呼び出す前に、該当するフレームワーク（たとえば `UIKit`）のヘッダーを `.mm` ファイルでインポートします。
* `throws` を付けた関数は `NSError **` パラメーターを受け取るメソッドとして、`async` 関数は完了ハンドラーを受け取るメソッドとして公開されます。
* ジェネリクス、関連値を持つ列挙型、構造体など、Swift 固有の機能は Objective-C から参照できません。これらは `@objc` を付けたクラスでラップします。
* `.mm` ファイルがコンパイルされるのは iOS と macOS 向けのビルドだけです。`.mm` と `.swift` のファイルしかない拡張を他のプラットフォーム向けにビルドすると、`Extension has no source!` エラーで失敗します。他のプラットフォーム向けにもビルドするには、`DM_DECLARE_EXTENSION` を `.cpp` ファイルに置き、そこから `.mm` ファイル内のコードを呼び出す部分を `DM_PLATFORM_IOS` または `DM_PLATFORM_OSX` で条件付きコンパイルします。


## Swift から Objective-C を呼び出す {#calling-objective-c-from-swift}

Swift から Objective-C や C の宣言を使うには、`<Module>-Bridging-Header.h` という名前のブリッジヘッダー（bridging header）を `src` フォルダーに追加します。たとえば `src/MyExtension-Bridging-Header.h` を次のように記述します。

```cpp
#import "mynative.h"
```

このヘッダーがあれば、Swift モジュールに自動的にインポートされます。ブリッジヘッダーがインクルードするヘッダーの検索先は、拡張の `include` フォルダーと、後述の `additionalSwiftIncludePaths` に指定したフォルダーです。

`Foundation`、`UIKit`、`StoreKit` などの Apple フレームワークは、Swift から通常の `import` でインポートできます。`ext.manifest` の `frameworks` と `weakFrameworks` に指定したフレームワークは、通常どおりリンクされます。システムフレームワークの多くは、Swift コードでインポートすると自動的にリンクされます。


## Swift コードから Swift パッケージを使う {#using-swift-packages-from-swift}

拡張の Swift コードからは、その拡張の `SwiftPackages.json` で宣言した [Swift パッケージ](/manuals/extensions-spm)のプロダクトを使えます。Swift ファイルでモジュールをインポートします。

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

パッケージの Objective-C ヘッダーは、`.mm` ファイルの場合と同じように、ブリッジヘッダーでインポートできます。

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

パッケージは、それを使う拡張の `SwiftPackages.json` で宣言します。ビルドサーバーは、先にパッケージをビルドし、次に拡張の Swift コードをビルドします。パッケージがエンジンのサポートする最小 OS バージョンより新しいバージョンを必要とする場合は、必要なバージョンを `SwiftPackages.json` の `minVersion` に設定します。拡張の Swift コードもそのバージョン向けにビルドされます。Swift コードから CocoaPods の依存関係を使うことはサポートされていません。Objective-C++ ファイルから使い、必要なものを Swift コードに渡してください。


## コンパイラーオプション {#compiler-options}

Swift コンパイラーのオプションは、`ext.manifest` ファイル内で C++ コンパイラーのオプションと同じ `context` に設定します。

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

* `defines` - C++ 用の定義は条件付きコンパイルの識別子として Swift に渡されるため、Swift でも `#if MY_DEFINE` を使えます。Swift がサポートするのは名前だけなので、`MY_DEFINE=1` のように値を指定しても、値の部分は破棄されます。
* `swiftFlags` - Swift コンパイラーに渡す追加のフラグです。各フラグと各値はそれぞれ独立したリスト項目として指定します。フラグは許可リストで絞り込まれ、リストにないフラグを指定すると `Invalid flag - 'swiftFlags'` エラーでビルドに失敗します。値に空白文字、バックスラッシュ、テンプレート構文が含まれる場合や、値で応答ファイルを指定した場合は、`invalid 'swiftFlags' value` エラーで失敗します。使用できるフラグは次のとおりです。
  * `-enable-upcoming-feature <Feature>` - 今後導入される言語機能を有効にします。たとえば `["-enable-upcoming-feature", "ExistentialAny"]` と指定します。
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`、`-Osize`、`-Onone` - 最適化レベルを指定します。デフォルトは `-O` です。
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - 拡張の `include` フォルダーに加えて、Swift コンパイラーがヘッダーやモジュールを検索するフォルダーです。
* `additionalFrameworkSearchPaths` - 拡張の `lib/<platform>` フォルダーに加えて、フレームワークの検索対象となるフォルダーです。Swift コンパイラーのほか、拡張のソースをコンパイルする C++ および Objective-C++ コンパイラーと、リンカーもこれらのフォルダーを検索します。

パスは拡張フォルダーを基準とする相対パスで指定し、その外側を参照することはできません。使用できる文字は英字、数字、および `._+-/` だけです。ビルドサーバーに送信されるのは拡張の `include`、`src`、`commonsrc`、`pluginsrc`、`lib/<platform>`、`manifests/<platform>`、`res/<platform>` フォルダーだけなので、パスはこれらのいずれかの中を指す必要があります。拡張のルートにある `vendor` フォルダーなど、それ以外のフォルダー内のファイルはビルド時には使えません。

`ios` プラットフォームの Swift 用のキーは、実機とシミュレーターの両方に適用されます。Swift のサポートが追加される前のビルドサーバーは、これらのキーを受け付けず、`Manifest context variable unsupported` エラーを返します。Defold のバージョンとビルドサーバーを更新するまで、プロジェクトをビルドできません。


## 最小 OS バージョン {#minimum-os-versions}

Swift ランタイムは、Defold がサポートするすべてのバージョンの iOS と macOS に含まれています。Swift コードは、ビルド対象の iOS または macOS の最小バージョン向けにビルドされ、アプリケーションは OS の Swift ランタイムを使います。その最小バージョンより後に導入された API を呼び出す前に、`#available` で利用できるか確認してください。

ランタイムの一部の機能は、新しいバージョンの OS にだけ含まれています。たとえば、`MutableSpan` とその関連型は iOS 26 と macOS 26 から OS に含まれています。最小バージョンがそれより古く、拡張の Swift コードやパッケージの動的フレームワークでこのような機能を使う場合、古い OS の端末でアプリケーションを実行するには追加のライブラリが必要になることがあります。手作業で追加する必要はありません。ビルドサーバーが Xcode と同じように、エンジンおよびエンジンと一緒に組み込まれる動的ライブラリが使うライブラリを特定し、アプリケーションに追加します。iOS では、これらのライブラリはアプリケーションの `Frameworks` フォルダーに配置され、残りのコードと一緒に署名されます。

ビルドの最小 OS バージョンは、エンジンがサポートする最小バージョンで、Defold のバージョンとビルドサーバーによって決まります。[Swift Package Manager のマニュアル](/manuals/extensions-spm)で説明しているように、`SwiftPackages.json` の `minVersion` を使うと、パッケージと Swift コードのビルド、およびエンジンのリンクに使う最小バージョンを引き上げることができます。引き下げることはできません。


## 制限 {#limitations}

* 拡張には、引き続き `DM_DECLARE_EXTENSION` を記述した C++ または Objective-C++ ファイルが必要です。Swift コードからは拡張を登録できません。Defold SDK（`dmsdk`）の C++ API も Swift からは使えないため、Objective-C++ ファイルから呼び出します。`dmsdk/dlib/hash.h` など、C と互換性がある `dmsdk` のヘッダーはブリッジヘッダーにインクルードできます。`.swift` ファイルだけでビルドすると、拡張名に由来するシンボルが未定義というエラーでリンクに失敗します。
* Swift コードから CocoaPods の依存関係を使うことはサポートされていません。Objective-C++ ファイルから使い、必要なものを Swift コードに渡してください。
* サポートされる言語モードは Swift 5 のみです。C++ との相互運用は有効になっていません。
* Swift ソースファイルに対応しているのは Defold 1.14.2 以降です。古い SDK を使うビルドサーバーでは、`Swift sources are not supported by this Defold SDK version` エラーでビルドに失敗します。
* `library` 成果物をビルドする場合（[Bob](/manuals/bob) の `--build-artifacts library`）、Swift ソースファイルはコンパイルされません。そのため、`<Module>-Swift.h` をインポートする Objective-C++ ファイルのコンパイルに失敗します。


## トラブルシューティング {#troubleshooting}

`no such module 'Name'`
: 指定したモジュールは、`SwiftPackages.json` で宣言したパッケージのプロダクトではありません。[Swift Package Manager のマニュアル](/manuals/extensions-spm)を参照し、そのモジュールを提供するプロダクトが `products` に含まれていることを確認します。

`Swift sources are only supported in the 'src' folder`
: `.swift` ファイルを拡張の `src` フォルダーに移動します。

`'MyExtension-Swift.h' file not found`
: モジュール名は `ext.manifest` の `name` から生成されます。`#import` 行の名前を確認します。

`unknown type name 'MyExtensionGreeter'`
: 生成されたヘッダーにクラスが含まれていません。クラスに `public` と `@objc` が付いていて `NSObject` を継承していること、また、`.mm` ファイルで `@objc(...)` に指定した名前を使っていることを確認します。

`cannot find 'AppStore' in scope` と `file 'A.swift' is part of module 'StoreKit'; ignoring import` が同時に表示される場合
: 拡張の名前が、インポートするモジュールの名前と同じです。`ext.manifest` で拡張の名前を変更します。

`Undefined symbols ... _MyExtension`
: 拡張に `DM_DECLARE_EXTENSION` がありません。上記の例に従って、拡張を登録する `.mm` ファイルを追加します。

`Invalid flag - 'swiftFlags'`
: 許可リストにないフラグを指定しています。そのフラグを削除するか、リストにあるフラグに変更します。

`invalid 'swiftFlags' value`
: 値に空白文字、バックスラッシュ、テンプレート構文が含まれているか、応答ファイルを指定しています。各フラグと各値を、それぞれ独立したリスト項目として指定します。
