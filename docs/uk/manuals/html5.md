---
title: Розробка в Defold для платформи HTML5
brief: Цей посібник описує процес створення гри для HTML5, а також відомі проблеми й обмеження.
---

# Розробка для HTML5 {#html5-development}

Defold підтримує збирання ігор для платформи HTML5 через звичайне меню пакування, як і для інших платформ. Крім того, отриману гру вбудовано у звичайну HTML-сторінку, оформлення якої можна змінювати за допомогою простої системи шаблонів.

Файл *game.project* містить налаштування для HTML5:

![Налаштування проєкту](images/html5/html5_project_settings.png)

## Розмір купи пам’яті {#heap-size}

Підтримка HTML5 у Defold ґрунтується на Emscripten (див. http://en.wikipedia.org/wiki/Emscripten). Якщо коротко, він створює ізольовану область пам’яті для купи (heap), у якій працює застосунок. За замовчуванням рушій виділяє значний обсяг пам’яті (256 МБ). Для типової гри цього має бути більш ніж достатньо. Під час оптимізації ви можете вибрати менше значення. Для цього виконайте такі кроки:

1. Установіть бажане значення *heap_size*. Воно має бути виражене в мегабайтах.
2. Створіть пакет HTML5 (див. нижче)

## Тестування збірки HTML5 {#testing-html5-build}

Для тестування збірки HTML5 потрібен HTTP-сервер. Defold створює його, якщо вибрати <kbd>Project ▸ Build HTML5</kbd>.

![Збирання HTML5](images/html5/html5_build_launch.png)

Щоб протестувати пакет, завантажте його на віддалений HTTP-сервер або створіть локальний сервер, наприклад за допомогою Python у папці пакета.
Python 2:

```sh
python -m SimpleHTTPServer
```

Python 3:

```sh
python -m http.server
```

або

```sh
python3 -m http.server
```

::: important
Не можна протестувати пакет HTML5, просто відкривши файл `index.html` у браузері. Для цього потрібен HTTP-сервер.
:::

::: important
Якщо в консолі з’являється помилка `"wasm streaming compile failed: TypeError: Failed to execute ‘compile’ on ‘WebAssembly’: Incorrect response MIME type. Expected ‘application/wasm’."`, переконайтеся, що ваш сервер використовує MIME-тип `application/wasm` для файлів `.wasm`.
:::

## Створення пакета HTML5 {#creating-html5-bundle}

Створювати вміст HTML5 за допомогою Defold просто: процес такий самий, як і для всіх інших підтримуваних платформ. Виберіть у меню <kbd>Project ▸ Bundle... ▸ HTML5 Application...</kbd>:

![Створення пакета HTML5](images/html5/html5_bundle.png)

Пакети HTML5 підтримують дві архітектури WebAssembly:

* `wasm-web` — звичайний рушій WebAssembly без підтримки потоків.
* `wasm_pthread-web` — рушій WebAssembly, який може використовувати потоки.

Можна включити будь-яку з цих архітектур або обидві. Якщо включено обидві, завантажувач вибирає `wasm_pthread-web`, коли браузер і середовище розміщення підтримують її, а в іншому разі використовує `wasm-web`. Канонічні назви цільових платформ наведено в [посібнику з Bob](/manuals/bob/#usage).

::: important
Для рушія з підтримкою потоків потрібен `SharedArrayBuffer` на захищеній сторінці, [ізольованій від інших джерел](https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated). Надавайте пакет через HTTPS (або localhost) і налаштуйте на сервері сумісні заголовки ізоляції між джерелами, зазвичай такі:

```txt
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Ресурси з інших джерел, які завантажує сторінка, також мають використовувати сумісні заголовки CORS або Cross-Origin-Resource-Policy. Пакет, що містить лише `wasm_pthread-web`, не може працювати, якщо ці вимоги не виконано; включіть `wasm-web` як запасний варіант, якщо гру можуть розмістити на сайті, який не підтримує ізоляцію між джерелами.
:::

Пакети Defold HTML5 потребують сучасного браузера з підтримкою WebAssembly. Internet Explorer 11 не підтримується.

Після натискання кнопки <kbd>Create bundle</kbd> вам буде запропоновано вибрати папку, у якій потрібно створити застосунок. Після завершення експорту ви знайдете в ній усі файли, необхідні для запуску застосунку.

## Версія контексту WebGL {#webgl-context-version}

Виберіть запитуваний графічний контекст за допомогою [`graphics.webgl_version_hint`](/manuals/project-settings/#webgl-version-hint). За замовчуванням використовується WebGL 2; запросіть WebGL 1, щоб перевірити цей контекст або використовувати його у браузерах, які підтримують обидві версії.

## Перевірка завантажень {#download-verification}

За замовчуванням завантажувач HTML5 перевіряє розміри завантажених файлів рушія й архівів. Якщо перевірка не проходить, завантаження повторюється, перш ніж завантажувач повідомить про помилку:

* Для мережевих помилок, невдалих статусів HTTP і невідповідностей розміру під час завантаження JavaScript або WebAssembly рушія використовується ліміт повторних спроб із `html5.retry_count`.
* Перевірка файлів архіву має власний ліміт повторних спроб для невідповідностей розміру або SHA-1. Кожна повторна перевірка знову завантажує частини файлу, причому для кожного завантаження доступні звичайні повторні спроби в разі мережевих помилок.

Налаштування `html5.retry_time` керує затримкою між повторними спробами в обох випадках.

Якщо ваш сервер, проксі або CDN навмисно переписує файли, які віддає, і змінює їхні розміри, вимкніть перевірку розміру в *game.project*:

```ini
[html5]
verify_downloaded_file_size = 0
```

Вимкнення **Verify Downloaded File Size** залишає ввімкненою будь-яку перевірку SHA-1, включену до пакета. Див. [налаштування проєкту для HTML5](/manuals/project-settings/#verify-downloaded-file-size).

## Відомі проблеми й обмеження {#known-issues-and-limitations}

* Гаряче перезавантаження (Hot Reload) — гаряче перезавантаження не працює у збірках HTML5. Для отримання оновлень із редактора застосунки Defold мають запускати власний мініатюрний вебсервер, що неможливо у збірці HTML5.
* Chrome
  * Повільні налагоджувальні збірки — у налагоджувальних збірках для HTML5 ми перевіряємо всі графічні виклики WebGL, щоб виявляти помилки. На жаль, під час тестування в Chrome це працює дуже повільно. Перевірку можна вимкнути, установивши в полі *Engine Arguments* файлу *game.project* значення `--verify-graphics-calls=false`.
* Підтримка геймпадів — [зверніться до документації про геймпади](/manuals/input-gamepads/#gamepads-in-html5), щоб дізнатися про особливості й кроки, які можуть знадобитися для HTML5.

## Налаштування пакета HTML5 {#customizing-html5-bundle}

Під час створення HTML5-версії гри Defold надає стандартну вебсторінку. Вона посилається на ресурси стилів і скриптів, які визначають вигляд вашої гри.

Щоразу під час експорту застосунку цей вміст створюється заново. Щоб налаштувати будь-який із цих елементів, потрібно змінити налаштування проєкту. Для цього відкрийте *game.project* у редакторі Defold і прокрутіть до розділу *html5*:

![Розділ HTML5](images/html5/html5_section.png)

Докладнішу інформацію про кожен параметр наведено в [посібнику з налаштувань проєкту](/manuals/project-settings/#html5).

::: important
Не можна змінювати файли стандартного шаблону html/css у папці `builtins`. Щоб застосувати власні зміни, скопіюйте потрібний файл із `builtins` і вкажіть його в *game.project*.
:::

::: important
Не задавайте полотну рамок або внутрішніх відступів у стилях. Інакше координати введення мишею будуть неправильними.
:::

У *game.project* можна вимкнути кнопку `Fullscreen` і посилання `Made with Defold`.
Defold надає темну й світлу теми для `index.html`. За замовчуванням установлено світлу тему, але її можна змінити, змінивши файл `Custom CSS`. Також у полі `Scale Mode` можна вибрати один із чотирьох попередньо визначених режимів масштабування.

::: important
Обчислення для всіх режимів масштабування враховують поточний DPI екрана, якщо ввімкнено параметр `High Dpi` у *game.project* (розділ `Display`)
:::

### Downscale Fit і Fit {#downscale-fit-and-fit}

У режимі `Fit` розмір полотна змінюється так, щоб усе ігрове полотно вміщувалося на екрані зі збереженням початкових пропорцій. Єдина відмінність режиму `Downscale Fit` полягає в тому, що розмір змінюється лише тоді, коли внутрішній розмір вебсторінки менший за початкове полотно гри, але не збільшується, коли вебсторінка більша за нього.

![Розділ HTML5](images/html5/html5_fit.png)

### Stretch {#stretch}

У режимі `Stretch` розмір полотна змінюється так, щоб воно повністю заповнювало внутрішній простір вебсторінки.

![Розділ HTML5](images/html5/html5_stretch.png)

### No Scale {#no-scale}
У режимі `No Scale` розмір полотна точно відповідає значенню, заданому у файлі *game.project*, у розділі `[display]`.

![Розділ HTML5](images/html5/html5_no_scale.png)

## Токени {#tokens}

Для створення файлу `index.html` ми використовуємо [мову шаблонів Mustache](https://mustache.github.io/mustache.5.html). Під час збирання або пакування файли HTML і CSS проходять через компілятор, який може замінювати певні токени значеннями, що залежать від налаштувань проєкту. Ці токени завжди взято у подвійні або потрійні фігурні дужки (`{{TOKEN}}` або `{{{TOKEN}}}`), залежно від того, чи потрібно екранувати послідовності символів. Ця можливість корисна, якщо ви часто змінюєте налаштування проєкту або плануєте повторно використовувати матеріал в інших проєктах.

::: sidenote
Докладнішу інформацію про мову шаблонів Mustache наведено в [посібнику](https://mustache.github.io/mustache.5.html).
:::

Будь-який параметр *game.project* може бути токеном. Наприклад, якщо ви хочете використати значення `Width` із розділу `Display`:

![Розділ Display](images/html5/html5_display.png)

Відкрийте *game.project* як текст і перевірте `[section_name]` та назву поля, яке хочете використати. Потім його можна використати як токен: `{{section_name.field}}` або `{{{section_name.field}}}`.

![Розділ Display](images/html5/html5_game_project.png)

Наприклад, у JavaScript в HTML-шаблоні:

```javascript
function doSomething() {
    var x = {{display.width}};
    // ...
}
```

Також доступні такі спеціальні токени:

DEFOLD_SPLASH_IMAGE
: Записує ім’я файлу зображення заставки або `false`, якщо `html5.splash_image` у *game.project* порожнє


```css
{{#DEFOLD_SPLASH_IMAGE}}
		background-image: url("{{DEFOLD_SPLASH_IMAGE}}");
{{/DEFOLD_SPLASH_IMAGE}}
```

exe-name
: Назва проєкту без неприпустимих символів

DEFOLD_ARCHIVE_LOCATION_PREFIX
: Обчислений префікс шляху архіву, який використовує завантажувач, на основі `html5.archive_location_prefix`.

DEFOLD_ARCHIVE_LOCATION_SUFFIX
: Обчислений суфікс, що додається до URL-адрес архівів, на основі `html5.archive_location_suffix`.

DEFOLD_HAS_ARCHIVE_ORIGIN
: `true`, якщо префікс архіву задає джерело HTTP або HTTPS, включно з URL-адресою без явного протоколу, як-от `//cdn.example.com/archive`. Для відносних префіксів архіву дорівнює `false`. Доступно починаючи з Defold 1.13.2.

DEFOLD_ARCHIVE_ORIGIN
: Джерело архіву, включно зі схемою, хостом і необов’язковим портом, або порожній рядок, якщо джерело не вказано. Префікс без явного протоколу утворює джерело без явного протоколу. Використовується для підказки preconnect і доступний починаючи з Defold 1.13.2.

DEFOLD_HAS_WASM_ENGINE
: `true`, якщо пакет містить рушій WebAssembly: `wasm-web` або `wasm_pthread-web`.

DEFOLD_HAS_WASM_PTHREAD_ENGINE
: `true`, якщо пакет містить `wasm_pthread-web`. Використовуйте це значення, щоб уникнути попереднього завантаження неправильного варіанта рушія, коли завантажувач вибирає архітектуру під час виконання.


DEFOLD_CUSTOM_CSS_INLINE
: Місце, куди вбудовується вміст CSS-файлу, зазначеного в налаштуваннях *game.project*.


```html
<style>
{{{DEFOLD_CUSTOM_CSS_INLINE}}}
</style>
```

::: important
Цей вбудований блок має з’являтися до завантаження основного скрипту застосунку. Оскільки він містить теги HTML, цей макрос слід брати в потрійні дужки `{{{TOKEN}}}`, щоб запобігти екрануванню послідовностей символів.
:::

DEFOLD_SCALE_MODE_IS_DOWNSCALE_FIT
: Цей токен має значення `true`, якщо `html5.scale_mode` дорівнює `Downscale Fit`.

DEFOLD_SCALE_MODE_IS_FIT
: Цей токен має значення `true`, якщо `html5.scale_mode` дорівнює `Fit`.

DEFOLD_SCALE_MODE_IS_NO_SCALE
: Цей токен має значення `true`, якщо `html5.scale_mode` дорівнює `No Scale`.

DEFOLD_SCALE_MODE_IS_STRETCH
: Цей токен має значення `true`, якщо `html5.scale_mode` дорівнює `Stretch`.

DEFOLD_HEAP_SIZE
: Розмір купи пам’яті, зазначений у `html5.heap_size` файлу *game.project*, перетворений у байти.

DEFOLD_ENGINE_ARGUMENTS
: Аргументи рушія, зазначені в `html5.engine_arguments` файлу *game.project* і розділені символом `,`.

build-timestamp
: Часова мітка поточного збирання в секундах.


## Додаткові параметри {#extra-parameters}

Якщо ви створюєте власний шаблон, можна змінювати параметри завантажувача рушія, призначаючи значення в глобальному об’єкті `CUSTOM_PARAMETERS`. Вбудований шаблон містить навмисно порожній блок `<script id="engine-setup">` для цих налаштувань.
::: important
Розміщуйте блок `engine-setup` після скрипту, який завантажує `dmloader.js`, і перед блоком `engine-start`, який викликає `EngineLoader.load()`.
:::
Наприклад:

```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.disable_context_menu = false;
        CUSTOM_PARAMETERS.unsupported_webgl_callback = function() {
            console.log("Oh-oh. WebGL not supported...");
        };
    </script>
```

`CUSTOM_PARAMETERS` може містити, зокрема, такі поля:

```
'archive_location_filter':
    Filter function that will run for each archive path.

'unsupported_webgl_callback':
    Function that is called if WebGL is not supported.

'engine_arguments':
    List of arguments (strings) that will be passed to the engine.

'custom_heap_size':
    Number of bytes specifying the memory heap size.

'disable_context_menu':
    Disables the right-click context menu on the canvas element if true.

'retry_time':
    Pause in seconds before retry file loading after error.

'retry_count':
    How many attempts we do when trying to download a file.

'can_not_download_file_callback':
    Function that is called if you can't download file after 'retry_count' attempts.

'resize_window_callback':
    Function that is called when resize/orientationchanges/focus events happened

'start_success':
    Function that is called just before main is called upon successful load.

'update_progress':
    Function that is called as progress is updated. Parameter progress is updated 0-100.
```

## Файлові операції в HTML5 {#file-operations-in-html5}

Збірки HTML5 підтримують файлові операції, як-от `sys.save()`, `sys.load()` та `io.open()`, але внутрішня обробка цих операцій відрізняється від інших платформ. Під час виконання JavaScript у браузері немає повноцінного поняття файлової системи, а доступ до локальних файлів заблоковано з міркувань безпеки. Натомість Emscripten (а отже, і Defold) використовує [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB), базу даних у браузері для постійного зберігання даних, щоб створити віртуальну файлову систему в браузері. Важлива відмінність від доступу до файлової системи на інших платформах полягає в тому, що між записом у файл і фактичним збереженням зміни в базі даних може бути невелика затримка. Консоль розробника браузера зазвичай дає змогу переглядати вміст IndexedDB.


## Передавання аргументів у гру HTML5 {#passing-arguments-to-an-html5-game}

Іноді потрібно передати грі додаткові аргументи до запуску або під час нього. Це може бути, наприклад, ідентифікатор користувача, токен сеансу або рівень, який потрібно завантажити під час запуску гри. Це можна зробити кількома різними способами, деякі з яких описано тут.

### Аргументи рушія {#engine-arguments}

Під час налаштування й завантаження рушія можна вказати додаткові аргументи рушія. Їх можна отримати під час виконання за допомогою `sys.get_config_string()`. Призначте аргументи безпосередньо в `CUSTOM_PARAMETERS.engine_arguments` у блоці `engine-setup` файлу `index.html`:


```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.engine_arguments = [
            "--config=example.foo1=bar1",
            "--config=example.foo2=bar2"
        ];
    </script>
```

Призначення нового масиву замінює всі аргументи рушія, налаштовані в *game.project*. Щоб зберегти ці аргументи й додати ще один, натомість використовуйте `CUSTOM_PARAMETERS.engine_arguments.push("--config=example.foo3=bar3")`.

Також можна додати `--config=example.foo1=bar1, --config=example.foo2=bar2` у поле *Engine Arguments* розділу HTML5 у *game.project*. Значення, розділені комами, додаються до `CUSTOM_PARAMETERS.engine_arguments` у згенерованому файлі `dmloader.js`.

Під час виконання значення можна отримати так:

```lua
local foo1 = sys.get_config_string("example.foo1")
local foo2 = sys.get_config_string("example.foo2")
print(foo1) -- bar1
print(foo2) -- bar2
```


### Аргументи запиту в URL {#query-arguments-in-the-url}

Ви можете передавати аргументи як параметри запиту в URL сторінки й читати їх під час виконання:

```
https://www.mygame.com/index.html?foo1=bar1&foo2=bar2
```

```lua
local url = html5.run("window.location")
print(url)
```

Повна допоміжна функція для отримання всіх параметрів запиту у вигляді таблиці Lua:

```lua
local function get_query_parameters()
    local url = html5.run("window.location")
    -- get the query part of the url (the bit after ?)
    local query = url:match(".*?(.*)")
    if not query then
        return {}
    end

    local params = {}
    -- iterate over all key value pairs
    for kvp in query:gmatch("([^&]+)") do
        local key, value = kvp:match("(.+)=(.+)")
        params[key] = value
    end
    return params
end

function init(self)
    local params = get_query_parameters()
    print(params.foo1) -- bar1
end
```

## Оптимізація {#optimizations}
Ігри HTML5 зазвичай мають суворі вимоги до початкового обсягу завантаження, часу запуску й використання пам’яті, щоб вони швидко завантажувалися та добре працювали на малопотужних пристроях і за повільного інтернет-з’єднання. Щоб оптимізувати гру HTML5, рекомендовано зосередитися на таких напрямах:

* [Використання пам’яті](/manuals/optimization-memory)
* [Розмір рушія](/manuals/optimization-size)
* [Розмір гри](/manuals/optimization-size)

## Поширені запитання {#faq}
:[Поширені запитання про HTML5](../shared/html5-faq.md)
