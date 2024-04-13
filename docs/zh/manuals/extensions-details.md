---
title: 原生扩展 - 详述
brief: 本教程介绍了有关编译系统用来编译原生扩展的一些细节.
---

# Defold 编译器

为了让你的扩展整合更加方便, 我们这里列举了一些编译相关的细节.

在创建 Defold 引擎扩展的时候, 要考虑一些事情. 对于更全面的如何开发跨平台原生代码以及扩展/Lua API的使用, 请参考 [原生扩展 - 最佳实践](/manuals/extensions-best-practices)

## C++ 版本

在引擎里我们用的都是不会高于C++98的版本. 你在开发扩展时可能使用了更高的版本, 注意高版本可能会引入 ABI 的变化. 这可能导致你无法在引擎或者asset store里使用你的扩展.

要记住创建代码库 (比如扩展)时, 最好选择最具兼容性的版本.

## 工具链

### SDK 版本

* Android: NDK r25b, Build Tools 33.0.1, Api Level 19 for armv7 and Api level 21 for arm64
* iOS: iPhoneOS17.2.sdk
* macOS: MacOSX14.2.sdk
* Windows: WindowsKits 10.0, Microsoft Visual Studio 2022
* Linux: Ubuntu 20.04, clang 17, locales, libssl-dev, openssl, libtool, autoconf, automake, build-essential, uuid-dev, libxi-dev, libopenal-dev, libgl1-mesa-dev, libglw1-mesa-dev, freeglut3-dev
* Html5: Emscripten 3.1.55

### C++ 版本 + ABI 兼容

* Linux: `clang 17`
* Android:`clang` using `NDK r25b`
* Html5: `Emscripten 3.1.55`
* Win32: `Microsoft Visual Studio 2022` (`clang 17` on build server)
* iOS/macOS: `apple-clang` (`clang 17` on build server)

对于 iOS/macOS, 我们分别使用了 `-miphoneos-version-min=11.0` 和 `-mmacosx-version-min=10.13` 参数.

由于我们不指定 C++ 版本, 所以各个编译器都使用了默认设置.

## Win32 + Clang

近来的版本能够在Windows上使用clang.
这使得我们编译服务器运行更快速, 同时打包更精简.

## 静态链接

自定义引擎使用静态链接进行编译.
主要原因时 iOS 版本 < 8 时, app store 不支持运行一个 .ipa 里的多个可执行程序.

## 没有 C++ Exceptions

在引擎里我们不使用任何C++ Exceptions.
游戏引擎基本用不到, 因为 (大多数) 游戏数据在引擎开发时是未知的.
移除 C++ exceptions 支持能够减小包体提升运行效率.
