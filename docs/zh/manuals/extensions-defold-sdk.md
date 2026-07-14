---
title: 原生扩展 - Defold SDK
brief: 本手册介绍了创建原生扩展时如何使用 Defold SDK。
---

# Defold SDK

Defold SDK 包含了声明原生扩展所需的功能，以及与应用运行的原生平台底层接口和创建游戏逻辑的高层Lua层进行交互的功能。

## 用法

C++ 扩展可以包含聚合头文件 `dmsdk/sdk.h`：

```cpp
#include <dmsdk/sdk.h>
```

该聚合头文件包含 C++ 声明，不能从 C 源文件中包含。C 源文件应包含它们所需的各个 C 兼容 `.h` 头文件，例如：

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

目前 dmSDK 只有一部分具有纯 C 接口；并非每个 C++ 子系统都有对应的 C 接口。可用函数和类型详见 [C API 概览](/ref/overview_defoldc/) 和 [C++ API 概览](/ref/overview_defoldcpp/)。Defold SDK 头文件作为单独的 `defoldsdk_headers.zip` 压缩包包含在每个 Defold [GitHub 发布版本](https://github.com/defold/defold/releases)中。您可以在自选编辑器中使用这些头文件进行代码补全。
