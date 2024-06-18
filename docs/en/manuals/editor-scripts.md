---
title: Editor scripts
brief: This manual explains how to extend editor using Lua
---

# Editor scripts

You can create custom menu items and editor lifecycle hooks using Lua files with special extension: `.editor_script`. Using this system, you can tweak editor to enhance your development workflow.

## Editor script runtime

Editor scripts run inside an editor, in a Lua VM emulated by Java VM. All scripts share the same single environment, which means they can interact with each other. You can require Lua modules, just as with `.script` files, but Lua version that is running inside the editor is different, so make sure your shared code is compatible. Editor uses Lua version 5.2.x, more specifically [luaj](https://github.com/luaj/luaj) runtime, which is currently the only viable solution to run Lua on JVM. Besides that, there are some restrictions:
- there is no `debug` package;
- there is no `os.execute`, though we provide a similar `editor.execute()`;
- there is no `os.tmpname` and `io.tmpfile` — currently editor scripts can access files only inside the project directory;
- there is currently no `os.rename`, although we want to add it;
- there is no `os.exit` and `os.setlocale`.

All editor extensions defined in editor scripts are loaded when you open a project. When you fetch libraries, extensions are reloaded, since there might be new editor scripts in a libraries you depend on. During this reload, no changes in your own editor scripts are picked up, since you might be in the middle of changing them. To reload them as well, you should run **Project → Reload Editor Scripts** command.

## Anatomy of `.editor_script`

Every editor script should return a module, like that:
```lua
local M = {}

function M.get_commands()
  -- TODO - define editor commands
end

function M.get_language_servers()
  -- TODO - define language servers
end

return M
```
Editor then collects all editor scripts defined in project and libraries, loads them into single Lua VM and calls into them when needed (more on that in [commands](#commands) and [lifecycle hooks](#lifecycle-hooks) sections).

## Editor API

You can interact with the editor using `editor` package that defines this API:
- `editor.platform` — a string, either `"x86_64-win32"` for Windows, `"x86_64-macos"` for macOS or `"x86_64-linux"` for Linux.
- `editor.version` — a string, version name of Defold, e.g. `"1.4.8"`
- `editor.engine_sha1` — a string, SHA1 of Defold engine
- `editor.editor_sha1` — a string, SHA1 of Defold editor
- `editor.get(node_id, property)` — get a value of some node inside the editor. Nodes in the editor are various entities, such as script or collection files, game objects inside collections, json files loaded as resources, etc. `node_id` is a userdata that is passed to the editor script by the editor. Alternatively, you can pass resource path instead of node id, for example `"/main/game.script"`. `property` is a string. Currently these properties are supported:
  - `"path"` — file path from the project folder for *resources* — entities that exist as files. Example of returned value: `"/main/game.script"`
  - `"text"` — text content of a resource editable as text (such as script files or json). Example of returned value: `"function init(self)\nend"`. Please note that this is not the same as reading file with `io.open()`, because you can edit a file without saving it, and these edits are available only when accessing `"text"` property.
  - some properties that are shown in the Properties view when you have selected something in the Outline view. These types of outline properties supported:
    - strings
    - booleans
    - numbers
    - vec2/vec3/vec4
    - resources

    Please note that some of these properties might be read-only, and some might be unavailable in different contexts, so you should use `editor.can_get` before reading them and `editor.can_set` before making editor set them. Hover over property name in Properties view to see a tooltip with information about how this property is named in editor scripts. You can set resource properties to `nil` by supplying `""` value.
- `editor.can_get(node_id, property)` — check if you can get this property so `editor.get()` won't throw an error.
- `editor.can_set(node_id, property)` — check if `editor.tx.set()` transaction step with this property won't throw an error.
- `editor.create_directory(resource_path)` — create a directory if it does not exist, and all non-existent parent directories.
- `editor.delete_directory(resource_path)` — delete a directory if it exists, and all existent child directories and files.
- `editor.execute(cmd, [...args], [options])` — run a shell command, optionally capturing its output.
- `editor.save()` — persist all unsaved changed to disk.
- `editor.transact(txs)` — modify the editor in-memory state using 1 or more transaction steps created with `editor.tx.*` functions.

## Commands

If editor script module defines function `get_commands`, it will be called on extension reload, and returned commands will be available for use inside the editor in menu bar or in context menus in Assets and Outline panes. Example:
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
      label = "Minify JSON"
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
Editor expects `get_commands()` to return an array of tables, each describing a separate command. Command description consists of:

- `label` (required) — text on a menu item that will be displayed to the user
- `locations` (required) — an array of either `"Edit"`, `"View"`, `"Assets"` or `"Outline"`, describes a place where this command should be available. `"Edit"` and `"View"` mean menu bar at the top, `"Assets"` means context menu in Assets pane, and `"Outline"` means context menu in Outline pane.
- `query` — a way for command to ask editor for relevant information and define what data it operates on. For every key in `query` table there will be corresponding key in `opts` table that `active` and `run` callbacks receive as argument. Supported keys:
  - `selection` means this command is valid when there is something selected, and it operates on this selection.
    - `type` is a type of selected nodes command is interested in, currently these types are allowed:
      - `"resource"` — in Assets and Outline, resource is selected item that has a corresponding file. In menu bar (Edit or View), resource is a currently open file;
      - `"outline"` — something that can be shown in the Outline. In Outline it's a selected item, in menu bar it's a currently open file;
    - `cardinality` defines how many selected items there should be. If `"one"`, selection passed to command callback will be a single node id. If `"many"`, selection passed to command callback will be an array of one or more node ids.
- `active` - a callback that is executed to check that command is active, expected to return boolean. If `locations` include `"Assets"` or `"Outline"`, `active` will be called when showing context menu. If locations include `"Edit"` or `"View"`, active will be called on every user interaction, such as typing on keyboard or clicking with mouse, so be sure that `active` is relatively fast.
- `run` - a callback that is executed when user selects the menu item.

### Use commands to change the in-memory editor state

Inside the `run` handler, you can query and change the in-memory editor state. Querying is done using `editor.get()` function, where you can ask the editor about the current state of files and selection (if using `query = {selection = ...}`). You can get the `"text"` property of script files, and also some properties shown in the Properties view — hover over property name to see a tooltip with information about how this property is named in editor scripts. Changing the editor state is done using `editor.transact()`, where you bundle 1 or more modifications in a single undoable step. For example, if you want to be able to reset transform of a game object, you could write a command like that:
```lua
{
  label = "Reset transform",
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

### Use shell commands

Inside the `run` handler, you can write to files (using `io` module) and execute shell commands (using `editor.execute()` command). When executing shell commands, it's possible to capture the output of a shell command as a string and then use it in code. For example, if you want to make a command for formatting JSON that shells out to globally installed [`jq`](https://jqlang.github.io/jq/), you can write the following command:
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
      reload_resources = false, -- don't reload resources since jq does not touch disk
      out = "capture" -- return text output instead of nothing
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```
Since this command invokes shell program in a read-only way (and notifies the editor about it using `reload_resources = false`), you get the benefit of making this action undoable.

::: sidenote
If you want to distribute your editor script as a library, you might want to bundle the binary program for editor platforms within the dependency. See [Editor scripts in libraries](#editor-scripts-in-libraries) for more details on how to do it.
:::

## Lifecycle hooks

There is a specially treated editor script file: `hooks.editor_script`, located in a root of your project, in the same directory as *game.project*. This and only this editor script will receive lifecycle events from the editor. Example of such file:
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
We decided to limit lifecycle hooks to single editor script file because order in which build hooks happen is more important than how easy it is to add another build step. Commands are independent from each other, so it does not really matter in what order they are shown in the menu, in the end user executes a particular command they selected. If it was possible to specify build hooks in different editor scripts, it would create a problem: in which order do hooks execute? You probably want to create a checksums of content after you compress it... And having a single file that establishes order of build steps by calling each step function explicitly is a way to solve this problem.

Existing lifecycle hooks that `/hooks.editor_script` may specify:
- `on_build_started(opts)` — executed when game is Built to run locally or on some remote target using either the Project Build or Debug Start options. Your changes will appear in the built game. Raising an error from this hook will abort a build. `opts` is a table that contains following keys:
  - `platform` — a string in `%arch%-%os%` format describing what platform it's built for, currently always the same value as in `editor.platform`.
- `on_build_finished(opts)` — executed when build is finished, be it successful or failed. `opts` is a table with following keys:
  - `platform` — same as in `on_build_started`
  - `success` — whether build is successful, either `true` or `false`
- `on_bundle_started(opts)` — executed when you create a bundle or Build HTML5 version of a game. As with `on_build_started`, changes triggered by this hook will appear in a bundle, and errors will abort a bundle. `opts` will have these keys:
  - `output_directory` — a file path pointing to a directory with bundle output, for example `"/path/to/project/build/default/__htmlLaunchDir"`
  - `platform` — platform the game is bundled for. See a list of possible platform values in [Bob manual](/manuals/bob).
  - `variant` — bundle variant, either `"debug"`, `"release"` or `"headless"`
- `on_bundle_finished(opts)` — executed when bundle is finished, be it successful or not. `opts` is a table with the same data as `opts` in `on_bundle_started`, plus `success` key indicating whether build is successful.
- `on_target_launched(opts)` — executed when user launched a game and it successfully started. `opts` contains an `url` key pointing to a launched engine service, for example, `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — executed when launched game is closed, has same opts as `on_target_launched`

Please note that lifecycle hooks currently are an editor-only feature, and they are not executed by Bob when bundling from command line.

## Language servers

The editor supports a subset [Language Server Protocol](https://microsoft.github.io/language-server-protocol/). While we aim to expand the editor's support for LSP features in the future, currently it can only show diagnostics (i.e. lints) in the edited files and provide completions.

To define the language server, you need to edit your editor script's `get_language_servers` function like so:

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
The editor will start the language server using the specified `command`, using the server process's standard input and output for communication.

Language server definition table may specify:
- `languages` (required) — a list of languages the server is interested in, as defined [here](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers) (file extensions also work);
- `command` (required) - an array of command and its arguments
- `watched_files` - an array of tables with `pattern` keys (a glob) that will trigger the server's [watched files changed](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) notification.

## Editor scripts in libraries

You can publish libraries for other people to use that contain commands, and they will be automatically picked up by the editor. Hooks, on the other hand, can't be picked up automatically, since they have to be defined in a file that is in a root folder of a project, but libraries expose only subfolders. This is intended to give more control over build process: you still can create lifecycle hooks as simple functions in `.lua` files, so users of your library can require and use them in their `/hooks.editor_script`.

Also note that although dependencies are shown in Assets view, they do not exist as files (they are entries in a zip archive). It's possible to make the editor extract some files from the dependencies into `build/plugins/` folder. To do it, you need to create `ext.manifest` file in your library folder, and then create `plugins/bin/${platform}` folder in the same folder where the `ext.manifest` file is located. Files in that folder will be automatically extracted to `/build/plugins/${extension-path}/plugins/bin/${platform}` folder, so your editor scripts can reference them.

## Actions

::: sidenote
Previously, the editor interacted with the Lua VM in a blocking way, so there was a hard requirement for editor scripts to not block, since some interactions have to be done from the editor UI thread. For that reason, there was e.g. no `editor.execute()` and `editor.transact()`. Executing scripts and changing the editor state was instead triggered by returning an array of "actions" from hooks and command `run` handlers.

Now the editor interacts with the Lua VM in a non-blocking way, so there is no need for these actions any more: using functions like `editor.execute()` is more convenient, concise, and powerful. The actions are now **DEPRECATED**, though we have no plans to remove them.
:::

Editor scripts may return an array of actions from a command's `run` function or from `/hooks.editor_script`'s hook functions. These actions will then be performed by the editor.

Action is a table describing what editor should do. Every action has an `action` key. Actions come in 2 flavors: undoable and non-undoable.

### Undoable actions

::: sidenote
Prefer using `editor.transact()`.
:::

Undoable action can be undone after it is executed. If a command returns multiple undoable actions, they are performed together, and get undone together. You should use undoable actions if you can. Their downside is that they are more limited.

Existing undoable actions:
- `"set"` — set a property of a node in the editor to some value. Example:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  `"set"` action requires these keys:
  - `node_id` — node id userdata. Alternatively, you can use resource path here instead of node id you received from the editor, for example `"/main/game.script"`;
  - `property` — a property of a node to set, e.g. `"text"`;
  - `value` — new value for a property. For `"text"` property it should be a string.

### Non-undoable actions

::: sidenote
Prefer using `editor.execute()`.
:::

Non-undoable action clears undo history, so if you want to undo such action, you will have to use other means, such as version control.

Existing non-undoable actions:
- `"shell"` — execute a shell script. Example:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- trim leading "/"
    }
  }
  ```
  `"shell"` action requires `command` key, which is an array of command and it's arguments.

### Mixing actions and side effects

You can mix undoable and non-undoable actions. Actions are executed sequentially, hence depending on an order of actions you will end up losing ability to undo parts of that command.

Instead of returning actions from functions that expect them, you can just read and write to files directly using `io.open()`. This will trigger a resource reload that will clear undo history.