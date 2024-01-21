---
title: Writing code
brief: This manual briefly covers how to work with code in Defold.
---

# Writing code

While Defold allows you to create a lot of your game content using visual tools such as the tilemap and particle effect editors you still create your game logic using a code editor. Game logic is written using the [Lua programming language](https://www.lua.org/) while extensions to the engine itself are written using the native language(s) for the target platform.

## Writing Lua code

Defold uses Lua 5.1 and LuaJIT (depending on target platform) and you need to follow the language specification for those specific versions of Lua when writing your game logic. For more details on how to work with Lua in Defold see our [Lua in Defold manual](/manuals/lua).

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


### Adding Lua code linting using LSP

Defold supports a subset of the [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) which can be used to analyse your code and highlight programmatic and stylistic errors, a process also known as linting.

The Lua language server and code linter is available as a plugin. Install the plugin by [adding it as a dependency](/manuals/libraries/#setting-up-library-dependencies):

```
https://github.com/defold/lua-language-server/releases/download/v0.0.5/release.zip
```

Available versions can be seen in the [release page](https://github.com/defold/lua-language-server/releases) for the plugin. Learn more about the plugin on the [plugin support page on the Defold forum](https://forum.defold.com/t/linting-in-the-code-editor/72465).


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
