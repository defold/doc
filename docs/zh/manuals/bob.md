---
title: Defold 项目编译教程
brief: Bob 是用于 Defold 项目的命令行编译工具. 本教程详述如何使用这个工具.
---

# 编译器 Bob

Bob 是一个用于Defold项目编辑器之外的命令行编译工具.

Bob 用来编译操作 (对应编辑器里的 <kbd>Project ▸ Build</kbd>), 来创建数据档或者创建可独立发布的应用 (对应编辑器里的 <kbd>Project ▸ Bundle ▸ ...</kbd> 选项)

Bob 集合了编译所需的一切, 作为Java包 _JAR_ 发布. 最新的 *bob.jar* 发布在 [Defold 下载页](http://d.defold.com) 和 [GitHub 发布页](https://github.com/defold/defold/releases) 上. 选择一个版本, 下载 *bob/bob.jar*. 运行这个工具, 您需要安装 OpenJDK 11.

下载 OpenJDK 11 的地址:
* https://docs.microsoft.com/en-us/java/openjdk/download#openjdk-11
* https://github.com/adoptium/temurin11-binaries/releases / https://adoptium.net/

比如在 Windows 平台上, 需要下载 OpenJDK 11 的 .msi 安装包.

## 用法

Bob 运行于命令行界面 `java` (再Windows上是 `java.exe`) 后跟bob的jar包作为参数:

```text
$ java -jar bob.jar --help
usage: bob [options] [commands]
-a,--archive                            编译数据包
-ar,--architectures <arg>               逗号分割的发布平台包含的架构列表
    --archive-resource-padding <arg>    游戏包中的资源对齐间隔. 默认值为4.
-bf,--bundle-format <arg>               逗号分割的发布平台格式列表
                                        (Android: 'apk' 和 'aab')
    --binary-output <arg>               指定可执行文件存放地址, 默认地址是
                                        "<build-output>/<platform>/"
-bo,--bundle-output <arg>               打包输出目录
-br,--build-report <arg>                自从 Defold 1.4.6 版本后已弃用! 
                                        使用 --build-report-json 代替
-brjson,--build-report-json <arg>       保存 JSON 编译报告的文件路径位置
                                        (自从 Defold 1.4.6 版本启用)
-brhtml,--build-report-html <arg>       指定编译生成的HTML报告的存放地址
    --build-artifacts <arg>             不指定的话默认为编译engine.
                                        可选项为 'engine', 'plugins'.
                                        以逗号分隔.
    --build-server <arg>                编译服务器 (使用原生扩展时需指定)
-ce,--certificate <arg>                 已弃用! 使用 --keystore 代替
-d,--debug                              已弃用! 使用 --variant=debug 代替
    --debug-ne-upload                   把文件打包為upload.zip后上傳到
                                        編譯服務器
    --defoldsdk <arg>                   指定 defold sdk (sha1) 使用版本
-e,--email <arg>                        用户电邮
-ea,--exclude-archive                   要从打包中排除的资源档案. 以此创建空应用用作编译目标
    --exclude-build-folder              逗号分割的排除目錄列表
-h,--help                               该命令的帮助文档
-i,--input <arg>                        指定源目录, 默认是当前目录
    --identity <arg>                    指定签名 (iOS)
-k,--keep-unused                        把未使用资源也打包进 output
-kp,--key-pass <arg>                    如果开发密钥不同于部署密钥的话
                                        则在这里指定 (Android)
-ks,--keystore <arg>                    用来签名 APKs (Android) 的部署密钥
-ksa,--keystore-alias <arg>             用来签名 (Android) 的 key+cert 别名
-ksp,--keystore-pass <arg>              用来签名 (Android) 的部署密钥密码
-l,--liveupdate <arg>                   要在发布后使用热更新功能, 该参数填 yes

    --manifest-private-key <arg>        用来签名 manifest 和 archive 的私钥

    --manifest-public-key <arg>         用来签名 manifest 和 archive 的公钥

-mp,--mobileprovisioning <arg>          指定 mobileprovisioning profile (iOS)
-o,--output <arg>                       输出目录. 默认是 "build/default"
-p,--platform <arg>                     发布平台 (打包时)
-pk,--private-key <arg>                 已弃用! 使用 --keystore 代替
-r,--root <arg>                         指定编译根目录. 默认是当前目录
    --resource-cache-local <arg>        本地资源缓存地址.
    --resource-cache-remote <arg>       远程资源缓存URL.
    --resource-cache-remote-pass <arg>  远程资源存取认证的密码/令牌.
    --resource-cache-remote-user <arg>  远程资源存取认证的用户名.
    --settings <arg>                    指定项目配置文件的路径. 可以使用多个
                                        文件. 配置文件从左到右依次被应用.
    --strip-executable                  去掉dmengine的debug信息 (编译 iOS 或 Android时)
-tc,--texture-compression <arg>         使用纹理档案中指定的纹理压缩
-tp,--texture-profiles <arg>            已弃用! 使用 --texture-compression 代替
-u,--auth <arg>                         用户认证令牌
   --use-async-build-server             为编译服务器启用异步编译处理 (使用原生扩展时)
   --use-uncompressed-lua-source        使用未压缩未加密的明文Lua源代码代替二进制文件
   --use-vanilla-lua                    已弃用! 使用 --use-uncompressed-lua-source 代替

-v,--verbose                            冗余输出
    --variant <arg>                     指定使用 debug, release 或者 headless
                                        的dmengine版本 (编译时)
    --version                           打印输出版本号
    --with-symbols                      生成标记文件 (如果可用)
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

`js-web` : HTML5 支持 `js-web` 和 `wasm-web` 架构. 默认情况下, `--architectures` 参数值为 `js-web,wasm-web`.

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
