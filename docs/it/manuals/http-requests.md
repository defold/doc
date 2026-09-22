---
title: Richieste HTTP
brief: Questo manuale spiega come effettuare richieste HTTP.
---

## Richieste HTTP {#http-requests}

Defold può effettuare normali richieste HTTP tramite la funzione `http.request()`.

### HTTP GET

Questa è la richiesta più semplice per ottenere dati dal server. Esempio:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

Questo codice effettua una richiesta HTTP GET a https://www.defold.com. La funzione è asincrona e non blocca l'esecuzione durante la richiesta. Una volta inviata la richiesta e ricevuta la risposta del server, viene chiamata la funzione di callback fornita. La callback riceve la risposta completa del server, inclusi il codice di stato e le intestazioni della risposta. Più avanti trovi ulteriori informazioni su come gestire la tabella della risposta.

::: sidenote
Le richieste HTTP vengono memorizzate automaticamente nella cache del client per migliorare le prestazioni di rete. I file della cache vengono salvati in una cartella denominata `defold/http-cache`, all'interno di un percorso di supporto dell'applicazione specifico del sistema operativo. Di solito non devi occuparti della cache HTTP, ma se hai bisogno di svuotarla durante lo sviluppo puoi eliminare manualmente la cartella che contiene i file della cache. Su macOS questa cartella si trova in `%HOME%/Library/Application Support/Defold/http-cache/` e su Windows in `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST

Per inviare dati a un server, per esempio un punteggio o dati di autenticazione, si usa in genere una richiesta POST:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### Altri metodi HTTP {#other-http-methods}

Le richieste HTTP di Defold supportano anche i metodi HEAD, DELETE e PUT. È supportato anche il metodo CONNECT (vedi più avanti la sezione sulle connessioni tramite proxy).

### Come gestire la risposta HTTP {#how-to-work-with-the-http-response}

La tabella `response` restituita nella callback contiene tutte le informazioni necessarie per gestire la risposta in dettaglio. Due dei campi principali sono `status` e `response`:

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

Quando la risposta contiene una grande quantità di dati binari, come un'immagine o un brano musicale, può essere utile scrivere i dati in un file invece di caricarli in memoria:

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

Un altro caso d'uso del caricamento di grandi quantità di dati dalla rete è lo streaming audio, in cui "blocchi" di dati audio vengono caricati da un URL e trasferiti a una risorsa audio. Trovi un esempio completo nel [manuale sullo streaming audio](/sound-streaming#sound-streaming).


### Intestazioni della richiesta {#request-headers}

Puoi impostare intestazioni aggiuntive quando invii una richiesta. Per esempio, puoi impostare un'intestazione `Authorization` oppure `Content-Type` per indicare al server il formato del corpo della richiesta.

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

Defold imposta automaticamente alcune intestazioni della richiesta:

* `If-None-Match: <etag>` viene impostata con l'ETag di un'eventuale risposta precedentemente memorizzata nella cache.
* `Transfer-Encoding: chunked` viene impostata se il corpo della richiesta supera i 16384 byte.
* `Content-Length` viene impostata con la dimensione del corpo della richiesta (a meno che la richiesta non sia suddivisa in blocchi).
* `Range: bytes=<from>-<to>` viene impostata se viene richiesta una risposta parziale, per esempio durante lo [streaming audio](/sound-streaming#sound-streaming).


### Intestazioni della risposta {#response-headers}

La risposta del server può contenere una o più intestazioni di risposta. Sono disponibili nella tabella `response`:

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### Proxy HTTP {#http-proxy}

A volte può essere utile inviare una richiesta tramite un server proxy. Per farlo, specifica il server proxy da usare per la connessione al server di destinazione. Quando si usa un proxy, la connessione al server di destinazione viene stabilita tramite un tunnel HTTP attraverso il proxy. Il tunnel HTTP viene stabilito usando il metodo HTTP CONNECT. Esempio:


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

### Riferimento API {#api-reference}

Consulta il [riferimento API](/ref/http/) per saperne di più.

### Estensioni {#extensions}

Puoi trovare un'implementazione alternativa delle richieste HTTP nell'[estensione TinyHTTP](https://defold.com/assets/tinyhttp/).
