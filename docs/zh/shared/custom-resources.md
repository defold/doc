## 自定义资源

自定义资源通过 *game.project* 中的[*自定义资源*字段](https://defold.com/manuals/project-settings/#custom-resources)捆绑到主游戏存档中。

*自定义资源*字段应包含将包含在主游戏存档中的以逗号分隔的资源列表。如果指定了目录，则该目录中的所有文件和目录都将被递归包含。您可以使用[`sys.load_resource()`](/ref/sys/#sys.load_resource)读取这些文件。