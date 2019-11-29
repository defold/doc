---
title: Defold 动画教程
brief: 本教程介绍了 Defold 的动画支持.
---

# 动画

Defold 内置支持多种动画:

* 逐帧动画
* Spine 动画
* 3D 蒙皮动画
* 属性动画

## 逐帧动画

逐帧动画就是由一些列静态图片轮流显示生成的动画. 这种技术类似于老式翻页动画 (详见 http://en.wikipedia.org/wiki/Traditional_animation). 由于每帧的独立性使得这种技术很自由. 但是每帧一张图片会很耗费内存. 相似图片越多动画过渡越平滑同时也带来了巨大的工作量. Defold 逐帧动画使用来自于 [图集](/manuals/atlas), 或者 [瓷砖图源](/manuals/tilesource) 里水平排列的图片.

  ![Animation sheet](images/animation/animsheet.png){.inline}
  ![Run loop](images/animation/runloop.gif){.inline}

## Spine 动画

Spine 动画提供 2D _骨骼动画_ 支持 (详见 http://en.wikipedia.org/wiki/Skeletal_animation). 这是一种类似于剪裁动画的技术. 剪裁动画把对象分成各部分 (比如身体, 眼睛, 嘴巴之类的) 在每帧上独立运动. Spine 动画可以建立隐藏的, 树形关联的虚拟 _骨骼_. 骨架, 或称 _绑定_, 来为骨骼上添加的图片单独做动画. Defold 支持以 [Spine JSON 格式](http://esotericsoftware.com/spine-json-format) 输出的动画. Skeletal 动画都很平滑因为骨骼动画关键帧之间可以自动进行插值.

  关于导入 Spine 数据作为 Spine 模型和动画, 详见 [Spine 教程](/manuals/spine).

  ![Spine animation](images/animation/spine_animation.png){.inline}
  ![Run loop](images/animation/frog_runloop.gif){.inline}

## 3D 蒙皮动画

Skeletal animation of 3D models is similar to Spine animation but works in 3D as opposed to 2D. The 3D model is not cut into separate parts and tied to a bone like in cutout animation. Instead, the bones apply deformation to vertices in the model and you have great control over how much a bone should affect the vertices.

  For details on how to import 3D data into a Model for animation, see the [Model documentation](/manuals/model).

  ![Blender animation](images/animation/blender_animation.png){.inline srcset="images/animation/blender_animation@2x.png 2x"}
  ![Wiggle loop](images/animation/suzanne.gif){.inline}

## Property animation

All numeric properties (numbers, vector3, vector4 and quaterions) and shader constants can be animated with the built in animation system, using the function `go.animate()`. The engine will automatically "tween" properties for you according to given playback modes and easing functions. You can also specify custom easing functions.

  ![Property animation](images/animation/property_animation.png){.inline srcset="images/animation/property_animation@2x.png 2x"}
  ![Bounce loop](images/animation/bounce.gif){.inline}

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

When selecting an animation or image for a node, you are in fact assigning the image source (atlas or tile source) and default animation in one go. The image source is statically set in the node, but the current animation to play can be changed in runtime. Still images are treated as one frame animations so changing an image means in run time is equivalent to playing a different flip book animation for the node:

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

## Spine model animation

To run animations on your model, simply call the [`spine.play_anim()`](/ref/spine#spine.play_anim) function:

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

![Spine model in game](images/animation/spine_ingame.png){srcset="images/animation/spine_ingame@2x.png 2x"}

If an animation is played with any of the `go.PLAYBACK_ONCE_*` modes and you have provided a callback function to `spine.play_anim()` the callback is run on animation complete. See below for information on callbacks.

### Spine model - Cursor animation

In addition to using the `spine.play_anim()` to advance a spine animation, *Spine Model* components expose a "cursor" property that can be manipulated with `go.animate()`:

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

### Spine model - The bone hierarchy

The individual bones in the Spine skeleton are represented internally as game objects. In the *Outline* view of the Spine model component, the full hierarchy is visible. You can see each bone's name and its place in the skeleton hierarchy.

![Spine model hierarchy](images/animation/spine_bones.png){srcset="images/animation/spine_bones@2x.png 2x"}

With the bone name at hand, you are able to retrieve the instance id of the bone in runtime. The function [`spine.get_go()`](/ref/spine#spine.get_go) returns the id of the specified bone and you can, for instance, child other game objects under the animated game object:

```lua
-- Attach pistol game object to the hand of the heroine
local hand = spine.get_go("heroine#spinemodel", "front_hand")
msg.post("pistol", "set_parent", { parent_id = hand })
```

### Spine model - Timeline events

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

## 3D Model animation

Models are animated with the [`model.play_anim()`](/ref/model#model.play_anim) function:

```lua
function init(self)
    -- Start the "wiggle" animation back and forth on #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold currently supports only baked animations. Animations need to have matrices for each animated bone each keyframe, and not position, rotation and scale as separate keys.

Animations are also linearly interpolated. If you do more advanced curve interpolation the animations needs to be prebaked from the exporter.

Animation clips in Collada are not supported. To use multiple animations per model, export them into separate *.dae* files and gather the files into an *.animationset* file in Defold.
:::

### 3D Model - The bone hierarchy

The bones in the Model skeleton are represented internally as game objects.

You can retrieve the instance id of the bone game object in runtime. The function [`model.get_go()`](/ref/model#model.get_go) returns the id of the game object for the specified bone.

```lua
-- Get the middle bone go of our wiggler model
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Now do something useful with the game object...
```

### 3D Model - Cursor animation

Just like Spine models, 3D models can be animated by manipulating the `cursor` property:

```lua
-- Set the animation on #model but don't start it
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Set the cursor to the beginning of the animation
go.set("#model", "cursor", 0)
-- Tween the cursor between 0 and 1 pingpong with in-out quad easing.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Property animation

To animate a game object or component property, use the function `go.animate()`. For GUI node properties, the corresponding function is `gui.animate()`.

```lua
-- Set the position property y component to 200
go.set(".", "position.y", 200)
-- Then animate it
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

To stop all animations of a given property, call `go.cancel_animations()`, or for GUI nodes, `gui.cancel_animation()`:

```lua
-- Stop euler z rotation animation on the current game object
go.cancel_animation(".", "euler.z")
```

If you cancel the animation of a composite property, like `position`, any animations of the sub-components (`position.x`, `position.y` and `position.z`) will be cancelled as well.

The [Properties Manual](/manuals/properties) contains all the available properties on game objects, components and GUI nodes.

## GUI node property animation

Almost all GUI node properties are possible to animate. You can, for instance, make a node invisible by setting its `color` property to full transparency and then fade it into view by animating the color to white (i.e. no tint color).

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

## Playback Modes

Animations can be played either once or in a loop. How the animation plays is determined by the playback mode:

* go.PLAYBACK_NONE
* go.PLAYBACK_ONCE_FORWARD
* go.PLAYBACK_ONCE_BACKWARD
* go.PLAYBACK_ONCE_PINGPONG
* go.PLAYBACK_LOOP_FORWARD
* go.PLAYBACK_LOOP_BACKWARD
* go.PLAYBACK_LOOP_PINGPONG

The pingpong modes run the animation first forward, then backward. A set of corresponding modes exist for GUI property animations:

* gui.PLAYBACK_NONE
* gui.PLAYBACK_ONCE_FORWARD
* gui.PLAYBACK_ONCE_BACKWARD
* gui.PLAYBACK_ONCE_PINGPONG
* gui.PLAYBACK_LOOP_FORWARD
* gui.PLAYBACK_LOOP_BACKWARD
* gui.PLAYBACK_LOOP_PINGPONG

## Easing

Easing defines how the animated value changes over time. The images below describe the functions applied over time to create the easing.

The following are valid easing values for `go.animate()`:

|---|---|
| go.EASING_LINEAR | |
| go.EASING_INBACK | go.EASING_OUTBACK |
| go.EASING_INOUTBACK | go.EASING_OUTINBACK |
| go.EASING_INBOUNCE | go.EASING_OUTBOUNCE |
| go.EASING_INOUTBOUNCE | go.EASING_OUTINBOUNCE |
| go.EASING_INELASTIC | go.EASING_OUTELASTIC |
| go.EASING_INOUTELASTIC | go.EASING_OUTINELASTIC |
| go.EASING_INSINE | go.EASING_OUTSINE |
| go.EASING_INOUTSINE | go.EASING_OUTINSINE |
| go.EASING_INEXPO | go.EASING_OUTEXPO |
| go.EASING_INOUTEXPO | go.EASING_OUTINEXPO |
| go.EASING_INCIRC | go.EASING_OUTCIRC |
| go.EASING_INOUTCIRC | go.EASING_OUTINCIRC |
| go.EASING_INQUAD | go.EASING_OUTQUAD |
| go.EASING_INOUTQUAD | go.EASING_OUTINQUAD |
| go.EASING_INCUBIC | go.EASING_OUTCUBIC |
| go.EASING_INOUTCUBIC | go.EASING_OUTINCUBIC |
| go.EASING_INQUART | go.EASING_OUTQUART |
| go.EASING_INOUTQUART | go.EASING_OUTINQUART |
| go.EASING_INQUINT | go.EASING_OUTQUINT |
| go.EASING_INOUTQUINT | go.EASING_OUTINQUINT |

The following are valid easing values for `gui.animate()`:

|---|---|
| gui.EASING_LINEAR | |
| gui.EASING_INBACK | gui.EASING_OUTBACK |
| gui.EASING_INOUTBACK | gui.EASING_OUTINBACK |
| gui.EASING_INBOUNCE | gui.EASING_OUTBOUNCE |
| gui.EASING_INOUTBOUNCE | gui.EASING_OUTINBOUNCE |
| gui.EASING_INELASTIC | gui.EASING_OUTELASTIC |
| gui.EASING_INOUTELASTIC | gui.EASING_OUTINELASTIC |
| gui.EASING_INSINE | gui.EASING_OUTSINE |
| gui.EASING_INOUTSINE | gui.EASING_OUTINSINE |
| gui.EASING_INEXPO | gui.EASING_OUTEXPO |
| gui.EASING_INOUTEXPO | gui.EASING_OUTINEXPO |
| gui.EASING_INCIRC | gui.EASING_OUTCIRC |
| gui.EASING_INOUTCIRC | gui.EASING_OUTINCIRC |
| gui.EASING_INQUAD | gui.EASING_OUTQUAD |
| gui.EASING_INOUTQUAD | gui.EASING_OUTINQUAD |
| gui.EASING_INCUBIC | gui.EASING_OUTCUBIC |
| gui.EASING_INOUTCUBIC | gui.EASING_OUTINCUBIC |
| gui.EASING_INQUART | gui.EASING_OUTQUART |
| gui.EASING_INOUTQUART | gui.EASING_OUTINQUART |
| gui.EASING_INQUINT | gui.EASING_OUTQUINT |
| gui.EASING_INOUTQUINT | gui.EASING_OUTINQUINT |

<div id="game-container" class="game-container">
<canvas id="game-canvas" tabindex="1" width="640" height="512"></canvas>
<script src="//storage.googleapis.com/defold-doc/assets/easier/dmloader.js"></script>
<script>
  var extra_params = {
   archive_location_filter: function( path ) { return ('//storage.googleapis.com/defold-doc/assets/easier/archive' + path + ''); },
   splash_image: '//storage.googleapis.com/defold-doc/assets/easier/preview.jpg',
   custom_heap_size: 268435456,
   disable_context_menu: true,
   game_start: function() {}
  };
  Module['onRuntimeInitialized'] = function() { Module.runApp("game-canvas", extra_params); };
  Module['locateFile'] = function(path, scriptDirectory) {
   if (path == "dmengine.wasm" || path == "dmengine_release.wasm" || path == "dmengine_headless.wasm") { path = "easier.wasm"; }
   return scriptDirectory + path;
  };
  function load_engine() {
   var engineJS = document.createElement('script');
   engineJS.type = 'text/javascript';
   if (Module['isWASMSupported']) {
   engineJS.src = '//storage.googleapis.com/defold-doc/assets/easier/easier_wasm.js';
   } else {
   engineJS.src = '//storage.googleapis.com/defold-doc/assets/easier/easier_asmjs.js';
   }
   document.head.appendChild(engineJS);
  }
  load_engine();
</script>
</div>

![Linear interpolation](images/properties/easing_linear.png){.inline}
![In back](images/properties/easing_inback.png){.inline}
![Out back](images/properties/easing_outback.png){.inline}
![In-out back](images/properties/easing_inoutback.png){.inline}
![Out-in back](images/properties/easing_outinback.png){.inline}
![In bounce](images/properties/easing_inbounce.png){.inline}
![Out bounce](images/properties/easing_outbounce.png){.inline}
![In-out bounce](images/properties/easing_inoutbounce.png){.inline}
![Out-in bounce](images/properties/easing_outinbounce.png){.inline}
![In elastic](images/properties/easing_inelastic.png){.inline}
![Out elastic](images/properties/easing_outelastic.png){.inline}
![In-out elastic](images/properties/easing_inoutelastic.png){.inline}
![Out-in elastic](images/properties/easing_outinelastic.png){.inline}
![In sine](images/properties/easing_insine.png){.inline}
![Out sine](images/properties/easing_outsine.png){.inline}
![In-out sine](images/properties/easing_inoutsine.png){.inline}
![Out-in sine](images/properties/easing_outinsine.png){.inline}
![In exponential](images/properties/easing_inexpo.png){.inline}
![Out exponential](images/properties/easing_outexpo.png){.inline}
![In-out exponential](images/properties/easing_inoutexpo.png){.inline}
![Out-in exponential](images/properties/easing_outinexpo.png){.inline}
![In circlic](images/properties/easing_incirc.png){.inline}
![Out circlic](images/properties/easing_outcirc.png){.inline}
![In-out circlic](images/properties/easing_inoutcirc.png){.inline}
![Out-in circlic](images/properties/easing_outincirc.png){.inline}
![In quadratic](images/properties/easing_inquad.png){.inline}
![Out quadratic](images/properties/easing_outquad.png){.inline}
![In-out quadratic](images/properties/easing_inoutquad.png){.inline}
![Out-in quadratic](images/properties/easing_outinquad.png){.inline}
![In cubic](images/properties/easing_incubic.png){.inline}
![Out cubic](images/properties/easing_outcubic.png){.inline}
![In-out cubic](images/properties/easing_inoutcubic.png){.inline}
![Out-in cubic](images/properties/easing_outincubic.png){.inline}
![In quartic](images/properties/easing_inquart.png){.inline}
![Out quartic](images/properties/easing_outquart.png){.inline}
![In-out quartic](images/properties/easing_inoutquart.png){.inline}
![Out-in quartic](images/properties/easing_outinquart.png){.inline}
![In quintic](images/properties/easing_inquint.png){.inline}
![Out quintic](images/properties/easing_outquint.png){.inline}
![In-out quintic](images/properties/easing_inoutquint.png){.inline}
![Out-in quintic](images/properties/easing_outinquint.png){.inline}

## Custom easing

You can create custom easing curves by defining a `vector` with a set of values and then provide the vector instead of one of the predefined easing constants above. The vector values express a curve from the start value (`0`) to the target value (`1`). The runtime samples values from the vector and linearly interpolates when calculating values in between the points expressed in the vector.

For example, the vector:

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5. 1 }
local my_easing = vmath.vector(values)
```

yields the following curve:

![Custom curve](images/animation/custom_curve.png)

The following example causes the y position of a game object to jump between the current position and 200 according to a square curve:

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

![Square curve](images/animation/square_curve.png)

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