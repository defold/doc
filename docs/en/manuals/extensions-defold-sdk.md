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

## Graphics adapter installation in 1.14.2

The engine normally installs its graphics adapter before initializing extensions. The following migration applies to custom engine hosts and native code that owns graphics initialization; ordinary extensions should use the engine's existing graphics context.

From Defold 1.14.2, `dmGraphics::InstallAdapter()` returns `dmGraphics::Result` instead of `bool`. Success is `dmGraphics::RESULT_OK`, whose value is zero. Replace boolean success checks with an explicit comparison:

```cpp
#include <dmsdk/graphics/graphics.h>

// Automatic selection before creating a graphics context.
dmGraphics::Result result = dmGraphics::InstallAdapter();
if (result != dmGraphics::RESULT_OK)
{
    // Report failure and stop graphics initialization.
}
```

The results are:

| Result | Meaning |
|---|---|
| `RESULT_OK` | An adapter was installed successfully. |
| `RESULT_ADAPTER_UNAVAILABLE` | No matching adapter is registered; for automatic selection, none are registered. |
| `RESULT_ADAPTER_UNSUPPORTED` | A matching adapter is registered but unsupported; for automatic selection, none of the registered adapters are supported. |

`InstallAdapter()` without arguments selects the highest-priority supported registered adapter. `InstallAdapter(family)` considers only the requested family and never falls back to another family. `ADAPTER_FAMILY_NONE` does not request automatic selection; use the no-argument overload instead.

Installation checks adapter support but does not create a window or graphics context. A successful return therefore does not guarantee that subsequent context creation will succeed. The engine handles startup fallback separately. Delete an existing graphics context before changing adapters or calling `dmGraphics::Finalize()`; reinstalling the current adapter succeeds without reinitializing it.

See the [graphics SDK declarations](https://github.com/defold/defold/blob/62f039ae1fafc5a036563fd8f44edf269288254f/engine/graphics/src/dmsdk/graphics/graphics.h) for the API introduced by this change.
