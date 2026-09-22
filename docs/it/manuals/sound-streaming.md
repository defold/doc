---
title: Streaming dei suoni in Defold
brief: Questo manuale spiega come caricare i suoni in streaming nel motore di gioco Defold
---

# Streaming dei suoni {#sound-streaming}

Per impostazione predefinita, i dati dei suoni vengono caricati per intero, ma può essere utile caricarli a blocchi prima di utilizzarli. Questa tecnica viene spesso chiamata "streaming".

Uno dei vantaggi dello streaming dei suoni è il minor consumo di memoria durante l'esecuzione. Inoltre, se carichi contenuti in streaming, per esempio da un URL HTTP, puoi aggiornarli in qualsiasi momento ed evitare il download iniziale.

### Esempio {#example}

Un progetto di esempio mostra questa configurazione: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## Come abilitare lo streaming dei suoni {#how-to-enable-streaming-sounds}

### Metodo semplice {#easy-way}

Il modo più semplice per utilizzare lo streaming dei suoni è abilitare l'[impostazione `sound.stream_enabled`](https://defold.com/manuals/project-settings/#stream-enabled) in *game.project*. Quando questa opzione è abilitata, il motore inizia a caricare i suoni in streaming.

Nota: se carichi molti file audio contemporaneamente, potresti dover aumentare il valore di `sound.stream_cache_size` (vedi sotto).

### Risorse a runtime {#runtime-resources}

Puoi anche creare una nuova risorsa di dati audio e assegnarla a un componente audio.

Per farlo:
* Carica la parte iniziale dei dati del file audio
    * Nota: si tratta del file audio grezzo, inclusa l'intestazione ogg/wav
* Crea una nuova risorsa di dati audio chiamando [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data).
* Assegna la nuova risorsa di dati audio al componente audio usando [`go.set()`](/ref/go#go.set)

Ecco un estratto del progetto di esempio che usa `http.request()` per ottenere la parte iniziale del file audio.

::: sidenote
Lo streaming vero e proprio richiede che il server web rispetti le [richieste HTTP per intervalli](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests) e restituisca il codice di stato `206`. Se il server ignora l'intestazione `Range` e restituisce il codice di stato `200`, l'esempio seguente crea invece una normale risorsa senza streaming a partire dalla risposta completa.
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

## Fornitori di risorse {#resource-providers}

Puoi utilizzare altri metodi per caricare il blocco iniziale del file audio. Ricorda che i blocchi rimanenti vengono caricati dal sistema di risorse e dai suoi fornitori di risorse (resource provider). In questo esempio aggiungiamo un nuovo fornitore di file (HTTP) creando un punto di montaggio Live Update tramite [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount).

Puoi trovare un esempio funzionante in [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming).

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

## Cache dei blocchi audio {#sound-chunk-cache}

La quantità di memoria occupata dai suoni durante l'esecuzione è controllata dall'[impostazione `sound.stream_cache_size`](https://defold.com/manuals/project-settings/#stream-cache-size) in *game.project*. I dati audio caricati non supereranno mai questo limite.

Il blocco iniziale di ciascun file audio non può essere rimosso dalla cache e la occupa finché la risorsa rimane caricata. La dimensione del blocco iniziale è controllata dall'[impostazione `sound.stream_preload_size`](https://defold.com/manuals/project-settings/#stream-preload-size) in *game.project*.

Puoi anche controllare la dimensione di ciascun blocco audio modificando l'[impostazione `sound.stream_chunk_size`](https://defold.com/manuals/project-settings/#stream-chunk-size) in *game.project*. Questo può aiutarti a ridurre ulteriormente le dimensioni della cache audio se carichi molti file audio contemporaneamente. I file audio più piccoli della dimensione di un blocco non vengono caricati in streaming e, se un nuovo blocco non trova spazio nella cache, il blocco più vecchio viene rimosso

::: important
La dimensione totale della cache dei blocchi audio dovrebbe essere maggiore del numero di file audio caricati moltiplicato per la dimensione del blocco di streaming. Altrimenti rischi di rimuovere dalla cache nuovi blocchi a ogni fotogramma e i suoni non verranno riprodotti correttamente
:::
