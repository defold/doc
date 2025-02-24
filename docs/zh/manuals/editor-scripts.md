---
title: 编辑器脚本
brief: 本教程介绍了如何使用 Lua 扩展编辑器功能
---

# 编辑器脚本

只需使用: `.editor_script` 扩展名的 Lua 脚本就可以创建自定义菜单项和编辑器生命周期回调. 使用这种方法, 你可以调整编辑器创建适合自己的开发流.

## 编辑器脚本运行环境

编辑器脚本运行于编辑器中, 在一个Java虚拟机下的Lua虚拟机下运行. 所有脚本共享一个环境, 也就是说它们能彼此访问. 你可以导入Lua模块, 就像 `.script` 文件一样, 但是编辑器内lua运行版本不同, 所以要注意代码兼容性. 编辑器使用 Lua 版本 5.2.x, 具体来说就是 [luaj](https://github.com/luaj/luaj) 运行时, 目前只有这个运行时能运行在Java虚拟机下. 除了这些, 还有一些限制:
- 没有 `debug` 和 `coroutine` 包;
- 没有 `os.execute` — 我们在 [actions](#actions) 部分提供了更有效安全的方法;
- 没有 `os.tmpname` 和 `io.tmpfile` — 目前编辑器可存取文件仅限于项目文件夹内的文件;
- 目前没有 `os.rename`, 以后可能加入;
- 没有 `os.exit` 和 `os.setlocale`.

用编辑器脚本定义的编辑器扩展会在打开项目时加载. 获取依赖库时, 扩展会重新加载, 因为依赖库里有可能有扩展脚本存在. 重新加载时, 不会改变当前扩展脚本, 因为此时也许你正在编辑它们. 要完全重新加载, 可以使用 Project → Reload 编辑器命令.

## `.editor_script` 构成

每个编辑器脚本需要返回一个模块, 如下:
```lua
local M = {}

function M.get_commands()
  -- TODO - 定义编辑器命令
end

function M.get_language_servers()
  -- TODO - 定义语言服务器
end

return M
```
然后编辑器会收集项目中和共享库里的所有的编辑器脚本, 把它们加载到Lua虚拟机中并在需要的时候调用它们 (详情请见 [commands](#commands) 和 [lifecycle hooks](#lifecycle-hooks) 部分).

## 编辑器 API

可以使用API中 `editor` 包与编辑器进行交互:
- `editor.platform` —字符串, 在Windows上是 `"x86_64-win32"`, 在macOS上是 `"x86_64-macos"`, 在Linux上是 `"x86_64-linux"`.
- `editor.get(node_id, property)` — 得到编辑器里某些节点的值. 编辑器里的节点是可变实体, 比如脚本或者集合文件, 集合中的游戏对象, 作为资源加载的 json 文件, 等等. `node_id` 是由编辑器发往编辑器脚本的一个 userdata. 或者, 可以用资源路径代替节点 id, 比如 `"/main/game.script"`. `property` 是一个字符串. 目前支持以下属性:
  - `"path"` — 基于项目文件夹对 *resources* 的相对路径 — 资源即代表文件. 有效值举例: `"/main/game.script"`
  - `"text"` — 可编辑文本资源文件 (比如脚本文件或者 json). 有效值举例: `"function init(self)\nend"`. 注意这里跟用 `io.open()` 读取文件不同, 文本资源可以只编辑不保存, 这些编辑仅在访问 `"text"` 属性时有效.
  - 在大纲试图做点选操作时, 有些属性可以在属性面板显示出来. 可以显示的属性有:
    - strings
    - booleans
    - numbers
    - vec2/vec3/vec4
    - resources

    注意这些属性有的不是只读的, 而且基于上下文有些可能不可用, 所以要在读取之前执行 `editor.can_get`, 设置之前执行 `editor.can_set`. 属性面板里用鼠标悬停在属性名上会显示一个信息提示标明该属性在编辑器脚本里是如何命名的. 资源属性赋值为 `""` 代表 nil 值.
- `editor.can_get(node_id, property)` — 检查属性是否可读, 确保 `editor.get()` 不会报错
- `editor.can_set(node_id, property)` — 检查属性是否可写, 确保设置操作不会报错
- `editor.create_directory(resource_path)` — 新建文件夹, 及其所有父文件夹
- `editor.delete_directory(resource_path)` — 删除文件夹, 及其所有子文件夹和文件.

## Command

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

## Language servers

编辑器支持 [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) 的小子集. 我们计划以后全面支持 LSP 特性, 但是目前只支持显示编辑文件的代码审查 (比如 lints).

要定义 language server, 需要设置编辑器脚本的 `get_language_servers` 函数如下:

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
编辑器会使用指定 `command` 启动 language server, 使用服务器进程的标准输入和输出进行通信.

Language server 定义表可以指定:
- `languages` (必要) — 服务器支持的语言列表, 详见 [这里](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers) (支持文件扩展名);
- `command` (必要) - 命令及其参数列表
- `watched_files` - 一组带有 `pattern` 键 (a glob) 的表, 用来激活服务器的 [监视文件更改](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) 通知功能.
