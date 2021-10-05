---
title: Working with files
brief: This manual explains how to save and load files and perform other kinds of file operations.
---

# Working with files
There are many different ways to create and/or access files. The file paths and the ways your access these files varies depending on the type of file and the location of the file.

## Functions for file and folder access
Defold provides several different functions to work with files:

* You can use the standard [`io.*` functions](https://defold.com/ref/stable/io/) to read and write files. These functions give you very fine-grained control over the entire I/O process.
* You can use [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) and [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) to rename and remove files.
* You can use [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) and [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) to read and write Lua tables. Additional [`sys.*`](https://defold.com/ref/stable/sys/) functions exist to help with platform independent file path resolution.

## File and folder locations
File and folder locations can be divided into three categories:

* Application specific files created by your application
* Files and folders bundled with your application
* System specific files accessed by your application

### How to save and load application specific files
When saving and loading application specific files such as high scores, user settings and game state it is recommended to do so in a location provided by the operating system and intended specifically for this purpose. You can use [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) to get the OS specific absolute path to a file. Once you have the absolute path you can use the `sys.*`, `io.*` and `os.*` functions (see above).

[Check the example showing how to use sys.save() and sys.load()](/examples/file/sys_save_load/).

### How to access files bundled with the application
You can bundle files with your application in two ways:

1. **CUSTOM RESOURCES** - As part of the game archive using the [*Custom Resources* field](https://defold.com/manuals/project-settings/#project) in *game.project*. You can read these files using [`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource). Note that these aren't actual files on the file system. Files included this way becomes part of the binary game archive and the only way to access them is through `sys.load_resource()`.

2. **BUNDLE RESOURES** - As additional files and folders located as a part of your application bundle using the [*Bundle Resources* field](https://defold.com/manuals/project-settings/#project) in *game.project*. You can use [`sys.get_application_path()`](https://defold.com/ref/stable/sys/#sys.get_application_path:) to get the path to where the application is stored. Use this application base path to create the final absolute path to the files you need access to. Once you have the absolute path of these files you can use the `io.*` and `os.*` functions to access the files (see above).

::: sidenote
For security reasons browsers (and by extension any JavaScript running in a browser) is prevented from accessing system files. File operations in HTML5 builds in Defold still work, but only on a "virtual file system" using the IndexedDB API in the browser. What this means is that there is no way to access bundle resources using `io.*` or `os.*` functions. You can however access bundle resources using `http.request()`.
:::


#### Custom and Bundle resources - comparison

| Characteristic              | Custom Resources                          | Bundle Resources                               |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| Loading speed               | Faster - files loaded from binary archive | Slower - files loaded from filesystem          |
| Load partial files          | No - only entire files                    | Yes - read arbitrary bytes from file           |
| Modify files after bundling | No - files stored inside a binary archive | Yes - files stored on the local file system    |
| HTML5 support               | Yes                                       | Yes - but access through http and not file I/O |


### System file access
Access to system files may be restricted by the operating system for security reasons. You can use the [`extension-directiories`](https://defold.com/assets/extensiondirectories/) native extension to get the absolute path to some common system directories (ie documents, resource, temp). Once you have the absolute path of these files you can use the `io.*` and `os.*` functions to access the files (see above).

::: sidenote
For security reasons browsers (and by extension any JavaScript running in a browser) is prevented from accessing system files. File operations in HTML5 builds in Defold still work, but only on a "virtual file system" using the IndexedDB API in the browser. What this means is that there is no way to access system files in HTML5 builds.
:::

## Extensions
The [Asset Portal](https://defold.com/assets/) contains several assets to simplify file and folder access. Some examples:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - Functions to work with directories, file permissions etc
* [DefSave](https://defold.com/assets/defsave/) - A module to help you save / load config and player data between session.
