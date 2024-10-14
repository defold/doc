---
title: Native extensions - Best Practices
brief: This manual describes best practices when developing native extensions.
---

# Best Practices

Writing cross platform code can be difficult, but there are some ways to make it easier to both develop and maintain such code.


## Project structure

When creating an extension, there are a few things that help out in developing it as well as maintaining it.

### Lua API

There should only be one Lua API, and one implementation of it. This makes it a lot easier to have the same behaviour for all platforms.

If the platform in question shouldn't support the extension, it is recommended to simply not registering a Lua module at all. That way you can detect support by checking for nil:

```lua
    if myextension ~= nil then
        myextension.do_something()
    end
```

### Folder structure

The following folder structure is used frequently for extensions:

```
    /root
        /input
        /main                            -- All the files for the actual example project
            /...
        /myextension                     -- The actual root folder of the extension
            ext.manifest
            /include                     -- External includes, used by other extensions
            /libs
                /<platform>              -- External libraries for all supported platforms
            /src
                myextension.cpp          -- The extension Lua api and the extension life cycle functions
                                            Also contains generic implementations of your Lua api functions.
                myextension_private.h    -- Your internal api that each platform will implement (I.e. `myextension_Init` etc)
                myextension.mm           -- If native calls are needed for iOS/macOS. Implements `myextension_Init` etc for iOS/macOS
                myextension_android.cpp  -- If JNI calls are needed for Android. Implements `myextension_Init` etc for Android
                /java
                    /<platform>          -- Any java files needed for Android
            /res                         -- Any resources needed for a platform
            /external
                README.md                -- Notes/scripts on how to build or package any external libraries
        /bundleres                       -- Resources that should be bundles for (see game.project and the [bundle_resources setting]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Any extra app configuration info
```

Note that the `myextension.mm` and `myextension_android.cpp` are only needed if you are doing specific native calls for that platform.

#### Platform folders

In certain places, the platform architecture is used as a folder name, to know what files to use when compiling/bundling the application. These are of the form:

    <architecture>-<platform>

The current list is:

    arm64-ios, armv7-ios, x86_64-ios, arm64-android, armv7-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

So for instance, put platform specific libraries under:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## Writing native code

In the Defold source, C++ is used very sparingly and most code is very C-like. There is hardly any templates, except for a few container classes, since templates incurs a cost on compilation times as well as executable size.

### C++ version

The Defold source is built with the default C++ version of each compiler. The Defold source itself uses no C++ version higher than C++98. While it is possible to use a higher version to build an extension, a higher version might come with ABI changes. This might make it impossible to use one extension in conjunction with an extensions in the engine or from the [asset portal](/assets).

The Defold source avoids using the latest features or versions of C++. Mostly because there is no need for new features when building a game engine, but also because keeping track of the latest features of C++ is a time consuming task, and to really master those features will require a lot of precious time.

It also has the added benefit for extension developers that Defold maintains a stable ABI. Also worth pointing out is that using the latest C++ features may prevent the code from compiling on different platforms due to varying support.

### No C++ Exceptions

Defold does not make use of any exceptions in the engine. Exceptions are generally avoided in game engines, since the data is (mostly) known beforehand, during development. Removing the support for C++ exceptions decreases executable size and improves the runtime performance.

### Standard Template Libraries - STL

Since the Defold engine doesn't use any STL code, except for some algorithms and math (`std::sort`, `std::upper_bound` etc), it may work for you to use STL in your extension.

Again, bear in mind that ABI incompatibilities may hinder you when using your extension in conjunction with other extensions or 3rd party libraries.

Avoiding the (heavily templated) STL libraries, also improves on our build times, and more importantly, the executable size.

#### Strings

In the Defold engine `const char*` is used instead of `std::string`. The use `std::string` is a common pitfall when mixing different versions of C++ or compiler versions since it may result in an ABI mismatch. Using `const char*` and a few helper functions will avoid this.

### Make functions hidden

Use the `static` keyword on functions local to your compile unit if possible. This lets the compiler do some optimizations, and can both improve performance as well as reduce executable size.

## 3rd party libraries

When choosing a 3rd party library to use (regardless of language), consider the following:

* Functionality - Does it solve the particular problem you have?
* Performance - Does it infer a performance cost in the runtime?
* Library size - How much bigger will the final executable be? Is it acceptable?
* Dependencies - Does it require extra libraries?
* Support - What state is the library in? Does it have many open issues? Is it still maintained?
* License - Is it ok to use for this project?


## Open source dependencies

Always make sure that you have access to your dependencies. E.g. if you depend on something on GitHub, there's nothing preventing that repository from either being removed, or suddenly change direction or ownership. You can mitigate this risk by forking the repository and using your fork instead of the upstream project.

Remember that the code in the library will be injected into your game, so make sure the library does what it's supposed to do, and nothing more!

