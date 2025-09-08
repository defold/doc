---
title: Defold 资源管理
brief: 本手册解释了 Defold 如何自动管理资源以及如何手动管理资源加载以遵守内存占用和包体大小限制。
---

# 资源管理

如果您制作一个非常小的游戏，目标平台的限制（内存占用、包体大小、计算能力和电池消耗）可能不会造成任何问题。然而，当制作较大的游戏时，尤其是在手持设备上，内存消耗很可能成为最大的限制之一。有经验的团队会根据平台限制仔细制定资源预算。Defold 提供了一系列功能来帮助管理内存和包体大小。本手册概述了这些功能。

## 静态资源树

当您在 Defold 中构建游戏时，您会静态声明资源树。游戏的每个部分都链接到树中，从引导集合（通常称为"main.collection"）开始。资源树跟随任何引用，并包含与这些引用关联的所有资源：

- 游戏对象和组件数据（图集、声音等）。
- 工厂组件原型（游戏对象和集合）。
- 集合代理组件引用（集合）。
- 在 *game.project* 中声明的[自定义资源](/manuals/project-settings/#custom-resources)。

![Resource tree](images/resource/resource_tree.png)

::: sidenote
Defold 还有一个[捆绑资源](/manuals/project-settings/#bundle-resources)的概念。捆绑资源包含在应用程序包中，但不是资源树的一部分。捆绑资源可以是从平台特定的支持文件到[从文件系统加载](/manuals/file-access/#how-to-access-files-bundled-with-the-application)并由您的游戏使用的外部文件的任何内容（例如 FMOD 声音库）。
:::

当游戏被*打包*时，只有资源树中的内容才会被包含。任何在树中没有引用的内容都会被排除。无需手动选择要包含或排除在包中的内容。

当游戏*运行*时，引擎从树的引导根开始，将资源拉入内存：

- 任何引用的集合及其内容。
- 游戏对象和组件数据。
- 工厂组件原型（游戏对象和集合）。

但是，引擎在运行时不会自动加载以下类型的引用资源：

- 通过集合代理引用的游戏世界集合。游戏世界相对较大，因此您需要在代码中手动触发这些集合的加载和卸载。详情请参阅[集合代理手册](/manuals/collection-proxy)。
- 通过 *game.project* 中的*自定义资源*设置添加的文件。这些文件使用[`sys.load_resource()`](/ref/sys/#sys.load_resource)函数手动加载。

Defold 打包和加载资源的默认方式可以被改变，以对资源如何以及何时进入内存进行细粒度控制。

![Resource loading](images/resource/loading.png)

## 动态加载工厂资源

工厂组件引用的资源通常在组件加载时被加载到内存中。然后，一旦工厂存在于运行时中，这些资源就可以准备好被生成到游戏中。要更改默认行为并推迟工厂资源的加载，您可以简单地将工厂标记为*动态加载*复选框。

![Load dynamically](images/resource/load_dynamically.png)

选中此框后，引擎仍会将引用的资源包含在游戏包中，但不会自动加载工厂资源。相反，您有两个选择：

1. 调用[`factory.create()`](/ref/factory/#factory.create)或[`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create)来生成对象。这将同步加载资源，然后生成新实例。
2. 调用[`factory.load()`](/ref/factory/#factory.load)或[`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load)来异步加载资源。当资源准备好生成时，会收到一个回调。

请阅读[工厂手册](/manuals/factory)和[集合工厂手册](/manuals/collection-factory)以了解其工作原理的详细信息。

## 卸载动态加载的资源

Defold 为所有资源保留引用计数器。如果资源的计数器达到零，这意味着没有任何东西再引用它。然后资源会自动从内存中卸载。例如，如果您删除了工厂生成的所有对象，并且还删除了持有工厂组件的对象，那么工厂先前引用的资源将从内存中卸载。

对于标记为*动态加载*的工厂，您可以调用[`factory.unload()`](/ref/factory/#factory.unload)或[`collectionfactory.unload()`](/ref/collectionfactory/#collectionfactory.unload)函数。此调用会移除工厂组件对资源的引用。如果没有其他东西引用该资源（例如，所有生成的对象都被删除），资源将从内存中卸载。

## 从包中排除资源

使用集合代理，可以将组件引用的所有资源从打包过程中排除。如果您需要将包体大小保持在最小，这很有用。例如，当在网络上作为 HTML5 运行游戏时，浏览器会在执行游戏之前下载整个包。

![Exclude](images/resource/exclude.png)

通过将集合代理标记为*排除*，引用的资源将被排除在游戏包之外。相反，您可以将排除的集合存储在选定的云存储上。[实时更新手册](/manuals/live-update/)解释了此功能的工作原理。
