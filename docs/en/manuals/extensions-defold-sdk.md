---
title: Native extensions - Defold SDK
brief: This manual describes how to work with the Defold SDK when creating native extensions.
---

# The Defold SDK

The Defold SDK contains the required functionality to declare a native extension as well as interface with the low-level native platform layer on which the application runs and the high-level Lua layer in which the game logic is created.

## Usage

You use the Defold SDK by including the `dmsdk/sdk.h` header file:

    #include <dmsdk/sdk.h>

The available SDK functions are documented in our [API reference](/ref/dmExtension/). The SDK contains the following namespaces with functions:

* [Align](/ref/dmAlign/) - Alignment macros. Use for compiler compatibility
* [Array](/ref/dmArray/) - Templatized array with bounds checking.
* [Buffer](/ref/dmBuffer/) - Buffer API for data buffers as the main way to communicate between systems. [Lua API](/ref/buffer/) for buffer creation also exists.
* [Condition Variable](/ref/dmConditionVariable/) - API for platform independent mutex synchronization primitive.
* [ConfigFile](/ref/dmConfigFile/) - Configuration file access functions. The configuration file is compiled version of the *game.project* file.
* [Connection Pool](/ref/dmConnectionPool/) - API for a pool of socket connections.
* [Crypt](/ref/dmCrypt/) - API with cryptographic functions.
* [DNS](/ref/dmDNS/) - API with DNS functions.
* [Engine](/ref/dmEngine/) - API with core engine functionality to get handles to config files, the internal web server, game object register etc.
* [Extension](/ref/dmExtension/) - Functions for creating and controlling engine native extension libraries.
* [Game Object](/ref/dmGameObject/) - API for manipulating game objects.
* [Graphics](/ref/dmGraphics/) - Platform specific native graphics functions.
* [Hash](/ref/dmHash/) - Hash functions.
* [HID](/ref/dmHid/) - API for generating programmatic input events.
* [HTTP Client](/ref/dmHttpClient/) - API for interacting with a HTTP clients.
* [Json](/ref/dmJson/) - API for platform independent parsing of json files.
* [Log](/ref/dmLog/) - Logging functions.
* [Math](/ref/dmMath/) - API with mathematical functions.
* [Mutex](/ref/dmMutex/) - API for platform independent mutex synchronization primitive.
* [SSL Socket](/ref/dmSSLSocket/) - API for secure socket functions.
* [Script](/ref/dmScript/) - Built-in scripting functions.
* [Socket](/ref/dmSocket/) - API for socket functions.
* [String Functions](/ref/dmStringFunc/) - API for manipulating strings.
* [Thread](/ref/dmThread/) - API for thread creation.
* [Time](/ref/dmTime/) - API for universal time and timing functions.
* [URI](/ref/dmURI/) - API for manipulation of URIs.
* [Web Server](/ref/dmWebServer/) - API for a simple high-level single-threaded Web server based on `dmHttpServer`.
* [Shared Library](/ref/sharedlibrary/) - Utility functions for shared library export/import.
* [Sony vector Math Library](../assets/Vector_Math_Library-Overview.pdf) - The Sony Vector Math library mainly provides functions used in 3-D graphics for 3-D and 4-D vector operations, matrix operations, and quaternion operations.

The Defold SDK headers are included as a separate `defoldsdk_headers.zip` archive for each Defold [release on GitHub](https://github.com/defold/defold/releases). You can use these headers for code completion in your editor of choice.