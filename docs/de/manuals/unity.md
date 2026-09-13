---
title: Defold für Unity-Nutzer
brief: Dieser Leitfaden hilft dir beim schnellen Umstieg auf Defold, wenn du bereits Erfahrung mit Unity hast. Er behandelt einige der wichtigsten Konzepte aus Unity und erläutert die entsprechenden Werkzeuge und Methoden in Defold.
---

# Defold für Unity-Nutzer {#defold-for-unity-users}

Wenn du bereits Erfahrung mit Unity hast, hilft dir dieser Leitfaden dabei, schnell produktiv mit Defold zu arbeiten. Er konzentriert sich auf das Wesentliche und verweist auf die offiziellen Defold-Handbücher, wenn du ausführlichere Informationen benötigst.

## Einführung {#introduction}

Defold ist eine vollständig kostenlose, durchgehend plattformübergreifende 3D-Game-Engine mit einem Editor für Windows, Linux und macOS. Der vollständige Quellcode ist auf [GitHub](https://github.com/defold/defold/) verfügbar.

Defold ist auf Leistung ausgelegt, auch auf leistungsschwachen Geräten. Es verwendet ein kleines Komponentenmodell, in dem viele Gameplay-Interaktionen durch Code und Nachrichtenübermittlung verarbeitet werden.

Defold ist viel kleiner als Unity. Die Größe der Engine mit einem leeren Projekt liegt auf allen Plattformen zwischen 1 und 3 MB. Du kannst weitere Teile der Engine entfernen und einige Spielinhalte in [Live Update](/manuals/live-update) auslagern, um sie später separat herunterzuladen. Einen Größenvergleich und weitere Gründe für Defold findest du auf der [Webseite „Warum Defold?“](https://defold.com/why/).

Um Defold an deine Anforderungen anzupassen, kannst du Folgendes selbst schreiben oder vorhandene Lösungen verwenden:

1. Eine vollständig skriptgesteuerte Rendering-Pipeline (Render-Skript + Materialien/Shader) mit einigen Backends zur Auswahl (OpenGL, Vulkan usw.).
2. Code und Komponenten (components) als native Erweiterungen (C++/C#).
3. Editor-Skripte und UI-Widgets zum Anpassen des Editors.
3. Einen veränderten Build der Engine und des Editors, da der vollständige Quellcode und eine Build-Pipeline verfügbar sind.

Wir empfehlen außerdem ein Video von Game From Scratch über [Defold für Unity-Entwickler](https://www.youtube.com/watch?v=-3CzCbd4QZ0).

---

## Installation

1. Lade Defold für dein Betriebssystem herunter.
2. Entpacke es und starte es.

Das war's. Kein Hub, keine Installation zusätzlicher SDKs, Toolchains oder Plattform-Bundles. Deshalb sagen wir, dass Defold keine Einrichtung benötigt.

Weitere Informationen findest du in diesem kurzen [Installationshandbuch](/manuals/install/).

### Versionen {#versions}

Defold wird häufig aktualisiert und hat keinen „LTS“-Versionszweig. Wir empfehlen, immer die neueste Version zu verwenden. Neue Versionen erscheinen regelmäßig, normalerweise monatlich, mit einer öffentlichen Betaphase von etwa zwei Wochen. Du kannst Defold direkt im Editor aktualisieren.

---

## Willkommensbildschirm {#welcome-screen}

Defold begrüßt dich mit einem Willkommensbildschirm ähnlich dem Unity Hub, auf dem du zuletzt verwendete Projekte öffnen kannst:

![Vergleich der Willkommensbildschirme](images/unity/unity_defold_start.png)

Oder du beginnst ein neues Projekt mit:
- `Templates` - grundlegenden leeren Projekten für einen schnelleren Einstieg auf einer bestimmten Plattform oder in einem bestimmten Genre,
- `Tutorials` - geführten Lerneinheiten, die dir bei deinen ersten Schritten helfen,
- `Samples` - offiziellen oder von der Community beigetragenen Anwendungsfällen und Beispielen,

![Vergleich der Vorlagen auf dem Willkommensbildschirm](images/unity/unity_defold_templates.png)

Wenn du dein erstes Projekt erstellst und/oder öffnest, wird es im Defold-Editor geöffnet.

## Hallo Welt {#hello-world}

So kannst du schnell etwas in Defold umsetzen: Befolge die Schritte und kehre anschließend zurück, um den Rest des Handbuchs zu lesen.

1. Wähle unter `Templates` ein leeres Projekt aus, gib ihm unter `Title` einen Namen, wähle einen Speicherort und erstelle es mit einem Klick auf `Create New Project`. Es wird im Defold-Editor geöffnet.
![Hallo Welt, Schritt 1](images/unity/helloworld_1.png)
2. Öffne links im Bereich `Assets` den Ordner `main` und doppelklicke auf `main.collection`, um die Datei zu öffnen.
3. Klicke rechts im Bereich `Outline` mit der rechten Maustaste auf `Collection` und wähle `Add Game Object`.
![Hallo Welt, Schritt 2](images/unity/helloworld_2.png)
4. Klicke mit der rechten Maustaste auf das erstellte Spielobjekt (game object) `go` und wähle `Add Component` und dann `Label`.
![Hallo Welt, Schritt 3](images/unity/helloworld_3.png)
5. Gib darunter auf der linken Seite im Bereich `Properties` etwas in die Eigenschaft `Text` ein.
6. Ziehe die Beschriftung in der zentralen Szenenansicht ungefähr an die Position `(480,320,0)` und lege sie dort ab, oder ändere ihre Position unter `Properties`: `Position`.
![Hallo Welt, Schritt 4](images/unity/helloworld_4.png)
7. Nachdem du die Position der Beschriftung geändert hast, speichere das Projekt über `File` -> `Save All` oder mit der Tastenkombination <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>Cmd</kbd>+<kbd>S</kbd> auf dem Mac).
8. Erstelle einen Build deines Projekts über `Project` -> `Build` oder mit der Tastenkombination <kbd>Ctrl</kbd>+<kbd>B</kbd> (<kbd>Cmd</kbd>+<kbd>B</kbd> auf dem Mac).
![Hallo Welt, Schritt 5](images/unity/helloworld_5.png)

Du hast gerade deinen ersten Projekt-Build in Defold erstellt und solltest deinen Text im Fenster sehen. Die Konzepte Spielobjekt und Komponente sollten dir vertraut sein. Sammlungen (collections), Outline, Eigenschaften und der Grund, warum wir die Beschriftung ein Stück nach rechts oben verschieben mussten, werden im Folgenden erklärt.

---

## Überblick über den Defold-Editor {#defold-editor-overview}

Wir stellen den Defold-Editor hier aus der Perspektive dessen vor, was Unity-Nutzer anfangs wissen möchten. Wir empfehlen dir aber, anschließend das vollständige [Handbuch zum Editor](/manuals/editor) zu lesen.

### Vergleich der Editoren {#editors-comparison}

Der erste Unterschied zwischen Unity und Defold, der dir auffallen wird, ist das Standardlayout des Editors. Wir zeigen einen Unity-Editor mit einem leicht angepassten Layout, das dem Standardlayout von Defold entspricht. Die Editoren stehen nebeneinander, damit sich die Hauptbereiche leichter visuell vergleichen lassen und du die Unity-Registerkarten leichter wiedererkennst.

![Vergleich der Editoren](images/unity/defold_unity_editor.png)

Standardmäßig öffnet sich der Defold-Editor mit einer orthografischen 2D-Vorschau. Wenn du an einem 3D-Projekt arbeitest oder eine Ansicht möchtest, die Unity stärker ähnelt, empfehlen wir, von 2D zu 3D zu wechseln, indem du in der Werkzeugleiste den Schalter `2D` deaktivierst und die Kameraprojektion auf perspektivisch umstellst, indem du den Schalter `Perspective` aktivierst:

![Defold-Werkzeugleiste](images/unity/defold_2d.png)

Du kannst auch die `Grid Settings` in der Werkzeugleiste anpassen, um wie in Unity die `Y`-Ebene zu verwenden:

![Defold-3D-Einstellungen](images/unity/defold_3d.png)

### Überblick über die Bereiche in Defold {#defold-panes-overview}

Der Defold-Editor ist in 6 Hauptbereiche unterteilt.

![Editor 2](images/editor/editor_overview.png)

Im Folgenden werden die Bezeichnungen und funktionalen Unterschiede von Defold verglichen:

| Defold | Unity | Unterschiede |
|---|---|---|
| 1. Assets | Project (Assets Browser) | In Defold ist der Bereich Assets links angedockt. Defold erstellt keine `meta`-Dateien. |
| 2. Main Editor | Scene View | Der Defold-Editor ist kontextabhängig (unterschiedliche Editoren für unterschiedliche Dateitypen), während Unity separate spezialisierte Fenster verwendet (z. B. Animator, Shader Graph). Defold hat außerdem einen integrierten Code-Editor. |
| 3. Outline | Hierarchy | Defold zeigt nur die aktuell geöffnete Datei oder das ausgewählte Element (Spielobjekt oder Komponente), keine globale Hierarchie. |
| 4. Properties | Inspector | Defold zeigt nur die Eigenschaften der **aktuellen Auswahl** in Outline an, nicht die aller Komponenten im Spielobjekt. |
| 5. Tools | Console | Defold stellt Werkzeuge in Registerkarten wie Console, Curve Editor, Build Errors, Search Results, Breakpoints und Debugger bereit. |
| 6. Changed Files | Unity Version Control (Plastic) | Sobald Git in dein Defold-Projekt integriert ist, werden hier geänderte Dateien angezeigt. Du kannst Git weiterhin extern verwenden. |

Weitere nützliche Bezeichnungen rund um den Editor:

| Defold | Unity | Unterschiede |
|---|---|---|
| Game Build | Game Preview | Zeigt das laufende Spiel, dessen Build mit der Engine erstellt wurde. Defold kann mehrere Instanzen des Spiels aus dem Editor starten, ähnlich dem Multiplayer Play Mode von Unity 6+. In Defold läuft das Spiel immer in einem separaten Fenster und ist nicht angedockt. Defold kann das Spiel auch auf einem externen Gerät ausführen (z. B. einem Mobiltelefon), ähnlich wie Unity Remote. |
| Tabs | Tabs | Defold ermöglicht die Bearbeitung nebeneinander in zwei Bereichen innerhalb der Ansicht Main Editor. Registerkarten und Bereiche sind in einem einzigen Editorfenster angedockt; die Sichtbarkeit der Bereiche lässt sich umschalten (<kbd>F6</kbd>, <kbd>F7</kbd>, <kbd>F8</kbd>), und ihre Größe lässt sich anpassen. |
| Toolbar | Toolbar / Scene View Options | Erst in neueren Unity-Versionen wurden die Transformationswerkzeuge ähnlich wie in Defold in die Szenenansicht verschoben. |
| Console | Console | Die Defold-Konsole lässt sich nicht abkoppeln. Build-Fehler werden in Defold in einer separaten Registerkarte `Build Errors` angezeigt. |
| Build Errors | Kompilierungsfehler in Console | Lua-Skripte werden interpretiert, daher gibt es keine Kompilierungsfehler. Für dein Projekt wird jedoch ein Build erstellt, bei dem einige Fehler auftreten können. Defold verwendet außerdem einen Lua Language Server zur statischen Analyse von Skripten. |
| Search Results | Search / Project Search | Defold bietet keine Filterung nach Typen und Labels. |
| Curve Editor | Unity Curve Editor | Der Curve Editor von Defold ermöglicht nur das Bearbeiten von Kurven für Partikeleffekt-Eigenschaften. |
| [Debugger](/manuals/debugging/) | Visual Studio Debugger | Der Debugger ist ohne weitere Einrichtung vollständig in Defold integriert. Es gibt eine zusätzliche Registerkarte, um Haltepunkte zu verfolgen, zu aktivieren und zu deaktivieren. |

---

## Grundlegende Konzepte {#key-concepts}

Wenn man sie ausreichend verallgemeinert, sind die grundlegenden Konzepte der meisten Game-Engines sehr ähnlich. Sie sollen Entwicklern das Erstellen von Spielen erleichtern, ähnlich dem Zusammensetzen von Bausteinen, während sie komplexe und plattformbezogene Aufgaben selbst übernehmen.

### Bausteine {#building-blocks}

Defold arbeitet mit nur wenigen grundlegenden Bausteinen:

![Bausteine](images/unity/blocks.png)

Weitere Informationen findest du im vollständigen Handbuch zu den [Defold-Bausteinen](/manuals/building-blocks/).

### Spielobjekte  {#game-objects}
Defold verwendet ähnlich wie Unity **„Spielobjekte“**. In beiden Engines sind Spielobjekte Datencontainer mit einem Bezeichner (ID), und alle haben Transformationen: Position, Drehung und Skalierung. In Defold ist die Transformation jedoch integriert und keine separate Komponente.

Du kannst Eltern-Kind-Beziehungen zwischen Spielobjekten erstellen. In Defold ist dies nur im Editor innerhalb einer „Sammlung“ (unten erläutert) oder dynamisch in einem Skript möglich. Spielobjekte können andere Spielobjekte nicht wie in Unity als verschachtelte Objekte enthalten.

### Komponenten {#components}
In beiden Engines lassen sich Spielobjekte mit **„Komponenten“** erweitern. Defold stellt einen minimalen Satz wesentlicher Komponenten bereit. Es wird weniger zwischen 2D und 3D unterschieden als in Unity (z. B. bei Kollidern), daher gibt es insgesamt weniger Komponenten, und einige aus Unity könnten dir fehlen.

#### Komponenten für Verhalten {#behaviour-components}

In Unity bezeichnet „Komponente“ normalerweise ein `MonoBehaviour`, das an ein `GameObject` angehängt ist. Du kannst eigene Komponenten erstellen, indem du von `MonoBehaviour` erbst, oder integrierte Komponenten wie Light, einige Physikfunktionen und sonstige Dinge verwenden, und so weiter und so fort.

In Defold bezieht sich Komponente ausschließlich auf das, was den integrierten Komponenten in Unity oder Ähnlichem entspricht. Defold behandelt ein Skript jedoch nicht als MonoBehaviour und verlangt außer dem Erstellen von Listener-Ereignissen/Callbacks keine ausdrückliche „Kennzeichnung“, um es an ein Spielobjekt anzuhängen.

Benutzerdefiniertes Gameplay-Verhalten wird normalerweise nicht in Form vieler separater Skriptkomponenten zu demselben Spielobjekt hinzugefügt. Stattdessen wird es üblicherweise in Lua-Modulen implementiert und von einem zentralen `.script` verwendet oder von einem übergeordneten Systemskript verarbeitet, das viele Objekte steuert. Der Abschnitt zum Schreiben von Code weiter unten erläutert dies ausführlicher.

Lies [hier mehr über Defold-Komponenten](/manuals/components/).

Die folgende Tabelle zeigt ähnliche Unity-Komponenten zum schnellen Nachschlagen, mit Links zum jeweiligen Handbuch der Defold-Komponente:

| Defold | Unity | Unterschiede |
|---|---|---|
| [Sprite](/manuals/sprite/) | Sprite Renderer | In Defold kannst du die Einfärbung (Farbeigenschaft) nur über Code ändern. |
| [Kachelkarte (tile map)](/manuals/tilemap/) | Tilemap / Grid | Defold hat einen integrierten Kachelkarten-Editor, der quadratische Raster unterstützt (es gibt aber eine Erweiterung z. B. für [Hexagon](https://github.com/selimanac/defold-hexagon/)) und keine integrierten Regeln zum automatischen Anordnen von Kacheln bietet. Werkzeuge wie [Tiled](https://defold.com/assets/tiled/), [TileSetter](https://defold.com/assets/tilesetter/) oder [Sprite Fusion](https://defold.com/assets/spritefusion/) bieten Exportmöglichkeiten für Defold. |
| [Beschriftung](/manuals/label/) | Text / TextMeshPro | Seit Defold 1.13.2 unterstützen Beschriftungskomponenten und GUI-Textknoten integriertes [Rich-Text-Markup](/manuals/font-richtext/) für Farben, Farbverläufe, Konturen und animierte Effekte. Eine separate [RichText-Erweiterung](https://defold.com/assets/richtext/) ist ebenfalls verfügbar. |
| [Audio](/manuals/sound/) | AudioSource | Defold hat nur eine globale Audioquelle (keine räumliche). Es gibt eine offizielle [FMOD-Erweiterung](https://github.com/defold/extension-fmod) für Defold. |
| [Fabrik](/manuals/factory/) | Prefab Instantiate() | In Defold ist eine Fabrik (factory) eine Komponente mit einem bestimmten Prototyp (Prefab). |
| [Sammlungsfabrik](/manuals/collection-factory/) | - (Keine direkt entsprechende Komponente) | Eine Sammlungsfabrik (collection factory) in Defold kann mehrere Spielobjekte mit Eltern-Kind-Beziehungen gleichzeitig erzeugen. |
| [Kollisionsobjekt](/manuals/physics-objects) | Rigidbody + Collider | In Defold sind Physikobjekte und Kollisionsformen in einer einzigen Komponente zusammengefasst. |
| [Kollisionsformen](/manuals/physics-shapes/)  | BoxCollider / SphereCollider / CapsuleCollider | In Defold werden Formen (Quader, Kugel, Kapsel) innerhalb der Kollisionsobjekt-Komponente konfiguriert. Beide unterstützen Kollisionsformen aus Kachelkarten und Daten für konvexe Hüllen. |
| [Kamera](/manuals/camera/) | Camera | In Unity hat die Kamera einige zusätzliche integrierte Einstellungen für Rendering und Nachbearbeitung, während Defold die benutzerdefinierte Steuerung über das Render-Skript dem Nutzer überlässt. |
| [GUI](/manuals/gui/) | UI Toolkit / Unity UI / uGUI Canvas | Defolds GUI ist eine leistungsfähige Komponente zum Erstellen vollständiger Benutzeroberflächen und Vorlagen. Unity hat keine entsprechende einzelne UI-Komponente, sondern mehrere UI-Frameworks. Defold hat auch eine Erweiterung für [Erweiterung](https://github.com/britzl/extension-imgui). |
| [GUI-Skript](/manuals/gui-script/) | Unity UI / uGUI-Skripte | Defolds GUI lässt sich über GUI-Skripte mit der dafür vorgesehenen `gui`-API steuern. |
| [Modell](/manuals/model/) | MeshRenderer + Material | In Defold bündelt eine Modellkomponente eine 3D-Modelldatei, Texturen und ein Material mit Shadern. |
| [Mesh](/manuals/mesh/) | MeshRenderer / MeshFilter / Procedural Mesh | In Defold ist Mesh eine Komponente zur Verwaltung einer Menge von Vertices über Code. Sie ähnelt einem Defold-Modell, arbeitet aber auf einer noch niedrigeren Ebene. |
| [ParticleFX](/manuals/particlefx/) | Particle System | Defolds Partikeleditor unterstützt 2D-/3D-Partikeleffekte mit vielen Eigenschaften und ermöglicht es dir, sie mit Kurven im Curve Editor über die Zeit zu animieren. Er bietet weder Spuren noch Kollisionen. |
| [Skript](/manuals/script/) | Script | Weitere Informationen zu Unterschieden bei der Programmierung findest du unten. |

#### Erweiterungen und benutzerdefinierte Komponenten {#extensions-and-custom-components}

Defold bietet außerdem offizielle [Spine](/extension-spine/)- und [Rive](/extension-rive/)-Komponenten über Erweiterungen an.

Du kannst mit nativen Erweiterungen auch eigene [benutzerdefinierte Komponenten](https://github.com/defold/extension-simpledata) erstellen, wie beispielsweise diese von der Community entwickelte [Komponente zur Objektinterpolation](https://github.com/indiesoftby/defold-object-interpolation).

Einige Unity-Komponenten haben in Defold keine direkt verfügbare Entsprechung, zum Beispiel Audio Listener, Light, Terrain, LineRenderer, TrailRenderer, Cloth oder Animator. Diese gesamte Funktionalität lässt sich jedoch in Skripten implementieren, und es sind bereits Lösungen verfügbar: beispielsweise verschiedene Beleuchtungs-Pipelines, die Mesh-Komponente zum Erzeugen beliebiger Meshes (einschließlich Gelände) oder [Hyper Trails](https://defold.com/assets/hypertrails/) für anpassbare Spureneffekte. Defold könnte in Zukunft auch neue integrierte Komponenten hinzufügen, etwa Lichtquellen.

### Ressourcen {#resources}

Einige Komponenten benötigen ähnlich wie in Unity **„Ressourcen“ (resources)**, zum Beispiel benötigen Sprites und Modelle Texturen. Einige davon werden in der folgenden Tabelle verglichen:

| Defold | Unity | Unterschiede |
|---|---|---|
| [Atlas](/manuals/atlas/) | Sprite Atlas / Texture2D | Defold hat auch eine [Erweiterung für Texture Packer](https://defold.com/extension-texturepacker/). |
| [Kachelquelle](/manuals/tilesource/) | Tile Palette + Asset | In Defold lässt sich eine Kachelquelle als Textur für Kachelkarten, aber auch für Sprites oder Partikel verwenden. |
| [Schriftart](/manuals/font/) | Font | Wird von der Beschriftungskomponente oder von Textknoten in Defolds GUI verwendet, ähnlich wie Text/TextMeshPro in Unity. |
| [Material](/manuals/material/) | Material | In Defold heißen Shader Vertex-Programm und Fragment-Programm. |

### Sammlung im Vergleich zur Szene {#collection-vs-scene}

In Defold können Spielobjekte und Komponenten ähnlich wie Unity-Prefabs in separaten Dateien liegen oder in einer zusammenführenden **„Sammlungsdatei“** definiert sein.

Eine Sammlung in Defold ist im Wesentlichen eine Textdatei mit einer statischen Szenenbeschreibung. Sie ist **kein** Laufzeitobjekt. Sie definiert lediglich, welche Spielobjekte im Spiel instanziiert werden sollen und wie Eltern-Kind-Beziehungen zwischen diesen Objekten hergestellt werden sollen.

#### Spielwelten {#game-worlds}

Unity-Szenen teilen standardmäßig denselben globalen Spielzustand und dieselbe Physiksimulation, also effektiv dieselbe *Welt* (*Spielwelt*). In Defold hast du zwei Möglichkeiten:
1. Instanziiere Spielobjekte aus einer einzelnen Spielobjektdatei über eine `Factory` oder aus einer Sammlungsdatei über eine `Collection Factory` in einer bestimmten, bereits instanziierten *Welt*, ähnlich wie Prefabs.
2. Erstelle zur Laufzeit eine separate *Spielwelt* mit eigenen Spielobjekten, einer eigenen Physikwelt, eigenen Engine-Vorgängen und einem eigenen Namensraum für Adressen über eine beim Start geladene Sammlung oder über eine Komponente vom Typ `Collection Proxy`, einen Sammlungs-Proxy (collection proxy).

Fabriken und Proxy-Komponenten werden ebenfalls weiter unten erläutert.
Lies mehr über Sammlungen im [Handbuch zu den Bausteinen](/manuals/building-blocks/#collections).

---

## Projektressourcen und Assets {#project-resources-and-assets}

Unity und Defold speichern Spielinhalte beide im Projektverzeichnis, unterscheiden sich aber darin, wie Assets erfasst und vorbereitet werden.

### Assets

Unity legt Assets unter `Assets/` ab und erzeugt `.meta`-Dateien. Defold hat keine Metadateien. Das Projekt in Defold entspricht einfach deiner Ordnerstruktur, genau wie auf dem Datenträger, und der Bereich `Assets` bildet sie immer ab.

### Ressourcenformate {#resource-formats}

Unity importiert Assets und konvertiert sie im Hintergrund in andere Formate. In Defold arbeitest du direkt mit Quellressourcen (`.png`, `.gltf`, `.wav`, `.ogg` usw.) und weist sie `Components` zu.

Unity kann ein einzelnes Bild als Sprite verwenden. In Defold lassen sich Bilder direkt für Modelle/Meshes verwenden, aber Sprites/GUI/Kachelkarten/Partikel benötigen einen Atlas (gepackte Texturen) oder eine Kachelquelle (Kacheln auf einem Raster).

Die meisten Defold-Ressourcen werden als Text gespeichert, was sich gut für die Versionsverwaltung eignet.

### Bibliotheks-Cache {#library-cache}

Unity erzeugt einen Ordner `Library/` für importierte Assets. Defold hat kein solches Verzeichnis; Assets werden beim Erstellen von Builds verarbeitet, und die Ergebnisse werden im Build-Ordner zwischengespeichert (sowie optional in lokalen/entfernten Build-Caches).

---

## Code schreiben {#code-writing}

Die Defold-Entsprechung zu `MonoBehaviour`-Skripten ist eine Skriptkomponente, allerdings gibt es einige wissenswerte Unterschiede.

### Lua

Defold-Skripte werden in der dynamisch typisierten Multiparadigmensprache [Lua](https://www.lua.org/) geschrieben.

Es gibt mehrere Arten von Lua-Skripten: `*.script`, `*.gui_script`, `*.render_script`, `*.editor_script` und `*.lua`-Module.

### Teal

Defold unterstützt Transpiler, die Lua-Code erzeugen, zum Beispiel [Teal](https://teal-language.org/), einen statisch typisierten Lua-Dialekt. Diese Funktionalität ist allerdings stärker eingeschränkt und erfordert zusätzliche Einrichtung. Weitere Informationen findest du im [Repository der Teal-Erweiterung](https://github.com/defold/extension-teal).

### Native Erweiterungen in C++/C# {#cc-native-extensions}

In Defold lassen sich native Erweiterungen in mehreren anderen Sprachen schreiben: je nach Zielplattform in C, C++, C#, Objective-C, Java oder JS. Wenn du dich mit C# sehr gut auskennst, ist es technisch möglich, den Großteil deiner Spiellogik in einer C#-Erweiterung zu strukturieren und lediglich aus einem kleinen Lua-Startskript aufzurufen. Dies erfordert jedoch fortgeschrittene API-Kenntnisse und wird Anfängern nicht empfohlen.

Lies mehr über Erweiterungen im [Defold-Handbuch zu nativen Erweiterungen](/manuals/extensions/).


### Von MonoBehaviours zu Lua-Modulen {#from-monobehaviours-to-lua-modules}

Unity hat ein offenes Skriptmodell. Da `MonoBehaviour` der wichtigste Weg ist, Verhalten im Editor hinzuzufügen, beginnen viele Unity-Projekte mit einem Steuerungsskript pro wichtigem GameObject: `PlayerController`, `EnemyController`, `BulletController`, `GameManager`, `EnemyManager` und so weiter.

Defold gibt seine Standardarchitektur konkreter vor. Ein Spielobjekt kann ein `.script` haben, aber du musst nur selten für jedes Spielobjekt ein Skript erstellen. Dank Defolds leistungsfähiger Adressierung und Nachrichtenübermittlung kann ein einzelnes Skript Hunderte oder Tausende anderer Objekte und ihre Komponenten steuern, ohne dass diese eigene Skripte haben. Passend zu jedem Spielobjekt ein Skript zu erstellen, ist selten erforderlich und kann zu kontraproduktiver Komplexität führen.

Für wiederverwendbares Gameplay-Verhalten gehen Unity-Entwickler oft zur Komposition über: kleinere `MonoBehaviour`-Skripte wie `Health.cs`, `Attack.cs` oder `EnemyFinder.cs`, die an dasselbe GameObject angehängt werden. In Defold behältst du normalerweise ein angehängtes `.script` als zentralen Koordinator bei und legst wiederverwendbare Logik in gewöhnlichen Lua-Modulen ab.

In Unity könnte diese Komposition so aussehen:

```text
Player
├── PlayerMovement.cs
├── PlayerAttack.cs
├── EnemyFinder.cs
└── Health.cs
```

In Defold werden dieselben Zuständigkeiten oft zwischen einem angehängten Skript und wiederverwendbaren Modulen aufgeteilt:

```text
player.go
├── sprite
├── collisionobject
└── player.script

modules/
├── player_movement.lua
├── player_attack.lua
├── enemy_finder.lua
└── health.lua
```

Das angehängte `.script` wird zum zentralen Koordinator. Die Lua-Module enthalten wiederverwendbare Logik, ähnlich wie kleine `MonoBehaviour`-Skripte in Unity oft jeweils eine Zuständigkeit abdecken.

```lua
local movement = require "modules.player_movement"
local attack = require "modules.player_attack"
local finder = require "modules.enemy_finder"
local health = require "modules.health"

function init(self)
    self.movement = movement.new(self)
    self.attack = attack.new(self)
    self.finder = finder.new(self)
    self.health = health.new(self)
end

function update(self, dt)
    self.movement:update(dt)
    self.attack:update(dt)
    self.finder:update(dt)
end

function on_message(self, message_id, message, sender)
    self.health:on_message(message_id, message, sender)
    self.attack:on_message(message_id, message, sender)
end
```

Der wichtige Unterschied besteht nicht darin, dass Defold modulare Architektur verhindert, sondern darin, wo die Komposition stattfindet und wie Gameplay-Code kommuniziert:

| Unity | Defold |
|---|---|
| Hänge mehrere `MonoBehaviour`-Skripte im Inspector an | Hänge ein `.script` an und setze Lua-Module im Code zusammen |
| Verwende `GetComponent<T>()` oder serialisierte Felder, um Verhalten zu verbinden | Speichere Modulinstanzen in `self` und verwende Adressen/Nachrichten zwischen Objekten |
| Jede Komponente kann eigene Lebenszyklusmethoden haben | Das zentrale Skript leitet `init()`, `update()`, `on_message()`, `final()` usw. weiter |
| Viele Architekturstile sind möglich | Nachrichtenorientierte, explizite Komposition im Code ist die übliche Praxis |

Das kann sich anfangs ungewohnt anfühlen, insbesondere wenn du Verhalten gewöhnlich durch das Hinzufügen von Komponenten im Inspector konfigurierst. In Defold lassen sich viele Dinge, die du in Unity vielleicht visuell konfigurierst, stattdessen über Code erstellen, verbinden, aktivieren, deaktivieren oder aktualisieren. Defolds Nachrichtensystem hilft, Logik zu entkoppeln: Der Absender sendet Daten an eine Adresse, und der Empfänger entscheidet, was er damit macht.

Obwohl dieser Ansatz empfohlen wird, ist er nicht vorgeschrieben. Du kannst deine Skripte weiterhin so schreiben, wie du möchtest, einschließlich mehrerer Skripte pro Spielobjekt oder eines stärker objektorientierten Programmierstils. Es gibt sogar Bibliotheken, die dich dabei unterstützen ([defold-oop](https://github.com/xiyoo0812/defold-oop) oder [lua-class](https://github.com/d954mas/lua-class)).

Bei vielen Objekten desselben Typs, etwa Geschossen, Gegnern, Partikeln, Kacheln oder einfachen interaktiven Elementen, ist es oft besser, sie aus einem System- oder Verwaltungsskript zu steuern, statt jedem Objekt ein separates Skript zu geben. Verwende eigene Skripte pro Objekt, wenn ein Objekt einen eigenen relevanten Zustand und eigenes Verhalten hat. Verwende Module für wiederverwendbare Logik. Verwende Systemskripte, wenn ein Skript viele Objekte effizient steuern kann.

Ein Beispiel dafür, wie du Skripteigenschaften, Fabriken, Adressierung und Nachrichten in Defold zur Steuerung mehrerer Einheiten nutzt, findest du [hier](https://defold.com/examples/factory/spawn_manager/).

Nützliche Handbücher zum Schreiben von Code:
- [Skripthandbuch](/manuals/script/)
- [Code schreiben](/manuals/writing-code/)
- [Debugging](/manuals/debugging/)


### Integrierter Code-Editor {#built-in-code-editor}

Der Defold-Editor enthält einen integrierten Code-Editor mit Codevervollständigung, Syntaxhervorhebung, schnellem Nachschlagen in der Dokumentation, statischer Codeprüfung und einem integrierten Debugger.

![Defold-Code-Editor](/images/editor/code-editor.png)

### VS Code und andere Editoren {#vs-code-and-other-editors}

Du kannst weiterhin deinen eigenen externen Editor verwenden, wenn du das bevorzugst. Alle Defold-Komponenten und zugehörigen Dateien sind textbasiert, sodass du sie mit jedem Texteditor bearbeiten kannst. Du musst jedoch die korrekte Formatierung und Elementstruktur einhalten, da sie auf Protobuf basieren.

Wenn du VS Code gewohnt bist und damit den Code deines Spiels schreiben möchtest, empfehlen wir, [Defold Kit](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) oder [Defold Buddy](https://marketplace.visualstudio.com/items?itemName=mikatuo.vscode-defold-ide) aus dem Visual Studio Marketplace zu installieren.

Du kannst die Einstellungen des Defold-Editors auch so konfigurieren, dass Textdateien standardmäßig in VS Code (oder einem anderen externen Editor) geöffnet werden. Weitere Informationen findest du unter [Editoreinstellungen](/manuals/editor-preferences/).

### Shader - GLSL {#shaders-glsl}

Defold verwendet ähnlich wie Unity GLSL (die OpenGL Shading Language) für Shader: `Vertex Programs` und `Fragment Programs`. Obwohl Defold keinen Shader Graph wie Unity bietet (was ein Nachteil sein kann), kannst du durch das Schreiben von Code trotzdem entsprechende Shader erstellen.

Lies mehr über Shader im [Shader-Handbuch](/manuals/shader).

#### Materialien {#materials}

Defold verwendet das Konzept `Material`, das `.fp`- und `.vp`-Shader, Sampler (Texturen) und weitere Dinge wie Vertex-Attribute oder Konstanten verbindet.

Lies mehr über Materialien im [Materialhandbuch](/manuals/material).

---

## Nachrichtensystem {#messaging-system}

In Defold halten Objekte keine direkten Referenzen aufeinander. Es gibt kein `GetComponent`, keine objektübergreifenden Methodenaufrufe zwischen Skripten und keinen globalen Szenenzugriff wie in Unity.

Stattdessen kommunizieren Skripte über Nachrichtenübermittlung: Du sendest Nachrichten an andere Skripte, anstatt Methoden aufzurufen oder direkt auf Komponenten zuzugreifen. Was diese Objekte mit den Nachrichten tun, entscheiden sie selbst.

Das kann sich anfangs ungewohnt anfühlen, fördert aber lose Kopplung und verringert enge gegenseitige Abhängigkeiten.


### Eine Nachricht senden {#sending-a-message}

In Unity sieht die Kommunikation normalerweise so aus:

```c#
var enemy = GameObject.Find("Enemy");
enemy.GetComponent<EnemyAI>().TakeDamage(10);
```

Objekte können also direkt aufeinander verweisen und Methoden in anderen Skripten aufrufen. Alles befindet sich in einem gemeinsamen Szenenraum.

In Defold sendest du eine Nachricht von einem Skript an ein anderes Skript (oder eine andere Komponente):

```lua
msg.post("#my_component", "my_message", { my_name = "Defold" })
```

Und du kannst diese Nachrichten im Skript verarbeiten:

```lua
function on_message(self, message_id, messsage)
    if message_id == hash("my_message") then
        print("Hello ", message.my_name)
    end
end
```

Ignoriere `#` und `hash` vorerst, darauf kommen wir später zurück. Der Rest sollte verständlich sein. Du kannst eine Nachricht an jede Komponente (sogar an dasselbe Skript) eines beliebigen instanziierten Spielobjekts senden.

#### Andere Komponenten als Skripte {#components-other-than-scripts}

Manchmal sendest du Nachrichten beispielsweise an Komponenten vom Typ `Sprite` oder `Collision`, um sie etwa zu aktivieren oder zu deaktivieren. Manchmal senden `Components` Nachrichten an dein Skript, zum Beispiel bei einer Kollision, damit du sie verarbeiten kannst. Defold verwendet intern dasselbe Nachrichtensystem für Engine-Ereignisse und Gameplay-Kommunikation. 

Das Nachrichtensystem ähnelt etwas Unitys SendMessage oder Ereignissystemen, allerdings unterscheiden sich die Adressierung und die Konventionen.

Weitere Informationen findest du im [Handbuch zur Nachrichtenübermittlung](/manuals/message-passing/).

### Adressierung {#addressing}

Objekte und Komponenten in Defold werden durch Adressen identifiziert, die als URLs bezeichnet werden.

Jedes instanziierte Objekt und jede Komponente hat eine eigene eindeutige Adresse, und du musst keinen Szenengraphen durchlaufen, um sie zu finden. Dadurch ist die Adressierung explizit und direkt.

Eine einfache URL in Defold könnte so aussehen:
```lua
"/player"
```

Dies ist *konzeptionell* ähnlich wie:
```c#
GameObject.Find("player")
```

Nun erklären wir, warum `"/"` oder `"#"` in Adressen verwendet wurden.

Eine Defold-URL besteht ähnlich wie eine [URL](https://en.wikipedia.org/wiki/URL) aus drei Teilen:

```yaml
socket: /path #fragment
```

Oder stärker an Defolds Bezeichnungen angelehnt:

```yaml
collection: /gameobject #component 
```
Die Leerzeichen in den obigen Beschreibungen dienen nur dazu, diese 3 Teile optisch zu trennen.

Vereinfacht gesagt:
1. `collection:` identifiziert den Sammlungskontext, mit `:` am Ende.
2. `/path` identifiziert das Spielobjekt, mit `/` vor der ID.
3. `#fragment` identifiziert die bestimmte Komponente an diesem Objekt (etwa eine Skript-, Sprite- oder Kollisionskomponente), mit `#` vor der ID.

#### Statische Adresse {#static-address}

Diese Bezeichner werden beim Erstellen des jeweiligen Elements festgelegt und ändern sich nie, auch wenn du die Eltern-Kind-Beziehungen änderst. Du kannst sie in Dateien über die Eigenschaft `Id` festlegen oder erhältst sie zur Laufzeit beim Instanziieren durch Aufrufe von `factory.create` oder `collectionfactory.create`.

#### Relative Adressierung {#relative-addressing}

Du musst nicht immer eine vollständige URL verwenden.

Wenn du Nachrichten innerhalb derselben Sammlung (derselben *Welt*) sendest, kannst du den Socket-Teil weglassen:

```yaml
/gameobject #component
```
Wenn du an eine Komponente innerhalb desselben Spielobjekts sendest, kannst du auch den Spielobjekt-Teil weglassen:

```yaml
#component
```

Zwei nützliche Kurzformen sind:
- `#` zum Senden an diese *Skriptkomponente*
- `.` zum Senden an alle Komponenten in diesem *Spielobjekt*

Mit relativer Adressierung und Kurzformen kannst du URLs schreiben, die in unterschiedlichen Kontexten und Spielobjekten wiederverwendbar sind, ohne vollständige Pfade anzugeben.

### Nachrichten an GUI und Rendering {#messaging-to-gui-and-render}

Da Defold die GUI-Welt von der Welt der Spielobjekte trennt, kannst du auch Nachrichten aus den `.scripts` deiner Spielobjekte an `.gui_scripts` senden.

Du kannst außerdem Nachrichten an spezielle Systemnamensräume senden, indem du einen Bezeichner verwendest, der mit `@` beginnt. Das Render-System lässt sich beispielsweise über `@render`: adressieren. Damit kannst du bestimmte integrierte Rendering-Funktionen steuern, etwa die Projektion im Standard-Render-Skript ändern:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

Weitere Informationen findest du im [Handbuch zur Adressierung](/manuals/addressing/).

---

## Prefabs und Instanzen {#prefabs-and-instances}

Unity kann alles in der Szene statisch oder dynamisch instanziieren, und Defold kann das ebenfalls. In Unity nimmst du ein Prefab und rufst `Instantiate(prefab)` auf. In Defold stehen dir 3 Komponenten zum Instanziieren von Inhalten zur Verfügung:

- `Factory` - instanziiert ein **einzelnes Spielobjekt** aus einem vorgegebenen Prototyp: einer `*.go`-Datei (Prefab).
- `Collection Factory` - instanziiert eine **Gruppe von Spielobjekten** mit Eltern-Kind-Beziehungen aus einem vorgegebenen Prototyp: einer `*.collection`-Datei.
- `Collection Proxy` - **lädt** und instanziiert eine neue *Welt* aus einer `*.collection`-Datei.

### Fabrik {#factory}

Sobald du eine Komponente vom Typ `Factory` definiert und ihre Eigenschaft `Prototype` auf die passende Spielobjektdatei gesetzt hast, genügt zum Erzeugen einer Instanz folgender Codeaufruf:

```lua
factory.create("#my_factory")
```

Dieser verwendet die Adresse der Komponente, in diesem Fall einen relativen Pfad mit dem Bezeichner `"#my_factory"`.

Er gibt den Bezeichner der neu erstellten Instanz zurück. Wenn du ihn später verwenden möchtest, lohnt es sich daher, ihn in einer Variablen zu speichern:

```lua
local new_instance_id = factory.create("#my_factory")
```

Denk daran, dass du Objekte in Defold nicht manuell in Pools verwalten musst. Die Engine übernimmt das Pooling intern für dich.

Weitere Informationen findest du im [Handbuch zu Fabriken](/manuals/factory/). 

### Sammlungsfabrik {#collection-factory}

Der Unterschied zwischen den Komponenten `Factory` und `Collection Factory` besteht darin, dass eine Sammlungsfabrik **mehrere** Spielobjekte gleichzeitig erzeugen und beim Erstellen die Eltern-Kind-Beziehungen entsprechend der `*.collection`-Datei festlegen kann.

Diese Unterscheidung gibt es in Unity nicht; es hat kein eigenes Konzept, das Defolds Sammlungsfabrik entspricht. Die ähnlichste Entsprechung ist ein verschachteltes Prefab, das eine Hierarchie von Objekten enthält.

Sie gibt eine **Tabelle** mit den IDs aller erzeugten Instanzen zurück:

```lua
local spawned_instances = collectionfactory.create("#my_collectionfactory")
```

Weitere Informationen findest du im [Handbuch zu Sammlungsfabriken](/manuals/collection-factory/).

#### Benutzerdefinierte Eigenschaften von Instanzen {#custom-properties-of-instances}

Beim Aufruf von `factory.create()` oder `collectionfactory.create()` kannst du auch optionale Parameter wie Position, Drehung, Skalierung und Skripteigenschaften angeben. So kannst du genau steuern, wie und wo die Instanz erscheint und wie sie sich verhält, zum Beispiel:

```lua
local scale_2d = vmath.vector3(0.5, 0.5, 1.0)
factory.create("#my_factory", my_position, my_rotation, my_properties, scale_2d)
```

Bei den optionalen Argumenten stehen die Eigenschaften vor der Skalierung. Verwende einen `vector3`, dessen Z-Wert ausdrücklich auf `1.0` gesetzt ist, wenn du nur die X- und Y-Achse eines 2D-Objekts skalierst; ein numerischer Skalierungsfaktor wird gleichmäßig auf alle drei Achsen angewendet.

#### Dynamisches Laden {#dynamic-loading}

Sowohl in Komponenten vom Typ `Factory` als auch vom Typ `Collection Factory` kannst du einen Prototyp für das dynamische Laden von Ressourcen markieren. Seine umfangreichen Assets werden dann nur bei Bedarf in den Speicher geladen und entladen, wenn sie nicht mehr verwendet werden.

Weitere Informationen findest du im [Handbuch zur Ressourcenverwaltung](/manuals/resource/). 

### Sammlungs-Proxy {#collection-proxy}

Der `Collection Proxy` verweist auf eine bestimmte `*.collection`-Datei. Statt die Objekte wie Fabriken in die *aktuelle Welt* einzufügen, **lädt und instanziiert er eine neue Spielwelt**. Das ähnelt dem Laden einer vollständigen Szene in Unity, allerdings mit strikterer Trennung.

In Unity könntest du eine additive Szene so laden:

```c#
SceneManager.LoadSceneAsync("Level2", LoadSceneMode.Additive);
```

In Defold lädst du die neue Sammlung, indem du einfach eine Nachricht an die Komponente `Collection Proxy` sendest:

```lua
msg.post("#myproxy", "load")
```

1. Wenn du dem Proxy die Nachricht `"load"` sendest (oder `"async_load"` zum asynchronen Laden), weist die Engine Speicher für eine neue Welt zu, instanziiert dort alles aus dieser Sammlung und hält die Welt isoliert.
2. Nach dem Laden sendet der Proxy eine Nachricht `"proxy_loaded"` zurück, die anzeigt, dass die Welt bereit ist.
3. Anschließend sendest du normalerweise die Nachrichten `"init"` und `"enable"`, damit die Objekte in dieser neuen Welt ihren normalen Lebenszyklus beginnen.

Für die Kommunikation zwischen den geladenen Welten musst du explizite Nachrichtenübermittlung mit URLs verwenden, die den Weltnamen enthalten (`collection:`, den ersten Teil der URL).

Diese Isolation kann bei der Implementierung von Levelübergängen, Minispielen oder großen modularen Systemen ein großer Vorteil sein: Sie verhindert unbeabsichtigte Interaktionen und ermöglicht bei Bedarf außerdem eine separate Steuerung des zeitlichen Ablaufs der Aktualisierungen (z. B. für Pausen oder Zeitlupe).

Wenn du in Unity schon einmal mehrere Szenen verwendet hast, die sich unabhängig voneinander verhalten mussten, kannst du dir einen `Collection Proxy` als Möglichkeit vorstellen, dieses Konzept direkt in Defold umzusetzen.

Weitere Informationen findest du im [Handbuch zu Sammlungs-Proxys](/manuals/collection-proxy/).

---

## Anwendungslebenszyklus {#application-lifecycle}

Du kennst bereits eine Reihe von Unity-Lebenszyklusereignissen: `Awake`, `Start`, `Update`, `FixedUpdate`, `LateUpdate`, `OnDestroy` oder `OnApplicationQuit`.

Defold hat ebenfalls einen klar definierten Anwendungslebenszyklus, aber die Konzepte und Begriffe unterscheiden sich. Defold stellt die Lebenszyklusphasen über eine Reihe vordefinierter Lua-Callbacks bereit, die von der Engine während der Initialisierung, in jedem Frame und bei der Finalisierung aufgerufen werden.

Hier ein Vergleich:

| Defold | Unity | Anmerkung |
|-|-|-|
| `init()` | `Awake()` / `Start()` / `OnEnable()`| Defold hat einen einzigen Einstiegspunkt und Callback für die Initialisierung: init(). Er wird beim Erstellen jeder Komponente aufgerufen. |
| `on_input` | Eingabemethoden | Defold empfängt Eingaben, wenn [der Eingabefokus für das Skript gesetzt ist](/manuals/input/#input-focus). Wird in der Aktualisierungsschleife zuerst verarbeitet. |
| `fixed_update()` | `FixedUpdate()` | Wird mit festem Zeitschritt aufgerufen. Um dies in Defold zu aktivieren, musst du `Use Fixed Timestep` einschalten; siehe [Details](https://defold.com/manuals/project-settings/#use-fixed-timestep). Seit 1.12.0 wird es vor `update()` ausgeführt. |
| `update()` | `Update()` | Wird einmal pro Frame mit der Zeitdifferenz aufgerufen. |
| `late_update()` | `LateUpdate()` | Wird nach `update()` aufgerufen, unmittelbar bevor der Frame gerendert wird. Seit 1.12.0 verfügbar. |
| `on_message` | Nachrichtenempfänger | Defolds zentraler Callback zum Empfangen von Nachrichten. Wird verarbeitet, wenn sich eine Nachricht in einer Warteschlange befindet. |
| `final` | `OnDisable` / `OnDestroy` / `OnApplicationQuit` | Defold ruft den Callback `final()` für jede Komponente auf, wenn ihr Spielobjekt zur Laufzeit zerstört wird (mit `go.delete()`) oder die Welt/Sammlung entladen wird, und beim Beenden der Anwendung für alle verbleibenden Objekte. |

::: sidenote
Denk daran, dass Defold keine Ausführungsreihenfolge zwischen Komponenten garantiert, wenn mehrere gleichzeitig initialisiert/aktualisiert/entfernt werden. Ein entkoppelter Aufbau wird empfohlen.
:::

### Initialisierung {#initialization}

Stell dir Defolds `init()` so vor, dass es Elemente von Unitys `Awake()`, `Start()` und `OnEnable()` in einem einzigen Einstiegspunkt vereint. Dort hat die Engine bereits alles eingerichtet, und du kannst den Zustand deiner Komponente sicher vorbereiten.

### Wann werden Nachrichten verarbeitet? {#when-messages-are-handled}

Da du bereits in `init()` Nachrichten senden kannst, werden Nachrichten erstmals direkt nach der Initialisierung zugestellt.

Anschließend werden Nachrichten nach jeder internen Verarbeitungsschleife verarbeitet, sobald sich etwas in einer Warteschlange befindet. Daher kann `on_message()` zum Beispiel auch mehrmals in einer Aktualisierungsschleife aufgerufen werden.

### Aktualisierungsschleife {#update-loop}

In jedem Frame durchläuft Defold eine Folge von Vorgängen: Eingaben verarbeiten, Nachrichten zustellen, Skript- und GUI-Aktualisierungen auslösen, Physik und Transformationen anwenden und zum Schluss die Grafik rendern.

### Finalisierung {#finalization}

In Defold ist das Aufräumen immer an das Löschen oder Entladen der Welt gebunden, und der einzige Ausstiegspunkt pro Komponente ist `final()`.

Ein subtiler Unterschied zum Modell von Unity besteht darin, dass nicht zwischen dem Deaktivieren einer Komponente und dem Beenden der gesamten Anwendung unterschieden wird.

### Rendering

Das Render-Skript (`*.render_script`) ist ein Teil der Rendering-Pipeline, der mit eigenen Callbacks für `init()`, `update()` und `on_message()` ebenfalls am Lebenszyklus teilnimmt. Diese laufen jedoch im Render-Thread und sind von der Logik der Spielobjekt- und GUI-Skripte getrennt.

Weitere Informationen findest du im [Handbuch zum Anwendungslebenszyklus](/manuals/application-lifecycle/).

---

## GUI

Defolds GUI ist ein einziges eigenständiges Framework für Benutzeroberflächen: Menüs, Overlays, Dialoge und andere Elemente, ähnlich wie UI Toolkit oder uGUI mit Canvas.

GUI ist eine Komponente und von Spielobjekten und Sammlungen getrennt. Anstelle von Spielobjekten arbeitest du mit GUI-Knoten, die in einer Hierarchie angeordnet sind und von einem GUI-Skript gesteuert werden.

### GUI-Knoten {#gui-nodes}

Wenn du in Defold eine Komponentendatei vom Typ `*.gui` öffnest, siehst du eine Zeichenfläche, auf der du `"GUI-Knoten"` platzierst. Dies sind die Bausteine der GUI. Du kannst GUI-Knoten der folgenden Typen hinzufügen:

- Box (rechteckige Form mit einer Textur)
- Text (mit beliebiger Schriftart)
- Pie (radial gefülltes Kreissektorelement mit einer Textur)
- ParticleFX
- Template (eine weitere vollständige verschachtelte `.gui`-Datei, ähnlich einem GUI-Prefab)
- und Spine-Knoten, wenn du die Spine-Erweiterung verwendest.

### GUI-Skript {#gui-script}

GUI-Komponenten haben eine spezielle Eigenschaft für GUI-Skripte: Du weist jeder Komponente eine `*.gui_script`-Datei zu, mit der sich das Verhalten der Komponente ändern lässt. Das ähnelt gewöhnlichen Skripten, allerdings wird nicht der Namensraum `go.*` verwendet (der für Spielobjekt-Skripte vorgesehen ist). Stattdessen wird die API des speziellen Namensraums `gui.*` verwendet, die nur innerhalb von GUI-Skripten (`*.gui_script`) funktioniert. Du kannst dir das wie eine separate Szene vorstellen. Unity UI (uGUI) mit Canvas.

### GUI-Rendering

GUI-Elemente werden unabhängig von der Spielkamera gerendert, üblicherweise im Bildschirmkoordinatensystem. Dieses Verhalten lässt sich jedoch in benutzerdefinierten Rendering-Pipelines ändern.

Weitere Informationen findest du im [GUI-Handbuch](/manuals/gui/).

## Wo sind die Sorting Layers? {#where-are-sorting-layers}

Dies ist eine sehr häufige Ursache für Verwirrung beim Umstieg von Unity.

GUI-Komponenten haben `Layers`, was fast genauso funktioniert wie „Sorting Layers“ in Unity. Für andere Komponenten wie `Sprites`, `Tilemaps`, `Models` usw. gibt es aber keine direkte Entsprechung.

Stattdessen kombinierst du normalerweise:
- Eine feine Sortierung über die Z-Achse bei Verwendung einer Standardkamera oder über die Tiefe bei Verwendung einer Kamerakomponente.
- Eine grobe Sortierung über das Render-Skript mit Render-Prädikaten, um anhand von Material-Tags auszuwählen, was gezeichnet werden soll.

Du solltest Unitys Sorting Layers jedoch nicht mit vielen Tags nachahmen, da Tags in Defold ein Mechanismus auf Rendering-Ebene sind. Übermäßige Verwendung kann die Bündelung von Zeichenoperationen (Batching) verhindern und den zusätzlichen Aufwand beim Zeichnen erhöhen.

---

## Wie geht es weiter? {#where-to-go-from-here}

- [Defold-Beispiele](/examples)
- [Tutorials](/tutorials)
- [Handbücher](/manuals)
- [API-Referenzen](/ref/go)
- [FAQ](/faq/faq)

Wenn du Fragen hast oder nicht weiterkommst, sind das [Defold-Forum](//forum.defold.com) oder [Discord](https://defold.com/discord/) gute Anlaufstellen für Hilfe.
