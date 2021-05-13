---
title: Руководство по анимации трёхмерных моделей
brief: Данное руководство объясняет как использовать анимации 3D моделей в Defold
---

# 3D Анимация моделей

Скелетная анимация трёхмерных моделей схожа со [скелетной 2D анимацией](/manuals/spine-animation) но работает по законам 3D вместо 2D. Трёхмерная модель не разрезается на отдельные части и не привязывается к кости как в анимационной технике перекладки. Вместо этого, кости влияют на вершины деформируя их в модели, а вам предоставляется гибкий контроль над тем как сильно конкретная кость влияет на геометрию вершин.

Подроьнее о том, как импортируются трехмерные данные в 3D модель для анимации, смотрите [Документация по моделям](/manuals/model).

  ![Blender animation](images/animation/blender_animation.png){.inline srcset="images/animation/blender_animation@2x.png 2x"}
  ![Wiggle loop](images/animation/suzanne.gif){.inline}


## Проигрывание анимаций

Модели анимируются вызовом функции [`model.play_anim()`](/ref/model#model.play_anim):

```lua
function init(self)
    -- Start the "wiggle" animation back and forth on #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
В данный момент Defold поддерживает лишь "запечённые" (предзаготовленные) анимации. Анимации должны иметь матрицы для каждой анимированной кости на каждом кадре, а не позицию, поворот и масштаб как отдельные ключи анимации.

Помимо этого, анимации линейно интерполируются. Если вы делаете более продвинутые кривые интерполяции нежели линейная, анимация должна быть пред-запечена из экспортера.

Анимационные клипы из Collada не поддерживаются. Чтобы пользоваться несколькими анимациями для одной модели, экспортируйте их в отдельные файлы расширения *.dae* и затем соберите все файлы в единый файл *.animationset* в Defold.
:::

### Иерархия костей

Кости в скелете модели внутренне в движке представлены как игровые объекты (game objects).

Можно получить идентификатор конкретного экземпляра игрового объекта кости во время выполнения игры. Функция [`model.get_go()`](/ref/model#model.get_go) возвращает идентификатор игрового объекта для заданной кости.

```lua
-- Get the middle bone go of our wiggler model
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Now do something useful with the game object...
```

### Анимация курсором

В дополнении к использованию метода `model.play_anim()` для более продвинутой анимации модели компоненты типа *Модель* предоставляют свойство "cursor" которым можно управлять с помощью вызова `go.animate()` (более подробно в разделе [анимация свойств](/manuals/property-animation)):

```lua
-- Set the animation on #model but don't start it
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Set the cursor to the beginning of the animation
go.set("#model", "cursor", 0)
-- Tween the cursor between 0 and 1 pingpong with in-out quad easing.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Функции обратного вызова по завершению

Анимация моделей поддерживает опциональные функции обратного вызова в качестве последнего переданного аргумента. Такие переданные функции будут вызваны когда анимация проиграется до конца. Функции никогда не будут вызваны для зацикленных анимаций, а также для анимаций, которые отменили вручную вызовом `go.cancel_animations()`. Функция обратного вызова может быть использована для активации других событий по завершению анимации или для склеивания нескольких анимаций в одну цепочку.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Done animating
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Методы проигрывания

Анимации могут быть проиграны либо однократно либо зацикленно. Как именно проигрывается анимация определяется режимом проигрывания:

* go.PLAYBACK_NONE
* go.PLAYBACK_ONCE_FORWARD
* go.PLAYBACK_ONCE_BACKWARD
* go.PLAYBACK_ONCE_PINGPONG
* go.PLAYBACK_LOOP_FORWARD
* go.PLAYBACK_LOOP_BACKWARD
* go.PLAYBACK_LOOP_PINGPONG
