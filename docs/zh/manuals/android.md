---
title: Defold 的 Android 平台开发
brief: 本教程介绍了如何在 Defold 中进行 Android 设备应用的开发
---

# Android 开发

Android 设备允许自由允许你开发的应用. 可以很容易地编译好游戏拷贝到 Android 设备上. 本手册介绍了对于 Android 游戏的打包步骤. 推荐开发时, 从 [开发应用](/manuals/dev-app) 上运行游戏因为可以通过无线连接设备进行代码和内容的热重载.

## Android 和 Google Play 签名

Android 需要安装的应用都进行数字签名. 不像 iOS 证书都需要由 Apple 签发, Android 允许开发者自己创建证书和密匙来对应用签名.

创建证书和密匙的过程看似复杂但是开发阶段 Defold 对此有自动化功能.你可以在打包 Android应用时指定证书和密匙. 不指定的话, Defold 会自动创建证书和密匙打包 *.apk* (Android Application Package) 文件.

注意如果要把应用上传至 Google Play, 就需要用自己的证书和密匙签名应用. 因为后续应用更新时, _新版本 *.apk* 文件签名需要与老版本保持一致_. 如果不一致, Google Play 会拒绝 *.apk* 更新上架, 除非作为全新应用发布.

详情请见 [Google Play 开发者中心](https://play.google.com/apps/publish/).

## 创建证书和密匙

基于 *.pem*-格式创建证书, 基于 *.pk8*-格式创建密匙. 二者的创建都可以使用 `openssl` 工具:

```sh
$ openssl genrsa -out key.pem 2048
$ openssl req -new -key key.pem -out request.pem
$ openssl x509 -req -days 9999 -in request.pem -signkey key.pem -out certificate.pem
$ openssl pkcs8 -topk8 -outform DER -in key.pem -inform PEM -out key.pk8 -nocrypt
```

这样就生成了 *certificate.pem* 和 *key.pk8* 文件可以用来签名应用包.

::: 注意
注意保存好证书和密匙文件. 一点丢失就 _不能_ 上传 *.apk* 更新文件到 Google Play 了.
:::

## 创建 Android 应用包

使用编辑器可以很容易地进行应用打包.打包前可以在  "game.project" [项目配置文件](/manuals/project-settings/#android) 里为应用设置图标, 版本号之类的. 菜单选择 <kbd>Project ▸ Bundle... ▸ Android Application...</kbd> 来进行打包.

如果希望编辑器自动生成调试用证书, 把 *Certificate* 和 *Private key* 置空即可:

![Signing Android bundle](images/android/sign_bundle.png)

如果希望使用自己的证书和密匙, 配置 *.pem* 和 *.pk8* 文件即可:

![Signing Android bundle](images/android/sign_bundle2.png)

点击 <kbd>Create Bundle</kbd> 会提示选择打包文件存放位置.

![Android Application Package file](images/android/apk_file.png)

### 安装 Android 应用包

编辑器生成 Android 应用包 *.apk* 文件. 应用包可以通过 `adb` 工具 (见下文), 或者通过 Google Play 的 [Google Play 开发者控制台](https://play.google.com/apps/publish/) 安装到设备上.

```
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
  pkg: /data/local/tmp/my_app.apk
Success
```

## 权限

Defold 引擎需要一些权限来运行各种功能. 权限在 `AndroidManifest.xml` 文件中定义, 并在 "game.project" [项目配置文件](/manuals/project-settings/#android) 中配置. 关于 Android 权限详见 [官方文档](https://developer.android.com/guide/topics/permissions/overview). 默认配置需要如下权限:

### android.permission.INTERNET and android.permission.ACCESS_NETWORK_STATE (Protection level: normal)
允许应用打开网络连接访问互联网. 需要上网时需要此权限. 见 ([Android 官方文档-网络](https://developer.android.com/reference/android/Manifest.permission#INTERNET)) 和 ([Android 官方文档-网络状态](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)).

### android.permission.WRITE_EXTERNAL_STORAGE (Protection level: dangerous)
允许应用写入外部存储器. 从 API level 19 开始, 读写 Context.getExternalFilesDir(String) 和 Context.getExternalCacheDir() 返回的应用目录不需要此权限. 需要 (使用 io.* 或 sys.save/load) 读写 [sys.get_save_file()](/ref/sys/#sys.get_save_file:application_id-file_name) 之外的目录文件以及 Android manifest 里设置 `android:minSdkVersion` 小于 19 时需要此权限. ([[Android 官方文档-外存写入](https://developer.android.com/reference/android/Manifest.permission#WRITE_EXTERNAL_STORAGE)).

### android.permission.WAKE_LOCK (Protection level: normal)
允许应用阻止屏幕息屏和调光. 接收通知保持亮屏时需要此权限. ([[Android 官方文档-亮屏锁定](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK))


## Android Debug Bridge

`adb` 命令行工具是一个多功能易使用的用来与 Android 设备进行交互的工具. 可以在 Mac, Linux 或者 Windows 上下载 Android SDK Platform-Tools 来安装 `adb`.

下载 Android SDK Platform-Tools 地址: https://developer.android.com/studio/releases/platform-tools. *adb* 工具就在 */platform-tools/* 里. 或者, 也通过各个平台的软件包管理器下载安装.

Ubuntu Linux:

```
$ sudo apt-get install android-tools-adb
```

Fedora 18/19:

```
$ sudo yum install android-tools
```

Mac OS X (Homebrew)

```
$ brew cask install android-platform-tools
```

通过如下代码让 `adb` 通过电脑 USB 与 Android 设备进行连接:

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

如果连接不上, 确保在 Android 设备上开启了 *USB debugging*. 在设备 *设置* 里找 *开发者选项* (或称 *开发选项*).

![Enable USB debugging](images/android/usb_debugging.png)

## 应用包调试

使用调试版引擎打包的应用 (即打包时选择 "Debug" 变体) 会把控制台信息全部发送至 Android 系统日志上. 使用 `adb` 工具的 `logcat` 命令访问日志. 使用标签 (`-s [标签名]`) 可以对日志信息进行过滤:

```
$ adb logcat -s "defold"
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:DLIB: SSDP started (ssdp://192.168.0.97:58089, http://0.0.0.0:38637)
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialised sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

## 常见问题

安装时报 "Failure [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES]" 错误
: Android 发现了你使用不同的证书安装应用. 编译调试包时, 使用的是临时证书. 安装前先卸载旧应用:

  ```
  $ adb uninstall com.defold.examples
  Success
  $ adb install Defold\ examples.apk
  4826 KB/s (18774344 bytes in 3.798s)
          pkg: /data/local/tmp/Defold examples.apk
  Success
  ```
