---
title: GUI box nodes in Defold
brief: This manual explains how to use GUI box nodes.
---

# GUI box nodes

A box node is a rectangle filled with a color or a texture or animation.

## Adding box nodes

Add new box nodes by either <kbd>right clicking</kbd> in the *Outline* and selecting <kbd>Add ▸ Box</kbd>, or press <kbd>A</kbd> and select <kbd>Box</kbd>.

You can use images and animations from atlases or tile sources that has been added to the GUI. You add textures by <kbd>right clicking</kbd> the *Textures* folder icon in the *Outline* and selecting <kbd>Add ▸ Textures...</kbd>. Then set the *Texture* property on the box node:

![Textures](images/gui-box/create.png){srcset="images/gui-box/create@2x.png 2x"}

Note that the color of the box node will tint the graphics. The tint color is multiplied onto the image data, meaning that if you set the color to white (the default) no tint is applied.

![Tinted texture](images/gui-box/tinted.png){srcset="images/gui-box/tinted@2x.png 2x"}

Box nodes are always rendered, even if they do not have a texture assigned to them, or have their alpha set to `0`, or are sized `0, 0, 0`. Box nodes should always have a texture assigned to them so the renderer can batch them properly and reduce the number of draw-calls.

## Slice-9 texturing

GUIs often feature elements that are context sensitive in regard to their size: panels and dialogs that need to be resized to fit the containing content. These may cause visual problems when you apply texturing to the resized node.

Normally, the engine scales the texture to fit the boundaries of a box node, but by defining slice-9 edge areas it is possible to limit what parts of the texture that should scale:

![GUI scaling](images/gui-box/scaling.png){srcset="images/gui-box/scaling@2x.png 2x"}

The *Slice9* box node consists of 4 numbers that specify the number of pixels for the left, top, right and bottom margin that should not be regularly scaled:

![Slice 9 properties](images/gui-box/slice9_properties.png){srcset="images/gui-box/slice9_properties@2x.png 2x"}

The margins are set clockwise, starting on the left edge:

![Slice 9 sections](images/gui-box/slice9.png){srcset="images/gui-box/slice9@2x.png 2x"}

- Corner segments are never scaled.
- Edge segments are scaled along a sigle axis. The left and right edge segments are scaled vertically. The top and bottom edge segments are scaled horizontally.
- The central texture area is scaled horizontally and vertically as needed.

Due to the way mipmapping works in the renderer, scaling of texture segments can sometimes exhibit artifacts. This happens when you _scale down_ segments below the original texture size. The renderer then selects a lower resolution mipmap for the segment, resulting in visual artifacts.

![Slice 9 mipmapping](images/gui-box/mipmap.png){srcset="images/gui-box/mipmap@2x.png 2x"}

To avoid this problem, make sure that the texture's segments that will be scaled are small enough never to be scaled down, only up.
