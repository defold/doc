---
title: Componente luce in Defold
brief: Questo manuale spiega come usare le luci ambientali, direzionali, puntiformi e a faretto e come accedere ai dati delle luci negli shader.
---

# Componente luce {#light-component}

Il componente luce (Light) rappresenta una sorgente luminosa in una collezione (collection). Defold supporta attualmente quattro tipi di risorse luce:

- Luce ambientale (`.ambient_light`)
- Luce direzionale (`.directional_light`)
- Luce puntiforme (`.point_light`)
- Luce a faretto (`.spot_light`)

Le risorse luce si aggiungono agli oggetti di gioco (game object) come le altre risorse componente. Puoi creare componenti luce direttamente sotto un oggetto di gioco oppure creare una risorsa luce nel pannello *Assets* e poi aggiungerla come componente a un oggetto di gioco nella vista *Outline*.

Defold non applica automaticamente l'illuminazione a tutti i materiali. Il motore raccoglie le luci e le rende disponibili agli shader attraverso il buffer delle luci integrato. Lo shader del materiale decide come utilizzare i dati delle luci.

Gli esempi seguenti utilizzano la stessa scena per mostrare come i diversi tipi di luce influiscono sul risultato finale:

![Scena senza luci](images/light/no_light.png)

## Proprietà delle luci {#light-properties}

Tutti i colori delle luci sono valori RGB. Le risorse luce non utilizzano il canale alfa.

### Luce ambientale {#ambient-light}

Le luci ambientali aggiungono una luce costante alla scena. La posizione, la rotazione e la scala dell'oggetto di gioco non influiscono su di esse. Puoi utilizzarle, ad esempio, per un'illuminazione generale di fondo o per dare agli oggetti un aspetto privo di effetti di illuminazione.

Il componente luce ambientale è rappresentato nell'editor da un'icona con frecce rivolte verso il centro. Il colore dell'icona corrisponde alla sua proprietà `color`. 

![Luce ambientale con intensità inferiore](images/light/ambient_light_less_intensity.png)

Proprietà:

`color`
: Il colore RGB della luce ambientale.

`intensity`
: Moltiplica il colore della luce ambientale.

![Luce ambientale con intensità superiore](images/light/ambient_light_full_intensity.png)

Le luci ambientali vengono accumulate in un unico colore ambientale `light_info.xyz` nel buffer delle luci dello shader. Non occupano elementi nell'array `lights[]`. Più componenti luce ambientale nella scena producono un solo colore in uscita, ottenuto dalla combinazione di tutti i loro colori.

### Luce direzionale {#directional-light}

Le luci direzionali rappresentano la luce proveniente da una direzione, come la luce del sole. Non utilizzano la posizione o la scala dell'oggetto di gioco, ma la direzione della luce deriva dalla rotazione dell'oggetto di gioco nello spazio globale applicata alla direzione locale in avanti `(0, 0, -1)`.

Il componente luce direzionale è rappresentato nell'editor da un'icona a forma di sole colorato con una freccia 3D che ne indica la direzione.

![Luce direzionale](images/light/directional_light.png)

Proprietà:

`color`
: Il colore RGB della luce direzionale.

`intensity`
: Moltiplica il colore della luce direzionale.


Le luci direzionali vengono spesso combinate con la luce ambientale per evitare che le superfici rivolte dalla parte opposta rispetto alla luce direzionale diventino completamente scure.

![Luce direzionale e ambientale](images/light/directional_and_ambient_light.png)

### Luce puntiforme {#point-light}

Le luci puntiformi emettono luce verso l'esterno dalla posizione dell'oggetto di gioco nello spazio globale. La posizione della luce puntiforme corrisponde alla posizione dell'oggetto di gioco nello spazio globale.

Il componente luce puntiforme è rappresentato nell'editor da un punto circondato da raggi, il cui colore corrisponde alla proprietà `color`, e da un cerchio che rappresenta `range`.

![Luce puntiforme](images/light/point_light.png)

Proprietà:

`color`
: Il colore RGB della luce puntiforme.

`intensity`
: Moltiplica il colore della luce puntiforme.

`range`
: Il raggio della luce in unità dello spazio globale.

La portata effettiva viene moltiplicata per il valore assoluto più piccolo tra le componenti della scala dell'oggetto di gioco nello spazio globale.

![Portata della luce puntiforme](images/light/point_light_range.png)

Modificare il colore della luce cambia la tinta del contributo della luce puntiforme, mentre la portata controlla fino a quale distanza dalla sorgente arriva la luce.

![Portata della luce puntiforme di colore verde](images/light/point_ight_range_green_color.png)

### Luce a faretto {#spot-light}

Le luci a faretto emettono luce in un cono dalla posizione dell'oggetto di gioco nello spazio globale. La direzione deriva dalla rotazione dell'oggetto di gioco nello spazio globale applicata a `(0, 0, -1)`.

Il componente luce a faretto è rappresentato nell'editor da un'icona a forma di lampada colorata e da linee guida che mostrano i coni esterno e interno.

![Luce a faretto](images/light/spot_light.png)

Proprietà:

`color`
: Il colore RGB della luce a faretto.

`intensity`
: Moltiplica il colore della luce a faretto.

`range`
: Il raggio della luce in unità dello spazio globale.

`inner_cone_angle`
: L'angolo del cono interno, espresso in gradi nell'editor. I pixel all'interno di questo cono ricevono l'intero contributo del faretto.

`outer_cone_angle`
: L'angolo del cono esterno, espresso in gradi nell'editor. La luce si attenua tra il cono interno e quello esterno.

La portata effettiva viene moltiplicata per il valore assoluto più piccolo tra le componenti della scala dell'oggetto di gioco nello spazio globale. Gli angoli dei coni si modificano in gradi e vengono convertiti in radianti nella risorsa luce compilata.

![Indicatori della luce a faretto](images/light/spot_light_gizmos.png)

## Validazione {#validation}

La pipeline di build convalida e normalizza i dati delle risorse luce:

- `color` deve contenere esattamente tre numeri.
- `intensity` viene limitata a valori maggiori o uguali a `0`.
- `range` viene limitata a valori maggiori o uguali a `0` per le luci puntiformi e a faretto.
- Gli angoli dei coni dei faretti vengono limitati all'intervallo `0..180` gradi.
- `inner_cone_angle` viene limitato in modo da non superare mai `outer_cone_angle`.

## Limite del progetto {#project-limit}

Il numero massimo di componenti luce è controllato dall'impostazione di progetto `light.max_count`. Il valore predefinito è `64`.

Le luci ambientali non occupano elementi nell'array `lights[]` dello shader, ma sono comunque componenti luce e vengono conteggiate nel limite `light.max_count`. Le luci direzionali, puntiformi e a faretto occupano elementi in `lights[]` quando sono attive.

Se il numero di componenti luce supera `light.max_count`, il motore segnala un errore di buffer dei componenti pieno.

## Buffer delle luci negli shader {#light-buffer-in-shaders}

Uno shader può accedere alle luci attive dichiarando un blocco uniform denominato `LightBuffer` con il layout integrato. Il motore rileva questo blocco e associa automaticamente i dati delle luci ai materiali e ai programmi di calcolo che lo utilizzano.

![Shader con buffer delle luci](images/light/light-buffer-shader.png)

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

struct Light
{
    vec4 position;        // xyz: world position, w: unused
    vec4 color;           // rgb: color, a: unused
    vec4 direction_range; // xyz: normalized world direction, w: range
    vec4 params;          // x: type, y: intensity, z: inner cone, w: outer cone
};

uniform LightBuffer
{
    // xyz: accumulated ambient color, w: active non-ambient light count
    vec4 light_info;
    Light lights[MAX_LIGHT_COUNT];
};
```

Il tipo di luce è memorizzato in `lights[i].params.x`:

| Tipo | Valore |
|------|-------|
| Direzionale | `0` |
| Puntiforme | `1` |
| A faretto | `2` |

Lo shader può dichiarare un array `lights[]` più piccolo di `light.max_count`, ma non più grande. Limita sempre i cicli sulle luci alla dimensione dichiarata dell'array:

```glsl
vec3 apply_lights(vec3 normal)
{
    vec3 result = light_info.xyz;
    int active_light_count = int(light_info.w);

    for (int i = 0; i < MAX_LIGHT_COUNT; ++i)
    {
        if (i >= active_light_count)
        {
            break;
        }

        int type = int(lights[i].params.x);
        vec3 light_color = lights[i].color.rgb * lights[i].params.y;

        if (type == 0) // Directional
        {
            vec3 light_dir = normalize(-lights[i].direction_range.xyz);
            result += light_color * max(dot(normal, light_dir), 0.0);
        }
        else if (type == 1) // Point
        {
            result += light_color;
        }
        else if (type == 2) // Spot
        {
            result += light_color;
        }
    }

    return result;
}
```

L'esempio precedente mostra come accedere al buffer. Uno shader completo per luci puntiformi o a faretto deve anche calcolare il vettore dal punto da ombreggiare a `lights[i].position.xyz`, applicare l'attenuazione in funzione della distanza usando `lights[i].direction_range.w` e, per le luci a faretto, utilizzare `lights[i].params.z` e `lights[i].params.w` come angoli dei coni in radianti.

## Funzioni di illuminazione integrate {#built-in-lighting-helper}

Defold include una libreria di supporto per gli shader in `/builtins/materials/lighting.glsl`. Definisci `MAX_LIGHT_COUNT`, fornisci le variabili varying richieste dalla libreria, quindi includila nel fragment shader:

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

in vec3 var_normal;
in vec4 var_position;
in mat4 var_view;

out vec4 color_out;

#include "/builtins/materials/lighting.glsl"

void main()
{
    vec3 normal = normalize(var_normal);
    vec3 ambient = ambient_light();
    vec3 diffuse = diffuse_lambert(normal, var_position.xyz);
    color_out = vec4(ambient + diffuse, 1.0);
}
```

La libreria definisce le costanti `LIGHT_DIRECTIONAL`, `LIGHT_POINT` e `LIGHT_SPOT`, espone `ambient_light()` e fornisce funzioni per l'illuminazione diffusa di Lambert per le luci nel buffer.

## Vedi anche {#see-also}

- [Manuale degli shader](/manuals/shader)
- [Manuale dei materiali](/manuals/material)
- [Manuale del rendering](/manuals/render)
