---
title: Defold 2D graphics manual
brief: This manual outlines Defold's support for 2D graphical elements.
---

# 2D Graphics

Defold is a full 3D engine, but it is designed and built with strong support for 2D games. The editor is currently best suited for making 2D games. 

In Defold, there are two types of asset that represent such a larger image:

![atlas](images/icons/atlas.png){.icon} Atlas
: An atlas contains a list of separate images files, which are automatically combined into a larger image.

![tile source](images/icons/tilesource.png){.icon} Tile Source
: A tile source references an image file that is already containing sub-images ordered on a uniform grid. Another term commonly used for this type of compound image is _sprite sheet_.



![sprite](images/icons/sprite.png){.icon}

![tile map](images/icons/tilemap.png){.icon} Tilemap
: A tilemap component

![particle effect](images/icons/particlefx.png){.icon} Particle fx
: 

![gui](images/icons/gui.png){.icon}


## Importing Image Files

Defold needs all assets that should be in your project hierarchy. Therefore you should start by importing the image files you want to build your graphics from. To import image assets, simply drag the files from the file system on your computer and drop them in an appropriate place in the Defold editor _Project Explorer_.

::: important
Currently, Defold supports the PNG and JPEG image formats.
:::

![Importing image files](images/2dgraphics/import.png){srcset="images/2dgraphics/import@2x.png 2x"}

## Manipulating Game Objects and components

When you add visual components (Sprites, ParticleFX, etc) to a game object, you are able to set the _position_ and _rotation_ of the component. These values are used as offsets against the position and rotation of the game object. What's more, the values are _set_ in the component when you assemble the game object.

![Component position](images/2dgraphics/2dgraphics_component_position.png)

Defold game objects can be moved, rotated, and have any of their properties animated. Components belonging to a manipulated game object undergo the same manipulations as the game object, but will keep their relative position and rotation as set in the game object. Components can be turned on and off, but it's not possible to animate, move, or rotate them dynamically (with an exception described below). Therefore, if you have graphics that you intend to alter you should put the graphics in separate game objects. A group of game objects or a game object hierarchy is conveniently assembled in a Collection. Then you can freely manipulate the objects through script:

![Component position](images/2dgraphics/2dgraphics_gameobject_position.png)

```lua
-- Animate the wand game object to specified position and rotation.
go.animate("wand", "position", go.PLAYBACK_ONCE_FORWARD, vmath.vector3(530, 79, -0.1), go.EASING_INOUTSINE, 0.5)
go.animate("wand", "euler", go.PLAYBACK_ONCE_FORWARD, vmath.vector3(0, 0, -70), go.EASING_INOUTSINE, 0.5)
```


## Blend modes

The *Blend Mode* property defines how the sprite should be blended with the graphics behind it. These are the available blend modes and how they are calculated:

Alpha
: Normal blending: a~0~ * rgb~0~ + (1 - a~0~) * rgb~1~

Add
: Brighten the background with the color values of the corresponding sprite pixels: rgb~0~ + rgb~1~

Add Alpha (deprecated!)
: Brighten the background with the corresponding visible sprite pixels: a~0~ * rgb~0~ + rgb~1~

Multiply
: Darken the background with values of the the corresponding sprite pixels: rgb~0~ * rgb~1~

## Shading

The default sprite shading files are located under */builtins/material/sprite.\** in your project. The default shading performs a regular texture lookup, but also has a tint (a fragment shader constant) which is multiplied with the texture color.

To obtain effects like flashing a sprite white when it is hit, you can implement custom shading. To set a custom shading for your sprites, follow these steps:

- Copy the files under */builtins/material/sprite.\** into one of your project directories (you can't modify the content of the *builtins*-directory). This is not mandatory but makes the process easier.
- Open the copied *sprite.material* file and remap the shader files (*.vp* and *.fp*) to your own copies.
- Edit the *.vp* and *.fp* copies as you please. If you introduce shader constants, they must also be declared in the material file.
- Open your sprite and specify your new material in the Properties.
- To set a shader constant while the game is running, use the functions [`sprite.set_constant()`](/ref/sprite#sprite.set_constant) and [`sprite.reset_constant()`](/ref/sprite#sprite.reset_constant).

## Texture Filtering and Sampling

Defold supports two different ways to do texture sampling. The method governs the visual result in cases when a _texel_ (a pixel in a texture) is not perfectly aligned with a screen pixel. This happens when you move a Sprite containing the texture seamlessly (say 0.2 pixels in any direction), if your camera is moving seamlessly or if your camera zooms in or out:

Nearest
: The nearest texel will be picked to color the screen pixel. This sampling method should be chosen if you want a perfect one-to-one pixel mapping from your textures to what you see on screen. With nearest filtering everything will snap from pixel to pixel when moving which looks twitchy if the Sprite moves slowly.


Linear
: The texel will be averaged with its neighbors before coloring the screen pixel. This produces smooth appearances for slow, continuous motions as a Sprite will bleed into the pixels before fully coloring them--thus it is possible to move a Sprite less than a whole pixel.


The setting for which filtering to use is stored in the [Project Settings](/manuals/project-settings) file. There are two settings:

default_texture_min_filter
: Minifying filtering applies whenever the texel is smaller than the screen pixel.

default_texture_mag_filter
: Magnifying filtering applies whenever the texel is larger than the screen pixel.

Both settings accept the values `linear` or `nearest`. For example:

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

If you don’t specify anything, both are set to `linear` by default.
