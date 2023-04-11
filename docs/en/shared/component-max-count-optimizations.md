## Component max count optimizations
The *game.project* settings file contains many values specifying the maximum number of a certain resource that can exist at the same time, often counted per loaded collection (also called world). The Defold engine will use these max values to preallocate memory for this amount of memory to avoid dynamic allocations and memory fragmentation while the game is running.

The Defold data structures used to represent components and other resources are optimized to use as little memory as possible but care should still be taken when setting the values to avoid allocating more memory than is actually necessary.

To further optimize memory usage the Defold build process will analyse the content of the game and override the max counts if it is possible to know for certain the exact amount:

* If a collection doesn't contain any factory components the exact amount of each component will be allocated and the max count values will be ignored.
* If a collection contains a factory component the spawned objects will be analysed and the max count will be used for components that can be spawned from the factories.
* If a collection contains a factory or a collection factory with activated "Dynamic Prototype" option, this collection will use the max counters.
