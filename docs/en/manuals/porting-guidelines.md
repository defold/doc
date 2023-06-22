---
title: Porting guidelines
brief: This manual highlights some things to consider when porting a game to a new platform
---

# Porting guidelines

Porting a Defold game to a new platform is usually a straight forward process. In theory it is enough to make sure that the relevant sections are configured in the *game.project* file, but to make the most out of each platform it is recommended to adapt the game to the specifics of each platform. This manual contains some best practices for porting in general and some specifics for some of the platforms.


## Best practices

### Input
Make sure to adapt the game to the input methods of the platform. Consider adding support for [gamepads](/manuals/input-gamepads) if the platform supports it! And make sure the game supports a pause menu - if a controller suddenly disconnects, the game should be paused!


### Localization
Localise/translate any text in the game as well as the text in the store page as this will have a positive impact on sales! For the localization, make sure it is possible to easily swap between different languages in-game (via the pause menu).


### Save games

#### Save games on desktop, mobile and web
Save games and other saved state can be stored using Defold API function `sys.save(filename, data)` and loaded using `sys.load(filename)`. You can use `sys.get_save_file(application_id, name)` to get a path to an operating system specific location where files can be saved, typically in the logged in users home folder.

#### Save games on console
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


### Performance
Always test on target hardware! Check game performance and optimise if needed. Use the [profiler](/manuals/profiling) to find bottlenecks in the code.


### Screen resolution
For platforms with a fixed orientation and screen resolution: Check that the game works on the target platform screen resolution and aspect ratio. For platforms with variable screen resolution and aspect ratio: Check that the game works on a variety of screen resolutions and aspect ratios. Take into consideration what kind of [view projection](/manuals/render/#default-view-projection) that is used in the render script and camera.

For mobile platforms either lock the screen orientation in *game.project* or make sure the game works in both landscape and portrait mode.


### Mobile phones and notch and hole punch cameras
It has become increasingly popular to use a small lens cut-out on the display screen to fit in the front camera and sensors (also known as a notch or hole punch camera). When porting a game to mobile it is recommended to make sure that no critical information is positioned where a notch (center of upper screen edge) or hole-punch (top left screen area) is typically found. It is also possible to use the [Safe Area extension](/extension-safearea) to restrict the game view to the area outside any notch or hole-punch camera.


### Nintendo Switch
Integrate platform specific code - For Nintendo Switch there's a separate extension with some helper functionality for user selection etc.

Defold for Nintendo Switch uses Vulkan as the graphics backend - Make sure to test the game using the [Vulkan graphics backend](https://github.com/defold/extension-vulkan).


### PlayStation®4
Integrate platform specific code - For PlayStation®4 there's a separate extension with some helper functionality for user selection etc.


### HTML5
Playing web games on mobile phones is increasing in popularity - Try to make the game run well in a mobile browser as well! It is also important to keep in mind that web games are expected to load fast! - Make sure to optimize the game for size. Also consider the loading experience in general to not lose players unnecessarily.

In 2018 browsers introduced an autoplay policy for sounds which prevent games and other web content from playing sounds until a user interaction event (touch, button, gamepad etc) has taken place. It is important to take this into account when porting to HTML5 and only start playing sounds and music upon first user interaction. Attempts to play sounds before any user interaction will be logged as an error in the browser developer console but will not impact the game.
