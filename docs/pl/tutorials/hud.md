---
title: Przykład kodu HUD
brief: W tym przykładowym projekcie poznasz efekty zliczania punktów.
---
# HUD - przykładowy projekt

<iframe width="560" height="315" src="https://www.youtube.com/embed/NoPHHG2kbOk" frameborder="0" allowfullscreen></iframe>

W tym przykładowym projekcie, który możesz [otworzyć z poziomu edytora](/manuals/project-setup/) albo [pobrać z GitHub](https://github.com/defold/sample-hud), pokazujemy efekty zliczania punktów. Punkty pojawiają się losowo na ekranie, symulując grę, w której gracz zdobywa punkty w różnych pozycjach.

Po pojawieniu się punkty unoszą się przez chwilę. Aby to osiągnąć, ustawiamy punkty jako przezroczyste, a następnie płynnie zwiększamy krycie ich koloru. Animujemy je również do góry. Jest to zrobione poniżej w `on_message()`.

Następnie przemieszczają się do sumy punktów na górze ekranu, gdzie są dodawane do całości.
Podczas ruchu lekko zanikają. Jest to zrobione w `float_done()`.

Gdy dotrą do wyniku u góry, ich wartości są dodawane do docelowego wyniku, do którego dąży licznik całkowitego wyniku. Jest to zrobione w `swoosh_done()`.

Podczas aktualizacji skrypt sprawdza, czy docelowy wynik został zwiększony i czy całkowity wynik trzeba podliczyć. Jeśli tak, całkowity wynik jest zwiększany mniejszym krokiem.
Następnie skala całkowitego wyniku jest animowana, aby uzyskać efekt odbicia. Jest to zrobione w `update()`.

Za każdym razem, gdy suma jest zwiększana, tworzymy pewną liczbę mniejszych gwiazdek i animujemy je od całkowitego wyniku na zewnątrz. Gwiazdki są tworzone, animowane i usuwane w `spawn_stars()`, `fade_out_star()` i `delete_star()`.

```lua
-- file: hud.gui_script
-- how fast the score counts up per second
local score_inc_speed = 1000

function init(self)
    -- the target score is the current score in the game
    self.target_score = 0
    -- the current score being counted up towards the target score
    self.current_score = 0
    -- the score as displayed in the hud
    self.displayed_score = 0
    -- keep a reference to the node displaying the score for later use below
    self.score_node = gui.get_node("score")
end

local function delete_star(self, star)
    -- star has finished animation, delete it
    gui.delete_node(star)
end

local function fade_out_star(self, star)
    -- fade out the star before deletion
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_INOUT, 0.2, 0.0, delete_star)
end

local function spawn_stars(self, amount)
    -- position of the score node, to be used for placing the stars
    local p = gui.get_position(self.score_node)
    -- distance from the position where the star is spawned
    local start_distance = 0
    -- distance where the star stops
    local end_distance = 240
    -- angle distance between each star in the star circle
    local angle_step = 2 * math.pi / amount
    -- randomize start angle
    local angle = angle_step * math.random()
    for i=1,amount do
        -- increment the angle by the step to get an even distribution of stars
        angle = angle + angle_step
        -- direction of the star movement
        local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0)
        -- start/end positions of the star
        local start_p = p + dir * start_distance
        local end_p = p + dir * end_distance
        -- create the star node
        local star = gui.new_box_node(vmath.vector3(start_p.x, start_p.y, 0), vmath.vector3(30, 30, 0))
        -- set its texture
        gui.set_texture(star, "star")
        -- set to transparent
        gui.set_color(star, vmath.vector4(1, 1, 1, 0))
        -- fade in
        gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.2, 0.0, fade_out_star)
        -- animate position
        gui.animate(star, gui.PROP_POSITION, end_p, gui.EASING_NONE, 0.55)
    end
end

function update(self, dt)
    -- check if the score needs to be updated
    if self.current_score < self.target_score then
        -- increment the score for this timestep to grow towards the target score
        self.current_score = self.current_score + score_inc_speed * dt
        -- clamp the score so it doesn't grow past the target score
        self.current_score = math.min(self.current_score, self.target_score)
        -- floor the score so it can be displayed without decimals
        local floored_score = math.floor(self.current_score)
        -- check if the displayed score should be updated
        if self.displayed_score ~= floored_score then
            -- update displayed score
            self.displayed_score = floored_score
            -- update the text of the score node
            gui.set_text(self.score_node, string.format("%d p", self.displayed_score))
            -- set the scale of the score node to be slightly bigger than normal
            local s = 1.3
            gui.set_scale(self.score_node, vmath.vector3(s, s, s))
            -- then animate the scale back to the original value
            s = 1.0
            gui.animate(self.score_node, gui.PROP_SCALE, vmath.vector3(s, s, s), gui.EASING_OUT, 0.2)
            -- spawn stars
            spawn_stars(self, 4)
        end
    end
end

-- this function stores the added score so that the displayed score can be counted up in the update function
local function swoosh_done(self, node)
    -- retrieve score from node
    local amount = tonumber(gui.get_text(node))
    -- increase the target score, see the update function for how the score is updated to match the target score
    self.target_score = self.target_score + amount
    -- remove the temp score
    gui.delete_node(node)
end

-- this function animates the node from having floated first to swoosh away towards the displayed total score
local function float_done(self, node)
    local duration = 0.2
    -- swoosh away towards the displayed score
    gui.animate(node, gui.PROP_POSITION, gui.get_position(self.score_node), gui.EASING_IN, duration, 0.0, swoosh_done)
    -- also fade out partially during the swoosh
    gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0.6), gui.EASING_IN, duration)
end

function on_message(self, message_id, message, sender)
    -- register added score, this message could be sent by anyone wanting to increment the score
    if message_id == hash("add_score") then
        -- create a new temporary score node
        local node = gui.new_text_node(message.position, tostring(message.amount))
        -- use the small font for it
        gui.set_font(node, "small_score")
        -- initially transparent
        gui.set_color(node, vmath.vector4(1, 1, 1, 0))
        gui.set_outline(node, vmath.vector4(0, 0, 0, 0))
        -- fade in
        gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.3)
        gui.animate(node, gui.PROP_OUTLINE, vmath.vector4(0, 0, 0, 1), gui.EASING_OUT, 0.3)
        -- float
        local offset = vmath.vector3(0, 20, 0)
        gui.animate(node, gui.PROP_POSITION, gui.get_position(node) + offset, gui.EASING_NONE, 0.5, 0.0, float_done)
    end
end
```

W `main.script` pobieramy wejście dotyku/myszy, a następnie wysyłamy wiadomość do skryptu GUI, tworząc nowe wyniki z użyciem pozycji dotknięcia.

```lua
-- On click/touch get touch position and send it via message to hud gui script as well as the scored point amount.

function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    local pos = vmath.vector3(action.x, action.y, 0) -- use input action.x & action.y as x & y positions of touch
    if action_id == hash("touch") then
        if action.pressed then
            msg.post("main:/hud#hud", "add_score" , { position = pos, amount = 1500})
        end
    end
end
```
