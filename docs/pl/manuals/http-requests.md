---
title: Żądania HTTP
brief: Ta instrukcja wyjaśnia, jak wykonywać żądania HTTP.
---

## Żądania HTTP

Defold może wykonywać zwykłe żądania HTTP za pomocą funkcji `http.request()`.

### HTTP GET

To najbardziej podstawowe żądanie służące do pobrania danych z serwera. Przykład:

```Lua
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

### Inne metody HTTP

Żądania HTTP w Defold obsługują także metody HEAD, DELETE i PUT.

### Dokumentacja API

Aby dowiedzieć się więcej, zobacz [dokumentację API](/ref/http/).

### Rozszerzenia

Alternatywną implementację żądań HTTP znajdziesz w [rozszerzeniu TinyHTTP](https://defold.com/assets/tinyhttp/).
