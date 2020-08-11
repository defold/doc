---
title: Texture filtering
brief: This manual describes the available options for texture filtering when rendering graphics.
---

# Texture filtering and sampling

Texture filtering decides the visual result in cases when a _texel_ (a pixel in a texture) is not perfectly aligned with a screen pixel. This happens when you move a graphical element that contains the texture less than a pixel. The following filter methods are available:

Nearest
: The nearest texel will be picked to color the screen pixel. This sampling method should be chosen if you want a perfect one-to-one pixel mapping from your textures to what you see on screen. With nearest filtering everything will snap from pixel to pixel when moving. This may  look twitchy if the Sprite moves slowly.

Linear
: The texel will be averaged with its neighbors before coloring the screen pixel. This produces smooth appearances for slow, continuous motions as a Sprite will bleed into the pixels before fully coloring them--thus it is possible to move a Sprite less than a whole pixel.

The setting for which filtering to use is stored in the [Project Settings](/manuals/project-settings/#graphics) file. There are two settings:

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

Note that the setting in "game.project" is used by in the default samplers. If you specify samplers in a custom material, you can set the filter method on each sampler specifically. See the [Materials manual](/manuals/material/) for details.
