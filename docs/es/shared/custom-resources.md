Los recursos personalizados se empaquetan en el archivo principal del juego usando el [campo *Custom Resources*](https://defold.com/manuals/project-settings/#custom-resources) en `game.project`.

El campo *Custom Resources* debe contener una lista separada por comas de los recursos que se incluirán en el archivo principal del juego. Si se especifican directorios, todos los archivos y directorios dentro de ese directorio se incluyen de forma recursiva. Puedes leer los archivos usando [`sys.load_resource()`](/ref/sys/#sys.load_resource).
