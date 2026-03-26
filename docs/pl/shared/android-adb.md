Narzędzie wiersza poleceń `adb` jest łatwym w użyciu i wszechstronnym programem służącym do komunikacji z urządzeniami z Androidem. `adb` można pobrać i zainstalować jako część Android SDK Platform-Tools dla systemów Mac, Linux lub Windows.

Pobierz Android SDK Platform-Tools z: https://developer.android.com/studio/releases/platform-tools. Narzędzie *adb* znajdziesz w katalogu */platform-tools/*. Alternatywnie pakiety dla konkretnych systemów można zainstalować za pomocą odpowiednich menedżerów pakietów.

W Ubuntu Linux:

```
$ sudo apt-get install android-tools-adb
```

W Fedora 18/19:

```
$ sudo yum install android-tools
```

W macOS (Homebrew)

```
$ brew cask install android-platform-tools
```

Możesz sprawdzić, czy `adb` działa, podłączając urządzenie z Androidem do komputera przez USB i wykonując następujące polecenie:

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

Jeśli urządzenie się nie pojawia, sprawdź, czy na urządzeniu z Androidem włączono *USB debugging*. Otwórz *Settings* urządzenia i poszukaj *Developer options* (lub *Development*).

![Włącz debugowanie USB](images/android/usb_debugging.png)
