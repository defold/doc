---
title: 原生扩展 - Defold SDK
brief: 本教程介绍了创建原生扩展时如何使用 Defold SDK.
---

# Defold SDK

Defold SDK 包含了应用运行的原生平台底层接口与高层Lua逻辑接口来实现原生扩展的功能.

## 用法

你可以通过引用 `dmsdk/sdk.h` 头文件来使用 Defold SDK:

    #include <dmsdk/sdk.h>

这个头文件并不公开发布但是SDK的所有功能都在 [API](/ref/dmExtension/) 里写明了. SDK包含以下命名空间和功能:

* [Align](/ref/dmAlign/) - 公共宏. 用来保证编译器兼容
* [Array](/ref/dmArray/) - 具有边界检测的模板化数组.
* [Buffer](/ref/dmBuffer/) - 数据缓存功能是不同平台互相交流的主要途径. [Lua API](/ref/buffer/) 同样具有缓存功能.
* [Condition Variable](/ref/dmConditionVariable/) - 条件变量.
* [ConfigFile](/ref/dmConfigFile/) - 配置文件的存取功能. 配置文件是 game.project 文件的编译后版本.
* [Extension](/ref/dmExtension/) - 创建和控制引擎扩展的功能.
* [Graphics](/ref/dmGraphics/) - 特定原生平台的图像功能.
* [Hash](/ref/dmHash/) - 哈希功能.
* [Json](/ref/dmJson/) - 平台与关的json解析器.
* [Log](/ref/dmLog/) - 日志功能.
* [Mutex](/ref/dmMutex/) - 平台无关的互斥同步基础功能
* [Script](/ref/dmScript/) - 内建脚本运行环境.
* [Shared Library](/ref/sharedlibrary/) - 共享库导入导出功能
* [Sony vector Math Library](/manuals/assets/Vector_Math_Library-Overview.pdf) - Sony 矢量计算库 主要为了3D图像和3D, 4D矢量运算, 矩阵运算和四元运算.
