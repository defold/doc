---
title: Manifest dell'applicazione
brief: Questo manuale descrive come usare il manifest dell'applicazione per escludere funzionalità dal motore.
---

# Manifest dell'applicazione {#app-manifest}

Il manifest dell'applicazione determina quali funzionalità e backend vengono integrati nel motore. È consigliabile escludere le funzionalità inutilizzate, perché questo riduce le dimensioni finali del file binario del gioco. Il manifest dell'applicazione contiene anche opzioni applicate in fase di build, come le versioni minime dei browser supportate per HTML5 e le impostazioni della memoria WebAssembly.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# Applicazione del manifest {#applying-the-manifest}

In `game.project`, assegna il manifest a `Native Extensions` -> `App Manifest`.

## Physics 2D

Seleziona l'implementazione di Box2D da includere:

* **Box2D Version 3** - Include Box2D 3. Questa opzione deve essere attivata esplicitamente e può produrre risultati di simulazione diversi rispetto all'implementazione precedente, quindi nei progetti esistenti potrebbe essere necessario ricalibrare le impostazioni della fisica.
* **Box2D (Legacy Defold version)** - Include l'implementazione precedente di Box2D di Defold. Questa è l'impostazione predefinita.
* **None** - Esclude la fisica 2D.

Le impostazioni del risolutore di Box2D dipendono dalla versione. Consulta le [impostazioni del progetto per Box2D](/manuals/project-settings/#box2d) per i dettagli.

## Physics 3D

Include l'implementazione della fisica 3D Bullet. È inclusa per impostazione predefinita; disattiva questa impostazione per escludere la fisica 3D.

## Rig + Model

Controlla le funzionalità di rig e modelli, oppure seleziona None per escludere completamente modelli e rig. (Consulta la documentazione di [`Model`](https://defold.com/manuals/model/#model-component)).


## Exclude Record

Esclude dal motore la funzionalità di registrazione video (consulta la documentazione del messaggio [`start_record`](https://defold.com/ref/stable/sys/#start_record)).


## Profiler

Determina quando le funzionalità del profilatore vengono integrate nel motore:

* **Debug Only** - Include il profilatore solo nelle build di debug. Questa è l'impostazione predefinita.
* **None** - Esclude le funzionalità del profilatore da tutte le varianti di build.
* **Always** - Include il profilatore sia nelle build di debug sia in quelle di release.

L'impostazione del manifest dell'applicazione determina se il codice del profilatore viene integrato in una build. Le impostazioni nella sezione `profiler` di *game.project* controllano il comportamento del profilatore durante l'esecuzione. Scopri come usare gli strumenti disponibili nel [manuale sulla profilazione](/manuals/profiling/).


## Sound

Le impostazioni audio determinano quale sistema audio e quali decodificatori vengono integrati nel motore.

### Exclude Sound

Esclude dal motore tutte le funzionalità di riproduzione audio.

### Exclude Sound Decoder: WAV

Esclude il supporto per le risorse audio WAV.

### Exclude Sound Decoder: OGG

Esclude il supporto per le risorse audio Ogg Vorbis.

### Include Sound Decoder: Opus

Include il supporto per le risorse audio Ogg Opus. Il decodificatore Opus è escluso per impostazione predefinita, quindi questa opzione deve essere attivata per poter riprodurre le risorse `.opus`. Consulta il [manuale sull'audio](/manuals/sound/) per i formati supportati.


## Exclude Input

Esclude dal motore tutta la gestione dell'input.


## Exclude GUI

Rimuove dal motore le risorse GUI, i componenti GUI e il relativo supporto Lua. Abilita questa opzione solo se il progetto non usa scene GUI o script GUI. I componenti Label rimangono disponibili. Questa opzione è disabilitata per impostazione predefinita.


## Exclude Particle FX

Rimuove le risorse degli effetti particellari, i relativi componenti e il modulo Lua `particlefx`. Rimuove anche il supporto per i nodi particellari nelle scene GUI; le scene GUI senza nodi particellari rimangono supportate. Prima di abilitare questa opzione, rimuovi i riferimenti agli effetti particellari e le chiamate alle loro API. È disabilitata per impostazione predefinita.


## Exclude Tilemaps

Rimuove le risorse tilemap, i relativi componenti e il modulo Lua `tilemap`. Abilita questa opzione solo se il progetto non usa componenti tilemap o le loro API. Le sorgenti di tile usate da altri componenti rimangono disponibili. Questa opzione è disabilitata per impostazione predefinita.


## Exclude Live Update

Esclude dal motore la [funzionalità Live Update](/manuals/live-update).


## Exclude Image

Esclude dal motore il modulo di script `image` [collegamento](https://defold.com/ref/stable/image/).


## Exclude Types

Esclude dal motore il modulo di script `types` [collegamento](https://defold.com/ref/stable/types/).


## Exclude Basis Transcoder

Esclude dal motore la [libreria di compressione delle texture](/manuals/texture-profiles) Basis Universal.


## Use Android Support Lib

Usa la libreria deprecata Android Support Library al posto di Android X. [Ulteriori informazioni](https://defold.com/manuals/android/#using-androidx).


## Graphics

Seleziona i backend grafici da includere per ciascuna piattaforma. Un'opzione combinata include entrambi i backend, così da poter usare quello alternativo quando il backend preferito non è disponibile.

| Campo | Piattaforme | Opzioni | Predefinito |
|---|---|---|---|
| **Graphics** | Windows e Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

Su Linux ARM64, l'opzione **OpenGL** usa il backend OpenGL ES. L'opzione combinata predefinita per Android preferisce Vulkan quando è disponibile e usa OpenGL ES come alternativa.

## Use full text layout system

Se abilitata (`true`), include il sistema completo di layout del testo per la composizione dei glifi, anche nelle lingue che si scrivono da destra a sinistra. Abilita questa opzione insieme a `font.runtime_generation` in *game.project* per generare a runtime font SDF da risorse TrueType (`.ttf`) o OpenType (`.otf`). La generazione a runtime da risorse `.otf` è supportata da Defold 1.13.2. Per ulteriori informazioni, consulta il [manuale dei font](/manuals/font/#enabling-runtime-fonts).


## Use Rich Text

Include l'analisi del testo formattato e gli effetti di stile per le etichette e il testo GUI. Questa opzione è abilitata per impostazione predefinita. Disabilitala per ridurre le dimensioni del motore quando al progetto serve soltanto testo semplice. Le etichette e il testo GUI rimangono supportati, ma il markup viene visualizzato come testo semplice senza applicare formattazione o effetti.


## Versioni minime dei browser {#minimum-browser-versions}

I campi YAML **`minSafariVersion`**, **`minFirefoxVersion`** e **`minChromeVersion`** specificano le versioni minime dei browser a cui si rivolge Emscripten. I valori predefiniti attuali e le versioni minime supportate differiscono tra le destinazioni senza e con supporto ai thread:

| Destinazione | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Specifica i valori sostitutivi nel contesto della destinazione interessata. La destinazione con supporto ai thread ha anche ulteriori [requisiti di hosting](/manuals/html5/#creating-html5-bundle). Consulta il riferimento delle impostazioni di Emscripten per [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) e [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version).

## Memoria iniziale (HTML5) {#initial-memory-html5}
Nome del campo YAML: **`initialMemory`**
Valore predefinito: **33554432**

La quantità iniziale di memoria allocata per l'applicazione web, in byte. Il valore deve essere un multiplo della dimensione di pagina di WebAssembly (64 KiB). Consulta l'impostazione [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory) di Emscripten.

Questa opzione fornisce il valore predefinito in fase di compilazione. Il valore [`html5.heap_size`](/manuals/html5/#heap-size) in *game.project* lo sostituisce durante l'esecuzione.

## Dimensione dello stack (HTML5) {#stack-size-html5}
Nome del campo YAML: **`stackSize`**
Valore predefinito: **5242880**

La dimensione dello stack dell'applicazione, in byte. Consulta l'impostazione [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size) di Emscripten.
