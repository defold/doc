The `adb` command line tool is an easy to use and versatile program that is used to interact with Android devices. You can download and install `adb` as part of the Android SDK Platform-Tools, for Mac, Linux or Windows.

Download the Android SDK Platform-Tools from: https://developer.android.com/studio/releases/platform-tools. You find the *adb* tool in */platform-tools/*. Alternatively, platform specific packages can be installed through respective package managers.

On Ubuntu Linux:

```
$ sudo apt-get install android-tools-adb
```

On Fedora 18/19:

```
$ sudo yum install android-tools
```

On macOS (Homebrew)

```
$ brew cask install android-platform-tools
```

You can verify that `adb` works by connecting your Android device to your computer via USB and issue the following command:

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

If your device does not show up, verify that you have enabled *USB debugging* on the Android device. Open the device *Settings* and look for *Developer options* (or *Development*).

![Enable USB debugging](images/android/usb_debugging.png)
