---
title: GUI box nodes in Defold
brief: This manual explains how to use GUI box nodes.
---

# GUI box nodes

A box node is a rectangle filled with a color or a texture or animation. Box nodes have the following special properties:


## Textures and flip book animations

You can use images and animations from texture atlases or tile sources as part of your GUI interface component. To do so, an image resource (atlas or tile source) must first be added, then all images and animations included in the resource can be applied to GUI nodes. You add textures either by right clicking the *Textures* folder, through the <kbd>GUI</kbd> top menu, or with keyboard shortcuts.

Textures that have been added to the GUI can be applied to box and pie nodes.

![Textures](images/gui/gui_texture.png)

The selected texture animation (or single frame image) will automatically play when the GUI component is drawn on screen.

Note that the color of the box node will tint the animation. The tint color is multiplied onto the image data, meaning that if you set the color to white (the default) no tint is applied.

![Tinted texture](images/gui/gui_tinted_texture.png)

::: sidenote
Box nodes are always rendered, even if they do not have a texture assigned to them, have their alpha set to `0`, or are sized `0, 0, 0`. Box nodes should always have a texture assigned to them so the renderer can batch them properly and reduce the number of draw-calls.
:::

## Slice-9 texturing

Many GUIs and HUDs feature elements that are context sensitive in regard to their size. Panels and dialogs often need to be resized to fit the containing content and that will cause problems as soon as you apply texturing to the scaled node. Let's say that you want to use a large set of buttons where the width is determined by the amount of text you write on the button. Making a box node, applying a texture and then scaling it will result in deformation:

![GUI bad scaling](images/gui/gui_scaling.png)

Defold contains a feature called _slice-9_ texturing that is intended to be used in situations like this. It works by allowing you to preserve the size of parts of the node texture when the node is scaled. A button texture is divided into bits and applied to the node so that the end bits don't scale as you change the horizontal size of the button node:

![Sliced scaling](images/gui/gui_slice9_scaling.png)

You can thus make buttons of any width using this simple technique. The *Slice9* box node property is used to control how the texture is sliced:

![Slice 9 properties](images/gui/gui_slice9_properties.png)

The slicing is controlled by 4 numbers that specify the margin width, in pixels, which will be preserved as the node is resized. Corner segments are never scaled, only moved; edge segments are scaled along one axis, and the center segment is scaled both horizontally and vertically as needed. The margins are set clockwise, starting on the left hand side:

![Slice 9 property sections](images/gui/gui_slice9_sections.png)

Due to the way mipmapping works in the renderer, scaling of texture segments can sometimes look incorrect. This happens when you _scale down_ segments below the original texture size. The renderer then selects a lower resolution mipmap for the segment, resulting in visual artifacts.

![Slice 9 mipmapping](images/gui/gui_slice9_mipmap.png)

It is easy to avoid this problem, but it implies some constraints to the source texture: simply make sure that the texture's segments that will be scaled are small enough never to be scaled down, only up.

::: sidenote
It might also be tempting to use a 1 pixel wide bottom or top edge segment to save texture memory. However, doing so might result in other unwanted artifacts, because of texture filtering. If you make the edge wider so that edge segments start and stop with similar neighbor pixels you will typically get nicer results.
:::



