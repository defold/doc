Custom resources são incluídos no arquivo principal do jogo usando o campo [*Custom Resources*](https://defold.com/manuals/project-settings/#custom-resources) em *game.project*.

O campo *Custom Resources* deve conter uma lista separada por vírgulas de recursos que serão incluídos no arquivo principal do jogo. Se diretórios forem especificados, todos os arquivos e diretórios dentro desse diretório serão incluídos recursivamente. Você pode ler os arquivos usando [`sys.load_resource()`](/ref/sys/#sys.load_resource).
