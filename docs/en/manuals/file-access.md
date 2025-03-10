---
title: Working with files
brief: This manual explains how to save and load files and perform other kinds of file operations.
---

# Working with files
There are many different ways to create and/or access files. The file paths and the ways your access these files varies depending on the type of file and the location of the file.

## Functions for file and folder access
Defold provides several different functions to work with files:

* You can use the standard [`io.*` functions](https://defold.com/ref/stable/io/) to read and write files. These functions give you very fine-grained control over the entire I/O process.

```lua
-- open myfile.txt for writing in binary mode
-- returns nil plus error message on failure
local f, err = io.open("path/to/myfile.txt", "wb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- write to the file, flush it to disk and then close the file
f:write("Foobar")
f:flush()
f:close()

-- open myfile.txt for reading in binary mode
-- returns nil plus error message on failure
local f, err = io.open("path/to/myfile.txt", "rb")
if not f then
	print("Something went wrong while opening the file", err)
	return
end

-- read the entire file as a string
-- returns nil on failure
local s = f:read("*a")
if not s then
	print("Error while reading file")
	return
end

print(s) -- Foobar
```

* You can use [`os.rename()`](https://defold.com/ref/stable/os/#os.rename:oldname-newname) and [`os.remove()`](https://defold.com/ref/stable/os/#os.remove:filename) to rename and remove files.

* You can use [`sys.save()`](https://defold.com/ref/stable/sys/#sys.save:filename-table) and [`sys.load()`](https://defold.com/ref/stable/sys/#sys.load:filename) to read and write Lua tables. Additional [`sys.*`](https://defold.com/ref/stable/sys/) functions exist to help with platform independent file path resolution.

```lua
-- get a platform independent path to the file "highscore" for application "mygame"
local path = sys.get_save_file("mygame", "highscore")

-- save a Lua table with some data
local ok = sys.save(path, { highscore = 100 })
if not ok then
	print("Failed to save", path)
	return
end

-- load the data
local data = sys.load(path)
print(data.highscore) -- 100
```


## File and folder locations
File and folder locations can be divided into three categories:

* Application specific files created by your application
* Files and folders bundled with your application
* System specific files accessed by your application

### How to save and load application specific files
When saving and loading application specific files such as high scores, user settings and game state it is recommended to do so in a location provided by the operating system and intended specifically for this purpose. You can use [`sys.get_save_file()`](https://defold.com/ref/stable/sys/#sys.get_save_file:application_id-file_name) to get the OS specific absolute path to a file. Once you have the absolute path you can use the `sys.*`, `io.*` and `os.*` functions (see above).

[Check the example showing how to use `sys.save()` and `sys.load()`](/examples/file/sys_save_load/).

### How to access files bundled with the application
You can include files with your application using bundle resources and custom resources.

#### Custom Resources
:[Custom Resources](../shared/custom-resources.md)

```lua
-- Load level data into a string
local data, error = sys.load_resource("/assets/level_data.json")
-- Decode json string to a Lua table
if data then
  local data_table = json.decode(data)
  pprint(data_table)
else
  print(error)
end
```

#### Bundle Resources
:[Bundle Resources](../shared/bundle-resources.md)

```lua
local path = sys.get_application_path()
local f = io.open(path .. "/mycommonfile.txt", "rb")
local txt, err = f:read("*a")
if not txt then
	print(err)
	return
end
print(txt)
```

::: sidenote
For security reasons browsers (and by extension any JavaScript running in a browser) is prevented from accessing system files. File operations in HTML5 builds in Defold still work, but only on a "virtual file system" using the IndexedDB API in the browser. What this means is that there is no way to access bundle resources using `io.*` or `os.*` functions. You can however access bundle resources using `http.request()`.
:::


#### Custom and Bundle resources - comparison

| Characteristic              | Custom Resources                          | Bundle Resources                               |
|-----------------------------|-------------------------------------------|------------------------------------------------|
| Loading speed               | Faster - files loaded from binary archive | Slower - files loaded from filesystem          |
| Load partial files          | No - only entire files                    | Yes - read arbitrary bytes from file           |
| Modify files after bundling | No - files stored inside a binary archive | Yes - files stored on the local file system    |
| HTML5 support               | Yes                                       | Yes - but access through http and not file I/O |


### System file access
Access to system files may be restricted by the operating system for security reasons. You can use the [`extension-directories`](https://defold.com/assets/extensiondirectories/) native extension to get the absolute path to some common system directories (ie documents, resource, temp). Once you have the absolute path of these files you can use the `io.*` and `os.*` functions to access the files (see above).

::: sidenote
For security reasons browsers (and by extension any JavaScript running in a browser) is prevented from accessing system files. File operations in HTML5 builds in Defold still work, but only on a "virtual file system" using the IndexedDB API in the browser. What this means is that there is no way to access system files in HTML5 builds.
:::

## Extensions
The [Asset Portal](https://defold.com/assets/) contains several assets to simplify file and folder access. Some examples:

* [Lua File System (LFS)](https://defold.com/assets/luafilesystemlfs/) - Functions to work with directories, file permissions etc
* [DefSave](https://defold.com/assets/defsave/) - A module to help you save / load config and player data between session.
