---
title: Defold-Projekteinstellungen
brief: Dieses Handbuch beschreibt, wie projektspezifische Einstellungen in Defold funktionieren.
---

# Projekteinstellungen {#project-settings}

Die Datei *game.project* enthält alle projektweiten Einstellungen. Sie muss im Stammordner des Projekts bleiben und *game.project* heißen. Wenn die Engine startet und dein Spiel ausführt, sucht sie zuerst nach dieser Datei.

Jede Einstellung in der Datei gehört zu einer Kategorie. Wenn du die Datei öffnest, zeigt Defold alle Einstellungen nach Kategorien gruppiert an.

![Projekteinstellungen](images/project-settings/settings.jpg)


## Dateiformat {#file-format}

Die Einstellungen in *game.project* werden normalerweise in Defold geändert, die Datei lässt sich aber auch in jedem herkömmlichen Texteditor bearbeiten. Sie folgt dem INI-Dateiformat und sieht so aus:

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

Ein konkretes Beispiel ist:

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

Das bedeutet, dass die Einstellung *main_collection* zur Kategorie *bootstrap* gehört. Wenn du wie im obigen Beispiel eine Dateireferenz verwendest, muss an den Pfad das Zeichen 'c' angehängt werden. Damit verweist du auf die kompilierte Version der Datei. Beachte außerdem, dass der Ordner mit *game.project* das Stammverzeichnis des Projekts ist. Deshalb beginnt der Pfad der Einstellung mit '/'.


## Zugriff zur Laufzeit {#runtime-access}

Du kannst Werte aus *game.project* zur Laufzeit mit [`sys.get_config_string(key)`](/ref/sys/#sys.get_config_string), [`sys.get_config_number(key)`](/ref/sys/#sys.get_config_number), [`sys.get_config_int(key)`](/ref/sys/#sys.get_config_int) und [`sys.get_config_boolean(key)`](/ref/sys/#sys.get_config_boolean) lesen. Beispiele:

```lua
local title = sys.get_config_string("project.title")
local gravity_y = sys.get_config_number("physics.gravity_y")
local fullscreen = sys.get_config_boolean("display.fullscreen", false)
```

::: sidenote
Der Schlüssel setzt sich aus Kategorie und Einstellungsname zusammen, getrennt durch einen Punkt. Er wird kleingeschrieben, und alle Leerzeichen werden durch Unterstriche ersetzt. Beispiele: Aus dem Feld „Title“ der Kategorie „Project“ wird `project.title`, und aus dem Feld „Gravity Y“ der Kategorie „Physics“ wird `physics.gravity_y`.
:::


## Abschnitte und Einstellungen {#sections-and-settings}

Im Folgenden findest du alle verfügbaren Einstellungen, nach Kategorien geordnet.

### Project

#### Title
Der Titel der Anwendung.

#### Version
Die Version der Anwendung.

#### Publisher
Name des Publishers.

#### Developer
Name des Entwicklers.

#### Write Log File
Steuert, wann die Engine eine Protokolldatei schreibt. Optionen:

- "Never": Keine Protokolldatei schreiben.
- "Debug": Eine Protokolldatei nur für Debug-Builds schreiben.
- "Always": Eine Protokolldatei sowohl für Debug- als auch für Release-Builds schreiben.

Wenn du mehr als eine Instanz aus dem Editor ausführst, heißt die Datei *instance_2_log.txt*, wobei `2` der Instanzindex ist. Wenn du eine einzelne Instanz oder ein Bundle ausführst, heißt die Datei *log.txt*. Die Protokolldatei wird unter einem der folgenden Pfade abgelegt, die der Reihe nach versucht werden:

1. Der in *project.log_dir* angegebene Pfad (ausgeblendete Einstellung)
2. Der Systempfad für Protokolle:
  * macOS/iOS: `NSDocumentDirectory`
  * Android: `Context.getExternalFilesDir()`
  * Andere: Stammverzeichnis der Anwendung
3. Der Pfad für Anwendungsunterstützungsdaten
  * macOS/iOS: `NSApplicationSupportDirectory`
  * Windows: `CSIDL_APPDATA` (z. B. `C:\Users\<username>\AppData\Roaming`)
  * Android: `Context.getFilesDir()`
  * Linux: Umgebungsvariable `HOME`

#### Minimum Log Level
Gib die Mindestprotokollstufe für das Protokollierungssystem an. Es werden nur Meldungen dieser oder einer höheren Stufe angezeigt.

#### Compress Archive
Aktiviert die Komprimierung von Archiven bei der Bundle-Erstellung. Beachte, dass dies derzeit für alle Plattformen außer Android gilt, da die APK dort bereits alle Daten komprimiert enthält.

#### Dependencies
Eine Liste der *Library URL*s des Projekts. Weitere Informationen findest du im [Handbuch zu Bibliotheken](/manuals/libraries/).

#### Custom Resources
`custom_resources`
:[Custom Resources](../shared/custom-resources.md)

Das Laden benutzerdefinierter Ressourcen wird im [Handbuch zum Dateizugriff](/manuals/file-access/#how-to-access-files-bundled-with-the-application) genauer beschrieben.

Pfade, die Erweiterungen über `custom_resources.default` in `ext.properties` bereitstellen, werden mit dieser Einstellung kombiniert. Ein Beispiel findest du unter [benutzerdefinierte Ressourcen von Erweiterungen](/manuals/extensions/#custom-resources).

#### Bundle Resources
`bundle_resources`
:[Bundle Resources](../shared/bundle-resources.md)

Das Laden von Bundle-Ressourcen wird im [Handbuch zum Dateizugriff](/manuals/file-access/#how-to-access-files-bundled-with-the-application) genauer beschrieben.

#### Bundle Exclude Resources
`bundle_exclude_resources`
Eine durch Kommas getrennte Liste von Ressourcen, die nicht im Bundle enthalten sein sollen. Sie werden also aus dem Ergebnis des Schritts entfernt, in dem die `bundle_resources` zusammengestellt werden.

---

### Bootstrap

#### Main Collection
Dateireferenz auf die Sammlung (collection), die zum Starten der Anwendung verwendet wird; standardmäßig `/logic/main.collection`.

#### Render
Die zu verwendende Render-Konfigurationsdatei, die die Rendering-Pipeline definiert; standardmäßig `/builtins/render/default.render`.

---

### Library

#### Include Dirs
Eine durch Leerzeichen getrennte Liste von Verzeichnissen, die aus deinem Projekt als Bibliothek freigegeben werden sollen. Weitere Informationen findest du im [Handbuch zu Bibliotheken](/manuals/libraries/).

---

### Script

#### Shared State
Aktiviere diese Option, um einen einzigen Lua-Zustand für alle Skripttypen gemeinsam zu verwenden.

---

### Engine

#### Run While Iconified
Erlaubt der Engine, weiterzulaufen, während das Anwendungsfenster minimiert ist (nur auf Desktop-Plattformen).

#### Fixed Update Frequency
Die Aktualisierungsfrequenz der Lebenszyklusfunktion `fixed_update(self, dt)` in Hertz.

#### Max Time Step
Wenn der Zeitschritt während eines einzelnen Frames zu groß wird, wird er auf diesen Höchstwert begrenzt. Angabe in Sekunden.

---

### Display

#### Width
Die Breite des Anwendungsfensters in Pixeln.

#### Height
Die Höhe des Anwendungsfensters in Pixeln.

#### High Dpi
Erstellt auf unterstützten Bildschirmen einen Backbuffer mit hoher Pixeldichte. Das Spiel wird normalerweise mit der doppelten Auflösung der Einstellungen *Width* und *Height* gerendert. Diese Einstellungen bestimmen weiterhin die logische Auflösung, die in Skripten und Eigenschaften verwendet wird.

#### Samples
Die Anzahl der Samples für die Kantenglättung durch Supersampling. Damit wird der Fensterhinweis `GLFW_FSAA_SAMPLES` gesetzt. Der Wert `0` bedeutet, dass die Kantenglättung ausgeschaltet ist.

Diese Einstellung steuert das Fenster. Außerhalb des Bildschirms gerenderte [Renderziele mit Multisampling](/manuals/render/#multisampled-render-targets) haben eine eigene Sample-Anzahl.

#### Fullscreen
Aktiviere diese Option, wenn die Anwendung im Vollbildmodus starten soll. Ist sie deaktiviert, läuft die Anwendung im Fenstermodus.

#### Update Frequency
Die gewünschte Bildrate in Hertz. Setze den Wert für eine variable Bildrate auf 0. Ein Wert größer als 0 führt zu einer festen Bildrate, die zur Laufzeit auf die tatsächliche Bildrate begrenzt wird (du kannst die Spielschleife also nicht zweimal in einem Engine-Frame aktualisieren). Verwende [`sys.set_update_frequency(hz)`](https://defold.com/ref/stable/sys/?q=set_update_frequency#sys.set_update_frequency:frequency), um diesen Wert zur Laufzeit zu ändern. Diese Einstellung funktioniert auch in Builds ohne grafische Oberfläche (headless).

#### Swap interval
Dieser ganzzahlige Wert steuert, wie die Anwendung mit Vsync umgeht. 0 deaktiviert Vsync, und der Standardwert ist 1. Bei Verwendung eines OpenGL-Adapters legt dieser Wert die Anzahl der Frames fest, die das Fenster [zwischen Pufferwechseln aktualisieren](https://www.khronos.org/opengl/wiki/Swap_Interval) soll. Vulkan hat kein integriertes Konzept eines Wechselintervalls. Der Wert steuert dort stattdessen, ob Vsync aktiviert werden soll.

#### Vsync
Einstellung für die Abwärtskompatibilität. Diese Einstellung ist veraltet und zur Ablösung vorgesehen; verwende für neue Projekte **Swap Interval**. Wenn sie deaktiviert ist, erzwingt sie das tatsächlich verwendete Wechselintervall `0`. Wenn sie aktiviert ist, bestimmt **Swap Interval** den tatsächlichen Wert.

#### Display Profiles
Gibt die zu verwendende Datei mit Anzeigeprofilen an; standardmäßig `/builtins/render/default.display_profilesc`. Weitere Informationen findest du im [Handbuch zu GUI-Layouts](/manuals/gui-layouts/#creating-display-profiles).

#### Dynamic Orientation
Aktiviere diese Option, wenn die App beim Drehen des Geräts dynamisch zwischen Hoch- und Querformat wechseln soll. Beachte, dass die Entwicklungs-App diese Einstellung derzeit nicht berücksichtigt.

#### Display Device Info
Gibt beim Start GPU-Informationen in der Konsole aus.

---

### Render {#render-1}

#### Clear Color Red
Rotkanal der Löschfarbe, verwendet vom Render-Skript und beim Erstellen des Fensters.

#### Clear Color Green
Grünkanal der Löschfarbe, verwendet vom Render-Skript und beim Erstellen des Fensters.

#### Clear Color Blue
Blaukanal der Löschfarbe, verwendet vom Render-Skript und beim Erstellen des Fensters.

#### Clear Color Alpha
Alphakanal der Löschfarbe, verwendet vom Render-Skript und beim Erstellen des Fensters.

---

### Font

#### Runtime Generation
Verwendet die Schriftgenerierung zur Laufzeit.

---

### Physics

#### Max Collision Object Count
Maximale Anzahl der Kollisionsobjekte (collision objects).

#### Type
Die zu verwendende Art der Physik: `2D` oder `3D`.

#### Gravity X
Schwerkraft der Welt entlang der x-Achse. In Metern pro Sekunde.

#### Gravity Y
Schwerkraft der Welt entlang der y-Achse. In Metern pro Sekunde.

#### Gravity Z
Schwerkraft der Welt entlang der z-Achse. In Metern pro Sekunde.

#### Debug
Aktiviere diese Option, wenn die Physik zur Fehlersuche visualisiert werden soll.

#### Debug Alpha
Wert der Alphakomponente für die visualisierte Physik, `0`--`1`.

#### World Count
Maximale Anzahl gleichzeitig vorhandener Physikwelten; standardmäßig `4`. Wenn du über Sammlungs-Proxys (collection proxies) mehr als 4 Welten gleichzeitig lädst, musst du diesen Wert erhöhen. Beachte, dass jede Physikwelt eine beträchtliche Menge Speicher reserviert.

#### Scale
Teilt der Physik-Engine mit, wie sie die Physikwelten im Verhältnis zur Spielwelt skalieren soll, um numerische Genauigkeit zu erreichen: `0.01`--`1.0`. Wenn der Wert auf `0.02` gesetzt ist, behandelt die Physik-Engine 50 Einheiten als 1 Meter ($1 / 0.02$).

#### Allow Dynamic Transforms
Aktiviere diese Option, wenn die Physik-Engine die Transformation eines Spielobjekts (game object) auf alle daran angehängten Komponenten (components) vom Typ Kollisionsobjekt anwenden soll. Damit kannst du Kollisionsformen verschieben, skalieren und drehen, auch dynamische.

#### Use Fixed Timestep
Aktiviere diese Option, wenn die Physik-Engine Aktualisierungen mit festem Zeitschritt unabhängig von der Bildrate verwenden soll. Verwende diese Einstellung zusammen mit der Lebenszyklusfunktion `fixed_update(self, dt)` und der Projekteinstellung `engine.fixed_update_frequency`, um in regelmäßigen Abständen mit der Physik-Engine zu interagieren. Für neue Projekte wird die Einstellung `true` empfohlen.

#### Debug Scale
Die Größe, in der Einheitsobjekte der Physik wie Achsendreibeine und Normalen gezeichnet werden.

#### Max Collisions
Die Anzahl der Kollisionen, die an die Skripte gemeldet werden.

#### Max Contacts
Die Anzahl der Kontaktpunkte, die an die Skripte gemeldet werden.

#### Contact Impulse Limit
Ignoriert Kontaktimpulse, deren Werte unter dieser Einstellung liegen.

#### Ray Cast Limit 2d
Die maximale Anzahl von 2D-Strahlabfragen (raycasts) pro Frame.

#### Ray Cast Limit 3d
Die maximale Anzahl von 3D-Strahlabfragen pro Frame.

#### Trigger Overlap Capacity
Die maximale Anzahl überlappender Physik-Trigger.

#### Velocity Threshold
Mindestgeschwindigkeit, die zu elastischen Kollisionen führt.

#### Max Fixed Timesteps
Maximale Anzahl der Simulationsschritte bei Verwendung eines festen Zeitschritts (nur 3D).

---

### Graphics

#### Default Texture Min Filter
Gibt die Filterung an, die beim Verkleinern verwendet werden soll.

#### Default Texture Mag Filter
Gibt die Filterung an, die beim Vergrößern verwendet werden soll.

#### Max Draw Calls
Die maximale Anzahl der Renderaufrufe.

#### Max Characters:
Die Anzahl der Zeichen, für die im Text-Rendering-Puffer vorab Speicher reserviert wird, also die Anzahl der Zeichen, die pro Frame angezeigt werden können.

#### Max Font Batches
Die maximale Anzahl von Textgruppen für gebündeltes Rendern (Batching), die pro Frame angezeigt werden können.

#### Max Debug Vertices
Die maximale Anzahl der Debug-Vertices. Sie werden unter anderem zum Rendern von Physikformen verwendet.

#### Texture Profiles
Die für dieses Projekt zu verwendende Texturprofildatei; standardmäßig `/builtins/graphics/default.texture_profiles`.

#### Verify Graphics Calls
Prüft den Rückgabewert nach jedem Grafikaufruf und meldet Fehler im Protokoll.

#### WebGL Version Hint
`graphics.webgl_version_hint` wählt die Version des WebGL-Kontexts aus, die für HTML5 angefordert wird. Gültige Werte sind `1` (WebGL 1) und `2` (WebGL 2, der Standardwert). Setze den Wert auf `1`, um WebGL 1 auch in einem Browser als Ziel zu verwenden oder zu testen, der WebGL 2 unterstützt. Lasse [Exclude GLES 2.0](#exclude-gles-20) deaktiviert, wenn du WebGL 1 als Ziel verwendest, damit die erforderlichen Shader enthalten sind.

#### OpenGL Version Hint
Versionshinweis für den OpenGL-Kontext. Wenn eine bestimmte Version ausgewählt ist, wird sie als erforderliche Mindestversion verwendet (gilt nicht für OpenGL ES).

#### OpenGL Core Profile Hint
Setzt beim Erstellen des Kontexts den OpenGL-Profilhinweis 'core'. Das Core-Profil entfernt alle veralteten Funktionen aus OpenGL, etwa das Rendering im Immediate Mode. Gilt nicht für OpenGL ES.

#### Vulkan Version Major
`graphics.vulkan_version_major` ist der Hinweis für die Hauptversion des Vulkan-Kontexts bzw. der Vulkan-API. Dies gilt nur, wenn das Vulkan-Grafik-Backend ausgewählt ist. Der Standardwert ist `1`.

#### Vulkan Version Minor
`graphics.vulkan_version_minor` ist der Hinweis für die Nebenversion des Vulkan-Kontexts bzw. der Vulkan-API. Dies gilt nur, wenn das Vulkan-Grafik-Backend ausgewählt ist. Der Standardwert ist `0`.

---

### Shader

#### Exclude GLES 2.0
Kompiliert keine Shader für Geräte, auf denen OpenGLES 2.0 / WebGL 1.0 läuft.

#### GLSL ES Default Precision Float
`shader.glsl_es_default_precision_float` legt den standardmäßigen globalen Genauigkeitsqualifizierer für Gleitkommawerte in nach GLSL ES querkompilierten Shadern fest. Gültige Werte sind `mediump` und `highp`; der Standardwert ist `mediump`.

#### GLSL ES Default Precision Int
`shader.glsl_es_default_precision_int` legt den standardmäßigen globalen Genauigkeitsqualifizierer für Ganzzahlwerte in nach GLSL ES querkompilierten Shadern fest. Gültige Werte sind `mediump` und `highp`; der Standardwert ist `highp`.

---

### Input

#### Repeat Delay
Die Wartezeit in Sekunden, bevor eine gedrückt gehaltene Eingabe wiederholt wird.

#### Repeat Interval
Die Wartezeit in Sekunden zwischen den Wiederholungen einer gedrückt gehaltenen Eingabe.

#### Gamepads
Dateireferenz auf die Gamepad-Konfigurationsdatei, die Gamepad-Signale dem Betriebssystem zuordnet; standardmäßig `/builtins/input/default.gamepads`.

#### Game Binding
Dateireferenz auf die Eingabekonfigurationsdatei, die Hardwareeingaben Aktionen zuordnet; standardmäßig `/input/game.input_binding`.

#### Use Accelerometer
Aktiviere diese Option, damit die Engine in jedem Frame Eingabeereignisse des Beschleunigungssensors empfängt. Das Deaktivieren dieser Eingabe kann die Leistung etwas verbessern.

---

### Resource

#### Http Cache
Wenn diese Option aktiviert ist, wird ein HTTP-Cache verwendet, um Ressourcen über das Netzwerk schneller in die laufende Engine auf dem Gerät zu laden.

#### Uri
Der Speicherort der Build-Daten des Projekts im URI-Format.

#### Max Resources
Die maximale Anzahl der Ressourcen, die gleichzeitig geladen werden können.

---

### Network

#### Http Timeout
Das HTTP-Zeitlimit in Sekunden. Setze den Wert auf `0`, um das Zeitlimit zu deaktivieren.

#### Http Thread Count
Die Anzahl der Arbeitsthreads für den HTTP-Dienst.

#### Http Cache Enabled
Aktiviere diese Option, um den HTTP-Cache für Netzwerkanfragen mit `http.request()` zu verwenden. Der HTTP-Cache speichert die zu einer Anfrage gehörende Antwort und verwendet sie für nachfolgende Anfragen wieder. Er unterstützt die HTTP-Antwortheader `ETag` und `Cache-Control: max-age`.

#### SSL Certificates
Datei mit SSL-Stammzertifikaten, die beim Überprüfen der Zertifikatskette während SSL-Handshakes verwendet werden sollen.

---

### Collection

#### Max Instances
Maximale Anzahl der Spielobjektinstanzen in einer Sammlung; standardmäßig `1024`. [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

#### Max Input Stack Entries
Maximale Anzahl der Spielobjekte im Eingabestapel.

---

### Sound

#### Gain
Globaler Verstärkungsfaktor (Lautstärke), `0`--`1`.

#### Use Linear Gain
Wenn diese Option aktiviert ist, ist der Verstärkungsfaktor linear. Andernfalls wird eine Exponentialkurve verwendet.

#### Max Sound Data
Maximale Anzahl der Audioressourcen, also die Anzahl unterschiedlicher Audiodateien zur Laufzeit.

#### Max Sound Buffers
(Derzeit nicht verwendet) Maximale Anzahl gleichzeitig vorhandener Audiopuffer.

#### Max Sound Sources
(Derzeit nicht verwendet) Maximale Anzahl gleichzeitig wiedergegebener Klänge.

#### Max Sound Instances
Maximale Anzahl gleichzeitig vorhandener Audioinstanzen, also tatsächlich gleichzeitig wiedergegebener Klänge.

#### Max Component Count
Maximale Anzahl der Audiokomponenten pro Sammlung.

#### Sample Frame Count
Anzahl der Samples, die für jede Audioaktualisierung verwendet werden. 0 bedeutet automatisch (1024 für 48 kHz, 768 für 44,1 kHz).

#### Use Thread
Wenn diese Option aktiviert ist, verwendet das Audiosystem Threads für die Audiowiedergabe, um das Risiko von Aussetzern bei hoher Auslastung des Hauptthreads zu verringern.

#### Stream Enabled
Wenn diese Option aktiviert ist, verwendet das Audiosystem Streaming, um Quelldateien zu laden.

#### Stream Cache Size
Die maximale Größe des Audio-Chunk-Caches, der _alle_ Chunks enthält. Standardmäßig `2097152` Byte.
Diese Zahl sollte größer sein als die Anzahl der geladenen Audiodateien multipliziert mit der Stream-Chunk-Größe.
Andernfalls besteht das Risiko, dass neue Chunks in jedem Frame aus dem Cache verdrängt werden.

#### Stream Chunk Size
Die Größe jedes gestreamten Chunks in Byte.

#### Stream Preload Size
Bestimmt die Größe des ersten Chunks in Byte für Audiodateien, die aus dem Archiv gelesen werden.

---

### Sprite

#### Max Count
Maximale Anzahl der Sprites pro Sammlung. [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

#### Subpixels
Aktiviere diese Option, damit Sprites ohne Ausrichtung am Pixelraster erscheinen können.

---

### Tilemap

#### Max Count {#max-count-1}
Maximale Anzahl der Kachelkarten (tile maps) pro Sammlung. [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

#### Max Tile Count
Maximale Anzahl gleichzeitig sichtbarer Kacheln pro Sammlung.

---

### Spine

#### Max Count {#max-count-2}
Maximale Anzahl der Spine-Modellkomponenten. [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

---

### Mesh

#### Max Count {#max-count-3}
Maximale Anzahl der Mesh-Komponenten pro Sammlung. [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

---

### Model

#### Max Count {#max-count-4}
Maximale Anzahl der Modellkomponenten pro Sammlung. [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

#### Split Meshes
Teilt Meshes mit mehr als 65536 Vertices in neue Meshes auf.

#### Max Bone Matrix Texture Width
Maximale Breite der Knochenmatrixtextur. Es wird nur die für Animationen benötigte Größe verwendet, aufgerundet auf die nächste Zweierpotenz.

#### Max Bone Matrix Texture Height
Maximale Höhe der Knochenmatrixtextur. Es wird nur die für Animationen benötigte Größe verwendet, aufgerundet auf die nächste Zweierpotenz.

---

### GUI

#### Max Count {#max-count-5}
Maximale Anzahl der GUI-Komponenten. [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

#### Max Particle Count
Die maximale Anzahl gleichzeitig vorhandener Partikel in der GUI.

#### Max Animation Count
Die maximale Anzahl aktiver Animationen in der GUI.

---

### Label

#### Max Count {#max-count-6}
Maximale Anzahl der Beschriftungskomponenten (labels). [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

#### Subpixels {#subpixels-1}
Aktiviere diese Option, damit Beschriftungen ohne Ausrichtung am Pixelraster erscheinen können.

---

### Particle FX

#### Max Count {#max-count-7}
Die maximale Anzahl gleichzeitig vorhandener Emitter. [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

#### Max Particle Count {#max-particle-count-1}
Die maximale Anzahl gleichzeitig vorhandener Partikel.

---

### Box2D

#### Velocity Iterations
Anzahl der Geschwindigkeitsiterationen für den Physik-Solver von Box2D 2.2.

#### Position Iterations
Anzahl der Positionsiterationen für den Physik-Solver von Box2D 2.2.

#### Sub Step Count
Anzahl der Teilschritte für den Physik-Solver von Box2D 3.x.

---

### Collection proxy

#### Max Count {#max-count-8}
Maximale Anzahl der Sammlungs-Proxys. [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

---

### Collection factory

#### Max Count {#max-count-9}
Maximale Anzahl der Sammlungsfabriken (collection factories). [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

---

### Factory

#### Max Count {#max-count-10}
Maximale Anzahl der Fabriken (factories) für Spielobjekte. [(Siehe Informationen zur Optimierung der maximalen Komponentenanzahl)](#component-max-count-optimizations).

---

### iOS

#### App Icon 57x57--180x180
Bilddatei (.png), die als Anwendungssymbol mit den angegebenen Maßen für Breite und Höhe `W` &times; `H` verwendet werden soll.

#### Launch Screen
Storyboard-Datei (.storyboard). Wie du eine solche Datei erstellst, erfährst du im [iOS-Handbuch](/manuals/ios/#creating-a-storyboard).

#### Icons Asset
Die Symbol-Asset-Datei (.car), die die App-Symbole enthält.

#### Prerendered Icons
(iOS 6 und früher) Aktiviere diese Option, wenn deine Symbole vorgerendert sind. Ist sie deaktiviert, wird den Symbolen automatisch ein Glanzeffekt hinzugefügt.

#### Bundle Identifier
Anhand der Bundle-ID erkennt iOS Aktualisierungen deiner App. Deine Bundle-ID muss bei Apple registriert und für deine App eindeutig sein. Du kannst nicht dieselbe Kennung für iOS- und macOS-Apps verwenden. Sie muss aus zwei oder mehr durch einen Punkt getrennten Segmenten bestehen. Jedes Segment muss mit einem Buchstaben beginnen. Jedes Segment darf nur alphanumerische Zeichen, Unterstriche oder Bindestriche (-) enthalten (siehe [`CFBundleIdentifier`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)).

#### Bundle Name
Der Kurzname des Bundles (15 Zeichen) (siehe [`CFBundleName`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)).

#### Bundle Version
Die Version des Bundles, entweder eine Zahl oder x.y.z. (siehe [`CFBundleVersion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)).

#### Info.plist
Wenn angegeben, wird diese Datei *`Info.plist`* bei der Bundle-Erstellung für deine App anstelle des integrierten iOS-Basismanifests verwendet. Das integrierte Manifest enthält die Einträge für das lokale Netzwerk und Bonjour, die zur Zielerkennung des Editors in Builds erforderlich sind, die keine Release-Builds sind. Wenn du ein benutzerdefiniertes Manifest bereitstellst und auf einem Gerät Zielerkennung, Profiling, Hot Reload oder Protokollstreaming benötigst, behalte diese Einträge wie im [iOS-Handbuch](/manuals/ios/#creating-an-ios-application-bundle) beschrieben bei.

#### Privacy Manifest
Das Apple-Datenschutzmanifest für die Anwendung. Der Standardwert des Felds ist `/builtins/manifests/ios/PrivacyInfo.xcprivacy`.

#### Custom Entitlements
Wenn angegeben, werden die Berechtigungen im bereitgestellten Bereitstellungsprofil (`.entitlements`, `.xcent`, `.plist`) mit den Berechtigungen aus dem Bereitstellungsprofil zusammengeführt, das bei der Bundle-Erstellung für die Anwendung angegeben wird.

#### Default Language
Die Sprache, die verwendet wird, wenn die vom Benutzer bevorzugte Sprache nicht in der Liste `Localizations` der Anwendung enthalten ist (siehe [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Verwende den zweibuchstabigen Standard ISO 639-1, wenn die bevorzugte Sprache darin verfügbar ist, andernfalls den dreibuchstabigen Standard ISO 639-2.

#### Localizations
Dieses Feld enthält durch Kommas getrennte Zeichenfolgen, die den Sprachnamen oder das ISO-Sprachkürzel der unterstützten Lokalisierungen angeben (siehe [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Android

#### App Icon 36x36--192x192
Bilddatei (.png), die als Anwendungssymbol mit den angegebenen Maßen für Breite und Höhe `W` &times; `H` verwendet werden soll.

#### Push Icon Small--LargeXxxhdpi
Bilddateien (.png), die als benutzerdefinierte Symbole für Push-Benachrichtigungen unter Android verwendet werden sollen. Die Symbole werden automatisch sowohl für lokale als auch für entfernte Push-Benachrichtigungen verwendet. Wenn keine angegeben sind, wird standardmäßig das Anwendungssymbol verwendet.

#### Push Field Title
Gibt an, welches JSON-Feld der Nutzdaten als Titel der Benachrichtigung verwendet werden soll. Wenn du diese Einstellung leer lässt, wird standardmäßig der Anwendungsname als Titel der Push-Benachrichtigungen verwendet.

#### Push Field Text
Gibt an, welches JSON-Feld der Nutzdaten als Benachrichtigungstext verwendet werden soll. Wenn du die Einstellung leer lässt, wird wie unter iOS der Text aus dem Feld `alert` verwendet.

#### Version Code
Ein ganzzahliger Wert, der die Version der App angibt. Erhöhe diesen Wert bei jeder weiteren Aktualisierung.

#### Minimum SDK Version
Das niedrigste API-Level, das zum Ausführen der Anwendung erforderlich ist (`android:minSdkVersion`).

#### Target SDK Version
Das API-Level, auf das die Anwendung ausgerichtet ist (`android:targetSdkVersion`).

#### Package
Paketkennung. Sie muss aus zwei oder mehr durch einen Punkt getrennten Segmenten bestehen. Jedes Segment muss mit einem Buchstaben beginnen. Jedes Segment darf nur alphanumerische Zeichen oder Unterstriche enthalten.

#### GCM Sender Id
Die Sender-ID für Google Cloud Messaging. Setze diesen Wert auf die von Google zugewiesene Zeichenfolge, um Push-Benachrichtigungen zu aktivieren.

#### FCM Application Id
Die Anwendungs-ID für Firebase Cloud Messaging.

#### Manifest
Wenn gesetzt, wird bei der Bundle-Erstellung die angegebene XML-Datei als Android-Manifest verwendet. Ein benutzerdefiniertes Manifest ersetzt das integrierte Basismanifest von Defold. Manifestfragmente nativer Erweiterungen werden weiterhin damit zusammengeführt, spätere Änderungen am integrierten Basismanifest werden jedoch nicht automatisch übernommen. Vergleiche benutzerdefinierte Manifeste deshalb bei einem Upgrade mit dem aktuellen integrierten Manifest. Setze bei Spielen `android:appCategory="game"` am Element `<application>`. Setze `android:appCategory` bei Anwendungen, die keine Spiele sind, nur dann, wenn eine der von Android definierten [Anwendungskategorien](https://developer.android.com/guide/topics/manifest/application-element#appCategory) die App zutreffend beschreibt.

#### Iap Provider
Gibt den zu verwendenden Store an. Gültige Optionen sind `Amazon` und `GooglePlay`. Weitere Informationen findest du unter [extension-iap](/extension-iap/).

#### Input Method
Gibt die Methode an, mit der Tastatureingaben auf Android-Geräten erfasst werden. Gültige Optionen sind `KeyEvent` (alte Methode) und `HiddenInputField` (neue Methode).

#### Immersive Mode
Wenn gesetzt, werden die Navigations- und Statusleisten ausgeblendet, und deine App kann alle Berührungsereignisse auf dem Bildschirm erfassen.

#### Display Cutout
Erweitert die Darstellung bis in den Bereich der Bildschirmaussparung.

#### Debuggable
Gibt an, ob sich die Anwendung mit Werkzeugen wie [GAPID](https://github.com/google/gapid) oder [Android Studio](https://developer.android.com/studio/profile/android-profiler) debuggen lässt. Dies setzt das Flag `android:debuggable` im Android-Manifest ([offizielle Dokumentation](https://developer.android.com/guide/topics/manifest/application-element#debug)).

#### R8 Keep Rules
`android.r8_keep_rules` wählt eine `.keep`-Datei aus, um die Verkleinerung, Optimierung und Verschleierung von Java-Code mit R8 in Android-Builds zu aktivieren. Lasse die Einstellung leer, um D8 ohne Verkleinerung zu verwenden.

Wähle `/builtins/manifests/android/dmengine.keep`, um die Standardregeln von Defold direkt zu verwenden. Erweiterungen liefern eigene [Regeln zum Beibehalten von Code](/manuals/extensions/#r8-keep-rules-for-android), die mit dieser Datei kombiniert werden.

Kopiere die integrierte Datei nur dann in dein Projekt, wenn du projektspezifische Regeln hinzufügen musst. Behalte die integrierten Regeln in der Kopie bei: Die Auswahl einer benutzerdefinierten Datei ersetzt den gesamten Regelsatz des Projekts.

Im [Android-Handbuch](/manuals/android/#shrinking-java-code-with-r8) erfährst du, wie du R8 aktivierst und seine Zuordnung der verschleierten Namen zusammen mit einem Release-Bundle aufbewahrst.

#### Extract Native Libraries
Gibt an, ob das Paketinstallationsprogramm native Bibliotheken aus der APK in das Dateisystem extrahiert. Wenn der Wert auf `false` gesetzt ist, werden deine nativen Bibliotheken unkomprimiert in der APK gespeichert. Obwohl deine APK dadurch größer sein kann, lädt deine Anwendung schneller, weil die Bibliotheken zur Laufzeit direkt aus der APK geladen werden. Dies setzt das Flag `android:extractNativeLibs` im Android-Manifest ([offizielle Dokumentation](https://developer.android.com/guide/topics/manifest/application-element#extractNativeLibs)).

---

### macOS

#### App Icon
Bundle-Symboldatei (.icns), die unter macOS als Anwendungssymbol verwendet werden soll.

#### Info.plist {#infoplist-1}
Wenn gesetzt, wird bei der Bundle-Erstellung die angegebene Datei info.plist verwendet.

#### Privacy Manifest {#privacy-manifest-1}
Das Apple-Datenschutzmanifest für die Anwendung. Der Standardwert des Felds ist `/builtins/manifests/osx/PrivacyInfo.xcprivacy`.

#### Bundle Identifier {#bundle-identifier-1}
Anhand der Bundle-ID erkennt macOS Aktualisierungen deiner App. Deine Bundle-ID muss bei Apple registriert und für deine App eindeutig sein. Du kannst nicht dieselbe Kennung für iOS- und macOS-Apps verwenden. Sie muss aus zwei oder mehr durch einen Punkt getrennten Segmenten bestehen. Jedes Segment muss mit einem Buchstaben beginnen. Jedes Segment darf nur alphanumerische Zeichen, Unterstriche oder Bindestriche (-) enthalten.

#### Default Language {#default-language-1}
Die Sprache, die verwendet wird, wenn die vom Benutzer bevorzugte Sprache nicht in der Liste `Localizations` der Anwendung enthalten ist (siehe [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Verwende den zweibuchstabigen Standard ISO 639-1, wenn die bevorzugte Sprache darin verfügbar ist, andernfalls den dreibuchstabigen Standard ISO 639-2.

#### Localizations {#localizations-1}
Dieses Feld enthält durch Kommas getrennte Zeichenfolgen, die den Sprachnamen oder das ISO-Sprachkürzel der unterstützten Lokalisierungen angeben (siehe [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Windows

#### App Icon {#app-icon-1}
Bilddatei (.ico), die unter Windows als Anwendungssymbol verwendet werden soll. Wie du eine .ico-Datei erstellst, erfährst du im [Windows-Handbuch](/manuals/windows).

---

### HTML5

Weitere Informationen zu vielen dieser Optionen findest du im [Handbuch zur HTML5-Plattform](/manuals/html5/).

#### Heap Size
Die Heap-Größe in Megabyte, die Emscripten verwenden soll.

#### .html Shell
Verwendet bei der Bundle-Erstellung die angegebene HTML-Vorlagendatei. Standardmäßig `/builtins/manifests/web/engine_template.html`.

#### Custom .css
Verwendet bei der Bundle-Erstellung die angegebene CSS-Datei für das Design. Standardmäßig `/builtins/manifests/web/light_theme.css`.

#### Splash Image
Wenn gesetzt, wird bei der Bundle-Erstellung das angegebene Startbild für die Anzeige beim Start anstelle des Defold-Logos verwendet.

#### Archive Location Prefix
Bei der Bundle-Erstellung für HTML5 werden die Spieldaten in eine oder mehrere Archivdatendateien aufgeteilt. Wenn die Engine das Spiel startet, werden diese Archivdateien in den Speicher eingelesen. Verwende diese Einstellung, um den Speicherort der Daten anzugeben.

#### Archive Location Suffix
Suffix, das an die Archivdateien angehängt wird. Dies ist beispielsweise nützlich, um Inhalte von einem CDN zu erzwingen, die nicht aus dem Cache stammen (zum Beispiel mit `?version2`).

#### Engine Arguments
Liste der Argumente, die an die Engine übergeben werden.

#### Wasm Streaming
Aktiviert das Streaming der wasm-Datei (schneller und mit geringerem Speicherverbrauch, erfordert jedoch den MIME-Typ `application/wasm`).

#### Show Fullscreen Button
Aktiviert die Schaltfläche Fullscreen in der Datei `index.html`.

#### Show Made With Defold
Aktiviert den Link Made With Defold in der Datei `index.html`.

#### Show Console Banner
Wenn diese Option aktiviert ist, werden beim Start der Engine Informationen über die Engine und ihre Version in der Browserkonsole ausgegeben (mit `console.log()`).

#### Scale Mode
Gibt die Methode an, mit der die Zeichenfläche des Spiels skaliert werden soll.

#### Retry Count
Die Anzahl der Wiederholungsversuche nach einem fehlgeschlagenen Download beim Start, einschließlich Netzwerkfehlern, HTTP-Fehlerstatus und Größenabweichungen bei der JavaScript- oder WebAssembly-Datei der Engine. Die erste Anfrage zählt separat. Für die Überprüfung der Archivdateien gilt eine eigene Höchstzahl an Wiederholungsversuchen; siehe [Download-Überprüfung](/manuals/html5/#download-verification) und `Retry Time`.

#### Retry Time
Die Wartezeit in Sekunden zwischen Versuchen, eine Datei herunterzuladen, wenn der Download fehlgeschlagen ist (siehe `Retry Count`).

#### Verify Downloaded File Size
`html5.verify_downloaded_file_size` prüft heruntergeladene Engine- und Archivdateien auf ihre erwarteten Größen. Standardmäßig aktiviert (`true`). Setze den Wert nur dann auf `false`, wenn ein Server, Proxy oder CDN Dateien absichtlich umschreibt und ihre Größen ändert. Eine fehlgeschlagene Überprüfung führt zu erneuten Download-Versuchen, bevor der Start fehlschlägt. Für Engine-Downloads und die Überprüfung von Archivdateien gelten unterschiedliche Höchstzahlen an Wiederholungsversuchen; siehe [Download-Überprüfung](/manuals/html5/#download-verification).

#### Transparent Graphics Context
Aktiviere diese Option, wenn der Grafikkontext einen transparenten Hintergrund haben soll.

---

### IAP

#### Auto Finish Transactions
Aktiviere diese Option, um IAP-Transaktionen automatisch abzuschließen. Ist sie deaktiviert, musst du nach einer erfolgreichen Transaktion ausdrücklich `iap.finish()` aufrufen.

---

### Live update

#### Settings
Die Ressourcendatei mit Live-Update-Einstellungen, die bei der Bundle-Erstellung verwendet werden soll.

---

### Native extension

#### _App Manifest_
Wenn gesetzt, wird das Anwendungsmanifest verwendet, um den Engine-Build anzupassen. Damit kannst du ungenutzte Teile aus der Engine entfernen, um die Größe der fertigen Binärdatei zu verringern. Wie du ungenutzte Funktionen ausschließt, erfährst du [im Handbuch zum Anwendungsmanifest](/manuals/app-manifest).

---

### Profiler

Die Einstellung **Profiler** im Anwendungsmanifest steuert, ob Profiler-Code in Debug- und Release-Builds gelinkt wird. Die folgenden Einstellungen steuern das Laufzeitverhalten des Profiler-Codes, der im ausgewählten Build enthalten ist. Einzelheiten findest du im [Handbuch zum Profiling](/manuals/profiling/).

#### Enabled
Aktiviert den Profiler im Spiel.

#### Track Cpu
Das Sampling der CPU-Auslastung ist in Debug-Builds standardmäßig aktiviert. Aktiviere diese Einstellung, wenn CPU-Sampling auch in einem Release-Build benötigt wird, der über das Anwendungsmanifest Profiler-Unterstützung enthält.

#### Sleep Between Server Updates
Die Wartezeit in Millisekunden zwischen Serveraktualisierungen.

#### Performance Timeline Enabled
Aktiviert die Leistungszeitleiste im Browser (nur HTML5).

#### Max Sample Count
`profiler.max_sample_count` ist die maximale Anzahl der Profiler-Samples, die pro Thread und Frame aufgezeichnet werden. Der Standardwert ist `4096` und der Mindestwert `128`. Erhöhe diesen Wert nur, wenn ein gültiges Profil das Limit überschreitet. Prüfe zuvor den Profiling-Code nativer Erweiterungen auf nicht zusammenpassende Aufrufe zum Beginn und Ende von Messbereichen.

---

## Konfigurationswerte beim Start der Engine setzen {#setting-config-values-on-engine-startup}

Beim Start der Engine kannst du über die Befehlszeile Konfigurationswerte angeben, die die Einstellungen aus *game.project* überschreiben:

```bash
# Specify a bootstrap collection
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# Set two custom config values
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=foobar
```

Benutzerdefinierte Werte kannst du wie jeden anderen Konfigurationswert mit der passenden Funktion lesen, die unter [Zugriff zur Laufzeit](#runtime-access) beschrieben ist:

```lua
local my_value = sys.get_config_number("test.my_value")
local my_value2 = sys.get_config_string("test.my_value2")
local my_flag = sys.get_config_boolean("test.my_flag", false)
```


:[Component max count optimizations](../shared/component-max-count-optimizations.md)


## Benutzerdefinierte Projekteinstellungen {#custom-project-settings}

Du kannst benutzerdefinierte Einstellungen für das Hauptprojekt oder für eine [native Erweiterung](/manuals/extensions/) definieren. Benutzerdefinierte Einstellungen für das Hauptprojekt müssen in einer Datei `game.properties` im Stammverzeichnis des Projekts definiert werden. Dateien namens `ext.properties` werden überall im Projekt und in abgerufenen Bibliotheksabhängigkeiten erkannt; sie benötigen keine benachbarte Datei `ext.manifest`. Alle gefundenen Erweiterungsmetadaten werden zusammengeführt. Anschließend wird die Datei `game.properties` aus dem Stammverzeichnis angewendet und kann diese Metadaten überschreiben.

Die Einstellungsdatei verwendet dasselbe INI-Format wie *game.project*, und Eigenschaftsattribute werden mit einer Punktnotation und einem Suffix definiert:

```
[my_category]
my_property.private = 1
...
```

Die Standardmetadatei, die immer angewendet wird, ist [hier](https://github.com/defold/defold/blob/dev/com.dynamo.cr/com.dynamo.cr.bob/src/com/dynamo/bob/meta.properties) verfügbar.

Die folgenden Attribute sind derzeit verfügbar:

```
[my_extension]
// `type` - used for the value string parsing
my_property.type = string // one of the following values: bool, string, number, integer, string_array, resource

// `help` - displayed as a help tooltip in the editor
my_property.help = string

// `default` - value used as default if user didn't set value manually
my_property.default = string

// `private` - private value used during the bundle process but will be removed from the bundle itself
my_property.private = 1 // boolean value 1 or 0

// `label` - editor input label
my_property.label = My Awesome Property

// `minimum` and/or `maximum` - valid range for numeric properties, validated in the editor UI
my_property.minimum = 0
my_property.maximum = 255

// `options` - drop-down choices for the editor UI, comma-separated value[:label] pairs
my_property.options = android: Android, ios: iOS

// `resource` type only:
my_property.filter = jpg,png // allowed file extensions for resource selector dialog
my_property.preserve-extension = 1 // use original resource extension instead of a built one

// deprecation
my_property.deprecated = 1 // mark property as deprecated
my_property.severity-default = warning // if deprecated property is specified, but set to a default value
my_property.severity-override = error  // if deprecated property is specified and set to a non-default value

```
Zusätzlich kannst du die folgenden Attribute für eine Einstellungskategorie setzen:
```
[my_extension]
// `group` - game.project category group, e.g. Main, Platforms, Components, Runtime, Distribution
group = Runtime
// `title` - displayed category title
title = My Awesome Extension
// `help` - displayed category help
help = Settings for My Awesome Extension
```


Sowohl Bob als auch der Editor lesen diese Metadatendateien ein. Der Editor verwendet sie, um die entsprechenden Felder, Auswahlmöglichkeiten, Validierungen und Hilfe-Tooltips in der Ansicht für *game.project* zu erstellen.
