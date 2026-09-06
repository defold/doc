---
title: Потокове завантаження звуку в Defold
brief: Цей посібник пояснює, як потоково завантажувати звуки в ігровий рушій Defold
---

# Потокове завантаження звуку {#sound-streaming}

За замовчуванням звукові дані завантажуються повністю, але іноді корисно завантажувати їх фрагментами перед використанням. Це часто називають «потоковим завантаженням» (streaming).

Одна з переваг потокового завантаження звуку — менше споживання пам’яті під час виконання. Інша перевага полягає в тому, що, завантажуючи вміст потоково, наприклад, з HTTP URL, ви можете оновлювати його будь-коли, а також уникнути початкового завантаження.

### Приклад {#example}

Існує проєкт-приклад, що демонструє таке налаштування: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## Як увімкнути потокове завантаження звуків {#how-to-enable-streaming-sounds}

### Простий спосіб {#easy-way}

Найпростіший спосіб використовувати потокове завантаження звуку — увімкнути [налаштування `sound.stream_enabled`](https://defold.com/manuals/project-settings/#stream-enabled) у *game.project*. Коли цю опцію ввімкнено, рушій почне завантажувати звуки потоково.

Примітка: якщо у вас одночасно завантажено багато звукових файлів, може знадобитися збільшити значення `sound.stream_cache_size` (див. нижче).

### Ресурси під час виконання {#runtime-resources}

Також можна створити новий ресурс звукових даних і призначити його звуковому компоненту (sound component).

Для цього:
* Завантажте початкову частину даних звукового файлу
    * Примітка: це необроблений звуковий файл разом із заголовком ogg/wav
* Створіть новий ресурс звукових даних, викликавши [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data).
* Призначте новий ресурс звукових даних звуковому компоненту за допомогою [`go.set()`](/ref/go#go.set)

Нижче наведено фрагмент із проєкту-прикладу, у якому `http.request()` використовується для початкового отримання звукового файлу.

::: sidenote
Для потокового завантаження вебсервер має обробляти [HTTP-запити діапазонів](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests) і повертати код статусу `206`. Якщо сервер ігнорує заголовок `Range` і повертає код статусу `200`, наведений нижче приклад натомість створює звичайний ресурс без потокового завантаження з повної відповіді.
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

## Постачальники ресурсів {#resource-providers}

Для завантаження початкового фрагмента звукового файлу можна використовувати й інші способи. Важливо пам’ятати, що решта фрагментів завантажується через систему ресурсів та її постачальників ресурсів. У цьому прикладі ми додаємо нового постачальника файлів (HTTP), додаючи точку монтування Live Update за допомогою виклику [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount).

Робочий приклад можна знайти тут: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming).

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

## Кеш звукових фрагментів {#sound-chunk-cache}

Обсяг пам’яті, який звуки споживають під час виконання, регулюється [налаштуванням `sound.stream_cache_size`](https://defold.com/manuals/project-settings/#stream-cache-size) у *game.project*. Обсяг завантажених звукових даних ніколи не перевищуватиме заданого обмеження.

Початковий фрагмент кожного звукового файлу не можна витіснити з кешу, і він займатиме місце в кеші, доки ресурс завантажений. Розмір початкового фрагмента регулюється [налаштуванням `sound.stream_preload_size`](https://defold.com/manuals/project-settings/#stream-preload-size) у *game.project*.

Ви також можете керувати розміром кожного звукового фрагмента, змінюючи [налаштування `sound.stream_chunk_size`](https://defold.com/manuals/project-settings/#stream-chunk-size) у *game.project*. Це може допомогти ще більше зменшити розмір звукового кешу, якщо у вас одночасно завантажено багато звукових файлів. Звукові файли, менші за розмір звукового фрагмента, не завантажуються потоково, а якщо новий фрагмент не вміщується в кеш, найстаріший фрагмент витісняється

::: important
Загальний розмір кешу звукових фрагментів має перевищувати добуток кількості завантажених звукових файлів і розміру фрагмента потоку. Інакше ви ризикуєте витісняти нові фрагменти кожного кадру, і звуки не відтворюватимуться належним чином
:::
