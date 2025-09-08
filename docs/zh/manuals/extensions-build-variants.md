---
title: 原生扩展 - Build variants
brief: 本手册介绍了 Defold 能创建的各种 Build variants 以及它们如何与原生扩展和引擎交互。
---

:[Build Variants](../shared/build-variants.md)

## App Manifest

不但可以为引擎加入原生扩展功能，还可以从引擎中剔除一些部分。比如你不需要物理引擎，就可以从应用中去除。关于如何去除引擎功能参见[应用清单手册](/manuals/app-manifest)。

### 上下文组合

实际上 app manifest 有着与 extension manifest 相同的结构和语法。这使我们能够在最终编译时为每个平台混合上下文配置。

而且，Defold 自身，有其基础 build manifest（`build.yml`）。编译每个扩展时，这些文件做如下混合：

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

用户可以覆盖引擎和每个扩展的默认行为。而且，对于最终链接阶段，我们混合了 app manifest 与 defold manifest：

	manifest = merge(game.appmanifest, build.yml)

### 语法

这是一个参考示例：

```yml
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
```

#### 白名单

对于所有关键字，我们提供白名单过滤。这样可以避免非法路径处理和访问编译上载文件夹之外的文件。

#### linkFlags

可以在这里添加指定平台的编译标志。

#### libs

此标志仅在需要添加平台或者 Defold SDK 里的库时使用。应用的扩展库是自动添加的，不应在这里添加。下面是从引擎中剔除 3D 物理的例子：

    x86_64-linux:
        context:
            excludeLibs: ["physics","LinearMath","BulletDynamics","BulletCollision"]
            excludeSymbols: []
            libs: ["physics_2d"]
            linkFlags: []

#### Exclude flags

此标志用于剔除平台上下文已经预先定义的东西。下面是从引擎中剔除 Facebook 扩展的例子（注意 `(.*)` 是帮助去掉正确元素而使用的正则表达式）。

    armv7-android:
        context:
            excludeLibs: ["facebookext"]
            excludeJars: ["(.*)/facebooksdk.jar","(.*)/facebook_android.jar"]
            excludeSymbols: ["FacebookExt"]
            libs: []
            linkFlags: []

#### 所有 flags、libraries、symbols 在哪？

与其在这里列举，我们不如努力把 manifest 的编辑功能加入编辑器，让用户使用更方便。

与此同时，[Manifestation](https://britzl.github.io/manifestation/) 工具也会持续更新。
