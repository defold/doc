---
title: HTTP-запити
brief: Цей посібник пояснює, як виконувати HTTP-запити.
---

## HTTP-запити {#http-requests}

У Defold можна виконувати звичайні HTTP-запити за допомогою функції `http.request()`.

### HTTP GET {#http-get}

Це найпростіший запит для отримання даних із сервера. Приклад:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

Цей код виконає запит HTTP GET до https://www.defold.com. Функція асинхронна й не блокує виконання під час запиту. Щойно запит буде виконано й сервер надішле відповідь, вона викличе передану функцію зворотного виклику. Функція зворотного виклику отримає повну відповідь сервера, зокрема код статусу та заголовки відповіді. Докладніше про роботу з таблицею відповіді читайте нижче.

::: sidenote
HTTP-запити автоматично кешуються на клієнті для підвищення продуктивності мережі. Кешовані файли зберігаються в теці `defold/http-cache` за шляхом до допоміжних даних застосунків, який залежить від ОС. Зазвичай вам не потрібно дбати про кеш HTTP, але якщо під час розробки його потрібно очистити, ви можете вручну видалити теку з кешованими файлами. У macOS ця тека розташована в `%HOME%/Library/Application Support/Defold/http-cache/`, а у Windows — у `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST {#http-post}

Для надсилання даних на сервер, наприклад набраних очок або даних автентифікації, зазвичай використовують запити POST:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### Інші методи HTTP {#other-http-methods}

HTTP-запити в Defold також підтримують методи HEAD, DELETE і PUT. Метод CONNECT теж підтримується (див. розділ про з’єднання через проксі нижче).

### Як працювати з відповіддю HTTP {#how-to-work-with-the-http-response}

Таблиця `response`, повернена у функцію зворотного виклику, містить усю інформацію, необхідну для реалізації детальної обробки відповіді. Два ключові поля — `status` і `response`:

```lua

local function handle_response(self, id, response)
	-- check the response status code. Common response codes:
	-- 200 OK - the request completed successfully
	-- 301 Moved permanently - the requested data has moved, see redirect header
	-- 307 Temporary redirect - same as above
	-- 208 Permanent redirect - same as above
	-- 400 Bad Request - the request was malformed
	-- 401 Unauthorized - the client must authenticate itself
	-- 404 Not Found - the server cannot find the information
	-- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
	if response.status == 200 then
		-- the response data
		-- this can be anything from plain text, json encoded data or binary data
		print(response.response)
		json.decode(response.response)
		sys.save(..., response.response)
	end
end
```

Коли відповідь містить великий блок двійкових даних, наприклад зображення або музичну композицію, може бути доцільно записати дані у файл замість завантаження в пам’ять:

```lua
-- in this example we download myimage.png and write it directly to a file on disk

local options = {
	path = sys.get_save_file("mygame", "myimage.png")
}

local function handle_response(self, id, response)
	if response.status == 200 then
		print("File was successfully written to:", response.path)
		print("File size:", response.document_size)
		print("File path:", response.path)
	else
		print("File was not written to disk:", response.error)
	end
end

http.request("https://www.foobar.com/myimage.png", "GET", handle_response, nil, nil, options)
```

Ще один випадок завантаження великих обсягів даних через мережу — потокове передавання звуку, коли «порції» звукових даних завантажуються з URL і передаються у звуковий ресурс. Повний приклад наведено в [посібнику з потокового передавання звуку](/sound-streaming#sound-streaming).


### Заголовки запиту {#request-headers}

Під час надсилання запиту можна встановити додаткові заголовки. Наприклад, можна встановити заголовок `Authorization` або `Content-Type`, щоб повідомити серверу формат тіла запиту.

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

-- send some form data
local headers = {
	["Content-Type"] = "application/x-www-form-urlencoded"
}
local body = "key1=value1&key2=value2"
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- send some json encoded data
local headers = {
	["Content-Type"] = "application/json"
}
local body = json.encode({ key1 = value1, key2 = value2 })
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- request some data which requires authorization to access
local token = ... -- generate an access token (JWT, OAuth etc)
local headers = {
	["Authorization"] = "Bearer " .. token
}
http.request("https://www.myserver.com/content", "GET", handle_response, headers)
```

Defold автоматично встановлює кілька заголовків запиту:

* `If-None-Match: <etag>` встановлюється зі значенням ETag раніше кешованої відповіді.
* `Transfer-Encoding: chunked` встановлюється, якщо тіло запиту перевищує 16384 байти.
* `Content-Length` встановлюється відповідно до розміру тіла запиту (якщо запит не передається частинами).
* `Range: bytes=<from>-<to>` встановлюється під час запиту часткової відповіді, наприклад для [потокового передавання звуку](/sound-streaming#sound-streaming).


### Заголовки відповіді {#response-headers}

Відповідь сервера може містити один або кілька заголовків відповіді. Вони доступні в таблиці `response`:

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### HTTP-проксі {#http-proxy}

Іноді виникає потреба надіслати запит через проксі-сервер. Для цього можна вказати проксі-сервер, який використовуватиметься для з’єднання із цільовим сервером. Коли використовується проксі, з’єднання із цільовим сервером встановлюється через HTTP-тунель у проксі. HTTP-тунель встановлюється за допомогою методу HTTP CONNECT. Приклад:


```lua
-- connect to www.defold.com via localhost proxy on port 8888
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

### Довідник API {#api-reference}

Щоб дізнатися більше, зверніться до [довідника API](/ref/http/).

### Розширення {#extensions}

Альтернативну реалізацію HTTP-запитів можна знайти в [розширенні TinyHTTP](https://defold.com/assets/tinyhttp/).
