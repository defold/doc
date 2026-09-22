---
title: Посібник з анімації властивостей у Defold
brief: У цьому посібнику описано, як використовувати анімацію властивостей у Defold.
---

# Анімація властивостей {#property-animation}

Усі числові властивості (`numbers`, `vector3`, `vector4` та кватерніони) і константи шейдерів можна анімувати за допомогою вбудованої системи анімації, використовуючи функцію `go.animate()`. Рушій автоматично інтерполюватиме властивості відповідно до заданих режимів відтворення та функцій згладжування (easing). Також можна задавати власні функції згладжування.

  ![Анімація властивостей](images/animation/property_animation.png)
  ![Циклічний відскок](images/animation/bounce.gif)

## Анімація властивостей {#property-animation-1}

Щоб анімувати властивість ігрового об’єкта (game object) або компонента (component), використовуйте функцію `go.animate()`. Для властивостей вузлів GUI відповідною функцією є `gui.animate()`.

```lua
-- Set the position property y component to 200
go.set(".", "position.y", 200)
-- Then animate it
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

Щоб зупинити всі анімації певної властивості, викличте `go.cancel_animations()`, а для вузлів GUI — `gui.cancel_animations()`:

```lua
-- Stop euler z rotation animation on the current game object
go.cancel_animations(".", "euler.z")
```

Якщо скасувати анімацію складеної властивості, наприклад `position`, усі анімації її складових (`position.x`, `position.y` і `position.z`) також буде скасовано.

У [посібнику з властивостей](/manuals/properties) наведено всі доступні властивості ігрових об’єктів, компонентів і вузлів GUI.

## Анімація властивостей вузлів GUI {#gui-node-property-animation}

Майже всі властивості вузлів GUI можна анімувати. Наприклад, можна зробити вузол невидимим, задавши повну прозорість у його властивості `color`, а потім поступово зробити його видимим, анімуючи зміну кольору на білий (тобто без тонування).

```lua
local node = gui.get_node("button")
local color = gui.get_color(node)
-- Animate the color to white
gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_INOUTQUAD, 0.5)
-- Animate the outline red color component
gui.animate(node, "outline.x", 1, gui.EASING_INOUTQUAD, 0.5)
-- And move to x position 100
gui.animate(node, hash("position.x"), 100, gui.EASING_INOUTQUAD, 0.5)
```

## Зворотні виклики після завершення {#completion-callbacks}

Функції анімації властивостей `go.animate()` і `gui.animate()` підтримують необов’язкову функцію зворотного виклику Lua як останній аргумент. Цю функцію буде викликано, коли анімація відтвориться до кінця. Функція ніколи не викликається для циклічних анімацій, а також коли анімацію скасовано вручну за допомогою `go.cancel_animations()` або `gui.cancel_animations()`. Зворотний виклик можна використовувати для запуску подій після завершення анімації або для об’єднання кількох анімацій у послідовність.

## Згладжування {#easing}

Згладжування визначає, як анімоване значення змінюється з часом. Наведені нижче зображення показують функції, які застосовуються в часі для створення згладжування.

Для `go.animate()` допустимі такі значення згладжування:

|---|---|
| `go.EASING_LINEAR` | |
| `go.EASING_INBACK` | `go.EASING_OUTBACK` |
| `go.EASING_INOUTBACK` | `go.EASING_OUTINBACK` |
| `go.EASING_INBOUNCE` | `go.EASING_OUTBOUNCE` |
| `go.EASING_INOUTBOUNCE` | `go.EASING_OUTINBOUNCE` |
| `go.EASING_INELASTIC` | `go.EASING_OUTELASTIC` |
| `go.EASING_INOUTELASTIC` | `go.EASING_OUTINELASTIC` |
| `go.EASING_INSINE` | `go.EASING_OUTSINE` |
| `go.EASING_INOUTSINE` | `go.EASING_OUTINSINE` |
| `go.EASING_INEXPO` | `go.EASING_OUTEXPO` |
| `go.EASING_INOUTEXPO` | `go.EASING_OUTINEXPO` |
| `go.EASING_INCIRC` | `go.EASING_OUTCIRC` |
| `go.EASING_INOUTCIRC` | `go.EASING_OUTINCIRC` |
| `go.EASING_INQUAD` | `go.EASING_OUTQUAD` |
| `go.EASING_INOUTQUAD` | `go.EASING_OUTINQUAD` |
| `go.EASING_INCUBIC` | `go.EASING_OUTCUBIC` |
| `go.EASING_INOUTCUBIC` | `go.EASING_OUTINCUBIC` |
| `go.EASING_INQUART` | `go.EASING_OUTQUART` |
| `go.EASING_INOUTQUART` | `go.EASING_OUTINQUART` |
| `go.EASING_INQUINT` | `go.EASING_OUTQUINT` |
| `go.EASING_INOUTQUINT` | `go.EASING_OUTINQUINT` |

Для `gui.animate()` допустимі такі значення згладжування:

|---|---|
| `gui.EASING_LINEAR` | |
| `gui.EASING_INBACK` | `gui.EASING_OUTBACK` |
| `gui.EASING_INOUTBACK` | `gui.EASING_OUTINBACK` |
| `gui.EASING_INBOUNCE` | `gui.EASING_OUTBOUNCE` |
| `gui.EASING_INOUTBOUNCE` | `gui.EASING_OUTINBOUNCE` |
| `gui.EASING_INELASTIC` | `gui.EASING_OUTELASTIC` |
| `gui.EASING_INOUTELASTIC` | `gui.EASING_OUTINELASTIC` |
| `gui.EASING_INSINE` | `gui.EASING_OUTSINE` |
| `gui.EASING_INOUTSINE` | `gui.EASING_OUTINSINE` |
| `gui.EASING_INEXPO` | `gui.EASING_OUTEXPO` |
| `gui.EASING_INOUTEXPO` | `gui.EASING_OUTINEXPO` |
| `gui.EASING_INCIRC` | `gui.EASING_OUTCIRC` |
| `gui.EASING_INOUTCIRC` | `gui.EASING_OUTINCIRC` |
| `gui.EASING_INQUAD` | `gui.EASING_OUTQUAD` |
| `gui.EASING_INOUTQUAD` | `gui.EASING_OUTINQUAD` |
| `gui.EASING_INCUBIC` | `gui.EASING_OUTCUBIC` |
| `gui.EASING_INOUTCUBIC` | `gui.EASING_OUTINCUBIC` |
| `gui.EASING_INQUART` | `gui.EASING_OUTQUART` |
| `gui.EASING_INOUTQUART` | `gui.EASING_OUTINQUART` |
| `gui.EASING_INQUINT` | `gui.EASING_OUTQUINT` |
| `gui.EASING_INOUTQUINT` | `gui.EASING_OUTINQUINT` |

![Лінійна інтерполяція](images/properties/easing_linear.png)
![Відхилення назад на вході](images/properties/easing_inback.png)
![Відхилення назад на виході](images/properties/easing_outback.png)
![Відхилення назад на вході-виході](images/properties/easing_inoutback.png)
![Відхилення назад на виході-вході](images/properties/easing_outinback.png)
![Відскоки на вході](images/properties/easing_inbounce.png)
![Відскоки на виході](images/properties/easing_outbounce.png)
![Відскоки на вході-виході](images/properties/easing_inoutbounce.png)
![Відскоки на виході-вході](images/properties/easing_outinbounce.png)
![Пружне згладжування на вході](images/properties/easing_inelastic.png)
![Пружне згладжування на виході](images/properties/easing_outelastic.png)
![Пружне згладжування на вході-виході](images/properties/easing_inoutelastic.png)
![Пружне згладжування на виході-вході](images/properties/easing_outinelastic.png)
![Синусоїдальне згладжування на вході](images/properties/easing_insine.png)
![Синусоїдальне згладжування на виході](images/properties/easing_outsine.png)
![Синусоїдальне згладжування на вході-виході](images/properties/easing_inoutsine.png)
![Синусоїдальне згладжування на виході-вході](images/properties/easing_outinsine.png)
![Експоненційне згладжування на вході](images/properties/easing_inexpo.png)
![Експоненційне згладжування на виході](images/properties/easing_outexpo.png)
![Експоненційне згладжування на вході-виході](images/properties/easing_inoutexpo.png)
![Експоненційне згладжування на виході-вході](images/properties/easing_outinexpo.png)
![Кругове згладжування на вході](images/properties/easing_incirc.png)
![Кругове згладжування на виході](images/properties/easing_outcirc.png)
![Кругове згладжування на вході-виході](images/properties/easing_inoutcirc.png)
![Кругове згладжування на виході-вході](images/properties/easing_outincirc.png)
![Квадратичне згладжування на вході](images/properties/easing_inquad.png)
![Квадратичне згладжування на виході](images/properties/easing_outquad.png)
![Квадратичне згладжування на вході-виході](images/properties/easing_inoutquad.png)
![Квадратичне згладжування на виході-вході](images/properties/easing_outinquad.png)
![Кубічне згладжування на вході](images/properties/easing_incubic.png)
![Кубічне згладжування на виході](images/properties/easing_outcubic.png)
![Кубічне згладжування на вході-виході](images/properties/easing_inoutcubic.png)
![Кубічне згладжування на виході-вході](images/properties/easing_outincubic.png)
![Згладжування за функцією четвертого степеня на вході](images/properties/easing_inquart.png)
![Згладжування за функцією четвертого степеня на виході](images/properties/easing_outquart.png)
![Згладжування за функцією четвертого степеня на вході-виході](images/properties/easing_inoutquart.png)
![Згладжування за функцією четвертого степеня на виході-вході](images/properties/easing_outinquart.png)
![Згладжування за функцією п’ятого степеня на вході](images/properties/easing_inquint.png)
![Згладжування за функцією п’ятого степеня на виході](images/properties/easing_outquint.png)
![Згладжування за функцією п’ятого степеня на вході-виході](images/properties/easing_inoutquint.png)
![Згладжування за функцією п’ятого степеня на виході-вході](images/properties/easing_outinquint.png)

## Власне згладжування {#custom-easing}

Ви можете створювати власні криві згладжування, визначивши `vector` із набором значень, а потім передати цей вектор замість однієї з наведених вище констант згладжування. Значення вектора задають криву від початкового значення (`0`) до цільового (`1`). Середовище виконання вибирає значення з вектора та використовує лінійну інтерполяцію для обчислення значень між точками, заданими у векторі.

Наприклад, вектор:

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5, 1 }
local my_easing = vmath.vector(values)
```

задає таку криву:

![Власна крива](images/animation/custom_curve.png)

У наведеному нижче прикладі позиція ігрового об’єкта за віссю y стрибкоподібно змінюється між поточною позицією та 200 відповідно до прямокутної кривої:

```lua
local values = { 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1 }
local square_easing = vmath.vector(values)
go.animate("go", "position.y", go.PLAYBACK_LOOP_PINGPONG, 200, square_easing, 2.0)
```

![Прямокутна крива](images/animation/square_curve.png)
