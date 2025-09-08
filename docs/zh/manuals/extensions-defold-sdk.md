---
title: 原生扩展 - Defold SDK
brief: 本手册介绍了创建原生扩展时如何使用 Defold SDK.
---

# Defold SDK

Defold SDK 包含了声明原生扩展所需的功能，以及与应用运行的原生平台底层接口和创建游戏逻辑的高层Lua层进行交互的功能.

## 用法

你可以通过引用 `dmsdk/sdk.h` 头文件来使用 Defold SDK:

    #include <dmsdk/sdk.h>

可用的SDK功能和命名空间在我们的 [API参考文档](/ref/overview_cpp) 中有详细说明. Defold SDK头文件作为单独的 `defoldsdk_headers.zip` 压缩包包含在每个Defold [GitHub发布版本](https://github.com/defold/defold/releases)中. 你可以在你选择的编辑器中使用这些头文件进行代码补全.

* [Align](/ref/dmAlign/) - 公共宏. 用来保证编译器兼容
* [Array](/ref/dmArray/) - 具有边界检测的模板化数组.
* [Buffer](/ref/dmBuffer/) - 数据缓存功能是不同平台互相交流的主要途径. [Lua API](/ref/buffer/) 同样具有缓存功能.
* [Condition Variable](/ref/dmConditionVariable/) - 条件变量.
* [ConfigFile](/ref/dmConfigFile/) - 配置文件的存取功能. 配置文件是 *game.project* 文件的编译后版本.
* [Connection Pool](/ref/dmConnectionPool/) - Socket连接池功能.
* [Crypt](/ref/dmCrypt/) - 加密功能.
* [DNS](/ref/dmDNS/) - DNS功能.
* [Engine](/ref/dmEngine/) - 引擎用于处理配置文件, 内部web服务器, 游戏对象等核心功能.
* [Extension](/ref/dmExtension/) - 创建和控制引擎原生扩展库功能.
* [Game Object](/ref/dmGameObject/) - 游戏对象管理功能.
* [Graphics](/ref/dmGraphics/) - 平台相关的原生图像功能.
* [Hash](/ref/dmHash/) - 哈希功能.
* [HID](/ref/dmHid/) - 通用程序化输入功能.
* [HTTP Client](/ref/dmHttpClient/) - HTTP客户端交互功能.
* [Json](/ref/dmJson/) - 平台无关的json文件解析器.
* [Log](/ref/dmLog/) - 日志功能.
* [Math](/ref/dmMath/) - 数学库.
* [Mutex](/ref/dmMutex/) - 平台无关的互斥锁同步基础功能.
* [SSL Socket](/ref/dmSSLSocket/) - 加密socket功能.
* [Script](/ref/dmScript/) - 内置脚本运行环境.
* [Socket](/ref/dmSocket/) - 非加密socket功能.
* [String Functions](/ref/dmStringFunc/) - 字符串管理功能.
* [Thread](/ref/dmThread/) - 线程创建功能.
* [Time](/ref/dmTime/) - 时间与计时功能.
* [URI](/ref/dmURI/) - URI管理功能.
* [Web Server](/ref/dmWebServer/) - 基于`dmHttpServer`的高级单线程web服务器.
* [Shared Library](/ref/sharedlibrary/) - 共享库导入导出功能.
* [Sony vector Math Library](../assets/Vector_Math_Library-Overview.pdf) - Sony 矢量计算库 主要为了3D图像和3D, 4D矢量运算, 矩阵运算和四元运算.

