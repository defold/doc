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
iOS only - Make sure you specify [Localizations](/manuals/project-settings/#localizations) in `game.project`, since sys.get_info() will never return language which isn’t in this list.
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

Make sure to store the `manifest.private.der` and `manifest.public.der` files which are generated in the project root during the first bundle. These are the public and private signing keys for the game archive and archive manifest. You need these files in order to recreate a previous build of your game.


## Application optimizations

Read the [Optimization manual](/manuals/optimizations) on how to optimize your application for performance, size, memory and battery usage.



## Performance
Always test on target hardware! Check game performance and optimize if needed. Use the [profiler](/manuals/profiling) to find bottlenecks in the code.


## Screen resolution and refresh rate
For platforms with a fixed orientation and screen resolution: Check that the game works on the target platform screen resolution and aspect ratio. For platforms with variable screen resolution and aspect ratio: Check that the game works on a variety of screen resolutions and aspect ratios. Take into consideration what kind of [view projection](/manuals/render/#default-view-projection) that is used in the render script and camera.

For mobile platforms either lock the screen orientation in *game.project* or make sure the game works in both landscape and portrait mode.

* **Display sizes** - Is everything looking good on a larger or smaller screen than the default width and height set in game project?
  * The projection used in the render script and the layouts used in the gui will play a role here.
* **Aspect ratios** - Is everything looking good on a screen with a different aspect ratio than the default aspect ratio from the width and height set in game project?
  * The projection used in the render script and the layouts used in the gui will play a role here.
* **Refresh rate** - Is the game running well on a screen with a higher refresh rate than 60 Hz?
  * The vsync and swap interval in the Display section of game.project 


## Mobile phones and notch and hole punch cameras
It has become increasingly popular to use a small lens cut-out on the display screen to fit in the front camera and sensors (also known as a notch or hole punch camera). When porting a game to mobile it is recommended to make sure that no critical information is positioned where a notch (center of upper screen edge) or hole-punch (top left screen area) is typically found. It is also possible to use the [Safe Area extension](/extension-safearea) to restrict the game view to the area outside any notch or hole-punch camera.


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
