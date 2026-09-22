---
title: Ein 15-Puzzle in Defold erstellen
brief: Wenn du neu bei Defold bist, hilft dir diese Anleitung, mit einigen Bausteinen von Defold zu experimentieren und Skriptlogik auszuführen.
---

# Das klassische 15-Puzzle {#the-classic-15-puzzle}

Dieses bekannte Puzzle wurde in Amerika in den 1870er-Jahren populär. Ziel des Puzzles ist es, die Kacheln auf dem Spielbrett durch horizontales und vertikales Verschieben in die richtige Reihenfolge zu bringen. Das Puzzle beginnt mit einer Anordnung, in der die Kacheln durcheinandergewürfelt sind.

Bei der gängigsten Version des Puzzles stehen auf den Kacheln die Zahlen 1--15. Du kannst das Puzzle jedoch etwas anspruchsvoller machen, indem die Kacheln Teile eines Bildes darstellen. Versuche, das Puzzle zu lösen, bevor wir beginnen. Klicke auf eine Kachel neben dem leeren Feld, um sie auf die leere Position zu schieben.

## Das Projekt erstellen {#creating-the-project}

1. Starte Defold.
2. Wähle links *New Project*.
3. Wähle den Tab *From Template*.
4. Wähle *Empty Project*
5. Wähle einen Speicherort für das Projekt auf deinem lokalen Laufwerk.
6. Klicke auf *Create New Project*.

Öffne die Einstellungsdatei *game.project* und setze die Abmessungen des Spiels auf 512 × 512. Diese Abmessungen entsprechen dem Bild, das du verwenden wirst.

![Anzeigeeinstellungen](images/15-puzzle/display_settings.png)

Lade als Nächstes ein geeignetes Bild für das Puzzle herunter. Wähle ein beliebiges quadratisches Bild und achte darauf, es auf 512 mal 512 Pixel zu skalieren. Wenn du nicht nach einem Bild suchen möchtest, kannst du dieses verwenden:

![Mona Lisa](images/15-puzzle/monalisa.png)

Lade das Bild herunter und ziehe es dann in den Ordner *main* deines Projekts.

## Das Raster darstellen {#representing-the-grid}

Defold enthält die eingebaute Komponente (component) *Kachelkarte* (tile map), die sich perfekt zur Darstellung des Spielbretts eignet. Mit Kachelkarten kannst du einzelne Kacheln setzen und auslesen, und mehr brauchst du für dieses Projekt nicht.

Bevor du die Kachelkarte erstellst, benötigst du jedoch eine *Kachelquelle* (tile source), aus der die Kachelkarte ihre Kachelbilder bezieht.

Mache einen <kbd>Rechtsklick</kbd> auf den Ordner *main* und wähle <kbd>New ▸ Tile Source</kbd>. Nenne die neue Datei `monalisa.tilesource`.

Setze die Kacheleigenschaften *Width* und *Height* auf 128. Dadurch wird das 512 × 512 Pixel große Bild in 16 Kacheln aufgeteilt. Die Kacheln werden mit 1--16 nummeriert, wenn du sie auf der Kachelkarte platzierst.

![Kachelquelle](images/15-puzzle/tilesource.png)

Mache als Nächstes einen <kbd>Rechtsklick</kbd> auf den Ordner *main* und wähle <kbd>New ▸ Tile Map</kbd>. Nenne die neue Datei "grid.tilemap".

Defold erfordert, dass du das Raster initialisierst. Wähle dazu die Ebene "layer1" und male das 4 × 4 große Kachelraster direkt oberhalb und rechts vom Ursprung. Es ist dabei nicht entscheidend, welche Kacheln du setzt. Du wirst gleich Code schreiben, der den Inhalt dieser Kacheln automatisch festlegt.

![Kachelkarte](images/15-puzzle/tilemap.png)

## Die Teile zusammenfügen {#putting-the-pieces-together}

Öffne die Sammlung (collection) *main.collection*. Mache einen <kbd>Rechtsklick</kbd> auf den Wurzelknoten in der Ansicht *Outline* und wähle <kbd>Add Game Object</kbd>. Setze die Eigenschaft *Id* des neuen Spielobjekts (game object) auf "game".

Mache einen <kbd>Rechtsklick</kbd> auf das Spielobjekt und wähle <kbd>Add Component File</kbd>. Wähle die Datei *grid.tilemap*. Setze die Eigenschaft *Id* auf "tilemap".

Mache einen <kbd>Rechtsklick</kbd> auf das Spielobjekt und wähle <kbd>Add Component ▸ Label</kbd>. Setze die Eigenschaft *Id* der Beschriftungskomponente (label) auf "done" und ihre Eigenschaft *Text* auf "Well done". Verschiebe die Beschriftung in die Mitte der Kachelkarte.

Setze die Z-Position der Beschriftung auf 1, damit sie über dem Raster gezeichnet wird.

![Hauptsammlung](images/15-puzzle/main_collection.png)

Erstelle als Nächstes eine Lua-Skriptdatei für die Puzzlelogik: Mache einen <kbd>Rechtsklick</kbd> auf den Ordner *main* und wähle <kbd>New ▸ Script</kbd>. Nenne die neue Datei "game.script".

Mache dann einen <kbd>Rechtsklick</kbd> auf das Spielobjekt namens "game" in *main.collection* und wähle <kbd>Add Component File</kbd>. Wähle die Datei *game.script*.

Starte das Spiel. Du solltest das Raster so sehen, wie du es gezeichnet hast, und darüber die Beschriftung mit der Meldung "Well done".

## Die Puzzlelogik {#the-puzzle-logic}

Jetzt sind alle Teile an ihrem Platz, sodass sich der Rest des Tutorials dem Aufbau der Puzzlelogik widmet.

Das Skript verwaltet eine eigene Darstellung der Kacheln des Spielbretts, getrennt von der Kachelkarte. So lässt sich die Verarbeitung erleichtern. Statt die Kacheln in einem zweidimensionalen Array zu speichern, werden sie als eindimensionale Liste in einer Lua-Tabelle gespeichert. Die Liste enthält die Kachelnummern in ihrer Reihenfolge, beginnend in der oberen linken Ecke des Rasters bis hin zur unteren rechten Ecke:

```lua
-- The completed board looks like this:
self.board = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}
```

Der Code, der eine solche Kachelliste auf unserer Kachelkarte zeichnet, ist recht einfach. Er muss jedoch die Position in der Liste in eine x- und eine y-Position umrechnen:

```lua
-- Draw a table list of tiles onto a 4x4 tilemap
local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4) -- <1>
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end
```
1. In Kachelkarten befindet sich die Kachel mit dem x-Wert 1 und dem y-Wert 1 unten links. Deshalb muss die y-Position umgekehrt werden.

Du kannst prüfen, ob die Funktion wie beabsichtigt arbeitet, indem du zum Testen eine `init()`-Funktion erstellst:

```lua
function init(self)
    -- An inverted board, for test
    self.board = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    draw(self.board)
end
```

Da die Kacheln als Liste in einer Lua-Tabelle vorliegen, lässt sich ihre Reihenfolge sehr leicht mischen. Der Code durchläuft einfach jedes Element der Liste und vertauscht jede Kachel mit einer anderen, zufällig ausgewählten Kachel:

```lua
-- Swap two items in a table list
local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

-- Randomize the order of a the elements in a table list
local function scramble(t)
    local n = #t
    for i = 1, n - 1 do
        t = swap(t, i, math.random(i, n))
    end
    return t
end
```

Bevor du fortfährst, musst du eine Besonderheit des 15-Puzzles beachten: Wenn du die Kacheln wie oben zufällig anordnest, besteht eine Wahrscheinlichkeit von 50 %, dass das Puzzle *unmöglich* zu lösen ist.

Das ist eine schlechte Nachricht, denn du möchtest dem Spieler auf keinen Fall ein unlösbares Puzzle vorsetzen.

Glücklicherweise lässt sich feststellen, ob eine Anordnung lösbar ist. Das geht so:

## Lösbarkeit {#solvability}

Um herauszufinden, ob eine Anordnung in einem 4 × 4 großen Puzzle lösbar ist, benötigst du zwei Informationen:

1. Die Anzahl der „Inversionen“ in der Anordnung. Eine Inversion liegt vor, wenn eine Kachel vor einer anderen Kachel mit einer kleineren Zahl steht. Die Liste `{1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 0}` hat beispielsweise 3 Inversionen:

    - Auf die Zahl 12 folgen 11 und 10, was 2 Inversionen ergibt.
    - Auf die Zahl 11 folgt 10, was 1 weitere Inversion ergibt.

    (Beachte, dass der gelöste Zustand des Puzzles keine Inversionen hat.)

2. Die Zeile, in der sich das leere Feld befindet (in der Liste durch `0` dargestellt).

Diese beiden Zahlen lassen sich mit den folgenden Funktionen berechnen:

```lua
-- Count the number of inversions in a list of tiles
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then -- <1>
                inv = inv + 1
            end
        end
    end
    return inv
end
```
1. Beachte, dass das leere Feld nicht mitgezählt wird.

```lua
-- Find the x and y position of a given tile
local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4) -- <1>
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end
```
1. Die y-Position, von unten gezählt.

Anhand dieser beiden Zahlen lässt sich nun feststellen, ob ein Zustand des Puzzles lösbar ist. Ein Zustand eines 4 × 4 großen Spielbretts ist *lösbar*, wenn:

- das leere Feld in einer *ungeraden* Zeile liegt (1 oder 3, von unten gezählt) und die Anzahl der Inversionen *gerade* ist.
- das leere Feld in einer *geraden* Zeile liegt (2 oder 4, von unten gezählt) und die Anzahl der Inversionen *ungerade* ist.

## Wie funktioniert das? {#how-does-this-work}

Bei jedem erlaubten Zug wird eine Kachel verschoben, indem sie horizontal oder vertikal ihren Platz mit dem leeren Feld tauscht.

Wird eine Kachel horizontal verschoben, ändert sich weder die Anzahl der Inversionen noch die Zeilennummer des leeren Feldes.

Wird eine Kachel dagegen vertikal verschoben, ändert sich die Parität der Anzahl der Inversionen (von ungerade zu gerade oder von gerade zu ungerade). Außerdem ändert sich die Parität der Zeilennummer des leeren Feldes.

Zum Beispiel:

![Eine Kachel verschieben](images/15-puzzle/slide.png)

Dieser Zug ändert die Kachelreihenfolge von:

`{ ... 0, 11, 2, 13, 6 ... }`

zu

`{ ... 6, 11, 2, 13, 0 ... }`

Die Gesamtzahl der Inversionen verringert sich dabei um 1:

- Die Zahl 6 fügt 1 Inversion hinzu (die Zahl 2 steht jetzt nach der 6).
- Die Zahl 11 verliert 1 Inversion (die Zahl 6 steht jetzt vor der 11).
- Die Zahl 13 verliert 1 Inversion (die Zahl 6 steht jetzt vor der 13).

Durch vertikales Verschieben kann sich die Anzahl der Inversionen um ±1 oder ±3 ändern.

Die Zeilennummer des leeren Feldes kann sich durch vertikales Verschieben um ±1 ändern.

Im Endzustand des Puzzles befindet sich das leere Feld in der unteren rechten Ecke (der *ungeraden* Zeile 1), und die Anzahl der Inversionen hat den *geraden* Wert 0. Jeder erlaubte Zug lässt diese beiden Werte entweder unverändert (horizontales Verschieben) oder kehrt ihre Parität um (vertikales Verschieben). Kein erlaubter Zug kann jemals dazu führen, dass die Parität der Inversionsanzahl und der Zeilennummer des leeren Feldes *ungerade*, *ungerade* oder *gerade*, *gerade* ist.

Ein Zustand des Puzzles, in dem beide Zahlen ungerade oder beide gerade sind, ist daher unmöglich zu lösen.

Hier ist der Code, der die Lösbarkeit prüft:

```lua
-- Is the given table list of 4x4 tiles solvable?
local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end
```

## Benutzereingaben {#user-input}

Jetzt musst du nur noch dafür sorgen, dass sich das Puzzle bedienen lässt.

Erstelle eine `init()`-Funktion, die mithilfe der oben erstellten Funktionen alle Vorbereitungen zur Laufzeit trifft:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>
    math.randomseed(socket.gettime()) -- <2>
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}) -- <3>
    while not solvable(self.board) do -- <4>
        self.board = scramble(self.board)
    end
    draw(self.board) -- <5>
    self.done = false -- <6>
    msg.post("#done", "disable") -- <7>
end
```
1. Teile der Engine mit, dass dieses Spielobjekt Eingaben empfangen soll.
2. Initialisiere den Zufallszahlengenerator mit einem Startwert.
3. Erstelle einen zufälligen Anfangszustand für das Spielbrett.
4. Wenn der Zustand unlösbar ist, mische erneut.
5. Zeichne das Spielbrett.
6. Setze ein Abschluss-Flag, um festzuhalten, ob das Puzzle gelöst ist.
7. Deaktiviere die Beschriftung mit der Abschlussmeldung.

Öffne */input/game.input_bindings* und füge einen neuen *Mouse Trigger* hinzu. Setze den Namen der Aktion auf "press":

![Eingabe](images/15-puzzle/input.png)

Kehre zum Skript zurück und erstelle eine `on_input()`-Funktion.

```lua
-- Deal with user input
function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then -- <1>
        local x = math.ceil(action.x / 128) -- <2>
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0) -- <3>
        if math.abs(x - ex) + math.abs(y - ey) == 1 then -- <4>
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x) -- <5>
            draw(self.board) -- <6>
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then -- <7>
            self.done = true
            msg.post("#done", "enable")
        end
    end
end
```
1. Wenn eine Maustaste gedrückt wird und das Spiel noch läuft, führe Folgendes aus.
2. Berechne die x- und y-Koordinaten des Feldes, auf das der Benutzer geklickt hat.
3. Ermittle die aktuelle Position des leeren Feldes (0).
4. Wenn das angeklickte Feld direkt über, unter, links oder rechts neben dem leeren Feld liegt, führe Folgendes aus:
5. Vertausche die Kacheln auf dem angeklickten und dem leeren Feld.
6. Zeichne das aktualisierte Spielbrett neu.
7. Wenn die Anzahl der Inversionen auf dem Spielbrett 0 ist, also alles in der richtigen Reihenfolge steht, und sich das leere Feld in der äußersten rechten Spalte befindet (es muss in der letzten Zeile liegen, damit die Anzahl der Inversionen 0 ist), dann ist das Puzzle gelöst. Führe daher Folgendes aus:
8. Setze das Abschluss-Flag.
9. Aktiviere beziehungsweise zeige die Abschlussmeldung an.

Und das war's! Du bist fertig, das Puzzlespiel ist vollständig!

## Das vollständige Skript {#the-complete-script}

Hier ist der vollständige Skriptcode zum Nachschlagen:

```lua
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then
                inv = inv + 1
            end
        end
    end
    return inv
end

local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4)
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end

local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end

local function scramble(t)
    for i=1, #t do
        local tmp = t[i]
        local r = math.random(#t)
        t[i] = t[r]
        t[r] = tmp
    end
    return t
end

local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4)
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end

function init(self)
    msg.post(".", "acquire_input_focus")
    math.randomseed(socket.gettime())
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0})   
    while not solvable(self.board) do
        self.board = scramble(self.board)
    end
    draw(self.board)
    self.done = false
    msg.post("#done", "disable")
end

function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then
        local x = math.ceil(action.x / 128)
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0)
        if math.abs(x - ex) + math.abs(y - ey) == 1 then
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x)
            draw(self.board)
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then
            self.done = true
            msg.post("#done", "enable")
        end
    end
end

function on_reload(self)
    self.done = false
    msg.post("#done", "disable")
end
```

## Weitere Übungen {#further-exercises}

1. Erstelle ein 5 × 5 großes Puzzle und anschließend eines mit 6 × 5 Feldern. Achte darauf, dass die Lösbarkeitsprüfungen allgemein funktionieren.
2. Füge Verschiebeanimationen hinzu. Kacheln lassen sich nicht unabhängig von der Kachelkarte bewegen, also musst du dir dafür eine Lösung überlegen. Vielleicht eine separate Kachelkarte, die nur die gerade verschobene Kachel enthält?
