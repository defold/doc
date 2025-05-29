---
title: Native extensions - Defold SDK
brief: This manual describes how to work with the Defold SDK when creating native extensions.
---

# The Defold SDK

The Defold SDK contains the required functionality to declare a native extension as well as interface with the low-level native platform layer on which the application runs and the high-level Lua layer in which the game logic is created.

## Usage

You use the Defold SDK by including the `dmsdk/sdk.h` header file:

    #include <dmsdk/sdk.h>

The available SDK functions and namespaces are documented in our [API reference](/ref/overview_cpp). The Defold SDK headers are included as a separate `defoldsdk_headers.zip` archive for each Defold [release on GitHub](https://github.com/defold/defold/releases). You can use these headers for code completion in your editor of choice.