---
title: Main menu code sample
brief: In this sample, you learn effects to present a main menu.
---
# Main menu

<iframe width="560" height="315" src="https://www.youtube.com/embed/ndkyRuXUr-4" frameborder="0" allowfullscreen></iframe>

In this sample, we demonstrate effects to present a main menu. The menu contains a background and two menu items.

Each of the background and the two menu items, have the same animations applied to them, but with different delays. This is set up in `init()` below.

The first animations is to have each node fade in while being scaled from 70% to 110%.
This is done in `anim1()`.

During the following animations, the scale is animated back and forth from 110% to 98%, to 106% and then to 100%. This gives the bouncing effect and is done in `anim2()`, `anim3()` and `anim4()`.

The background has a special slight fade out at the end, which is applied in `anim5()`.

```lua
-- file: menu.gui_script

-- the functions animX represents the animation time-line
-- first is anim1 executed, when finished anim2 is executed, etc
-- anim1 to anim4 creates a bouncing rubber effect.
-- anim5 fades down alpha and is only used for the background

local function anim5(self, node)
    if gui.get_node("background") == node then
        -- special case for background. animate alpha to 60%
        local to_color = gui.get_color(node)
        to_color.w = 0.6
        gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_OUT, 1.2, 0.1)
    end
end

local function anim4(self, node)
    -- animate scale to 100%
    local s = 1
    gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUT, 0.12, 0, anim5)
end

local function anim3(self, node)
    -- animate scale to 106%
    local s = 1.06
    gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUT, 0.12, 0, anim4)
end

local function anim2(self, node)
    -- animate scale to 98%
    local s = 0.98
    gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_INOUT, 0.12, 0, anim3)
end

local function anim1(node, d)
    -- set scale to 70%
    local start_scale = 0.7
    gui.set_scale(node, vmath.vector4(start_scale, start_scale, start_scale, 0))

    -- get current color and set alpha to 0 to fade up
    local from_color = gui.get_color(node)
    local to_color = gui.get_color(node)
    from_color.w = 0
    gui.set_color(node, from_color)

    -- animate alpha value from 0 to 1
    gui.animate(node, gui.PROP_COLOR, to_color, gui.EASING_IN, 0.2, d)

    -- animate scale from %70 to 110%
    local s = 1.1
    gui.animate(node, gui.PROP_SCALE, vmath.vector4(s, s, s, 0), gui.EASING_IN, 0.2, d, anim2)
end

function init(self)
    -- start animations for all nodes
    -- background, button-boxes and text are animated equally
    -- d is the animation start delay
    local d = 0.4
    anim1(gui.get_node("new_game"), d)
    anim1(gui.get_node("new_game_shadow"), d)
    anim1(gui.get_node("new_game_button"), d)

    d = 0.3
    anim1(gui.get_node("quit"), d)
    anim1(gui.get_node("quit_shadow"), d)
    anim1(gui.get_node("quit_button"), d)

    d = 0.1
    anim1(gui.get_node("background"), d)
end
```
