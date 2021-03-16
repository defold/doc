---
title: 3D model animation in Defold manual
brief: This manual describes how to use 3D model animations in Defold.
---

# 3D skinned animation

Skeletal animation of 3D models is similar to [Spine animation](/manuals/spine-animation) but works in 3D as opposed to 2D. The 3D model is not cut into separate parts and tied to a bone like in cutout animation. Instead, the bones apply deformation to vertices in the model and you have great control over how much a bone should affect the vertices.

For details on how to import 3D data into a Model for animation, see the [Model documentation](/manuals/model).

  ![Blender animation](images/animation/blender_animation.png){.inline srcset="images/animation/blender_animation@2x.png 2x"}
  ![Wiggle loop](images/animation/suzanne.gif){.inline}


## Playing animations

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

### The bone hierarchy

The bones in the Model skeleton are represented internally as game objects.

You can retrieve the instance id of the bone game object in runtime. The function [`model.get_go()`](/ref/model#model.get_go) returns the id of the game object for the specified bone.

```lua
-- Get the middle bone go of our wiggler model
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Now do something useful with the game object...
```

### Cursor animation

In addition to using the `model.play_anim()` to advance a model animation, *Model* components expose a "cursor" property that can be manipulated with `go.animate()` (more about [property animations](/manuals/property-animation)):

```lua
-- Set the animation on #model but don't start it
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Set the cursor to the beginning of the animation
go.set("#model", "cursor", 0)
-- Tween the cursor between 0 and 1 pingpong with in-out quad easing.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Completion callbacks

The model animation `model.play_anim()`) support an optional Lua callback function as the last argument. This function will be called when the animation has played to the end. The function is never called for looping animations, nor when an animation is manually canceled via `go.cancel_animations()`. The callback can be used to trigger events on animation completion or to chain multiple animations together.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Done animating
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
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
