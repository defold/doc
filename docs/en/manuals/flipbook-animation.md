---
title: Flipbook animations in Defold manual
brief: This manual describes how to use flipbook animations in Defold.
---

# Flip-book animation

A flipbook animation consists of a series of still images that are shown in succession. The technique is very similar to traditional cell animation (see http://en.wikipedia.org/wiki/Traditional_animation). The technique offers limitless opportunities since each frame can be manipulated individually. However, since each frame is stored in a unique image, the memory footprint can be high. The smoothness of animation is also dependent on the number of images shown each second but increasing the number of images usually also increase the amount of work. Defold flipbook animations are either stored as individual images added to an [Atlas](/manuals/atlas), or as a [Tile Source](/manuals/tilesource) with all frames laid out in a horizontal sequence.

  ![Animation sheet](images/animation/animsheet.png){.inline}
  ![Run loop](images/animation/runloop.gif){.inline}

## Playing flip-book animations

Sprites and GUI box nodes can play flip-book animations and you have great control over them at runtime.

Sprites
: To run an animation during runtime you use the [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]) function. See below for an example.

GUI box nodes
: To run an animation during runtime you use the [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]) function. See below for an example.

::: sidenote
The playback mode once ping-pong will play the animation until the last frame and then reverse the order and play back until the **second** frame of the animation, not back to the first frame. This is done so that chaining of animations becomes easier.
:::

### Sprite example

Suppose that your game has a "dodge" feature that allows the player to press a specific button to dodge. You have created four animations to support the feature with visual feedback:

"idle"
: A looping animation of the player character idling.

"dodge_idle"
: A looping animation of the player character idling while being in the dodging stance.

"start_dodge"
: A play-once transition animation taking the player character from standing to dodging.

"stop_dodge"
: A play-once transition animation taking the player character from dodging back to standing.

The following script provides the logic:

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

### GUI box node example

When selecting an animation or image for a node, you are in fact assigning the image source (atlas or tile source) and default animation in one go. The image source is statically set in the node, but the current animation to play can be changed in runtime. Still images are treated as one frame animations so changing an image means in run time is equivalent to playing a different flipbook animation for the node:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    local character_node = gui.get_node("character")
    -- This requires that the node has a default animation in the same atlas or tile source as
    -- the new animation/image we're playing.
    gui.play_flipbook(character_node, "jump_left", flipbook_done)
end
```

An optional function that is called on completion can be provided. It will be called on animations that are played back in any of the `ONCE_*` modes.


## Completion callbacks

All animation functions (`go.animate()`, `gui.animate()`, `gui.play_flipbook()`, `gui.play_spine_anim()`, `sprite.play_flipbook()`, `spine.play_anim()` and `model.play_anim()`) support an optional Lua callback function as the last argument. This function will be called when the animation has played to the end. The function is never called for looping animations, nor when an animation is manually canceled via `go.cancel_animations()`. The callback can be used to trigger events on animation completion or to chain multiple animations together.

The exact function signature of the callback differs slightly between the animation functions. See the API documentation for the function you are using.

```lua
local function done_bouncing(self, url, property)
    -- We're done animating. Do something...
end

function init(self)
    go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, 100, go.EASING_OUTBOUNCE, 2, 0, done_bouncing)
end
```
