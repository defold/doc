---
title: Конвеєр рендерингу в Defold
brief: Цей посібник пояснює, як працює конвеєр рендерингу Defold і як його програмувати.
---

# Рендеринг {#render}

Кожен об’єкт, який рушій показує на екрані, — спрайт, модель, плитку, частинку або вузол GUI — малює рендерер. В основі рендерера лежить скрипт рендерингу, який керує конвеєром рендерингу. За замовчуванням кожен 2D-об’єкт малюється з відповідним растровим зображенням, заданим змішуванням і на правильній глибині Z — тож вам, можливо, ніколи не доведеться думати про рендеринг за межами порядку малювання й простого змішування. Для більшості 2D-ігор стандартний конвеєр працює добре, але ваша гра може мати особливі вимоги. У такому разі Defold дає змогу написати власний конвеєр рендерингу.

### Конвеєр рендерингу — що, коли й де? {#render-pipeline-what-when-and-where}

Конвеєр рендерингу керує тим, що, коли й де рендерити. Що рендерити, визначають [предикати рендерингу](#render-predicates). Коли рендерити предикат, визначається у [скрипті рендерингу](#the-render-script), а де його рендерити — [видом і проєкцією](#default-view-projection). Конвеєр рендерингу також може відсікати графіку, яку малює предикат рендерингу, якщо вона лежить поза заданим обмежувальним паралелепіпедом або об’ємом видимості. Цей процес називається відсіканням за об’ємом видимості (frustum culling).


## Стандартний рендеринг {#the-default-render}

Файл рендерингу містить посилання на поточний скрипт рендерингу, а також власні матеріали, які мають бути доступні в цьому скрипті (для використання з [`render.enable_material()`](/ref/render/#render.enable_material))

В основі конвеєра рендерингу лежить _скрипт рендерингу_. Це скрипт Lua з функціями `init()`, `update()` та `on_message()`, який переважно використовується для взаємодії з базовим графічним API. Скрипт рендерингу посідає особливе місце в життєвому циклі вашої гри. Докладніше про це можна прочитати в [документації про життєвий цикл застосунку](/manuals/application-lifecycle).

У папці "Builtins" вашого проєкту можна знайти стандартний ресурс рендерингу ("default.render") і стандартний скрипт рендерингу ("default.render_script").

![Вбудований рендеринг](images/render/builtin.png)

Щоб налаштувати власний рендерер:

1. Скопіюйте файли "default.render" і "default.render_script" у потрібне місце в ієрархії проєкту. Звісно, ви можете створити скрипт рендерингу з нуля, але варто почати з копії стандартного скрипту, особливо якщо ви лише знайомитеся з Defold та/або програмуванням графіки.

2. Відредагуйте свою копію файлу "default.render" і змініть властивість *Script* так, щоб вона посилалася на вашу копію скрипту рендерингу.

3. Змініть властивість *Render* (у розділі *bootstrap*) у файлі налаштувань *game.project* так, щоб вона посилалася на вашу копію файлу "default.render".


## Предикати рендерингу {#render-predicates}

Щоб керувати порядком малювання об’єктів, створіть _предикати_ рендерингу. Предикат визначає, що слід малювати, на основі вибраних _тегів_ матеріалів.

Кожен об’єкт, який малюється на екрані, має прикріплений матеріал, що керує способом його малювання. У матеріалі ви задаєте один або кілька _тегів_, які мають бути пов’язані з цим матеріалом.

Потім у скрипті рендерингу ви можете створити *предикат рендерингу* й указати, які теги мають до нього належати. Коли ви даєте рушію команду намалювати предикат, буде намальовано кожен об’єкт, матеріал якого містить усі теги, задані для цього предиката.

```
Sprite 1        Sprite 2        Sprite 3        Sprite 4
Material A      Material A      Material B      Material C
  outlined        outlined        greyscale       outlined
  tree            tree            tree            house
```

```lua
-- a predicate matching all sprites with tag "tree"
local trees = render.predicate({"tree"})
-- will draw Sprite 1, 2 and 3
render.draw(trees)

-- a predicate matching all sprites with tag "outlined"
local outlined = render.predicate({"outlined"})
-- will draw Sprite 1, 2 and 4
render.draw(outlined)

-- a predicate matching all sprites with tags "outlined" AND "tree"
local outlined_trees = render.predicate({"outlined", "tree"})
-- will draw Sprite 1 and 2
render.draw(outlined_trees)
```


Докладний опис роботи матеріалів наведено в [документації про матеріали](/manuals/material).


## Стандартний вид і проєкція {#default-view-projection}

Стандартний скрипт рендерингу налаштовано на використання ортографічної проєкції, придатної для 2D-ігор. Він надає три різні ортографічні проєкції: `Stretch` (за замовчуванням), `Fixed Fit` і `Fixed`. Як альтернативу ортографічним проєкціям стандартного скрипту рендерингу ви також можете використовувати матрицю проєкції, яку надає компонент камери (camera component).

### Проєкція з розтягуванням {#stretch-projection}

Проєкція з розтягуванням завжди малює ділянку гри, що відповідає розмірам, заданим у *game.project*, навіть після змінення розміру вікна. Якщо співвідношення сторін зміниться, вміст гри розтягнеться по вертикалі або горизонталі:

![Проєкція з розтягуванням](images/render/stretch_projection.png)

*Проєкція з розтягуванням за початкового розміру вікна*

![Проєкція з розтягуванням після змінення розміру](images/render/stretch_projection_resized.png)

*Проєкція з розтягуванням із розтягнутим по горизонталі вікном*

Проєкція з розтягуванням використовується за замовчуванням, але якщо ви змінили її й хочете повернутися до неї, надішліть повідомлення скрипту рендерингу:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

### Проєкція з вписуванням {#fixed-fit-projection}

Як і проєкція з розтягуванням, проєкція з вписуванням завжди показує ділянку гри, що відповідає розмірам, заданим у *game.project*. Проте якщо розмір вікна та співвідношення сторін зміняться, вміст гри збереже початкове співвідношення сторін, а по вертикалі або горизонталі буде показано додатковий вміст гри:

![Проєкція з вписуванням](images/render/fixed_fit_projection.png)

*Проєкція з вписуванням за початкового розміру вікна*

![Проєкція з вписуванням після змінення розміру](images/render/fixed_fit_projection_resized.png)

*Проєкція з вписуванням із розтягнутим по горизонталі вікном*

![Проєкція з вписуванням після зменшення](images/render/fixed_fit_projection_resized_smaller.png)

*Проєкція з вписуванням із вікном, зменшеним до 50% початкового розміру*

Щоб увімкнути проєкцію з вписуванням, надішліть повідомлення скрипту рендерингу:

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

### Фіксована проєкція {#fixed-projection}

Фіксована проєкція зберігає початкове співвідношення сторін і рендерить вміст гри з фіксованим рівнем наближення. Це означає, що за рівня наближення, відмінного від 100%, вона показуватиме більшу або меншу ділянку гри, ніж визначено розмірами в *game.project*:

![Фіксована проєкція](images/render/fixed_projection_zoom_2_0.png)

*Фіксована проєкція з рівнем наближення 2*

![Фіксована проєкція](images/render/fixed_projection_zoom_0_5.png)

*Фіксована проєкція з рівнем наближення 0.5*

![Фіксована проєкція](images/render/fixed_projection_zoom_2_0_resized.png)

*Фіксована проєкція з рівнем наближення 2 і вікном, зменшеним до 50% початкового розміру*

Щоб увімкнути фіксовану проєкцію, надішліть повідомлення скрипту рендерингу:

```lua
msg.post("@render:", "use_fixed_projection", { near = -1, far = 1, zoom = 2 })
```

### Проєкція камери {#camera-projection}

Якщо ви використовуєте стандартний скрипт рендерингу й у проєкті є ввімкнені [компоненти камери](/manuals/camera), вони матимуть пріоритет над усіма іншими видами та проєкціями, заданими у скрипті рендерингу. Докладніше про роботу з компонентами камери у скриптах рендерингу читайте в [документації про камеру](/manuals/camera).

Ортографічні камери підтримують `Orthographic Mode`, що керує пристосуванням камери до вікна:
- `Fixed` використовує значення `Orthographic Zoom` камери.
- `Auto Fit` (вписування) зберігає всю проєктну ділянку видимою.
- `Auto Cover` (заповнення) заповнює вікно й може обрізати зображення.

Ви можете перемикати режими в редакторі або під час виконання через API камери:

```lua
-- Use auto-fit behavior with an orthographic camera
camera.set_orthographic_mode("main:/go#camera", camera.ORTHO_MODE_AUTO_FIT)
-- Query current mode
local mode = camera.get_orthographic_mode("main:/go#camera")
```

## Відсікання за об’ємом видимості {#frustum-culling}

API рендерингу Defold дає розробникам змогу виконувати так зване відсікання за об’ємом видимості. Коли його ввімкнено, будь-яка графіка поза заданим обмежувальним паралелепіпедом або об’ємом видимості ігнорується. У великому ігровому світі, де одночасно видно лише частину, відсікання за об’ємом видимості може значно зменшити обсяг даних, які потрібно надсилати до GPU для рендерингу, а отже, підвищити продуктивність і заощадити заряд акумулятора (на мобільних пристроях). Для створення обмежувального паралелепіпеда зазвичай використовують вид і проєкцію камери. Стандартний скрипт рендерингу використовує вид і проєкцію (від камери), щоб обчислити об’єм видимості.

Увімкніть відсікання за об’ємом видимості для виклику малювання, передавши матрицю виду-проєкції в параметрі `frustum` до `render.draw()`:

```lua
local frustum = self.proj * self.view
render.draw(predicates.particle, { frustum = frustum })
```

Під час рендерингу з компонентом камери `render.set_camera()` може автоматично використовувати матрицю виду-проєкції камери для подальших викликів малювання:

```lua
render.set_camera("main:/go#camera", { use_frustum = true })
render.draw(predicates.particle)
render.set_camera()
```

За використання будь-якого з цих способів емітери ефектів частинок відсікаються з урахуванням їхніх меж.

Відсікання за об’ємом видимості реалізовано в рушії окремо для кожного типу компонента. Поточний стан:

| Компонент   | Підтримується |
|-------------|-----------|
| Спрайт      | ТАК       |
| Модель      | ТАК       |
| Меш         | ТАК (1)   |
| Напис       | ТАК       |
| Spine       | ТАК       |
| Ефект частинок | ТАК       |
| Карта плиток | ТАК       |
| Rive        | НІ        |

1 = Обмежувальний паралелепіпед меша має задати розробник. [Докладніше](/manuals/mesh/#frustum-culling).


::: sidenote
Починаючи з Defold 1.13.0, примітиви компонентів використовують порядок обходу вершин проти годинникової стрілки, а нормаль примітива спрямована до камери. Спрайти, вузли GUI, карти плиток (сітки плиток) і ефекти частинок використовують той самий порядок обходу, що й інші типи компонентів, тому для всіх компонентів можна застосовувати однакові налаштування відсікання граней.

Це може вплинути на проєкти, які налаштовують відсікання граней для компонентів, відмінних від моделей. Якщо компонент несподівано відсікається, переконайтеся, що викликом `render.set_cull_face(graphics.FACE_TYPE_BACK)` вибрано задні грані, або вилучіть виклик `render.set_cull_face()`, щоб використовувати стандартний режим `graphics.FACE_TYPE_BACK`.
:::

## Системи координат {#coordinate-systems}

Коли йдеться про рендеринг компонентів, зазвичай зазначають, у якій системі координат вони рендеряться. У більшості ігор частина компонентів малюється у світовому просторі, а частина — в екранному.

Компоненти GUI та їхні вузли зазвичай малюються в системі координат екранного простору, де нижній лівий кут екрана має координати (0,0), а верхній правий — (ширина екрана, висота екрана). Камера ніколи не зміщує й не переносить систему координат екранного простору в інший спосіб. Завдяки цьому вузли GUI завжди малюються на екрані незалежно від того, як рендериться світ.

Спрайти, карти плиток та інші компоненти, які використовують ігрові об’єкти (game objects) у вашому ігровому світі, зазвичай малюються в системі координат світового простору. Якщо ви не змінюєте скрипт рендерингу й не використовуєте компонент камери для змінення виду та проєкції, ця система координат збігається із системою координат екранного простору. Проте щойно ви додаєте камеру й переміщуєте її або змінюєте вид і проєкцію, ці дві системи координат починають відрізнятися. Коли камера рухається, нижній лівий кут екрана зміщується відносно (0, 0), щоб рендерилися інші частини світу. Якщо проєкція змінюється, координати одночасно переносяться (тобто зміщуються відносно 0, 0) і змінюються на коефіцієнт масштабу.


## Скрипт рендерингу {#the-render-script}

Нижче наведено код власного скрипту рендерингу, який є дещо зміненою версією вбудованого.

init()
: Функція `init()` використовується для налаштування предикатів, виду й кольору очищення. Ці змінні використовуватимуться безпосередньо під час рендерингу.

```lua
function init(self)
    -- Define the render predicates. Each predicate is drawn by itself and
    -- that allows us to change the state of OpenGL between the draws.
    self.predicates = create_predicates("tile", "gui", "text", "particle", "model")

    -- Create and fill data tables will be used in update()
    local state = create_state()
    self.state = state
    local camera_world = create_camera(state, "camera_world", true)
    init_camera(camera_world, get_stretch_projection)
    local camera_gui = create_camera(state, "camera_gui")
    init_camera(camera_gui, get_gui_projection)
    update_state(state)
end
```

update()
: Функція `update()` викликається один раз на кадр. Вона безпосередньо виконує малювання, викликаючи базові API OpenGL ES (OpenGL Embedded Systems API). Щоб правильно зрозуміти, що відбувається у функції `update()`, потрібно розуміти роботу OpenGL. Існує багато чудових матеріалів про OpenGL ES. Почати варто з офіційного сайту, який розміщено за адресою https://www.khronos.org/opengles/

  Цей приклад містить налаштування, необхідні для малювання 3D-моделей. Функція `init()` визначила предикат `self.predicates.model`. В іншому місці було створено матеріал із тегом "model". Також є кілька компонентів моделей, які використовують цей матеріал:

```lua
function update(self)
    local state = self.state
     if not state.valid then
        if not update_state(state) then
            return
        end
    end

    local predicates = self.predicates
    -- clear screen buffers
    --
    render.set_depth_mask(true)
    render.set_stencil_mask(0xff)
    render.clear(state.clear_buffers)

    local camera_world = state.cameras.camera_world
    render.set_viewport(0, 0, state.window_width, state.window_height)
    render.set_view(camera_world.view)
    render.set_projection(camera_world.proj)


    -- render models
    --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_CULL_FACE)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_depth_mask(true)
    render.draw(predicates.model_pred)
    render.set_depth_mask(false)
    render.disable_state(graphics.STATE_DEPTH_TEST)
    render.disable_state(graphics.STATE_CULL_FACE)

     -- render world (sprites, tilemaps, particles etc)
     --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.enable_state(graphics.STATE_BLEND)
    render.draw(predicates.tile)
    render.draw(predicates.particle)
    render.disable_state(graphics.STATE_STENCIL_TEST)
    render.disable_state(graphics.STATE_DEPTH_TEST)

    -- debug
    render.draw_debug3d()

    -- render GUI
    --
    local camera_gui = state.cameras.camera_gui
    render.set_view(camera_gui.view)
    render.set_projection(camera_gui.proj)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.draw(predicates.gui, camera_gui.frustum)
    render.draw(predicates.text, camera_gui.frustum)
    render.disable_state(graphics.STATE_STENCIL_TEST)
end
```

Поки що це простий і зрозумілий скрипт рендерингу. Він малює однаково в кожному кадрі. Однак інколи корисно додати до скрипту рендерингу стан і виконувати різні операції залежно від нього. Також може знадобитися обмін даними зі скриптом рендерингу з інших частин коду гри.

on_message()
: Скрипт рендерингу може визначати функцію `on_message()` і отримувати повідомлення від інших частин вашої гри або застосунку. Типовий приклад зовнішнього компонента, який надсилає інформацію скрипту рендерингу, — _камера_. Компонент камери, який отримав фокус камери, автоматично надсилатиме свої вид і проєкцію скрипту рендерингу в кожному кадрі. Це повідомлення має назву `"set_view_projection"`:

```lua
local MSG_CLEAR_COLOR =         hash("clear_color")
local MSG_WINDOW_RESIZED =      hash("window_resized")
local MSG_SET_VIEW_PROJ =       hash("set_view_projection")

function on_message(self, message_id, message)
    if message_id == MSG_CLEAR_COLOR then
        -- Someone sent us a new clear color to be used.
        update_clear_color(state, message.color)
    elseif message_id == MSG_SET_VIEW_PROJ then
        -- The camera component that has camera focus will sent set_view_projection
        -- messages to the @render socket. We can use the camera information to
        -- set view (and possibly projection) of the rendering.
        camera.view = message.view
        self.camera_projection = message.projection or vmath.matrix4()
        update_camera(camera, state)
    end
end
```

Проте будь-який скрипт або скрипт GUI може надсилати повідомлення скрипту рендерингу через спеціальний сокет `@render`:

```lua
-- Change the clear color.
msg.post("@render:", "clear_color", { color = vmath.vector4(0.3, 0.4, 0.5, 0) })
```

## Ресурси рендерингу {#render-resources}
Щоб передати певні ресурси рушія до скрипту рендерингу, ви можете додати їх до таблиці `Render Resources` у файлі `.render`, призначеному для проєкту:

![Ресурси рендерингу](images/render/render_resources.png)

Використання цих ресурсів у скрипті рендерингу:

```lua
-- "my_material" will now be used for all draw calls associated with the predicate
render.enable_material("my_material")
-- anything drawn by the predicate will end up in "my_render_target"
render.set_render_target("my_render_target")
render.draw(self.my_full_screen_predicate)
render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.disable_material()

-- bind the render target result texture to whatever is getting rendered via the predicate
render.enable_texture(0, "my_render_target", graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.my_tile_predicate)
```

::: sidenote
Наразі Defold підтримує лише `Materials` і `Render Targets` як ресурси рендерингу за посиланням, але з часом ця система підтримуватиме більше типів ресурсів.
:::

## Дескриптори текстур {#texture-handles}

Усередині Defold текстури представлені дескриптором, який фактично є числом, що має однозначно ідентифікувати об’єкт текстури будь-де в рушії. Це означає, що ви можете поєднати світ ігрових об’єктів зі світом рендерингу, передаючи ці дескриптори між системою рендерингу та скриптом ігрового об’єкта. Наприклад, скрипт, прикріплений до ігрового об’єкта, може створити динамічну текстуру й надіслати її рендереру для використання як глобальної текстури в команді малювання.

У файлі `.script`:

```lua
local my_texture_resource = resource.create_texture("/my_texture.texture", tparams)
-- note: my_texture_resource is a hash to the resource path, which can't be used as a handle!
local my_texture_handle = resource.get_texture_info(my_texture_resource)
-- my_texture_handle contains information about the texture, such as width, height and so on
-- it does also contain the handle, which is what we are after
msg.post("@render:", "set_texture", { handle = my_texture_handle.handle })
```

У файлі `.render_script`:

```lua
function on_message(self, message_id, message)
    if message_id == hash("set_texture") then
        self.my_texture = message.handle
    end
end

function update(self)
    -- bind the custom texture to the draw state
    render.enable_texture(0, self.my_texture)
    -- do drawing..
end
```

::: sidenote
Наразі неможливо змінити, на яку текстуру має вказувати ресурс; використовувати безпосередньо такі дескриптори можна лише у скрипті рендерингу.
:::

## Підтримувані графічні API {#supported-graphics-apis}
API скрипту рендерингу Defold перетворює операції рендерингу на виклики таких графічних API:

:[Графічні API](../shared/graphics-api.md)


## Системні повідомлення {#system-messages}

`"set_view_projection"`
: Це повідомлення надсилають компоненти камери, які отримали фокус камери.

`"window_resized"`
: Рушій надсилає це повідомлення після змінення розміру вікна. Ви можете обробляти це повідомлення, щоб змінювати рендеринг, коли змінюється розмір цільового вікна. На настільних комп’ютерах це означає, що змінився фактичний розмір вікна гри, а на мобільних пристроях це повідомлення надсилається щоразу, коли змінюється орієнтація.

```lua
local MSG_WINDOW_RESIZED =      hash("window_resized")

function on_message(self, message_id, message)
  if message_id == MSG_WINDOW_RESIZED then
    -- The window was resized. message.width and message.height contain the new dimensions.
    ...
  end
end
```

`"draw_line"`
: Намалювати налагоджувальну лінію. Використовуйте для візуалізації `ray_casts`, векторів тощо. Лінії малюються викликом `render.draw_debug3d()`.

```lua
-- draw a white line
local p1 = vmath.vector3(0, 0, 0)
local p2 = vmath.vector3(1000, 1000, 0)
local col = vmath.vector4(1, 1, 1, 1)
msg.post("@render:", "draw_line", { start_point = p1, end_point = p2, color = col } )  
```

`"draw_text"`
: Намалювати налагоджувальний текст. Використовуйте для виведення налагоджувальної інформації. Текст малюється вбудованим шрифтом `always_on_top.font`. Системний шрифт має матеріал із тегом `debug_text` і рендериться разом з іншим текстом у стандартному скрипті рендерингу.

```lua
-- draw a text message
local pos = vmath.vector3(500, 500, 0)
msg.post("@render:", "draw_text", { text = "Hello world!", position = pos })  
```

Візуальний профайлер, доступний через повідомлення `"toggle_profile"`, надіслане до сокета `@system`, не є частиною рендерера, керованого скриптами. Він малюється окремо від вашого скрипту рендерингу.


## Виклики малювання та пакетування {#draw-calls-and-batching}

Виклик малювання (draw call) — це термін, що описує процес налаштування GPU для малювання об’єкта на екрані з використанням текстури й матеріалу та, за потреби, додаткових налаштувань. Цей процес зазвичай потребує значних ресурсів, тому рекомендовано зводити кількість викликів малювання до мінімуму. Ви можете вимірювати кількість викликів малювання та час їх виконання за допомогою [вбудованого профайлера](/manuals/profiling/).

Defold намагатиметься об’єднувати операції рендерингу в пакети, щоб зменшити кількість викликів малювання, за наведеними нижче правилами. Ці правила відрізняються для компонентів GUI та всіх інших типів компонентів.


### Правила пакетування для компонентів поза GUI {#batch-rules-for-non-gui-components}

Кожен виклик `render.draw()` керує сортуванням відповідних елементів, упорядкованих у світовому просторі. За замовчуванням використовується `render.SORT_BACK_TO_FRONT`; для рендерингу від ближнього до дальнього використовуйте `render.SORT_FRONT_TO_BACK`, а щоб зберегти порядок додавання — `render.SORT_NONE`:

```lua
render.draw(self.opaque_predicate, {
    sort_order = render.SORT_FRONT_TO_BACK
})
render.draw(self.transparent_predicate, {
    sort_order = render.SORT_BACK_TO_FRONT
})
```

Вибраний порядок визначає, які елементи є сусідніми, а отже, може впливати на пакетування. У цьому впорядкованому списку кожен об’єкт об’єднується з попереднім у той самий виклик малювання, якщо виконуються такі умови:

* Належить до того самого проксі колекції (collection proxy)
* Має той самий тип компонента (спрайт, ефект частинок, карта плиток тощо)
* Використовує ту саму текстуру (атлас або джерело плиток)
* Має той самий матеріал
* Має ті самі константи шейдера (наприклад, відтінок)

Це означає, що якщо два компоненти спрайтів у тому самому проксі колекції є сусідніми після вибраного сортування й використовують однакові текстуру, матеріал і константи, вони будуть об’єднані в один виклик малювання.


### Правила пакетування для компонентів GUI {#batch-rules-for-gui-components}

Вузли компонента GUI рендеряться згори донизу за списком вузлів. Кожен вузол у списку об’єднується з попереднім у той самий виклик малювання, якщо виконуються такі умови:

* Має той самий тип (прямокутник, текст, сектор тощо)
* Використовує ту саму текстуру (атлас або джерело плиток)
* Має той самий режим змішування.
* Має той самий шрифт (лише для текстових вузлів)
* Має ті самі налаштування трафарету

::: sidenote
Вузли рендеряться окремо для кожного компонента. Це означає, що вузли з різних компонентів GUI не об’єднуватимуться в пакети.
:::

Можливість упорядковувати вузли в ієрархії спрощує їх об’єднання у зручні для керування групи. Проте ієрархії можуть порушити пакетний рендеринг, якщо ви змішуєте різні типи вузлів. За допомогою шарів GUI можна ефективніше об’єднувати вузли GUI в пакети, зберігаючи їхню ієрархію. Докладніше про шари GUI та їхній вплив на виклики малювання читайте в [посібнику з GUI](/manuals/gui#layers-and-draw-calls).
