---
title: Налагодження — журнали гри й системи
brief: У цьому посібнику пояснюється, як читати журнали гри й системи.
---

# Журнали гри й системи {#game-and-system-log}

У журналі гри відображається все виведення рушія, нативних розширень і вашої ігрової логіки. Команди [print()](/ref/stable/base/#print:...) і [pprint()](/ref/stable/builtins/?q=pprint#pprint:v) можна використовувати у скриптах і модулях Lua, щоб виводити інформацію в журнал гри. Для запису в журнал гри з нативних розширень можна використовувати функції з [простору імен `dmLog`](/ref/stable/dmLog/). Журнал гри можна читати в редакторі, у вікні термінала, за допомогою інструментів для конкретної платформи або з файлу журналу.

Системні журнали створює операційна система, і вони можуть містити додаткову інформацію, яка допоможе точно визначити проблему. Системні журнали можуть містити трасування стека для аварійних завершень і попередження про нестачу пам’яті.

::: important
Виведення журналу в консоль/на екран показує інформацію лише в налагоджувальних збірках (Debug). У збірках випуску (Release) журнал консолі порожній, але для Release можна ввімкнути запис журналу у файл, задавши налаштуванню проєкту «Write Log File» значення «Always». Докладніше див. нижче.
:::

## Читання журналу гри в редакторі {#reading-the-game-log-from-the-editor}

Коли ви запускаєте гру локально з редактора або підключаєтеся до [мобільного застосунку для розробки](/manuals/dev-app), усе виведення відображається на панелі консолі редактора:

![Редактор 2](images/editor/editor2_overview.png)

## Читання журналу гри в терміналі {#reading-the-game-log-from-the-terminal}

Коли ви запускаєте гру Defold з термінала, журнал відображається в самому вікні термінала. У Windows і Linux для запуску гри введіть у терміналі ім’я виконуваного файлу. У macOS потрібно запустити рушій із файлу .app:

```
$ > ./mygame.app/Contents/MacOS/mygame
```

## Читання журналів гри й системи за допомогою інструментів для конкретної платформи {#reading-game-and-system-logs-using-platform-specific-tools}

### HTML5 {#html5}

Журнали можна читати за допомогою інструментів розробника, доступних у більшості браузерів.

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - Menu > More Tools > Developer Tools
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - Tools > Web Developer > Web Console
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - Develop > Show JavaScript Console

### Android {#android}

Для перегляду журналів гри й системи можна використовувати інструмент Android Debug Bridge (ADB).

:[Android ADB](../shared/android-adb.md)

Після встановлення й налаштування підключіть пристрій через USB, відкрийте термінал і виконайте:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat
```

Після цього пристрій передаватиме все виведення в поточний термінал разом з усіма повідомленнями, які виводить гра.

Щоб бачити лише виведення застосунку Defold, скористайтеся цією командою:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialized sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS {#ios}

Є кілька способів читати журнали гри й системи в iOS:

1. Для читання журналів гри й системи можна використовувати [інструмент Console](https://support.apple.com/guide/console/welcome/mac).
2. Можна використовувати налагоджувач LLDB, щоб підключитися до гри, запущеної на пристрої. Для налагодження гри її потрібно підписати за допомогою профілю «Apple Developer Provisioning Profile», до якого включено пристрій, на якому ви хочете виконувати налагодження. Створіть пакет гри в редакторі та вкажіть профіль підготовки в діалоговому вікні пакування (пакування для iOS доступне лише в macOS).

Щоб запустити гру й підключити налагоджувач, знадобиться інструмент [ios-deploy](https://github.com/phonegap/ios-deploy). Установіть гру й запустіть її налагодження, виконавши в терміналі таку команду:

```txt
$ ios-deploy --debug --bundle <path_to_game.app> # NOTE: not the .ipa file
```

Ця команда встановить застосунок на пристрій, запустить його й автоматично підключить до нього налагоджувач LLDB. Якщо ви ще не знайомі з LLDB, прочитайте [Початок роботи з LLDB](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html).


## Читання журналу гри з файлу журналу {#reading-the-game-log-from-the-log-file}

Використовуйте налаштування проєкту «Write Log File» у *game.project*, щоб керувати записом журналу у файл:

- «Never»: не записувати файл журналу.
- «Debug»: записувати файл журналу лише для налагоджувальних збірок.
- «Always»: записувати файл журналу як для налагоджувальних збірок, так і для збірок випуску.

Коли запис увімкнено, усе виведення гри записується на диск у файл `log.txt`. Ось як отримати цей файл, якщо ви запускаєте гру на пристрої:

iOS
: Підключіть пристрій до комп’ютера з установленими macOS і Xcode.

  Відкрийте Xcode і перейдіть до <kbd>Window ▸ Devices and Simulators</kbd>.

  Виберіть свій пристрій у списку, а потім виберіть відповідний застосунок у списку *Installed Apps*.

  Натисніть значок шестерні під списком і виберіть <kbd>Download Container...</kbd>.

  ![Завантаження контейнера](images/debugging/download_container.png)

  Після отримання контейнер відобразиться у *Finder*. Клацніть контейнер правою кнопкою миші й виберіть <kbd>Show Package Content</kbd>. Знайдіть файл `log.txt`, який має бути в `AppData/Documents/`.

Android(
: Можливість отримати `log.txt` залежить від версії ОС і виробника. Ось короткий і простий [покроковий посібник](https://stackoverflow.com/a/48077004/129360).
