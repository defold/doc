---
title: Gamepad input in Defold
brief: This manual explains how gamepad input works.
---

::: sidenote
It is recommended that you familiarise yourself with the general way in which input works in Defold, how to receive input and in which order input is received in your script files. Learn more about the input system in the [Input Overview manual](/manuals/input).
:::

# Gamepads
Gamepad triggers allow you to bind standard gamepad input to game functions. Gamepad input offers bindings for:

- Left and right sticks (direction and clicks)
- Left and right digital pads. Right pad usually translates to the "A", "B", "X" and "Y" buttons on the Xbox controller and "square", "circle", "triangle" and "cross" buttons on the Playstation controller.
- Left and right triggers
- Left and right shoulder buttons
- Start, Back and Guide buttons

![](images/input/gamepad_bindings.png)

::: important
The examples below use the actions shown in the image above. As with all input you are free to name your input actions any way you want to.
:::

## Digital buttons
Digital buttons generate pressed, released and repeated events. Example showing how to detect input for a digital button (either pressed or released):

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lpad_left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

## Analog sticks
Analog sticks generate continuous input events when the stick is moved outside the dead zone defined in the gamepad settings file (see below). Example showing how to detect input for an analog stick:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- left stick was moved down
        print(action.value) -- a value between 0.0 an -1.0
    end
end
```

Analog sticks also generate pressed and released events when moved in the cardinal directions above a certain threshold value. This makes it easy to also use an analog stick as digital directional input:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- left stick was moved to its extreme down position
    end
end
```

## Multiple gamepads
Defold supports multiple gamepads through the host operating system, actions set the `gamepad` field of the action table to the gamepad number the input originated from:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- gamepad 0 wants to join the game
        end
    end
end
```

## Connect and Disconnect
Gamepad input bindings also provides two separate bindings named `Connected` and `Disconnected` to detect when a gamepad is connected (even those connected from the start) or disconnected.

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- gamepad 0 was connected
        end
    elseif action_id == hash("gamepad_dicconnected") then
        if action.gamepad == 0 then
          -- gamepad 0 was dicconnected
        end
    end
end
```

## Gamepads settings file
On Windows, only XBox 360 controllers are currently supported. To hook up your 360 controller to your Windows machine, make sure it is setup correctly. See http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows

Gamepad input setup uses a separate mapping file for each hardware gamepad type. Gamepad mappings for specific hardware gamepads are set in a *gamepads* file. Defold ships with a built-in gamepads file with settings for common gamepads:

![Gamepad settings](images/input/gamepads.png){srcset="images/input/gamepads@2x.png 2x"}

If you need to create a new gamepad settings file, we have a simple tool to help:

[Click to download gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

It includes binaries for Windows, Linux and macOS. Run it from the command line:

```sh
./gdc
```

The tool will ask you to press different buttons on your connected controller. It will then output a new gamepads file with correct mappings for your controller. Save the new file, or merge it with your existing gamepads file, then update the setting in "game.project":

![Gamepad settings](images/input/gamepad_setting.png){srcset="images/input/gamepad_setting@2x.png 2x"}
