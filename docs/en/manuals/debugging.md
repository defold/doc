---
title: Debugging in Defold
brief: This manual explains the debugging facilities present in Defold.
---

# Debugging

Defold contains an integrated Lua debugger with an inspection facility. Together with the built-in [profiling tools](/manuals/profiling) it is a powerful tool that can help finding the cause of bugs in your game logic or help analyze performance issues. Defold also provides crash logs for the rare occasions when the engine itself crashes.

The Lua debugger uses the engine's native Debug Adapter Protocol (DAP) server. It is available in native debug and headless builds; Web and release builds do not provide the TCP debugger.

* Learn more about [debugging your game logic](/manuals/debugging-game-logic).
* Learn how to [connect to the native Lua DAP debugger](/manuals/debugging-game-logic/#native-dap-connections) from an external client, including a [VS Code setup example](/manuals/debugging-game-logic/#vs-code).
* Learn more about [debugging native code](/manuals/debugging-native-code).
* Learn how to [record the game window to an MP4 file](/manuals/recording) from Lua or development tools.
