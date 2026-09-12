---
brief: Wenn du Defold noch nicht kennst, hilft dir diese Anleitung beim Einstieg in die Skriptlogik und einige Bausteine von Defold, mit denen du einen Snake-Klon von Grund auf erstellst.
layout: tutorial
title: Ein Snake-Spiel in Defold erstellen
difficulty: Beginner
---

# Snake

Dieses Tutorial führt dich durch die Entwicklung eines der bekanntesten Spieleklassiker, die du nachbauen kannst. Es gibt viele Varianten dieses Spiels. In dieser Variante frisst eine Schlange „Futter“ und wächst nur beim Fressen. Außerdem bewegt sie sich über ein Spielfeld mit Hindernissen.

![Vorschaubild](images/snake/thumbnail.png)

### Was du lernen wirst {#what-youll-learn}

In diesem Tutorial lernst du, wie du:
- In Defold ein Spiel von Grund auf erstellst
- Eingaben einrichtest und verarbeitest
- Kachelkarten (tile maps) erstellst und sie zur Laufzeit änderst
- Skripte in Lua schreibst

### Ein Hinweis für Einsteiger {#a-note-for-beginners}

Dieses Tutorial richtet sich an Einsteiger. Wenn du aber mit Defold und der Spieleentwicklung noch gar nicht vertraut bist, empfehlen wir dir, zuerst einige einführende Handbücher zu lesen, insbesondere über [Defolds Bausteine](/manuals/building-blocks/) und das [Glossar](/manuals/glossary/). Falls du Defold noch nicht heruntergeladen hast, sieh dir das [Installationshandbuch](/manuals/install/) an. Empfehlenswert ist auch die [Übersicht des Editors](/manuals/editor/), um dich schnell im Editor zurechtzufinden. Hier zeigen wir aber ebenfalls Bildschirmaufnahmen zu jedem Schritt.

## Das Projekt erstellen {#creating-the-project}

Starte Defold und:

1. Wähle auf der linken Seite *Create From* ▸ *Templates*.
2. Wähle *Empty Project*.
3. Gib im Feld *Title* einen Projektnamen ein.
4. Wähle unter *Location* einen Speicherort für das Projekt.
5. Klicke auf *Create New Project*.

![Projekt erstellen](images/snake/1.png)

<input type="checkbox"/> Erledigt!

## Projekteinstellungen {#project-settings}

Zuerst legen wir die Auflösung des Spiels fest.

1. Suche nach dem Öffnen des Editors auf der linken Seite im Bereich *Assets* nach der Datei `game.project`. Doppelklicke darauf, um sie zu öffnen.
2. Gehe zum Abschnitt *Display* der Datei `game.project`.
3. Setze die Abmessungen des Spiels (`Width` und `Height`) auf 768 × 768 oder ein anderes Vielfaches von 16.

![Anzeigeeinstellungen](images/snake/2.png)

Das ist sinnvoll, weil das Spiel auf einem Raster gezeichnet wird, in dem jedes Segment 16 × 16 Pixel groß ist. So schneidet der Spielbildschirm keine Segmente teilweise ab. Die Datei `game.project` enthält alle wichtigen Einstellungen des Projekts. Du kannst sie im [Handbuch zu den Projekteinstellungen](/manuals/project-settings/) nachlesen.

<input type="checkbox"/> Erledigt!

## Neue Ordner im Bereich Assets erstellen {#creating-new-folders-in-the-assets-pane}

Für einen minimalistischen Snake-Klon brauchst du nur wenig Grafik: ein grünes Segment mit 16 × 16 Pixeln für die Schlange, einen weißen Block für die Hindernisse und einen kleineren roten Block, der das Futter darstellt.

Erstelle zuerst im Defold-Editor ein Verzeichnis für die Assets:

1. Klicke mit der <kbd>rechten Maustaste</kbd> auf den Ordner `main`
2. Wähle `New Folder`.
3. Ein Popup fragt nach einem Namen. Gib `assets` ein und klicke auf `Create Folder`.

![Neuer Ordner](images/snake/3.png)

<input type="checkbox"/> Erledigt!

## Dem Spiel Grafiken hinzufügen {#adding-graphics-to-the-game}

Das folgende Bild ist das einzige Asset, das du brauchst:

![Snake-Sprites](images/snake/snake.png)

1. Klicke mit der <kbd>rechten Maustaste</kbd> auf das Bild oben und speichere es auf deinem lokalen Datenträger. Ziehe das heruntergeladene Bild anschließend an den gerade erstellten Ort im Projektordner und lege es dort ab (oder kopiere es und füge es dort ein).

![Neuer Ordner](images/snake/4.png)

Weitere Einzelheiten zum [Importieren von Assets findest du hier](/manuals/importing-graphics/).

<input type="checkbox"/> Erledigt!

## Eine Kachelquelle hinzufügen {#adding-a-tile-source}

Defold bietet eine integrierte Komponente (component) für [Kachelkarten](/manuals/tilemap/), mit der du das Spielfeld aus *Kacheln* erstellst, die in einem Raster angeordnet sind. Eine Kachelkarte ermöglicht es dir, einzelne Kacheln zu setzen und auszulesen, was perfekt zu diesem Spiel passt. Da Kachelkarten ihre Grafiken aus einer [Kachelquelle](/manuals/tilesource/) (tile source) beziehen, musst du eine erstellen:

1. Klicke mit der <kbd>rechten Maustaste</kbd> auf den Ordner `assets`.
2. Wähle `New` ▸ `Tile Source` im Abschnitt „Resources“.
3. Nenne die neue Datei „snake“ (der Editor speichert die Datei als `snake.tilesource`).

![Neue Kachelquelle](images/snake/5.png)

Die Kachelquelle öffnet sich in einem eigenen Kachelquelleneditor für diesen Dateityp. Du wirst aufgefordert, ein Bild dafür anzugeben, damit sie funktioniert. Auf der rechten Seite findest du den Bereich `Properties`:

4. Setze die Eigenschaft `Image` auf die gerade importierte Grafikdatei.
![Kachelquelle](images/snake/6.png)

5. Die Eigenschaften `Width` und `Height` sollten auf 16 (dem Standardwert) bleiben. Dadurch wird das 32 × 32 Pixel große Bild in 4 Kacheln mit den Nummern 1–4 aufgeteilt.

![Eigenschaften der Kachelquelle](images/snake/7.png)

Beachte, dass die Eigenschaft *Extrude Borders* auf 2 Pixel gesetzt ist. Das verhindert Bildfehler an den Rändern von Kacheln, deren Grafik bis ganz an den Rand reicht.

Wenn du eine Datei änderst, erscheint neben ihrem Namen auf ihrer Registerkarte ein Sternchen `*`. Wähle `File` ▸ `Save All` oder verwende die Tastenkombination <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>⌘Cmd</kbd> + <kbd>S</kbd> auf dem Mac), um alle Dateien zu speichern.

<input type="checkbox"/> Erledigt!

## Die Kachelkarte für das Spielfeld erstellen {#creating-the-playfield-tile-map}

Deine Kachelquelle ist jetzt einsatzbereit. Es ist also Zeit, die Kachelkartenkomponente für das Spielfeld zu erstellen:

1. Klicke mit der <kbd>rechten Maustaste</kbd> auf den Ordner `main` und wähle <kbd>New</kbd> ▸ <kbd>Tile Map</kbd> im Abschnitt „Components“. Nenne die neue Datei „grid“ (der Editor speichert die Datei als „grid.tilemap“).
![Kachelkarte hinzufügen](images/snake/8.png)

2. Sie öffnet sich in einem Kachelkarteneditor, der hervorhebt, dass eine **Tile Source** benötigt wird. Setze deshalb die Eigenschaft *Tile Source* auf die zuvor erstellte Datei „snake.tilesource“.
![Kachelquelle festlegen](images/snake/9.png)

<input type="checkbox"/> Erledigt!

## Kacheln in die Kachelkarte zeichnen {#drawing-tiles-in-the-tile-map}

Defold speichert nur den tatsächlich verwendeten Bereich der Kachelkarte. Du musst daher genügend Kacheln hinzufügen, um den Bildschirm bis zu seinen Grenzen auszufüllen.

1. Wähle im Bereich `Outline` auf der rechten Seite die Ebene `layer1`.
2. Wähle den Menüpunkt `Edit` ▸ `Select Tile...` oder die Taste <kbd>Space</kbd>, um die Kachelpalette anzuzeigen. Klicke dann auf die Kachel, die du zum Zeichnen verwenden möchtest.
![Kachelkarte](images/snake/10.png)

3. Zeichne einen Rand entlang des Bildschirmrands und einige Hindernisse.
![Fertige Kachelkarte](images/snake/11.png)

Du brauchst eine Kachelkarte mit 48 × 48 Kacheln, um unseren Spielbildschirm auszufüllen (denn unsere Anzeige ist 768 Pixel groß und unsere Kacheln sind 16 Pixel groß, also 768/16 = 48).

Speichere die Kachelkarte, wenn du fertig bist.

<input type="checkbox"/> Erledigt!

## Die Kachelkarte zum Spiel hinzufügen {#adding-the-tile-map-to-the-game}

Jetzt müssen wir unsere Kachelkarte zum Spiel hinzufügen. Wenn du mit Defolds Bausteinen vertraut bist, weißt du: Komponenten sind Teil von Spielobjekten (game objects), und Spielobjekte können in Sammlungen (collections) definiert werden.

1. Öffne `main.collection`, indem du im Bereich `Assets` darauf doppelklickst. In der Vorlage Empty Project ist dies standardmäßig die Startsammlung (bootstrap collection), die beim Start der Engine geladen wird.

2. Klicke mit der <kbd>rechten Maustaste</kbd> auf die Wurzel in `Outline` und wähle `Add Game Object`. Dadurch entsteht ein neues Spielobjekt in der Sammlung, die beim Spielstart geladen wird.
![Spielobjekt hinzufügen](images/snake/12.png)

3. Klicke mit der <kbd>rechten Maustaste</kbd> auf das neue Spielobjekt und wähle `Add Component File`. Wähle die gerade erstellte Datei „grid.tilemap“.
![Komponente hinzufügen](images/snake/13.png)

Jetzt haben wir eine Kachelkarte in unserer Spielsammlung. Sie sollte sichtbar sein, wenn du das Spiel aus dem Editor startest.

1. Wähle `Project` ▸ `Build` oder verwende die Tastenkombination <kbd>Ctrl</kbd> + <kbd>B</kbd> (<kbd>⌘Cmd</kbd> + <kbd>B</kbd> auf dem Mac).

![Spiel starten](images/snake/14.png)

<input type="checkbox"/> Erledigt!

## Dem Spiel ein Skript hinzufügen {#adding-a-script-to-the-game}

1. Klicke mit der <kbd>rechten Maustaste</kbd> im Browser `Assets` auf den Ordner `main` und wähle `New` ▸ `Script` im Abschnitt Scripts. Nenne die neue Skriptdatei „snake“ (sie wird als „snake.script“ gespeichert). Diese Datei wird die gesamte Spiellogik enthalten.
![Skript hinzufügen](images/snake/15.png)

2. Kehre zu *main.collection* zurück und klicke mit der <kbd>rechten Maustaste</kbd> auf das Spielobjekt, das die Kachelkarte enthält. Wähle <kbd>Add&nbsp;Component&nbsp;File</kbd> und dann die Datei „snake.script“.

![Hauptsammlung](images/snake/16.png)

Jetzt sind die Kachelkartenkomponente und das Skript eingerichtet.

<input type="checkbox"/> Erledigt!

## Das Spielskript {#the-game-script}

Das Skript, das du jetzt schreibst, wird das gesamte Spiel steuern. Wir fügen die Funktionen nach und nach hinzu.

### Einfacher Bewegungsalgorithmus {#simple-movement-algorithm}

Die Idee dafür ist folgende:

1. Das Skript führt eine Liste der Kachelpositionen, die die Schlange aktuell belegt.
2. Wenn der Spieler eine Richtungstaste drückt, speichert es die Richtung, in die sich die Schlange bewegen soll.
3. In regelmäßigen Abständen bewegt es die Schlange einen Schritt in die aktuelle Bewegungsrichtung.

### Initialisierung {#initialization}

Öffne *snake.script* und suche die Funktion `init()`. Die Engine ruft diese Funktion auf, wenn das Skript beim Spielstart initialisiert wird. Ändere den Code wie folgt:

```lua
function init(self)
    self.segments = { -- <1>
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0} -- <2>
    self.speed = 7.0 -- <3>
    self.time = 0 -- <4>
end
```

In diesem Code führen wir Folgendes aus:

1. Wir speichern die Segmente der Schlange in einer Lua-Tabelle namens `self.segments`. Sie enthält eine Liste von Tabellen, die jeweils die X- und Y-Position eines Segments speichern.
2. Wir speichern die aktuelle Richtung in einer Tabelle namens `self.dir`, die eine X- und eine Y-Richtung enthält.
3. Wir speichern die aktuelle Bewegungsgeschwindigkeit in `self.speed`, angegeben in Kacheln pro Sekunde.
4. Wir speichern in `self.time` einen Zeitgeberwert, mit dem wir die Bewegungsgeschwindigkeit steuern werden.

Der Skriptcode oben ist in der Sprache Lua geschrieben. Es gibt ein paar Dinge am Code zu beachten, aber wenn du etwas davon noch nicht verstehst, mach dir keine Sorgen. Mach einfach mit, experimentiere und lass dir Zeit --- irgendwann wirst du es verstehen. Für den Moment kannst du dir merken, dass wir in `init()` nur die Variablen initialisiert haben, die wir verwenden werden.

- Defold reserviert eine Reihe integrierter Callback-*Funktionen*, die während der Lebensdauer einer Skriptkomponente aufgerufen werden. Das sind *keine* Methoden, sondern gewöhnliche Funktionen.
- Die Laufzeitumgebung übergibt über den Parameter `self` eine Referenz auf die aktuelle Instanz der Skriptkomponente. Die Referenz `self` wird zum Speichern von Instanzdaten verwendet.
- Du kannst die Referenz `self` wie eine Lua-Tabelle verwenden, in der du Daten speicherst. Verwende dafür einfach die Punktnotation wie bei jeder anderen Tabelle: `self.data = "value"`. Die Referenz ist während der gesamten Lebensdauer des Skripts gültig, in diesem Fall vom Spielstart bis zum Beenden des Spiels.
- Lua-Tabellenliterale werden von geschweiften Klammern `{}` umschlossen.
- Tabelleneinträge können Schlüssel-Wert-Paare (`{x = 10, y = 20}`), verschachtelte Lua-Tabellen (`{ {a = 1}, {b = 2} }`) oder andere Datentypen sein.

<input type="checkbox"/> Erledigt!

### Aktualisierung {#update}

Die Funktion `init()` wird genau einmal aufgerufen, wenn die Skriptkomponente im laufenden Spiel instanziiert wird. Die Funktion `update()` hingegen wird einmal **pro Frame** aufgerufen. Damit eignet sie sich ideal für Spiellogik in Echtzeit.

Die Idee für die Aktualisierung ist, in einem festgelegten Zeitabstand Folgendes zu tun:

1. Ermittle die Position des Schlangenkopfs und erstelle dann einen neuen Kopf an der benachbarten Position, die um die aktuelle Bewegungsrichtung versetzt ist. Wenn sich die Schlange also mit X=1 und Y=0 bewegt und der aktuelle Kopf bei X=0 und Y=0 liegt, sollte der neue Kopf bei X=1 und Y=0 liegen.
2. Speichere die neue Kopfposition in der Liste der Segmente, aus denen die Schlange besteht.
3. Lies die Position des Schwanzendes aus der Segmenttabelle aus.
4. Lösche die Kachel des Schwanzendes an dieser Position.
5. Zeichne alle Schlangensegmente (Kacheln) an den Positionen aus der Tabelle.

![Algorithmus](images/snake/17.png)

:::sidenote
Denk daran, dass der Kopf unserer Schlange am Ende der Tabelle steht und das Schwanzende am Anfang.
:::

1. Suche die Funktion `update()` in *snake.script* und ändere den Code wie folgt:

```lua
function update(self, dt)
    self.time = self.time + dt -- <1>
    if self.time >= 1.0 / self.speed then -- <2>
        local head = self.segments[#self.segments] -- <3>

        local newhead = {
            x = head.x + self.dir.x,
            y = head.y + self.dir.y
        } -- <4>

        table.insert(self.segments, newhead) -- <5>

        local tail = table.remove(self.segments, 1) -- <6>

        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0) -- <7>

        for i, s in ipairs(self.segments) do -- <8>
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2) -- <9>
        end

        self.time = 0 -- <10>
    end
end
```

In diesem Code führen wir Folgendes aus:

1. Wir erhöhen den Zeitgeber um die Zeitdifferenz (in Sekunden) seit dem letzten Aufruf von `update()` --- die sogenannte „delta time“, kurz `dt`.
2. Wenn genügend Zeit vergangen ist:
3. Wir lesen die aktuelle Kopfposition aus. `#` ist der Operator, mit dem du die Länge einer Tabelle ermittelst, sofern sie als Array verwendet wird. Das ist bei uns der Fall --- alle Segmente sind Tabellenwerte ohne angegebenen Schlüssel.
4. Wir erstellen anhand der aktuellen Kopfposition und der Bewegungsrichtung (`self.dir`) ein neues Kopfsegment.
5. Wir fügen den neuen Kopf am Ende der Segmenttabelle hinzu.
6. Wir entfernen das Schwanzende vom Anfang der Segmenttabelle.
7. Wir löschen die Kachel an der Position des entfernten Schwanzendes. Unsere Kachelkarte `#grid` hat nur 1 Ebene namens `layer1`.
8. Wir durchlaufen die Elemente der Segmenttabelle. Bei jedem Durchlauf enthält `i` die Position in der Tabelle (beginnend bei 1) und `s` das aktuelle Segment.
9. Wir setzen die Kachel an der Position des Segments auf den Wert 2 (die Kachel mit der grünen Farbe der Schlange).
10. Zum Schluss setzen wir den Zeitgeber auf null zurück.

Wenn du das Spiel jetzt startest, solltest du sehen, wie die 4 Segmente lange Schlange von links nach rechts über das Spielfeld kriecht.

![Spiel starten](images/snake/snake_run_1.png)

<input type="checkbox"/> Erledigt!

## Spielereingaben {#player-input}

Bevor du Code hinzufügst, der auf Spielereingaben reagiert, musst du die Eingabezuordnungen einrichten.

### Eingabebindungen {#input-bindings}

1. Suche im Ordner `input` die Datei `game.input_binding` und öffne sie mit einem <kbd>Doppelklick</kbd>.
2. Füge Eingabebindungen (input bindings) vom Typ *Key Trigger* für Bewegungen nach oben, unten, links und rechts hinzu. Wähle in der Spalte *Input* die Tastaturtasten aus und gib in der Spalte *Action* die Aktionsnamen ein.

![Eingabe](images/snake/18.png)

Die Eingabebindungsdatei ordnet tatsächliche Benutzereingaben (Tasten, Mausbewegungen usw.) den *Namen* von Aktionen zu. Diese werden an Skripte weitergegeben, die Eingaben angefordert haben.

<input type="checkbox"/> Erledigt!

### Den Eingabefokus anfordern {#acquiring-input-focus}

Wenn die Bindungen eingerichtet sind, öffne *snake.script* und füge am Anfang der Funktion `init()` die folgende Zeile hinzu:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0
end
```

Die hinzugefügte Zeile:
1. Sendet eine Nachricht an das aktuelle Spielobjekt („.“ ist die Kurzform für das aktuelle Spielobjekt), die es auffordert, Eingaben von der Engine zu empfangen.

Suche dann die Funktion `on_input` und gib den folgenden Code ein:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then -- <1>
        self.dir.x = 0 -- <2>
        self.dir.y = 1
    elseif action_id == hash("down") and action.pressed then
        self.dir.x = 0
        self.dir.y = -1
    elseif action_id == hash("left") and action.pressed then
        self.dir.x = -1
        self.dir.y = 0
    elseif action_id == hash("right") and action.pressed then
        self.dir.x = 1
        self.dir.y = 0
    end
end
```

Diese `if...elseif...`-Verzweigungen führen Folgendes aus:
1. Wenn die Eingabeaktion „up“ empfangen wird, wie in den Eingabebindungen eingerichtet, und das Feld `pressed` in der Tabelle `action` auf `true` gesetzt ist (der Spieler hat die Taste gedrückt), dann:
2. Setzen sie die Bewegungsrichtung.

Starte das Spiel erneut und prüfe, ob du die Schlange steuern kannst.

<input type="checkbox"/> Erledigt!

### Die Eingabeverarbeitung verbessern {#improving-input-handling}

Beachte nun, dass das gleichzeitige Drücken zweier Tasten zu zwei Aufrufen von `on_input()` führt, einem für jeden Tastendruck. Im oben gezeigten Code wirkt sich nur der letzte Aufruf auf die Richtung der Schlange aus, weil nachfolgende Aufrufe von `on_input()` die Werte in `self.dir` überschreiben.

Beachte außerdem, dass die Schlange in sich selbst hineinsteuert, wenn sie sich nach links bewegt und du die Taste <kbd>right</kbd> drückst. Die *scheinbar* naheliegende Lösung ist, den `if`-Bedingungen in `on_input()` eine weitere Bedingung hinzuzufügen:

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

Wenn sich die Schlange jedoch nach links bewegt und der Spieler vor dem nächsten Bewegungsschritt *schnell* zuerst <kbd>up</kbd> und dann <kbd>right</kbd> drückt, wirkt sich nur der Tastendruck auf <kbd>right</kbd> aus, und die Schlange bewegt sich in sich selbst hinein. Mit den oben ergänzten Bedingungen in den `if`-Abfragen wird die Eingabe ignoriert. *Nicht gut!*

Eine geeignete Lösung ist, die Eingaben in einer Warteschlange zu speichern und bei jeder Bewegung der Schlange Einträge daraus zu entnehmen:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0

    self.dirqueue = {} -- <1>
end
```

Diesmal haben wir:
1. Eine Variable `self.dirqueue` hinzugefügt, die als leere Tabelle initialisiert wird.

Ergänze die Funktion `update()` wie folgt:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed then
        local newdir = table.remove(self.dirqueue, 1) -- <1>
        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y -- <2>
            if not opposite then
                self.dir = newdir -- <3>
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tail = table.remove(self.segments, 1)
        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0)

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end
```

1. Entnimm den ersten Eintrag aus der Richtungswarteschlange.
2. Wenn ein Eintrag vorhanden ist (`newdir` ist nicht null), prüfe, ob `newdir` in die entgegengesetzte Richtung zu `self.dir` zeigt.
3. Setze die neue Richtung nur, wenn sie nicht in die entgegengesetzte Richtung zeigt.

Ändere außerdem `on_input` so, dass es die aktuelle Eingabe stattdessen in der Warteschlange speichert:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1}) -- <1>
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

1. Füge die Eingaberichtung zur Richtungswarteschlange hinzu, statt `self.dir` direkt zu setzen.

Starte das Spiel und prüfe, ob es sich wie erwartet spielt.

<input type="checkbox"/> Erledigt!

## Futter und Kollisionen mit Hindernissen {#food-and-collision-with-obstacles}

Die Schlange braucht Futter auf der Karte, damit sie lang und schnell werden kann. Fügen wir es hinzu!

### Das Futter erzeugen {#spawning-the-food}

Füge oberhalb der Funktion `init()` eine neue Funktion hinzu:

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end
```

In dieser Funktion führen wir Folgendes aus:
1. Wir deklarieren eine neue Funktion namens `put_food()`, die ein Stück Futter auf der Karte platziert.
2. Wir speichern eine zufällige X- und Y-Position in einer Variablen namens `self.food`.
3. Wir setzen die Kachel an der Position X und Y auf den Wert 3. Das ist die Kachelgrafik für das Futter.

Rufe sie dann am Ende der Funktion `init()` auf:
```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    math.randomseed(socket.gettime()) -- <1>
    put_food(self) -- <2>
end
```

1. Setze den Startwert des Zufallszahlengenerators, bevor du mit `math.random()` Zufallswerte abrufst. Sonst wird dieselbe Folge von Zufallswerten erzeugt. Dieser Startwert sollte nur einmal gesetzt werden.
2. Rufe die Funktion `put_food()` beim Spielstart auf, damit sich zu Beginn ein Stück Futter auf der Karte befindet.

<input type="checkbox"/> Erledigt!

### Das Futter fressen {#eating-the-food}

Um jetzt zu erkennen, ob die Schlange mit etwas kollidiert, musst du nur nachsehen, was sich auf der Kachelkarte an der Position befindet, auf die die Schlange zusteuert, und darauf reagieren.

Füge eine Variable hinzu, die festhält, ob die Schlange lebt oder nicht:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true -- <1>

    math.randomseed(socket.gettime())
    put_food(self)
end
```

1. Ein Kennzeichen, das angibt, ob die Schlange lebt oder nicht.

Füge dann Logik hinzu, die auf Kollisionen mit Wänden/Hindernissen und Futter prüft:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then -- <1>
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y) -- <2>

        if tile == 2 or tile == 4 then
            self.alive = false -- <3>
        elseif tile == 3 then
            self.speed = self.speed + 1 -- <4>
            put_food(self)
        else
            local tail = table.remove(self.segments, 1) -- <5>
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end
```

1. Bewege die Schlange nur weiter, wenn sie lebt.
2. Lies vor dem Zeichnen auf die Kachelkarte aus, was sich an der Position des neuen Schlangenkopfs befindet.
3. Wenn die Kachel ein Hindernis oder ein anderer Teil der Schlange ist, ist das Spiel vorbei!
4. Wenn die Kachel Futter ist, erhöhe die Geschwindigkeit und platziere dann ein neues Stück Futter.
5. Beachte, dass das Schwanzende nur entfernt wird, wenn keine Kollision vorliegt. Wenn der Spieler Futter frisst, wächst die Schlange deshalb um ein Segment, weil bei diesem Zug kein Schwanzende entfernt wird.

Probiere das Spiel jetzt aus und stelle sicher, dass es sich gut spielt!

Damit ist das Tutorial abgeschlossen. Experimentiere aber gern weiter mit dem Spiel und bearbeite einige der folgenden Übungen!

<input type="checkbox"/> Erledigt!

## Das vollständige Skript {#the-complete-script}

Hier ist der vollständige Skriptcode zum Nachschlagen:

```lua
local function put_food(self)
    self.food = {x = math.random(2, 47), y = math.random(2, 47)}
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3)        
end

function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true

    math.randomseed(socket.gettime())
    put_food(self)
end

function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y)

        if tile == 2 or tile == 4 then
            self.alive = false
        elseif tile == 3 then
            self.speed = self.speed + 1
            put_food(self)
        else
            local tail = table.remove(self.segments, 1)
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end

function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1})
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

## Übungen {#exercises}

Es ist eine gute Übung, diese Verbesserungen umzusetzen:

1. Füge die Verarbeitung einer Tastatureingabe hinzu, um das Spiel nach dem Spielende neu zu starten.
2. Füge eine Punktewertung und einen Punktezähler hinzu, entweder nur mit einer Beschriftungskomponente (einfacher) oder mit einer vollständigen GUI.
3. Die Funktion put_food() berücksichtigt weder die Position der Schlange noch Hindernisse. Behebe das, sodass Futter nur an freien Stellen erzeugt wird.
4. Zeige nach dem Spielende die Nachricht „Game Over“ an und ermögliche dem Spieler einen neuen Versuch.
5. Zusatzaufgabe: Füge eine zweite, vom Spieler gesteuerte Schlange hinzu.
