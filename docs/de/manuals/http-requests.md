---
title: HTTP-Anfragen
brief: Dieses Handbuch erklärt, wie du HTTP-Anfragen sendest.
---

## HTTP-Anfragen {#http-requests}

Defold kann mit der Funktion `http.request()` normale HTTP-Anfragen senden.

### HTTP GET

Dies ist die einfachste Anfrage, um Daten vom Server abzurufen. Beispiel:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

Dies sendet eine HTTP-GET-Anfrage an https://www.defold.com. Die Funktion ist asynchron und blockiert während der Anfrage nicht. Sobald die Anfrage gesendet wurde und ein Server eine Antwort zurückgegeben hat, ruft sie die angegebene Callback-Funktion auf. Die Callback-Funktion erhält die vollständige Serverantwort einschließlich Statuscode und Antwort-Headern. Weiter unten findest du zusätzliche Informationen dazu, wie du mit der Antworttabelle arbeitest.

::: sidenote
HTTP-Anfragen werden automatisch im Cache des Clients gespeichert, um die Netzwerkleistung zu verbessern. Die zwischengespeicherten Dateien werden in einem betriebssystemspezifischen Pfad für Anwendungsdaten in einem Ordner namens `defold/http-cache` gespeichert. Normalerweise musst du dich nicht um den HTTP-Cache kümmern. Wenn du den Cache während der Entwicklung leeren musst, kannst du den Ordner mit den zwischengespeicherten Dateien manuell löschen. Unter macOS befindet sich dieser Ordner in `%HOME%/Library/Application Support/Defold/http-cache/` und unter Windows in `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST

Wenn du Daten wie einen Punktestand oder Authentifizierungsdaten an einen Server sendest, geschieht dies üblicherweise mit einer POST-Anfrage:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### Weitere HTTP-Methoden {#other-http-methods}

HTTP-Anfragen in Defold unterstützen auch die Methoden HEAD, DELETE und PUT. Die Methode CONNECT wird ebenfalls unterstützt (siehe den Abschnitt über Proxy-Verbindungen weiter unten).

### Mit der HTTP-Antwort arbeiten {#how-to-work-with-the-http-response}

Die im Callback zurückgegebene Tabelle `response` enthält alle Informationen, die du für eine differenzierte Verarbeitung der Antwort benötigst. Zwei der wichtigsten Felder sind `status` und `response`:

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

Wenn die Antwort einen großen Block binärer Daten enthält, etwa ein Bild oder ein Musikstück, kann es sinnvoll sein, die Daten in eine Datei zu schreiben, statt sie in den Arbeitsspeicher zu laden:

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

Ein weiterer Anwendungsfall für das Laden großer Datenmengen über das Netzwerk ist Audiostreaming. Dabei werden „Blöcke“ von Audiodaten von einer URL geladen und einer Audioressource zugeführt. Ein vollständiges Beispiel findest du im [Handbuch zum Audiostreaming](/sound-streaming#sound-streaming).


### Anfrage-Header {#request-headers}

Beim Senden einer Anfrage kannst du zusätzliche Header setzen. So kannst du beispielsweise einen `Authorization`-Header oder `Content-Type` setzen, um dem Server mitzuteilen, welches Format der Anfrageinhalt hat.

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

Defold setzt einige Anfrage-Header automatisch:

* `If-None-Match: <etag>` wird auf den ETag einer zuvor zwischengespeicherten Antwort gesetzt.
* `Transfer-Encoding: chunked` wird gesetzt, wenn der Anfrageinhalt größer als 16384 Bytes ist.
* `Content-Length` wird auf die Größe des Anfrageinhalts gesetzt (außer wenn die Anfrage in Blöcken übertragen wird).
* `Range: bytes=<from>-<to>` wird gesetzt, wenn eine Teilantwort angefordert wird, beispielsweise beim [Streamen von Audiodaten](/sound-streaming#sound-streaming).


### Antwort-Header {#response-headers}

Die Serverantwort kann einen oder mehrere Antwort-Header enthalten. Diese sind in der Tabelle `response` verfügbar:

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### HTTP-Proxy

Manchmal ist es erwünscht, eine Anfrage über einen Proxyserver zu senden. Dazu kannst du einen Proxyserver angeben, der beim Verbinden mit dem Zielserver verwendet wird. Wenn ein Proxy verwendet wird, wird die Verbindung zum Zielserver über einen HTTP-Tunnel durch den Proxy aufgebaut. Der HTTP-Tunnel wird mit der HTTP-Methode CONNECT aufgebaut. Beispiel:


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

### API-Referenz {#api-reference}

Weitere Informationen findest du in der [API-Referenz](/ref/http/).

### Erweiterungen {#extensions}

Eine alternative Implementierung für HTTP-Anfragen findest du in der [TinyHTTP-Erweiterung](https://defold.com/assets/tinyhttp/).
