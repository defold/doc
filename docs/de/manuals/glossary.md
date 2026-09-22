---
title: Defold-Glossar
brief: Dieses Handbuch enthält kurze Beschreibungen zu allem, was dir bei der Arbeit mit Defold begegnet.
---

# Defold-Glossar {#defold-glossary}

Dieses Glossar beschreibt kurz alles, was dir in Defold begegnet. In den meisten Fällen findest du einen Link zu weiterführender Dokumentation.

## Animationssatz {#animation-set}

![Animationssatz](images/icons/animationset.png){.left} Eine Animationssatz-Ressource enthält eine Liste von glTF-Dateien oder anderen .animationset-Dateien, aus denen Animationen gelesen werden. Eine .animationset-Datei zu einer anderen hinzuzufügen ist praktisch, wenn du Teilmengen von Animationen für mehrere Modelle gemeinsam verwendest. Einzelheiten findest du im [Handbuch zur Modellanimation](/manuals/model-animation/).

## Atlas

![Atlas](images/icons/atlas.png){.left} Ein Atlas ist eine Zusammenstellung einzelner Bilder, die aus Leistungs- und Speichergründen zu einem größeren Bildbogen zusammengefügt werden. Atlanten können Standbilder oder Bildfolgen für Flipbook-Animationen enthalten. Verschiedene Komponenten (components) verwenden Atlanten, um Grafikressourcen gemeinsam zu nutzen. Weitere Informationen findest du in der [Atlas-Dokumentation](/manuals/atlas).

## Builtins

![Builtins](images/icons/builtins.png){.left} Der Projektordner builtins ist ein schreibgeschützter Ordner mit nützlichen Standardressourcen. Hier findest du den Standard-Renderer, das Standard-Render-Skript, Materialien und mehr. Wenn du eine dieser Ressourcen anpassen musst, kopiere sie einfach in dein Projekt und bearbeite sie nach Bedarf.

## Kamera {#camera}

![Kamera](images/icons/camera.png){.left} Die Kamerakomponente hilft dir festzulegen, welcher Teil der Spielwelt sichtbar sein und wie er projiziert werden soll. Ein häufiger Anwendungsfall besteht darin, eine Kamera am Spielobjekt (game object) des Spielers anzubringen oder ein separates Spielobjekt mit einer Kamera zu verwenden, die dem Spieler mithilfe eines Glättungsalgorithmus folgt. Weitere Informationen findest du in der [Kamera-Dokumentation](/manuals/camera).

## Kollisionsobjekt {#collision-object}

![Kollisionsobjekt](images/icons/collision-object.png){.left} Kollisionsobjekte sind Komponenten, die Spielobjekte um physikalische Eigenschaften erweitern, etwa räumliche Form, Gewicht, Reibung und Rückprallkoeffizient. Diese Eigenschaften bestimmen, wie das Kollisionsobjekt mit anderen Kollisionsobjekten kollidieren soll. Die häufigsten Arten von Kollisionsobjekten sind kinematische Objekte, dynamische Objekte und Trigger. Ein kinematisches Objekt liefert detaillierte Kollisionsinformationen, auf die du manuell reagieren musst. Ein dynamisches Objekt wird von der Physik-Engine automatisch nach den Newtonschen Bewegungsgesetzen simuliert. Trigger sind einfache Formen, die erkennen, ob andere Formen in den Trigger eingetreten sind oder ihn verlassen haben. Einzelheiten zur Funktionsweise findest du in der [Physik-Dokumentation](/manuals/physics).

## Komponente {#component}

Komponenten geben Spielobjekten ein bestimmtes Erscheinungsbild und/oder bestimmte Funktionen, etwa Grafik, Animation, programmiertes Verhalten und Audio. Sie existieren nicht unabhängig, sondern müssen in Spielobjekten enthalten sein. In Defold stehen viele Arten von Komponenten zur Verfügung. Eine Beschreibung der Komponenten findest du im [Handbuch zu den Bausteinen](/manuals/building-blocks).

## Sammlung {#collection}

![Sammlung](images/icons/collection.png){.left} Eine Sammlung (collection) ist Defolds Mechanismus zum Erstellen von Vorlagen, die in anderen Engines „Prefabs“ heißen und mit denen sich Hierarchien von Spielobjekten wiederverwenden lassen. Sammlungen sind Baumstrukturen, die Spielobjekte und andere Sammlungen enthalten. Eine Sammlung wird immer in einer Datei gespeichert und entweder statisch durch manuelles Platzieren im Editor oder dynamisch durch das Erzeugen ihrer Inhalte ins Spiel eingebracht. Eine Beschreibung der Sammlungen findest du im [Handbuch zu den Bausteinen](/manuals/building-blocks).

## Sammlungsfabrik {#collection-factory}

![Sammlungsfabrik](images/icons/collection-factory.png){.left} Eine Sammlungsfabrik (collection factory) ist eine Komponente, mit der du Hierarchien von Spielobjekten dynamisch in einem laufenden Spiel erzeugst. Einzelheiten findest du im [Handbuch zu Sammlungsfabriken](/manuals/collection-factory).

## Sammlungs-Proxy {#collection-proxy}

![Sammlung](images/icons/collection.png){.left} Ein Sammlungs-Proxy (collection proxy) wird verwendet, um Sammlungen während der Ausführung einer Anwendung oder eines Spiels zu laden und zu aktivieren. Der häufigste Anwendungsfall für Sammlungs-Proxys ist das Laden von Levels, sobald sie gespielt werden sollen. Einzelheiten findest du in der [Dokumentation zu Sammlungs-Proxys](/manuals/collection-proxy).

## Cubemap

![Cubemap](images/icons/cubemap.png){.left} Eine Cubemap ist ein besonderer Texturtyp, der aus 6 verschiedenen Texturen besteht, die auf die Seiten eines Würfels abgebildet werden. Das ist nützlich zum Rendern von Skyboxen und verschiedenen Arten von Reflexions- und Beleuchtungstexturen.

## Debugging

Irgendwann wird sich dein Spiel unerwartet verhalten und du musst herausfinden, was schiefläuft. Debuggen zu lernen ist eine Kunst. Glücklicherweise enthält Defold einen integrierten Debugger, der dir dabei hilft. Weitere Informationen findest du im [Debugging-Handbuch](/manuals/debugging).

## Anzeigeprofile {#display-profiles}

![Anzeigeprofile](images/icons/display-profiles.png){.left} Die Ressourcendatei für Anzeigeprofile legt GUI-Layouts abhängig von der Ausrichtung, dem Seitenverhältnis oder dem Gerätemodell fest. Sie hilft dir, deine Benutzeroberfläche an alle Arten von Geräten anzupassen. Mehr dazu erfährst du im [Handbuch zu Layouts](/manuals/gui-layouts).

## Fabrik {#factory}

![Fabrik](images/icons/factory.png){.left} In manchen Situationen kannst du nicht alle benötigten Spielobjekte manuell in einer Sammlung platzieren, sondern musst sie dynamisch während des Spiels erzeugen. Beispielsweise kann ein Spieler Geschosse abfeuern, wobei jedes Geschoss dynamisch erzeugt und abgeschossen werden soll, sobald der Spieler den Abzug betätigt. Um Spielobjekte dynamisch aus einem vorab reservierten Pool von Objekten zu erzeugen, verwendest du eine Fabrikkomponente (factory). Einzelheiten findest du im [Handbuch zu Fabriken](/manuals/factory).

## Schriftart {#font}

![Schriftdatei](images/icons/font.png){.left} Eine Schriftressource wird aus einer TrueType- oder OpenType-Schriftdatei erstellt. Sie legt fest, in welcher Größe die Schrift gerendert wird und welche Verzierungen (Kontur und Schatten) die gerenderte Schrift haben soll. Schriftarten werden von GUI- und Beschriftungskomponenten verwendet. Einzelheiten findest du im [Handbuch zu Schriftarten](/manuals/font/).

## Fragment-Shader

![Fragment-Shader](images/icons/fragment-shader.png){.left} Dies ist ein Programm, das auf dem Grafikprozessor für jedes Pixel (Fragment) eines Polygons ausgeführt wird, wenn es auf den Bildschirm gezeichnet wird. Der Fragment-Shader bestimmt die Farbe jedes resultierenden Fragments. Dies geschieht durch Berechnungen, einen oder mehrere Texturzugriffe oder eine Kombination aus Texturzugriffen und Berechnungen. Weitere Informationen findest du im [Shader-Handbuch](/manuals/shader).

## Gamepads

![Gamepads](images/icons/gamepad.png){.left} Eine Gamepads-Ressourcendatei definiert, wie die Eingaben bestimmter Gamepad-Geräte auf einer bestimmten Plattform den Eingabeauslösern für Gamepads zugeordnet werden. Einzelheiten findest du im [Handbuch zur Eingabe](/manuals/input).

## Spielobjekt {#game-object}

![Spielobjekt](images/icons/game-object.png){.left} Spielobjekte sind einfache Objekte, die während der Ausführung deines Spiels eine eigene Lebensdauer haben. Spielobjekte sind Container und werden üblicherweise mit sichtbaren oder hörbaren Komponenten ausgestattet, etwa einer Audiokomponente oder einem Sprite. Durch Skriptkomponenten können sie auch Verhalten erhalten. Du erstellst Spielobjekte und platzierst sie im Editor in Sammlungen oder erzeugst sie zur Laufzeit dynamisch mit Fabriken. Eine Beschreibung der Spielobjekte findest du im [Handbuch zu den Bausteinen](/manuals/building-blocks).

## GUI

![GUI-Komponente](images/icons/gui.png){.left} Eine GUI-Komponente enthält Elemente zum Aufbau von Benutzeroberflächen: Text sowie farbige und/oder texturierte Blöcke. Die Elemente lassen sich in hierarchischen Strukturen organisieren, per Skript steuern und animieren. GUI-Komponenten werden üblicherweise verwendet, um eingeblendete Spielinformationen (HUDs), Menüsysteme und Bildschirmbenachrichtigungen zu erstellen. GUI-Komponenten werden mit GUI-Skripten gesteuert, die das Verhalten der GUI definieren und die Interaktion der Benutzer mit ihr steuern. Mehr dazu erfährst du in der [GUI-Dokumentation](/manuals/gui).

## GUI-Skript {#gui-script}

![GUI-Skript](images/icons/script.png){.left} GUI-Skripte steuern das Verhalten von GUI-Komponenten. Sie steuern GUI-Animationen und die Interaktion der Benutzer mit der GUI. Einzelheiten zur Verwendung von Lua-Skripten in Defold findest du im [Handbuch zu Lua in Defold](/manuals/lua).

## Hot Reload

Mit dem Defold-Editor kannst du Inhalte in einem bereits laufenden Spiel aktualisieren, sowohl auf dem Desktop als auch auf einem Gerät. Diese Funktion ist äußerst leistungsfähig und kann den Arbeitsablauf bei der Entwicklung erheblich verbessern. Weitere Informationen findest du im [Handbuch zu Hot Reload](/manuals/hot-reload).

## Eingabebindung {#input-binding}

![Eingabebindung](images/icons/input-binding.png){.left} Dateien für die Eingabebindung (input binding) definieren, wie das Spiel Hardwareeingaben von Maus, Tastatur, Touchscreen und Gamepad interpretieren soll. Die Datei bindet Hardwareeingaben an übergeordnete _Eingabeaktionen_ wie "jump" und "move_forward". In Skriptkomponenten, die Eingaben empfangen, kannst du programmieren, welche Aktionen das Spiel oder die Anwendung bei bestimmten Eingaben ausführen soll. Einzelheiten findest du in der [Dokumentation zur Eingabe](/manuals/input).

## Beschriftung {#label}

![Beschriftung](images/icons/label.png){.left} Mit der Beschriftungskomponente kannst du jedem Spielobjekt Text hinzufügen. Sie rendert einen Text in einer bestimmten Schriftart im Spielraum auf den Bildschirm. Weitere Informationen findest du im [Handbuch zu Beschriftungen](/manuals/label).

## Bibliothek {#library}

![Spielobjekt](images/icons/builtins.png){.left} Defold ermöglicht es dir, Daten über einen leistungsfähigen Bibliotheksmechanismus zwischen Projekten zu teilen. Damit kannst du gemeinsame Bibliotheken einrichten, auf die du von all deinen Projekten aus zugreifen kannst, entweder für dich allein oder für das gesamte Team. Mehr über den Bibliotheksmechanismus erfährst du in der [Dokumentation zu Bibliotheken](/manuals/libraries).

## Programmiersprache Lua {#lua-language}

Die Programmiersprache Lua wird in Defold verwendet, um Spiellogik zu erstellen. Lua ist eine leistungsfähige, effiziente und sehr kleine Skriptsprache. Sie unterstützt prozedurale Programmierung, objektorientierte Programmierung, funktionale Programmierung, datengetriebene Programmierung und Datenbeschreibung. Mehr über die Sprache erfährst du auf der offiziellen Lua-Website unter https://www.lua.org/ und im [Handbuch zu Lua in Defold](/manuals/lua).

## Lua-Modul {#lua-module}

![Lua-Modul](images/icons/lua-module.png){.left} Mit Lua-Modulen kannst du dein Projekt strukturieren und wiederverwendbaren Bibliothekscode erstellen. Mehr dazu erfährst du im [Handbuch zu Lua-Modulen](/manuals/modules/)

## Material

![Material](images/icons/material.png){.left} Materialien legen durch die Angabe von Shadern und deren Eigenschaften fest, wie verschiedene Objekte gerendert werden sollen. Weitere Informationen findest du im [Handbuch zu Materialien](/manuals/material).

## Nachricht {#message}

Komponenten kommunizieren untereinander und mit anderen Systemen durch Nachrichtenübermittlung. Komponenten reagieren außerdem auf eine Reihe vordefinierter Nachrichten, die sie verändern oder bestimmte Aktionen auslösen. Du sendest Nachrichten, um Grafiken auszublenden oder Physikobjekten einen Anstoß zu geben. Die Engine verwendet Nachrichten außerdem, um Komponenten über Ereignisse zu informieren, etwa wenn Physikformen kollidieren. Der Mechanismus zur Nachrichtenübermittlung benötigt für jede gesendete Nachricht einen Empfänger. Deshalb hat alles im Spiel eine eindeutige Adresse. Um die Kommunikation zwischen Objekten zu ermöglichen, erweitert Defold Lua um die Nachrichtenübermittlung. Defold stellt außerdem eine Bibliothek mit nützlichen Funktionen bereit.

Der Lua-Code zum Ausblenden einer Sprite-Komponente auf einem Spielobjekt sieht beispielsweise so aus:

```lua
msg.post("#weapon", "disable")
```

Hier ist `"#weapon"` die Adresse der Sprite-Komponente des aktuellen Objekts. `"disable"` ist eine Nachricht, auf die Sprite-Komponenten reagieren. Eine ausführliche Erklärung zur Funktionsweise der Nachrichtenübermittlung findest du in der [Dokumentation zur Nachrichtenübermittlung](/manuals/message-passing).

## Modell {#model}

![Modell](images/icons/model.png){.left} Die 3D-Modellkomponente kann glTF-Assets für Meshes, Skelette und Animationen in dein Spiel importieren. Weitere Informationen findest du im [Handbuch zu Modellen](/manuals/model/).

## ParticleFX

![ParticleFX](images/icons/particlefx.png){.left} Partikel sind sehr nützlich, um ansprechende visuelle Effekte zu erstellen, insbesondere in Spielen. Du kannst damit Nebel, Rauch, Feuer, Regen oder fallende Blätter erzeugen. Defold enthält einen leistungsfähigen Editor für Partikeleffekte, mit dem du Effekte erstellen und anpassen kannst, während sie in deinem Spiel in Echtzeit laufen. Die [ParticleFX-Dokumentation](/manuals/particlefx) beschreibt die Funktionsweise im Detail.

## Profiling

Gute Leistung ist für Spiele entscheidend. Daher musst du Leistungs- und Speicherprofiling durchführen können, um dein Spiel zu vermessen und Leistungsengpässe sowie Speicherprobleme zu erkennen, die behoben werden müssen. Weitere Informationen zu den für Defold verfügbaren Profiling-Werkzeugen findest du im [Profiling-Handbuch](/manuals/profiling).

## Render-Ressource {#render}

![Render-Ressource](images/icons/render.png){.left} Render-Dateien enthalten Einstellungen, die beim Rendern des Spiels auf den Bildschirm verwendet werden. Sie legen fest, welches Render-Skript und welche Materialien beim Rendern verwendet werden. Weitere Einzelheiten findest du im [Handbuch zum Rendering](/manuals/render/).

## Render-Skript {#render-script}

![Render-Skript](images/icons/script.png){.left} Ein Render-Skript ist ein Lua-Skript, das steuert, wie das Spiel oder die Anwendung auf den Bildschirm gerendert werden soll. Es gibt ein Standard-Render-Skript, das die häufigsten Fälle abdeckt. Du kannst aber auch ein eigenes schreiben, wenn du benutzerdefinierte Beleuchtungsmodelle und andere Effekte benötigst. Weitere Einzelheiten zur Funktionsweise der Rendering-Pipeline findest du im [Handbuch zum Rendering](/manuals/render/). Einzelheiten zur Verwendung von Lua-Skripten in Defold findest du im [Handbuch zu Lua in Defold](/manuals/lua).

## Skript {#script}

![Skript](images/icons/script.png){.left}  Ein Skript ist eine Komponente, die ein Programm enthält, das das Verhalten von Spielobjekten definiert. Mit Skripten legst du die Regeln deines Spiels fest und bestimmst, wie Objekte auf verschiedene Interaktionen mit dem Spieler und mit anderen Objekten reagieren sollen. Alle Skripte werden in der Programmiersprache Lua geschrieben. Um mit Defold arbeiten zu können, musst du oder jemand aus deinem Team lernen, in Lua zu programmieren. Einen Überblick über Lua und Einzelheiten zur Verwendung von Lua-Skripten in Defold findest du im [Handbuch zu Lua in Defold](/manuals/lua).

## Audio {#sound}

![Audio](images/icons/sound.png){.left} Die Audiokomponente ist für die Wiedergabe eines bestimmten Klangs zuständig. Defold unterstützt Dateien in den Formaten WAV, Ogg Vorbis und Ogg Opus. Die Unterstützung für Opus muss im Anwendungsmanifest aktiviert werden. Weitere Informationen findest du im [Handbuch zu Audio](/manuals/sound).

## Sprite

![Sprite](images/icons/sprite.png){.left} Ein Sprite ist eine Komponente, die Spielobjekte um Grafik erweitert. Es zeigt ein Bild aus einer Kachelquelle oder einem Atlas an. Sprites bieten integrierte Unterstützung für Flipbook- und Skelettanimationen. Sprites werden üblicherweise für Figuren und Gegenstände verwendet.

## Texturprofile {#texture-profiles}

![Texturprofile](images/icons/texture-profiles.png){.left} Die Ressourcendatei für Texturprofile wird bei der Bundle-Erstellung verwendet, um Bilddaten automatisch zu verarbeiten und zu komprimieren. Dazu zählen Bilddaten in Atlanten, Kachelquellen, Cubemaps und eigenständigen Texturen, die für Modelle, GUIs usw. verwendet werden. Mehr dazu erfährst du im [Handbuch zu Texturprofilen](/manuals/texture-profiles).

## Kachelkarte {#tile-map}

![Kachelkarte](images/icons/tilemap.png){.left} Komponenten vom Typ Kachelkarte (tile map) zeigen Bilder aus einer Kachelquelle in einem oder mehreren überlagerten Rastern an. Sie werden am häufigsten zum Aufbau von Spielumgebungen verwendet: Boden, Wände, Gebäude und Hindernisse. Eine Kachelkarte kann mehrere übereinander ausgerichtete Ebenen mit einem festgelegten Mischmodus anzeigen. Das ist beispielsweise nützlich, um Blattwerk über Hintergrundkacheln mit Gras zu legen. Außerdem kannst du das in einer Kachel angezeigte Bild dynamisch ändern. So kannst du etwa eine Brücke zerstören und unpassierbar machen, indem du die Kacheln einfach durch solche ersetzt, die die zerstörte Brücke darstellen und die entsprechende Physikform enthalten. Weitere Informationen findest du in der [Dokumentation zu Kachelkarten](/manuals/tilemap).

## Kachelquelle {#tile-source}

![Kachelquelle](images/icons/tilesource.png){.left} Eine Kachelquelle beschreibt eine Textur, die aus mehreren kleineren Bildern gleicher Größe besteht. Du kannst Flipbook-Animationen aus einer Bildfolge in einer Kachelquelle definieren. Kachelquellen können außerdem automatisch Kollisionsformen aus Bilddaten berechnen. Das ist sehr nützlich, um Levels aus Kacheln zu erstellen, mit denen Objekte kollidieren und interagieren können. Kachelkartenkomponenten sowie Sprite- und ParticleFX-Komponenten verwenden Kachelquellen, um Grafikressourcen gemeinsam zu nutzen. Beachte, dass Atlanten oft besser geeignet sind als Kachelquellen. Weitere Informationen findest du in der [Dokumentation zu Kachelkarten](/manuals/tilemap).

## Vertex-Shader

![Vertex-Shader](images/icons/vertex-shader.png){.left} Der Vertex-Shader berechnet die Bildschirmgeometrie der primitiven Polygonformen einer Komponente. Bei jeder Art von visueller Komponente, ob Sprite, Kachelkarte oder Modell, wird die Form durch eine Menge von Vertex-Positionen der Polygone dargestellt. Das Vertex-Shader-Programm verarbeitet jeden Vertex im Weltkoordinatensystem und berechnet die resultierende Koordinate, die jeder Vertex eines Primitivs haben soll. Weitere Informationen findest du im [Shader-Handbuch](/manuals/shader).
