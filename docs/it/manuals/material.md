---
title: Manuale dei materiali di Defold
brief: Questo manuale spiega come lavorare con i materiali, le costanti degli shader e i campionatori.
---

# Materiali {#materials}

I materiali definiscono come deve essere renderizzato un componente grafico (uno sprite, una mappa di tasselli, un font, un nodo GUI, un modello ecc.).

Un materiale contiene _tag_, informazioni usate dalla pipeline di rendering per selezionare gli oggetti da renderizzare. Contiene inoltre riferimenti a _programmi shader_, che vengono compilati tramite il driver grafico disponibile, caricati sull'hardware grafico ed eseguiti quando il componente viene renderizzato a ogni fotogramma.

* Per ulteriori informazioni sulla pipeline di rendering, consulta la [documentazione sul rendering](/manuals/render).
* Per una spiegazione approfondita dei programmi shader, consulta la [documentazione sugli shader](/manuals/shader).

## Creare un materiale {#creating-a-material}

Per creare un materiale, <kbd>fai clic con il pulsante destro</kbd> su una cartella di destinazione nel browser *Assets* e seleziona <kbd>New... ▸ Material</kbd>. (Puoi anche selezionare <kbd>File ▸ New...</kbd> dal menu e poi selezionare <kbd>Material</kbd>). Assegna un nome al nuovo file del materiale e premi <kbd>Ok</kbd>.

![File del materiale](images/materials/material_file.png)

Il nuovo materiale si aprirà nel *Material Editor*.

![Editor dei materiali](images/materials/material.png)

Il file del materiale contiene le seguenti informazioni:

Name
: L'identità del materiale. Questo nome viene usato per elencare il materiale nella risorsa *Render* e includerlo nella build. Il nome viene usato anche nella funzione dell'API di rendering `render.enable_material()`. Il nome deve essere univoco.

Vertex Program
: Il file del programma vertex shader (*`.vp`*) da usare per il rendering con il materiale. Il programma vertex shader viene eseguito sulla GPU per ciascun vertice delle primitive di un componente. Calcola la posizione sullo schermo di ogni vertice e può anche produrre variabili "varying", che vengono interpolate e passate al fragment shader.

Fragment Program
: Il file del programma fragment shader (*`.fp`*) da usare per il rendering con il materiale. Il programma viene eseguito sulla GPU per ciascun frammento (pixel) di una primitiva e determina il colore di ogni frammento. In genere lo fa consultando le texture ed eseguendo calcoli basati sulle variabili di input (variabili varying o costanti).

Vertex Constants
: Variabili uniform da passare al programma vertex shader. Di seguito trovi l'elenco delle costanti disponibili.

Fragment Constants
: Variabili uniform da passare al programma fragment shader. Di seguito trovi l'elenco delle costanti disponibili.

Samplers
: Puoi configurare campionatori specifici nel file del materiale. Aggiungi un campionatore, assegnagli il nome usato nel programma shader e configura le impostazioni di ripetizione e filtraggio come preferisci.

Tags
: I tag associati al materiale. I tag sono rappresentati nel motore come una _maschera di bit_, usata da [`render.predicate()`](/ref/render#render.predicate) per raggruppare i componenti da disegnare insieme. Per sapere come fare, consulta la [documentazione sul rendering](/manuals/render). Il numero massimo di tag utilizzabili in un progetto è 32.

## Attributi {#attributes}

Gli attributi degli shader (chiamati anche flussi di vertici o attributi dei vertici) definiscono come la GPU recupera i vertici dalla memoria per renderizzare la geometria. Il vertex shader specifica un insieme di flussi tramite la parola chiave `attribute` e, nella maggior parte dei casi, Defold produce e associa automaticamente i dati in base ai nomi dei flussi. In alcuni casi, però, potresti voler passare più dati per vertice per ottenere un effetto specifico che il motore non produce. Un attributo dei vertici può essere configurato con i seguenti campi:

Name
: Il nome dell'attributo. Come per le costanti degli shader, la configurazione dell'attributo viene usata soltanto se corrisponde a un attributo specificato nel vertex shader.

Semantic type
: Un tipo semantico indica *che cosa* rappresenta l'attributo e/o *come* deve essere mostrato nell'editor. Per esempio, specificando un attributo con `SEMANTIC_TYPE_COLOR`, nell'editor verrà mostrato un selettore di colore, mentre i dati verranno comunque passati dal motore allo shader senza modifiche.

  - `SEMANTIC_TYPE_NONE` Il tipo semantico predefinito. Non ha altri effetti sull'attributo se non passare i dati del materiale per l'attributo direttamente al buffer dei vertici (predefinito)
  - `SEMANTIC_TYPE_POSITION` Produce dati di posizione per ciascun vertice dell'attributo. Può essere usato insieme allo spazio delle coordinate per indicare al motore come calcolare le posizioni
  - `SEMANTIC_TYPE_TEXCOORD` Produce coordinate di texture per ciascun vertice dell'attributo
  - `SEMANTIC_TYPE_PAGE_INDEX` Produce indici di pagina per ciascun vertice dell'attributo
  - `SEMANTIC_TYPE_COLOR` Influisce sul modo in cui l'editor interpreta l'attributo. Se un attributo è configurato con una semantica di colore, nell'ispettore viene mostrato un selettore di colore
  - `SEMANTIC_TYPE_NORMAL` Produce dati delle normali per ciascun vertice dell'attributo
  - `SEMANTIC_TYPE_TANGENT` Produce dati delle tangenti per ciascun vertice dell'attributo
  - `SEMANTIC_TYPE_WORLD_MATRIX` Produce dati della matrice del mondo per ciascun vertice dell'attributo
  - `SEMANTIC_TYPE_NORMAL_MATRIX` Produce dati della matrice delle normali per ciascun vertice dell'attributo
  - `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D` Produce una matrice 3x3 di trasformazione della texture per ciascun vertice dell'attributo. Per i componenti particellari, il motore fornisce una matrice che trasforma le coordinate nello spazio dell'atlas per la proprietà immagine del componente. Per i componenti sprite, il motore fornisce una matrice per ogni immagine usata dal componente (quando si usano più texture). Per i componenti modello viene fornita una matrice identità.

Data type
: Il tipo di dati usato per memorizzare i dati dell'attributo.

  - `TYPE_BYTE` Valori byte a 8 bit con segno
  - `TYPE_UNSIGNED_BYTE` Valori byte a 8 bit senza segno
  - `TYPE_SHORT` Valori short a 16 bit con segno
  - `TYPE_UNSIGNED_SHORT` Valori short a 16 bit senza segno
  - `TYPE_INT` Valori interi con segno
  - `TYPE_UNSIGNED_INT` Valori interi senza segno
  - `TYPE_FLOAT` Valori in virgola mobile (predefinito)

Normalize
: Se attivo, i valori dell'attributo verranno normalizzati dal driver della GPU. Può essere utile quando non serve la massima precisione, ma vuoi eseguire un calcolo senza conoscere i limiti specifici. Per esempio, per un vettore di colore in genere bastano valori byte nell'intervallo 0..255, che nello shader vengono comunque trattati come valori nell'intervallo 0..1.

Coordinate space
: Alcuni tipi semantici permettono di fornire dati in spazi di coordinate diversi. Per implementare un effetto billboard con gli sprite, in genere servono sia un attributo di posizione nello spazio locale sia una posizione completamente trasformata nello spazio del mondo, così da rendere il raggruppamento delle chiamate di disegno il più efficace possibile.

Vector type
: Il tipo di vettore dell'attributo.

  - `VECTOR_TYPE_SCALAR` Un singolo valore scalare
  - `VECTOR_TYPE_VEC2` Vettore 2D
  - `VECTOR_TYPE_VEC3` Vettore 3D
  - `VECTOR_TYPE_VEC4` Vettore 4D (predefinito)
  - `VECTOR_TYPE_MAT2` Matrice 2D
  - `VECTOR_TYPE_MAT3` Matrice 3D
  - `VECTOR_TYPE_MAT4` Matrice 4D

Step function
: Specifica come passare i dati dell'attributo alla funzione del vertex shader. È rilevante soltanto per l'instancing.

  - `Vertex` Una volta per vertice; per esempio, un attributo di posizione viene in genere passato alla funzione del vertex shader per ciascun vertice della mesh (predefinito)
  - `Instance` Una volta per istanza; per esempio, un attributo della matrice del mondo viene in genere passato alla funzione del vertex shader una volta per istanza

Value
: Il valore dell'attributo. I valori degli attributi possono essere sovrascritti per ciascun componente; altrimenti, questo viene usato come valore predefinito dell'attributo dei vertici. Nota: per gli attributi *predefiniti* (posizione, coordinate di texture e indici di pagina), il valore viene ignorato.

::: sidenote
Gli attributi personalizzati possono anche ridurre l'occupazione di memoria sia sulla CPU sia sulla GPU, riconfigurando i flussi affinché usino un tipo di dati più piccolo o un numero di elementi diverso.
:::

### Semantica predefinita degli attributi {#default-attribute-semantics}

Durante l'esecuzione, il sistema dei materiali assegna automaticamente un tipo semantico predefinito in base al nome dell'attributo, per il seguente insieme di nomi:

  - `position` - tipo semantico: `SEMANTIC_TYPE_POSITION`
  - `texcoord0` - tipo semantico: `SEMANTIC_TYPE_TEXCOORD`
  - `texcoord1` - tipo semantico: `SEMANTIC_TYPE_TEXCOORD`
  - `page_index` - tipo semantico: `SEMANTIC_TYPE_PAGE_INDEX`
  - `color` - tipo semantico: `SEMANTIC_TYPE_COLOR`
  - `normal` - tipo semantico: `SEMANTIC_TYPE_NORMAL`
  - `tangent` - tipo semantico: `SEMANTIC_TYPE_TANGENT`
  - `mtx_world` - tipo semantico: `SEMANTIC_TYPE_WORLD_MATRIX`
  - `mtx_normal` - tipo semantico: `SEMANTIC_TYPE_NORMAL_MATRIX`
  - `mtx_texture_transform_2d` - tipo semantico: `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D`

Se il materiale contiene voci per questi attributi, il tipo semantico predefinito verrà sostituito con quello configurato nell'editor dei materiali.

### Impostare i dati degli attributi dei vertici personalizzati {#setting-custom-vertex-attribute-data}

Come per le costanti degli shader definite dall'utente, puoi aggiornare gli attributi dei vertici durante l'esecuzione chiamando `go.get`, `go.set` e `go.animate`:

![Attributo personalizzato del materiale](images/materials/set_custom_attribute.png)

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

L'aggiornamento degli attributi dei vertici richiede però alcune accortezze: la possibilità che un componente usi il valore dipende dal tipo semantico dell'attributo. Per esempio, un componente sprite supporta `SEMANTIC_TYPE_POSITION`; se aggiorni un attributo con questo tipo semantico, il componente ignora il valore sovrascritto, perché il tipo semantico impone che i dati siano sempre ricavati dalla posizione dello sprite.

Anche i componenti modello espongono gli attributi personalizzati dei materiali tramite `go.get()`, `go.set()` e `go.animate()`. Per esempio, dopo aver definito un attributo chiamato `my_attribute` nel materiale del modello:

```lua
go.set("#model", "my_attribute", vmath.vector4(1, 0, 0, 1))
go.animate("#model", "my_attribute", go.PLAYBACK_LOOP_PINGPONG,
    vmath.vector4(0, 1, 0, 1), go.EASING_LINEAR, 2)
```

Al momento, in un modello con più mesh, soltanto la prima mesh può essere gestita in questo modo. L'aggiornamento di un attributo per vertice che non usa l'instancing può inoltre ricostruire e caricare una quantità di dati dei vertici proporzionale alle dimensioni della mesh; perciò, aggiornamenti frequenti possono essere costosi per mesh di grandi dimensioni.

Se un attributo dei vertici è uno scalare o un tipo di vettore diverso da `Vec4`, puoi comunque impostarne i dati tramite `go.set`:

```lua
-- The last two components in the vec4 will not be used!
go.set("#sprite", "sprite_position_2d", vmath.vector4(my_x,my_y,0,0))
go.animate("#sprite", "sprite_position_2d", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,2,0,0), go.EASING_LINEAR, 2)
```

Lo stesso vale per gli attributi matrice: se l'attributo è un tipo di matrice diverso da `Mat4`, puoi comunque impostarne i dati tramite `go.set`.

### Esempi di utilizzo degli attributi dei vertici personalizzati {#examples-of-using-custom-vertex-attributes}

Uso di un attributo di trasformazione della texture per convertire le coordinate UV nello spazio dell'atlas:

```glsl
#version 140

in vec3 position;
in vec4 texcoord0;
in mat3 texture_transform_2d;

out vec2 var_texcoord0;

void main()
{
  // Extract position from the transform
  vec2 atlas_pos = texture_transform_2d[2].xy;
  // Extract the scale from the transform
  vec2 atlas_size = vec2(
      length(texture_transform_2d[0].xy),
      length(texture_transform_2d[1].xy)
  );
  // convert to local UV (0..1)
  vec2 localUV = (texcoord0 - atlas_pos) / atlas_size;

  // Alternatively, if the UV coordinates already are in the 0..1 range,
  // you can transform into atlas space directly by multiplying the transform:
  vec2 transformedUv = texture_transform_2d * texcoord0;

  // Pass the value into the fragment shader
  var_texcoord0 = localUV;

  // ... rest of vertex shader
}
```

### Instancing

L'instancing è una tecnica che permette di disegnare in modo efficiente più copie dello stesso oggetto in una scena. Invece di creare una copia separata dell'oggetto ogni volta che viene usato, l'instancing consente al motore grafico di creare un solo oggetto e riutilizzarlo più volte. Per esempio, in un gioco con una grande foresta, invece di creare un modello separato per ciascun albero, l'instancing permette di creare un solo modello di albero e collocarlo centinaia o migliaia di volte con posizioni e scale diverse. La foresta può così essere renderizzata con una sola chiamata di disegno invece che con una chiamata separata per ciascun albero.

::: sidenote
L'instancing è attualmente disponibile soltanto per i componenti modello.
:::

L'instancing viene abilitato automaticamente quando possibile. Defold cerca di raggruppare il più possibile le operazioni con lo stesso stato di disegno; affinché l'instancing funzioni, devono essere soddisfatti alcuni requisiti:

- Tutte le istanze devono usare lo stesso materiale. L'instancing funziona anche se è stato impostato un materiale personalizzato tramite `render.enable_material`)
- Il materiale deve essere configurato per usare lo spazio dei vertici 'local'
- Il materiale deve avere almeno un attributo dei vertici ripetuto per istanza
- I valori delle costanti devono essere uguali per tutte le istanze. In alternativa, i valori delle costanti possono essere inseriti in attributi dei vertici personalizzati o memorizzati in altro modo (per esempio in una texture)
- Le risorse degli shader, come texture o buffer di archiviazione, devono essere uguali per tutte le istanze

Per configurare un attributo dei vertici affinché venga ripetuto per istanza, occorre impostare `Step function` su `Instance`. Per determinati tipi semantici questo avviene automaticamente in base al nome (vedi la tabella `Default attribute semantics` qui sopra), ma puoi anche configurarlo manualmente nell'editor dei materiali impostando `Step function` su `Instance`.

Come semplice esempio, la scena seguente contiene quattro oggetti di gioco, ciascuno con un componente modello:

![Configurazione dell'instancing](images/materials/instancing-setup.png)

Il materiale è configurato come mostrato, con un solo attributo dei vertici personalizzato che viene ripetuto per istanza:

![Materiale per l'instancing](images/materials/instancing-material.png)

Nel vertex shader sono specificati più attributi per istanza:

```glsl
// Per vertex attributes
attribute highp vec4 position;
attribute mediump vec2 texcoord0;
attribute mediump vec3 normal;

// Per instance attributes
attribute mediump mat4 mtx_world;
attribute mediump mat4 mtx_normal;
attribute mediump vec4 instance_color;
```

Nota che `mtx_world` e `mtx_normal` vengono configurati per usare la funzione di avanzamento `Instance` per impostazione predefinita. Puoi modificarla nell'editor dei materiali aggiungendo una voce per ciascuno e impostando `Step function` su `Vertex`: in questo modo l'attributo viene ripetuto per vertice anziché per istanza.

Per verificare che l'instancing funzioni in questo caso, puoi consultare il profilatore web. Poiché tra le istanze del parallelepipedo cambiano soltanto gli attributi per istanza, è possibile renderizzarle con una sola chiamata di disegno:

![Chiamate di disegno con instancing](images/materials/instancing-draw-calls.png)

#### Compatibilità con le versioni precedenti {#backwards-compatibility}

OpenGL 3.1 su desktop e OpenGL ES 3.0 su dispositivi mobili offrono l'instancing come funzionalità di base. I contesti OpenGL ES e WebGL meno recenti possono comunque supportarlo tramite un'estensione come `ANGLE_instanced_arrays`; altri adattatori meno recenti non lo supportano. Quando l'instancing non è disponibile, il rendering continua a funzionare per impostazione predefinita, ma le prestazioni possono essere inferiori.

Usa `graphics.get_adapter_info()` per rilevare il supporto e scegliere un materiale meno costoso oppure omettere contenuti con molte istanze quando necessario. Il campo `features` è un array delle costanti delle funzionalità supportate, non una tabella che usa tali costanti come chiavi:

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

local instancing_supported = has_context_feature(
    graphics.CONTEXT_FEATURE_INSTANCING
)
```

## Costanti dei vertex shader e dei fragment shader {#vertex-and-fragment-constants}

Le costanti degli shader, o "uniform", sono valori passati dal motore ai programmi vertex shader e fragment shader. Per usare una costante, definiscila nel file del materiale come proprietà *Vertex Constant* o *Fragment Constant*. Nel programma shader devono essere definite le variabili `uniform` corrispondenti. In un materiale puoi impostare le seguenti costanti:

`CONSTANT_TYPE_WORLD`
: La matrice del mondo. Usala per trasformare i vertici nello spazio del mondo. Per alcuni tipi di componenti, i vertici sono già nello spazio del mondo quando arrivano al vertex shader (a causa del raggruppamento delle chiamate di disegno). In questi casi, moltiplicarli per la matrice del mondo nello shader produce risultati errati.

`CONSTANT_TYPE_VIEW`
: La matrice di vista. Usala per trasformare i vertici nello spazio di vista (della camera).

`CONSTANT_TYPE_PROJECTION`
: La matrice di proiezione. Usala per trasformare i vertici nello spazio dello schermo.

`CONSTANT_TYPE_VIEWPROJ`
: Una matrice che contiene il prodotto delle matrici di vista e di proiezione.

`CONSTANT_TYPE_WORLDVIEW`
: Una matrice che contiene il prodotto delle matrici del mondo e di vista.

`CONSTANT_TYPE_WORLDVIEWPROJ`
: Una matrice che contiene il prodotto delle matrici del mondo, di vista e di proiezione.

`CONSTANT_TYPE_WORLD_INVERSE`
: L'inversa della matrice del mondo. Usala per trasformare dallo spazio del mondo allo spazio locale dell'oggetto.

`CONSTANT_TYPE_VIEW_INVERSE`
: L'inversa della matrice di vista. Usala per trasformare dallo spazio della camera allo spazio del mondo.

`CONSTANT_TYPE_PROJECTION_INVERSE`
: L'inversa della matrice di proiezione. Usala per trasformare dallo spazio di ritaglio allo spazio della camera.

`CONSTANT_TYPE_VIEWPROJ_INVERSE`
: L'inversa delle matrici di vista e di proiezione combinate. Usala per trasformare dallo spazio di ritaglio allo spazio del mondo.

`CONSTANT_TYPE_WORLDVIEW_INVERSE`
: L'inversa delle matrici del mondo e di vista combinate. Usala per trasformare dallo spazio della camera allo spazio locale dell'oggetto.

`CONSTANT_TYPE_WORLDVIEWPROJ_INVERSE`
: L'inversa delle matrici del mondo, di vista e di proiezione combinate. Usala per trasformare dallo spazio di ritaglio allo spazio locale dell'oggetto. Queste costanti inverse evitano di calcolare l'inversa di una matrice nello shader.

`CONSTANT_TYPE_NORMAL`
: Una matrice per calcolare l'orientamento delle normali. La trasformazione del mondo può includere un ridimensionamento non uniforme, che rompe l'ortogonalità della trasformazione combinata mondo-vista. La matrice delle normali evita problemi di direzione durante la trasformazione delle normali. (La matrice delle normali è l'inversa trasposta della matrice mondo-vista).

`CONSTANT_TYPE_TIME`
: Un `vector4` fornito dal motore, in cui `.x` è il tempo trascorso dall'avvio del motore, `.y` è l'intervallo di tempo dal fotogramma precedente e `.z` e `.w` sono attualmente zero. Il motore aggiorna questo valore automaticamente; non è necessario aggiornarlo con `go.set()`. Consulta il [tutorial su Shadertoy](/tutorials/shadertoy/#animation) per un esempio.

  Dichiara una costante Time chiamata `time` in un blocco uniform GLSL moderno:

  ```glsl
  uniform fragment_inputs
  {
      vec4 time;
  };
  ```

`CONSTANT_TYPE_USER`
: Una costante vector4 che puoi usare per qualsiasi dato personalizzato da passare ai programmi shader. Puoi impostare il valore iniziale della costante nella sua definizione e modificarlo tramite le funzioni [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate). Puoi anche recuperare il valore con [go.get()](/ref/stable/go/#go.get). Modificare una costante del materiale di una singola istanza di componente [interrompe il raggruppamento del rendering e genera chiamate di disegno aggiuntive](/manuals/render/#draw-calls-and-batching).

Esempio:

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

`CONSTANT_TYPE_USER_MATRIX4`
: Una costante matrix4 che puoi usare per qualsiasi dato personalizzato da passare ai programmi shader. Puoi impostare il valore iniziale della costante nella sua definizione e modificarlo tramite le funzioni [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate). Puoi anche recuperare il valore con [go.get()](/ref/stable/go/#go.get). Modificare una costante del materiale di una singola istanza di componente [interrompe il raggruppamento del rendering e genera chiamate di disegno aggiuntive](/manuals/render/#draw-calls-and-batching).

Esempio:

```lua
go.set("#sprite", "m", vmath.matrix4())
```

### Costanti del materiale dei nodi GUI {#gui-node-material-constants}

All'interno di uno script GUI, leggi e scrivi le costanti del materiale di un nodo con `gui.get()` e `gui.set()`, anziché con le funzioni `go`. Sono supportati i componenti dei vettori, le costanti matrice e gli array di costanti. Gli indici degli array nella tabella delle opzioni partono da 1:

```lua
local node = gui.get_node("button")

local tint = gui.get(node, "tint")
gui.set(node, "tint.x", 0.5)
gui.set(node, "light_matrix", vmath.matrix4())
gui.set(node, "tint_array", vmath.vector4(1, 0, 0, 1), { index = 1 })
```

::: sidenote
Affinché una costante del materiale di tipo `CONSTANT_TYPE_USER` o `CONSTANT_TYPE_USER_MATRIX4` sia disponibile tramite `go.get()` e `go.set()`, oppure `gui.get()` e `gui.set()`, deve essere usata nel programma shader. Se la costante è definita nel materiale ma non viene usata nel programma, viene rimossa dal materiale e non sarà disponibile durante l'esecuzione.
:::

## Campionatori {#samplers}

I campionatori servono a campionare le informazioni sul colore da una texture (una sorgente di tile o un atlas). Le informazioni sul colore possono poi essere usate per i calcoli nel programma shader.

I componenti sprite, tilemap, GUI ed effetto particellare associano automaticamente la texture della propria immagine al primo `sampler2D` dichiarato. I componenti sprite supportano anche più texture: ogni campionatore dichiarato nel materiale diventa uno slot immagine con un nome nel componente Sprite. La prima texture fornisce i dati dell'animazione dello sprite e determina la sequenza dei fotogrammi. Per ogni fotogramma, l'ID della sua immagine viene usato per trovare l'immagine corrispondente in ciascuna texture aggiuntiva, che fornisce le proprie coordinate UV. Gli atlas o le sorgenti di tile assegnati devono quindi contenere ID dei fotogrammi corrispondenti e immagini di forma simile; forme poligonali diverse usate per l'impacchettamento possono causare contaminazioni ai bordi delle texture. Consulta [Sprite con più texture](/manuals/sprite/#multi-textured-sprites) per i dettagli.

Per un componente o un flusso di lavoro di rendering che non espone uno slot per una texture aggiuntiva, usa [`render.enable_texture()`](/ref/render/#render.enable_texture) per associare campionatori di texture aggiuntivi dallo script di rendering.

![Campionatore dello sprite](images/materials/sprite_sampler.png)

```glsl
-- mysprite.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D MY_SAMPLER;
void main()
{
    gl_FragColor = texture2D(MY_SAMPLER, var_texcoord0.xy);
}
```

Puoi specificare le impostazioni del campionatore di un componente aggiungendo il campionatore per nome nel file del materiale. Se non configuri il campionatore nel file del materiale, vengono usate le impostazioni globali del progetto nella sezione *graphics*.

![Impostazioni del campionatore](images/materials/my_sampler.png)

Per i componenti modello, devi specificare i campionatori nel file del materiale con le impostazioni desiderate. L'editor ti permetterà quindi di impostare le texture per qualsiasi componente modello che usa il materiale:

![Campionatori del modello](images/materials/model_samplers.png)

```glsl
-- mymodel.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D TEXTURE_1;
uniform lowp sampler2D TEXTURE_2;
void main()
{
    lowp vec4 color1 = texture2D(TEXTURE_1, var_texcoord0.xy);
    lowp vec4 color2 = texture2D(TEXTURE_2, var_texcoord0.xy);
    gl_FragColor = color1 * color2;
}
```

![Modello](images/materials/model.png)

## Impostazioni dei campionatori {#sampler-settings}

Name
: Il nome del campionatore. Questo nome deve corrispondere al `sampler2D` dichiarato nel fragment shader.

Wrap U/W
: La modalità di ripetizione lungo gli assi U e V:

  - `WRAP_MODE_REPEAT` ripete i dati della texture al di fuori dell'intervallo [0,1].
  - `WRAP_MODE_MIRRORED_REPEAT` ripete i dati della texture al di fuori dell'intervallo [0,1], ma a ripetizioni alterne li specchia.
  - `WRAP_MODE_CLAMP_TO_EDGE` imposta a 1.0 i valori superiori a 1.0 e a 0.0 i valori inferiori a 0.0 per i dati della texture; in altre parole, i pixel del bordo vengono ripetuti fino al margine.

Filter Min/Mag
: Il filtraggio per l'ingrandimento e la riduzione. Il filtraggio con il texel più vicino richiede meno calcoli dell'interpolazione lineare, ma può causare artefatti di aliasing. L'interpolazione lineare offre spesso risultati più uniformi:

  - `Default` usa l'opzione di filtraggio predefinita specificata nel file `game.project`, nella sezione `Graphics`, come `Default Texture Min Filter` e `Default Texture Mag Filter`.
  - `FILTER_MODE_NEAREST` usa il texel con le coordinate più vicine al centro del pixel.
  - `FILTER_MODE_LINEAR` calcola una media lineare ponderata della matrice 2x2 di texel più vicini al centro del pixel.
  - `FILTER_MODE_NEAREST_MIPMAP_NEAREST` sceglie il valore del texel più vicino all'interno di una singola mipmap.
  - `FILTER_MODE_NEAREST_MIPMAP_LINEAR` seleziona il texel più vicino nelle due mipmap più adatte e poi interpola linearmente tra questi due valori.
  - `FILTER_MODE_LINEAR_MIPMAP_NEAREST` interpola linearmente all'interno di una singola mipmap.
  - `FILTER_MODE_LINEAR_MIPMAP_LINEAR` usa l'interpolazione lineare per calcolare il valore in ciascuna di due mappe e poi interpola linearmente tra questi due valori.

Max Anisotropy
: Il filtraggio anisotropico è una tecnica avanzata di filtraggio che preleva più campioni e combina i risultati. Questa impostazione controlla il livello di anisotropia dei campionatori di texture. Se la GPU non supporta il filtraggio anisotropico, il parametro non ha alcun effetto e viene impostato sul valore predefinito 1.

## Buffer delle costanti {#constants-buffers}

Quando la pipeline di rendering disegna, recupera i valori delle costanti da un buffer delle costanti predefinito del sistema. Puoi creare un buffer delle costanti personalizzato per sovrascrivere le costanti predefinite e impostare invece le variabili uniform del programma shader tramite codice nello script di rendering:

```lua
self.constants = render.constant_buffer() -- <1>
self.constants.tint = vmath.vector4(1, 0, 0, 1) -- <2>
...
render.draw(self.my_pred, {constants = self.constants}) -- <3>
```
1. Crea un nuovo buffer delle costanti
2. Imposta la costante `tint` su un rosso acceso
3. Disegna il predicato usando le nostre costanti personalizzate

Nota che gli elementi costanti del buffer si possono referenziare come in una normale tabella Lua, ma non puoi iterare sul buffer con `pairs()` o `ipairs()`.
