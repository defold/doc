---
title: Manual de animación de modelos 3D en Defold
brief: Este manual describe cómo usar animaciones de modelos 3D en Defold.
---

# Animación de modelos 3D

Los componentes Model pueden reproducir animaciones esqueléticas y animaciones de morph targets importadas desde archivos glTF. La animación esquelética usa los huesos del modelo para aplicar deformación a los vértices del modelo. La animación de morph targets, también conocida como animación blend shape, cambia la forma del modelo animando pesos para posiciones alternativas de vértices.

Para obtener detalles sobre cómo importar datos 3D en un Model para animación, consulta la [documentación de Model](/manuals/model).

  ![Animación de Blender](images/animation/blender_animation.png)
  ![Bucle wiggle](images/animation/suzanne.gif)


## Reproducir animaciones

Los modelos se animan con la función [`model.play_anim()`](/ref/model#model.play_anim):

```lua
function init(self)
    -- Inicia la animación "wiggle" de ida y vuelta en #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Actualmente Defold solo admite animaciones esqueléticas horneadas. Las animaciones esqueléticas deben tener matrices para cada hueso animado en cada keyframe, y no posición, rotación y escala como claves separadas.

Las animaciones también se interpolan linealmente. Si usas una interpolación de curvas más avanzada, las animaciones deben prehornearse desde el exportador.
:::

### Morph targets

Los morph targets son formas alternativas para la misma malla. Cada uno almacena deltas de posición, normal y tangente, y cada uno tiene un peso de mezcla que controla cuánto se aplica de esa forma. Un peso de `0` significa que el morph target no tiene efecto, mientras que un peso de `1` aplica la forma completa del morph target. Los valores fuera de ese rango también pueden ser útiles para efectos exagerados si el shader y el asset están preparados para ello.

Defold importa morph targets y pesos de morph iniciales desde los datos de modelo glTF. Las animaciones glTF que animan pesos de morph se importan en el Animation Set del modelo y pueden reproducirse con [`model.play_anim()`](/ref/model#model.play_anim), igual que las animaciones esqueléticas:

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

Los datos de morph targets pueden usarse por sí solos o junto con animación esquelética, pero un componente Model solo puede reproducir una animación de modelo a la vez. Esto significa que no puedes reproducir una animación esquelética y una animación separada de morph targets al mismo tiempo usando `model.play_anim()`. Si un modelo tiene datos de animación pero no tiene esqueleto, solo se usarán los datos de animación de morph targets.

Aun así, puedes combinar la reproducción de animaciones esqueléticas con cambios de morph targets que vengan de otras fuentes, por ejemplo, definiendo pesos de morph targets desde script con `model.set_blend_weights()`.

También puedes leer y sobrescribir pesos de morph targets desde script. [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) devuelve los pesos actuales de la primera malla del modelo que tenga morph targets. [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) aplica una sobrescritura desde script a cada malla con morph targets del modelo:

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

La tabla de pesos usa índices Lua basados en uno, en el mismo orden que los morph targets de la malla. Los valores extra se ignoran, y los valores que falten se tratan como cero en mallas con más morph targets de los que contiene la tabla. La sobrescritura desde script se aplica después de la animación en cada frame hasta que se borra:

```lua
model.set_blend_weights("#model")     -- borra la sobrescritura
model.set_blend_weights("#model", nil) -- también borra la sobrescritura
```

### Soporte de shader

Para renderizar morph targets, el vertex shader del material del modelo necesita muestrear la textura generada `morph_targets` y aplicar los deltas ponderados a los datos de vértice. La textura de morph targets es una textura array 2D donde cada morph target usa tres capas del array: delta de posición, delta de normal y delta de tangente.

El motor proporciona los pesos de morph actuales al vertex shader mediante un uniform llamado `morph_targets_weights`. Cada `vec4` almacena cuatro pesos, por lo que `morph_targets_weights[2]` tiene espacio para ocho morph targets.

El siguiente ejemplo muestra las partes relevantes del vertex shader para un material de modelo no instanciado:

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
    // Cada vec4 almacena cuatro pesos de mezcla. Usa morph_targets_weights[1]
    // para hasta 4 morph targets, [2] para hasta 8, [3] para hasta 12, etc.
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

El bloque `#ifndef EDITOR` es necesario porque la previsualización de animación de modelos aún no está disponible en el editor, por lo que los datos de textura de morph targets generados solo están disponibles en runtime. Aumenta el tamaño del array `morph_targets_weights` y agrega más llamadas a `apply_morph_target()` si la malla tiene más morph targets.

::: important
El ejemplo de shader anterior usa `textureSize()` y no funciona en OpenGL ES 2.0.
:::

### La jerarquía de huesos

Los huesos del esqueleto del Model se representan internamente como objetos de juego.

Puedes recuperar en runtime el id de instancia del objeto de juego del hueso. La función [`model.get_go()`](/ref/model#model.get_go) devuelve el id del objeto de juego para el hueso especificado.

```lua
-- Obtiene el objeto de juego del hueso central de nuestro modelo wiggler
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Ahora haz algo útil con el objeto de juego...
```

### Animación con cursor

Además de usar `model.play_anim()` para avanzar una animación de modelo, los componentes *Model* exponen una propiedad "cursor" que se puede manipular con `go.animate()` (más sobre [animaciones de propiedades](/manuals/property-animation)):

```lua
-- Define la animación en #model pero no la inicia
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Define el cursor al inicio de la animación
go.set("#model", "cursor", 0)
-- Interpola el cursor entre 0 y 1 en ping-pong con easing quad de entrada-salida.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Callbacks de finalización

La función de animación de modelo `model.play_anim()` admite una función callback Lua opcional como último argumento. Esta función se llamará cuando la animación se haya reproducido hasta el final. La función nunca se llama para animaciones en bucle, ni cuando una animación se cancela manualmente mediante `go.cancel_animations()`. El callback se puede usar para activar eventos al finalizar una animación o para encadenar varias animaciones.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Animación finalizada
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Modos de reproducción

Las animaciones se pueden reproducir una vez o en bucle. La forma en que se reproduce la animación la determina el modo de reproducción:

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
