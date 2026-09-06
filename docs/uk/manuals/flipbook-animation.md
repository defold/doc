---
title: Посібник з покадрових анімацій у Defold
brief: Цей посібник описує, як використовувати покадрові анімації в Defold.
---

# Покадрова анімація {#flip-book-animation}

Покадрова анімація (flipbook animation) складається з послідовності нерухомих зображень, які показуються одне за одним. Цей метод дуже схожий на традиційну мальовану анімацію (див. http://en.wikipedia.org/wiki/Traditional_animation). Він відкриває безмежні можливості, оскільки кожен кадр можна змінювати окремо. Однак кожен кадр зберігається в окремому зображенні, тому обсяг споживаної пам’яті може бути значним. Плавність анімації також залежить від кількості зображень, що показуються щосекунди, але збільшення їхньої кількості зазвичай збільшує й обсяг роботи. Покадрові анімації в Defold зберігаються або як окремі зображення, додані до [атласу](/manuals/atlas), або як [джерело плиток](/manuals/tilesource), у якому всі кадри розташовано в горизонтальній послідовності.

  ![Аркуш анімації](images/animation/animsheet.png){.inline}
  ![Цикл бігу](images/animation/runloop.gif){.inline}

## Відтворення покадрових анімацій {#playing-flip-book-animations}

Спрайти та вузли GUI типу Box можуть відтворювати покадрові анімації, а ви маєте широкі можливості керування ними під час виконання.

Спрайти
: Щоб запустити анімацію під час виконання, використовуйте функцію [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]). Приклад наведено нижче.

Вузли GUI типу Box
: Щоб запустити анімацію під час виконання, використовуйте функцію [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]). Приклад наведено нижче.

::: sidenote
У режимі відтворення `Once Ping Pong` анімація відтворюється до останнього кадру, а потім у зворотному порядку до **другого** кадру анімації, а не до першого. Це спрощує поєднання анімацій у ланцюжок.
:::

### Приклад зі спрайтом {#sprite-example}

Припустімо, що у вашій грі є функція ухилення ("dodge"), яка дає гравцеві змогу натиснути певну кнопку, щоб ухилитися. Ви створили чотири анімації, щоб візуально відобразити цю дію:

"idle"
: Зациклена анімація персонажа гравця у стані спокою.

"dodge_idle"
: Зациклена анімація персонажа гравця у стані спокою в позі ухилення.

"start_dodge"
: Одноразова анімація переходу персонажа гравця зі звичайної стійки в позу ухилення.

"stop_dodge"
: Одноразова анімація переходу персонажа гравця з пози ухилення назад у звичайну стійку.

Таку логіку реалізує наведений нижче скрипт:

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

### Приклад із вузлом GUI типу Box {#gui-box-node-example}

Вибираючи анімацію або зображення для вузла, ви насправді одночасно задаєте джерело зображень (атлас або джерело плиток) та типову анімацію. Джерело зображень задається у вузлі статично, але поточну анімацію для відтворення можна змінювати під час виконання. Нерухомі зображення вважаються однокадровими анімаціями, тому зміна зображення під час виконання рівнозначна відтворенню іншої покадрової анімації для вузла:

```lua
function init(self)
    local character_node = gui.get_node("character")
    -- This requires that the node has a default animation in the same atlas or tile source as
    -- the new animation/image we're playing.
    gui.play_flipbook(character_node, "jump_left")
end
```


## Зворотні виклики після завершення {#completion-callbacks}

Функції `sprite.play_flipbook()` та `gui.play_flipbook()` підтримують необов’язкову функцію зворотного виклику Lua як останній аргумент. Ця функція викликається, коли анімація відтвориться до кінця. Для зациклених анімацій вона ніколи не викликається. Зворотний виклик можна використовувати, щоб запускати події після завершення анімації або поєднувати кілька анімацій у ланцюжок. Приклади:

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
