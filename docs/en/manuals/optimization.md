---
title: Optimizing a Defold game
brief: This manual describes how to optimize a Defold app for size and performance.
---

# Optimizing a Defold game

It is important to understand the technical constraints of the platform(s) where your game is supposed to run and to optimize your game for the platform(s) while developing your game. There are several aspects to consider:

* Application size
* Speed
* Memory usage
* Battery usage

## Optimizing application size

Defold will create a dependency tree when building and bundling your application. The build system will start from the bootstrap collection specified in the *game.project* file and inspect every referenced collection, game object and component to build a list of the assets that are in use. It is only these assets that will get included in the final application bundle. Anything not directly referenced will get excluded. While it is good to know that unused assets will not be included you as a developer still needs to consider what goes into the final application and the size of the individual assets and the total size of the application bundle. Some target platforms and distribution channels have limitations on application size:

* Apple and Google has defined application size limits when downloading over mobile networks (as opposed to downloading over Wifi).
  * In the summer of 2019 these limits were 100 MB for Google Play and 150 MB for the Apple App Store.
* Facebook has a recommendation that a Facebook Instant Game should start in less than 5 seconds and preferably less than 3 seconds.
  * What this means for actual application size is not clearly defined but we are talking size in the range of up to 20 MB.
* Playable ads are usually limited to between 2 and 5 MB depending on the ad network.

To get a better understanding of what makes up the size of your application you can [generate a build report](/manuals/bundling/#_build_reports) when bundling. It is quite common that sounds and graphics is what takes up the bulk of the size of any game.

### Optimizing sounds

Defold supports .ogg and .wav files where .ogg is typically used for music and .wav for sound effects. Sounds must be 16-bit with a sampling rate of 44100 so any optimizations must be done on the sounds before encoding them. You can edit the sounds in an external sound editor software to reduce the quality or convert from .wav to .ogg.

### Optimizing graphics

You have several options when it comes to optimizing the graphics used by your game but the first thing to do is to check the size of the graphics that gets added to an atlas or used as a tilesource. You should never use a larger size on the graphics than is actually needed in your game. Importing large images and scaling them down to the appropriate size is a waste of texture memory and should be avoided. Start by adjusting the size of the images using external image editing software to the actual size needed in your game. For things such as background images it might also be ok to use a small image and scale it up to the desired size. Once you have the images down to the correct size and added to atlases or used in tilesources you also need to consider the size of the atlases themselves. The maximum atlas size that can be used varies between platforms and graphics hardware.

::: sidenote
[This forum posts](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl) suggests several tips on how to resize multiple images using scripts or third party software.
:::

* Max texture size on HTML5: https://webglstats.com/webgl/parameter/MAX_TEXTURE_SIZE
* Max texture size on iOS:
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* Max texture size on Android varies greatly but in general all reasonably new devices support 4096x4096.

If an atlas is too large you need to either split it into several smaller atlases or scale the entire atlas using a texture profile. The texture profile system in Defold allows you to not only scale entire atlases but also to apply compression algorithms to reduce the size of the atlas on disk. You can [read more about texture profiles in the manual](/manuals/texture-profiles/).

::: sidenote
You can read more about how to optimize and manage textures in [this forum post](https://forum.defold.com/t/texture-management-in-defold/8921).
:::

### Excluding content for download on demand

Another way of reducing initial application size is to exclude parts of the game content from the application bundle and make this content downloadable on demand. Excluded content can be anything from entire levels to unlockable characters, skins, weapons or vehicles. Defold provides a system called Live Update for excluding content for download on demand. Learn more in the [Live Update manual](/manuals/live-update/).


## Optimizing for application speed

The section is not yet finished. Topics that will be covered:

* Reactive code
* Running code every frame
* Reduce garbage collection
* Optimize rendering
* Culling
* [Profiling](/manuals/profiling/)


## Optimizing memory usage

This section is not yet finished. Topics that will be covered:

* [Texture compression](/manuals/texture-profiles/)
* [Dynamic loading of collections](https://www.defold.com/manuals/collection-proxy/)
* [Dynamic loading of factories](https://www.defold.com/manuals/collection-factory/#_dynamic_loading_of_factory_resources)
* [Profiling](/manuals/profiling/)


## Optimizing battery usage

This section is not yet finished. Topics that will be covered:

* Running code every frame
* Accelerometer on mobile
* [Profiling](/manuals/profiling/)
