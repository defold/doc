Le risorse personalizzate vengono incluse nell'archivio principale del gioco tramite il [campo *Custom Resources*](https://defold.com/manuals/project-settings/#custom-resources) in *game.project*.

Il campo *Custom Resources* deve contenere un elenco di risorse separate da virgole che verranno incluse nell'archivio principale del gioco. Se specifichi delle directory, tutti i file e le directory al loro interno vengono inclusi in modo ricorsivo. Puoi leggere i file usando [`sys.load_resource()`](/ref/sys/#sys.load_resource).
