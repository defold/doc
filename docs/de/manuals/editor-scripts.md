---
title: Editor-Skripte
brief: Dieses Handbuch erklärt, wie du den Editor mit Lua erweiterst
---

# Editor-Skripte {#editor-scripts}

Du kannst eigene Menüeinträge und Lebenszyklus-Hooks (lifecycle hooks) für den Editor erstellen, indem du Lua-Dateien mit der speziellen Erweiterung `.editor_script` verwendest. Mit diesem System kannst du den Editor anpassen und deinen Arbeitsablauf bei der Entwicklung verbessern.

## Laufzeitumgebung für Editor-Skripte {#editor-script-runtime}

Editor-Skripte (editor scripts) laufen innerhalb des Editors in einer Lua-VM, die von der Java-VM emuliert wird. Alle Skripte teilen sich eine einzige Umgebung und können daher miteinander interagieren. Du kannst Lua-Module mit `require` laden, genau wie in `.script`-Dateien. Im Editor läuft jedoch eine andere Lua-Version, daher solltest du sicherstellen, dass dein gemeinsam verwendeter Code kompatibel ist. Der Editor verwendet Lua in Version 5.2.x, genauer gesagt die Laufzeitumgebung [luaj](https://github.com/luaj/luaj), die derzeit die einzige praktikable Lösung zum Ausführen von Lua auf der JVM ist. Darüber hinaus gelten einige Einschränkungen:
- Es gibt kein `debug`-Paket;
- es gibt kein `os.execute`, aber mit `editor.execute()` stellen wir eine ähnliche Funktion bereit;
- es gibt weder `os.tmpname` noch `io.tmpfile` — derzeit können Editor-Skripte nur auf Dateien innerhalb des Projektverzeichnisses zugreifen;
- derzeit gibt es kein `os.rename`, wir möchten es jedoch hinzufügen;
- es gibt weder `os.exit` noch `os.setlocale`.
- Einige länger laufende Funktionen dürfen nicht in Kontexten verwendet werden, in denen der Editor eine sofortige Antwort vom Skript benötigt. Weitere Informationen findest du unter [Ausführungsmodi](#execution-modes).

Alle in Editor-Skripten definierten Editor-Erweiterungen werden geladen, wenn du ein Projekt öffnest. Wenn du Bibliotheken abrufst, werden die Erweiterungen neu geladen, da Bibliotheken, von denen dein Projekt abhängt, neue Editor-Skripte enthalten können. Bei diesem Neuladen werden Änderungen an deinen eigenen Editor-Skripten nicht übernommen, da du sie möglicherweise gerade bearbeitest. Um auch diese neu zu laden, solltest du den Befehl **Project → Reload Editor Scripts** ausführen.

## Aufbau einer `.editor_script`-Datei {#anatomy-of-editor_script}

Jedes Editor-Skript sollte ein Modul zurückgeben, zum Beispiel so:
```lua
local M = {}

function M.get_commands()
  -- TODO - define editor commands
end

function M.get_language_servers()
  -- TODO - define language servers
end

function M.get_prefs_schema()
  -- TODO - define preferences
end

return M
```
Der Editor sammelt dann alle im Projekt und in den Bibliotheken definierten Editor-Skripte, lädt sie in eine einzige Lua-VM und ruft sie bei Bedarf auf (mehr dazu in den Abschnitten [Befehle](#commands) und [Lebenszyklus-Hooks](#lifecycle-hooks)).

## Editor-API

Über das Paket `editor`, das die folgende API definiert, kannst du mit dem Editor interagieren:
- `editor.platform` — eine Zeichenfolge, entweder `"x86_64-win32"` für Windows, `"x86_64-macos"` für macOS oder `"x86_64-linux"` für Linux.
- `editor.version` — eine Zeichenfolge mit dem Versionsnamen von Defold, z. B. `"1.4.8"`
- `editor.engine_sha1` — eine Zeichenfolge mit dem SHA1-Wert der Defold-Engine
- `editor.editor_sha1` — eine Zeichenfolge mit dem SHA1-Wert des Defold-Editors
- `editor.get(node_id, property)` — einen Wert eines Knotens innerhalb des Editors abrufen. Knoten im Editor sind verschiedene Entitäten, etwa eine Skriptdatei oder eine Datei für eine Sammlung (collection), ein Spielobjekt (game object) innerhalb einer Sammlung, eine als Ressource geladene JSON-Datei usw. `node_id` ist ein userdata-Wert, den der Editor an das Editor-Skript übergibt. Alternativ kannst du statt der Knoten-ID einen Ressourcenpfad übergeben, zum Beispiel `"/main/game.script"`. `property` ist eine Zeichenfolge. Derzeit werden folgende Eigenschaften unterstützt:
  - `"path"` — Dateipfad relativ zum Projektordner für *Ressourcen* — Entitäten, die als Dateien oder Verzeichnisse existieren. Beispiel für einen Rückgabewert: `"/main/game.script"`
  - `"children"` — Liste der Ressourcenpfade untergeordneter Elemente für Verzeichnisressourcen
  - `"parent"` — übergeordneter Editorknoten eines Knotens in Outline, der einen übergeordneten Knoten hat
  - `"text"` — Textinhalt einer als Text bearbeitbaren Ressource (etwa Skriptdateien oder JSON). Beispiel für einen Rückgabewert: `"function init(self)\nend"`. Beachte, dass dies nicht dem Lesen einer Datei mit `io.open()` entspricht: Du kannst eine Datei bearbeiten, ohne sie zu speichern, und diese Änderungen sind nur über den Zugriff auf die Eigenschaft `"text"` verfügbar.
  - für Atlanten: `images` (Liste der Editorknoten für Bilder im Atlas) und `animations` (Liste der Animationsknoten)
  - für Atlasanimationen: `images` (wie `images` im Atlas)
  - für eine Kachelkarte (tile map): `layers` (Liste der Editorknoten für Ebenen in der Kachelkarte)
  - für Kachelkartenebenen: `tiles` (ein unbegrenztes 2D-Raster aus Kacheln), weitere Informationen findest du unter `tilemap.tiles.*`
  - für Partikeleffekte: `emitters` (Liste der Editorknoten für Emitter) und `modifiers` (Liste der Editorknoten für Modifikatoren)
  - für Emitter von Partikeleffekten: `modifiers` (Liste der Editorknoten für Modifikatoren)
  - für Kollisionsobjekte: `shapes` (Liste der Editorknoten für Kollisionsformen)
  - für GUI-Dateien: Knotenlisten wie `layers`, `fonts`, `materials`, `textures`, `particlefxs`, `nodes` und `layouts`
  - einige Eigenschaften, die in der Ansicht Properties angezeigt werden, wenn du etwas in der Ansicht Outline ausgewählt hast. Folgende Typen von Outline-Eigenschaften werden unterstützt:
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    Beachte, dass einige dieser Eigenschaften schreibgeschützt sein können und andere je nach Kontext möglicherweise nicht verfügbar sind. Deshalb solltest du vor dem Lesen `editor.can_get` und vor dem Setzen durch den Editor `editor.can_set` verwenden. Bewege den Mauszeiger über den Eigenschaftsnamen in der Ansicht Properties, um einen Tooltip mit Informationen dazu anzuzeigen, wie diese Eigenschaft in Editor-Skripten heißt. Du kannst Ressourceneigenschaften auf `nil` setzen, indem du den Wert `""` übergibst.
- `editor.properties(node_id)` — eine sortierte, kontextabhängige Liste der Eigenschaftsnamen zurückgeben, die von einem Knoten gelesen werden können, zum Beispiel `pprint(editor.properties("/game.project"))`. Verwende die Funktionen `editor.can_*`, um zu prüfen, ob eine aufgelistete Eigenschaft auch geändert oder zurückgesetzt werden kann, ob sich ihr Elemente hinzufügen lassen oder ob deren Reihenfolge geändert werden kann.
- `editor.can_get(node_id, property)` — prüfen, ob du diese Eigenschaft abrufen kannst, sodass `editor.get()` keinen Fehler auslöst.
- `editor.can_set(node_id, property)` — prüfen, ob ein Transaktionsschritt mit `editor.tx.set()` für diese Eigenschaft keinen Fehler auslöst.
- `editor.create_directory(resource_path)` — ein Verzeichnis erstellen, falls es nicht existiert, einschließlich aller fehlenden übergeordneten Verzeichnisse.
- `editor.create_resources(resources)` — 1 oder mehr Ressourcen erstellen, entweder aus Vorlagen oder mit eigenen Inhalten
- `editor.delete_directory(resource_path)` — ein Verzeichnis löschen, falls es existiert, einschließlich aller vorhandenen Unterverzeichnisse und Dateien.
- `editor.execute(cmd, [...args], [options])` — einen Shell-Befehl ausführen und optional seine Ausgabe erfassen.
- `editor.save()` — alle ungespeicherten Änderungen auf dem Datenträger speichern.
- `editor.transact(txs)` — den Zustand des Editors im Arbeitsspeicher mit 1 oder mehr Transaktionsschritten ändern, die mit den Funktionen `editor.tx.*` erstellt wurden.
- `editor.ui.*` — verschiedene Funktionen für die Benutzeroberfläche, siehe [UI-Handbuch](/manuals/editor-scripts-ui).
- `editor.prefs.*` — Funktionen für den Zugriff auf Editoreinstellungen, siehe [Editoreinstellungen](#preferences).

Die vollständige Editor-API-Referenz findest du [hier](/ref/stable/editor/).

## Befehle {#commands}

Wenn ein Editor-Skriptmodul `get_commands()` definiert, wird diese Funktion beim Neuladen der Erweiterungen aufgerufen. Die zurückgegebenen Befehle können abhängig von ihren `locations` in den Menüs der Menüleiste und in den Kontextmenüs von Assets, Outline, Scene und Code erscheinen. Beispiel:

```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
      locations = {"Edit", "Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        local path = editor.get(opts.selection, "path")
        return ends_with(path, ".lua") or ends_with(path, ".script")
      end,
      run = function(opts)
        local text = editor.get(opts.selection, "text")
        editor.transact({
          editor.tx.set(opts.selection, "text", strip_comments(text))
        })
      end
    },
    {
      label = "Minify JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        editor.execute("./scripts/minify-json.sh", path:sub(2))
      end
    }
  }
end

return M
```
Der Editor erwartet, dass `get_commands()` ein Array von Tabellen zurückgibt, die jeweils einen eigenen Befehl beschreiben. Eine Befehlsbeschreibung besteht aus:

- `label` (erforderlich) — Text eines Menüeintrags, der angezeigt wird
- `locations` (erforderlich) — ein Array, das angibt, wo dieser Befehl verfügbar sein soll. Unterstützte Werte sind `"Edit"`, `"View"`, `"Project"`, `"Debug"` und `"Help"` für die entsprechenden Menüs der Menüleiste; `"Bundle"` für das Untermenü **Project → Bundle**; sowie `"Assets"`, `"Outline"`, `"Scene"` und `"Code"` für die entsprechenden Kontextmenüs.
- `query` — eine Möglichkeit für den Befehl, relevante Informationen beim Editor abzufragen und festzulegen, mit welchen Daten er arbeitet. Zu jedem Schlüssel in der Tabelle `query` gibt es einen entsprechenden Schlüssel in der Tabelle `opts`, die die Callbacks `active` und `run` als Argument erhalten. Unterstützte Schlüssel:
  - `selection` bedeutet, dass dieser Befehl gültig ist, wenn etwas ausgewählt ist, und dass er auf dieser Auswahl arbeitet.
    - `type` ist der Typ der ausgewählten Knoten, für die der Befehl relevant ist. Derzeit sind diese Typen zulässig:
      - `"resource"` — in Assets und Outline ist eine Ressource das ausgewählte Element, zu dem eine Datei gehört. In der Menüleiste (Edit oder View) ist eine Ressource die aktuell geöffnete Datei;
      - `"outline"` — etwas, das in Outline angezeigt werden kann. In Outline ist es ein ausgewähltes Element, in der Menüleiste die aktuell geöffnete Datei;
      - `"scene"` — etwas, das in Scene gerendert werden kann.
    - `cardinality` legt fest, wie viele Elemente ausgewählt sein sollen. Bei `"one"` ist die an den Befehls-Callback übergebene Auswahl eine einzelne Knoten-ID. Bei `"many"` ist sie ein Array mit einer oder mehreren Knoten-IDs.
  - `active_view` bedeutet, dass dieser Befehl gültig ist, wenn die aktive Editoransicht dem angeforderten Typ entspricht. Die aktive Ansicht wird dem Befehls-Callback als `opts.active_view` übergeben.
    - `type` ist der Typ der aktiven Ansicht, für den der Befehl relevant ist, entweder `"code"`, `"scene"`, `"html"` oder `"form"`.
    - Die aktive Ansicht unterstützt die Eigenschaften `"type"`, `"resource"` und `"dirty"`. Verwende `editor.get(view, "resource")`, um die in der Ansicht angezeigte Ressource abzurufen, und `editor.get(view, "dirty")`, um zu prüfen, ob sie ungespeicherte Änderungen enthält.
  - `argument` — Befehlsargument. Derzeit erhalten nur Befehle am Ort `"Bundle"` ein Argument. Es ist `true`, wenn der Bundle-Befehl ausdrücklich ausgewählt wird, und `false`, wenn das Bundle erneut erstellt wird.
- `id` - eine Zeichenfolge als Bezeichner des Befehls, die z. B. zum Speichern des zuletzt verwendeten Bundle-Befehls in `prefs` dient
- `active` - ein Callback, der prüft, ob der Befehl aktiv ist, und einen booleschen Wert zurückgeben soll. Wenn `locations` die Werte `"Assets"`, `"Scene"` oder `"Outline"` enthält, wird `active` beim Anzeigen des Kontextmenüs aufgerufen. Wenn locations die Werte `"Edit"` oder `"View"` enthält, wird active bei jeder Interaktion aufgerufen, etwa beim Tippen auf der Tastatur oder beim Klicken mit der Maus. Stelle daher sicher, dass `active` relativ schnell ist.
- `run` - ein Callback, der ausgeführt wird, wenn du den Menüeintrag auswählst.

### Den Zustand des Editors im Arbeitsspeicher mit Befehlen ändern {#use-commands-to-change-the-in-memory-editor-state}

Im Handler `run` kannst du den Zustand des Editors im Arbeitsspeicher abfragen und ändern. Für Abfragen verwendest du die Funktion `editor.get()`, mit der du den Editor nach dem aktuellen Zustand von Dateien und der Auswahl fragen kannst (wenn du `query = {selection = ...}` verwendest). Du kannst die Eigenschaft `"text"` von Ressourcen abrufen, die als Text bearbeitbar sind, sowie einige Eigenschaften aus der Ansicht Properties. Bewege den Mauszeiger über den Eigenschaftsnamen, um einen Tooltip mit Informationen dazu anzuzeigen, wie diese Eigenschaft in Editor-Skripten heißt. Den Editorzustand änderst du mit `editor.transact()`. Dabei fasst du 1 oder mehr Änderungen in einem einzigen Schritt zusammen, der rückgängig gemacht werden kann. Wenn du zum Beispiel die Transformation eines Spielobjekts zurücksetzen möchtest, könntest du einen Befehl wie diesen schreiben:
```lua
{
  label = "Reset transform",
  locations = {"Outline"},
  query = {selection = {type = "outline", cardinality = "one"}},
  active = function(opts)
    local node = opts.selection
    return editor.can_set(node, "position") 
       and editor.can_set(node, "rotation") 
       and editor.can_set(node, "scale")
  end,
  run = function(opts)
    local node = opts.selection
    editor.transact({
      editor.tx.set(node, "position", {0, 0, 0}),
      editor.tx.set(node, "rotation", {0, 0, 0}),
      editor.tx.set(node, "scale", {1, 1, 1})
    })
  end
}
```

### Befehle mit der aktiven Editoransicht verwenden {#use-commands-with-the-active-editor-view}

Befehle in Menüs wie `"View"` können die aktuell aktive Editoransicht abfragen. Das ist nützlich, wenn ein Befehl mit der Datei oder Szene arbeiten soll, die du gerade ansiehst:

```lua
editor.command({
  label = "Print Active View",
  locations = {"View"},
  query = {active_view = {type = "code"}},
  run = function(opts)
    local view = opts.active_view
    local resource = editor.get(view, "resource")
    print(editor.get(view, "type"))
    print(editor.get(resource, "path"))
    print(editor.get(view, "dirty"))
  end
})
```

#### Atlanten bearbeiten {#editing-atlases}

Du kannst nicht nur Eigenschaften eines Atlas lesen und schreiben, sondern auch seine Bilder und Animationen lesen und ändern. Ein Atlas definiert die Knotenlisteneigenschaften `images` und `animations`, und Animationen definieren die Knotenlisteneigenschaft `images`. Mit diesen Eigenschaften kannst du die Transaktionsschritte `editor.tx.add`, `editor.tx.remove` und `editor.tx.clear` verwenden.

Um beispielsweise ein Bild zu einem Atlas hinzuzufügen, führe den folgenden Code im Handler `run` des Befehls aus:
```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```
Um die Menge aller Bilder in einem Atlas zu ermitteln, führe den folgenden Code aus:
```lua
local all_images = {} ---@type table<string, true>
-- first, collect all "bare" images
local image_nodes = editor.get("/main.atlas", "images")
for i = 1, #image_nodes do
    all_images[editor.get(image_nodes[i], "image")] = true
end
-- second, collect all images used in animations
local animation_nodes = editor.get("/main.atlas", "animations")
for i = 1, #animation_nodes do
    local animation_image_nodes = editor.get(animation_nodes[i], "images")
    for j = 1, #animation_image_nodes do
        all_images[editor.get(animation_image_nodes[j], "image")] = true
    end
end
pprint(all_images)
-- {
--     ["/assets/hero.png"] = true,
--     ["/assets/enemy.png"] = true,
-- }}
```
So ersetzt du alle Animationen in einem Atlas:
```lua
editor.transact({
    editor.tx.clear("/main.atlas", "animations"),
    editor.tx.add("/main.atlas", "animations", {
        id = "hero_run",
        images = {
            {image = "/assets/hero_run_1.png"},
            {image = "/assets/hero_run_2.png"},
            {image = "/assets/hero_run_3.png"},
            {image = "/assets/hero_run_4.png"}
        }
    })
})
```

#### Kachelquellen bearbeiten {#editing-tilesources}

Zusätzlich zu den Outline-Eigenschaften definiert eine Kachelquelle (tile source) die folgenden Eigenschaften:
- `animations` - eine Liste der Animationsknoten der Kachelquelle
- `collision_groups` - eine Liste der Kollisionsgruppenknoten der Kachelquelle
- `tile_collision_groups` - eine Tabelle mit den Zuordnungen von Kollisionsgruppen zu Kacheln in der Kachelquelle

So kannst du zum Beispiel eine Kachelquelle einrichten:
```lua
local tilesource = "/game/world.tilesource"
editor.transact({
    editor.tx.add(tilesource, "animations", {id = "idle", start_tile = 1, end_tile = 1}),
    editor.tx.add(tilesource, "animations", {id = "walk", start_tile = 2, end_tile = 6, fps = 10}),
    editor.tx.add(tilesource, "collision_groups", {id = "player"}),
    editor.tx.add(tilesource, "collision_groups", {id = "obstacle"}),
    editor.tx.set(tilesource, "tile_collision_groups", {
        [1] = "player",
        [7] = "obstacle",
        [8] = "obstacle"
    })
})
```

#### Kachelkarten bearbeiten {#editing-tilemaps}

Kachelkarten definieren die Eigenschaft `layers`, eine Knotenliste der Kachelkartenebenen. Jede Ebene definiert außerdem die Eigenschaft `tiles`, die ein unbegrenztes 2D-Raster mit den Kacheln dieser Ebene enthält. Dies unterscheidet sich von der Engine: Das Kachelraster ist unbegrenzt und Kacheln können überall hinzugefügt werden, auch an negativen Koordinaten. Zum Bearbeiten von Kacheln definiert die Editor-Skript-API das Modul `tilemap.tiles` mit den folgenden Funktionen:
- `tilemap.tiles.new()`, um eine neue Datenstruktur zu erstellen, die ein unbegrenztes 2D-Kachelraster enthält (im Editor ist die Kachelkarte im Gegensatz zur Engine unbegrenzt und Koordinaten dürfen negativ sein)
- `tilemap.tiles.get_tile(tiles, x, y)`, um den Kachelindex an einer bestimmten Koordinate abzurufen
- `tilemap.tiles.get_info(tiles, x, y)`, um vollständige Kachelinformationen an einer bestimmten Koordinate abzurufen (die Datenstruktur entspricht der Funktion `tilemap.get_tile_info` der Engine)
- `tilemap.tiles.iterator(tiles)`, um einen Iterator über alle Kacheln in der Kachelkarte zu erstellen
- `tilemap.tiles.clear(tiles)`, um alle Kacheln aus der Kachelkarte zu entfernen
- `tilemap.tiles.set(tiles, x, y, tile_or_info)`, um eine Kachel an einer bestimmten Koordinate zu setzen
- `tilemap.tiles.remove(tiles, x, y)`, um eine Kachel an einer bestimmten Koordinate zu entfernen

So kannst du zum Beispiel den Inhalt der gesamten Kachelkarte ausgeben:
```lua
local layers = editor.get("/level.tilemap", "layers")
for i = 1, #layers do
    local layer = layers[i]
    local id = editor.get(layer, "id")
    local tiles = editor.get(layer, "tiles")
    print("layer " .. id .. ": {")
    for x, y, tile in tilemap.tiles.iterator(tiles) do
        print("  [" .. x .. ", " .. y .. "] = " .. tile)
    end
    print("}")
end
```

Dieses Beispiel zeigt, wie du einer Kachelkarte eine Ebene mit Kacheln hinzufügst:
```lua
local tiles = tilemap.tiles.new()
tilemap.tiles.set(tiles, 1, 1, 2)
editor.transact({
    editor.tx.add("/level.tilemap", "layers", {
        id = "new_layer",
        tiles = tiles
    })
})
```

#### Partikeleffekte bearbeiten {#editing-particlefx}

Du kannst Partikeleffekte mit den Eigenschaften `modifiers` und `emitters` bearbeiten. So fügst du zum Beispiel einen kreisförmigen Emitter mit einem Beschleunigungsmodifikator hinzu:
```lua
editor.transact({
    editor.tx.add("/fire.particlefx", "emitters", {
        type = "emitter-type-circle",
        modifiers = {
          {type = "modifier-type-acceleration"}
        }
    })
})
```
Viele Eigenschaften von Partikeleffekten sind Kurven oder Kurven mit Streuung (d. h. eine Kurve + ein Wert für zufällige Abweichungen). Kurven werden als Tabelle mit einer nicht leeren Liste von `points` dargestellt, wobei jeder Punkt eine Tabelle mit den folgenden Eigenschaften ist:
- `x` - die x-Koordinate des Punktes; sie sollte bei 0 beginnen und bei 1 enden
- `y` - der Wert des Punktes
- `tx` (0 bis 1) und `ty` (-1 bis 1) - Tangenten des Punktes. Bei einem Winkel von 80 Grad sollte `tx` zum Beispiel `math.cos(math.rad(80))` und `ty` entsprechend `math.sin(math.rad(80))` sein.
Kurven mit Streuung haben zusätzlich die numerische Eigenschaft `spread`. 

So könnte beispielsweise das Setzen einer Alphakurve über die Partikellebensdauer für einen bereits vorhandenen Emitter aussehen:
```lua
local emitter = editor.get("/fire.particlefx", "emitters")[1]
editor.transact({
    editor.tx.set(emitter, "particle_key_alpha", { points = {
        {x = 0,   y = 0, tx = 0.1, ty = 1}, -- start at 0, go up quickly
        {x = 0.2, y = 1, tx = 1,   ty = 0}, -- reach 1 at 20% of a lifetime
        {x = 1,   y = 0, tx = 1,   ty = 0}  -- slowly go down to 0
    }})
})
```
Natürlich kannst du den Schlüssel `particle_key_alpha` auch in einer Tabelle verwenden, wenn du einen Emitter erstellst. Außerdem kannst du stattdessen eine einzelne Zahl verwenden, um eine „statische“ Kurve darzustellen.

#### Kollisionsobjekte bearbeiten {#editing-collision-objects}

Zusätzlich zu den standardmäßigen Outline-Eigenschaften definieren Kollisionsobjekte die Knotenlisteneigenschaft `shapes`. So fügst du neue Kollisionsformen hinzu:
```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- or "shape-type-sphere", "shape-type-capsule"
    })
})
```
Die Eigenschaft `type` einer Form ist beim Erstellen erforderlich und kann nach dem Hinzufügen der Form nicht mehr geändert werden. Es gibt 3 Formtypen:
- `shape-type-box` - Quaderform mit der Eigenschaft `dimensions`
- `shape-type-sphere` - Kugelform mit der Eigenschaft `diameter`
- `shape-type-capsule` - Kapselform mit den Eigenschaften `diameter` und `height`

#### GUI-Dateien bearbeiten {#editing-gui-files}

Zusätzlich zu den Outline-Eigenschaften definieren GUI-Dateien mehrere Eigenschaften für Knotenlisten:

- `layers` — Liste der Editorknoten für Ebenen (Reihenfolge änderbar)
- `fonts` — Liste der Editorknoten für Schriftarten
- `materials` — Liste der Editorknoten für Materialien
- `textures` — Liste der Editorknoten für Texturen
- `particlefxs` — Liste der Editorknoten für Partikeleffekte
- `nodes` — Liste der Editorknoten für GUI-Knoten
- `layouts` — Liste der Editorknoten für GUI-Layouts

Du kannst GUI-Ebenen über die Editoreigenschaft `layers` bearbeiten, zum Beispiel:
```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```
Außerdem kannst du die Reihenfolge der Ebenen ändern:
```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```
Ebenso bearbeitest du Schriftarten, Materialien, Texturen und Partikeleffekte mit den Eigenschaften `fonts`, `materials`, `textures` und `particlefxs`:
```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.particlefx"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```
Diese Eigenschaften unterstützen keine Änderung der Reihenfolge.

Schließlich kannst du GUI-Knoten mit der Listeneigenschaft `nodes` bearbeiten, zum Beispiel:
```lua
editor.transact({
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-box",
        position = {20, 20, 20}
    }),
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-template",
        template = "/button.gui"
    }),
})
```
Die integrierten Knotentypen sind:
- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

Wenn du die Spine-Erweiterung verwendest, kannst du auch den Knotentyp `gui-node-type-spine` verwenden.

Wenn die GUI-Datei Layouts definiert, kannst du die Werte aus den Layouts mit der Syntax `layout:property` abrufen und setzen, zum Beispiel:
```lua
local node = editor.get("/main.gui", "nodes")[1]

-- GET:
local position = editor.get(node, "position")
pprint(position) -- {20, 20, 20}
local landscape_position = editor.get(node, "Landscape:position")
pprint(landscape_position) -- {20, 20, 20}

-- SET:
editor.transact({
    editor.tx.set(node, "Landscape:position", {30, 30, 30})
})
pprint(editor.get(node, "Landscape:position")) -- {30, 30, 30}
```

Gesetzte Layout-Eigenschaften kannst du mit `editor.tx.reset` auf ihre Standardwerte zurücksetzen:
```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```
Knotenbäume von Vorlagen können gelesen, aber nicht bearbeitet werden — du kannst nur die Knoteneigenschaften im Knotenbaum der Vorlage setzen:
```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (overrides a value in the template)
```

#### Spielobjekte bearbeiten {#editing-game-objects}

Mit Editor-Skripten kannst du die Komponenten (components) einer Spielobjektdatei bearbeiten. Es gibt 2 Arten von Komponenten: referenzierte und eingebettete. Referenzierte Komponenten verwenden den Typ `component-reference` und dienen als Referenzen auf andere Ressourcen. Dabei lassen sich nur die in Skripten definierten Spielobjekteigenschaften überschreiben. Eingebettete Komponenten verwenden Typen wie `sprite`, `label` usw. und erlauben es, alle im Komponententyp definierten Eigenschaften zu bearbeiten sowie untergeordnete Komponenten wie Formen von Kollisionsobjekten hinzuzufügen. Mit folgendem Code kannst du zum Beispiel ein Spielobjekt einrichten:
```lua
editor.transact({
    editor.tx.add("/npc.go", "components", {
        type = "sprite",
        id = "view"
    }),
    editor.tx.add("/npc.go", "components", {
        type = "collisionobject",
        id = "collision",
        shapes = {
            {
                type = "shape-type-box",
                dimensions = {32, 32, 32}
            }
        }
    }),
    editor.tx.add("/npc.go", "components", {
        type = "component-reference",
        path = "/npc.script",
        id = "controller",
        __hp = 100 -- set a go property defined in the script
    })
})
```

#### Sammlungen bearbeiten {#editing-collections}
Mit Editor-Skripten kannst du Sammlungen bearbeiten. Du kannst Spielobjekte (eingebettet oder referenziert) und Sammlungen (referenziert) hinzufügen. Zum Beispiel:
```lua
local coll = "/char.collection"
editor.transact({
    editor.tx.add(coll, "children", {
        -- embbedded game object
        type = "go",
        id = "root",
        children = {
            {
                -- referenced game object
                type = "go-reference",
                path = "/char-view.go",
                id = "view"
            },
            {
                -- referenced collection
                type = "collection-reference",
                path = "/body-attachments.collection",
                id = "attachments"
            }
        },
        -- embedded gos can also have components
        components = {
            {
                type = "collisionobject",
                id = "collision",
                shapes = {
                    {type = "shape-type-box", dimensions = {2.5, 2.5, 2.5}}
                }
            },
            {
                type = "component-reference",
                id = "controller",
                path = "/char.script",
                __hp = 100 -- set a go property defined in the script
            }
        }
    })
})
```

Wie im Editor können referenzierte Sammlungen nur auf der obersten Ebene der bearbeiteten Sammlung hinzugefügt werden. Spielobjekte können nur eingebetteten oder referenzierten Spielobjekten hinzugefügt werden, nicht aber referenzierten Sammlungen oder Spielobjekten innerhalb dieser referenzierten Sammlungen.

### Shell-Befehle verwenden {#use-shell-commands}

Im Handler `run` kannst du in Dateien schreiben (mit dem Modul `io`) und Shell-Befehle ausführen (mit dem Befehl `editor.execute()`). Beim Ausführen eines Shell-Befehls kannst du dessen Ausgabe als Zeichenfolge erfassen und anschließend im Code verwenden. Wenn du zum Beispiel einen Befehl zur Formatierung von JSON erstellen möchtest, der das global installierte [`jq`](https://jqlang.github.io/jq/) über die Shell aufruft, kannst du folgenden Befehl schreiben:
```lua
{
  label = "Format JSON",
  locations = {"Assets"},
  query = {selection = {type = "resource", cardinality = "one"}},
  action = function(opts)
    local path = editor.get(opts.selection, "path")
    return path:match(".json$") ~= nil
  end,
  run = function(opts)
    local text = editor.get(opts.selection, "text")
    local new_text = editor.execute("jq", "-n", "--argjson", "data", text, "$data", {
      reload_resources = false, -- don't reload resources since jq does not touch disk
      out = "capture" -- return text output instead of nothing
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```
Da dieser Befehl das Shell-Programm nur lesend aufruft (und dem Editor dies mit `reload_resources = false` mitteilt), hat er den Vorteil, dass sich diese Aktion rückgängig machen lässt.

::: sidenote
Zur Verteilung deines Editor-Skripts als Bibliothek möchtest du möglicherweise das Binärprogramm für die Editorplattformen innerhalb der Abhängigkeit mitliefern. Unter [Editor-Skripte in Bibliotheken](#editor-scripts-in-libraries) findest du weitere Informationen dazu.
:::

## Lebenszyklus-Hooks {#lifecycle-hooks}

Eine Editor-Skriptdatei wird besonders behandelt: `hooks.editor_script` im Stammverzeichnis deines Projekts, im selben Verzeichnis wie *game.project*. Ausschließlich dieses Editor-Skript empfängt Lebenszyklusereignisse vom Editor. Beispiel für eine solche Datei:
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
Wir haben uns entschieden, Lebenszyklus-Hooks auf eine einzige Editor-Skriptdatei zu beschränken, weil die Reihenfolge der Build-Hooks wichtiger ist als die Frage, wie leicht sich ein weiterer Build-Schritt hinzufügen lässt. Befehle sind voneinander unabhängig, daher ist ihre Reihenfolge im Menü nicht wirklich wichtig; letztlich wird ein bestimmter, ausgewählter Befehl ausgeführt. Wenn Build-Hooks in verschiedenen Editor-Skripten definiert werden könnten, entstünde ein Problem: In welcher Reihenfolge werden die Hooks ausgeführt? Wahrscheinlich möchtest du Prüfsummen für Inhalte erst nach deren Komprimierung erstellen ... Eine einzelne Datei, die die Reihenfolge der Build-Schritte festlegt, indem sie die Funktion jedes Schritts ausdrücklich aufruft, löst dieses Problem.

Verfügbare Lebenszyklus-Hooks, die `/hooks.editor_script` definieren kann:
- `on_build_started(opts)` — wird ausgeführt, wenn mit den Optionen Project Build oder Debug Start ein Build des Spiels erstellt wird, um es lokal oder auf einem entfernten Ziel auszuführen. Deine Änderungen erscheinen im erstellten Spiel. Wenn dieser Hook einen Fehler auslöst, wird der Build abgebrochen. `opts` ist eine Tabelle mit folgenden Schlüsseln:
  - `platform` — eine Zeichenfolge im Format `%arch%-%os%`, die die Zielplattform des Builds beschreibt; derzeit immer derselbe Wert wie in `editor.platform`.
- `on_build_finished(opts)` — wird ausgeführt, wenn der Build abgeschlossen ist, unabhängig davon, ob er erfolgreich war oder fehlgeschlagen ist. `opts` ist eine Tabelle mit folgenden Schlüsseln:
  - `platform` — wie in `on_build_started`
  - `success` — gibt an, ob der Build erfolgreich ist, entweder `true` oder `false`
- `on_bundle_started(opts)` — wird ausgeführt, wenn du ein Bundle erstellst oder mit Build HTML5 eine HTML5-Version eines Spiels erstellst. Wie bei `on_build_started` erscheinen die durch diesen Hook ausgelösten Änderungen im Bundle, und Fehler brechen die Bundle-Erstellung ab. `opts` enthält folgende Schlüssel:
  - `output_directory` — ein Dateipfad zu einem Verzeichnis mit der Bundle-Ausgabe. **Project ▸ Build HTML5** verwendet einen eigenen Artefaktbaum, zum Beispiel `"/path/to/project/build/default_html5/__htmlLaunchDir"`, getrennt von der normalen Build-Ausgabe unter `build/default`.
  - `platform` — die Plattform, für die das Bundle des Spiels erstellt wird. Eine Liste möglicher Plattformwerte findest du im [Bob-Handbuch](/manuals/bob).
  - `variant` — die Bundle-Variante, entweder `"debug"`, `"release"` oder `"headless"`
- `on_bundle_finished(opts)` — wird ausgeführt, wenn die Bundle-Erstellung abgeschlossen ist, unabhängig davon, ob sie erfolgreich war. `opts` ist eine Tabelle mit denselben Daten wie `opts` in `on_bundle_started`, ergänzt um den Schlüssel `success`, der angibt, ob der Build erfolgreich ist.
- `on_target_launched(opts)` — wird ausgeführt, nachdem du ein Spiel gestartet hast und es erfolgreich angelaufen ist. `opts` enthält den Schlüssel `url`, der auf den gestarteten Engine-Dienst verweist, zum Beispiel `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — wird ausgeführt, wenn das gestartete Spiel geschlossen wird, und erhält dieselben opts wie `on_target_launched`

Beachte, dass Lebenszyklus-Hooks derzeit nur im Editor verfügbar sind. Bob führt sie bei der Bundle-Erstellung über die Kommandozeile nicht aus.

## Sprachserver {#language-servers}

Der Editor unterstützt einen Teil des [Language Server Protocol](https://microsoft.github.io/language-server-protocol/): Diagnosemeldungen (statische Codeprüfungen), Vervollständigungen, Informationen beim Bewegen des Mauszeigers über Symbole, Dokumentsymbole im Bereich Structure, das Springen zur Definition, das Suchen von Referenzen, das Umbenennen von Symbolen sowie die Formatierung von Dokumenten und Bereichen. Bewege den Mauszeiger über ein Symbol, um Informationen des Sprachservers zu sehen. Wenn sich der Cursor auf einem Symbol befindet, kannst du es mit <kbd>F2</kbd> umbenennen, mit <kbd>F12</kbd> zu seiner Definition springen oder mit <kbd>Shift+F12</kbd> Referenzen suchen. Diese Aktionen sind auch im Menü <kbd>Edit</kbd> verfügbar. Informationen zum Formatierungsbefehl und zur Einstellung für das Formatieren beim Speichern findest du unter [Code formatieren](/manuals/writing-code/#formatting-code).

Der mitgelieferte Lua-Sprachserver enthält Defold-Typannotationen für die Laufzeit-API und die Editor-Skript-API. In `.editor_script`-Dateien erkennen die Vervollständigung und die Diagnosefunktionen die Funktionen `editor.*` sowie deren Argument- und Rückgabetypen. Siehe [Codevervollständigung](/manuals/writing-code/#code-completion).

Um einen zusätzlichen Sprachserver zu registrieren, definiere die Funktion `get_language_servers` deines Editor-Skripts wie folgt:

```lua
function M.get_language_servers()
  local command = 'build/plugins/my-ext/plugins/bin/' .. editor.platform .. '/lua-lsp'
  if editor.platform == 'x86_64-win32' then
    command = command .. '.exe'
  end
  return {
    {
      languages = {'lua'},
      watched_files = {
        { pattern = '**/.luacheckrc' }
      },
      command = {command, '--stdio'}
    }
  }
end
```
Der Editor startet den Sprachserver mit dem angegebenen `command` und verwendet zur Kommunikation die Standardeingabe und Standardausgabe des Serverprozesses.

Die Tabelle zur Definition des Sprachservers kann Folgendes angeben:
- `languages` (erforderlich) — eine Liste der Sprachen, für die der Server zuständig ist, wie [hier](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers) definiert (Dateierweiterungen funktionieren ebenfalls);
- `command` (erforderlich) - ein Array mit dem Befehl und seinen Argumenten
- `watched_files` - ein Array von Tabellen mit `pattern`-Schlüsseln (ein Glob-Muster), die die Serverbenachrichtigung [über geänderte überwachte Dateien](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) auslösen.

## HTTP-Server

Jede laufende Instanz des Editors betreibt einen HTTP-Server. Du kannst diesen Server mit Editor-Skripten erweitern. Um den HTTP-Server des Editors zu erweitern, musst du die Editor-Skriptfunktion `get_http_server_routes` hinzufügen — sie sollte die zusätzlichen Routen zurückgeben:
```lua
print("My route: " .. http.server.url .. "/my-extension")

function M.get_http_server_routes()
  return {
    http.server.route("/my-extension", "GET", function(request)
      return http.server.response(200, "Hello world!")
    end)
  }
end
```
Nach dem Neuladen der Editor-Skripte siehst du in der Konsole folgende Ausgabe: `My route: http://0.0.0.0:12345/my-extension`. Wenn du diesen Link im Browser öffnest, siehst du deine Nachricht `"Hello world!"`.

Das Eingabeargument `request` ist eine einfache Lua-Tabelle mit Informationen zur Anfrage. Sie enthält Schlüssel wie `path` (URL-Pfadsegment, das mit `/` beginnt), `method` für die Anfragemethode (z. B. `"GET"`), `headers` (eine Tabelle mit Headernamen in Kleinbuchstaben) sowie optional `query` (die Abfragezeichenfolge) und `body` (wenn die Route definiert, wie der Anfrageinhalt zu interpretieren ist). Wenn du zum Beispiel eine Route erstellen möchtest, die JSON als Anfrageinhalt akzeptiert, definierst du sie mit dem Konverterparameter `"json"`:
```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```
Du kannst diesen Endpunkt mit `curl` und `jq` über die Kommandozeile testen:
```sh
curl 'http://0.0.0.0:12345/my-extension/echo-request?q=1' -X POST --data '{"input": "json"}' | jq
{
  "path": "/my-extension/echo-request",
  "method": "POST",
  "query": "q=1",
  "headers": {
    "host": "0.0.0.0:12345",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "user-agent": "curl/8.7.1",
    "content-length": "17"
  },
  "body": {
    "input": "json"
  }
}
```
Der Routenpfad unterstützt Muster, deren Werte aus dem Anfragepfad extrahiert und der Handlerfunktion als Teil der Anfrage übergeben werden können, zum Beispiel:
```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```
Wenn du nun zum Beispiel `http://0.0.0.0:12345/my-extension/setting/project.title` öffnest, siehst du den Titel deines Spiels aus der Datei `/game.project`.

Neben einem Muster für ein einzelnes Pfadsegment kannst du mit der Syntax `{*name}` auch den restlichen URL-Pfad erfassen. Hier ist beispielsweise ein einfacher Dateiserver-Endpunkt, der Dateien aus dem Stammverzeichnis des Projekts bereitstellt:
```lua
http.server.route("/my-extension/files/{*file}", function(request)
  local attrs = editor.external_file_attributes(request.file)
  if attrs.is_file then
    return http.server.external_file_response(request.file)
  else
    return 404
  end
end)
```
Wenn du nun zum Beispiel `http://0.0.0.0:12345/my-extension/files/main/main.collection` im Browser öffnest, wird der Inhalt der Datei `main/main.collection` angezeigt.

## Editor-Skripte in Bibliotheken {#editor-scripts-in-libraries}

Du kannst Bibliotheken mit Befehlen veröffentlichen, damit andere sie verwenden können; der Editor erkennt diese Befehle automatisch. Hooks können dagegen nicht automatisch erkannt werden, da sie in einer Datei im Stammordner eines Projekts definiert werden müssen, während Bibliotheken nur Unterordner bereitstellen. Dadurch hast du mehr Kontrolle über den Build-Vorgang: Du kannst Lebenszyklus-Hooks weiterhin als einfache Funktionen in `.lua`-Dateien erstellen, sodass die Nutzer deiner Bibliothek sie in ihrer `/hooks.editor_script` laden und verwenden können.

Beachte außerdem, dass Abhängigkeiten zwar in der Ansicht Assets angezeigt werden, aber nicht als Dateien existieren (sie sind Einträge in einem ZIP-Archiv). Du kannst den Editor veranlassen, bestimmte Dateien aus den Abhängigkeiten in den Ordner `build/plugins/` zu extrahieren. Dazu musst du in deinem Bibliotheksordner eine Datei `ext.manifest` erstellen und dann den Ordner `plugins/bin/${platform}` im selben Ordner anlegen, in dem sich die Datei `ext.manifest` befindet. Dateien aus diesem Ordner werden automatisch in den Ordner `/build/plugins/${extension-path}/plugins/bin/${platform}` extrahiert, sodass deine Editor-Skripte auf sie verweisen können.

## Editoreinstellungen {#preferences}

Editor-Skripte können Editoreinstellungen definieren und verwenden — dauerhaft auf deinem Computer gespeicherte Daten, die nicht in die Versionsverwaltung übernommen werden. Diese Einstellungen haben drei wesentliche Merkmale:
- typisiert: Jede Einstellung hat eine Schemadefinition mit dem Datentyp und weiteren Metadaten wie dem Standardwert
- mit Gültigkeitsbereich: Einstellungen gelten entweder pro Projekt oder pro Nutzer
- verschachtelt: Jeder Einstellungsschlüssel ist eine durch Punkte getrennte Zeichenfolge. Das erste Pfadsegment identifiziert ein Editor-Skript, die übrigen Segmente identifizieren Gruppen und einzelne Einstellungen darin

Alle Einstellungen müssen durch die Definition ihres Schemas registriert werden:
```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```
Nachdem ein solches Editor-Skript neu geladen wurde, registriert der Editor dieses Schema. Anschließend kann das Editor-Skript die Einstellungen abrufen und setzen, zum Beispiel:
```lua
-- Get a specific preference
editor.prefs.get("my_json_formatter.indent.type")
-- Returns: "spaces"

-- Get an entire preference group
editor.prefs.get("my_json_formatter")
-- Returns:
-- {
--   jq_path = "",
--   indent = {
--     size = 2,
--     type = "spaces"
--   }
-- }

-- Set multiple nested preferences at once
editor.prefs.set("my_json_formatter.indent", {
    type = "tabs",
    size = 1
})
```

## Ausführungsmodi {#execution-modes}

Die Laufzeitumgebung für Editor-Skripte verwendet 2 Ausführungsmodi, die für Editor-Skripte weitgehend transparent sind: **sofortige Ausführung (immediate)** und **länger laufende Ausführung (long-running)**. 

Die **sofortige Ausführung** wird verwendet, wenn der Editor so schnell wie möglich eine Antwort vom Skript benötigt. Beispielsweise werden die `active`-Callbacks von Menübefehlen in diesem Modus ausgeführt, da diese Prüfungen im UI-Thread des Editors als Reaktion auf die Interaktion mit dem Editor stattfinden und die Benutzeroberfläche innerhalb desselben Frames aktualisieren sollen. 

Die **länger laufende Ausführung** wird verwendet, wenn der Editor keine sofortige Antwort vom Skript benötigt. Beispielsweise werden die `run`-Callbacks von Menübefehlen im Modus für **länger laufende Ausführung** ausgeführt, sodass das Skript mehr Zeit für seine Arbeit in Anspruch nehmen kann.

Einige Funktionen, die Editor-Skripte verwenden können, benötigen möglicherweise viel Ausführungszeit. Beispielsweise kann `editor.execute("git", "status", {reload_resources=false, out="capture"})` bei ausreichend großen Projekten bis zu einer Sekunde dauern. Damit der Editor reaktionsfähig bleibt und seine Leistung beibehält, sind potenziell zeitaufwendige Funktionen in Kontexten nicht erlaubt, in denen der Editor eine sofortige Antwort benötigt. Der Versuch, eine solche Funktion in einem Kontext mit sofortiger Ausführung zu verwenden, führt zu einem Fehler: `Cannot use long-running editor function in immediate context`. Um diesen Fehler zu beheben, vermeide solche Funktionen in Kontexten mit sofortiger Ausführung.

Die folgenden Funktionen gelten als länger laufend und können nicht im Modus für sofortige Ausführung verwendet werden:
- `editor.create_directory()`, `editor.create_resources()`, `editor.delete_directory()`, `editor.save()`, `os.remove()` und `file:write()`: Diese Funktionen ändern Dateien auf dem Datenträger. Dadurch synchronisiert der Editor seinen Ressourcenbaum im Arbeitsspeicher mit dem Zustand auf dem Datenträger, was bei großen Projekten Sekunden dauern kann.
- `editor.execute()`: Die Ausführung von Shell-Befehlen kann unvorhersehbar lange dauern.
- `editor.transact()`: Große Transaktionen an Knoten, auf die viele Referenzen verweisen, können Hunderte von Millisekunden dauern, was für eine reaktionsfähige Benutzeroberfläche zu langsam ist.

Die folgenden Kontexte für die Codeausführung verwenden den Modus für sofortige Ausführung:
- `active`-Callbacks von Menübefehlen: Der Editor benötigt innerhalb desselben UI-Frames eine Antwort vom Skript.
- Code auf der obersten Ebene von Editor-Skripten: Wir erwarten, dass das Neuladen von Editor-Skripten keine Seiteneffekte hat.

## Aktionen {#actions}

::: sidenote
Früher interagierte der Editor blockierend mit der Lua-VM. Daher galt die strikte Anforderung, dass Editor-Skripte nicht blockieren dürfen, da einige Interaktionen vom UI-Thread des Editors aus erfolgen müssen. Aus diesem Grund gab es beispielsweise weder `editor.execute()` noch `editor.transact()`. Das Ausführen von Skripten und das Ändern des Editorzustands wurden stattdessen durch die Rückgabe eines Arrays von „Aktionen“ aus Hooks und den Handlern `run` von Befehlen ausgelöst.

Jetzt interagiert der Editor ohne Blockierung mit der Lua-VM, sodass diese Aktionen nicht mehr benötigt werden: Funktionen wie `editor.execute()` sind bequemer, kürzer und leistungsfähiger. Die Aktionen sind jetzt **VERALTET UND ZUR ABLÖSUNG VORGESEHEN**, wir planen jedoch nicht, sie zu entfernen.
:::

Editor-Skripte können aus der Funktion `run` eines Befehls oder aus den Hook-Funktionen von `/hooks.editor_script` ein Array von Aktionen zurückgeben. Der Editor führt diese Aktionen anschließend aus.

Eine Aktion ist eine Tabelle, die beschreibt, was der Editor tun soll. Jede Aktion hat einen Schlüssel `action`. Es gibt 2 Arten von Aktionen: solche, die rückgängig gemacht werden können, und solche, die nicht rückgängig gemacht werden können.

### Aktionen, die rückgängig gemacht werden können {#undoable-actions}

::: sidenote
Verwende vorzugsweise `editor.transact()`.
:::

Eine solche Aktion kann nach ihrer Ausführung rückgängig gemacht werden. Wenn ein Befehl mehrere solche Aktionen zurückgibt, werden sie gemeinsam ausgeführt und gemeinsam rückgängig gemacht. Du solltest nach Möglichkeit Aktionen verwenden, die rückgängig gemacht werden können. Ihr Nachteil ist, dass ihre Möglichkeiten stärker eingeschränkt sind.

Verfügbare Aktionen, die rückgängig gemacht werden können:
- `"set"` — eine Eigenschaft eines Knotens im Editor auf einen Wert setzen. Beispiel:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  Die Aktion `"set"` benötigt diese Schlüssel:
  - `node_id` — ein userdata-Wert mit der Knoten-ID. Alternativ kannst du hier statt der vom Editor erhaltenen Knoten-ID einen Ressourcenpfad verwenden, zum Beispiel `"/main/game.script"`;
  - `property` — die zu setzende Eigenschaft eines Knotens, z. B. `"text"`;
  - `value` — der neue Wert der Eigenschaft. Für die Eigenschaft `"text"` sollte er eine Zeichenfolge sein.

### Aktionen, die nicht rückgängig gemacht werden können {#non-undoable-actions}

::: sidenote
Verwende vorzugsweise `editor.execute()`.
:::

Eine solche Aktion löscht den Verlauf für das Rückgängigmachen. Wenn du sie rückgängig machen möchtest, musst du daher andere Mittel verwenden, etwa die Versionsverwaltung.

Verfügbare Aktionen, die nicht rückgängig gemacht werden können:
- `"shell"` — ein Shell-Skript ausführen. Beispiel:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- trim leading "/"
    }
  }
  ```
  Die Aktion `"shell"` benötigt den Schlüssel `command`, ein Array mit dem Befehl und seinen Argumenten.

### Aktionen und Seiteneffekte kombinieren {#mixing-actions-and-side-effects}

Du kannst Aktionen kombinieren, die rückgängig gemacht werden können, und solche, die es nicht können. Die Aktionen werden nacheinander ausgeführt. Je nach Reihenfolge verlierst du daher die Möglichkeit, Teile dieses Befehls rückgängig zu machen.

Anstatt Aktionen aus Funktionen zurückzugeben, die sie erwarten, kannst du Dateien mit `io.open()` direkt lesen und schreiben. Dies löst ein Neuladen der Ressourcen aus, das den Verlauf für das Rückgängigmachen löscht.
