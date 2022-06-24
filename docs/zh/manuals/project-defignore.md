---
title: Defold 项目忽略文件
brief: 本教程介绍了 Defold 中如何忽略文件和目录.
---

# 忽略文件

可以在 Defold 编辑器和工具中忽略项目的文件和文件夹. 当 Defold 自用文件的扩展名与项目文件的扩展名冲突时这会很有用. 比如编辑器使用的游戏对象文件就可能与项目扩展库里的 Go 语言的 .go 文件相冲突.

## 忽略定义 .defignore 文件
需要被忽略的文件和文件夹被定义在项目根目录的一个 `.defignore` 的文件中. 文件中包含被忽略的文件和路径, 一行定义一个. 比如:

```
/path/to/file.png
/otherpath
```

这样就会忽略 `/path/to/file.png` 文件和路径 `/otherpath` 下的所有文件.