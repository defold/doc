---
title: Anwendungsmanifest
brief: Dieses Handbuch beschreibt, wie du mit dem Anwendungsmanifest Funktionen aus der Engine ausschließen kannst.
---

# Anwendungsmanifest {#app-manifest}

Das Anwendungsmanifest (app manifest) steuert, welche Funktionen und Backends in die Engine eingebunden werden. Es wird empfohlen, ungenutzte Funktionen auszuschließen, da dadurch die fertige Binärdatei deines Spiels kleiner wird. Das Anwendungsmanifest enthält außerdem Optionen für den Build-Vorgang, etwa die mindestens unterstützten HTML5-Browserversionen und die Speichereinstellungen für WebAssembly.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# Das Manifest anwenden {#applying-the-manifest}

Weise das Manifest in `game.project` unter `Native Extensions` -> `App Manifest` zu.

## Physics 2D

Wähle aus, welche Box2D-Implementierung eingebunden werden soll:

* **Box2D Version 3** - Bindet Box2D 3 ein. Diese Option muss ausdrücklich aktiviert werden und kann andere Simulationsergebnisse liefern als die bisherige Implementierung. Bei bestehenden Projekten musst du daher möglicherweise die Physikeinstellungen neu abstimmen.
* **Box2D (Legacy Defold version)** - Bindet die bisherige Box2D-Implementierung von Defold ein. Dies ist die Standardeinstellung.
* **None** - Schließt die 2D-Physik aus.

Die Einstellungen des Box2D-Solvers sind versionsabhängig. Einzelheiten findest du in den [Box2D-Projekteinstellungen](/manuals/project-settings/#box2d).

## Physics 3D

Bindet die 3D-Physikimplementierung Bullet ein. Sie ist standardmäßig enthalten; deaktiviere diese Einstellung, um die 3D-Physik auszuschließen.

## Rig + Model

Steuere die Funktionalität von Rigs und Modellen (models), oder wähle None aus, um Modelle und Rigs vollständig auszuschließen. (Siehe die Dokumentation zu [`Model`](https://defold.com/manuals/model/#model-component)).


## Exclude Record

Schließt die Videoaufnahmefunktion aus der Engine aus (siehe die Dokumentation zur Nachricht [`start_record`](https://defold.com/ref/stable/sys/#start_record)).


## Profiler

Steuere, wann die Profiler-Funktionalität in die Engine eingebunden wird:

* **Debug Only** - Bindet den Profiler nur in Debug-Builds ein. Dies ist die Standardeinstellung.
* **None** - Schließt die Profiler-Funktionalität aus allen Build-Varianten aus.
* **Always** - Bindet den Profiler sowohl in Debug- als auch in Release-Builds ein.

Die Einstellung im Anwendungsmanifest steuert, ob der Profiler-Code in einen Build eingebunden wird. Die Einstellungen unter `profiler` in *game.project* steuern das Verhalten des Profilers zur Laufzeit. Wie du die verfügbaren Funktionen verwendest, erfährst du im [Profiling-Handbuch](/manuals/profiling/).


## Sound

Die Audioeinstellungen bestimmen, welches Audiosystem und welche Decoder in die Engine eingebunden werden.

### Exclude Sound

Schließt sämtliche Funktionen zur Audiowiedergabe aus der Engine aus.

### Exclude Sound Decoder: WAV

Schließt die Unterstützung für WAV-Audioressourcen aus.

### Exclude Sound Decoder: OGG

Schließt die Unterstützung für Ogg-Vorbis-Audioressourcen aus.

### Include Sound Decoder: Opus

Bindet die Unterstützung für Ogg-Opus-Audioressourcen ein. Der Opus-Decoder ist standardmäßig ausgeschlossen. Du musst diese Option daher aktivieren, bevor `.opus`-Ressourcen wiedergegeben werden können. Die unterstützten Formate findest du im [Audiohandbuch](/manuals/sound/).


## Exclude Input

Schließt die gesamte Eingabeverarbeitung aus der Engine aus.


## Exclude GUI

Entfernt GUI-Ressourcen, Komponenten (components) und die Lua-Unterstützung aus der Engine. Aktiviere diese Option nur, wenn das Projekt keine GUI-Szenen oder GUI-Skripte verwendet. Beschriftungskomponenten (label components) bleiben verfügbar. Diese Option ist standardmäßig deaktiviert.


## Exclude Particle FX

Entfernt Ressourcen und Komponenten für Partikeleffekte (particle effects) sowie das Lua-Modul `particlefx`. Dadurch entfällt auch die Unterstützung für Partikelknoten in GUI-Szenen; GUI-Szenen ohne Partikelknoten werden weiterhin unterstützt. Entferne Referenzen auf Partikeleffekte und Aufrufe ihrer APIs, bevor du diese Option aktivierst. Sie ist standardmäßig deaktiviert.


## Exclude Tilemaps

Entfernt Ressourcen und Komponenten für Kachelkarten (tile maps) sowie das Lua-Modul `tilemap`. Aktiviere diese Option nur, wenn das Projekt keine Kachelkartenkomponenten oder deren APIs verwendet. Kachelquellen, die von anderen Komponenten verwendet werden, bleiben verfügbar. Diese Option ist standardmäßig deaktiviert.


## Exclude Live Update

Schließt die [Live-Update-Funktionalität](/manuals/live-update) aus der Engine aus.


## Exclude Image

Schließt das Skriptmodul `image` aus der Engine aus ([Link](https://defold.com/ref/stable/image/)).


## Exclude Types

Schließt das Skriptmodul `types` aus der Engine aus ([Link](https://defold.com/ref/stable/types/)).


## Exclude Basis Transcoder

Schließt die [Bibliothek zur Texturkomprimierung](/manuals/texture-profiles) Basis Universal aus der Engine aus.


## Use Android Support Lib

Verwendet die veraltete und zur Ablösung vorgesehene Android Support Library anstelle von Android X. [Weitere Informationen](https://defold.com/manuals/android/#using-androidx).


## Graphics

Wähle für jede Plattform aus, welche Grafik-Backends eingebunden werden sollen. Eine kombinierte Auswahl bindet beide Backends ein, sodass auf das andere Backend zurückgegriffen werden kann, wenn das bevorzugte nicht verfügbar ist.

| Feld | Plattformen | Auswahlmöglichkeiten | Standard |
|---|---|---|---|
| **Graphics** | Windows und Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

Unter Linux ARM64 verwendet die Auswahl **OpenGL** das OpenGL-ES-Backend. Die kombinierte Standardeinstellung für Android bevorzugt Vulkan, sofern es verfügbar ist, und greift andernfalls auf OpenGL ES zurück.

## Use full text layout system

Wenn diese Option aktiviert ist (`true`), wird das vollständige Textlayoutsystem für die Textformung eingebunden, einschließlich der Unterstützung für Sprachen, die von rechts nach links geschrieben werden. Aktiviere diese Option zusammen mit `font.runtime_generation` in *game.project*, um SDF-Schriftarten zur Laufzeit aus TrueType- (`.ttf`) oder OpenType-Ressourcen (`.otf`) zu erzeugen. Die Erzeugung zur Laufzeit aus `.otf`-Ressourcen wird seit Defold 1.13.2 unterstützt. Weitere Informationen findest du im [Schriftartenhandbuch](/manuals/font/#enabling-runtime-fonts).


## Use Rich Text

Bindet die Verarbeitung von Rich-Text-Auszeichnungen und Stileffekte für Beschriftungen und GUI-Text ein. Diese Option ist standardmäßig aktiviert. Deaktiviere sie, um die Engine zu verkleinern, wenn das Projekt nur unformatierten Text benötigt. Beschriftungen und GUI-Text werden weiterhin unterstützt, aber Auszeichnungen werden als unformatierter Text gerendert, statt Formatierungen oder Effekte anzuwenden.


## Mindestens unterstützte Browserversionen {#minimum-browser-versions}

Die YAML-Felder **`minSafariVersion`**, **`minFirefoxVersion`** und **`minChromeVersion`** geben die mindestens unterstützten Browserversionen an, auf die Emscripten ausgerichtet ist. Die aktuellen Standardwerte und die mindestens unterstützten Versionen unterscheiden sich zwischen den Zielen ohne und mit Thread-Unterstützung:

| Ziel | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Gib abweichende Werte im Kontext des jeweiligen Ziels an. Für das Ziel mit Thread-Unterstützung gelten außerdem zusätzliche [Hosting-Anforderungen](/manuals/html5/#creating-html5-bundle). Siehe die Emscripten-Einstellungsreferenz für [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) und [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version).

## Anfänglicher Speicher (HTML5) {#initial-memory-html5}
YAML-Feldname: **`initialMemory`**
Standardwert: **33554432**

Die anfänglich für die Webanwendung zugewiesene Speichermenge in Bytes. Der Wert muss ein Vielfaches der WebAssembly-Seitengröße (64 KiB) sein. Siehe die Emscripten-Einstellung [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory).

Diese Option legt den Standardwert zur Kompilierungszeit fest. Der Wert von [`html5.heap_size`](/manuals/html5/#heap-size) in *game.project* überschreibt ihn zur Laufzeit.

## Stack-Größe (HTML5) {#stack-size-html5}
YAML-Feldname: **`stackSize`**
Standardwert: **5242880**

Die Größe des Anwendungs-Stacks in Bytes. Siehe die Emscripten-Einstellung [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size).
