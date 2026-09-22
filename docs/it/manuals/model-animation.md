---
title: Manuale dell'animazione di modelli 3D in Defold
brief: Questo manuale descrive come usare le animazioni dei modelli 3D in Defold.
---

# Animazione di modelli 3D {#3d-model-animation}

I componenti modello (Model) possono riprodurre animazioni scheletriche e animazioni con forme di destinazione (morph target) importate da file glTF. L'animazione scheletrica usa le ossa del modello per deformarne i vertici. L'animazione con forme di destinazione, nota anche come animazione con fusione di forme (blend shape), modifica la forma del modello animando i pesi associati a posizioni alternative dei vertici.

Per i dettagli su come importare dati 3D in un modello da animare, consulta la [documentazione sui modelli](/manuals/model).

  ![Animazione in Blender](images/animation/blender_animation.png)
  ![Oscillazione in ciclo](images/animation/suzanne.gif)


## Riproduzione delle animazioni {#playing-animations}

I modelli vengono animati con la funzione [`model.play_anim()`](/ref/model#model.play_anim):

```lua
function init(self)
    -- Start the "wiggle" animation back and forth on #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold attualmente supporta solo animazioni scheletriche precalcolate. Le animazioni scheletriche devono contenere matrici per ogni osso animato a ogni fotogramma chiave, anziché chiavi separate per posizione, rotazione e scala.

Le animazioni sono inoltre interpolate linearmente. Se usi un'interpolazione delle curve più avanzata, le animazioni devono essere precalcolate dallo strumento di esportazione.
:::

### Forme di destinazione {#morph-targets}

Le forme di destinazione sono forme alternative della stessa mesh. Ogni forma memorizza le variazioni di posizione, normale e tangente e ha un peso di fusione che controlla quanto viene applicata. Un peso di `0` significa che la forma non ha alcun effetto, mentre un peso di `1` applica completamente la forma di destinazione. Anche valori al di fuori di questo intervallo possono essere utili per effetti esagerati, se lo shader e l'asset sono stati creati per supportarli.

Defold importa le forme di destinazione e i pesi iniziali dai dati dei modelli glTF. Le animazioni glTF che animano questi pesi vengono importate nell'insieme di animazioni del modello e possono essere riprodotte con [`model.play_anim()`](/ref/model#model.play_anim), proprio come le animazioni scheletriche:

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

I dati delle forme di destinazione possono essere usati da soli o insieme all'animazione scheletrica, ma un componente modello può riprodurre una sola animazione del modello alla volta. Questo significa che non puoi riprodurre contemporaneamente un'animazione scheletrica e un'animazione separata con forme di destinazione usando `model.play_anim()`. Se un modello contiene dati di animazione ma non ha uno scheletro, verranno usati solo i dati di animazione delle forme di destinazione.

Puoi comunque combinare la riproduzione di un'animazione scheletrica con modifiche alle forme di destinazione provenienti da altre fonti, ad esempio impostandone i pesi da script con `model.set_blend_weights()`.

Puoi anche leggere e sovrascrivere i pesi delle forme di destinazione da script. [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) restituisce i pesi correnti della prima mesh del modello che contiene forme di destinazione. [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) applica una sovrascrittura da script a ogni mesh del modello deformata tramite forme di destinazione:

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

La tabella dei pesi usa indici Lua a partire da uno, nello stesso ordine delle forme di destinazione nella mesh. I valori in eccesso vengono ignorati e quelli mancanti vengono considerati pari a zero per le mesh che hanno più forme di destinazione di quante ne contenga la tabella. La sovrascrittura da script viene applicata dopo l'animazione a ogni fotogramma, finché non viene rimossa:

```lua
model.set_blend_weights("#model")     -- clear the override
model.set_blend_weights("#model", nil) -- also clears the override
```

### Supporto degli shader {#shader-support}

Per eseguire il rendering delle forme di destinazione, il vertex shader del materiale del modello deve campionare la texture generata `morph_targets` e applicare le variazioni ponderate ai dati dei vertici. La texture delle forme di destinazione è una texture array 2D in cui ogni forma usa tre livelli dell'array: variazione di posizione, variazione della normale e variazione della tangente.

Il motore fornisce i pesi correnti delle forme a una variabile uniform del vertex shader chiamata `morph_targets_weights`. Ogni `vec4` memorizza quattro pesi, quindi `morph_targets_weights[2]` può contenere i pesi di otto forme di destinazione.

L'esempio seguente mostra le parti rilevanti del vertex shader per il materiale di un modello senza istanziazione:

```glsl
#version 140

in highp vec4 position;
in mediump vec2 texcoord0;
in mediump vec3 normal;
in mediump vec4 tangent;

out mediump vec2 var_texcoord0;
out mediump vec3 var_normal;
out mediump vec4 var_tangent;

uniform vs_uniforms
{
    mediump mat4 mtx_worldview;
    mediump mat4 mtx_proj;
    mediump mat4 mtx_normal;
    // Each vec4 stores four blend weights. Use morph_targets_weights[1]
    // for up to 4 morph targets, [2] for up to 8, [3] for up to 12, etc.
    mediump vec4 morph_targets_weights[2];
};

uniform sampler2DArray morph_targets;

vec2 get_morph_uv(int vertex_index, int width, int height)
{
    int x = vertex_index % width;
    int y = vertex_index / width;
    return vec2(
        (float(x) + 0.5) / float(width),
        (float(y) + 0.5) / float(height)
    );
}

void apply_morph_target(vec2 uv, float weight, int target,
    inout vec3 position_delta, inout vec3 normal_delta, inout vec3 tangent_delta)
{
    if (weight == 0.0) {
        return;
    }

    int position_layer = target * 3 + 0;
    int normal_layer = target * 3 + 1;
    int tangent_layer = target * 3 + 2;

    position_delta += weight * texture(morph_targets, vec3(uv, position_layer)).xyz;
    normal_delta += weight * texture(morph_targets, vec3(uv, normal_layer)).xyz;
    tangent_delta += weight * texture(morph_targets, vec3(uv, tangent_layer)).xyz;
}

void get_morph_target_data(int vertex_index,
    out vec3 position_delta, out vec3 normal_delta, out vec3 tangent_delta)
{
    position_delta = vec3(0.0);
    normal_delta = vec3(0.0);
    tangent_delta = vec3(0.0);

#ifndef EDITOR
    ivec3 texture_size = textureSize(morph_targets, 0);
    vec2 uv = get_morph_uv(vertex_index, texture_size.x, texture_size.y);

    apply_morph_target(uv, morph_targets_weights[0].x, 0, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].y, 1, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].z, 2, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].w, 3, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].x, 4, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].y, 5, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].z, 6, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].w, 7, position_delta, normal_delta, tangent_delta);
#endif
}

void main()
{
    vec3 position_delta;
    vec3 normal_delta;
    vec3 tangent_delta;
    get_morph_target_data(gl_VertexIndex, position_delta, normal_delta, tangent_delta);

    vec3 morphed_position = position.xyz + position_delta;
    vec3 morphed_normal = normalize(normal + normal_delta);
    vec3 morphed_tangent = normalize(tangent.xyz + tangent_delta);

    var_texcoord0 = texcoord0;
    var_normal = normalize((mtx_normal * vec4(morphed_normal, 0.0)).xyz);
    var_tangent = vec4(normalize((mtx_normal * vec4(morphed_tangent, 0.0)).xyz), tangent.w);

    gl_Position = mtx_proj * mtx_worldview * vec4(morphed_position, 1.0);
}
```

Il wrapper `#ifndef EDITOR` è necessario perché l'anteprima dell'animazione dei modelli non è ancora disponibile nell'editor, quindi i dati della texture generata per le forme di destinazione sono disponibili solo durante l'esecuzione. Aumenta la dimensione dell'array `morph_targets_weights` e aggiungi altre chiamate a `apply_morph_target()` se la mesh contiene più forme di destinazione.

::: important
L'esempio di shader qui sopra usa `textureSize()` e non funziona con OpenGL ES 2.0.
:::

### La gerarchia delle ossa {#the-bone-hierarchy}

Le ossa dello scheletro del modello sono rappresentate internamente come oggetti di gioco.

Durante l'esecuzione puoi recuperare l'ID dell'istanza dell'oggetto di gioco di un osso. La funzione [`model.get_go()`](/ref/model#model.get_go) restituisce l'ID dell'oggetto di gioco dell'osso specificato.

```lua
-- Get the middle bone go of our wiggler model
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Now do something useful with the game object...
```

### Animazione del cursore {#cursor-animation}

Oltre a usare `model.play_anim()` per far avanzare l'animazione di un modello, i componenti *Model* espongono una proprietà `cursor` che può essere modificata con `go.animate()` (maggiori informazioni sulle [animazioni delle proprietà](/manuals/property-animation)):

```lua
-- Set the animation on #model but don't start it
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Set the cursor to the beginning of the animation
go.set("#model", "cursor", 0)
-- Tween the cursor between 0 and 1 pingpong with in-out quad easing.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Callback di completamento {#completion-callbacks}

La funzione di animazione dei modelli `model.play_anim()` supporta una funzione di callback Lua facoltativa come ultimo argomento. Questa funzione viene chiamata quando l'animazione arriva alla fine. Non viene mai chiamata per le animazioni in ciclo, né quando un'animazione viene annullata manualmente tramite `go.cancel_animations()`. La callback può essere usata per attivare eventi al completamento dell'animazione o per concatenare più animazioni.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Done animating
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Modalità di riproduzione {#playback-modes}

Le animazioni possono essere riprodotte una sola volta o in ciclo. Il modo in cui viene riprodotta l'animazione è determinato dalla modalità di riproduzione:

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
