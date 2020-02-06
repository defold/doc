---
title: Native extensions - Best Practices
brief: This manual describes best practices when developing native extensions.
---

# Best Practices

Writing cross platform code can be difficult, but there are some ways to make it easier to both develop and maintain. In this manual we list some ways we at Defold work with cross platform native code and APIs.

## Defold code

In the Defold engine we use C++ very sparingly. In fact, most code is very C-like. We avoid templates, except for a few container classes, due to the fact that templates both incurs a cost on compilation times as well as executable size.

### C++ version

The Defold source is built with the default C++ version of each compiler (See [Native Extensions - Best Practices](/manuals/extensions-best-practices/)).

We avoid using the latest features or versions of C++. Mostly because we already have what we need to build a game engine. Keeping track of the latest features of C++ is a time consuming task, and to really master those features will require a lot of precious time.

It also has the added benefit for our extension developers that we keep a stable ABI. Also worth pointing out is that using the latest C++ features may prevent the code from compiling on different platforms due to varying support.

### Standard Template Libraries - STL

Since the Defold engine doesn't use any STL code, except for some algorithms and math (std::sort, std::upper_bound etc), it may work for you to use STL in your extension.

Again, bear in mind that ABI incompatibilites may hinder you when using your extension in conjunction with other extensions or 3rd party libraries.

Avoiding the (heavily templated) STL libraries, also improves on our build times, and more importantly, the executable size.

#### Strings

In the Defold engine, we use `const char*` instead of `std::string`.

`std::string` is a common pitfall when mixing different versions of C++ or compiler versions: you'll get an ABI mismatch.
For us, it's better to use `const char*` and a few helper functions.

### Make functions hidden

Use the `static` keywork on functions local to your compile unit if possible. This lets the compiler do some optimizations, and can both improve performance as well as reduce executable size.

## 3rd party libraries

When choosing a 3rd party library to use (regardless of language), we consider at least these things:

* Functionality - Does it solve the particular problem you have?
* Performance - Does it infer a performance cost in the runtime?
* Library size - How much bigger will the final executable be? Is it acceptable?
* Dependencies - Does it require extra libraries?
* Support - What state is the library in? Does it have many open issues? Is it still maintained?
* License - Is it ok to use for this project?


## Open source dependencies

Always make sure that you have access to your dependencies. E.g. if you depend on something on GitHub, there's nothing preventing that repository either being removed, or suddenly changes direction or ownership. You can mitigate this risk by forking the repository and using your fork instead of the upstream project.

The code in that library will be injected into your game, so make sure the library does what it's supposed to do, and nothing more!


## Project structure

When creating an extension, there are a few things that help out in developing it as well as maintaining it.

### Lua api

There should only be one Lua api, and one implementation of it. This makes it a lot easier to behave the same for all platforms.

If the platform in question shouldn't support the extension, we recommend simply not registering a Lua module at all.
That way you can detect support by checking for nil:

    if myextension ~= nil then
        myextension.do_something()
    end

### Folder structure

Here is a folder structure that we use frequently for our extensions.

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


Note that the `myextension.mm` and `myextension_android.cpp` are only needed if you are doing specific native calls for that platform.

#### Platform folders

In certain places, we use the platform architecture as a folder name, to know what files to use when compiling/bundling the application.
These are of the form:

    <architecture>-<platform>

The current list is:

    arm64-ios, armv7-ios, x86_64-ios, arm64-android, armv7-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

So for instance, put platform specific libraries under:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a
