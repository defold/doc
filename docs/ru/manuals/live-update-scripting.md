---
title: Скриптование контента Live Update
brief: Чтобы использовать контент Live Update, нужно скачать и смонтировать данные в игру. В этом руководстве показано, как работать с Live Update из скриптов.
---

# Скриптование Live Update

API состоит всего из нескольких функций:

* `liveupdate.add_mount()`
* `liveupdate.remove_mount()`
* `liveupdate.get_mounts()`

## Получение mount'ов

Если вы используете более одного архива Live Update, рекомендуется при запуске
перебирать каждый mount и определять, нужно ли его по-прежнему использовать.

Это важно, поскольку контент может больше не подходить для текущей версии движка
из-за изменений формата файлов.

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- таблица с mount'ами

    -- У каждого mount'а есть: mount.uri, mount.priority, mount.name
	for _,mount in ipairs(mounts) do

        -- Имя файла должно быть уникальным, чтобы мы не получили файл из другого архива
        -- Эти данные разработчик создает как способ задать метаданные для архива
		local version_data = sys.load_resource("/version_" .. mount.name .. ".json")

		if version_data then
			version_data = json.decode(version_data)
		else
			version_data = {version = 0} -- если файла версии нет, скорее всего архив старый или недействительный
		end

        -- Проверяем версию архива относительно версии, поддерживаемой игрой
        if version_data.version < sys.get_config_int("game.minimum_lu_version") then
            -- Архив недействителен, поэтому размонтируем его
            liveupdate.remove_mount(mount.name)
        end
	end
end
```

## Скриптование с исключенными collection proxy

Collection proxy, исключенный из бандла, работает как обычный collection proxy, но с одним важным отличием. Если отправить ему сообщение `load`, пока часть его ресурсов недоступна в хранилище бандла, загрузка завершится ошибкой.

Поэтому перед отправкой `load` нужно проверить, есть ли отсутствующие ресурсы. Если они есть, нужно скачать архив, содержащий эти ассеты, а затем сохранить и смонтировать его.

Следующий пример кода предполагает, что ресурсы доступны по URL, указанному в настройке `game.http_url`.

```lua

-- Нужно отслеживать, какой архив содержит какой контент
-- В этом примере используется только один архив liveupdate, содержащий все отсутствующие ресурсы.
-- Если вы используете несколько архивов, нужно соответствующим образом организовать загрузки
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

        -- Выполняем запрос. При необходимости можно использовать учетные данные
        http.request(url, "GET", function(self, id, response) -- <7>
			if response.status == 200 or response.status == 304 then
				mount_zip(self, message.info.name, message.info.priority, download_path, function(uri, path, status) -- <8>
					msg.post("#", "load_level", message) -- пробуем загрузить уровень снова
				end)

			else
				print("Не удалось скачать архив ", download_path, "из", url, ":", response.status)
			end
		end, nil, nil, {path=download_path})

    elseif message_id == hash("proxy_loaded") then -- уровень загружен, и теперь его можно включить
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` монтирует один архив, используя заданные имя, приоритет и zip-файл. После этого данные сразу доступны для загрузки, перезапускать движок не нужно.
Сведения о mount'е сохраняются и будут автоматически добавлены снова при следующем запуске движка, поэтому повторно вызывать `liveupdate.add_mount()` для того же mount'а не требуется.
2. Архив нужно хранить онлайн, например на S3, откуда его можно будет скачать.
3. По имени collection proxy нужно определить, какой архив или архивы нужно скачать и как их смонтировать.
4. При запуске мы пытаемся загрузить уровень.
5. Проверяем, доступны ли все ресурсы collection proxy.
6. Если каких-то ресурсов не хватает, нужно скачать архив и смонтировать его.
7. Выполняем HTTP-запрос и скачиваем архив в `download_path`.
8. Данные скачаны, и теперь их можно смонтировать в работающий движок.


После того как код загрузки готов, можно протестировать приложение. Однако при запуске из редактора ничего скачиваться не будет. Это происходит потому, что Live Update работает только в собранном бандле. При запуске в среде редактора ресурсы никогда не исключаются. Чтобы убедиться, что все работает корректно, нужно создать бандл.
