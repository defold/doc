---
title: Defold プロジェクトビルダーのマニュアル
brief: Bob は Defold プロジェクトをビルドするためのコマンドラインツールです。このマニュアルでは、ツールの使い方を説明します。
---

# ビルドツール Bob {#bob-the-builder}

Bob は、通常のエディターでのワークフローを使わずに Defold プロジェクトをビルドするためのコマンドラインツールです。

Bob は、データのビルド（エディターのメニュー項目 <kbd>Project ▸ Build</kbd> を選択したときのビルド処理に相当）、データアーカイブの作成、スタンドアロンで配布可能なアプリケーションバンドル（bundle）の作成（エディターのメニュー項目 <kbd>Project ▸ Bundle ▸ ...</kbd> の各オプションに相当）ができます。

Bob は、ビルドに必要なものをすべて含む Java _JAR_ アーカイブとして配布されています。最新の *bob.jar* は [GitHub のリリースページ](https://github.com/defold/defold/releases) で入手できます。リリースを選択し、*bob/bob.jar* をダウンロードします。実行には OpenJDK 25 が必要です。

互換性のある OpenJDK 25 のミラー:
* [Microsoft による OpenJDK 25](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [Adoptium Working Group による OpenJDK 25](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

Windows を使用している場合は、OpenJDK の `.msi` ファイルのインストーラーを使用します。

## 使い方 {#usage}

Bob は、シェルまたはコマンドラインから `java`（Windows では `java.exe`）を呼び出し、引数に Bob の Java アーカイブを指定して実行します。

```text
$ java -jar bob.jar --help
usage: bob [options] [commands]
 -a,--archive                            Build archive
 -ar,--architectures <arg>               Comma separated list of
                                         architectures to include for the
                                         platform
    --archive-resource-padding <arg>     The alignment of the resources in
                                         the game archive. Default is 4
 -bf,--bundle-format <arg>               Which formats to create the
                                         application bundle in. Comma
                                         separated list. (Android: 'apk'
                                         and 'aab')
    --binary-output <arg>                Location where built engine
                                         binary will be placed. Default is
                                         "<build-output>/<platform>/"
 -bo,--bundle-output <arg>               Bundle output directory
 -br,--build-report <arg>                DEPRECATED! Use
                                         --build-report-json instead
 -brhtml,--build-report-html <arg>       Filepath where to save a build
                                         report as HTML
 -brjson,--build-report-json <arg>       Filepath where to save a build
                                         report as JSON
    --build-artifacts <arg>              If left out, will default to
                                         build the engine. Choices:
                                         'engine', 'plugins', 'library'.
                                         Comma separated list
    --build-input <arg>                  Project resource path to build
                                         instead of game.project. May be
                                         specified more than once. More
                                         than one occurrence is allowed
    --build-input-file <arg>             File containing project resource
                                         paths to build instead of
                                         game.project. May be specified
                                         more than once. More than one
                                         occurrence is allowed
    --build-server <arg>                 The build server (when using
                                         native extensions)
    --build-server-header <arg>          Additional build server header to
                                         set. More than one occurrence is
                                         allowed
 -ce,--certificate <arg>                 DEPRECATED! Use --keystore
                                         instead
 -d,--debug                              DEPRECATED! Use --variant=debug
                                         instead
    --debug-ne-upload                    Outputs the files sent to build
                                         server as upload.zip
    --debug-output-glsl <arg>            Force build GLSL shaders
    --debug-output-hlsl <arg>            Force build HLSL shaders
    --debug-output-msl <arg>             Force build Metal shaders
    --debug-output-spirv <arg>           Force build SPIR-V shaders
    --debug-output-wgsl <arg>            Force build WGSL shaders
    --defoldsdk <arg>                    What version of the defold sdk
                                         (sha1) to use
 -e,--email <arg>                        User email
 -ea,--exclude-archive                   Exclude resource archives from
                                         application bundle. Use this to
                                         create an empty Defold
                                         application for use as a build
                                         target
    --exclude-build-folder <arg>         DEPRECATED! Use '.defignore' file
                                         instead
    --experimental-path-minification     Minimizes resource path names in
                                         order to save bundle size.
 -h,--help                               This help message
 -i,--input <arg>                        DEPRECATED! Use --root instead
    --identity <arg>                     Sign identity (iOS)
 -kp,--key-pass <arg>                    Password of the deployment key if
                                         different from the keystore
                                         password (Android)
 -ks,--keystore <arg>                    Deployment keystore used to sign
                                         APKs (Android)
 -ksa,--keystore-alias <arg>             The alias of the signing key+cert
                                         you want to use (Android)
 -ksp,--keystore-pass <arg>              Password of the deployment
                                         keystore (Android)
 -l,--liveupdate <arg>                   Yes if liveupdate content should
                                         be published
    --max-cpu-threads <arg>              Max count of threads that bob.jar
                                         can use
 -mp,--mobileprovisioning <arg>          mobileprovisioning profile (iOS)
    --ne-build-dir <arg>                 Specify a folder with includes or
                                         source, to build a specific
                                         library. More than one occurrence
                                         is allowed
    --ne-output-name <arg>               Specify a library target name
 -o,--output <arg>                       Output directory. Default is
                                         "build/default"
 -p,--platform <arg>                     Platform (when building and
                                         bundling)
 -pk,--private-key <arg>                 DEPRECATED! Use --keystore
                                         instead
 -r,--root <arg>                         Build root directory. Default is
                                         current directory
    --resource-cache-local <arg>         Path to local resource cache
    --resource-cache-remote <arg>        URL to remote resource cache
    --resource-cache-remote-pass <arg>   Password/token to authenticate
                                         access to the remote resource
                                         cache
    --resource-cache-remote-user <arg>   Username to authenticate access
                                         to the remote resource cache
    --settings <arg>                     Path to a game project settings
                                         file. The settings files are
                                         applied left to right. More than
                                         one occurrence is allowed
    --strip-executable                   Strip the dmengine of debug
                                         symbols (when bundling iOS or
                                         Android)
 -tc,--texture-compression               Use texture compression as
                                         specified in texture profiles
 -tp,--texture-profiles <arg>            DEPRECATED! Use
                                         --texture-compression instead
 -u,--auth <arg>                         User auth token
    --use-async-build-server             DEPRECATED! Asynchronous build is
                                         now the default
    --use-lua-bytecode-delta             Use byte code delta compression
                                         when building for multiple
                                         architectures
    --use-uncompressed-lua-source        Use uncompressed and unencrypted
                                         Lua source code instead of byte
                                         code
    --use-vanilla-lua                    DEPRECATED! Use
                                         --use-uncompressed-lua-source
                                         instead
 -v,--verbose                            Verbose output
    --variant <arg>                      Specify debug, release or
                                         headless version of dmengine
                                         (when bundling)
    --version                            Prints the version number to the
                                         output
    --with-sha1                          Generate (and verify) sha1
                                         signatures from build artifacts
                                         (when bunding for web)
    --with-symbols                       Generate the symbol file (if
                                         applicable)
```

`--texture-compression` は値を指定しないスイッチです。指定すると、テクスチャプロファイル（texture profiles）で選択した圧縮が有効になります。テクスチャ圧縮を無効にするには、このスイッチを省略します。従来の `--texture-compression=true` という形式も引き続き使用できます。従来の `--texture-compression=false` という形式は無視され、警告が出力されます。代わりにスイッチを省略してください。

使用可能なコマンド:

`clean`
: ビルドディレクトリ内のビルド済みファイルを削除します。

`distclean`
: ビルドディレクトリ内のすべてのファイルを削除します。

`build`
: 選択したビルドルート（build root）から到達可能な依存関係グラフをビルドします。デフォルトの起点は `game.project` です。`--build-input` と `--build-input-file` で別の起点を指定できます。ファイルがプロジェクトのルートディレクトリ以下に存在するというだけでは、ビルドされません。`game.project` がビルドルートの場合は、`--archive` を追加すると、ビルドディレクトリ内にゲームデータのアーカイブをビルドします。

`bundle`
: プラットフォーム固有のアプリケーションバンドルを作成します。バンドルの作成には、ビルド済みのアーカイブが存在すること（`--archive` オプションを付けて `build` を実行）と、対象プラットフォームが指定されていること（`--platform` オプションで指定）が必要です。Bob は、`--bundle-output` オプションで別のディレクトリを指定しない限り、出力ディレクトリにバンドルを作成します。バンドルの名前は、*game.project* のプロジェクト名の設定に従います。`--variant` はバンドル作成時にビルドする実行ファイルの種類を指定し、`--strip-executable` オプションと組み合わせて `--debug` オプションの代わりになります。`--variant` を指定しない場合は、リリース版のエンジンが作成されます（Android と iOS ではシンボルが除去されます）。`--variant` を debug に設定し、`--strip-executable` を省略すると、以前の `--debug` と同じ種類の実行ファイルが作成されます。

`resolve`
: 外部ライブラリへの依存関係をすべて解決します。

使用可能なプラットフォームとアーキテクチャ:

`x86_64-macos`
: macOS 64 ビット

`arm64-macos`
: macOS Apple Silicon（ARM）

`x86_64-win32`
: Windows 64 ビット

`x86-win32`
: Windows 32 ビット

`x86_64-linux`
: Linux 64 ビット

`arm64-linux`
: Raspberry Pi と Linux ベースの携帯型デバイス向けの Linux ARM64。

`arm64_sim-ios`
: Apple Silicon 搭載 Mac 上の iOS シミュレーター。シミュレーターのバンドルは署名 ID やプロビジョニングプロファイルを使用しないため、`--identity` と `--mobileprovisioning` は無視されます。

`arm64-ios`
: iOS 64 ビット。`--architectures` 引数のデフォルト値は `arm64-ios` です。

`armv7-android`
: Android では、32 ビットの `armv7-android`、64 ビットの `arm64-android`、64 ビットの `x86_64-android` アーキテクチャを使用できます。`--architectures` 引数のデフォルト値は `armv7-android,arm64-android` です。`x86_64-android` アーキテクチャは任意で選択するもので（主に Android エミュレーター、ChromeOS、Windows Subsystem for Android で役立ちます）、明示的に追加する必要があります。

`wasm-web`
: HTML5 では、`wasm-web` と `wasm_pthread-web` アーキテクチャを使用できます。`--architectures` 引数のデフォルト値は `wasm-web` です。

デフォルトでは、Bob は現在のディレクトリでプロジェクトを探し、`game.project` から到達可能なリソース（resource）を *build/default* にビルドします。参照されていないリソースはコンパイルされません。コードが実行時にパスを指定して未加工のファイルを読み込む場合は、[プロジェクト設定の Custom Resources](/manuals/project-settings/#custom-resources) を使って、それらを含めてください。それ以外の Defold リソースには、ビルドルートから到達可能な参照が必要です。

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

コマンドを並べて指定すると、一連のタスクをまとめて実行できます。次の例では、ライブラリの依存関係を解決し、ビルドディレクトリの内容をすべて削除し、アーカイブデータをビルドして、macOS アプリケーションのバンドル（名前は *My Game.app*）を作成します。

```sh
$ java -jar bob.jar --archive --platform x86_64-macos resolve distclean build bundle
100%
$ ls -al build/default/
total 70784
drwxr-xr-x   13 sicher  staff       442  1 Dec 10:15 .
drwxr-xr-x    3 sicher  staff       102  1 Dec 10:15 ..
drwxr-xr-x    3 sicher  staff       102  1 Dec 10:15 My Game.app
drwxr-xr-x    8 sicher  staff       272  1 Dec 10:15 builtins
-rw-r--r--    1 sicher  staff    140459  1 Dec 10:15 digest_cache
drwxr-xr-x    4 sicher  staff       136  1 Dec 10:15 fonts
-rw-r--r--    1 sicher  staff  35956340  1 Dec 10:15 game.darc
-rw-r--r--    1 sicher  staff       735  1 Dec 10:15 game.projectc
drwxr-xr-x  223 sicher  staff      7582  1 Dec 10:15 graphics
drwxr-xr-x    3 sicher  staff       102  1 Dec 10:15 input
drwxr-xr-x   20 sicher  staff       680  1 Dec 10:15 logic
drwxr-xr-x   27 sicher  staff       918  1 Dec 10:15 sound
-rw-r--r--    1 sicher  staff    131926  1 Dec 10:15 state
$
```
