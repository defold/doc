Le risorse del bundle sono file e cartelle aggiuntivi inclusi nel bundle dell'applicazione tramite il [campo *Bundle Resources*](/manuals/project-settings/#bundle-resources) in *game.project*.

Il campo *Bundle Resources* deve contenere un elenco, separato da virgole, di directory contenenti file e cartelle di risorse da copiare senza modifiche nel pacchetto risultante durante la creazione del bundle. Le directory devono essere specificate con un percorso assoluto a partire dalla radice del progetto, per esempio `/res`. La directory delle risorse deve contenere sottocartelle denominate secondo lo schema `platform` o `architecture-platform`.

Le piattaforme supportate sono `ios`, `android`, `osx`, `win32`, `linux`, `web`, `switch`. È consentita anche una sottocartella denominata `common`, contenente file di risorse comuni a tutte le piattaforme. Esempio:

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

Puoi usare [`sys.get_application_path()`](/ref/stable/sys/#sys.get_application_path:) per ottenere il percorso in cui si trova l'applicazione. Usa questo percorso di base dell'applicazione per costruire il percorso assoluto completo dei file a cui devi accedere. Una volta ottenuto il percorso assoluto di questi file, puoi usare le funzioni `io.*` e `os.*` per accedervi.