---
title: Żądania HTTP
brief: Ta instrukcja wyjaśnia, jak wykonywać żądania HTTP.
---

## Żądania HTTP

Defold może wykonywać zwykłe żądania HTTP za pomocą funkcji `http.request()`.

### HTTP GET

To najbardziej podstawowe żądanie służące do pobrania danych z serwera. Przykład:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

Spowoduje to wysłanie żądania HTTP GET do adresu https://www.defold.com. Funkcja działa asynchronicznie i nie blokuje programu podczas wykonywania żądania. Gdy żądanie zostanie wysłane, a serwer zwróci odpowiedź, wywoła przekazaną funkcję zwrotną. Funkcja zwrotna otrzyma pełną odpowiedź serwera, w tym kod statusu i nagłówki odpowiedzi.

::: sidenote
Żądania HTTP są automatycznie buforowane w kliencie, aby poprawić wydajność sieci. Zbuforowane pliki są przechowywane w ścieżce specyficznej dla systemu operacyjnego, w folderze o nazwie `defold/http-cache`. Zwykle nie trzeba zajmować się buforem HTTP, ale jeśli chcesz go wyczyścić podczas pracy nad projektem, możesz ręcznie usunąć folder zawierający zbuforowane pliki. Na macOS folder ten znajduje się w `%HOME%/Library/Application Support/Defold/http-cache/`, a w systemie Windows w `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST

Gdy wysyłasz do serwera dane, takie jak wynik punktowy albo dane uwierzytelniające, zwykle robi się to za pomocą żądania POST:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```

### Inne metody HTTP

Żądania HTTP w Defold obsługują także metody HEAD, DELETE i PUT. Obsługiwana jest również metoda CONNECT (zobacz sekcję o połączeniach proxy poniżej).

### Jak pracować z odpowiedzią HTTP

Tabela `response` zwracana w callbacku zawiera wszystkie informacje potrzebne do szczegółowej obsługi odpowiedzi. Dwa najważniejsze pola to `status` i `response`:

```lua

local function handle_response(self, id, response)
	-- sprawdź kod statusu odpowiedzi. Typowe kody:
	-- 200 OK - żądanie zakończyło się powodzeniem
	-- 301 Moved permanently - żądane dane zostały przeniesione, zobacz nagłówek redirect
	-- 307 Temporary redirect - jak wyżej
	-- 208 Permanent redirect - jak wyżej
	-- 400 Bad Request - żądanie było niepoprawnie sformułowane
	-- 401 Unauthorized - klient musi się uwierzytelnić
	-- 404 Not Found - serwer nie może znaleźć informacji
	-- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
	if response.status == 200 then
		-- dane odpowiedzi
		-- może to być zwykły tekst, dane zakodowane jako json albo dane binarne
		print(response.response)
		json.decode(response.response)
		sys.save(..., response.response)
	end
end
```

Gdy odpowiedź zawiera duży blok danych binarnych, na przykład obraz albo utwór muzyczny, sensowne może być zapisanie danych do pliku zamiast wczytywania ich do pamięci:

```lua
-- w tym przykładzie pobieramy myimage.png i zapisujemy go bezpośrednio do pliku na dysku

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

Innym przypadkiem użycia dużych ilości danych pobieranych przez sieć jest strumieniowanie dźwięku, gdy „fragmenty” danych dźwiękowych są wczytywane z adresu URL i przekazywane do zasobu dźwięku. Pełny przykład znajdziesz w [podręczniku strumieniowania dźwięku](/sound-streaming#sound-streaming).

### Nagłówki żądania

Podczas wysyłania żądania można ustawić dodatkowe nagłówki. Można tego użyć na przykład do ustawienia nagłówka autoryzacji albo typu zawartości, aby poinformować serwer o formacie danych.

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

-- wyślij dane formularza
local headers = {
	["Content-Type"] = "application/x-www-form-urlencoded"
}
local body = "key1=value1&key2=value2"
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- wyślij dane zakodowane jako json
local headers = {
	["Content-Type"] = "application/json"
}
local body = json.encode({ key1 = value1, key2 = value2 })
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- pobierz dane wymagające autoryzacji
local token = ... -- wygeneruj token dostępu (JWT, OAuth itd.)
local headers = {
	["Authorization"] = "Bearer " .. token
}
http.request("https://www.myserver.com/content", "GET", handle_response, headers)
```

Defold automatycznie ustawi kilka nagłówków żądania:

* `If-None-Match: <etag>` zostanie ustawiony z ETagiem każdej wcześniej zbuforowanej odpowiedzi.
* `Transfer-Encoding: chunked` zostanie ustawiony, jeśli ciało żądania jest większe niż 16384 bajty.
* `Content-Length` zostanie ustawiony z rozmiarem ciała żądania, chyba że żądanie jest dzielone na fragmenty.
* `Range: bytes=<from>-<to>` zostanie ustawiony przy żądaniu częściowej odpowiedzi, na przykład podczas [strumieniowania dźwięków](/manuals/sound-streaming/#sound-streaming).

### Nagłówki odpowiedzi

Odpowiedź serwera może zawierać jeden lub więcej nagłówków. Są one dostępne w tabeli `response`:

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```

### HTTP Proxy

Czasem warto wysłać żądanie przez serwer proxy. Można to zrobić, wskazując serwer proxy używany podczas łączenia z serwerem docelowym. Gdy używany jest proxy, połączenie z serwerem docelowym jest ustanawiane przez tunel HTTP przez proxy. Tunel HTTP jest ustanawiany za pomocą metody HTTP CONNECT. Przykład:

```lua
-- połącz się z www.defold.com przez lokalny proxy na porcie 8888
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

### Dokumentacja API

Aby dowiedzieć się więcej, zobacz [dokumentację API](/ref/http/).

### Rozszerzenia

Alternatywną implementację żądań HTTP znajdziesz w [rozszerzeniu TinyHTTP](https://defold.com/assets/tinyhttp/).
