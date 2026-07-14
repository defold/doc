---
title: Потоковая загрузка звука в Defold
brief: В этом руководстве объясняется, как организовать потоковую загрузку звука в игровой движок Defold
---

# Потоковая загрузка звука

Хотя по умолчанию звуковые данные загружаются целиком, в некоторых случаях может быть полезно загружать их частями перед использованием. Это обычно называют "потоковой загрузкой" (streaming).

Одно из преимуществ потоковой загрузки звука состоит в том, что во время выполнения требуется меньше памяти. Другое преимущество в том, что если вы загружаете контент, например, по HTTP URL, то можете обновлять его в любое время, а также избежать первоначальной полной загрузки.

### Пример

Есть пример проекта, демонстрирующий такую настройку: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## Как включить потоковую загрузку звука

### Простой способ

Самый простой способ использовать потоковую загрузку звука - включить параметр [`sound.stream_enabled`](https://defold.com/manuals/project-settings/#stream-enabled) в *game.project*. Когда эта опция включена, движок начнет загружать звуки потоково.

Примечание: если у вас одновременно загружено много звуковых файлов, возможно, потребуется увеличить значение `sound.stream_cache_size` (см. ниже).

### Ресурсы времени выполнения

Также можно создать новый ресурс звуковых данных и назначить его звуковому компоненту.

Для этого нужно:
* Загрузить начальную часть данных звукового файла
    * Примечание: это исходный звуковой файл, включая заголовок ogg/wav
* Создать новый ресурс звуковых данных, вызвав [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data).
* Назначить новый ресурс звуковых данных звуковому компоненту с помощью [`go.set()`](/ref/go#go.set)

Ниже приведен фрагмент из примерного проекта, использующий `http.request()` для получения начального звукового файла.

::: sidenote
Для настоящего потокового воспроизведения веб-сервер должен обрабатывать [диапазонные HTTP-запросы](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests) и возвращать статус `206`. Если сервер игнорирует заголовок `Range` и возвращает статус `200`, приведённый ниже пример вместо потокового ресурса создаёт обычный ресурс из полного ответа.
:::

```lua
local function play_sound(self, hash)
    go.set(self.component, "sound", hash) -- override the resource data on the component
    sound.play(self.component)            -- start playing the sound
end

local function parse_content_range(value)
    if not value then
        return nil
    end
    local rstart, rend, filesize = value:match("^bytes%s+(%d+)%-(%d+)/(%d+)$")
    return tonumber(rstart), tonumber(rend), tonumber(filesize)
end

-- Callback for the http response.
local function http_result(self, _id, response)
    if response.status ~= 200 and response.status ~= 206 then
        return
    end

    local options = {
        data = response.response,
    }

    if response.status == 206 then
        local rstart, _, filesize = parse_content_range(response.headers["content-range"])
        if rstart ~= 0 or not filesize then
            print("Invalid Content-Range response")
            return
        end

        -- A partial resource enables streaming. filesize is the size of the
        -- complete file, not only the returned range.
        if #response.response < filesize then
            options.filesize = filesize
            options.partial = true
        end
    end

    local relative_path = self.filename
    print("Creating resource", relative_path)
    local resource_hash = resource.create_sound_data(relative_path, options)
    play_sound(self, resource_hash)
end

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end
```

## Провайдеры ресурсов

Можно использовать и другие способы загрузки начального фрагмента звукового файла. Важно помнить, что остальные фрагменты загружаются через систему ресурсов и ее провайдеров ресурсов. В этом примере мы добавляем нового (HTTP) файлового провайдера, добавляя mount live update с помощью вызова [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount).

Рабочий пример можно найти здесь: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming).

```lua
-- See http_result() from above example

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    -- Request the initial part of the file
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end

function init(self)
    self.base_url = "http://my.server.com"
    self.filename = "/path/to/sound.ogg"

    liveupdate.add_mount("webmount", self.base_url, 100, function (_self, _name, _uri, _result)
                    -- once the mount is ready, we can start our request for downloading the first chunk
                    load_web_sound(self.base_url, self.filename)
                end)
end

function final(self)
    liveupdate.remove_mount("webmount")
end
```

## Кэш звуковых фрагментов

Объем памяти, потребляемой звуками во время выполнения, управляется параметром [`sound.stream_cache_size`](https://defold.com/manuals/project-settings/#stream-cache-size) в *game.project*. При заданном лимите объем загруженных звуковых данных никогда не превысит это значение.

Начальный фрагмент каждого звукового файла не может быть вытеснен из кэша и будет занимать место в кэше до тех пор, пока ресурс загружен. Размер начального фрагмента задается параметром [`sound.stream_preload_size`](https://defold.com/manuals/project-settings/#stream-preload-size) в *game.project*.

Также можно управлять размером каждого звукового фрагмента, изменяя параметр [`sound.stream_chunk_size`](https://defold.com/manuals/project-settings/#stream-chunk-size) в *game.project*. Это может помочь еще сильнее уменьшить размер кэша звука, если у вас одновременно загружено много звуковых файлов. Звуковые файлы, размер которых меньше размера звукового фрагмента, не загружаются потоково, а если новый фрагмент не помещается в кэш, вытесняется самый старый фрагмент.

::: important
Общий размер кэша звуковых фрагментов должен быть больше, чем количество загруженных звуковых файлов, умноженное на размер звукового фрагмента. Иначе вы рискуете вытеснять новые фрагменты каждый кадр, и звук не будет воспроизводиться корректно
:::
