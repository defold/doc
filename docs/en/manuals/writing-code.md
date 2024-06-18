---
title: Writing code
brief: This manual briefly covers how to work with code in Defold.
---

# Writing code

While Defold allows you to create a lot of your game content using visual tools such as the tilemap and particle effect editors you still create your game logic using a code editor. Game logic is written using the [Lua programming language](https://www.lua.org/) while extensions to the engine itself are written using the native language(s) for the target platform.

## Writing Lua code

Defold uses Lua 5.1 and LuaJIT (depending on target platform) and you need to follow the language specification for those specific versions of Lua when writing your game logic. For more details on how to work with Lua in Defold see our [Lua in Defold manual](/manuals/lua).

## Using other languages that transpile to Lua

Starting from version 1.8.1, Defold supports the use of transpilers that emit Lua code. With transpiler extension installed, you can use alternative languages — such as [Teal](https://github.com/defold/extension-teal) — to write statically-checked Lua. It is a preview feature that has limitations: current transpiler support does not expose the information about modules and functions defined in the Defold Lua runtime. It means that using Defold APIs like `go.animate` will require you to write external definitions yourself.

## Writing native code

Defold allows you to extend the game engine with native code to access platform specific functionality not provided by the engine itself. You can also use native code when the performance of Lua isn't enough (resource intensive calculations, image processing etc). Refer to our [manuals on Native Extensions](/manuals/extensions/) to learn more.

## Using the built-in code editor

Defold has a built-in code editor that allows you to open and edit Lua files (.lua), Defold script files (.script, .gui_script and .render_script) as well as any other file with a file extension not natively handled by the editor. Additionally the editor provides syntax highlighting for Lua and script files.

![](/images/editor/code-editor.png)


### Code completion

The built-in code editor will show code completion of functions while writing code:

![](/images/editor/codecompletion.png)

Pressing <kbd>CTRL</kbd> + <kbd>Space</kbd> will show additional information about functions, arguments and return values:

![](/images/editor/apireference.png)

### Linting configuration

The built-in code editor performs code linting using [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) and [Lua language server](https://luals.github.io/wiki/diagnostics/). To configure the Luacheck, create a `.luacheckrc` file in the project root. You can read the [Luacheck configuration page](https://luacheck.readthedocs.io/en/stable/config.html) for the list of the available options. Defold uses the following defaults for the Luacheck configuration:

```lua
unused_args = false      -- don't warn on unused arguments (common for .script files)
max_line_length = false  -- don't warn on long lines
ignore = {
    "611",               -- line contains only whitespace
    "612",               -- line contains trailing whitespace
    "614"                -- trailing whitespace in a comment
},
```

## Using an external code editor

The code editor in Defold provides the basic functionality you need to write code, but for more advanced use cases or for power users with a favorite code editor it is possible to let Defold open files using an external editor. In the [Preferences window under the Code tab](/manuals/editor-preferences/#code) it is possible to define an external editor that should be used when editing code.

### Visual Studio Code - Defold Kit

Defold Kit is a Visual Studio Code plugin with the following features:

* Installing recommended extensions
* Lua highlighting, autocompletion and linting
* Applying relevant settings to the workspace
* Lua annotations for Defold API
* Lua annotations for dependencies
* Building and launching
* Debugging with breakpoints
* Bundling for all the platforms
* Deploying to connected mobile devices

Learn more and install Defold Kit from the [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).


## Documentation software

Community created API reference packages are available for [Dash and Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
