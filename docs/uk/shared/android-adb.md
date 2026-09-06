Засіб командного рядка `adb` — це проста у використанні й універсальна програма для взаємодії з пристроями Android. Ви можете завантажити й установити `adb` у складі Android SDK Platform-Tools для Mac, Linux або Windows.

Завантажте Android SDK Platform-Tools за адресою: https://developer.android.com/studio/releases/platform-tools. Засіб *adb* міститься в */platform-tools/*. Також можна встановити пакети для вашої платформи через відповідний менеджер пакетів.

В Ubuntu Linux:

```
$ sudo apt-get install android-tools-adb
```

У Fedora 18/19:

```
$ sudo yum install android-tools
```

У macOS (Homebrew)

```
$ brew cask install android-platform-tools
```

Щоб перевірити, чи працює `adb`, під’єднайте пристрій Android до комп’ютера через USB і виконайте таку команду:

```
$ adb devices
List of devices attached
31002535c90ef000    device
```

Якщо пристрій не відображається, перевірте, чи ввімкнено на ньому *USB debugging*. Відкрийте *Settings* пристрою й знайдіть *Developer options* (або *Development*).

![Увімкнення налагодження через USB](images/android/usb_debugging.png)
