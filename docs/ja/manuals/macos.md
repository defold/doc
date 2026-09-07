---
title: macOS プラットフォーム向けの Defold 開発
brief: このマニュアルでは、macOS で Defold アプリケーションをビルドして実行する方法を説明します
---

# macOS 向けの開発 {#macos-development}

macOS プラットフォーム向けの Defold アプリケーションの開発は、考慮すべき点がごく少なく、手順も簡単です。

## プロジェクト設定 {#project-settings}

macOS 固有のアプリケーション設定は、*game.project* 設定ファイルの [macOS セクション](/manuals/project-settings/#macos)で行います。

## アプリケーションアイコン {#application-icon}

macOS ゲームで使うアプリケーションアイコンは .`icns` 形式である必要があります。複数の `.png` ファイルを `.iconset` としてまとめると、簡単に `.icns` ファイルを作成できます。[`.icns` ファイルを作成するための公式手順](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html)に従ってください。手順の概要は次のとおりです。

* アイコン用のフォルダー（例: `game.iconset`）を作成します。
* 作成したフォルダーにアイコンファイルをコピーします。

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* `iconutil` コマンドラインツールを使って、`.iconset` フォルダーを `.icns` ファイルに変換します。

```
iconutil -c icns -o game.icns game.iconset
```

## アプリケーションの公開 {#publishing-your-application}
アプリケーションは、Mac App Store、Steam や itch.io などのサードパーティーのストアやポータル、または自身のウェブサイトで公開できます。アプリケーションを公開する前に、提出の準備をする必要があります。アプリケーションの配布方法にかかわらず、次の手順が必要です。

1. 実行権限を追加して、誰でもゲームを実行できるようにします（デフォルトでは、ファイルの所有者にのみ実行権限があります）。

```
$ chmod +x Game.app/Contents/MacOS/Game
```

2. ゲームが必要とする権限を指定するエンタイトルメント（entitlements）ファイルを作成します。ほとんどのゲームでは、次の権限で十分です。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - アプリケーションが MAP_JIT フラグを使って、書き込み可能かつ実行可能なメモリを作成してよいかどうかを示します。
  * `com.apple.security.cs.allow-unsigned-executable-memory` - アプリケーションが MAP_JIT フラグの使用による制限を受けずに、書き込み可能かつ実行可能なメモリを作成してよいかどうかを示します。
  * `com.apple.security.cs.allow-dyld-environment-variables` - アプリケーションがダイナミックリンカーの環境変数の影響を受けてよいかどうかを示します。これらの環境変数を使うと、アプリケーションのプロセスにコードを挿入できます。

アプリケーションによっては、追加のエンタイトルメントも必要になる場合があります。Steamworks 拡張では、次の追加エンタイトルメントが必要です。

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

  * `com.apple.security.cs.disable-library-validation` - アプリケーションがコード署名を要求せずに、任意のプラグインやフレームワークを読み込んでよいかどうかを示します。

アプリケーションに付与できるすべてのエンタイトルメントは、公式の [Apple 開発者ドキュメント](https://developer.apple.com/documentation/bundleresources/entitlements)に記載されています。

3. `codesign` を使ってゲームに署名します。

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Mac App Store 以外での公開 {#publishing-outside-the-mac-app-store}
Apple は、Mac App Store 以外で配布されるすべてのソフトウェアについて、macOS Catalina のデフォルト設定で実行するために Apple による公証を受けることを要求しています。Xcode の外でスクリプトによるビルド環境に公証を追加する方法は、[公式ドキュメント](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow)を参照してください。手順の概要は次のとおりです。

1. 上記の手順に従って権限を追加し、アプリケーションに署名します。

2. ゲームを ZIP 形式に圧縮し、`altool` を使って公証のためにアップロードします。

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

3. `altool --notarize-app` の呼び出しから返されたリクエスト UUID を使って、提出したアプリケーションのステータスを確認します。

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

4. ステータスが `success` になるまで待ち、公証チケットをゲームに添付します。

```
$ xcrun stapler staple "Game.app"
```

5. これでゲームを配布する準備ができました。

## Mac App Store での公開 {#publishing-to-the-mac-app-store}
Mac App Store で公開する手順は、[Apple 開発者ドキュメント](https://developer.apple.com/macos/submit/)に詳しく記載されています。提出する前に、上記の説明に従って権限を追加し、`codesign` でアプリケーションに署名してください。

注意: Mac App Store で公開する場合、ゲームの公証は必要ありません。

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)
