---
title: Посібник з обчислювальних програм у Defold
brief: Цей посібник пояснює, як працювати з обчислювальними програмами, константами шейдерів і семплерами.
---

# Обчислювальні програми {#compute-programs}

::: sidenote
Підтримка обчислювальних шейдерів у Defold наразі перебуває на етапі *попередньої технічної версії*.
Це означає, що деякі можливості ще відсутні, а API може змінитися в майбутньому.
:::

Обчислювальні шейдери (compute shaders) — потужний інструмент для виконання обчислень загального призначення на GPU. Вони дають змогу використовувати можливості паралельного оброблення даних на GPU для таких завдань, як фізичні симуляції, оброблення зображень тощо. Обчислювальний шейдер працює з даними, що зберігаються в буферах або текстурах, паралельно виконуючи операції в багатьох потоках GPU. Саме цей паралелізм робить обчислювальні шейдери настільки ефективними для інтенсивних обчислень.

* Докладніше про конвеєр рендерингу див. у [документації з рендерингу](/manuals/render).
* Докладне пояснення шейдерних програм див. у [документації з шейдерів](/manuals/shader).

## Що можна робити за допомогою обчислювальних шейдерів? {#what-can-i-do-with-compute-shaders}

Оскільки обчислювальні шейдери призначені для обчислень загального призначення, їхні можливості практично необмежені. Ось кілька прикладів типового використання обчислювальних шейдерів:

Оброблення зображень
  - Фільтрування зображень: застосування розмиття, виявлення контурів, фільтра підвищення різкості тощо.
  - Корекція кольору: налаштування колірного простору зображення.

Фізика
  - Системи частинок: симуляція великої кількості частинок для таких ефектів, як дим, вогонь і динаміка рідин.
  - Фізика м’яких тіл: симуляція об’єктів, що деформуються, як-от тканина та желе.
  - Відсікання: відсікання закритих об’єктів, відсікання за пірамідою видимості.

Процедурне генерування
  - Генерування ландшафту: створення деталізованого ландшафту за допомогою функцій шуму.
  - Рослинність і листя: процедурне генерування рослин і дерев.

Ефекти рендерингу
  - Глобальне освітлення: симуляція реалістичного освітлення шляхом наближеного відтворення відбиттів світла в сцені.
  - Вокселізація: створення тривимірної воксельної сітки з даних меша.

## Як працюють обчислювальні шейдери? {#how-does-compute-shaders-work}

Загалом обчислювальні шейдери працюють, розділяючи завдання на багато менших завдань, які можна виконувати одночасно. Для цього використовуються поняття `робочих груп` (work groups) і `викликів` (invocations):

Робочі групи
: Обчислювальний шейдер працює на сітці `робочих груп`. Кожна робоча група містить фіксовану кількість викликів (або потоків). Розмір робочих груп і кількість викликів визначаються в коді шейдера.

Виклики
: Кожен виклик (або потік) виконує програму обчислювального шейдера. Виклики в межах робочої групи можуть обмінюватися даними через спільну пам’ять, що забезпечує ефективну взаємодію та синхронізацію між ними.

GPU виконує обчислювальний шейдер, паралельно запускаючи багато викликів у кількох робочих групах, що забезпечує значну обчислювальну потужність для відповідних завдань.

## Створення обчислювальної програми {#creating-a-compute-program}

Щоб створити обчислювальну програму, <kbd>клацніть правою кнопкою миші</kbd> цільову папку в браузері *Assets* і виберіть <kbd>New... ▸ Compute</kbd>. (Також можна вибрати <kbd>File ▸ New...</kbd> у меню, а потім вибрати <kbd>Compute</kbd>). Задайте назву нового файлу обчислювальної програми й натисніть <kbd>Ok</kbd>.

![Файл обчислювальної програми](images/compute/compute_file.png)

Нова обчислювальна програма відкриється в редакторі *Compute Editor*.

![Редактор обчислювальних програм](images/compute/compute.png)

Файл обчислювальної програми містить таку інформацію:

Compute Program
: Файл програми обчислювального шейдера (*`.cp`*), який слід використовувати. Шейдер працює з «абстрактними робочими елементами», тобто типи вхідних і вихідних даних не визначені наперед. Програміст сам визначає, що має створювати обчислювальний шейдер.

Constants
: Уніформ-змінні, які будуть передані програмі обчислювального шейдера. Список доступних констант див. нижче.

Samplers
: За потреби у файлі матеріалу можна налаштувати окремі семплери. Додайте семплер, назвіть його відповідно до імені, використаного в шейдерній програмі, і задайте потрібні налаштування обгортання та фільтрування.


## Використання обчислювальної програми в Defold {#using-the-compute-program-in-defold}

На відміну від матеріалів, обчислювальні програми не призначаються компонентам (components) і не є частиною звичайного процесу рендерингу. Щоб обчислювальна програма виконала роботу, її потрібно `запустити` (dispatch) у скрипті рендерингу. Однак перед запуском потрібно переконатися, що скрипт рендерингу має посилання на обчислювальну програму. Наразі єдиний спосіб зробити обчислювальну програму доступною скрипту рендерингу — додати її до файлу .render, який містить посилання на ваш скрипт рендерингу:

![Файл рендерингу з обчислювальною програмою](images/compute/compute_render_file.png)

Щоб використовувати обчислювальну програму, спочатку її потрібно прив’язати до контексту рендерингу. Це робиться так само, як і для матеріалів:

```lua
render.set_compute("my_compute")
-- Do compute work here, call render.set_compute() to unbind
render.set_compute()
```

Константи обчислювальної програми застосовуються автоматично під час її запуску, проте прив’язати будь-які вхідні чи вихідні ресурси (текстури, буфери тощо) до обчислювальної програми з редактора неможливо. Це потрібно робити за допомогою скриптів рендерингу:

```lua
render.enable_texture("blur_render_target", "tex_blur")
render.enable_texture(self.storage_texture, "tex_storage")
```

Щоб виконати програму у визначеному вами робочому просторі, потрібно запустити її:

```lua
render.dispatch_compute(128, 128, 1)
-- dispatch_compute also accepts an options table as the last argument
-- you can use this argument table to pass in render constants to the dispatch call
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### Запис даних з обчислювальних програм {#writing-data-from-compute-programs}

Наразі отримати вихідні дані будь-якого типу з обчислювальної програми можна лише через `текстури зберігання` (storage textures). Текстура зберігання подібна до «звичайної текстури», але підтримує більше функцій і налаштувань. Як випливає з назви, текстури зберігання можна використовувати як універсальний буфер, з якого обчислювальна програма може читати дані та в який може їх записувати. Потім цей самий буфер можна прив’язати до іншої шейдерної програми для читання.

Щоб створити текстуру зберігання в Defold, потрібно зробити це зі звичайного файлу `.script`. Скрипти рендерингу не мають такої можливості, оскільки динамічні текстури потрібно створювати через API `resource`, доступний лише у звичайних файлах `.script`.

```lua
-- In a .script file:
function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- get the texture handle from the resource
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- notify the renderer of the backing texture, so it can be bound with render.enable_texture
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## Поєднання всіх частин {#putting-it-all-together}

### Шейдерна програма {#shader-program}

```glsl
// compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// specify the input resources
uniform vec4 color;
uniform sampler2D texture_in;

// specify the output image
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // This isn't a particularly interesting shader, but it demonstrates
    // how to read from a texture and constant buffer and write to a storage texture

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // Write the output value to the storage texture
    imageStore(texture_out, tex_coord, output_value);
}
```

### Компонент-скрипт {#script-component}
```lua
-- In a .script file

-- Here we specify the input texture that we later will bind to the
-- compute program. We can assign this texture to a model component,
-- or enable it to the render context in the render script.
go.property("texture_in", resource.texture())

function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    local textures = {
        texture_in = resource.get_texture_info(self.texture_in).handle,
        texture_out = resource.get_texture_info(t_backing).handle
    }

    -- notify the renderer of the input and output textures
    msg.post("@render:", "set_backing_texture", textures)
end
```

### Скрипт рендерингу {#render-script}
```lua
-- respond to the message "set_backing_texture"
-- to set the backing texture for the compute program
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- We can bind textures to specific named constants
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- Dispatch the compute program as many times as we have pixels.
    -- This constitutes our "working group". The shader will be invoked
    -- 128 x 128 x 1 times, or once per pixel.
    render.dispatch_compute(128, 128, 1)
    -- when we are done with the compute program, we need to unbind it
    render.set_compute()
end
```

## Сумісність {#compatibility}

Наразі Defold підтримує обчислювальні шейдери в таких графічних адаптерах:

- Vulkan
- Metal (через MoltenVK)
- OpenGL 4.3+
- OpenGL ES 3.1+

Використовуйте `graphics.get_adapter_info()`, щоб перевірити, чи підтримує активний графічний адаптер обчислювальні шейдери. Поле `features` містить масив констант можливостей контексту, які підтримує адаптер:

```lua
local function has_context_feature(feature)
    local adapter_info = graphics.get_adapter_info()
    for _, supported_feature in ipairs(adapter_info.features) do
        if supported_feature == feature then
            return true
        end
    end
    return false
end

local compute_shaders_supported = has_context_feature(
    graphics.CONTEXT_FEATURE_COMPUTE_SHADER
)
```

До масиву входять лише підтримувані можливості; це не таблиця, ключами якої є константи можливостей. Завжди виконуйте цю перевірку перед використанням обчислювальних шейдерів, якщо гра може працювати з різними графічними адаптерами або на пристроях з різним рівнем підтримки драйверів. Підтримка в OpenGL і OpenGL ES залежить від версії API та драйвера. Vulkan і Metal через MoltenVK підтримують обчислювальні шейдери починаючи з версії 1.0. Використовуйте [маніфест застосунку](/manuals/app-manifest), щоб вибрати Vulkan на платформах, де він ще не є типовою графічною підсистемою.
