---
title: Porting and release guidelines
brief: This manual highlights some things to consider when porting a game to a new platform or when releasing your game for the first time.
---

# Porting and release guidelines

This page contains a helpful guide and checklist of things to consider when releasing a game or when porting to a new platform.

Porting a Defold game to a new platform or releasing for the first time is usually a straight forward process. In theory it is enough to make sure that the relevant sections are configured in the *game.project* file, but to make the most out of each platform it is recommended to adapt the game to the specifics of each platform.


## Input
Make sure to adapt the game to the input methods of the platform. Consider adding support for [gamepads](/manuals/input-gamepads) if the platform supports it! And make sure the game supports a pause menu - if a controller suddenly disconnects, the game should be paused!

## Localization
Translate any text in the game. For release in Europe and Americas consider translating to at least EFIGS (English, French, Italian, German and Spanish). Make sure it is possible to easily swap between different languages in-game (via the pause menu).

::: important
iOS only - Make sure you specify [Localizations](/manuals/project-settings/#localizations) in `game.project`, since `sys.get_info()` will never return language which isn’t in this list.
:::

Translate the text on the store page as this will have a positive impact on sales! Some platforms require the text on the store page to be translated to the language of each country where the game is available.

## Store materials

### App icon
Make sure your game stands out from the competition. The icon is often your first point of contact with potential players. It should be easy to find on a page full of game icons.

### Store banners and images
Make sure to use impactful and exciting art for your game. It is probably worth spending some money to work with an artist to create art that attracts players.


## Save games

### Save games on desktop, mobile and web
Save games and other saved state can be stored using Defold API function `sys.save(filename, data)` and loaded using `sys.load(filename)`. You can use `sys.get_save_file(application_id, name)` to get a path to an operating system specific location where files can be saved, typically in the logged in users home folder.

### Save games on console
Using `sys.get_save_file()` and `sys.save()` works well on most platforms, but on consoles it is recommended to take a different approach. Console platforms typically associate a user with each connected controller, and as such save games, achievements and other features should be associated with their respective user.

The gamepad input events will contain a user id which can be used to associate the actions of a controller with a user on the console.

The console platforms and their native extensions will expose platform specific API functions to save and load data associated with a specific user. Use these APIs when saving and loading on console.

Console platform APIs for file operations are typically asynchronous. When developing a cross platform game targeted for console it is recommended to design your game such that all file operations are asynchronous, regardless of platform. Example:

```lua
local function save_game(data, user_id, cb)
	if console then
		local filename = "savegame"
		consoleapi.save(user_id, filename, data, cb)
	else
		local filename = sys.get_save_file("mygame", "savegame" .. user_id)
		local success = sys.save(filename, data)
		cb(success)
	end
end
```


## Build artifacts

Make sure to [generate debug symbols](/manuals/debugging-native-code/#symbolicate-a-callstack) for each released version so that you can debug crashes. Store these together with the application bundle.

## Application optimizations

Read the [Optimization manual](/manuals/optimization) on how to optimize your application for performance, size, memory and battery usage.



## Performance
Always test on target hardware! Check game performance and optimize if needed. Use the [profiler](/manuals/profiling) to find bottlenecks in the code.


## Screen resolution and refresh rate
For platforms with a fixed orientation and screen resolution: Check that the game works on the target platform screen resolution and aspect ratio. For platforms with variable screen resolution and aspect ratio: Check that the game works on a variety of screen resolutions and aspect ratios. Take into consideration what kind of [view projection](/manuals/render/#default-view-projection) that is used in the render script and camera.

For mobile platforms either lock the screen orientation in *game.project* or make sure the game works in both landscape and portrait mode.

* **Display sizes** - Is everything looking good on a larger or smaller screen than the default width and height set in *game.project*?
  * The projection used in the render script and the layouts used in the gui will play a role here.
* **Aspect ratios** - Is everything looking good on a screen with a different aspect ratio than the default aspect ratio from the width and height set in *game.project*?
  * The projection used in the render script and the layouts used in the gui will play a role here.
* **Refresh rate** - Is the game running well on a screen with a higher refresh rate than 60 Hz?
  * The vsync and swap interval in the Display section of *game.project* 


## Mobile phones and notch and hole punch cameras
It has become increasingly popular to use a small lens cut-out on the display screen to fit in the front camera and sensors (also known as a notch or hole punch camera). When porting a game to mobile, make sure that critical information is kept within the platform safe area.

Defold has built-in safe-area support on Android and iOS. Set `gui.safe_area_mode` in *game.project* to control which opposing safe-area insets affect GUI adjustment. `none` is the default and ignores the insets; `long` applies left/right in landscape and top/bottom in portrait; `short` applies the opposite pair; and `both` applies all four edges. A GUI script can override the project-wide mode for its scene with [`gui.set_safe_area_mode()`](/ref/gui/#gui.set_safe_area_mode). For custom GUI or rendering logic, [`window.get_safe_area()`](/ref/window/#window.get_safe_area) returns the safe rectangle and the individual edge insets. Platforms without built-in safe-area insets return the full window and zero insets.

The [Safe Area extension](/extension-safearea) remains an alternative for legacy projects or workflows that need behavior beyond the built-in APIs; it is not required for standard Android and iOS safe-area handling.

### Reserved screen areas

[`window.get_reserved_areas()`](/ref/window/#window.get_reserved_areas) reports individual regions that obstruct the game window, such as camera cutouts and the Dynamic Island. Use these rectangles when positioning content around individual obstructions. Use `window.get_safe_area()` when you need a single safe layout rectangle and its edge insets.

The result is an array of tables with `x`, `y`, `width` and `height` fields. Each rectangle is clipped to the game window. The origin is at the bottom left: `x` is the left edge and `y` is the bottom edge, in window pixels matching [`window.get_size()`](/ref/window/#window.get_size). These coordinates are independent of GUI adjustment and the logical resolution in *game.project*, so account for your GUI transforms before using them as node positions.

Platform support is:

- **iOS 27.1 and later:** active occlusions reported by UIKit, including its interaction margins.
- **Android 9 (API level 28) and later:** display cutout rectangles.

The function returns an empty table on unsupported platforms and OS versions, or when no obstructions are reported for the window. An empty table does not mean the entire window is safe for important content: folds, system bars, keyboards and gesture regions are outside this API. Use `window.get_safe_area()` for the platform's safe rectangle.

### Refreshing areas after window events

Query reserved areas during initialization and again on every [`window.WINDOW_EVENT_RESIZED`](/ref/window/#window.WINDOW_EVENT_RESIZED) callback. After the first query, changes to reserved-area geometry also trigger this event on supported platforms, even when the window size stays the same. Each returned table is a snapshot; saved tables are not updated automatically.

On iOS, this event is also sent after orientation transitions and safe-area inset changes. A 180° landscape rotation can move a camera cutout or the Dynamic Island to the other side while both the window dimensions and safe-area insets stay the same. Refresh your geometry on the event even if `data.width` and `data.height` equal their previous values.

The following script keeps both sets of geometry current:

```lua
local function refresh_screen_areas(self)
    self.safe_area = window.get_safe_area()
    self.reserved_areas = window.get_reserved_areas()
    -- Update your UI using the new safe rectangle and reserved areas.
end

local function on_window_event(self, event, data)
    if event == window.WINDOW_EVENT_RESIZED then
        -- Refresh even when the width and height have not changed.
        refresh_screen_areas(self)
    end
end

function init(self)
    refresh_screen_areas(self)
    window.set_listener(on_window_event)
end

function final(self)
    window.set_listener(nil)
end
```

Only one window event listener can be registered at a time. If your game already has one, add this refresh logic to that listener. Replacing the saved array on each refresh also clears obsolete rectangles when the result becomes empty.


## Platform specific guidelines

### Android
Make sure to store your [keystore](/manuals/android/#creating-a-keystore) somewhere safe so that you can update your game.


### Consoles
Store the complete bundle for each version. You will need these files if you want to patch the game.


### Nintendo Switch
Integrate platform specific code - For Nintendo Switch there's a separate extension with some helper functionality for user selection etc.

Defold for Nintendo Switch uses Vulkan as the graphics backend - Make sure to test the game using the [Vulkan graphics backend](https://github.com/defold/extension-vulkan).


### PlayStation®4
Integrate platform specific code - For PlayStation®4 there's a separate extension with some helper functionality for user selection etc.


### HTML5
Playing web games on mobile phones is increasing in popularity - Try to make the game run well in a mobile browser as well! It is also important to keep in mind that web games are expected to load fast! - Make sure to optimize the game for size. Also consider the loading experience in general to not lose players unnecessarily.

In 2018 browsers introduced an autoplay policy for sounds which prevent games and other web content from playing sounds until a user interaction event (touch, button, gamepad etc) has taken place. It is important to take this into account when porting to HTML5 and only start playing sounds and music upon first user interaction. Attempts to play sounds before any user interaction will be logged as an error in the browser developer console but will not impact the game.

Also make sure to pause any playing sounds if the game is showing ads.
