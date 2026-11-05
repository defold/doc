---
title: Пример кода HUD
brief: В этом примере проекта вы познакомитесь с эффектами для подсчёта очков.
---
# HUD — пример проекта

<iframe width="560" height="315" src="https://www.youtube.com/embed/NoPHHG2kbOk" frameborder="0" allowfullscreen></iframe>

В этом примере проекта, который можно [открыть из редактора](/manuals/project-setup/) или [скачать с GitHub](https://github.com/defold/sample-hud), мы показываем эффекты для подсчёта очков. Очки случайным образом появляются в разных местах экрана, имитируя игру, где игрок получает очки в разных позициях.

После появления очки некоторое время парят в воздухе. Чтобы добиться этого, мы сначала делаем их прозрачными, затем плавно проявляем цвет. Одновременно они анимированно двигаются вверх. Это делается в `on_message()` ниже.

Затем они перемещаются к общей сумме очков в верхней части экрана, где складываются с ней.
Во время этого движения они также немного исчезают. Это выполняется в `float_done()`.

Когда они достигают верхнего счёта, их значения добавляются к целевому счёту, до которого должен досчитаться общий итог. Это делается в `swoosh_done()`.

При обновлении скрипта проверяется, увеличился ли целевой счёт и нужно ли увеличивать общий итог. Если да, общий счёт наращивается небольшими шагами.
После этого масштаб общего счёта анимируется, создавая эффект подпрыгивания. Это делается в `update()`.

Каждый раз, когда общий итог увеличивается, мы создаём несколько маленьких звёзд и анимируем их вылет от общего счёта. Звёзды создаются, анимируются и удаляются в `spawn_stars()`, `fade_out_star()` и `delete_star()`.

```lua
-- файл: hud.gui_script
-- скорость увеличения счёта в секунду
local score_inc_speed = 1000

function init(self)
    -- целевой счёт — это текущий счёт в игре
    self.target_score = 0
    -- текущий счёт, постепенно приближающийся к целевому
    self.current_score = 0
    -- счёт, отображаемый в HUD
    self.displayed_score = 0
    -- сохранить ссылку на ноду, отображающую счёт, для дальнейшего использования
    self.score_node = gui.get_node("score")
end

local function delete_star(self, star)
    -- анимация звезды завершилась, удалить её
    gui.delete_node(star)
end

local function fade_out_star(self, star)
    -- плавно скрыть звезду перед удалением
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_INOUT, 0.2, 0.0, delete_star)
end

local function spawn_stars(self, amount)
    -- позиция ноды со счётом для размещения звёзд
    local p = gui.get_position(self.score_node)
    -- расстояние от позиции, в которой создаётся звезда
    local start_distance = 0
    -- расстояние, на котором звезда останавливается
    local end_distance = 240
    -- угловое расстояние между звёздами в круге
    local angle_step = 2 * math.pi / amount
    -- выбрать случайный начальный угол
    local angle = angle_step * math.random()
    for i=1,amount do
        -- увеличить угол на шаг, чтобы звёзды распределялись равномерно
        angle = angle + angle_step
        -- направление движения звезды
        local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0)
        -- начальная и конечная позиции звезды
        local start_p = p + dir * start_distance
        local end_p = p + dir * end_distance
        -- создать ноду звезды
        local star = gui.new_box_node(vmath.vector3(start_p.x, start_p.y, 0), vmath.vector3(30, 30, 0))
        -- задать её текстуру
        gui.set_texture(star, "star")
        -- сделать прозрачной
        gui.set_color(star, vmath.vector4(1, 1, 1, 0))
        -- плавно проявить
        gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.2, 0.0, fade_out_star)
        -- анимировать позицию
        gui.animate(star, gui.PROP_POSITION, end_p, gui.EASING_NONE, 0.55)
    end
end

function update(self, dt)
    -- проверить, нужно ли обновить счёт
    if self.current_score < self.target_score then
        -- увеличить счёт за этот шаг, приближая его к целевому значению
        self.current_score = self.current_score + score_inc_speed * dt
        -- ограничить счёт, чтобы он не превысил целевое значение
        self.current_score = math.min(self.current_score, self.target_score)
        -- округлить счёт вниз, чтобы отображать его без дробной части
        local floored_score = math.floor(self.current_score)
        -- проверить, нужно ли обновить отображаемый счёт
        if self.displayed_score ~= floored_score then
            -- обновить отображаемый счёт
            self.displayed_score = floored_score
            -- обновить текст ноды со счётом
            gui.set_text(self.score_node, string.format("%d p", self.displayed_score))
            -- сделать масштаб ноды со счётом немного больше обычного
            local s = 1.3
            gui.set_scale(self.score_node, vmath.vector3(s, s, s))
            -- затем анимировать возвращение масштаба к исходному значению
            s = 1.0
            gui.animate(self.score_node, gui.PROP_SCALE, vmath.vector3(s, s, s), gui.EASING_OUT, 0.2)
            -- создать звёзды
            spawn_stars(self, 4)
        end
    end
end

-- эта функция сохраняет добавленные очки, чтобы функция update могла постепенно увеличивать отображаемый счёт
local function swoosh_done(self, node)
    -- получить очки из ноды
    local amount = tonumber(gui.get_text(node))
    -- увеличить целевой счёт; в функции update показано, как отображаемый счёт постепенно достигает целевого
    self.target_score = self.target_score + amount
    -- удалить временную ноду с очками
    gui.delete_node(node)
end

-- эта функция анимирует ноду: после плавного движения она быстро перемещается к отображаемому общему счёту
local function float_done(self, node)
    local duration = 0.2
    -- быстро переместить к отображаемому счёту
    gui.animate(node, gui.PROP_POSITION, gui.get_position(self.score_node), gui.EASING_IN, duration, 0.0, swoosh_done)
    -- также частично уменьшить непрозрачность во время перемещения
    gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0.6), gui.EASING_IN, duration)
end

function on_message(self, message_id, message, sender)
    -- зарегистрировать добавленные очки; это сообщение может отправить любой, кому нужно увеличить счёт
    if message_id == hash("add_score") then
        -- создать новую временную ноду с очками
        local node = gui.new_text_node(message.position, tostring(message.amount))
        -- использовать для неё маленький шрифт
        gui.set_font(node, "small_score")
        -- изначально прозрачна
        gui.set_color(node, vmath.vector4(1, 1, 1, 0))
        gui.set_outline(node, vmath.vector4(0, 0, 0, 0))
        -- плавно проявить
        gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.3)
        gui.animate(node, gui.PROP_OUTLINE, vmath.vector4(0, 0, 0, 1), gui.EASING_OUT, 0.3)
        -- плавно переместить вверх
        local offset = vmath.vector3(0, 20, 0)
        gui.animate(node, gui.PROP_POSITION, gui.get_position(node) + offset, gui.EASING_NONE, 0.5, 0.0, float_done)
    end
end
```

В main.script мы принимаем ввод с мыши или касания, а затем отправляем сообщение в gui-скрипт, который создаёт новые очки в позиции касания.

```lua
-- При нажатии мыши или касании получить позицию и отправить её в GUI-скрипт HUD вместе с числом набранных очков.

function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    local pos = vmath.vector3(action.x, action.y, 0) -- использовать action.x и action.y из события ввода как координаты x и y касания
    if action_id == hash("touch") then
        if action.pressed then
            msg.post("main:/hud#hud", "add_score" , { position = pos, amount = 1500})
        end
    end
end
```