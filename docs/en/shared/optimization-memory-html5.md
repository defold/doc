## Heap size (HTML5)
The heap size of a Defold HTML5 game can be configured from the [`heap_size` field](/manuals/project-settings/#heap-size) in *game.project*. Make sure to optimize memory usage of your game and set a minimal heap size.

For small games, 32 MB is an achievable heap size. For larger games, aim for 64–128 MB. If, for example, you're at 58 MB and further optimization isn't feasible, you can settle on 64 MB without overthinking it. There’s no strict target size — it depends on the game. Just aim for smaller sizes, ideally in steps of powers of two. 

To check current heap usage you can launch your game and play the game in the most "resource heavy" level or section and monitor memory usage:

```lua
if html5 then
    local mem = tonumber(html5.run("HEAP8.length") / 1024 / 1024)
    print(mem)
end
```

You can also open the developer tools of your browser and write the following in the console:

```js
HEAP8.length / 1024 / 1024
```

If the memory usage remains at 32 MB, that's great! If not, follow the steps to [optimize memory usage](/manuals/optimization-memory).