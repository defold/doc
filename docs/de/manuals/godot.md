---
title: Defold für Godot-Nutzer
brief: Dieser Leitfaden erleichtert dir den Umstieg von Godot auf Defold. Er vergleicht vertraute Konzepte und zeigt dir, wie du die entsprechenden Werkzeuge und APIs in Defold einsetzt.
---

# Defold für Godot-Nutzer {#defold-for-godot-users}

Wenn du schon mit Godot gearbeitet hast, bringst du vieles mit, was du für dein erstes Spiel in Defold brauchst. Dieser Leitfaden zeigt dir, wo du deine Erfahrung direkt einsetzen kannst und welche Unterschiede du kennen solltest, um typische Fehler zu vermeiden. Für die Beispiele haben wir Godot 4.7 verwendet.

## Einführung {#introduction}

Defold ist eine kostenlose, plattformübergreifende Game-Engine für 2D- und 3D-Spiele mit einem Editor für Windows, Linux und macOS. Den vollständigen Quellcode der Engine und des Editors findest du auf [GitHub](https://github.com/defold/defold/). Du kannst Defold selbst bauen oder eine fertige Version für dein Betriebssystem herunterladen.

Auf den ersten Blick ähnelt Defold Godot. In beiden Engines setzt du ein Spiel aus wiederverwendbaren Bausteinen zusammen und legst ihr Verhalten in Skripten fest. Godot bietet viele spezialisierte Knoten. Defold kommt mit weniger, vielseitigeren Komponenten (components) aus. Das Spielverhalten dazu schreibst du in Lua-Skripten und -Modulen. Eine Spielfigur in Defold kann zum Beispiel aus einem Spielobjekt (game object) mit einem Sprite oder Modell, einem Kollisionsobjekt und einem Skript bestehen.

Defold legt Wert auf eine kleine Laufzeitumgebung und einen sparsamen Umgang mit Ressourcen. Das kommt besonders Web- und Mobilspielen zugute. Einige Kapazitätsgrenzen der Engine werden im Voraus festgelegt, damit sie den benötigten Speicher vorab reservieren kann.

Defold bietet weniger vorgefertigte Elemente für Spielmechaniken und Benutzeroberflächen als Godot. Du kannst die vorhandenen Komponenten aber kombinieren oder erweitern, um dasselbe Ergebnis zu erzielen. Der Kern der Engine ist bewusst klein gehalten. Du kannst ihn weiter verkleinern, indem du ungenutzte Funktionen ausschließt, oder ihn mit nativen Erweiterungen und Lua-Modulen ergänzen. Im [Defold Asset Portal](https://defold.com/assets/) findest du Hunderte von Modulen, Bibliotheken und Erweiterungen, etwa für komplexe Benutzeroberflächen, aufwendigere Rendering-Pipelines oder häufige Aufgaben bei der Entwicklung.

Weitere Einzelheiten findest du in der [Funktionsübersicht von Defold](https://defold.com/product/).

## Installation

1. Lade Defold für dein Betriebssystem von der [Downloadseite](https://defold.com/download/) herunter.
2. Entpacke das Archiv und starte den Editor.

Du kannst dein erstes Projekt erstellen und ausführen, ohne einen separaten Hub oder Exportvorlagen zu installieren. Die Anweisungen für die einzelnen Plattformen findest du im [Installationshandbuch](/manuals/install/).

Du kannst Defold direkt im Editor aktualisieren. Wenn du ein bestehendes Projekt auf eine neue Version umstellst, lies die Versionshinweise und teste das Spiel auf seinen Zielplattformen.

## Willkommensbildschirm {#welcome-screen}

Auf dem Willkommensbildschirm von Defold kannst du zuletzt verwendete Projekte öffnen oder ein neues Projekt anlegen. Er erfüllt damit eine ähnliche Aufgabe wie der Projektmanager von Godot.

![Godots Projektmanager und der Willkommensbildschirm von Defold](images/godot/godot_1.png)

Für neue Projekte bietet Defold drei Ausgangspunkte.

- **Templates** enthält leere und plattformspezifische Projektvorlagen.
- **Tutorials** führt dich Schritt für Schritt durch Einstiegsprojekte.
- **Samples** enthält Beispiele und Starter-Kits, die du ausführen und erkunden kannst.

![Godots Projektmanager und die Projektvorlagen in Defold](images/godot/godot_2.png)

Unter Samples findest du Einstiegsprojekte und Beispiele, ähnlich wie die Starter-Kits und Beispiele im Godot Asset Store.

![Projektbeispiele in Godot und Defold](images/godot/godot_3.png)

:[Hello World](../shared/hello-world.md)

---

## Überblick über den Defold-Editor {#defold-editor-overview}

Die wichtigsten Bereiche werden dir vertraut vorkommen, auch wenn sie anders heißen und anders angeordnet sind. Für den direkten Vergleich haben wir die Bereiche im Godot-Editor ähnlich wie in der Standardansicht von Defold angeordnet.

![Übersicht des Godot-Editors](images/godot/godot_4.png)
![Übersicht des Defold-Editors](images/godot/godot_5.png)

| Godot | Defold | Funktion im Defold-Editor |
|---|---|---|
| FileSystem | Assets | Hier verwaltest du die Dateien und Ordner deines Projekts. Ihre Struktur entspricht genau dem Projektverzeichnis auf der Festplatte. |
| 2D-/3D-Ansicht und Ressourcen-Editoren | Haupteditor | Die Ansicht richtet sich nach der geöffneten Datei, etwa einer Sammlung (collection), einer GUI, einem Atlas oder einem Skript. Du kannst sie in zwei Bereiche teilen. |
| Scene | Outline | Zeigt die Struktur der aktuellen Ressource. Einen globalen Szenenbaum für die Laufzeit gibt es hier nicht. |
| Inspector | Properties | Zeigt die Eigenschaften des ausgewählten Objekts, der Komponente oder der Ressource an. |
| Output und Debugger | Tools | Enthält Console, Build Errors, Search Results und den Debugger. |
| Versionskontrollintegration | Changed Files | Zeigt geänderte Dateien an, wenn das Projekt Git verwendet. |

Im 3D-Editor von Defold findest du oben rechts eine Werkzeugleiste. Mehr zu ihren Funktionen steht im [Handbuch zur Szenenbearbeitung](/manuals/scene-editing/#toolbar-overview).

### Szenenausrichtung in 2D und 3D {#2d-and-3d-scene-orientation}

:[Szenenausrichtung in 2D und 3D](../shared/2d-and-3d-scene-orientation.md)

### Editorbereiche {#panes}

Die Bereiche des Defold-Editors lassen sich nicht als eigenständige Fenster abtrennen. Du kannst ihre Größe durch Ziehen am Rand ändern. Mit `F6`, `F7` und `F8` oder über das Menü `View` blendest du sie ein und aus.

![Editorbereiche ein- und ausblenden](images/editor/editor_panes.png)

### Koordinaten {#coordinates}

Verwendest du in 2D das standardmäßige Render-Skript und enthält deine Sammlung keine Kamerakomponente, liegt der Ursprung `(0, 0)` unten links im Spielfenster. Die positive Y-Achse zeigt **nach oben**, die positive X-Achse nach rechts.

In Godots üblichem 2D-Bildschirmkoordinatensystem zeigt die positive Y-Achse **nach unten**. Berücksichtige das, wenn du Positionen oder Bewegungscode übernimmst.

![Unterschiedliche Ausrichtung der 2D-Koordinaten in Defold und Godot](images/godot/godot_6.png)

Im 3D-Koordinatensystem von Godot zeigt die positive Y-Achse wie in Defold nach oben. Defold verwendet für 2D- und 3D-Spiele dasselbe dreidimensionale Koordinatensystem. Eine typische 2D-Ansicht zeigt die XY-Ebene mit orthografischer Projektion. Bei Bedarf kannst du die Kamera anders konfigurieren.

![Übereinstimmende Ausrichtung der 3D-Koordinaten in Defold und Godot](images/godot/godot_7.png)

Mehr über den Defold-Editor erfährst du im [Handbuch zum Editor](/manuals/editor/).

---

## Grundlegende Konzepte {#key-concepts}

In Godot baust du **Szenen** aus Knoten auf. In Defold arbeitest du mit Komponenten, Spielobjekten und Sammlungen von Spielobjekten.

In Godot könntest du eine Spielfigur etwa aus einem `Node2D` mit einem untergeordneten `Sprite2D` aufbauen und dem Wurzelknoten ein Skript zuweisen. Diese Figur setzt du dann in deine erste Szene (`Scene`).
In Defold könntest du die Figur als Spielobjekt mit einer `Sprite`- und einer `Script`-Komponente aufbauen. Das Spielobjekt fügst du einer Sammlung hinzu.

![Knoten einer Spielfigur in Godot im Vergleich zu Spielobjekt und Komponenten in Defold](images/godot/key_concepts.png)

Das [Handbuch zu den Bausteinen](/manuals/building-blocks/) erläutert diese Konzepte im Detail.

### Spielobjekte {#game-objects}

In Defold dient ein **Spielobjekt** als *Container* für Komponenten. Es verfügt über zwei grundlegende Merkmale.

- eine **Identität**
- eine **Transformation** (Position, Drehung und Skalierung)

Ein Spielobjekt kann eine ähnliche Rolle übernehmen wie ein `Node2D` oder `Node3D` in Godot. Defold kennt keinen eigenen Spielobjekttyp für 2D. Alle Spielobjekte verwenden eine 3D-Transformation, auch in 2D-Spielen.

Du kannst in Defold ein Spielobjekt einem anderen unterordnen, sodass es dessen Transformation erbt. Diese Beziehungen kannst du in einer Sammlung einrichten oder zur Laufzeit ändern. Die Adresse des Spielobjekts bleibt bei der Zuordnung zu einem Elternobjekt gleich.

Du kannst ein Spielobjekt direkt in der `.collection`-Datei als **eingebettetes** Objekt definieren oder einen wiederverwendbaren `.go`-Prototyp referenzieren. Bearbeitest du die Definition eines eingebetteten Objekts, ändert sich diese Sammlung. Andere, unabhängig definierte Objekte sind davon unberührt. Änderungen an einem `.go`-Prototyp gelten für alle Instanzen, die ihn referenzieren, sofern sie die jeweilige Eigenschaft nicht selbst überschreiben. Auch eingebettete Objekte können auf gemeinsame Komponentenressourcen verweisen. Änderst du eine solche Ressource, kann sich das auf andere Objekte auswirken, die sie verwenden. Verwendest du eine Sammlung mehrfach, sind Änderungen an ihren eingebetteten Objekten überall sichtbar, wo die Sammlung referenziert wird.

### Komponenten {#components}

Komponenten sind spezialisierte Bausteine. Sie bestimmen zum Beispiel das Aussehen eines Spielobjekts, geben Klang aus oder steuern seine Physik und sein Verhalten.

Füge einem Spielobjekt eine `Sprite`-Komponente hinzu, um ein Bild anzuzeigen, eine `Sound`-Komponente, um Audio abzuspielen, oder eine `Script`-Komponente, um Lua-Code auszuführen.

Komponenten gehören zu Spielobjekten und können keine untergeordneten Komponenten haben. Eine Hierarchie baust du auf, indem du Spielobjekte in einer Sammlung einander unterordnest.

Anders als in Godot kannst du einer Komponente kein Skript anhängen, um ihr Verhalten zu ändern. Du kannst sie über ihre Eigenschaften anpassen und ähnlich wie mit GDExtensions über native Erweiterungen eigene Komponententypen erstellen. Beispiele sind die offiziellen Komponenten für [Rive](https://github.com/defold/extension-rive) und [Spine](https://github.com/defold/extension-spine) sowie [Sprite Loop](https://github.com/Balkan-Ram-Games/spriteloop-defold) und [Object Interpolation](https://github.com/indiesoftby/defold-object-interpolation) aus der Community.

Ein Skript ist in Defold eine eigenständige Komponente, die du jedem Spielobjekt hinzufügen kannst. Ein einzelnes Spielobjekt kann mehrere Komponenten enthalten, darunter auch mehrere Skripte.

Weil die Komponenten eine flache Struktur bilden und von benutzerdefinierten Skripten entkoppelt sind, kann Defold sie nach den Prinzipien des datenorientierten Designs platzsparend im Speicher anordnen.

| Godot-Knoten | Defold-Komponente | Hinweise |
|---|---|---|
| `Sprite2D` / `AnimatedSprite2D` | [Sprite](/manuals/sprite/) | Rendert 2D-Texturen und Flipbook-Animationen aus einem Atlas (einer Textur mit mehreren Bildern) oder einer Kachelquelle. |
| `Area2D` / `RigidBody2D` / `StaticBody2D` und ihre 3D-Entsprechungen | [Kollisionsobjekt](/manuals/physics-objects/) | Verarbeitet Physik und Trigger. Kollisionsformen definierst du direkt in dieser Komponente. Du brauchst dafür keine eigenen Kindknoten. Als Typ kannst du statisch, dynamisch, kinematisch oder Trigger wählen. |
| `.gd`-Skript an einem Knoten | Skript | Enthält Lua-Code für die Spiellogik, die Eingabeverarbeitung und die Steuerung anderer Komponenten und Spielobjekte. |
| `TileMapLayer` | [Kachelkarte](/manuals/tilemap/) (tile map) | Rendert eine rasterbasierte Karte aus einer Kachelquelle und den Ebenen der Kachelkarte. |
| `Label` | [GUI-Textknoten](/manuals/gui-text/) | Verwende GUI-Text für die Benutzeroberfläche. Für Text in der Spielwelt verwendest du eine [Label-Komponente](/manuals/label/). |
| `AudioStreamPlayer` | [Sound](/manuals/sound/) | Gibt Audio wieder. Mit Speed, Pan und Gain legst du Wiedergabegeschwindigkeit, Stereopanorama und Verstärkung fest. |
| `Camera2D` / `Camera3D` | [Kamera](/manuals/camera/) | Unterstützt orthografische und perspektivische Projektion. |
| `Control`-Hierarchie / `CanvasLayer` | [GUI](/manuals/gui/) | Innerhalb einer GUI-Komponente gibt es eine eigene Knotenhierarchie, etwa mit Knoten vom Typ Box, Text oder Pie. Das zugehörige `.gui_script` steuert die GUI. |
| `MeshInstance3D` | [Modell](/manuals/model/) oder [Mesh](/manuals/mesh/) | Model unterstützt importierte 3D-Inhalte, Mesh eigene Geometrie aus einem Puffer. |
| `CPUParticles2D` / `GPUParticles2D` und ihre 3D-Entsprechungen | [ParticleFX](/manuals/particlefx/) | Erzeugt 2D- bzw. 3D-Partikel, die du im Partikeleditor von Defold konfigurierst. |
| `PackedScene.instantiate()` | Fabrik / Sammlungsfabrik | Für das Erzeugen von Spielobjekten und Sammlungen zur Laufzeit stehen eigene Komponenten zur Verfügung. |

### Sammlungen und Spielwelten {#collections-and-worlds}

Eine **Sammlung** beschreibt Spielobjekte, ihre Komponenten und die Eltern-Kind-Beziehungen der Objekte. Du kannst Sammlungen in andere Sammlungen einfügen, um eine Gruppe von Objekten wiederzuverwenden, ähnlich wie beim Verschachteln einer Szene in Godot. Defold bietet keine allgemeine Szenenvererbung wie Godot. Verwende Prototypen und Sammlungen mehrfach und passe die einzelnen Instanzen über Eigenschaften oder Skripte an.

Die Sammlungsdatei selbst stellt zur Laufzeit kein Objekt dar. Es gibt weder ein Sammlungsobjekt, dessen Methoden du aufrufen könntest, noch einen Wurzelknoten für die Sammlung selbst. Die Datei enthält die Definitionen, aus denen Defold zur Laufzeit die Spielobjekte, ihre Komponenten und ihre Hierarchie aufbaut.

Beim Start des Spiels liest Defold die Datei `game.project`. Dort legst du unter **Bootstrap ▸ Main Collection** fest, welche Sammlung zuerst geladen wird. Aus ihr entsteht die erste Spielwelt. Objekte aus verschachtelten Sammlungen werden Teil derselben Welt.

Eine **Sammlungsfabrik** (collection factory) erzeugt eine Gruppe von Spielobjekten samt Komponenten in der **bestehenden** Welt, in der sich die Fabrik befindet.

Ein **Sammlungs-Proxy** (collection proxy) lädt eine separate Sammlung und erstellt damit eine **neue Spielwelt** mit eigenem Adressnamensraum und eigener Physiksimulation. Der Unterschied ist wichtig, wenn du etwa in einem laufenden Level einen Gegner erzeugen willst, der mit der Geometrie dieses Levels kollidiert, oder ein ganz neues Level laden möchtest, bei Bedarf asynchron. Beide Vorgänge lernst du weiter unten kennen.

Godot verwendet `PackedScene` sowohl zum Erzeugen von Instanzen als auch für Szenenwechsel. Der Wechsel über den `SceneTree` ist mit dem Laden einer separaten Spielwelt über einen Sammlungs-Proxy vergleichbar.

Die wichtigsten Entsprechungen im Überblick.

| Godot | Defold | Hinweise |
|---|---|---|
| `Node3D` mit Kindknoten | Spielobjekt mit Komponenten | Komponenten liefern Funktionen und Verhalten. Das Spielobjekt stellt Transformation und Identität bereit. |
| Transformation von `Node2D` / `Node3D` | Transformation des Spielobjekts | Bestandteil jedes Spielobjekts. |
| Szene / `PackedScene` | Spielobjektprototyp (`.go`) oder Sammlung (`.collection`) | Ein Prototyp beschreibt ein einzelnes Objekt. Eine Sammlung beschreibt eine Gruppe von Objekten und ihre Hierarchie. |
| `PackedScene.instantiate()` | Fabrik oder Sammlungsfabrik | Erzeugt ein Spielobjekt oder eine Gruppe von Spielobjekten in der aktuellen Spielwelt und gibt die jeweiligen Bezeichner zurück. |
| Szenenwechsel über `SceneTree` und `PackedScene.instantiate()` | Sammlungs-Proxy | Lädt eine Sammlung, erstellt eine separate Spielwelt und erzeugt darin Spielobjekte. |

---

## Code schreiben {#code-writing}

Der Defold-Editor enthält einen Texteditor für sämtliche Textdateien und Skripte. Er bietet unter anderem Autovervollständigung, Formatierung und die Ansicht Structure mit einer Übersicht der Daten und Funktionen. Einzelheiten findest du im [Handbuch zum integrierten Code-Editor](/manuals/writing-code/#using-the-built-in-code-editor).

Du kannst alle textbasierten Dateien und Skripte deines Defold-Projekts auch in einem externen Editor öffnen. Defold bietet Funktionen, die die Integration mit Werkzeugen wie VS Code und die Arbeit aus diesen Werkzeugen heraus erleichtern. Mehr dazu steht im [Handbuch zu externen Code-Editoren](/manuals/writing-code/#using-an-external-code-editor).

### Lua und Skripte {#lua-and-scripts}

In Defold schreibst du die Skripte für dein Spiel in Lua. Manches wird dir aus GDScript vertraut vorkommen, doch es gibt wichtige Unterschiede. Defold unterstützt auch Teal, einen statisch typisierten Lua-Dialekt. Ähnlich wie bei GDExtensions kannst du je nach Zielplattform native Erweiterungen in C, C++, C#, Objective-C, Java oder JavaScript verwenden. Auf diese Erweiterungen gehen wir später ein.

Bei der Arbeit mit Lua in Defold begegnen dir vor allem die folgenden Dateitypen.

| Datei | Zweck |
|---|---|
| `.script` | Spiellogik und Verhalten. Über APIs wie `go`, `factory`, `sprite`, `tilemap` oder `physics` steuerst du andere Spielobjekte und Komponenten. |
| `.gui_script` | Skript für die GUI. Es legt mit der `gui`-API das Verhalten der Benutzeroberfläche fest. |
| `.render_script` | Rendering mit der `render`-API. |
| `.lua` | Wiederverwendbare Lua-Module, die du mit `require()` lädst, etwa Codebibliotheken oder Hilfsskripte. |

Lua-Tabellen können Daten, Funktionen oder beides enthalten. Für die Struktur deines Codes brauchst du die Klassenhierarchie von GDScript nicht nachzubauen. Lege wiederverwendbare Logik in Modulen ab und rufe sie aus dem Skript auf, das für das jeweilige Verhalten zuständig ist.

Defold verwendet eine mit Lua 5.1 kompatible Skriptumgebung. Sprachunterschiede und plattformspezifische Details erläutert das Handbuch [Lua in Defold](/manuals/lua/).

### Anwendungslebenszyklus {#application-lifecycle}

Ein Defold-Spiel beginnt mit einer Initialisierungsphase und endet mit einer Finalisierungsphase. Dazwischen durchläuft die Engine in jedem Frame eine Aktualisierungsschleife, in der sie Transformationen und Komponenten aktualisiert, Code ausführt und Nachrichten verarbeitet.

![Anwendungslebenszyklus in Defold](images/application_lifecycle/application_lifecycle.png)

Wie Godot und andere Game-Engines ruft Defold während des Anwendungslebenszyklus bestimmte Funktionen in deinen Skripten auf. Diese Lua-Callbacks haben andere Namen als in Godot, ihre Aufgaben werden dir aber vertraut sein.

| Godot | Defold | Aufgabe |
|---|---|---|
| `_ready()` | `init(self)` | Instanzdaten initialisieren und bei Bedarf den Eingabefokus anfordern. |
| `_process(delta)` | `update(self, dt)` | Einmal pro Frame aktualisieren. |
| `_physics_process(delta)` | `fixed_update(self, dt)` | In festen Zeitschritten aktualisieren, wenn diese Funktion aktiviert ist. |
| `_input(event)` | `on_input(self, action_id, action)` | Eingaben verarbeiten, die den Eingabeempfängern des Objekts zugestellt werden. |
| Signal-Callback | `on_message(self, message_id, message, sender)` | Nachrichten von Skripten oder Engine-Komponenten empfangen. |
| `_exit_tree()` | `final(self)` | Aufräumen, wenn die Skriptinstanz finalisiert wird. |

Godot ruft `_ready()` bei Kindknoten vor dem Elternknoten auf. Defold garantiert keine bestimmte Reihenfolge, in der Spielobjekte und Komponenten initialisiert oder aktualisiert werden. Stimme Objekte über Nachrichten aufeinander ab. So hängt dein Code nicht davon ab, welches Objekt `init()` zuerst ausführt.

Um `fixed_update()` zu verwenden, setze in `game.project` unter **Engine ▸ Fixed Update Frequency** einen positiven Wert, zum Beispiel 60, und aktiviere **Physics ▸ Use Fixed Timestep**.

Für Aufgaben zwischen der regulären Aktualisierung und dem Rendering, etwa das Nachführen einer Kamera, stellt Defold außerdem `late_update(self, dt)` bereit. Falls nötig, kann die Engine danach die Transformationen noch einmal aktualisieren.

Eine deaktivierte Komponente bleibt vorhanden, während eine gelöschte Komponente entfernt wird.

Im [Handbuch zum Anwendungslebenszyklus](/manuals/application-lifecycle/) findest du die vollständige Abfolge und die verfügbaren Callbacks für jeden Skripttyp.

### Instanzdaten und lokale Daten {#instance-data-vs-local-data}

Jede Instanz einer Skriptkomponente erhält in den Callbacks ein eigenes `self` für ihren Zustand, etwa für `self.health` oder `self.target`. Selbst zwei Skriptkomponenten auf demselben Spielobjekt haben unterschiedliche `self`-Werte. `self` ist ein Userdata-Wert, auf dessen Felder du wie bei einer Tabelle zugreifen kannst. Da es keine Lua-Tabelle ist, funktionieren Operationen wie `pairs(self)` nicht. In Godot dienen Instanzvariablen (`var`) einem ähnlichen Zweck.

In Godot definiert jede `.gd`-Datei eine Klasse. Weist du dieselbe `.gd`-Datei zehn Gegnern zu, erzeugt Godot zehn getrennte Instanzen. Jede bekommt eigene Kopien der Variablen, die auf Klassenebene mit var deklariert sind.

Defold führt eine `.script`-Datei beim Laden der Skriptressource als zusammenhängenden Block Lua-Code aus. In Lebenszyklus-Callbacks wie `init(self)` und `update(self, dt)` erhält jede Instanz der Skriptkomponente ihr eigenes `self`.

Eine lokale Variable, die du auf Dateiebene in einer Defold-Datei mit der Endung `.script` deklarierst, teilen sich dagegen **alle Instanzen** dieses Skripts. In dieser Hinsicht entsprechen lokale Variablen auf Dateiebene den statischen Variablen (`static var`) in Godot.

![Unterschied zwischen Instanzdaten und lokalen Daten in Defold](images/lua/self_local.png)

Setzt du im Beispiel den Wert von `self.has_shield` für eine Instanz auf `true`, bleiben die anderen Instanzen davon unberührt. Die lokale Variable `color` teilen sich dagegen alle Instanzen, die diese Skriptdatei verwenden. Eine Änderung kann sich deshalb auf alle diese Instanzen auswirken.

### Eigenschaften {#properties}

Mit `go.property()` definierst du eine bearbeitbare **Eigenschaft** für eine Instanz. Sie ist über `self` zugänglich. Wie bei `@export` in Godot erscheint der Wert im Editor. In Defold findest du diese Eigenschaften unter `Properties`.

![Eigenschaften im Defold-Editor](images/script-properties/properties.png)

**GDScript** in Godot, hier in einem Skript an einem `Node3D`.

```gdscript
extends Node3D

@export var speed: float = 100.0

func _process(delta):
    position.x += speed * delta
```

**Lua** in Defold, hier als Skriptkomponente.

```lua
go.property("speed", 100)

function update(self, dt)
    local position = go.get_position()
    position.x = position.x + self.speed * dt
    go.set_position(position)
end
```

Die Lua-Eigenschaft ist als `self.speed` verfügbar. Du kannst ihren Wert auch beim Erzeugen des Objekts angeben. Da Defold selbst für 2D-Transformationen `vector3` verwendet, gibst du auch eine Z-Koordinate an.

Die unterstützten Typen findest du im Handbuch [Skripteigenschaften](/manuals/script-properties/), weitere Beispiele unter [Skripte](/manuals/script/).

---

## Nachrichten und Adressierung {#messages-and-addressing}

Über Signale kann ein Godot-Objekt ein Ereignis an die verbundenen Empfänger melden. Defold-Skripte kommunizieren meist, indem sie eine Nachricht an die Adresse eines Spielobjekts oder einer Komponente senden.

In Defold kannst du aus jedem Skript mit `msg.post()` eine Nachricht senden. Zum Empfangen und Verarbeiten von Nachrichten dient der Callback `on_message()` des jeweiligen Skripts.

![Nachrichten in Defold](images/message_passing/messages_overview.png)

So kann beispielsweise eine Spielfigur eine Änderung des Punktestands an das HUD melden.

In Godot verwendet der `Player` (`Node2D`) das Skript `player.gd`. Sein Geschwisterknoten `GUI` (`CanvasLayer`) verwendet `gui.gd` und enthält ein Label namens `ScoreText`.

![Knoten für die Signalübermittlung in Godot](images/godot/godot_signals.png)

In Defold hat das Spielobjekt `player` das Skript `player.script`. Das Spielobjekt `hud` hat eine `gui`-Komponente mit einem Textknoten namens `score`. Die GUI-Komponente verwendet das Skript `hud.gui_script`.

![Spielobjekte und Komponenten für die Nachrichtenübermittlung in Defold](images/godot/defold_messages.png)

### Nachrichten senden {#sending-messages}

In Godot sind Player und GUI Geschwisterknoten. Der Player verbindet sein Signal `score_changed` mit einer Methode im GUI-Skript, die das Label aktualisiert.

**GDScript** in `player.gd`

```gdscript
extends Node2D

signal score_changed(value: int)
var score: int = 0

func _ready() -> void:
    score_changed.connect(get_node("../GUI").set_score)

func collect() -> void:
    score += 1
    score_changed.emit(score)

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        if event.keycode == KEY_SPACE:
            collect()
```

In Godot definiert der `Player` ein Signal namens `score_changed`. In `_ready()` verbindet er dieses Signal mit der Methode `set_score()` im GUI-Skript. Jeder Aufruf von `collect()` erhöht den Punktestand und löst das Signal mit dem neuen Wert aus.

In Defold ordnest du in den Eingabebindungen (input bindings) die **Leertaste** (Space) der Aktion `collect` zu. Der `player` initialisiert seinen Punktestand in `init()` und fordert den Eingabefokus an, um Eingabeereignisse zu erhalten. Bei einem Aufruf von `collect(self)` erhöht er den Punktestand und sendet die Nachricht `score_changed` an `/hud#gui`. Der neue Punktestand steht in der Nachrichtentabelle.

**Lua** in `player.script`

```lua
function init(self)
    self.score = 0
    msg.post(".", "acquire_input_focus")
end

local function collect(self)
    self.score = self.score + 1
    msg.post("/hud#gui", "score_changed", { value = self.score })
end

function on_input(self, action_id, action)
    if action_id == hash("collect") and action.pressed then
        collect(self)
    end
end
```

In Defold braucht der Player vorab kein Signal mit der GUI zu verbinden. Er sendet die Nachricht an die Adresse des Empfängers. Zusammen mit der relativen Adressierung von Defold kannst du so wiederverwendbare Funktionen und Skripte schreiben.

### Nachrichten empfangen und verarbeiten {#receiving-and-handling-messages}

Die GUI empfängt den Wert und aktualisiert die Anzeige des Punktestands.

**GDScript** in `gui.gd` am Knoten `GUI` (`CanvasLayer`)

```gdscript
extends CanvasLayer

func set_score(value: int) -> void:
    $ScoreText.text = str(value)
```

Das GUI-Skript empfängt den übermittelten Wert über `set_score()` und aktualisiert das untergeordnete Label `ScoreText`. Der Player selbst greift nicht direkt auf das Label zu.

Das GUI-Skript in Defold holt sich zunächst mit `gui.get_node()` den Textknoten für die Punkteanzeige. Empfängt die GUI-Komponente eine Nachricht, prüft `on_message()` deren Bezeichner. Bei `score_changed` liest das Skript `message.value` aus und aktualisiert den Text mit `gui.set_text()`.

**Lua** in `hud.gui_script`, dem Skript der GUI-Komponente

```lua
function init(self)
    self.score_node = gui.get_node("score")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("score_changed") then
        gui.set_text(self.score_node, tostring(message.value))
    end
end
```

In Defold ist die Nachricht an die GUI-**Komponente** adressiert. Der Textknoten mit dem Punktestand hat keine eigene Empfängeradresse. Das GUI-Skript entscheidet beim Empfang, wie es die Nachricht verarbeitet und welchen Textknoten es aktualisiert.

Beide Abbildungen zeigen anfangs den Text `Score: 0`. Sobald sich der Punktestand ändert, ersetzen die Beispielskripte den gesamten Text durch den Zahlenwert.

`msg.post()` reiht eine Nachricht zur späteren Zustellung ein. Der Aufruf führt den Empfänger nicht sofort aus und liefert kein Ergebnis des empfangenden Skripts zurück. Die Zustellung erfolgt häufig im selben Frame. Weil die Zahl der Zustelldurchläufe begrenzt ist, kann sich eine lange Nachrichtenkette aber über mehrere Frames erstrecken. Um zu antworten, kann der Empfänger über die an `on_message()` übergebene Absender-URL eine neue Nachricht an den ursprünglichen Absender senden. Einzelheiten stehen unter [Nachrichtenketten](/manuals/message-passing/#message-chains).

Auch bei mehreren Empfängern gibt es einen Unterschied. Ein Godot-Signal kann mit mehreren Methoden verbunden sein und benachrichtigt beim Auslösen alle verbundenen Empfänger. Jede Defold-Nachricht hat eine bestimmte Zieladresse. Um mehrere Empfänger zu erreichen, kann der Absender separate Nachrichten senden, oder du kannst im Spiel ein System zum Abonnieren von Nachrichten implementieren.

### Objekte über ihre Adresse finden {#finding-an-object-addressing-in-defold}

In Defold gibt es keine allgemeine Entsprechung zu `get_node()`, die eine andere Skriptinstanz als Lua-Objekt zurückgibt. Du übergibst einen Bezeichner oder eine **URL** an eine Engine-Funktion wie `go.get_position()`, `go.set()` oder `msg.post()`.

Eine URL in Defold besteht aus drei Teilen.

```lua
socket:/path#component
```

- Der **Socket** bezeichnet die Spielwelt, etwa die der Startsammlung (bootstrap collection) oder eine Welt, die über einen Sammlungs-Proxy geladen wurde.
- Der **Pfad** bezeichnet ein Spielobjekt innerhalb dieser Welt.
- Der **Komponententeil** bezeichnet eine Komponente dieses Spielobjekts.

Du kannst die vollständige URL angeben oder Teile auslassen, um eine relative Adresse zu bilden. Ein Skript kann zum Beispiel nur den Komponententeil verwenden, um eine Komponente desselben Spielobjekts anzusprechen. Die folgende Tabelle zeigt gebräuchliche Adressen.

| Adresse | Bedeutung |
|---|---|
| `"#sprite"` | Die Sprite-Komponente des aktuellen Spielobjekts. |
| `"/player#controller"` | Die Komponente controller des Spielobjekts player in der aktuellen Welt. |
| `"level:/player#controller"` | Die Komponente controller in der geladenen Welt namens level. |
| `"."` | Kurzform für das aktuelle Spielobjekt (`Game Object`). Nachrichten gehen an dessen Komponenten. |
| `"#"` | Kurzform für die aktuelle Skriptkomponente (`Script`). |

Verschachtelte Sammlungen können dem Objektpfad Präfixe hinzufügen. Die Zuordnung zu einem Elternobjekt für die Transformation ändert die Adresse eines Objekts dagegen nicht.

Wenn du Objekte dynamisch erzeugst, speichere die von `factory.create()` bzw. `collectionfactory.create()` zurückgegebenen Bezeichner in deinem Code.

Godots Gruppen für Abfragen in der Spiellogik oder für `call_group()` haben in Defold keine eingebaute Entsprechung. Dafür brauchst du ein eigenes Verzeichnis der Objekte oder einen Mechanismus zur Weiterleitung von Nachrichten.

Die Physikgruppen der Kollisionsobjekte sind Kollisionsfilter. Sie legen zusammen mit der Maske fest, welche Gruppen miteinander kollidieren, und sind unabhängig von der Nachrichtenübermittlung.

Lies die Handbücher zur [Adressierung](/manuals/addressing/) und zur [Nachrichtenübermittlung](/manuals/message-passing/) am besten schon zu Beginn. Dort findest du Antworten auf viele Fragen, die sich beim ersten Projekt ergeben.

---

## Autoloads und gemeinsamer Zustand {#autoloads-and-shared-state}

Mit Lua-Modulen kannst du Lua-Funktionen auch direkt aufrufen. Für diesen Austausch brauchst du das Nachrichtensystem von Defold nicht.

Wenn du in Godot einen **Autoload** für gemeinsame Daten verwendest, kann ein Lua-Modul in Defold dieselbe Aufgabe übernehmen. Speichere das Modul zum Beispiel als `modules/game_state.lua` und lade es mit `require "modules.game_state"`.

**GDScript** mit `game_state.gd`, als Autoload unter dem Namen `GameState` registriert

```gdscript
extends Node
var score: int = 0
```

Das entsprechende Modul in **Lua** in der Datei `modules/game_state.lua`

```lua
local M = { score = 0 }
return M
```

Ein anderes Skript kann nun auf die gemeinsamen Daten zugreifen.

**GDScript**

```gdscript
func add_point():
    GameState.score += 1
```

**Lua**

```lua
local game_state = require "modules.game_state"

local function add_point()
    game_state.score = game_state.score + 1
end
```

Die Funktion `require()` speichert das Modul zwischen. Deshalb teilen sich die Aufrufer die Tabelle, die es zurückgibt. Spielobjekt-, GUI- und Render-Skripte teilen sich den Lua-Zustand. Das Entladen eines Sammlungs-Proxys setzt die Moduldaten nicht zurück. Beim Start eines neuen Spiels kannst du sie ausdrücklich zurücksetzen.

Ein Lua-Modul ist in Defold kein Spielobjekt. Es erhält keine Lebenszyklus-, Nachrichten- oder Eingabe-Callbacks. Wenn du mit einem Autoload in jedem Frame Code ausführst, Klänge abspielst oder Levelwechsel steuerst, übertrage dieses Verhalten auf ein Skript an einem Spielobjekt in der Sammlung. Du kannst im Modul auch eigene Funktionen definieren und sie in den entsprechenden Lebenszyklus-Callbacks deiner Skripte aufrufen.

Lua-Modul `my_module`

```lua
local M = {}

function M.init(self)
    print("My init")
end

return M
```

Lua-Skript
```lua
local my_module = require "my_module"

function init(self)
    my_module.init(self)
end
```

Für instanzspezifische Daten kann ein Modul eine Funktion zurückgeben, die bei jedem Aufruf eine neue Tabelle erzeugt. Diese Tabelle kannst du in `self` speichern. Weitere Einzelheiten und Hinweise zu Hot Reload findest du im [Handbuch zu Lua-Modulen](/manuals/modules/).

---

## Objekte erzeugen und Level laden {#spawning-objects-and-loading-levels}

### Fabriken {#factories}

Um in Defold ein einzelnes Spielobjekt zu erzeugen, füge eine **Fabrik** (factory) hinzu und wähle für ihre Eigenschaft **Prototype** die gewünschte `.go`-Datei.

Für eine Sammlung fügst du entsprechend eine **Sammlungsfabrik** hinzu und gibst eine `.collection`-Datei an. Die Fabrik erzeugt eine Gruppe von Spielobjekten und behält deren Eltern-Kind-Beziehungen bei.

Im folgenden Godot-Beispiel befindet sich ein `Node2D` am Ursprung der Szene. Sein Skript erzeugt Geschosse.

**GDScript**

```gdscript
extends Node2D

const BULLET = preload("res://bullet.tscn")

func spawn_bullet():
    var bullet = BULLET.instantiate()
    bullet.position = Vector2(200, 100)
    add_child(bullet)
    return bullet
```

In Defold enthält ein Spielobjekt eine Fabrik mit der ID `bullet_factory`. Mit `factory.create()` lassen wir die Fabrik das Spielobjekt erzeugen, auf das ihre Eigenschaft `Prototype` verweist.

![Spielobjekt mit Fabrik in Defold](images/godot/defold_factory.png)

Die Abbildung zeigt den Aufruf der Fabrik in `init()`. Die folgende Hilfsfunktion zeigt, wie du beim Erzeugen eine Position vorgibst und den Bezeichner zurückgibst.

**Lua**

```lua
local function spawn_bullet()
    local position = vmath.vector3(200, 100, 0)
    local id = factory.create("#bullet_factory", position)
    return id
end
```

Die Funktion in Defold gibt den **Bezeichner** des neuen Objekts zurück. Dieser Bezeichner hat keine Methoden. Du kannst ihn an Funktionen der `go`-API übergeben. Hat das erzeugte Objekt eine Skriptkomponente namens `controller`, kannst du ihre URL mit `msg.url(nil, id, "controller")` bilden.

Eine Sammlungsfabrik gibt eine Tabelle zurück, die die IDs der Prototypobjekte den IDs der erzeugten Spielobjekte zuordnet. Bewahre sie auf, wenn du die Objekte später löschen möchtest.

```lua
local ids = collectionfactory.create("#collection_factory")
-- Later, when the spawned objects are no longer needed:
go.delete(ids)
```

Anders als `queue_free()` in Godot löscht `go.delete(id)` die Kinder standardmäßig nicht rekursiv. Mit `go.delete(id, true)` löschst du ein Objekt und alle ihm aktuell untergeordneten Objekte. Übergibst du die Tabelle der Fabrik an `go.delete(ids)`, löscht Defold die aufgelisteten Objekte. Andere, erst später untergeordnete Objekte bleiben dabei erhalten. Beim rekursiven Löschen eines bekannten Wurzelobjekts werden dagegen auch solche später hinzugekommenen Nachkommen gelöscht. Siehe [`go.delete()`](/ref/go/#go.delete).

Defold reserviert die Kapazität für Spielobjekte und Komponenten im Voraus. Falls du keine weiteren Objekte erzeugen kannst, weil ein Limit erreicht ist, prüfe in `game.project` die Einstellung **Collection ▸ Max Instances** und die Limits der beteiligten Komponenten. Erhöhst du pauschal alle Limits, steigt auch der Speicherbedarf.

Informationen zu Eigenschaften, Transformationen und dynamischem Laden findest du in den Handbüchern zu [Fabriken](/manuals/factory/) und [Sammlungsfabriken](/manuals/collection-factory/).

### Sammlungs-Proxys {#collection-proxies}

Um eine Sammlung zu laden, etwa für einen Levelwechsel, füge einem dauerhaft vorhandenen Spielobjekt eine Komponente vom Typ **Collection Proxy** hinzu. Wähle in der Eigenschaft **Collection** die entsprechende `.collection`-Datei.

![Konfiguration eines Sammlungs-Proxys in Defold](images/godot/defold_proxy.png)

Fordere das Laden mit `"load"` oder `"async_load"` über `msg.post()` an. Sobald der Ladevorgang abgeschlossen ist, antwortet der Proxy mit `"proxy_loaded"`. Anschließend kannst du `"init"` und `"enable"` an die geladene Sammlung senden, um die Spielwelt zu initialisieren und zu starten. Die Zieladresse erhältst du in on_message über `sender`.

Damit bestimmst du ausdrücklich, welche Welten geladen werden und laufen. Die aktuelle Szene wird dabei nicht wie bei einem Szenenwechsel in Godot automatisch ersetzt. Sende dem jeweiligen Proxy die Nachricht `"unload"`, wenn du die zugehörige Spielwelt entfernen möchtest. Der Proxy deaktiviert und finalisiert die Welt vor dem Entladen automatisch und bestätigt den Abschluss mit `"proxy_unloaded"`. Bei Bedarf kannst du `"disable"` und `"final"` auch einzeln senden, um den Zeitpunkt dieser Schritte selbst zu steuern.

Kollisionsobjekte in unterschiedlichen Proxy-Welten können nicht miteinander kollidieren, selbst wenn beide Welten gleichzeitig geladen und auf dem Bildschirm sichtbar sind. Spielobjekte und Komponenten können aber über die Weltgrenzen hinweg Nachrichten austauschen. Die URL muss dafür den Socket des Ziels enthalten.

Lies vor dem Einrichten eines Levelwechsels das [Handbuch zu Sammlungs-Proxys](/manuals/collection-proxy/). Es beschreibt das Laden und Entladen, die Weiterleitung von Eingaben und die Steuerung der Aktualisierungsrate einer geladenen Welt.

## Projektressourcen und Assets {#project-resources-and-assets}

Ein Defold-Projekt ist ein Ordner mit `game.project`, Skripten und Ressourcen. Der Bereich **Assets** bildet diese Ordnerstruktur ab. Die meisten Ressourcen sind in Textdateien definiert, sodass du Änderungen in der Versionsverwaltung nachvollziehen kannst.

Beim Bauen oder Bündeln des Spiels wandelt Defold die Quellressourcen in Laufzeitformate um. Die Ressourcen, auf die Hauptsammlung, Fabriken und Sammlungs-Proxys verweisen, bilden einen Abhängigkeitsbaum. Eine Datei, die nur im Projektordner liegt und nirgendwo referenziert wird, gelangt nicht in das Bundle.

In Defold gibt es keine allgemeine Entsprechung für Godots eigene `Resource`-Klassen und `.tres`-Dateien. Verwende die Ressourcentypen der Engine für Engine-Inhalte und Lua-Tabellen oder Datendateien für deine eigenen Spieldaten. Mit der [`resource`-API](/ref/resource/) kannst du unterstützte Ressourcen zur Laufzeit erstellen oder verändern.

Die Ressourcen einer gewöhnlichen Fabrik werden zusammen mit ihr geladen. Aktiviere **Load Dynamically**, wenn du sie erst später laden möchtest. Mit `factory.load()` oder `collectionfactory.load()` kannst du sie dann asynchron vorbereiten. Die Inhalte eines Sammlungs-Proxys werden geladen, wenn du dies anforderst.

Du kannst im Bundle enthaltene Inhalte zu einem späteren Zeitpunkt laden. Sollen Inhalte hingegen nachträglich heruntergeladen werden, kannst du sie mit [Live Update](/manuals/live-update/) aus dem anfänglichen Bundle ausschließen und separat bereitstellen.

Weitere Informationen findest du im [Handbuch zur Ressourcenverwaltung](/manuals/resource/).

---

## Eingabe {#input}

Godots `InputMap` entspricht in Defold der Datei mit der Endung `.input_binding`. Darin ordnest du Auslöser von Tastatur, Gamepad, Maus, Touch- oder Texteingabe einem Aktionsnamen zu. Die Bindungsdatei wählst du in `game.project` unter **Input ▸ Game Binding** aus.

![Eingabebindungen im Defold-Editor](images/input/defold_input.png)

Damit ein Spielobjekt Eingaben erhält, muss es in Defold den **Eingabefokus anfordern**. Dadurch gelangt es auf den Eingabestapel. Seine Skript- und GUI-Komponenten können jetzt über `on_input()` Eingaben empfangen.

In der Abbildung ist die Leertaste mit `collect` verknüpft. Das folgende eigenständige Beispiel verwendet eine Aktion namens `fire`. Füge diese Aktion ebenfalls deinen Eingabebindungen hinzu.

**GDScript**

```gdscript
extends Node

func _input(event):
    if event.is_action_pressed("fire"):
        print("Fire")
```

**Lua**

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("fire") and action.pressed then
        print("Fire")
    end
end
```

Die Tabelle `action` enthält je nach Eingabe Felder wie `pressed`, `released` und `value`.

Die Eingabe wird den Stapel hinunter weitergereicht, beginnend mit dem Empfänger, der zuletzt den Fokus erhalten hat. Gib in `on_input()` den Wert `true` zurück, um eine Aktion zu verbrauchen, etwa wenn ein Menü einen Klick verarbeitet.

Bei einer über einen Proxy geladenen Welt müssen sowohl das Spielobjekt mit dem Proxy als auch die Eingabeempfänger in der geladenen Welt den Fokus anfordern. Fehlt einer dieser Schritte, erhält ein zuvor funktionierendes Eingabeskript nach einem Levelwechsel keine Eingaben mehr.

Weitere Informationen findest du im [Eingabehandbuch](/manuals/input/) und in den Handbüchern zu [Maus und Touch](/manuals/input-mouse-and-touch/) sowie [Gamepads](/manuals/input-gamepads/).

---

## Physik und Kollisionen {#physics-and-collisions}

Ein **Kollisionsobjekt** in Defold entspricht einem Physikkörper in Godot. Es vereint die Physikeinstellungen **und** die Kollisionsformen in einer Komponente. Ob dein Spiel 2D- oder 3D-Physik verwendet, legst du in `game.project` fest. Im App-Manifest kannst du außerdem die Version der Physik-Engine auswählen oder die Physik ganz deaktivieren.

Defold bietet vier Typen von Kollisionsobjekten.

| Godot | Defold-Typ | Verhalten |
|---|---|---|
| `StaticBody2D` / `3D` | `Static` | Bewegt sich nicht. Dynamische Objekte reagieren darauf. |
| `RigidBody2D` / `3D` | `Dynamic` | Die Physik-Engine simuliert die Bewegung und löst Kollisionen auf. |
| `CharacterBody2D` / `3D` | `Kinematic` | Die Physik-Engine liefert die Kollisionsdaten. Dein Code muss auf Kollisionen reagieren und sie auflösen. |
| `Area2D` | `Trigger` | Meldet nur das Betreten und Verlassen des Bereichs, ohne eine physikalische Reaktion auszulösen. |

Ein kinematisches Objekt in Defold verhält sich anders als ein `CharacterBody2D` mit `move_and_slide()`. Defold erkennt die Kontakte und liefert die Daten in einer Kollisionsnachricht. Dein Skript ist für die Bewegung und die Reaktion auf die Kollision zuständig. Wenn du die Steuerung einer Spielfigur entwickelst, lies das [Handbuch zum Auflösen von Kollisionen](/manuals/physics-resolving-collisions/).

Für Gruppen und Masken verwendest du Namen anstelle nummerierter Kollisionsebenen. Damit die Engine eine Kollision registriert, **muss jedes der beiden Objekte die Gruppe des anderen in seiner Maske enthalten**.

![Kollisionsgruppen und Masken in Defold](images/physics/collision_groups.png)

Das Spielobjekt namens `danger` gehört in dieser Abbildung zur Gruppe `player`, das Objekt namens `player` zur Gruppe `danger`. Die Gruppennamen müssen also nicht mit den Objekt-IDs übereinstimmen. Die Masken erlauben trotzdem Kollisionen zwischen diesen beiden Gruppen.

Standardmäßig senden Kollisionsobjekte Nachrichten an die Skripte auf ihrem Spielobjekt. Verarbeite `"collision_response"`, `"contact_point_response"` oder `"trigger_response"` in `on_message()`. Trigger-Nachrichten haben ein Feld `enter`, mit dem du Eintritt und Austritt unterscheiden kannst. Solange zwei Objekte in Kontakt bleiben, können weitere Kollisions- und Kontaktnachrichten eintreffen. Eine Nachricht bedeutet also nicht zwingend einen neuen Treffer.

Du kannst Physikereignisse auch mit einem [Listener für Kollisionsereignisse](/manuals/physics-events/) verarbeiten. Entscheide dich für einen der beiden Ansätze. Sobald du einen Listener einsetzt, ersetzt er die standardmäßige Zustellung der Physiknachrichten und die Skripte erhalten diese Nachrichten nicht mehr.

Es stehen verschiedene einfache und komplexe Kollisionsformen zur Verfügung. Näheres dazu findest du im [Handbuch zu Kollisionsformen](/manuals/physics-shapes).

![Mesh als Kollisionsform](images/physics/mesh.png)

Weitere Informationen und die zugehörigen APIs findest du in der [Physikübersicht](/manuals/physics/) sowie in den Handbüchern zu [Kollisionsobjekten](/manuals/physics-objects/), [Kollisionsnachrichten](/manuals/physics-messages/) und [Strahlabfragen](/manuals/physics-ray-casts/).

---

## GUI

Die Benutzeroberfläche eines Defold-Spiels liegt in einer **GUI-Komponente**, die du aus einer `.gui`-Datei erstellst. Darin ordnest du GUI-Knoten wie Boxen, Textknoten oder Kreissektoren an. Ein eigenes `.gui_script` steuert die GUI-Komponente, ähnlich wie ein Skript an einem `CanvasLayer` in Godot.

Die Knoten gehören zur GUI und haben eine eigene Hierarchie außerhalb der Transformationshierarchie des Spielobjekts. Standardmäßig wird die GUI über der Spielwelt gezeichnet. Weder die Spielkamera noch das Spielobjekt mit der GUI-Komponente bewegen die GUI mit sich.

Weise der GUI ein `.gui_script` zu, um die Knoten mit `gui.get_node()`, `gui.set_text()` und weiteren Funktionen der `gui`-API zu steuern. Die `gui`-API steht nur GUI-Skripten zur Verfügung, die `go`-API nur Spielobjektskripten. Tausche zwischen beiden Nachrichten aus, wie oben im Beispiel mit dem Punktestand.

Mit Vorlagen kannst du die Knotenhierarchie einer anderen GUI wiederverwenden. Das ähnelt der Wiederverwendung eines Knotens in Godot.

Defold stellt einfache Knoten als Bausteine für deine Oberfläche bereit. Ein Satz fertiger Widgets wie Godots Button oder Layout-Container gehört nicht dazu. Für eine Schaltfläche kannst du etwa eine Box und einen Textknoten kombinieren, die Eingaben im GUI-Skript verarbeiten und mit `gui.pick_node()` prüfen, ob sich der Zeiger über der Schaltfläche befindet.

Die GUI von Defold unterstützt auch **Ebenen**, ähnlich den Ebenen von Godots `CanvasLayer`. In Defold haben Ebenen Namen anstelle von Nummern. Ihre Reihenfolge unter „Layers“ bestimmt die Zeichenreihenfolge.

Anker, Drehpunkte, Anpassungsmodi und [GUI-Layouts](/manuals/gui-layouts/) helfen dir, deine Oberfläche an verschiedene Bildschirmgrößen anzupassen. Sie erfüllen ähnliche Aufgaben wie die Layout-Container von Godot, funktionieren aber im Einzelnen anders.

Für eine größere oder komplexere Benutzeroberfläche kannst du eigenen Code für Layouts und Widgets ergänzen oder eine Bibliothek aus der Community wie [Druid](https://defold.com/assets/druid/) verwenden.

Weitere Einzelheiten findest du in den Handbüchern zur [GUI](/manuals/gui/) und zu [GUI-Skripten](/manuals/gui-script/).

## Animation

Die Aufgaben von Godots `AnimationPlayer` verteilen sich in Defold auf mehrere Animationswerkzeuge.

- **Flipbook-Animationen** spielen Bildfolgen auf Sprites und GUI-Boxen ab.
- **Modellanimationen** spielen importierte Skelettanimationen auf 3D-Modellen ab.
- **Eigenschaftsanimationen** interpolieren Werte mit `go.animate()` oder `gui.animate()`.
- **[Spine](https://github.com/defold/extension-spine)**, **[Rive](https://github.com/defold/extension-rive)** und **[SpriteLoop](https://github.com/Balkan-Ram-Games/spriteloop-defold)** stehen über Erweiterungen als zusätzliche Animationsformate zur Verfügung.

### Tweens als Eigenschaftsanimationen in Defold {#tweens-defold-property-animations}

Ein einfacher Tween aus Godot lässt sich in Defold als Eigenschaftsanimation umsetzen. Beide Beispiele bewegen ein Objekt innerhalb einer halben Sekunde auf `X = 200`.

**GDScript** an einem `Node2D`

```gdscript
func move_to_target():
    var tween = create_tween()
    tween.set_trans(Tween.TRANS_QUAD)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(self, "position:x", 200.0, 0.5)
```

**Lua** in einem Spielobjektskript

```lua
local function move_to_target()
    go.animate(".", "position.x", go.PLAYBACK_ONCE_FORWARD,
        200, go.EASING_OUTQUAD, 0.5)
end
```

Wenn eine Sequenz mehrere Eigenschaften ändern, Klänge abspielen oder Spielereignisse auslösen soll, steuerst du die Abfolge in Lua. Defold hat noch keinen eigenen Zeitleisten-Editor für Animationen. Der Curve Editor im Bereich Tools dient dazu, ParticleFX-Eigenschaftskurven über die Lebensdauer eines Partikels zu bearbeiten.

Weitere Informationen findest du unter [Animation](/manuals/animation/), [Eigenschaftsanimation](/manuals/property-animation/), [Flipbook-Animation](/manuals/flipbook-animation/) und [Modellanimation](/manuals/model-animation/). Die Übersicht verweist auch auf die Erweiterungen für Spine und Rive.

## Kachelkarten {#tilemaps}

Eine `Tilemap`-Komponente in Defold verwendet eine **Kachelquelle**, die ein Raster aus Kacheln enthält. Im integrierten Kachelkarten-Editor kannst du Kacheln auf Ebenen malen und sie zur Laufzeit über die `tilemap`-API ändern.

Die integrierte Kachelkarte von Defold verwendet ein rechteckiges Raster. Godots Terrain-Sets und Regeln zur automatischen Kachelplatzierung lassen sich derzeit nicht direkt übernehmen. Du kannst das benötigte Verhalten in Code nachbilden oder einen externen Karteneditor verwenden, der nach Defold exportieren kann, etwa [Tiled](https://doc.mapeditor.org/en/stable/manual/export-defold/?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website) oder [TileSetter](https://www.tilesetter.org/docs/exporting?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website#defold).

Mehr dazu erfährst du im [Handbuch zu Kachelkarten](/manuals/tilemap/).

---

## Rendering-Pipeline

Defold bietet eine vollständig skriptbare Rendering-Pipeline mit einer eigenen `.render`-Datei, einem `.render_script` und Unterstützung für Shader. Für die meisten Spiele kannst du die integrierte Standard-Pipeline verwenden.

Das standardmäßige Render-Skript von Defold deckt gängige 2D- und 3D-Inhalte ab. Mit einem eigenen `.render_script` steuerst du Zeichendurchläufe, Renderziele und weitere Rendering-Vorgänge. Anhand von Material-Tags kann das Skript über Render-Prädikate Gruppen von Komponenten auswählen. Defold unterstützt von Haus aus physikalisch basiertes Rendering (PBR). Aus der Community stehen außerdem zahlreiche eigene Rendering-Pipelines und Shader zur Verfügung.


Defold verwendet GLSL-Shader mit getrennten Dateien für Vertex- und Fragment-Shader. Godot hat eine eigene GLSL-ähnliche Shader-Sprache mit Engine-spezifischen eingebauten Funktionen und Variablen. Daher musst du Shader aus Godot oder aus anderen Quellen wie Shadertoy gegebenenfalls anpassen. Die Anforderungen von Defold findest du im [Shader-Handbuch](/manuals/shader/).

In Defold verknüpfen **Materialien** Vertex- und Fragmentprogramme (Shader), Texturen sowie Shader-Konstanten und -Attribute. Die Standardmaterialien im Ordner `builtins` sind gute Ausgangspunkte für eigene Materialien.

Wenn du das Standardverhalten anpassen möchtest, lies die Handbücher zu [Rendering](/manuals/render/), [Materialien](/manuals/material/) und [Shadern](/manuals/shader/).

### Zeichenreihenfolge und Ebenen {#draw-order-and-layers}

Godots ganzzahliger `z_index` hat in Defold keine direkte Entsprechung. Defold verwendet als 3D-Engine eine räumliche Z-Koordinate. Ob sich eine Bewegung entlang dieser Achse als Änderung der Bildtiefe auswirkt, hängt von der Rendering-Konfiguration ab. Godot verwendet für die Sortierung in 2D einen eigenen ganzzahligen Wert.

In der **standardmäßigen** orthografischen Ansicht von Defold werden nur Objekte mit einer Z-Position zwischen −1,0 und 1,0 gerendert. Für verschiedene Ebenen eignen sich Zwischenwerte wie 0,1 oder 0,2. Den Bereich kannst du mit einer Nachricht an das Render-Skript ändern. Innerhalb dieses Bereichs werden Spielobjekte und Sprite-Komponenten im einfachen Standardfall nach ihrer räumlichen Z-Position sortiert. Objekte mit höheren Z-Werten werden über denen mit niedrigeren Werten gezeichnet. Das kann sich ähnlich verhalten wie `z_index` in Godot. Wechselst du zu einer perspektivischen Kamera oder änderst du das `.render_script`, kann die Reihenfolge anders ausfallen.

Die Zeichenreihenfolge von GUI-Knoten ist unabhängig von der Z-Koordinate in der Spielwelt. Standardmäßig werden GUI-Komponenten in einem eigenen Durchlauf nach den Sprites der Welt gerendert. Eine Änderung der Z-Position eines GUI-Knotens hat daher keinen Einfluss auf seine Zeichenreihenfolge. Entscheidend sind die Reihenfolge der Knoten in der GUI-Hierarchie (in der Outline von oben nach unten) und die GUI-Ebenen unter `Layers`. Die Ebenen haben Vorrang vor der Knotenreihenfolge, damit Zeichenaufrufe gebündelt werden können. In dieser Hinsicht ähneln sie den Ebenen von `CanvasLayer`.

### Kameras und Koordinaten {#cameras-and-coordinates}

Füge einem Spielobjekt eine `Camera`-Komponente hinzu. Bewegst du das Spielobjekt, bewegt sich die Kamera mit. Für eine typische 2D-Ansicht wählst du eine orthografische Projektion, für 3D eine perspektivische.

Das standardmäßige Render-Skript verwendet automatisch die zuletzt aktivierte Kamera. Ohne Kamera erhältst du eine orthografische 2D-Ansicht. Ist eine Kamera aktiviert, verwendet das Skript diese. Damit kannst du anfangen und das Rendering später an die Anforderungen deines Spiels anpassen.

Eine Kamera verändert die Abbildung von Welt- auf Bildschirmkoordinaten. Verwende bei Zeigereingaben in der Spielwelt die Umrechnungsfunktionen der [Kamera-API](/ref/camera/), denn die Zeigerposition entspricht nicht unbedingt der Weltposition. Die Trefferprüfung für GUI-Knoten verwendet standardmäßig weiterhin GUI-Koordinaten.

Projektion, Zoom und Koordinatenumrechnung sind im [Kamerahandbuch](/manuals/camera/) beschrieben.

---

## Ein Spiel exportieren {#exporting-a-game}

Den Export nennt Defold **Bündeln** (bundling). Wähle **Project ▸ Bundle**, gib eine Zielplattform an und lege die Bundle-Optionen fest. Der Editor liefert die Build-Werkzeuge mit. Eine separate Installation wie bei Godots Exportvorlagen entfällt.

Die Datei `game.project` enthält die Projekt- und Plattformeinstellungen, darunter die Hauptsammlung, die Eingabebindungen und die Anzeigegröße. Je nach Plattform gelten zusätzliche Vorgaben für die Signierung oder die Veröffentlichung im Store. Für Projekte mit nativen Erweiterungen erstellt der Cloud-Build-Dienst eine angepasste Engine. Dafür brauchst du eine Netzwerkverbindung. Du kannst den Build-Dienst auch selbst lokal einrichten.

Die endgültige Bundle-Größe hängt von den Assets, Erweiterungen und Build-Einstellungen ab. Erstelle einen `Build Report`, um zu sehen, welche Ressourcen dein Spiel enthält.

Lies die Handbücher zum [Bündeln](/manuals/bundling/), zu den [Projekteinstellungen](/manuals/project-settings/) und zu [HTML5](/manuals/html5/). Teste ein Bundle frühzeitig auf der Zielplattform, vor allem wenn dein Spiel Shader, native Erweiterungen oder Plattformdienste nutzt.

## Bibliotheken und Erweiterungen {#libraries-and-extensions}

Du kannst deinem Defold-Projekt **Bibliotheksabhängigkeiten** mit gemeinsam genutzten Skripten und Ressourcen hinzufügen. Trage dafür die Archiv-URLs in `game.project` ein und lade die Bibliotheken. Eine gute Anlaufstelle ist das [Defold Asset Portal](https://defold.com/assets/). Mit der Editor-Erweiterung **Asset Store** kannst du Assets wie in Godot direkt im Editor suchen und herunterladen.

Mit **Editor-Skripten und eigenen Editoroberflächen** kannst du Befehle hinzufügen, Aufgaben automatisieren und den Editor anpassen, etwa um Level schneller zu bearbeiten, Ressourcen zu erstellen oder Kacheln automatisch zu platzieren. Diese Werkzeuge übernehmen ähnliche Aufgaben wie `EditorPlugin` und `@tool` in Godot, verwenden aber die `editor`-API und den Lebenszyklus von Defold.

Über **native Erweiterungen** kannst du Skripten Funktionen aus nativem Code zur Verfügung stellen oder die Engine um Komponenten und Plattformintegrationen ergänzen. Damit erfüllen sie eine ähnliche Aufgabe wie GDExtension, verwenden aber eine andere API und einen anderen Build-Prozess.

Mehr dazu findest du unter [Bibliotheken](/manuals/libraries/), [Editor-Skripte](/manuals/editor-scripts/) und [Native Erweiterungen](/manuals/extensions/).

## Hot Reload

Mit Hot Reload kannst du ein laufendes Spiel in Defold aktualisieren. Baue und starte das Spiel, bearbeite eine unterstützte Ressource, speichere sie und wähle **File ▸ Hot Reload**, um die Änderung zu übernehmen. Das funktioniert auch mit einem Debug-Build auf einem als Ziel ausgewählten Gerät.

Beim erneuten Laden eines Skripts ruft Defold `init()` nicht noch einmal auf. Bereits vorhandene Instanzdaten bleiben erhalten. Ein geänderter Anfangswert wird deshalb nicht automatisch in `self` übernommen. Mit `on_reload(self)` kannst du den bestehenden Zustand anpassen. Für einen vollständigen Neustart baust du das Spiel erneut. Wenn ein neu geladenes Lua-Modul eine neue Tabelle zurückgibt, verweisen andere Skripte, die die alte Tabelle gespeichert haben, weiterhin auf diese. Einzelheiten findest du im [Handbuch zu Lua-Modulen](/manuals/modules/).

Mehr dazu im [Handbuch zu Hot Reload](/manuals/hot-reload/).

## Haltepunkte und Debugging {#breakpoints-and-debugging}

Mit dem integrierten Debugger kannst du Haltepunkte setzen, Code schrittweise ausführen und Werte untersuchen. In der Console siehst du die Laufzeitausgaben, unter Build Errors die Fehler beim Bauen. Der Profiler zeigt dir Frame-Zeit, Speicherverbrauch und Rendering-Daten. Build-Berichte zeigen, welche Ressourcen wie viel zur Bundle-Größe beitragen.

Siehe [Spiellogik debuggen](/manuals/debugging-game-logic/) und [Profiling](/manuals/profiling/).

## Automatisierte Arbeitsabläufe {#automated-workflows}

Defold bietet mehrere Schnittstellen für automatisierte Abläufe und KI-gestützte Entwicklung. Mit Editor-Skripten kannst du wiederkehrende Aufgaben automatisieren. Über die mit OpenAPI dokumentierte HTTP-API des Editors können externe Werkzeuge und KI-Agenten Projekte untersuchen, Befehle ausführen und Builds starten. Der HTTP-Dienst der Engine und die Erweiterung Automation Bridge ermöglichen die Untersuchung des laufenden Spiels, simulierte Eingaben und Screenshots. Damit können KI-Programmieragenten wie Codex, Claude Code und Cursor in mehreren Durchläufen Projekte bearbeiten, Spiele bauen, ihr Verhalten testen und Fehler beheben.

Weitere Einzelheiten findest du unter [Automatisierung](/manuals/automation/), [HTTP-API des Editors](/manuals/editor-http-api/), [Engine-Dienst](/manuals/engine-service/) und [Automatisiertes Testen](/manuals/automated-testing/).

---

## Typische Stolperfallen {#common-pitfalls}

### Eine Sammlung als Wurzelknoten behandeln {#treating-a-collection-as-a-root-node}

Eine Defold-Sammlung beschreibt Spielobjekte und ihre Beziehungen. Zur Laufzeit gibt es aber kein Wurzelobjekt für die Sammlung selbst. Um die Objekte in einem Level zu koordinieren, füge ein Spielobjekt mit einem eigenen Skript hinzu. Siehe [Sammlungen und Spielwelten](#collections-and-worlds).

### Eine Hierarchie löschen {#deleting-a-hierarchy}

In Godot löscht `queue_free()` auch die Nachkommen des Knotens. In Defold lässt `go.delete(id)` untergeordnete Spielobjekte bestehen, sofern du nicht ausdrücklich rekursiv löschst. Unter [Fabriken](#factories) findest du ein Beispiel und erfährst, wie du die von einer Sammlungsfabrik erzeugten Objekte wieder löschst.

### Szenenvererbung voraussetzen {#expecting-scene-inheritance}

Defold unterstützt die Szenenvererbung von Godot nicht in gleicher Weise. Die Struktur einer abgeleiteten Szene lässt sich deshalb nicht ebenso frei überschreiben. Du kannst Prototypen und Sammlungen wiederverwenden und ihre Instanzen über Eigenschaften oder Skripte anpassen. Siehe [Sammlungen und Spielwelten](#collections-and-worlds).

### Ein anderes Skript über eine Objektreferenz aufrufen {#calling-another-script-through-an-object-reference}

Der Bezeichner eines Defold-Spielobjekts bietet keinen allgemeinen Zugriff auf Funktionen einer anderen Skriptinstanz. Verwende für die Kommunikation zwischen Komponenten Nachrichten oder lagere gemeinsam genutzte Funktionen in ein Lua-Modul aus. Siehe [Nachrichten und Adressierung](#messages-and-addressing) sowie [Autoloads und gemeinsamer Zustand](#autoloads-and-shared-state).

### Instanzdaten in einer lokalen Variablen auf Dateiebene speichern {#keeping-instance-state-in-a-top-level-local}

Alle Instanzen einer Skriptdatei teilen sich die lokalen Variablen auf Dateiebene. Eine Änderung für eine Instanz kann sich daher auf die anderen auswirken. Speichere den Zustand der einzelnen Instanz in `self`, wie im Abschnitt [Instanzdaten und lokale Daten](#instance-data-vs-local-data) beschrieben.

### Davon ausgehen, dass die Eingabe automatisch aktiv ist {#assuming-input-is-enabled-automatically}

Erst wenn ein Spielobjekt in Defold den Eingabefokus anfordert, können seine Komponenten Eingaben empfangen. Bei einer über einen Proxy geladenen Welt braucht auch das Objekt mit dem Proxy den Fokus. Der Abschnitt [Eingabe](#input) erklärt Eingabebindungen, Fokus und Eingabestapel.

### Automatisches Gleiten bei kinematischen Kollisionsobjekten erwarten {#expecting-automatic-sliding-from-a-kinematic-collider}

Defold erkennt die Kontakte kinematischer Kollisionsobjekte. Das Verhalten von Godots `move_and_slide()` stellt die Engine aber nicht automatisch bereit. Für Bewegung und Kollisionsreaktion ist dein Skript zuständig. Siehe [Physik und Kollisionen](#physics-and-collisions).

### Nur eine der beiden Kollisionsmasken konfigurieren {#configuring-only-one-collision-mask}

Wenn nur eines der beiden Objekte für die Interaktion mit dem anderen konfiguriert ist, wird keine Kollision registriert. Jedes Objekt muss die Gruppe des anderen in seiner Maske enthalten. Siehe [Physik und Kollisionen](#physics-and-collisions).

### 2D-Koordinaten unverändert übernehmen {#copying-2d-coordinates-unchanged}

In Godot und einer typischen 2D-Ansicht in Defold zeigen die Y-Achsen in entgegengesetzte Richtungen. Übernimmst du Bewegungscode unverändert, können sich Objekte in die falsche Richtung bewegen. Auch Bildschirm- und Weltposition können voneinander abweichen, wenn eine Kamera im Spiel ist. Siehe [Koordinaten](#coordinates) sowie [Kameras und Koordinaten](#cameras-and-coordinates).

### GUI-Knoten nach der Z-Koordinate der Spielwelt sortieren {#using-world-z-to-sort-gui-nodes}

Die Z-Position eines GUI-Knotens bestimmt in Defold nicht seine Zeichenreihenfolge. Verwende dafür die Reihenfolge der GUI-Knoten und die Ebenen, wie unter [Zeichenreihenfolge und Ebenen](#draw-order-and-layers) beschrieben.

### Nach einem Hot Reload mit einer Neuinitialisierung rechnen {#expecting-hot-reload-to-restart-the-object}

Wenn du ein Skript per Hot Reload neu lädst, wird `init()` nicht erneut ausgeführt. Der Zustand der Instanz kann daher seine bisherigen Werte behalten. Der Abschnitt [Hot Reload](#hot-reload) beschreibt, wie du mit bestehenden Daten und neu geladenen Modulen umgehst.

### Beim Entladen eines Levels mit dem Zurücksetzen gemeinsamer Daten rechnen {#expecting-a-level-unload-to-clear-shared-state}

Sowohl der Zustand eines Godot-Autoloads als auch zwischengespeicherte Daten eines Lua-Moduls können einen Levelwechsel überdauern. Setze gemeinsame Daten bei Bedarf ausdrücklich zurück. Anders als ein Autoload-Knoten erhält ein Lua-Modul nicht automatisch Callbacks. Siehe [Autoloads und gemeinsamer Zustand](#autoloads-and-shared-state).

## Wie geht es weiter? {#where-to-go-from-here}

Im [Defold Learn Hub](https://defold.com/learn/) findest du alle Handbücher sowie Beispiele, Tutorials, Videos und Kurse für den Einstieg und zur Vertiefung. Zum Weiterlesen empfehlen wir die folgenden Seiten.

- [Bausteine](/manuals/building-blocks/)
- [Adressierung](/manuals/addressing/)
- [Nachrichtenübermittlung](/manuals/message-passing/)
- [Defold-Beispiele](/examples/)
- [Tutorials](/tutorials/)
- [API-Referenz](/ref/go/)

Wenn du nicht weiterkommst, frag im [Defold-Forum](https://forum.defold.com/) oder auf [Discord](https://defold.com/discord/). Mit einem kleinen Beispielprojekt und einer Beschreibung, welches Verhalten aus Godot du nachbilden möchtest, machst du es anderen leichter, dir zu helfen.
