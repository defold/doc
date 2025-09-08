---
title: 原生扩展 - 最佳实践
brief: 本手册介绍了开发原生扩展的最佳实践。
---

# 最佳实践

编写跨平台代码可能很困难，但是通过一些方法可以更易于开发与维护。

## 编写原生代码

在 Defold 源码中，C++ 的使用非常有限，大多数代码非常类似于 C。除了少数容器类外，几乎没有模板，因为模板会增加编译时间和可执行文件大小。

### C++ 版本

Defold 源码是使用每个编译器的默认 C++ 版本构建的。Defold 源码本身使用的 C++ 版本不高于 C++98。虽然可以使用更高版本来构建扩展，但更高版本可能带来 ABI 变化。这可能会使得无法在引擎或[资源门户](/assets)中将一个扩展与其他扩展一起使用。

Defold 源码避免使用 C++ 的最新功能或版本。主要是因为在构建游戏引擎时不需要新功能，而且追踪 C++ 的最新功能是一项耗时的任务，真正掌握这些功能需要大量宝贵时间。

这对扩展开发者还有一个额外的好处，即 Defold 维护了稳定的 ABI。还值得指出的是，使用最新的 C++ 功能可能会由于不同平台的支持程度不同而阻止代码在不同平台上编译。

### 标准模板库 - STL

由于 Defold 引擎不使用任何 STL 代码，除了一些算法和数学函数（`std::sort`、`std::upper_bound` 等），在你的扩展中使用 STL 可能是可行的。

再次记住，当你的扩展与其他扩展或第三方库一起使用时，ABI 不兼容性可能会阻碍你。

避免使用（重度模板化的）STL 库，也可以改善我们的构建时间，更重要的是，减少可执行文件大小。

#### 字符串

在 Defold 引擎中，使用 `const char*` 而不是 `std::string`。使用 `std::string` 是在混合不同版本的 C++ 或编译器版本时的常见陷阱，因为它可能导致 ABI 不匹配。使用 `const char*` 和一些辅助函数可以避免这种情况。

### 使函数隐藏

如果可能，在编译单元本地函数上使用 `static` 关键字。这让编译器可以进行一些优化，既可以提高性能，也可以减少可执行文件大小。

## 第三方库

当选择要使用的第三方库时（无论语言），请考虑以下几点：

* 功能 - 它是否解决了你遇到的特定问题？
* 性能 - 它是否会在运行时带来性能成本？
* 库大小 - 最终可执行文件会增大多少？这是否可接受？
* 依赖 - 它是否需要额外的库？
* 支持 - 库的状态如何？它是否有很多未解决的问题？它是否仍在维护？
* 许可证 - 是否可以在这个项目中使用？


## 开源依赖

始终确保你可以访问你的依赖项。例如，如果你依赖于 GitHub 上的某些内容，没有什么可以阻止该存储库被删除，或者突然改变方向或所有权。你可以通过分叉存储库并使用你的分叉而不是上游项目来减轻这种风险。

记住，库中的代码将被注入到你的游戏中，所以确保库做了它应该做的事情，而不是其他事情！


## 项目结构

创建扩展时，有几件事可以帮助开发和维护它。

### Lua API

应该只有一个 Lua API，并且只有一个实现。这使得在所有平台上具有相同的行为变得更加容易。

如果相关平台不支持该扩展，建议根本不注册 Lua 模块。这样你可以通过检查 nil 来检测支持：

    if myextension ~= nil then
        myextension.do_something()
    end

### 文件夹结构

以下文件夹结构经常用于扩展：

    /root
        /input
        /main                            -- 实际示例项目的所有文件
            /...
        /myextension                     -- 扩展的实际根文件夹
            ext.manifest
            /include                     -- 外部包含，其他扩展使用
            /libs
                /<platform>              -- 所有支持平台的外部库
            /src
                myextension.cpp          -- 扩展的 Lua api 和扩展生命周期函数
                                            还包含你的 Lua api 函数的通用实现。
                myextension_private.h    -- 每个平台将实现的内部 api（即 `myextension_Init` 等）
                myextension.mm           -- 如果 iOS/macOS 需要原生调用。为 iOS/macOS 实现 `myextension_Init` 等
                myextension_android.cpp  -- 如果 Android 需要 JNI 调用。为 Android 实现 `myextension_Init` 等
                /java
                    /<platform>          -- Android 需要的任何 java 文件
            /res                         -- 平台需要的任何资源
            /external
                README.md                -- 关于如何构建或打包任何外部库的说明/脚本
        /bundleres                       -- 应该为（参见 game.project 和 [bundle_resources 设置]([physics scale setting](/manuals/project-settings/#project))）捆绑的资源
            /<platform>
        game.project
        game.appmanifest                 -- 任何额外的应用配置信息


注意，`myextension.mm` 和 `myextension_android.cpp` 只有在为该平台进行特定的原生调用时才需要。

#### 平台文件夹

在某些地方，平台架构被用作文件夹名称，以了解在编译/捆绑应用程序时使用哪些文件。这些形式如下：

    <architecture>-<platform>

当前列表是：

    arm64-ios, armv7-ios, x86_64-ios, arm64-android, armv7-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

因此，例如，将平台特定的库放在：

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a
