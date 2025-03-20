---
title: Defold project ignores
brief: This manual describes how to ignore files and folders in Defold.
---

# Ignoring files

It is possible to configure the Defold editor and tools to ignore files and folders in a project. This can be useful if the project contains files with file extensions which conflict with file extensions used by Defold. One such example is Go language files with the .go file extension which is the same as the editor uses for game object files.

## The `.defignore` file
The files and folders to exclude are defined in a file named `.defignore` in the project root. The file should list files and folders to exclude, one per line. Example:

```
/path/to/file.png
/otherpath
```

This will exclude the file `/path/to/file.png` and anything in the path `/otherpath`.

## The `.defunload` file

For certain large projects that contain multiple independent modules, you may want to exclude parts of it from loading to reduce memory usage and load times in the editor. To achieve this, you can list paths to exclude from loading in a `.defunload` file below the project directory.

Simply put, the `.defunload` file allows you to hide parts of the project from the editor without making it a build error to reference the hidden resources.

The patterns in `.defunload` use the same rules as the `.defignore` file. Unloaded Collections and Game Objects will behave as if they were empty when referenced by loaded resources. Other resources that match `.defunload` patterns will be in an unloaded state, and cannot be viewed in the editor. However, if a resource that is loaded depends on them, the unloaded resources and their dependencies are loaded automatically.

For example, if a Sprite depends on images in an Atlas, we have to load the Atlas, or the missing image will be reported as an error. If this happens, a notification will warn the user about the situation and provide information about which unloaded resource was referenced from where.

The editor will prevent the user from adding references to `.defunloaded` resources from loaded resources, so this situation only occurs when resources are read from disk.

Contrary to the `.defignore` file, you need to restart the editor after you edit the `.defunload` file to see the changes take effect.
