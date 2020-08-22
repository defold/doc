---
title: 打包应用
brief: 本教程介绍了如何打包应用.
---

# 打包应用

开发项目时常常需要在目标平台上进行测试. 开发中越早发现性能问题越好解决. 同样鼓励在各平台间做测试以便发现诸如shader之类的兼容问题. 在做手机开发时可以使用 [手机开发应用](/manuals/dev-app/) 把内容推送到手机上, 避免反复的安装和卸载.

你可以在 Defold 编辑器中生成其支持的所有平台应用, 不需要外界工具辅助. 也可以在控制台使用命令行工具打包应用. 如果应用里包含 [原生扩展](/manuals/extensions) 的话打包时需要网络连接.

## 从编辑器中打包

使用 Project 菜单的 Bundle 选项进行打包:

![](images/bundling/bundle_menu.png)

选择不同的打包平台会出现不同的对话窗.

### 编译报告

有一个编译选项控制编译时是否生成报告. 从报告中可以方便检查游戏包中各个资源占用的空间. 在编译时打开 *Generate build report* 选项即可.

![build report](images/profiling/build_report.png){srcset="images/profiling/build_report@2x.png 2x"}

关于编译报告详情请见 [调试教程](/manuals/profiling/#编译报告).


### Android

建立安卓应用 (.apk 文件) 详见 [安卓教程](/manuals/android/#creating-an-android-application-bundle).

### iOS

建立苹果移动应用 (.ipa 文件) 详见 [iOS 教程](/manuals/ios/#creating-an-ios-application-bundle).

### OSX

建立Mac系统应用 (.app 文件) 详见 [macOS 教程](/manuals/macos).

### Linux

建立Linux应用无需特别设置 "game.project" [项目配置文件](/manuals/project-settings/#linux).

### Windows

建立Windows应用 (.exe 文件) 详见 [Windows 教程](/manuals/windows).

### HTML5

建立HTML5应用及其参数设置详见 [HTML5 教程](/manuals/html5/#打包html5应用).

#### Facebook Instant Games

可以为 Facebook Instant Games 打包成 HTML5 应用的一种特殊版本. 这一过程详见 [Facebook Instant Games 教程](/manuals/instant-games/).

## 命令行打包

日常开发中一般使用 Defold 编辑器编译和打包应用. 如果需要自动生成机制, 比如发布新版本时批处理所有平台或者使用持续集成环境持续生成最新版本. 可以使用 [Bob 命令行工具](/manuals/bob/) 编译和打包.
