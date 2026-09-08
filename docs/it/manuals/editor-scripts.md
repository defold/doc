---
title: Script dell'editor
brief: Questo manuale spiega come estendere l'editor usando Lua
---

# Script dell'editor {#editor-scripts}

Puoi creare voci di menu personalizzate e hook del ciclo di vita dell'editor usando file Lua con un'estensione speciale: `.editor_script`. Questo sistema ti consente di personalizzare l'editor per migliorare il tuo flusso di lavoro di sviluppo.

## Runtime degli script dell'editor {#editor-script-runtime}

Gli script dell'editor vengono eseguiti nell'editor, in una macchina virtuale Lua emulata dalla macchina virtuale Java. Tutti gli script condividono un unico ambiente e possono quindi interagire tra loro. Puoi caricare moduli Lua con `require`, come nei file `.script`, ma la versione di Lua eseguita nell'editor è diversa: assicurati quindi che il codice condiviso sia compatibile. L'editor usa Lua versione 5.2.x, più precisamente il runtime [luaj](https://github.com/luaj/luaj), che attualmente è l'unica soluzione praticabile per eseguire Lua sulla JVM. Esistono inoltre alcune limitazioni:
- il pacchetto `debug` non è disponibile;
- `os.execute` non è disponibile, ma forniamo la funzione analoga `editor.execute()`;
- `os.tmpname` e `io.tmpfile` non sono disponibili: attualmente gli script dell'editor possono accedere ai file soltanto nella directory del progetto;
- `os.rename` non è attualmente disponibile, anche se intendiamo aggiungerla;
- `os.exit` e `os.setlocale` non sono disponibili.
- alcune funzioni la cui esecuzione può richiedere tempo non possono essere usate nei contesti in cui l'editor richiede una risposta immediata dallo script; consulta [Modalità di esecuzione](#execution-modes) per maggiori dettagli.

Tutte le estensioni dell'editor definite negli script dell'editor vengono caricate quando apri un progetto. Quando recuperi le librerie, le estensioni vengono ricaricate perché le librerie da cui dipendi potrebbero contenere nuovi script dell'editor. Durante questo ricaricamento, le modifiche ai tuoi script dell'editor non vengono rilevate, perché potresti essere ancora impegnato a modificarli. Per ricaricare anche questi, esegui il comando **Project → Reload Editor Scripts**.

## Struttura di `.editor_script` {#anatomy-of-editor_script}

Ogni script dell'editor deve restituire un modulo, come questo:
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
L'editor raccoglie quindi tutti gli script dell'editor definiti nel progetto e nelle librerie, li carica in un'unica macchina virtuale Lua e li chiama quando necessario (per maggiori dettagli, consulta le sezioni [comandi](#commands) e [hook del ciclo di vita](#lifecycle-hooks)).

## API dell'editor {#editor-api}

Puoi interagire con l'editor usando il pacchetto `editor`, che definisce questa API:
- `editor.platform` — una stringa: `"x86_64-win32"` per Windows, `"x86_64-macos"` per macOS oppure `"x86_64-linux"` per Linux.
- `editor.version` — una stringa con il nome della versione di Defold, ad esempio `"1.4.8"`
- `editor.engine_sha1` — una stringa con lo SHA1 del motore Defold
- `editor.editor_sha1` — una stringa con lo SHA1 dell'editor Defold
- `editor.get(node_id, property)` — ottiene il valore di una proprietà di un nodo nell'editor. I nodi nell'editor rappresentano varie entità, come file di script o di collezione, oggetti di gioco all'interno di collezioni, file JSON caricati come risorse e così via. `node_id` è un valore userdata passato dall'editor allo script dell'editor. In alternativa all'ID del nodo puoi passare il percorso della risorsa, ad esempio `"/main/game.script"`. `property` è una stringa. Attualmente sono supportate queste proprietà:
  - `"path"` — il percorso del file a partire dalla cartella del progetto per le *risorse*, cioè entità che esistono come file o directory. Esempio di valore restituito: `"/main/game.script"`
  - `"children"` — elenco dei percorsi delle risorse figlie di una risorsa directory
  - `"parent"` — nodo genitore nell'editor per un nodo di Outline che ha un genitore
  - `"text"` — contenuto testuale di una risorsa modificabile come testo (ad esempio file di script o JSON). Esempio di valore restituito: `"function init(self)\nend"`. Questo non equivale a leggere il file con `io.open()`, perché puoi modificare un file senza salvarlo e tali modifiche sono disponibili soltanto accedendo alla proprietà `"text"`.
  - per gli atlas: `images` (elenco dei nodi dell'editor per le immagini dell'atlas) e `animations` (elenco dei nodi delle animazioni)
  - per le animazioni dell'atlas: `images` (come `images` nell'atlas)
  - per le tilemap: `layers` (elenco dei nodi dell'editor per i livelli della tilemap)
  - per i livelli delle tilemap: `tiles` (una griglia 2D illimitata di tile); consulta `tilemap.tiles.*` per maggiori informazioni
  - per gli effetti particellari: `emitters` (elenco dei nodi dell'editor per gli emettitori) e `modifiers` (elenco dei nodi dell'editor per i modificatori)
  - per gli emettitori degli effetti particellari: `modifiers` (elenco dei nodi dell'editor per i modificatori)
  - per gli oggetti di collisione: `shapes` (elenco dei nodi dell'editor per le forme di collisione)
  - per i file GUI: elenchi di nodi come `layers`, `fonts`, `materials`, `textures`, `particlefxs`, `nodes` e `layouts`
  - alcune proprietà mostrate nella vista Properties quando selezioni qualcosa nella vista Outline. Sono supportati questi tipi di proprietà della struttura:
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    Alcune di queste proprietà potrebbero essere di sola lettura o non essere disponibili in determinati contesti, quindi usa `editor.can_get` prima di leggerle e `editor.can_set` prima di farle impostare all'editor. Passa il puntatore sul nome di una proprietà nella vista Properties per visualizzare un suggerimento che indica come si chiama negli script dell'editor. Puoi impostare le proprietà delle risorse a `nil` fornendo il valore `""`.
- `editor.properties(node_id)` — restituisce un elenco ordinato, dipendente dal contesto, dei nomi delle proprietà leggibili da un nodo, ad esempio `pprint(editor.properties("/game.project"))`. Usa le funzioni `editor.can_*` per verificare se una proprietà elencata può anche essere modificata, reimpostata o riordinata, oppure se è possibile aggiungervi elementi.
- `editor.can_get(node_id, property)` — verifica se puoi leggere questa proprietà senza che `editor.get()` generi un errore.
- `editor.can_set(node_id, property)` — verifica se un passaggio di transazione `editor.tx.set()` con questa proprietà può essere eseguito senza generare un errore.
- `editor.create_directory(resource_path)` — crea una directory se non esiste, insieme a tutte le directory genitrici mancanti.
- `editor.create_resources(resources)` — crea una o più risorse, a partire da modelli o con contenuti personalizzati
- `editor.delete_directory(resource_path)` — elimina una directory, se esiste, e tutte le directory e i file che contiene.
- `editor.execute(cmd, [...args], [options])` — esegue un comando della shell, acquisendone facoltativamente l'output.
- `editor.save()` — salva su disco tutte le modifiche non salvate.
- `editor.transact(txs)` — modifica lo stato dell'editor in memoria usando uno o più passaggi di transazione creati con le funzioni `editor.tx.*`.
- `editor.ui.*` — varie funzioni relative all'interfaccia utente; consulta il [manuale dell'interfaccia utente](/manuals/editor-scripts-ui).
- `editor.prefs.*` — funzioni per interagire con le preferenze dell'editor; consulta [preferenze](#preferences).

Puoi trovare [qui](/ref/stable/editor/) il riferimento completo dell'API dell'editor.

## Comandi {#commands}

Se un modulo di script dell'editor definisce `get_commands()`, questa funzione viene chiamata al ricaricamento delle estensioni. I comandi restituiti possono comparire nei menu della barra dei menu e nei menu contestuali di Assets, Outline, Scene e Code, a seconda delle loro `locations`. Esempio:

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
L'editor si aspetta che `get_commands()` restituisca un array di tabelle, ognuna delle quali descrive un comando distinto. La descrizione di un comando comprende:

- `label` (obbligatorio) — testo della voce di menu mostrato all'utente
- `locations` (obbligatorio) — un array che descrive dove deve essere disponibile il comando. I valori supportati sono `"Edit"`, `"View"`, `"Project"`, `"Debug"` e `"Help"` per i menu corrispondenti nella barra dei menu; `"Bundle"` per il sottomenu **Project → Bundle**; e `"Assets"`, `"Outline"`, `"Scene"` e `"Code"` per i menu contestuali corrispondenti.
- `query` — un modo per il comando di richiedere all'editor le informazioni pertinenti e definire su quali dati opera. A ogni chiave nella tabella `query` corrisponde una chiave nella tabella `opts`, ricevuta come argomento dalle callback `active` e `run`. Chiavi supportate:
  - `selection` indica che il comando è valido quando è presente una selezione e che opera su tale selezione.
    - `type` è il tipo dei nodi selezionati a cui il comando è interessato; attualmente sono consentiti questi tipi:
      - `"resource"` — in Assets e Outline, la risorsa è l'elemento selezionato a cui corrisponde un file. Nella barra dei menu (Edit o View), la risorsa è il file attualmente aperto;
      - `"outline"` — qualcosa che può essere mostrato in Outline. In Outline è un elemento selezionato, nella barra dei menu è il file attualmente aperto;
      - `"scene"` — qualcosa che può essere visualizzato nella vista Scene.
    - `cardinality` definisce quanti elementi devono essere selezionati. Se vale `"one"`, la selezione passata alla callback del comando è l'ID di un singolo nodo. Se vale `"many"`, la selezione passata alla callback del comando è un array di uno o più ID di nodi.
  - `active_view` indica che il comando è valido quando la vista attiva dell'editor corrisponde al tipo richiesto. La vista attiva viene passata alla callback del comando come `opts.active_view`.
    - `type` è il tipo di vista attiva a cui il comando è interessato: `"code"`, `"scene"`, `"html"` oppure `"form"`.
    - La vista attiva supporta le proprietà `"type"`, `"resource"` e `"dirty"`. Usa `editor.get(view, "resource")` per ottenere la risorsa mostrata nella vista ed `editor.get(view, "dirty")` per verificare se contiene modifiche non salvate.
  - `argument` — argomento del comando. Attualmente ricevono un argomento soltanto i comandi nella posizione `"Bundle"`: vale `true` quando il comando di creazione del bundle viene selezionato esplicitamente e `false` quando si ricrea il bundle.
- `id` - stringa identificativa del comando, usata ad esempio per memorizzare in `prefs` l'ultimo comando di creazione del bundle utilizzato
- `active` - una callback eseguita per verificare che il comando sia attivo; deve restituire un valore booleano. Se `locations` include `"Assets"`, `"Scene"` o `"Outline"`, `active` viene chiamata quando viene mostrato il menu contestuale. Se le posizioni includono `"Edit"` o `"View"`, active viene chiamata a ogni interazione dell'utente, ad esempio quando digita sulla tastiera o fa clic con il mouse: assicurati quindi che `active` sia relativamente veloce.
- `run` - una callback eseguita quando l'utente seleziona la voce di menu.

### Usare i comandi per modificare lo stato dell'editor in memoria {#use-commands-to-change-the-in-memory-editor-state}

Nel gestore `run` puoi interrogare e modificare lo stato dell'editor in memoria. Le interrogazioni avvengono tramite la funzione `editor.get()`, con cui puoi chiedere all'editor lo stato attuale dei file e della selezione (se usi `query = {selection = ...}`). Puoi ottenere la proprietà `"text"` delle risorse modificabili come testo e alcune proprietà mostrate nella vista Properties: passa il puntatore sul nome della proprietà per visualizzare un suggerimento che indica come si chiama negli script dell'editor. Per modificare lo stato dell'editor usa `editor.transact()`, che raggruppa una o più modifiche in un unico passaggio annullabile. Ad esempio, per reimpostare la trasformazione di un oggetto di gioco, puoi scrivere un comando come questo:
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

### Usare i comandi con la vista attiva dell'editor {#use-commands-with-the-active-editor-view}

I comandi in posizioni di menu come `"View"` possono interrogare la vista attualmente attiva dell'editor. Questo è utile quando un comando deve operare sul file o sulla scena che l'utente sta visualizzando:

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

#### Modificare gli atlas {#editing-atlases}

Oltre a leggere e scrivere le proprietà di un atlas, puoi leggere e modificare le sue immagini e animazioni. L'atlas definisce le proprietà `images` e `animations`, che contengono elenchi di nodi, e le animazioni definiscono la proprietà `images`, anch'essa un elenco di nodi: puoi usare i passaggi di transazione `editor.tx.add`, `editor.tx.remove` ed `editor.tx.clear` con queste proprietà.

Ad esempio, per aggiungere un'immagine a un atlas, esegui il codice seguente nel gestore `run` del comando:
```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```
Per ottenere l'insieme di tutte le immagini di un atlas, esegui il codice seguente:
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
Per sostituire tutte le animazioni di un atlas:
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

#### Modificare le sorgenti di tile {#editing-tilesources}

Oltre alle proprietà della struttura, le sorgenti di tile definiscono le proprietà seguenti:
- `animations` - un elenco dei nodi delle animazioni della sorgente di tile
- `collision_groups` - un elenco dei nodi dei gruppi di collisione della sorgente di tile
- `tile_collision_groups` - una tabella che assegna i gruppi di collisione ai tile della sorgente

Ad esempio, puoi configurare una sorgente di tile in questo modo:
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

#### Modificare le tilemap {#editing-tilemaps}

Le tilemap definiscono la proprietà `layers`, un elenco dei nodi dei livelli della tilemap. Ogni livello definisce anche una proprietà `tiles`, che contiene una griglia 2D illimitata dei tile presenti nel livello. A differenza di quanto avviene nel motore, i tile non hanno limiti e possono essere aggiunti ovunque, anche a coordinate negative. Per modificare i tile, l'API degli script dell'editor definisce un modulo `tilemap.tiles` con le funzioni seguenti:
- `tilemap.tiles.new()` per creare una nuova struttura dati che contiene una griglia 2D illimitata di tile (nell'editor, a differenza del motore, la tilemap non ha limiti e le coordinate possono essere negative)
- `tilemap.tiles.get_tile(tiles, x, y)` per ottenere l'indice del tile a una coordinata specifica
- `tilemap.tiles.get_info(tiles, x, y)` per ottenere tutte le informazioni sul tile a una coordinata specifica (la struttura dei dati è identica a quella della funzione `tilemap.get_tile_info` del motore)
- `tilemap.tiles.iterator(tiles)` per creare un iteratore su tutti i tile della tilemap
- `tilemap.tiles.clear(tiles)` per rimuovere tutti i tile dalla tilemap
- `tilemap.tiles.set(tiles, x, y, tile_or_info)` per impostare un tile a una coordinata specifica
- `tilemap.tiles.remove(tiles, x, y)` per rimuovere un tile a una coordinata specifica

Ad esempio, puoi stampare il contenuto dell'intera tilemap in questo modo:
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

Questo esempio mostra come aggiungere a una tilemap un livello contenente dei tile:
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

#### Modificare gli effetti particellari {#editing-particlefx}

Puoi modificare gli effetti particellari usando le proprietà `modifiers` ed `emitters`. Ad esempio, per aggiungere un emettitore circolare con un modificatore di accelerazione:
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
Molte proprietà degli effetti particellari sono curve o curve con dispersione (cioè una curva più un valore di variazione casuale). Le curve sono rappresentate da una tabella con un elenco non vuoto di `points`, in cui ogni punto è una tabella con le proprietà seguenti:
- `x` - la coordinata x del punto; deve partire da 0 e terminare a 1
- `y` - il valore del punto
- `tx` (da 0 a 1) e `ty` (da -1 a 1) - componenti della tangente nel punto. Ad esempio, per un angolo di 80 gradi, `tx` deve essere `math.cos(math.rad(80))` e `ty` deve essere `math.sin(math.rad(80))`.
Le curve con dispersione hanno anche una proprietà numerica `spread`. 

Ad esempio, per impostare la curva del valore alfa lungo la durata di vita delle particelle di un emettitore già esistente, puoi usare:
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
Naturalmente puoi usare la chiave `particle_key_alpha` in una tabella anche quando crei un emettitore. Inoltre, puoi usare un singolo numero per rappresentare una curva "statica".

#### Modificare gli oggetti di collisione {#editing-collision-objects}

Oltre alle proprietà predefinite della struttura, gli oggetti di collisione definiscono la proprietà `shapes`, che contiene un elenco di nodi. Per aggiungere nuove forme di collisione:
```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- or "shape-type-sphere", "shape-type-capsule"
    })
})
```
La proprietà `type` della forma è obbligatoria durante la creazione e non può essere modificata dopo l'aggiunta della forma. Esistono 3 tipi di forme:
- `shape-type-box` - forma a parallelepipedo con la proprietà `dimensions`
- `shape-type-sphere` - forma sferica con la proprietà `diameter`
- `shape-type-capsule` - forma a capsula con le proprietà `diameter` e `height`

#### Modificare i file GUI {#editing-gui-files}

Oltre alle proprietà della struttura, i file GUI definiscono diverse proprietà che contengono elenchi di nodi:

- `layers` — elenco dei nodi dell'editor per i livelli (riordinabile)
- `fonts` — elenco dei nodi dell'editor per i font
- `materials` — elenco dei nodi dell'editor per i materiali
- `textures` — elenco dei nodi dell'editor per le texture
- `particlefxs` — elenco dei nodi dell'editor per gli effetti particellari
- `nodes` — elenco dei nodi dell'editor per i nodi GUI
- `layouts` — elenco dei nodi dell'editor per i layout della GUI

Puoi modificare i livelli della GUI usando la proprietà `layers` dell'editor, ad esempio:
```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```
Puoi inoltre riordinare i livelli:
```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```
Analogamente, puoi modificare font, materiali, texture ed effetti particellari usando le proprietà `fonts`, `materials`, `textures` e `particlefxs`:
```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.particlefx"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```
Queste proprietà non supportano il riordinamento.

Infine, puoi modificare i nodi GUI usando la proprietà elenco `nodes`, ad esempio:
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
I tipi di nodo integrati sono:
- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

Se usi l'estensione Spine, puoi utilizzare anche il tipo di nodo `gui-node-type-spine`.

Se il file GUI definisce dei layout, puoi ottenere e impostare i valori dei layout usando la sintassi `layout:property`, ad esempio:
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

Puoi ripristinare i valori predefiniti delle proprietà del layout che sono state impostate usando `editor.tx.reset`:
```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```
Gli alberi dei nodi dei modelli possono essere letti, ma non modificati: puoi soltanto impostare le proprietà dei nodi all'interno dell'albero del modello:
```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (overrides a value in the template)
```

#### Modificare gli oggetti di gioco {#editing-game-objects}

Puoi modificare i componenti di un file di oggetto di gioco usando gli script dell'editor. Esistono 2 tipi di componenti: referenziati e incorporati. I componenti referenziati usano il tipo `component-reference` e fanno riferimento ad altre risorse, consentendo soltanto di sovrascrivere le proprietà go definite negli script. I componenti incorporati usano tipi come `sprite`, `label` e così via, e consentono di modificare tutte le proprietà definite dal tipo di componente, oltre ad aggiungere sottocomponenti come le forme degli oggetti di collisione. Ad esempio, puoi usare il codice seguente per configurare un oggetto di gioco:
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

#### Modificare le collezioni {#editing-collections}
Puoi modificare le collezioni usando gli script dell'editor. Puoi aggiungere oggetti di gioco (incorporati o referenziati) e collezioni (referenziate). Ad esempio:
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

Come nell'editor, le collezioni referenziate possono essere aggiunte soltanto alla radice della collezione che stai modificando, mentre gli oggetti di gioco possono essere aggiunti soltanto a oggetti di gioco incorporati o referenziati, e non a collezioni referenziate o agli oggetti di gioco al loro interno.

### Usare i comandi della shell {#use-shell-commands}

Nel gestore `run` puoi scrivere nei file (usando il modulo `io`) ed eseguire comandi della shell (usando il comando `editor.execute()`). Quando esegui un comando della shell, puoi acquisirne l'output come stringa e usarlo nel codice. Ad esempio, per creare un comando che formatta JSON richiamando dalla shell [`jq`](https://jqlang.github.io/jq/) installato globalmente, puoi scrivere il comando seguente:
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
Poiché questo comando richiama un programma della shell in sola lettura (e lo comunica all'editor usando `reload_resources = false`), questa azione ha il vantaggio di poter essere annullata.

::: sidenote
Se vuoi distribuire il tuo script dell'editor come libreria, puoi includere nella dipendenza l'eseguibile del programma per le piattaforme dell'editor. Consulta [Script dell'editor nelle librerie](#editor-scripts-in-libraries) per maggiori dettagli su come farlo.
:::

## Hook del ciclo di vita {#lifecycle-hooks}

Esiste un file di script dell'editor che viene trattato in modo speciale: `hooks.editor_script`, situato nella radice del progetto, nella stessa directory di *game.project*. Soltanto questo script dell'editor riceve gli eventi del ciclo di vita dall'editor. Ecco un esempio di questo file:
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
Abbiamo deciso di limitare gli hook del ciclo di vita a un unico file di script dell'editor perché l'ordine di esecuzione degli hook di build è più importante della facilità con cui si aggiunge un altro passaggio di build. I comandi sono indipendenti tra loro, quindi l'ordine in cui compaiono nel menu non è particolarmente rilevante: l'utente esegue comunque il comando specifico che ha selezionato. Se fosse possibile definire gli hook di build in diversi script dell'editor, sorgerebbe un problema: in quale ordine verrebbero eseguiti? Probabilmente vorrai calcolare le checksum dei contenuti dopo averli compressi... Un unico file che stabilisce l'ordine dei passaggi di build chiamando esplicitamente la funzione di ogni passaggio permette di risolvere questo problema.

Gli hook del ciclo di vita disponibili che puoi definire in `/hooks.editor_script` sono:
- `on_build_started(opts)` — eseguito quando viene creata una build del gioco per l'esecuzione locale o su una destinazione remota usando le opzioni Project Build o Debug Start. Le tue modifiche saranno presenti nella build del gioco. Generare un errore da questo hook interrompe la build. `opts` è una tabella che contiene le chiavi seguenti:
  - `platform` — una stringa nel formato `%arch%-%os%` che descrive la piattaforma per cui viene creata la build; attualmente ha sempre lo stesso valore di `editor.platform`.
- `on_build_finished(opts)` — eseguito al termine della build, indipendentemente dall'esito. `opts` è una tabella con le chiavi seguenti:
  - `platform` — come in `on_build_started`
  - `success` — indica se la build è riuscita: `true` oppure `false`
- `on_bundle_started(opts)` — eseguito quando crei un bundle o una build HTML5 del gioco. Come per `on_build_started`, le modifiche attivate da questo hook saranno presenti nel bundle e gli errori ne interromperanno la creazione. `opts` contiene queste chiavi:
  - `output_directory` — un percorso di file che indica la directory con l'output del bundle. **Project ▸ Build HTML5** usa una propria struttura di artefatti, ad esempio `"/path/to/project/build/default_html5/__htmlLaunchDir"`, distinta dal normale output di Build in `build/default`.
  - `platform` — piattaforma per cui viene creato il bundle del gioco. Consulta l'elenco dei possibili valori della piattaforma nel [manuale di Bob](/manuals/bob).
  - `variant` — variante del bundle: `"debug"`, `"release"` oppure `"headless"`
- `on_bundle_finished(opts)` — eseguito al termine della creazione del bundle, indipendentemente dall'esito. `opts` è una tabella con gli stessi dati di `opts` in `on_bundle_started`, più la chiave `success` che indica se la build è riuscita.
- `on_target_launched(opts)` — eseguito quando l'utente avvia un gioco e l'avvio riesce. `opts` contiene una chiave `url` che indica il servizio del motore avviato, ad esempio `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — eseguito quando il gioco avviato viene chiuso; ha gli stessi opts di `on_target_launched`

Tieni presente che gli hook del ciclo di vita sono attualmente una funzionalità esclusiva dell'editor e non vengono eseguiti da Bob quando crei un bundle dalla riga di comando.

## Server di linguaggio {#language-servers}

L'editor supporta un sottoinsieme del [Language Server Protocol](https://microsoft.github.io/language-server-protocol/): diagnostica (analisi statica), completamento, informazioni al passaggio del puntatore, simboli del documento nel pannello Structure, navigazione alla definizione, ricerca dei riferimenti e ridenominazione dei simboli. Passa il puntatore su un simbolo per visualizzare le informazioni del server di linguaggio. Con il cursore su un simbolo, usa <kbd>F2</kbd> per rinominarlo, <kbd>F12</kbd> per andare alla sua definizione oppure <kbd>Shift+F12</kbd> per trovare i riferimenti. Queste azioni sono disponibili anche nel menu <kbd>Edit</kbd>.

Per definire il server di linguaggio, modifica la funzione `get_language_servers` del tuo script dell'editor in questo modo:

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
L'editor avvia il server di linguaggio usando il `command` specificato e comunica tramite l'input e l'output standard del processo del server.

La tabella che definisce il server di linguaggio può specificare:
- `languages` (obbligatorio) — un elenco dei linguaggi a cui il server è interessato, come definiti [qui](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers) (sono accettate anche le estensioni dei file);
- `command` (obbligatorio) - un array contenente il comando e i suoi argomenti
- `watched_files` - un array di tabelle con chiavi `pattern` (un glob) che attivano la notifica del server relativa ai [file monitorati modificati](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles).

## Server HTTP {#http-server}

Ogni istanza dell'editor in esecuzione dispone di un server HTTP attivo. Puoi estendere il server usando gli script dell'editor. Per estendere il server HTTP dell'editor, aggiungi allo script dell'editor la funzione `get_http_server_routes`, che deve restituire le route aggiuntive:
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
Dopo aver ricaricato gli script dell'editor, vedrai nella console l'output seguente: `My route: http://0.0.0.0:12345/my-extension`. Aprendo questo link nel browser, vedrai il messaggio `"Hello world!"`.

L'argomento di input `request` è una semplice tabella Lua con informazioni sulla richiesta. Contiene chiavi come `path` (il segmento di percorso dell'URL che inizia con `/`), `method` della richiesta (ad esempio `"GET"`), `headers` (una tabella con i nomi delle intestazioni in minuscolo) e, facoltativamente, `query` (la stringa di query) e `body` (se la route definisce come interpretare il corpo). Ad esempio, se vuoi creare una route che accetta un corpo JSON, definiscila con il parametro del convertitore impostato a `"json"`:
```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```
Puoi provare questo endpoint dalla riga di comando usando `curl` e `jq`:
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
Il percorso della route supporta pattern che permettono di estrarre valori dal percorso della richiesta e passarli alla funzione del gestore come parte della richiesta, ad esempio:
```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```
Ora, aprendo ad esempio `http://0.0.0.0:12345/my-extension/setting/project.title`, vedrai il titolo del gioco letto dal file `/game.project`.

Oltre ai pattern che corrispondono a un singolo segmento di percorso, puoi acquisire anche il resto del percorso dell'URL usando la sintassi `{*name}`. Ad esempio, questo semplice endpoint di un server di file serve i file dalla radice del progetto:
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
Ora, aprendo ad esempio `http://0.0.0.0:12345/my-extension/files/main/main.collection` nel browser, vedrai il contenuto del file `main/main.collection`.

## Script dell'editor nelle librerie {#editor-scripts-in-libraries}

Puoi pubblicare librerie contenenti comandi che altre persone possono usare: l'editor li rileva automaticamente. Gli hook, invece, non possono essere rilevati automaticamente perché devono essere definiti in un file nella cartella radice di un progetto, mentre le librerie espongono soltanto le sottocartelle. Questo comportamento offre un maggiore controllo sul processo di build: puoi comunque creare gli hook del ciclo di vita come semplici funzioni nei file `.lua`, così che gli utenti della tua libreria possano caricarle e usarle nel proprio `/hooks.editor_script`.

Tieni inoltre presente che le dipendenze, pur essendo mostrate nella vista Assets, non esistono come file: sono voci di un archivio ZIP. Puoi fare in modo che l'editor estragga alcuni file dalle dipendenze nella cartella `build/plugins/`. Per farlo, crea un file `ext.manifest` nella cartella della libreria, quindi crea la cartella `plugins/bin/${platform}` nella stessa cartella in cui si trova `ext.manifest`. I file presenti in questa cartella vengono estratti automaticamente nella cartella `/build/plugins/${extension-path}/plugins/bin/${platform}`, in modo che i tuoi script dell'editor possano farvi riferimento.

## Preferenze {#preferences}

Gli script dell'editor possono definire e usare preferenze: dati persistenti, esclusi dai commit, memorizzati sul computer dell'utente. Queste preferenze hanno tre caratteristiche fondamentali:
- tipizzate: ogni preferenza ha una definizione di schema che include il tipo di dato e altri metadati, come il valore predefinito
- con un ambito: le preferenze si applicano a un singolo progetto o a un utente
- annidate: ogni chiave di preferenza è una stringa con segmenti separati da punti, in cui il primo segmento del percorso identifica uno script dell'editor, mentre i restanti identificano gruppi e singole preferenze al suo interno

Tutte le preferenze devono essere registrate definendone lo schema:
```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```
Dopo il ricaricamento di questo script dell'editor, l'editor registra lo schema. Lo script dell'editor può quindi ottenere e impostare le preferenze, ad esempio:
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

## Modalità di esecuzione {#execution-modes}

Il runtime degli script dell'editor usa 2 modalità di esecuzione, perlopiù trasparenti agli script dell'editor: **immediata** e **di lunga durata**. 

La modalità **immediata** viene usata quando l'editor deve ricevere una risposta dallo script il più rapidamente possibile. Ad esempio, le callback `active` dei comandi di menu vengono eseguite in modalità immediata perché queste verifiche avvengono sul thread dell'interfaccia utente dell'editor in risposta alle interazioni dell'utente e devono aggiornare l'interfaccia entro lo stesso frame. 

La modalità **di lunga durata** viene usata quando l'editor non ha bisogno di una risposta istantanea dallo script. Ad esempio, le callback `run` dei comandi di menu vengono eseguite in modalità **di lunga durata**, consentendo allo script di impiegare più tempo per completare il proprio lavoro.

Alcune funzioni disponibili agli script dell'editor possono richiedere molto tempo per essere eseguite. Ad esempio, `editor.execute("git", "status", {reload_resources=false, out="capture"})` può richiedere fino a un secondo nei progetti abbastanza grandi. Per mantenere la reattività e le prestazioni dell'editor, le funzioni che possono richiedere tempo non sono consentite nei contesti in cui l'editor richiede una risposta immediata. Tentare di usare una di queste funzioni in un contesto immediato genera l'errore: `Cannot use long-running editor function in immediate context`. Per risolverlo, evita di usare queste funzioni nei contesti immediati.

Le funzioni seguenti sono considerate di lunga durata e non possono essere usate in modalità immediata:
- `editor.create_directory()`, `editor.create_resources()`, `editor.delete_directory()`, `editor.save()`, `os.remove()` e `file:write()`: queste funzioni modificano i file su disco e inducono l'editor a sincronizzare il proprio albero delle risorse in memoria con lo stato del disco; nei progetti grandi questa operazione può richiedere secondi.
- `editor.execute()`: l'esecuzione dei comandi della shell può richiedere una quantità di tempo imprevedibile.
- `editor.transact()`: transazioni di grandi dimensioni su nodi a cui fanno riferimento molti altri nodi possono richiedere centinaia di millisecondi, compromettendo la reattività dell'interfaccia utente.

I contesti di esecuzione del codice seguenti usano la modalità immediata:
- Le callback `active` dei comandi di menu: l'editor richiede una risposta dallo script entro lo stesso frame dell'interfaccia utente.
- Il livello principale degli script dell'editor: il ricaricamento degli script dell'editor non deve avere effetti collaterali.

## Azioni {#actions}

::: sidenote
In precedenza, l'editor interagiva con la macchina virtuale Lua in modo bloccante. Era quindi indispensabile che gli script dell'editor non bloccassero l'esecuzione, perché alcune interazioni devono avvenire dal thread dell'interfaccia utente dell'editor. Per questo motivo, ad esempio, `editor.execute()` ed `editor.transact()` non erano disponibili. L'esecuzione degli script e la modifica dello stato dell'editor venivano invece attivate restituendo un array di "azioni" dagli hook e dai gestori `run` dei comandi.

Ora l'editor interagisce con la macchina virtuale Lua in modo non bloccante, quindi queste azioni non sono più necessarie: usare funzioni come `editor.execute()` è più comodo, conciso e potente. Le azioni sono ora **DEPRECATE**, anche se non prevediamo di rimuoverle.
:::

Gli script dell'editor possono restituire un array di azioni dalla funzione `run` di un comando o dalle funzioni degli hook di `/hooks.editor_script`. Queste azioni vengono poi eseguite dall'editor.

Un'azione è una tabella che descrive ciò che l'editor deve fare. Ogni azione ha una chiave `action`. Esistono 2 tipi di azioni: annullabili e non annullabili.

### Azioni annullabili {#undoable-actions}

::: sidenote
Preferisci `editor.transact()`.
:::

Un'azione annullabile può essere annullata dopo l'esecuzione. Se un comando restituisce più azioni annullabili, queste vengono eseguite insieme e annullate insieme. Usa le azioni annullabili quando possibile. Il loro svantaggio è che sono più limitate.

Azioni annullabili disponibili:
- `"set"` — imposta un valore per una proprietà di un nodo nell'editor. Esempio:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  L'azione `"set"` richiede queste chiavi:
  - `node_id` — userdata con l'ID del nodo. In alternativa, puoi usare il percorso della risorsa al posto dell'ID del nodo ricevuto dall'editor, ad esempio `"/main/game.script"`;
  - `property` — una proprietà del nodo da impostare, ad esempio `"text"`;
  - `value` — nuovo valore della proprietà. Per la proprietà `"text"` deve essere una stringa.

### Azioni non annullabili {#non-undoable-actions}

::: sidenote
Preferisci `editor.execute()`.
:::

Un'azione non annullabile cancella la cronologia di annullamento. Se vuoi annullarla, devi quindi usare altri mezzi, come il controllo di versione.

Azioni non annullabili disponibili:
- `"shell"` — esegue uno script della shell. Esempio:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- trim leading "/"
    }
  }
  ```
  L'azione `"shell"` richiede la chiave `command`, che è un array contenente il comando e i suoi argomenti.

### Combinare azioni ed effetti collaterali {#mixing-actions-and-side-effects}

Puoi combinare azioni annullabili e non annullabili. Le azioni vengono eseguite in sequenza, quindi, a seconda del loro ordine, potresti perdere la possibilità di annullare alcune parti del comando.

Invece di restituire azioni dalle funzioni che le prevedono, puoi leggere e scrivere direttamente nei file usando `io.open()`. Questo attiva un ricaricamento delle risorse che cancella la cronologia di annullamento.
