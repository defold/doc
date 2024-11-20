---
title: Defold 项目编译教程
brief: Bob 是用于 Defold 项目的命令行编译工具. 本教程详述如何使用这个工具.
---

# 编译器 Bob

Bob 是一个用于Defold项目编辑器之外的命令行编译工具.

Bob 用来编译操作 (对应编辑器里的 <kbd>Project ▸ Build</kbd>), 来创建数据档或者创建可独立发布的应用 (对应编辑器里的 <kbd>Project ▸ Bundle ▸ ...</kbd> 选项)

Bob 集合了编译所需的一切, 作为Java包 _JAR_ 发布. 最新的 *bob.jar* 发布在 [Defold 下载页](http://d.defold.com) 和 [GitHub 发布页](https://github.com/defold/defold/releases) 上. 选择一个版本, 下载 *bob/bob.jar*. 如果你使用的是 Defold 1.9.6, 您需要安装 OpenJDK 21. 对于 Defold 老版本, 你需要 openJDK 17.

兼容 OpenJDK 21 镜像 (自从 Defold 1.9.6):
* https://docs.microsoft.com/en-us/java/openjdk/download#openjdk-21
* https://github.com/adoptium/temurin21-binaries/releases / https://adoptium.net/

比如在 Windows 平台上, 需要下载 OpenJDK 21 的 .msi 安装包.

## 用法

Bob 运行于命令行界面 `java` (再Windows上是 `java.exe`) 后跟bob的jar包作为参数:

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

支持的命令:

`clean`
: 清空编译目录下的编译文件.

`distclean`
: 清空编译目录下的所有文件.

`build`
: 编译所有项目文件. 加入 `--archive` 选项可生成编译数据包 (编译目录下生成 "game.darc" 文件).

`bundle`
: 指定平台打包. 打包需要数据包已经编译生成 (`build` 加入 `--archive` 选项) 然后指定打包平台 (使用 `--platform` 选项). Bob 会把应用打包到编译目录下, 除非使用 `--bundle-output` 选项手动指定打包输出目录. 包名根据 *game.project* 文件中设置的项目名命名. 使用 `--variant` 指定打何种运行类型的包, 连同 `--strip-executable` 选项代替了老的 `--debug` 选项. 如果 `--variant` 没有指定, 默认时release类型的 (去除 Android 和 iOS 的debug信息). 把 `--variant` 设置为 debug 而省略 `--strip-executable` 选项, 就相当于老的 `--debug`选项.

`resolve`
: 解析所有外部依赖库.

支持平台和架构:

`x86_64-darwin` (Defold 1.3.5 及更老版本)
`x86_64-macos` (Defold 1.3.6 及更新版本)
: macOS 64 bit

`arm64-macos` (Defold 1.5.0 and older)
: macOS Apple Silicon (ARM)

`x86_64-win32`
: Windows 64 bit

`x86-win32`
: Windows 32 bit

`x86_64-linux`
: Linux 64 bit

`x86_64-ios`
: iOS macOS 64 bit (iOS 模拟器)

`armv7-darwin` (Defold 1.3.5 及更老版本)
`armv7-ios` (Defold 1.3.6 及更新版本)
: iOS 支持 32-bit `armv7-darwin` 和 64-bit `arm64-darwin` 架构. 默认情况下, `--architectures` 参数值为 `armv7-darwin,arm64-darwin`.

`armv7-android`
: Android 支持 32 bit `armv7-android` 和 64 bit `arm64-android` 架构. 默认情况下, `--architectures` 参数值为 `armv7-android,arm64-android`.

`js-web`
: HTML5 支持 `js-web` 和 `wasm-web` 架构. 默认情况下, `--architectures` 参数值为 `js-web,wasm-web`.

默认情况下, Bob 在当前目录下寻找项目来编译. 切换到 Defold 项目目录下使用 bob, 它会把数据编译到默认输出 *build/default* 目录下.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

还可以把命令连成一行一起执行. 下面的例子包含了解析库, 清理编译目录, 编译数据包然后打包成 macOS 应用 (命名为 *My Game.app*):

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
