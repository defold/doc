---
title: Руководство по покадровой анимации в Defold
brief: Данное руководство объясняет как использовать покадровую анимацию в Defold
---

# Покадровая анимация

Покадровая анимация состоит из серии неподвижных изображений, которые отображаются одно за другим. Данная техника весьма схожа с традиционной рисованной мультипликацией (см. https://ru.wikipedia.org/wiki/%D0%A0%D0%B8%D1%81%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F_%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D0%B8%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F). Эта техника предлагает безграничные возможности, т.к. каждым кадром можно управлять отдельно. Однако, так как каждый кадр хранится в отдельном изображении, расходование памяти может быть ощутимым. Плавность анимации также зависит от числа изображений на секунду времени, но увеличение числа изображений как правило увеличивает и количество работы. Покадровая анимация в Defold ъранится либо как отдельные изображения, добавленные в Атлас * (/manuals/atlas) либо как Tile Source (/manuals/tilesource) в виде кадров выстроенных в горизонтальную последовательность.

  ![Лист кадров анимации](images/animation/animsheet.png){.inline}
  ![Цикл бега](images/animation/runloop.gif){.inline}

## Проигрывание покадровой анимации

Спрайты и GUI box-ноды могут отображать покадровые анимации и вы можете достаточно гибко управлять ими прямо во время выполнения игры
Sprites and GUI box nodes can play flip-book animations and you have great control over them at runtime.

Спрайты
: Чтобы запустить анимацию во время выполнения игры используйте функцию [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]). Смотрите пример ниже.

GUI box-ноды
: Чтобы запустить анимацию во время выполнения игры используйте функцию [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]). Смотрите пример ниже.

::: Примечание
Метод проигрывания "однократный, пинг-понг" проиграет анимацию до последнего кадра, затем в обратном порядке до **второго** кадра анимации, а не до самого первого. Это сделано, чтобы облегчить процесс склеивания цепочек анимаций.
:::

### Примеры со спрайтами

Предположим, что в вашей игре есть фича "уклониться", которая позволяет игроку уклоняться по нажатию специальной кнопки. Для визуального эффекта такой фичи, вы реализовали 4 анимации:

"idle"
: Зацикленная анимация игрового персонажа в состоянии покоя.

"dodge_idle"
: Зацикленная анимация игрового персонажа в состоянии покоя, находясь в позиции уклонения.

"start_dodge"
: Однократная анимация-переход переводящая игрового персонажа из обычной стойки в уклонение.

"stop_dodge"
: Однократная анимация-переход переводящая игрового персонажа из уклонения в обычную стойку.

Следующий скрипт реализует такую логику:

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" is our input action
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- remember that we are dodging
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- we are not dodging anymore
            self.dodge = false
        end
    end
end
```

### Примеры с GUI box-нодами

Выбирая анимацию или изображение для ноды, вы фактически назначаете источник изображения (атлас или Tile source) и анимацию по-умолчанию. Источник изображения статически устанавливается для ноды, но текущая анимация для проигрывания может быть изменена во время работы игры. Обычные изображения трактуются движком как однокадровые анимации, так что, изменение изображения во время работы игры есть эквивалент покадровой анимации для ноды:

```lua
function init(self)
    local character_node = gui.get_node("character")
    -- This requires that the node has a default animation in the same atlas or tile source as
    -- the new animation/image we're playing.
    gui.play_flipbook(character_node, "jump_left")
end
```


## Функции обратного вызова по завершению

Функции `sprite.play_flipbook()` и `gui.play_flipbook()` поддерживают опциональные функции обратного вызова в качестве последнего переданного аргумента. Такие переданные функции будут вызваны когда анимация проиграется до конца. Функции никогда не будут вызваны для зацикленных анимаций. Функция обратного вызова может быть использована для активации других событий по завершению анимации или для склеивания нескольких анимаций в одну цепочку. Примеры:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    sprite.play_flipbook("#character", "jump_left", flipbook_done)
end
```

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    gui.play_flipbook(gui.get_node("character"), "jump_left", flipbook_done)
end
```
