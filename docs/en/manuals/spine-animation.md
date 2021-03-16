---
title: Spine animation in Defold manual
brief: This manual describes hpw to use Spine animations in Defold.
---

# Spine animation

Spine animation provides 2D _skeletal animation_ support (see http://en.wikipedia.org/wiki/Skeletal_animation). This is a fundamentally different technique from [flipbook animations](/manuals/flipbook-animation) that is closer to cutout animation. In cutout animation separate pieces of the animated object (e.g body parts, eyes, mouth etc) are moved individually between each frame. Spine animation let you build an invisible, virtual skeleton consisting of a hierarchy of interconnected _bones_. This skeleton, or _rig_, is then animated and individual images are attached to the bones. Defold supports animations created or exported in the [Spine JSON format](http://esotericsoftware.com/spine-json-format). Skeletal animation is very smooth since the engine can interpolate the location of each bone for each frame.

For details on how to import Spine data into a Spine model for animation, see the [Spine documentation](/manuals/spine).

  ![Spine animation](images/animation/spine_animation.png){.inline}
  ![Run loop](images/animation/frog_runloop.gif){.inline}

:::sidenote
Spine animations can also be used within a GUI. Refer to the [GUI manual](/manuals/gui-spine) manual for more information.
:::

## Playing animations

To run animations on your model, simply call the [`spine.play_anim()`](/ref/spine#spine.play_anim) function:

```lua
function init(self)
    -- Play the "walk" animation on component "spinemodel" and blend against previous
    -- animation for the first 0.1 seconds
    local anim_props = { blend_duration = 0.1 }
    spine.play_anim("#spinemodel", "run", go.PLAYBACK_LOOP_FORWARD, anim_props)
end
```

![Spine model in game](images/animation/spine_ingame.png){srcset="images/animation/spine_ingame@2x.png 2x"}

If an animation is played with any of the `go.PLAYBACK_ONCE_*` modes and you have provided a callback function to `spine.play_anim()` the callback is run on animation complete. See below for information on callbacks.

### Cursor animation

In addition to using the `spine.play_anim()` to advance a spine animation, *Spine Model* components expose a "cursor" property that can be manipulated with `go.animate()` (more about [property animations](/manuals/property-animation)):

```lua
-- Set the animation on the spine model but don't run it.
spine.play_anim("#spinemodel", "run_right", go.PLAYBACK_NONE)

-- Set the cursor to position 0
go.set("#spinemodel", "cursor", 0)

-- Tween the cursor slowly between 0 and 1 pingpong with in-out quad easing.
go.animate("#spinemodel", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 6)
```

::: important
When tweening or setting the cursor, timeline events may not fire as expected.
:::

### The bone hierarchy

The individual bones in the Spine skeleton are represented internally as game objects. In the *Outline* view of the Spine model component, the full hierarchy is visible. You can see each bone's name and its place in the skeleton hierarchy.

![Spine model hierarchy](images/animation/spine_bones.png){srcset="images/animation/spine_bones@2x.png 2x"}

With the bone name at hand, you are able to retrieve the instance id of the bone in runtime. The function [`spine.get_go()`](/ref/spine#spine.get_go) returns the id of the specified bone and you can, for instance, child other game objects under the animated game object:

```lua
-- Attach pistol game object to the hand of the heroine
local hand = spine.get_go("heroine#spinemodel", "front_hand")
msg.post("pistol", "set_parent", { parent_id = hand })
```

### Timeline events

Spine animations can trigger timed events by sending messages at precise moments. They are very useful for events that should take place in sync with your animation, like playing footstep sounds, spawning particle effects, attaching or detaching objects to the bone hierarchy or anything else you would like to happen.

Events are added in the Spine software and are visualized on the playback timeline:

![Spine events](images/animation/spine_events.png)

Each event is referenced with a name identifier ("bump" in the example above) and each event instance on the timeline can contain additional information:

Integer
: A numerical value expressed as an integer.

Float
: A floating point numerical value.

String
: A string value.

When the animation plays and events are encountered, `spine_event` messages are sent back to the script component that called `spine.play()`. The message data contains the custom numbers and strings embedded in the event, as well as a few additional fields that are sometimes useful:

`t`
: The number of seconds passed since the first frame of the animation.

`animation_id`
: The animation name, hashed.

`string`
: The provided string value, hashed.

`float`
: The provided floating point numerical value.

`integer`
: The provided integer numerical value.

`event_id`
: The event identifier, hashed.

`blend_weight`
: How much of the animation is blended in at this point. 0 means that nothing of the current animation is part of the blend yet, 1 means that the blend consists of the current animation to 100%.

```lua
-- Spine animation contains events that are used to play sounds in sync with the animation.
-- These arrive here as messages.
function on_message(self, message_id, message, sender)
  if message_id == hash("spine_event") and message.event_id == hash("play_sound") then
    -- Play animation sound. The custom event data contains the sound component and the gain.
    local url = msg.url("sounds")
    url.fragment = message.string
    sound.play(url, { gain = message.float })
  end
end
```

## Completion callbacks

The spine animation function `spine.play_anim()` support an optional Lua callback function as the last argument. This function will be called when the animation has played to the end. The function is never called for looping animations, nor when an animation is manually canceled via `spine.cancel()`. The callback can be used to trigger events on animation completion or to chain multiple animations together.

```lua
local function anim_done(self)
    -- the animation is done, do something useful...
end

function init(self)
    -- Play the "walk" animation on component "spinemodel" and blend against previous
    -- animation for the first 0.1 seconds, then call callback.
    local anim_props = { blend_duration = 0.1 }
    spine.play_anim("#spinemodel", "run", go.PLAYBACK_LOOP_FORWARD, anim_props, anim_done)
end
```


## Playback Modes

Animations can be played either once or in a loop. How the animation plays is determined by the playback mode:

* go.PLAYBACK_NONE
* go.PLAYBACK_ONCE_FORWARD
* go.PLAYBACK_ONCE_BACKWARD
* go.PLAYBACK_ONCE_PINGPONG
* go.PLAYBACK_LOOP_FORWARD
* go.PLAYBACK_LOOP_BACKWARD
* go.PLAYBACK_LOOP_PINGPONG

The pingpong modes run the animation first forward, then backward.
