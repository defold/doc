---
title: Нативные расширения - Defold SDK
brief: В этом руководстве описывается работа с Defold SDK при создании нативных расширений.
---

# Defold SDK

Defold SDK содержит необходимую функциональность для объявления нативного расширения, а также взаимодействия с низкоуровневым нативным слоем платформы, на котором работает приложение, и высокоуровневым слоем Lua, в котором создается игровая логика.

## Использование

Используете Defold SDK, включив заголовочный файл `dmsdk/sdk.h`:

    #include <dmsdk/sdk.h>
    
Доступные функции SDK и пространства имён задокументированы в нашем [справочнике по API](/ref/overview_cpp). Заголовочные файлы Defold SDK включены в отдельный архив `defoldsdk_headers.zip` для каждого [релиза Defold на GitHub](https://github.com/defold/defold/releases). Вы можете использовать эти заголовочные файлы для автодополнения кода в выбранном вами редакторе.
