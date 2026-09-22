Das Kommandozeilenwerkzeug `adb` ist ein einfach zu bedienendes und vielseitiges Programm, mit dem du mit Android-Geräten interagieren kannst. Du kannst `adb` als Teil der Android SDK Platform-Tools für Mac, Linux oder Windows herunterladen und installieren.

Lade die Android SDK Platform-Tools hier herunter: https://developer.android.com/studio/releases/platform-tools. Das Werkzeug *adb* findest du unter */platform-tools/*. Alternativ kannst du plattformspezifische Pakete über die jeweiligen Paketmanager installieren.

Unter Ubuntu Linux:

```
$ sudo apt-get install android-tools-adb
```

Unter Fedora 18/19:

```
$ sudo yum install android-tools
```

Unter macOS (Homebrew)

```
$ brew cask install android-platform-tools
```

Du kannst überprüfen, ob `adb` funktioniert, indem du dein Android-Gerät per USB mit deinem Computer verbindest und den folgenden Befehl ausführst:

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

Wenn dein Gerät nicht angezeigt wird, prüfe, ob du *USB debugging* auf dem Android-Gerät aktiviert hast. Öffne auf dem Gerät *Settings* und suche nach *Developer options* (oder *Development*).

![USB-Debugging aktivieren](images/android/usb_debugging.png)
