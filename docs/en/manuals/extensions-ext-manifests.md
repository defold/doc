---
title: Native extensions - extension manifests
brief: This manual describes the extension manifest and how it correlates to the application manifest and engine manifest.
---

# Extension, Application and Engine manifest files

The extension manifest is a configuration file with flags and defines used when building a single extension. This configuration is combined with an application level configuration and a base level configuration for the Defold engine itself.

## App Manifest

The application manifest (file extension `.appmanifest`) is an application level configuration of how to build your game on the build servers. The application manifest lets you remove parts of the engine that you don't use. If you don't need a physics engine, you can remove that from the executable to reduce it's size. Learn how to exclude unused feature [in the application manifest manual](/manuals/app-manifest).

## Engine manifest

The Defold engine has a build manifest (`build.yml`) which is included with each release of the engine and the Defold SDK. The manifest controls which SDK versions to use, which compilers, linkers and other tools to run and which default build and link flags to pass to these tools. The manifest can be found in share/extender/build_input.yml [on GitHub](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml).

## Extension Manifest

The extension manifest (`ext.manifest`) on the other hand is a configuration file specifically for an extension. The extension manifest controls how the source code of the extension is compiled and linked and which additional libraries to include. 

The three different manifest files all share the same syntax so that they can be merged and fully control how the extensions and the game is built.

For each extension that is built, the manifests are combined as follows:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

This allows the user to override the default behaviour of the engine and also each extension. And, for the final link stage, we merge the app manifest with the defold manifest:

	manifest = merge(game.appmanifest, build.yml)


### The ext.manifest file

Apart from the name of the extension, the manifest file can contain platform specific compile flags, link flags, libs and frameworks. If the *ext.manifest* file does not contain a "platforms" segment, or a platform is missing from the list, the platform you bundle for will still build, but without any extra flags set.

Here is an example:

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    armv7-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### Allowed keys

Allowed keys are for platform specific compile flags are:

* `frameworks` - Apple frameworks to include when building (iOS and OSX)
* `flags` - Flags that should be passed to the compiler
* `linkFlags` - Flags that should be passed to the linker
* `libs` - Additional libraries to include when linking
* `defines` - Defines to set when building
* `aaptExtraPackages` - Extra package name that should be generated (Android)
* `aaptExcludePackages` - Regexp (or exact names) of packages to exclude (Android)
* `aaptExcludeResourceDirs` - Regexp (or exact names) of resource dirs to exclude (Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` - These flags are used to remove things previously defined in the platform context.

For all the keywords, we apply white listing filter. This is to avoid illegal path handling and accessing files outside of the build upload folder.
