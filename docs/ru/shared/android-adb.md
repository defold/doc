Инструмент командной строки `adb` — это удобная и универсальная программа для взаимодействия с устройствами Android. Вы можете скачать и установить `adb` как часть Android SDK Platform-Tools для Mac, Linux или Windows.

Скачать Android SDK Platform-Tools можно здесь: https://developer.android.com/studio/releases/platform-tools. Инструмент *adb* находится в каталоге */platform-tools/*. Также можно установить платформенные пакеты через соответствующие менеджеры пакетов.

В Ubuntu Linux:

```
$ sudo apt-get install android-tools-adb
```

В Fedora 18/19:

```
$ sudo yum install android-tools
```

В macOS (Homebrew)

```
$ brew cask install android-platform-tools
```

Проверить, что `adb` работает, можно так: подключите Android-устройство к компьютеру по USB и выполните следующую команду:

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

Если устройство не появляется в списке, убедитесь, что на Android-устройстве включена *USB debugging*. Откройте *Settings* устройства и найдите *Developer options* (или *Development*).

![Enable USB debugging](images/android/usb_debugging.png)
