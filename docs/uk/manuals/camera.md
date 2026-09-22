---
title: Посібник із компонента камери
brief: Цей посібник описує функціональність компонента камери в Defold.
---

# Камери {#cameras}

Камера в Defold — це компонент (component), який змінює область перегляду та проєкцію ігрового світу. Компонент камери визначає базову перспективну або ортографічну камеру, яка надає скрипту рендерингу матрицю виду та матрицю проєкції.

Перспективну камеру зазвичай використовують у 3D-іграх, де вид із камери, розмір і перспектива об’єктів залежать від зрізаної піраміди видимості (view frustum), а також від відстані й кута огляду від камери до об’єктів у грі.

У 2D-іграх часто бажано рендерити сцену з ортографічною проєкцією. Це означає, що вид із камери визначає вже не зрізана піраміда видимості, а паралелепіпед. Ортографічна проєкція нереалістична, оскільки не змінює розмір об’єктів залежно від відстані до них. Об’єкт на відстані 1000 одиниць буде відображено в тому самому розмірі, що й об’єкт безпосередньо перед камерою.

![проєкції](images/camera/projections.png)


## Створення камери {#creating-a-camera}

Щоб створити камеру, <kbd>клацніть правою кнопкою миші</kbd> ігровий об’єкт (game object) і виберіть <kbd>Add Component ▸ Camera</kbd>. Також можна створити файл компонента в ієрархії проєкту й додати цей файл до ігрового об’єкта.

![створення компонента камери](images/camera/create.png)

Компонент камери має наведені нижче властивості, які визначають її *зрізану піраміду видимості*:

![налаштування камери](images/camera/settings.png)

Id
: Ідентифікатор компонента

Aspect Ratio
: (**Лише для перспективної камери**) — Співвідношення ширини та висоти зрізаної піраміди видимості. Значення 1.0 означає квадратну область перегляду. Значення 1.33 підходить для області перегляду зі співвідношенням сторін 4:3, наприклад 1024x768. Значення 1.78 підходить для співвідношення 16:9. Це налаштування ігнорується, якщо ввімкнено *Auto Aspect Ratio*.

Fov
: (**Лише для перспективної камери**) — *Вертикальне* поле зору камери, виражене в _радіанах_. Що ширше поле зору, то більше камера бачитиме.

Near Z
: Значення Z ближньої площини відсікання.

Far Z
: Значення Z дальньої площини відсікання.

Auto Aspect Ratio
: (**Лише для перспективної камери**) — Увімкніть, щоб камера автоматично обчислювала співвідношення сторін.

Orthographic Projection
: Увімкніть, щоб перемкнути камеру на ортографічну проєкцію (див. нижче).

Orthographic Zoom
: (**Лише для ортографічної камери**) — Керований користувачем множник масштабу (> 1 = наближення, < 1 = віддалення). У режимі `Fixed` це підсумковий масштаб. У режимах `Auto Fit` і `Auto Cover` він множиться на автоматично обчислений масштаб, що дає змогу додати наближення, не вимикаючи автоматичного підлаштування розміру.

Orthographic Mode
: (**Лише для ортографічної камери**) — Визначає, як ортографічна камера обчислює масштаб відносно розміру вікна та базової роздільності (значень у `game.project` → `display.width/height`).
  - `Fixed` (використовує сталий масштаб): Використовує поточне значення `Orthographic Zoom` без змін.
  - `Auto Fit` (вміщення): Автоматично обчислює масштаб так, щоб уся базова область уміщувалася у вікні, а потім множить його на `Orthographic Zoom`. Може показувати додатковий вміст із боків або зверху й знизу.
  - `Auto Cover` (покриття): Автоматично обчислює масштаб так, щоб базова область покривала все вікно, а потім множить його на `Orthographic Zoom`. Може обрізати вміст із боків або зверху й знизу.
  Доступно лише тоді, коли ввімкнено `Orthographic Projection`.


## Використання камери {#using-the-camera}

Усі камери автоматично вмикаються й оновлюються протягом кадру, а модуль Lua `camera` доступний у всіх контекстах скриптів. Починаючи з Defold 1.8.1, більше не потрібно явно вмикати камеру, надсилаючи її компоненту повідомлення `acquire_camera_focus`. Старі повідомлення отримання та звільнення фокуса досі доступні, але рекомендовано натомість використовувати повідомлення `enable` і `disable`, як і для будь-якого іншого компонента, який потрібно ввімкнути або вимкнути:

```lua
msg.post("#camera", "disable")
msg.post("#camera", "enable")
```

Щоб отримати список усіх наразі доступних камер, використовуйте `camera.get_cameras()`:

```lua
-- Note: The render calls are only available in a render script.
--       The camera.get_cameras() function can be used anywhere,
--       but render.set_camera can only be used in a render script.

for k,v in pairs(camera.get_cameras()) do
    -- the camera table contains the URLs of all cameras
    render.set_camera(v)
    -- do rendering here - anything rendered here that uses materials with
    -- view and projection matrices specified, will use matrices from the camera.
end
-- to disable a camera, pass in nil (or no arguments at all) to render.set_camera.
-- after this call, all render calls will use the view and projection matrices
-- that are specified on the render context (render.set_view and render.set_projection)
render.set_camera()
```

Модуль `camera` для скриптів містить кілька функцій для керування камерою. Нижче наведено лише деякі з них; усі доступні функції описано в [документації API](/ref/camera/)).

```lua
camera.get_aspect_ratio(camera) -- get aspect ratio
camera.get_far_z(camera) -- get far z
camera.get_fov(camera) -- get field of view
camera.get_orthographic_mode(camera) -- get orthographic mode (one of camera.ORTHO_MODE_*)
camera.get_orthographic_zoom(camera) -- get the user-controlled zoom multiplier
camera.get_orthographic_auto_zoom(camera) -- get the automatically calculated zoom
camera.set_aspect_ratio(camera, ratio) -- set aspect ratio
camera.set_far_z(camera, far_z) -- set far z
camera.set_near_z(camera, near_z) -- set near z
camera.set_orthographic_mode(camera, camera.ORTHO_MODE_AUTO_FIT) -- set orthographic mode
... And so forth
```

Камеру ідентифікує URL, який є повним шляхом компонента у сцені й містить колекцію (collection), ігровий об’єкт, якому він належить, та ідентифікатор компонента. У цьому прикладі використовуйте URL `/go#camera`, щоб звернутися до компонента камери з тієї самої колекції, і `main:/go#camera`, коли звертаєтеся до камери з іншої колекції або зі скрипту рендерингу.

![створення компонента камери](images/camera/create.png)

```lua
-- Accessing a camera from a script in the same collection:
camera.get_fov("/go#camera")

-- Accessing a camera from a script in a different collection:
camera.get_fov("main:/go#camera")

-- Accessing a camera from the render script:
render.set_camera("main:/go#camera")
```

Кожного кадру компонент камери, який наразі має фокус камери, надсилає повідомлення `set_view_projection` до сокета `@render`:

```lua
-- builtins/render/default.render_script
--
function on_message(self, message_id, message)
    if message_id == hash("set_view_projection") then
        self.view = message.view                    -- [1]
        self.projection = message.projection
    end
end
```
1. Повідомлення, надіслане компонентом камери, містить матрицю виду та матрицю проєкції.

Компонент камери надає скрипту рендерингу матрицю перспективної або ортографічної проєкції залежно від властивості камери *Orthographic Projection*. Матриця проєкції також враховує задані ближню й дальню площини відсікання, поле зору та налаштування співвідношення сторін камери.

Матриця виду, яку надає камера, визначає її позицію та орієнтацію. Камера з *Orthographic Projection* розташовує центр області перегляду в позиції ігрового об’єкта, до якого її прикріплено, тоді як камера з *Perspective Projection* розташовує в цій позиції нижній лівий кут області перегляду.


### Скрипт рендерингу {#render-script}

Якщо використовується стандартний скрипт рендерингу, Defold автоматично вибирає для рендерингу останню ввімкнену камеру. До цієї зміни один зі скриптів проєкту мав явно надсилати рендереру повідомлення `use_camera_projection`, щоб указати, що слід використовувати вид і проєкцію з компонентів камер. Тепер це не потрібно, але така можливість зберігається для зворотної сумісності.

Також у скрипті рендерингу можна вказати конкретну камеру, яку слід використовувати для рендерингу. Це може знадобитися, коли потрібно точніше контролювати вибір камери для рендерингу, наприклад у багатокористувацькій грі.

```lua
-- render.set_camera will automatically use the view and projection matrices
-- for any rendering happening until render.set_camera() is called.
render.set_camera("main:/my_go#camera")
```

Щоб перевірити, чи активна камера, використовуйте функцію `get_enabled` з [API камери](https://defold.com/ref/alpha/camera/#camera.get_enabled:camera):

```lua
if camera.get_enabled("main:/my_go#camera") then
    -- camera is enabled, use it for rendering!
    render.set_camera("main:/my_go#camera")
end
```

::: sidenote
Щоб використовувати функцію `set_camera` разом із відсіканням за пірамідою видимості, передайте їй відповідний параметр:
`render.set_camera("main:/my_go#camera", {use_frustum = true})`
:::

### Панорамування камери {#panning-the-camera}

Щоб панорамувати або переміщувати камеру ігровим світом, переміщуйте ігровий об’єкт, до якого прикріплено компонент камери. Компонент камери автоматично надсилатиме оновлену матрицю виду на основі поточної позиції камери вздовж осей x та y.

### Масштабування камери {#zooming-the-camera}

Щоб наближати й віддаляти зображення під час використання перспективної камери, переміщуйте ігровий об’єкт, до якого її прикріплено, вздовж осі z. Компонент камери автоматично надсилатиме оновлену матрицю виду на основі поточної позиції камери вздовж осі z.

Щоб наближати й віддаляти зображення під час використання ортографічної камери, змінюйте її властивість *Orthographic Zoom* у редакторі або під час виконання:

```lua
-- In Fixed mode, this is the effective zoom.
go.set("#camera", "orthographic_zoom", 2)
```

У режимах `Auto Fit` і `Auto Cover` властивість *Orthographic Zoom* застосовується додатково до автоматично обчисленого масштабу, а не ігнорується. Наприклад, установіть у редакторі *Orthographic Mode* у `Auto Fit`, а *Orthographic Zoom* у `1.25`, щоб умістити базову область у вікні, а потім додатково наблизити її на 25%. Еквівалентне налаштування під час виконання:

```lua
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)
go.set("#camera", "orthographic_zoom", 1.25)

local auto_zoom = camera.get_orthographic_auto_zoom("#camera")
local zoom_multiplier = camera.get_orthographic_zoom("#camera")
local effective_zoom = auto_zoom * zoom_multiplier
```

`camera.get_orthographic_auto_zoom()` повертає масштаб, обчислений на основі поточного розміру вікна та розмірів, заданих у проєкті, у режимах `Auto Fit` і `Auto Cover`. У режимі `Fixed` функція повертає `1.0`. Те саме значення доступне через властивість компонента `orthographic_auto_zoom`, призначену лише для читання:

```lua
local auto_zoom = go.get("#camera", "orthographic_auto_zoom")
```

Під час використання ортографічної камери також можна змінювати спосіб визначення масштабу за допомогою налаштування `Orthographic Mode` або зі скрипту:

```lua
-- get current mode (one of camera.ORTHO_MODE_FIXED, _AUTO_FIT, _AUTO_COVER)
local mode = camera.get_orthographic_mode("#camera")

-- switch to auto-fit (contain) to always keep the full design area visible
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)

-- switch to auto-cover to ensure the design area covers the window
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_COVER)

-- switch to fixed mode to use orthographic_zoom without automatic sizing
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_FIXED)
```

### Адаптивне масштабування {#adaptive-zoom}

Ідея адаптивного масштабування полягає в підлаштуванні значення масштабу камери, коли роздільність дисплея змінюється відносно початкової роздільності, заданої в *game.project*.

Два поширені підходи до адаптивного масштабування:

1. Максимальний масштаб — обчислити таке значення масштабу, щоб вміст, охоплений початковою роздільністю в *game.project*, заповнював екран і виходив за його межі, можливо приховуючи частину вмісту з боків або зверху й знизу.
2. Мінімальний масштаб — обчислити таке значення масштабу, щоб вміст, охоплений початковою роздільністю в *game.project*, повністю вміщувався в межах екрана, можливо показуючи додатковий вміст із боків або зверху й знизу.

Приклад:

```lua
local DISPLAY_WIDTH = sys.get_config_int("display.width")
local DISPLAY_HEIGHT = sys.get_config_int("display.height")

function init(self)
    local initial_zoom = go.get("#camera", "orthographic_zoom")
    local display_scale = window.get_display_scale()
    window.set_listener(function(self, event, data)
        if event == window.WINDOW_EVENT_RESIZED then
            local window_width = data.width
            local window_height = data.height
            local design_width = DISPLAY_WIDTH / initial_zoom
            local design_height = DISPLAY_HEIGHT / initial_zoom

            -- max zoom: ensure that the initial design dimensions will fill and expand beyond the screen bounds
            local zoom = math.max(window_width / design_width, window_height / design_height) / display_scale

            -- min zoom: ensure that the initial design dimensions will shrink and be contained within the screen bounds
            --local zoom = math.min(window_width / design_width, window_height / design_height) / display_scale
            
            go.set("#camera", "orthographic_zoom", zoom)
        end
    end)
end
```

Повний приклад адаптивного масштабування наведено в [цьому прикладі проєкту](https://github.com/defold/sample-adaptive-zoom).

Примітка: з ортографічною камерою тепер можна отримати вміщення або покриття без власного коду, установивши `Orthographic Mode` у `Auto Fit` (вміщення) або `Auto Cover` (покриття). У цих режимах масштаб, обчислений на основі розміру вікна та базової роздільності, множиться на `Orthographic Zoom`.


### Слідування за ігровим об’єктом {#following-a-game-object}

Щоб камера слідувала за ігровим об’єктом, зробіть ігровий об’єкт, до якого прикріплено компонент камери, дочірнім об’єктом того, за яким потрібно слідувати:

![слідування за ігровим об’єктом](images/camera/follow.png)

Інший спосіб — кожного кадру оновлювати позицію ігрового об’єкта, до якого прикріплено компонент камери, відповідно до руху об’єкта, за яким потрібно слідувати.

### Перетворення між екранними та світовими координатами {#converting-mouse-to-world-coordinates}

Після панорамування, масштабування або зміни проєкції камери координати введення вже не відповідають світовим координатам безпосередньо. Використовуйте функції перетворення камери з `action.screen_x` і `action.screen_y`. Якщо необов’язковий URL камери не вказано, використовується остання ввімкнена камера.

Для ортографічної камери [`camera.screen_xy_to_world()`](/ref/camera/#camera.screen_xy_to_world:x-y-[camera]) повертає точку у світовому просторі на ближній площині камери, яка відповідає пікселю екрана:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local world_position = camera.screen_xy_to_world(
            action.screen_x, action.screen_y, "#camera")
        go.set_position(world_position, "/marker")
    end
end
```

Для перспективної камери [`camera.screen_to_world()`](/ref/camera/#camera.screen_to_world:pos-[camera]) приймає `vector3`, у якому компонент Z задає глибину огляду в одиницях світового простору, відлічену від площини камери:

```lua
local depth = 10
local world_position = camera.screen_to_world(
    vmath.vector3(action.screen_x, action.screen_y, depth), "#camera")
```

[`camera.world_to_screen()`](/ref/camera/#camera.world_to_screen:world_pos-[camera]) виконує зворотне перетворення. Функція повертає X і Y у пікселях екрана, а Z містить глибину огляду за тим самим правилом, тому її результат можна передати назад у `camera.screen_to_world()`:

```lua
-- Update the cached world transform first if the object moved this frame.
go.update_world_transform("/marker")
local world_position = go.get_world_position("/marker")
local screen_position = camera.world_to_screen(world_position, "#camera")
```

Перегляньте [сторінку прикладів](https://defold.com/examples/render/screen_to_world/), щоб побачити перетворення координат у дії. Також є [приклад проєкту](https://github.com/defold/sample-screen-to-world-coordinates/), який демонструє ті самі API.

::: sidenote
[Сторонні рішення для камер, згадані в цьому посібнику](/manuals/camera/#third-party-camera-solutions), надають функції перетворення в екранні координати й навпаки.
:::

## Керування під час виконання {#runtime-manipulation}
Камерами можна керувати під час виконання за допомогою різних повідомлень і властивостей (див. [документацію API щодо використання](/ref/camera/)).

Камера має низку властивостей, які можна читати й змінювати за допомогою `go.get()` і `go.set()`:

`fov`
: Поле зору камери (`number`).

`near_z`
: Ближнє значення Z камери (`number`).

`far_z`
: Дальнє значення Z камери (`number`).

`orthographic_zoom`
: Керований користувачем множник масштабу ортографічної камери. У режимах `Auto Fit` і `Auto Cover` він множиться на `orthographic_auto_zoom`. (`number`).

`orthographic_auto_zoom`
: Обчислений ортографічний масштаб для режимів `Auto Fit` і `Auto Cover` або `1.0` у режимі `Fixed`. ЛИШЕ ДЛЯ ЧИТАННЯ. (`number`).

`aspect_ratio`
: Співвідношення ширини та висоти зрізаної піраміди видимості. Використовується під час обчислення проєкції перспективної камери. (`number`).

`view`
: Обчислена матриця виду камери. ЛИШЕ ДЛЯ ЧИТАННЯ. (`matrix4`).

`projection`
: Обчислена матриця проєкції камери. ЛИШЕ ДЛЯ ЧИТАННЯ. (`matrix4`).


## Сторонні рішення для камер {#third-party-camera-solutions}

Спільнота створила рішення для камер, які реалізують поширені можливості, зокрема тремтіння екрана, слідування за ігровими об’єктами, перетворення екранних координат у світові та багато іншого. Їх можна завантажити з порталу ресурсів Defold:

- [Ортографічна камера](https://defold.com/assets/orthographic/) (лише 2D), автор — Björn Ritzl.
- [Defold Rendy](https://defold.com/assets/defold-rendy/) (2D і 3D), автор — Klayton Kowalski.
