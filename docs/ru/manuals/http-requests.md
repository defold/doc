---
title: HTTP запросы
brief: В этом руководстве объясняется, как выполнять HTTP запросы.
---

## HTTP запросы

Defold может выполнять обычные HTTP запросы с помощью функции `http.request()`.

### HTTP GET

Это самый базовый запрос для получения данных с сервера. Пример:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

Этот код выполнит HTTP GET запрос к https://www.defold.com. Функция асинхронная и не блокирует выполнение во время запроса. Когда запрос будет выполнен и сервер отправит ответ, будет вызвана переданная callback-функция. Функция обратного вызова получит полный ответ сервера, включая код состояния и заголовки ответа. Ниже приведена дополнительная информация о том, как работать с таблицей ответа.

::: sidenote
HTTP запросы автоматически кэшируются на клиенте для повышения производительности сети. Кэшированные файлы хранятся в зависящем от ОС пути поддержки приложения, в папке `defold/http-cache`. Обычно вам не нужно беспокоиться о HTTP кэше, но если во время разработки его нужно очистить, можно вручную удалить папку с кэшированными файлами. На macOS эта папка находится в `%HOME%/Library/Application Support/Defold/http-cache/`, а на Windows в `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST

Когда нужно отправить данные, например результат или данные аутентификации, на сервер, обычно используется POST запрос:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### Другие HTTP методы

HTTP запросы Defold также поддерживают методы HEAD, DELETE и PUT. Метод CONNECT тоже поддерживается (см. раздел о прокси-подключениях ниже).

### Как работать с HTTP ответом

Таблица `response`, передаваемая в callback-функцию, содержит всю информацию, необходимую для детальной обработки ответа. Два ключевых поля это `status` и `response`:

```lua

local function handle_response(self, id, response)
	-- проверяем код состояния ответа. Распространенные коды:
	-- 200 OK - запрос успешно завершен
	-- 301 Moved permanently - запрошенные данные были перемещены, смотрите заголовок redirect
	-- 307 Temporary redirect - то же, что и выше
	-- 208 Permanent redirect - то же, что и выше
	-- 400 Bad Request - запрос был сформирован неверно
	-- 401 Unauthorized - клиент должен пройти аутентификацию
	-- 404 Not Found - сервер не может найти информацию
	-- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
	if response.status == 200 then
		-- данные ответа
		-- это может быть обычный текст, данные в формате json или бинарные данные
		print(response.response)
		json.decode(response.response)
		sys.save(..., response.response)
	end
end
```

Когда ответ содержит большой бинарный блок данных, например изображение или музыкальный трек, может иметь смысл записать данные в файл, а не загружать их в память:

```lua
-- в этом примере мы загружаем myimage.png и сразу записываем его в файл на диске

local options = {
	path = sys.get_save_file("mygame", "myimage.png")
}

local function handle_response(self, id, response)
	if response.status == 200 then
		print("Файл был успешно записан в:", response.path)
		print("Размер файла:", response.document_size)
		print("Путь к файлу:", response.path)
	else
		print("Файл не был записан на диск:", response.error)
	end
end

http.request("https://www.foobar.com/myimage.png", "GET", handle_response)
```

Еще один сценарий использования загрузки больших объемов данных по сети это потоковая передача звука, когда "фрагменты" звуковых данных загружаются по URL и передаются в звуковой ресурс. Полный пример можно найти в [руководстве по потоковой передаче звука](/sound-streaming#sound-streaming).


### Заголовки запроса

При отправке запроса можно задавать дополнительные заголовки. Например, это можно использовать для установки заголовка авторизации или типа содержимого, чтобы сообщить серверу, в каком формате отправлены данные.

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

-- отправляем данные формы
local headers = {
	["Content-Type"] = "application/x-www-form-urlencoded"
}
local body = "key1=value1&key2=value2"
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- отправляем данные, закодированные в json
local headers = {
	["Content-Type"] = "application/json"
}
local body = json.encode({ key1 = value1, key2 = value2 })
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- запрашиваем данные, для доступа к которым требуется авторизация
local token = ... -- генерируем токен доступа (JWT, OAuth и т.д.)
local headers = {
	["Authorization"] = "Bearer " .. token
}
http.request("https://www.myserver.com/content", "GET", handle_response, headers)
```

Defold автоматически устанавливает несколько заголовков запроса:

* `If-None-Match: <etag>` будет установлен с ETag любого ранее кэшированного ответа.
* `Transfer-Encoding: chunked` будет установлен, если тело запроса больше 16384 байт.
* `Content-Length` будет установлен с размером тела запроса (если запрос не использует chunked).
* `Range: bytes=<from>-<to>` будет установлен при запросе частичного ответа, например при [потоковой передаче звука](/sound-streaming#sound-streaming).


### Заголовки ответа

Ответ сервера может содержать один или несколько заголовков ответа. Они доступны в таблице `response`:

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### HTTP Proxy

Иногда бывает нужно отправить запрос через прокси-сервер. Это можно сделать, указав прокси-сервер, который следует использовать при подключении к целевому серверу. Когда используется прокси, соединение с целевым сервером устанавливается через HTTP туннель через прокси. Этот HTTP туннель создается с помощью метода CONNECT. Пример:


```lua
-- подключаемся к www.defold.com через локальный прокси на порту 8888
local url = "https://www.defold.com:443"
local method = "GET"
local headers = {}
local post_data = nil
local options = {
	proxy = "https://127.0.0.1:8888"
}
http.request(url, method, function(self, id, response)
	pprint(response)
end, headers, post_data, options)
```

### Справочник по API

Обратитесь к [справочнику API](/ref/http/), чтобы узнать больше.

### Расширения

Альтернативную реализацию HTTP запросов можно найти в [расширении TinyHTTP](https://defold.com/assets/tinyhttp/).
