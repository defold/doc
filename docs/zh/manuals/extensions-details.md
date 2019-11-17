---
title: 原生扩展 - 详述
brief: 本教程介绍了有关编译系统用来编译原生扩展的一些细节.
---

# Defold 编译器 （流程应该是 编译--构建--打包， 为了方便这里把编译和构建统称为了编译）

为了让你的扩展整合更加方便，我们这里列举了一些编译相关的细节.

在创建 Defold 引擎扩展的时候，要考虑一些事情.
对于更全面的如何开发跨平台原生代码以及扩展/Lua API的使用，请参考 [原生扩展 - 最佳实践](/manuals/extensions-best-practices)

## C++ 版本

在引擎里我们用的都是不会高于C++98的版本. 你在开发扩展时可能使用了更高的版本, 注意高版本可能会引入 ABI 的变化. 这可能导致你无法在引擎或者asset store里使用你的扩展.

要记住创建代码库 (比如扩展)时, 最好选择最具兼容性的版本.

## 工具链

Clang - macOS, iOS, Win32, Android
GCC - Linux

*我们打算以后也给Linux使用 clang *

### SDK 版本

* Android: NDK 20r, Build Tools 23.0.2, Api Level 16 for armv7 and Api level 21 for arm64
* iOS: iPhoneOS11.2.sdk
* MacOS: MacOSX10.13.sdk
* Windows: WindowsKits 8.1 + 10.0, Microsoft Visual Studio 14.0
* Linux: Ubuntu 16.04, gcc 5.4.0, libssl-dev, uuid-dev, libxi-dev, libopenal-dev, libgl1-mesa-dev, libglw1-mesa-dev, freeglut3-dev
* Html5: Emscripten 1.38.0,

### C++ 版本 + ABI 兼容

* Linux: `GCC 5.4.0`
* Android:`GCC 4.9`
* Html5: `Emscripten 1.35.0`
* Win32: `Microsoft Visual Studio 14.0` 或 `clang-6.0`
* iOS/MacOS: `apple-clang` 或 `clang-6.0`

对于 iOS/MacOS, 我们分别使用了 `-miphoneos-version-min=8.0` 和 `-mmacosx-version-min=10.7`.

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