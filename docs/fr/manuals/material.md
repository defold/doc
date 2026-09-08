---
title: Manuel des matériaux de Defold
brief: Ce manuel explique comment utiliser les matériaux, les constantes de shader et les échantillonneurs.
---

# Matériaux {#materials}

Les matériaux servent à définir la manière dont un composant (component) graphique (un sprite, une tilemap, une police, un nœud d'interface graphique, un modèle, etc.) doit être rendu.

Un matériau contient des _étiquettes_, des informations utilisées dans le pipeline de rendu pour sélectionner les objets à rendre. Il contient également des références à des _programmes de shader_, qui sont compilés par le pilote graphique disponible, transférés au matériel graphique et exécutés lors du rendu du composant à chaque image.

* Pour plus d'informations sur le pipeline de rendu, consultez la [documentation sur le rendu](/manuals/render).
* Pour une explication approfondie des programmes de shader, consultez la [documentation sur les shaders](/manuals/shader).

## Création d'un matériau {#creating-a-material}

Pour créer un matériau, faites un <kbd>clic droit</kbd> sur un dossier cible dans le navigateur *Assets* et sélectionnez <kbd>New... ▸ Material</kbd>. (Vous pouvez également sélectionner <kbd>File ▸ New...</kbd> dans le menu, puis <kbd>Material</kbd>). Nommez le nouveau fichier de matériau et appuyez sur <kbd>Ok</kbd>.

![Fichier de matériau](images/materials/material_file.png)

Le nouveau matériau s'ouvre dans le *Material Editor*.

![Éditeur de matériaux](images/materials/material.png)

Le fichier de matériau contient les informations suivantes :

Name
: L'identité du matériau. Ce nom permet de répertorier le matériau dans la ressource *Render* afin de l'inclure dans le build. Il est également utilisé dans la fonction `render.enable_material()` de l'API de rendu. Ce nom devrait être unique.

Vertex Program
: Le fichier du programme de shader de sommets (*`.vp`*) à utiliser pour le rendu avec ce matériau. Le programme de shader de sommets s'exécute sur le GPU pour chaque sommet des primitives d'un composant. Il calcule la position de chaque sommet à l'écran et peut aussi produire des variables « varying », qui sont interpolées et transmises en entrée au programme de fragments.

Fragment Program
: Le fichier du programme de shader de fragments (*`.fp`*) à utiliser pour le rendu avec ce matériau. Le programme s'exécute sur le GPU pour chaque fragment (pixel) d'une primitive et détermine la couleur de chaque fragment. Il procède généralement par lectures de textures et calculs à partir des variables d'entrée (variables varying ou constantes).

Vertex Constants
: Les variables uniformes qui seront transmises au programme de shader de sommets. Consultez ci-dessous la liste des constantes disponibles.

Fragment Constants
: Les variables uniformes qui seront transmises au programme de shader de fragments. Consultez ci-dessous la liste des constantes disponibles.

Samplers
: Vous pouvez configurer des échantillonneurs spécifiques dans le fichier de matériau. Ajoutez un échantillonneur, donnez-lui le nom utilisé dans le programme de shader et définissez les paramètres de répétition et de filtrage selon vos besoins.

Tags
: Les étiquettes associées au matériau. Dans le moteur, les étiquettes sont représentées par un _masque de bits_ utilisé par [`render.predicate()`](/ref/render#render.predicate) pour regrouper les composants qui doivent être dessinés ensemble. Consultez la [documentation sur le rendu](/manuals/render) pour savoir comment procéder. Vous pouvez utiliser au maximum 32 étiquettes dans un projet.

## Attributs {#attributes}

Les attributs de shader (également appelés flux de sommets ou attributs de sommet) constituent le mécanisme par lequel le GPU récupère les sommets en mémoire pour rendre la géométrie. Le shader de sommets spécifie un ensemble de flux à l'aide du mot-clé `attribute` et, dans la plupart des cas, Defold produit et lie automatiquement les données en interne d'après les noms des flux. Toutefois, vous pouvez parfois vouloir transmettre davantage de données par sommet pour obtenir un effet particulier que le moteur ne produit pas. Un attribut de sommet peut être configuré à l'aide des champs suivants :

Name
: Le nom de l'attribut. Comme pour les constantes de shader, la configuration de l'attribut n'est utilisée que si elle correspond à un attribut spécifié dans le programme de sommets.

Semantic type
: Un type sémantique indique *ce que* représente l'attribut et/ou *comment* il doit être affiché dans l'éditeur. Par exemple, spécifier un attribut avec `SEMANTIC_TYPE_COLOR` affiche un sélecteur de couleur dans l'éditeur, tandis que les données sont toujours transmises telles quelles du moteur au shader.

  - `SEMANTIC_TYPE_NONE` Le type sémantique par défaut. N'a aucun autre effet sur l'attribut que de transmettre directement les données du matériau pour cet attribut au tampon de sommets (par défaut)
  - `SEMANTIC_TYPE_POSITION` Produit des données de position par sommet pour l'attribut. Peut être utilisé avec l'espace de coordonnées pour indiquer au moteur comment calculer les positions
  - `SEMANTIC_TYPE_TEXCOORD` Produit des coordonnées de texture par sommet pour l'attribut
  - `SEMANTIC_TYPE_PAGE_INDEX` Produit des indices de page par sommet pour l'attribut
  - `SEMANTIC_TYPE_COLOR` Influence la manière dont l'éditeur interprète l'attribut. Si un attribut est configuré avec une sémantique de couleur, un sélecteur de couleur s'affiche dans l'inspecteur
  - `SEMANTIC_TYPE_NORMAL` Produit des données de normale par sommet pour l'attribut
  - `SEMANTIC_TYPE_TANGENT` Produit des données de tangente par sommet pour l'attribut
  - `SEMANTIC_TYPE_WORLD_MATRIX` Produit des données de matrice monde par sommet pour l'attribut
  - `SEMANTIC_TYPE_NORMAL_MATRIX` Produit des données de matrice des normales par sommet pour l'attribut
  - `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D` Produit une matrice de transformation de texture 3x3 par sommet pour l'attribut. Pour les composants de particules, le moteur fournit une matrice qui transforme les coordonnées dans l'espace de l'atlas pour la propriété d'image du composant. Pour les composants sprite, le moteur fournit une matrice pour chaque image utilisée par le composant (lorsque plusieurs textures sont utilisées). Pour les composants de modèle, une matrice identité est fournie.

Data type
: Le type des données sous-jacentes de l'attribut.

  - `TYPE_BYTE` Valeurs d'octets signés sur 8 bits
  - `TYPE_UNSIGNED_BYTE` Valeurs d'octets non signés sur 8 bits
  - `TYPE_SHORT` Valeurs d'entiers courts signés sur 16 bits
  - `TYPE_UNSIGNED_SHORT` Valeurs d'entiers courts non signés sur 16 bits
  - `TYPE_INT` Valeurs d'entiers signés
  - `TYPE_UNSIGNED_INT` Valeurs d'entiers non signés
  - `TYPE_FLOAT` Valeurs à virgule flottante (par défaut)

Normalize
: Si cette option est activée, les valeurs de l'attribut sont normalisées par le pilote du GPU. Cela peut être utile lorsque vous n'avez pas besoin d'une précision maximale, mais souhaitez effectuer un calcul sans connaître les limites exactes. Par exemple, un vecteur de couleur n'a généralement besoin que de valeurs d'octets de 0..255, tout en étant traité comme une valeur de 0..1 dans le shader.

Coordinate space
: Certains types sémantiques permettent de fournir les données dans différents espaces de coordonnées. Pour réaliser un effet de billboarding avec des sprites, vous avez généralement besoin d'un attribut de position dans l'espace local ainsi que d'une position entièrement transformée dans l'espace monde, afin de regrouper les appels de rendu le plus efficacement possible.

Vector type
: Le type de vecteur de l'attribut.

  - `VECTOR_TYPE_SCALAR` Valeur scalaire unique
  - `VECTOR_TYPE_VEC2` Vecteur 2D
  - `VECTOR_TYPE_VEC3` Vecteur 3D
  - `VECTOR_TYPE_VEC4` Vecteur 4D (par défaut)
  - `VECTOR_TYPE_MAT2` Matrice 2D
  - `VECTOR_TYPE_MAT3` Matrice 3D
  - `VECTOR_TYPE_MAT4` Matrice 4D

Step function
: Spécifie comment les données de l'attribut doivent être présentées à la fonction de sommets. Cela ne concerne que l'instanciation.

  - `Vertex` Une fois par sommet ; par exemple, un attribut de position est généralement fourni à la fonction de sommets pour chaque sommet du maillage (par défaut)
  - `Instance` Une fois par instance ; par exemple, un attribut de matrice monde est généralement fourni à la fonction de sommets une fois par instance

Value
: La valeur de l'attribut. Les valeurs d'attribut peuvent être remplacées individuellement pour chaque composant ; sinon, cette valeur sert de valeur par défaut de l'attribut de sommet. Remarque : pour les attributs *par défaut* (position, coordonnées de texture et indices de page), la valeur est ignorée.

::: sidenote
Les attributs personnalisés peuvent également réduire l'empreinte mémoire côté CPU comme côté GPU, en reconfigurant les flux pour utiliser un type de données plus petit ou un nombre d'éléments différent.
:::

### Sémantique par défaut des attributs {#default-attribute-semantics}

À l'exécution, le système de matériaux attribue automatiquement un type sémantique par défaut en fonction du nom de l'attribut, pour un ensemble précis de noms :

  - `position` - type sémantique : `SEMANTIC_TYPE_POSITION`
  - `texcoord0` - type sémantique : `SEMANTIC_TYPE_TEXCOORD`
  - `texcoord1` - type sémantique : `SEMANTIC_TYPE_TEXCOORD`
  - `page_index` - type sémantique : `SEMANTIC_TYPE_PAGE_INDEX`
  - `color` - type sémantique : `SEMANTIC_TYPE_COLOR`
  - `normal` - type sémantique : `SEMANTIC_TYPE_NORMAL`
  - `tangent` - type sémantique : `SEMANTIC_TYPE_TANGENT`
  - `mtx_world` - type sémantique : `SEMANTIC_TYPE_WORLD_MATRIX`
  - `mtx_normal` - type sémantique : `SEMANTIC_TYPE_NORMAL_MATRIX`
  - `mtx_texture_transform_2d` - type sémantique : `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D`

Si le matériau contient des entrées pour ces attributs, le type sémantique par défaut est remplacé par celui que vous avez configuré dans l'éditeur de matériaux.

### Définition des données d'attributs de sommet personnalisés {#setting-custom-vertex-attribute-data}

Comme pour les constantes de shader définies par l'utilisateur, vous pouvez aussi mettre à jour les attributs de sommet à l'exécution en appelant `go.get`, `go.set` et `go.animate` :

![Attribut de matériau personnalisé](images/materials/set_custom_attribute.png)

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

La mise à jour des attributs de sommet présente toutefois certaines limites : la possibilité pour un composant d'utiliser la valeur dépend du type sémantique de l'attribut. Par exemple, un composant sprite prend en charge `SEMANTIC_TYPE_POSITION` ; si vous mettez à jour un attribut de ce type sémantique, le composant ignore la valeur de remplacement, car ce type impose que les données proviennent toujours de la position du sprite.

Les composants de modèle exposent également les attributs de matériau personnalisés par l'intermédiaire de `go.get()`, `go.set()` et `go.animate()`. Par exemple, après avoir défini un attribut nommé `my_attribute` dans le matériau du modèle :

```lua
go.set("#model", "my_attribute", vmath.vector4(1, 0, 0, 1))
go.animate("#model", "my_attribute", go.PLAYBACK_LOOP_PINGPONG,
    vmath.vector4(0, 1, 0, 1), go.EASING_LINEAR, 2)
```

Seul le premier maillage d'un modèle comportant plusieurs maillages peut actuellement être adressé de cette manière. La mise à jour d'un attribut par sommet non instancié peut également reconstruire et transférer une quantité de données de sommets proportionnelle à la taille du maillage ; des mises à jour fréquentes peuvent donc être coûteuses pour les grands maillages.

Lorsqu'un attribut de sommet est un scalaire ou un type de vecteur autre que `Vec4`, vous pouvez quand même définir ses données avec `go.set` :

```lua
-- The last two components in the vec4 will not be used!
go.set("#sprite", "sprite_position_2d", vmath.vector4(my_x,my_y,0,0))
go.animate("#sprite", "sprite_position_2d", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,2,0,0), go.EASING_LINEAR, 2)
```

Il en va de même pour les attributs matriciels : si l'attribut est d'un type de matrice autre que `Mat4`, vous pouvez quand même définir ses données avec `go.set`.

### Exemples d'utilisation d'attributs de sommet personnalisés {#examples-of-using-custom-vertex-attributes}

Utilisation d'un attribut de transformation de texture pour convertir les coordonnées UV dans l'espace de l'atlas :

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

### Instanciation {#instancing}

L'instanciation est une technique qui permet de dessiner efficacement plusieurs copies du même objet dans une scène. Au lieu de créer une copie distincte de l'objet à chaque utilisation, l'instanciation permet au moteur graphique de créer un seul objet, puis de le réutiliser plusieurs fois. Par exemple, dans un jeu comportant une grande forêt, au lieu de créer un modèle d'arbre distinct pour chaque arbre, l'instanciation permet de créer un seul modèle, puis de le placer des centaines ou des milliers de fois avec des positions et des échelles différentes. La forêt peut alors être rendue avec un seul appel de rendu au lieu d'un appel distinct pour chaque arbre.

::: sidenote
L'instanciation n'est actuellement disponible que pour les composants de modèle.
:::

L'instanciation est activée automatiquement lorsque c'est possible. Defold cherche autant que possible à regrouper les appels qui partagent le même état de rendu ; pour que l'instanciation fonctionne, certaines conditions doivent être remplies :

- Le même matériau doit être utilisé pour toutes les instances. L'instanciation fonctionne toujours si un matériau personnalisé a été défini avec `render.enable_material`
- Le matériau doit être configuré pour utiliser l'espace de sommets 'local'
- Le matériau doit avoir au moins un attribut de sommet répété pour chaque instance
- Les valeurs des constantes doivent être identiques pour toutes les instances. Ces valeurs peuvent être placées dans des attributs de sommet personnalisés ou dans un autre support (par exemple, une texture)
- Les ressources des shaders, telles que les textures ou les tampons de stockage, doivent être identiques pour toutes les instances

Pour configurer un attribut de sommet afin qu'il soit répété pour chaque instance, `Step function` doit être réglé sur `Instance`. Cela se fait automatiquement pour certains types sémantiques en fonction du nom (voir le tableau `Default attribute semantics` ci-dessus), mais peut aussi être défini manuellement dans l'éditeur de matériaux en réglant `Step function` sur `Instance`.

À titre d'exemple simple, la scène suivante contient quatre objets de jeu (game objects), chacun doté d'un composant de modèle :

![Configuration de l'instanciation](images/materials/instancing-setup.png)

Le matériau est configuré ainsi, avec un seul attribut de sommet personnalisé répété pour chaque instance :

![Matériau pour l'instanciation](images/materials/instancing-material.png)

Le shader de sommets spécifie plusieurs attributs par instance :

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

Notez que `mtx_world` et `mtx_normal` sont configurés par défaut pour utiliser la fonction de progression `Instance`. Vous pouvez modifier cela dans l'éditeur de matériaux en ajoutant une entrée pour chacun et en réglant `Step function` sur `Vertex`, afin que l'attribut soit répété pour chaque sommet au lieu de chaque instance.

Pour vérifier que l'instanciation fonctionne dans ce cas, vous pouvez consulter le profileur web. Ici, comme seuls les attributs par instance changent entre les instances de la boîte, son rendu peut être effectué en un seul appel :

![Appels de rendu avec instanciation](images/materials/instancing-draw-calls.png)

#### Rétrocompatibilité {#backwards-compatibility}

OpenGL 3.1 sur ordinateur et OpenGL ES 3.0 sur mobile proposent l'instanciation comme fonctionnalité de base. Les anciens contextes OpenGL ES et WebGL peuvent encore la prendre en charge grâce à une extension telle que `ANGLE_instanced_arrays` ; d'autres anciens adaptateurs ne la prennent pas en charge. Lorsque l'instanciation n'est pas disponible, le rendu fonctionne toujours par défaut, mais ses performances peuvent être moindres.

Utilisez `graphics.get_adapter_info()` pour détecter cette prise en charge et sélectionner un matériau moins coûteux ou exclure les contenus comportant beaucoup d'instances si nécessaire. Le champ `features` est un tableau contenant les constantes des fonctionnalités prises en charge, et non une table dont ces constantes seraient les clés :

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

## Constantes de sommets et de fragments {#vertex-and-fragment-constants}

Les constantes de shader, ou « uniformes », sont des valeurs transmises par le moteur aux programmes de shader de sommets et de fragments. Pour utiliser une constante, définissez-la dans le fichier de matériau comme propriété *Vertex Constant* ou *Fragment Constant*. Les variables `uniform` correspondantes doivent être définies dans le programme de shader. Les constantes suivantes peuvent être définies dans un matériau :

`CONSTANT_TYPE_WORLD`
: La matrice monde. Utilisez-la pour transformer les sommets dans l'espace monde. Pour certains types de composants, les sommets sont déjà dans l'espace monde lorsqu'ils arrivent au programme de sommets (en raison du regroupement des appels de rendu). Dans ces cas, une multiplication par la matrice monde dans le shader donne des résultats incorrects.

`CONSTANT_TYPE_VIEW`
: La matrice de vue. Utilisez-la pour transformer les sommets dans l'espace de vue (de la caméra).

`CONSTANT_TYPE_PROJECTION`
: La matrice de projection. Utilisez-la pour transformer les sommets dans l'espace écran.

`CONSTANT_TYPE_VIEWPROJ`
: Une matrice dans laquelle les matrices de vue et de projection ont déjà été multipliées.

`CONSTANT_TYPE_WORLDVIEW`
: Une matrice dans laquelle les matrices monde et de vue ont déjà été multipliées.

`CONSTANT_TYPE_WORLDVIEWPROJ`
: Une matrice dans laquelle les matrices monde, de vue et de projection ont déjà été multipliées.

`CONSTANT_TYPE_WORLD_INVERSE`
: L'inverse de la matrice monde. Utilisez-la pour revenir de l'espace monde à l'espace local de l'objet.

`CONSTANT_TYPE_VIEW_INVERSE`
: L'inverse de la matrice de vue. Utilisez-la pour revenir de l'espace caméra à l'espace monde.

`CONSTANT_TYPE_PROJECTION_INVERSE`
: L'inverse de la matrice de projection. Utilisez-la pour revenir de l'espace de découpage à l'espace caméra.

`CONSTANT_TYPE_VIEWPROJ_INVERSE`
: L'inverse des matrices de vue et de projection combinées. Utilisez-la pour revenir de l'espace de découpage à l'espace monde.

`CONSTANT_TYPE_WORLDVIEW_INVERSE`
: L'inverse des matrices monde et de vue combinées. Utilisez-la pour revenir de l'espace caméra à l'espace local de l'objet.

`CONSTANT_TYPE_WORLDVIEWPROJ_INVERSE`
: L'inverse des matrices monde, de vue et de projection combinées. Utilisez-la pour revenir de l'espace de découpage à l'espace local de l'objet. Ces constantes inverses évitent de calculer l'inverse d'une matrice dans le shader.

`CONSTANT_TYPE_NORMAL`
: Une matrice permettant de calculer l'orientation des normales. La transformation monde peut inclure une mise à l'échelle non uniforme, qui rompt l'orthogonalité de la transformation monde-vue combinée. La matrice des normales permet d'éviter les problèmes de direction lors de la transformation des normales. (La matrice des normales est la transposée de l'inverse de la matrice monde-vue).

`CONSTANT_TYPE_TIME`
: Un `vector4` fourni par le moteur, où `.x` est le temps écoulé depuis le démarrage du moteur, `.y` est le temps écoulé depuis l'image précédente, et `.z` et `.w` valent actuellement zéro. Le moteur met cette valeur à jour automatiquement ; il n'est pas nécessaire de la mettre à jour avec `go.set()`. Consultez le [tutoriel Shadertoy](/tutorials/shadertoy/#animation) pour un exemple.

  Déclarez une constante Time nommée `time` dans un bloc de variables uniformes en GLSL moderne :

  ```glsl
  uniform fragment_inputs
  {
      vec4 time;
  };
  ```

`CONSTANT_TYPE_USER`
: Une constante vector4 que vous pouvez utiliser pour toute donnée personnalisée à transmettre à vos programmes de shader. Vous pouvez définir sa valeur initiale dans la définition de la constante, mais vous pouvez ensuite la modifier avec les fonctions [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate). Vous pouvez également récupérer sa valeur avec [go.get()](/ref/stable/go/#go.get). Modifier une constante de matériau d'une seule instance de composant [rompt le regroupement des appels de rendu et entraîne des appels de rendu supplémentaires](/manuals/render/#draw-calls-and-batching).

Exemple :

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

`CONSTANT_TYPE_USER_MATRIX4`
: Une constante matrix4 que vous pouvez utiliser pour toute donnée personnalisée à transmettre à vos programmes de shader. Vous pouvez définir sa valeur initiale dans la définition de la constante, mais vous pouvez ensuite la modifier avec les fonctions [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate). Vous pouvez également récupérer sa valeur avec [go.get()](/ref/stable/go/#go.get). Modifier une constante de matériau d'une seule instance de composant [rompt le regroupement des appels de rendu et entraîne des appels de rendu supplémentaires](/manuals/render/#draw-calls-and-batching).

Exemple :

```lua
go.set("#sprite", "m", vmath.matrix4())
```

### Constantes de matériau des nœuds d'interface graphique {#gui-node-material-constants}

Dans un script GUI, lisez et écrivez les constantes de matériau d'un nœud avec `gui.get()` et `gui.set()` plutôt qu'avec les fonctions `go`. Les composantes de vecteur, les constantes matricielles et les tableaux de constantes sont pris en charge. Dans la table d'options, les indices de tableau commencent à 1 :

```lua
local node = gui.get_node("button")

local tint = gui.get(node, "tint")
gui.set(node, "tint.x", 0.5)
gui.set(node, "light_matrix", vmath.matrix4())
gui.set(node, "tint_array", vmath.vector4(1, 0, 0, 1), { index = 1 })
```

::: sidenote
Pour qu'une constante de matériau de type `CONSTANT_TYPE_USER` ou `CONSTANT_TYPE_USER_MATRIX4` soit accessible avec `go.get()` et `go.set()`, ou avec `gui.get()` et `gui.set()`, elle doit être utilisée dans le programme de shader. Si la constante est définie dans le matériau mais n'est pas utilisée dans le programme, elle est supprimée du matériau et n'est pas disponible à l'exécution.
:::

## Échantillonneurs {#samplers}

Les échantillonneurs servent à échantillonner les informations de couleur d'une texture (une source de tuiles ou un atlas). Ces informations de couleur peuvent ensuite être utilisées pour les calculs du programme de shader.

Les composants sprite, tilemap, d'interface graphique et d'effet de particules lient automatiquement leur texture d'image au premier `sampler2D` déclaré. Les composants sprite prennent également en charge plusieurs textures : chaque échantillonneur déclaré dans le matériau devient un emplacement d'image nommé dans le composant sprite. La première texture fournit les données d'animation du sprite et détermine la séquence des images. Pour chaque image de l'animation, son identifiant est utilisé pour trouver l'image correspondante dans chaque texture supplémentaire, qui fournit ses propres coordonnées UV. Les atlas ou sources de tuiles affectés devraient donc contenir des identifiants d'images d'animation correspondants et des images de formes similaires ; des formes différentes lors du compactage polygonal peuvent provoquer des débordements de texture. Consultez [Sprites à plusieurs textures](/manuals/sprite/#multi-textured-sprites) pour plus de détails.

Pour un composant ou un flux de travail de rendu qui n'expose pas d'emplacement de texture supplémentaire, utilisez [`render.enable_texture()`](/ref/render/#render.enable_texture) pour lier des échantillonneurs de texture supplémentaires depuis le script de rendu.

![Échantillonneur de sprite](images/materials/sprite_sampler.png)

```glsl
-- mysprite.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D MY_SAMPLER;
void main()
{
    gl_FragColor = texture2D(MY_SAMPLER, var_texcoord0.xy);
}
```

Vous pouvez spécifier les paramètres d'échantillonneur d'un composant en ajoutant l'échantillonneur par son nom dans le fichier de matériau. Si vous ne configurez pas votre échantillonneur dans ce fichier, les paramètres globaux *graphics* du projet sont utilisés.

![Paramètres d'échantillonneur](images/materials/my_sampler.png)

Pour les composants de modèle, vous devez spécifier vos échantillonneurs dans le fichier de matériau avec les paramètres souhaités. L'éditeur vous permet alors de définir des textures pour tout composant de modèle utilisant ce matériau :

![Échantillonneurs de modèle](images/materials/model_samplers.png)

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

![Modèle](images/materials/model.png)

## Paramètres des échantillonneurs {#sampler-settings}

Name
: Le nom de l'échantillonneur. Ce nom devrait correspondre au `sampler2D` déclaré dans le shader de fragments.

Wrap U/W
: Le mode de répétition pour les axes U et V :

  - `WRAP_MODE_REPEAT` répète les données de texture en dehors de l'intervalle [0,1].
  - `WRAP_MODE_MIRRORED_REPEAT` répète les données de texture en dehors de l'intervalle [0,1], mais une répétition sur deux est inversée en miroir.
  - `WRAP_MODE_CLAMP_TO_EDGE` ramène les valeurs supérieures à 1.0 à 1.0 et les valeurs inférieures à 0.0 à 0.0 pour les données de texture---les pixels du bord sont donc répétés jusqu'à la limite.

Filter Min/Mag
: Le filtrage pour l'agrandissement et la réduction. Le filtrage au plus proche voisin demande moins de calculs que l'interpolation linéaire, mais peut produire des artefacts de crénelage. L'interpolation linéaire offre souvent des résultats plus lisses :

  - `Default` utilise l'option de filtrage par défaut spécifiée dans le fichier `game.project`, sous `Graphics`, par les paramètres `Default Texture Min Filter` et `Default Texture Mag Filter`.
  - `FILTER_MODE_NEAREST` utilise le texel dont les coordonnées sont les plus proches du centre du pixel.
  - `FILTER_MODE_LINEAR` calcule une moyenne linéaire pondérée du bloc de texels 2x2 les plus proches du centre du pixel.
  - `FILTER_MODE_NEAREST_MIPMAP_NEAREST` choisit la valeur du texel le plus proche au sein d'un seul mipmap.
  - `FILTER_MODE_NEAREST_MIPMAP_LINEAR` sélectionne le texel le plus proche dans les deux mipmaps les plus adaptés, puis effectue une interpolation linéaire entre ces deux valeurs.
  - `FILTER_MODE_LINEAR_MIPMAP_NEAREST` effectue une interpolation linéaire au sein d'un seul mipmap.
  - `FILTER_MODE_LINEAR_MIPMAP_LINEAR` utilise l'interpolation linéaire pour calculer la valeur dans chacun des deux mipmaps, puis effectue une interpolation linéaire entre ces deux valeurs.

Max Anisotropy
: Le filtrage anisotrope est une technique de filtrage avancée qui prélève plusieurs échantillons et mélange leurs résultats. Ce paramètre contrôle le niveau d'anisotropie des échantillonneurs de texture. Si le GPU ne prend pas en charge le filtrage anisotrope, ce paramètre n'a aucun effet et prend la valeur 1 par défaut.

## Tampons de constantes {#constants-buffers}

Lorsque le pipeline de rendu dessine, il récupère les valeurs des constantes dans le tampon de constantes par défaut du système. Vous pouvez créer un tampon de constantes personnalisé pour remplacer les constantes par défaut et définir les variables uniformes du programme de shader par programmation dans le script de rendu :

```lua
self.constants = render.constant_buffer() -- <1>
self.constants.tint = vmath.vector4(1, 0, 0, 1) -- <2>
...
render.draw(self.my_pred, {constants = self.constants}) -- <3>
```
1. Créez un nouveau tampon de constantes
2. Définissez la constante `tint` sur un rouge vif
3. Dessinez le prédicat en utilisant nos constantes personnalisées

Notez que les constantes du tampon sont référencées comme dans une table Lua ordinaire, mais que vous ne pouvez pas parcourir le tampon avec `pairs()` ou `ipairs()`.
