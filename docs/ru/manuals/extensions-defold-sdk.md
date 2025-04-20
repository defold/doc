---
title: Нативные расширения - Defold SDK
brief: В этом руководстве описывается работа с Defold SDK при создании нативных расширений.
---

# Defold SDK

Defold SDK содержит необходимую функциональность для объявления нативного расширения, а также взаимодействия с низкоуровневым нативным слоем платформы, на котором работает приложение, и высокоуровневым слоем Lua, в котором создается игровая логика.

## Использование

Используете Defold SDK, включив заголовочный файл `dmsdk/sdk.h`:

    #include <dmsdk/sdk.h>

Доступные функции SDK документированы в [API reference](/ref/dmExtension/). SDK содержит следующие пространства имен с функциями:

* [Align](/ref/dmAlign/) - Макросы выравнивания. Используются для совместимости с компилятором
* [Array](/ref/dmArray/) - Шаблонный массив с проверкой границ.
* [Buffer](/ref/dmBuffer/) - API для буферов данных как основного способа взаимодействия между системами. Для буфера создания также существует [Lua API](/ref/buffer/).
* [Condition Variable](/ref/dmConditionVariable/) - API для условной переменной независимого от платформы синхронизации mutex.
* [ConfigFile](/ref/dmConfigFile/) - Функции доступа к файлу конфигурации. Файл конфигурации является скомпилированной версией файла *game.project*.
* [Connection Pool](/ref/dmConnectionPool/) - API для пула сокетных соединений.
* [Crypt](/ref/dmCrypt/) - API с криптографическими функциями.
* [DNS](/ref/dmDNS/) - API с функциями DNS.
* [Engine](/ref/dmEngine/) - API с основной функциональностью движка для получения доступа к файлам конфигурации, внутреннему веб-серверу, реестру игровых объектов и т.д.
* [Extension](/ref/dmExtension/) - Функции для создания и управления нативными библиотеками расширений движка.
* [Game Object](/ref/dmGameObject/) - API для манипулирования игровыми объектами.
* [Graphics](/ref/dmGraphics/) - Встроенные графические функции, специфичные для конкретной платформы.
* [Hash](/ref/dmHash/) - Хеш-функции.
* [HID](/ref/dmHid/) - API для генерации программных событий ввода.
* [HTTP Client](/ref/dmHttpClient/) - API для взаимодействия с HTTP-клиентами.
* [Json](/ref/dmJson/) - API для независимого от платформы парсинга json-файлов.
* [Log](/ref/dmLog/) - Функции ведения журнала.
* [Math](/ref/dmMath/) - API с математическими функциями.
* [Mutex](/ref/dmMutex/) - API для независимого от платформы синхронизации mutex.
* [SSL Socket](/ref/dmSSLSocket/) - API для функций защищенных сокетов.
* [Script](/ref/dmScript/) - Встроенные функции для создание скриптов.
* [Socket](/ref/dmSocket/) - API для функций сокетов.
* [String Functions](/ref/dmStringFunc/) - API для манипуляций со строками.
* [Thread](/ref/dmThread/) - API для создания потоков.
* [Time](/ref/dmTime/) - API для универсального времени и функций времени.
* [URI](/ref/dmURI/) - API для манипуляций с URI.
* [Web Server](/ref/dmWebServer/) - API для простого высокоуровневого однопоточного веб-сервера, основанного на `dmHttpServer`.
* [Shared Library](/ref/sharedlibrary/) - Утилитные функции для экспорта/импорта общих библиотек.
* [Sony vector Math Library](../assets/Vector_Math_Library-Overview.pdf) - Библиотека Sony Vector Math в основном предоставляет функции, используемые в трехмерной графике для трехмерных и четырехмерных векторных операций, матричных операций и операций с кватернионами.

Если вам нужен заголовочный файл `dmsdk/sdk.h` для кода в выбранном вами редакторе, его можно найти [здесь в основном репозитории GitHub для Defold](https://github.com/defold/defold/blob/dev/engine/sdk/src/dmsdk/sdk.h) с [заголовочными файлами для отдельных пространств имен](https://github.com/defold/defold/tree/dev/engine/dlib/src/dmsdk/dlib).
