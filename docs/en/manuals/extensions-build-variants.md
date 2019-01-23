---
title: Native extensions - Build variants
brief: This manual describes the different builds variants that Defold can create and how they interact with native extensions and the engine.
---

# Native Extensions - Build Variants

## Build Variants

When you bundle a game, you need to choose what type of engine you wish to use.

  * Debug
  * Release
  * Headless

These different versions are also referred to as `Build variants`

Note: When you choose `Build and run` you'll get the debug version.

### Debug

This type of executable still has the debugging feature left inside it, such as profiling, logging and hot reload. This variant is chosen during development of the game.

### Release

This variant has the debugging features disabled. This options is chosen when the game is ready to be released to the app store.

### Headless

This executable runs without any graphics and sound. It means that you can run the game unit/smoke tests on a CI server, or even have it as a game server in the cloud.

## App Manifest

Not only can you add native code to the engine with the Native Extensions feature, you can also remove standard parts of the engine. E.g. if you don't need a physics engine, you can remove that from the executable.

We support this via a file called an `App Manifest` (.appmanifest). In such a file, you can configure what libraries or symbols to remove, or perhaps add compile flags

This feature is still being developed and improved.

### Combined context

The app manifest actually has the same structure and syntax as the extension manifest. This allows us to merge the contexts for one platform together when finally building.

And, Defold itself, has its own build manifest as the foundation (`build.yml`). For each extension that is built, the manifests are combined as follows:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

This is so the user can override the default behaviour of the engine and also each extension. And, for the final link stage, we merge the app manifest with the defold manifest:

	manifest = merge(game.appmanifest, build.yml)

### Editing

Currently, the process can be done manually, but we recommend our users to use the [Manifestation](https://britzl.github.io/manifestation/) tool to create their app manifest. Eventually, the creation and modification of the app manifests will be done in the Editor.

### Syntax

Here is an example from the [Manifestation](https://britzl.github.io/manifestation/) tool for reference (Subject to change. Don't copy this file directly. Instead, use the online tool):

	platforms:
	    x86_64-osx:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    x86_64-linux:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    js-web:
	        context:
	            excludeLibs: []
	            excludeJsLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    wasm-web:
	        context:
	            excludeLibs: []
	            excludeJsLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    x86-win32:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    x86_64-win32:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    armv7-android:
	        context:
	            excludeLibs: []
	            excludeJars: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    armv7-ios:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []
	    arm64-ios:
	        context:
	            excludeLibs: []
	            excludeSymbols: []
	            libs: []
	            linkFlags: []


#### White listing

For all the keywords, we apply white listing filter. This is to avoid illegal path handling and accessing files outside of the build upload folder.

#### linkFlags

Here you can add flags to the specific platform compiler.

#### libs

This flag is only used if you wish to add a library that is part of the platform or Defold SDK. All libraries in your app's extensions are added automatically, and you shouldn't add those to this flag. Here's an example where the 3D physics is removed from the engine:

    x86_64-linux:
        context:
            excludeLibs: ["physics","LinearMath","BulletDynamics","BulletCollision"]
            excludeSymbols: []
            libs: ["physics_2d"]
            linkFlags: []

#### Exclude flags

These flags are used to remove things previously defined in the platform context. Here's an example of how to remove the Facebook extension from the engine (Note the `(.*)` which is a regexp to help remove the correct items).

    armv7-android:
        context:
            excludeLibs: ["facebookext"]
            excludeJars: ["(.*)/facebooksdk.jar","(.*)/facebook_android.jar"]
            excludeSymbols: ["FacebookExt"]
            libs: []
            linkFlags: []

#### Where's the list of all flags, libraries, symbols???

We might put some of them here, but we also think our time is better spent completing the feature of moving the manifest configuration into the Editor, making it a seamless step for the user.

In the meantime, we'll keep the [Manifestation](https://britzl.github.io/manifestation/) tool updated.
