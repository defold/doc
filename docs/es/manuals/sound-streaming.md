---
title: Streaming de sonido en Defold
brief: Este manual explica cómo hacer streaming de sonidos en el motor de videojuegos Defold
---

# Streaming de sonido

Aunque el comportamiento por defecto es cargar los datos de sonido completos, también puede ser beneficioso cargar los datos en fragmentos antes de usarlos. Esto suele llamarse "streaming".

Una ventaja del streaming de sonido es que requiere menos memoria en tiempo de ejecución. Otra es que, si haces streaming de contenido desde, por ejemplo, una URL HTTP, puedes actualizar el contenido en cualquier momento y también evitar la descarga inicial.

### Ejemplo

Hay un proyecto de ejemplo que muestra esta configuración: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## Cómo habilitar sonidos en streaming

### Forma sencilla

La forma más simple de usar streaming de sonido es habilitar la configuración [`sound.stream_enabled`](https://defold.com/manuals/project-settings/#stream-enabled) en *game.project*. Cuando esta opción está habilitada, el motor empezará a hacer streaming de los sonidos.

Nota: Si tienes muchos archivos de sonido cargados al mismo tiempo, es posible que necesites aumentar el valor de `sound.stream_cache_size` (consulta más abajo).

### Recursos de runtime

También puedes crear un nuevo recurso de datos de sonido y asignarlo a un componente de sonido.

Para hacerlo:
* Carga la parte inicial de los datos del archivo de sonido
    * Nota: Este es el archivo de sonido sin procesar, incluido el encabezado ogg/wav
* Crea un nuevo recurso de datos de sonido llamando a [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data).
* Asigna el nuevo recurso de datos de sonido al componente de sonido usando [`go.set()`](/ref/go#go.set)

Aquí hay un extracto del proyecto de ejemplo, que usa `http.request()` para obtener la parte inicial del archivo de sonido.

::: sidenote
El servidor web desde el que cargas contenido debe admitir [solicitudes HTTP de rango](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests).
:::

```lua
local function play_sound(self, hash)
    go.set(self.component, "sound", hash) -- sobrescribe los datos del recurso en el componente
    sound.play(self.component)            -- empieza a reproducir el sonido
end

local function parse_range(s)
    local _, _, rstart, rend, size = string.find(s, "(%d+)-(%d+)/(%d+)") -- "bytes 0-16383/103277"
    return rstart, rend, size
end

-- Callback para la respuesta HTTP.
local function http_result(self, _id, response, extra)
    if response.status == 200 or response.status == 206 then
        -- Solicitud correcta
        local relative_path = self.filename
        local range = response.headers['content-range'] -- content-range = "bytes 0-16383/103277"
        local rstart, rend, filesize = parse_range(range)
        -- Crea el recurso de Defold
        --   "partial" habilita el modo streaming
        print("Creating resource", relative_path)
        local hash = resource.create_sound_data(relative_path, { data = response.response, filesize = filesize, partial = true })
        -- envía "play_sound" al componente
        play_sound(self, hash)
    end
end

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end
```

## Proveedores de recursos

Puedes usar otros medios para cargar el fragmento inicial del archivo de sonido. Lo importante que debes recordar es que el resto de los fragmentos se cargan desde el sistema de recursos y sus proveedores de recursos. En este ejemplo, agregamos un nuevo proveedor de archivos (http) mediante un montaje de live update, llamando a [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount).

Puedes encontrar un ejemplo funcional en [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming).

```lua
-- Consulta http_result() en el ejemplo anterior

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    -- Solicita la parte inicial del archivo
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end

function init(self)
    self.base_url = "http://my.server.com"
    self.filename = "/path/to/sound.ogg"

    liveupdate.add_mount("webmount", self.base_url, 100, function (_self, _name, _uri, _result)
                    -- cuando el montaje esté listo, podemos iniciar la solicitud para descargar el primer fragmento
                    load_web_sound(self.base_url, self.filename)
                end)
end

function final(self)
    liveupdate.remove_mount("webmount")
end
```

## Caché de fragmentos de sonido

La cantidad de memoria consumida por los sonidos en runtime se controla con la configuración [`sound.stream_cache_size`](https://defold.com/manuals/project-settings/#stream-cache-size) en *game.project*. Dado este límite, los datos de sonido cargados nunca lo superarán.

El fragmento inicial de cada archivo de sonido no puede desalojarse y ocupará la caché mientras los recursos estén cargados. El tamaño del fragmento inicial se controla con la configuración [`sound.stream_preload_size`](https://defold.com/manuals/project-settings/#stream-preload-size) en *game.project*.

También puedes controlar el tamaño de cada fragmento de sonido cambiando la configuración [`sound.stream_chunk_size`](https://defold.com/manuals/project-settings/#stream-chunk-size) en *game.project*. Esto puede ayudarte a reducir aún más el tamaño de la caché de sonido si tienes muchos archivos de sonido cargados al mismo tiempo. Los archivos de sonido más pequeños que el tamaño del fragmento de sonido no se cargan en streaming y, si un nuevo fragmento no cabe en la caché, se desaloja el fragmento más antiguo.

::: important
El tamaño total de la caché de fragmentos de sonido debe ser mayor que el número de archivos de sonido cargados multiplicado por el tamaño del fragmento de streaming. De lo contrario, corres el riesgo de desalojar fragmentos nuevos en cada frame y los sonidos no se reproducirán correctamente.
:::
