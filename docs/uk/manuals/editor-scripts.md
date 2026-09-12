---
title: Скрипти редактора
brief: Цей посібник пояснює, як розширити можливості редактора за допомогою Lua
---

# Скрипти редактора {#editor-scripts}

Ви можете створювати власні пункти меню й обробники життєвого циклу редактора за допомогою файлів Lua зі спеціальним розширенням: `.editor_script`. Ця система дає змогу налаштувати редактор, щоб удосконалити робочий процес розробки.

## Середовище виконання скриптів редактора {#editor-script-runtime}

Скрипти редактора виконуються всередині редактора, у віртуальній машині Lua, яку емулює віртуальна машина Java. Усі скрипти використовують єдине спільне середовище, а отже, можуть взаємодіяти між собою. Ви можете підключати модулі Lua за допомогою `require`, як і у файлах `.script`, але версія Lua, що працює всередині редактора, відрізняється, тому переконайтеся, що ваш спільний код сумісний із нею. Редактор використовує Lua версії 5.2.x, а саме середовище виконання [luaj](https://github.com/luaj/luaj), яке наразі є єдиним практичним рішенням для запуску Lua на JVM. Крім того, є певні обмеження:
- пакет `debug` відсутній;
- `os.execute` відсутня, але ми надаємо подібну функцію `editor.execute()`;
- `os.tmpname` та `io.tmpfile` відсутні — наразі скрипти редактора можуть отримувати доступ до файлів лише в каталозі проєкту;
- наразі `os.rename` відсутня, хоча ми плануємо її додати;
- `os.exit` та `os.setlocale` відсутні.
- деякі функції з тривалим виконанням не можна використовувати в контекстах, де редактору потрібна негайна відповідь від скрипту; докладніше див. у розділі [Режими виконання](#execution-modes).

Усі розширення редактора, визначені в скриптах редактора, завантажуються, коли ви відкриваєте проєкт. Коли ви отримуєте бібліотеки, розширення перезавантажуються, оскільки в бібліотеках, від яких залежить ваш проєкт, можуть з’явитися нові скрипти редактора. Під час цього перезавантаження зміни у ваших власних скриптах редактора не враховуються, адже ви можете саме працювати над ними. Щоб перезавантажити і їх, виконайте команду **Project → Reload Editor Scripts**.

## Будова `.editor_script` {#anatomy-of-editor_script}

Кожен скрипт редактора має повертати модуль, наприклад:
```lua
local M = {}

function M.get_commands()
  -- TODO - define editor commands
end

function M.get_language_servers()
  -- TODO - define language servers
end

function M.get_prefs_schema()
  -- TODO - define preferences
end

return M
```
Потім редактор збирає всі скрипти редактора, визначені в проєкті й бібліотеках, завантажує їх у спільну віртуальну машину Lua та викликає за потреби (докладніше про це — у розділах [Команди](#commands) та [Обробники життєвого циклу](#lifecycle-hooks)).

## API редактора {#editor-api}

Ви можете взаємодіяти з редактором через пакет `editor`, який визначає такий API:
- `editor.platform` — рядок зі значенням `"x86_64-win32"` для Windows, `"x86_64-macos"` для macOS або `"x86_64-linux"` для Linux.
- `editor.version` — рядок із назвою версії Defold, наприклад `"1.4.8"`
- `editor.engine_sha1` — рядок із SHA1 рушія Defold
- `editor.editor_sha1` — рядок із SHA1 редактора Defold
- `editor.get(node_id, property)` — отримати значення властивості певного вузла всередині редактора. Вузлами в редакторі є різні сутності, як-от файли скриптів або колекцій (collection), ігрові об’єкти (game object) усередині колекцій, файли json, завантажені як ресурси, тощо. `node_id` — це значення типу userdata, яке редактор передає скрипту редактора. Замість ідентифікатора вузла також можна передати шлях до ресурсу, наприклад `"/main/game.script"`. `property` — це рядок. Наразі підтримуються такі властивості:
  - `"path"` — шлях до файлу відносно каталогу проєкту для *ресурсів* — сутностей, що існують як файли або каталоги. Приклад значення, що повертається: `"/main/game.script"`
  - `"children"` — список шляхів до дочірніх ресурсів для ресурсів-каталогів
  - `"parent"` — батьківський вузол редактора для вузла Outline, що має батьківський вузол
  - `"text"` — текстовий вміст ресурсу, який можна редагувати як текст (наприклад, файлів скриптів або json). Приклад значення, що повертається: `"function init(self)\nend"`. Зауважте, що це не те саме, що читання файлу за допомогою `io.open()`, оскільки ви можете редагувати файл, не зберігаючи його, і ці зміни доступні лише під час звернення до властивості `"text"`.
  - для атласів: `images` (список вузлів редактора для зображень в атласі) та `animations` (список вузлів анімацій)
  - для анімацій атласу: `images` (те саме, що й `images` в атласі)
  - для карт плиток: `layers` (список вузлів редактора для шарів у карті плиток)
  - для шарів карти плиток: `tiles` (необмежена двовимірна сітка плиток), докладніше див. `tilemap.tiles.*`
  - для ефектів частинок: `emitters` (список вузлів випромінювачів у редакторі) та `modifiers` (список вузлів модифікаторів у редакторі)
  - для випромінювачів ефектів частинок: `modifiers` (список вузлів модифікаторів у редакторі)
  - для об’єктів колізій: `shapes` (список вузлів форм колізій у редакторі)
  - для файлів GUI: списки вузлів, як-от `layers`, `fonts`, `materials`, `textures`, `particlefxs`, `nodes` та `layouts`
  - деякі властивості, що відображаються на панелі Properties, коли ви щось вибрали на панелі Outline. Підтримуються такі типи властивостей Outline:
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    Зауважте, що деякі з цих властивостей можуть бути доступні лише для читання, а деякі — недоступні в певних контекстах, тому використовуйте `editor.can_get` перед їх читанням і `editor.can_set` перед встановленням їхніх значень у редакторі. Наведіть вказівник на назву властивості на панелі Properties, щоб побачити підказку з інформацією про те, як ця властивість називається у скриптах редактора. Ви можете встановити властивості ресурсу в `nil`, передавши значення `""`.
- `editor.properties(node_id)` — повернути відсортований список назв властивостей, які можна прочитати з вузла, з урахуванням контексту, наприклад `pprint(editor.properties("/game.project"))`. За допомогою функцій `editor.can_*` перевіряйте, чи можна також змінювати або скидати властивість зі списку, додавати до неї елементи чи змінювати їхній порядок.
- `editor.can_get(node_id, property)` — перевірити, чи можна отримати цю властивість, щоб `editor.get()` не спричинила помилку.
- `editor.can_set(node_id, property)` — перевірити, чи не спричинить помилку крок транзакції `editor.tx.set()` із цією властивістю.
- `editor.create_directory(resource_path)` — створити каталог, якщо він не існує, і всі відсутні батьківські каталоги.
- `editor.create_resources(resources)` — створити 1 або більше ресурсів із шаблонів або з власним вмістом
- `editor.delete_directory(resource_path)` — видалити каталог, якщо він існує, а також усі наявні дочірні каталоги й файли.
- `editor.execute(cmd, [...args], [options])` — виконати команду оболонки, за потреби перехопивши її виведення.
- `editor.save()` — зберегти всі незбережені зміни на диску.
- `editor.transact(txs)` — змінити стан редактора в пам’яті за допомогою 1 або більше кроків транзакції, створених функціями `editor.tx.*`.
- `editor.ui.*` — різні функції для роботи з інтерфейсом користувача, див. [посібник з інтерфейсів скриптів редактора](/manuals/editor-scripts-ui).
- `editor.prefs.*` — функції для взаємодії з налаштуваннями редактора, див. [Налаштування редактора](#preferences).

Повний довідник API редактора можна знайти [тут](/ref/stable/editor/).

## Команди {#commands}

Якщо модуль скрипту редактора визначає `get_commands()`, ця функція викликається під час перезавантаження розширень. Повернуті команди можуть з’являтися в меню на панелі меню та в контекстних меню Assets, Outline, Scene і Code залежно від їхніх `locations`. Приклад:

```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
      locations = {"Edit", "Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        local path = editor.get(opts.selection, "path")
        return ends_with(path, ".lua") or ends_with(path, ".script")
      end,
      run = function(opts)
        local text = editor.get(opts.selection, "text")
        editor.transact({
          editor.tx.set(opts.selection, "text", strip_comments(text))
        })
      end
    },
    {
      label = "Minify JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        editor.execute("./scripts/minify-json.sh", path:sub(2))
      end
    }
  }
end

return M
```
Редактор очікує, що `get_commands()` поверне масив таблиць, кожна з яких описує окрему команду. Опис команди складається з таких полів:

- `label` (обов’язкове) — текст пункту меню, який бачитиме користувач
- `locations` (обов’язкове) — масив, що описує, де ця команда має бути доступною. Підтримуються значення `"Edit"`, `"View"`, `"Project"`, `"Debug"` та `"Help"` для відповідних меню на панелі меню; `"Bundle"` для підменю **Project → Bundle**; а також `"Assets"`, `"Outline"`, `"Scene"` та `"Code"` для відповідних контекстних меню.
- `query` — спосіб, яким команда запитує в редактора потрібну інформацію та визначає, з якими даними вона працює. Кожному ключу в таблиці `query` відповідатиме ключ у таблиці `opts`, яку зворотні виклики `active` і `run` отримують як аргумент. Підтримувані ключі:
  - `selection` означає, що ця команда доступна, коли щось вибрано, і працює з цим вибраним вмістом.
    - `type` — тип вибраних вузлів, які потрібні команді; наразі допускаються такі типи:
      - `"resource"` — в Assets та Outline ресурсом є вибраний елемент, який має відповідний файл. На панелі меню (Edit або View) ресурсом є поточний відкритий файл;
      - `"outline"` — щось, що можна показати в Outline. В Outline це вибраний елемент, на панелі меню — поточний відкритий файл;
      - `"scene"` — щось, що можна відобразити в Scene.
    - `cardinality` визначає, скільки елементів має бути вибрано. Якщо значення дорівнює `"one"`, вибір, переданий зворотному виклику команди, буде одним ідентифікатором вузла. Якщо `"many"` — масивом з одного або більше ідентифікаторів вузлів.
  - `active_view` означає, що ця команда доступна, коли активна область редактора відповідає запитаному типу. Активна область передається зворотному виклику команди як `opts.active_view`.
    - `type` — тип активної області, яка потрібна команді: `"code"`, `"scene"`, `"html"` або `"form"`.
    - Активна область підтримує властивості `"type"`, `"resource"` та `"dirty"`. Використовуйте `editor.get(view, "resource")`, щоб отримати ресурс, показаний в області, та `editor.get(view, "dirty")`, щоб перевірити, чи є в ньому незбережені зміни.
  - `argument` — аргумент команди. Наразі аргумент отримують лише команди в розташуванні `"Bundle"`: він дорівнює `true`, коли команду пакування вибрано явно, та `false` під час повторного пакування.
- `id` — рядок ідентифікатора команди, який використовується, наприклад, для збереження останньої використаної команди пакування в `prefs`
- `active` — зворотний виклик, який перевіряє, чи активна команда; він має повертати булеве значення. Якщо `locations` містить `"Assets"`, `"Scene"` або `"Outline"`, `active` викликатиметься під час показу контекстного меню. Якщо розташування містять `"Edit"` або `"View"`, active викликатиметься під час кожної дії користувача, наприклад введення з клавіатури чи клацання мишею, тому переконайтеся, що `active` працює досить швидко.
- `run` — зворотний виклик, який виконується, коли користувач вибирає пункт меню.

### Змінення стану редактора в пам’яті за допомогою команд {#use-commands-to-change-the-in-memory-editor-state}

Усередині обробника `run` ви можете запитувати та змінювати стан редактора в пам’яті. Для запитів використовується функція `editor.get()`, за допомогою якої можна дізнатися поточний стан файлів і вибраного вмісту (якщо використовується `query = {selection = ...}`). Ви можете отримати властивість `"text"` ресурсів, які можна редагувати як текст, а також деякі властивості, показані на панелі Properties — наведіть вказівник на назву властивості, щоб побачити підказку про її назву в скриптах редактора. Для змінення стану редактора використовується `editor.transact()`, де ви об’єднуєте 1 або більше змін в один крок, який можна скасувати. Наприклад, якщо ви хочете мати можливість скидати трансформацію ігрового об’єкта, можна написати таку команду:
```lua
{
  label = "Reset transform",
  locations = {"Outline"},
  query = {selection = {type = "outline", cardinality = "one"}},
  active = function(opts)
    local node = opts.selection
    return editor.can_set(node, "position") 
       and editor.can_set(node, "rotation") 
       and editor.can_set(node, "scale")
  end,
  run = function(opts)
    local node = opts.selection
    editor.transact({
      editor.tx.set(node, "position", {0, 0, 0}),
      editor.tx.set(node, "rotation", {0, 0, 0}),
      editor.tx.set(node, "scale", {1, 1, 1})
    })
  end
}
```

### Використання команд з активною областю редактора {#use-commands-with-the-active-editor-view}

Команди в меню, як-от `"View"`, можуть запитувати поточну активну область редактора. Це корисно, коли команда має працювати з файлом або сценою, які користувач зараз переглядає:

```lua
editor.command({
  label = "Print Active View",
  locations = {"View"},
  query = {active_view = {type = "code"}},
  run = function(opts)
    local view = opts.active_view
    local resource = editor.get(view, "resource")
    print(editor.get(view, "type"))
    print(editor.get(resource, "path"))
    print(editor.get(view, "dirty"))
  end
})
```

#### Редагування атласів {#editing-atlases}

Окрім читання та записування властивостей атласу, ви можете читати та змінювати зображення й анімації атласу. Атлас визначає властивості списків вузлів `images` та `animations`, а анімації визначають властивість списку вузлів `images`: із цими властивостями можна використовувати кроки транзакцій `editor.tx.add`, `editor.tx.remove` та `editor.tx.clear`.

Наприклад, щоб додати зображення до атласу, виконайте такий код в обробнику `run` команди:
```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```
Щоб знайти множину всіх зображень в атласі, виконайте такий код:
```lua
local all_images = {} ---@type table<string, true>
-- first, collect all "bare" images
local image_nodes = editor.get("/main.atlas", "images")
for i = 1, #image_nodes do
    all_images[editor.get(image_nodes[i], "image")] = true
end
-- second, collect all images used in animations
local animation_nodes = editor.get("/main.atlas", "animations")
for i = 1, #animation_nodes do
    local animation_image_nodes = editor.get(animation_nodes[i], "images")
    for j = 1, #animation_image_nodes do
        all_images[editor.get(animation_image_nodes[j], "image")] = true
    end
end
pprint(all_images)
-- {
--     ["/assets/hero.png"] = true,
--     ["/assets/enemy.png"] = true,
-- }}
```
Щоб замінити всі анімації в атласі:
```lua
editor.transact({
    editor.tx.clear("/main.atlas", "animations"),
    editor.tx.add("/main.atlas", "animations", {
        id = "hero_run",
        images = {
            {image = "/assets/hero_run_1.png"},
            {image = "/assets/hero_run_2.png"},
            {image = "/assets/hero_run_3.png"},
            {image = "/assets/hero_run_4.png"}
        }
    })
})
```

#### Редагування джерел плиток {#editing-tilesources}

Окрім властивостей Outline, джерела плиток визначають такі властивості:
- `animations` — список вузлів анімацій джерела плиток
- `collision_groups` — список вузлів груп колізій джерела плиток
- `tile_collision_groups` — таблиця призначень груп колізій для плиток у джерелі плиток

Наприклад, ось як можна налаштувати джерело плиток:
```lua
local tilesource = "/game/world.tilesource"
editor.transact({
    editor.tx.add(tilesource, "animations", {id = "idle", start_tile = 1, end_tile = 1}),
    editor.tx.add(tilesource, "animations", {id = "walk", start_tile = 2, end_tile = 6, fps = 10}),
    editor.tx.add(tilesource, "collision_groups", {id = "player"}),
    editor.tx.add(tilesource, "collision_groups", {id = "obstacle"}),
    editor.tx.set(tilesource, "tile_collision_groups", {
        [1] = "player",
        [7] = "obstacle",
        [8] = "obstacle"
    })
})
```

#### Редагування карт плиток {#editing-tilemaps}

Карти плиток визначають властивість `layers` — список вузлів шарів карти плиток. Кожен шар також визначає властивість `tiles`, яка містить необмежену двовимірну сітку плиток цього шару. Це відрізняється від рушія: плитки не мають меж і їх можна додавати будь-де, зокрема за від’ємними координатами. Для редагування плиток API скриптів редактора визначає модуль `tilemap.tiles` із такими функціями:
- `tilemap.tiles.new()` — створити нову структуру даних, що містить необмежену двовимірну сітку плиток (у редакторі, на відміну від рушія, карта плиток не має меж, а координати можуть бути від’ємними)
- `tilemap.tiles.get_tile(tiles, x, y)` — отримати індекс плитки за заданими координатами
- `tilemap.tiles.get_info(tiles, x, y)` — отримати повну інформацію про плитку за заданими координатами (структура даних така сама, як у функції `tilemap.get_tile_info` рушія)
- `tilemap.tiles.iterator(tiles)` — створити ітератор для всіх плиток карти плиток
- `tilemap.tiles.clear(tiles)` — видалити всі плитки з карти плиток
- `tilemap.tiles.set(tiles, x, y, tile_or_info)` — встановити плитку за заданими координатами
- `tilemap.tiles.remove(tiles, x, y)` — видалити плитку за заданими координатами

Наприклад, ось як можна вивести вміст усієї карти плиток:
```lua
local layers = editor.get("/level.tilemap", "layers")
for i = 1, #layers do
    local layer = layers[i]
    local id = editor.get(layer, "id")
    local tiles = editor.get(layer, "tiles")
    print("layer " .. id .. ": {")
    for x, y, tile in tilemap.tiles.iterator(tiles) do
        print("  [" .. x .. ", " .. y .. "] = " .. tile)
    end
    print("}")
end
```

Ось приклад додавання шару з плитками до карти плиток:
```lua
local tiles = tilemap.tiles.new()
tilemap.tiles.set(tiles, 1, 1, 2)
editor.transact({
    editor.tx.add("/level.tilemap", "layers", {
        id = "new_layer",
        tiles = tiles
    })
})
```

#### Редагування ефектів частинок {#editing-particlefx}

Ви можете редагувати ефекти частинок за допомогою властивостей `modifiers` та `emitters`. Наприклад, ось як додати випромінювач у формі кола з модифікатором прискорення:
```lua
editor.transact({
    editor.tx.add("/fire.particlefx", "emitters", {
        type = "emitter-type-circle",
        modifiers = {
          {type = "modifier-type-acceleration"}
        }
    })
})
```
Багато властивостей ефектів частинок є кривими або кривими з розкидом (тобто кривою та певним значенням для випадкового відхилення). Криві подаються як таблиця з непорожнім списком `points`, де кожна точка — це таблиця з такими властивостями:
- `x` — координата x точки; має починатися з 0 і закінчуватися на 1
- `y` — значення точки
- `tx` (від 0 до 1) і `ty` (від -1 до 1) — компоненти дотичної в точці. Наприклад, для кута 80 градусів `tx` має бути `math.cos(math.rad(80))`, а `ty` — `math.sin(math.rad(80))`.
Криві з розкидом додатково мають числову властивість `spread`.

Наприклад, встановлення кривої альфа-каналу впродовж часу існування частинки для вже наявного випромінювача може виглядати так:
```lua
local emitter = editor.get("/fire.particlefx", "emitters")[1]
editor.transact({
    editor.tx.set(emitter, "particle_key_alpha", { points = {
        {x = 0,   y = 0, tx = 0.1, ty = 1}, -- start at 0, go up quickly
        {x = 0.2, y = 1, tx = 1,   ty = 0}, -- reach 1 at 20% of a lifetime
        {x = 1,   y = 0, tx = 1,   ty = 0}  -- slowly go down to 0
    }})
})
```
Звісно, ключ `particle_key_alpha` також можна використовувати в таблиці під час створення випромінювача. Крім того, для подання «статичної» кривої натомість можна використати одне число.

#### Редагування об’єктів колізій {#editing-collision-objects}

Окрім стандартних властивостей Outline, об’єкти колізій визначають властивість списку вузлів `shapes`. Ось як додати нові форми колізій:
```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- or "shape-type-sphere", "shape-type-capsule"
    })
})
```
Властивість `type` форми є обов’язковою під час створення та не може бути змінена після додавання форми. Є 3 типи форм:
- `shape-type-box` — форма паралелепіпеда з властивістю `dimensions`
- `shape-type-sphere` — форма сфери з властивістю `diameter`
- `shape-type-capsule` — форма капсули з властивостями `diameter` та `height`

#### Редагування файлів GUI {#editing-gui-files}

Окрім властивостей Outline, файли GUI визначають кілька властивостей списків вузлів:

- `layers` — список вузлів шарів у редакторі (порядок можна змінювати)
- `fonts` — список вузлів шрифтів у редакторі
- `materials` — список вузлів матеріалів у редакторі
- `textures` — список вузлів текстур у редакторі
- `particlefxs` — список вузлів ефектів частинок у редакторі
- `nodes` — список вузлів GUI у редакторі
- `layouts` — список вузлів макетів GUI у редакторі

Ви можете редагувати шари GUI за допомогою властивості редактора `layers`, наприклад:
```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```
Крім того, можна змінювати порядок шарів:
```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```
Аналогічно, шрифти, матеріали, текстури й ефекти частинок редагуються за допомогою властивостей `fonts`, `materials`, `textures` та `particlefxs`:
```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.particlefx"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```
Ці властивості не підтримують змінення порядку.

Нарешті, ви можете редагувати вузли GUI за допомогою властивості списку `nodes`, наприклад:
```lua
editor.transact({
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-box",
        position = {20, 20, 20}
    }),
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-template",
        template = "/button.gui"
    }),
})
```
Вбудовані типи вузлів:
- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

Якщо ви використовуєте розширення spine, також можна використовувати тип вузла `gui-node-type-spine`.

Якщо файл GUI визначає макети, ви можете отримувати й установлювати значення з макетів за допомогою синтаксису `layout:property`, наприклад:
```lua
local node = editor.get("/main.gui", "nodes")[1]

-- GET:
local position = editor.get(node, "position")
pprint(position) -- {20, 20, 20}
local landscape_position = editor.get(node, "Landscape:position")
pprint(landscape_position) -- {20, 20, 20}

-- SET:
editor.transact({
    editor.tx.set(node, "Landscape:position", {30, 30, 30})
})
pprint(editor.get(node, "Landscape:position")) -- {30, 30, 30}
```

Установлені властивості макету можна скинути до типових значень за допомогою `editor.tx.reset`:
```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```
Дерева вузлів шаблонів можна читати, але не редагувати — у дереві вузлів шаблону можна лише встановлювати властивості вузлів:
```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (overrides a value in the template)
```

#### Редагування ігрових об’єктів {#editing-game-objects}

За допомогою скриптів редактора можна редагувати компоненти (component) файлу ігрового об’єкта. Компоненти бувають двох видів: додані за посиланням (by reference) та вбудовані. Компоненти, додані за посиланням, мають тип `component-reference` і посилаються на інші ресурси, даючи змогу перевизначати лише властивості go, визначені у скриптах. Вбудовані компоненти мають типи на кшталт `sprite`, `label` тощо й дають змогу редагувати всі властивості, визначені типом компонента, а також додавати підкомпоненти, як-от форми об’єктів колізій. Наприклад, щоб налаштувати ігровий об’єкт, можна використати такий код:
```lua
editor.transact({
    editor.tx.add("/npc.go", "components", {
        type = "sprite",
        id = "view"
    }),
    editor.tx.add("/npc.go", "components", {
        type = "collisionobject",
        id = "collision",
        shapes = {
            {
                type = "shape-type-box",
                dimensions = {32, 32, 32}
            }
        }
    }),
    editor.tx.add("/npc.go", "components", {
        type = "component-reference",
        path = "/npc.script",
        id = "controller",
        __hp = 100 -- set a go property defined in the script
    })
})
```

#### Редагування колекцій {#editing-collections}
За допомогою скриптів редактора можна редагувати колекції. Ви можете додавати ігрові об’єкти (вбудовані або за посиланням) та колекції (за посиланням). Наприклад:
```lua
local coll = "/char.collection"
editor.transact({
    editor.tx.add(coll, "children", {
        -- embbedded game object
        type = "go",
        id = "root",
        children = {
            {
                -- referenced game object
                type = "go-reference",
                path = "/char-view.go",
                id = "view"
            },
            {
                -- referenced collection
                type = "collection-reference",
                path = "/body-attachments.collection",
                id = "attachments"
            }
        },
        -- embedded gos can also have components
        components = {
            {
                type = "collisionobject",
                id = "collision",
                shapes = {
                    {type = "shape-type-box", dimensions = {2.5, 2.5, 2.5}}
                }
            },
            {
                type = "component-reference",
                id = "controller",
                path = "/char.script",
                __hp = 100 -- set a go property defined in the script
            }
        }
    })
})
```

Як і в редакторі, колекції за посиланням можна додавати лише до кореня редагованої колекції, а ігрові об’єкти — лише до вбудованих ігрових об’єктів або ігрових об’єктів за посиланням, але не до колекцій за посиланням чи ігрових об’єктів усередині цих колекцій за посиланням.

### Використання команд оболонки {#use-shell-commands}

Усередині обробника `run` ви можете записувати дані у файли (за допомогою модуля `io`) та виконувати команди оболонки (за допомогою команди `editor.execute()`). Під час виконання команд оболонки можна перехопити виведення команди як рядок, а потім використати його в коді. Наприклад, якщо ви хочете створити команду форматування JSON, яка викликає через оболонку глобально встановлену програму [`jq`](https://jqlang.github.io/jq/), можна написати таку команду:
```lua
{
  label = "Format JSON",
  locations = {"Assets"},
  query = {selection = {type = "resource", cardinality = "one"}},
  action = function(opts)
    local path = editor.get(opts.selection, "path")
    return path:match(".json$") ~= nil
  end,
  run = function(opts)
    local text = editor.get(opts.selection, "text")
    local new_text = editor.execute("jq", "-n", "--argjson", "data", text, "$data", {
      reload_resources = false, -- don't reload resources since jq does not touch disk
      out = "capture" -- return text output instead of nothing
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```
Оскільки ця команда викликає програму оболонки лише для читання (і повідомляє про це редактор за допомогою `reload_resources = false`), ви отримуєте можливість скасувати цю дію.

::: sidenote
Якщо ви хочете поширювати свій скрипт редактора як бібліотеку, можливо, варто додати до залежності двійкову програму для платформ редактора. Докладніше про це див. у розділі [Скрипти редактора в бібліотеках](#editor-scripts-in-libraries).
:::

## Обробники життєвого циклу {#lifecycle-hooks}

Є файл скрипту редактора, який обробляється особливим чином: `hooks.editor_script`, розташований у корені вашого проєкту, у тому самому каталозі, що й *game.project*. Лише цей скрипт редактора отримуватиме події життєвого циклу від редактора. Приклад такого файлу:
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
Ми вирішили обмежити обробники життєвого циклу одним файлом скрипту редактора, оскільки порядок виконання обробників збирання важливіший за простоту додавання чергового кроку збирання. Команди незалежні одна від одної, тому порядок їх відображення в меню не має особливого значення: зрештою користувач виконує конкретну вибрану команду. Якби обробники збирання можна було визначати в різних скриптах редактора, виникла б проблема: у якому порядку вони виконуватимуться? Імовірно, ви хочете обчислювати контрольні суми вмісту після його стиснення... Один файл, який задає порядок кроків збирання, явно викликаючи функцію кожного кроку, дає змогу розв’язати цю проблему.

Наявні обробники життєвого циклу, які можна визначити в `/hooks.editor_script`:
- `on_build_started(opts)` — виконується, коли гра збирається для локального запуску або запуску на віддаленій цілі за допомогою команд Project Build або Debug Start. Ваші зміни з’являться в зібраній грі. Помилка з цього обробника перерве збирання. `opts` — таблиця, яка містить такі ключі:
  - `platform` — рядок у форматі `%arch%-%os%`, який описує платформу, для якої виконується збирання; наразі його значення завжди збігається з `editor.platform`.
- `on_build_finished(opts)` — виконується після завершення збирання, незалежно від того, чи було воно успішним. `opts` — таблиця з такими ключами:
  - `platform` — те саме, що й в `on_build_started`
  - `success` — чи успішне збирання: `true` або `false`
- `on_bundle_started(opts)` — виконується, коли ви створюєте пакет або збираєте HTML5-версію гри. Як і з `on_build_started`, зміни, спричинені цим обробником, з’являться в пакеті, а помилки перервуть пакування. `opts` матиме такі ключі:
  - `output_directory` — шлях до каталогу з результатом пакування. **Project ▸ Build HTML5** використовує власне дерево артефактів, наприклад `"/path/to/project/build/default_html5/__htmlLaunchDir"`, окреме від звичайних результатів Build у `build/default`.
  - `platform` — платформа, для якої пакується гра. Перелік можливих значень платформи див. у [посібнику з Bob](/manuals/bob).
  - `variant` — варіант пакета: `"debug"`, `"release"` або `"headless"`
- `on_bundle_finished(opts)` — виконується після завершення пакування, незалежно від того, чи було воно успішним. `opts` — таблиця з тими самими даними, що й `opts` в `on_bundle_started`, а також ключем `success`, який указує, чи було збирання успішним.
- `on_target_launched(opts)` — виконується, коли користувач запустив гру і вона успішно стартувала. `opts` містить ключ `url`, який указує на запущений сервіс рушія, наприклад `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — виконується, коли запущена гра закривається; має ті самі opts, що й `on_target_launched`

Зауважте, що наразі обробники життєвого циклу доступні лише в редакторі й не виконуються Bob під час пакування з командного рядка.

## Мовні сервери {#language-servers}

Редактор підтримує частину можливостей [Language Server Protocol](https://microsoft.github.io/language-server-protocol/): діагностику (перевірки коду), автодоповнення, інформацію при наведенні, символи документа в панелі Structure, перехід до визначення, пошук посилань, перейменування символів і форматування документа або діапазону. Наведіть вказівник на символ, щоб побачити інформацію від мовного сервера. Установивши курсор на символі, натисніть <kbd>F2</kbd>, щоб перейменувати його, <kbd>F12</kbd>, щоб перейти до його визначення, або <kbd>Shift+F12</kbd>, щоб знайти посилання. Ці дії також доступні в меню <kbd>Edit</kbd>. Команду форматування й налаштування форматування під час збереження описано в розділі [Форматування коду](/manuals/writing-code/#formatting-code).

Вбудований мовний сервер Lua містить анотації типів Defold для API скриптів середовища виконання й редактора. У файлах `.editor_script` автодоповнення та діагностика розпізнають функції `editor.*`, типи їхніх аргументів і повернених значень. Див. [автодоповнення коду](/manuals/writing-code/#code-completion).

Щоб зареєструвати додатковий мовний сервер, визначте функцію `get_language_servers` свого скрипту редактора так:

```lua
function M.get_language_servers()
  local command = 'build/plugins/my-ext/plugins/bin/' .. editor.platform .. '/lua-lsp'
  if editor.platform == 'x86_64-win32' then
    command = command .. '.exe'
  end
  return {
    {
      languages = {'lua'},
      watched_files = {
        { pattern = '**/.luacheckrc' }
      },
      command = {command, '--stdio'}
    }
  }
end
```
Редактор запустить мовний сервер за допомогою вказаної `command`, використовуючи стандартні потоки введення та виведення процесу сервера для обміну даними.

У таблиці визначення мовного сервера можна вказати:
- `languages` (обов’язкове) — список мов, з якими працює сервер, визначених [тут](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers) (розширення файлів також підходять);
- `command` (обов’язкове) — масив із командою та її аргументами
- `watched_files` — масив таблиць із ключами `pattern` (шаблон glob), які спричинятимуть надсилання серверу сповіщення про [зміну відстежуваних файлів](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles).

## HTTP-сервер {#http-server}

У кожному запущеному екземплярі (instance) редактора працює HTTP-сервер. Його можна розширювати за допомогою скриптів редактора. Щоб розширити HTTP-сервер редактора, додайте до скрипту редактора функцію `get_http_server_routes` — вона має повертати додаткові маршрути:
```lua
print("My route: " .. http.server.url .. "/my-extension")

function M.get_http_server_routes()
  return {
    http.server.route("/my-extension", "GET", function(request)
      return http.server.response(200, "Hello world!")
    end)
  }
end
```
Після перезавантаження скриптів редактора ви побачите в консолі таке виведення: `My route: http://0.0.0.0:12345/my-extension`. Якщо ви відкриєте це посилання у браузері, то побачите своє повідомлення `"Hello world!"`.

Вхідний аргумент `request` — це проста таблиця Lua з інформацією про запит. Вона містить такі ключі, як `path` (сегмент шляху URL, що починається з `/`), `method` запиту (наприклад, `"GET"`), `headers` (таблиця з назвами заголовків у нижньому регістрі), а також необов’язкові `query` (рядок запиту) та `body` (якщо маршрут визначає, як інтерпретувати тіло). Наприклад, якщо ви хочете створити маршрут, який приймає тіло JSON, визначте його з параметром перетворювача `"json"`:
```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```
Ви можете перевірити цю кінцеву точку з командного рядка за допомогою `curl` та `jq`:
```sh
curl 'http://0.0.0.0:12345/my-extension/echo-request?q=1' -X POST --data '{"input": "json"}' | jq
{
  "path": "/my-extension/echo-request",
  "method": "POST",
  "query": "q=1",
  "headers": {
    "host": "0.0.0.0:12345",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "user-agent": "curl/8.7.1",
    "content-length": "17"
  },
  "body": {
    "input": "json"
  }
}
```
Шлях маршруту підтримує шаблони, за якими можна витягувати значення зі шляху запиту й передавати їх функції-обробнику як частину запиту, наприклад:
```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```
Тепер, якщо ви відкриєте, наприклад, `http://0.0.0.0:12345/my-extension/setting/project.title`, то побачите назву своєї гри з файлу `/game.project`.

Окрім шаблону для одного сегмента шляху, ви також можете зіставити решту шляху URL за допомогою синтаксису `{*name}`. Наприклад, ось проста кінцева точка файлового сервера, яка надає файли з кореня проєкту:
```lua
http.server.route("/my-extension/files/{*file}", function(request)
  local attrs = editor.external_file_attributes(request.file)
  if attrs.is_file then
    return http.server.external_file_response(request.file)
  else
    return 404
  end
end)
```
Тепер, якщо ви відкриєте у браузері, наприклад, `http://0.0.0.0:12345/my-extension/files/main/main.collection`, то побачите вміст файлу `main/main.collection`.

## Скрипти редактора в бібліотеках {#editor-scripts-in-libraries}

Ви можете публікувати бібліотеки з командами для інших користувачів, і редактор автоматично підхоплюватиме ці команди. Обробники ж не можна підхоплювати автоматично, оскільки вони мають бути визначені у файлі в кореневому каталозі проєкту, а бібліотеки надають доступ лише до підкаталогів. Це дає більше контролю над процесом збирання: ви все одно можете створювати обробники життєвого циклу як звичайні функції у файлах `.lua`, щоб користувачі вашої бібліотеки могли підключати та використовувати їх у своїх `/hooks.editor_script`.

Також зауважте, що хоча залежності показано на панелі Assets, вони не існують як файли (це записи в zip-архіві). Редактор може витягти деякі файли із залежностей до каталогу `build/plugins/`. Для цього створіть файл `ext.manifest` у каталозі своєї бібліотеки, а потім створіть каталог `plugins/bin/${platform}` у тому самому каталозі, де розташований файл `ext.manifest`. Файли з цього каталогу будуть автоматично витягнуті до каталогу `/build/plugins/${extension-path}/plugins/bin/${platform}`, тож ваші скрипти редактора зможуть на них посилатися.

## Налаштування редактора {#preferences}

Скрипти редактора можуть визначати й використовувати налаштування — дані, які постійно зберігаються на комп’ютері користувача й не додаються до комітів. Ці налаштування мають три основні характеристики:
- типізованість: кожне налаштування має визначення схеми, яке містить тип даних та інші метадані, як-от типове значення
- область дії: налаштування мають область дії на рівні проєкту або користувача
- вкладеність: кожен ключ налаштування — це рядок із частинами, розділеними крапками, де перший сегмент шляху визначає скрипт редактора, а решта — групи й окремі налаштування в ньому

Усі налаштування потрібно зареєструвати, визначивши їхню схему:
```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```
Після перезавантаження такого скрипту редактор зареєструє цю схему. Потім скрипт редактора зможе отримувати й установлювати налаштування, наприклад:
```lua
-- Get a specific preference
editor.prefs.get("my_json_formatter.indent.type")
-- Returns: "spaces"

-- Get an entire preference group
editor.prefs.get("my_json_formatter")
-- Returns:
-- {
--   jq_path = "",
--   indent = {
--     size = 2,
--     type = "spaces"
--   }
-- }

-- Set multiple nested preferences at once
editor.prefs.set("my_json_formatter.indent", {
    type = "tabs",
    size = 1
})
```

## Режими виконання {#execution-modes}

Середовище виконання скриптів редактора використовує 2 режими, робота яких здебільшого непомітна для скриптів: **негайний** та **тривалий**.

**Негайний** режим використовується, коли редактору потрібно отримати відповідь від скрипту якнайшвидше. Наприклад, зворотні виклики `active` команд меню виконуються в негайному режимі, оскільки ці перевірки відбуваються в потоці інтерфейсу користувача редактора у відповідь на взаємодію користувача з редактором і мають оновити інтерфейс у межах того самого кадру.

**Тривалий** режим використовується, коли редактору не потрібна миттєва відповідь від скрипту. Наприклад, зворотні виклики `run` команд меню виконуються у **тривалому** режимі, завдяки чому скрипт може витратити більше часу на завершення своєї роботи.

Деякі функції, доступні скриптам редактора, можуть виконуватися довго. Наприклад, `editor.execute("git", "status", {reload_resources=false, out="capture"})` може тривати до секунди в достатньо великих проєктах. Щоб редактор залишався чутливим до дій користувача та продуктивним, функції, які можуть виконуватися довго, заборонено використовувати в контекстах, де редактору потрібна негайна відповідь. Спроба використати таку функцію в негайному контексті призведе до помилки: `Cannot use long-running editor function in immediate context`. Щоб усунути цю помилку, уникайте використання таких функцій у негайних контекстах.

Наведені нижче функції вважаються тривалими й не можуть використовуватися в негайному режимі:
- `editor.create_directory()`, `editor.create_resources()`, `editor.delete_directory()`, `editor.save()`, `os.remove()` та `file:write()`: ці функції змінюють файли на диску, через що редактор синхронізує своє дерево ресурсів у пам’яті зі станом на диску; у великих проєктах це може тривати кілька секунд.
- `editor.execute()`: час виконання команд оболонки може бути непередбачуваним.
- `editor.transact()`: великі транзакції над вузлами, на які посилається багато інших вузлів, можуть тривати сотні мілісекунд, що надто повільно для швидкого реагування інтерфейсу.

Наведені нижче контексти виконання коду використовують негайний режим:
- Зворотні виклики `active` команд меню: редактору потрібна відповідь від скрипту в межах того самого кадру інтерфейсу.
- Верхній рівень скриптів редактора: ми не очікуємо, що перезавантаження скриптів редактора матиме побічні ефекти.

## Дії {#actions}

::: sidenote
Раніше редактор взаємодіяв із віртуальною машиною Lua у блокувальний спосіб, тому скрипти редактора мали суворо дотримуватися вимоги не блокувати виконання, адже деякі взаємодії мають відбуватися з потоку інтерфейсу редактора. Саме тому, наприклад, не було `editor.execute()` та `editor.transact()`. Натомість виконання скриптів і змінення стану редактора запускалися поверненням масиву «дій» з обробників життєвого циклу та обробників `run` команд.

Тепер редактор взаємодіє з віртуальною машиною Lua в неблокувальний спосіб, тому ці дії більше не потрібні: використання функцій на кшталт `editor.execute()` зручніше, лаконічніше й надає більше можливостей. Наразі дії **ЗАСТАРІЛІ**, хоча ми не плануємо їх видаляти.
:::

Скрипти редактора можуть повертати масив дій із функції `run` команди або з функцій-обробників у `/hooks.editor_script`. Потім ці дії виконає редактор.

Дія — це таблиця, яка описує, що має зробити редактор. Кожна дія має ключ `action`. Є 2 види дій: ті, які можна скасувати, і ті, які не можна скасувати.

### Дії, які можна скасувати {#undoable-actions}

::: sidenote
Віддавайте перевагу `editor.transact()`.
:::

Дію з можливістю скасування можна скасувати після її виконання. Якщо команда повертає кілька таких дій, вони виконуються разом і скасовуються разом. За можливості використовуйте дії, які можна скасувати. Їхній недолік — менші можливості.

Наявні дії, які можна скасувати:
- `"set"` — встановити властивість вузла в редакторі в певне значення. Приклад:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  Дія `"set"` потребує таких ключів:
  - `node_id` — ідентифікатор вузла типу userdata. Замість ідентифікатора вузла, отриманого від редактора, тут також можна використати шлях до ресурсу, наприклад `"/main/game.script"`;
  - `property` — властивість вузла, яку потрібно встановити, наприклад `"text"`;
  - `value` — нове значення властивості. Для властивості `"text"` воно має бути рядком.

### Дії, які не можна скасувати {#non-undoable-actions}

::: sidenote
Віддавайте перевагу `editor.execute()`.
:::

Дія без можливості скасування очищує історію скасувань, тому, якщо ви хочете скасувати таку дію, доведеться скористатися іншими засобами, наприклад системою контролю версій.

Наявні дії, які не можна скасувати:
- `"shell"` — виконати скрипт оболонки. Приклад:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- trim leading "/"
    }
  }
  ```
  Дія `"shell"` потребує ключа `command`, який є масивом із командою та її аргументами.

### Поєднання дій і побічних ефектів {#mixing-actions-and-side-effects}

Ви можете поєднувати дії, які можна й не можна скасувати. Дії виконуються послідовно, тому залежно від їхнього порядку ви втратите можливість скасувати частину цієї команди.

Замість повертати дії з функцій, які їх очікують, ви можете просто читати й записувати файли безпосередньо за допомогою `io.open()`. Це спричинить перезавантаження ресурсів, яке очистить історію скасувань.
