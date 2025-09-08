---
title: Defold 的 Android 平台开发
brief: 本手册描述了如何在 Android 设备上构建和运行 Defold 应用程序
---

# Android 开发

Android 设备允许你自由运行自己的应用程序。构建游戏版本并将其复制到 Android 设备上非常容易。本手册解释了为 Android 打包游戏所涉及的步骤。在开发过程中，通过[开发应用](/manuals/dev-app)运行游戏通常是首选，因为它允许你直接将内容和代码热重载到设备上。

## Android 和 Google Play 签名流程

Android 要求所有 APK 在安装到设备上或更新之前都必须使用证书进行数字签名。如果你使用 Android App Bundles，只需在上传到 Play Console 之前对你的应用包进行签名，[Play App Signing](https://developer.android.com/studio/publish/app-signing#app-signing-google-play)会处理其余部分。但是，你也可以手动为应用签名，以便上传到 Google Play、其他应用商店以及在任何商店之外分发。

当你从 Defold 编辑器或[命令行工具](/manuals/bob)创建 Android 应用包时，你可以提供一个密钥库（包含你的证书和密钥）和密钥库密码，这些将在签名你的应用程序时使用。如果你不提供，Defold 会生成一个调试密钥库并在签名应用程序包时使用它。

::: important
你**绝对不应该**将使用调试密钥库签名的应用程序上传到 Google Play。始终使用你自己创建的专用密钥库。
:::

## 创建密钥库

::: sidenote
Defold 中的 Android 签名流程在版本 1.2.173 中发生了变化，从使用独立的密钥和证书改为使用密钥库。[更多信息请参阅此论坛帖子](https://forum.defold.com/t/upcoming-change-to-the-android-build-pipeline/66084)。
:::

你可以[使用 Android Studio](https://developer.android.com/studio/publish/app-signing#generate-key)或从终端/命令提示符创建密钥库：

```bash
keytool -genkey -v -noprompt -dname "CN=John Smith, OU=Area 51, O=US Air Force, L=Unknown, ST=Nevada, C=US" -keystore mykeystore.keystore -storepass 5Up3r_53cR3t -alias myAlias -keyalg RSA -validity 9125
```

这将创建一个名为 `mykeystore.keystore` 的密钥库文件，其中包含一个密钥和证书。对密钥和证书的访问将受到密码 `5Up3r_53cR3t` 的保护。密钥和证书将在 25 年（9125 天）内有效。生成的密钥和证书将通过别名 `myAlias` 进行标识。

::: important
确保将密钥库和相关密码存储在安全的地方。如果你自己签名并将应用程序上传到 Google Play，而密钥库或密钥库密码丢失，你将无法在 Google Play 上更新应用程序。你可以通过使用 Google Play App Signing 并让 Google 为你签名应用程序来避免这种情况。
:::


## 创建 Android 应用包

编辑器允许你轻松地为游戏创建独立的应用包。在打包之前，你可以在 *game.project* [项目设置文件](/manuals/project-settings/#android) 中指定要使用的图标、设置版本代码等。

要从菜单中选择打包，请选择 <kbd>Project ▸ Bundle... ▸ Android Application...</kbd>。

如果你希望编辑器自动创建随机调试证书，请将 *Keystore* 和 *Keystore password* 字段留空：

![Signing Android bundle](images/android/sign_bundle.png)

如果你想使用特定的密钥库为你的包签名，请指定 *Keystore* 和 *Keystore password*。*Keystore* 预期具有 `.keystore` 文件扩展名，而密码预期存储在具有 `.txt` 扩展名的文本文件中。如果密钥库中的密钥使用与密钥库本身不同的密码，也可以指定 *Key password*：

![Signing Android bundle](images/android/sign_bundle2.png)

Defold 支持创建 APK 和 AAB 文件。从 Bundle Format 下拉菜单中选择 APK 或 AAB。

配置好应用包设置后，按 <kbd>Create Bundle</kbd>。然后系统会提示你指定在计算机上创建包的位置。

![Android Application Package file](images/android/apk_file.png)

:[Build Variants](../shared/build-variants.md)

### 安装 Android 应用包

#### 安装 APK

一个 *`.apk`* 文件可以使用 `adb` 工具复制到你的设备上，或者通过 [Google Play 开发者控制台](https://play.google.com/apps/publish/) 复制到 Google Play。

:[Android ADB](../shared/android-adb.md)

```
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
  pkg: /data/local/tmp/my_app.apk
Success
```

#### 使用编辑器安装 APK

你可以使用编辑器打包对话框中的"在连接的设备上安装"和"启动已安装的应用"复选框来安装和启动 *`.apk`* 文件：

![Install and Launch APK](images/android/install_and_launch.png)

要使此功能正常工作，你需要安装 ADB 并在连接的设备上启用 *USB 调试*。如果编辑器无法检测到 ADB 命令行工具的安装位置，你需要在[首选项](/manuals/editor-preferences/#tools)中指定它。

#### 安装 AAB

一个 *`.aab`* 文件可以通过 [Google Play 开发者控制台](https://play.google.com/apps/publish/) 上传到 Google Play。也可以使用 *`.aab`* 文件制作 *`.apk`* 以便使用 [Android 打包工具](https://developer.android.com/studio/command-line/bundletool) 在本地安装。

## 权限

Defold 引擎需要许多不同的权限才能使所有引擎功能正常工作。权限在 `AndroidManifest.xml` 中定义，在 *game.project* [项目设置文件](/manuals/project-settings/#android) 中指定。你可以在[官方文档](https://developer.android.com/guide/topics/permissions/overview)中阅读更多关于 Android 权限的信息。默认清单中请求以下权限：

### android.permission.INTERNET and android.permission.ACCESS_NETWORK_STATE (Protection level: normal)

允许应用程序打开网络套接字并访问网络信息。这些权限是访问互联网所必需的。（[Android 官方文档](https://developer.android.com/reference/android/Manifest.permission#INTERNET)）和（[Android 官方文档](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)）。

### android.permission.WAKE_LOCK (Protection level: normal)

允许使用 PowerManager WakeLocks 来防止处理器休眠或屏幕变暗。在接收推送通知时暂时防止设备休眠需要此权限。（[Android 官方文档](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK)）


## 使用 AndroidX

AndroidX 是对原始 Android 支持库的重大改进，该支持库已不再维护。AndroidX 包通过提供功能对等和新库完全取代了支持库。[资源门户](/assets) 中的大多数 Android 扩展都支持 AndroidX。如果你不想使用 AndroidX，可以通过在[应用程序清单](https://defold.com/manuals/app-manifest/)中勾选 `Use Android Support Lib` 来明确禁用它，转而使用旧的 Android 支持库。

![](images/android/enable_supportlibrary.png)

## 常见问题
:[Android 问答](../shared/android-faq.md)
