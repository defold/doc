---
title: Property animations in Defold manual
brief: This manual describes how to use property animations in Defold.
---

# Property animation

All numeric properties (numbers, vector3, vector4 and quaterions) and shader constants can be animated with the built-in animation system, using the function `go.animate()`. The engine will automatically "tween" properties for you according to given playback modes and easing functions. You can also specify custom easing functions.

  ![Property animation](images/animation/property_animation.png)
  ![Bounce loop](images/animation/bounce.gif)

## Property animation

To animate a game object or component property, use the function `go.animate()`. For GUI node properties, the corresponding function is `gui.animate()`.

```lua
-- Set the position property y component to 200
go.set(".", "position.y", 200)
-- Then animate it
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

To stop all animations of a given property, call `go.cancel_animations()`, or for GUI nodes, `gui.cancel_animation()`:

```lua
-- Stop euler z rotation animation on the current game object
go.cancel_animations(".", "euler.z")
```

If you cancel the animation of a composite property, like `position`, any animations of the sub-components (`position.x`, `position.y` and `position.z`) will be cancelled as well.

The [Properties Manual](/manuals/properties) contains all the available properties on game objects, components and GUI nodes.

## GUI node property animation

Almost all GUI node properties are possible to animate. You can, for instance, make a node invisible by setting its `color` property to full transparency and then fade it into view by animating the color to white (i.e. no tint color).

```lua
local node = gui.get_node("button")
local color = gui.get_color(node)
-- Animate the color to white
gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_INOUTQUAD, 0.5)
-- Animate the outline red color component
gui.animate(node, "outline.x", 1, gui.EASING_INOUTQUAD, 0.5)
-- And move to x position 100
gui.animate(node, hash("position.x"), 100, gui.EASING_INOUTQUAD, 0.5)
```

## Completion callbacks

The property animation functions `go.animate()` and `gui.animate()` support an optional Lua callback function as the last argument. This function will be called when the animation has played to the end. The function is never called for looping animations, nor when an animation is manually canceled via `go.cancel_animations()` or `gui.cancel_animation()`. The callback can be used to trigger events on animation completion or to chain multiple animations together.

## Easing

Easing defines how the animated value changes over time. The images below describe the functions applied over time to create the easing.

The following are valid easing values for `go.animate()`:

|---|---|
| `go.EASING_LINEAR` | |
| `go.EASING_INBACK` | `go.EASING_OUTBACK` |
| `go.EASING_INOUTBACK` | `go.EASING_OUTINBACK` |
| `go.EASING_INBOUNCE` | `go.EASING_OUTBOUNCE` |
| `go.EASING_INOUTBOUNCE` | `go.EASING_OUTINBOUNCE` |
| `go.EASING_INELASTIC` | `go.EASING_OUTELASTIC` |
| `go.EASING_INOUTELASTIC` | `go.EASING_OUTINELASTIC` |
| `go.EASING_INSINE` | `go.EASING_OUTSINE` |
| `go.EASING_INOUTSINE` | `go.EASING_OUTINSINE` |
| `go.EASING_INEXPO` | `go.EASING_OUTEXPO` |
| `go.EASING_INOUTEXPO` | `go.EASING_OUTINEXPO` |
| `go.EASING_INCIRC` | `go.EASING_OUTCIRC` |
| `go.EASING_INOUTCIRC` | `go.EASING_OUTINCIRC` |
| `go.EASING_INQUAD` | `go.EASING_OUTQUAD` |
| `go.EASING_INOUTQUAD` | `go.EASING_OUTINQUAD` |
| `go.EASING_INCUBIC` | `go.EASING_OUTCUBIC` |
| `go.EASING_INOUTCUBIC` | `go.EASING_OUTINCUBIC` |
| `go.EASING_INQUART` | `go.EASING_OUTQUART` |
| `go.EASING_INOUTQUART` | `go.EASING_OUTINQUART` |
| `go.EASING_INQUINT` | `go.EASING_OUTQUINT` |
| `go.EASING_INOUTQUINT` | `go.EASING_OUTINQUINT` |

The following are valid easing values for `gui.animate()`:

|---|---|
| `gui.EASING_LINEAR` | |
| `gui.EASING_INBACK` | `gui.EASING_OUTBACK` |
| `gui.EASING_INOUTBACK` | `gui.EASING_OUTINBACK` |
| `gui.EASING_INBOUNCE` | `gui.EASING_OUTBOUNCE` |
| `gui.EASING_INOUTBOUNCE` | `gui.EASING_OUTINBOUNCE` |
| `gui.EASING_INELASTIC` | `gui.EASING_OUTELASTIC` |
| `gui.EASING_INOUTELASTIC` | `gui.EASING_OUTINELASTIC` |
| `gui.EASING_INSINE` | `gui.EASING_OUTSINE` |
| `gui.EASING_INOUTSINE` | `gui.EASING_OUTINSINE` |
| `gui.EASING_INEXPO` | `gui.EASING_OUTEXPO` |
| `gui.EASING_INOUTEXPO` | `gui.EASING_OUTINEXPO` |
| `gui.EASING_INCIRC` | `gui.EASING_OUTCIRC` |
| `gui.EASING_INOUTCIRC` | `gui.EASING_OUTINCIRC` |
| `gui.EASING_INQUAD` | `gui.EASING_OUTQUAD` |
| `gui.EASING_INOUTQUAD` | `gui.EASING_OUTINQUAD` |
| `gui.EASING_INCUBIC` | `gui.EASING_OUTCUBIC` |
| `gui.EASING_INOUTCUBIC` | `gui.EASING_OUTINCUBIC` |
| `gui.EASING_INQUART` | `gui.EASING_OUTQUART` |
| `gui.EASING_INOUTQUART` | `gui.EASING_OUTINQUART` |
| `gui.EASING_INQUINT` | `gui.EASING_OUTQUINT` |
| `gui.EASING_INOUTQUINT` | `gui.EASING_OUTINQUINT` |

![Linear interpolation](images/properties/easing_linear.png)
![In back](images/properties/easing_inback.png)
![Out back](images/properties/easing_outback.png)
![In-out back](images/properties/easing_inoutback.png)
![Out-in back](images/properties/easing_outinback.png)
![In bounce](images/properties/easing_inbounce.png)
![Out bounce](images/properties/easing_outbounce.png)
![In-out bounce](images/properties/easing_inoutbounce.png)
![Out-in bounce](images/properties/easing_outinbounce.png)
![In elastic](images/properties/easing_inelastic.png)
![Out elastic](images/properties/easing_outelastic.png)
![In-out elastic](images/properties/easing_inoutelastic.png)
![Out-in elastic](images/properties/easing_outinelastic.png)
![In sine](images/properties/easing_insine.png)
![Out sine](images/properties/easing_outsine.png)
![In-out sine](images/properties/easing_inoutsine.png)
![Out-in sine](images/properties/easing_outinsine.png)
![In exponential](images/properties/easing_inexpo.png)
![Out exponential](images/properties/easing_outexpo.png)
![In-out exponential](images/properties/easing_inoutexpo.png)
![Out-in exponential](images/properties/easing_outinexpo.png)
![In circlic](images/properties/easing_incirc.png)
![Out circlic](images/properties/easing_outcirc.png)
![In-out circlic](images/properties/easing_inoutcirc.png)
![Out-in circlic](images/properties/easing_outincirc.png)
![In quadratic](images/properties/easing_inquad.png)
![Out quadratic](images/properties/easing_outquad.png)
![In-out quadratic](images/properties/easing_inoutquad.png)
![Out-in quadratic](images/properties/easing_outinquad.png)
![In cubic](images/properties/easing_incubic.png)
![Out cubic](images/properties/easing_outcubic.png)
![In-out cubic](images/properties/easing_inoutcubic.png)
![Out-in cubic](images/properties/easing_outincubic.png)
![In quartic](images/properties/easing_inquart.png)
![Out quartic](images/properties/easing_outquart.png)
![In-out quartic](images/properties/easing_inoutquart.png)
![Out-in quartic](images/properties/easing_outinquart.png)
![In quintic](images/properties/easing_inquint.png)
![Out quintic](images/properties/easing_outquint.png)
![In-out quintic](images/properties/easing_inoutquint.png)
![Out-in quintic](images/properties/easing_outinquint.png)

## Custom easing

You can create custom easing curves by defining a `vector` with a set of values and then provide the vector instead of one of the predefined easing constants above. The vector values express a curve from the start value (`0`) to the target value (`1`). The runtime samples values from the vector and linearly interpolates when calculating values in between the points expressed in the vector.

For example, the vector:

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5, 1 }
local my_easing = vmath.vector(values)
```

yields the following curve:

![Custom curve](images/animation/custom_curve.png)

The following example causes the y position of a game object to jump between the current position and 200 according to a square curve:

```lua
local values = { 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1 }
local square_easing = vmath.vector(values)
go.animate("go", "position.y", go.PLAYBACK_LOOP_PINGPONG, 200, square_easing, 2.0)
```

![Square curve](images/animation/square_curve.png)
