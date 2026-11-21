---
title: Debugging native code on HTML5
brief: This manual describes how to debug the engine and native extensions in the browser, and how to symbolicate HTML5 callstacks.
---

# Debugging native code on HTML5

HTML5 builds run as WebAssembly, and you can debug the engine and your native extensions as C/C++ code in the browser developer tools. This manual covers:

* What to bundle and how to serve it
* [Debugging in Chrome](#chrome), which offers the most complete experience
* [Firefox](#firefox) and [Safari](#safari)
* How to [symbolicate a callstack](#symbolicate-a-callstack) collected from a player's browser

## Bundling with debug info

Bundle the *Debug* variant with debug symbols. In the editor these are the defaults of the HTML5 bundle dialog: the *Debug* variant, with **Generate debug symbols** checked. With [Bob](/manuals/bob/):

```
$ java -jar bob.jar --platform=wasm-web --architectures=wasm-web --variant=debug --with-symbols --archive resolve build bundle --bundle-output bundle/web
```

Next to the engine the bundle now contains two extra files:

| File | Used by | Contains |
|------|---------|----------|
| `<project_name>.wasm.debug.wasm` | Chrome | The DWARF debug info |
| `<project_name>.wasm.map` | Firefox, and Chrome without the DWARF extension | A source map |

Bundles for the `wasm_pthread-web` architecture have the files `<project_name>_pthread.wasm.debug.wasm` and `<project_name>_pthread.wasm.map`.

The bundled `dmloader.js` also instantiates the engine directly from its URL, because the browser finds the two files relative to that URL. It does this even if `html5.wasm_streaming` is disabled.

::: important
A Debug bundle with debug symbols has these files in the same folder as your game, so they will be uploaded if you upload that folder. They are large, and they expose the structure of your code and possibly its sources. The running game does not need them. Before you share a Debug bundle, remove them or bundle without **Generate debug symbols**.
:::

### Which builds have debug info

| Build | Debug variant | Release variant |
|-------|---------------|-----------------|
| Project using the official engine | Next to the engine | None, only the [symbol map](#symbolicate-a-callstack) |
| Project built by the build server, because it has native extensions or an app manifest | Next to the engine | None, only the symbol map, unless you [ask for it](#debug-info-for-release-builds) |

### Debug info for Release builds

Linking with debug info changes the engine: the build keeps the function names, skips minifying the JavaScript and limits the WebAssembly optimizations. In a small test project a Release build grew from 3.0 MB to 3.8 MB for the `.wasm` and from 257 KB to 460 KB for the `.js`. That is why a Release build only has function names in its callstacks by default.

If you want file and line numbers for the crashes of a Release build, and your project is built by the build server, ask for debug info in your [app manifest](/manuals/app-manifest/) and bundle with symbols:

```yaml
context:
    releaseDebugInfo: true
```

The `.wasm.debug.wasm` and `.wasm.map` files are then stored in the `<project_name>_symbols` folder next to the bundle, so they stay out of the folder you deploy, and the engine does not reference them. You use them to [symbolicate a callstack](#symbolicate-a-callstack), not to debug the game in the browser. A callstack can only be resolved with the debug info of the build that produced it, so the build with this setting is the one to ship.

### Bundle settings that disable debugging

The developer tools can't attach debug info if the engine is instantiated from memory instead of from its URL. This happens in the following cases, and the loader prints a warning in the console when it does:

* Bundling with `--with-sha1`, because the loader then has to download the file and verify it before it instantiates the engine. Don't use this option for bundles you want to debug.
* Serving the `.wasm` with the wrong `Content-Type`. See below.

If the engine appears as `wasm://wasm/...` in the developer tools, no debug info is loaded. If the console has no such warning, the bundle has no debug info. Check that the `.wasm.debug.wasm` is next to the `.wasm`. The **Project ▸ Build HTML5** command in the editor does not include debug info, so use a bundle.

## Serving the bundle

An HTML5 bundle [needs an HTTP server](/manuals/html5/#creating-html5-bundle). For debugging, the server has to meet these requirements:

* Serve the `.wasm` with `Content-Type: application/wasm`.
* Serve the `.wasm.debug.wasm` and `.wasm.map` from the same directory as the `.wasm`.
* For the `wasm_pthread-web` architecture, send the headers `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`. Without them the browser uses the single threaded engine, if the bundle has one. See the [HTML5 manual](/manuals/html5/#creating-html5-bundle).

For a build without threads, Python's web server is enough:

```
$ cd bundle/web/<project_name>
$ python3 -m http.server
```

## Chrome

Chrome gives you breakpoints, stepping and call stacks with C/C++ names. You can also inspect the variables of your native extensions, as far as the optimized code allows it. The official engines only contain line information, so engine code has no variables to inspect.

1. Install the [C/C++ DevTools Support (DWARF)](https://chromewebstore.google.com/detail/cc++-devtools-support-dwa/pdcpmagijalfljmkmjngeonclgbbannb) extension.
2. Open the developer tools, and then load the page. Loading with the tools open makes sure they see the engine from the start.
3. Open the C/C++ files in the *Sources* panel, and set your breakpoints.

### Finding the source files

The debug info stores the paths the sources had when they were compiled, and they rarely exist on your computer. You map them to local folders in the extension options, under *Path substitutions*. To open the options, right-click the extension icon and select *Options*.

The official engines use these paths:

| Path in the debug info | Map it to |
|------------------------|-----------|
| `engine/...` | The `engine` folder of a [Defold source](https://github.com/defold/defold) checkout, at the same version as your engine |
| `defoldsdk/...` | The unpacked `defoldsdk` folder of the Defold SDK for your engine version, from `https://d.defold.com/archive/stable/<sha1>/engine/defoldsdk.zip` |
| `/emsdk/emscripten/...` | The folder `upstream/emscripten` of an Emscripten SDK |

Native extension code is compiled in a temporary folder on the build server. To get a stable path, set `debugSourcePath` at the top level of your [app manifest](/manuals/app-manifest/):

```yaml
context:
    debugSourcePath: /Users/me/mygame
```

The sources of an extension then get the path `/Users/me/mygame/extensions/<path in your project>`, where the folder `extensions` is always added by the build server. Add a path substitution from `/Users/me/mygame/extensions` to the folder of your project. The value does not have to be a real path. It can contain letters, digits and the characters `._+-/`, so on Windows you need a value without a drive letter, such as `/mygame`.

## Firefox

Firefox reads the source map, so you get files, line breakpoints and stepping, but no variable inspection.

* The official engines include their sources in the map. In a build from the build server, the map only has the file names of the sources, so the files appear without content.
* The sources usually appear after a second reload with the developer tools open.
* A breakpoint on a C/C++ line is often not active until the debugger has paused once. Pause and resume the execution, and the breakpoints start to work.
* Firefox logs a `Source map error` for a small module named after `dmloader.js`. The loader compiles this module to detect WebAssembly support, and you can ignore the error. The engine has its own entry, named after the `.wasm`.

## Safari

Safari has no support for C/C++ debugging of WebAssembly: Web Inspector reads neither the source map nor the DWARF info. You get the WebAssembly disassembly, the console and the JavaScript callstacks. Use Chrome to debug native code, and Safari to reproduce Safari specific issues. You can still [symbolicate](#symbolicate-a-callstack) the callstacks from Safari, but they only resolve to function names.

## Symbolicate a callstack

If the engine crashes, it logs the callstack to the browser console between `CALL STACK:` and `CALL STACK END`, as a list of frames followed by the Lua callstack:

```
ERROR:CRASH: CALL STACK:
["RuntimeError: unreachable","dmengine.wasm.func@https://host/Game.wasm:wasm-function[521]:0x8c6d",...]Lua Callstack:
  main/main.script:17: in function <main/main.script:7>

CALL STACK END
```

Each WebAssembly frame has the index of the function, and in Chrome and Firefox a byte offset from the start of the `.wasm`. Safari only reports the index. Depending on the browser and on how the callstack was captured, the frames look like this:

* `at name (https://host/Game.wasm:wasm-function[1234]:0x56789a)`
* `name@https://host/Game.wasm:wasm-function[1234]:0x56789a`
* `<?>.wasm-function[1234]@[wasm code]`

To translate these frames into names and lines, keep the following files for every version you release, and do not deploy them. They are all in the `<project_name>_symbols` folder next to the bundle, except in a Debug bundle, where the debug info is in the bundle folder:

* `<project_name>_wasm.js.symbols`, which maps function indices to names. For `wasm_pthread-web` the name is `<project_name>_pthread_wasm.js.symbols`.
* `<project_name>.wasm.debug.wasm` if your build has it, which [depends on the build](#which-builds-have-debug-info). It maps offsets to files and lines.

They must come from the exact build that crashed. A build from the build server is unique, so another build of the same code will not match.

Then run the script [`symbolicate_web_callstack.py`](https://github.com/defold/defold/blob/dev/scripts/web/symbolicate_web_callstack.py) from the Defold repository on a file with the callstack. It needs `llvm-symbolizer` from the Emscripten SDK, which it finds through the `EMSDK` environment variable, the `--emsdk` option or your `PATH`:

```
$ python3 symbolicate_web_callstack.py --wasm-debug Game_symbols/Game.wasm.debug.wasm callstack.txt
```

The script finds the symbol map in the same folder, or in the `<project_name>_symbols` folder for a Debug bundle. If you stored it somewhere else, add `--symbols path/to/Game_wasm.js.symbols`. Each WebAssembly frame then gets a line with its function, file and line:

```
dmengine.wasm.func@https://host/Game.wasm:wasm-function[521]:0x8c6d
    -> CrashInner() at /Users/me/mygame/extensions/myextension/src/myextension.cpp:15:5
```

A build without a `.wasm.debug.wasm` only resolves to function names:

```
$ python3 symbolicate_web_callstack.py --symbols Game_symbols/Game_wasm.js.symbols callstack.txt
```

The script does not print frames for inlined functions.

### Debug IDs for symbolication services

A build linked with symbols has a `build_id` section with the same value in both the `.wasm` and the `.wasm.debug.wasm`. Services that accept WebAssembly debug files can use it to match a crash with the right file. Sentry, for example, shows it with `sentry-cli debug-files check <project_name>.wasm.debug.wasm` and receives the file through `sentry-cli debug-files upload`. The engine does not include a crash reporter for such a service, so sending the reports is up to your project, for example through a native extension.
