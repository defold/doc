---
title: Handbuch zur 3D-Modellanimation in Defold
brief: Dieses Handbuch beschreibt, wie du 3D-Modellanimationen in Defold verwendest.
---

# 3D-Modellanimation {#3d-model-animation}

Modellkomponenten (model components) können Skelettanimationen und Morph-Ziel-Animationen abspielen, die aus glTF-Dateien importiert wurden. Die Skelettanimation (skeletal animation) nutzt die Knochen des Modells, um dessen Vertices zu verformen. Die Morph-Ziel-Animation (morph target animation), auch als Blend-Shape-Animation bekannt, verändert die Form des Modells, indem sie Gewichtungen für alternative Vertex-Positionen animiert.

Einzelheiten dazu, wie du 3D-Daten für die Animation in ein Modell importierst, findest du in der [Modelldokumentation](/manuals/model).

  ![Blender-Animation](images/animation/blender_animation.png)
  ![Wackelanimation in einer Schleife](images/animation/suzanne.gif)


## Animationen abspielen {#playing-animations}

Modelle werden mit der Funktion [`model.play_anim()`](/ref/model#model.play_anim) animiert:

```lua
function init(self)
    -- Start the "wiggle" animation back and forth on #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold unterstützt derzeit nur vorab berechnete Skelettanimationen. Skelettanimationen müssen in jedem Schlüsselbild (keyframe) für jeden animierten Knochen Matrizen enthalten, anstelle separater Schlüssel für Position, Drehung und Skalierung.

Animationen werden außerdem linear interpoliert. Wenn du eine komplexere Kurveninterpolation verwendest, müssen die Animationen beim Export vorab berechnet werden.
:::

### Morph-Ziele {#morph-targets}

Morph-Ziele (morph targets) sind alternative Formen desselben Meshes. Jedes Ziel speichert Differenzen für Position, Normale und Tangente und besitzt eine Mischgewichtung, die steuert, wie stark diese Form angewendet wird. Eine Gewichtung von `0` bedeutet, dass das Ziel keine Auswirkung hat, während eine Gewichtung von `1` die vollständige Zielform anwendet. Werte außerhalb dieses Bereichs können ebenfalls für überzeichnete Effekte nützlich sein, wenn der Shader und das Asset dafür ausgelegt sind.

Defold importiert Morph-Ziele und anfängliche Morph-Gewichtungen aus glTF-Modelldaten. glTF-Animationen, die Morph-Gewichtungen animieren, werden in den Animationssatz des Modells importiert und können genau wie Skelettanimationen mit [`model.play_anim()`](/ref/model#model.play_anim) abgespielt werden:

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

Morph-Ziel-Daten können allein oder zusammen mit einer Skelettanimation verwendet werden, aber eine Modellkomponente kann jeweils nur eine Modellanimation abspielen. Das bedeutet, dass du mit `model.play_anim()` eine Skelettanimation und eine separate Morph-Ziel-Animation nicht gleichzeitig abspielen kannst. Wenn ein Modell Animationsdaten, aber kein Skelett besitzt, werden nur die Animationsdaten der Morph-Ziele verwendet.

Du kannst die Wiedergabe einer Skelettanimation dennoch mit Änderungen an Morph-Zielen aus anderen Quellen kombinieren, beispielsweise indem du die Gewichtungen der Morph-Ziele per Skript mit `model.set_blend_weights()` festlegst.

Du kannst die Gewichtungen der Morph-Ziele auch per Skript auslesen und überschreiben. [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) gibt die aktuellen Gewichtungen für das erste Mesh im Modell zurück, das Morph-Ziele besitzt. [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) überschreibt die Werte per Skript für jedes durch Morph-Ziele verformte Mesh im Modell:

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

Die Gewichtungstabelle verwendet bei eins beginnende Lua-Indizes in derselben Reihenfolge wie die Morph-Ziele im Mesh. Zusätzliche Werte werden ignoriert. Bei Meshes mit mehr Morph-Zielen als Einträgen in der Tabelle werden fehlende Werte als null behandelt. Die Überschreibung per Skript wird in jedem Frame nach der Animation angewendet, bis sie aufgehoben wird:

```lua
model.set_blend_weights("#model")     -- clear the override
model.set_blend_weights("#model", nil) -- also clears the override
```

### Shader-Unterstützung {#shader-support}

Um Morph-Ziele zu rendern, muss der Vertex-Shader des Modellmaterials die erzeugte Textur `morph_targets` abtasten und die gewichteten Differenzen auf die Vertex-Daten anwenden. Die Morph-Ziel-Textur ist eine 2D-Array-Textur, in der jedes Morph-Ziel drei Array-Ebenen verwendet: die Differenz für die Position, die Normale und die Tangente.

Die Engine stellt die aktuellen Morph-Gewichtungen über eine Vertex-Shader-Uniform namens `morph_targets_weights` bereit. Jeder `vec4` speichert vier Gewichtungen, sodass `morph_targets_weights[2]` Platz für acht Morph-Ziele bietet.

Das folgende Beispiel zeigt die relevanten Teile des Vertex-Shaders für ein Modellmaterial ohne Instancing:

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

Die Umschließung mit `#ifndef EDITOR` ist erforderlich, da der Editor noch keine Vorschau von Modellanimationen unterstützt und die erzeugten Morph-Ziel-Texturdaten deshalb nur zur Laufzeit verfügbar sind. Vergrößere das Array `morph_targets_weights` und füge weitere Aufrufe von `apply_morph_target()` hinzu, wenn das Mesh mehr Morph-Ziele besitzt.

::: important
Das obige Shader-Beispiel verwendet `textureSize()` und funktioniert nicht mit OpenGL ES 2.0.
:::

### Die Knochenhierarchie {#the-bone-hierarchy}

Die Knochen im Skelett des Modells werden intern als Spielobjekte (game objects) dargestellt.

Du kannst den Instanzbezeichner des Knochen-Spielobjekts zur Laufzeit abrufen. Die Funktion [`model.get_go()`](/ref/model#model.get_go) gibt den Bezeichner des Spielobjekts für den angegebenen Knochen zurück.

```lua
-- Get the middle bone go of our wiggler model
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Now do something useful with the game object...
```

### Cursor-Animation

Neben der Möglichkeit, eine Modellanimation mit `model.play_anim()` voranzutreiben, stellen *Modellkomponenten* eine Eigenschaft `cursor` bereit, die du mit `go.animate()` verändern kannst (mehr über [Eigenschaftsanimationen](/manuals/property-animation)):

```lua
-- Set the animation on #model but don't start it
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Set the cursor to the beginning of the animation
go.set("#model", "cursor", 0)
-- Tween the cursor between 0 and 1 pingpong with in-out quad easing.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Callbacks beim Abschluss {#completion-callbacks}

Die Modellanimationsfunktion `model.play_anim()` unterstützt eine optionale Lua-Callback-Funktion als letztes Argument. Diese Funktion wird aufgerufen, wenn die Animation bis zum Ende abgespielt wurde. Die Funktion wird weder bei wiederholten Animationen noch beim manuellen Abbrechen einer Animation über `go.cancel_animations()` aufgerufen. Mit dem Callback kannst du beim Abschluss einer Animation Ereignisse auslösen oder mehrere Animationen miteinander verketten.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Done animating
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Wiedergabemodi {#playback-modes}

Animationen können entweder einmalig oder in einer Schleife abgespielt werden. Der Wiedergabemodus bestimmt, wie die Animation abgespielt wird:

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
