---
title: Properties in Defold
brief: This manual explains what types of properties exist in Defold, and how they are used and animated.
---

# Properties

Defold exposes properties for game objects, components and GUI nodes that can be read, set and animated. The following types of properties exist:

* System defined game object transforms (position, rotation and scale) and component specific properties (for example a sprite's pixel size or a collision object's mass)
* User defined script component properties defined in Lua scripts (see [Script properties documentation](/manuals/script-properties) for details)
* GUI node properties
* Shader constants defined in shaders and material files (see [Material documentation](/manuals/material) for details)

Depending on where a property is found, you access it via a generic function, or a property-specific function. Many of the properties can be automatically animated. Animating properties through the built-in system is highly recommended over manipulating the properties yourself (inside an `update()` function), both for performance reasons as well as convenience.

Composite properties of type `vector3`, `vector4` or `quaternion` also expose their sub-components (`x`, `y`, `z` and `w`). You can address the components individually by suffixing the name with a dot (`.`) and the name of the component. For example, to set the x-component of a game object's position:

```lua
-- Set the x positon of "game_object" to 10.
go.set("game_object", "position.x", 10)
```

The functions `go.get()`, `go.set()` and `go.animate()` take a reference as their first parameter and a property identifier as their second. The reference identifies the game object or component and can be a string, a hash or a URL. URLs are explained in detail in the [addressing manual](/manuals/addressing). The property identifier is a string or hash that names the property:

```lua
-- Set the x-scale of the sprite component
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

For GUI nodes, the node identifier is provided as the first parameter to the property specific function:

```lua
-- Get the color of the button
local node = gui.get_node("button")
local color = gui.get_color(node)
```

## Game object and component properties

All game objects, and some component types have properties that can be read and manipulated in runtime. Read these values with [`go.get()`](/ref/go#go.get) and write them with [`go.set()`](/ref/go#go.set). Depending on the property value type, you can animate the values with [`go.animate()`](/ref/go#go.animate). A small set of the properties are read only.

`get`{.mark}
: Can be read with [`go.get()`](/ref/go#go.get).

`get+set`{.mark}
: Can be read with [`go.get()`](/ref/go#go.get) and written with [`go.set()`](/ref/go#go.set). Numerical values can be animated with [`go.animate()`](/ref/go#go.animate).

::: sidenote
Legacy functions for reading and writing game object properties also exist. They are `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`,  and so forth.
:::

*GAME OBJECT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | The local position of the game object. | `vector3`      | `get+set`{.mark} |
| *rotation* | Local rotation of game object, expressed as a quaternion.  | `quaternion` | `get+set`{.mark} |
| *euler*    | Local rotation of game object, Euler angles. | `vector3` | `get+set`{.mark} |
| *scale*    | Local non uniform scale of the game object, expressed as a vector where each component contains a multiplier along each axis. To double the size in x and y, provide vmath.vector3(2.0, 2.0, 0) | `vector3` | `get+set`{.mark} |

*SPRITE COMPONENT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | The non scaled size of the sprite---its size as taken from the source atlas. | `vector3` | `get`{.mark} |
| *texture0* | The texture path hash of the sprite. | `hash` | `get`{.mark}|
| *scale* | Non uniform scale of the sprite. | `vector3` | `get+set`{.mark}|

*COLLISION OBJECT COMPONENT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | The mass of the collision object. | `number` | `get`{.mark} |
| *linear_velocity* | The current linear velocity of the collision object. | `vector3` | `get`{.mark} |
| *angular_velocity* | The current angular velocity of the collision object. | `vector3` | `get`{.mark} |
| *linear_damping* | Linear damping of the collision object. | `vector3` | `get+set`{.mark} |
| *angular_damping* | Angular damping of the collision object. | `vector3` | `get+set`{.mark} |

*SPINE MODEL COMPONENT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | The current animation. | `hash` | `get`{.mark} |
| *skin*     | The currently applied model skin. (cannot be animated!) | `hash` | `get+set`{.mark} |
| *cursor*   | The current position (between 0-1) of the animation playback cursor. | `number` | `get+set`{.mark} |
| *playback_rate* | The playback rate of the animation. A multiplier to the animation playback rate. | `number` | `get+set`{.mark} |

*MODEL (3D) COMPONENT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | The current animation.                | `hash`          | `get`{.mark}     |
| *texture0* | The texture path hash of the model. | `hash` | `get`{.mark}|
| *cursor*  | Position (between 0--1) of playback cursor. | `number`   | `get+set`{.mark} |
| *playback_rate* | The playback rate of the animation. A multiplier to the animation playback rate. | `number` | `get+set`{.mark} |

*LABEL COMPONENT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *scale* | The scale of the label. | `vector3` | `get+set`{.mark} |
| *color*     | The color of the label. | `vector4` | `get+set`{.mark} |
| *outline* | The outline color of the label. | `vector4` | `get+set`{.mark} |
| *shadow* | The shadow color of the label. | `vector4` | `get+set`{.mark} |
| *size* | The size of the label. The size will constrain the text if line break is enabled. | `vector3` | `get+set`{.mark} |

## GUI node properties

GUI nodes also contain properties, but they are read and written through special getter and setter functions. For each property there exists one get- and one set- function. There is also a set of constants defined to use as reference to the properties when animating them. If you need to refer to separate property components you have to use the string name of the property, or a hash of the string name.

* `position` (or `gui.PROP_POSITION`)
* `rotation` (or `gui.PROP_ROTATION`)
* `scale` (or `gui.PROP_SCALE`)
* `color` (or `gui.PROP_COLOR`)
* `outline` (or `gui.PROP_OUTLINE`)
* `shadow` (or `gui.PROP_SHADOW`)
* `size` (or `gui.PROP_SIZE`)
* `fill_angle` (or `gui.PROP_FILL_ANGLE`)
* `inner_radius` (or `gui.PROP_INNER_RADIUS`)
* `slice9` (or `gui.PROP_SLICE9`)

Note that all color values are encoded in a vector4 where the components correspond to the RGBA values:

`x`
: The red color component

`y`
: The green color component

`z`
: The blue color component

`w`
: The alpha component

*GUI NODE PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*   | The face color of the node.            | `vector4`      | `gui.get_color()` `gui.set_color()` |
| *outline* | The outline color of the node.         | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | The position of the node. | `vector3` | `gui.get_position()` `gui.set_position()` |
| *rotation* | The rotation of the node expressed as Euler angles--degrees rotated around each axis. | `vector3` | `gui.get_rotation()` `gui.set_rotation()` |
| *scale* | The scale of the node expressed as a multiplier along each axis. | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | The shadow color of the node. | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | The unscaled size of the node. | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | The fill angle of a pie node expressed as degrees counter-clockwise. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | The inner radius of a pie node. | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *slice9* | The edge distances of a slice9 node. | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
