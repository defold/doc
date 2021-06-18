---
title: HTTP запросы
brief: Данное руководство объясняет как делать HTTP запросы.
---

## HTTP запросы

Defold может делать обыкновенные HTTP запросы с использованием функции `http.request()`.

### HTTP GET

Это самый базовый запрос, чтобы получить некие данные от сервера. Пример:

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

Данный код выполнит HTTP GET запрос на адрес https://www.defold.com. Эта функция асинхронна и она не заблокирует основной код по мере выполнения запроса. Как только запрос будет сделан и сервер отправит ответ, будет вызвана предоставленная функция обратного вызова. Функция обратного вызова получит полный ответ сервера, включая код статуса и заголовки ответа.

::: sidenote
HTTP запросы автоматически кэшируются на клиенте для повышения сетевой производительности. Кэшированные файлы хранятся по специфичному для каждой ОС пути в папке с именем `defold/http-cache`. Обычно вам не нужно беспокоиться о HTTP кэше, но если вам нужно очищать кэш во время разработки, вы можете вручную удалить папку, содержащую кэшированные файлы. На macOS эта папка располагается в `%HOME%/Library/Application Support/Defold/http-cache/`, а на Windows в `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST

Посылка данных, таких как очки или некие данные аутентификации, на сервер обычно делается через POST запросы:

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local headers = {
	["Content-Type"] = "application/x-www-form-urlencoded"
}
local body = "foo=bar"
http.request("https://httpbin.org/post", "POST", handle_response, headers, body)
```

### Другие HTTP методы

HTTP запросы в Defold также поддерживают методы HEAD, DELETE и PUT.

### Справочник по API

Обратитесь к [Справочнику по API](/ref/http/) чтобы узнать больше.

### Расширения

Альтернативную реализацию HTTP запросов можно найти здесь [TinyHTTP extension](https://defold.com/assets/tinyhttp/).
