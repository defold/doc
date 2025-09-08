## 捆绑资源

捆绑资源是使用 *game.project* 文件中的[*Bundle Resources* 字段](/manuals/project-settings/#bundle-resources)作为应用程序包一部分存放的附加文件和文件夹。

*Bundle Resources* 字段应包含一个以逗号分隔的目录列表，这些目录包含资源文件和文件夹，在打包时应原样复制到最终包中。目录必须使用从项目根目录开始的绝对路径指定，例如 `/res`。资源目录必须包含以 `platform` 或 `architecture-platform` 命名的子文件夹。

支持的平台有 `ios`、`android`、`osx`、`win32`、`linux`、`web`、`switch`。还允许使用名为 `common` 的子文件夹，其中包含所有平台通用的资源文件。示例：

```
res
├── win32
│   └── mywin32file.txt
├── common
│   └── mycommonfile.txt
└── android
    ├── myandroidfile.txt
    └── res
        └── xml
            └── filepaths.xml
```

您可以使用 [`sys.get_application_path()`](/ref/stable/sys/#sys.get_application_path:) 来获取应用程序存储的路径。使用此应用程序基本路径来创建您需要访问的文件的最终绝对路径。一旦获得这些文件的绝对路径，您就可以使用 `io.*` 和 `os.*` 函数来访问这些文件。