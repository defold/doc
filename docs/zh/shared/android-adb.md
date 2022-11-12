`adb` 命令行工具是一个多功能易使用的用来与 Android 设备进行交互的工具. 可以在 Mac, Linux 或者 Windows 上下载 Android SDK Platform-Tools 来安装 `adb`.

下载 Android SDK Platform-Tools 地址: https://developer.android.com/studio/releases/platform-tools. *adb* 工具就在 */platform-tools/* 里. 或者, 也通过各个平台的软件包管理器下载安装.

Ubuntu Linux 上:

```
$ sudo apt-get install android-tools-adb
```

Fedora 18/19 上:

```
$ sudo yum install android-tools
```

macOS (Homebrew) 上

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