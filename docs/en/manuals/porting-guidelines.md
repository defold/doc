---
title: Porting guidelines
brief: This manual highlights some things to consider when porting a game to a new platform
---

Porting a Defold game to a new platform is usually a very straight forward process. In theory it is enough to make sure that the relevant sections are configured in the *game.project* file, but to make the most out of each platform it is recommended to adapt the game to the specifics of each platform. This manual contains some best practices for porting in general and some specifics for some of the platforms.


## Best practices

### Input
Make sure to adapt the game to the input methods of the platform. Consider adding support for [gamepads](/manuals/input-gamepads) if the platform supports it! And make sure the game supports a pause menu - if a controller suddenly disconnects, the game should be paused!


### Localization
Localise/translate any text in the game as well as the text in the store page as this will have a positive impact on sales! For the localization, make sure it is possible to easily swap between different languages in-game (via the pause menu).


### Performance
Always test on target hardware! Check game performance and optimise if needed. Use the [profiler](/manuals/profiling) to find bottlenecks in the code.


### Screen resolution
For platforms with a fixed orientation and screen resolution: Check that the game works on the target platform screen resolution and aspect ratio. For platforms with variable screen resolution and aspect ratio: Check that the game works on a variety of screen resolutions and aspect ratios. Take into consideration what kind of [view projection](/manuals/render/#default-view-projection) that is used in the render script and camera.

For mobile platforms either lock the screen orientation in *game.project* or make sure the game works in both landscape and portrait mode.


### Mobile phones and notch and hole punch cameras
It has become increasingly popular to use a small lens cut-out on the display screen to fit in the front camera and sensors (also known as a notch or hole punch camera). When porting a game to mobile it is recommended to make sure that no critical information is positioned where a notch (center of upper screen edge) or hole-punch (top left screen area) is typically found. It is also possible to use the [Safe Area extension](/extension-safearea) to restrict the game view to the area outside any notch or hole-punch camera.


### Nintendo Switch
Integrate platform specific code - For Nintendo Switch there's a separate extension with some helper functionality for user selection etc

Defold for Nintendo Switch uses Vulkan as the graphics backend - Make sure to test the game using the [Vulkan graphics backend](https://github.com/defold/extension-vulkan).


### HTML5
Playing web games on mobile phones is increasing in popularity - Try to make the game run well in a mobile browser as well! It is also important to keep in mind that web games are expected to load fast! - Make sure to optimize the game for size. Also consider the loading experience in general to not lose players unnecessarily.

In 2018 browsers introduced an autoplay policy for sounds which prevent games and other web content from playing sounds until a user interaction event (touch, button, gamepad etc) has taken place. It is important to take this into account when porting to HTML5 and only start playing sounds and music upon first user interaction. Attempts to play sounds before any user interaction will be logged as an error in the browser developer console but will not impact the game.
