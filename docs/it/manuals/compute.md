---
title: Manuale dei programmi di calcolo in Defold
brief: Questo manuale spiega come lavorare con i programmi di calcolo, le costanti degli shader e i campionatori.
---

# Programmi di calcolo {#compute-programs}

::: sidenote
Il supporto degli shader di calcolo (compute shader) in Defold è attualmente in *anteprima tecnica*.
Questo significa che alcune funzionalità sono ancora assenti e che l'API potrebbe cambiare in futuro.
:::

Gli shader di calcolo sono uno strumento potente per eseguire calcoli di uso generale sulla GPU. Ti permettono di sfruttare la capacità di elaborazione parallela della GPU per attività come simulazioni fisiche, elaborazione delle immagini e molto altro. Uno shader di calcolo opera sui dati memorizzati in buffer o texture, eseguendo operazioni in parallelo su numerosi thread della GPU. È questo parallelismo a rendere gli shader di calcolo così potenti per i calcoli intensivi.

* Per ulteriori informazioni sulla pipeline di rendering, consulta la [documentazione sul rendering](/manuals/render).
* Per una spiegazione approfondita dei programmi shader, consulta la [documentazione sugli shader](/manuals/shader).

## Che cosa posso fare con gli shader di calcolo? {#what-can-i-do-with-compute-shaders}

Poiché gli shader di calcolo sono pensati per eseguire calcoli generici, non ci sono veri limiti a ciò che puoi fare con essi. Ecco alcuni esempi degli usi tipici degli shader di calcolo:

Elaborazione delle immagini
  - Filtraggio delle immagini: applicare sfocature, rilevamento dei bordi, un filtro di nitidezza e così via.
  - Correzione cromatica: regolare lo spazio colore di un'immagine.

Fisica
  - Sistemi particellari: simulare un gran numero di particelle per effetti come fumo, fuoco e fluidodinamica.
  - Fisica dei corpi deformabili: simulare oggetti deformabili come tessuti e gelatina.
  - Esclusione degli elementi non visibili: per occlusione (occlusion culling), rispetto al frustum (frustum culling)

Generazione procedurale
  - Generazione del terreno: creare terreni dettagliati tramite funzioni di rumore.
  - Vegetazione e fogliame: creare piante e alberi generati proceduralmente.

Effetti di rendering
  - Illuminazione globale: simulare un'illuminazione realistica approssimando il modo in cui la luce rimbalza nella scena.
  - Voxelizzazione: creare una griglia di voxel 3D a partire dai dati di una mesh.

## Come funzionano gli shader di calcolo? {#how-does-compute-shaders-work}

A grandi linee, gli shader di calcolo funzionano suddividendo un'attività in molte attività più piccole che possono essere eseguite contemporaneamente. Questo è possibile grazie ai concetti di gruppi di lavoro (`work groups`) e invocazioni (`invocations`):

Gruppi di lavoro
: Lo shader di calcolo opera su una griglia di gruppi di lavoro (`work groups`). Ogni gruppo di lavoro contiene un numero fisso di invocazioni (o thread). La dimensione dei gruppi di lavoro e il numero di invocazioni sono definiti nel codice dello shader.

Invocazioni
: Ogni invocazione (o thread) esegue il programma dello shader di calcolo. Le invocazioni all'interno di un gruppo di lavoro possono condividere dati tramite una memoria condivisa, che consente loro di comunicare e sincronizzarsi in modo efficiente.

La GPU esegue lo shader di calcolo avviando molte invocazioni in parallelo su più gruppi di lavoro, offrendo una notevole potenza di calcolo per le attività adatte.

## Creare un programma di calcolo {#creating-a-compute-program}

Per creare un programma di calcolo, <kbd>fai clic con il pulsante destro</kbd> su una cartella di destinazione nel browser *Assets* e seleziona <kbd>New... ▸ Compute</kbd>. (Puoi anche selezionare <kbd>File ▸ New...</kbd> dal menu e poi selezionare <kbd>Compute</kbd>). Assegna un nome al nuovo file di calcolo e premi <kbd>Ok</kbd>.

![File di calcolo](images/compute/compute_file.png)

Il nuovo programma di calcolo si aprirà nel *Compute Editor*.

![Editor dei programmi di calcolo](images/compute/compute.png)

Il file di calcolo contiene le seguenti informazioni:

Compute Program
: Il file del programma dello shader di calcolo (*`.cp`*) da usare. Lo shader opera su "elementi di lavoro astratti", quindi non esiste una definizione fissa dei tipi di dati di input e output. Spetta al programmatore definire che cosa deve produrre lo shader di calcolo.

Constants
: Le variabili uniform da passare al programma dello shader di calcolo. Più avanti trovi un elenco delle costanti disponibili.

Samplers
: Puoi configurare facoltativamente campionatori specifici nel file dei materiali. Aggiungi un campionatore, assegnagli il nome usato nel programma shader e configura le impostazioni di ripetizione e filtraggio come preferisci.


## Usare il programma di calcolo in Defold {#using-the-compute-program-in-defold}

A differenza dei materiali, i programmi di calcolo non sono assegnati ad alcun componente e non fanno parte del normale flusso di rendering. Un programma di calcolo deve essere avviato (`dispatched`) in uno script di rendering per eseguire qualsiasi operazione. Prima di avviarlo, però, devi assicurarti che lo script di rendering contenga un riferimento al programma di calcolo. Attualmente, l'unico modo per rendere il programma di calcolo disponibile a uno script di rendering è aggiungerlo al file .render che contiene il riferimento allo script di rendering:

![File di rendering con un programma di calcolo](images/compute/compute_render_file.png)

Per usare il programma di calcolo, devi prima associarlo al contesto di rendering. Questa operazione avviene nello stesso modo dei materiali:

```lua
render.set_compute("my_compute")
-- Do compute work here, call render.set_compute() to unbind
render.set_compute()
```

Le costanti di calcolo vengono applicate automaticamente quando il programma viene avviato, ma non è possibile associare risorse di input o output (texture, buffer e così via) a un programma di calcolo dall'editor. Devi invece farlo tramite gli script di rendering:

```lua
render.enable_texture("blur_render_target", "tex_blur")
render.enable_texture(self.storage_texture, "tex_storage")
```

Per eseguire il programma nello spazio di lavoro che hai definito, devi avviare il programma:

```lua
render.dispatch_compute(128, 128, 1)
-- dispatch_compute also accepts an options table as the last argument
-- you can use this argument table to pass in render constants to the dispatch call
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### Scrivere dati dai programmi di calcolo {#writing-data-from-compute-programs}

Attualmente, per generare qualsiasi tipo di output da un programma di calcolo puoi usare soltanto le texture di archiviazione (`storage textures`). Una texture di archiviazione è simile a una "texture normale", ma supporta più funzionalità e opzioni di configurazione. Come suggerisce il nome, le texture di archiviazione possono essere usate come buffer generici da cui leggere e in cui scrivere dati tramite un programma di calcolo. Puoi poi associare lo stesso buffer a un altro programma shader per la lettura.

Per creare una texture di archiviazione in Defold, devi operare da un normale file `.script`. Gli script di rendering non offrono questa funzionalità, perché le texture dinamiche devono essere create tramite l'API `resource`, disponibile soltanto nei normali file `.script`.

```lua
-- In a .script file:
function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- get the texture handle from the resource
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- notify the renderer of the backing texture, so it can be bound with render.enable_texture
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## Mettere tutto insieme {#putting-it-all-together}

### Programma shader {#shader-program}

```glsl
// compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// specify the input resources
uniform vec4 color;
uniform sampler2D texture_in;

// specify the output image
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // This isn't a particularly interesting shader, but it demonstrates
    // how to read from a texture and constant buffer and write to a storage texture

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // Write the output value to the storage texture
    imageStore(texture_out, tex_coord, output_value);
}
```

### Componente script {#script-component}
```lua
-- In a .script file

-- Here we specify the input texture that we later will bind to the
-- compute program. We can assign this texture to a model component,
-- or enable it to the render context in the render script.
go.property("texture_in", resource.texture())

function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    local textures = {
        texture_in = resource.get_texture_info(self.texture_in).handle,
        texture_out = resource.get_texture_info(t_backing).handle
    }

    -- notify the renderer of the input and output textures
    msg.post("@render:", "set_backing_texture", textures)
end
```

### Script di rendering {#render-script}
```lua
-- respond to the message "set_backing_texture"
-- to set the backing texture for the compute program
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- We can bind textures to specific named constants
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- Dispatch the compute program as many times as we have pixels.
    -- This constitutes our "working group". The shader will be invoked
    -- 128 x 128 x 1 times, or once per pixel.
    render.dispatch_compute(128, 128, 1)
    -- when we are done with the compute program, we need to unbind it
    render.set_compute()
end
```

## Compatibilità {#compatibility}

Defold attualmente supporta gli shader di calcolo nei seguenti adattatori grafici:

- Vulkan
- Metal (tramite MoltenVK)
- OpenGL 4.3+
- OpenGL ES 3.1+

Usa `graphics.get_adapter_info()` per verificare se l'adattatore grafico attivo supporta gli shader di calcolo. Il campo `features` contiene un array delle costanti delle funzionalità del contesto supportate dall'adattatore:

```lua
local function has_context_feature(feature)
    local adapter_info = graphics.get_adapter_info()
    for _, supported_feature in ipairs(adapter_info.features) do
        if supported_feature == feature then
            return true
        end
    end
    return false
end

local compute_shaders_supported = has_context_feature(
    graphics.CONTEXT_FEATURE_COMPUTE_SHADER
)
```

L'array include soltanto le funzionalità supportate; non è una tabella con le costanti delle funzionalità come chiavi. Esegui sempre questa verifica prima di usare gli shader di calcolo quando il gioco può essere eseguito con adattatori grafici diversi o su dispositivi con un supporto dei driver variabile. Il supporto di OpenGL e OpenGL ES dipende dalla versione dell'API e dal driver. Vulkan e Metal tramite MoltenVK supportano gli shader di calcolo dalla versione 1.0. Usa un [manifest dell'applicazione](/manuals/app-manifest) per selezionare Vulkan sulle piattaforme in cui non è già il backend grafico predefinito.
