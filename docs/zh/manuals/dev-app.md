---
title: 在设备上运行开发用app
brief: 本教程介绍了如何在设备上安装开发用app以方便开发流程.
---

# 移动端开发用app

开发用app 让你可以通过wifi把内容推送到设备上. 这样进行修改测试的时候就不用反复打包安装了. 只需要在设备上安装开发用app, 打开app然后在编辑器里选择设备作为推送目标即可.

## 安装开发用app

Debug  模式下编译的任何 iOS 或 Android 应用都可以作为开发用app. 事实上, 我们推荐这么做因为开发用app包含正确的项目配置而且拥有和开发时使用的相同的 [原生扩展](/manuals/extensions/). 还有 [Defold 的独立项目](https://github.com/defold/dev-app) (不包含原生扩展的项目) 也设计做为开发用app使用.

![launch](images/dev-app/launch.png)

::: sidenote
只有在不使用 [原生扩展](/manuals/extensions/) 的项目可以使用我们提供的开发用apk. 否则你需要自己手动打debug包并且加入你所使用的原生扩展.
:::

从 Defold 1.4.0 版本开始可以给项目打空的 debug 包. 使用这个选项可以创建带原生扩展的应用版本, 适合于教程里提到的开发迭代.

![content less bundle](images/dev-app/contentless-bundle.png)

### Installing on iOS

依照 [iOS 教程介绍的步骤](/manuals/ios/#creating-an-ios-application-bundle) 打包 iOS 应用. 记得 variant 要选择 Debug!

### Installing on Android

依照 [Android 教程介绍的步骤](https://defold.com/manuals/android/#creating-an-android-application-bundle) 打包 Android 应用.

## 启动游戏

要在设备上启动游戏, 应用与编辑器之间需要互联, 可以使用 wifi 也可以使用 USB 线缆 (见下文).

1. 确保编辑器处于运行中.
2. 在设备上启动开发用app.
3. 在编辑器的 <kbd>Project ▸ Targets</kbd> 中选择设备.
4. 选择 <kbd>Project ▸ Build</kbd> 运行游戏. 如果用网络连接的话可能需要等一小会儿.
5. 游戏运行时, 就可以照常使用 [热重载](/manuals/hot-reload/) 功能了.

### 在 Windows 上使用 USB 连接 iOS 设备

要在 Windows 上使用 USB 连接运行于 iOS 设备上的app, 首先 [安装 iTunes](https://www.apple.com/lae/itunes/download/). 安装完之后还需从iOS设备的设置菜单里 [开启 Personal Hotspot](https://support.apple.com/en-us/HT204023). 如果跳出 "Trust This Computer?" 则选择 Trust. 这样设备就会出现在 <kbd>Project ▸ Targets</kbd> 列表中了.

### 在 Linux 上使用 USB 连接 iOS 设备

Linux 上同样开启 Personal Hotspot 然后 "Trust This Computer".

### 在 macOS 上使用 USB 连接 iOS 设备

当设备与 macOS 通过 USB 连线时, 新版本 iOS 能自动开启连接,  <kbd>Project ▸ Targets</kbd> 会自动显示出设备.

老iOS设备还是同样开启 Personal Hotspot 然后 "Trust This Computer".

### 在 macOS 上使用 USB 连接 Android 设备

当设备处于 USB 共享模式时,  可以通过 USB 连接设备与 macOS. 在 macOS 上需要安装 [HoRNDIS](https://joshuawise.com/horndis#available_versions) 这类的第三方驱动程序. 当 HoRNDIS 安装好后还需要在 Security & Privacy 设置里允许其运行. 设备上开启 USB 共享模式后就会出现在 <kbd>Project ▸ Targets</kbd> 列表中了.

### 在 Windows 或 Linux 上使用 USB 连接 Android 设备

同样在设备上开启 USB 共享模式后就会出现在 <kbd>Project ▸ Targets</kbd> 列表中了.

## 故障排除

无法下载应用
: 确保你的设备 UDID 包含在手机应用签名 provisioning 中.

Targets 菜单没有设备
: 确保设备于计算机处于相同 wifi 网络之下. 确保使用 Debug 模式编译开发用app.

弹出消息说版本不匹配
: 这是由于更新了编辑器没更新应用. 用新编辑器重新编译安装应用即可.
