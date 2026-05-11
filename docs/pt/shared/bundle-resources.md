Bundle resources são arquivos e pastas adicionais localizados como parte do bundle da sua aplicação usando o campo [*Bundle Resources*](/manuals/project-settings/#bundle-resources) em *game.project*.

O campo *Bundle Resources* deve conter uma lista separada por vírgulas de diretórios com arquivos e pastas de recursos que devem ser copiados como estão para o pacote resultante ao empacotar. Os diretórios devem ser especificados com um caminho absoluto a partir da raiz do projeto, por exemplo `/res`. O diretório de recursos deve conter subpastas nomeadas por `platform`, ou `architecture-platform`.

As plataformas suportadas são `ios`, `android`, `osx`, `win32`, `linux`, `web`, `switch`. Uma subpasta chamada `common` também é permitida, contendo arquivos de recursos comuns a todas as plataformas. Exemplo:

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

Você pode usar [`sys.get_application_path()`](/ref/stable/sys/#sys.get_application_path:) para obter o caminho onde a aplicação está armazenada. Use esse caminho base da aplicação para criar o caminho absoluto final para os arquivos que você precisa acessar. Depois de ter o caminho absoluto desses arquivos, você pode usar as funções `io.*` e `os.*` para acessá-los.
