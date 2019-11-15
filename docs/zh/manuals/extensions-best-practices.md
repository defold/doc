---
title: 原生扩展 - 最佳实践
brief: 本教程介绍了开发原生扩展的最佳实践.
---

# 最佳实践

编写跨平台代码可能很困难, 但是通过一些方法可以更易于开发与维护. 本教程列举了 Defold 与跨平台原生代码共同工作的 API 和方法.

## Defold 代码

在 Defold 引擎中我们很少使用 C++ 代码. 事实上, 大多数是 C-like 代码. 除了少数容器类外, 我们去掉了模板, 因为模板会增加编译时间和包体大小.

### C++ 版本

Defold 源码使用默认 C++ 版本编译.

我们不用最新的 C++ 版本及特性. 主要因为默认版本对于游戏引擎足够用了. 追寻最新 C++ 版本特性相当耗费时间.

这也有助于向扩展开发者提供稳定 ABI. 而且使用最新 C++ 特性的话很可能会在不同平台上造成编译问题.

### 标准模板库 - STL

Defold 引擎不支持 STL 代码, 除了某些算法和数学库 (std::sort, std::upper_bound 等), 但是你的扩展里可以使用 STL.

再次注意 ABI 的不兼容性可能使你使用其他扩展或者第三方库造成困难.

去掉 (重模板化的) STL 库, 还能减少编译时间, 更重要的是, 减小应用体积.

#### 字符串

在 Defold 引擎中, 我们使用 `const char*` 代替了 `std::string`.

`std::string` 使得 C++ 不同版本混合编译造成困难: 原因是 ABI 不匹配.
所以我们选择使用 `const char*` 及相关工具函数代替.

### 函数隐藏

本地函数尽量使用 `static` 关键字定义. 这样便于编译器优化, 提高性能减小应用体积.

## 第三方库

当我们选用第三方库时 (不管由什么语言编写), 至少需要考虑这些事情:

* 功能 - 这个库满足你的功能要求了吗?
* 性能 - 运行时是否需要消耗大量性能?
* 体积 - 会给包体增大多少体积?是否在可接受范围内?
* 依赖 - 是否依赖其他库?
* 支持 - 这个库是个什么样的状态? 是否有许多bug? 是否还在维护?
* 证书 - 是否可以合法使用?


## 开源依赖

确定你能访问你的依赖库. 比如说在 GitHub 上托管的库, 随时可能被移除, 突然改变开发方向或者改变拥有者维护者. 如果你fork了这个库就能减少这些变化带来的损失.

库代码是直接注入你的游戏中的, 所以需要保证它在满足你的要求的前提下不会在后台做什么小动作!


## 项目结构

当你创建扩展, 开发和维护时是有些技巧的.

### Lua api

应该只有一个 Lua api, 只有一个实现方法. 这样有助于在所有平台上保持一致的表现.

如果某平台不支持这个扩展, 建议不要注册 Lua 模块.
这样就可以通过检查非 nil 来判断对扩展的支持性:

    if myextension ~= nil then
        myextension.do_something()
    end

### 文件夹结构

这是我们开发扩展使用的常用结构.

    /root
        /input
        /main                            -- 示例项目根目录
            /...
        /myextension                     -- 扩展根目录
            ext.manifest
            /include                     -- 其他扩展使用的外部包含
            /libs
                /<platform>              -- 各个平台使用的外部包含
            /src
                myextension.cpp          -- 扩展的 Lua api 及其生命周期函数
                                            还包含 Lua api 功能的通用实现方法.
                myextension_private.h    -- 每个平台需要实现的内部 api (也就是 `myextension_Init` 之类的功能)
                myextension.mm           -- 如果需要调用 iOS/macOS 原生功能. 就要为 iOS/macOS 实现 `myextension_Init` 之类的功能 
                myextension_android.cpp  -- 如果需要调用 Android 的JNI. 就要为 Android 实现 `myextension_Init` 之类的功能
                /java
                    /<platform>          -- Android 需要的java文件
            /res                         -- 平台需要的资源文件
            /external
                README.md                -- 扩展相关编译打包的说明/脚本
        /bundleres                       -- 需要打包的资源 (参见 game.project 以及 [bundle_resources 设置](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- 其他应用设置


注意 `myextension.mm` 和 `myextension_android.cpp` 只在调用平台特定原生功能时使用.

#### 平台文件夹

在某些地方, 需要针对架构平台命名文件夹, 以便应用编译/打包时使用正确的文件.
结构是这样的:

    <architecture>-<platform>

目前支持的有:

    arm64-ios, armv7-ios, x86_64-ios, arm64-android, armv7-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

比如, 这么放置平台相关库:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a
