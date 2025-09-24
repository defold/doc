---
title: 编辑器脚本
brief: 本手册解释了如何使用 Lua 扩展编辑器功能
---

# 编辑器脚本

您可以使用具有特殊扩展名的 Lua 文件创建自定义菜单项和编辑器生命周期钩子：`.editor_script`。使用此系统，您可以调整编辑器以增强您的开发工作流程。

## 编辑器脚本运行时

编辑器脚本在编辑器内部运行，在 Java 虚拟机模拟的 Lua 虚拟机中运行。所有脚本共享同一个环境，这意味着它们可以相互交互。您可以导入 Lua 模块，就像使用 `.script` 文件一样，但编辑器内部运行的 Lua 版本不同，因此请确保您的共享代码是兼容的。编辑器使用 Lua 版本 5.2.x，更具体地说是 [luaj](https://github.com/luaj/luaj) 运行时，这目前是在 JVM 上运行 Lua 的唯一可行解决方案。除此之外，还有一些限制：
- 没有 `debug` 包；
- 没有 `os.execute`，尽管我们提供了类似的 `editor.execute()`；
- 没有 `os.tmpname` 和 `io.tmpfile` — 目前编辑器脚本只能访问项目目录内的文件；
- 目前没有 `os.rename`，尽管我们希望添加它；
- 没有 `os.exit` 和 `os.setlocale`。
- 在编辑器需要脚本立即响应的上下文中，不允许使用一些长时间运行的函数，详见[执行模式](#execution-modes)。

所有在编辑器脚本中定义的编辑器扩展在您打开项目时都会加载。当您获取库时，扩展会重新加载，因为您依赖的库中可能有新的编辑器脚本。在此重新加载期间，不会获取您自己的编辑器脚本的更改，因为您可能正在更改它们。要同时重新加载它们，您应该运行 **Project → Reload Editor Scripts** 命令。

## `.editor_script` 的构成

每个编辑器脚本都应该返回一个模块，如下所示：
```lua
local M = {}

function M.get_commands()
  -- TODO - 定义编辑器命令
end

function M.get_language_servers()
  -- TODO - 定义语言服务器
end

function M.get_prefs_schema()
  -- TODO - 定义首选项
end

return M
```
然后编辑器会收集项目和库中定义的所有编辑器脚本，将它们加载到单个 Lua 虚拟机中，并在需要时调用它们（更多内容请参见[命令](#commands)和[生命周期钩子](#lifecycle-hooks)部分）。

## 编辑器 API

您可以使用定义此 API 的 `editor` 包与编辑器进行交互：
- `editor.platform` — 字符串，Windows 上为 `"x86_64-win32"`，macOS 上为 `"x86_64-macos"`，Linux 上为 `"x86_64-linux"`。
- `editor.version` — 字符串，Defold 的版本名称，例如 `"1.4.8"`
- `editor.engine_sha1` — 字符串，Defold 引擎的 SHA1
- `editor.editor_sha1` — 字符串，Defold 编辑器的 SHA1
- `editor.get(node_id, property)` — 获取编辑器内某个节点的值。编辑器中的节点是各种实体，例如脚本或集合文件，集合内的游戏对象，作为资源加载的 json 文件等。`node_id` 是由编辑器传递给编辑器脚本的 userdata。或者，您可以使用资源路径代替节点 id，例如 `"/main/game.script"`。`property` 是一个字符串。目前支持以下属性：
  - `"path"` — *资源* 的项目文件夹文件路径 — 作为文件或目录存在的实体。返回值示例：`"/main/game.script"`
  - `"children"` — 目录资源的子资源路径列表
  - `"text"` — 可编辑为文本的资源文本内容（例如脚本文件或 json）。返回值示例：`"function init(self)\nend"`。请注意，这与使用 `io.open()` 读取文件不同，因为您可以在不保存文件的情况下编辑文件，这些编辑仅在访问 `"text"` 属性时可用。
  - 对于图集：`images`（图集中图像的编辑器节点列表）和 `animations`（动画节点列表）
  - 对于图集动画：`images`（与图集中的 `images` 相同）
  - 对于瓦片地图：`layers`（瓦片地图中图层的编辑器节点列表）
  - 对于瓦片地图图层：`tiles`（瓦片的无限 2D 网格），详见 `tilemap.tiles.*`
  - 对于粒子效果：`emitters`（发射器编辑器节点列表）和 `modifiers`（修改器编辑器节点列表）
  - 对于粒子效果发射器：`modifiers`（修改器编辑器节点列表）
  - 对于碰撞对象：`shapes`（碰撞形状编辑器节点列表）
  - 对于 GUI 文件：`layers`（图层编辑器节点列表）
  - 当您在大纲视图中选择某些内容时，属性视图中显示的一些属性。这些类型的大纲属性支持：
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    请注意，其中一些属性可能是只读的，有些在不同上下文中可能不可用，因此您应该在读取它们之前使用 `editor.can_get`，在让编辑器设置它们之前使用 `editor.can_set`。将鼠标悬停在属性视图中的属性名称上，可以看到一个工具提示，其中包含有关该属性在编辑器脚本中如何命名的信息。您可以通过提供 `""` 值将资源属性设置为 `nil`。
- `editor.can_get(node_id, property)` — 检查您是否可以获取此属性，以便 `editor.get()` 不会抛出错误。
- `editor.can_set(node_id, property)` — 检查带有此属性的 `editor.tx.set()` 事务步骤不会抛出错误。
- `editor.create_directory(resource_path)` — 如果目录不存在，则创建目录，以及所有不存在的父目录。
- `editor.create_resources(resources)` — 创建 1 个或多个资源，可以从模板创建或使用自定义内容创建
- `editor.delete_directory(resource_path)` — 如果目录存在，则删除目录，以及所有存在的子目录和文件。
- `editor.execute(cmd, [...args], [options])` — 运行 shell 命令，可选择捕获其输出。
- `editor.save()` — 将所有未保存的更改持久化到磁盘。
- `editor.transact(txs)` — 使用 1 个或多个由 `editor.tx.*` 函数创建的事务步骤修改编辑器内存状态。
- `editor.ui.*` — 各种与 UI 相关的函数，请参见[UI 手册](/manuals/editor-scripts-ui)。
- `editor.prefs.*` — 与编辑器首选项交互的函数，请参见[首选项](#preferences)。

您可以在[此处](https://defold.com/ref/alpha/editor/)找到完整的编辑器 API 参考。

## 命令

如果编辑器脚本模块定义了函数 `get_commands`，它将在扩展重新加载时被调用，返回的命令将在编辑器的菜单栏或资源和大纲窗格的上下文菜单中可用。例如：
```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "删除注释",
      locations = {"Edit", "Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        local path = editor.get(opts.selection, "path")
        return ends_with(path, ".lua") or ends_with(path, ".script")
      end,
      run = function(opts)
        local text = editor.get(opts.selection, "text")
        editor.transact({
          editor.tx.set(opts.selection, "text", strip_comments(text))
        })
      end
    },
    {
      label = "压缩 JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        editor.execute("./scripts/minify-json.sh", path:sub(2))
      end
    }
  }
end

return M
```
编辑器期望 `get_commands()` 返回一个表数组，每个表描述一个单独的命令。命令描述包括：

- `label`（必需）— 将显示给用户的菜单项上的文本
- `locations`（必需）— 一个数组，包含 `"Edit"`、`"View"`、`"Project"`、`"Debug"`、`"Assets"`、`"Bundle"`、`"Scene"` 或 `"Outline"` 中的一个或多个，描述了该命令应该可用的位置。`"Edit"`、`"View"`、`"Project"` 和 `"Debug"` 表示顶部的菜单栏，`"Assets"` 表示资源窗格中的上下文菜单，`"Outline"` 表示大纲窗格中的上下文菜单，`"Bundle"` 表示 **Project → Bundle** 子菜单。
- `query` — 命令向编辑器询问相关信息并定义它操作的数据的一种方式。对于 `query` 表中的每个键，`opts` 表中将有相应的键，`active` 和 `run` 回调将作为参数接收。支持的键：
  - `selection` 表示此命令在有选择内容时有效，并且它对该选择进行操作。
    - `type` 是命令感兴趣的所选节点类型，目前允许的类型有：
      - `"resource"` — 在资源和大纲中，资源是具有相应文件的选定项。在菜单栏（编辑或视图）中，资源是当前打开的文件；
      - `"outline"` — 可以在大纲中显示的内容。在大纲中它是选定项，在菜单栏中它是当前打开的文件；
      - `"scene"` — 可以渲染到场景中的内容。
    - `cardinality` 定义应该有多少个选定项。如果是 `"one"`，传递给命令回调的选择将是单个节点 id。如果是 `"many"`，传递给命令回调的选择将是一个或多个节点 id 的数组。
  - `argument` — 命令参数。目前，只有 `"Bundle"` 位置中的命令接收参数，当明确选择打包命令时为 `true`，在重新打包时为 `false`。
- `id` - 命令标识符字符串，例如用于在 `prefs` 中持久化最后使用的打包命令
- `active` - 一个回调函数，用于检查命令是否处于活动状态，预期返回布尔值。如果 `locations` 包括 `"Assets"`、`"Scene"` 或 `"Outline"`，在显示上下文菜单时将调用 `active`。如果位置包括 `"Edit"` 或 `"View"`，则会在每次用户交互时调用 active，例如键盘输入或鼠标点击，因此请确保 `active` 相对较快。
- `run` - 当用户选择菜单项时执行的回调函数。

### 使用命令更改编辑器内存状态

在 `run` 处理程序中，您可以查询和更改编辑器的内存状态。查询使用 `editor.get()` 函数完成，您可以在其中询问编辑器有关文件和选择的当前状态（如果使用 `query = {selection = ...}`）。您可以获取脚本文件的 `"text"` 属性，以及属性视图中显示的一些属性 — 将鼠标悬停在属性名称上以查看工具提示，其中包含有关该属性在编辑器脚本中如何命名的信息。更改编辑器状态使用 `editor.transact()` 完成，您可以在其中将 1 个或多个修改捆绑在一个可撤销的步骤中。例如，如果您希望能够重置游戏对象的变换，您可以编写如下命令：
```lua
{
  label = "重置变换",
  locations = {"Outline"},
  query = {selection = {type = "outline", cardinality = "one"}},
  active = function(opts)
    local node = opts.selection
    return editor.can_set(node, "position") 
       and editor.can_set(node, "rotation") 
       and editor.can_set(node, "scale")
  end,
  run = function(opts)
    local node = opts.selection
    editor.transact({
      editor.tx.set(node, "position", {0, 0, 0}),
      editor.tx.set(node, "rotation", {0, 0, 0}),
      editor.tx.set(node, "scale", {1, 1, 1})
    })
  end
}
```

#### 编辑图集

除了读取和写入图集的属性外，您还可以读取和修改图集图像和动画。图集定义了 `images` 和 `animations` 节点列表属性，动画定义了 `images` 节点列表属性：您可以将 `editor.tx.add`、`editor.tx.remove` 和 `editor.tx.clear` 事务步骤与这些属性一起使用。

例如，要向图集添加图像，请在命令的 `run` 处理程序中执行以下代码：
```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```
要查找图集中的所有图像集，请执行以下代码：
```lua
local all_images = {} ---@type table<string, true>
-- 首先，收集所有"裸"图像
local image_nodes = editor.get("/main.atlas", "images")
for i = 1, #image_nodes do
    all_images[editor.get(image_nodes[i], "image")] = true
end
-- 其次，收集动画中使用的所有图像
local animation_nodes = editor.get("/main.atlas", "animations")
for i = 1, #animation_nodes do
    local animation_image_nodes = editor.get(animation_nodes[i], "images")
    for j = 1, #animation_image_nodes do
        all_images[editor.get(animation_image_nodes[j], "image")] = true
    end
end
pprint(all_images)
-- {
--     ["/assets/hero.png"] = true,
--     ["/assets/enemy.png"] = true,
-- }}
```
要替换图集中的所有动画：
```lua
editor.transact({
    editor.tx.clear("/main.atlas", "animations"),
    editor.tx.add("/main.atlas", "animations", {
        id = "hero_run",
        images = {
            {image = "/assets/hero_run_1.png"},
            {image = "/assets/hero_run_2.png"},
            {image = "/assets/hero_run_3.png"},
            {image = "/assets/hero_run_4.png"}
        }
    })
})
```

#### 编辑瓦片源

除了大纲属性外，瓦片源还定义了以下属性：
- `animations` - 瓦片源的动画节点列表
- `collision_groups` - 瓦片源的碰撞组节点列表
- `tile_collision_groups` - 瓦片源中瓦片的碰撞组分配表

例如，以下是设置瓦片源的方法：
```lua
local tilesource = "/game/world.tilesource"
editor.transact({
    editor.tx.add(tilesource, "animations", {id = "idle", start_tile = 1, end_tile = 1}),
    editor.tx.add(tilesource, "animations", {id = "walk", start_tile = 2, end_tile = 6, fps = 10}),
    editor.tx.add(tilesource, "collision_groups", {id = "player"}),
    editor.tx.add(tilesource, "collision_groups", {id = "obstacle"}),
    editor.tx.set(tilesource, "tile_collision_groups", {
        [1] = "player",
        [7] = "obstacle",
        [8] = "obstacle"
    })
})
```

#### 编辑瓦片地图

瓦片地图定义了 `layers` 属性，即瓦片地图图层的节点列表。每个图层还定义了 `tiles` 属性，该属性保存此图层上瓦片的无限 2D 网格。这与引擎不同：瓦片没有边界，可以添加到任何位置，包括负坐标。要编辑瓦片，编辑器脚本 API 定义了一个 `tilemap.tiles` 模块，具有以下功能：
- `tilemap.tiles.new()` 创建一个新的数据结构，用于保存无限的 2D 瓦片网格（在编辑器中，与引擎相反，瓦片地图是无限的，坐标可以是负数）
- `tilemap.tiles.get_tile(tiles, x, y)` 获取特定坐标处的瓦片索引
- `tilemap.tiles.get_info(tiles, x, y)` 获取特定坐标处的完整瓦片信息（数据形状与引擎的 `tilemap.get_tile_info` 函数相同）
- `tilemap.tiles.iterator(tiles)` 创建一个遍历瓦片地图中所有瓦片的迭代器
- `tilemap.tiles.clear(tiles)` 从瓦片地图中移除所有瓦片
- `tilemap.tiles.set(tiles, x, y, tile_or_info)` 在特定坐标处设置瓦片
- `tilemap.tiles.remove(tiles, x, y)` 移除特定坐标处的瓦片

例如，以下是打印整个瓦片地图内容的方法：
```lua
local layers = editor.get("/level.tilemap", "layers")
for i = 1, #layers do
    local layer = layers[i]
    local id = editor.get(layer, "id")
    local tiles = editor.get(layer, "tiles")
    print("layer " .. id .. ": {")
    for x, y, tile in tilemap.tiles.iterator(tiles) do
        print("  [" .. x .. ", " .. y .. "] = " .. tile)
    end
    print("}")
end
```

以下示例显示如何向瓦片地图添加带有瓦片的图层：
```lua
local tiles = tilemap.tiles.new()
tilemap.tiles.set(tiles, 1, 1, 2)
editor.transact({
    editor.tx.add("/level.tilemap", "layers", {
        id = "new_layer",
        tiles = tiles
    })
})
```

#### 编辑粒子效果

您可以使用 `modifiers` 和 `emitters` 属性编辑粒子效果。例如，添加带有加速度修改器的圆形发射器的方法如下：
```lua
editor.transact({
    editor.tx.add("/fire.particlefx", "emitters", {
        type = "emitter-type-circle",
        modifiers = {
          {type = "modifier-type-acceleration"}
        }
    })
})
```
许多粒子效果属性是曲线或曲线扩展（即曲线 + 一些随机值）。曲线表示为具有非空 `points` 列表的表，其中每个点是具有以下属性的表：
- `x` - 点的 x 坐标，应从 0 开始，以 1 结束
- `y` - 点的值
- `tx`（0 到 1）和 `ty`（-1 到 1）- 点的切线。例如，对于 80 度角，`tx` 应该是 `math.cos(math.rad(80))`，`ty` 应该是 `math.sin(math.rad(80))`。
曲线扩展还具有 `spread` 数字属性。

例如，为现有发射器设置粒子生命周期 alpha 曲线可能如下所示：
```lua
local emitter = editor.get("/fire.particlefx", "emitters")[1]
editor.transact({
    editor.tx.set(emitter, "particle_key_alpha", { points = {
        {x = 0,   y = 0, tx = 0.1, ty = 1}, -- 从 0 开始，快速上升
        {x = 0.2, y = 1, tx = 1,   ty = 0}, -- 在生命周期的 20% 处达到 1
        {x = 1,   y = 0, tx = 1,   ty = 0}  -- 缓慢下降到 0
    }})
})
```
当然，也可以在创建发射器时在表中使用 `particle_key_alpha` 键。此外，您可以使用单个数字来表示"静态"曲线。

#### 编辑碰撞对象

除了默认的大纲属性外，碰撞对象还定义了 `shapes` 节点列表属性。添加新的碰撞形状的方法如下：
```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- 或 "shape-type-sphere", "shape-type-capsule"
    })
})
```
形状的 `type` 属性在创建期间是必需的，并且在添加形状后不能更改。有 3 种形状类型：
- `shape-type-box` - 具有 `dimensions` 属性的盒形
- `shape-type-sphere` - 具有 `diameter` 属性的球形
- `shape-type-capsule` - 具有 `diameter` 和 `height` 属性的胶囊形

#### 编辑 GUI 文件

除了大纲属性外，GUI 节点还定义了以下属性：
- `layers` — 图层编辑器节点列表（可重新排序）
- `materials` — 材质编辑器节点列表

可以使用编辑器的 `layers` 属性编辑 GUI 图层，例如：
```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```
此外，可以重新排序图层：
```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```
类似地，使用 `fonts`、`materials`、`textures` 和 `particlefxs` 属性编辑字体、材质、纹理和粒子效果：
```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.material"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```
这些属性不支持重新排序。

最后，您可以使用 `nodes` 列表属性编辑 GUI 节点，例如：
```lua
editor.transact({
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-box",
        position = {20, 20, 20}
    }),
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-template",
        template = "/button.gui"
    }),
})
```
内置节点类型有：
- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

如果您使用spine扩展，还可以使用`gui-node-type-spine`节点类型。

如果GUI文件定义了布局，您可以使用`layout:property`语法从布局中获取和设置值，例如：
```lua
local node = editor.get("/main.gui", "nodes")[1]

-- GET:
local position = editor.get(node, "position")
pprint(position) -- {20, 20, 20}
local landscape_position = editor.get(node, "Landscape:position")
pprint(landscape_position) -- {20, 20, 20}

-- SET:
editor.transact({
    editor.tx.set(node, "Landscape:position", {30, 30, 30})
})
pprint(editor.get(node, "Landscape:position")) -- {30, 30, 30}
```

可以使用`editor.tx.reset`重置已设置的布局属性为默认值：
```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```

模板节点树可以被读取，但不能编辑 — 您只能设置模板节点树的节点属性：
```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (覆盖模板中的值)
```

#### 编辑游戏对象

可以使用编辑器脚本编辑游戏对象文件的组件。组件有两种类型：引用型和嵌入型。引用型组件使用`component-reference`类型，作为对其他资源的引用，只允许覆盖脚本中定义的go属性。嵌入型组件使用`sprite`、`label`等类型，允许编辑组件类型中定义的所有属性，以及添加子组件（如碰撞对象的形状）。例如，您可以使用以下代码设置游戏对象：
```lua
editor.transact({
    editor.tx.add("/npc.go", "components", {
        type = "sprite",
        id = "view"
    }),
    editor.tx.add("/npc.go", "components", {
        type = "collisionobject",
        id = "collision",
        shapes = {
            {
                type = "shape-type-box",
                dimensions = {32, 32, 32}
            }
        }
    }),
    editor.tx.add("/npc.go", "components", {
        type = "component-reference",
        path = "/npc.script",
        id = "controller",
        __hp = 100 -- 设置脚本中定义的go属性
    })
})
```

#### 编辑集合

可以使用编辑器脚本编辑集合。您可以添加游戏对象（嵌入型或引用型）和集合（引用型）。例如：
```lua
local coll = "/char.collection"
editor.transact({
    editor.tx.add(coll, "children", {
        -- 嵌入式游戏对象
        type = "go",
        id = "root",
        children = {
            {
                -- 引用型游戏对象
                type = "go-reference",
                path = "/char-view.go",
                id = "view"
            },
            {
                -- 引用型集合
                type = "collection-reference",
                path = "/body-attachments.collection",
                id = "attachments"
            }
        },
        -- 嵌入式游戏对象也可以有组件
        components = {
            {
                type = "collisionobject",
                id = "collision",
                shapes = {
                    {type = "shape-type-box", dimensions = {2.5, 2.5, 2.5}}
                }
            },
            {
                type = "component-reference",
                id = "controller",
                path = "/char.script",
                __hp = 100 -- 设置脚本中定义的go属性
            }
        }
    })
})
```

与编辑器中一样，引用型集合只能添加到被编辑集合的根目录，而游戏对象只能添加到嵌入式或引用型游戏对象，但不能添加到引用型集合或这些引用型集合中的游戏对象。

### 使用 shell 命令

在`run`处理程序中，您可以写入文件（使用`io`模块）并执行shell命令（使用`editor.execute()`命令）。执行shell命令时，可以将shell命令的输出捕获为字符串，然后在代码中使用它。例如，如果您想创建一个格式化JSON的命令，该命令使用全局安装的[`jq`](https://jqlang.github.io/jq/)，您可以编写以下命令：
```lua
{
  label = "Format JSON",
  locations = {"Assets"},
  query = {selection = {type = "resource", cardinality = "one"}},
  action = function(opts)
    local path = editor.get(opts.selection, "path")
    return path:match(".json$") ~= nil
  end,
  run = function(opts)
    local text = editor.get(opts.selection, "text")
    local new_text = editor.execute("jq", "-n", "--argjson", "data", text, "$data", {
      reload_resources = false, -- 不要重新加载资源，因为jq不接触磁盘
      out = "capture" -- 返回文本输出而不是无输出
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```
由于此命令以只读方式调用shell程序（并使用`reload_resources = false`通知编辑器），您可以使此操作可撤销。

::: sidenote
如果您想将编辑器脚本作为库分发，您可能希望将编辑器平台的二进制程序捆绑在依赖项中。有关如何执行此操作的更多详细信息，请参阅[库中的编辑器脚本](#editor-scripts-in-libraries)。
:::

## 生命周期钩子

有一个特殊的编辑器脚本文件: `hooks.editor_script`, 位于项目根目录, 就是跟 *game.project* 并存于同一目录. 只有这个编辑器脚本会从编辑器获得生命周期事件. 脚本文件举例:
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
我们决定将生命周期事件只发给这个文件, 这里构建事件顺序比加入构建步骤容易度更重要. 命令互相独立, 所以它们在菜单里的次序并不重要, 用户回选择需要的命令来执行. 编译事件也可以发给多个脚本, 但这会产生一个问题: 事件顺序是什么样的? 你可能希望压缩资源后检查校验和... 用单一文件通过每步的函数配置好构建步骤不失为一种解决方案.

现有的生命周期钩子 `/hooks.editor_script` 可以指定:
- `on_build_started(opts)` — 游戏开始构建到本地或某远程设备上时执行. 你的更改, 不论是返回行为还是更新文件内容, 都会反应在构建好的游戏中. 在这里抛出错误的话会导致构建终止. `opts` 是包含如下 key 的表:
  - `platform` — `%arch%-%os%` 格式的字符串, 描述了构建的目标平台, 目前其值与 `editor.platform` 中的值相同.
- `on_build_finished(opts)` — 构建完成时执行, 无论构建成功与否. `opts` 是包含如下 key 的表:
  - `platform` — 与 `on_build_started` 中的值相同
  - `success` — 构建是否成功, 其值为 `true` 或 `false`
- `on_bundle_started(opts)` — 当游戏打包或生成 HTML5 游戏版本时执行. 像 `on_build_started` 一样, 这里做出的更改会反应在打包好的游戏中, 抛出错误的话会导致打包终止. `opts` 包含如下 key:
  - `output_directory` — 指定打包输出的文件路径, 比如 `"/path/to/project/build/default/__htmlLaunchDir"`
  - `platform` — 打包的目标平台. 支持的平台值详见 [Bob 教程](/manuals/bob).
  - `variant` — 打包变体, 可以是 `"debug"`, `"release"` 或 `"headless"`
- `on_bundle_finished(opts)` — 打包完成时执行, 无论打包成功与否. `opts` 与 `on_bundle_started` 里的 `opts` 相同, 加上 `success` 键代表打包是否成功.
- `on_target_launched(opts)` — 游戏成功启动时执行. `opts` 包含一个 `url` 键指定已启动引擎的服务地址, 例如, `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — 已启动的游戏关闭时执行, 参数与 `on_target_launched` 相同.

注意目前生命周期处理脚本只是编辑器特性, 使用 Bob 以命令行编译打包时该脚本不会被执行.

## 语言服务器

编辑器支持 [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) 的子集。虽然我们旨在未来扩展编辑器对 LSP 功能的支持，但目前它只能在编辑的文件中显示诊断（即 lints）并提供补全。

要定义语言服务器，您需要像这样编辑编辑器脚本的 `get_language_servers` 函数：

```lua
function M.get_language_servers()
  local command = 'build/plugins/my-ext/plugins/bin/' .. editor.platform .. '/lua-lsp'
  if editor.platform == 'x86_64-win32' then
    command = command .. '.exe'
  end
  return {
    {
      languages = {'lua'},
      watched_files = {
        { pattern = '**/.luacheckrc' }
      },
      command = {command, '--stdio'}
    }
  }
end
```
编辑器将使用指定的 `command` 启动语言服务器，使用服务器进程的标准输入和输出进行通信。

语言服务器定义表可以指定：
- `languages`（必需）— 服务器感兴趣的语言列表，如[此处](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers)所定义（文件扩展名也可以工作）；
- `command`（必需）- 命令及其参数的数组
- `watched_files` - 带有 `pattern` 键（glob）的表数组，将触发服务器的[监视文件更改](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles)通知。

## HTTP 服务器

每个运行的编辑器实例都有一个正在运行的 HTTP 服务器。可以使用编辑器脚本扩展该服务器。要扩展编辑器 HTTP 服务器，您需要添加 `get_http_server_routes` 编辑器脚本函数 — 它应该返回额外的路由：
```lua
print("My route: " .. http.server.url .. "/my-extension")

function M.get_http_server_routes()
  return {
    http.server.route("/my-extension", "GET", function(request)
      return http.server.response(200, "Hello world!")
    end)
  }
end
```
重新加载编辑器脚本后，您将在控制台中看到以下输出：`My route: http://0.0.0.0:12345/my-extension`。如果在浏览器中打开此链接，您将看到您的 `"Hello world!"` 消息。

输入的 `request` 参数是一个包含请求信息的简单 Lua 表。它包含诸如 `path`（以 `/` 开头的 URL 路径段）、请求 `method`（例如 `"GET"`）、`headers`（带有小写标题名称的表）以及可选的 `query`（查询字符串）和 `body`（如果路由定义了如何解释正文）等键。例如，如果您想创建一个接受 JSON 正文的路由，可以使用 `"json"` 转换器参数定义它：
```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```
您可以使用 `curl` 和 `jq` 在命令行中测试此端点：
```sh
curl 'http://0.0.0.0:12345/my-extension/echo-request?q=1' -X POST --data '{"input": "json"}' | jq
{
  "path": "/my-extension/echo-request",
  "method": "POST",
  "query": "q=1",
  "headers": {
    "host": "0.0.0.0:12345",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "user-agent": "curl/8.7.1",
    "content-length": "17"
  },
  "body": {
    "input": "json"
  }
}
```
路由路径支持可以从请求路径中提取并作为请求的一部分提供给处理函数的模式，例如：
```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```
现在，如果您打开例如 `http://0.0.0.0:12345/my-extension/setting/project.title`，您将看到从 `/game.project` 文件中获取的游戏标题。

除了单段路径模式外，您还可以使用 `{*name}` 语法匹配 URL 路径的其余部分。例如，这是一个简单的文件服务器端点，它从项目根目录提供文件：
```lua
http.server.route("/my-extension/files/{*file}", function(request)
  local attrs = editor.external_file_attributes(request.file)
  if attrs.is_file then
    return http.server.external_file_response(request.file)
  else
    return 404
  end
end)
```
现在，在浏览器中打开例如 `http://0.0.0.0:12345/my-extension/files/main/main.collection` 将显示 `main/main.collection` 文件的内容。

## 库中的编辑器脚本

您可以发布包含命令的库供他人使用，编辑器会自动获取这些命令。另一方面，钩子不能自动获取，因为它们必须定义在项目根目录的文件中，而库只公开子文件夹。这是为了在构建过程中提供更多控制：您仍然可以在 `.lua` 文件中创建生命周期钩子作为简单函数，以便库的用户可以在他们的 `/hooks.editor_script` 中 require 并使用它们。

还要注意，尽管依赖项显示在资源视图中，但它们并不作为文件存在（它们是 zip 存档中的条目）。可以使编辑器从依赖项中提取一些文件到 `build/plugins/` 文件夹中。为此，您需要在库文件夹中创建 `ext.manifest` 文件，然后在 `ext.manifest` 文件所在的同一文件夹中创建 `plugins/bin/${platform}` 文件夹。该文件夹中的文件将自动提取到 `/build/plugins/${extension-path}/plugins/bin/${platform}` 文件夹，因此您的编辑器脚本可以引用它们。

## 首选项

编辑器脚本可以定义和使用首选项 — 存储在用户计算机上的持久化、未提交的数据。这些首选项具有三个关键特性：
- 类型化：每个首选项都有一个模式定义，包括数据类型和其他元数据，如默认值
- 作用域：首选项的作用域可以是每个项目或每个用户
- 嵌套：每个首选项键是一个点分隔的字符串，其中第一个路径段标识一个编辑器脚本，其余部分

所有首选项必须通过定义其模式来注册：
```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```
重新加载此类编辑器脚本后，编辑器将注册此模式。然后编辑器脚本可以获取和设置首选项，例如：
```lua
-- 获取特定首选项
editor.prefs.get("my_json_formatter.indent.type")
-- 返回: "spaces"

-- 获取整个首选项组
editor.prefs.get("my_json_formatter")
-- 返回:
-- {
--   jq_path = "",
--   indent = {
--     size = 2,
--     type = "spaces"
--   }
-- }

-- 一次设置多个嵌套首选项
editor.prefs.set("my_json_formatter.indent", {
    type = "tabs",
    size = 1
})
```

## 执行模式

编辑器脚本运行时使用两种执行模式，这些模式对编辑器脚本基本上是透明的：**即时**和**长时间运行**。 

**即时**模式用于编辑器需要尽快从脚本接收响应的情况。例如，菜单命令的 `active` 回调在即时模式下执行，因为这些检查是在编辑器 UI 线程上响应与编辑器的用户交互而执行的，并且应该在同一帧内更新 UI。 

**长时间运行**模式用于编辑器不需要脚本即时响应的情况。例如，菜单命令的 `run` 回调在**长时间运行**模式下执行，允许脚本有更多时间来完成其工作。

编辑器脚本可以使用的一些函数可能需要很长时间才能运行。例如，`editor.execute("git", "status", {reload_resources=false, out="capture"})` 在足够大的项目上可能需要长达一秒钟的时间。为了保持编辑器的响应性和性能，在编辑器需要即时响应的情况下，不允许使用可能耗时的函数。尝试在即时上下文中使用此类函数将导致错误：`Cannot use long-running editor function in immediate context`。要解决此错误，请避免在即时上下文中使用此类函数。

以下函数被认为是长时间运行的，不能在即时模式下使用：
- `editor.create_directory()`、`editor.create_resources()`、`editor.delete_directory()`、`editor.save()`、`os.remove()` 和 `file:write()`：这些函数修改磁盘上的文件，导致编辑器将其内存中的资源树与磁盘状态同步，这在大型项目中可能需要几秒钟。
- `editor.execute()`：执行 shell 命令可能需要不可预测的时间。
- `editor.transact()`：对广泛引用的节点的大型事务可能需要数百毫秒，这对于 UI 响应性来说太慢了。

以下代码执行上下文使用即时模式：
- 菜单命令的 `active` 回调：编辑器需要在同一 UI 帧内从脚本接收响应。
- 编辑器脚本的顶层：我们不期望重新加载编辑器脚本的行为有任何副作用。

## 操作

::: sidenote
以前，编辑器以阻塞方式与 Lua VM 交互，因此编辑器脚本有一个硬性要求，即不能阻塞，因为某些交互必须从编辑器 UI 线程完成。因此，例如没有 `editor.execute()` 和 `editor.transact()`。执行脚本和更改编辑器状态是通过从钩子和命令 `run` 处理程序返回一个 "actions" 数组来触发的。

现在编辑器以非阻塞方式与 Lua VM 交互，因此不再需要这些操作：使用像 `editor.execute()` 这样的函数更方便、简洁和强大。这些操作现在已**弃用**，尽管我们没有计划删除它们。
:::

编辑器可以从命令的 `run` 函数或 `/hooks.editor_script` 的钩子函数返回一个操作数组。然后这些操作将由编辑器执行。

操作是描述编辑器应该做什么的表。每个操作都有一个 `action` 键。操作有两种类型：可撤销和不可撤销。

### 可撤销操作

::: sidenote
优先使用 `editor.transact()`。
:::

可撤销操作在执行后可以撤销。如果一个命令返回多个可撤销操作，它们将一起执行，并一起撤销。如果可以，您应该使用可撤销操作。它们的缺点是它们更受限制。

现有的可撤销操作：
- `"set"` — 将编辑器中节点的属性设置为某个值。例如：
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  `"set"` 操作需要以下键：
  - `node_id` — 节点 id userdata。或者，您可以在这里使用资源路径代替从编辑器接收的节点 id，例如 `"/main/game.script"`；
  - `property` — 要设置的节点属性，例如 `"text"`；
  - `value` — 属性的新值。对于 `"text"` 属性，它应该是一个字符串。

### 不可撤销操作

::: sidenote
优先使用 `editor.execute()`。
:::

不可撤销操作会清除撤销历史记录，因此如果您想撤销此类操作，您将不得不使用其他方法，例如版本控制。

现有的不可撤销操作：
- `"shell"` — 执行 shell 脚本。例如：
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- trim leading "/"
    }
  }
  ```
  `"shell"` 操作需要 `command` 键，它是命令及其参数的数组。

### 操作混用及其副作用

您可以混合使用可撤销和不可撤销操作。操作是按顺序执行的，因此根据操作的顺序，您将失去撤销该命令部分操作的能力。

除了从期望它们的函数返回操作外，您可以直接使用 `io.open()` 读写文件。这将触发资源重载，从而清除撤销历史记录。
