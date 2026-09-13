Bundle-Ressourcen (bundle resources) sind zusätzliche Dateien und Ordner, die du über das [Feld *Bundle Resources*](/manuals/project-settings/#bundle-resources) in *game.project* in das Bundle deiner Anwendung aufnimmst.

Das Feld *Bundle Resources* sollte eine durch Kommas getrennte Liste von Verzeichnissen enthalten. In diesen Verzeichnissen liegen die Ressourcendateien und Ordner, die bei der Bundle-Erstellung unverändert in das resultierende Paket kopiert werden sollen. Die Verzeichnisse müssen mit einem absoluten Pfad vom Projektstamm aus angegeben werden, zum Beispiel `/res`. Das Ressourcenverzeichnis muss Unterordner enthalten, die nach dem Schema `platform` oder `architecture-platform` benannt sind.

Unterstützte Plattformen sind `ios`, `android`, `osx`, `win32`, `linux`, `web`, `switch`. Ein Unterordner namens `common` ist ebenfalls zulässig und enthält Ressourcendateien, die für alle Plattformen gemeinsam verwendet werden. Beispiel:

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

Du kannst [`sys.get_application_path()`](/ref/stable/sys/#sys.get_application_path:) verwenden, um den Pfad zu ermitteln, unter dem die Anwendung gespeichert ist. Verwende diesen Basispfad der Anwendung, um den vollständigen absoluten Pfad zu den Dateien zu bilden, auf die du zugreifen musst. Sobald du den absoluten Pfad dieser Dateien hast, kannst du mit den Funktionen `io.*` und `os.*` auf die Dateien zugreifen.
