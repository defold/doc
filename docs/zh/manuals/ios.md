---
title: Defold iOS 平台开发
brief: 本教程介绍了如何在 Defold 里编译运行 iOS 设备应用.
---

# iOS 开发

iOS 要求 _所有_ 运行于手机或者平板电脑上的应用 _必须_ 使用 Apple 核发的 certificate 和 provisioning profile 进行签名. 本教程介绍了 iOS 平台的游戏打包. 在开发阶段, 推荐使用 [开发用app](/manuals/dev-app) 以利用热重载功能实现对移动设备的无线推送.

## Apple 签名过程

iOS 应用安全包含几个要点. 通过访问 [Apple's iOS Developer Program](https://developer.apple.com/programs/) 可以得到必要的工具. 如需注册, 请访问 [Apple's Developer Member Center](https://developer.apple.com/membercenter/index.action).

![Apple Member Center](images/ios/apple_member_center.png)

*Certificates, Identifiers & Profiles* 部分包含了所有所需工具. 在这里可以创建, 删除和编辑:

Certificates
: Apple 为开发者颁发的加密证书. You can create development or production certificates. Developer certificates allow you to test certain features such as the in-app purchase mechanism in a sandbox test environment. Production certificates are used to sign the final app for upload to the App Store. You need a certificate to sign apps before you can put them on your device for testing.

Identifiers
: Identifiers for various uses. It is possible to register wildcard identifiers (i.e. `some.prefix.*`) which can be used with several apps. App IDs can contain Application Service information, like if the app enables Passbook integration, the Game Center, etc. Such App IDs cannot be wildcard identifiers. For Application Services to function, your application's *bundle identifier* must match the App ID identifier.

Devices
: Each development device needs to be registered with their UDID (Unique Device IDentifier, see below).

Provisioning Profiles
: Provisioning profiles associate certificates with App IDs and a list of devices. They tell which app by what developer is allowed to be on what devices.

When signing your games and apps in Defold, you need a valid certificate and a valid provisioning profile.

::: sidenote
Some of the things you can do on the Member Center homepage you can also perform from inside the XCode development environment---if you have that installed.
:::

Device identifier (UDID)
: The UDID for an iOS device can be found by connecting the device to a computer via wifi or cable. Open Xcode and select <kbd>Window ▸ Devices and Simulators</kbd>. The serial number and identifier are displayed when you select your device.

  ![xcode devices](images/ios/xcode_devices.png)

  If you don't have Xcode installed you can find the identifier in iTunes. Click on the devices symbol and select your device.

  ![itunes devices](images/ios/itunes_devices.png)

  1. On the *Summary* page, locate the *Serial Number*.
  2. Click the *Serial Number* once so the field changes into *UDID*. If you click repeatedly, several pieces of information about the device will show up. Just continue to click until *UDID* shows.
  3. Right-click the long UDID string and select <kbd>Copy</kbd> to copy the identifier to the clipboard so you can easily paste it into the UDID field when registering the device on Apple's Developer Member Center.

## Developing using a free Apple developer account

Since Xcode 7, anyone can install Xcode and do on-device development for free. You don't have to sign up for the iOS Developer Program. Instead, Xcode will automatically issue a certificate for you as a developer (valid for 1 year) and a provisioning profile for your app (valid for one week) on your specific device.

1. Connect your device.
2. Install Xcode.
3. Add a new account to Xcode and sign in with your Apple ID.
4. Create a new project. The simplest "Single View App" works fine.
5. Select your "Team" (auto created for you) and give the app a bundle identifier.
6. Make sure that Xcode has created a *Provisioning Profile* and *Signing Certificate* for the app.

   ![](images/ios/xcode_certificates.png)

7. Build and launch the app on your device. The first time, Xcode will ask you to enable Developer mode and will prepare the device with debugger support. This may take a while.
8. When you have verified that the app works, find it on your disk. You can see the build location in the Build report in the "Report Navigator".

   ![](images/ios/app_location.png)

9. Locate the app, right-click it and select <kbd>Show Package Contents</kbd>.

   ![](images/ios/app_contents.png)

10. Copy the file "embedded.mobileprovision" to some place on your drive where you will find it.

   ![](images/ios/free_provisioning.png)

This provision file can be used together with your code signing identity to sign apps in Defold for one week, for _one device_. There is no way to add additional device UDIDs to this generated provisioning profile.

When the provision expires, you need to build the app again in Xcode and get a new temporary provision file as described above.

## Creating an iOS application bundle

When you have the code signing identity and privisioning profile, you are ready to create a stand alone application bundle for your game from the editor. Simply select <kbd>Project ▸ Bundle... ▸ iOS Application...</kbd> from the menu.

![Signing iOS bundle](images/ios/sign_bundle.png)

Select your code signing identity and browse for your mobile provisioning file. Select which architectures (32 bit, 64 bit and the iOS simulator) to bundle for as well as the variant (Debug or Release). You can optionally untick the `Sign application` checkbox to skip the signing process and then manually sign at a later stage.

::: important
You **must** untick the `Sign application` checkbox when testing your game on the iOS simulator. You will be able to install the application but it will not boot.
:::

Press *Create Bundle* and you will then be prompted to specify where on your computer the bundle will be created.

You specify what icon to use for the app, the launch screen image(s) and so forth on the *game.project* project settings file.

::: important
When your game launches on iOS, the launch images are used to set the correct screen resolution. If you do not supply the correct image size, you will get a lower resolution with resulting black bars.
:::

![ipa iOS application bundle](images/ios/ipa_file.png){.left}

## Installing an iOS application bundle

The editor writes an *.ipa* file which is an iOS application bundle. To install the file on your device, you can use Xcode (via the "Devices and Simulators" window). Other options are to use a command line tool such as [ios-deploy](https://github.com/phonegap/ios-deploy) or iTunes.

You can use the `xcrun simctl` command line tool to work with the iOS simulators available via Xcode:

```
# show a list of available devices
xcrun simctl list

# boot an iPhone X simulator
xcrun simctl boot "iPhone X"

# install your.app to a booted simulator
xcrun simctl install booted your.app

# launch the simulator
open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
```
