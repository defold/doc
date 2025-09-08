---
title: 优化 Defold 游戏的内存使用
brief: 本手册描述了如何优化 Defold 游戏的内存使用。
---

# 优化内存使用

## 纹理压缩
使用纹理压缩不仅可以减少游戏存档中的资源大小，压缩后的纹理还可能减少所需的 GPU 内存量。

## 动态加载
大多数游戏至少有一些内容使用不频繁。从内存使用的角度来看，一直将这样的内容加载在内存中是没有意义的，而是在需要时加载和卸载它。这显然是在以运行时内存为代价使某些内容易于访问，和以加载时间为代价加载某些内容之间的权衡。

Defold 有几种不同的动态加载内容的方式：

* [集合代理](/manuals/collection-proxy/)
* [动态集合工厂](/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [动态工厂](/manuals/factory/#dynamic-loading-of-factory-resources)
* [实时更新](/manuals/live-update/)

## 优化组件计数器
Defold 会在创建集合时为组件和资源分配一次内存，以减少内存碎片。分配的内存量取决于 *game.project* 中各种组件计数器的配置。使用[分析器](/manuals/profiling/)获取准确的组件和资源使用情况，并将您的游戏配置为使用更接近组件和资源实际数量的最大值。这将减少您的游戏使用的内存量（请参阅有关组件[最大计数优化](/manuals/project-settings/#component-max-count-optimizations)的信息）。

## 优化 GUI 节点数量
通过将 GUI 文件中的最大节点数设置为仅需要的数量来优化 GUI 节点数量。[GUI 组件属性](https://defold.com/manuals/gui/#gui-properties)中的`当前节点`字段将显示 GUI 组件使用的节点数量。

:[HTML5 优化](../shared/optimization-memory-html5.md)