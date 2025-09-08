---
title: Defold 项目构建器手册
brief: Bob 是用于构建 Defold 项目的命令行工具。本手册详述如何使用这个工具。
---

# 构建器 Bob

Bob 是一个命令行工具，用于在正常编辑器工作流程之外构建 Defold 项目。

Bob 能够构建数据（对应于选择编辑器菜单项 <kbd>Project ▸ Build</kbd> 的构建步骤），创建数据存档，并创建独立的、可分发的应用程序包（对应于编辑器菜单项 <kbd>Project ▸ Bundle ▸ ...</kbd> 选项）。

Bob 作为 Java _JAR_ 存档分发，其中包含构建所需的一切。您可以在 [GitHub 发布页面](https://github.com/defold/defold/releases) 上找到最新的 *bob.jar* 分发版本。选择一个发布版本，然后下载 *bob/bob.jar*。如果您使用的是 Defold 1.9.6，您将需要 OpenJDK 21 来运行它。对于旧版本的 Defold，您将需要 OpenJDK 17 或 11。

兼容的 OpenJDK 21 镜像（从 Defold 1.9.6 开始）：
* [Microsoft 提供的 OpenJDK 21](https://docs.microsoft.com/en-us/java/openjdk/download#openjdk-21)
* [Adoptium 工作组提供的 OpenJDK 21](https://github.com/adoptium/temurin21-binaries/releases) / [Adoptium.net](https://adoptium.net/)

如果您在 Windows 上，您需要 OpenJDK 的 `.msi` 文件安装程序。

## 用法

Bob 通过在 shell 或命令行中调用 `java`（在 Windows 上是 `java.exe`）并提供 bob java 存档作为参数来运行：

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
                                         Comma separated list.
    --build-server <arg>                 The build server (when using
                                         native extensions)
    --build-server-header <arg>          Additional build server header to
                                         set
 -ce,--certificate <arg>                 DEPRECATED! Use --keystore
                                         instead
 -d,--debug                              DEPRECATED! Use --variant=debug
                                         instead
    --debug-ne-upload                    Outputs the files sent to build
                                         server as upload.zip
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
    --manifest-private-key <arg>         Private key to use when signing
                                         manifest and archive.
    --manifest-public-key <arg>          Public key to use when signing
                                         manifest and archive.
    --max-cpu-threads <arg>              Max count of threads that bob.jar
                                         can use
 -mp,--mobileprovisioning <arg>          mobileprovisioning profile (iOS)
    --ne-build-dir <arg>                 Specify a folder with includes or
                                         source, to build a specific
                                         library. More than one occurrance
                                         is allowed.
    --ne-output-name <arg>               Specify a library target name
 -o,--output <arg>                       Output directory. Default is
                                         "build/default"
 -p,--platform <arg>                     Platform (when building and
                                         bundling)
 -pk,--private-key <arg>                 DEPRECATED! Use --keystore
                                         instead
 -r,--root <arg>                         Build root directory. Default is
                                         current directory
    --resource-cache-local <arg>         Path to local resource cache.
    --resource-cache-remote <arg>        URL to remote resource cache.
    --resource-cache-remote-pass <arg>   Password/token to authenticate
                                         access to the remote resource
                                         cache.
    --resource-cache-remote-user <arg>   Username to authenticate access
                                         to the remote resource cache.
    --settings <arg>                     Path to a game project settings
                                         file. More than one occurrance is
                                         allowed. The settings files are
                                         applied left to right.
    --strip-executable                   Strip the dmengine of debug
                                         symbols (when bundling iOS or
                                         Android)
 -tc,--texture-compression <arg>         Use texture compression as
                                         specified in texture profiles
 -tp,--texture-profiles <arg>            DEPRECATED! Use
                                         --texture-compression instead
 -u,--auth <arg>                         User auth token
    --use-async-build-server             DEPRECATED! Asynchronous build is
                                         now the default.
    --use-lua-bytecode-delta             Use byte code delta compression
                                         when building for multiple
                                         architectures
    --use-uncompressed-lua-source        Use uncompressed and unencrypted
                                         Lua source code instead of byte
                                         code
    --use-vanilla-lua                    DEPRECATED! Use
                                         --use-uncompressed-lua-source
                                         instead.
 -v,--verbose                            Verbose output
    --variant <arg>                      Specify debug, release or
                                         headless version of dmengine
                                         (when bundling)
    --version                            Prints the version number to the
                                         output
    --with-symbols                       Generate the symbol file (if
                                         applicable)
```

可用命令：

`clean`
: 删除构建目录中已构建的文件。

`distclean`
: 删除构建目录中的所有文件。

`build`
: 构建所有项目数据。添加 `--archive` 选项以构建数据存档文件（构建目录中的 "`game.darc`"）。

`bundle`
: 创建特定于平台的应用程序包。打包需要存在已构建的存档（使用 `--archive` 选项的 `build`）并指定目标平台（使用 `--platform` 选项）。除非使用 `--bundle-output` 选项指定不同的目录，否则 Bob 会在输出目录中创建包。包根据 *game.project* 中的项目名称设置命名。`--variant` 指定打包时构建哪种类型的可执行文件，它与 `--strip-executable` 选项一起取代了 `--debug` 选项。如果没有指定 `--variant`，您将获得引擎的发布版本（在 Android 和 iOS 上剥离符号）。将 `--variant` 设置为 debug 并省略 `--strip-executable` 会产生与 `--debug` 过去相同的可执行文件类型。

`resolve`
: 解析所有外部库依赖项。

可用平台和架构：

`x86_64-darwin` (Defold 1.3.5 及更早版本)
`x86_64-macos` (Defold 1.3.6 及更新版本)
: macOS 64 位

`arm64-macos` (Defold 1.5.0 及更早版本)
: macOS Apple Silicon (ARM)

`x86_64-win32`
: Windows 64 位

`x86-win32`
: Windows 32 位

`x86_64-linux`
: Linux 64 位

`x86_64-ios`
: iOS macOS 64 位 (iOS 模拟器)

`armv7-darwin` (Defold 1.3.5 及更早版本)
`armv7-ios` (Defold 1.3.6 及更新版本)
: iOS，具有可用的 32 位 `armv7-darwin` 和 64 位 `arm64-darwin` 架构。默认情况下，`--architectures` 参数值为 `armv7-darwin,arm64-darwin`。

`armv7-android`
: Android，具有可用的 32 位 `armv7-android` 和 64 位 `arm64-android` 架构。默认情况下，`--architectures` 参数值为 `armv7-android,arm64-android`。

`js-web`
: HTML5，具有可用的 `js-web` 和 `wasm-web` 架构。默认情况下，`--architectures` 参数值为 `js-web,wasm-web`。

默认情况下，Bob 在当前目录中寻找要构建的项目。如果您将当前目录更改为 Defold 项目并调用 bob，它将在默认输出目录 *build/default* 中构建项目的数据。

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

您可以将命令串联在一起以一次性执行一系列任务。以下示例解析库，清除构建目录，构建存档数据并将 macOS 应用程序捆绑（命名为 *My Game.app*）：

```sh
$ java -jar bob.jar --archive --platform x86-darwin resolve distclean build bundle
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
