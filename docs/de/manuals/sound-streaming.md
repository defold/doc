---
title: Audiostreaming in Defold
brief: Dieses Handbuch erklärt, wie du Audiodaten in die Defold-Game-Engine streamst.
---

# Audiostreaming {#sound-streaming}

Standardmäßig werden Audiodaten vollständig geladen. Es kann jedoch sinnvoll sein, die Daten blockweise zu laden, bevor sie verwendet werden. Dies wird häufig als „Streaming“ bezeichnet.

Ein Vorteil des Audiostreamings ist der geringere Speicherbedarf zur Laufzeit. Wenn du Inhalte beispielsweise von einer HTTP-URL streamst, kannst du sie außerdem jederzeit aktualisieren und den anfänglichen Download vermeiden.

### Beispiel {#example}

Ein Beispielprojekt zeigt diese Einrichtung: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## Audiostreaming aktivieren {#how-to-enable-streaming-sounds}

### Einfacher Weg {#easy-way}

Am einfachsten verwendest du Audiostreaming, indem du die [Einstellung `sound.stream_enabled`](https://defold.com/manuals/project-settings/#stream-enabled) in *game.project* aktivierst. Wenn diese Option aktiviert ist, beginnt die Engine mit dem Streaming der Audiodaten.

Hinweis: Wenn viele Audiodateien gleichzeitig geladen sind, musst du möglicherweise den Wert von `sound.stream_cache_size` erhöhen (siehe unten).

### Ressourcen zur Laufzeit {#runtime-resources}

Du kannst auch eine neue Audiodatenressource (sound data resource) erstellen und sie einer Audiokomponente (sound component) zuweisen.

Gehe dazu so vor:
* Lade den ersten Teil der Audiodateidaten.
    * Hinweis: Gemeint ist die unverarbeitete Audiodatei einschließlich des ogg/wav-Headers.
* Erstelle eine neue Audiodatenressource, indem du [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data) aufrufst.
* Weise die neue Audiodatenressource mit [`go.set()`](/ref/go#go.set) der Audiokomponente zu.

Hier siehst du einen Auszug aus dem Beispielprojekt, der mit `http.request()` die anfänglichen Daten der Audiodatei abruft.

::: sidenote
Tatsächliches Streaming setzt voraus, dass der Webserver [HTTP-Bereichsanfragen](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests) berücksichtigt und den Status `206` zurückgibt. Wenn der Server den Header `Range` ignoriert und den Status `200` zurückgibt, erstellt das folgende Beispiel stattdessen eine normale Ressource ohne Streaming aus der vollständigen Antwort.
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

## Ressourcenanbieter {#resource-providers}

Du kannst den ersten Block der Audiodatei auch auf andere Weise laden. Beachte dabei, dass die restlichen Blöcke über das Ressourcensystem und seine Ressourcenanbieter (resource providers) geladen werden. In diesem Beispiel fügen wir einen neuen (HTTP-)Dateianbieter hinzu, indem wir mit [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount) einen Live-Update-Mount hinzufügen.

Ein funktionsfähiges Beispiel findest du unter [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming).

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

## Cache für Audiodatenblöcke {#sound-chunk-cache}

Die [Einstellung `sound.stream_cache_size`](https://defold.com/manuals/project-settings/#stream-cache-size) in *game.project* steuert den Speicherverbrauch der Audiodaten zur Laufzeit. Die geladenen Audiodaten überschreiten diese Grenze daher niemals.

Der erste Block jeder Audiodatei kann nicht aus dem Cache verdrängt werden und belegt dort Speicher, solange die Ressourcen geladen sind. Die Größe des ersten Blocks wird durch die [Einstellung `sound.stream_preload_size`](https://defold.com/manuals/project-settings/#stream-preload-size) in *game.project* gesteuert.

Du kannst außerdem die Größe jedes Audiodatenblocks steuern, indem du die [Einstellung `sound.stream_chunk_size`](https://defold.com/manuals/project-settings/#stream-chunk-size) in *game.project* änderst. Dadurch kannst du die Größe des Audio-Caches möglicherweise noch weiter verringern, wenn viele Audiodateien gleichzeitig geladen sind. Audiodateien, die kleiner als die Größe eines Audiodatenblocks sind, werden nicht gestreamt. Wenn ein neuer Block nicht in den Cache passt, wird der älteste Block verdrängt.

::: important
Die Gesamtgröße des Caches für Audiodatenblöcke sollte größer sein als die Anzahl der geladenen Audiodateien multipliziert mit der Größe eines Streaming-Blocks. Andernfalls besteht die Gefahr, dass in jedem Frame neue Blöcke verdrängt werden und die Audiodaten nicht korrekt wiedergegeben werden.
:::
