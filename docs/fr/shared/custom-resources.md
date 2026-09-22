Les ressources personnalisées sont incluses dans l'archive principale du jeu au moyen du [champ *Custom Resources*](https://defold.com/manuals/project-settings/#custom-resources) de *game.project*.

Le champ *Custom Resources* doit contenir une liste de ressources séparées par des virgules qui seront incluses dans l'archive principale du jeu. Si des répertoires sont indiqués, tous les fichiers et répertoires qu'ils contiennent sont inclus de manière récursive. Vous pouvez lire les fichiers avec [`sys.load_resource()`](/ref/sys/#sys.load_resource).
