---
title: Робота з файлами
brief: Цей посібник пояснює, як зберігати й завантажувати файли та виконувати інші файлові операції.
---

# Робота з файлами {#working-with-files}
Є багато різних способів створювати файли та/або отримувати до них доступ. Шляхи до файлів і способи доступу до них залежать від типу та розташування файлу.

## Функції для доступу до файлів і папок {#functions-for-file-and-folder-access}
Defold надає кілька різних функцій для роботи з файлами:

* Для читання й записування файлів можна використовувати стандартні [функції `io.*`](https://defold.com/ref/stable/io/). Ці функції дають змогу дуже точно керувати всім процесом введення-виведення.

```lua
-- open myfile.txt for writing in binary mode
-- returns nil plus error message on failure
local f, err = io.open("path/to/myfile.txt", "wb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- write to the file, flush it to disk and then close the file
f:write("Foobar")
f:flush()
f:close()

-- open myfile.txt for reading in binary mode
-- returns nil plus error message on failure
local f, err = io.open("path/to/myfile.txt", "rb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- read the entire file as a string
-- returns nil on failure
local s = f:read("*a")
if not s then
	print("Error while reading file")
	return
end

print(s) -- Foobar
```

* Для перейменування й видалення файлів можна використовувати [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) та [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename).

* Для читання й записування таблиць Lua можна використовувати [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) та [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename). Додаткові функції [`sys.*`](https://defold.com/ref/stable/sys/) допомагають визначати шляхи до файлів незалежно від платформи.

```lua
-- get a platform independent path to the file "highscore" for application "mygame"
local path = sys.get_save_file("mygame", "highscore")

-- save a Lua table with some data
local ok = sys.save(path, { highscore = 100 })
if not ok then
	print("Failed to save", path)
	return
end

-- load the data
local ok, data = pcall(sys.load, path)
if not ok then
	-- The file exists, but is corrupt, foreign, or uses an unsupported format.
	print("Failed to load save data:", data)
	data = {}
end
print(data.highscore) -- 100
```

`sys.load()` повертає порожню таблицю, якщо файл не існує. Якщо файл існує, але його створено не за допомогою `sys.save()`, він пошкоджений або використовує непідтримуваний формат серіалізованої таблиці, `sys.load()` спричиняє помилку Lua. Використовуйте `pcall()`, як показано вище, коли потрібно забезпечити відновлення після пошкодження або зовнішньої зміни збережених даних.


## Розташування файлів і папок {#file-and-folder-locations}
Розташування файлів і папок можна поділити на три категорії:

* Файли застосунку, які створює ваш застосунок
* Файли й папки, що входять до пакета вашого застосунку
* Системні файли, до яких звертається ваш застосунок

### Як зберігати й завантажувати файли застосунку {#how-to-save-and-load-application-specific-files}
Для зберігання й завантаження файлів застосунку, як-от рекордів, налаштувань користувача та стану гри, рекомендовано використовувати розташування, яке операційна система надає спеціально для цієї мети. За допомогою [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) можна отримати абсолютний шлях до файлу для відповідної ОС. Отримавши абсолютний шлях, ви можете використовувати функції `sys.*`, `io.*` та `os.*` (див. вище).

[Перегляньте приклад використання `sys.save()` і `sys.load()`](/examples/file/sys_save_load/).

### Як отримати доступ до файлів, що входять до пакета застосунку {#how-to-access-files-bundled-with-the-application}
Ви можете включити файли до свого застосунку за допомогою ресурсів пакета (bundle resources) та користувацьких ресурсів (custom resources).

#### Користувацькі ресурси {#custom-resources}
:[Користувацькі ресурси](../shared/custom-resources.md)

Розширення також можуть надавати ці файли через `ext.properties`. Їхні шляхи об’єднуються з користувацькими ресурсами проєкту як у збірках редактора, так і в архівах Bob. Див. [користувацькі ресурси розширень](/manuals/extensions/#custom-resources).

```lua
-- Load level data into a string
local data, error = sys.load_resource("/assets/level_data.json")
-- Decode json string to a Lua table
if data then
  local data_table = json.decode(data)
  pprint(data_table)
else
  print(error)
end
```

#### Ресурси пакета {#bundle-resources}
:[Ресурси пакета](../shared/bundle-resources.md)

```lua
local path = sys.get_application_path()
local f = io.open(path .. "/mycommonfile.txt", "rb")
local txt, err = f:read("*a")
if not txt then
	print(err)
	return
end
print(txt)
```

::: sidenote
З міркувань безпеки браузерам (а отже, і будь-якому коду JavaScript, що виконується у браузері) заборонено доступ до системних файлів. Файлові операції у збірках HTML5 у Defold працюють, але лише у «віртуальній файловій системі», яка використовує API IndexedDB у браузері. Це означає, що отримати доступ до ресурсів пакета за допомогою функцій `io.*` або `os.*` неможливо. Однак ви можете отримати доступ до ресурсів пакета за допомогою `http.request()`.
:::


#### Порівняння користувацьких ресурсів і ресурсів пакета {#custom-and-bundle-resources-comparison}

| Характеристика              | Користувацькі ресурси                     | Ресурси пакета                                 |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| Швидкість завантаження      | Швидше — файли завантажуються з двійкового архіву | Повільніше — файли завантажуються з файлової системи |
| Часткове завантаження файлів | Ні — лише файли цілком                    | Так — читання довільних байтів із файлу         |
| Змінення файлів після пакування | Ні — файли зберігаються всередині двійкового архіву | Так — файли зберігаються в локальній файловій системі |
| Підтримка HTML5              | Так                                       | Так — але доступ через http, а не файлове введення-виведення |


### Доступ до системних файлів {#system-file-access}
Операційна система може обмежувати доступ до системних файлів із міркувань безпеки. За допомогою нативного розширення [`extension-directories`](https://defold.com/assets/extensiondirectories/) можна отримати абсолютний шлях до деяких поширених системних каталогів (наприклад, `documents`, `resource`, `temp`). Отримавши абсолютний шлях до цих файлів, ви можете використовувати функції `io.*` та `os.*` для доступу до них (див. вище).

::: sidenote
З міркувань безпеки браузерам (а отже, і будь-якому коду JavaScript, що виконується у браузері) заборонено доступ до системних файлів. Файлові операції у збірках HTML5 у Defold працюють, але лише у «віртуальній файловій системі», яка використовує API IndexedDB у браузері. Це означає, що у збірках HTML5 неможливо отримати доступ до системних файлів.
:::

## Розширення {#extensions}
На [порталі Defold Assets](https://defold.com/assets/) є кілька ресурсів для спрощення доступу до файлів і папок. Ось деякі приклади:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) — функції для роботи з каталогами, дозволами на доступ до файлів тощо
* [DefSave](https://defold.com/assets/defsave/) — модуль, що допомагає зберігати й завантажувати налаштування та дані гравця між сеансами.
