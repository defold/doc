---
title: Programmi shader in Defold
brief: Questo manuale descrive in dettaglio i vertex shader e i fragment shader e spiega come usarli in Defold.
---

# Shader {#shaders}

I programmi shader sono alla base del rendering grafico. Sono programmi scritti in un linguaggio simile al C, chiamato GLSL (GL Shading Language), che l'hardware grafico esegue per operare sui dati 3D sottostanti (i vertici) oppure sui pixel visualizzati sullo schermo (i "frammenti"). Gli shader servono a disegnare sprite, illuminare modelli 3D, creare effetti di post-elaborazione a schermo intero e molto altro.

Questo manuale descrive come la pipeline di rendering di Defold interagisce con gli shader della GPU. Per creare shader per i tuoi contenuti, devi anche comprendere il concetto di materiale e il funzionamento della pipeline di rendering.

* Consulta il [manuale del rendering](/manuals/render) per i dettagli sulla pipeline di rendering.
* Consulta il [manuale dei materiali](/manuals/material) per i dettagli sui materiali.
* Consulta il [manuale dei programmi di calcolo](/manuals/compute) per i dettagli sui programmi di calcolo.

Le specifiche di OpenGL ES 2.0 (OpenGL for Embedded Systems) e di OpenGL ES Shading Language sono disponibili nel [registro OpenGL di Khronos](https://www.khronos.org/registry/gles/).

Tieni presente che sui computer desktop puoi scrivere shader che usano funzionalità non disponibili in OpenGL ES 2.0. Il driver della tua scheda grafica potrebbe compilare ed eseguire senza problemi codice shader che non funzionerà sui dispositivi mobili.


## Concetti {#concepts}

Vertex shader
: Un vertex shader non può creare o eliminare vertici, ma soltanto modificare la posizione di un vertice. I vertex shader vengono comunemente usati per trasformare le posizioni dei vertici dallo spazio 3D del mondo allo spazio 2D dello schermo.

  L'input di un vertex shader è costituito dai dati dei vertici (sotto forma di `attributes`) e dalle costanti (`uniforms`). Tra le costanti più comuni ci sono le matrici necessarie per trasformare e proiettare la posizione di un vertice nello spazio dello schermo.

  L'output del vertex shader è la posizione calcolata del vertice sullo schermo (`gl_Position`). È inoltre possibile passare dati dal vertex shader al fragment shader tramite variabili `varying`.

Fragment shader
: Dopo l'esecuzione del vertex shader, il fragment shader ha il compito di determinare il colore di ciascun frammento (o pixel) delle primitive risultanti.

  L'input di un fragment shader è costituito dalle costanti (`uniforms`) e da tutte le variabili `varying` impostate dal vertex shader.

  L'output del fragment shader è il valore del colore del frammento specifico (`gl_FragColor`).

Compute shader
: Un compute shader è uno shader generico che può eseguire qualsiasi tipo di operazione su una GPU. Non fa parte della pipeline grafica: i compute shader vengono eseguiti in un contesto separato e non dipendono dall'input di altri shader.

  L'input di un compute shader è costituito da buffer di costanti (`uniforms`), immagini di texture (`image2D`), campionatori (`sampler2D`) e buffer di archiviazione (`buffer`).

  L'output di un compute shader non è definito esplicitamente: a differenza dei vertex shader e dei fragment shader, non deve produrre un output specifico. Poiché i compute shader sono generici, spetta al programmatore definire il tipo di risultato che devono produrre.

Matrice del mondo
: Le posizioni dei vertici che definiscono la forma di un modello sono memorizzate rispetto all'origine del modello. Questo è lo "spazio del modello". Il mondo di gioco, invece, è uno "spazio del mondo", in cui la posizione, l'orientamento e la scala di ciascun vertice sono espressi rispetto all'origine del mondo. Mantenendo separati questi spazi, il motore di gioco può spostare, ruotare e ridimensionare ciascun modello senza alterare i valori originali dei vertici memorizzati nel componente modello.

  Quando un modello viene posizionato nel mondo di gioco, le coordinate locali dei suoi vertici devono essere convertite in coordinate del mondo. Questa conversione viene eseguita da una *matrice di trasformazione del mondo*, che indica la traslazione (spostamento), la rotazione e la scala da applicare ai vertici del modello per posizionarli correttamente nel sistema di coordinate del mondo di gioco.

  ![Trasformazione del mondo](images/shader/world_transform.png)

Matrici di vista e di proiezione
: Per visualizzare sullo schermo i vertici del mondo di gioco, le coordinate 3D vengono prima convertite in coordinate relative alla camera. Questa operazione viene eseguita con una _matrice di vista_. Successivamente, i vertici vengono proiettati nello spazio 2D dello schermo con una _matrice di proiezione_:

  ![Proiezione](images/shader/projection.png)

Attributi
: Un attributo è un valore associato a un singolo vertice. Il motore passa gli attributi allo shader e, per accedere a un attributo, basta dichiararlo nel programma shader. Tipi di componenti diversi hanno insiemi di attributi diversi:
  - Uno sprite ha `position` e `texcoord0`.
  - Una griglia di tile ha `position` e `texcoord0`.
  - Un nodo GUI ha `position`, `textcoord0` e `color`.
  - ParticleFX ha `position`, `texcoord0` e `color`.
  - Un modello ha `position`, `texcoord0` e `normal`.
  - Un font ha `position`, `texcoord0`, `face_color`, `outline_color` e `shadow_color`.

Costanti
: Le costanti degli shader rimangono costanti per tutta la durata della chiamata di disegno. Le costanti vengono aggiunte alle sezioni *Constants* del file del materiale e poi dichiarate come `uniform` nel programma shader. Le uniform dei campionatori vengono aggiunte alla sezione *Samplers* del materiale e poi dichiarate come `uniform` nel programma shader. Le matrici necessarie per eseguire le trasformazioni dei vertici in un vertex shader sono disponibili come costanti:

  - `CONSTANT_TYPE_WORLD` è la *matrice del mondo*, che converte dallo spazio di coordinate locali di un oggetto allo spazio del mondo.
  - `CONSTANT_TYPE_VIEW` è la *matrice di vista*, che converte dallo spazio del mondo allo spazio della camera.
  - `CONSTANT_TYPE_PROJECTION` è la *matrice di proiezione*, che converte dallo spazio della camera allo spazio dello schermo.
  - `CONSTANT_TYPE_WORLDVIEW`, `CONSTANT_TYPE_VIEWPROJ` e `CONSTANT_TYPE_WORLDVIEWPROJ` forniscono le corrispondenti matrici combinate.
  - `CONSTANT_TYPE_WORLD_INVERSE`, `CONSTANT_TYPE_VIEW_INVERSE`, `CONSTANT_TYPE_PROJECTION_INVERSE`, `CONSTANT_TYPE_VIEWPROJ_INVERSE`, `CONSTANT_TYPE_WORLDVIEW_INVERSE` e `CONSTANT_TYPE_WORLDVIEWPROJ_INVERSE` forniscono le matrici inverse senza richiedere allo shader di calcolarle.
  - `CONSTANT_TYPE_TIME` è un `vec4` fornito dal motore: contiene il tempo trascorso dall'avvio del motore in `.x`, l'intervallo di tempo del frame in `.y` e zero in `.z` e `.w`.
  - `CONSTANT_TYPE_USER` è una costante di tipo `vec4` che puoi usare come preferisci.

  Il [manuale dei materiali](/manuals/material) spiega come specificare le costanti.

Campionatori
: Gli shader possono dichiarare variabili uniform di tipo *sampler*. I campionatori servono a leggere valori da un'immagine sorgente:

  - `sampler2D` campiona una texture con un'immagine 2D.
  - `sampler2DArray` campiona una texture con un array di immagini 2D. Viene usato principalmente per gli atlas suddivisi in pagine.
  - `samplerCube` campiona una texture cubemap composta da 6 immagini.
  - `image2D` carica (e potenzialmente memorizza) i dati delle texture in un oggetto immagine. Viene usato principalmente per l'archiviazione nei compute shader.

  Puoi usare un campionatore solo nelle funzioni di lettura delle texture della libreria standard GLSL. Il [manuale dei materiali](/manuals/material) spiega come specificare le impostazioni dei campionatori.

Coordinate UV
: A un vertice è associata una coordinata 2D che corrisponde a un punto su una texture 2D. È quindi possibile applicare una parte della texture, o l'intera texture, alla forma descritta da un insieme di vertici.

  ![Coordinate UV](images/shader/uv_map.png)

  Una mappa UV viene solitamente generata nel programma di modellazione 3D e memorizzata nella mesh. Le coordinate della texture di ciascun vertice vengono fornite al vertex shader come attributo. Una variabile `varying` viene poi usata per determinare la coordinata UV di ciascun frammento, interpolandola dai valori dei vertici.

Variabili varying
: Le variabili di tipo `Varying` servono a passare informazioni tra la fase dei vertici e quella dei frammenti.

  1. Nel vertex shader viene impostata una variabile varying per ciascun vertice.
  2. Durante la rasterizzazione, questo valore viene interpolato per ciascun frammento della primitiva di cui viene eseguito il rendering. La distanza del frammento dai vertici della forma determina il valore interpolato.
  3. La variabile viene impostata per ogni chiamata al fragment shader e può essere usata nei calcoli del frammento.

  ![Interpolazione delle variabili varying](images/shader/varying_vertex.png)

  Ad esempio, impostando una variabile `varying` su un valore di colore RGB `vec3` in ciascun vertice di un triangolo, i colori verranno interpolati su tutta la forma. Allo stesso modo, impostando le coordinate di lettura della texture (o *coordinate UV*) in ciascun vertice di un rettangolo, il fragment shader può leggere i valori di colore della texture per tutta l'area della forma.

  ![Interpolazione delle variabili varying](images/shader/varying.png)

## Scrivere shader GLSL moderni {#writing-modern-glsl-shaders}

Poiché il motore Defold supporta più piattaforme e API grafiche, per gli sviluppatori deve essere semplice scrivere shader che funzionino ovunque. La pipeline degli asset lo consente principalmente in due modi (da qui in avanti chiamati `shader pipelines`):

1. La pipeline legacy, in cui gli shader sono scritti in codice GLSL compatibile con ES2.
2. La pipeline moderna, in cui gli shader sono scritti in codice GLSL compatibile con SPIR-v.

A partire da Defold 1.9.2, si consiglia di scrivere shader che usino la nuova pipeline. Per farlo, la maggior parte degli shader deve essere migrata alla versione 140 (OpenGL 3.1) o successiva. Per migrare uno shader, assicurati che soddisfi questi requisiti:

### Dichiarazione della versione {#version-declaration}
Inserisci almeno #version 140 all'inizio dello shader:

```glsl
#version 140
```

La pipeline degli shader viene scelta in questo modo durante il processo di build, ed è per questo che puoi continuare a usare i vecchi shader. Se non viene trovata alcuna direttiva del preprocessore per la versione, Defold usa la pipeline legacy.

### Attributi {#attributes}
Nei vertex shader, sostituisci la parola chiave `attribute` con `in`:

```glsl
// instead of:
// attribute vec4 position;
// do:
in vec4 position;
```

Nota: i fragment shader (e i compute shader) non ricevono vertici in input.

### Variabili varying {#varyings}
Nei vertex shader, le variabili varying devono essere precedute da `out`. Nei fragment shader, le variabili varying diventano `in`:

```glsl
// In a vertex shader, instead of:
// varying vec4 var_color;
// do:
out vec4 var_color;

// In a fragment shader, instead of:
// varying vec4 var_color;
// do:
in vec4 var_color;
```

### Uniform (chiamate costanti in Defold) {#uniforms-called-constants-in-defold}

I tipi uniform opachi (campionatori, immagini, contatori atomici, SSBO) non richiedono alcuna migrazione: puoi continuare a usarli come fai ora:

```glsl
uniform sampler2D my_texture;
uniform image2D my_image;
```

I tipi uniform non opachi devono essere inseriti in un `uniform block`. Un blocco uniform è semplicemente un insieme di variabili uniform e viene dichiarato con la parola chiave `uniform`:

```glsl
uniform vertex_inputs
{
    mat4 mtx_world;
    mat4 mtx_proj;
    mat4 mtx_view;
    mat4 mtx_normal;
    ...
};

void main()
{
    // Individual members of the uniform block can be used as-is
    gl_Position = mtx_proj * mtx_view * mtx_world * vec4(position, 1.0);
}
```

Tutti i membri del blocco uniform vengono esposti ai materiali e ai componenti come costanti individuali. Non è necessaria alcuna migrazione per usare i buffer di costanti del rendering, né `go.set` e `go.get`.

### Variabili integrate {#built-in-variables}

Nei fragment shader, `gl_FragColor` è deprecata a partire dalla versione 140. Usa invece `out`:

```glsl
// instead of:
// gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
// do:
out vec4 color_out;

void main()
{
    color_out = vec4(1.0, 0.0, 0.0, 1.0);
}
```

### Funzioni per le texture {#texture-functions}

Le funzioni specifiche di campionamento delle texture, come `texture2D` e `texture2DArray`, non esistono più. Al loro posto, usa semplicemente la funzione `texture`:

```glsl
uniform sampler2D my_texture;
uniform sampler2DArray my_texture_array;

// instead of:
// vec4 sampler_2d = texture2D(my_texture, uv);
// vec4 sampler_2d_array = texture2DArray(my_texture_array, vec3(uv, slice));
// do:
vec4 sampler_2d = texture(my_texture, uv);
vec4 sampler_2d_array = texture(my_texture_array, vec3(uv, slice));
```

### Precisione {#precision}

Defold genera qualificatori di precisione predefiniti globali durante la compilazione incrociata degli shader per GLSL ES. I valori predefiniti sono `mediump` per i valori in virgola mobile e `highp` per gli interi. Puoi modificarli con le [impostazioni del progetto](/manuals/project-settings/#shader) **GLSL ES Default Precision Float** (`shader.glsl_es_default_precision_float`) e **GLSL ES Default Precision Int** (`shader.glsl_es_default_precision_int`); entrambe accettano `mediump` o `highp`.

Un qualificatore esplicito su una variabile, un input o un output ha la precedenza sul valore predefinito globale generato. Nei fragment shader OpenGL ES 2.0 e WebGL 1.0, `highp` non è supportato da tutti i dispositivi. Quando `highp` è selezionato come valore predefinito globale, Defold lo protegge con `GL_FRAGMENT_PRECISION_HIGH` e usa `mediump` sui dispositivi che non lo supportano.

### Esempio completo {#putting-it-together}

Come esempio finale che applica tutte queste regole, ecco gli shader integrati per gli sprite convertiti nel nuovo formato:

```glsl
#version 140

uniform vx_uniforms
{
    mat4 view_proj;
};

// positions are in world space
in vec4 position;
in vec2 texcoord0;

out vec2 var_texcoord0;

void main()
{
    gl_Position = view_proj * vec4(position.xyz, 1.0);
    var_texcoord0 = texcoord0;
}
```

```glsl
#version 140

in vec2 var_texcoord0;

out vec4 color_out;

uniform sampler2D texture_sampler;

uniform fs_uniforms
{
    vec4 tint;
};

void main()
{
    // Premultiply alpha since all runtime textures already are
    vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);
    color_out = texture(texture_sampler, var_texcoord0.xy) * tint_pm;
}

```

## Includere frammenti di codice negli shader {#including-snippets-into-shaders}

Gli shader in Defold supportano l'inclusione di codice sorgente da file del progetto con estensione `.glsl`. Per includere un file glsl da uno shader, usa il pragma `#include` con virgolette doppie o parentesi angolari. Le inclusioni devono usare percorsi relativi al progetto oppure al file che le contiene:

```glsl
// In file /main/my-shader.fp

// Absolute path
#include "/main/my-snippet.glsl"
// The file is in the same folder
#include "my-snippet.glsl"
// The file is in a sub-folder on the same level as 'my-shader'
#include "sub-folder/my-snippet.glsl"
// The file is in a sub-folder on the parent directory, i.e /some-other-folder/my-snippet.glsl
#include "../some-other-folder/my-snippet.glsl"
// The file is on the parent directory, i.e /root-level-snippet.glsl
#include "../root-level-snippet.glsl"
```

Ci sono alcune particolarità da considerare nel modo in cui vengono gestite le inclusioni:

  - I file devono essere relativi al progetto: puoi includere solo file che si trovano al suo interno. Qualsiasi percorso assoluto deve iniziare con `/`
  - Puoi includere codice in qualsiasi punto del file, ma non puoi includere un file all'interno di un'istruzione sulla stessa riga. Ad esempio, `const float #include "my-float-name.glsl" = 1.0` non funzionerà

### Protezioni contro inclusioni multiple {#header-guards}

I frammenti di codice possono a loro volta includere altri file `.glsl`: lo shader finale potrebbe quindi includere più volte lo stesso codice e, a seconda del contenuto dei file, causare problemi di compilazione dovuti a simboli dichiarati più di una volta. Per evitarlo, puoi usare le *protezioni contro inclusioni multiple*, un concetto comune a diversi linguaggi di programmazione. Esempio:

```glsl
// In my-shader.vs
#include "math-functions.glsl"
#include "pi.glsl"

// In math-functions.glsl
#include "pi.glsl"

// In pi.glsl
const float PI = 3.14159265359;
```

In questo esempio, la costante `PI` verrà definita due volte, causando errori di compilazione quando esegui il progetto. Devi invece proteggere il contenuto dalle inclusioni multiple:

```glsl
// In pi.glsl
#ifndef PI_GLSL_H
#define PI_GLSL_H

const float PI = 3.14159265359;

#endif // PI_GLSL_H
```

Il codice di `pi.glsl` verrà espanso due volte in `my-shader.vs`, ma, avendolo racchiuso nelle protezioni contro inclusioni multiple, il simbolo PI verrà definito una sola volta e lo shader verrà compilato correttamente.

Tuttavia, a seconda del caso d'uso, queste protezioni non sono sempre strettamente necessarie. Se vuoi riutilizzare il codice localmente in una funzione o in un altro punto in cui non serve che i valori siano disponibili globalmente nel codice dello shader, probabilmente è meglio non usare le protezioni contro inclusioni multiple. Esempio:

```glsl
// In red-color.glsl
vec3 my_red_color = vec3(1.0, 0.0, 0.0);

// In my-shader.fp
vec3 get_red_color()
{
  #include "red-color.glsl"
  return my_red_color;
}

vec3 get_red_color_inverted()
{
  #include "red-color.glsl"
  return 1.0 - my_red_color;
}
```

## Codice shader specifico per l'editor {#editor-specific-shader-code}

Quando viene eseguito il rendering degli shader nel viewport dell'editor Defold, è disponibile la definizione del preprocessore `EDITOR`. Questo ti permette di scrivere codice shader che si comporta in modo diverso quando viene eseguito nell'editor rispetto al motore di gioco vero e proprio.

Questo è particolarmente utile per:
  - Aggiungere visualizzazioni di debug che devono apparire solo nell'editor.
  - Implementare funzionalità specifiche per l'editor, come modalità wireframe o anteprime dei materiali.
  - Fornire un rendering alternativo per i materiali che potrebbero non funzionare correttamente nel viewport dell'editor.

Usa la direttiva del preprocessore `#ifdef EDITOR` per compilare in modo condizionale il codice che deve essere eseguito solo nell'editor:

```glsl
#ifdef EDITOR
    // This code will only execute when the shader is rendered in the Defold Editor
    color_out = vec4(1.0, 0.0, 1.0, 1.0); // Magenta color for editor preview
#else
    // This code will execute when running in the game
    color_out = texture(texture_sampler, var_texcoord0) * tint_pm;
#endif
```

## Il processo di rendering {#the-rendering-process}

Prima di essere visualizzati sullo schermo, i dati che crei per il tuo gioco attraversano una serie di passaggi:

![Pipeline di rendering](images/shader/pipeline.png)

Tutti i componenti visivi (sprite, nodi GUI, effetti particellari o modelli) sono costituiti da vertici, punti nel mondo 3D che descrivono la forma del componente. Questo permette di osservare la forma da qualsiasi angolazione e distanza. Il compito del programma vertex shader è prendere un singolo vertice e convertirlo in una posizione nel viewport, in modo che la forma possa essere visualizzata sullo schermo. Per una forma con 4 vertici, il programma vertex shader viene eseguito 4 volte, in parallelo.

![Vertex shader](images/shader/vertex_shader.png)

L'input del programma è la posizione del vertice (e gli altri dati degli attributi associati al vertice), mentre l'output è una nuova posizione del vertice (`gl_Position`), insieme alle eventuali variabili `varying` da interpolare per ciascun frammento.

Il programma vertex shader più semplice si limita a impostare la posizione di output su un vertice nullo (il che non è molto utile):

```glsl
void main()
{
    gl_Position = vec4(0.0,0.0,0.0,1.0);
}
```

Un esempio più completo è il vertex shader integrato per gli sprite:

```glsl
-- sprite.vp
uniform mediump mat4 view_proj;             // [1]

attribute mediump vec4 position;            // [2]
attribute mediump vec2 texcoord0;

varying mediump vec2 var_texcoord0;         // [3]

void main()
{
  gl_Position = view_proj * vec4(position.xyz, 1.0);    // [4]
  var_texcoord0 = texcoord0;                            // [5]
}
```
1. Una uniform (costante) contenente il prodotto delle matrici di vista e di proiezione.
2. Gli attributi del vertice dello sprite. `position` è già trasformata nello spazio del mondo. `texcoord0` contiene la coordinata UV del vertice.
3. Dichiara una variabile varying di output. Questa variabile verrà interpolata per ciascun frammento tra i valori impostati per ogni vertice e inviata al fragment shader.
4. `gl_Position` viene impostata sulla posizione di output del vertice corrente nello spazio di proiezione. Questo valore ha 4 componenti: `x`, `y`, `z` e `w`. La componente `w` serve a calcolare un'interpolazione corretta per la prospettiva. Questo valore è normalmente 1.0 per ogni vertice prima che venga applicata una matrice di trasformazione.
5. Imposta la coordinata UV varying per la posizione di questo vertice. Dopo la rasterizzazione, verrà interpolata per ciascun frammento e inviata al fragment shader.




Dopo l'elaborazione dei vertici, la forma del componente sullo schermo è definita: vengono generate e rasterizzate le primitive, cioè l'hardware grafico suddivide ciascuna forma in *frammenti*, o pixel. Esegue quindi il programma fragment shader una volta per ciascun frammento. Per un'immagine sullo schermo di 16x24 pixel, il programma viene eseguito 384 volte, in parallelo.

![Fragment shader](images/shader/fragment_shader.png)

L'input del programma è costituito dai dati inviati dalla pipeline di rendering e dal vertex shader, solitamente le *coordinate UV* del frammento, i colori della tinta e così via. L'output è il colore finale del pixel (`gl_FragColor`).

Il programma fragment shader più semplice si limita a impostare il colore di ciascun pixel sul nero (anche in questo caso, un programma poco utile):

```glsl
void main()
{
    gl_FragColor = vec4(0.0,0.0,0.0,1.0);
}
```

Anche in questo caso, un esempio più completo è il fragment shader integrato per gli sprite:

```glsl
// sprite.fp
varying mediump vec2 var_texcoord0;             // [1]

uniform lowp sampler2D DIFFUSE_TEXTURE;         // [2]
uniform lowp vec4 tint;                         // [3]

void main()
{
  lowp vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);          // [4]
  lowp vec4 diff = texture2D(DIFFUSE_TEXTURE, var_texcoord0.xy);// [5]
  gl_FragColor = diff * tint_pm;                                // [6]
}
```
1. Viene dichiarata la variabile varying delle coordinate della texture. Il suo valore verrà interpolato per ciascun frammento tra i valori impostati per ogni vertice della forma.
2. Viene dichiarata una variabile uniform `sampler2D`. Il campionatore, insieme alle coordinate interpolate della texture, serve a leggere la texture affinché venga applicata correttamente allo sprite. Poiché si tratta di uno sprite, il motore assocerà questo campionatore all'immagine impostata nella proprietà *Image* dello sprite.
3. Nel materiale viene definita una costante di tipo `CONSTANT_TYPE_USER`, dichiarata come `uniform`. Il suo valore permette di applicare una tinta allo sprite. Il valore predefinito è il bianco puro.
4. Il valore del colore della tinta viene premoltiplicato per il suo valore alfa, poiché tutte le texture a runtime contengono già l'alfa premoltiplicato.
5. Campiona la texture alla coordinata interpolata e restituisce il valore campionato.
6. `gl_FragColor` viene impostata sul colore di output del frammento: il colore diffuso della texture moltiplicato per il valore della tinta.

Il valore del frammento risultante viene poi sottoposto a dei test. Un test comune è il *test di profondità*, in cui il valore di profondità del frammento viene confrontato con quello nel buffer di profondità per il pixel in esame. A seconda del test, il frammento può essere scartato oppure un nuovo valore viene scritto nel buffer di profondità. Un uso comune di questo test permette agli elementi grafici più vicini alla camera di nascondere quelli più lontani.

Se il test stabilisce che il frammento deve essere scritto nel framebuffer, questo viene *miscelato* con i dati del pixel già presenti nel buffer. I parametri di miscelazione impostati nello script di rendering permettono di combinare in vari modi il colore sorgente (il valore scritto dal fragment shader) e il colore di destinazione (il colore dell'immagine nel framebuffer). Un uso comune della miscelazione è consentire il rendering di oggetti trasparenti.

## Approfondimenti {#further-study}

- [Shadertoy](https://www.shadertoy.com) contiene un'enorme quantità di shader creati dagli utenti. È un'ottima fonte di ispirazione per imparare diverse tecniche di uso degli shader. Molti degli shader presentati sul sito possono essere adattati a Defold con pochissimo lavoro. Il [tutorial di Shadertoy](https://www.defold.com/tutorials/shadertoy/) illustra i passaggi per convertire uno shader esistente a Defold.

- Il [tutorial sulla correzione del colore](https://www.defold.com/tutorials/grading/) mostra come creare un effetto di correzione del colore a schermo intero usando texture con tabelle di corrispondenza dei colori.

- [The Book of Shaders](https://thebookofshaders.com/00/) ti insegnerà a usare e integrare gli shader nei tuoi progetti, migliorandone le prestazioni e la qualità grafica.
