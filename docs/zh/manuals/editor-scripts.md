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

如果编辑器脚本模块定义了 `get_commands` 函数，它将在扩展重新加载时被调用，返回的命令将在编辑器菜单栏或资源和大纲视图的上下文菜单中可用。例如：
```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
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
      label = "Minify JSON",
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
编辑器期望 `get_commands()` 返回一个表数组，每个表描述一个单独的命令。命令描述包含：

- `label`（必需）— 将显示给用户的菜单项上的文本
- `locations`（必需）— 包含 `"Edit"`、`"View"`、`"Project"`、`"Debug"`、`"Assets"`、`"Bundle"`、`"Scene"` 或 `"Outline"` 的数组，描述此命令应该可用的位置。`"Edit"`、`"View"`、`"Project"` 和 `"Debug"` 表示顶部的菜单栏，`"Assets"` 表示资源视图中的上下文菜单，`"Outline"` 表示大纲视图中的上下文菜单，`"Bundle"` 表示 **Project → Bundle** 子菜单。
- `query` — 命令向编辑器询问相关信息并定义其操作数据的方式。对于 `query` 表中的每个键，`active` 和 `run` 回调接收的 `opts` 表中将有相应的键。支持的键：
  - `selection` 表示当有选中内容时此命令有效，并且它对该选择进行操作。
    - `type` 是命令感兴趣的选中节点类型，目前允许这些类型：
      - `"resource"` — 在资源和大纲视图中，资源是具有相应文件的选中项。在菜单栏（Edit 或 View）中，资源是当前打开的文件；
      - `"outline"` — 可以在大纲视图中显示的内容。在大纲视图中是选中项，在菜单栏中是当前打开的文件；
      - `"scene"` — 可以渲染到场景中的内容。
    - `cardinality` 定义应该有多少个选中项。如果是 `"one"`，传递给命令回调的选择将是单个节点 id。如果是 `"many"`，传递给命令回调的选择将是一个或多个节点 id 的数组。
  - `argument` — 命令参数。目前，只有 `"Bundle"` 位置中的命令接收参数，当明确选择打包命令时为 `true`，在重新打包时为 `false`。
- `id` - 命令标识符字符串，例如用于在 `prefs` 中持久化最后使用的打包命令
- `active` - 一个回调函数，用于检查命令是否处于活动状态，预期返回布尔值。如果 `locations` 包括 `"Assets"`、`"Scene"` 或 `"Outline"`，在显示上下文菜单时将调用 `active`。如果位置包括 `"Edit"` 或 `"View"`，将在每次用户交互（例如键盘输入或鼠标点击）时调用 active，因此请确保 `active` 相对较快。
- `run` - 当用户选择菜单项时执行的回调。

## 事务

事务是修改编辑器状态的方法。它们是原子的，这意味着它们要么全部成功，要么全部失败。事务由一个或多个步骤组成，每个步骤都是对编辑器状态的单个修改。您可以使用 `editor.tx.*` 函数创建事务步骤。以下是可用的事务步骤：

- `editor.tx.set(node_id, property, value)` — 设置节点的属性值。
- `editor.tx.create(resource_path, template_path, [data])` — 创建新资源。如果指定了 `template_path`，则从模板创建资源。`data` 是一个可选表，包含要传递给模板的数据。
- `editor.tx.delete(resource_path)` — 删除资源。
- `editor.tx.rename(resource_path, new_name)` — 重命名资源。
- `editor.tx.move(resource_path, new_path)` — 移动资源。
- `editor.tx.copy(resource_path, new_path)` — 复制资源。
- `editor.tx.duplicate(resource_path, [new_name])` — 复制资源。如果指定了 `new_name`，则使用该名称作为新资源的名称。
- `editor.tx.set_resource_property(resource_path, property, value)` — 设置资源的属性值。
- `editor.tx.set_resource_properties(resource_path, properties)` — 设置资源的多个属性值。
- `editor.tx.set_game_object_property(game_object_id, property, value)` — 设置游戏对象的属性值。
- `editor.tx.set_game_object_properties(game_object_id, properties)` — 设置游戏对象的多个属性值。
- `editor.tx.set_component_property(component_id, property, value)` — 设置组件的属性值。
- `editor.tx.set_component_properties(component_id, properties)` — 设置组件的多个属性值。
- `editor.tx.set_input_binding_property(input_binding_id, property, value)` — 设置输入绑定的属性值。
- `editor.tx.set_input_binding_properties(input_binding_id, properties)` — 设置输入绑定的多个属性值。
- `editor.tx.set_input_binding_game_object_property(input_binding_id, game_object_id, property, value)` — 设置输入绑定游戏对象的属性值。
- `editor.tx.set_input_binding_game_object_properties(input_binding_id, game_object_id, properties)` — 设置输入绑定游戏对象的多个属性值。
- `editor.tx.set_input_binding_component_property(input_binding_id, component_id, property, value)` — 设置输入绑定组件的属性值。
- `editor.tx.set_input_binding_component_properties(input_binding_id, component_id, properties)` — 设置输入绑定组件的多个属性值。
- `editor.tx.set_input_binding_input_property(input_binding_id, input_id, property, value)` — 设置输入绑定输入的属性值。
- `editor.tx.set_input_binding_input_properties(input_binding_id, input_id, properties)` — 设置输入绑定输入的多个属性值。
- `editor.tx.set_input_binding_input_game_object_property(input_binding_id, input_id, game_object_id, property, value)` — 设置输入绑定输入游戏对象的属性值。
- `editor.tx.set_input_binding_input_game_object_properties(input_binding_id, input_id, game_object_id, properties)` — 设置输入绑定输入游戏对象的多个属性值。
- `editor.tx.set_input_binding_input_component_property(input_binding_id, input_id, component_id, property, value)` — 设置输入绑定输入组件的属性值。
- `editor.tx.set_input_binding_input_component_properties(input_binding_id, input_id, component_id, properties)` — 设置输入绑定输入组件的多个属性值。
- `editor.tx.set_tilemap_layer_property(tilemap_id, layer_id, property, value)` — 设置瓦片地图图层的属性值。
- `editor.tx.set_tilemap_layer_properties(tilemap_id, layer_id, properties)` — 设置瓦片地图图层的多个属性值。
- `editor.tx.set_tilemap_tile_property(tilemap_id, layer_id, x, y, property, value)` — 设置瓦片地图瓦片的属性值。
- `editor.tx.set_tilemap_tile_properties(tilemap_id, layer_id, x, y, properties)` — 设置瓦片地图瓦片的多个属性值。
- `editor.tx.set_particlefx_emitter_property(particlefx_id, emitter_id, property, value)` — 设置粒子效果发射器的属性值。
- `editor.tx.set_particlefx_emitter_properties(particlefx_id, emitter_id, properties)` — 设置粒子效果发射器的多个属性值。
- `editor.tx.set_particlefx_modifier_property(particlefx_id, emitter_id, modifier_id, property, value)` — 设置粒子效果修改器的属性值。
- `editor.tx.set_particlefx_modifier_properties(particlefx_id, emitter_id, modifier_id, properties)` — 设置粒子效果修改器的多个属性值。
- `editor.tx.set_collisionobject_shape_property(collisionobject_id, shape_id, property, value)` — 设置碰撞对象形状的属性值。
- `editor.tx.set_collisionobject_shape_properties(collisionobject_id, shape_id, properties)` — 设置碰撞对象形状的多个属性值。
- `editor.tx.set_gui_layer_property(gui_id, layer_id, property, value)` — 设置 GUI 图层的属性值。
- `editor.tx.set_gui_layer_properties(gui_id, layer_id, properties)` — 设置 GUI 图层的多个属性值。
- `editor.tx.set_gui_node_property(gui_id, node_id, property, value)` — 设置 GUI 节点的属性值。
- `editor.tx.set_gui_node_properties(gui_id, node_id, properties)` — 设置 GUI 节点的多个属性值。

> **注意：** 事务系统已弃用，请使用编辑器 API 函数代替。

要执行事务，请使用 `editor.transact(txs)` 函数，其中 `txs` 是事务步骤的列表。例如：
```lua
local txs = {}
txs[#txs + 1] = editor.tx.set(node_id, "position", vmath.vector3(100, 100, 0))
txs[#txs + 1] = editor.tx.set(node_id, "rotation", vmath.quat_rotation_z(math.rad(45)))
editor.transact(txs)
```

## 生命周期钩子

您可以通过在 `hooks.editor_script` 文件中定义函数来响应编辑器中的各种事件：

```lua
function on_build_started()
  print("Build started")
end

function on_build_completed()
  print("Build completed")
end

function on_build_failed()
  print("Build failed")
end

function on_editor_started()
  print("Editor started")
end

function on_editor_exiting()
  print("Editor exiting")
end

function on_editor_shutdown()
  print("Editor shutdown")
end
```

可用的事件：
- `on_build_started()` — 当构建开始时调用。
- `on_build_completed()` — 当构建完成时调用。
- `on_build_failed()` — 当构建失败时调用。
- `on_editor_started()` — 当编辑器启动时调用。
- `on_editor_exiting()` — 当编辑器即将退出时调用。
- `on_editor_shutdown()` — 当编辑器关闭时调用。

## 执行模式

编辑器脚本支持两种执行模式：

### 即时模式

在即时模式下，脚本会立即执行，并阻塞编辑器直到完成。这是默认模式。

### 长时间运行模式

在长时间运行模式下，脚本会在后台执行，不会阻塞编辑器。要启用长时间运行模式，请在脚本开头添加以下代码：

```lua
editor.set_async(true)
```

长时间运行模式有以下限制：
- 不能使用 `editor.transact()` 函数。
- 不能使用 `editor.get()` 函数。
- 不能使用 `editor.set()` 函数。
- 不能使用 `editor.create()` 函数。
- 不能使用 `editor.delete()` 函数。
- 不能使用 `editor.reorder()` 函数。
- 不能使用 `editor.add()` 函数。
- 不能使用 `editor.remove()` 函数。
- 不能使用 `editor.clear()` 函数。
- 不能使用 `editor.execute()` 函数。
- 不能使用 `editor.prefs()` 函数。
- 不能使用 `editor.message()` 函数。
- 不能使用 `editor.confirm()` 函数。
- 不能使用 `editor.input()` 函数。
- 不能使用 `editor.select()` 函数。
- 不能使用 `editor.open()` 函数。
- 不能使用 `editor.save()` 函数。
- 不能使用 `editor.close()` 函数。
- 不能使用 `editor.reload()` 函数。
- 不能使用 `editor.exit()` 函数。

## 首选项

您可以使用 `editor.prefs()` 函数来访问和修改编辑器首选项：

```lua
-- 获取首选项
local value = editor.prefs("key")

-- 设置首选项
editor.prefs("key", value)
```

首选项是持久化的，即使编辑器关闭后也会保留。

如果编辑器脚本模块定义了 `get_commands` 函数, 它会在扩展重载时被调用, 返回的命令可以在编辑器菜单栏或者资源和大纲视图的右键菜单里使用. 例如:
```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
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
        return {
          {
            action = "set",
            node_id = opts.selection,
            property = "text",
            value = strip_comments(text)
          }
        }
      end
    },
    {
      label = "Minify JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        return {
          {
            action = "shell",
            command = {"./scripts/minify-json.sh", path:sub(2)}
          }
        }
      end
    }
  }
end

return M
```
编辑器需要 `get_commands()` 返回一组 table, 每个 table 描述一个命令. 命令描述由以下部分组成:

- `label` (必要) — 显示在菜单栏项上的文字
- `locations` (必要) — 包含 `"Edit"`, `"View"`, `"Assets"` 或者 `"Outline"` 的数组, 描述该命令在哪里生效. `"Edit"` 和 `"View"` 表示菜单栏最高层, `"Assets"` 表示在资源视图右键菜单里, "Outline"` 表示在大纲视图右键菜单里.
- `query` — 命令向编辑器查询信息并定义被操作数据的地方. 在 `query` 表里的每个键都会一一对应包裹在 `opts` 表里, 作为参数传给 `active` 和 `run` 回调函数. 支持的 key 有:
  - `selection` 意思是在选择了什么时可用, 操作将作用于被选择的东西上.
    - `type` 命令能作用于选择节点的类型, 目前支持以下几种:
      - `"resource"` — 大纲视图或者资源视图里, 被选择资源对应的文件. 在菜单栏 (Edit 或 View), 资源是当前打开了的文件;
      - `"outline"` — 在大纲视图显示的东西. 在大纲视图被选择的项, 在菜单栏是当前打开了的文件;
    - `cardinality` 定义备选项的个数. 如果是 `"one"`, 将传给命令回调一个节点 id. 如果是 `"many"`, 将传给命令回调一个数组, 包含一个或多个节点 id.
- `active` - 检测命令是否可用的回调, 返回布尔值. 如果 `locations` 包含 `"Assets"` 或 `"Outline"`, `active` 会在显示右键菜单时被调用. 如果包含 `"Edit"` 或 `"View"`, 它会在每个用户交互时被调用, 比如按键盘或者点鼠标的时候, 所以 `active` 应该快速执行完毕.
- `run` - 用户点选菜单项时运行的回调, 返回包含 [actions](#actions) 的数组.

## Action

行为是描述编辑器要做什么的表. 每个行为包含一个 `action` 键. 行为有两种: 可撤销行为和不可撤销行为.

### 可撤销行为

可撤销行为在执行后可以撤销. 如果一个命令返回了多个可撤销行为, 它们会一起执行, 撤销时也一起被撤销. 应尽量使用可撤销行为. 只是可撤销行为有更多一些限制.

目前的可撤销行为有:
- `"set"` — 设置编辑器里一个节点的属性为指定值. 例如:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  `"set"` 行为有如下键:
  - `node_id` — 表示节点 id 的 userdata. 或者, 可以用资源路径代替编辑器发来的节点 id, 例如 `"/main/game.script"`;
  - `property` — 要设置的节点属性, 目前只支持 `"text"`;
  - `value` — 给节点属性设置的新值. 对于 `"text"` 属性来说该值应该是一个字符串.

### 不可撤销行为

不可撤销行为会清空可撤销历史, 所以要撤销这种行为, 必须使用其他特殊方法, 比如版本控制系统.

目前可用的不可撤销行为:
- `"shell"` — 执行一个 shell 脚本. 例如:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- trim leading "/"
    }
  }
  ```
  `"shell"` 行为要有一个 `command` 键, 它是一组命令连同其参数. 它与 `os.execute` 主要区别在于, 鉴于它是一种潜在危险操作, 编辑器会弹出一个对话框询问用户是否确认进行此操作. 用户允许的每个命令授权都会被记住.

### 行为混用及其副作用

可以混用可撤销行为和不可撤销行为. 行为是依次执行的, 根据执行顺序撤销操作会停在不可撤销行为上.

除了从函数返回行为, 还可以直接用 `io.open()` 读写文件. 这会触发资源重载并且清空撤销历史记录.

## Lifecycle hooks

有一个特殊的编辑器脚本文件: `hooks.editor_script`, 位于项目根目录, 就是跟 *game.project* 并存于同一目录. 只有这个编辑器脚本会从编辑器获得生命周期事件. 脚本文件举例:
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write("{\"build_time\": \"".. os.date() .."\"}")
  file:close()
end

return M
```
我们决定将生命周期事件只发给这个文件, 这里构建事件顺序比加入构建步骤容易度更重要. 命令互相独立, 所以它们在菜单里的次序并不重要, 用户回选择需要的命令来执行. 编译事件也可以发给多个脚本, 但这会产生一个问题: 事件顺序是什么样的? 你可能希望压缩资源后检查校验和... 用单一文件通过每步的函数配置好构建步骤不失为一种解决方案.

生命周期函数可以返回行为或者在项目文件夹的文件里写入数据.

目前的生命周期脚本 `/hooks.editor_script` 可以指定:
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

## Editor scripts in libraries

可以为他人发布包含命令的库, 编辑器会自动配置它们. 事件处理脚本除外, 因为它要放在项目根目录, 而库则是解压在子目录里. 这是为了在构建处理时提供更多控制权: 可以在 `.lua` 文件里提供简单的事件处理函数, 库用户则可以在他们的 `/hooks.editor_script` 文件里引入并使用它们.

还要注意虽然依赖库显示在资源视窗里, 它们却不是文件 (而是 zip 包), 所以目前没办法从依赖库里执行 shell 脚本. 如果实在要执行, 需要先用 `editor.get()` 读取脚本, 然后用 `file:write()` 写入脚本文件, 比如写到 `build/editor-scripts/your-extension-name` 目录下.

更简单的办法是使用原生扩展插件系统.
首先在库目录创建 `ext.manifest` 文件, 然后在 `ext.manifest` 文件所在文件夹里创建 `plugins/bin/${platform}`. 该文件夹下的文件会被自动提取到 `/build/plugins/${extension-path}/plugins/bin/${platform}` 目录下, 可以在编辑器脚本中引用它们.

## HTTP 服务器

每个运行的编辑器实例都有一个 HTTP 服务器在运行。服务器可以通过编辑器脚本进行扩展。要扩展编辑器 HTTP 服务器，您需要添加 `get_http_server_routes` 编辑器脚本函数 — 它应该返回额外的路由：
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
重新加载编辑器脚本后，您将在控制台中看到以下输出：`My route: http://0.0.0.0:12345/my-extension`。如果您在浏览器中打开此链接，您将看到您的 `"Hello world!"` 消息。

输入的 `request` 参数是一个包含请求信息的简单 Lua 表。它包含诸如 `path`（以 `/` 开头的 URL 路径段）、请求 `method`（例如 `"GET"`）、`headers`（带有小写标题名称的表）以及可选的 `query`（查询字符串）和 `body`（如果路由定义了如何解释正文）等键。例如，如果您想创建一个接受 JSON 正文的路由，您可以使用 `"json"` 转换器参数定义它：
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

## Language servers

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

## Actions

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

### 混合操作和副作用

您可以混合可撤销和不可撤销操作。操作是按顺序执行的，因此根据操作的顺序，您将最终失去撤销该命令部分的能力。

除了从期望它们的函数返回操作外，您可以直接使用 `io.open()` 读写文件。这将触发资源重新加载，从而清除撤销历史记录。
