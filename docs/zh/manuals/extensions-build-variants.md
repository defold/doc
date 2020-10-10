---
title: 原生扩展 - Build variants
brief: 本教程介绍了 Defold 能创建的各种 Build variants 以及它们如何与原生扩展和引擎交互.
---

# 原生扩展 - Build variants

## Build variants

打包游戏时, 需要选择你想用的引擎类型.

  * Debug
  * Release
  * Headless

不同类型即是 `Build variants`

注意: 使用 `Build and run` 时使用的是 debug 版引擎.

### Debug

此版本保留调试功能, 例如 profiling, logging 和 hot reload. 开发阶段使用此版本.

### Release

此版本移除调试功能. 准备发布到应用商店时使用此版本.

### Headless

此版本没有图像和声音. 也就是说它可以 CI 服务器上进行 unit/smoke 测试, 甚至可以在云端作为服务器程序使用.

## App Manifest

不但可以为引擎加入原生扩展功能, 还可以从引擎中剔除一些部分. 比如你不需要物理引擎, 就可以从应用中去除.

我们通过 `App Manifest` (.appmanifest) 文件支持这个功能. 在这个文件里, 你可以配置哪些库或 symbols 需要去除, 或者增加编译选项

此功能尚在开发中.

### 上下文组合

实际上 app manifest 有着与 extension manifest 相同的结构和语法. 这使我们能够在最终编译时为每个平台混合上下文配置.

而且, Defold 自身, 有其基础 build manifest (`build.yml`). 编译每个扩展时, 这些文件做如下混合:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

用户可以覆盖引擎和每个扩展的默认行为. 而且, 对于最终链接阶段, 我们混合了 app manifest 与 defold manifest:

	manifest = merge(game.appmanifest, build.yml)

### 编辑

目前, 这些文件可以手动编辑, 但是推荐使用 [Manifestation](https://britzl.github.io/manifestation/) 工具生成 app manifest. 最终, app manifest 文件的创建和修改功能会并入编辑器中.

### 语法

这是 [Manifestation](https://britzl.github.io/manifestation/) 工具生成的一个结构 (很有可能会改变. 不要直接从这里拷贝. 而要使用最新的在线工具):

	platforms:
	    x86_64-osx:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    x86_64-linux:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    js-web:
	        context:
	            excludeLibs: []
	            excludeJsLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    wasm-web:
	        context:
	            excludeLibs: []
	            excludeJsLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    x86-win32:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    x86_64-win32:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    armv7-android:
	        context:
	            excludeLibs: []
	            excludeJars: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    armv7-ios:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    arm64-ios:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []


#### 白名单

对于所有关键字, 我们提供白名单过滤. 这样可以避免非法路径处理和访问编译上载文件夹之外的文件.

#### linkFlags

可以在这里添加指定平台的编译标志.

#### libs

此标志仅在需要添加平台或者 Defold SDK 里的库时使用. 应用的扩展库是自动添加的, 不应在这里添加. 下面是从引擎中剔除 3D 物理的例子:

    x86_64-linux:
        context:
            excludeLibs: ["physics","LinearMath","BulletDynamics","BulletCollision"]
            excludeSymbols: []
            libs: ["physics_2d"]
            linkFlags: []

#### Exclude flags

此标志用于剔除平台上下文已经预先定义的东西. 下面是从引擎中剔除 Facebook 扩展的例子 (注意 `(.*)` 是帮助去掉正确元素而使用的正则表达式).

    armv7-android:
        context:
            excludeLibs: ["facebookext"]
            excludeJars: ["(.*)/facebooksdk.jar","(.*)/facebook_android.jar"]
            excludeSymbols: ["FacebookExt"]
            libs: []
            linkFlags: []

#### 所有 flags, libraries, symbols 在哪？

与其在这里列举我们不然努力把 manifest 的编辑功能加入编辑器, 让用户使用更方便.

与此同时, [Manifestation](https://britzl.github.io/manifestation/) 工具也会持续更新.
