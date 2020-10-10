---
title: Writing code
brief: This manual briefly covers how to work with code in Defold.
---

# Writing code

While Defold allows you to create a lot of your game content using visual tools such as the tilemap and particle effect editors you still create your game logic using a code editor. Game logic is written using the [Lua programming language](https://www.lua.org/) while extensions to the engine itself are written using the native language(s) for the target platform.

Defold has a built-in text editor that allows you to open and edit Lua files (.lua), Defold script files (.script, .gui_script and .render_script) as well as any other file with a file extension not natively handled by the editor. Additionally the editor provides syntax highlighting for Lua and script files.

## Writing Lua code

Defold uses Lua 5.1 and LuaJIT (depending on target platform) and you need to follow the language specification for those specific versions of Lua when writing your game logic. For more details on how to work with Lua in Defold see our [Lua in Defold manual](/manuals/lua).

## Writing native code

Defold allows you to extend the game engine with native code to access platform specific functionality not provided by the engine itself. You can also use native code when the performance of Lua isn't enough (resource intensive calculations, image processing etc). Refer to our [manuals on Native Extensions](/manuals/extensions/) to learn more.

## Using an external code editor

The code editor in Defold provides the basic functionality you need to write code, but for more advanced use cases or for power users with a favorite code editor it is possible to let Defold open files using an external editor. In the Preferences window under the Code tab it is possible to define an external editor that should be used when editing code.

The Defold community has created auto-complete plugins for popular editors such as [Atom](https://atom.io/packages/defold-ide), [Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=selimanac.defold-vsc-snippets) and [Sublime](https://forum.defold.com/t/full-autocomplete-defold-api-for-sublime-text-3/10910). In addition to these there is also API reference packages for [Dash and Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
