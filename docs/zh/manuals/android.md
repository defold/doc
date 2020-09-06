---
title: Defold 的 Android 平台开发
brief: 本教程介绍了如何在 Defold 中进行 Android 设备应用的开发
---

# Android 开发

Android 设备允许自由允许你开发的应用. 可以很容易地编译好游戏拷贝到 Android 设备上. 本手册介绍了对于 Android 游戏的打包步骤. 推荐开发时, 从 [开发应用](/manuals/dev-app) 上运行游戏因为可以通过无线连接设备进行代码和内容的热重载.

## Android 和 Google Play 签名

Android 要求每个 APK 文件在被安装到设备上或者在设备上更新之前必须进行数字签名. 如果你是安卓开发者, 只需要在把程序包上传到 Play Console 之前, 经过 [Play App Signing](https://developer.android.com/studio/publish/app-signing#app-signing-google-play) 的自动处理即可. 然而, 你还可以选择手动对程序包进行签名以便上传到 Google Play, 其他应用商店以及在整个互联网上传播.

从 Defold 编辑器或者 [命令行工具](/manuals/bob) 打包安卓包需要提供一个 keystore (包括证书和公匙), 然后对应用签名时还要用到私匙. 没有的话, Defold 会自动生成一个临时调试用 keystore 用于打包和签名.

::: 注意
千万 **不要** 带着调试签名就上传到 Google Play 上去. 开发者必须自己制作属于自己的签名.
:::

## 制作 keystore

::: 注意
Defold 应对安卓应用包签名的改变是从 1.2.173 版开始的, 就是使用单独的证书和密码来合成 keystore.
:::

也可以 [使用 Android Studio](https://developer.android.com/studio/publish/app-signing#generate-key) 或者通过使用控制台命令来生成签名:

```bash
keytool -genkey -v -noprompt -dname "CN=John Smith, OU=Area 51, O=US Air Force, L=Unknown, ST=Nevada, C=US" -keystore mykeystore.keystore -storepass 5Up3r_53cR3t -alias myAlias -keyalg RSA -validity 9125
```

这个命令会生成一个叫做 `mykeystore.keystore` 的签名, 其中包含了证书和密码. 密匙 `5Up3r_53cR3t` 保护其不备破解. 这个签名有效期为 25 年 (9125 天). 这个签名的id叫做 `myAlias`.

::: 注意
要把签名和密匙保存好. 如果要手动上传 Google Play 但是签名密码丢失的话就没办法使用 Google Play 来更新你的应用了. 图省事的话就用 Google Play App Signing 搞定签名把.
:::


## 证书和安卓包

编辑器打包安卓包十分方便. 打包之前可以为应用指定图标, 设置版本号等等, 都在 "game.project" [项目配置文件](/manuals/project-settings/#android) 里设置.

选择菜单栏 <kbd>Project ▸ Bundle... ▸ Android Application...</kbd> 就可以打包了.

要让编辑器自动生成调试用签名, 只需把 *Keystore* 和 *Keystore password* 字段留空即可:

![Signing Android bundle](images/android/sign_bundle.png)

要让编辑器使用你自己指定的签名打包, 就要设置好 *Keystore* 和 *Keystore password* 字段. *Kyestore* 的扩展名是 `.keystore`, 而密码要保存成文本 `.txt` 文件:

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
:[Android 问答](../shared/android-faq.md)
