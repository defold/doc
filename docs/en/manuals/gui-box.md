---
title: GUI box nodes in Defold
brief: This manual explains how to use GUI box nodes.
---

# GUI box nodes

A box node is a rectangle filled with a color or a texture or animation.

## Adding box nodes

Add new box nodes by either <kbd>right clicking</kbd> in the *Outline* and selecting <kbd>Add ▸ Box</kbd>, or press <kbd>A</kbd> and select <kbd>Box</kbd>.

You can use images and animations from atlases or tile sources that has been added to the GUI. You add textures by <kbd>right clicking</kbd> the *Textures* folder icon in the *Outline* and selecting <kbd>Add ▸ Textures...</kbd>. Then set the *Texture* property on the box node:

![Textures](images/gui-box/create.png)

Note that the color of the box node will tint the graphics. The tint color is multiplied onto the image data, meaning that if you set the color to white (the default) no tint is applied.

![Tinted texture](images/gui-box/tinted.png)

Box nodes are always rendered, even if they do not have a texture assigned to them, or have their alpha set to `0`, or are sized `0, 0, 0`. Box nodes should always have a texture assigned to them so the renderer can batch them properly and reduce the number of draw-calls.

## Playing animations

Box nodes can play animations from atlases or tile sources. Refer to the [flipbook animation manual](/manuals/flipbook-animation) to learn more.

:[Slice-9](../shared/slice-9-texturing.md)