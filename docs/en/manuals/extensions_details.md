
# The Defold build setup

Here we list some relevant build information, in order to make the integrations with your extensions as easy as possible.

Here are some things to consider when you create an extension for the Defold engine.

# Static linkage

The custom engine is built using static linkage.
The main reason is that on iOS, multiple executable binaries in an .ipa aren't allowed in the app store.

# No Exceptions:

We don't make use of any exceptions in the engine, as it decreases executable size and improves the runtime performance. This may be beneficial for you to if you wish to get a minimal extension.

# C++ version

In the engine itself we use no C++ version higher than C++98. While you may use a higher version to build your extension, bear in mind that a higher version might come with ABI changes. This might make it impossible to use your extension in conjunction with other extensions in the engine or on the asset store.

When creating libraries (such as extensions), it's good to keep the lowest common denominator as a target.

# Standard Template Libraries - STL

Since the Defold engine doesn't use any STL code (except std::sort), it may work for you to use STL in your extension. Again, bear in mind that ABI incompatibilites may hinder you when using your extension in conjunction with other extensions.

In the Defold engine, we use `const char*` instead of `std::string`. And writing your own dynamic array or hash table isn't very hard, but there are also good alternatives found online.

# Toolchain

Clang - MscOS, iOS, (Win32)
GCC - Android, Linux (deprecated)
CL - Windows (deprecated)

_NOTE: We are aiming to compile all platforms with Clang in the near future in order to streamline our builds_

## SDK Versions

* Android:
* iOS: iPhoneOS11.2.sdk
* MacOS: MacOSX10.13.sdk
* Windows: WindowsKits 8.1 + 10.0, Microsoft Visual Studio 14.0
* Linux: Ubuntu 16.04, gcc 5.4.0, libssl-dev, uuid-dev, libxi-dev, libopenal-dev, libgl1-mesa-dev, libglw1-mesa-dev, freeglut3-dev
* Html5: Emscripten 1.35.0,

## C++ version + ABI compatibility

We build our engine using `-std=c++98`

For iOS/MacOS, we use `-miphoneos-version-min=6.0` and `-mmacosx-version-min=10.7` respectively.

* Linux: `GCC 5.4.0`
* Android:`GCC 4.8`
* Html5: `Emscripten 1.35.0`
* Win32: `Microsoft Visual Studio 14.0` alt `clang-6.0`
* iOS/MacOS: `apple-clang` alt `clang-6.0`

# Win32 + Clang

A recent addition is to be able to build the Windows builds using clang.
This allows for faster builds on our servers, and also it allows us to streamline our builds.

_NOTE: This feature is new, so it's not enabled by default yet_

You can use this feature by adding the flag `use-clang` to your app manifest:

    platforms:
        x86_64-win32:
            use-clang: true


## CL.exe / LINK.exe

Although this feature is still supported, it will soon be deprecated.





