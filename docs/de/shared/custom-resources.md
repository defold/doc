Benutzerdefinierte Ressourcen (custom resources) werden über das [Feld *Custom Resources*](https://defold.com/manuals/project-settings/#custom-resources) in *game.project* in das Hauptarchiv des Spiels aufgenommen.

Das Feld *Custom Resources* sollte eine durch Kommas getrennte Liste der Ressourcen enthalten, die in das Hauptarchiv des Spiels aufgenommen werden. Wenn Verzeichnisse angegeben sind, werden alle Dateien und Verzeichnisse im jeweiligen Verzeichnis rekursiv aufgenommen. Du kannst die Dateien mit [`sys.load_resource()`](/ref/sys/#sys.load_resource) lesen.
