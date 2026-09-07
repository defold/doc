Les ressources de bundle sont des fichiers et dossiers supplémentaires intégrés au bundle de votre application à l'aide du [champ *Bundle Resources*](/manuals/project-settings/#bundle-resources) dans *game.project*.

Le champ *Bundle Resources* doit contenir une liste, séparée par des virgules, de répertoires contenant les fichiers et dossiers de ressources à copier tels quels dans le paquet résultant lors de la création du bundle. Les répertoires doivent être spécifiés par un chemin absolu à partir de la racine du projet, par exemple `/res`. Le répertoire des ressources doit contenir des sous-dossiers nommés selon `platform` ou `architecture-platform`.

Les plateformes prises en charge sont `ios`, `android`, `osx`, `win32`, `linux`, `web`, `switch`. Un sous-dossier nommé `common` est également autorisé, contenant les fichiers de ressources communs à toutes les plateformes. Exemple :

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

Vous pouvez utiliser [`sys.get_application_path()`](/ref/stable/sys/#sys.get_application_path:) pour obtenir le chemin de l'emplacement où l'application est stockée. Utilisez ce chemin de base de l'application pour créer le chemin absolu final vers les fichiers auxquels vous devez accéder. Une fois que vous disposez du chemin absolu de ces fichiers, vous pouvez utiliser les fonctions `io.*` et `os.*` pour y accéder.
