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

Numeric properties display a drag handle when you hover over their input field. You can increase/decrease their value, by dragging the handle right/left or up/down respectively.

Depending on where a property is found, you access it via a generic function, or a property-specific function. Many of the properties can be automatically animated. Animating properties through the built-in system is highly recommended over manipulating the properties yourself (inside an `update()` function), both for performance reasons as well as convenience.

Composite properties of type `vector3`, `vector4` or `quaternion` also expose their sub-components (`x`, `y`, `z` and `w`). You can address the components individually by suffixing the name with a dot (`.`) and the name of the component. For example, to set the x-component of a game object's position:

```lua
-- Set the x position of "game_object" to 10.
go.set("game_object", "position.x", 10)
```

The functions `go.get()`, `go.set()` and `go.animate()` take a reference as their first parameter and a property identifier as their second. The reference identifies the game object or component and can be a string, a hash or a URL. URLs are explained in detail in the [addressing manual](/manuals/addressing). The property identifier is a string or hash that names the property:

```lua
-- Set the x-scale of the sprite component
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

For GUI nodes, the node is provided as the first parameter to either a property-specific function or the generic `gui.get()` and `gui.set()` functions:

```lua
-- Get the color of the button
local node = gui.get_node("button")
local color = gui.get_color(node)
local same_color = gui.get(node, "color")
gui.set(node, "color.x", 1)
```

## Game object and component properties

All game objects, and some component types have properties that can be read and manipulated in runtime. Read these values with [`go.get()`](/ref/go#go.get) and write them with [`go.set()`](/ref/go#go.set). Depending on the property value type, you can animate the values with [`go.animate()`](/ref/go#go.animate). A small set of the properties are read only.

`get`{.mark}
: Can be read with [`go.get()`](/ref/go#go.get).

`get+set`{.mark}
: Can be read with [`go.get()`](/ref/go#go.get) and written with [`go.set()`](/ref/go#go.set). Numerical values can be animated with [`go.animate()`](/ref/go#go.animate).

*GAME OBJECT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | The local position of the game object. | `vector3`      | `get+set`{.mark} |
| *rotation* | Local rotation of game object, expressed as a `quaternion`.  | `quaternion` | `get+set`{.mark} |
| *euler*    | Local rotation of game object, Euler angles. | `vector3` | `get+set`{.mark} |
| *scale*    | Local non uniform scale of the game object, expressed as a vector where each component contains a multiplier along each axis. To double the size in X and Y without changing Z, use `vmath.vector3(2.0, 2.0, 1.0)`. | `vector3` | `get+set`{.mark} |
| *scale.xy*    | Local non uniform scale of the game object along the X and Y axes. Use this property or `go.set_scale_xy()` when Z scaling is not intended. | `vector3` | `get+set`{.mark} |

::: sidenote
Specific functions for working with the game object transform also exist; they are `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`,  `go.get_scale()`, `go.set_scale()` and `go.set_scale_xy()`.
:::

*SPRITE COMPONENT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | The non scaled size of the sprite---its size as taken from the source atlas. | `vector3` | `get`{.mark} |
| *image* | The texture path hash of the sprite. | `hash` | `get`{.mark}|
| *scale* | Non uniform scale of the sprite . | `vector3` | `get+set`{.mark}|
| *scale.xy* | Non uniform scale of the sprite along X and Y axis. | `vector3` | `get+set`{.mark}|
| *material* | The material used by the sprite. | `hash` | `get+set`{.mark}|
| *cursor* | Position (between 0--1) of playback cursor. | `number` | `get+set`{.mark}|
| *playback_rate* | The framerate of the flipbook animation. | `number` | `get+set`{.mark}|

*COLLISION OBJECT COMPONENT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | The mass of the collision object. | `number` | `get`{.mark} |
| *linear_velocity* | The current linear velocity of the collision object. | `vector3` | `get`{.mark} |
| *angular_velocity* | The current angular velocity of the collision object. | `vector3` | `get`{.mark} |
| *linear_damping* | Linear damping of the collision object. | `vector3` | `get+set`{.mark} |
| *angular_damping* | Angular damping of the collision object. | `vector3` | `get+set`{.mark} |

*MODEL (3D) COMPONENT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | The current animation.                | `hash`          | `get`{.mark}     |
| *texture0*--*texture15* | The texture path hashes of the model. | `hash` | `get+set`{.mark}|
| *cursor*  | Position (between 0--1) of playback cursor. | `number`   | `get+set`{.mark} |
| *playback_rate* | The playback rate of the animation. A multiplier to the animation playback rate. | `number` | `get+set`{.mark} |
| *material* | The material used by the model. | `hash` | `get+set`{.mark}|

*LABEL COMPONENT PROPERTIES*

| property   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *scale* | The scale of the label. | `vector3` | `get+set`{.mark} |
| *scale.xy* | The scale of the label along X and Y axis. | `vector3` | `get+set`{.mark}|
| *color*     | The color of the label. | `vector4` | `get+set`{.mark} |
| *outline* | The outline color of the label. | `vector4` | `get+set`{.mark} |
| *shadow* | The shadow color of the label. | `vector4` | `get+set`{.mark} |
| *size* | The size of the label. The size will constrain the text if line break is enabled. | `vector3` | `get+set`{.mark} |
| *material* | The material used by the label. | `hash` | `get+set`{.mark}|
| *font* | The font used by the label. | `hash` | `get+set`{.mark}|


## GUI node properties

GUI nodes have property-specific getter and setter functions, such as `gui.get_position()` and `gui.set_position()`. The built-in properties listed below can alternatively be read and written with `gui.get(node, property)` and `gui.set(node, property, value)`. Other node values may still require their dedicated functions. Material constants on GUI nodes also use the generic functions. To address one component of a vector property, append its name, for example `gui.set(node, "color.x", 1)`.

The generic and property-specific functions do not always use identical value types. `gui.get()` returns a `vector4` for the complete `position`, `scale`, `size`, and `euler` properties, while the corresponding property-specific functions return a `vector3`. `gui.set()` accepts either a `vector3` or `vector4` for those properties. The generic `rotation` property uses a quaternion; use `euler` when setting rotation in degrees.

* `position` (or `gui.PROP_POSITION`)
* `rotation` (or `gui.PROP_ROTATION`)
* `euler` (or `gui.PROP_EULER`)
* `scale` (or `gui.PROP_SCALE`)
* `color` (or `gui.PROP_COLOR`)
* `outline` (or `gui.PROP_OUTLINE`)
* `shadow` (or `gui.PROP_SHADOW`)
* `size` (or `gui.PROP_SIZE`)
* `fill_angle` (or `gui.PROP_FILL_ANGLE`)
* `inner_radius` (or `gui.PROP_INNER_RADIUS`)
* `leading` (or `gui.PROP_LEADING`)
* `tracking` (or `gui.PROP_TRACKING`)
* `slice9` (or `gui.PROP_SLICE9`)

Note that all color values are encoded in a `vector4` where the components correspond to the RGBA values:

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
| *rotation* | The node rotation. The getter returns a quaternion; the setter accepts a quaternion or Euler angles as a vector. | `quaternion`, `vector3`, or `vector4` | `gui.get_rotation()` `gui.set_rotation()` |
| *euler* | The rotation of the node expressed as Euler angles in degrees. | `vector3` | `gui.get_euler()` `gui.set_euler()` |
| *scale* | The scale of the node expressed as a multiplier along each axis. | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | The shadow color of the node. | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | The unscaled size of the node. | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | The fill angle of a pie node expressed as degrees counter-clockwise. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | The inner radius of a pie node. | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *leading* | The line-spacing scale of a text node. | `number` | `gui.get_leading()` `gui.set_leading()` |
| *tracking* | The letter-spacing scale of a text node. | `number` | `gui.get_tracking()` `gui.set_tracking()` |
| *slice9* | The edge distances of a slice9 node. | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
