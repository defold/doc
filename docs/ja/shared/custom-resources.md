カスタムリソース（custom resource）は、*game.project* の [*Custom Resources* フィールド](https://defold.com/manuals/project-settings/#custom-resources) を使って、ゲームのメインアーカイブに同梱されます。

*Custom Resources* フィールドには、ゲームのメインアーカイブに含めるリソースをカンマ区切りのリストで指定します。ディレクトリを指定すると、そのディレクトリ内のすべてのファイルとディレクトリが再帰的に含まれます。[`sys.load_resource()`](/ref/sys/#sys.load_resource) を使ってファイルを読み込めます。
