---
title: Skryptowanie zawartości Live update
brief: Aby korzystać z zawartości Live update, trzeba pobrać dane i zamontować je w grze. Ta instrukcja wyjaśnia, jak używać funkcji Live update w skryptach.
---

# Skryptowanie Live update

Podstawowy przepływ montowania używa funkcji `liveupdate.add_mount()`, `liveupdate.remove_mount()` i `liveupdate.get_mounts()`. Pełną listę dostępnych funkcji znajdziesz w [dokumentacji API `liveupdate`](/ref/liveupdate/).

Użyj `liveupdate.is_built_with_excluded_files()`, gdy kod musi rozróżnić bundle, którego manifest budowania oczekuje wykluczonej zawartości Live Update:

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

Funkcja informuje wyłącznie o metadanych manifestu budowania. Nie oznacza to, że archiwum jest obecnie zamontowane ani że konkretny zasób jest dostępny. Aktywne mounty sprawdzaj za pomocą `liveupdate.get_mounts()`, a hashe zasobów zapisane w manifeście pełnomocnika kolekcji za pomocą [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources).

Zalecany sposób polega na pobraniu i zamontowaniu pełnego archiwum Zip za pomocą URI `zip:`.

## Pobieranie mountów

`liveupdate.get_mounts()` zwraca mounty aktywne w bieżącej sesji. Każdy wpis zawiera URI `mount.uri`, liczbowy priorytet `mount.priority` oraz hash `mount.name`. Mounty nie są przywracane po restarcie; aplikacja musi zapisać potrzebne ustawienia i ponownie wywołać `liveupdate.add_mount()`.

Ponieważ `mount.name` jest hashem, użyj go jako klucza tabeli lub porównaj z `hash("name")`; nie łącz go ze ścieżką. Przypisz każdy hash nazwy do unikalnej ścieżki metadanych:

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- tabela z mountami
	local version_resources = {
		[hash("liveupdate")] = "/version_liveupdate.json",
	}

    -- Każdy mount ma: mount.uri, mount.priority, mount.name
	for _,mount in ipairs(mounts) do

        -- Wymaga to, aby nazwa pliku była unikalna, dzięki czemu nie pobierzemy pliku z innego archiwum.
        -- Te dane są tworzone przez twórcę gry jako sposób na określenie metadanych archiwum.
		local version_resource = version_resources[mount.name]
		local version_data = version_resource and sys.load_resource(version_resource)

		if version_data then
			version_data = json.decode(version_data)
		elseif mount.priority >= 0 then
			version_data = {version = 0} -- jeśli nie ma pliku wersji, prawdopodobnie jest to stare lub nieprawidłowe archiwum
		end

        -- Sprawdź wersję archiwum względem wersji obsługiwanej przez grę.
        if version_data and version_data.version < sys.get_config_int("game.minimum_lu_version") then
            -- Było nieprawidłowe, więc je odmontujemy!
            liveupdate.remove_mount(mount.name)
        end
	end
end
```

## Skryptowanie z wykluczonymi pełnomocnikami kolekcji

Pełnomocnik kolekcji, który został wykluczony z bundlowania, działa jak zwykły pełnomocnik kolekcji, z jedną ważną różnicą. Wysłanie do niego wiadomości `load`, kiedy nadal ma zasoby niedostępne w magazynie bundla, spowoduje błąd.

W przepływie opartym na archiwach zwykle z góry decydujesz, którego archiwum lub archiwów potrzebuje proxy, i montujesz je przed wczytaniem. Aby sprawdzić zapisane w manifeście hashe zasobów znanego wykluczonego proxy, użyj `collectionproxy.get_resources()`.

Po zamontowaniu pakietu wykluczony i niewczytany pełnomocnik można również przekierować do innej skompilowanej kolekcji za pomocą `collectionproxy.set_collection()`. Ograniczenia i kolejność wczytywania opisano w sekcji [Zmienianie kolekcji wykluczonego pełnomocnika](/manuals/collection-proxy/#changing-an-excluded-proxys-collection).

W bundlu zbudowanym z opublikowaną zawartością Live Update główny manifest pomija wykluczone wpisy Live Update, natomiast manifest opublikowanego pakietu je zachowuje. `collectionproxy.get_resources()` odczytuje metadane zależności z manifestu; nie sprawdza, czy dostępny jest każdy wskazany blob danych:

* Przed zamontowaniem manifestu pakietu zawierającego wykluczone wpisy proxy funkcja `collectionproxy.get_resources("#proxy")` zwraca pustą tabelę `{}`.
* Po zamontowaniu odpowiedniego pakietu zwraca niepustą tabelę hashy zasobów dla danego proxy, na przykład:

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

Poniższy przykład zakłada, że zasoby są dostępne pod adresem URL podanym w ustawieniu `game.http_url`.

```lua

-- Musisz śledzić, które archiwum zawiera jaką zawartość
-- W tym przykładzie używamy tylko jednego archiwum liveupdate, które zawiera wszystkie brakujące zasoby.
-- Jeśli używasz wielu archiwów, musisz odpowiednio zorganizować pobieranie
local lu_infos = {
    liveupdate = {
        name = "liveupdate",
        priority = 10,
    }
}

local function get_lu_info_for_level(level_name)
    if level_name == "level1" then
        return lu_infos['liveupdate']
    end
end

local function mount_zip(self, name, priority, path, callback)
    liveupdate.add_mount(name, "zip:" .. path, priority, function(_self, _name, _uri, _result) -- <1>
        callback(_name, _uri, _result)
    end)
end

local function has_mount(name)
    local name_hash = hash(name)
    for _, mount in ipairs(liveupdate.get_mounts()) do
        if mount.name == name_hash then
            return true
        end
    end
    return false
end

function init(self)
    self.http_url = sys.get_config_string("game.http_url", nil) -- <2>

    local level_name = "level1"

    local info = get_lu_info_for_level(level_name) -- <3>

    msg.post("#", "load_level", {level = "level1", info = info }) -- <4>
end

function on_message(self, message_id, message, sender)
    if message_id == hash("load_level") then
        local proxy_resources = collectionproxy.get_resources("#" .. message.level) -- <5>

        -- Build publikujący zawartość Live Update pomija wykluczone wpisy w manifeście
        -- bundla, więc ta tabela jest pusta, dopóki nie zostanie zamontowany manifest
        -- odpowiedniego pakietu. Po zamontowaniu zawiera hashe zasobów proxy.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
        local zip_filename = message.info.name .. ".zip"
        local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Sprawdź, czy archiwum już istnieje. Jeśli tak, spróbuj je zamontować!
        if sys.exists(download_path) then
            mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                if result == liveupdate.LIVEUPDATE_OK then
                    msg.post("#", "load_level", message) -- spróbuj ponownie wczytać poziom
                else
                    os.remove(download_path)             -- usuń je i spróbuj
                    msg.post("#", "load_level", message) -- ponownie je pobrać
                end
            end)
        else
            -- Wykonaj żądanie. Możesz użyć poświadczeń.
            http.request(url, "GET", function(self, id, response) -- <7>
                if response.status == 200 or response.status == 304 then
                    mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                        if result == liveupdate.LIVEUPDATE_OK then
                            msg.post("#", "load_level", message) -- spróbuj ponownie wczytać poziom
                        else
                            print("Failed to mount archive", download_path, ":", result)
                        end
                    end)
                else
                    print("Failed to download archive", download_path, "from", url, ":", response.status)
                end
            end, nil, nil, {path=download_path})
        end

    elseif message_id == hash("proxy_loaded") then -- Poziom jest wczytany, więc możemy go włączyć.
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` montuje jedno archiwum, używając podanej nazwy, priorytetu i pliku zip. Dane stają się wtedy natychmiast dostępne do wczytania, bez potrzeby restartowania silnika. Mount jest aktywny tylko w bieżącej sesji. Zapisz ścieżkę pobranego pakietu i wymagane ustawienia mounta we własnych trwałych danych, a po każdym restarcie ponownie wywołaj `liveupdate.add_mount()`.
2. Trzeba przechowywać archiwum online, na przykład w S3, skąd będzie można je pobrać.
3. Mając nazwę pełnomocnika kolekcji, trzeba ustalić, które archiwum lub archiwa pobrać i jak je zamontować.
4. Przy starcie próbujemy wczytać poziom.
5. W tym przepływie publikowania archiwum użyj `collectionproxy.get_resources()`, aby sprawdzić metadane wykluczonej zawartości proxy. Funkcja zwraca `{}`, dopóki manifest odpowiedniego pakietu nie zostanie zamontowany, a po zamontowaniu zwraca niepustą tabelę hashy zasobów. Hashe opisują zależności; sam wynik nie potwierdza dostępności każdego bloba danych.
6. Jeśli proxy używa zawartości Live Update, a pasujące archiwum nie jest jeszcze zamontowane, pobieramy je i montujemy przed wczytaniem proxy.
7. Wykonaj żądanie HTTP i pobierz archiwum do `download_path`.
8. Dane zostały pobrane i czas je zamontować w uruchomionym silniku.


Gdy kod wczytywania jest już gotowy, możemy przetestować aplikację. Jednak uruchamianie jej z poziomu edytora nie pobierze żadnych zasobów. Dzieje się tak dlatego, że Live update jest funkcją bundla. Gdy uruchamiasz w środowisku edytora, żadne zasoby nigdy nie są wykluczane. Aby upewnić się, że wszystko działa poprawnie, musimy utworzyć bundle.
