---
title: Учебник Shadertoy to Defold
brief: В этом учебнике вы перенесёте шейдер с shadertoy.com в Defold.
---

# Учебник Shadertoy

[Shadertoy.com](https://www.shadertoy.com/) — это сайт, где собраны пользовательские GL-шейдеры. Это отличный источник шейдерного кода и вдохновения. В этом учебнике мы возьмём шейдер из Shadertoy и заставим его работать в Defold. Предполагается базовое понимание шейдеров. Если вам нужно освежить тему, хорошим началом будет [руководство по Shader](/manuals/shader/).

В качестве примера мы будем использовать шейдер [Star Nest](https://www.shadertoy.com/view/XlfGRj) от Pablo Andrioli (пользователь "Kali" на Shadertoy). Это полностью процедурный фрагментный шейдер на математической чёрной магии, который рисует очень эффектное звёздное поле.

![Star Nest](../images/shadertoy/starnest.png)

Шейдер занимает всего 65 строк довольно сложного GLSL-кода, но не беспокойтесь. Мы будем относиться к нему как к чёрному ящику, который делает своё дело на основе нескольких простых входных параметров. Наша задача — изменить шейдер так, чтобы он взаимодействовал с Defold, а не с Shadertoy.

## Что будем текстурировать

Шейдер Star Nest — это чистый фрагментный шейдер, поэтому нам нужен лишь объект, который он будет текстурировать. Вариантов несколько: sprite, tilemap, GUI или model. В этом учебнике мы будем использовать простую 3D-модель. Причина в том, что так мы легко можем превратить рендеринг модели в полноэкранный эффект, что полезно, например, для постобработки.

Мы можем начать с пустого проекта.

1. Откройте Defold и выберите Create From *Templates*.
2. Выберите *Empty Project*.
3. Укажите *Title* и выберите *Location* на диске.
4. Нажмите <kbd>Create New Project</kbd>.

![start](../images/shadertoy/empty_project.png)

Можно использовать встроенный mesh `quad.gltf` из `builtins/assets/meshes`.

При желании можно также создать квадратную плоскость в Blender или любой другой программе для 3D-моделирования — для удобства 4 вершины должны иметь координаты -1 и 1 по оси X и -1 и 1 по оси Y. В Blender по умолчанию ось Z направлена вверх, поэтому нужно повернуть mesh на 90° вокруг оси X. Также убедитесь, что для mesh созданы корректные UV-координаты. В Blender выберите mesh, перейдите в *Edit Mode*, затем выполните <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>.

<div class='sidenote' markdown='1'>
Blender — бесплатная 3D-программа с открытым исходным кодом, её можно скачать с [blender.org](https://www.blender.org).
</div>

![quad in Blender](../images/shadertoy/quad_blender.png)

1. Откройте файл "main.collection" в Defold и создайте новый игровой объект "star-nest".
2. Добавьте к "star-nest" компонент *Model*.
3. Установите свойство *Mesh* на наш `quad.gltf`.
4. Нужно задать материал для модели, поэтому пока выберите встроенный `model.material`.

Модель должна появиться в редакторе сцены, но она будет полностью чёрной. Это потому, что для неё ещё не задана текстура:

![quad in Defold](../images/shadertoy/quad_default_material.png)

## Создание материала

1. Создайте новый файл материала *`star-nest.material`*: нажмите <kbd>Right Mouse Button</kbd> на папке `main` в панели `Assets`, выберите <kbd>New</kbd>-><kbd>Material</kbd> и назовите его `star-nest`.

 ![material](../images/shadertoy/new_material.png)

2. Тем же способом создайте vertex shader program `star-nest.vp` и fragment shader program `star-nest.fp`:
3. Откройте *star-nest.material*.
4. Установите *Vertex Program* на `star-nest.vp`.
5. Установите *Fragment Program* на `star-nest.fp`.
6. Добавьте *Vertex Constant* и назовите его "`view_proj`" типа `Viewproj` (для "view projection").
8. Добавьте тег "tile" в *Tags*. Это нужно, чтобы quad включался в проход рендеринга, когда рисуются sprites и tiles.

 ![material](../images/shadertoy/material.png)

### Вершинная программа

1. Откройте файл vertex shader program `star-nest.vp`. Он должен содержать следующий код:

    ```glsl
    #version 140

    // positions are in world space
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### Фрагментная программа

1. Откройте файл fragment shader program `star-nest.fp` и измените код так, чтобы цвет фрагмента задавался на основе X и Y координат UV (`var_texcoord0`). Мы делаем это, чтобы убедиться, что модель настроена правильно:

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. Установите свойство `Material` на только что созданный материал `star-nest` у model component игрового объекта `star-nest` в `main.collection`.

Теперь редактор должен отрисовывать модель новым шейдером, и мы сможем ясно увидеть, верны ли UV-координаты: нижний левый угол должен быть чёрным (0, 0, 0), верхний левый — зелёным (0, 1, 0), верхний правый — жёлтым (1, 1, 0), а нижний правый — красным (1, 0, 0):

![quad in Defold](../images/shadertoy/quad_material.png)

## Камера

Теперь проект можно запустить (<kbd>Project</kbd>-><kbd>Build</kbd> или сочетание <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>), но мы увидим чёрный экран (ну, почти, возможно за исключением одного крошечного пикселя в левом нижнем углу). Это происходит потому, что камеры нет, а стандартный render script использует простой fallback: показывает огромное 2D-пространство, тогда как наша модель находится в позиции (0,0,0) и имеет ширину всего 1.

Добавим game object с camera component, чтобы определить, что будет видно в игре.

1. Добавьте game object с именем `camera` и позицией (0,0,1). (Важно установить координату Z в 1, чтобы этот game object находился перед нашей моделью, поскольку в стандартной 2D-настройке ось Z сейчас направлена к нам).
2. Добавьте компонент `Camera`, и вы увидите camera preview с нашим quad внутри. Со стандартными свойствами нам повезло: в такой настройке ничего менять не нужно, и мы уже должны видеть правильный результат, кроме одного момента — нам не нужен такой большой camera view frustum, поэтому можно уменьшить `Far Z` до `2`.

![camera](../images/shadertoy/camera.png)

При желании можно изменить тип камеры, установив `Orthographic Projection` в `true`, а затем также настроить `Orthographic Zoom` примерно на 600, но в этом случае не будет автоматического aspect ratio, поэтому модель не заполнит экран.

## Шейдер star nest

Теперь всё готово, чтобы заняться собственно кодом шейдера. Сначала посмотрим на оригинал. Он состоит из нескольких частей:

![Star Nest shader code](../images/shadertoy/starnest_code.png)

Мы будем использовать современный pipeline с GLSL версии 140: для этого объявим версию в начале файла с помощью `#version 140`.

1. Строки 5--18 задают набор констант. Их можно оставить как есть. Это обычные GLSL constants, которые не зависят конкретно от Shadertoy или Defold.

2. Строки 21 и 63 содержат входные экранные координаты фрагмента (`in vec2 fragCoord`) и выходной цвет фрагмента (`out vec4 fragColor`).

    Defold передаёт texture coordinates из вершинного шейдера во фрагментный через интерполированную переменную как UV coordinates (в диапазоне 0--1). В нашем вершинном шейдере она объявлена с qualifier `out`:

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     Во фрагментном шейдере это же значение принимается с qualifier `in`:

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    Затем, в GLSL 140, мы объявляем явный fragment output с qualifier `out`:

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    Поэтому там, где исходный код Shadertoy пишет в `fragColor`, наш шейдер Defold пишет в `out_fragColor`.

3. Строки 23--27 задают размеры текстуры, направление движения и масштабированное время. Разрешение viewport/texture передаётся в шейдер как `uniform vec3 iResolution`. Шейдер вычисляет UV-подобные координаты с правильным aspect ratio на основе координат фрагмента и разрешения. Также выполняется небольшое смещение, чтобы кадрирование выглядело лучше.

    В Defold мы не начинаем с pixel coordinates. Вместо этого мы уже получаем нормализованные UV coordinates из вершинного шейдера через `var_texcoord0`. Эти координаты находятся в диапазоне от `0.0` до `1.0` по всему отрисованному quad.

    В версии для Defold эти вычисления нужно изменить так, чтобы использовать UV-координаты из `var_texcoord0`.
    Типичное преобразование выглядит так:

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    Точное значение `aspect` зависит от того, как настроен пример. Если эффект рисуется на full-screen quad с известным display size, aspect ratio можно захардкодить для учебника. Если эффект должен поддерживать произвольные размеры окна, передайте resolution как fragment constant и поместите его в uniform block GLSL 140.

    Здесь же задаётся время. Оно передаётся в шейдер как `uniform float iGlobalTime`. Defold (начиная с 1.12.3) предоставляет время в shaders через специальную константу `Time`, которую мы и будем использовать.

    В современном Defold non-opaque uniforms объявляются внутри uniform blocks.
    Во фрагментном шейдере мы объявляем её так:

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    Затем в `star-nest.material` мы добавим Fragment Constant с именем `time` и типом `Time`.

    Значение можно использовать так:

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    где `time.x` — это время с момента запуска engine, а `time.y` — delta time предыдущего кадра.

4. Строки 29--39 задают вращение объёмного рендеринга, на которое влияет положение мыши. Координаты мыши передаются в шейдер как `uniform vec4 iMouse`.

    В этом учебнике мы пропустим ввод мыши.

5. Строки 41--62 — это ядро шейдера. Этот код можно оставить без изменений.

## Модифицированный шейдер star nest

Если пройтись по описанным выше разделам и внести необходимые изменения, получится следующий шейдер. Он немного приведён в порядок для лучшей читаемости. Отличия между версиями Defold и Shadertoy отмечены:

```glsl
#version 140 // <1>

// Star Nest by Pablo Román Andrioli
// This content is under the MIT License.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// get coords and direction
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// volumetric rendering
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// tiling fold
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// the magic formula
			p = abs(p) / dot(p, p) - formuparam;

			// absolute sum of average change
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// dark matter
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// dark matter, don't render near
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// coloring based on distance
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// color adjust
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```
1. Мы объявляем #version 140 в начале файла, чтобы использовать современный GLSL pipeline Defold. Затем оставляем defines как есть.
2. Вершинный шейдер передаёт UV coordinates во фрагментный шейдер через var_texcoord0. В GLSL 140 фрагментный шейдер принимает это интерполированное значение с qualifier in.
3. В GLSL 140 фрагментный шейдер должен объявить явную output variable вместо записи в gl_FragColor. Здесь мы используем out vec4 out_fragColor.
4. Material constant Time из Defold передаётся в шейдер через uniform block. В star-nest.material добавьте Fragment Constant с именем time и задайте ей тип Time.
5. Shadertoy использует mainImage(out vec4 fragColor, in vec2 fragCoord). В Defold мы используем обычную точку входа void main(), читаем интерполированные UV coordinates из var_texcoord0 и записываем итоговый цвет в out_fragColor.
6. В этом учебнике мы задаём статическое значение resolution/aspect для рендеринга. Сейчас модель квадратная, поэтому можно использовать `vec2 res = vec2(1.0, 1.0);`. Если бы модель была прямоугольной, размером 1280×720, мы могли бы вместо этого использовать `vec2 res = vec2(1.78, 1.0);` и умножать на него UV coordinates, чтобы сохранить правильный aspect ratio.
7. Исходный шейдер Shadertoy использует iGlobalTime. В этой версии для Defold time.x содержит время с момента запуска engine, поэтому мы присваиваем его локальной переменной iGlobalTime и используем для анимации движения камеры через звёздное поле.
8. Мы упрощаем учебник, полностью удаляя значения iMouse. Само вращение при этом сохраняется, потому что оно уменьшает визуальную симметрию объёмного рендеринга.
9. Наконец, шейдер записывает итоговый цвет фрагмента в out_fragColor.

Сохраните fragment shader program. Теперь модель должна красиво отображаться со звёздным полем в Scene editor и во время выполнения:

![quad with starnest](../images/shadertoy/quad_starnest.png)


## Анимация {#animation}

Последний кусочек пазла — добавить время, чтобы звёзды двигались. Defold (начиная с 1.12.3) предоставляет его автоматически через fragment constant типа `Time`.

1. Откройте *star-nest.material*.
2. Добавьте *Fragment Constant* и назовите её "time".
3. Установите её *Type* в `Time`.

![time constant](../images/shadertoy/time_constant.png)

И всё! Мы уже обрабатываем этот `time` во фрагментном шейдере. Готово!

## Упражнения

Хорошее продолжение в качестве упражнения — добавить в шейдер исходный ввод движения мыши. Для этого нужно создать новую Fragment Constant, на этот раз типа `User`, и обновлять её в `on_input` в каком-нибудь script, который отслеживает движение мыши с помощью функции `go.set()` и передаёт входные координаты в новую константу.

Приятной работы с Defold!
