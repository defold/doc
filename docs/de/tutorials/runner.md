---
title: Tutorial für einen Endless Runner
brief: In diesem Tutorial beginnst du mit einem leeren Projekt und entwickelst ein vollständiges Runner-Spiel mit einer animierten Figur, physikalischen Kollisionen, Sammelobjekten und einem Punktesystem.
---

# Runner-Tutorial

In diesem Tutorial beginnen wir mit einem leeren Projekt und entwickeln ein vollständiges Runner-Spiel mit einer animierten Figur, physikalischen Kollisionen, Sammelobjekten und einem Punktesystem.

Beim Erlernen einer neuen Game-Engine gibt es viel aufzunehmen. Deshalb haben wir dieses Tutorial erstellt, um dir den Einstieg zu erleichtern. Es ist ein recht umfassendes Tutorial, das dir zeigt, wie die Engine und der Editor funktionieren. Wir setzen voraus, dass du bereits etwas Erfahrung mit dem Programmieren hast.

Wenn du eine Einführung in die Lua-Programmierung brauchst, lies unser [Handbuch zu Lua in Defold](/manuals/lua).

Falls dir dieses Tutorial für den Anfang etwas zu umfangreich erscheint, sieh dir unsere [Tutorial-Seite](//www.defold.com/tutorials) an. Dort findest du eine Auswahl an Tutorials mit unterschiedlichen Schwierigkeitsgraden.

Wenn du lieber Video-Tutorials ansiehst, schau dir [die Videoversion auf YouTube](https://www.youtube.com/playlist?list=PLXsXu5srjNlxtYPQ_YJQSxJG2AN9OVS5b) an.

Wir verwenden Spiel-Assets aus zwei anderen Tutorials und nehmen daran einige kleine Änderungen vor. Dieses Tutorial ist in mehrere Schritte unterteilt, von denen uns jeder dem fertigen Spiel ein gutes Stück näherbringt.

Am Ende entsteht ein Spiel, in dem du eine Heldenfigur steuerst, die durch eine Umgebung läuft, Münzen sammelt und Hindernissen ausweicht. Die Heldenfigur läuft mit einer festen Geschwindigkeit. Der Spieler steuert nur ihre Sprünge, indem er eine einzige Taste drückt (oder auf einem Mobilgerät den Bildschirm berührt). Das Level besteht aus einem endlosen Strom von Plattformen, auf die du springen kannst, und Münzen zum Einsammeln.

Wenn du an irgendeiner Stelle dieses Tutorials oder beim Erstellen deines Spiels nicht weiterkommst, zögere nicht, uns im [Defold-Forum](//forum.defold.com) um Hilfe zu bitten. Im Forum kannst du dich über Defold austauschen, das Defold-Team um Hilfe bitten, sehen, wie andere Spieleentwickler ihre Probleme gelöst haben, und neue Anregungen finden. Leg jetzt los.

::: sidenote
Ausführliche Beschreibungen von Konzepten und bestimmten Arbeitsschritten sind im gesamten Tutorial so markiert wie dieser Absatz. Wenn dir diese Abschnitte zu sehr ins Detail gehen, überspringe sie.
:::

Fangen wir also an. Wir hoffen, dass dir dieses Tutorial viel Spaß macht und dir beim Einstieg in Defold hilft.

> Lade die Assets für dieses Tutorial [hier](https://github.com/defold/sample-runner/tree/main/def-runner) herunter.

## SCHRITT 1 - Installation und Einrichtung {#step-1-installation-and-setup}

Lade als ersten Schritt [die folgenden Dateien herunter](https://github.com/defold/sample-runner/tree/main/def-runner).

Wenn du den Defold-Editor noch nicht heruntergeladen und installiert hast, ist jetzt der richtige Zeitpunkt dafür:

:[install](../shared/install.md)

Nachdem der Editor installiert und gestartet ist, kannst du ein neues Projekt erstellen und vorbereiten. Erstelle ein [neues Projekt](/manuals/project-setup/#creating-a-new-project) mit der Vorlage "Empty Project".

::: sidenote
Dieses Tutorial verwendet Spine-Funktionen aus der [Spine-Erweiterung](https://github.com/defold/extension-spine). Füge die Erweiterung zum Abschnitt für Abhängigkeiten in *game.project* hinzu.
:::

## Der Editor {#the-editor}

Beim ersten Start ist der Editor leer, ohne geöffnetes Projekt. Wähle deshalb <kbd>Open Project</kbd> im Menü und öffne dein gerade erstelltes Projekt. Du wirst außerdem aufgefordert, einen „Branch“ für das Projekt zu erstellen.

Im Bereich *Assets pane* siehst du nun alle Dateien, die zum Projekt gehören. Wenn du auf die Datei "main/main.collection" doppelklickst, wird sie in der Editoransicht in der Mitte geöffnet:

![Übersicht des Editors](images/runner/1/editor2_overview.png)

Der Editor besteht aus den folgenden Hauptbereichen:

Assets-Bereich
: Diese Ansicht zeigt alle Dateien in deinem Projekt. Verschiedene Dateitypen haben unterschiedliche Symbole. Doppelklicke auf eine Datei, um sie in einem für diesen Dateityp vorgesehenen Editor zu öffnen. Der besondere schreibgeschützte Ordner *builtins* ist für alle Projekte verfügbar. Er enthält nützliche Dinge wie ein Standard-Render-Skript, eine Schriftart, Materialien zum Rendern verschiedener Komponenten (components) und weitere Ressourcen.

Hauptansicht des Editors
: Je nachdem, welchen Dateityp du bearbeitest, zeigt diese Ansicht den passenden Editor an. Am häufigsten kommt der Szeneneditor zum Einsatz, den du hier siehst. Jede geöffnete Datei wird in einem eigenen Tab angezeigt.

Changed Files
: Enthält Dateien, die im Vergleich zum aktuellen Git-Commit lokal hinzugefügt, geändert, umbenannt oder gelöscht wurden. Für jeweils eine geänderte oder umbenannte Textdatei kannst du die Unterschiede anzeigen lassen. Hier kannst du auch ausgewählte lokale Änderungen zurücknehmen. Verwende einen externen Git-Client oder die Befehlszeile, um mit einem entfernten Repository zu synchronisieren.

Outline
: Zeigt den Inhalt der gerade bearbeiteten Datei als Hierarchie an. Über diese Ansicht kannst du Objekte und Komponenten hinzufügen, löschen, ändern und auswählen.

Properties
: Die Eigenschaften des aktuell ausgewählten Objekts oder der aktuell ausgewählten Komponente.

Console
: Wenn das Spiel läuft, zeigt diese Ansicht Ausgaben der Game-Engine an (Protokollmeldungen, Fehler, Debug-Informationen usw.) sowie alle eigenen Debug-Meldungen, die deine Skripte mit `print()` und `pprint()` ausgeben. Wenn deine App oder dein Spiel nicht startet, solltest du zuerst die Konsole prüfen. Hinter der Konsole befinden sich mehrere Tabs mit Fehlerinformationen sowie ein Kurveneditor, der beim Erstellen von Partikeleffekten verwendet wird.

## Das Spiel ausführen {#running-the-game}

Die Projektvorlage "Empty" ist tatsächlich vollständig leer. Wähle trotzdem <kbd>Project ▸ Build</kbd>, um einen Build des Projekts zu erstellen und das Spiel zu starten.

![Build erstellen](images/runner/1/build_and_launch.png)

Ein schwarzer Bildschirm ist vielleicht nicht besonders aufregend, aber dahinter läuft eine Defold-Spielanwendung, die wir leicht zu etwas Interessanterem machen können. Machen wir das also.

::: sidenote
Der Defold-Editor arbeitet mit Dateien. Wenn du im Bereich *Assets pane* auf eine Datei doppelklickst, öffnest du sie in einem geeigneten Editor. Anschließend kannst du den Inhalt der Datei bearbeiten.

Wenn du mit dem Bearbeiten einer Datei fertig bist, musst du sie speichern. Wähle dazu <kbd>File ▸ Save</kbd> im Hauptmenü. Der Editor weist auf ungespeicherte Änderungen hin, indem er im Tab der betreffenden Datei ein Sternchen '\*' an den Dateinamen anhängt.

![Datei mit ungespeicherten Änderungen](images/runner/1/file_changed.png)
:::

## Das Projekt einrichten {#setting-up-the-project}

Bevor wir beginnen, nehmen wir einige Projekteinstellungen vor. Öffne das Asset *game.project* im `Assets Pane` und scrolle zum Abschnitt Display. Setze `width` und `height` des Projekts auf `1280` beziehungsweise `720`.

Außerdem musst du die Spine-Erweiterung zum Projekt hinzufügen, damit wir die Heldenfigur animieren können. Füge eine Version der Spine-Erweiterung hinzu, die mit deiner installierten Version des Defold-Editors kompatibel ist. Die verfügbaren Spine-Versionen findest du hier:

[https://github.com/defold/extension-spine/releases](https://github.com/defold/extension-spine/releases)

Klicke mit der rechten Maustaste auf den Link zur ZIP-Datei der Version, die du verwenden möchtest:

![Mit der rechten Maustaste klicken und den Link zur Version kopieren](images/runner/extension-spine-releases.png)

Füge den Link zur Version zu deiner Liste der [Abhängigkeiten in game.project](/manuals/libraries/#setting-up-library-dependencies) hinzu. Nachdem du die Spine-Erweiterung hinzugefügt hast, musst du den Editor neu starten, um die mitgelieferte Editorintegration zu aktivieren.


## SCHRITT 2 - Den Boden erstellen {#step-2-creating-the-ground}

Machen wir die ersten kleinen Schritte und erstellen eine Spielfläche für unsere Figur, genauer gesagt ein Stück scrollenden Boden. Dazu gehen wir in wenigen Schritten vor.

1. Importiere die Bild-Assets in das Projekt, indem du die Bilddateien "ground01.png" und "ground02.png" aus dem Unterordner "level-images" des Asset-Pakets an eine geeignete Stelle im Projekt ziehst, zum Beispiel in einen Ordner "images" innerhalb des Ordners "main".
2. Erstelle eine neue *Atlas*-Datei für die Bodentexturen. Klicke dazu im Bereich *Assets pane* mit der rechten Maustaste auf einen geeigneten Ordner, beispielsweise den Ordner *main*, und wähle <kbd>New ▸ Atlas File</kbd>. Nenne die Atlasdatei *level.atlas*.

  ::: sidenote
  Ein *Atlas* ist eine Datei, die mehrere einzelne Bilder in einer größeren Bilddatei zusammenfasst. Das spart Speicherplatz und verbessert die Leistung. Mehr über Atlanten und andere Funktionen für 2D-Grafik erfährst du in der [Dokumentation zur 2D-Grafik](/manuals/2dgraphics).
  :::

3. Füge die Bodenbilder zum neuen Atlas hinzu, indem du in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten des Atlas klickst und <kbd>Add Images</kbd> wählst. Wähle die importierten Bilder aus und klicke auf *OK*. Jedes Bild im Atlas steht jetzt als Animation mit einem Einzelbild (Standbild) für Sprites, Partikeleffekte und andere visuelle Elemente zur Verfügung. Speichere die Datei.

  ![Einen neuen Atlas erstellen](images/runner/1/new_atlas.png)

  ![Bilder zum Atlas hinzufügen](images/runner/1/add_images_to_atlas.png)

  ::: sidenote
  *Warum funktioniert das nicht!?* Ein häufiges Problem beim Einstieg in Defold ist, dass das Speichern vergessen wird! Nachdem du Bilder zu einem Atlas hinzugefügt hast, musst du die Datei speichern, bevor du auf die Bilder zugreifen kannst.
  :::

4. Erstelle für den Boden eine Datei *ground.collection* für eine Sammlung (collection) und füge ihr 7 Spielobjekte (game objects) hinzu. Klicke dazu in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten der Sammlung und wähle <kbd>Add Game Object</kbd>. Nenne die Objekte "ground0", "ground1", "ground2" usw., indem du die Eigenschaft *Id* in der Ansicht *Properties* änderst. Beachte, dass Defold neuen Spielobjekten automatisch einen eindeutigen Bezeichner zuweist.

5. Füge jedem Objekt eine Sprite-Komponente hinzu. Klicke dazu in der Ansicht *Outline* mit der rechten Maustaste auf das Spielobjekt und wähle <kbd>Add Component</kbd>, dann *Sprite* und schließlich *OK*. Setze die Eigenschaft *Image* der Sprite-Komponente auf den gerade erstellten Atlas und die Standardanimation des Sprites auf eines der beiden Bodenbilder. Setze die X-Position der _Sprite-Komponente_ (nicht des Spielobjekts) auf 190 und die Y-Position auf 40. Das Bild ist 380 Pixel breit und wir verschieben es um die Hälfte dieser Pixelzahl zur Seite. Dadurch liegt der Bezugspunkt (pivot) des Spielobjekts am linken Rand des Sprite-Bildes.

  ![Die Bodensammlung erstellen](images/runner/1/ground_collection.png)

6. Die verwendete Grafik ist etwas zu groß. Skaliere deshalb jedes Spielobjekt auf 60 % (Skalierung von 0.6 in X und Y, wodurch 228 Pixel breite Bodenstücke entstehen).

  ![Den Boden skalieren](images/runner/1/scale_ground.png)

7. Ordne alle _Spielobjekte_ in einer Reihe an. Setze die X-Positionen der _Spielobjekte_ (nicht der Sprite-Komponenten) auf 0, 228, 456, 684, 912, 1140 und 1368 (Vielfache der Breite von 228 Pixeln).

  ::: sidenote
  Am einfachsten ist es wahrscheinlich, ein vollständiges, skaliertes Spielobjekt mit einer Sprite-Komponente zu erstellen und es anschließend zu kopieren. Markiere es in der Ansicht *Outline*, wähle <kbd>Edit ▸ Copy</kbd> und danach <kbd>Edit ▸ Paste</kbd>.

  Wenn du größere oder kleinere Kacheln möchtest, kannst du einfach die Skalierung ändern. Dann musst du allerdings auch die X-Positionen aller Boden-Spielobjekte auf Vielfache der neuen Breite ändern.
  :::

8. Speichere die Datei und füge anschließend *ground.collection* zur Datei *main.collection* hinzu: Doppelklicke zuerst auf die Datei *main.collection*. Klicke dann in der Ansicht *Outline* mit der rechten Maustaste auf das oberste Objekt und wähle <kbd>Add Collection From File</kbd>. Wähle im Dialog *ground.collection* aus und klicke auf *OK*. Achte darauf, *ground.collection* an der Position 0, 0, 0 zu platzieren, sonst erscheint sie versetzt. Speichere die Datei.

9. Starte das Spiel (<kbd>Project ▸ Build</kbd>), um zu sehen, ob alles an seinem Platz ist.

  ![Unbewegter Boden](images/runner/1/still_ground.png)

Vielleicht bist du inzwischen etwas verwirrt und fragst dich, was all die Dinge, die wir erstellt haben, eigentlich sind. Nehmen wir uns deshalb einen Moment Zeit, um die grundlegenden Bausteine jedes Defold-Projekts anzusehen:

Spielobjekte
: Spielobjekte sind Dinge, die im laufenden Spiel existieren. Jedes Spielobjekt hat eine Position im 3D-Raum, eine Drehung und eine Skalierung. Es muss nicht unbedingt sichtbar sein. Ein Spielobjekt enthält eine beliebige Anzahl von _Komponenten_, die ihm Fähigkeiten verleihen: Grafik (Sprites, Kachelkarten (tile maps), Modelle, Spine-Modelle und Partikeleffekte), Ton, Physik, Fabriken (factories, zum dynamischen Erzeugen) und mehr. Du kannst auch _Skriptkomponenten_ in Lua hinzufügen, um einem Spielobjekt Verhalten zu geben. Jedes Spielobjekt in deinen Spielen hat eine *id*, die du benötigst, um per Nachrichtenübermittlung mit ihm zu kommunizieren.

Sammlungen
: Sammlungen existieren im laufenden Spiel nicht als eigenständige Objekte. Sie ermöglichen eine feste Benennung von Spielobjekten und gleichzeitig mehrere Instanzen desselben Spielobjekts. In der Praxis dienen Sammlungen als Behälter für Spielobjekte und andere Sammlungen. Du kannst Sammlungen wie Prototypen (in anderen Engines auch „Prefabs“ oder „Baupläne“ genannt) für komplexe Hierarchien aus Spielobjekten und Sammlungen verwenden. Beim Start lädt die Engine eine Hauptsammlung und erweckt alles zum Leben, was du darin abgelegt hast. Standardmäßig ist das die Datei *main.collection* im Ordner *main* deines Projekts. Du kannst dies aber in den Projekteinstellungen ändern.

Für den Moment reichen diese Beschreibungen wahrscheinlich aus. Eine wesentlich ausführlichere Erklärung findest du jedoch im [Handbuch zu Bausteinen](/manuals/building-blocks). Es ist sinnvoll, dieses Handbuch später zu lesen, um genauer zu verstehen, wie Defold funktioniert.

## SCHRITT 3 - Den Boden bewegen {#step-3-making-the-ground-move}

Jetzt, wo alle Bodenstücke an ihrem Platz sind, können wir sie recht einfach in Bewegung setzen. Die Idee: Wir bewegen die Stücke von rechts nach links. Sobald ein Stück links außerhalb des Bildschirms angekommen ist, verschieben wir es an die Position ganz rechts. Um all diese Spielobjekte zu bewegen, brauchen wir ein Lua-Skript. Erstellen wir also eines:

1. Klicke im Bereich *Assets pane* mit der rechten Maustaste auf den Ordner *main* und wähle <kbd>New ▸ Script File</kbd>. Nenne die neue Datei *ground.script*.
2. Doppelklicke auf die neue Datei, um den Lua-Skripteditor zu öffnen.
3. Lösche den Standardinhalt der Datei und kopiere den folgenden Lua-Code hinein. Speichere anschließend die Datei.

```lua
-- ground.script
local pieces = { "ground0", "ground1", "ground2", "ground3",
                    "ground4", "ground5", "ground6" } -- <1>

function init(self) -- <2>
    self.speed = 360  -- Speed in pixels/s
end

function update(self, dt) -- <3>
    for i, p in ipairs(pieces) do -- <4>
        local pos = go.get_position(p)
        if pos.x <= -228 then -- <5>
            pos.x = 1368 + (pos.x + 228)
        end
        pos.x = pos.x - self.speed * dt -- <6>
        go.set_position(pos, p) -- <7>
    end
end
```
1. Speichere die Bezeichner der Boden-Spielobjekte in einer Lua-Tabelle, damit wir sie durchlaufen können.
2. Die Funktion `init()` wird aufgerufen, wenn das Spielobjekt im Spiel zum Leben erweckt wird. Wir initialisieren eine zum Objekt gehörende Variable, die die Geschwindigkeit des Bodens enthält.
3. `update()` wird einmal pro Frame aufgerufen, normalerweise 60-mal pro Sekunde. `dt` enthält die Anzahl der Sekunden seit dem letzten Aufruf.
4. Durchlaufe alle Boden-Spielobjekte.
5. Speichere die aktuelle Position in einer lokalen Variablen. Wenn sich das aktuelle Objekt am linken Rand befindet, verschiebe es an den rechten Rand.
6. Verringere die aktuelle X-Position entsprechend der eingestellten Geschwindigkeit. Multipliziere mit `dt`, um eine von der Bildrate unabhängige Geschwindigkeit in Pixel/s zu erhalten.
7. Aktualisiere die Position des Objekts mit der neuen Geschwindigkeit.

::: sidenote
Defold ist ein schneller Engine-Kern, der deine Daten und Spielobjekte verwaltet. Alle Logik und jedes Verhalten, das du für dein Spiel brauchst, erstellst du in Lua. Lua ist eine schnelle und schlanke Programmiersprache, die sich hervorragend zum Schreiben von Spiellogik eignet. Es gibt gute Lernmaterialien, zum Beispiel das Buch [Programming in Lua](http://www.lua.org/pil/) und das offizielle [Lua-Referenzhandbuch](http://www.lua.org/manual/5.3/).

Defold ergänzt Lua um mehrere APIs sowie ein System zur _Nachrichtenübermittlung_, mit dem du die Kommunikation zwischen Spielobjekten programmieren kannst. Wie das funktioniert, erfährst du im [Handbuch zur Nachrichtenübermittlung](/manuals/message-passing).
:::

::: sidenote
Du kannst die Editorbereiche Assets Pane, Console und Outline mit den Tasten <kbd>F6</kbd>, <kbd>F7</kbd> beziehungsweise <kbd>F8</kbd> ein- und ausblenden.
:::

Jetzt, wo wir eine Skriptdatei haben, sollten wir eine Referenz darauf in einer Komponente eines Spielobjekts hinterlegen. So wird das Skript als Teil des Lebenszyklus des Spielobjekts ausgeführt. Dazu erstellen wir ein neues Spielobjekt in *ground.collection* und fügen ihm eine *Script*-Komponente hinzu, die auf die gerade erstellte Lua-Skriptdatei verweist:

1. Klicke mit der rechten Maustaste auf den obersten Knoten der Sammlung und wähle <kbd>Add Game Object</kbd>. Setze den *id*-Wert des Objekts auf "controller".
2. Klicke mit der rechten Maustaste auf das Objekt "controller" und wähle <kbd>Add Component from file</kbd>. Wähle anschließend die Datei *ground.script*.

![Bodensteuerung](images/runner/1/ground_controller.png)

Wenn du das Spiel jetzt startest, führt das Spielobjekt "controller" das Skript in seiner *Script*-Komponente aus. Dadurch scrollt der Boden gleichmäßig über den Bildschirm.

## SCHRITT 4 - Eine Heldenfigur erstellen {#step-4-creating-a-hero-character}

Die Heldenfigur wird ein Spielobjekt, das aus den folgenden Komponenten besteht:

Ein *Spine Model*
: Damit erhalten wir eine kleine Heldenfigur, die einer Papierpuppe ähnelt und deren Körperteile sich flüssig und mit geringem Rechenaufwand animieren lassen.

Ein *Collision Object*
: Dieses Kollisionsobjekt (collision object) erkennt Kollisionen zwischen der Heldenfigur und Dingen im Level, auf denen sie laufen kann, die gefährlich sind oder die sie einsammeln kann.

Ein *Script*
: Dieses Skript empfängt Benutzereingaben und reagiert darauf, lässt die Heldenfigur springen, animiert sie und verarbeitet Kollisionen.

Importiere zunächst die Bilder der Körperteile und füge sie dann zu einem neuen Atlas hinzu, den wir *hero.atlas* nennen:

1. Erstelle einen neuen Ordner, indem du im Bereich *Assets pane* mit der rechten Maustaste klickst und <kbd>New ▸ Folder</kbd> wählst. Achte darauf, vorher keinen Ordner auszuwählen, sonst wird der neue Ordner innerhalb des markierten Ordners erstellt. Nenne den Ordner "hero".
2. Erstelle eine neue Atlasdatei, indem du mit der rechten Maustaste auf den Ordner *hero* klickst und <kbd>New ▸ Atlas File</kbd> wählst. Nenne die Datei *hero.atlas*.
3. Erstelle im Ordner *hero* einen neuen Unterordner *images*. Klicke dazu mit der rechten Maustaste auf den Ordner *hero* und wähle <kbd>New ▸ Folder</kbd>.
4. Ziehe die Bilder der Körperteile aus dem Ordner *hero-images* des Asset-Pakets in den gerade erstellten Ordner *images* im Bereich *Assets pane*.
5. Öffne *hero.atlas*, klicke in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Images</kbd>. Markiere alle Bilder der Körperteile und klicke auf *OK*.
6. Speichere die Atlasdatei.

![Atlas der Heldenfigur](images/runner/2/hero_atlas.png)

Außerdem müssen wir die Spine-Animationsdaten importieren und dafür eine *Spine Scene* einrichten:

1. Ziehe die Datei *hero.spinejson* (sie ist im Asset-Paket enthalten) in den Ordner *hero* im Bereich *Assets pane*.
2. Erstelle eine *Spine Scene*-Datei. Klicke mit der rechten Maustaste auf den Ordner *hero* und wähle <kbd>New ▸ Spine Scene File</kbd>. Nenne die Datei *hero.spinescene*.
3. Doppelklicke auf die neue Datei, um die *Spine Scene* zu öffnen und zu bearbeiten.
4. Setze die Eigenschaft *spine_json* auf die importierte JSON-Datei *hero.spinejson*. Klicke auf die Eigenschaft und dann auf die Schaltfläche *...* zur Dateiauswahl, um den Ressourcenbrowser zu öffnen.
5. Setze die Eigenschaft *atlas* so, dass sie auf die Datei *hero.atlas* verweist.
6. Speichere die Datei.

![Spine-Szene der Heldenfigur](images/runner/2/hero_spinescene.png)

::: sidenote
Die Datei *hero.spinejson* wurde im Spine-JSON-Format exportiert. Um solche Dateien zu erstellen, benötigst du die Animationssoftware Spine. Wenn du eine andere Animationssoftware verwenden möchtest, kannst du deine Animationen als Sprite-Bögen (sprite sheets) exportieren und sie als Flipbook-Animationen aus *Tile Source*- oder *Atlas*-Ressourcen verwenden. Weitere Informationen findest du im Handbuch zu [Animationen](/manuals/animation).
:::

### Das Spielobjekt aufbauen {#building-the-game-object}

Jetzt können wir mit dem Aufbau des Spielobjekts für die Heldenfigur beginnen:

1. Erstelle eine neue Datei *hero.go*. Klicke dazu mit der rechten Maustaste auf den Ordner *hero* und wähle <kbd>New ▸ Game Object File</kbd>.
2. Öffne die Spielobjektdatei.
3. Füge ihr eine *Spine Model*-Komponente hinzu. (Klicke in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Component</kbd>, dann "Spine Model".)
4. Setze die Eigenschaft *Spine Scene* der Komponente auf die gerade erstellte Datei *hero.spinescene* und wähle "run_right" als Standardanimation (um die Animation kümmern wir uns später genauer).
5. Speichere die Datei.

![Eigenschaften des Spine-Modells](images/runner/2/spinemodel_properties.png)

Jetzt fügen wir Physik hinzu, damit Kollisionen funktionieren:

1. Füge dem Spielobjekt der Heldenfigur eine *Collision Object*-Komponente hinzu. (Klicke in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Component</kbd>, dann "Collision Object".)
2. Klicke mit der rechten Maustaste auf die neue Komponente und wähle <kbd>Add Shape</kbd>. Füge zwei Formen hinzu, die den Körper der Figur abdecken. Eine Kugel und ein Quader reichen aus.
3. Klicke auf die Formen und verwende das *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>), um die Formen passend zu positionieren.
4. Markiere die *Collision Object*-Komponente und setze die Eigenschaft *Type* auf "Kinematic".

::: sidenote
Bei Kollisionen vom Typ "Kinematic" werden Kollisionen erkannt, aber die Physik-Engine löst sie nicht automatisch auf und simuliert die Objekte nicht. Die Physik-Engine unterstützt verschiedene Typen von Kollisionsobjekten. Mehr darüber erfährst du in der [Physikdokumentation](/manuals/physics).
:::

Wir müssen angeben, womit das Kollisionsobjekt interagieren soll:

1. Setze die Eigenschaft *Group* auf eine neue Kollisionsgruppe namens "hero".
2. Setze die Eigenschaft *Mask* auf eine andere Gruppe namens "geometry", mit der dieses Kollisionsobjekt Kollisionen erkennen soll. Beachte, dass die Gruppe "geometry" noch nicht existiert. Wir werden aber gleich Kollisionsobjekte hinzufügen, die ihr angehören.

Erstelle abschließend eine neue Datei *hero.script* und füge sie dem Spielobjekt hinzu.

1. Klicke im Bereich *Assets pane* mit der rechten Maustaste auf den Ordner *hero* und wähle <kbd>New ▸ Script File</kbd>. Nenne die neue Datei *hero.script*.
2. Öffne die neue Datei, kopiere den folgenden Code in die Skriptdatei und speichere sie. (Der Code ist recht übersichtlich, abgesehen von der Kollisionsauflösung, die die Kollisionsform der Heldenfigur von dem trennt, womit sie kollidiert. Das übernimmt die Funktion `handle_geometry_contact()`.)

![Spielobjekt der Heldenfigur](images/runner/2/hero_game_object.png)

::: sidenote
Wir behandeln die Kollisionen selbst, weil die Engine eine Newtonsche Simulation der beteiligten Körper ausführen würde, wenn wir den Typ des Kollisionsobjekts der Figur auf dynamisch setzen würden. Für ein Spiel wie dieses ist eine solche Simulation alles andere als optimal. Anstatt der Physik-Engine mit verschiedenen Kräften entgegenzuwirken, übernehmen wir die volle Kontrolle.

Dafür und für eine korrekte Behandlung der Kollisionen brauchen wir ein wenig Vektorrechnung. Eine ausführliche Erklärung zur Auflösung kinematischer Kollisionen findest du in der [Physikdokumentation](/manuals/physics-resolving-collisions/).
:::

```lua
-- gravity pulling the player down in pixel units/sˆ2
local gravity = -20

-- take-off speed when jumping in pixel units/s
local jump_takeoff_speed = 900

function init(self)
    -- this tells the engine to send input to on_input() in this script
    msg.post(".", "acquire_input_focus")

    -- save the starting position
    self.position = go.get_position()

    -- keep track of movement vector and if there is ground contact
    self.velocity = vmath.vector3(0, 0, 0)
    self.ground_contact = false
end

function final(self)
    -- Return input focus when the object is deleted
    msg.post(".", "release_input_focus")
end

function update(self, dt)
    local gravity = vmath.vector3(0, gravity, 0)

    if not self.ground_contact then
        -- Apply gravity if there's no ground contact
        self.velocity = self.velocity + gravity
    end

    -- apply velocity to the player character
    go.set_position(go.get_position() + self.velocity * dt)

    -- reset volatile state
    self.correction = vmath.vector3()
    self.ground_contact = false
end

local function handle_geometry_contact(self, normal, distance)
    -- project the correction vector onto the contact normal
    -- (the correction vector is the 0-vector for the first contact point)
    local proj = vmath.dot(self.correction, normal)
    -- calculate the compensation we need to make for this contact point
    local comp = (distance - proj) * normal
    -- add it to the correction vector
    self.correction = self.correction + comp
    -- apply the compensation to the player character
    go.set_position(go.get_position() + comp)
    -- check if the normal points enough up to consider the player standing on the ground
    -- (0.7 is roughly equal to 45 degrees deviation from pure vertical direction)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- project the velocity onto the normal
    proj = vmath.dot(self.velocity, normal)
    -- if the projection is negative, it means that some of the velocity points towards the contact point
    if proj < 0 then
        -- remove that component in that case
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("contact_point_response") then
        -- check if we received a contact point message. One message for each contact point
        if message.group == hash("geometry") then
            handle_geometry_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- only allow jump from ground
    if self.ground_contact then
        -- set take-off speed
        self.velocity.y = jump_takeoff_speed
    end
end

local function abort_jump(self)
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == hash("jump") or action_id == hash("touch") then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    end
end
```

1. Füge das Skript dem Heldenobjekt als *Script*-Komponente hinzu. Klicke dazu in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten von *hero.go* und wähle <kbd>Add Component from File</kbd>, dann die Datei *hero.script*.

Wenn du möchtest, kannst du die Heldenfigur jetzt vorübergehend zur Hauptsammlung hinzufügen und das Spiel starten, um zu sehen, wie sie durch die Welt fällt.

Damit die Heldenfigur funktioniert, fehlen uns nur noch Eingaben. Das obige Skript enthält bereits eine Funktion `on_input()`, die auf die Aktionen "jump" und "touch" (für Touchscreens) reagiert. Fügen wir Eingabebindungen (input bindings) für diese Aktionen hinzu.

1. Öffne "input/game.input_bindings".
2. Füge einen Tastenauslöser für "KEY_SPACE" hinzu und nenne die Aktion "jump".
3. Füge einen Berührungsauslöser für "TOUCH_MULTI" hinzu und nenne die Aktion "touch". (Die Aktionsnamen sind frei wählbar, sollten aber mit den Namen in deinem Skript übereinstimmen. Beachte, dass du denselben Aktionsnamen nicht für mehrere Auslöser verwenden kannst.)
4. Speichere die Datei.

![Eingabebindungen](images/runner/2/input_bindings.png)

## SCHRITT 5 - Das Level umstrukturieren {#step-5-refactoring-the-level}

Jetzt, wo unsere Heldenfigur samt Kollisionen eingerichtet ist, müssen wir auch dem Boden Kollisionen hinzufügen. So bekommt die Figur etwas, mit dem sie kollidieren beziehungsweise auf dem sie laufen kann. Das machen wir gleich. Zunächst sollten wir aber etwas aufräumen: Wir legen alle Levelinhalte in eine separate Sammlung und ordnen die Dateistruktur neu:

1. Erstelle eine neue Datei *level.collection*. Klicke dazu im Bereich *Assets pane* mit der rechten Maustaste auf *main* und wähle <kbd>New ▸ Collection File</kbd>.
2. Öffne die neue Datei, klicke in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Collection from File</kbd>, dann *ground.collection*.
3. Klicke in *level.collection* in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Game Object File</kbd>, dann *hero.go*.
4. Erstelle nun im Stammverzeichnis des Projekts einen neuen Ordner namens *level*. Klicke dazu mit der rechten Maustaste auf die freie Fläche unter *game.project* und wähle <kbd>New ▸ Folder</kbd>. Verschiebe anschließend die bisher erstellten Level-Assets in diesen Ordner: die Dateien *level.collection* und *level.atlas*, den Ordner "images" mit den Bildern für den Level-Atlas sowie die Dateien *ground.collection* und *ground.script*.
5. Öffne *main.collection*, lösche *ground.collection* und füge stattdessen *level.collection* hinzu, die jetzt die *ground.collection* enthält (Rechtsklick und <kbd>Add Collection from File</kbd>). Achte darauf, die Sammlung an der Position 0, 0, 0 zu platzieren.

::: sidenote
Wie du vielleicht schon bemerkt hast, ist die Dateihierarchie im Bereich *Assets pane* von der Inhaltsstruktur getrennt, die du in deinen Sammlungen aufbaust. Einzelne Dateien werden aus Sammlungs- und Spielobjektdateien referenziert, ihr Speicherort ist aber völlig frei wählbar.

Wenn du eine Datei an einen neuen Ort verschieben möchtest, hilft Defold dir, indem es die Referenzen auf diese Datei automatisch aktualisiert (Refactoring). Beim Entwickeln komplexer Software wie eines Spiels ist es äußerst hilfreich, die Projektstruktur mit dem wachsenden und sich verändernden Projekt anpassen zu können. Defold unterstützt das und sorgt für einen reibungslosen Ablauf. Du brauchst also keine Scheu davor zu haben, deine Dateien zu verschieben!
:::

Außerdem sollten wir der Levelsammlung ein Spielobjekt für die Steuerung mit einer Skriptkomponente hinzufügen:

1. Erstelle eine neue Skriptdatei. Klicke im Bereich *Assets pane* mit der rechten Maustaste auf den Ordner *level* und wähle <kbd>New ▸ Script File</kbd>. Nenne die Datei *controller.script*.
2. Öffne die Skriptdatei, kopiere den folgenden Code hinein und speichere sie:

    ```lua
    -- controller.script
    go.property("speed", 360) -- <1>

    function init(self)
        msg.post("ground/controller#ground", "set_speed", { speed = self.speed })
    end
    ```
    1. Dies ist eine Skripteigenschaft. Wir geben ihr einen Standardwert. Jede platzierte Instanz des Skripts kann diesen Wert jedoch direkt in der Eigenschaftsansicht des Editors überschreiben.

3. Öffne die Datei *level.collection*.
4. Klicke in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Game Object</kbd>.
5. Setze *Id* auf "controller".
6. Klicke in der Ansicht *Outline* mit der rechten Maustaste auf das Spielobjekt "controller" und wähle <kbd>Add Component from File</kbd>. Wähle die Datei *controller.script* im Ordner *level*.
7. Speichere die Datei.

![Skripteigenschaft](images/runner/2/script_property.png)

::: sidenote
Das Spielobjekt "controller" liegt nicht in einer eigenen Datei vor, sondern wird direkt in der Levelsammlung erstellt. Die Spielobjektinstanz wird somit aus den dort eingebetteten Daten erzeugt. Für Spielobjekte mit einer einzigen Aufgabe wie dieses ist das in Ordnung. Wenn du mehrere Instanzen eines Spielobjekts brauchst und die Möglichkeit haben möchtest, den Prototyp beziehungsweise die Vorlage anzupassen, aus der jede Instanz entsteht, erstelle einfach eine Spielobjektdatei und füge das Spielobjekt aus dieser Datei zur Sammlung hinzu. Dadurch entsteht ein Spielobjekt, das die Datei als Prototyp beziehungsweise Vorlage referenziert.

Das Spielobjekt "controller" soll alles steuern, was mit dem laufenden Level zusammenhängt. Bald wird dieses Skript Plattformen und Münzen dynamisch erzeugen, mit denen die Heldenfigur interagieren kann. Vorerst legt es aber nur die Geschwindigkeit des Levels fest.
:::

In seiner Funktion `init()` sendet das Skript zur Levelsteuerung eine Nachricht an die Skriptkomponente des Bodensteuerungsobjekts. Es adressiert sie über ihren Bezeichner:

```lua
msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
```

Der Bezeichner des Spielobjekts für die Steuerung lautet `"ground/controller"`, da es in der Sammlung "ground" liegt. Den Komponentenbezeichner `"controller"` hängen wir hinter dem Rautenzeichen `"#"` an, das den Objektbezeichner vom Komponentenbezeichner trennt. Beachte, dass das Bodenskript noch keinen Code enthält, der auf die Nachricht `set_speed` reagiert. Deshalb müssen wir eine Funktion `on_message()` zu *ground.script* hinzufügen und die entsprechende Logik ergänzen.

1. Öffne *ground.script*.
2. Füge den folgenden Code hinzu und speichere die Datei:

```lua
-- ground.script
function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then -- <1>
        self.speed = message.speed -- <2>
    end
end
```
1. Alle Nachrichten werden beim Senden intern gehasht und müssen mit dem Hashwert verglichen werden.
2. Die Nachrichtendaten sind eine Lua-Tabelle mit den Daten, die mit der Nachricht gesendet werden.

![Code für den Boden hinzufügen](images/runner/insert_ground_code.png)

## SCHRITT 6 - Bodenphysik und Plattformen {#step-6-ground-physics-and-platforms}

An dieser Stelle sollten wir physikalische Kollisionen für den Boden hinzufügen:

1. Öffne die Datei *ground.collection*.
2. Füge einem geeigneten Spielobjekt eine neue *Collision Object*-Komponente hinzu. Da das Bodenskript nicht auf Kollisionen reagiert (die gesamte Logik dafür liegt im Heldenskript), können wir sie in einem beliebigen _unbewegten_ Spielobjekt platzieren. Die Objekte der Bodenkacheln bewegen sich, verwende diese also nicht. Das Spielobjekt "controller" eignet sich gut. Du kannst dafür aber auch ein separates Objekt erstellen, wenn du möchtest. Klicke mit der rechten Maustaste auf das Spielobjekt und wähle <kbd>Add Component</kbd>, dann *Collision Object*.
3. Füge eine Quaderform hinzu, indem du mit der rechten Maustaste auf die *Collision Object*-Komponente klickst und <kbd>Add Shape</kbd>, dann *Box* wählst.
4. Verwende das *Move Tool* und das *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> und <kbd>Scene ▸ Scale Tool</kbd>), damit der Quader alle Bodenkacheln abdeckt.
5. Setze die Eigenschaft *Type* des Kollisionsobjekts auf "Static", da sich die Physik des Bodens nicht bewegen wird.
6. Setze die Eigenschaft *Group* des Kollisionsobjekts auf "geometry" und *Mask* auf "hero". Jetzt erkennen dieses Kollisionsobjekt und das der Heldenfigur Kollisionen miteinander.
7. Speichere die Datei.

![Bodenkollision](images/runner/2/ground_collision.png)

Jetzt solltest du das Spiel probeweise starten können (<kbd>Project ▸ Build</kbd>). Die Heldenfigur sollte auf dem Boden laufen und mit der Taste <kbd>Space</kbd> springen können. Wenn du das Spiel auf einem Mobilgerät ausführst, kannst du durch Tippen auf den Bildschirm springen.

Um das Leben in unserer Spielwelt etwas weniger eintönig zu machen, sollten wir Plattformen hinzufügen, auf die wir springen können.

1. Ziehe die Bilddatei *rock_planks.png* aus dem Asset-Paket in den Unterordner *level/images*.
2. Öffne *level.atlas* und füge das neue Bild zum Atlas hinzu. Klicke dazu in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Images</kbd>.
3. Speichere die Datei.
4. Erstelle im Ordner *level* eine neue *Game Object*-Datei namens *platform.go*. (Klicke im Bereich *Assets pane* mit der rechten Maustaste auf *level* und wähle <kbd>New ▸ Game Object File</kbd>.)
5. Füge dem Spielobjekt eine *Sprite*-Komponente hinzu. Klicke dazu in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Component</kbd>, dann *Sprite*.
6. Setze die Eigenschaft *Image* so, dass sie auf die Datei *level.atlas* verweist, und setze *Default Animation* auf "rock_planks". Bewahre die Levelobjekte der Übersicht halber in einem Unterordner "level/objects" auf.
7. Füge dem Spielobjekt der Plattform eine *Collision Object*-Komponente hinzu. Klicke dazu in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Component</kbd>.
8. Achte darauf, *Type* der Komponente auf "Kinematic", *Group* auf "geometry" und *Mask* auf "hero" zu setzen.
9. Füge der *Collision Object*-Komponente eine *Box Shape* hinzu. (Klicke in der Ansicht *Outline* mit der rechten Maustaste auf die Komponente und wähle <kbd>Add Shape</kbd>, dann *Box*.)
10. Verwende das *Move Tool* und das *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> und <kbd>Scene ▸ Scale Tool</kbd>), damit die Form in der *Collision Object*-Komponente die Plattform abdeckt.
11. Erstelle eine *Script*-Datei namens *platform.script*. Klicke dazu im Bereich *Assets pane* mit der rechten Maustaste und wähle <kbd>New ▸ Script File</kbd>. Füge den folgenden Code in die Datei ein und speichere sie:

    ```lua
    -- platform.script
    function init(self)
        self.speed = 540      -- Default speed in pixels/s
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            go.delete() -- <1>
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        end
    end
    ```
    1. Lösche die Plattform einfach, sobald sie über den rechten Bildschirmrand hinausbewegt wurde.

12. Öffne *platform.go* und füge das neue Skript als Komponente hinzu. Klicke dazu in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Component From File</kbd>, dann *platform.script*.
13. Kopiere *platform.go* in eine neue Datei. Klicke dazu im Bereich *Assets pane* mit der rechten Maustaste auf die Datei und wähle <kbd>Copy</kbd>. Klicke dann erneut mit der rechten Maustaste und wähle <kbd>Paste</kbd>. Nenne die neue Datei *platform_long.go*.
14. Öffne *platform_long.go* und füge eine zweite *Sprite*-Komponente hinzu. Klicke dazu in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Component</kbd>. Alternativ kannst du das vorhandene *Sprite* kopieren.
15. Verwende das *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>), um die *Sprite*-Komponenten nebeneinander zu platzieren.
16. Verwende das *Move Tool* und das *Scale Tool*, damit die Form in der *Collision Object*-Komponente beide Plattformen abdeckt.

![Plattform](images/runner/2/platform_long.png)

::: sidenote
Beachte, dass sowohl *platform.go* als auch *platform_long.go* eine *Script*-Komponente haben, die auf dieselbe Skriptdatei verweist. Das ist praktisch, denn jede Änderung an dieser Skriptdatei wirkt sich sowohl auf das Verhalten der normalen als auch der langen Plattformen aus.
:::

## Plattformen dynamisch erzeugen {#spawning-platforms}

Das Spiel soll ein einfacher Endless Runner werden. Deshalb können wir die Spielobjekte der Plattformen nicht im Editor in einer Sammlung platzieren. Stattdessen müssen wir sie dynamisch erzeugen:

1. Öffne *level.collection*.
2. Füge dem Spielobjekt "controller" zwei *Factory*-Komponenten hinzu. Klicke dazu mit der rechten Maustaste darauf und wähle <kbd>Add Component</kbd>, dann *Factory*.
3. Setze die Eigenschaften *Id* der Komponenten auf "platform_factory" und "platform_long_factory".
4. Setze die Eigenschaft *Prototype* von "platform_factory" auf die Datei */level/objects/platform.go*.
5. Setze die Eigenschaft *Prototype* von "platform_long_factory" auf die Datei */level/objects/platform_long.go*.
6. Speichere die Datei.
7. Öffne die Datei *controller.script*, die das Level verwaltet.
8. Ändere das Skript so, dass es den folgenden Inhalt hat, und speichere die Datei:

```lua
-- controller.script
go.property("speed", 360)

local grid = 460
local platform_heights = { 100, 200, 350 } -- <1>

function init(self)
    msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
    self.gridw = 0
end

function update(self, dt) -- <2>
    self.gridw = self.gridw + self.speed * dt

    if self.gridw >= grid then
        self.gridw = 0

        -- Maybe spawn a platform at random height
        if math.random() > 0.2 then
            local h = platform_heights[math.random(#platform_heights)]
            local f = "#platform_factory"
            if math.random() > 0.5 then
                f = "#platform_long_factory"
            end

            local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, vmath.vector3(0.6, 0.6, 1))
            msg.post(p, "set_speed", { speed = self.speed })
        end
    end
end
```
1. Vordefinierte Werte für die Y-Positionen, an denen Plattformen dynamisch erzeugt werden.
2. Die Funktion `update()` wird einmal pro Frame aufgerufen. Wir nutzen sie, um in bestimmten Abständen (damit keine Überlappungen entstehen) und auf bestimmten Höhen zu entscheiden, ob eine normale oder eine lange Plattform dynamisch erzeugt werden soll. Du kannst leicht mit verschiedenen Algorithmen für die Erzeugung experimentieren, um unterschiedliches Gameplay zu gestalten.

Starte jetzt das Spiel (<kbd>Project ▸ Build</kbd>).

Wow, langsam wird daraus etwas (fast) Spielbares ...

![Das Spiel ausführen](images/runner/2/run_game.png)

## SCHRITT 7 - Animation und Tod {#step-7-animation-and-death}

Als Erstes erwecken wir die Heldenfigur zum Leben. Im Moment steckt die arme Figur in einer endlosen Laufanimation fest und reagiert weder auf Sprünge noch auf andere Ereignisse passend. Die Spine-Datei, die wir aus dem Asset-Paket hinzugefügt haben, enthält bereits mehrere Animationen genau dafür.

1. Öffne die Datei *hero.script* und füge die folgenden Funktionen _vor_ der vorhandenen Funktion `update()` ein:

```lua
    -- hero.script
    local function play_animation(self, anim)
        -- only play animations which are not already playing
        if self.anim ~= anim then
            -- tell the spine model to play the animation
            local anim_props = { blend_duration = 0.15 }
            spine.play_anim("#spinemodel", anim, go.PLAYBACK_LOOP_FORWARD, anim_props)
            -- remember which animation is playing
            self.anim = anim
        end
    end

    local function update_animation(self)
        -- make sure the right animation is playing
        if self.ground_contact then
            play_animation(self, hash("run"))
        else
            play_animation(self, hash("jump"))

        end
    end
```

2. Suche die Funktion `update()` und füge einen Aufruf von `update_animation` hinzu:

```lua
    ...
    -- apply it to the player character
    go.set_position(go.get_position() + self.velocity * dt)

    update_animation(self)
    ...
  ```

![Code für die Heldenfigur einfügen](images/runner/insert_hero_code.png)

::: sidenote
Lua verwendet für lokale Variablen einen „lexikalischen Gültigkeitsbereich“. Deshalb kommt es auf die Reihenfolge an, in der du Funktionen mit `local` anordnest. Die Funktion `update()` ruft die lokalen Funktionen `update_animation()` und `play_animation()` auf. Die Laufzeitumgebung muss diese lokalen Funktionen also bereits kennen, um sie aufrufen zu können. Daher müssen wir die Funktionen vor `update()` platzieren. Wenn du die Reihenfolge der Funktionen vertauschst, erhältst du einen Fehler. Beachte, dass dies nur für `local`-Variablen gilt. Mehr über die Gültigkeitsbereiche und lokalen Funktionen in Lua erfährst du unter http://www.lua.org/pil/6.2.html
:::

Mehr ist nicht nötig, um der Heldenfigur Sprung- und Fallanimationen hinzuzufügen. Wenn du das Spiel startest, wirst du merken, dass es sich viel besser spielt. Vielleicht fällt dir auch auf, dass die Plattformen die Heldenfigur leider vom Bildschirm schieben können. Das ist eine Nebenwirkung der Kollisionsbehandlung. Die Lösung ist aber einfach: Füge etwas Gewalt hinzu und mache die Kanten der Plattformen gefährlich!

1. Ziehe *spikes.png* aus dem Asset-Paket in den Ordner "level/images" im Bereich *Assets pane*.
2. Öffne *level.atlas* und füge das Bild hinzu (Rechtsklick und <kbd>Add Images</kbd>).
3. Öffne *platform.go* und füge einige *Sprite*-Komponenten hinzu. Setze *Image* auf *level.atlas* und *Default Animation* auf "spikes".
4. Verwende das *Move Tool* und das *Rotate Tool*, um die Stacheln entlang der Plattformkanten zu platzieren.
5. Damit die Stacheln hinter der Plattform gerendert werden, setze die *Z*-Position der Stachel-Sprites auf -0.1.
6. Füge den Plattformen eine neue *Collision Object*-Komponente hinzu. Klicke dazu in der Ansicht *Outline* mit der rechten Maustaste auf den obersten Knoten und wähle <kbd>Add Component</kbd>. Setze die Eigenschaft *Group* auf "danger" und *Mask* auf "hero".
7. Füge dem *Collision Object* eine Quaderform hinzu (Rechtsklick und <kbd>Add Shape</kbd>). Platziere die Form mit dem *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) und dem *Scale Tool* so, dass die Heldenfigur mit dem Objekt "danger" kollidiert, wenn sie von der Seite oder von unten auf die Plattform trifft.
8. Speichere die Datei.

    ![Stacheln an der Plattform](images/runner/3/danger_edges.png)

9. Öffne *hero.go*, markiere das *Collision Object* und füge den Namen "danger" zur Eigenschaft *Mask* hinzu. Speichere anschließend die Datei.

    ![Kollision der Heldenfigur](images/runner/3/hero_collision.png)

10. Öffne *hero.script* und ändere die Funktion `on_message()`, damit eine Reaktion erfolgt, wenn die Heldenfigur mit einer "danger"-Kante kollidiert:

    ```lua
    -- hero.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            self.velocity = vmath.vector3(0, 0, 0)
            self.correction = vmath.vector3()
            self.ground_contact = false
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- check if we received a contact point message
            if message.group == hash("danger") then
                -- Die and restart
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("#", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end
    ```
    1. Füge eine Drehung und eine Fallbewegung hinzu, wenn die Heldenfigur stirbt. Das lässt sich noch deutlich verbessern!

11. Ändere die Funktion `init()` so, dass sie zum Initialisieren des Objekts eine Nachricht "reset" sendet. Speichere anschließend die Datei:

    ```lua
    -- hero.script
    function init(self)
        -- this lets us handle input in this script
        msg.post(".", "acquire_input_focus")
        -- save position
        self.position = go.get_position()
        msg.post("#", "reset")
    end
    ```

## SCHRITT 8 - Das Level zurücksetzen {#step-8-resetting-the-level}

Wenn du das Spiel jetzt ausprobierst, wird schnell klar, dass das Zurücksetzen nicht richtig funktioniert. Die Heldenfigur selbst wird zwar korrekt zurückgesetzt, aber sie kann dabei leicht in eine Situation geraten, in der sie sofort auf eine Plattformkante fällt und erneut stirbt. Wir möchten beim Tod das gesamte Level richtig zurücksetzen. Da das Level nur aus einer Folge dynamisch erzeugter Plattformen besteht, müssen wir lediglich alle erzeugten Plattformen erfassen und sie beim Zurücksetzen löschen:

1. Öffne die Datei *controller.script* und passe den Code so an, dass er die Bezeichner aller dynamisch erzeugten Plattformen speichert:

    ```lua
    -- controller.script
    go.property("speed", 360)

    local grid = 460
    local platform_heights = { 100, 200, 350 }

    function init(self)
        msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
        self.gridw = 0
        self.spawns = {} -- <1>
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= grid then
            self.gridw = 0

            -- Maybe spawn a platform at random height
            if math.random() > 0.2 then
                local h = platform_heights[math.random(#platform_heights)]
                local f = "#platform_factory"
                if math.random() > 0.5 then
                    f = "#platform_long_factory"
                end

                local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, vmath.vector3(0.6, 0.6, 1))
                msg.post(p, "set_speed", { speed = self.speed })
                table.insert(self.spawns, p) -- <1>
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then -- <2>
            -- Tell the hero to reset.
            msg.post("hero#hero", "reset")
            -- Delete all platforms
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then -- <3>
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```
    1. Wir verwenden eine Tabelle, um alle dynamisch erzeugten Plattformen zu speichern.
    2. Die Nachricht "reset" löscht alle in der Tabelle gespeicherten Plattformen.
    3. Die Nachricht "delete_spawn" löscht eine bestimmte Plattform und entfernt sie aus der Tabelle.

2. Speichere die Datei.
3. Öffne *platform.script* und ändere es so, dass es eine Plattform, die den linken Rand erreicht hat, nicht einfach löscht. Stattdessen soll es eine Nachricht an die Levelsteuerung senden und sie auffordern, die Plattform zu entfernen:

    ```lua
    -- platform.script
    ...
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    ...
    ```

    ![Code für die Plattform einfügen](images/runner/insert_platform_code.png)

4. Speichere die Datei.
5. Öffne *hero.script*. Als Letztes müssen wir jetzt dem Level mitteilen, dass es sich zurücksetzen soll. Die Nachricht, die die Heldenfigur zum Zurücksetzen auffordert, haben wir in das Skript zur Levelsteuerung verschoben. Es ist sinnvoll, das Zurücksetzen auf diese Weise zentral zu steuern. So können wir beispielsweise leichter eine längere, zeitlich gesteuerte Todessequenz einbauen:

```lua
-- hero.script
...
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
    function()
        msg.post("controller#controller", "reset")
    end)
...
```

![Code für die Heldenfigur einfügen](images/runner/insert_hero_code_2.png)

Damit steht jetzt der grundlegende Ablauf aus Neustart und Tod!

Als Nächstes kommt etwas, für das es sich zu leben lohnt: Münzen!

## SCHRITT 9 - Münzen zum Einsammeln {#step-9-coins-to-collect}

Wir möchten Münzen im Level platzieren, die der Spieler einsammeln kann. Zuerst stellt sich die Frage, wie wir sie ins Level bekommen. Wir könnten beispielsweise ein Verfahren zur dynamischen Erzeugung entwickeln, das auf den Algorithmus zum Erzeugen der Plattformen abgestimmt ist. Letztlich haben wir uns aber für einen viel einfacheren Ansatz entschieden: Die Plattformen selbst erzeugen die Münzen:

1. Ziehe das Bild *coin.png* aus dem Asset-Paket nach "level/images" im Bereich *Assets pane*.
2. Öffne *level.atlas* und füge das Bild hinzu (Rechtsklick und <kbd>Add Images</kbd>).
3. Erstelle im Ordner *level* eine *Game Object*-Datei namens *coin.go*. Klicke dazu im Bereich *Assets pane* mit der rechten Maustaste auf *level* und wähle <kbd>New ▸ Game Object File</kbd>.
4. Öffne *coin.go* und füge eine *Sprite*-Komponente hinzu (Rechtsklick in der Ansicht *Outline* und <kbd>Add Component</kbd>). Setze *Image* auf *level.atlas* und *Default Animation* auf "coin".
5. Füge ein *Collision Object* hinzu (Rechtsklick in der Ansicht *Outline* und <kbd>Add Component</kbd>)
und füge eine *Sphere*-Form hinzu, die das Bild abdeckt (Rechtsklick auf die Komponente und <kbd>Add Shape</kbd>).
6. Verwende das *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) und das *Scale Tool*, damit die Kugel das Münzbild abdeckt.
7. Setze *Type* des Kollisionsobjekts auf "Kinematic", *Group* auf "pickup" und *Mask* auf "hero".
8. Öffne *hero.go* und füge "pickup" zur Eigenschaft *Mask* der *Collision Object*-Komponente hinzu. Speichere anschließend die Datei.
9. Erstelle eine neue Skriptdatei namens *coin.script*. Klicke dazu im Bereich *Assets pane* mit der rechten Maustaste auf *level* und wähle <kbd>New ▸ Script File</kbd>. Ersetze den Vorlagencode durch Folgendes:

    ```lua
    -- coin.script
    function init(self)
        self.collected = false
    end

    function on_message(self, message_id, message, sender)
        if self.collected == false and message_id == hash("collision_response") then
            self.collected = true
            msg.post("#sprite", "disable")
        elseif message_id == hash("start_animation") then
            pos = go.get_position()
            go.animate(go.get_id(), "position.y", go.PLAYBACK_LOOP_PINGPONG, pos.y + 24, go.EASING_INOUTSINE, 0.75, message.delay)
        end
    end
    ```

10. Füge dem Münzobjekt die Skriptdatei als *Script*-Komponente hinzu (Rechtsklick auf den obersten Knoten in *Outline* und <kbd>Add Component from File</kbd>).

    ![Spielobjekt der Münze](images/runner/3/coin.png)

Die Münzen sollen von den Plattformobjekten dynamisch erzeugt werden. Füge deshalb Fabriken für die Münzen in *platform.go* und *platform_long.go* ein.

1. Öffne *platform.go* und füge eine *Factory*-Komponente hinzu (Rechtsklick in der Ansicht *Outline* und <kbd>Add Component</kbd>).
2. Setze die *Id* der *Factory* auf "coin_factory" und ihren *Prototype* auf die Datei *coin.go*.
3. Öffne nun *platform_long.go* und erstelle eine identische *Factory*-Komponente.
4. Speichere beide Dateien.

![Münzfabrik](images/runner/3/coin_factory.png)

Jetzt müssen wir *platform.script* so ändern, dass es die Münzen dynamisch erzeugt und löscht:

```lua
-- platform.script
function init(self)
    self.speed = 540     -- Default speed in pixels/s
    self.coins = {}
end

function final(self)
    for i,p in ipairs(self.coins) do
        go.delete(p)
    end
end

function update(self, dt)
    local pos = go.get_position()
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    pos.x = pos.x - self.speed * dt
    go.set_position(pos)
end

function create_coins(self, params)
    local spacing = 56
    local pos = go.get_position()
    local x = pos.x - params.coins * (spacing*0.5) - 24
    for i = 1, params.coins do
        local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
        msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
        msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
        table.insert(self.coins, coin)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then
        self.speed = message.speed
    elseif message_id == hash("create_coins") then
        create_coins(self, message)
    end
end
```
1. Indem wir die Plattform als übergeordnetes Objekt der dynamisch erzeugten Münze festlegen, bewegt sich die Münze mit der Plattform.
2. Die Animation lässt die Münzen auf und ab tanzen, relativ zur Plattform, die jetzt ihr übergeordnetes Objekt ist.

::: sidenote
Eltern-Kind-Beziehungen verändern ausschließlich den _Szenengraphen_. Ein untergeordnetes Objekt wird zusammen mit seinem übergeordneten Objekt transformiert, also verschoben, skaliert oder gedreht. Wenn du zusätzliche „Besitzbeziehungen“ zwischen Spielobjekten benötigst, musst du diese ausdrücklich im Code verwalten.
:::

Als letzten Schritt dieses Tutorials fügen wir einige Zeilen zu *controller.script* hinzu:

```lua
-- controller.script
...
local platform_heights = { 100, 200, 350 }
local coins = 3 -- <1>
...
```
1. Die Anzahl der Münzen, die auf einer normalen Plattform dynamisch erzeugt werden sollen.

```lua
-- controller.script
...
local coins = coins
if math.random() > 0.5 then
    f = "#platform_long_factory"
    coins = coins * 2 -- Twice the number of coins on long platforms
end
...
```

```lua
-- controller.script
...
msg.post(p, "set_speed", { speed = self.speed })
msg.post(p, "create_coins", { coins = coins })
table.insert(self.spawns, p)
...
```

![Code für die Steuerung einfügen](images/runner/insert_controller_code.png)

Jetzt haben wir ein einfaches, aber funktionsfähiges Spiel! Wenn du es bis hierher geschafft hast, möchtest du vielleicht selbstständig weitermachen und Folgendes hinzufügen:

1. Ein Punktesystem und Lebenszähler
2. Partikeleffekte für Sammelobjekte und den Tod
3. Ansprechende Hintergrundbilder

> Lade die fertige Version des Projekts [hier](images/runner/sample-runner.zip) herunter.

Damit endet dieses einführende Tutorial. Leg jetzt los und erkunde Defold. Wir haben viele [Handbücher und Tutorials](//www.defold.com/learn) vorbereitet, die dich unterstützen. Wenn du nicht weiterkommst, bist du im [Forum](//forum.defold.com) willkommen.

Viel Spaß mit Defold!
