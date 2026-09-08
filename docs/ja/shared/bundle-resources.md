バンドルリソース（bundle resources）は、*game.project* の [*Bundle Resources* フィールド](/manuals/project-settings/#bundle-resources) を使用してアプリケーションのバンドル（bundle）の一部として配置される、追加のファイルやフォルダーです。

*Bundle Resources* フィールドには、バンドル作成時に生成されるパッケージへそのままコピーするリソースファイルやフォルダーを含むディレクトリを、カンマ区切りで指定します。ディレクトリは、たとえば `/res` のように、プロジェクトのルートからの絶対パスで指定する必要があります。リソースディレクトリには、`platform` または `architecture-platform` という形式で名前を付けたサブフォルダーを含める必要があります。

サポートされているプラットフォームは、`ios`、`android`、`osx`、`win32`、`linux`、`web`、`switch` です。すべてのプラットフォームで共通のリソースファイルを含む、`common` という名前のサブフォルダーも使用できます。例:

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

[`sys.get_application_path()`](/ref/stable/sys/#sys.get_application_path:) を使用すると、アプリケーションが保存されている場所のパスを取得できます。このアプリケーションのベースパスを使用して、アクセスする必要があるファイルへの最終的な絶対パスを作成します。これらのファイルの絶対パスを取得したら、`io.*` と `os.*` の関数を使用してファイルにアクセスできます。
