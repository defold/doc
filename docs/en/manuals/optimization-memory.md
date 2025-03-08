---
title: Optimizing memory usage of a Defold game
brief: This manual describes how to optimize memory usage of a Defold game.
---

# Optimizing memory usage

## Texture compression
The use of texture compression will not only reduce the size of resources within your game archive, but compressed textures may also reduce the amount of GPU memory required.

## Dynamic loading
Most game have at least some content that is used infrequently. From a memory usage stand point it does not make sense to have such content loaded in memory at all times, but rather load and unload it when it is needed. This will obviously be a trade-off between having something readily accessible at the cost of runtime memory and loading something at the cost of loading time.

Defold has several different ways of loading content dynamically:

* [Collection proxies](/manuals/collection-proxy/)
* [Dynamic collection factories](/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [Dynamic factories](/manuals/factory/#dynamic-loading-of-factory-resources)
* [Live Update](/manuals/live-update/)

## Optimize component counters
Defold will allocate memory for components and resources once when a collection is created, to reduce memory fragmentation. The amount of memory that is allocated depends on the configuration of various components counters in *game.project*. Use the [profiler](/manuals/profiling/) to get accurate component and resource usage and configure your game to use max values that are closer to the real count of components and resources. This will reduce the amount of memory your game is using (refer to information about component [max count optimizations](/manuals/project-settings/#component-max-count-optimizations)).

## Optimize GUI node count
Optimize GUI node counts by setting the max number of nodes in the GUI file to only what is needed. The `Current Nodes` field of the [GUI component properties](https://defold.com/manuals/gui/#gui-properties) will show the number of nodes used by the GUI component.

:[HTML5 Optimizations](../shared/optimization-memory-html5.md)

