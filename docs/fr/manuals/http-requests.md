---
title: Requêtes HTTP
brief: Ce manuel explique comment effectuer des requêtes HTTP.
---

## Requêtes HTTP {#http-requests}

Defold peut effectuer des requêtes HTTP classiques à l'aide de la fonction `http.request()`.

### Requêtes HTTP GET {#http-get}

Il s'agit de la requête la plus simple pour récupérer des données du serveur. Exemple :

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

Cela envoie une requête HTTP GET à https://www.defold.com. La fonction est asynchrone et ne bloque pas l'exécution pendant la requête. Une fois la requête effectuée et la réponse du serveur reçue, elle appelle la fonction de rappel (callback) fournie. La fonction de rappel reçoit la réponse complète du serveur, y compris le code d'état et les en-têtes de réponse. Vous trouverez ci-dessous des informations supplémentaires sur la façon de traiter la table de réponse.

::: sidenote
Les requêtes HTTP sont automatiquement mises en cache dans le client pour améliorer les performances réseau. Les fichiers mis en cache sont stockés dans un répertoire de données d'application propre au système d'exploitation, dans un dossier nommé `defold/http-cache`. Vous n'avez généralement pas à vous préoccuper du cache HTTP, mais si vous devez le vider pendant le développement, vous pouvez supprimer manuellement le dossier contenant les fichiers mis en cache. Sur macOS, ce dossier se trouve dans `%HOME%/Library/Application Support/Defold/http-cache/` et, sur Windows, dans `%APP_DATA%/defold/http-cache`.
:::

### Requêtes HTTP POST {#http-post}

L'envoi de données à un serveur, comme un score ou des données d'authentification, se fait généralement à l'aide d'une requête POST :

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### Autres méthodes HTTP {#other-http-methods}

Les requêtes HTTP de Defold prennent également en charge les méthodes HEAD, DELETE et PUT. La méthode CONNECT est également prise en charge (voir la section sur les connexions via un proxy ci-dessous).

### Traitement de la réponse HTTP {#how-to-work-with-the-http-response}

La table `response` renvoyée dans la fonction de rappel contient toutes les informations nécessaires pour mettre en place un traitement détaillé des réponses. Deux des champs principaux sont `status` et `response` :

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

Lorsque la réponse contient un grand volume de données binaires, comme une image ou un morceau de musique, il peut être judicieux d'écrire les données dans un fichier au lieu de les charger en mémoire :

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

La diffusion audio en continu est un autre cas d'utilisation du chargement de grandes quantités de données via le réseau : des « fragments » de données audio sont chargés depuis une URL et transmis à une ressource sonore. Vous trouverez un exemple complet dans le [manuel sur la diffusion audio en continu](/sound-streaming#sound-streaming).


### En-têtes de requête {#request-headers}

Vous pouvez définir des en-têtes supplémentaires lors de l'envoi d'une requête. Cela permet par exemple de définir un en-tête `Authorization` ou `Content-Type` pour indiquer au serveur le format du corps de la requête.

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

Defold définit automatiquement plusieurs en-têtes de requête :

* `If-None-Match: <etag>` sera défini avec l'ETag d'une éventuelle réponse précédemment mise en cache.
* `Transfer-Encoding: chunked` sera défini si le corps de la requête dépasse 16384 octets.
* `Content-Length` sera défini avec la taille du corps de la requête (sauf si la requête est envoyée par fragments).
* `Range: bytes=<from>-<to>` sera défini si vous demandez une réponse partielle, par exemple lors de la [diffusion de sons en continu](/sound-streaming#sound-streaming).


### En-têtes de réponse {#response-headers}

La réponse du serveur peut contenir un ou plusieurs en-têtes de réponse. Ceux-ci sont disponibles dans la table `response` :

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### Proxy HTTP {#http-proxy}

Il est parfois souhaitable d'envoyer une requête via un serveur proxy. Pour ce faire, vous pouvez spécifier le serveur proxy à utiliser lors de la connexion au serveur de destination. Lorsqu'un proxy est utilisé, la connexion au serveur de destination est établie au moyen d'un tunnel HTTP à travers le proxy. Le tunnel HTTP est établi à l'aide de la méthode HTTP CONNECT. Exemple :


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

### Référence de l'API {#api-reference}

Consultez la [référence de l'API](/ref/http/) pour en savoir plus.

### Extensions {#extensions}

Une autre implémentation des requêtes HTTP est disponible dans l'[extension TinyHTTP](https://defold.com/assets/tinyhttp/).
