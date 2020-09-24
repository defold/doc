---
title: macOS 平台游戏开发
brief: 本教程介绍了在 macOS 平台上编译和运行 Defold 游戏的方法
---

# macOS 开发

为 macOS 平台开发游戏非常简单, 有几件事需要注意.

## 项目配置

macOS 相关选项位于 *game.project* 配置文件的 [OSX 部分](/manuals/project-settings/#MacOS 和 OS X).

## 应用图标

macOS 图标只支持 .icns 格式. 可以使用一组.png文件生成一个.icns图标集. 参照 [官方 .icns 文件生成方法](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html). 其主要步骤有:

* 新建图标集文件夹, 比如 `game.iconset`
* 把图片文件放入上述文件夹里:

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

* 使用命令行工具 `iconutil` 把文件夹转化成图标集:

```
iconutil -c icns -o game.icns game.iconset
```

## 发布游戏应用
可以把游戏发布到 Mac App Store, 第三方软件商店或者像 Steam 和 itch.io 这样的门户网站, 当然也可以放在自己的网站上. 发布之前做好提交准备. 无论发布到哪, 下面这些都是应该要考虑的事情:

* 1) 添加运行权限以便所有玩家都能运行游戏 (默认文件所有者拥有运行权限):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

* 2) 建立 entitlements 文件表明游戏所需权限. 例如:

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

  * `com.apple.security.cs.allow-jit` - 让游戏可以使用 MAP_JIT 标识写入和运行内存内容
  * `com.apple.security.cs.allow-unsigned-executable-memory` - 让游戏可以不必严格使用 MAP_JIT 标识也能写入和运行内存内容
  * `com.apple.security.cs.allow-dyld-environment-variables` - 让游戏接受动态连接环境变量以便可以向游戏进程注入代码

根据自己的游戏情况增减项目. 比如 Steamworks 扩展库需要如下权限:

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

    * `com.apple.security.cs.disable-library-validation` - 让游戏可以载入任意插件和库而不需要它们的代码签名.

应用可以设置的一切权限都列在 [Apple 开发者文档](https://developer.apple.com/documentation/bundleresources/entitlements) 里.

* 3) 使用 `codesign` 为游戏签名:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## 发布到 Mac App Store 以外的地方
Apple 要求发布到 Mac App Store 以外的应用必须加入苹果认证才能在 macOS Catalina 上运行. 关于命令行编译环境加入认证的方法参考 [官方文档](https://developer.apple.com/documentation/Xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow). 大体步骤是:

* 1) 完成上述添加权限和签名的工作.

* 2) 使用 `altool` 命令行工具上传游戏包来添加苹果认证.

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

* 3) 使用 `altool --notarize-app` 命令行工具检查这个 UUID 的应用状态:

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

* 4) 等到状态变为 `success` 然后把证书打入游戏包:

```
$ xcrun stapler staple "Game.app"
```

* 5) 完成之后就可以发布了. --苹果之壁（莲）

## 发布到 Mac App Store
这在 [Apple 开发者文档](https://developer.apple.com/macos/submit/) 里已经详细说明. 注意提交前要确保已加入权限和签名.

注意: 发布到 Mac App Store 不需要任何认证.
