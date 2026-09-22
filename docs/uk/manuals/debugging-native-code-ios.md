---
title: Налагодження на iOS/macOS
brief: Цей посібник описує, як налагоджувати збірку за допомогою Xcode.
---

# Налагодження на iOS/macOS {#debugging-on-iosmacos}

Тут описано, як налагоджувати збірку за допомогою [Xcode](https://developer.apple.com/xcode/) — рекомендованого Apple середовища розробки для macOS та iOS.

## Xcode {#xcode}

* Створіть пакет застосунку за допомогою bob з параметром `--with-symbols` ([докладніше](/manuals/debugging-native-code/#symbolicate-a-callstack)):

```sh
$ cd myproject
$ wget http://d.defold.com/archive/<sha1>/bob/bob.jar
$ java -jar bob.jar --platform armv7-darwin build --with-symbols --variant debug --archive bundle -bo build/ios -mp <app>.mobileprovision --identity "iPhone Developer: Your Name (ID)"
```

* Установіть застосунок за допомогою `Xcode`, `iTunes` або [ios-deploy](https://github.com/ios-control/ios-deploy)

```sh
$ ios-deploy -b <AppName>.ipa
```

* Отримайте папку `.dSYM` (тобто налагоджувальні символи)

	* Якщо застосунок не використовує нативні розширення, ви можете завантажити файл `.dSYM` із [d.defold.com](http://d.defold.com)

	* Якщо ви використовуєте нативне розширення, папка `.dSYM` створюється під час збирання за допомогою [bob.jar](https://www.defold.com/manuals/bob/). Потрібне лише збирання (без архівування чи пакування):

```sh
$ cd myproject
$ unzip .internal/cache/arm64-ios/build.zip
$ mv dmengine.dSYM <AppName>.dSYM
$ mv <AppName>.dSYM/Contents/Resources/DWARF/dmengine <AppName>.dSYM/Contents/Resources/DWARF/<AppName>
```

### Створення проєкту {#create-project}

Для належного налагодження потрібен проєкт і налаштоване зіставлення вихідного коду.
Ми використовуватимемо цей проєкт лише для налагодження, а не для збирання.

* Створіть новий проєкт Xcode і виберіть шаблон `Game`

	![Шаблон проєкту](images/extensions/debugging/ios/project_template.png)

* Виберіть назву (наприклад, `debug`) і налаштування за замовчуванням

* Виберіть папку для збереження проєкту

* Додайте свій код до застосунку

	![Додавання файлів](images/extensions/debugging/ios/add_files.png)

* Переконайтеся, що прапорець «Copy items if needed» знято.

	![Додавання вихідного коду](images/extensions/debugging/ios/add_source.png)

* Ось кінцевий результат

	![Доданий вихідний код](images/extensions/debugging/ios/added_source.png)


* Вимкніть крок `Build`

	![Редагування схеми](images/extensions/debugging/ios/edit_scheme.png)

	![Вимкнення збирання](images/extensions/debugging/ios/disable_build.png)

* Установіть версію `Deployment target` так, щоб вона тепер була вищою за версію iOS на вашому пристрої

	![Версія розгортання](images/extensions/debugging/ios/deployment_version.png)

* Виберіть цільовий пристрій

	![Вибір пристрою](images/extensions/debugging/ios/select_device.png)


### Запуск налагоджувача {#launch-the-debugger}

Є кілька способів налагодження застосунку

1. Виберіть `Debug` -> `Attach to process...` і знайдіть застосунок у списку

2. Або виберіть `Attach to process by PID or Process name`

	![Вибір пристрою](images/extensions/debugging/ios/attach_to_process_name.png)

3. Запустіть застосунок на пристрої

4. У `Edit Scheme` додайте папку <AppName>.app як виконуваний файл

### Налагоджувальні символи {#debug-symbols}

**Для використання lldb виконання має бути призупинене**

* Додайте шлях до `.dSYM` у lldb

```
(lldb) add-dsym <PathTo.dSYM>
```

![Додавання налагоджувальних символів](images/extensions/debugging/ios/add_dsym.png)

* Перевірте, що `lldb` успішно прочитав символи

```
(lldb) image list <AppName>
```

### Зіставлення шляхів {#path-mappings}

* Додайте вихідний код рушія (змініть шляхи відповідно до своїх потреб)

```
(lldb) settings set target.source-map /Users/builder/ci/builds/engine-ios-64-master/build /Users/mathiaswesterdahl/work/defold
(lldb) settings append target.source-map /private/var/folders/m5/bcw7ykhd6vq9lwjzq1mkp8j00000gn/T/job4836347589046353012/upload/videoplayer/src /Users/mathiaswesterdahl/work/projects/extension-videoplayer-native/videoplayer/src
```

* Шлях до папки завдання можна отримати з виконуваного файлу. Папка завдання має назву на кшталт `job1298751322870374150`, щоразу з випадковим числом.

```sh
$ dsymutil -dump-debug-map <executable> 2>&1 >/dev/null | grep /job

```

* Перевірте зіставлення шляхів до вихідного коду

```
(lldb) settings show target.source-map
```

Ви можете перевірити, з якого файлу вихідного коду походить символ, за допомогою

```
(lldb) image lookup -va <SymbolName>
```

### Точки зупину {#breakpoints}

* Відкрийте файл у поданні проєкту та встановіть точку зупину

	![Точка зупину](images/extensions/debugging/ios/breakpoint.png)

## Примітки {#notes}

### Перевірка UUID двійкового файлу {#check-uuid-of-binary}

Щоб налагоджувач прийняв папку `.dSYM`, її UUID має збігатися з UUID виконуваного файлу, який ви налагоджуєте. Перевірити UUID можна так:

```sh
$ dwarfdump -u <PathToBinary>
```
