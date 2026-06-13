---
title: Solicitudes HTTP
brief: Este manual explica cómo hacer solicitudes HTTP.
---

## Solicitudes HTTP

Defold puede hacer solicitudes HTTP normales usando la función `http.request()`.

### HTTP GET

Esta es la solicitud más básica para obtener datos del servidor. Ejemplo:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

Esto hará una solicitud HTTP GET a https://www.defold.com. La función es asíncrona y no bloqueará la ejecución mientras hace la solicitud. Una vez que se haya hecho la solicitud y un servidor haya enviado una respuesta, invocará/llamará a la función callback proporcionada. La función callback recibirá la respuesta completa del servidor, incluido el código de estado y los headers de la respuesta. Consulta más abajo para obtener información adicional sobre cómo trabajar con la tabla de respuesta.

::: sidenote
Las solicitudes HTTP se almacenan automáticamente en caché en el cliente para mejorar el rendimiento de red. Los archivos en caché se almacenan en una ruta de soporte de la aplicación específica del sistema operativo, en una carpeta llamada `defold/http-cache`. Normalmente no tienes que preocuparte por la caché HTTP, pero si necesitas borrar la caché durante el desarrollo puedes eliminar manualmente la carpeta que contiene los archivos en caché. En macOS esta carpeta se encuentra en `%HOME%/Library/Application Support/Defold/http-cache/` y en Windows en `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST

Cuando se envían datos a un servidor, como una puntuación o algunos datos de autenticación, normalmente se hace usando una solicitud POST:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### Otros métodos HTTP

Las solicitudes HTTP de Defold también admiten los métodos HEAD, DELETE y PUT. El método CONNECT también está admitido (consulta la sección sobre conexiones proxy más abajo).

### Cómo trabajar con la respuesta HTTP

La tabla `response` devuelta en el callback contiene toda la información necesaria para implementar un manejo granular de la respuesta. Dos de los campos clave son `status` y `response`:

```lua

local function handle_response(self, id, response)
	-- comprueba el código de estado de la respuesta. Códigos de respuesta comunes:
	-- 200 OK - la solicitud se completó correctamente
	-- 301 Moved permanently - los datos solicitados se movieron, consulta el header de redirección
	-- 307 Temporary redirect - igual que arriba
	-- 208 Permanent redirect - igual que arriba
	-- 400 Bad Request - la solicitud estaba mal formada
	-- 401 Unauthorized - el cliente debe autenticarse
	-- 404 Not Found - el servidor no puede encontrar la información
	-- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
	if response.status == 200 then
		-- los datos de la respuesta
		-- esto puede ser cualquier cosa, desde texto plano, datos codificados en json o datos binarios
		print(response.response)
		json.decode(response.response)
		sys.save(..., response.response)
	end
end
```

Cuando la respuesta contiene un blob grande de datos binarios, como una imagen o una pista de música, puede tener sentido escribir los datos en un archivo en vez de cargarlos en memoria:

```lua
-- en este ejemplo descargamos myimage.png y lo escribimos directamente en un archivo en disco

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

Otro caso de uso para cargar grandes cantidades de datos por la red es el streaming de sonido, cuando se cargan "chunks" de datos de sonido desde una URL y se entregan a un recurso de sonido. Puedes encontrar un ejemplo completo en el [manual de streaming de sonido](/sound-streaming#sound-streaming).


### Headers de solicitud

Es posible definir headers adicionales al enviar una solicitud. Por ejemplo, esto se puede usar para definir un header de autorización o el tipo de contenido para indicar al servidor qué formato tiene el cuerpo de la solicitud.

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

-- enviar algunos datos de formulario
local headers = {
	["Content-Type"] = "application/x-www-form-urlencoded"
}
local body = "key1=value1&key2=value2"
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- enviar algunos datos codificados en JSON
local headers = {
	["Content-Type"] = "application/json"
}
local body = json.encode({ key1 = value1, key2 = value2 })
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- solicitar algunos datos que requieren autorización para acceder
local token = ... -- generar un token de acceso (JWT, OAuth etc)
local headers = {
	["Authorization"] = "Bearer " .. token
}
http.request("https://www.myserver.com/content", "GET", handle_response, headers)
```

Defold definirá automáticamente algunos headers de solicitud:

* `If-None-Match: <etag>` se definirá con el ETag de cualquier respuesta almacenada previamente en caché.
* `Transfer-Encoding: chunked` se definirá si el cuerpo de la solicitud es mayor que 16384 bytes.
* `Content-Length` se definirá con el tamaño del cuerpo de la solicitud (a menos que la solicitud esté dividida en chunks).
* `Range: bytes=<from>-<to>` se definirá si se solicita una respuesta parcial, por ejemplo al hacer [streaming de sonidos](/sound-streaming#sound-streaming).


### Headers de respuesta

La respuesta del servidor puede contener uno o más headers de respuesta. Están disponibles en la tabla `response`:

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### Proxy HTTP

A veces es deseable enviar una solicitud a través de un servidor proxy. Esto se puede hacer especificando un servidor proxy que se usará al conectar con el servidor de destino. Cuando se usa un proxy, la conexión con el servidor de destino se establece usando un túnel HTTP a través del proxy. El túnel HTTP se establece usando el método HTTP CONNECT. Ejemplo:


```lua
-- conectar a www.defold.com mediante un proxy localhost en el puerto 8888
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

### Referencia de la API

Consulta la [referencia de la API](/ref/http/) para obtener más información.

### Extensiones

Puedes encontrar una implementación alternativa de solicitudes HTTP en la [extensión TinyHTTP](https://defold.com/assets/tinyhttp/).
