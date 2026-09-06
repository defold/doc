---
title: Робота з вмістом Live Update у скриптах
brief: Щоб використовувати вміст Live Update, потрібно завантажити дані й змонтувати їх у грі. Цей посібник пояснює, як працювати з Live Update у скриптах.
---

# Робота з Live Update у скриптах {#scripting-live-update}

Основний порядок монтування передбачає використання `liveupdate.add_mount()`, `liveupdate.remove_mount()` і `liveupdate.get_mounts()`. Опис усіх доступних функцій дивіться в повному [довіднику API `liveupdate`](/ref/liveupdate/).

Використовуйте `liveupdate.is_built_with_excluded_files()`, коли в коді потрібно визначити, чи маніфест збірки пакета передбачає наявність виключеного вмісту Live Update:

```lua
if liveupdate.is_built_with_excluded_files() then
    print("The bundle expects excluded Live Update content")
end
```

Результат відображає лише метадані маніфесту збірки. Це не означає, що архів наразі змонтовано або що певний ресурс доступний. Використовуйте `liveupdate.get_mounts()`, щоб перевірити активні монтування, і [`collectionproxy.get_resources()`](/ref/collectionproxy/#collectionproxy.get_resources), щоб перевірити записані в маніфесті хеші ресурсів для проксі колекції (collection proxy).

Рекомендований порядок роботи — завантажити й змонтувати повний архів Zip за допомогою URI `zip:`.

## Отримання монтувань {#get-mounts}

`liveupdate.get_mounts()` повертає монтування, активні в поточному сеансі. Кожен запис має рядок `uri`, числовий `priority` і хеш `name`. Список також містить базові монтування рушія, пріоритети яких менші за нуль і які не можна видалити.

Рушій не відновлює монтування після перезапуску. Якщо застосунку потрібен раніше завантажений вміст у наступному сеансі, він має зберегти URI, ім’я та пріоритет пакета у власних даних збереження й знову викликати `liveupdate.add_mount()` під час запуску.

Коли змонтовано кілька пакетів, корисно перевіряти їхні метадані, визначені застосунком. Оскільки `mount.name` — це хеш, використовуйте його як ключ таблиці або порівнюйте з `hash("mount-name")`; не додавайте його до шляху ресурсу за допомогою конкатенації. У наведеному нижче прикладі кожен хеш імені зіставлено з унікальним шляхом до ресурсу метаданих:

```lua
local function remove_old_mounts()
	local mounts = liveupdate.get_mounts() -- table with mounts
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
			version_data = {version = 0} -- if it has no version file, it's likely an old/invalid archive
		end

		-- Ignore the engine's base mounts, which have negative priorities.
		if version_data and version_data.version < sys.get_config_int("game.minimum_lu_version") then
			liveupdate.remove_mount(mount.name)
		end
	end
end
```

Використовуйте унікальні шляхи до метаданих для різних пакетів. Пошук ресурсів відбувається відповідно до пріоритету монтування, тому, якщо кілька пакетів використовують той самий шлях, буде прочитано копію з монтування, що має найвищий пріоритет.

## Робота з виключеними проксі колекцій у скриптах {#scripting-with-excluded-collection-proxies}

Проксі колекції, виключений із пакування, працює як звичайний проксі колекції, але має одну важливу відмінність. Якщо надіслати йому повідомлення `load`, коли він усе ще має ресурси, недоступні у сховищі пакета, завантаження завершиться помилкою.

Під час роботи з архівами ви зазвичай заздалегідь визначаєте, який архів або архіви потрібні проксі, і монтуєте їх перед завантаженням. Щоб перевірити записані в маніфесті хеші ресурсів для відомого виключеного проксі, використовуйте `collectionproxy.get_resources()`.

Після монтування пакета виключений і ще не завантажений проксі також можна перенаправити на іншу скомпільовану колекцію за допомогою `collectionproxy.set_collection()`. Обмеження й послідовність завантаження описано в розділі [Змінення колекції виключеного проксі](/manuals/collection-proxy/#changing-an-excluded-proxys-collection).

Для збірки архіву, що публікує вміст Live Update, основний маніфест у пакеті не містить записів виключеного вмісту Live Update, тоді як маніфест опублікованого пакета зберігає їх. `collectionproxy.get_resources()` читає метадані залежностей із маніфесту; функція не перевіряє доступність кожного блоку даних, на який є посилання:

* Поки не змонтовано маніфест пакета, що містить виключені записи проксі, `collectionproxy.get_resources("#proxy")` повертає порожню таблицю `{}`.
* Після монтування відповідного пакета функція повертає непорожню таблицю хешів ресурсів для цього проксі, наприклад:

```lua
{
    "a1b2c3...",
    "d4e5f6...",
    "7890ab...",
    ...
}
```

 Наведений нижче приклад коду передбачає, що ресурси доступні за URL, указаним у налаштуванні `game.http_url`.

```lua

-- You'll need to track which archive contains which content
-- In this example, we only use a single liveupdate archive, containing all missing resource.
-- If you are using multiple archive, you need to structure the downloads accordingly
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

        -- A build that publishes Live Update content omits excluded entries from the
        -- bundled manifest, so this table is empty until the relevant package manifest
        -- is mounted. After mounting, it contains the resource hashes for the proxy.
        if message.info and #proxy_resources == 0 and not has_mount(message.info.name) then
            msg.post("#", "download_archive", message) -- <6>
        else
            msg.post("#" .. message.level, "load")
        end

    elseif message_id == hash("download_archive") then
        local zip_filename = message.info.name .. ".zip"
        local download_path = sys.get_save_file("mygame", zip_filename)
        local url = self.http_url .. "/" .. zip_filename

        -- Check if the archive already exists. If it does, try to mount it!
        if sys.exists(download_path) then
            mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                if result == liveupdate.LIVEUPDATE_OK then
                    msg.post("#", "load_level", message) -- try to load the level again
                else
                    os.remove(download_path)             -- remove and try to
                    msg.post("#", "load_level", message) -- download again
                end
            end)
        else
            -- Make the request. You can use credentials
            http.request(url, "GET", function(self, id, response) -- <7>
                if response.status == 200 or response.status == 304 then
                    mount_zip(self, message.info.name, message.info.priority, download_path, function(name, uri, result) -- <8>
                        if result == liveupdate.LIVEUPDATE_OK then
                            msg.post("#", "load_level", message) -- try to load the level again
                        else
                            print("Failed to mount archive", download_path, ":", result)
                        end
                    end)
                else
                    print("Failed to download archive", download_path, "from", url, ":", response.status)
                end
            end, nil, nil, {path=download_path})
        end

    elseif message_id == hash("proxy_loaded") then -- the level is loaded, and we can enable it
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

1. `liveupdate.add_mount()` монтує один архів, використовуючи вказані ім’я, пріоритет і файл zip. Після цього дані одразу доступні для завантаження (перезапускати рушій не потрібно). Монтування активне лише протягом поточного сеансу. Зберігайте шлях до завантаженого пакета й потрібні налаштування монтування у власних даних збереження та знову викликайте `liveupdate.add_mount()` після кожного перезапуску.
2. Архів потрібно розмістити в інтернеті (наприклад, на S3), звідки його можна завантажити.
3. За іменем проксі колекції потрібно визначити, які архіви завантажити та як їх змонтувати
4. Під час запуску ми намагаємося завантажити рівень.
5. У цьому порядку роботи з публікуванням архівів використовуйте `collectionproxy.get_resources()`, щоб перевірити метадані виключеного вмісту проксі. Функція повертає `{}`, доки не змонтовано маніфест відповідного пакета, а після монтування — непорожню таблицю хешів ресурсів. Ці хеші описують залежності; сам результат не підтверджує доступність кожного блоку даних.
6. Якщо проксі використовує вміст Live Update, а відповідний архів ще не змонтовано, ми завантажуємо й монтуємо його перед завантаженням проксі.
7. Зробіть запит HTTP і завантажте архів у `download_path`
8. Дані завантажено, і тепер їх потрібно змонтувати в запущеному рушії.


Коли код завантаження готовий, можна протестувати застосунок. Однак під час запуску з редактора нічого не завантажуватиметься. Причина в тому, що функція Live Update призначена для пакетів. Під час запуску в середовищі редактора жодні ресурси не виключаються. Щоб переконатися, що все працює належним чином, потрібно створити пакет.
