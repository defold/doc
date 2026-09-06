---
title: Посібник з анімації 3D-моделей у Defold
brief: Цей посібник описує, як використовувати анімації 3D-моделей у Defold.
---

# Анімація 3D-моделей {#3d-model-animation}

Компоненти (component) типу Model можуть відтворювати скелетні анімації та анімації цілей морфінгу (morph target animations), імпортовані з файлів glTF. Скелетна анімація використовує кістки моделі для деформації її вершин. Анімація цілей морфінгу, також відома як анімація змішування форм (blend shape animation), змінює форму моделі, анімуючи ваги альтернативних позицій вершин.

Докладніше про імпортування 3D-даних у Model для анімації дивіться в [документації Model](/manuals/model).

  ![Анімація в Blender](images/animation/blender_animation.png)
  ![Циклічне погойдування](images/animation/suzanne.gif)


## Відтворення анімацій {#playing-animations}

Моделі анімують за допомогою функції [`model.play_anim()`](/ref/model#model.play_anim):

```lua
function init(self)
    -- Start the "wiggle" animation back and forth on #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Наразі Defold підтримує лише запечені (baked) скелетні анімації. Скелетні анімації мають містити матриці для кожної анімованої кістки в кожному ключовому кадрі, а не позицію, поворот і масштаб як окремі ключі.

Анімації також інтерполюються лінійно. Якщо ви використовуєте складнішу інтерполяцію кривих, анімації потрібно попередньо запекти засобом експорту.
:::

### Цілі морфінгу {#morph-targets}

Цілі морфінгу — це альтернативні форми тієї самої сітки. Кожна ціль зберігає різниці позицій, нормалей і дотичних та має вагу змішування, яка визначає, якою мірою застосовується ця форма. Вага `0` означає, що ціль не має впливу, а вага `1` застосовує її форму повністю. Значення поза цим діапазоном також можуть бути корисними для перебільшених ефектів, якщо шейдер і ресурс створено з урахуванням цього.

Defold імпортує цілі морфінгу та початкові ваги морфінгу з даних моделі glTF. Анімації glTF, які анімують ваги морфінгу, імпортуються до набору анімацій моделі, і їх можна відтворювати за допомогою [`model.play_anim()`](/ref/model#model.play_anim), як і скелетні анімації:

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

Дані цілей морфінгу можна використовувати окремо або разом зі скелетною анімацією, але компонент моделі може відтворювати лише одну анімацію моделі за раз. Це означає, що за допомогою `model.play_anim()` не можна одночасно відтворювати одну скелетну анімацію та одну окрему анімацію цілей морфінгу. Якщо модель має дані анімації, але не має скелета, використовуватимуться лише дані анімації цілей морфінгу.

Ви все одно можете поєднувати відтворення скелетної анімації зі змінами цілей морфінгу з інших джерел, наприклад установлюючи ваги цілей морфінгу зі скрипту за допомогою `model.set_blend_weights()`.

Ви також можете зчитувати й перевизначати ваги цілей морфінгу зі скрипту. [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) повертає поточні ваги для першої сітки моделі, що має цілі морфінгу. [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) застосовує перевизначення зі скрипту до кожної сітки моделі з морфінгом:

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

Таблиця ваг використовує індекси Lua, що починаються з одиниці, у тому самому порядку, що й цілі морфінгу в сітці. Зайві значення ігноруються, а відсутні значення вважаються нульовими для сіток, що мають більше цілей морфінгу, ніж значень у таблиці. Перевизначення зі скрипту застосовується після анімації в кожному кадрі, доки його не буде скинуто:

```lua
model.set_blend_weights("#model")     -- clear the override
model.set_blend_weights("#model", nil) -- also clears the override
```

### Підтримка в шейдерах {#shader-support}

Для рендерингу цілей морфінгу вершинний шейдер матеріалу моделі має зчитувати дані зі згенерованої текстури `morph_targets` і застосовувати зважені різниці до даних вершин. Текстура цілей морфінгу — це текстура у вигляді масиву 2D-текстур, у якій кожна ціль морфінгу використовує три шари масиву: різницю позицій, різницю нормалей і різницю дотичних.

Рушій передає поточні ваги морфінгу в uniform-змінну вершинного шейдера з назвою `morph_targets_weights`. Кожен `vec4` зберігає чотири ваги, тож `morph_targets_weights[2]` вміщує ваги для восьми цілей морфінгу.

У наступному прикладі показано відповідні частини вершинного шейдера матеріалу моделі без інстансингу:

```glsl
#version 140

in highp vec4 position;
in mediump vec2 texcoord0;
in mediump vec3 normal;
in mediump vec4 tangent;

out mediump vec2 var_texcoord0;
out mediump vec3 var_normal;
out mediump vec4 var_tangent;

uniform vs_uniforms
{
    mediump mat4 mtx_worldview;
    mediump mat4 mtx_proj;
    mediump mat4 mtx_normal;
    // Each vec4 stores four blend weights. Use morph_targets_weights[1]
    // for up to 4 morph targets, [2] for up to 8, [3] for up to 12, etc.
    mediump vec4 morph_targets_weights[2];
};

uniform sampler2DArray morph_targets;

vec2 get_morph_uv(int vertex_index, int width, int height)
{
    int x = vertex_index % width;
    int y = vertex_index / width;
    return vec2(
        (float(x) + 0.5) / float(width),
        (float(y) + 0.5) / float(height)
    );
}

void apply_morph_target(vec2 uv, float weight, int target,
    inout vec3 position_delta, inout vec3 normal_delta, inout vec3 tangent_delta)
{
    if (weight == 0.0) {
        return;
    }

    int position_layer = target * 3 + 0;
    int normal_layer = target * 3 + 1;
    int tangent_layer = target * 3 + 2;

    position_delta += weight * texture(morph_targets, vec3(uv, position_layer)).xyz;
    normal_delta += weight * texture(morph_targets, vec3(uv, normal_layer)).xyz;
    tangent_delta += weight * texture(morph_targets, vec3(uv, tangent_layer)).xyz;
}

void get_morph_target_data(int vertex_index,
    out vec3 position_delta, out vec3 normal_delta, out vec3 tangent_delta)
{
    position_delta = vec3(0.0);
    normal_delta = vec3(0.0);
    tangent_delta = vec3(0.0);

#ifndef EDITOR
    ivec3 texture_size = textureSize(morph_targets, 0);
    vec2 uv = get_morph_uv(vertex_index, texture_size.x, texture_size.y);

    apply_morph_target(uv, morph_targets_weights[0].x, 0, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].y, 1, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].z, 2, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].w, 3, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].x, 4, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].y, 5, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].z, 6, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].w, 7, position_delta, normal_delta, tangent_delta);
#endif
}

void main()
{
    vec3 position_delta;
    vec3 normal_delta;
    vec3 tangent_delta;
    get_morph_target_data(gl_VertexIndex, position_delta, normal_delta, tangent_delta);

    vec3 morphed_position = position.xyz + position_delta;
    vec3 morphed_normal = normalize(normal + normal_delta);
    vec3 morphed_tangent = normalize(tangent.xyz + tangent_delta);

    var_texcoord0 = texcoord0;
    var_normal = normalize((mtx_normal * vec4(morphed_normal, 0.0)).xyz);
    var_tangent = vec4(normalize((mtx_normal * vec4(morphed_tangent, 0.0)).xyz), tangent.w);

    gl_Position = mtx_proj * mtx_worldview * vec4(morphed_position, 1.0);
}
```

Обгортка `#ifndef EDITOR` потрібна, оскільки попередній перегляд анімацій моделей у редакторі ще недоступний, тож згенеровані дані текстури цілей морфінгу доступні лише під час виконання. Збільште розмір масиву `morph_targets_weights` і додайте більше викликів `apply_morph_target()`, якщо сітка має більше цілей морфінгу.

::: important
Наведений вище приклад шейдера використовує `textureSize()` і не працює в OpenGL ES 2.0.
:::

### Ієрархія кісток {#the-bone-hierarchy}

У внутрішньому представленні кістки скелета Model є ігровими об’єктами (game object).

Під час виконання можна отримати ідентифікатор екземпляра ігрового об’єкта кістки. Функція [`model.get_go()`](/ref/model#model.get_go) повертає ідентифікатор ігрового об’єкта для вказаної кістки.

```lua
-- Get the middle bone go of our wiggler model
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Now do something useful with the game object...
```

### Анімація курсора {#cursor-animation}

Окрім використання `model.play_anim()` для просування анімації моделі, компоненти *Model* надають властивість `cursor`, якою можна керувати за допомогою `go.animate()` (докладніше про [анімації властивостей](/manuals/property-animation)):

```lua
-- Set the animation on #model but don't start it
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Set the cursor to the beginning of the animation
go.set("#model", "cursor", 0)
-- Tween the cursor between 0 and 1 pingpong with in-out quad easing.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Зворотні виклики завершення {#completion-callbacks}

Функція анімації моделі `model.play_anim()` підтримує необов’язкову функцію зворотного виклику Lua як останній аргумент. Ця функція викликається, коли анімація відтвориться до кінця. Функція ніколи не викликається для циклічних анімацій, а також коли анімацію вручну скасовано за допомогою `go.cancel_animations()`. Зворотний виклик можна використовувати для запуску подій після завершення анімації або для поєднання кількох анімацій у послідовність.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Done animating
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Режими відтворення {#playback-modes}

Анімації можна відтворювати один раз або циклічно. Спосіб відтворення анімації визначається режимом відтворення:

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
