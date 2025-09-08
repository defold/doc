`adb` 命令行工具是一个易于使用且功能多样的程序，用于与 Android 设备进行交互。您可以作为 Android SDK Platform-Tools 的一部分下载并安装 `adb`，适用于 Mac、Linux 或 Windows。

从以下地址下载 Android SDK Platform-Tools：https://developer.android.com/studio/releases/platform-tools。您可以在 */platform-tools/* 目录中找到 *adb* 工具。或者，也可以通过各平台相应的软件包管理器安装特定平台的软件包。

在 Ubuntu Linux 上：

```
$ sudo apt-get install android-tools-adb
```

在 Fedora 18/19 上：

```
$ sudo yum install android-tools
```

在 macOS (Homebrew) 上：

```
$ brew cask install android-platform-tools
```

您可以通过 USB 将 Android 设备连接到计算机，然后发出以下命令来验证 `adb` 是否正常工作：

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

如果您的设备没有显示，请确认您已在 Android 设备上启用 *USB 调试*。打开设备的 *设置* 并查找 *开发者选项*（或 *开发*）。

![Enable USB debugging](images/android/usb_debugging.png)