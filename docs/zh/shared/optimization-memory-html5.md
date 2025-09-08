## 堆大小 (HTML5)
Defold HTML5 游戏的堆大小可以在 *game.project* 中的 [`heap_size` 字段](/manuals/project-settings/#heap-size) 进行配置。请确保优化您游戏的内存使用并设置最小的堆大小。

对于小型游戏，32 MB 是一个可实现的堆大小。对于较大的游戏，目标应为 64–128 MB。例如，如果您当前使用 58 MB 且进一步优化不可行，您可以设定为 64 MB 而不必过度纠结。没有严格的目标大小 — 这取决于游戏。只需尽量追求更小的大小，理想情况下以 2 的幂次方为步长。

要检查当前堆使用情况，您可以启动游戏并在最"资源密集"的关卡或部分中进行游戏，然后监控内存使用情况：

```lua
if html5 then
    local mem = tonumber(html5.run("HEAP8.length") / 1024 / 1024)
    print(mem)
end
```

您也可以打开浏览器的开发者工具，并在控制台中输入以下内容：

```js
HEAP8.length / 1024 / 1024
```

如果内存使用量保持在 32 MB，那就太好了！如果没有，请按照以下步骤[优化引擎本身以及声音和纹理等大型资源的大小](/manuals/optimization-size)。