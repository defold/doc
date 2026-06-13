Los recursos de bundle son archivos y carpetas adicionales ubicados como parte del bundle de tu aplicación usando el [campo *Bundle Resources*](/manuals/project-settings/#bundle-resources) en *game.project*.

El campo *Bundle Resources* debe contener una lista separada por comas de directorios que contienen archivos de recursos y carpetas que deben copiarse tal cual en el paquete resultante al crear el bundle. Los directorios deben especificarse con una ruta absoluta desde la raíz del proyecto, por ejemplo `/res`. El directorio de recursos debe contener subcarpetas con nombres según `platform` o `architecture-platform`.

Las plataformas soportadas son `ios`, `android`, `osx`, `win32`, `linux`, `web`, `switch`. También se permite una subcarpeta llamada `common`, que contiene archivos de recursos comunes para todas las plataformas. Ejemplo:

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

Puedes usar [`sys.get_application_path()`](/ref/stable/sys/#sys.get_application_path:) para obtener la ruta donde está almacenada la aplicación. Usa esta ruta base de la aplicación para crear la ruta absoluta final a los archivos a los que necesitas acceder. Una vez que tengas la ruta absoluta de estos archivos, puedes usar las funciones `io.*` y `os.*` para acceder a los archivos.
