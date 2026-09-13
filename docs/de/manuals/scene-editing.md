---
title: Der Szeneneditor von Defold
brief: Im Szeneneditor bearbeitest du Sammlungen, Spielobjekte, GUIs, Partikeleffekte und andere visuelle Assets. Dieses Handbuch erklärt die Auswahl, die Werkzeuge und die Navigation in der Szenenansicht in 2D und 3D – einschließlich des freien Kameramodus und der Kameraeinstellungen.
---

# Der Szeneneditor von Defold {#the-defold-scene-editor}

Der **Szeneneditor** (Scene Editor) ist der visuelle Editor zum Erstellen und Bearbeiten von Szenen wie Sammlungen (collection), Spielobjekten (game object) und anderen visuellen Assets.

Die anfängliche Kameraansicht hängt von der Ressource ab. 3D-Ressourcen wie Modelle und glTF-Szenen verwenden standardmäßig eine **perspektivische** Ansicht, während 2D-Ressourcen wie Sprites, Kachelkarten (tile map) und GUI-Szenen standardmäßig eine **orthografische** Ansicht verwenden. Du kannst die Kameraausrichtung, die Projektion und das Raster über die Werkzeugleiste der Szene ändern.

## Den Szeneneditor öffnen {#opening-the-scene-editor}

Öffne den Szeneneditor durch einen Doppelklick auf eine visuelle Ressource im Bereich *Assets*, zum Beispiel:

- **Szenenstruktur** — Sammlungen (`.collection`), Spielobjekte (`.go`)
- **2D-Assets** — Atlas (`.atlas`), Kachelkarten (`.tilemap`), Sprites (`.sprite`), Kachelquellen (`.tilesource`)
- **3D-Assets** — Modelle (`.model`, `.glb`, `.gltf`)
- **UI** — GUI-Szenen (`.gui`)
- **Effekte** — Partikeleffekte (`.particlefx`)
- Und weitere

## Gespeicherte Szenenansichten {#remembered-scene-views}

Der Editor speichert den Kamerazustand für jede Szenenressource, wenn deren Registerkarte geschlossen oder der Editor beendet wird. Beim erneuten Öffnen derselben Ressource wird ihre Ansicht wiederhergestellt. So können verschiedene Sammlungen oder Modelle unterschiedliche Kamerapositionen, Ausrichtungen und Projektionen beibehalten.

Sichtbarkeitsfilter werden ebenfalls für jede Szene gespeichert. Wenn du Modelle oder Hilfslinien für Komponenten (component) in einer Szene ausblendest, musst du in einer anderen Szene nicht dieselben Filter verwenden. Dies sind Ansichtseinstellungen des Editors; sie ändern weder die Kamera des Spiels noch die Sichtbarkeit zur Laufzeit.

Bei Ressourcen ohne gespeicherten Kamerazustand starten Modell-, Mesh- und glTF-Ressourcen mit einer perspektivischen Ansicht. Die Ansicht von Kollisionsobjekten richtet sich nach der Einstellung für 2D-/3D-Physik des Projekts; Sammlungen und Spielobjekte wählen ihre anfängliche Ansicht anhand ihrer Szenengeometrie.

## Navigation in der Szenenansicht (Kamerasteuerung) {#scene-view-navigation-camera-controls}

Die Kamera des Szeneneditors lässt sich mit Maus und Tastatur steuern. Die verfügbaren Steuerelemente hängen davon ab, ob du die normale Kameranavigation oder den **freien Kameramodus** (Free Camera Mode) verwendest.

### Normale Navigation (alle visuellen Editoren) {#standard-navigation-all-visual-editors}

Diese Steuerelemente stehen in visuellen Editoren zur Verfügung:

- **Verschieben**
  - <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Vergrößern und verkleinern**
  - <kbd>Mouse Wheel</kbd> oder
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Um die Auswahl drehen/kreisen (3D)**
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Left Mouse Button</kbd>

Du kannst auch **Frame Selection** (<kbd>F</kbd>) verwenden, um die Kamera auf die aktuelle Auswahl auszurichten.

## Szenenausrichtung in 2D und 3D {#2d-and-3d-scene-orientation}

Du kannst die Szenenansicht sowohl für die Arbeit in 2D als auch in 3D verwenden:

- In **2D** arbeitest du normalerweise in einer orthografischen Ansicht mit einem für 2D ausgerichteten Raster.
- In **3D** gehst du normalerweise so vor:
  - Du richtest die Ansicht für 3D neu aus,
  - verwendest eine **perspektivische** Kamera,
  - wählst eine geeignete Rasterebene (häufig **Y** für den „Boden“).

Diese Funktionen erreichst du über die Werkzeugleiste und das Menü **View**.

![Szeneneditor in 3D](images/editor/3d_scene.png)

## Übersicht der Werkzeugleiste {#toolbar-overview}

Oben rechts in der Szenenansicht befindet sich eine Werkzeugleiste mit häufig verwendeten Werkzeugen und Ansichtsoptionen (von links nach rechts):

- **Move tool** (<kbd>W</kbd>)
- **Rotate tool** (<kbd>E</kbd>)
- **Scale tool** (<kbd>R</kbd>)
- **Grid Settings** (`▦`)
- **Align/Realign Camera 2D/3D** (`2D`) — wechselt zwischen der Ausrichtung in 2D und 3D (Tastenkürzel <kbd>.</kbd>)
- **Camera Perspective/Orthographic**
- **Visibility Filters** (`👁`)

![Werkzeugleiste](images/editor/toolbar.png)

## Objekte auswählen und verändern {#manipulating-objects}

### Objekte auswählen {#selecting-objects}

Wähle Objekte im Hauptfenster mit einem <kbd>Linksklick</kbd> aus. Das Rechteck (oder der Quader), das das Objekt in der Editoransicht umgibt, wird cyanfarben hervorgehoben, um das ausgewählte Element zu kennzeichnen. Das ausgewählte Objekt wird auch in der Ansicht `Outline` hervorgehoben, wie im Bild oben zu sehen.

  Du kannst Objekte auch folgendermaßen auswählen:

- Wähle mit <kbd>Linksklick</kbd> und <kbd>Ziehen</kbd> alle Objekte innerhalb des Auswahlbereichs aus.
- Wähle Objekte in `Outline` mit einem <kbd>Linksklick</kbd> aus. Wenn du dabei <kbd>⇧ Shift</kbd> gedrückt hältst, kannst du die Auswahl erweitern. Wenn du <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> gedrückt hältst, kannst du angeklickte Objekte auswählen oder ihre Auswahl aufheben.

#### Verschiebewerkzeug {#move-tool}

![Verschiebewerkzeug](images/editor/icon_move.png){.left}

Verwende das *Move Tool*, um Objekte zu verschieben. Du findest es in der Werkzeugleiste oben rechts im Szeneneditor oder aktivierst es durch Drücken der Taste <kbd>W</kbd>.

![Objekt verschieben](images/editor/move.png){.inline}![Objekt in 3D verschieben](images/editor/move_3d.png){.inline}

Das Gizmo verändert sich und zeigt mehrere Manipulatoren – Quadrate und Pfeile (der ausgewählte Manipulator wird orange), an denen du <kbd>ziehen</kbd> kannst, um Objekte zu verschieben:

- einen cyanfarbenen quadratischen Griff in der Mitte, mit dem du das Objekt nur im Bildschirmkoordinatensystem verschiebst,
- 3 rote, grüne und blaue Pfeile entlang der einzelnen Achsen, mit denen du das Objekt nur entlang der jeweiligen X-, Y- oder Z-Achse verschiebst.
- 3 rote, grüne und blaue quadratische Griffe (umrandet und mit transparenter Füllung), mit denen du das Objekt nur auf der jeweiligen Ebene verschiebst, z. B. auf der X-Y-Ebene (blau) und auf den Ebenen X-Z (grün) und Y-Z (rot), die sichtbar werden, wenn du die Kamera in 3D drehst.

#### Drehwerkzeug {#rotate-tool}

![Drehwerkzeug](images/editor/icon_rotate.png){.left}

Verwende das *Rotate Tool*, um Objekte zu drehen. Wähle es in der Werkzeugleiste aus oder drücke die Taste <kbd>E</kbd>.

![Objekt drehen](images/editor/rotate.png){.inline}![Objekt in 3D drehen](images/editor/rotate_3d.png){.inline}

Dieses Werkzeug besteht aus vier kreisförmigen Manipulatoren (der ausgewählte Manipulator wird orange), an denen du <kbd>ziehen</kbd> kannst, um Objekte zu drehen:

- ein cyanfarbener Manipulator (der äußere, größte Kreis), der das Objekt im Bildschirmkoordinatensystem dreht
- 3 kleinere rote, grüne und blaue kreisförmige Manipulatoren, mit denen du das Objekt einzeln um die X-, Y- und Z-Achse drehst. In der orthografischen 2D-Ansicht stehen zwei davon senkrecht zur X- und Y-Achse, sodass diese Kreise nur als zwei Linien erscheinen, die das Objekt kreuzen.

#### Skalierungswerkzeug {#scale-tool}

![Skalierungswerkzeug](images/editor/icon_scale.png){.left}

Verwende das *Scale Tool*, um Objekte zu skalieren. Wähle es in der Werkzeugleiste aus oder drücke die Taste <kbd>R</kbd>.

![Objekt skalieren](images/editor/scale.png){.inline}![Objekt in 3D skalieren](images/editor/scale_3d.png){.inline}

Dieses Werkzeug besteht aus mehreren quadratischen/würfelförmigen Manipulatoren (der ausgewählte Manipulator wird orange), an denen du <kbd>ziehen</kbd> kannst, um Objekte zu skalieren:

- ein cyanfarbener Würfel in der Mitte skaliert das Objekt gleichmäßig entlang aller Achsen (einschließlich Z).
- 3 rote, blaue und grüne würfelförmige Manipulatoren skalieren das Objekt einzeln entlang der X-, Y- und Z-Achse.
- 3 rote, grüne und blaue quadratische Manipulatoren (umrandet und mit transparenter Füllung) skalieren das Objekt einzeln auf der X-Y-, X-Z- oder Y-Z-Ebene.

### Sichtbarkeitsfilter {#visibility-filters}

Klicke auf das **Augensymbol für die Sichtbarkeit** (`👁`) in der Werkzeugleiste, um verschiedene Komponententypen sowie Begrenzungsrechtecke bzw. Begrenzungsquader und Hilfslinien ein- oder auszublenden (`Component Guides` oder Tastenkombination <kbd>Ctrl</kbd> + <kbd>H</kbd> (Win/Linux) oder <kbd>^ Ctrl</kbd> + <kbd>⌘ Cmd</kbd> + <kbd>H</kbd>(Mac)).

![Sichtbarkeitsfilter](images/editor/visibilityfilters.png)

## Rastereinstellungen {#grid-settings}

Du kannst das Raster an deine Arbeitsweise anpassen (besonders nützlich in 3D). Klicke auf die Schaltfläche **Grid Settings** (`▦`), um das Popup mit den Rastereinstellungen zu öffnen.

Der Editor speichert separate Rastereinstellungen für 2D- und 3D-Ansichten. Stelle Größe, Ebene und Darstellung ein, während der gewünschte Modus aktiv ist. Beim Wechsel des Modus werden dessen Rastereinstellungen wiederhergestellt. **Reset to Defaults** setzt die Einstellungen des aktiven Modus zurück.

![Rastereinstellungen](images/editor/grid_popup.png)

Die Einstellungen umfassen:

- **Grid size (X/Y/Z)**
  Legt den Abstand zwischen den Rasterlinien entlang jeder Achse fest. Verwende kleinere Werte, um kleine Objekte präzise zu platzieren, oder größere Werte für einen umfassenderen Überblick.
- **Active plane (X/Y/Z)**
  Wählt die Ebene aus, auf der das Raster gezeichnet wird. Bei der Arbeit in 2D ist dies normalerweise **Z** (die standardmäßige X-Y-Ebene). In 3D ist **Y** üblich, um eine Bodenebene darzustellen.
- **Grid color**
  Legt die Farbe der Rasterlinien fest. Dies ist nützlich, um einen Kontrast zu verschiedenen Szenenhintergründen zu schaffen.
- **Grid opacity**
  Steuert, wie transparent die Rasterlinien sind. Bei niedrigeren Werten ist das Raster weniger aufdringlich und bietet weiterhin eine Orientierungshilfe.
- Eine Schaltfläche **Reset to Defaults**
  Stellt die ursprünglichen Werte aller Rastereinstellungen wieder her.

## Kameratyp: perspektivisch und orthografisch {#camera-type-perspective-vs-orthographic}

Der Szeneneditor unterstützt beide Typen:

- **Orthografische** Kamera (üblich bei der Arbeit in 2D)
- **Perspektivische** Kamera (üblich bei der Arbeit in 3D)

Verwende den Kameraumschalter in der Werkzeugleiste, um zwischen ihnen zu wechseln. In 3D-Szenen fühlt sich die perspektivische Navigation meist natürlicher an.

## Freier Kameramodus {#free-camera-mode}

Für die schnelle Navigation in 3D bietet der Szeneneditor den **freien Kameramodus**, eine Kamera aus der Ichperspektive im Stil eines „Ego-Shooters“.

### Den freien Kameramodus aktivieren {#activating-free-camera-mode}

- Halte <kbd>Right Mouse Button</kbd> gedrückt — der freie Kameramodus ist aktiv, solange du die Taste gedrückt hältst
- <kbd>Shift</kbd> + <kbd>`</kbd> (Backtick) — schaltet den freien Kameramodus ein; er bleibt nach dem Loslassen aktiv

::: sidenote
Bei einigen Tastaturbelegungen (z. B. der schwedischen) ist die Backtick-Taste eine Tottaste und löst die Tastenkombination möglicherweise nicht wie erwartet aus. Du
kannst diese Tastenkombination unter `File ▸ Preferences ▸ Keys` neu zuweisen und eine Tastenkombination für `Scene -> Free Camera -> Activate` eingeben.
:::

Wenn der freie Kameramodus aktiv ist, wird die Szenenansicht durch eine Linie entlang ihrer Ränder hervorgehoben.

### Den freien Kameramodus beenden {#exiting-free-camera-mode}

- Lasse <kbd>Right Mouse Button</kbd> los (wenn er durch Gedrückthalten aktiviert wurde), oder
- drücke <kbd>Left Mouse Button</kbd> oder <kbd>Right Mouse Button</kbd> und lasse die Taste wieder los, oder drücke <kbd>Esc</kbd>, wenn der freie Kameramodus per Umschaltung aktiviert wurde.

### Umschauen (Blicksteuerung mit der Maus) {#looking-around-mouse-look}

Während der freie Kameramodus aktiv ist, steuern diese Tasten die Kamerabewegung (anstelle der Editorwerkzeuge):

- Bewege die Maus, um die **Gierung** (links/rechts) und die **Neigung** (oben/unten) zu steuern
- Die Neigung ist begrenzt, um ein Überschlagen der Kamera zu vermeiden

Du kannst die Y-Achse bei Bedarf auch umkehren (siehe **Einstellungen der freien Kamera** weiter unten).

### Bewegen {#moving}

Während der freie Kameramodus aktiv ist:

- <kbd>W</kbd> — vorwärts
- <kbd>S</kbd> — rückwärts
- <kbd>A</kbd> — links
- <kbd>D</kbd> — rechts
- <kbd>E</kbd> — nach oben
- <kbd>Q</kbd> — nach unten

::: sidenote
Du kannst alle Bewegungstasten unter `File ▸ Preferences ▸ Keys` neu zuweisen. Suche dort nach `Scene -> Free Camera`.
:::

Tasten zur Änderung der Geschwindigkeit:

- Halte <kbd>Shift</kbd> gedrückt — schneller bewegen
- Halte <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> gedrückt — langsamer/präziser bewegen

### Gehmodus (optional) {#walking-mode-optional}

Der freie Kameramodus unterstützt den **Gehmodus** (Walking Mode).

Wenn er aktiviert ist:
- Die Aufwärts-/Abwärtsbewegung wird so eingeschränkt, dass sie eher dem Gehen auf einer Bodenebene aus der Ichperspektive entspricht.
- Dies ist nützlich, wenn du ein Level erkundest und eine gleichbleibende Bewegung „am Boden“ möchtest.

## Popup mit Kameraeinstellungen {#camera-settings-popup}

Die Schaltfläche für die perspektivische Kamera in der Werkzeugleiste bietet ein Popup mit Einstellungen für die Kamera.

![Einstellungen der perspektivischen Kamera](images/editor/camera_popup.png)

Das Popup enthält:

- **Move Speed**
  Passt die Bewegungsgeschwindigkeit der freien Kamera an.

- **Look Sensitivity**
  Passt an, wie schnell sich die Kamera als Reaktion auf Mausbewegungen dreht.

- **Invert Y**
  Kehrt die vertikale Blicksteuerung mit der Maus um.

- **Walking Mode**
  Schränkt die Bewegung für eine bodennahe Navigation ein.

- **Reset to Defaults**
  Stellt die Standardeinstellungen der Kamera wieder her.
