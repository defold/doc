Zasoby pakietu aplikacji to dodatkowe pliki i katalogi dołączane do pakietu za pomocą pola [*Bundle Resources*](/manuals/project-settings/#bundle-resources) w *game.project*.

Pole *Bundle Resources* powinno zawierać listę katalogów rozdzielonych przecinkami. Katalogi te muszą zawierać pliki zasobów i podkatalogi, które podczas tworzenia pakietu zostaną skopiowane bez zmian do wynikowej aplikacji. Katalogi trzeba podawać jako ścieżki bezwzględne, liczone od katalogu głównego projektu, na przykład `/res`. Katalog zasobów musi zawierać podkatalogi nazwane według schematu `platform` albo `architecture-platform`.

Obsługiwane platformy to `ios`, `android`, `osx`, `win32`, `linux`, `web`, `switch`. Dozwolony jest również podkatalog `common`, zawierający pliki zasobów wspólne dla wszystkich platform. Przykład:

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

Możesz użyć [`sys.get_application_path()`](/ref/stable/sys/#sys.get_application_path:) do pobrania ścieżki do katalogu, w którym znajduje się aplikacja. Użyj tej bazowej ścieżki aplikacji, aby zbudować końcową ścieżkę bezwzględną do plików, do których chcesz uzyskać dostęp. Gdy już znasz bezwzględną ścieżkę do tych plików, możesz użyć funkcji `io.*` i `os.*`, aby uzyskać do nich dostęp.
