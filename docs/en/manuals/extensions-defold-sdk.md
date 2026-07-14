---
title: Native extensions - Defold SDK
brief: This manual describes how to work with the Defold SDK when creating native extensions.
---

# The Defold SDK

The Defold SDK contains the required functionality to declare a native extension as well as interface with the low-level native platform layer on which the application runs and the high-level Lua layer in which the game logic is created.

## Usage

C++ extensions can include the aggregate `dmsdk/sdk.h` header file:

```cpp
#include <dmsdk/sdk.h>
```

The aggregate header includes C++ declarations and cannot be included from a C source file. C source files should include the individual C-compatible `.h` headers they require, for example:

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

Only part of dmSDK currently has a pure-C interface; not every C++ subsystem has a C equivalent. The available functions and types are documented in the [C API overview](/ref/overview_defoldc/) and [C++ API overview](/ref/overview_defoldcpp/). The Defold SDK headers are included as a separate `defoldsdk_headers.zip` archive for each Defold [release on GitHub](https://github.com/defold/defold/releases). You can use these headers for code completion in your editor of choice.
