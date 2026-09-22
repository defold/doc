---
title: Composant de lumière dans Defold
brief: Ce manuel explique comment utiliser les lumières ambiantes, directionnelles et ponctuelles ainsi que les projecteurs, et comment accéder aux données des lumières dans les shaders.
---

# Composant de lumière {#light-component}

Le composant (component) Light représente une source lumineuse dans une collection. Defold prend actuellement en charge quatre types de ressources de lumière :

- Lumière ambiante (`.ambient_light`)
- Lumière directionnelle (`.directional_light`)
- Lumière ponctuelle (`.point_light`)
- Projecteur (`.spot_light`)

Les ressources de lumière s'ajoutent aux objets de jeu (game objects) comme les autres ressources de composant. Vous pouvez créer des composants de lumière directement sous un objet de jeu, ou créer une ressource de lumière dans le navigateur *Assets*, puis l'ajouter comme composant à un objet de jeu dans la vue *Outline*.

Defold n'applique pas automatiquement l'éclairage à chaque matériau. Le moteur rassemble les lumières et les met à disposition des shaders au moyen du tampon des lumières intégré. Le shader de votre matériau décide comment utiliser les données des lumières.

Les exemples ci-dessous utilisent la même scène pour montrer l'effet des différents types de lumière sur le résultat final :

![Scène sans lumières](images/light/no_light.png)

## Propriétés des lumières {#light-properties}

Toutes les couleurs des lumières sont des valeurs RGB. Le canal alpha n'est pas utilisé par les ressources de lumière.

### Lumière ambiante {#ambient-light}

Les lumières ambiantes ajoutent une lumière constante à la scène. Elles ne sont pas affectées par la position, la rotation ou l'échelle de l'objet de jeu. Elles peuvent servir, par exemple, à fournir un éclairage général d'arrière-plan ou à donner aux objets un aspect indépendant de l'éclairage.

Le composant de lumière ambiante est représenté dans l'éditeur par une icône dont les flèches pointent vers le centre. La couleur de l'icône est celle de sa propriété `color`. 

![Lumière ambiante d'intensité plus faible](images/light/ambient_light_less_intensity.png)

Propriétés :

`color`
: La couleur RGB de la lumière ambiante.

`intensity`
: Multiplie la couleur de la lumière ambiante.

![Lumière ambiante d'intensité plus élevée](images/light/ambient_light_full_intensity.png)

Les lumières ambiantes sont cumulées en une seule couleur ambiante `light_info.xyz` dans le tampon des lumières du shader. Elles n'occupent pas d'entrées dans le tableau `lights[]`. Plusieurs composants de lumière ambiante dans la scène ne produisent qu'une seule couleur de sortie, qui est un mélange de toutes leurs couleurs.

### Lumière directionnelle {#directional-light}

Les lumières directionnelles représentent une lumière provenant d'une seule direction, comme la lumière du soleil. Elles n'utilisent ni la position ni l'échelle de l'objet de jeu, mais la direction de la lumière est obtenue en appliquant la rotation de l'objet de jeu dans le monde à la direction avant locale `(0, 0, -1)`.

Le composant de lumière directionnelle est représenté dans l'éditeur par une icône de soleil colorée accompagnée d'une flèche 3D qui indique sa direction.

![Lumière directionnelle](images/light/directional_light.png)

Propriétés :

`color`
: La couleur RGB de la lumière directionnelle.

`intensity`
: Multiplie la couleur de la lumière directionnelle.


Les lumières directionnelles sont souvent combinées avec une lumière ambiante pour éviter que les surfaces orientées à l'opposé de la lumière directionnelle ne deviennent complètement sombres.

![Lumières directionnelle et ambiante](images/light/directional_and_ambient_light.png)

### Lumière ponctuelle {#point-light}

Les lumières ponctuelles émettent de la lumière vers l'extérieur depuis la position de l'objet de jeu dans le monde. La position de la lumière ponctuelle provient de la position de l'objet de jeu dans le monde.

Le composant de lumière ponctuelle est représenté dans l'éditeur par un point entouré de rayons, dont la couleur correspond à sa propriété `color`, et par un cercle représentant la propriété `range`.

![Lumière ponctuelle](images/light/point_light.png)

Propriétés :

`color`
: La couleur RGB de la lumière ponctuelle.

`intensity`
: Multiplie la couleur de la lumière ponctuelle.

`range`
: Le rayon de la lumière en unités du monde.

La portée effective est multipliée par la plus petite valeur absolue des composantes de l'échelle de l'objet de jeu dans le monde.

![Portée de la lumière ponctuelle](images/light/point_light_range.png)

La modification de la couleur de la lumière teinte la contribution de la lumière ponctuelle, tandis que la portée contrôle la distance jusqu'à laquelle la lumière s'étend depuis la source.

![Portée de la lumière ponctuelle de couleur verte](images/light/point_ight_range_green_color.png)

### Projecteur {#spot-light}

Les projecteurs émettent de la lumière dans un cône depuis la position de l'objet de jeu dans le monde. La direction est obtenue en appliquant la rotation de l'objet de jeu dans le monde à `(0, 0, -1)`.

Le composant de projecteur est représenté dans l'éditeur par une icône de lampe colorée et des lignes de guidage qui montrent les cônes extérieur et intérieur.

![Projecteur](images/light/spot_light.png)

Propriétés :

`color`
: La couleur RGB du projecteur.

`intensity`
: Multiplie la couleur du projecteur.

`range`
: Le rayon de la lumière en unités du monde.

`inner_cone_angle`
: L'angle du cône intérieur, en degrés dans l'éditeur. Les pixels à l'intérieur de ce cône reçoivent la contribution complète du projecteur.

`outer_cone_angle`
: L'angle du cône extérieur, en degrés dans l'éditeur. La lumière s'atténue entre le cône intérieur et le cône extérieur.

La portée effective est multipliée par la plus petite valeur absolue des composantes de l'échelle de l'objet de jeu dans le monde. Les angles des cônes sont modifiés en degrés et convertis en radians dans la ressource de lumière compilée.

![Repères de manipulation du projecteur](images/light/spot_light_gizmos.png)

## Validation {#validation}

La chaîne de build valide et normalise les données des ressources de lumière :

- `color` doit contenir exactement trois nombres.
- `intensity` est bornée à `0` au minimum.
- `range` est bornée à `0` au minimum pour les lumières ponctuelles et les projecteurs.
- Les angles des cônes des projecteurs sont bornés à `0..180` degrés.
- `inner_cone_angle` est borné de sorte qu'il ne dépasse jamais `outer_cone_angle`.

## Limite du projet {#project-limit}

Le nombre maximal de composants de lumière est contrôlé par le paramètre de projet `light.max_count`. La valeur par défaut est `64`.

Les lumières ambiantes n'occupent pas d'entrées dans le tableau `lights[]` du shader, mais elles restent des composants Light et sont comptabilisées dans `light.max_count`. Les lumières directionnelles, les lumières ponctuelles et les projecteurs occupent des entrées dans `lights[]` lorsqu'ils sont actifs.

Si le nombre de composants de lumière dépasse `light.max_count`, le moteur signale une erreur indiquant que le tampon des composants est plein.

## Tampon des lumières dans les shaders {#light-buffer-in-shaders}

Un shader peut accéder aux lumières actives en déclarant un bloc d'uniformes nommé `LightBuffer` avec la disposition intégrée. Le moteur détecte ce bloc et lie automatiquement les données des lumières aux matériaux et aux programmes de calcul qui l'utilisent.

![Shader utilisant le tampon des lumières](images/light/light-buffer-shader.png)

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

Le type de lumière est stocké dans `lights[i].params.x` :

| Type | Valeur |
|------|-------|
| Directionnelle | `0` |
| Ponctuelle | `1` |
| Projecteur | `2` |

Le shader peut déclarer un tableau `lights[]` plus petit que `light.max_count`, mais pas plus grand. Limitez toujours les boucles parcourant les lumières à la taille déclarée du tableau :

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

L'exemple ci-dessus montre comment accéder au tampon. Un véritable shader de lumière ponctuelle ou de projecteur devrait également calculer le vecteur allant du point traité par le shader à `lights[i].position.xyz`, appliquer une atténuation selon la distance à l'aide de `lights[i].direction_range.w` et, pour les projecteurs, utiliser `lights[i].params.z` et `lights[i].params.w` comme angles de cône en radians.

## Utilitaire d'éclairage intégré {#built-in-lighting-helper}

Defold fournit un utilitaire de shader dans `/builtins/materials/lighting.glsl`. Définissez `MAX_LIGHT_COUNT`, fournissez les variables interpolées attendues par l'utilitaire, puis incluez-le dans votre shader de fragment :

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

L'utilitaire définit les constantes `LIGHT_DIRECTIONAL`, `LIGHT_POINT` et `LIGHT_SPOT`, expose `ambient_light()` et fournit des fonctions d'éclairage diffus de Lambert pour les lumières du tampon.

## Voir aussi {#see-also}

- [Manuel des shaders](/manuals/shader)
- [Manuel des matériaux](/manuals/material)
- [Manuel du rendu](/manuals/render)
