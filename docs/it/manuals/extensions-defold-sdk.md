---
title: Estensioni native - SDK di Defold
brief: Questo manuale descrive come utilizzare l'SDK di Defold per creare estensioni native.
---

# L'SDK di Defold {#the-defold-sdk}

L'SDK di Defold contiene le funzionalità necessarie per dichiarare un'estensione nativa e per interfacciarsi con lo strato nativo di basso livello della piattaforma su cui viene eseguita l'applicazione e con lo strato Lua di alto livello in cui viene creata la logica di gioco.

## Utilizzo {#usage}

Le estensioni C++ possono includere il file di intestazione aggregato `dmsdk/sdk.h`:

```cpp
#include <dmsdk/sdk.h>
```

Il file di intestazione aggregato include dichiarazioni C++ e non può essere incluso in un file sorgente C. I file sorgente C devono includere i singoli file di intestazione `.h` compatibili con C di cui hanno bisogno, per esempio:

```c
#include <dmsdk/extension/extension.h>
#include <dmsdk/dlib/configfile.h>
#include <dmsdk/resource/resource.h>
```

Attualmente solo una parte di dmSDK dispone di un'interfaccia in C puro; non tutti i sottosistemi C++ hanno un equivalente in C. Le funzioni e i tipi disponibili sono documentati nella [panoramica dell'API C](/ref/overview_defoldc/) e nella [panoramica dell'API C++](/ref/overview_defoldcpp/). I file di intestazione dell'SDK di Defold sono inclusi in un archivio separato `defoldsdk_headers.zip` per ogni [release di Defold su GitHub](https://github.com/defold/defold/releases). Puoi utilizzare questi file di intestazione per il completamento del codice nell'editor che preferisci.
