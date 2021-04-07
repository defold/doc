---
title: Defold 项目编译教程
brief: Bob 是用于 Defold 项目的命令行编译工具. 本教程详述如何使用这个工具.
---

# 编译器 Bob

Bob 是一个用于Defold项目编辑器之外的命令行编译工具.

Bob 用来编译操作 (对应编辑器里的 <kbd>Project ▸ Build</kbd>), 来创建数据档或者创建可独立发布的应用 (对应编辑器里的 <kbd>Project ▸ Bundle ▸ ...</kbd> 选项)

Bob 集合了编译所需的一切, 作为Java包 _JAR_ 发布. 最新的 *bob.jar* 发布在 [Defold 下载页](http://d.defold.com) 和 [GitHub 发布页](https://github.com/defold/defold/releases) 上. 选择一个版本, 下载 *bob/bob.jar*. 运行这个工具, 需要 [OpenJDK 11](https://openjdk.java.net/projects/jdk/11/) 支持.

## 用法

Bob 运行于命令行界面 `java` (再Windows上是 `java.exe`) 后跟bob的jar包作为参数:

```text
$ java -jar bob.jar --help
usage: bob [options] [commands]
 -a,--archive                        编译数据包
 -ar,--architectures <arg>           逗号分割发布架构, 例如 "arm64-android,armv7-android"
                                     
    --binary-output <arg>            指定可执行文件存放地址
                                     默认地址是
                                     "<build-output>/<platform>/"
 -bo,--bundle-output <arg>           打包输出目录
 -br,--build-report <arg>            指定编译报告的存放存放地址
                                     报告为JSON格式
 -brhtml,--build-report-html <arg>   指定编译报告的存放存放地址
                                     报告为HTML格式
    --build-server <arg>             编译服务器 (当使用原生扩展
                                     时使用)
 -d,--debug                          使用dmengine的debug版本(当
                                     编译时). 弃用, 使用--variant
                                     代替
    --defoldsdk <arg>                指定defold sdk (sha1)
                                     使用版本
 -e,--email <arg>                    用户电邮
 -h,--help                           帮助文档
 -i,--input <arg>                    指定源目录, 默认是当前
                                     目录
    --identity <arg>                 指定签名 (iOS)
 -k,--keep-unused                    指定未使用资源仍然打包
                                     输出
 -l,--liveupdate <arg>               要在发布后使用热更新功能
                                     参数填yes
 -mp,--mobileprovisioning <arg>      指定mobileprovisioning profile (iOS)
 -o,--output <arg>                   输出目录. 默认是
                                     "build/default"
 -p,--platform <arg>                 发布平台 (打包时)
 -r,--root <arg>                     指定编译目录. 默认是
                                     当前目录
    --settings <arg>                 指定项目设置文件的
                                     路径. 可以使用多个
                                     文件. 设置根据文件
                                     从左到右应用.
    --strip-executable               去掉dmengine的debug信息
                                     (编译 iOS 或 Android时)
 -tc,--texture-compression <arg>     使用纹理档中指定的
                                     纹理压缩
 -tp,--texture-profiles <arg>        使用纹理压缩档 (弃用)
 -u,--auth <arg>                     用户auth符
    --use-vanilla-lua                只使用 vanilla 源代码 (即
                                     不要字节码)
 -v,--verbose                        冗余输出
    --variant <arg>                  指定使用 debug, release 或者 headless
                                     dmengine的版本 (编译时)
    --version                        打印输出
                                     版本号
    --with-symbols                   生成标记文件 (如果
                                     可用)
    --bundle-format <apk|aab>        使用哪种格式打 Android 包.
    --keystore <arg>                 使用哪个密匙注册
                                     Android 包.
    --keystore-pass <arg>            密匙密码路径用于打 Android 包.
    --keystore-alias <arg>           密匙别名用于打 Android 包.
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

`x86_64-darwin`
: macOS 64 bit

`x86_64-win32`
: Windows 64 bit

`x86-win32`
: Windows 32 bit

`x86_64-linux`
: Linux 64 bit

`x86_64-ios`
: iOS macOS 64 bit (iOS 模拟器)

`armv7-darwin`
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
