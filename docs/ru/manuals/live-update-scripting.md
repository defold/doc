---
title: Скриптование контента Live Update
brief: Чтобы использовать контент Live Update, нужно скачать и смонтировать данные в игру. В этом руководстве показано, как работать с Live Update из скриптов.
---

# Скриптование Live Update

Основной процесс монтирования использует `liveupdate.add_mount()`, `liveupdate.remove_mount()` и `liveupdate.get_mounts()`. Полный список доступных функций см. в [справочнике API `liveupdate`](/ref/liveupdate/).

Если коду необходимо определить, ожидает ли манифест сборки исключённый контент Live Update, используйте `liveupdate.is_built_with_excluded_files()`:

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

Функция сообщает только о метаданных манифеста сборки. Она не означает, что какой-либо архив сейчас смонтирован или что конкретный ресурс доступен. Для просмотра активных mount'ов используйте `liveupdate.get_mounts()`, а для просмотра записанных в манифесте хешей ресурсов Collection Proxy --- [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources).

Рекомендуемый процесс --- скачать и смонтировать целый Zip-архив с URI `zip:`.

## Получение mount'ов

`liveupdate.get_mounts()` возвращает mount'ы, активные в текущей сессии. Каждая запись содержит строку `uri`, числовой `priority` и хеш `name`. Список также содержит базовые mount'ы движка, приоритет которых меньше нуля и которые невозможно удалить.

Движок не восстанавливает mount'ы после перезапуска. Если приложению нужен ранее скачанный контент в следующей сессии, оно должно сохранить URI, имя и приоритет пакета в собственных данных сохранения и снова вызвать `liveupdate.add_mount()` при запуске.

Когда смонтировано несколько пакетов, полезно проверять их метаданные, определяемые приложением. Поскольку `mount.name` является хешем, используйте его как ключ таблицы или сравнивайте с `hash("mount-name")`; не добавляйте его к пути ресурса. Следующий пример сопоставляет каждому хешу имени уникальный путь к ресурсу метаданных:

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- таблица с mount'ами
	local version_resources = {
		[hash("level-pack")] = "/version_level_pack.json",
		[hash("season-pack")] = "/version_season_pack.json",
	}

	for _, mount in ipairs(mounts) do
		local version_resource = version_resources[mount.name]
		local version_data = version_resource and sys.load_resource(version_resource)

		if version_data then
			version_data = json.decode(version_data)
		elseif mount.priority >= 0 then
			version_data = {version = 0} -- если файла версии нет, скорее всего, это старый или недействительный архив
		end

		-- Игнорировать базовые mount'ы движка с отрицательными приоритетами.
		if version_data and version_data.version < sys.get_config_int("game.minimum_lu_version") then
			liveupdate.remove_mount(mount.name)
		end
	end
end
```

Используйте уникальные пути метаданных для разных пакетов. Поиск ресурсов следует приоритету mount, поэтому одинаковый путь в нескольких пакетах приведёт к чтению копии из mount с наибольшим приоритетом.

## Скриптование с исключенными collection proxy

Collection proxy, исключенный из бандла, работает как обычный collection proxy, но с одним важным отличием. Если отправить ему сообщение `load`, пока часть его ресурсов недоступна в хранилище бандла, загрузка завершится ошибкой.

В архивном сценарии вы обычно заранее определяете, какой архив или набор архивов нужен proxy, и монтируете их перед загрузкой. Чтобы просмотреть записанные в манифесте хеши ресурсов известного исключённого proxy, используйте `collectionproxy.get_resources()`.

После монтирования пакета исключённый и незагруженный прокси также можно перенаправить на другую скомпилированную коллекцию с помощью `collectionproxy.set_collection()`. Ограничения и порядок загрузки описаны в разделе [Изменение коллекции исключённого прокси](/manuals/collection-proxy/#changing-an-excluded-proxys-collection).

При сборке архива с публикацией контента Live Update основной манифест в бандле не содержит исключённых записей Live Update, а манифест опубликованного пакета сохраняет их. `collectionproxy.get_resources()` читает метаданные зависимостей из манифеста, но не проверяет доступность каждого указанного блока данных:

* до монтирования манифеста пакета с исключёнными записями proxy вызов `collectionproxy.get_resources("#proxy")` возвращает пустую таблицу `{}`;
* после монтирования соответствующего пакета функция возвращает непустую таблицу хешей ресурсов этого proxy, например:

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

Следующий пример кода предполагает, что ресурсы доступны по URL, указанному в настройке `game.http_url`.

```lua

-- Необходимо отслеживать, какой контент содержится в каждом архиве
-- В этом примере используется один архив liveupdate, содержащий все недостающие ресурсы.
-- Если архивов несколько, необходимо соответствующим образом организовать их скачивание
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

        -- При сборке с публикацией контента Live Update исключённые записи не входят
        -- в манифест бандла, поэтому эта таблица пуста, пока не смонтирован
        -- манифест соответствующего пакета. После монтирования она содержит хеши ресурсов прокси.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
        local zip_filename = message.info.name .. ".zip"
        local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Проверить, существует ли архив. Если да, попробовать его смонтировать!
        if sys.exists(download_path) then
            mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                if result == liveupdate.LIVEUPDATE_OK then
                    msg.post("#", "load_level", message) -- попробовать загрузить уровень снова
                else
                    os.remove(download_path)             -- удалить и попробовать
                    msg.post("#", "load_level", message) -- скачать снова
                end
            end)
        else
            -- Выполнить запрос. Можно использовать учётные данные
            http.request(url, "GET", function(self, id, response) -- <7>
                if response.status == 200 or response.status == 304 then
                    mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                        if result == liveupdate.LIVEUPDATE_OK then
                            msg.post("#", "load_level", message) -- попробовать загрузить уровень снова
                        else
                            print("Failed to mount archive", download_path, ":", result)
                        end
                    end)
                else
                    print("Failed to download archive", download_path, "from", url, ":", response.status)
                end
            end, nil, nil, {path=download_path})
        end

    elseif message_id == hash("proxy_loaded") then -- уровень загружен, и его можно включить
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` монтирует один архив, используя заданные имя, приоритет и zip-файл. После этого данные сразу доступны для загрузки, перезапускать движок не нужно. Mount активен только в текущей сессии. Сохраните путь к скачанному пакету и требуемые настройки mount в собственных данных сохранения и после каждого перезапуска снова вызывайте `liveupdate.add_mount()`.
2. Архив нужно хранить онлайн, например на S3, откуда его можно будет скачать.
3. По имени collection proxy нужно определить, какой архив или архивы нужно скачать и как их смонтировать.
4. При запуске мы пытаемся загрузить уровень.
5. В этом сценарии публикации архива с помощью `collectionproxy.get_resources()` проверяем метаданные исключённого контента proxy. Функция возвращает `{}` до монтирования манифеста нужного пакета, а после монтирования --- непустую таблицу хешей ресурсов. Эти хеши описывают зависимости; результат сам по себе не подтверждает доступность каждого блока данных.
6. Если proxy использует контент Live Update и соответствующий архив еще не смонтирован, мы скачиваем и монтируем его до загрузки proxy.
7. Выполняем HTTP-запрос и скачиваем архив в `download_path`.
8. Данные скачаны, и теперь их можно смонтировать в работающий движок.


После того как код загрузки готов, можно протестировать приложение. Однако при запуске из редактора ничего скачиваться не будет. Это происходит потому, что Live Update работает только в собранном бандле. При запуске в среде редактора ресурсы никогда не исключаются. Чтобы убедиться, что все работает корректно, нужно создать бандл.
