---
title: HUD code sample
brief: In this sample, you learn effects for score counting.
---
# HUD

<iframe width="560" height="315" src="https://www.youtube.com/embed/bcU9PCrPAeY" frameborder="0" allowfullscreen></iframe>

In this sample, we demonstrate effects for score counting. The scores appear randomly over the screen, simulating a game where the player obtains scores at different positions.

The scores float for a while after they appear. To achieve this, we set the scores to transparent and then fade in their color. We also animate them upwards. This is done in `on_message()` below.

Then they move up to the total score in the top of the screen where they are summed up.
They are also slightly fading out while moving up. This is done in `float_done()`.

When they have reached the top score, their amounts are added to a target score that the total score counts up towards. This is done in `swoosh_done()`.

When the script is updated, it checks if the target score has been increased and the total score needs to be counted up. When this is true, the total score is incremented by a smaller step.
The scale of the total score is then animated to give a bouncing effect. This is done in `update()`.

Each time the total is incremented, we spawn an amount of smaller stars and animate them out from the total score. The stars are spawned, animated and deleted in `spawn_stars()`, `fade_out_star()` and `delete_star()`.

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
