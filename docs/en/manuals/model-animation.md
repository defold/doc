---
title: 3D model animation in Defold manual
brief: This manual describes how to use 3D model animations in Defold.
---

# 3D model animation

Model components can play skeletal animations and morph target animations imported from glTF files. Skeletal animation uses the bones of the model to apply deformation to vertices in the model. Morph target animation, also known as blend shape animation, changes the shape of the model by animating weights for alternate vertex positions.

For details on how to import 3D data into a Model for animation, see the [Model documentation](/manuals/model).

  ![Blender animation](images/animation/blender_animation.png)
  ![Wiggle loop](images/animation/suzanne.gif)


## Playing animations

Models are animated with the [`model.play_anim()`](/ref/model#model.play_anim) function:

```lua
function init(self)
    -- Start the "wiggle" animation back and forth on #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold currently supports only baked skeletal animations. Skeletal animations need to have matrices for each animated bone each keyframe, and not position, rotation and scale as separate keys.

Animations are also linearly interpolated. If you do more advanced curve interpolation the animations needs to be prebaked from the exporter.
:::

### Morph targets

Morph targets are alternative shapes for the same mesh. Each target stores vertex deltas, and each target has a blend weight that controls how much of that shape is applied. A weight of `0` means that the target has no effect, while a weight of `1` applies the full target shape. Values outside that range can also be useful for exaggerated effects if the shader and asset are authored for it.

Defold imports morph targets and initial morph weights from glTF model data. glTF animations that animate morph weights are imported into the model animation set and can be played with [`model.play_anim()`](/ref/model#model.play_anim), just like skeletal animations:

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

Morph target animations can be used on their own or together with skeletal animation. If a model has animation data but no skeleton, only morph target animation data will be used.

You can also read and override morph target weights from script. [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) returns the current weights for the first mesh in the model that has morph targets. [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) applies a script override to every morphed mesh in the model:

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

The weight table uses one-based Lua indices in the same order as the morph targets in the mesh. Extra values are ignored, and missing values are treated as zero for meshes with more morph targets than the table contains. The script override is applied after animation every frame until it is cleared:

```lua
model.set_blend_weights("#model")     -- clear the override
model.set_blend_weights("#model", nil) -- also clears the override
```

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

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
