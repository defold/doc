---
title: Optimizing size of a Defold game
brief: This manual describes how to optimize the size of a Defold game.
---

# Optimizing game size

The size of your game can be a critical success factor for platforms such as web and mobile, while it is of less importance on desktop and consoles where disk space is cheap and often plentiful.

### iOS and Android
Apple and Google has defined application size limits when downloading over mobile networks (as opposed to downloading over Wifi). For Android this limit is 200 MB for apps published with [app bundles](https://developer.android.com/guide/app-bundle#size_restrictions). For iOS users will get a warning if the application is larger than 200 MB, but can still proceed to download it.

::: sidenote
According to a 2017 study it was shown that "For every 6 MB increase to an APK's size, we see a decrease in the install conversion rate of 1%." ([source](https://medium.com/googleplaydev/shrinking-apks-growing-installs-5d3fcba23ce2))
:::

### HTML5
Poki and many other web game platforms recommend that the initial download should be no larger than 5 MB.

Facebook has a recommendation that a Facebook Instant Game should start in less than 5 seconds and preferably less than 3 seconds. What this means for actual application size is not clearly defined but we are talking size in the range of up to 20 MB.

Playable ads are usually limited to between 2 and 5 MB depending on the ad network.

## Size optimization strategies
You can optimize the application size in two ways; by reducing the size of the engine and/or by reducing the size of the game assets.

To get a better understanding of what makes up the size of your application you can [generate a build report](/manuals/bundling/#build-reports) when bundling. It is quite common that sounds and graphics is what takes up the bulk of the size of any game.

::: important
Defold will create a dependency tree when building and bundling your application. The build system will start from the bootstrap collection specified in the *game.project* file and inspect every referenced collection, game object and component to build a list of the assets that are in use. It is only these assets that will get included in the final application bundle. Anything not directly referenced will get excluded. While it is good to know that unused assets will not be included you as a developer still needs to consider what goes into the final application and the size of the individual assets and the total size of the application bundle. 
:::

## Optimize engine size
A quick way to reduce the engine size is to remove functionality in the engine that you do not use. This is done [application manifest file](https://defold.com/manuals/app-manifest/) where it is possible to remove engine components that you do not need. Examples:

* Physics - If your game does not make use of Box2D or Bullet3D physics then it is strongly advised to remove the physics engines
* LiveUpdate - If your game does not use LiveUpdate it can be removed
* Image loaded - If your game does not manually load and decode images using `image.load()`
* BasisU - If your game has few textures, compare the build size without BasisU (removed via app manifest) and without texture compression versus a build with BasisU and compressed textures. For games with limited textures, it might be more beneficial to reduce the binary size and skip texture compression. Additionally, not using the transcoder can lower the amount of memory required to run your game.

## Optimize asset size
The biggest wins in terms of asset size optimizations are usually gained by reducing the size of sounds and textures.

### Optimize sounds
Defold supports these formats:
* .wav
* .ogg
* .opus

Sounds files must be using 16-bit samples.
Our sound decoders will up/downscale sounds sample rates as needed for the current sound device.

Shorter sounds like sound effects are often compressed harder, whereas music files have less compression.
No compression is done by Defold, so the developer will have to handle that specifically for each audio format.

You can edit the sounds in an external sound editor software (or command line using e.g. [ffmpeg](https://ffmpeg.org)) to reduce the quality or convert between formats. Also consider converting sounds from stereo to mono to further reduce the size of the content.

### Optimize textures
You have several options when it comes to optimizing the textures used by your game, but the first thing to do is to check the size of the images that gets added to an atlas or used as a tilesource. You should never use a larger size on the images than is actually needed in your game. Importing large images and scaling them down to the appropriate size is a waste of texture memory and should be avoided. Start by adjusting the size of the images using external image editing software to the actual size needed in your game. For things such as background images it might also be ok to use a small image and scale it up to the desired size. Once you have the images down to the correct size and added to atlases or used in tilesources you also need to consider the size of the atlases themselves. The maximum atlas size that can be used varies between platforms and graphics hardware.

::: sidenote
[This forum posts](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl) suggests several tips on how to resize multiple images using scripts or third party software.
:::

* Max texture size on HTML5 reported to the [Web3D Survey project](https://web3dsurvey.com/webgl/parameters/MAX_TEXTURE_SIZE)
* Max texture size on iOS:
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* Max texture size on Android varies greatly but in general all reasonably new devices support at least 4096x4096.

If an atlas is too large you need to either split it into several smaller atlases, use multi-page atlases or scale the entire atlas using a texture profile. The texture profile system in Defold allows you to not only scale entire atlases but also to apply compression algorithms to reduce the size of the atlas on disk. You can [read more about texture profiles in the manual](/manuals/texture-profiles/). If you don’t know what to use, try to start with these settings as a starting point for further customizations:

* mipmaps: false
* premultiply_alpha: true
* format: TEXTURE_FORMAT_RGBA
* compression_level: NORMAL
* compression_type: COMPRESSION_TYPE_BASIS_UASTC

::: sidenote
You can read more about how to optimize and manage textures in [this forum post](https://forum.defold.com/t/texture-management-in-defold/8921).
:::

### Optimize fonts
The size of your fonts will be smaller if you specify what symbols you are going to use and set this in [Characters](/manuals/font/#properties) instead of using the All Chars checkbox.

### Exclude content for download on demand
Another way of reducing initial application size is to exclude parts of the game content from the application bundle and download it on demand. Defold provides a system called Live Update for excluding content for download on demand.

Excluded content can be anything from entire levels to unlockable characters, skins, weapons or vehicles. If your game has a lot of content, organize the loading process so that the bootstrap collection and the first level collection include the bare minimum resources required for that level. You achieve this by using collection proxies or factories with the "Exclude" checkbox enabled. Split resources according to the player's progress. This approach ensures efficient resource loading and keeps initial memory usage low. Learn more in the [Live Update manual](/manuals/live-update/).

## Android specific size optimizations
Android builds must support both 32-bit and 64-bit CPU architectures. When you [bundle for Android](/manuals/android) you can specify which CPU architectures to include:

![Signing Android bundle](images/android/sign_bundle.png)

Google Play has support for [multiple APKs](https://developer.android.com/google/play/publishing/multiple-apks) per release of a game, which means that you can reduce the application size by generating two APKs, one per CPU architecture, and uploading both to Google Play.

You can also make use of a combination of [APK Expansion Files](https://developer.android.com/google/play/expansion-files) and [Live Update content](/manuals/live-update) thanks to the [APKX extension in the Asset Portal](https://defold.com/assets/apkx/).
