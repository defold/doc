---
title: 3D models in Defold
brief: This manual describes how to bring 3D models, skeletons and animations into your game.
---

# Model component

Defold is at its core a 3D engine. Even when you work with 2D material only all rendering is done in 3D, but orthographically projected onto the screen. Defold allows you to utilize full 3D content by including 3D assets, or _Models_ into your collections. You can build games in strictly 3D with only 3D assets, or you can mix 3D and 2D content as you wish.

## Creating a model component

Model components are created just like any other game object component. You can do it two ways:

- Create a *Model file* by <kbd>right-clicking</kbd> a location in the *Assets* browser and select <kbd>New... ▸ Model</kbd>.
- Create the component embedded directly into a game object by <kbd>right-clicking</kbd> a game object in the *Outline* view and selecting <kbd>Add Component ▸ Model</kbd>.

![Model in game object](images/model/model_gltf.png)

With the model created you need to specify a number of properties:

### Model properties

Apart from the properties *Id*, *Position* and *Rotation* the following component specific properties exist:

*Mesh*
: This property should refer to the glTF *.gltf* or *.glb* file that contains the mesh to use. If the file contains morph targets, they are imported together with the mesh. If the file contains multiple meshes, only the first one is read.

*Create GO Bones*
: Check this to create a game object for every bone of the model. You can use the game objects to attach other game objects such as weapons to hand bones and so on. 

*Skeleton*
: This property should refer to the glTF *.gltf* or *.glb* file that contains the skeleton to use for animation. Note that Defold requires a single root bone in your hierarchy.

*Animations*
: Set this to the *Animation Set File* that contains the animations you want to use on the model.

*Default Animation*
: This is the animation (from the animation set) that will be automatically played on the model.

In addition to the properties above there will also be a field to assign a material for every mesh of the model:

*Material*
: Set this property to a material you have created that is suitable for a textured 3D object. There are a number of built-in materials that you can use as a starting point:

  * Use *model.material* for static non-instanced models
  * Use *model_instanced.material* for static instanced models
  * Use *model_skinned.material* for skinned (animated) non-instanced models
  * Use *model_skinned_instanced.material* for skinned (animated) instanced models

Depending on the material there will be one or more texture properties:

*Texture*
: This property should point to the texture image file that you want applied to the object.


## Editor manipulation

With the model component in place you are free to edit and manipulate the component and/or the encapsulating game object with the regular *Scene Editor* tools to move, rotate and scale the model to your liking.

## Runtime manipulation

You can manipulate models in runtime through a number of different functions and properties (refer to the [API docs for usage](/ref/model/)).

![Wiggler ingame](images/model/runtime.png)

### Runtime animation

Defold provides powerful support for controlling animation in runtime. More in the [model animation manual](/manuals/model-animation):

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

The animation playback cursor can be animated either by hand or through the property animation system:

```lua
-- set the run animation
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- animate the cursor
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

Models can also use glTF morph target animations. Morph target weights are animated with `model.play_anim()` like other model animations, and can be read or overridden at runtime using [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) and [`model.set_blend_weights()`](/ref/model#model.set_blend_weights). See the [morph targets section](/manuals/model-animation#morph-targets) in the model animation manual for details.

### Changing properties

A model also has a number of different properties that can be manipulated using `go.get()` and `go.set()`:

`animation`
: The current model animation (`hash`) (READ ONLY). You change animation using `model.play_anim()` (see above).

`cursor`
: The normalized animation cursor (`number`).

`material`
: The model material (`hash`). You can change this using a material resource property and `go.set()`. Refer to the [API reference for an example](/ref/model/#material).

`playback_rate`
: The animation playback rate (`number`).

`textureN`
: The model textures where N is 0-15 (`hash`). You can read these properties with `go.get()` and change them using a texture resource property and `go.set()`. Defold supports at most 16 textures per draw, but the number usable by a shader may be lower on graphics adapters with a smaller texture-sampler limit.


## Material

3D software commonly allows you to set properties on your object vertices, like coloring and texturing. This information goes into the glTF *.gltf* or *.glb* file that you export from your 3D software. Depending on the requirements of your game you will have to select and/or create appropriate and _performant_ materials for your objects. A material combines _shader programs_ with a set of parameters for rendering of the object.

There are a number of built-in materials that you can use as a starting point:

  * Use *model.material* for static non-instanced models
  * Use *model_instanced.material* for static instanced models
  * Use *model_skinned.material* for skinned (animated) non-instanced models
  * Use *model_skinned_instanced.material* for skinned (animated) instanced models

The built-in model materials use local vertex space. For skinned models, local vertex space allows the vertex shader to perform skinning on the GPU using a bone-matrix texture; local vertex space is also required for model instancing. A custom material intended for GPU-skinned or instanced models should therefore use the *Local* vertex-space setting.

The bone-matrix cache uses an `RGBA32F` texture. If the active graphics adapter does not support that texture format, Defold cannot create an animated Model component that uses a local-space material. On OpenGL ES 2.0 and WebGL 1.0, support therefore depends on the adapter's floating-point texture extension. For compatibility with an adapter that lacks it, use a custom world-space material, which uses CPU skinning and cannot use model instancing. The cache dimensions can be adjusted with the [Model project settings](/manuals/project-settings/#model).

If you need to create custom materials for your models, see the [Material documentation](/manuals/material) for information. The [Shader manual](/manuals/shader) contains information on how shader programs work.


### Material constants

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: The color tint of the model (`vector4`). The `vector4` is used to represent the tint with x, y, z, and w corresponding to the red, green, blue and alpha tint.


## Rendering

The default render script is tailor made for 2D games and does not work with 3D models. But by copying the default render script and adding a handful of lines of code to the render script you can enable rendering of your models. For instance:

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- orthographic
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

See the [Render documentation](/manuals/render) for details on how render scripts work.
