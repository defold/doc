---
title: Добавление автозаполнения редактора в нативные расширения
brief: В этом руководстве объясняется, как создать определение API сценария, чтобы редактор Defold мог обеспечить автозаполнение для пользовательских расширения.
---

# Автозаполнение для нативных расширений

Редактор Defold обеспечивает автоматическое заполнение предложений для всех функций API Defold и генерирует предложения для модулей Lua, необходимых для ваших скриптов. Однако редактор не может автоматически предоставлять предложения по автозаполнению для функций, предоставляемых родными расширениями. Родное расширение может предоставить определение API в отдельном файле, чтобы обеспечить автоматическое заполнение предложений также для API расширения


## Создание определения API в скрипте

Файл определения API скрипта имеет расширение `.script_api`. Он должен быть в формате [YAML](https://yaml.org/) и находиться вместе с файлами расширения. Ожидаемый формат определения API скрипта следующий:

```yml
- name: The name of the extension
  type: table
  desc: Extension description
  members:
  - name: Name of the first member
    type: Member type
    desc: Member description
    # если тип члена - "function"
    parameters:
    - name: Name of the first parameter
      type: Parameter type
      desc: Parameter description
    - name: Name of the second parameter
      type: Parameter type
      desc: Parameter description
    # если тип члена - "function"
    returns:
    - name: Name of first return value
      type: Return value type
      desc: Return value description
    examples:
    - desc: First example of member usage
    - desc: Second example of member usage

  - name: Name of the second member
    ...
```

Типы могут быть любыми из `table, string, boolean, number, function`. Если значение может иметь несколько типов, оно записывается как `[type1, type2, type3]`.
::: sidenote
В настоящее время типы не отображаются в редакторе. Рекомендуется все же предоставить их, чтобы они были доступны, когда редактор будет поддерживать отображение информации о типах.
:::

## Примеры

Примеры использования приведены в следующих проектах:

* [Расширение для Facebook](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [Расширение для WebView](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
