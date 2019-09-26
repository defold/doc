---
title: Native extensions - Defold SDK
brief: This manual describes how to work with the Defold SDK when creating native extensions.
---

# The Defold SDK

The Defold SDK contains the required functionality to declare a native extension as well as interface with the low-level native platform layer on which the application runs and the high-level Lua layer in which the game logic is created.

## Usage

You use the Defold SDK by including the `dmsdk/sdk.h` header file:

    #include <dmsdk/sdk.h>

The header file is not publicly published but all of the available SDK functions are documented in our [API reference](/ref/dmExtension/). The SDK contains the following namespaces with functions:

* [Align](/ref/dmAlign/) - Alignment macros. Use for compiler compatibility
* [Array](/ref/dmArray/) - Templatized array with bounds checking.
* [Buffer](/ref/dmBuffer/) - Buffer API for data buffers as the main way to communicate between systems. [Lua API](/ref/buffer/) for buffer creation also exists.
* [Condition Variable](/ref/dmConditionVariable/) - API for platform independent mutex synchronization primitive.
* [ConfigFile](/ref/dmConfigFile/) - Configuration file access functions. The configuration file is compiled version of the game.project file.
* [Extension](/ref/dmExtension/) - Functions for creating and controlling engine native extension libraries.
* [Graphics](/ref/dmGraphics/) - Platform specific native graphics functions.
* [Hash](/ref/dmHash/) - Hash functions.
* [Json](/ref/dmJson/) - API for platform independent parsing of json files.
* [Log](/ref/dmLog/) - Logging functions.
* [Mutex](/ref/dmMutex/) - API for platform independent mutex synchronization primitive
* [Script](/ref/dmScript/) - Built-in scripting functions.
* [Shared Library](/ref/sharedlibrary/) - Utility functions for shared library export/import
* [Sony vector Math Library](/manuals/assets/Vector_Math_Library-Overview.pdf) - The Sony Vector Math library mainly provides functions used in 3-D graphics for 3-D and 4-D vector operations, matrix operations, and quaternion operations.
