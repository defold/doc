---
title: Defold iOS 平台开发
brief: 本教程介绍了如何在 Defold 里编译运行 iOS 设备应用.
---

# iOS 开发

iOS 要求 _所有_ 运行于手机或者平板电脑上的应用 _必须_ 使用 Apple 核发的 certificate 和 provisioning profile 进行签名. 本教程介绍了 iOS 平台的游戏打包. 在开发阶段, 推荐使用 [开发用app](/manuals/dev-app) 以利用热重载功能实现对移动设备的无线推送.

## Apple 签名过程

iOS 应用安全包含几个要素. 通过访问 [Apple's iOS Developer Program](https://developer.apple.com/programs/) 可以得到必要的工具. 如需注册, 请访问 [Apple's Developer Member Center](https://developer.apple.com/membercenter/index.action).

![Apple Member Center](images/ios/apple_member_center.png)

*Certificates, Identifiers & Profiles* 部分包含了所有所需工具. 在这里可以创建, 删除和编辑:

Certificates
: Apple 为开发者颁发的加密证书. 分为开发证书和发布证书两种. 开发证书用以在沙盒环境中测试某些功能比如应用内购. 发布证书是将应用发布到 App Store 时用的证书. 在设备上测试之前要用证书对应用进行签名.

Identifiers
: 应用id. 用于多个应用的通配符id (类似 `some.prefix.*`) 是允许的. 应用id也在集成某些服务时使用, 比如 Passbook, Game Center 之类的. 这种情况下不支持通配符id. 因为使用服务时 *bundle identifier* 必须与应用id一致.

Devices
: 用于开发的设备要注册 UDID (Unique Device IDentifier, 见下文).

Provisioning Profiles
: 提供商档案与应用id与开发设备的证书相关. 这样可以确保让谁的哪个应用可以运行于哪个设备上.

在 Defold 中给应用做签名时, 需要提供加密证书和提供商档案文件.

::: 注意
Member Center 页面的一些功能在 XCode 里也可以进行---前提是先安装好XCode.
:::

Device identifier (UDID)
: iOS 设备的 UDID 可以通过wifi或者线路连接计算机查找. 打开 Xcode 选择 <kbd>Window ▸ Devices and Simulators</kbd>. 选中设备就会显示出序列号和UDID.

  ![xcode devices](images/ios/xcode_devices.png)

  如果没安装 Xcode也可以从 iTunes 里查看. 首先选中要查看的设备.

  ![itunes devices](images/ios/itunes_devices.png)

  1. 在 *Summary* 页, 可以找到 *Serial Number*.
  2. 点击 *Serial Number* 一次, 它会切换成 *UDID*. 再点击下去还会显示其他设备信息. 这里我们找到 *UDID* 即可.
  3. 右键点击 UDID 那一长串字符, 选择 <kbd>Copy</kbd> 即可将其存入剪贴板, 在 Apple 开发中心注册设备时就可以直接粘贴填入了.

## 使用免费账户开发应用

从 Xcode 7 开始, 所有人都被允许安装 Xcode 并且免费开发设备应用. 无需注册iOS开发者. Xcode 会为设备自动核发一个临时开发者证书 (有效期1年) 和一个临时应用提供商档案 (有效期1周).

1. 连接设备.
2. 安装 Xcode.
3. 在 Xcode 注册并登录 Apple ID.
4. 新建项目. 最简单的 "Single View App" 就好.
5. 选择 "Team" (自动生成) 并为app设置 bundle identifier.
6. 确保 Xcode 为app生成了 *Provisioning Profile* 和 *Signing Certificate*.

   ![](images/ios/xcode_certificates.png)

7. 编译并且在设备上运行. 首次运行, Xcode 会提示打开开发者模式并为调试做好准备. 可能要等待一会儿.
8. 确定应用正常运行后, 在硬盘上找到编译好的app. 可以在 "Report Navigator" 的编译报告里找到app位置.

   ![](images/ios/app_location.png)

9. 找到app, 右键选择 <kbd>Show Package Contents</kbd>.

   ![](images/ios/app_contents.png)

10. 把 "embedded.mobileprovision" 文件拷贝出来.

   ![](images/ios/free_provisioning.png)

这个供应商档案文件连同加密证书可以在 Defold 为应用签名, 有效期一周, _限一个设备_. 这样生成的供应商档案无法向其增加更多的 UDID.

档案过期后, 可以在 Xcode 里如法炮制再次生成临时档案文件.

## 打包 iOS 应用

如果你有加密证书和这个供应商档案文件, 就可以在编辑器里打包应用了. 从菜单中选择 <kbd>Project ▸ Bundle... ▸ iOS Application...</kbd>.

![Signing iOS bundle](images/ios/sign_bundle.png)

选择证书和档案. 设置架构 (32 bit, 64 bit 和 iOS 模拟器) 再选择打包模式 (Debug 或者 Release). 也可以取消选择 `Sign application` 跳过签名步骤留待后面完成.

::: 注意
要在模拟器中测试游戏 **必须取消** `Sign application` 选项. 否则的话游戏能安装却不能运行.
:::

点击 *Create Bundle* 并选择打包应用存放位置.

可以在 *game.project* 项目配置文件中设置app图标, 启动图片等等.

::: 注意
iOS 上的应用, 启动图片决定了应用分辨率. 如果图片分辨率错误, 应用可能也会分辨率错误带黑边.
:::

![ipa iOS application bundle](images/ios/ipa_file.png){.left}

## 安装 iOS 打包应用

编辑器对iOS应用打包后生成 *.ipa* 文件. 要安装此文件, 可以使用 Xcode (通过 "Devices and Simulators" 窗口). 或者使用命令行工具 [ios-deploy](https://github.com/phonegap/ios-deploy) 或者使用 iTunes.

可以使用 `xcrun simctl` 命令行工具与 Xcode 的 iOS 模拟器进行交互:

```
# 显示可用设备列表
xcrun simctl list

# 启动 iPhone X 模拟器
xcrun simctl boot "iPhone X"

# 在模拟器上安装 your.app
xcrun simctl install booted your.app

# 启动模拟器
open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
```
