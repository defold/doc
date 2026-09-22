---
title: ネイティブ拡張 - 拡張マニフェスト
brief: このマニュアルでは、拡張マニフェストと、アプリケーションマニフェストおよびエンジンマニフェストとの関係を説明します。
---

# 拡張、アプリケーション、エンジンのマニフェストファイル {#extension-application-and-engine-manifest-files}

拡張マニフェスト（extension manifest）は、1つの拡張をビルドする際に使用するフラグや定義を記述する設定ファイルです。この設定は、アプリケーションレベルの設定および Defold エンジン自体の基本設定と組み合わされます。

## アプリケーションマニフェスト {#app-manifest}

アプリケーションマニフェスト（application manifest、ファイルの拡張子は `.appmanifest`）は、ビルドサーバーでゲームをビルドする方法を指定するアプリケーションレベルの設定です。アプリケーションマニフェストを使うと、エンジンの使用していない部分を削除できます。物理エンジンが不要であれば、実行ファイルから削除してサイズを小さくできます。使用していない機能を除外する方法については、[アプリケーションマニフェストのマニュアル](/manuals/app-manifest)を参照してください。

## エンジンマニフェスト {#engine-manifest}

Defold エンジンには、エンジンと Defold SDK の各リリースに含まれるビルドマニフェスト（build manifest、`build.yml`）があります。このマニフェストは、使用する SDK のバージョン、実行するコンパイラーやリンカーなどのツール、およびそれらのツールに渡すデフォルトのビルドフラグとリンクフラグを制御します。このマニフェストは、[GitHub 上](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml)の share/extender/build_input.yml にあります。

## 拡張マニフェスト {#extension-manifest}

一方、拡張マニフェスト（`ext.manifest`）は、拡張専用の設定ファイルです。拡張マニフェストは、拡張のソースコードをコンパイルおよびリンクする方法と、含める追加のライブラリを制御します。 

3種類のマニフェストファイルはすべて同じ構文を共有しているため、マージして拡張とゲームのビルド方法を完全に制御できます。

ビルドする拡張ごとに、次のようにマニフェストが組み合わされます。

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

これにより、ユーザーはエンジンと各拡張のデフォルトの動作を上書きできます。また、最終リンク段階では、アプリケーションマニフェストを Defold のマニフェストとマージします。

	manifest = merge(game.appmanifest, build.yml)


### ext.manifest ファイル {#the-extmanifest-file}

マニフェストファイルには、拡張の名前のほかに、プラットフォーム固有のコンパイルフラグ、リンクフラグ、ライブラリ、フレームワークを記述できます。*ext.manifest* ファイルに "platforms" セクションがない場合や、リストにプラットフォームがない場合でも、バンドルの作成対象のプラットフォーム向けにビルドされますが、追加のフラグは設定されません。

以下に例を示します。

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    arm64_sim-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### 使用できるキー {#allowed-keys}

プラットフォーム固有のコンパイルフラグに使用できるキーは次のとおりです。

* `frameworks` - ビルド時に含める Apple のフレームワーク（iOS および macOS）
* `weakFrameworks` - ビルド時に任意で含める Apple のフレームワーク（iOS および macOS）
* `flags` - コンパイラーに渡すフラグ
* `linkFlags` - リンカーに渡すフラグ
* `libs` - リンク時に含める追加のライブラリ
* `defines` - ビルド時に設定する定義
* `aaptExtraPackages` - 生成する追加のパッケージ名（Android）
* `aaptExcludePackages` - 除外するパッケージの正規表現（または正確な名前）（Android）
* `aaptExcludeResourceDirs` - 除外するリソースディレクトリの正規表現（または正確な名前）（Android）
* `excludeLibs`, `excludeJars`, `excludeSymbols` - これらのフラグは、プラットフォームのコンテキストですでに定義されているものを削除するために使用します。

すべてのキーワードには、許可リストによるフィルターを適用します。これは、不正なパスの処理や、ビルド用のアップロードフォルダー外のファイルへのアクセスを防ぐためです。
