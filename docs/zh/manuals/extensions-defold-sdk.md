---
title: 原生扩展 - Defold SDK
brief: 本手册介绍了创建原生扩展时如何使用 Defold SDK。
---

# Defold SDK

Defold SDK 包含了声明原生扩展所需的功能，以及与应用运行的原生平台底层接口和创建游戏逻辑的高层Lua层进行交互的功能。

## 用法

你可以通过引用 `dmsdk/sdk.h` 头文件来使用 Defold SDK:

    #include <dmsdk/sdk.h>

可用的SDK功能和命名空间在我们的 [API参考文档](/ref/overview_cpp) 中有详细说明。Defold SDK头文件作为单独的 `defoldsdk_headers.zip` 压缩包包含在每个Defold [GitHub发布版本](https://github.com/defold/defold/releases)中。你可以在你选择的编辑器中使用这些头文件进行代码补全。

