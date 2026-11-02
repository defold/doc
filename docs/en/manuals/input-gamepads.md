---
title: Gamepad input in Defold
brief: This manual explains how gamepad input works.
---

::: sidenote
It is recommended that you familiarize yourself with the general way in which input works in Defold, how to receive input and in which order input is received in your script files. Learn more about the input system in the [Input Overview manual](/manuals/input).
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
Digital buttons generate `pressed`, `released` and `repeated` events. Example showing how to detect input for a digital button (either pressed or released):

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

Analog sticks also generate `pressed` and `released` events when moved in the cardinal directions above a certain threshold value. This makes it easy to also use an analog stick as digital directional input:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- left stick was moved to its extreme down position
    end
end
```

## Multiple gamepads
Defold supports multiple gamepads through the host operating system, actions set the `gamepad` field of the `action` table to the gamepad number the input originated from:

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
Gamepad input bindings also provide two separate bindings named `Connected` and `Disconnected` to detect when a gamepad is connected (even those connected from the start) or disconnected.

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- gamepad 0 was connected
        end
    elseif action_id == hash("gamepad_disconnected") then
        if action.gamepad == 0 then
          -- gamepad 0 was disconnected
        end
    end
end
```

## Raw gamepads

Gamepad input bindings also provide a separate binding named `Raw` to give the unfiltered (without applied deadzone) button, axis and hat input of any connected gamepad.

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## Gamepads settings file

Gamepad mappings translate a controller's buttons, axes and hats into the standard controls used by your input bindings. Defold combines two mapping sources configured in the *Input* section of *game.project*:

| Setting | Mapping format | Default |
| --- | --- | --- |
| [Gamepad Database](/manuals/project-settings/#gamepad-database) | SDL-format text database, matched using the controller's GUID | `/builtins/input/gamecontrollerdb.txt` |
| [Gamepads](/manuals/project-settings/#gamepads) | Legacy `.gamepads` entries for device names and platforms | `/builtins/input/default.gamepads` |

SDL database mappings and automatic platform mappings use [Gamepad Deadzone](/manuals/project-settings/#gamepad-deadzone). Legacy `.gamepads` entries define their own dead zones. On Android, a controller without a database entry may also receive an [automatic mapping](#gamepads-on-android).

### Legacy .gamepads mappings

A `.gamepads` file can contain mappings for multiple controllers. Existing legacy mappings remain supported. Defold includes mappings for common controllers in the default file:

![Gamepad settings](images/input/gamepads.png)

If you need to create a legacy `.gamepads` mapping on a desktop platform, the following tool can help. For Android, see [Gamepads on Android](#gamepads-on-android).

[Click to download gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

It includes binaries for Windows, Linux and macOS. Run it from the command line:

```sh
./gdc
```

The tool will ask you to press different buttons on your connected controller. It will then output a new gamepads file with correct mappings for your controller. Save the new file, or merge it with your existing gamepads file, then update the setting in *game.project*:

![Gamepad settings](images/input/gamepad_setting.png)

### Unidentified gamepads

When neither a configured mapping nor an automatic platform mapping is available, the gamepad only generates the actions bound to `Connected`, `Disconnected` and `Raw`. You can add a controller mapping or handle its raw input in your game.

It is possible to check if an input action for a gamepad is from an unknown gamepad or not by reading the `gamepad_unknown` value from the `action`:

```lua
function on_input(self, action_id, action)
    if action_id == hash("connected") then
        if action.gamepad_unknown then
            print("The connected gamepad is unidentified and will only generate raw input")
        else
            print("The connected gamepad is known and will generate input actions for buttons and sticks")
        end
    end
end
```

## Gamepads in HTML5
Gamepads are supported in HTML5 builds and generate the same input events as on other platforms. Support for gamepads is based on the [Gamepad API](https://www.w3.org/TR/gamepad/) which is supported in most browsers ([refer to this support chart](https://caniuse.com/?search=gamepad)). If the browser doesn't support the Gamepad API Defold will silently ignore any Gamepad triggers in your project. You can check if the browser supports the Gamepad API by checking if the `getGamepads` function exists on the `navigator` object:

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end

if supports_gamepads() then
    print("Platform supports gamepads")
end
```

If your game is running from inside an `iframe` you must also make sure that the `iframe` has the `gamepad` permission added:

```html
<iframe allow="gamepad"></iframe>
```

### Standard gamepad

If a connected gamepad is identified by the browser as a standard gamepad it will use the mapping for `Standard Gamepad` in the [gamepads settings file](/manuals/input-gamepads/#gamepads-settings-file) (a `Standard Gamepad` mapping is included in the `default.gamepads` file in `/builtins`). A standard gamepad is defined as having 16 buttons and 2 analog sticks with a button layout similar to a PlayStation or Xbox controller (see the [W3C definition and button layout](https://w3c.github.io/gamepad/#dfn-standard-gamepad) for more information). If the connected gamepad is not identified as a standard gamepad Defold will look for a mapping matching the hardware gamepad type in the gamepad settings file.

## Gamepads on Windows
On Windows, only XBox 360 controllers are currently supported. To hook up your 360 controller to your Windows machine, [make sure it is setup correctly](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Gamepads on Android

Gamepads are supported in Android builds and generate the same input actions as on other platforms. Defold uses the configured [gamepad mappings](#gamepads-settings-file) and can automatically map some controllers that have no matching entry.

If a controller is unidentified or its controls are incorrect, test it on the Android device and add or update its mapping. See [Unidentified gamepads](#unidentified-gamepads) and [Raw gamepads](#raw-gamepads) for troubleshooting.
