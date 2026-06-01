---
title: Animacja modeli 3D w instrukcji Defold
brief: Ta instrukcja opisuje, jak używać animacji modeli 3D w Defold.
---

# Animacja modelu 3D

Komponenty Model mogą odtwarzać animacje szkieletowe i animacje celów morfingu importowane z plików glTF. Animacja szkieletowa wykorzystuje kości modelu do deformowania wierzchołków w siatce modelu. Animacja celów morfingu, znana też jako animacja blend shape, zmienia kształt modelu przez animowanie wag alternatywnych pozycji wierzchołków.

Szczegóły dotyczące importowania danych 3D do komponentu Model na potrzeby animacji znajdziesz w [dokumentacji Model](/manuals/model).

![Blender animation](images/animation/blender_animation.png)
![Wiggle loop](images/animation/suzanne.gif)

## Odtwarzanie animacji

Modele animuje się za pomocą funkcji [`model.play_anim()`](/ref/model#model.play_anim):

```lua
function init(self)
    -- Uruchom animację "wiggle" w tę i z powrotem na komponencie #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold obecnie obsługuje tylko wypieczone animacje szkieletowe (baked skeletal animations). Animacje szkieletowe muszą zawierać macierze dla każdej animowanej kości na każdej klatce kluczowej, a nie osobne klucze pozycji, rotacji i skali.

Animacje są też interpolowane liniowo. Jeśli potrzebujesz bardziej zaawansowanej interpolacji krzywych, musisz wypiec animację wcześniej, w eksporcie.
:::

### Cele morfingu {#morph-targets}

Cele morfingu to alternatywne kształty tej samej siatki. Każdy cel przechowuje delty pozycji, normalnej i tangenta, a także ma wagę mieszania, która kontroluje, w jakim stopniu dany kształt zostanie zastosowany. Waga `0` oznacza, że cel nie ma wpływu, a waga `1` stosuje pełny kształt celu. Wartości spoza tego zakresu również mogą być przydatne do przesadzonych efektów, jeśli shader i zasób zostały do tego przygotowane.

Defold importuje cele morfingu i początkowe wagi morfingu z danych modelu glTF. Animacje glTF, które animują wagi morfingu, są importowane do zestawu animacji modelu i można je odtwarzać funkcją [`model.play_anim()`](/ref/model#model.play_anim), tak samo jak animacje szkieletowe:

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

Dane celów morfingu mogą być używane samodzielnie albo razem z animacją szkieletową, ale komponent modelu może odtwarzać tylko jedną animację modelu naraz. Oznacza to, że nie można jednocześnie odtwarzać jednej animacji szkieletowej i osobnej animacji celów morfingu za pomocą `model.play_anim()`. Jeśli model ma dane animacji, ale nie ma szkieletu, użyte zostaną tylko dane animacji celów morfingu.

Nadal możesz łączyć odtwarzanie animacji szkieletowej ze zmianami celów morfingu pochodzącymi z innych źródeł, na przykład ustawiając wagi celów morfingu ze skryptu za pomocą `model.set_blend_weights()`.

Możesz też odczytywać i nadpisywać wagi celów morfingu ze skryptu. [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) zwraca bieżące wagi dla pierwszej siatki w modelu, która ma cele morfingu. [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) stosuje nadpisanie ze skryptu do każdej morfowanej siatki w modelu:

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

Tabela wag używa indeksów Lua zaczynających się od jedynki, w tej samej kolejności co cele morfingu w siatce. Nadmiarowe wartości są ignorowane, a brakujące wartości są traktowane jako zero dla siatek, które mają więcej celów morfingu niż wartości w tabeli. Nadpisanie ze skryptu jest stosowane po animacji w każdej klatce, dopóki nie zostanie wyczyszczone:

```lua
model.set_blend_weights("#model")     -- clear the override
model.set_blend_weights("#model", nil) -- also clears the override
```

### Obsługa shaderów

Aby renderować cele morfingu, vertex shader materiału modelu musi próbkować wygenerowaną teksturę `morph_targets` i zastosować ważone delty do danych wierzchołka. Tekstura celów morfingu to tekstura tablicowa 2D, w której każdy cel morfingu używa trzech warstw tablicy: delty pozycji, delty normalnej i delty tangenta.

Silnik przekazuje bieżące wagi morfingu do uniformu vertex shadera o nazwie `morph_targets_weights`. Każdy `vec4` przechowuje cztery wagi, więc `morph_targets_weights[2]` ma miejsce na osiem celów morfingu.

Poniższy przykład pokazuje istotne części vertex shadera dla materiału modelu bez instancingu:

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

Opakowanie `#ifndef EDITOR` jest potrzebne, ponieważ podgląd animacji modelu nie jest jeszcze dostępny w edytorze, więc wygenerowane dane tekstury celów morfingu są dostępne tylko w czasie działania. Zwiększ rozmiar tablicy `morph_targets_weights` i dodaj więcej wywołań `apply_morph_target()`, jeśli siatka ma więcej celów morfingu.

::: important
Powyższy przykład shadera używa `textureSize()` i nie działa w OpenGL ES 2.0.
:::

### Hierarchia kości

Kości w szkielecie modelu są wewnętrznie reprezentowane jako obiekty gry (game objects).

W czasie działania gry możesz pobrać identyfikator obiektu gry odpowiadającego danej kości za pomocą funkcji [`model.get_go()`](/ref/model#model.get_go).

```lua
-- Pobierz obiekt gry dla środkowej kości modelu wiggler
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Potem wykonaj na nim potrzebną operację...
```

### Animacja kursora

Oprócz używania `model.play_anim()` do sterowania animacją komponenty *Model* udostępniają właściwość "cursor", którą można animować za pomocą `go.animate()` (więcej w sekcji [animacje właściwości](/manuals/property-animation)).

```lua
-- Ustaw animację na komponencie #model, ale jej nie uruchamiaj
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Ustaw kursor na początku animacji
go.set("#model", "cursor", 0)
-- Animuj kursor między 0 a 1 w trybie pingpong z easingiem in-out quad
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Wywołania zwrotne po zakończeniu

Funkcja `model.play_anim()` obsługuje opcjonalny callback Lua jako ostatni argument. Zostaje on wywołany, gdy animacja dobiegnie końca. Nie jest wywoływany dla animacji zapętlonych ani wtedy, gdy anulujesz animację ręcznie przez `go.cancel_animations()`. Callback możesz wykorzystać do uruchamiania zdarzeń po zakończeniu animacji albo do łączenia kilku animacji w sekwencję.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Zakończono animację
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Tryby odtwarzania

Animacje można odtwarzać raz albo w pętli. Sposób ich odtwarzania zależy od wybranego trybu:

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
