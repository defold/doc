---
title: Defold project ignores
brief: This manual describes how to ignore files and folders in Defold.
---

# Ignoring files

It is possible to configure the Defold editor and tools to ignore files and folders in a project. This can be useful if the project contains files with file extensions which conflict with file extensions used by Defold. One such example is Go language files with the .go file extension which is the same as the editor uses for game object files.

## The .defignore file
The files and folders to exclude are defined in a file named `.defignore` in the project root. The file should list files and folders to exclude, one per line. Example:

```
/path/to/file.png
/otherpath
```

This will exclude the file `/path/to/file.png` and anything in the path `/otherpath`.