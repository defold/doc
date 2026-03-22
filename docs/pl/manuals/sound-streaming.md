---
title: Strumieniowanie dźwięku w silniku Defold
brief: Ta instrukcja wyjaśnia, jak strumieniować dźwięki w silniku Defold
---

# Strumieniowanie dźwięku

Domyślnie dane dźwiękowe są wczytywane w całości, ale czasem korzystniejsze może być ładowanie ich partiami, jeszcze przed użyciem. Nazywa się to często strumieniowaniem.

Jedną z korzyści strumieniowania dźwięku jest mniejsze zużycie pamięci w czasie działania. Inną jest to, że jeśli strumieniujesz treści np. z adresu URL HTTP, możesz je aktualizować w dowolnym momencie i uniknąć początkowego pobierania.

### Przykład

Istnieje przykładowy projekt demonstrujący to rozwiązanie: [przykładowy projekt](https://github.com/defold/example-sound-streaming)

## Jak włączyć strumieniowanie dźwięków

### Najprostszy sposób

Najprostszym sposobem korzystania ze strumieniowania dźwięku jest włączenie ustawienia [`sound.stream_enabled`](https://defold.com/manuals/project-settings/#stream-enabled) w pliku *game.project*. Gdy ta opcja jest włączona, silnik zacznie strumieniować dźwięki.

Uwaga: jeśli jednocześnie załadowanych jest wiele plików dźwiękowych, może być konieczne zwiększenie wartości `sound.stream_cache_size` (zobacz niżej).

### Zasoby w czasie działania

Możesz też utworzyć nowy zasób danych dźwięku i przypisać go do komponentu dźwięku.

Można to zrobić tak:
* Wczytaj początkową część danych pliku dźwiękowego
    * Uwaga: jest to surowy plik dźwiękowy, łącznie z nagłówkiem ogg/wav
* Utwórz nowy zasób danych dźwięku, wywołując [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data).
* Ustaw nowy zasób danych dźwięku na komponencie dźwięku, używając [`go.set()`](/ref/go#go.set)

Poniżej znajduje się fragment przykładowego projektu, który używa `http.request()` do pobrania początkowego fragmentu pliku dźwiękowego.

::: sidenote
Serwer WWW, z którego pobierasz treści, musi obsługiwać [żądania zakresowe HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests).
:::

```lua
local function play_sound(self, hash)
    go.set(self.component, "sound", hash) -- zastąp dane zasobu na komponencie
    sound.play(self.component)            -- rozpocznij odtwarzanie dźwięku
end

local function parse_range(s)
    local _, _, rstart, rend, size = string.find(s, "(%d+)-(%d+)/(%d+)") -- "bytes 0-16383/103277"
    return rstart, rend, size
end

-- Funkcja zwrotna dla odpowiedzi HTTP.
local function http_result(self, _id, response, extra)
    if response.status == 200 or response.status == 206 then
        -- Pomyślne żądanie
        local relative_path = self.filename
        local range = response.headers['content-range'] -- content-range = "bytes 0-16383/103277"
        local rstart, rend, filesize = parse_range(range)
        -- Utwórz zasób
        --   "partial" włączy tryb strumieniowania
        print("Creating resource", relative_path)
        local hash = resource.create_sound_data(relative_path, { data = response.response, filesize = filesize, partial = true })
        -- wyślij do komponentu wiadomość "play_sound"
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

## Dostawcy zasobów

Początkowy fragment pliku dźwiękowego możesz wczytać także innymi sposobami. Ważne jest to, że pozostałe fragmenty są ładowane przez system zasobów i jego dostawców zasobów. W tym przykładzie dodajemy nowego dostawcę plików (http), tworząc punkt montowania live update za pomocą [`liveupdate.add_mount()`](/ref/liveupdate/#liveupdate.add_mount).

Działający przykład znajdziesz w [przykładowym projekcie](https://github.com/defold/example-sound-streaming).

```lua
-- Zobacz http_result() z powyższego przykładu

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    -- Zażądaj początkowej części pliku
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end

function init(self)
    self.base_url = "http://my.server.com"
    self.filename = "/path/to/sound.ogg"

    liveupdate.add_mount("webmount", self.base_url, 100, function ()
                    -- gdy punkt montowania będzie gotowy, możemy rozpocząć pobieranie pierwszego fragmentu
                    load_web_sound(self.base_url, self.filename)
                end)
end

function final(self)
    liveupdate.remove_mount("webmount")
end
```

## Cache fragmentów dźwięku

Ilość pamięci zużywanej przez dźwięki w czasie działania jest kontrolowana przez ustawienie [`sound.stream_cache_size`](https://defold.com/manuals/project-settings/#stream-cache-size) w pliku *game.project*. Przy tym limicie wczytane dane dźwiękowe nigdy go nie przekroczą.

Początkowego fragmentu każdego pliku dźwiękowego nie można usunąć z cache i będzie on zajmował miejsce tak długo, jak zasoby pozostają załadowane. Rozmiar początkowego fragmentu jest kontrolowany przez ustawienie [`sound.stream_preload_size`](https://defold.com/manuals/project-settings/#stream-preload-size) w pliku *game.project*.

Rozmiar każdego fragmentu dźwięku możesz też kontrolować, zmieniając ustawienie [`sound.stream_chunk_size`](https://defold.com/manuals/project-settings/#stream-chunk-size) w pliku *game.project*. Może to pomóc jeszcze bardziej zmniejszyć rozmiar cache dźwięku, jeśli jednocześnie masz załadowanych wiele plików dźwiękowych. Pliki dźwiękowe mniejsze niż rozmiar fragmentu dźwięku nie są strumieniowane, a jeśli nowy fragment nie mieści się w cache, usuwany jest najstarszy fragment.

::: important
Całkowity rozmiar cache fragmentów dźwięku powinien być większy niż liczba załadowanych plików dźwiękowych pomnożona przez rozmiar fragmentu strumieniowania. W przeciwnym razie ryzykujesz usuwanie nowych fragmentów w każdej klatce i dźwięki nie będą odtwarzane poprawnie.
:::
