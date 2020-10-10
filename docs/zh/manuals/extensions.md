---
title: 为 Defold 编写原生扩展
brief: 本教程介绍了给 Defold 游戏引擎编写原生扩展的方法以及云端编译器的用法.
---

# 原生扩展

如果需要使用 Lua 本身不提供的功能, 比如第三方软件交互或者底层硬件控制, Defold SDK 接受使用 C, C++, Objective C, Java 以及 Javascript 编写的扩展程序, 语言选取取决于目标发布平台. 原生扩展的常见用法有:

- 与特定硬件交互, 例如手机摄像头.
- 与底层软件交互, 例如未提供的底层网络交互要使用 Luasocket 扩展包实现.
- 高性能计算, 数据处理等.

## 编译平台

Defold 提供了一个云端服务器编译方案. 游戏项目的各种依赖, 或者直接引用或者通过 [库项目](/manuals/libraries/) 加入, 都会变成项目内容的一部分. 没有必要重新编译特别版引擎然后分发给开发组成员, 任何成员对项目的编译运行使所有成员都能得到嵌入全部所需库的引擎程序.

![Cloud build](images/extensions/cloud_build.png)

## 项目结构

在项目根目录下为扩展程序建立一个文件夹. 这个文件夹将包含扩展程序所需要的一切, 源代码, 外部库和资源文件. 云编译服务器解析这个结构以便分别获取所需要的各种文件.

```
 myextension/
 │
 ├── ext.manifest
 │
 ├── src/
 │
 ├── include/
 │
 ├── lib/
 │   └──[platforms]
 │
 ├── manifests/
 │   └──[platforms]
 │
 └── res/
     └──[platforms]

```
*ext.manifest*
: 原生扩展程序文件夹下 _必须_ 包含一个 *ext.manifest* 文件. 这是一个 YAML 格式的文件, 编译服务器通过此文件了解扩展项目结构. 这个文件里至少要包含一项就是原生扩展的名字.

*src*
: 包含所有源代码.

*include*
: 包含所有外部引用文件（可选）.

*lib*
: 包含要用到的所有外部编译好的库. 库文件要根据称为 `platform` 或 `architecure-platform` 的子文件夹分类放置, 也就是说什么平台用什么库.

  :[platforms](../shared/platforms.md)

*manifests*
: 包含编译过程所需配置文件（可选）. 详见下文.

*res*
: 包含原生扩展所需的一切资源文件（可选）. 资源文件要根据称为 `platform` 或 `architecure-platform` 的子文件夹分类放置, 也就是说什么平台用什么资源. 其中 `common` 文件夹包含各种平台的通用资源文件.

### Manifest files

*manifests* 包含编译时不同平台所需的配置文件. 配置文件要根据称为 `platform` 的子文件夹分类放置:

* `android` - 这里存放片段配置文件用以与主配置文件混合 ([就像这里介绍的那样](extension-manifest-merge-tool)). 还可以存放 `build.gradle` 文件及其依赖以便 Gradle 可以解析 ([示例](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/android/build.gradle)). 还能存放0个或多个 ProGuard 代码混淆文件 (试验功能).
* `ios` - 这里存放片段配置文件用以与主配置文件混合 ([就像这里介绍的那样](extension-manifest-merge-tool)).
* `osx` - 这里存放片段配置文件用以与主配置文件混合 ([就像这里介绍的那样](extension-manifest-merge-tool)).
* `web` - 这里存放片段配置文件用以与主配置文件混合 ([就像这里介绍的那样](extension-manifest-merge-tool)).


## 共享原生扩展

原生扩展如同其他资源文件一样也可以共享. 如果库项目包含原生扩展文件夹的话, 它就能作为项目依赖库共享给其他人. 详情请见 [库项目教程](/manuals/libraries/).


## 简单示例

从头开始做一个简单的原生扩展. 第一步, 创建 *myextension* 文件夹并加入 *ext.manifest* 文件, 文件中包含扩展名 "MyExtension". 注意这个扩展名会作为一个 C++ 变量名填充在 `DM_DECLARE_EXTENSION` 宏的第一个参数位置上 (见下文).

![Manifest](images/extensions/manifest.png)

```yaml
# C++ symbol in your extension
name: "MyExtension"
```

这个扩展就一个 C++ 文件, *myextension.cpp*, 位于 "src" 文件夹里.

![C++ file](images/extensions/cppfile.png)

源代码如下:

```cpp
// myextension.cpp
// Extension lib defines
#define LIB_NAME "MyExtension"
#define MODULE_NAME "myextension"

// include the Defold SDK
#include <dmsdk/sdk.h>

static int Reverse(lua_State* L)
{
    // The number of expected items to be on the Lua stack
    // once this struct goes out of scope
    DM_LUA_STACK_CHECK(L, 1);

    // Check and get parameter string from stack
    char* str = (char*)luaL_checkstring(L, 1);

    // Reverse the string
    int len = strlen(str);
    for(int i = 0; i < len / 2; i++) {
        const char a = str[i];
        const char b = str[len - i - 1];
        str[i] = b;
        str[len - i - 1] = a;
    }

    // Put the reverse string on the stack
    lua_pushstring(L, str);

    // Return 1 item
    return 1;
}

// Functions exposed to Lua
static const luaL_reg Module_methods[] =
{
    {"reverse", Reverse},
    {0, 0}
};

static void LuaInit(lua_State* L)
{
    int top = lua_gettop(L);

    // Register lua names
    luaL_register(L, MODULE_NAME, Module_methods);

    lua_pop(L, 1);
    assert(top == lua_gettop(L));
}

dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result InitializeMyExtension(dmExtension::Params* params)
{
    // Init Lua
    LuaInit(params->m_L);
    printf("Registered %s Extension\n", MODULE_NAME);
    return dmExtension::RESULT_OK;
}

dmExtension::Result AppFinalizeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result FinalizeMyExtension(dmExtension::Params* params)
{
    return dmExtension::RESULT_OK;
}


// Defold SDK uses a macro for setting up extension entry points:
//
// DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)

// MyExtension is the C++ symbol that holds all relevant extension data.
// It must match the name field in the `ext.manifest`
DM_DECLARE_EXTENSION(MyExtension, LIB_NAME, AppInitializeMyExtension, AppFinalizeMyExtension, InitializeMyExtension, 0, 0, FinalizeMyExtension)
```

注意 `DM_DECLARE_EXTENSION` 宏用来声明扩展程序执行入口. 第一个参数 `symbol` 要与 *ext.manifest* 上的扩展名一致. 本例中没有用到 "update" 或 "on_event" 执行入口, 所以用 `0` 填充了宏的相应参数.

现在就差编译运行了 (<kbd>Project ▸ Build and Launch</kbd>). 带原生扩展的项目会被上传到云编译服务器编译. 如果编译出错, 将会弹出一个包含错误信息的窗口.

测试扩展运行, 新建一个游戏对象和一个脚本组件, 再写一些测试代码:

```lua
local s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
local reverse_s = myextension.reverse(s)
print(reverse_s) --> ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba
```

成功了! 我们从零开始完整地制作了一个扩展程序.


## 扩展程序生命周期

上面提到了 `DM_DECLARE_EXTENSION` 宏用来声明程序执行入口:

`DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)`

入口对应扩展程序的各种生命周期函数, 运行顺序如下:

* 引擎启动
  * 引擎代码运行
  * 扩展 `app_init`
  * 扩展 `init` - Defold API 初始化. 建议扩展程序从这里开始运行并且暴露给Lua脚本.
  * 脚本 `init()` 函数调用.
* 引擎循环
  * 引擎刷新
    * 扩展 `update`
    * 脚本 `update()` 函数调用.
  * 引擎事件 (窗口最大/最小化之类的)
    * 扩展 `on_event`
* 引擎关闭 (或重启)
  * 脚本 `final()` 函数调用.
  * 扩展 `final`
  * 扩展 `app_final`

## 预定义的平台标识

编译器中预定义了如下平台标识:

* DM_PLATFORM_WINDOWS
* DM_PLATFORM_OSX
* DM_PLATFORM_IOS
* DM_PLATFORM_ANDROID
* DM_PLATFORM_LINUX
* DM_PLATFORM_HTML5

## 编译服务器日志

当项目使用了原生扩展, 编译时就会生成编译服务器日志. 编译服务器日志文件 (`log.txt`) 与被编译的项目一起下载到本地, 并保存在项目 build 文件夹的 `.internal/%platform%/build.zip` 文件中.


## ext.manifest 文件

除了扩展名称, ext.manifest 文件还可以包含指定平台的编译参数, 链接参数, 外部程序和链接库. 如果 *ext.manifest* 文件不包含 "platforms" 项, 或者找不到对应的平台配置参数, 编译仍会继续, 只是不加各种编译参数.

Here is an example:

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    armv7-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

### 可用参数项

各个平台可用参数项如下:

* `frameworks` - 加入苹果库 (iOS 和 OSX)
* `flags` - 编译参数
* `linkFlags` - 链接参数
* `libs` - 链接库
* `defines` - 编译预定义
* `aaptExtraPackages` - 导入外部包 (Android)
* `aaptExcludePackages` - 排除内部包 (Android)
* `aaptExcludeResourceDirs` - 排除资源文件夹 (Android)

## 原生扩展举例

* [基础示例](https://github.com/defold/template-native-extension) (本教程所使用的简单示例)
* [Android 扩展示例](https://github.com/defold/extension-android)
* [HTML5 扩展示例](https://github.com/defold/extension-html5)
* [MacOS, iOS 和 Android 的 videoplayer 扩展程序](https://github.com/defold/extension-videoplayer)
* [MacOS 和 iOS 的摄像头扩展程序](https://github.com/defold/extension-camera)
* [iOS 和 Android 的内支付扩展程序](https://github.com/defold/extension-iap)
* [iOS 和 Android 的 Firebase Analytics 扩展程序](https://github.com/defold/extension-firebase-analytics)

[Defold 资源中心](https://www.defold.com/assets/) 也包含有许多原生扩展项目资源.