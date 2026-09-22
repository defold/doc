---
title: Додавання автодоповнення в редакторі для нативних розширень
brief: Цей посібник пояснює, як створити опис API скриптів, щоб редактор Defold міг пропонувати автодоповнення користувачам розширення.
---

# Автодоповнення для нативних розширень {#auto-complete-for-native-extensions}

Редактор Defold пропонує підказки автодоповнення для всіх функцій API Defold і генерує підказки для модулів Lua, підключених у ваших скриптах. Однак редактор не може автоматично пропонувати підказки автодоповнення для функціональності, яку надають нативні розширення. Нативне розширення може містити опис API в окремому файлі, щоб увімкнути підказки автодоповнення також для API розширення.


## Створення опису API скриптів {#creating-a-script-api-definition}

Файл опису API скриптів має розширення `.script_api`. Він має бути у [форматі YAML](https://yaml.org/) і розташовуватися разом із файлами розширення. Очікуваний формат опису API скриптів:

```yml
- name: The name of the extension
  type: table
  desc: Extension description
  members:
  - name: Name of the first member
    type: Member type
    desc: Member description
    # if member type is "function"
    parameters:
    - name: Name of the first parameter
      type: Parameter type
      desc: Parameter description
    - name: Name of the second parameter
      type: Parameter type
      desc: Parameter description
    # if member type is "function"
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

Типом може бути будь-який із `table, string , boolean, number, function`. Якщо значення може мати кілька типів, їх записують як `[type1, type2, type3]`.
::: sidenote
Наразі типи не відображаються в редакторі. Рекомендуємо все ж указувати їх, щоб вони були доступні, щойно редактор почне підтримувати відображення інформації про типи.
:::

## Приклади {#examples}

Приклади реального використання наведено в таких проєктах:

* [Розширення Facebook](https://github.com/defold/extension-facebook/tree/master/facebook/api)
* [Розширення WebView](https://github.com/defold/extension-webview/blob/master/webview/api/webview.script_api)
