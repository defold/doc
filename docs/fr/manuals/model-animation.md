---
title: Manuel de l’animation de modèles 3D dans Defold
brief: Ce manuel décrit comment utiliser les animations de modèles 3D dans Defold.
---

# Animation de modèles 3D {#3d-model-animation}

Les composants (component) Model peuvent lire des animations squelettiques et des animations par cibles de morphing importées de fichiers glTF. L’animation squelettique utilise les os du modèle pour déformer ses sommets. L’animation par cibles de morphing, également appelée animation par formes de mélange, modifie la forme du modèle en animant les poids de positions alternatives des sommets.

Pour savoir comment importer des données 3D dans un composant Model afin de l’animer, consultez la [documentation des modèles](/manuals/model).

  ![Animation dans Blender](images/animation/blender_animation.png)
  ![Ondulation en boucle](images/animation/suzanne.gif)


## Lecture des animations {#playing-animations}

Les modèles sont animés à l’aide de la fonction [`model.play_anim()`](/ref/model#model.play_anim) :

```lua
function init(self)
    -- Start the "wiggle" animation back and forth on #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold ne prend actuellement en charge que les animations squelettiques précalculées. Les animations squelettiques doivent disposer de matrices pour chaque os animé à chaque image clé, et non de clés distinctes de position, de rotation et d’échelle.

Les animations sont également interpolées linéairement. Si vous utilisez une interpolation de courbes plus avancée, les animations doivent être précalculées par l’outil d’exportation.
:::

### Cibles de morphing {#morph-targets}

Les cibles de morphing sont des formes alternatives d’un même maillage. Chaque cible stocke des écarts de position, de normale et de tangente, et possède un poids de mélange qui détermine dans quelle proportion cette forme est appliquée. Un poids de `0` signifie que la cible n’a aucun effet, tandis qu’un poids de `1` applique la totalité de la forme cible. Des valeurs hors de cet intervalle peuvent également être utiles pour obtenir des effets exagérés si le shader et la ressource sont conçus à cet effet.

Defold importe les cibles de morphing et leurs poids initiaux à partir des données de modèles glTF. Les animations glTF qui animent les poids de morphing sont importées dans l’ensemble d’animations du modèle et peuvent être lues avec [`model.play_anim()`](/ref/model#model.play_anim), comme les animations squelettiques :

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

Les données des cibles de morphing peuvent être utilisées seules ou avec une animation squelettique, mais un composant de modèle ne peut lire qu’une seule animation de modèle à la fois. Vous ne pouvez donc pas lire simultanément une animation squelettique et une animation distincte par cibles de morphing avec `model.play_anim()`. Si un modèle possède des données d’animation mais aucun squelette, seules les données d’animation par cibles de morphing seront utilisées.

Vous pouvez toutefois combiner la lecture d’une animation squelettique avec des modifications de cibles de morphing provenant d’autres sources, par exemple en définissant les poids des cibles de morphing depuis un script avec `model.set_blend_weights()`.

Vous pouvez également lire et remplacer les poids des cibles de morphing depuis un script. [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) renvoie les poids actuels du premier maillage du modèle qui possède des cibles de morphing. [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) applique un remplacement par script à chaque maillage du modèle soumis au morphing :

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

La table des poids utilise des indices Lua commençant à un, dans le même ordre que les cibles de morphing du maillage. Les valeurs supplémentaires sont ignorées, et les valeurs manquantes sont considérées comme égales à zéro pour les maillages qui possèdent plus de cibles de morphing que la table ne contient de valeurs. Le remplacement par script est appliqué après l’animation à chaque image, jusqu’à ce qu’il soit supprimé :

```lua
model.set_blend_weights("#model")     -- clear the override
model.set_blend_weights("#model", nil) -- also clears the override
```

### Prise en charge par les shaders {#shader-support}

Pour effectuer le rendu des cibles de morphing, le shader de sommets du matériau du modèle doit échantillonner la texture `morph_targets` générée et appliquer les écarts pondérés aux données des sommets. La texture des cibles de morphing est un tableau de textures 2D dans lequel chaque cible de morphing utilise trois couches : écart de position, écart de normale et écart de tangente.

Le moteur fournit les poids de morphing actuels à une variable uniforme du shader de sommets nommée `morph_targets_weights`. Chaque `vec4` stocke quatre poids ; `morph_targets_weights[2]` peut donc contenir les poids de huit cibles de morphing.

L’exemple suivant présente les parties concernées du shader de sommets pour un matériau de modèle sans instanciation :

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

L’encapsulation par `#ifndef EDITOR` est nécessaire, car l’aperçu des animations de modèles n’est pas encore disponible dans l’éditeur : les données générées de la texture des cibles de morphing ne sont donc disponibles qu’à l’exécution. Augmentez la taille du tableau `morph_targets_weights` et ajoutez des appels à `apply_morph_target()` si le maillage possède davantage de cibles de morphing.

::: important
L’exemple de shader ci-dessus utilise `textureSize()` et ne fonctionne pas avec OpenGL ES 2.0.
:::

### Hiérarchie des os {#the-bone-hierarchy}

Les os du squelette du composant Model sont représentés en interne par des objets de jeu (game object).

Vous pouvez récupérer l’identifiant d’instance de l’objet de jeu d’un os à l’exécution. La fonction [`model.get_go()`](/ref/model#model.get_go) renvoie l’identifiant de l’objet de jeu correspondant à l’os spécifié.

```lua
-- Get the middle bone go of our wiggler model
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Now do something useful with the game object...
```

### Animation du curseur {#cursor-animation}

Outre l’utilisation de `model.play_anim()` pour faire avancer une animation de modèle, les composants *Model* exposent une propriété `cursor` que vous pouvez manipuler avec `go.animate()` (pour en savoir plus, consultez les [animations de propriétés](/manuals/property-animation)) :

```lua
-- Set the animation on #model but don't start it
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Set the cursor to the beginning of the animation
go.set("#model", "cursor", 0)
-- Tween the cursor between 0 and 1 pingpong with in-out quad easing.
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Callbacks de fin d’animation {#completion-callbacks}

La fonction d’animation de modèle `model.play_anim()` accepte une fonction de rappel Lua facultative comme dernier argument. Cette fonction est appelée lorsque l’animation a été lue jusqu’à la fin. Elle n’est jamais appelée pour les animations en boucle, ni lorsqu’une animation est annulée manuellement avec `go.cancel_animations()`. Ce callback peut servir à déclencher des événements à la fin d’une animation ou à enchaîner plusieurs animations.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Done animating
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Modes de lecture {#playback-modes}

Les animations peuvent être lues une seule fois ou en boucle. Le mode de lecture détermine comment l’animation est lue :

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
