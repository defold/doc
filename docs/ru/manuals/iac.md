---
title: Inter-app communication в Defold
brief: Inter-app communication позволяет определять аргументы запуска, используемые при запуске приложения. В этом руководстве объясняется API Defold и весь доступный функционал.
---

# Inter-app communication

В большинстве операционных систем приложения могут быть запущены несколькими способами:

* Из списка установленных приложений.
* Из ссылки на конкретное приложение.
* Из push-уведомления.
* В качестве последнего шага процесса установки.

В случае, когда приложение запускается по ссылке, уведомлению или при установке, можно передать дополнительные аргументы, такие как referrer или deep-link при запуске, по специфической для приложения ссылке или уведомлению. Defold предоставляет унифицированный способ получения информации о том, как приложение было вызвано с помощью встроенных расширений.

## Установка расширения

Чтобы начать использовать расширение Inter-app communication, необходимо добавить его в качестве зависимости в файл `game.project`. Последняя стабильная версия доступна по URL-адресу зависимости:
```
https://github.com/defold/extension-iac/archive/master.zip
```

Мы рекомендуем использовать ссылку на zip-файл [конкретного выпуска](https://github.com/defold/extension-iac/releases).

## Использование расширения

API очень прост в использовании. Мы предоставляете расширению функцию и обратную связь слушателя.

```
local function iac_listener(self, payload, type)
     if type == iac.TYPE_INVOCATION then
         -- This was an invocation
         print(payload.origin) -- origin may be empty string if it could not be resolved
         print(payload.url)
     end
end

function init(self)
     iac.set_listener(iac_listener)
end
```

Полная документация по API доступна на странице [GitHub](https://defold.github.io/extension-iac/).