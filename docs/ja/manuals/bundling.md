---
title: アプリケーションのバンドル作成
brief: このマニュアルでは、アプリケーションのバンドルを作成する方法を説明します。
---

# アプリケーションのバンドル作成 {#bundling-an-application}

アプリケーションの開発中は、対象プラットフォームでできるだけ頻繁にゲームをテストする習慣を付けることをお勧めします。パフォーマンスの問題を開発の早い段階で検出するためです。この段階では、こうした問題をはるかに修正しやすくなります。また、シェーダーなどの動作の違いを見つけるために、すべての対象プラットフォームでテストすることをお勧めします。モバイル向けの開発では、[モバイル開発用アプリ](/manuals/dev-app/) を使ってアプリにコンテンツを転送できます。これにより、バンドル（bundle）全体の作成とアンインストール、インストールのサイクルを繰り返す必要がなくなります。

Defold がサポートするすべてのプラットフォーム向けのアプリケーションバンドルを、外部ツールを使わずに Defold エディター内で作成できます。Defold のコマンドラインツールを使って、コマンドラインからバンドルを作成することもできます。プロジェクトに1つ以上の [ネイティブ拡張（native extension）](/manuals/extensions) が含まれている場合、アプリケーションのバンドル作成にはネットワーク接続が必要です。

## エディター内でのバンドル作成 {#bundling-from-within-the-editor}

Project メニューの Bundle オプションからアプリケーションバンドルを作成します。

![](images/bundling/bundle_menu.png)

メニューのいずれかのオプションを選択すると、そのプラットフォーム用の Bundle ダイアログが表示されます。

### ビルドレポート {#build-reports}

ゲームのバンドル作成時には、ビルドレポート（build report）を作成するオプションがあります。これは、ゲームのバンドルに含まれるすべてのアセット（asset）のサイズを把握するのにとても役立ちます。ゲームのバンドル作成時に *Generate build report* チェックボックスをオンにするだけです。

![ビルドレポート](images/profiling/build_report.png)

ビルドレポートの詳細については、[プロファイリングのマニュアル](/manuals/profiling/#build-reports) を参照してください。

### Android

Android アプリケーションバンドル（.apk ファイル）の作成方法は、[Android のマニュアル](/manuals/android/#creating-an-android-application-bundle) で説明しています。

### iOS

iOS アプリケーションバンドル（.ipa ファイル）の作成方法は、[iOS のマニュアル](/manuals/ios/#creating-an-ios-application-bundle) で説明しています。

### macOS

macOS アプリケーションバンドル（.app ファイル）の作成方法は、[macOS のマニュアル](/manuals/macos) で説明しています。

### Linux

Linux アプリケーションバンドルの作成には特別なセットアップは不要で、[プロジェクト設定ファイル](/manuals/project-settings/) の *game.project* にプラットフォーム固有の任意設定もありません。

### Windows

Windows アプリケーションバンドル（.exe ファイル）の作成方法は、[Windows のマニュアル](/manuals/windows) で説明しています。

### HTML5

HTML5 アプリケーションバンドルの作成方法と任意のセットアップについては、[HTML5 のマニュアル](/manuals/html5/#creating-html5-bundle) で説明しています。

#### Facebook Instant Games

Facebook Instant Games 専用の、特別なバージョンの HTML5 アプリケーションバンドルを作成できます。この手順は、[Facebook Instant Games のマニュアル](/manuals/instant-games/) で説明しています。

## コマンドラインからのバンドル作成 {#bundling-from-the-command-line}

エディターは、Defold のコマンドラインツール [Bob](/manuals/bob/) を使ってアプリケーションのバンドルを作成します。

日々のアプリケーション開発では、Defold エディター内でビルドとバンドル作成を行うことが多いでしょう。それ以外の状況では、アプリケーションバンドルを自動生成したい場合があります。たとえば、新しいバージョンをリリースするときにすべてのターゲット向けに一括ビルドする場合や、ゲームの最新バージョンのナイトリービルドを作成する場合です。こうした処理は CI 環境で行うこともあるでしょう。[Bob コマンドラインツール](/manuals/bob/) を使えば、通常のエディターのワークフロー以外でも、アプリケーションのビルドとバンドル作成を行えます。

## バンドルの構成 {#the-bundle-layout}

バンドルの論理的な構成は、次のようになっています。

![](images/bundling/bundle_schematic_01.png)

バンドルはフォルダーに出力されます。プラットフォームによっては、そのフォルダーが `.apk` または `.ipa` として ZIP 形式でアーカイブされることもあります。
フォルダーの内容は、プラットフォームによって異なります。

Defold のバンドル作成処理では、実行ファイルに加えて、そのプラットフォームに必要なアセット（たとえば Android の .xml リソースファイル）も収集します。

[bundle_resources](https://defold.com/manuals/project-settings/#bundle-resources) 設定を使って、バンドル内にそのまま配置するアセットを指定できます。
これはプラットフォームごとに設定できます。

ゲームのアセットは `game.arcd` ファイル内に格納され、LZ4 圧縮で個別に圧縮されます。
[custom_resources](https://defold.com/manuals/project-settings/#custom-resources) 設定を使って、`game.arcd` 内に圧縮して配置するアセットを指定できます。
これらのアセットには、[`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource) 関数でアクセスできます。

## リリースとデバッグの違い {#release-vs-debug}

アプリケーションのバンドル作成時には、デバッグバンドルとリリースバンドルのどちらを作成するか選択できます。両者の違いはわずかですが、次の点を把握しておくことが重要です。

* リリースビルドには、既定では [プロファイラー](/manuals/profiling) が含まれません。デバッグビルドとリリースビルドの両方でプロファイラーを利用できるようにするには、[アプリケーションマニフェスト（app manifest）](/manuals/app-manifest/#profiler) の **Profiler** を **Always** に設定します。
* リリースビルドには、[画面レコーダー](/ref/stable/sys/#start_record) が含まれません。
* リリースビルドでは、どの `print()` 呼び出しの出力も、どのネイティブ拡張からの出力も表示されません。
* リリースビルドでは、`sys.get_engine_info()` の `is_debug` 値が `false` に設定されます。
* リリースビルドでは、`tostring()` を呼び出したときに `hash` 値の逆引きが行われません。つまり、`url` 型または `hash` 型の値に対する `tostring()` は、元の文字列ではなく数値表現を返します（`'hash: [/camera_001]'` と `'hash: [11844936738040519888 (unknown)]'` の違いです）。
* リリースビルドでは、[ホットリロード（hot reload）](/manuals/hot-reload) などの機能を使うために、エディターから実行対象として指定することはできません。


