---
title: Programmes shaders dans Defold
brief: Ce manuel décrit en détail les shaders de sommets et de fragments et explique comment les utiliser dans Defold.
---

# Shaders {#shaders}

Les programmes shaders sont au cœur du rendu graphique. Ce sont des programmes écrits dans un langage proche du C appelé GLSL (GL Shading Language), que le matériel graphique exécute pour effectuer des opérations sur les données 3D sous-jacentes (les sommets) ou sur les pixels qui apparaissent à l'écran (les « fragments »). Les shaders servent à dessiner des sprites, à éclairer des modèles 3D, à créer des effets de post-traitement plein écran et à bien d'autres choses encore.

Ce manuel décrit comment le pipeline de rendu de Defold interagit avec les shaders du GPU. Pour créer des shaders pour votre contenu, vous devez également comprendre le concept de matériau ainsi que le fonctionnement du pipeline de rendu.

* Consultez le [manuel du rendu](/manuals/render) pour en savoir plus sur le pipeline de rendu.
* Consultez le [manuel des matériaux](/manuals/material) pour en savoir plus sur les matériaux.
* Consultez le [manuel des programmes de calcul](/manuals/compute) pour en savoir plus sur les programmes de calcul.

Les spécifications d'OpenGL ES 2.0 (OpenGL for Embedded Systems) et d'OpenGL ES Shading Language sont disponibles dans le [registre OpenGL de Khronos](https://www.khronos.org/registry/gles/).

Sur les ordinateurs de bureau, il est possible d'écrire des shaders qui utilisent des fonctionnalités indisponibles dans OpenGL ES 2.0. Le pilote de votre carte graphique peut parfaitement compiler et exécuter du code de shader qui ne fonctionnera pas sur les appareils mobiles.


## Concepts {#concepts}

Shader de sommets
: Un shader de sommets ne peut ni créer ni supprimer des sommets, seulement modifier la position d'un sommet. Les shaders de sommets servent généralement à transformer les positions des sommets de l'espace monde 3D vers l'espace écran 2D.

  Un shader de sommets reçoit en entrée des données de sommets (sous forme d'`attributes`) et des constantes (`uniforms`). Parmi les constantes courantes figurent les matrices nécessaires pour transformer et projeter la position d'un sommet dans l'espace écran.

  La sortie du shader de sommets est la position calculée du sommet à l'écran (`gl_Position`). Il est également possible de transmettre des données du shader de sommets au shader de fragments au moyen de variables `varying`.

Shader de fragments
: Une fois le shader de sommets terminé, le shader de fragments détermine la couleur de chaque fragment (ou pixel) des primitives obtenues.

  Un shader de fragments reçoit en entrée des constantes (`uniforms`) ainsi que les variables `varying` définies par le shader de sommets.

  La sortie du shader de fragments est la valeur de couleur du fragment concerné (`gl_FragColor`).

Shader de calcul
: Un shader de calcul est un shader généraliste qui peut servir à effectuer tout type de travail sur un GPU. Il ne fait pas partie du pipeline graphique : les shaders de calcul s'exécutent dans un contexte d'exécution distinct et ne dépendent d'aucune donnée provenant d'un autre shader.

  Un shader de calcul reçoit en entrée des tampons de constantes (`uniforms`), des images de texture (`image2D`), des échantillonneurs (`sampler2D`) et des tampons de stockage (`buffer`).

  La sortie du shader de calcul n'est pas définie explicitement : aucune sortie particulière ne doit être produite, contrairement aux shaders de sommets et de fragments. Les shaders de calcul étant généralistes, c'est au programmeur de définir le type de résultat que le shader de calcul doit produire.

Matrice monde
: Les positions des sommets qui constituent la forme d'un modèle sont stockées relativement à l'origine du modèle. C'est ce que l'on appelle l'« espace modèle ». Le monde de jeu (game world), en revanche, est un « espace monde » où la position, l'orientation et l'échelle de chaque sommet sont exprimées relativement à l'origine du monde. En séparant ces deux espaces, le moteur de jeu peut déplacer, faire pivoter et redimensionner chaque modèle sans détruire les valeurs d'origine des sommets stockées dans le composant (component) de modèle.

  Lorsqu'un modèle est placé dans le monde de jeu, les coordonnées locales de ses sommets doivent être converties en coordonnées monde. Cette conversion est effectuée par une *matrice de transformation monde*, qui indique la translation (déplacement), la rotation et l'échelle à appliquer aux sommets d'un modèle pour les placer correctement dans le système de coordonnées du monde de jeu.

  ![Transformation monde](images/shader/world_transform.png)

Matrices de vue et de projection
: Pour placer les sommets du monde de jeu à l'écran, les coordonnées 3D de chaque matrice sont d'abord converties en coordonnées relatives à la caméra. Cette opération est effectuée à l'aide d'une _matrice de vue_. Les sommets sont ensuite projetés dans l'espace écran 2D à l'aide d'une _matrice de projection_ :

  ![Projection](images/shader/projection.png)

Attributs
: Une valeur associée à un sommet individuel. Les attributs sont transmis au shader par le moteur ; pour accéder à un attribut, il vous suffit de le déclarer dans votre programme shader. Chaque type de composant dispose d'un ensemble d'attributs différent :
  - Un sprite possède `position` et `texcoord0`.
  - Tilegrid possède `position` et `texcoord0`.
  - Un nœud d'interface graphique possède `position`, `textcoord0` et `color`.
  - ParticleFX possède `position`, `texcoord0` et `color`.
  - Un modèle possède `position`, `texcoord0` et `normal`.
  - Une police possède `position`, `texcoord0`, `face_color`, `outline_color` et `shadow_color`.

Constantes
: Les constantes d'un shader restent constantes pendant toute la durée de l'appel de dessin du rendu. Les constantes sont ajoutées aux sections *Constants* du fichier de matériau, puis déclarées comme `uniform` dans le programme shader. Les variables uniformes d'échantillonneur sont ajoutées à la section *Samplers* du matériau, puis déclarées comme `uniform` dans le programme shader. Les matrices nécessaires pour effectuer les transformations de sommets dans un shader de sommets sont disponibles sous forme de constantes :

  - `CONSTANT_TYPE_WORLD` est la *matrice monde* qui transforme les coordonnées de l'espace local d'un objet en coordonnées de l'espace monde.
  - `CONSTANT_TYPE_VIEW` est la *matrice de vue* qui transforme les coordonnées de l'espace monde en coordonnées de l'espace caméra.
  - `CONSTANT_TYPE_PROJECTION` est la *matrice de projection* qui transforme les coordonnées de l'espace caméra en coordonnées de l'espace écran.
  - `CONSTANT_TYPE_WORLDVIEW`, `CONSTANT_TYPE_VIEWPROJ` et `CONSTANT_TYPE_WORLDVIEWPROJ` fournissent les matrices combinées correspondantes.
  - `CONSTANT_TYPE_WORLD_INVERSE`, `CONSTANT_TYPE_VIEW_INVERSE`, `CONSTANT_TYPE_PROJECTION_INVERSE`, `CONSTANT_TYPE_VIEWPROJ_INVERSE`, `CONSTANT_TYPE_WORLDVIEW_INVERSE` et `CONSTANT_TYPE_WORLDVIEWPROJ_INVERSE` fournissent les matrices inverses sans que le shader ait à les calculer.
  - `CONSTANT_TYPE_TIME` est un `vec4` fourni par le moteur : le temps écoulé depuis le démarrage du moteur dans `.x`, le temps écoulé depuis l'image précédente dans `.y`, et zéro dans `.z` et `.w`.
  - `CONSTANT_TYPE_USER` est une constante de type `vec4` que vous pouvez utiliser comme vous le souhaitez.

  Le [manuel des matériaux](/manuals/material) explique comment spécifier les constantes.

Échantillonneurs
: Les shaders peuvent déclarer des variables uniformes de type *sampler*. Les échantillonneurs servent à lire des valeurs dans une image source :

  - `sampler2D` échantillonne une texture d'image 2D.
  - `sampler2DArray` échantillonne une texture de tableau d'images 2D. Ce type est principalement utilisé pour les atlas paginés.
  - `samplerCube` échantillonne une texture cubique composée de six images.
  - `image2D` charge (et peut stocker) des données de texture dans un objet image. Ce type est principalement utilisé pour le stockage dans les shaders de calcul.

  Vous ne pouvez utiliser un échantillonneur que dans les fonctions de lecture de texture de la bibliothèque standard GLSL. Le [manuel des matériaux](/manuals/material) explique comment spécifier les paramètres des échantillonneurs.

Coordonnées UV
: Une coordonnée 2D est associée à un sommet et correspond à un point sur une texture 2D. Une partie ou la totalité de la texture peut donc être appliquée à la forme décrite par un ensemble de sommets.

  ![Coordonnées UV](images/shader/uv_map.png)

  Une carte UV est généralement générée dans le logiciel de modélisation 3D et stockée dans le maillage. Les coordonnées de texture de chaque sommet sont fournies au shader de sommets sous forme d'attribut. Une variable `varying` sert ensuite à déterminer les coordonnées UV de chaque fragment, par interpolation des valeurs des sommets.

Variables interpolées
: Les variables de type `Varying` servent à transmettre des informations entre l'étape de traitement des sommets et l'étape de traitement des fragments.

  1. Une variable interpolée est définie dans le shader de sommets pour chaque sommet.
  2. Pendant la rastérisation, cette valeur est interpolée pour chaque fragment de la primitive en cours de rendu. La distance entre le fragment et les sommets de la forme détermine la valeur interpolée.
  3. La variable est définie pour chaque appel au shader de fragments et peut être utilisée dans les calculs du fragment.

  ![Interpolation des variables](images/shader/varying_vertex.png)

  Par exemple, attribuer à une variable `varying` une valeur de couleur RVB de type `vec3` à chaque sommet d'un triangle permet d'interpoler les couleurs sur toute la forme. De même, définir des coordonnées de lecture dans une texture (ou *coordonnées UV*) à chaque sommet d'un rectangle permet au shader de fragments de lire les valeurs de couleur de la texture sur toute la surface de la forme.

  ![Interpolation des variables](images/shader/varying.png)

## Écrire des shaders GLSL modernes {#writing-modern-glsl-shaders}

Comme le moteur Defold prend en charge plusieurs plateformes et API graphiques, les développeurs doivent pouvoir écrire facilement des shaders qui fonctionnent partout. Le pipeline de ressources y parvient principalement de deux manières (appelées désormais `shader pipelines`) :

1. Le pipeline historique, dans lequel les shaders sont écrits en code GLSL compatible avec ES2.
2. Le pipeline moderne, dans lequel les shaders sont écrits en code GLSL compatible avec SPIR-v.

À partir de Defold 1.9.2, il est recommandé d'écrire des shaders qui utilisent le nouveau pipeline. Pour cela, la plupart des shaders doivent être migrés vers des shaders écrits au minimum en version 140 (OpenGL 3.1). Pour migrer un shader, assurez-vous que les exigences suivantes sont respectées :

### Déclaration de version {#version-declaration}
Placez au minimum #version 140 au début du shader :

```glsl
#version 140
```

C'est ainsi que le pipeline du shader est choisi lors du build, ce qui vous permet de continuer à utiliser les anciens shaders. Si aucune directive de préprocesseur indiquant la version n'est trouvée, Defold utilise le pipeline historique.

### Attributs {#attributes}
Dans les shaders de sommets, remplacez le mot-clé `attribute` par `in` :

```glsl
// instead of:
// attribute vec4 position;
// do:
in vec4 position;
```

Remarque : les shaders de fragments (et les shaders de calcul) ne reçoivent aucune donnée de sommet en entrée.

### Variables interpolées {#varyings}
Dans les shaders de sommets, les variables interpolées doivent être précédées de `out`. Dans les shaders de fragments, elles deviennent des variables `in` :

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

### Variables uniformes (appelées constantes dans Defold) {#uniforms-called-constants-in-defold}

Les types de variables uniformes opaques (échantillonneurs, images, compteurs atomiques, SSBO) ne nécessitent aucune migration ; vous pouvez les utiliser comme vous le faites aujourd'hui :

```glsl
uniform sampler2D my_texture;
uniform image2D my_image;
```

Pour les types de variables uniformes non opaques, vous devez les placer dans un `uniform block`. Un bloc de variables uniformes est simplement un ensemble de variables uniformes, déclaré avec le mot-clé `uniform` :

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

Tous les membres du bloc de variables uniformes sont exposés aux matériaux et aux composants sous forme de constantes individuelles. Aucune migration n'est nécessaire pour utiliser les tampons de constantes de rendu, ni `go.set` et `go.get`.

### Variables intégrées {#built-in-variables}

Dans les shaders de fragments, `gl_FragColor` est obsolète à partir de la version 140. Utilisez `out` à la place :

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

### Fonctions de texture {#texture-functions}

Les fonctions spécifiques d'échantillonnage de texture, telles que `texture2D` et `texture2DArray`, n'existent plus. Utilisez simplement la fonction `texture` à la place :

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

### Précision {#precision}

Defold génère des qualificateurs globaux de précision par défaut lors de la compilation croisée des shaders vers GLSL ES. Les valeurs par défaut sont `mediump` pour les valeurs à virgule flottante et `highp` pour les entiers. Vous pouvez les modifier à l'aide des [paramètres du projet](/manuals/project-settings/#shader) **GLSL ES Default Precision Float** (`shader.glsl_es_default_precision_float`) et **GLSL ES Default Precision Int** (`shader.glsl_es_default_precision_int`) ; tous deux acceptent `mediump` ou `highp`.

Un qualificateur explicite sur une variable, une entrée ou une sortie a priorité sur la valeur globale par défaut générée. Dans les shaders de fragments OpenGL ES 2.0 et WebGL 1.0, `highp` n'est pas pris en charge par tous les appareils. Lorsque `highp` est choisi comme valeur globale par défaut, Defold le protège avec `GL_FRAGMENT_PRECISION_HIGH` et utilise `mediump` sur les appareils qui ne le prennent pas en charge.

### Exemple complet {#putting-it-together}

Voici, comme dernier exemple appliquant l'ensemble de ces règles, les shaders de sprite intégrés convertis au nouveau format :

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

## Inclure des extraits de code dans les shaders {#including-snippets-into-shaders}

Les shaders de Defold permettent d'inclure du code source provenant de fichiers du projet portant l'extension `.glsl`. Pour inclure un fichier glsl depuis un shader, utilisez la directive `#include` avec des guillemets doubles ou des chevrons. Les chemins d'inclusion doivent être relatifs au projet ou au fichier qui effectue l'inclusion :

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

La prise en compte des inclusions présente quelques particularités :

  - Les fichiers doivent être relatifs au projet : vous ne pouvez inclure que des fichiers situés à l'intérieur du projet. Tout chemin absolu doit commencer par `/`
  - Vous pouvez inclure du code n'importe où dans le fichier, mais vous ne pouvez pas inclure un fichier au milieu d'une instruction. Par exemple, `const float #include "my-float-name.glsl" = 1.0` ne fonctionnera pas

### Gardes d'inclusion {#header-guards}

Les extraits de code peuvent eux-mêmes inclure d'autres fichiers `.glsl`. Le shader final peut donc contenir plusieurs fois le même code et, selon le contenu des fichiers, vous pouvez rencontrer des problèmes de compilation si les mêmes symboles sont déclarés plusieurs fois. Pour éviter cela, vous pouvez utiliser des *gardes d'inclusion*, un concept courant dans plusieurs langages de programmation. Exemple :

```glsl
// In my-shader.vs
#include "math-functions.glsl"
#include "pi.glsl"

// In math-functions.glsl
#include "pi.glsl"

// In pi.glsl
const float PI = 3.14159265359;
```

Dans cet exemple, la constante `PI` sera définie deux fois, ce qui provoquera des erreurs de compilation lors de l'exécution du projet. Vous devriez donc protéger le contenu à l'aide de gardes d'inclusion :

```glsl
// In pi.glsl
#ifndef PI_GLSL_H
#define PI_GLSL_H

const float PI = 3.14159265359;

#endif // PI_GLSL_H
```

Le code de `pi.glsl` sera développé deux fois dans `my-shader.vs`, mais comme vous l'avez entouré de gardes d'inclusion, le symbole PI ne sera défini qu'une seule fois et le shader sera compilé correctement.

Cependant, selon le cas d'utilisation, cette protection n'est pas toujours strictement nécessaire. Si vous souhaitez réutiliser du code localement dans une fonction ou à un autre endroit où les valeurs n'ont pas besoin d'être disponibles globalement dans le code du shader, vous devriez probablement vous passer de gardes d'inclusion. Exemple :

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

## Code de shader propre à l'éditeur {#editor-specific-shader-code}

Lorsque les shaders sont rendus dans la fenêtre d'affichage de l'éditeur Defold, une définition de préprocesseur `EDITOR` est disponible. Elle vous permet d'écrire du code de shader qui se comporte différemment dans l'éditeur et dans le moteur de jeu lui-même.

Cela est particulièrement utile pour :
  - Ajouter des visualisations de débogage qui ne doivent apparaître que dans l'éditeur.
  - Implémenter des fonctionnalités propres à l'éditeur, comme des modes filaires ou des aperçus de matériaux.
  - Fournir un rendu de secours pour les matériaux qui pourraient ne pas fonctionner correctement dans la fenêtre d'affichage de l'éditeur.

Utilisez la directive de préprocesseur `#ifdef EDITOR` pour compiler conditionnellement le code qui ne doit s'exécuter que dans l'éditeur :

```glsl
#ifdef EDITOR
    // This code will only execute when the shader is rendered in the Defold Editor
    color_out = vec4(1.0, 0.0, 1.0, 1.0); // Magenta color for editor preview
#else
    // This code will execute when running in the game
    color_out = texture(texture_sampler, var_texcoord0) * tint_pm;
#endif
```

## Le processus de rendu {#the-rendering-process}

Avant d'apparaître à l'écran, les données que vous créez pour votre jeu passent par une série d'étapes :

![Pipeline de rendu](images/shader/pipeline.png)

Tous les composants visuels (sprites, nœuds d'interface graphique, effets de particules ou modèles) sont constitués de sommets, des points du monde 3D qui décrivent la forme du composant. Cela permet d'observer la forme sous n'importe quel angle et à n'importe quelle distance. Le rôle du shader de sommets est de prendre un sommet et de le convertir en une position dans la fenêtre d'affichage pour que la forme puisse apparaître à l'écran. Pour une forme à quatre sommets, le programme shader de sommets s'exécute quatre fois, en parallèle.

![Shader de sommets](images/shader/vertex_shader.png)

Le programme reçoit en entrée la position du sommet (et les autres données d'attribut associées au sommet) et produit en sortie une nouvelle position de sommet (`gl_Position`), ainsi que les variables `varying` à interpoler pour chaque fragment.

Le programme shader de sommets le plus simple se contente de placer le sommet de sortie à l'origine (ce qui n'est pas très utile) :

```glsl
void main()
{
    gl_Position = vec4(0.0,0.0,0.0,1.0);
}
```

Un exemple plus complet est le shader de sommets intégré pour les sprites :

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
1. Une variable uniforme (constante) contenant le produit des matrices de vue et de projection.
2. Les attributs du sommet du sprite. `position` est déjà transformé dans l'espace monde. `texcoord0` contient les coordonnées UV du sommet.
3. Déclarez une variable interpolée de sortie. Sa valeur sera interpolée pour chaque fragment entre les valeurs définies pour chaque sommet, puis transmise au shader de fragments.
4. `gl_Position` reçoit la position de sortie du sommet actuel dans l'espace de projection. Cette valeur a quatre composantes : `x`, `y`, `z` et `w`. La composante `w` sert à calculer une interpolation corrigée pour la perspective. Cette valeur est normalement de 1.0 pour chaque sommet avant l'application d'une matrice de transformation.
5. Définissez les coordonnées UV interpolées pour cette position de sommet. Après la rastérisation, elles seront interpolées pour chaque fragment et transmises au shader de fragments.




Après le traitement des sommets, la forme du composant à l'écran est déterminée : des primitives sont générées et rastérisées, c'est-à-dire que le matériel graphique divise chaque forme en *fragments*, ou pixels. Il exécute ensuite le programme shader de fragments une fois pour chaque fragment. Pour une image à l'écran de 16x24 pixels, le programme s'exécute 384 fois, en parallèle.

![Shader de fragments](images/shader/fragment_shader.png)

Le programme reçoit en entrée les données envoyées par le pipeline de rendu et le shader de sommets, généralement les *coordonnées UV* du fragment, les couleurs de teinte, etc. La sortie est la couleur finale du pixel (`gl_FragColor`).

Le programme shader de fragments le plus simple se contente de définir la couleur de chaque pixel sur le noir (là encore, ce programme n'est pas très utile) :

```glsl
void main()
{
    gl_FragColor = vec4(0.0,0.0,0.0,1.0);
}
```

Là encore, un exemple plus complet est le shader de fragments intégré pour les sprites :

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
1. La variable interpolée de coordonnées de texture est déclarée. Sa valeur sera interpolée pour chaque fragment entre les valeurs définies pour chaque sommet de la forme.
2. Une variable uniforme `sampler2D` est déclarée. L'échantillonneur, associé aux coordonnées de texture interpolées, sert à lire la texture pour l'appliquer correctement au sprite. Comme il s'agit d'un sprite, le moteur associera cet échantillonneur à l'image définie dans la propriété *Image* du sprite.
3. Une constante de type `CONSTANT_TYPE_USER` est définie dans le matériau et déclarée comme `uniform`. Sa valeur permet de teinter le sprite. La valeur par défaut est le blanc pur.
4. La valeur de couleur de la teinte est prémultipliée par sa valeur alpha, car toutes les textures utilisées à l'exécution contiennent déjà un alpha prémultiplié.
5. Échantillonnez la texture aux coordonnées interpolées et renvoyez la valeur échantillonnée.
6. `gl_FragColor` reçoit la couleur de sortie du fragment : la couleur diffuse de la texture multipliée par la valeur de teinte.

La valeur du fragment obtenu est ensuite soumise à des tests. Un test courant est le *test de profondeur*, qui compare la profondeur du fragment à la valeur du tampon de profondeur pour le pixel testé. Selon le test, le fragment peut être rejeté ou une nouvelle valeur peut être écrite dans le tampon de profondeur. Ce test sert couramment à permettre aux éléments graphiques les plus proches de la caméra de masquer ceux qui sont plus éloignés.

Si le test conclut que le fragment doit être écrit dans le tampon d'image, il sera *mélangé* aux données du pixel déjà présentes dans le tampon. Les paramètres de mélange définis dans le script de rendu permettent de combiner de différentes manières la couleur source (la valeur écrite par le shader de fragments) et la couleur de destination (la couleur de l'image dans le tampon d'image). Le mélange sert couramment à rendre des objets transparents.

## Pour approfondir {#further-study}

- [Shadertoy](https://www.shadertoy.com) contient un très grand nombre de shaders proposés par les utilisateurs. C'est une excellente source d'inspiration pour découvrir diverses techniques de rendu par shaders. De nombreux shaders présentés sur le site peuvent être portés vers Defold avec très peu de travail. Le [tutoriel Shadertoy](https://www.defold.com/tutorials/shadertoy/) détaille les étapes de conversion d'un shader existant vers Defold.

- Le [tutoriel sur l'étalonnage des couleurs](https://www.defold.com/tutorials/grading/) montre comment créer un effet d'étalonnage des couleurs plein écran à l'aide de textures de tables de correspondance des couleurs.

- [The Book of Shaders](https://thebookofshaders.com/00/) vous apprendra à utiliser et à intégrer des shaders dans vos projets pour améliorer leurs performances et leur qualité graphique.
