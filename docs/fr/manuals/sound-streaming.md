---
title: Lecture audio en flux continu dans Defold
brief: Ce manuel explique comment charger des sons en flux continu dans le moteur de jeu Defold
---

# Lecture audio en flux continu {#sound-streaming}

Bien que le comportement par défaut consiste à charger l'intégralité des données audio, il peut également être utile de charger les données par blocs avant leur utilisation. Ce procédé est souvent appelé « lecture en flux continu ».

La lecture audio en flux continu permet de réduire la mémoire nécessaire à l'exécution. Elle présente un autre avantage lorsque vous chargez du contenu en flux continu, par exemple depuis une URL HTTP : vous pouvez mettre à jour le contenu à tout moment et éviter le téléchargement initial.

### Exemple {#example}

Un projet exemple présente cette configuration : [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## Activer la lecture audio en flux continu {#how-to-enable-streaming-sounds}

### Méthode simple {#easy-way}

Le moyen le plus simple d'utiliser la lecture audio en flux continu consiste à activer le [paramètre `sound.stream_enabled`](https://defold.com/manuals/project-settings/#stream-enabled) dans *game.project*. Lorsque cette option est activée, le moteur commence à charger les sons en flux continu.

Remarque : si de nombreux fichiers audio sont chargés en même temps, vous devrez peut-être augmenter la valeur de `sound.stream_cache_size` (voir ci-dessous).

### Ressources à l'exécution {#runtime-resources}

Vous pouvez également créer une nouvelle ressource de données audio et l'affecter à un composant (component) sonore.

Pour cela :
* Chargez la partie initiale des données du fichier audio
    * Remarque : il s'agit du fichier audio brut, y compris son en-tête ogg/wav
* Créez une nouvelle ressource de données audio en appelant [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data).
* Affectez la nouvelle ressource de données audio au composant sonore avec [`go.set()`](/ref/go#go.set)

Voici un extrait du projet exemple qui utilise `http.request()` pour récupérer la partie initiale du fichier audio.

::: sidenote
Pour que le chargement en flux continu fonctionne, le serveur web doit prendre en charge les [requêtes HTTP par plage](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests) et renvoyer le code d'état `206`. Si le serveur ignore l'en-tête `Range` et renvoie le code d'état `200`, l'exemple ci-dessous crée à la place une ressource classique, sans chargement en flux continu, à partir de la réponse complète.
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

## Fournisseurs de ressources {#resource-providers}

Vous pouvez utiliser d'autres moyens pour charger le bloc initial du fichier audio. Retenez que les autres blocs sont chargés depuis le système de ressources et ses fournisseurs de ressources. Dans cet exemple, nous ajoutons un nouveau fournisseur de fichiers (HTTP) en ajoutant un point de montage de mise à jour en direct à l'aide de [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount).

Vous trouverez un exemple fonctionnel dans [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming).

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

## Cache de blocs audio {#sound-chunk-cache}

La quantité de mémoire consommée par les sons à l'exécution est définie par le [paramètre `sound.stream_cache_size`](https://defold.com/manuals/project-settings/#stream-cache-size) dans *game.project*. Les données audio chargées ne dépasseront jamais cette limite.

Le bloc initial de chaque fichier audio ne peut pas être évincé et occupe le cache tant que la ressource reste chargée. La taille du bloc initial est définie par le [paramètre `sound.stream_preload_size`](https://defold.com/manuals/project-settings/#stream-preload-size) dans *game.project*.

Vous pouvez également définir la taille de chaque bloc audio en modifiant le [paramètre `sound.stream_chunk_size`](https://defold.com/manuals/project-settings/#stream-chunk-size) dans *game.project*. Cela peut vous aider à réduire encore la taille du cache audio si de nombreux fichiers audio sont chargés en même temps. Les fichiers audio plus petits que la taille d'un bloc audio ne sont pas chargés en flux continu et, si un nouveau bloc ne tient pas dans le cache, le bloc le plus ancien est évincé.

::: important
La taille totale du cache de blocs audio devrait être supérieure au nombre de fichiers audio chargés multiplié par la taille d'un bloc audio. Sinon, vous risquez d'évincer de nouveaux blocs à chaque image et les sons ne seront pas lus correctement.
:::
