---
title: La pipeline di rendering in Defold
brief: Questo manuale spiega come funziona la pipeline di rendering di Defold e come puoi programmarla.
---

# Rendering {#render}

Ogni oggetto che il motore mostra sullo schermo, che si tratti di sprite, modelli, tile, particelle o nodi GUI, viene disegnato da un sistema di rendering. Al centro di questo sistema c'è uno script di rendering che controlla la pipeline di rendering. Per impostazione predefinita, ogni oggetto 2D viene disegnato con la bitmap corretta, la fusione specificata e la profondità Z appropriata---quindi potresti non doverti mai occupare del rendering oltre all'ordinamento e alle semplici operazioni di fusione. Per la maggior parte dei giochi 2D, la pipeline predefinita funziona bene, ma il tuo gioco potrebbe avere esigenze particolari. In tal caso, Defold ti consente di scrivere una pipeline di rendering su misura.

### Pipeline di rendering - Cosa, quando e dove? {#render-pipeline-what-when-and-where}

La pipeline di rendering controlla cosa disegnare, quando disegnarlo e anche dove disegnarlo. I [predicati di rendering](#render-predicates) controllano cosa disegnare. Lo [script di rendering](#the-render-script) controlla quando disegnare un predicato, mentre la [proiezione della vista](#default-view-projection) controlla dove disegnarlo. La pipeline di rendering può anche escludere gli elementi grafici disegnati da un predicato di rendering che si trovano all'esterno di un volume delimitatore (bounding box) o di un volume di vista (frustum) definito. Questo processo è chiamato frustum culling.


## Il rendering predefinito {#the-default-render}

Il file di rendering contiene un riferimento allo script di rendering corrente e ai materiali personalizzati da rendere disponibili nello script di rendering (da usare con [`render.enable_material()`](/ref/render/#render.enable_material))

Al centro della pipeline di rendering c'è lo _script di rendering_. È uno script Lua con le funzioni `init()`, `update()` e `on_message()`, usato principalmente per interagire con l'API grafica sottostante. Lo script di rendering occupa un posto particolare nel ciclo di vita del gioco. Puoi trovare i dettagli nella [documentazione sul ciclo di vita dell'applicazione](/manuals/application-lifecycle).

Nella cartella "Builtins" dei tuoi progetti puoi trovare la risorsa di rendering predefinita ("default.render") e lo script di rendering predefinito ("default.render_script").

![Rendering integrato](images/render/builtin.png)

Per configurare un sistema di rendering personalizzato:

1. Copia i file "default.render" e "default.render_script" in una posizione nella gerarchia del tuo progetto. Puoi naturalmente creare uno script di rendering da zero, ma partire da una copia dello script predefinito è una buona idea, soprattutto se stai iniziando a usare Defold e/o a programmare la grafica.

2. Modifica la tua copia del file "default.render" e cambia la proprietà *Script* in modo che faccia riferimento alla tua copia dello script di rendering.

3. Cambia la proprietà *Render* (nella sezione *bootstrap*) nel file delle impostazioni *game.project* in modo che faccia riferimento alla tua copia del file "default.render".


## Predicati di rendering {#render-predicates}

Per controllare l'ordine in cui vengono disegnati gli oggetti, crea dei _predicati_ di rendering. Un predicato dichiara cosa deve essere disegnato in base a una selezione di _tag_ dei materiali.

Ogni oggetto disegnato sullo schermo ha un materiale associato che controlla come deve essere disegnato. Nel materiale specifichi uno o più _tag_ da associare al materiale stesso.

Nel tuo script di rendering puoi quindi creare un *predicato di rendering* e specificare quali tag devono appartenervi. Quando indichi al motore di disegnare il predicato, viene disegnato ogni oggetto il cui materiale contiene tutti i tag specificati per quel predicato.

```
Sprite 1        Sprite 2        Sprite 3        Sprite 4
Material A      Material A      Material B      Material C
  outlined        outlined        greyscale       outlined
  tree            tree            tree            house
```

```lua
-- a predicate matching all sprites with tag "tree"
local trees = render.predicate({"tree"})
-- will draw Sprite 1, 2 and 3
render.draw(trees)

-- a predicate matching all sprites with tag "outlined"
local outlined = render.predicate({"outlined"})
-- will draw Sprite 1, 2 and 4
render.draw(outlined)

-- a predicate matching all sprites with tags "outlined" AND "tree"
local outlined_trees = render.predicate({"outlined", "tree"})
-- will draw Sprite 1 and 2
render.draw(outlined_trees)
```


Una descrizione dettagliata del funzionamento dei materiali è disponibile nella [documentazione sui materiali](/manuals/material).


## Proiezione della vista predefinita {#default-view-projection}

Lo script di rendering predefinito è configurato per usare una proiezione ortografica adatta ai giochi 2D. Offre tre diverse proiezioni ortografiche: `Stretch` (predefinita), `Fixed Fit` e `Fixed`. In alternativa alle proiezioni ortografiche dello script di rendering predefinito, puoi anche usare la matrice di proiezione fornita da un componente camera.

### Proiezione Stretch {#stretch-projection}

La proiezione Stretch disegna sempre un'area del gioco corrispondente alle dimensioni impostate in *game.project*, anche quando la finestra viene ridimensionata. Se il rapporto d'aspetto cambia, il contenuto del gioco viene allungato verticalmente oppure orizzontalmente:

![Proiezione Stretch](images/render/stretch_projection.png)

*Proiezione Stretch con le dimensioni originali della finestra*

![Proiezione Stretch dopo il ridimensionamento](images/render/stretch_projection_resized.png)

*Proiezione Stretch con la finestra allargata orizzontalmente*

La proiezione Stretch è quella predefinita, ma se l'hai cambiata e vuoi ripristinarla puoi farlo inviando un messaggio allo script di rendering:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

### Proiezione Fixed Fit {#fixed-fit-projection}

Come la proiezione Stretch, la proiezione Fixed Fit mostra sempre un'area del gioco corrispondente alle dimensioni impostate in *game.project*. Tuttavia, se la finestra viene ridimensionata e il rapporto d'aspetto cambia, il contenuto del gioco mantiene il rapporto d'aspetto originale e viene mostrato ulteriore contenuto in verticale oppure in orizzontale:

![Proiezione Fixed Fit](images/render/fixed_fit_projection.png)

*Proiezione Fixed Fit con le dimensioni originali della finestra*

![Proiezione Fixed Fit dopo il ridimensionamento](images/render/fixed_fit_projection_resized.png)

*Proiezione Fixed Fit con la finestra allargata orizzontalmente*

![Proiezione Fixed Fit con dimensioni ridotte](images/render/fixed_fit_projection_resized_smaller.png)

*Proiezione Fixed Fit con la finestra ridotta al 50% delle dimensioni originali*

Per attivare la proiezione Fixed Fit, invia un messaggio allo script di rendering:

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

### Proiezione Fixed {#fixed-projection}

La proiezione Fixed mantiene il rapporto d'aspetto originale e disegna il contenuto del gioco con un livello di zoom fisso. Questo significa che, se il livello di zoom è diverso dal 100%, viene mostrata un'area del gioco maggiore o minore rispetto a quella definita dalle dimensioni in *game.project*:

![Proiezione Fixed](images/render/fixed_projection_zoom_2_0.png)

*Proiezione Fixed con zoom impostato a 2*

![Proiezione Fixed](images/render/fixed_projection_zoom_0_5.png)

*Proiezione Fixed con zoom impostato a 0.5*

![Proiezione Fixed](images/render/fixed_projection_zoom_2_0_resized.png)

*Proiezione Fixed con zoom impostato a 2 e finestra ridotta al 50% delle dimensioni originali*

Per attivare la proiezione Fixed, invia un messaggio allo script di rendering:

```lua
msg.post("@render:", "use_fixed_projection", { near = -1, far = 1, zoom = 2 })
```

### Proiezione della camera {#camera-projection}

Quando usi lo script di rendering predefinito e nel progetto sono disponibili [componenti camera](/manuals/camera) abilitati, questi hanno la precedenza su qualsiasi altra vista o proiezione impostata nello script di rendering. Per saperne di più sull'uso dei componenti camera negli script di rendering, consulta la [documentazione sulla camera](/manuals/camera).

Le camere ortografiche supportano una proprietà `Orthographic Mode` che controlla come la camera si adatta alla finestra:
- `Fixed` usa il valore `Orthographic Zoom` della camera.
- `Auto Fit` (contenimento) mantiene visibile l'intera area di progetto.
- `Auto Cover` (copertura) riempie la finestra e può ritagliare il contenuto.

Puoi cambiare modalità nell'editor oppure durante l'esecuzione tramite l'API della camera:

```lua
-- Use auto-fit behavior with an orthographic camera
camera.set_orthographic_mode("main:/go#camera", camera.ORTHO_MODE_AUTO_FIT)
-- Query current mode
local mode = camera.get_orthographic_mode("main:/go#camera")
```

## Frustum culling

L'API di rendering di Defold consente agli sviluppatori di eseguire il cosiddetto frustum culling. Quando il frustum culling è abilitato, tutti gli elementi grafici che si trovano all'esterno di un volume delimitatore o di un frustum definito vengono ignorati. In un mondo di gioco ampio, di cui è visibile solo una parte alla volta, il frustum culling può ridurre drasticamente la quantità di dati da inviare alla GPU per il rendering, migliorando così le prestazioni e risparmiando batteria sui dispositivi mobili. Per creare il volume delimitatore si usano comunemente la vista e la proiezione della camera. Lo script di rendering predefinito usa la vista e la proiezione della camera per calcolare un frustum.

Abilita il frustum culling per una chiamata di disegno passando una matrice di vista-proiezione nell'opzione `frustum` di `render.draw()`:

```lua
local frustum = self.proj * self.view
render.draw(predicates.particle, { frustum = frustum })
```

Quando esegui il rendering con un componente camera, `render.set_camera()` può usare automaticamente la matrice di vista-proiezione della camera per le successive chiamate di disegno:

```lua
render.set_camera("main:/go#camera", { use_frustum = true })
render.draw(predicates.particle)
render.set_camera()
```

Con entrambi i metodi, gli emettitori di effetti particellari vengono esclusi in base ai loro volumi delimitatori.

Il frustum culling è implementato nel motore per ciascun tipo di componente. Stato attuale:

| Componente  | Supportato |
|-------------|-----------|
| Sprite      | SÌ        |
| Modello     | SÌ        |
| Mesh        | SÌ (1)    |
| Etichetta   | SÌ        |
| Spine       | SÌ        |
| Effetto particellare | SÌ |
| Tilemap     | SÌ        |
| Rive        | NO        |

1 = Il volume delimitatore della mesh deve essere impostato dallo sviluppatore. [Ulteriori informazioni](/manuals/mesh/#frustum-culling).


::: sidenote
A partire da Defold 1.13.0, le primitive dei componenti usano un ordinamento antiorario dei vertici, con la normale della primitiva rivolta verso la camera. Sprite, nodi GUI, tilemap (griglie di tile) ed effetti particellari usano lo stesso ordinamento degli altri tipi di componenti, quindi è possibile usare le stesse impostazioni di esclusione delle facce per tutti i componenti.

Questo può influire sui progetti che impostano l'esclusione delle facce per componenti diversi dai modelli. Se un componente viene escluso inaspettatamente, assicurati che siano selezionate le facce posteriori con `render.set_cull_face(graphics.FACE_TYPE_BACK)`, oppure rimuovi la chiamata a `render.set_cull_face()` per usare la modalità predefinita `graphics.FACE_TYPE_BACK`.
:::

## Sistemi di coordinate {#coordinate-systems}

Quando si esegue il rendering dei componenti, di solito si specifica il sistema di coordinate in cui vengono disegnati. Nella maggior parte dei giochi, alcuni componenti vengono disegnati nello spazio del mondo e altri nello spazio dello schermo.

I componenti GUI e i loro nodi vengono solitamente disegnati nelle coordinate dello spazio dello schermo, dove l'angolo inferiore sinistro ha coordinate (0,0) e quello superiore destro ha coordinate (larghezza dello schermo, altezza dello schermo). Il sistema di coordinate dello spazio dello schermo non viene mai spostato o traslato in altro modo da una camera. In questo modo i nodi GUI vengono sempre disegnati sullo schermo, indipendentemente da come viene rappresentato il mondo.

Sprite, tilemap e altri componenti usati dagli oggetti di gioco presenti nel tuo mondo di gioco vengono solitamente disegnati nel sistema di coordinate dello spazio del mondo. Se non modifichi lo script di rendering e non usi un componente camera per cambiare la proiezione della vista, questo sistema di coordinate coincide con quello dello spazio dello schermo. Appena aggiungi una camera e la sposti oppure cambi la proiezione della vista, però, i due sistemi di coordinate iniziano a differire. Quando la camera si muove, l'angolo inferiore sinistro dello schermo si sposta rispetto a (0, 0), in modo da disegnare altre parti del mondo. Se la proiezione cambia, le coordinate vengono sia traslate (cioè spostate rispetto a 0, 0) sia modificate da un fattore di scala.


## Lo script di rendering {#the-render-script}

Di seguito trovi il codice di uno script di rendering personalizzato, che è una versione leggermente modificata di quello integrato.

init()
: La funzione `init()` serve a configurare i predicati, la vista e il colore di cancellazione. Queste variabili vengono usate durante il rendering vero e proprio.

```lua
function init(self)
    -- Define the render predicates. Each predicate is drawn by itself and
    -- that allows us to change the state of OpenGL between the draws.
    self.predicates = create_predicates("tile", "gui", "text", "particle", "model")

    -- Create and fill data tables will be used in update()
    local state = create_state()
    self.state = state
    local camera_world = create_camera(state, "camera_world", true)
    init_camera(camera_world, get_stretch_projection)
    local camera_gui = create_camera(state, "camera_gui")
    init_camera(camera_gui, get_gui_projection)
    update_state(state)
end
```

update()
: La funzione `update()` viene chiamata una volta per ogni fotogramma. Il suo compito è eseguire il disegno vero e proprio chiamando le API OpenGL ES sottostanti (OpenGL Embedded Systems API). Per capire bene cosa succede nella funzione `update()`, devi conoscere il funzionamento di OpenGL. Sono disponibili molte ottime risorse su OpenGL ES. Il sito ufficiale è un buon punto di partenza e si trova all'indirizzo https://www.khronos.org/opengles/

  Questo esempio contiene la configurazione necessaria per disegnare modelli 3D. La funzione `init()` ha definito un predicato `self.predicates.model`. Altrove è stato creato un materiale con il tag "model". Sono inoltre presenti alcuni componenti modello che usano quel materiale:

```lua
function update(self)
    local state = self.state
     if not state.valid then
        if not update_state(state) then
            return
        end
    end

    local predicates = self.predicates
    -- clear screen buffers
    --
    render.set_depth_mask(true)
    render.set_stencil_mask(0xff)
    render.clear(state.clear_buffers)

    local camera_world = state.cameras.camera_world
    render.set_viewport(0, 0, state.window_width, state.window_height)
    render.set_view(camera_world.view)
    render.set_projection(camera_world.proj)


    -- render models
    --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_CULL_FACE)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_depth_mask(true)
    render.draw(predicates.model_pred)
    render.set_depth_mask(false)
    render.disable_state(graphics.STATE_DEPTH_TEST)
    render.disable_state(graphics.STATE_CULL_FACE)

     -- render world (sprites, tilemaps, particles etc)
     --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.enable_state(graphics.STATE_BLEND)
    render.draw(predicates.tile)
    render.draw(predicates.particle)
    render.disable_state(graphics.STATE_STENCIL_TEST)
    render.disable_state(graphics.STATE_DEPTH_TEST)

    -- debug
    render.draw_debug3d()

    -- render GUI
    --
    local camera_gui = state.cameras.camera_gui
    render.set_view(camera_gui.view)
    render.set_projection(camera_gui.proj)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.draw(predicates.gui, camera_gui.frustum)
    render.draw(predicates.text, camera_gui.frustum)
    render.disable_state(graphics.STATE_STENCIL_TEST)
end
```

Fin qui, lo script di rendering è semplice e lineare: disegna nello stesso modo a ogni fotogramma. A volte, però, può essere utile introdurre uno stato nello script di rendering ed eseguire operazioni diverse in base a tale stato. Può anche essere utile comunicare con lo script di rendering da altre parti del codice del gioco.

on_message()
: Uno script di rendering può definire una funzione `on_message()` e ricevere messaggi da altre parti del gioco o dell'applicazione. Un caso comune in cui un componente esterno invia informazioni allo script di rendering è la _camera_. Un componente camera che ha acquisito il focus della camera invia automaticamente la propria vista e la propria proiezione allo script di rendering a ogni fotogramma. Questo messaggio si chiama `"set_view_projection"`:

```lua
local MSG_CLEAR_COLOR =         hash("clear_color")
local MSG_WINDOW_RESIZED =      hash("window_resized")
local MSG_SET_VIEW_PROJ =       hash("set_view_projection")

function on_message(self, message_id, message)
    if message_id == MSG_CLEAR_COLOR then
        -- Someone sent us a new clear color to be used.
        update_clear_color(state, message.color)
    elseif message_id == MSG_SET_VIEW_PROJ then
        -- The camera component that has camera focus will sent set_view_projection
        -- messages to the @render socket. We can use the camera information to
        -- set view (and possibly projection) of the rendering.
        camera.view = message.view
        self.camera_projection = message.projection or vmath.matrix4()
        update_camera(camera, state)
    end
end
```

Qualsiasi script o script GUI può comunque inviare messaggi allo script di rendering tramite il socket speciale `@render`:

```lua
-- Change the clear color.
msg.post("@render:", "clear_color", { color = vmath.vector4(0.3, 0.4, 0.5, 0) })
```

## Risorse di rendering {#render-resources}
Per passare determinate risorse del motore allo script di rendering, puoi aggiungerle alla tabella `Render Resources` nel file `.render` assegnato al progetto:

![Risorse di rendering](images/render/render_resources.png)

Uso di queste risorse in uno script di rendering:

```lua
-- "my_material" will now be used for all draw calls associated with the predicate
render.enable_material("my_material")
-- anything drawn by the predicate will end up in "my_render_target"
render.set_render_target("my_render_target")
render.draw(self.my_full_screen_predicate)
render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.disable_material()

-- bind the render target result texture to whatever is getting rendered via the predicate
render.enable_texture(0, "my_render_target", graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.my_tile_predicate)
```

::: sidenote
Attualmente Defold supporta soltanto `Materials` e `Render Targets` come risorse di rendering referenziate, ma nel tempo questo sistema supporterà altri tipi di risorse.
:::

### Render target multicampionati {#multisampled-render-targets}

I render target supportano l'antialiasing multicampione (MSAA), che smussa i bordi della geometria in un passaggio di rendering fuori schermo. Il numero di campioni del target è indipendente da [Display ▸ Samples](/manuals/project-settings/#samples), che controlla l'antialiasing della finestra.

Per una risorsa `.render_target`, imposta **Sample Count** nell'editor su `1`, `2`, `4`, `8` o `16`. Il valore `1` disabilita il multicampionamento. Aggiungi la risorsa alla tabella **Render Resources** del file `.render` e usa il nome assegnato con `render.set_render_target()`, come nell'esempio precedente.

In alternativa, crea un target in `init()` dello script di rendering. Inserisci `sample_count` nella tabella esterna dei parametri, accanto agli allegati:

```lua
self.offscreen = render.render_target({
    sample_count = 4,
    [graphics.BUFFER_TYPE_COLOR0_BIT] = {
        format = graphics.TEXTURE_FORMAT_RGBA,
        width = 1024,
        height = 1024,
        min_filter = graphics.TEXTURE_FILTER_LINEAR,
        mag_filter = graphics.TEXTURE_FILTER_LINEAR,
        u_wrap = graphics.TEXTURE_WRAP_CLAMP_TO_EDGE,
        v_wrap = graphics.TEXTURE_WRAP_CLAMP_TO_EDGE,
    },
})
self.scene_predicate = render.predicate({"scene"})
self.present_predicate = render.predicate({"present"})
```

Questo esempio usa un target con il solo colore. Tutti gli allegati di colore, profondità e stencil di un target condividono il suo numero di campioni. Aggiungi un allegato di profondità e il normale stato del test di profondità se il passaggio lo richiede.

Per il seguente frammento di `update()`, assegna il tag `scene` ai materiali della scena e il tag `present` al materiale di un quadrilatero a schermo intero. Il materiale del quadrilatero deve campionare l'unità di texture `0`. Imposta vista e proiezione appropriate per ogni passaggio:

```lua
render.set_render_target(self.offscreen)
render.set_viewport(0, 0, 1024, 1024)
render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = vmath.vector4(0, 0, 0, 1)})
-- Set the scene view and projection here.
render.draw(self.scene_predicate)

render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.set_viewport(0, 0, render.get_window_width(), render.get_window_height())
-- Set the full-screen quad view and projection here.
render.enable_texture(0, self.offscreen, graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.present_predicate)
render.disable_texture(0)
```

Passare a un altro target termina il passaggio e risolve automaticamente i suoi allegati di colore multicampionati. `render.enable_texture()` associa la texture di colore risolta, quindi il quadrilatero usa un normale campionatore di texture. Non serve un comando di risoluzione separato.

Il numero di campioni richiesto ha valore predefinito `1` e deve essere un intero positivo. I backend grafici riducono le richieste non supportate a un numero supportato che sia una potenza di due, ricorrendo a `1` se necessario, e registrano un avviso quando il numero cambia. Un numero maggiore di campioni aumenta la memoria richiesta dagli allegati.

Quando usi una risorsa render target, verifica il numero effettivo di campioni da uno `.script` di un oggetto di gioco con `resource.get_render_target_info()`. Per esempio, dopo aver aggiunto `/render/offscreen.render_target` a **Render Resources**:

```lua
function init(self)
    local info = resource.get_render_target_info("/render/offscreen.render_targetc")
    print("Render target sample count:", info.sample_count)
end
```

Usa questo numero effettivo per verificare il supporto del dispositivo, senza presumere che il numero richiesto fosse disponibile. Consulta [`render.render_target()`](/ref/beta/render/#render.render_target:parameters) e [`resource.get_render_target_info()`](/ref/beta/resource/#resource.get_render_target_info:path) per le tabelle complete di parametri e risultati.

## Handle delle texture {#texture-handles}

Le texture in Defold sono rappresentate internamente da un handle, che in sostanza corrisponde a un numero che dovrebbe identificare in modo univoco un oggetto texture in qualsiasi parte del motore. Questo significa che puoi collegare il mondo degli oggetti di gioco a quello del rendering passando questi handle tra il sistema di rendering e uno script di un oggetto di gioco. Per esempio, uno script associato a un oggetto di gioco può creare una texture dinamica e inviarla al sistema di rendering per usarla come texture globale in un comando di disegno.

In un file `.script`:

```lua
local my_texture_resource = resource.create_texture("/my_texture.texture", tparams)
-- note: my_texture_resource is a hash to the resource path, which can't be used as a handle!
local my_texture_handle = resource.get_texture_info(my_texture_resource)
-- my_texture_handle contains information about the texture, such as width, height and so on
-- it does also contain the handle, which is what we are after
msg.post("@render:", "set_texture", { handle = my_texture_handle.handle })
```

In un file `.render_script`:

```lua
function on_message(self, message_id, message)
    if message_id == hash("set_texture") then
        self.my_texture = message.handle
    end
end

function update(self)
    -- bind the custom texture to the draw state
    render.enable_texture(0, self.my_texture)
    -- do drawing..
end
```

::: sidenote
Attualmente non è possibile cambiare la texture a cui una risorsa deve fare riferimento: puoi usare direttamente gli handle in questo modo soltanto nello script di rendering.
:::

## API grafiche supportate {#supported-graphics-apis}
L'API degli script di rendering di Defold traduce le operazioni di rendering nelle seguenti API grafiche:

:[Graphics API](../shared/graphics-api.md)


## Messaggi di sistema {#system-messages}

`"set_view_projection"`
: Questo messaggio viene inviato dai componenti camera che hanno acquisito il focus della camera.

`"window_resized"`
: Il motore invia questo messaggio quando cambiano le dimensioni della finestra. Puoi gestire il messaggio per modificare il rendering quando cambia la dimensione della finestra di destinazione. Sui computer desktop questo significa che la finestra del gioco è stata ridimensionata, mentre sui dispositivi mobili il messaggio viene inviato ogni volta che cambia l'orientamento.

```lua
local MSG_WINDOW_RESIZED =      hash("window_resized")

function on_message(self, message_id, message)
  if message_id == MSG_WINDOW_RESIZED then
    -- The window was resized. message.width and message.height contain the new dimensions.
    ...
  end
end
```

`"draw_line"`
: Disegna una linea di debug. Usala per visualizzare `ray_casts`, vettori e altro. Le linee vengono disegnate con la chiamata a `render.draw_debug3d()`.

```lua
-- draw a white line
local p1 = vmath.vector3(0, 0, 0)
local p2 = vmath.vector3(1000, 1000, 0)
local col = vmath.vector4(1, 1, 1, 1)
msg.post("@render:", "draw_line", { start_point = p1, end_point = p2, color = col } )  
```

`"draw_text"`
: Disegna testo di debug. Usalo per mostrare informazioni di debug. Il testo viene disegnato con il carattere integrato `always_on_top.font`. Il carattere di sistema ha un materiale con il tag `debug_text` e viene disegnato insieme agli altri testi nello script di rendering predefinito.

```lua
-- draw a text message
local pos = vmath.vector3(500, 500, 0)
msg.post("@render:", "draw_text", { text = "Hello world!", position = pos })  
```

Il profilatore visivo, accessibile tramite il messaggio `"toggle_profile"` inviato al socket `@system`, non fa parte del sistema di rendering programmabile. Viene disegnato separatamente dallo script di rendering.


## Chiamate di disegno e raggruppamento {#draw-calls-and-batching}

Una chiamata di disegno è il processo con cui si configura la GPU per disegnare un oggetto sullo schermo usando una texture e un materiale, con eventuali impostazioni aggiuntive. Questo processo richiede solitamente molte risorse, quindi è consigliabile ridurre al minimo il numero di chiamate di disegno. Puoi misurare il numero di chiamate di disegno e il tempo necessario per eseguirle con il [profilatore integrato](/manuals/profiling/).

Defold cerca di raggruppare le operazioni di rendering per ridurre il numero di chiamate di disegno secondo le regole descritte di seguito. Le regole differiscono tra i componenti GUI e tutti gli altri tipi di componenti.


### Regole di raggruppamento per i componenti non GUI {#batch-rules-for-non-gui-components}

Ogni chiamata a `render.draw()` controlla come vengono ordinate le voci corrispondenti con ordinamento nello spazio del mondo. Il valore predefinito è `render.SORT_BACK_TO_FRONT`; usa `render.SORT_FRONT_TO_BACK` per disegnare dagli elementi più vicini a quelli più lontani, oppure `render.SORT_NONE` per mantenere l'ordine di inserimento:

```lua
render.draw(self.opaque_predicate, {
    sort_order = render.SORT_FRONT_TO_BACK
})
render.draw(self.transparent_predicate, {
    sort_order = render.SORT_BACK_TO_FRONT
})
```

L'ordine selezionato determina quali voci sono adiacenti e può quindi influire sul raggruppamento. In questo elenco ordinato, ogni oggetto viene raggruppato nella stessa chiamata di disegno dell'oggetto precedente se soddisfa le seguenti condizioni:

* Appartiene allo stesso proxy di collezione
* È dello stesso tipo di componente (sprite, effetto particellare, tilemap e così via)
* Usa la stessa texture (atlas o sorgente di tile)
* Ha lo stesso materiale
* Ha le stesse costanti dello shader (come la tinta)

Questo significa che, se due componenti sprite nello stesso proxy di collezione sono adiacenti dopo l'ordinamento selezionato e usano la stessa texture, lo stesso materiale e le stesse costanti, vengono raggruppati nella stessa chiamata di disegno.


### Regole di raggruppamento per i componenti GUI {#batch-rules-for-gui-components}

I nodi di un componente GUI vengono disegnati dall'alto verso il basso dell'elenco dei nodi. Ogni nodo dell'elenco viene raggruppato nella stessa chiamata di disegno del nodo precedente se soddisfa le seguenti condizioni:

* È dello stesso tipo (riquadro, testo, settore circolare e così via)
* Usa la stessa texture (atlas o sorgente di tile)
* Ha la stessa modalità di fusione.
* Ha lo stesso carattere (solo per i nodi di testo)
* Ha le stesse impostazioni dello stencil

::: sidenote
I nodi vengono disegnati separatamente per ciascun componente. Questo significa che i nodi di componenti GUI diversi non vengono raggruppati.
:::

La possibilità di organizzare i nodi in gerarchie permette di raggrupparli facilmente in unità gestibili. Le gerarchie possono però interrompere il raggruppamento delle operazioni di rendering se mescoli tipi di nodi diversi. I livelli GUI consentono di raggruppare i nodi GUI in modo più efficace mantenendo le gerarchie dei nodi. Puoi leggere di più sui livelli GUI e su come influiscono sulle chiamate di disegno nel [manuale della GUI](/manuals/gui#layers-and-draw-calls).
