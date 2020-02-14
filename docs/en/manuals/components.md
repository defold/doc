---
title: Game object components
brief: This manual gives an overview of the components and how to use them.
---

#  Components

:[components](../shared/components.md)

## Component types

Defold supports the following component types:

* [Collection factory](/manuals/collection-factory) - Spawn collections
* [Collection proxy](/manuals/collection-proxy) - Load and unload collections
* [Collision object](/manuals/physics) - 2D and 3D physics
* [Camera](/manuals/camera) - Change the viewport and projection of the game world
* [Factory](/manuals/factory) - Spawn game objects
* [GUI](/manuals/gui) - Render a graphical user interface
* [Label](/manuals/label) - Render a piece of text
* [Model](/manuals/model) Show a 3D model (with optional animations)
* [Particle FX](/manuals/particlefx) -  Spawn particles
* [Script](/manuals/script) - Add game logic
* [Sound](/manuals/sound) - Play sound or music
* [Spine model](/manuals/spinemodel) - Render a spine animation
* [Sprite](/manuals/sprite) - Show a 2D image (with optional flipbook animation)
* [Tilemap](/manuals/tilemap) - Show a grid of tiles

## Enabling and disabling components

The components of a game object are enabled when the game object is created. If you wish to disable a component this is done by sending a [`disable`](/ref/go/#disable) message to the component:

```lua
-- disable the component with id 'weapon' on the same game object as this script
msg.post("#weapon", "disable")

-- disable the component with id 'shield' on the 'enemy' game object
msg.post("enemy#shield", "disable")

-- disable all components on the current game object
msg.post(".", "disable")

-- disable all components on the 'enemy' game object
msg.post("enemy", "disable")
```

To enable a component again you can post an [`enable`](/ref/go/#enable) message to the component:

```lua
-- enable the component with id 'weapon'
msg.post("#weapon", "enable")
```

## Component properties

The Defold components types all have different properties. The [Properties pane](/manuals/editor/#the-editor-views) in the editor will show the properties of the currently selected component in the [Outline pane](/manuals/editor/#the-editor-views). Refer to the manuals of the different component types to learn more about the available component properties.

## Component position, rotation and scale

Visual components usually have a position and rotation property and most often also a scale property. These properties can be changed from the editor and in almost all cases the properties can't be changed at run-time (the only exception is sprite and label component scale which can be changed at run-time).

If you need to change the position, rotation or scale of a component at run-time you instead modify the position, rotation or scale of the game object that the component belongs to. This has the side effect that all components on the game object will be affected. If you wish to only manipulate a single component out of many attached to a game object it is recommended that the component in question is moved to a separate game object and added as a child game object to the game object the component originally belonged to.

## Component draw order

The draw order of visual components depend on two things:

### Render script predicates
Each component is assigned a [material](/manuals/material/) and each material has one or more tags. The render script will in turn define a number of predicates, each matching one or more material tags. The render script [predicates are drawn one by one](/manuals/render/#render-predicates) in the *update()* function of the render script and the components matching the tags defined in each predicate will be drawn. The default render script will first draw sprites and tilemaps in one pass, then particle effects in another pass, both in world space. The render script will then proceed to draw GUI components in a separate pass in screen space.

### Component z-value
All game objects and components are positioned in 3D space with positions expressed as vector3 objects. When you view your game's graphics content in 2D, the X and Y value determine the position of an object along the "width" and "height" axis, and the Z position determines the position along the "depth" axis. The Z position allows you to control the visibility of overlapping objects: a sprite with a Z value of 1 will appear in front of a sprite at Z position 0. By default, Defold uses a coordinate system allowing Z values between -1 and 1:

![model](images/graphics/z-order.png){srcset="images/graphics/z-order@2x.png 2x"}

The components matching a [render predicate](/manuals/render/#render-predicates) are drawn together, and the order in which they are drawn depends on the final z-value of the component. The final z-value of a component is the sum of the z-values of the component itself, the game object it belongs to and the z-value of any parent game objects.

::: sidenote
The order in which multiple GUI components are drawn is **not** determined by the z-value of the GUI components. GUI component draw order is controlled by the [gui.set_render_order()](/ref/gui/#gui.set_render_order:order) function.
:::

Example: Two game objects A and B. B is a child of A. B has a sprite component.

| What     | Z-value |
|----------|---------|
| A        | 2       |
| B        | 1       |
| B#sprite | 0.5     |

With the above hierarchy the final z-value of the sprite component on B is 2 + 1 + 0.5 = 2.5.

::: important
If two components have the exact same z-value the order is undefined and you may end up with components flickering back and forth or components being rendered in one order on one platform and in another order on another platform.

The render script defines a near and far plane for z-values. Any component with a z-value that falls outside of this range will not be rendered. The default range is -1 to 1 but [it can easily be changed](/manuals/render/#default-view-projection). The numerical precision on the Z values with a near and far limit of -1 and 1 is very high. When working with 3D assets, you may need to change the near and far limits of the default projection in a custom render script. See the [Render manual](/manuals/render/) for more information.
:::
