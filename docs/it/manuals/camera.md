---
title: Manuale del componente telecamera
brief: Questo manuale descrive le funzionalità del componente telecamera di Defold.
---

# Telecamere {#cameras}

Una telecamera (camera) in Defold è un componente che modifica il viewport e la proiezione del mondo di gioco. Il componente telecamera definisce una telecamera prospettica o ortografica essenziale che fornisce una matrice di vista e una matrice di proiezione allo script di rendering.

Una telecamera prospettica viene generalmente utilizzata nei giochi 3D, dove la vista della telecamera, le dimensioni e la prospettiva degli oggetti dipendono da un frustum di vista e dalla distanza e dall'angolo di visuale tra la telecamera e gli oggetti nel gioco.

Nei giochi 2D è spesso preferibile eseguire il rendering della scena con una proiezione ortografica. In questo caso la vista della telecamera non è più determinata da un frustum di vista, ma da un parallelepipedo. La proiezione ortografica non è realistica, perché non modifica le dimensioni degli oggetti in base alla loro distanza. Un oggetto distante 1000 unità viene visualizzato con le stesse dimensioni di un oggetto posto proprio davanti alla telecamera.

![proiezioni](images/camera/projections.png)


## Creare una telecamera {#creating-a-camera}

Per creare una telecamera, <kbd>fai clic con il pulsante destro</kbd> su un oggetto di gioco e seleziona <kbd>Add Component ▸ Camera</kbd>. In alternativa, puoi creare un file di componente nella gerarchia del progetto e aggiungerlo all'oggetto di gioco.

![creazione del componente telecamera](images/camera/create.png)

Il componente telecamera ha le seguenti proprietà che definiscono il *frustum* della telecamera:

![impostazioni della telecamera](images/camera/settings.png)

Id
: L'ID del componente

Aspect Ratio
: (**Solo per le telecamere prospettiche**) - Il rapporto tra la larghezza e l'altezza del frustum. 1.0 indica una vista quadrata. 1.33 è adatto a una vista 4:3, come 1024x768. 1.78 è adatto a una vista 16:9. Questa impostazione viene ignorata se *Auto Aspect Ratio* è attiva.

Fov
: (**Solo per le telecamere prospettiche**) - Il campo visivo *verticale* della telecamera, espresso in _radianti_. Più ampio è il campo visivo, maggiore è l'area visibile dalla telecamera.

Near Z
: Il valore Z del piano di clipping vicino.

Far Z
: Il valore Z del piano di clipping lontano.

Auto Aspect Ratio
: (**Solo per le telecamere prospettiche**) - Attiva questa impostazione per consentire alla telecamera di calcolare automaticamente il rapporto d'aspetto.

Orthographic Projection
: Attiva questa impostazione per passare alla proiezione ortografica (vedi sotto).

Orthographic Zoom
: (**Solo per le telecamere ortografiche**) - Un moltiplicatore dello zoom controllato dall'utente (> 1 = ingrandimento, < 1 = riduzione). In modalità `Fixed` corrisponde allo zoom effettivo. Nelle modalità `Auto Fit` e `Auto Cover` viene moltiplicato per lo zoom calcolato automaticamente, consentendo di aggiungere ulteriore zoom senza disattivare il dimensionamento automatico.

Orthographic Mode
: (**Solo per le telecamere ortografiche**) - Controlla come la telecamera ortografica determina lo zoom in relazione alle dimensioni della finestra e alla risoluzione di progetto (i valori in `game.project` → `display.width/height`).
  - `Fixed` (zoom costante): Utilizza il valore corrente di `Orthographic Zoom` così com'è.
  - `Auto Fit` (contenimento): Calcola automaticamente lo zoom affinché l'intera area di progetto rientri nella finestra, poi lo moltiplica per `Orthographic Zoom`. Può mostrare contenuti aggiuntivi ai lati o in alto e in basso.
  - `Auto Cover` (copertura): Calcola automaticamente lo zoom affinché l'area di progetto copra l'intera finestra, poi lo moltiplica per `Orthographic Zoom`. Può tagliare i contenuti ai lati o in alto e in basso.
  Disponibile solo quando `Orthographic Projection` è attiva.


## Usare la telecamera {#using-the-camera}

Tutte le telecamere sono automaticamente abilitate e aggiornate durante ogni fotogramma, e il modulo Lua `camera` è disponibile in tutti i contesti di script. A partire da Defold 1.8.1 non è più necessario abilitare esplicitamente una telecamera inviando un messaggio `acquire_camera_focus` al componente telecamera. I vecchi messaggi di acquisizione e rilascio sono ancora disponibili, ma si consiglia di utilizzare i messaggi `enable` e `disable`, come per qualsiasi altro componente che desideri abilitare o disabilitare:

```lua
msg.post("#camera", "disable")
msg.post("#camera", "enable")
```

Per elencare tutte le telecamere attualmente disponibili, puoi usare `camera.get_cameras()`:

```lua
-- Note: The render calls are only available in a render script.
--       The camera.get_cameras() function can be used anywhere,
--       but render.set_camera can only be used in a render script.

for k,v in pairs(camera.get_cameras()) do
    -- the camera table contains the URLs of all cameras
    render.set_camera(v)
    -- do rendering here - anything rendered here that uses materials with
    -- view and projection matrices specified, will use matrices from the camera.
end
-- to disable a camera, pass in nil (or no arguments at all) to render.set_camera.
-- after this call, all render calls will use the view and projection matrices
-- that are specified on the render context (render.set_view and render.set_projection)
render.set_camera()
```

Il modulo di scripting `camera` offre diverse funzioni per controllare la telecamera. Di seguito sono riportate solo alcune delle funzioni disponibili; per conoscerle tutte, consulta la [documentazione API](/ref/camera/)).

```lua
camera.get_aspect_ratio(camera) -- get aspect ratio
camera.get_far_z(camera) -- get far z
camera.get_fov(camera) -- get field of view
camera.get_orthographic_mode(camera) -- get orthographic mode (one of camera.ORTHO_MODE_*)
camera.get_orthographic_zoom(camera) -- get the user-controlled zoom multiplier
camera.get_orthographic_auto_zoom(camera) -- get the automatically calculated zoom
camera.set_aspect_ratio(camera, ratio) -- set aspect ratio
camera.set_far_z(camera, far_z) -- set far z
camera.set_near_z(camera, near_z) -- set near z
camera.set_orthographic_mode(camera, camera.ORTHO_MODE_AUTO_FIT) -- set orthographic mode
... And so forth
```

Una telecamera è identificata da un URL, che rappresenta il percorso completo del componente nella scena e comprende la collezione, l'oggetto di gioco a cui appartiene e l'ID del componente. In questo esempio, useresti l'URL `/go#camera` per identificare il componente telecamera dall'interno della stessa collezione e `main:/go#camera` per accedere a una telecamera da una collezione diversa o dallo script di rendering.

![creazione del componente telecamera](images/camera/create.png)

```lua
-- Accessing a camera from a script in the same collection:
camera.get_fov("/go#camera")

-- Accessing a camera from a script in a different collection:
camera.get_fov("main:/go#camera")

-- Accessing a camera from the render script:
render.set_camera("main:/go#camera")
```

A ogni fotogramma, il componente telecamera che detiene il focus della telecamera invia un messaggio `set_view_projection` al socket `@render`:

```lua
-- builtins/render/default.render_script
--
function on_message(self, message_id, message)
    if message_id == hash("set_view_projection") then
        self.view = message.view                    -- [1]
        self.projection = message.projection
    end
end
```
1. Il messaggio inviato dal componente telecamera include una matrice di vista e una matrice di proiezione.

Il componente telecamera fornisce allo script di rendering una matrice di proiezione prospettica oppure ortografica, a seconda della proprietà *Orthographic Projection* della telecamera. La matrice di proiezione tiene conto anche dei piani di clipping vicino e lontano definiti, del campo visivo e delle impostazioni del rapporto d'aspetto della telecamera.

La matrice di vista fornita dalla telecamera ne definisce la posizione e l'orientamento. Una telecamera con *Orthographic Projection* centra la vista sulla posizione dell'oggetto di gioco a cui è collegata, mentre una telecamera con *Perspective Projection* posiziona l'angolo inferiore sinistro della vista sull'oggetto di gioco a cui è collegata.


### Script di rendering {#render-script}

Quando usi lo script di rendering predefinito, Defold imposta automaticamente l'ultima telecamera abilitata come telecamera da utilizzare per il rendering. Prima di questa modifica, uno script del progetto doveva inviare esplicitamente il messaggio `use_camera_projection` al renderer per indicargli di utilizzare la vista e la proiezione dei componenti telecamera. Questo passaggio non è più necessario, ma resta possibile per garantire la retrocompatibilità.

In alternativa, puoi impostare una telecamera specifica da utilizzare per il rendering in uno script di rendering. Può essere utile quando devi controllare con maggiore precisione quale telecamera utilizzare per il rendering, per esempio in un gioco multigiocatore.

```lua
-- render.set_camera will automatically use the view and projection matrices
-- for any rendering happening until render.set_camera() is called.
render.set_camera("main:/my_go#camera")
```

Per verificare se una telecamera è attiva, puoi utilizzare la funzione `get_enabled` dell'[API della telecamera](https://defold.com/ref/alpha/camera/#camera.get_enabled:camera):

```lua
if camera.get_enabled("main:/my_go#camera") then
    -- camera is enabled, use it for rendering!
    render.set_camera("main:/my_go#camera")
end
```

::: sidenote
Per usare la funzione `set_camera` insieme all'esclusione degli oggetti esterni al frustum, devi passare questa impostazione come opzione alla funzione:
`render.set_camera("main:/my_go#camera", {use_frustum = true})`
:::

### Spostare la telecamera {#panning-the-camera}

Puoi spostare la telecamera nel mondo di gioco muovendo l'oggetto di gioco a cui è collegato il componente telecamera. Il componente telecamera invia automaticamente una matrice di vista aggiornata in base alla posizione corrente della telecamera sugli assi x e y.

### Regolare lo zoom della telecamera {#zooming-the-camera}

Con una telecamera prospettica puoi ingrandire e ridurre la vista spostando lungo l'asse z l'oggetto di gioco a cui è collegata la telecamera. Il componente telecamera invia automaticamente una matrice di vista aggiornata in base alla posizione z corrente della telecamera.

Con una telecamera ortografica puoi ingrandire e ridurre la vista modificando la proprietà *Orthographic Zoom* della telecamera, nell'editor oppure durante l'esecuzione:

```lua
-- In Fixed mode, this is the effective zoom.
go.set("#camera", "orthographic_zoom", 2)
```

Nelle modalità `Auto Fit` e `Auto Cover`, *Orthographic Zoom* viene applicato allo zoom calcolato automaticamente e non viene ignorato. Per esempio, imposta *Orthographic Mode* su `Auto Fit` e *Orthographic Zoom* su `1.25` nell'editor per adattare l'area di progetto alla finestra e poi ingrandirla di un ulteriore 25%. La configurazione equivalente durante l'esecuzione è:

```lua
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)
go.set("#camera", "orthographic_zoom", 1.25)

local auto_zoom = camera.get_orthographic_auto_zoom("#camera")
local zoom_multiplier = camera.get_orthographic_zoom("#camera")
local effective_zoom = auto_zoom * zoom_multiplier
```

`camera.get_orthographic_auto_zoom()` restituisce lo zoom calcolato a partire dalle dimensioni correnti della finestra e del progetto nelle modalità `Auto Fit` e `Auto Cover`. Restituisce `1.0` in modalità `Fixed`. Lo stesso valore è disponibile tramite la proprietà di sola lettura `orthographic_auto_zoom` del componente:

```lua
local auto_zoom = go.get("#camera", "orthographic_auto_zoom")
```

Quando usi una telecamera ortografica, puoi anche cambiare il modo in cui viene determinato lo zoom tramite l'impostazione `Orthographic Mode` o tramite script:

```lua
-- get current mode (one of camera.ORTHO_MODE_FIXED, _AUTO_FIT, _AUTO_COVER)
local mode = camera.get_orthographic_mode("#camera")

-- switch to auto-fit (contain) to always keep the full design area visible
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)

-- switch to auto-cover to ensure the design area covers the window
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_COVER)

-- switch to fixed mode to use orthographic_zoom without automatic sizing
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_FIXED)
```

### Zoom adattivo {#adaptive-zoom}

Il principio dello zoom adattivo consiste nel regolare il valore di zoom della telecamera quando la risoluzione dello schermo cambia rispetto alla risoluzione iniziale impostata in *game.project*.

Due approcci comuni allo zoom adattivo sono:

1. Zoom massimo - Calcolare un valore di zoom tale che il contenuto coperto dalla risoluzione iniziale in *game.project* riempia lo schermo e ne superi i bordi, nascondendo eventualmente parte del contenuto ai lati o in alto e in basso.
2. Zoom minimo - Calcolare un valore di zoom tale che il contenuto coperto dalla risoluzione iniziale in *game.project* sia completamente contenuto entro i bordi dello schermo, mostrando eventualmente contenuti aggiuntivi ai lati o in alto e in basso.

Esempio:

```lua
local DISPLAY_WIDTH = sys.get_config_int("display.width")
local DISPLAY_HEIGHT = sys.get_config_int("display.height")

function init(self)
    local initial_zoom = go.get("#camera", "orthographic_zoom")
    local display_scale = window.get_display_scale()
    window.set_listener(function(self, event, data)
        if event == window.WINDOW_EVENT_RESIZED then
            local window_width = data.width
            local window_height = data.height
            local design_width = DISPLAY_WIDTH / initial_zoom
            local design_height = DISPLAY_HEIGHT / initial_zoom

            -- max zoom: ensure that the initial design dimensions will fill and expand beyond the screen bounds
            local zoom = math.max(window_width / design_width, window_height / design_height) / display_scale

            -- min zoom: ensure that the initial design dimensions will shrink and be contained within the screen bounds
            --local zoom = math.min(window_width / design_width, window_height / design_height) / display_scale
            
            go.set("#camera", "orthographic_zoom", zoom)
        end
    end)
end
```

Puoi trovare un esempio completo di zoom adattivo in [questo progetto di esempio](https://github.com/defold/sample-adaptive-zoom).

Nota: con una telecamera ortografica puoi ora ottenere il comportamento di contenimento o copertura senza codice personalizzato, impostando `Orthographic Mode` su `Auto Fit` (contenimento) o `Auto Cover` (copertura). In queste modalità lo zoom calcolato a partire dalle dimensioni della finestra e dalla risoluzione di progetto viene moltiplicato per `Orthographic Zoom`.


### Seguire un oggetto di gioco {#following-a-game-object}

Puoi fare in modo che la telecamera segua un oggetto di gioco impostando l'oggetto di gioco a cui è collegato il componente telecamera come figlio dell'oggetto di gioco da seguire:

![inseguimento di un oggetto di gioco](images/camera/follow.png)

In alternativa, puoi aggiornare a ogni fotogramma la posizione dell'oggetto di gioco a cui è collegato il componente telecamera, mentre l'oggetto di gioco da seguire si sposta.

### Convertire tra coordinate dello schermo e del mondo {#converting-mouse-to-world-coordinates}

Quando una telecamera è stata spostata, ha cambiato zoom o ha modificato la propria proiezione, le coordinate di input non corrispondono più direttamente alle coordinate del mondo. Usa le funzioni di conversione della telecamera con `action.screen_x` e `action.screen_y`. Se l'URL facoltativo della telecamera viene omesso, viene utilizzata l'ultima telecamera abilitata.

Per una telecamera ortografica, [`camera.screen_xy_to_world()`](/ref/camera/#camera.screen_xy_to_world:x-y-[camera]) restituisce il punto nello spazio del mondo sul piano vicino della telecamera corrispondente a un pixel dello schermo:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local world_position = camera.screen_xy_to_world(
            action.screen_x, action.screen_y, "#camera")
        go.set_position(world_position, "/marker")
    end
end
```

Per una telecamera prospettica, [`camera.screen_to_world()`](/ref/camera/#camera.screen_to_world:pos-[camera]) accetta un `vector3` la cui componente Z rappresenta la profondità di vista in unità del mondo misurata dal piano della telecamera:

```lua
local depth = 10
local world_position = camera.screen_to_world(
    vmath.vector3(action.screen_x, action.screen_y, depth), "#camera")
```

[`camera.world_to_screen()`](/ref/camera/#camera.world_to_screen:world_pos-[camera]) esegue la conversione inversa. Restituisce X e Y in pixel dello schermo e Z secondo la stessa convenzione per la profondità di vista, quindi il risultato può essere passato nuovamente a `camera.screen_to_world()`:

```lua
-- Update the cached world transform first if the object moved this frame.
go.update_world_transform("/marker")
local world_position = go.get_world_position("/marker")
local screen_position = camera.world_to_screen(world_position, "#camera")
```

Visita la [pagina degli esempi](https://defold.com/examples/render/screen_to_world/) per vedere la conversione delle coordinate in azione. È disponibile anche un [progetto di esempio](https://github.com/defold/sample-screen-to-world-coordinates/) che mostra le stesse API.

::: sidenote
Le [soluzioni per telecamere di terze parti menzionate in questo manuale](/manuals/camera/#third-party-camera-solutions) forniscono funzioni per convertire da e verso le coordinate dello schermo.
:::

## Modifiche durante l'esecuzione {#runtime-manipulation}
Puoi controllare le telecamere durante l'esecuzione tramite diversi messaggi e proprietà (consulta la [documentazione API per l'utilizzo](/ref/camera/)).

Una telecamera ha diverse proprietà che puoi modificare usando `go.get()` e `go.set()`:

`fov`
: Il campo visivo della telecamera (`number`).

`near_z`
: Il valore Z vicino della telecamera (`number`).

`far_z`
: Il valore Z lontano della telecamera (`number`).

`orthographic_zoom`
: Il moltiplicatore dello zoom della telecamera ortografica controllato dall'utente. Nelle modalità `Auto Fit` e `Auto Cover` viene moltiplicato per `orthographic_auto_zoom`. (`number`).

`orthographic_auto_zoom`
: Lo zoom ortografico calcolato per le modalità `Auto Fit` e `Auto Cover`, oppure `1.0` in modalità `Fixed`. SOLA LETTURA. (`number`).

`aspect_ratio`
: Il rapporto tra la larghezza e l'altezza del frustum. Viene utilizzato per calcolare la proiezione di una telecamera prospettica. (`number`).

`view`
: La matrice di vista calcolata della telecamera. SOLA LETTURA. (`matrix4`).

`projection`
: La matrice di proiezione calcolata della telecamera. SOLA LETTURA. (`matrix4`).


## Soluzioni per telecamere di terze parti {#third-party-camera-solutions}

Esistono soluzioni per telecamere realizzate dalla comunità che implementano funzionalità comuni come lo scuotimento dello schermo, l'inseguimento degli oggetti di gioco, la conversione dalle coordinate dello schermo a quelle del mondo e molto altro. Puoi scaricarle dall'Asset Portal di Defold:

- [Orthographic camera](https://defold.com/assets/orthographic/) (solo 2D) di Björn Ritzl.
- [Defold Rendy](https://defold.com/assets/defold-rendy/) (2D e 3D) di Klayton Kowalski.
