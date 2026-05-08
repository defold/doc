---
title: Skryptowanie zawartości Live update
brief: Aby korzystać z zawartości Live update, trzeba pobrać dane i zamontować je w grze. Ta instrukcja wyjaśnia, jak używać funkcji Live update w skryptach.
---

# Skryptowanie Live update

Interfejs API składa się tylko z kilku funkcji:

* `liveupdate.add_mount()`
* `liveupdate.remove_mount()`
* `liveupdate.get_mounts()`.

## Pobieranie mountów

Jeśli używasz więcej niż jednego archiwum Live update, zalecamy przejść po każdym mouncie
przy starcie i sprawdzić, czy nadal powinien być używany.

Jest to ważne, ponieważ zawartość może już nie być poprawna dla silnika z powodu zmian formatu plików.

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- tabela z mountami

    -- Każdy mount ma: mount.uri, mount.priority, mount.name
	for _,mount in ipairs(mounts) do

        -- Wymaga to, aby nazwa pliku była unikalna, dzięki czemu nie pobierzemy pliku z innego archiwum.
        -- Te dane są tworzone przez twórcę gry jako sposób na określenie metadanych archiwum.
		local version_data = sys.load_resource("/version_" .. mount.name .. ".json")

		if version_data then
			version_data = json.decode(version_data)
		else
			version_data = {version = 0} -- jeśli nie ma pliku wersji, prawdopodobnie jest to stare lub nieprawidłowe archiwum
		end

        -- Sprawdź wersję archiwum względem wersji obsługiwanej przez grę.
        if version_data.version < sys.get_config_int("game.minimum_lu_version") then
            -- Było nieprawidłowe, więc je odmontujemy!
            liveupdate.remove_mount(mount.name)
        end
	end
end
```

## Skryptowanie z wykluczonymi pełnomocnikami kolekcji

Pełnomocnik kolekcji, który został wykluczony z bundlowania, działa jak zwykły pełnomocnik kolekcji, z jedną ważną różnicą. Wysłanie do niego wiadomości `load`, kiedy nadal ma zasoby niedostępne w magazynie bundla, spowoduje błąd.

Zanim więc wyślemy mu `load`, musimy sprawdzić, czy nie brakuje jakichś zasobów. Jeśli tak, trzeba pobrać archiwum zawierające te zasoby, a następnie je zamontować.

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
	liveupdate.add_mount(name, "zip:" .. path, priority, function(_uri, _path, _status) -- <1>
		callback(_uri, _path, _status)
	end)
end

function init(self)
    self.http_url = sys.get_config_string("game.http_url", nil) -- <2>

    local level_name = "level1"

    local info = get_lu_info_for_level(level_name) -- <3>

    msg.post("#", "load_level", {level = "level1", info = info }) -- <4>
end

function on_message(self, message_id, message, sender)
    if message_id == hash("load_level") then
        local missing_resources = collectionproxy.missing_resources("#" .. message.level) -- <5>

        if #missing_resources then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
		local zip_filename = message.info.name .. ".zip"
		local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Wykonaj żądanie. Możesz użyć poświadczeń.
        http.request(url, "GET", function(self, id, response) -- <7>
			if response.status == 200 or response.status == 304 then
				mount_zip(self, message.info.name, message.info.priority, download_path, function(uri, path, status) -- <8>
					msg.post("#", "load_level", message) -- spróbuj ponownie wczytać poziom
				end)

			else
				print("Failed to download archive ", download_path, "from", url, ":", response.status)
			end
		end, nil, nil, {path=download_path})

    elseif message_id == hash("proxy_loaded") then -- Poziom jest wczytany, więc możemy go włączyć.
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` montuje jedno archiwum, używając podanej nazwy, priorytetu i pliku zip. Dane stają się wtedy natychmiast dostępne do wczytania, bez potrzeby restartowania silnika. Informacja o mouncie jest zapisywana i zostanie automatycznie dodana ponownie przy następnym uruchomieniu silnika, więc nie trzeba wywoływać ponownie `liveupdate.add_mount()` dla tego samego mounta.
2. Trzeba przechowywać archiwum online, na przykład w S3, skąd będzie można je pobrać.
3. Mając nazwę pełnomocnika kolekcji, trzeba ustalić, które archiwum lub archiwa pobrać i jak je zamontować.
4. Przy starcie próbujemy wczytać poziom.
5. Sprawdź, czy pełnomocnik kolekcji ma dostępne wszystkie zasoby.
6. Jeśli brakuje zasobów, trzeba pobrać archiwum i je zamontować.
7. Wykonaj żądanie HTTP i pobierz archiwum do `download_path`.
8. Dane zostały pobrane i czas je zamontować w uruchomionym silniku.


Gdy kod wczytywania jest już gotowy, możemy przetestować aplikację. Jednak uruchamianie jej z poziomu edytora nie pobierze żadnych zasobów. Dzieje się tak dlatego, że Live update jest funkcją bundla. Gdy uruchamiasz w środowisku edytora, żadne zasoby nigdy nie są wykluczane. Aby upewnić się, że wszystko działa poprawnie, musimy utworzyć bundle.
