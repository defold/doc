---
title: 原生扩展 - Defold SDK
brief: 本教程介绍了创建原生扩展时如何使用 Defold SDK.
---

# Defold SDK

Defold SDK 包含了应用运行的原生平台底层接口与高层Lua逻辑接口来实现原生扩展的功能.

## 用法

你可以通过引用 `dmsdk/sdk.h` 头文件来使用 Defold SDK:

    #include <dmsdk/sdk.h>

可用的SDK功能都在 [API文档](/ref/dmExtension/) 里写明了. SDK包含以下命名空间和功能:

* [Align](/ref/dmAlign/) - 公共宏. 用来保证编译器兼容
* [Array](/ref/dmArray/) - 具有边界检测的模板化数组.
* [Buffer](/ref/dmBuffer/) - 数据缓存功能是不同平台互相交流的主要途径. [Lua API](/ref/buffer/) 同样具有缓存功能.
* [Condition Variable](/ref/dmConditionVariable/) - 条件变量.
* [ConfigFile](/ref/dmConfigFile/) - 配置文件的存取功能. 配置文件是 game.project 文件的编译后版本.
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
* [Web Server](/ref/dmWebServer/) - 基于dmHttpServer的高级单线程web服务器.
* [Shared Library](/ref/sharedlibrary/) - 共享库导入导出功能.
* [Sony vector Math Library](../assets/Vector_Math_Library-Overview.pdf) - Sony 矢量计算库 主要为了3D图像和3D, 4D矢量运算, 矩阵运算和四元运算.

如果需要 `dmsdk/sdk.h` 头文件请到 [Defold 官方 Github 库](https://github.com/defold/defold/blob/dev/engine/sdk/src/dmsdk/sdk.h) 查询, 这里有 [各种命名空间的头文件](https://github.com/defold/defold/tree/dev/engine/dlib/src/dmsdk/dlib).

