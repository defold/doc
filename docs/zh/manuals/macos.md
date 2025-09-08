---
title: macOS 平台的 Defold 开发
brief: 本手册介绍了如何在 macOS 上构建和运行 Defold 应用程序
---

# macOS 开发

为 macOS 平台开发 Defold 应用程序是一个直接的过程，几乎不需要考虑太多事项。

## 项目设置

macOS 特定的应用程序配置是在 *game.project* 设置文件的 [macOS 部分](/manuals/project-settings/#macos) 中完成的。

## 应用图标

macOS 游戏使用的应用图标必须是 .icns 格式。您可以轻松地从一组收集为 .iconset 的 .png 文件创建 .icns 文件。请遵循[创建 .icns 文件的官方说明](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html)。涉及的步骤简要总结如下：

* 为图标创建一个文件夹，例如 `game.iconset`
* 将图标文件复制到创建的文件夹中：

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* 使用 `iconutil` 命令行工具将 .iconset 文件夹转换为 .icns 文件：

```
iconutil -c icns -o game.icns game.iconset
```

## 发布您的应用程序
您可以将应用程序发布到 Mac App Store，使用第三方商店或门户网站（如 Steam 或 itch.io），或者通过自己的网站发布。在发布应用程序之前，您需要准备提交。无论您打算如何分发应用程序，都需要以下步骤：

* 1) 通过添加执行权限确保任何人都能运行您的游戏（默认情况下只有文件所有者拥有执行权限）：

```
$ chmod +x Game.app/Contents/MacOS/Game
```

* 2) 创建一个指定游戏所需权限的授权文件。对于大多数游戏，以下权限就足够了：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - 表示应用程序是否可以使用 MAP_JIT 标志创建可写和可执行的内存
  * `com.apple.security.cs.allow-unsigned-executable-memory` - 表示应用程序是否可以在不使用 MAP_JIT 标志施加的限制的情况下创建可写和可执行的内存
  * `com.apple.security.cs.allow-dyld-environment-variables` - 表示应用程序是否可能受到动态链接器环境变量的影响，您可以使用这些变量向应用程序的进程注入代码

某些应用程序可能还需要额外的授权。Steamworks 扩展需要这个额外的授权：

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

    * `com.apple.security.cs.disable-library-validation` - 表示应用程序是否可以加载任意插件或框架，而不需要代码签名。

可以授予应用程序的所有授权都列在官方的 [Apple 开发者文档](https://developer.apple.com/documentation/bundleresources/entitlements) 中。

* 3) 使用 `codesign` 为您的游戏签名：

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## 发布到 Mac App Store 以外的地方
Apple 要求所有在 Mac App Store 之外分发的软件都必须经过 Apple 公证，才能在 macOS Catalina 上默认运行。请参阅[官方文档](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow)了解如何在 Xcode 之外的脚本构建环境中添加公证。涉及的步骤简要总结如下：

* 1) 完成上述添加权限和签名应用程序的步骤。

* 2) 使用 `altool` 压缩并上传您的游戏以进行公证：

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

* 3) 使用从 `altool --notarize-app` 调用返回的请求 UUID 检查您的提交状态：

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

* 4) 等待状态变为 `success`，然后将公证票证钉到游戏上：

```
$ xcrun stapler staple "Game.app"
```

* 5) 您的游戏现在可以分发了。

## 发布到 Mac App Store
发布到 Mac App Store 的过程在 [Apple 开发者文档](https://developer.apple.com/macos/submit/) 中有详细记录。在提交之前，请确保如上所述添加权限并为应用程序签名。

注意：发布到 Mac App Store 时，游戏不必经过公证。

:[Apple 隐私清单](../shared/apple-privacy-manifest.md)