---
title: Налагодження нативного коду в Defold
brief: Цей посібник пояснює, як налагоджувати нативний код у Defold.
---

# Налагодження нативного коду {#debugging-native-code}

Defold ретельно протестовано, і за звичайних обставин аварійні завершення мають траплятися дуже рідко. Однак неможливо гарантувати, що їх ніколи не буде, особливо якщо ваша гра використовує нативні розширення. Якщо ви зіткнулися з аварійними завершеннями або нативним кодом, який працює не так, як очікується, є кілька способів розібратися з проблемою:

* Використайте налагоджувач для покрокового виконання коду
* Скористайтеся налагодженням за допомогою виведення
* Проаналізуйте журнал аварійного завершення
* Відновіть символи стека викликів


## Використання налагоджувача {#use-a-debugger}

Найпоширеніший спосіб — запускати код через `налагоджувач`. Він дає змогу виконувати код покроково, встановлювати `точки зупинки` й зупиняє виконання в разі аварії.

Для кожної платформи є кілька налагоджувачів.

* Visual studio — Windows
* VSCode — Windows, macOS, Linux
* Android Studio — Windows, macOS, Linux
* Xcode — macOS
* WinDBG — Windows
* lldb / gdb — macOS, Linux, (Windows)
* ios-deploy — macOS

Кожен інструмент підтримує налагодження на певних платформах:

* Visual studio — Windows + платформи з підтримкою gdbserver (наприклад, Linux/Android)
* VSCode — Windows, macOS (lldb), Linux (lldb/gdb) + платформи з підтримкою gdbserver
* Xcode — macOS, iOS ([докладніше](/manuals/debugging-native-code-ios))
* Android Studio — Android ([докладніше](/manuals/debugging-native-code-android))
* WinDBG — Windows
* lldb/gdb — macOS, Linux, (iOS)
* ios-deploy — iOS (через lldb)


## Налагодження за допомогою виведення {#use-print-debugging}

Найпростіший спосіб налагодження нативного коду — [налагодження за допомогою виведення](http://en.wikipedia.org/wiki/Debugging#Techniques). Використовуйте функції з [простору імен `dmLog`](/ref/stable/dmLog/), щоб відстежувати змінні або позначати перебіг виконання. Будь-яка з функцій журналювання виводитиме повідомлення на панель *Console* у редакторі та до [журналу гри](/manuals/debugging-game-and-system-logs).


## Аналіз журналу аварійного завершення {#analyze-a-crash-log}

У разі критичної аварії рушій Defold зберігає файл `_crash`. Цей файл містить інформацію про систему та аварію. У [журналі гри](/manuals/debugging-game-and-system-logs) буде вказано розташування файлу аварії (воно залежить від операційної системи, пристрою та застосунку).

Ви можете скористатися [модулем crash](https://www.defold.com/ref/crash/), щоб прочитати цей файл під час наступного сеансу. Рекомендуємо прочитати файл, зібрати інформацію, вивести її в консоль і надіслати до [аналітичного сервісу](/tags/stars/analytics/), який підтримує збирання журналів аварійних завершень.

::: important
У Windows також створюється файл `_crash.dmp`. Він стане в пригоді під час налагодження аварійного завершення.
:::

### Отримання журналу аварійного завершення з пристрою {#getting-the-crash-log-from-a-device}

Якщо аварія трапилася на мобільному пристрої, ви можете завантажити файл аварії на свій комп’ютер і проаналізувати його локально.

#### Android

Якщо застосунок [дозволяє налагодження](/manuals/project-settings/#android), ви можете отримати журнал аварійного завершення за допомогою [інструмента Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb.html) і команди `adb shell`:

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

В iTunes можна переглянути або завантажити контейнер застосунку.

У вікні `Xcode -> Devices` також можна вибрати журнали аварійних завершень


## Відновлення символів стека викликів {#symbolicate-a-callstack}

Якщо ви отримали стек викликів із файлу `_crash` або [файлу журналу](/manuals/debugging-game-and-system-logs), можна відновити в ньому символи (symbolication). Це означає перетворення кожної адреси в стеку викликів на ім’я файлу та номер рядка, що допомагає знайти першопричину.

Важливо використовувати саме той рушій, якому відповідає стек викликів, інакше ви, найімовірніше, шукатимете проблему не там! Використовуйте прапорець [`--with-symbols`](https://www.defold.com/manuals/bob/) під час пакування за допомогою [bob](https://www.defold.com/manuals/bob/) або встановіть прапорець <kbd>Generate debug symbols</kbd> у діалоговому вікні пакування в редакторі:

* iOS — папка `dmengine.dSYM.zip` у `build/arm64-ios` містить налагоджувальні символи для збірок iOS.
* macOS — папка `dmengine.dSYM.zip` у `build/x86_64-macos` містить налагоджувальні символи для збірок macOS.
* Android — вихідна папка пакета `projecttitle.apk.symbols/lib/` містить налагоджувальні символи для цільових архітектур.
* Linux — виконуваний файл містить налагоджувальні символи.
* Windows — файл `dmengine.pdb` у `build/x86_64-win32` містить налагоджувальні символи для збірок Windows.
* HTML5 — каталог `<project_name>_symbols` поруч із пакетом HTML5 містить `<project_name>_wasm.js.symbols`, а якщо вибрано архітектуру `wasm_pthread-web`, то й `<project_name>_pthread_wasm.js.symbols`.

::: important
Дуже важливо зберігати налагоджувальні символи для кожного публічного випуску вашої гри та знати, якому випуску вони належать. Без налагоджувальних символів ви не зможете дослідити жодне аварійне завершення в нативному коді! Також слід зберігати версію рушія з невидаленими символами (`unstripped`). Це дає змогу найточніше відновлювати символи стека викликів.
:::


### Завантаження символів у Google Play {#uploading-symbols-to-google-play}
Ви можете [завантажити налагоджувальні символи в Google Play](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems), щоб у всіх аварійних завершеннях, зареєстрованих у Google Play, відображалися стеки викликів із відновленими символами. Заархівуйте у форматі ZIP вміст вихідної папки пакета `projecttitle.apk.symbols/lib/`. Вона містить одну або кілька вкладених папок із назвами архітектур, як-от `arm64-v8a`, `armeabi-v7a` і `x86_64`.


### Відновлення символів стека викликів Android {#symbolicate-an-android-callstack}

1. Візьміть рушій із папки збірки

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. Розпакуйте в папку:

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. Знайдіть адресу в стеку викликів

	Наприклад, у стеку викликів без відновлених символів запис може мати такий вигляд

	`#00 pc 00257224 libmy_game_name.so`

	Де *`00257224`* — адреса

4. Визначте, чому відповідає адреса

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

Примітка: якщо ви отримали трасування стека з [журналів Android](/manuals/debugging-game-and-system-logs), можливо, вам вдасться відновити символи за допомогою [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html)

### Відновлення символів стека викликів iOS {#symbolicate-an-ios-callstack}

1. Якщо ви використовуєте нативні розширення, сервер може надати вам символи (.dSYM) (передайте `--with-symbols` до bob.jar)

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# it will produce a Contents/Resources/DWARF/dmengine
```

2. Якщо ви не використовуєте нативні розширення, завантажте символи стандартного рушія:

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. Відновіть символи за допомогою адреси завантаження

	З якоїсь причини просте використання адреси зі стека викликів не працює (тобто з адресою завантаження 0x0)

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# Neither does specifying the load address directly

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

А от додавання адреси завантаження до адреси працює:

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
