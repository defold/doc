---
title: Showing 2D images
brief: This manual describes how to show 2D images and animations using the sprite component.
---

#  Sprites

A Sprite component is a simple image or flipbook animation that is displayed on screen.

![sprite](images/graphics/sprite.png){srcset="images/graphics/sprite@2x.png 2x"}

The Sprite component can use either an [Atlas](/manuals/atlas) or a [Tile Source](/manuals/tilesource) for it's graphics.

## Sprite properties

Apart from the properties *Id*, *Position* and *Rotation* the following component specific properties exist:

*Image*
: The atlas or tilesource resource to use for the sprite.

*DefaultAnimation*
: The animation to use for the sprite.

*Material*
: The material to use for rendering the sprite.

*Blend Mode*
: The blend mode to use when rendering the sprite.

### Blend modes
:[blend-modes](../shared/blend-modes.md)

## Runtime manipulation

You can manipulate sprites in runtime through a number of different functions and properties (refer to the [API docs for usage](/ref/sprite/)). Functions:

* `sprite.play_flipbook()` - Play an animation on a sprite component.
* `sprite.set_hflip()` and `sprite.set_vflip()` - Set horizontal and vertical flipping on a sprite's animation.

A sprite also has a number of different properties that can be manipulated using `go.get()` and `go.set()`:

`cursor`
: The normalized animation cursor (`number`).

`image`
: The sprite image (`hash`). You can change this using an atlas or tile source resource property and `go.set()`. Refer to the [API reference for an example](/ref/sprite/#image).

`material`
: The sprite material (`hash`). You can change this using a material resource property and `go.set()`. Refer to the [API reference for an example](/ref/sprite/#material).

`playback_rate`
: The animation playback rate (`number`).

`scale`
: The non-uniform scale of the sprite (`vector3`).

`size`
: The size of the sprite (`vector3`) (READ ONLY).

## Material constants

The default sprite material has the following constants that can be changed using `sprite.set_constant()` and reset using `sprite.reset_constant()` (refer to the [Material manual for more details](/manuals/material/#vertex-and-fragment-constants)):

`tint`
: The color tint of the sprite (`vector4`). The vector4 is used to represent the tint with x, y, z, and w corresponding to the red, green, blue and alpha tint. Refer to the [API reference for an example](/ref/sprite/#sprite.set_constant:url-constant-value).
