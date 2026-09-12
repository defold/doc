---
title: Magic Link-Tutorial
brief: In diesem Tutorial erstellst du ein vollständiges kleines Puzzlespiel mit einem Startbildschirm, der Spielmechanik und einem einfachen Levelfortschritt in Form zunehmender Schwierigkeit.
---

# Magic Link-Tutorial

Dieses Spiel ist eine Variante klassischer Kombinationsspiele wie _Bejeweled_ und _Candy Crush_. Durch Ziehen verbindet der Spieler Blöcke derselben Farbe, um sie zu entfernen. Das Ziel ist allerdings nicht, lange Reihen gleichfarbiger Blöcke zu entfernen, das Spielfeld zu leeren oder Punkte zu sammeln, sondern mehrere besondere „magische Blöcke“, die über das Spielfeld verteilt sind, miteinander zu verbinden.

Dieses Tutorial ist eine Schritt-für-Schritt-Anleitung, in der wir das Spiel auf Grundlage eines fertigen Designs erstellen. In der Praxis kostet es viel Zeit und Mühe, ein funktionierendes Design zu finden. Vielleicht beginnst du mit einer Grundidee und suchst dann nach einer Möglichkeit, sie als Prototyp umzusetzen, um ihr Potenzial besser zu verstehen. Selbst ein einfaches Spiel wie „Magic Link“ erfordert einiges an Designarbeit. Dieses Spiel durchlief mehrere Überarbeitungen und Experimente, bis es seine endgültige (und immer noch längst nicht perfekte) Form und seine Spielregeln hatte. Für dieses Tutorial überspringen wir diesen Prozess aber und beginnen direkt mit der Umsetzung des fertigen Designs.

## Erste Schritte {#getting-started}

Zunächst musst du ein neues Projekt erstellen und das Asset-Paket importieren:

* Erstelle ein [neues Projekt](/manuals/project-setup/#creating-a-new-project) aus der Vorlage „Empty Project“
* Lade das vollständige „Magic Link“-Projekt [magic-link.zip](https://github.com/defold/defold-examples/releases/latest) als Referenz herunter. Das vollständige Projekt enthält alle Assets, falls du das Projekt von Grund auf erstellen möchtest.

## Spielregeln {#game-rules}

![Schematische Darstellung der Spielregeln](images/magic-link/linker_rules.png)

Das Spielfeld wird in jeder Runde zufällig mit farbigen Blöcken und mehreren magischen Blöcken gefüllt. Für die farbigen Blöcke gelten diese Regeln:

* Sie verschwinden, wenn der Spieler sie durch Ziehen mit gleichfarbigen Blöcken verbindet.
* Wenn Blöcke verschwinden, hinterlassen sie Lücken. Farbige Blöcke fallen einfach senkrecht nach unten in die Lücken, die sich unter ihnen geöffnet haben.
* Der untere Bildschirmrand verhindert, dass Blöcke weiter nach unten fallen.

Die magischen Blöcke verhalten sich anders. Für sie gelten diese Regeln:

* Magische Blöcke bewegen sich _seitwärts_, wenn auf einer der beiden Seiten eine Lücke entsteht.
* Wenn unter ihnen eine Lücke entsteht, fallen sie stattdessen wie gewöhnliche farbige Blöcke nach unten.

Für die Interaktion des Spielers mit dem Spiel gelten die folgenden Regeln:

* Der Spieler kann farbige Blöcke durch Ziehen verbinden, wenn sie waagerecht, senkrecht oder diagonal aneinandergrenzen.
* Verbundene Blöcke verschwinden, sobald der Spieler die Berührungseingabe beendet (den Finger anhebt).
* Magische Blöcke reagieren nicht auf Ziehen und können nicht manuell verbunden werden.
* Magische Blöcke reagieren jedoch darauf, wenn sie waagerecht oder senkrecht aneinandergrenzen. Unter diesen Umständen verbinden sie sich also automatisch.
* Das Level ist abgeschlossen, wenn es dem Spieler gelingt, alle magischen Blöcke auf dem Spielfeld automatisch miteinander zu verbinden.

Der Schwierigkeitsgrad bestimmt die Anzahl der magischen Blöcke, die auf dem Spielfeld platziert werden.

## Überblick {#overview}

Wie bei jedem Projekt brauchen wir einen groben Plan für die Umsetzung. Es gibt viele Möglichkeiten, das Spiel zu strukturieren und aufzubauen. Technisch könnten wir das gesamte Spiel im GUI-System umsetzen, wenn wir wollten. Meist ist es jedoch naheliegend, ein Spiel mit Spielobjekten (game objects) und Sprites aufzubauen und die GUI-APIs für die Bildschirmoberfläche und eingeblendete Spielinformationen zu verwenden. Diesen Weg gehen wir hier.

Da wir mit einer recht geringen Anzahl von Dateien rechnen, halten wir die Ordnerstruktur des Projekts sehr einfach:

![Ordnerstruktur](images/magic-link/linker_folders.png)

*main*
: Dieser Ordner enthält die gesamte Spiellogik. Hier liegen alle Skripte, Spielobjektdateien, Sammlungsdateien, GUI-Dateien und so weiter. Du kannst diesen Ordner auch in mehrere Ordner aufteilen oder Unterordner verwenden.

*images*
: In diesem Ordner liegen alle Bild-Assets.

*fonts*
: Hier werden die Schriftarten für das Rendern von Text aufbewahrt.

*input*
: In diesem Ordner liegen die Eingabebindungen (input bindings).

## Das Projekt einrichten {#setting-up-the-project}

Die Datei *game.project* behält größtenteils ihre Standardeinstellungen, aber einige Einstellungen müssen wir festlegen. Zunächst brauchen wir eine Auflösung für das Spiel. Die Auflösung lässt sich später recht leicht ändern. Für ein fertiges Spiel müssen wir außerdem dafür sorgen, dass es unabhängig von der Auflösung und dem Seitenverhältnis des Zielgeräts gut aussieht.

Wir haben uns für eine Auflösung von 640 × 960 Pixeln entschieden, die native Auflösung des iPhone 4. Diese Auflösung passt auch auf viele Monitore, was Spieltests am Computer angenehm macht. Wenn du mit einer anderen Auflösung arbeiten möchtest, musst du nur einige Werte entsprechend anpassen.

![Projekteinstellungen](images/magic-link/linker_project_settings.png)

Außerdem müssen wir die maximale Anzahl gerenderter Sprites erhöhen. Wenn du möchtest, kannst du zum nächsten Abschnitt springen und hierher zurückkehren, sobald dich die Konsole darauf hinweist, dass du die Sprite-Grenze erreicht hast.

![Aufteilung und Größenverhältnisse des Spielfelds](images/magic-link/linker_layout.png)

Wir können die maximal benötigte Anzahl an Sprites berechnen:

* Das Spielfeld enthält 7 × 9 Blöcke. An den Rändern braucht es etwas Abstand und oben Platz für einige GUI-Elemente. Die Blöcke sind deshalb etwa 90 × 90 Pixel groß. Kleinere Blöcke wären zu winzig, um auf dem kleinen Bildschirm eines Telefons mit ihnen zu interagieren.
* Jeder Block besteht aus einem Sprite. Wir verwenden Animationen mit einem einzelnen Bild, um die Farbe des Blocks festzulegen.
* Einige Blöcke sind magische Blöcke, und für jeden davon verwenden wir 4 Sprites für Spezialeffekte.
* Die Verbindungsgrafiken benötigen ein Sprite pro Element. Im ungünstigsten Fall sind das 61 zusätzliche Sprites, wenn der Spieler es irgendwie schafft, das gesamte Spielfeld zu verbinden (abzüglich 2 magischer Blöcke, die sich nicht durch Ziehen verbinden lassen).

Nehmen wir also an, dass wir höchstens 30 magische Blöcke haben. Das Spielfeld besteht aus 63 Blöcken (Sprites). Bei den 30 magischen Blöcken kommen jeweils 4 Sprites für Spezialeffekte hinzu. Das sind 120 zusätzliche Sprites. Zusammen mit den Verbindungsgrafiken (in diesem Fall höchstens 33) müssen wir also in jedem Frame mindestens 120 + 33 = 153 Sprites zeichnen. Die nächste Zweierpotenz ist 256.

Es reicht jedoch nicht aus, das Maximum auf 256 zu setzen. Jedes Mal, wenn wir das Spielfeld leeren und zurücksetzen, löschen wir alle aktuellen Spielobjekte und erzeugen neue. Die Sprite-Anzahl muss alle Objekte berücksichtigen, die während des Frames existieren. Dazu gehören auch gelöschte Objekte, da sie erst am Ende des Frames entfernt werden. Es genügt daher, die maximale Anzahl an Sprites auf 512 zu setzen.

![Maximale Sprite-Anzahl](images/magic-link/linker_sprite_max_count.png)

## Die Grafik-Assets hinzufügen {#adding-the-graphics-assets}

Alle für das Spiel benötigten Assets wurden im Voraus vorbereitet. Wir fügen sie als Bilder mit 512 × 512 Pixeln hinzu und lassen die Engine sie auf die Zielgröße verkleinern.

::: sidenote
Wenn du *hidpi* in den Projekteinstellungen aktivierst, erhält der Backbuffer eine hohe Auflösung. Große Bilder, die verkleinert gezeichnet werden, erscheinen auf Retina-Bildschirmen dadurch sehr scharf.
:::

![Bilder hinzufügen](images/magic-link/linker_add_images.png)

Neben den Blöcken sind ein „connector“-Bild und Effekt-Sprites enthalten. Außerdem gibt es zwei Hintergrundbilder: eines als Hintergrund für das Spielfeld und eines für das Hauptmenü. Füge alle Bilder zum Ordner *images* hinzu und erstelle dann eine Atlasdatei namens *sprites.atlas*. Öffne die Atlasdatei und füge alle Bilder hinzu.

![Bilder zum Atlas hinzufügen](images/magic-link/linker_add_to_atlas.png)

Es gibt außerdem einige GUI-Bilder, mit denen GUI-Elemente wie Schaltflächen und Popups erstellt werden. Diese fügen wir einem separaten Atlas namens *gui.atlas* hinzu.

## Das Spielfeld erzeugen {#generating-the-board}

Im ersten Schritt erstellen wir die Spielfeldlogik. Das Spielfeld liegt in einer eigenen Sammlung (collection), die alles enthält, was während des Spiels auf dem Bildschirm zu sehen ist. Fürs Erste benötigen wir nur die Komponente (component) „blockfactory“ vom Typ Fabrik (factory) und das Skript. Später ergänzen wir eine Fabrik für Verbindungen, eine GUI-Komponente für das Hauptmenü und schließlich die Lademechanik, um das Spiel vom Hauptmenü aus zu starten, sowie eine Möglichkeit, zum Menü zurückzukehren.

1. Erstelle *`board.collection`* im Ordner *`main`*. Gib der Sammlung den Namen „board“, damit wir sie später adressieren können. Wenn du die Sprite-Komponente für den Hintergrund hinzufügst, setze ihre Z-Position unbedingt auf -1. Andernfalls wird sie nicht hinter all den Blöcken gezeichnet, die wir später erzeugen.
2. Setze *Main Collection* (unter *Bootstrap*) in *game.project* vorübergehend auf `/main/board.collection`, damit wir leicht testen können.

![Sammlung für das Spielfeld](images/magic-link/linker_board_collection.png)

![Spielfeldsammlung als Startsammlung](images/magic-link/linker_bootstrap_board.png)

Die Skriptdatei *board.script* enthält die gesamte Logik für das Spielfeld selbst und die Blöcke darauf. Erstelle zunächst die Funktion zum Aufbau des Spielfelds und rufe sie (vorübergehend) aus `init()` auf. Wir fügen außerdem zwei Funktionen hinzu, die wir jetzt noch nicht verwenden, die später aber nützlich sind:

`filter()`
: Mit dieser Funktion können wir Listen von Elementen (Blöcken) filtern.

`build_blocklist()`
: Erstellt eine flache Liste aller Blöcke auf dem Spielfeld, die sich dadurch filtern lässt.

Nach dem Aufbau des Spielfelds verwenden wir zwei verschiedene Datenbestände mit allen Blöcken, `self.blocks` und `self.board`:

```lua
-- board.script
go.property("timer", 0)     -- Use to time events
local blocksize = 80        -- Distance between block centers
local edge = 40             -- Left and right edge.
local bottom_edge = 50      -- Bottom edge.
local boardwidth = 7        -- Number of columns
local boardheight = 9       -- Number of rows
local centeroff = vmath.vector3(8, -8, 0) -- Center offset for connector gfx since there's shadow below in the block img
local dropamount = 3        -- The number of blocks dropped on a "drop"
local colors = { hash("orange"), hash("pink"), hash("blue"), hash("yellow"), hash("green") }

--
-- filter(function, table)
-- e.g: filter(is_even, {1,2,3,4}) -> {2,4}
--
local function filter(func, tbl)
    local new = {}
    for i, v in pairs(tbl) do
        if func(v) then
            new[i] = v
        end
    end
    return new
end

--
-- Build a list of blocks in 1 dimension for easy filtering
--
local function build_blocklist(self)
    self.blocks = {}
    for x, l in pairs(self.board) do
        for y, b in pairs(self.board[x]) do
            table.insert(self.blocks, { id = b.id, color = b.color, x = b.x, y = b.y })
        end
    end
end

--
-- INIT
--
function init(self)
    self.board = {}             -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.
    self.chain = {}             -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3          -- Number of magic blocks on the board
    self.drops = 1              -- Number of drops you have available
    self.magic_blocks = {}      -- Magic blocks that are lined up
    self.dragging = false       -- Drag touch input
    msg.post(".", "acquire_input_focus")
    msg.post("#", "start_level")
end

local function build_board(self)
    math.randomseed(os.time())
    local pos = vmath.vector3()
    local c
    local x = 0
    local y = 0
    for x = 0,boardwidth-1 do
        pos.x = edge + blocksize / 2 + blocksize * x
        self.board[x] = {}
        for y = 0,boardheight-1 do
            pos.y = bottom_edge + blocksize / 2 + blocksize * y
            -- Calc z
            pos.z = x * -0.1 + y * 0.01 -- <1>
            c = colors[math.random(#colors)]    -- Pick a random color
            local id = factory.create("#blockfactory", pos, null, { color = c })
            self.board[x][y] = { id = id, color = c,  x = x, y = y }
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        build_board(self)
    end
end
```
1. Da sich die Blockgrafiken überlappen, müssen wir sie in der richtigen Reihenfolge zeichnen. Dazu setzen wir die Z-Koordinate jedes Blocks. Der Wert bleibt deutlich über -1, wo sich das Hintergrund-Sprite befindet.

Die Spielfeldlogik erzeugt „`block`“-Spielobjekte über die Fabrikkomponente „`blockfactory`“. Damit das funktioniert, müssen wir das Spielobjekt für den Block erstellen. Der Block besitzt ein Skript und ein Sprite. Wir setzen die Standardanimation des Sprites auf einen beliebigen farbigen Block in *`sprites.atlas`* und ergänzen dann *`block.script`* um Code, damit der Block beim Erzeugen die richtige Farbe annimmt:

![Spielobjekt für einen Block](images/magic-link/linker_block.png)

```lua
-- block.script
go.property("color", hash("none"))

function init(self)
    go.set_scale_xy(0.18)     -- render scaled down without changing Z

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end
```

Setze *Prototype* der Fabrikkomponente „blockfactory“ auf die neue Spielobjektdatei *block.go*.

![Fabrik für Blöcke](images/magic-link/linker_blockfactory.png)

Jetzt solltest du das Spiel starten können und ein Spielfeld sehen, das mit zufällig gefärbten Blöcken gefüllt ist:

![Erste Bildschirmaufnahme](images/magic-link/linker_first_screenshot.png)

## Interaktionen {#interactions}

Jetzt haben wir ein Spielfeld und sollten die Interaktion mit dem Spieler hinzufügen. Zunächst definieren wir die Eingabebindungen in *game.input_binding* im Ordner *input*. Stelle sicher, dass die Einstellungen in *game.project* deine Eingabebindungsdatei verwenden.

![Eingabebindungen](images/magic-link/linker_input_bindings.png)

Wir benötigen nur eine Bindung und weisen `MOUSE_BUTTON_LEFT` dem Aktionsnamen „touch“ zu. Dieses Spiel verwendet keine Mehrfacheingabe per Berührung. Praktischerweise übersetzt Defold Berührungseingaben mit einem Finger in Klicks mit der linken Maustaste.

Das Spielfeld übernimmt die Verarbeitung der Eingaben, deshalb müssen wir den entsprechenden Code in *board.script* ergänzen:

```lua
-- board.script
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.value == 1 then
        -- What block was touched or dragged over?
        local x = math.floor((action.x - edge) / blocksize)
        local y = math.floor((action.y - bottom_edge) / blocksize)

        if x < 0 or x >= boardwidth or y < 0 or y >= boardheight or self.board[x][y] == nil then
            -- outside board.
            return
        end

        if action.pressed then
            -- Player started touch
            msg.post(self.board[x][y].id, "make_orange")

            self.dragging = true
        elseif self.dragging then
            -- then drag
            msg.post(self.board[x][y].id, "make_green")
        end
    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false
    end
end
```

Die Nachrichten `make_orange` und `make_green` dienen nur vorübergehend als sichtbare Rückmeldung, dass der Code funktioniert. Wir müssen *block.script* um Code ergänzen, der diese Nachrichten verarbeitet:

```lua
-- block.script
function on_message(self, message_id, message, sender)
    if message_id == hash("make_orange") then
        sprite.play_flipbook("#sprite", hash("orange"))
    elseif message_id == hash("make_green") then
        sprite.play_flipbook("#sprite", hash("green"))
    end
end
```

Jetzt erhalten die Blöcke zuerst eine `make_orange`-Nachricht und danach `make_green`-Nachrichten, solange du den Bildschirm berührst (oder die Maustaste gedrückt hältst). Daher flackern die Blöcke wahrscheinlich nur kurz orange auf (wenn überhaupt), bevor sie grün werden. Aber wir wissen nun, welchen Block der Spieler berührt! Wenn du die Verarbeitung der Eingabe genauer verfolgen möchtest, füge `print()`- oder `pprint()`-Aufrufe in den Code ein.

## Verbindungen markieren {#mark-links}

Jetzt brauchen wir Assets für die Markierung, die anzeigt, wenn der Spieler Blöcke miteinander verbindet. Die Idee ist, einfach eine Grafik über jeden Block zu legen, um seine Verbindung anzuzeigen.

Wir müssen ein Spielobjekt namens „connector“ erstellen, das das Sprite-Bild für die Verbindungen enthält, sowie eine Fabrikkomponente namens „connector factory“ im Spielobjekt „board“:

![Spielobjekt für eine Verbindung](images/magic-link/linker_connector.png)

![Fabrik für Verbindungen](images/magic-link/linker_connector_factory.png)

Das Skript für dieses Spielobjekt ist minimal. Es muss nur die Grafik passend zum restlichen Spiel skalieren und die Z-Reihenfolge richtig einstellen.

```lua
-- connector.script
function init(self)
    go.set_scale_xy(0.18)           -- Scale in 2D without changing Z.
    go.set(".", "position.z", 1)    -- Put on top.
end
```

Die Funktion `same_color_neighbors()` gibt eine Liste von Blöcken zurück, die an einen bestimmten Block (an der Position x, y) angrenzen und dieselbe Farbe haben. Sie verwendet die Funktion `filter()`, die auf die vollständige flache Liste der Blöcke in `self.blocks` angewendet wird.

```lua
-- board.script
--
-- Returns a list of neighbor blocks of the same color as the
-- block on x, y
--
local function same_color_neighbors(self, x, y)
    local f = function (v)
        return (v.id ~= self.board[x][y].id) and
               (v.x == x or v.x == x - 1 or v.x == x + 1) and
               (v.y == y or v.y == y - 1 or v.y == y + 1) and
               (v.color == self.board[x][y].color)
    end
    return filter(f, self.blocks)
end
```

Die Hilfsfunktion `in_blocklist()` prüft, ob ein Block in einer Liste von Blöcken vorhanden ist:

```lua
-- board.script
--
-- Does the block exist in the list of blocks?
--
local function in_blocklist(blocks, block)
    for i, b in pairs(blocks) do
        if b.id == block then
            return true
        end
    end
    return false
end
```

Wir verwenden diese Funktionen bei Berührungs- und Zieheingaben in `on_input()`, um die berührten Blöcke zu einer Verbindungskette zusammenzustellen. Dabei prüfen wir bereits auf magische Blöcke und ignorieren sie, obwohl es noch keine gibt:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    -- If trying to manipulate magic blocks, ignore.
    if self.board[x][y].color == hash("magic") then
        return
    end

    if action.pressed then
        -- List of neighbors of the same color as touched block
        self.neighbors = same_color_neighbors(self, x, y)
        self.chain = {}
        table.insert(self.chain, self.board[x][y])

        -- Mark block.
        p = go.get_position(self.board[x][y].id)
        local id = factory.create("#connectorfactory", p + centeroff)
        table.insert(self.connectors, id)

        self.dragging = true
    elseif self.dragging then
        -- then drag
        if in_blocklist(self.neighbors, self.board[x][y].id) and not in_blocklist(self.chain, self.board[x][y].id) then
            -- dragging over a same-colored neighbor
            table.insert(self.chain, self.board[x][y])
            self.neighbors = same_color_neighbors(self, x, y)

            -- Mark block.
            p = go.get_position(self.board[x][y].id)
            local id = factory.create("#connectorfactory", p + centeroff)
            table.insert(self.connectors, id)
        end
    end
```

Zum Schluss entfernen wir beim Beenden der Berührung alle sichtbaren Verbindungsmarkierungen.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
end
```

![Verbindungen im Spiel](images/magic-link/linker_connector_screen.png)

## Verbundene Blöcke entfernen {#remove-linked-blocks}

Jetzt haben wir die Logik zum Verbinden gleichfarbiger Blöcke, und die verbundenen Blöcke zu entfernen ist einfach. Wir setzen die Position auf dem Spielfeld auf `hash("removing")` statt einfach auf `nil`, weil wir später bei der Logik für magische Blöcke sicherstellen müssen, dass diese nur an die Stellen gerade entfernter Blöcke gleiten. Wenn wir die Position auf dem Spielfeld hier auf `nil` setzen, können wir gerade entfernte Blöcke nicht von solchen unterscheiden, die schon zuvor entfernt wurden.

```lua
-- board.script
-- Remove the currently selected block-chain
--
local function remove_chain(self)
    -- Delete all chained blocks
    for i, c in ipairs(self.chain) do
        self.board[c.x][c.y] = hash("removing")
        go.delete(c.id)
    end
    self.chain = {}
end
```

Außerdem brauchen wir eine Funktion, die Positionen auf dem Spielfeld tatsächlich entfernt (auf `nil` setzt), wenn sie zuvor auf `hash("removing")` gesetzt wurden:

```lua
-- board.script
--
-- Set removed blocks to nil
--
local function nilremoved(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] == hash("removing") then
                self.board[x][y] = nil
            end
        end
    end
end
```

Wir erstellen auch eine Funktion, die die übrigen Blöcke nach unten gleiten lässt, wenn Blöcke darunter entfernt (auf `nil` gesetzt) werden. Wir durchlaufen das Spielfeld spaltenweise von links nach rechts und jede Spalte von unten nach oben. Wenn wir auf eine leere (`nil`) Position stoßen, lassen wir alle Blöcke darüber nach unten gleiten.

```lua
-- board.script
--
-- Apply shift-down logic to all blocks.
--
local function slide_board(self)
    -- Slide all remaining blocks down into blank spots.
    -- Going column by column makes this easy.
    local dy = 0
    local pos = vmath.vector3()
    for x = 0,boardwidth - 1 do
        dy = 0
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil then
                if dy > 0 then
                    -- Move down dy steps
                    self.board[x][y - dy] = self.board[x][y]
                    self.board[x][y] = nil
                    -- Calc new position
                    self.board[x][y - dy].y = self.board[x][y - dy].y - dy
                    go.animate(self.board[x][y-dy].id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * (y - dy), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y-dy].id, "position.z", x * -0.1 + (y-dy) * 0.01)
                end
            else
                dy = dy + 1
            end
        end
    end
    -- blocklist needs updating
    build_blocklist(self)
end
```

![Blöcke nach unten gleiten lassen](images/magic-link/linker_blocks_slide.png)

Jetzt können wir diese Funktionen einfach in `on_input()` aufrufen, wenn die Berührung beendet wurde und sich Blöcke in `self.chain` befinden.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and slide the remaining blocks down.
            remove_chain(self)
            nilremoved(self)
            slide_board(self)
        end

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

## Logik für magische Blöcke {#magic-block-logic}

Jetzt ist es Zeit, die magischen Blöcke hinzuzufügen. Zuerst ermöglichen wir es, einen Block in einen magischen Block umzuwandeln. So können wir das gefüllte Spielfeld in einem separaten Durchlauf bearbeiten und die gewünschten Blöcke in magische verwandeln. Um die magischen Blöcke etwas interessanter zu gestalten, erstellen wir zunächst einen animierten magischen Effekt als Spielobjekt *`magic_fx.go`*, das wir vom magischen Block aus erzeugen können.

![Magic_fx.go](images/magic-link/linker_magic_fx.png)

Dieses Spielobjekt enthält zwei Sprites. Eines stellt die Farbe „magic“ dar (ein Sprite mit dem Bild *`magic-sphere_layer2.png`*), das andere einen Lichteffekt namens „light“ (ein Sprite mit dem Bild *`magic-sphere_layer3.png`*). Das Objekt beginnt beim Erzeugen abhängig vom Wert der Eigenschaft `direction` zu rotieren. Außerdem reagiert es auf zwei Nachrichten: `lights_on` und `lights_off`, die das Sprite für den Lichteffekt steuern.

Erstelle ein neues Skript und füge es als Skriptkomponente zu *`magic_fx.go`* hinzu:

```lua
-- magic_fx.script
go.property("direction", hash("left"))

function init(self)
    msg.post("#", "lights_off")
    if self.direction == hash("left") then
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, 360,  go.EASING_LINEAR, 3 + math.random())
    else
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, -360,  go.EASING_LINEAR, 2 + math.random())
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("lights_on") then
        msg.post("#light", "enable")
    elseif message_id == hash("lights_off") then
        msg.post("#light", "disable")
    end
end
```

Der magische Block erzeugt nun bei der Nachricht `make_magic` zwei `magic_fx`-Spielobjekte. Sie drehen sich in entgegengesetzte Richtungen und erzeugen dadurch ein schönes Farbenspiel im Inneren der Blöcke. Außerdem fügen wir *`block.go`* ein weiteres Sprite mit dem Bild *`magic-sphere_layer4.png`* hinzu. Dieses Bild erhält einen höheren Z-Wert als der erzeugte Effekt und zeichnet die Hülle oder Abdeckung („cover“) der magischen Kugel.

![Sprite für die Abdeckung](images/magic-link/linker_cover.png)

Beachte, dass wir dem Spielobjekt des Blocks eine *Factory*-Komponente hinzufügen und ihr unser Spielobjekt *`magic_fx.go`* als *Prototype* zuweisen müssen. Das Blockskript muss außerdem auf die Nachrichten `lights_on` und `lights_off` reagieren und sie an die erzeugten Objekte weiterleiten. Beachte auch, dass die erzeugten Objekte gelöscht werden müssen, wenn der Block gelöscht wird. Dafür sorgt die Funktion `final()` des Blocks. All das geschieht in *`block.script`*.

```lua
-- block.script
function init(self)
    go.set_scale_xy(0.18) -- render scaled down without changing Z

    self.fx1 = nil
    self.fx2 = nil

    msg.post("#cover", "disable")

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end

function final(self)
    if self.fx1 ~= nil then
        go.delete(self.fx1)
    end

    if self.fx2 ~= nil then
        go.delete(self.fx2)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("make_magic") then
        self.color = hash("magic")
        msg.post("#cover", "enable")
        msg.post("#sprite", "enable")
        sprite.play_flipbook("#sprite", hash("magic-sphere_layer1"))

        self.fx1 = factory.create("#fxfactory", p, nil, { direction = hash("left") })
        self.fx2 = factory.create("#fxfactory", p, nil, { direction = hash("right") })

        go.set_parent(self.fx1, go.get_id())
        go.set_parent(self.fx2, go.get_id())

        go.set(self.fx1, "position.z", 0.01)
        go.set(self.fx1, "scale.xy", 1)
        go.set(self.fx2, "position.z", 0.02)
        go.set(self.fx2, "scale.xy", 1)
    elseif message_id == hash("lights_on") or message_id == hash("lights_off") then
        msg.post(self.fx1, message_id)
        msg.post(self.fx2, message_id)
    end
end
```

Jetzt können wir magische Blöcke erzeugen und sie auch aufleuchten lassen. Mit diesem Effekt zeigen wir an, dass ein magischer Block neben einem anderen magischen Block liegt.

![Magischer Block ohne und mit Licht](images/magic-link/linker_magic_blocks.png)

Den Code, der das Spielfeld mit Blöcken füllt, müssen wir nun so ändern, dass auch einige magische Blöcke darauf erscheinen:

```lua
-- board.script
local function build_board(self)

    ...

    -- Distribute magic blocks.
    local rand_x = 0
    local rand_y
    for y = 0, boardheight - 1, boardheight / self.num_magic do
        local set = false
        while not set do
            rand_y = math.random(math.floor(y), math.min(boardheight - 1, math.floor(y + boardheight / self.num_magic)))
            rand_x = math.random(0, boardwidth - 1)
            if self.board[rand_x][rand_y].color ~= hash("magic") then
                msg.post(self.board[rand_x][rand_y].id, "make_magic")
                self.board[rand_x][rand_y].color = hash("magic")
                set = true
            end
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end
```

Die wichtigste Mechanik der magischen Blöcke ist ihre Fähigkeit, seitwärts zu gleiten, wenn neben ihnen ein anderer Block verschwindet. Alle Einzelheiten dieser Mechanik setzen wir in der Funktion `slide_magic_blocks()` in *board.script* um. Der Algorithmus ist einfach:

1. Erstelle für jede Zeile des Spielfelds eine Liste `M` der magischen Blöcke.
2. Durchlaufe jeden magischen Block in der Liste `M` so lange, bis die Liste nicht mehr schrumpft. Für jeden Durchlauf gilt:
    1. Wenn sich unter dem magischen Block eine mit `hash("removing")` markierte Blockposition befindet, entferne ihn einfach aus der Liste `M`.
    2. Wenn sich neben dem magischen Block eine mit `hash("removing")` markierte Lücke befindet, lasse ihn dorthin gleiten, setze seine alte Position auf `hash("removing")` und entferne ihn dann aus der Liste `M`.

```lua
-- board.script
-- Apply the shifting logic to magic blocks. Only slide to positions
-- marked for removal with hash("removing")
--
local function slide_magic_blocks(self)
    -- Slide all magic blocks to the side that should slide first.
    -- This works best going row by row!
    local row_m
    for y = 0,boardheight - 1 do
        row_m = {}
        -- Build list of magic blocks on this row.
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil and self.board[x][y] ~= hash("removing") and self.board[x][y].color == hash("magic") then
                table.insert(row_m, self.board[x][y])
            end
        end

        local mc = #row_m + 1
        -- Go through list, slide and remove if possible. Reiterate until the list does not shrink.
        while #row_m < mc do
            mc = #row_m
            for i, m in pairs(row_m) do
                local x = m.x
                if y > 0 and self.board[x][y-1] == hash("removing") then
                    -- Hole below, do nothing.
                    row_m[i] = nil
                elseif x > 0 and self.board[x-1][y] == hash("removing") then
                    -- Hole to the left! Slide magic block there
                    self.board[x-1][y] = self.board[x][y]
                    self.board[x-1][y].x = x - 1
                    go.animate(self.board[x][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x - 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y].id, "position.z", (x - 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                elseif x < boardwidth - 1 and self.board[x + 1][y] == hash("removing") then
                    -- Hole to the right. Slide magic block there
                    self.board[x+1][y] = self.board[x][y]
                    self.board[x+1][y].x = x + 1
                    go.animate(self.board[x+1][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x + 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x+1][y].id, "position.z", (x + 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                end
            end
        end
    end
end
```

Wir können die Mechanik ausprobieren, indem wir in `on_input()` einen Aufruf der Funktion ergänzen:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Jetzt wird klar, warum wir beim Entfernen von Positionen die Zwischenmarkierung `hash("removing")` verwendet haben. Ohne sie würden magische Blöcke in jede freie Position neben ihnen hin- und hergleiten. Das wäre vielleicht eine interessante Mechanik, aber nicht die für dieses kleine Spiel vorgesehene.

Nun brauchen wir Logik, die erkennt, ob magische Blöcke verbunden sind (links, rechts, über- oder untereinander liegen). Außerdem müssen wir wissen, ob alle magischen Blöcke auf dem Spielfeld miteinander verbunden sind. Der verwendete Algorithmus ist recht geradlinig:

1. Erstelle eine Liste `M` aller magischen Blöcke auf dem Spielfeld.
2. Für jeden Block in der Liste `M`:
    1. Wenn für den Block keine `region` gesetzt ist, weise ihm die Regionsnummer `R` zu (anfangs `1`).
    2. Markiere alle noch nicht markierten Nachbarn des Blocks mit derselben Regionsnummer `R` und gehe dann zu deren Nachbarn, den Nachbarn dieser Nachbarn und so weiter über.
    3. Erhöhe die Regionsnummer `R` um `1`.

![Regionen markieren](images/magic-link/linker_regions.png)

Hier ist die Implementierung des Algorithmus:

```lua
-- board.script
--
-- Build list of all current magic blocks.
--
local function magic_blocks(self)
    local magic = {}
    for x = 0,boardwidth - 1 do
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil and self.board[x][y].color == hash("magic") then
                table.insert(magic, self.board[x][y])
            end
        end
    end
    return magic
end

--
-- Filter out adjacent magic blocks
--
local function adjacent_magic_blocks(blocks, block)
    return filter(function (e)
        return (block.x == e.x and math.abs(block.y - e.y) == 1) or
            (block.y == e.y and math.abs(block.x - e.x) == 1)
    end, blocks)
end

--
-- Spread region to neighbors
--
local function mark_neighbors(blocks, block, region)
    local neighbors = adjacent_magic_blocks(blocks, block)
    for i, m in pairs(neighbors) do
        if m.region == nil then
            m.region = region
            mark_neighbors(blocks, m, region)
        end
    end
end

--
-- Mark all magic block regions
--
local function mark_magic_regions(self)
    local m_blocks = magic_blocks(self)
    -- 1. Clear all region marks and count neighbors
    for i, m in pairs(m_blocks) do
        m.region = nil
        local n = 0
        for _ in pairs(adjacent_magic_blocks(m_blocks, m)) do n = n + 1 end
        m.neighbors = n
    end

    -- 2. Assign regions and spread them
    local region = 1
    for i, m in pairs(m_blocks) do
        if m.region == nil then
            m.region = region
            mark_neighbors(m_blocks, m, region)
            region = region + 1
        end
    end
    return m_blocks
end
```

Wir erstellen außerdem Funktionen, mit denen wir die Anzahl der Regionen unter den magischen Blöcken zählen können. Ist die Anzahl der Regionen 1, wissen wir, dass alle magischen Blöcke miteinander verbunden sind. Außerdem fügen wir eine Funktion hinzu, die das Licht in allen magischen Blöcken ausschaltet, und eine weitere, die die Lichteffekte in den magischen Blöcken einschaltet, die magische Nachbarblöcke haben:

```lua
-- board.script
--
-- Count the number of connected regions among the magic blocks.
--
local function count_magic_regions(blocks)
    local maxr = 0
    for i, m in pairs(blocks) do
        if m.region > maxr then
            maxr = m.region
        end
    end
    return maxr
end

--
-- Shut off lights on all listed magic blocks
--
local function shutdown_lined_up_magic(self)
    for i, m in ipairs(self.lined_up_magic) do
        msg.post(m.id, "lights_off")
    end
end

--
-- Set highlight for all magic blocks
--
local function highlight_magic(blocks)
    for i, m in pairs(blocks) do
        if m.neighbors > 0 then
            msg.post(m.id, "lights_on")
        else
            msg.post(m.id, "lights_off")
        end
    end
end
```

Jetzt können wir diese Teile der Logik in den Gesamtablauf einfügen. Da das Spielfeld zufällig erzeugt wird, besteht zunächst eine geringe Wahrscheinlichkeit, dass es bereits im Gewinnzustand beginnt. In diesem Fall verwerfen wir das Spielfeld einfach und bauen es erneut auf:

```lua
-- board.script
--
-- Clear the board
--
local function clear_board(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil then
                go.delete(self.board[x][y].id)
                self.board[x][y] = nil
            end
        end
    end
end

local function build_board(self)

    ...

    -- Build 1d list that we can easily filter.
    build_blocklist(self)

    local magic_blocks = mark_magic_regions(self)
    if count_magic_regions(magic_blocks) == 1 then
        -- "Win" from start. Make new board.
        clear_board(self)
        build_board(self)
    end
    highlight_magic(magic_blocks)
end
```

Die restliche Logik kommt in `on_input()`. Es gibt noch keinen Code, der die Nachricht `level_completed` verarbeitet, aber das genügt fürs Erste:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and refill board.
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)

            local magic_blocks = mark_magic_regions(self)
            -- Highlight adjacent magic blocks.
            if count_magic_regions(magic_blocks) == 1 then
                -- Win!
                msg.post("#", "level_completed")
            end
            highlight_magic(magic_blocks)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Jetzt lässt sich das Spiel spielen und der Gewinnzustand erreichen, auch wenn noch nichts passiert, sobald du alle magischen Blöcke miteinander verbindest.

![Erster Sieg](images/magic-link/linker_first_win.png)

## Abwürfe {#drops}

Die Idee hinter dem „Abwurf“ (drop) ist, eine einfache Mechanik für den Spielfortschritt hinzuzufügen. Der Spieler kann durch Drücken der Schaltfläche *DROP* eine begrenzte Anzahl von Abwürfen auslösen. Dabei fallen einfach einige neue zufällige Blöcke auf das Spielfeld. Der Spieler beginnt mit einem Abwurf und erhält jedes Mal, wenn er ein Level abschließt, einen weiteren. Der Code für die Abwurfmechanik passt in zwei Funktionen: Eine gibt eine Liste möglicher Stellen zurück, an denen abgeworfene Blöcke landen können, und die andere führt den eigentlichen Abwurf samt Animation aus.

```lua
-- board.script
--
-- Find spots for a drop.
--
local function dropspots(self)
    local spots = {}
    for x = 0, boardwidth - 1 do
        for y = 0, boardheight - 1 do
            if self.board[x][y] == nil then
                table.insert(spots, { x = x, y = y })
                break
            end
        end
    end
    -- If more than dropamount, randomly remove a slot until dropamount
    for c = 1, #spots - dropamount do
        table.remove(spots, math.random(#spots))
    end
    return spots
end

--
-- Perform the drop
--
local function drop(self, spots)
    for i, s in pairs(spots) do
        local pos = vmath.vector3()
        pos.x = edge + blocksize / 2 + blocksize * s.x
        pos.y = 1000
        c = colors[math.random(#colors)]    -- Pick a random color
        local id = factory.create("#blockfactory", pos, null, { color = c })
        go.animate(id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * s.y, go.EASING_OUTBOUNCE, 0.5)
        -- Calc new z
        go.set(id, "position.z", s.x * -0.1 + s.y * 0.01)

        self.board[s.x][s.y] = { id = id, color = c,  x = s.x, y = s.y }
    end

    -- Rebuild blocklist
    build_blocklist(self)
end
```

Wir können Abwürfe testen, indem wir den folgenden Code beispielsweise in `on_reload()` ausführen oder ihn an eine vorübergehende Eingabeaktion binden:

```lua
s = dropspots(self)
if #s > 0 then
    -- Do the drop
    drop(self, s)
end
```

![Abwurf](images/magic-link/linker_drop.png)

## Das Hauptmenü {#the-main-menu}

Jetzt ist es Zeit, alles zusammenzufügen. Zuerst erstellen wir einen Startbildschirm und trennen ihn vom Spielfeld. Schritt 1 besteht darin, eine *main_menu.gui* zu erstellen und sie mit einer *Start*-Schaltfläche (einem Textknoten und einem texturierten Box-Knoten), einem Textknoten für den Titel und einigen dekorativen Blöcken (texturierten Box-Knoten) einzurichten. Das Skript *main_menu.gui_script*, das wir an die GUI anhängen, animiert die dekorativen Blöcke in `init()`. Es enthält außerdem eine Funktion `on_input()`, die eine `start_game`-Nachricht an ein Hauptskript sendet. Dieses Skript erstellen wir gleich.

![GUI des Hauptmenüs](images/magic-link/linker_main_menu.png)

```lua
-- main_menu.gui_script
function init(self)
    msg.post(".", "acquire_input_focus")

    local bs = { "brick1", "brick2", "brick3", "brick4", "brick5", "brick6" }
    for i, b in ipairs(bs) do
        local n = gui.get_node(b)
        local rt = (math.random() * 3) + 1
        local a = math.random(-45, 45)
        gui.set_color(n, vmath.vector4(1, 1, 1, 0))

        gui.animate(n, "position.y", -100 - math.random(0, 50), gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "color.w", 1, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "rotation.z", a, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
    end

    gui.animate(gui.get_node("start"), "color.x", 1, gui.EASING_INOUTSINE, 1, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local start = gui.get_node("start")

        if gui.pick_node(start, action.x, action.y) then
            msg.post("/main#script", "start_game")
        end
    end
end
```

Da das Starten des Spiels bald das Skript des Hauptmenüs übernimmt, entferne den vorübergehenden Aufruf zum Aufbau des Spielfelds aus `init()` in *board.script*:

```lua
-- board.script
--
-- INIT
--
function init(self)
    self.board = {}                -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.

    self.chain = {}                -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3            -- Number of magic blocks on the board

    self.drops = 1                -- Number of drops you have available

    self.magic_blocks = {}        -- Magic blocks that are lined up

    self.dragging = false        -- Drag touch input
end
```

Das Hauptskript verwaltet den gesamten Spielzustand und startet das Spiel auf Anforderung. Wir möchten hier erreichen, dass *main.collection* nur die Mindestmenge an Assets enthält, die wir beim Start anzeigen müssen. Dazu enthält *main.collection* ein Spielobjekt namens „main“ mit der GUI des Hauptmenüs, einer Skriptkomponente und vor allem einer *Collection Proxy*-Komponente.

Mit dem Sammlungs-Proxy (collection proxy) können wir Sammlungen im laufenden Spiel dynamisch laden und entladen. Er handelt stellvertretend für eine angegebene Sammlungsdatei. Indem wir Nachrichten an den Proxy senden, laden, initialisieren, aktivieren, deaktivieren und entladen wir die dynamische Sammlung. Eine vollständige Beschreibung ihrer Verwendung findest du in der [Dokumentation zu Sammlungs-Proxys](/manuals/collection-proxy).

In unserem Fall setzen wir die Eigenschaft *Collection* der Sammlungs-Proxy-Komponente auf *board.collection*, die das „Level“ enthält.

![Hauptsammlung](images/magic-link/linker_main_collection.png)

Öffne nun *game.project* und ändere die Startsammlung (bootstrap collection) *main_collection* auf `/main/main.collectionc`.

![Hauptsammlung als Startsammlung](images/magic-link/linker_bootstrap_main.png)

Ein Spiel zu starten bedeutet jetzt, unserem Sammlungs-Proxy Nachrichten zum Laden, Initialisieren und Aktivieren des Spielfelds zu senden und anschließend das Hauptmenü zu deaktivieren (damit es nicht angezeigt wird). Bei der Rückkehr zum Hauptmenü geschieht das Umgekehrte (vorausgesetzt, der Proxy hat die Sammlung geladen).

```lua
-- main.script
function init(self)
    msg.post("#", "to_main_menu")
    self.state = "MAIN_MENU"
end

function on_message(self, message_id, message, sender)
    if message_id == hash("to_main_menu") then
        if self.state ~= "MAIN_MENU" then
            msg.post("#boardproxy", "unload")
        end
        msg.post("main:/main#menu", "enable") -- <1>
        self.state = "MAIN_MENU"
    elseif message_id == hash("start_game") then
        msg.post("#boardproxy", "load")
        msg.post("#menu", "disable")
    elseif message_id == hash("proxy_loaded") then
        -- Board collection has loaded...
        msg.post(sender, "init")
        msg.post("board:/board#script", "start_level", { difficulty = 1 }) -- <2>
        msg.post(sender, "enable")
        self.state = "GAME_RUNNING"
    end
end
```
1. Beachte, dass wir den Socket „main“ nennen. Stelle deshalb sicher, dass dieser Name auch für *main.collection* gesetzt ist. Wähle den obersten Knoten aus und prüfe, ob die Eigenschaft *Name* auf „main“ gesetzt ist.
2. Ebenso senden wir Nachrichten an die geladene Sammlung über ihren Socket, dessen Name durch die Eigenschaft *Name* der Sammlung festgelegt wird.

## Die GUI im Spiel {#the-in-game-gui}

Bevor wir die letzten Teile der Logik zum Spielfeldskript hinzufügen, sollten wir das Spielfeld um einige GUI-Elemente ergänzen. Zuerst fügen wir oberhalb des Spielfelds eine Schaltfläche *RESTART* und eine Schaltfläche *DROP* hinzu.

![GUI des Spielfelds](images/magic-link/linker_board_gui.png)

Das Skript für die GUI des Spielfelds sendet bei einem Klick Nachrichten an den GUI-Dialog für den Neustart und beim Klicken auf *DROP* zurück an das Spielfeldskript selbst:

```lua
-- board.gui_script
function init(self)
    msg.post("#", "show")
    msg.post("/restart#gui", "hide")
    msg.post("/level_complete#gui", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
    elseif message_id == hash("set_drop_counter") then
        local n = gui.get_node("drop_counter")
        gui.set_text(n, message.drops .. " x")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local restart = gui.get_node("restart")
        local drop = gui.get_node("drop")

        if gui.pick_node(restart, action.x, action.y) then
            -- Show the restart dialog box.
            msg.post("/restart#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(drop, action.x, action.y) then
            msg.post("/board#script", "drop")
        end
    end
end
```

Der Dialog *RESTART* ist einfach. Wir erstellen ihn als *restart.gui* und hängen ein einfaches Skript an, das bei einem Klick auf *NO* nichts tut, bei einem Klick auf *YES* eine `restart_level`-Nachricht an das Spielfeldskript sendet und bei einem Klick auf *Quit to main menu* eine `to_main_menu`-Nachricht an das Hauptskript:

![GUI für den Neustart](images/magic-link/linker_restart_gui.png)

```lua
-- restart.gui_script
function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local yes = gui.get_node("yes")
        local no = gui.get_node("no")
        local quit = gui.get_node("quit")

        if gui.pick_node(no, action.x, action.y) then
            msg.post("#", "hide")
            msg.post("/board#gui", "show")
        elseif gui.pick_node(yes, action.x, action.y) then
            msg.post("board:/board#script", "restart_level")
            msg.post("/board#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(quit, action.x, action.y) then
            msg.post("main:/main#script", "to_main_menu")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Wir erstellen außerdem in *level_complete.gui* einen einfachen GUI-Dialog für den Levelabschluss mit einem einfachen Skript, das eine `next_level`-Nachricht an das Spielfeldskript sendet, wenn der Spieler auf *CONTINUE* klickt:

![Dialog für den Levelabschluss](images/magic-link/linker_level_complete_gui.png)

```lua
-- level_complete.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local continue = gui.get_node("continue")

        if gui.pick_node(continue, action.x, action.y) then
            msg.post("board#script", "next_level")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Ein Dialog stellt das aktuelle Level vor. Sein Skript enthält nur das Ausblenden und Anzeigen des Dialogs. Beim Anzeigen wird der Dialogtext auf eine Nachricht gesetzt, die den aktuellen Schwierigkeitsgrad enthält:

![GUI zur Vorstellung des Levels](images/magic-link/linker_present_level_gui.png)

```lua
-- present_level.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        local n = gui.get_node("message")
        gui.set_text(n, "Level " .. message.level)
        msg.post("#", "enable")
    end
end
```

Wir fügen außerdem einen Dialog hinzu, der erscheint, wenn der Spieler einen Abwurf versucht, dafür aber kein Platz ist.

![GUI bei fehlendem Platz für einen Abwurf](images/magic-link/linker_no_drop_room_gui.png)

```lua
-- no_drop_room.gui_script
function init(self)
    msg.post("#", "hide")
    self.t = 0
end

function update(self, dt)
    if self.t < 0 then
        msg.post("#", "hide")
    else
        self.t = self.t - dt
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        self.t = 1
        msg.post("#", "enable")
    end
end
```

Zum Schluss fügen wir diese GUI-Komponenten zu *board.collection* hinzu und ergänzen den benötigten Code in *board.script*:

![Fertige Spielfeldsammlung](images/magic-link/linker_board_collection_final.png)

In `on_message()` brauchen wir Code für alle Nachrichten, die an das Spielfeld und von ihm gesendet werden.

`start_level`
: Setze die Anzahl der magischen Blöcke entsprechend dem Schwierigkeitsparameter, baue das Spielfeld auf und zeige dann den GUI-Dialog „present_level“ für 2 Sekunden an, bevor das Spiel beginnt (der Dialog entfernt und der Eingabefokus angefordert wird). Beachte, dass wir `go.animate()` als Zeitgeber verwenden, indem wir den Wert von „timer“ animieren, der sonst für nichts verwendet wird.

`restart_level`
: Dies geschieht, wenn der Spieler die GUI-Schaltfläche *RESTART* drückt und den Neustart bestätigt. Leere das Spielfeld, baue es neu auf und setze den Abwurfzähler zurück.

`level_completed`
: Wird gesendet, sobald sich das Spielfeld im Gewinnzustand befindet. Schalte die Eingabe aus, animiere die magischen Blöcke und zeige den GUI-Dialog „level_complete“ an. Der Dialog sendet eine `next_level`-Nachricht zurück, wenn der Spieler darin auf die Schaltfläche *CONTINUE* klickt.

`next_level`
: Wenn diese Nachricht empfangen wird, leere das Spielfeld, erhöhe den Abwurfzähler und sende `start_level` mit dem nächsten Schwierigkeitsgrad.

`drop`
: Prüfe, wo Abwürfe möglich sind. Wenn es keine möglichen Stellen gibt, zeige den GUI-Dialog „no_drop_room“ an. Führe andernfalls den Abwurf aus (wenn der Spieler noch Abwürfe übrig hat), verringere den Abwurfzähler und aktualisiere die Anzeige des Zählers.

```lua
-- board.script
function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        self.num_magic = message.difficulty + 1
        build_board(self)

        msg.post("#gui", "set_drop_counter", { drops = self.drops } )

        msg.post("present_level#gui", "show", { level = message.difficulty } )
        -- Wait some...
        go.animate("#", "timer", go.PLAYBACK_ONCE_FORWARD, 1, go.EASING_LINEAR, 2, 0, function ()
            msg.post("present_level#gui", "hide")
            msg.post(".", "acquire_input_focus")
        end)
    elseif message_id == hash("restart_level") then
        clear_board(self)
        build_board(self)
        self.drops = 1
        msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        msg.post(".", "acquire_input_focus")
    elseif message_id == hash("level_completed") then
        -- turn off input
        msg.post(".", "release_input_focus")

        -- Animate the magic!
        for i, m in ipairs(magic_blocks(self)) do
            go.set_scale_xy(0.17, m.id)
            go.animate(m.id, "scale.xy", go.PLAYBACK_LOOP_PINGPONG, 0.19, go.EASING_INSINE, 0.5, 0)
        end

        -- Show completion screen
        msg.post("level_complete#gui", "show")
    elseif message_id == hash("next_level") then
        clear_board(self)
        self.drops = self.drops + 1
        -- Difficulty level is number of magic blocks - 1
        msg.post("#", "start_level", { difficulty = self.num_magic })
    elseif message_id == hash("drop") then
        s = dropspots(self)
        if #s == 0 then
            -- Can't perform drop
            msg.post("no_drop_room#gui", "show")
        elseif self.drops > 0 then
            -- Do the drop
            drop(self, s)
            self.drops = self.drops - 1
            msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        end
    end
end
```

Geschafft! Das Spiel und dieses Tutorial sind jetzt abgeschlossen! Viel Spaß beim Spielen!

![Fertiges Spiel](images/magic-link/linker_game_finished.png)

## Weiterführende Schritte {#moving-on}

Dieses kleine Spiel hat einige interessante Eigenschaften. Experimentiere ruhig damit. Hier sind einige Übungen, mit denen du dich weiter mit Defold vertraut machen kannst:

* Verdeutliche die Interaktion. Neuen Spielern fällt es möglicherweise schwer zu verstehen, wie das Spiel funktioniert und womit sie interagieren können. Nimm dir etwas Zeit, um das Spiel verständlicher zu machen, ohne Tutorial-Elemente einzubauen.
* Füge Ton hinzu. Das Spiel ist derzeit völlig stumm und würde von einem schönen Soundtrack und Klängen bei Interaktionen profitieren.
* Erkenne das Spielende automatisch.
* Höchstpunktzahl. Füge eine Funktion für eine dauerhaft gespeicherte Höchstpunktzahl hinzu.
* Implementiere das Spiel neu und verwende dabei ausschließlich die GUI-APIs.
* Derzeit kommt bei jedem neuen Level ein magischer Block hinzu. Das lässt sich nicht beliebig lange fortsetzen. Finde eine zufriedenstellende Lösung für dieses Problem.
* Optimiere das Spiel und senke die maximale Sprite-Anzahl, indem du Sprites wiederverwendest, statt sie zu löschen und neu zu erzeugen.
* Implementiere ein von der Auflösung unabhängiges Rendering des Spiels, damit es auf Bildschirmen mit unterschiedlichen Auflösungen und Seitenverhältnissen gleichermaßen gut aussieht.
