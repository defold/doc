---
title: Manuel des programmes de calcul Defold
brief: Ce manuel explique comment utiliser les programmes de calcul, les constantes de shader et les échantillonneurs.
---

# Programmes de calcul {#compute-programs}

::: sidenote
La prise en charge des shaders de calcul dans Defold est actuellement en *préversion technique*.
Cela signifie que certaines fonctionnalités manquent encore et que l'API pourrait changer à l'avenir.
:::

Les shaders de calcul sont un outil puissant pour effectuer des calculs à usage général sur le GPU. Ils vous permettent d'exploiter la puissance de traitement parallèle du GPU pour des tâches telles que les simulations physiques, le traitement d'images et bien d'autres. Un shader de calcul opère sur des données stockées dans des tampons ou des textures et effectue des opérations en parallèle sur de nombreux threads du GPU. C'est ce parallélisme qui rend les shaders de calcul si puissants pour les calculs intensifs.

* Pour plus d'informations sur le pipeline de rendu, consultez la [documentation sur le rendu](/manuals/render).
* Pour une explication approfondie des programmes de shader, consultez la [documentation sur les shaders](/manuals/shader).

## Que puis-je faire avec les shaders de calcul ? {#what-can-i-do-with-compute-shaders}

Les shaders de calcul étant destinés au calcul généraliste, leurs possibilités sont pratiquement illimitées. Voici quelques exemples d'utilisations courantes des shaders de calcul :

Traitement d'images
  - Filtrage d'images : appliquer des flous, une détection des contours, un filtre d'accentuation de la netteté, etc.
  - Étalonnage des couleurs : ajuster l'espace colorimétrique d'une image.

Physique
  - Systèmes de particules : simuler un grand nombre de particules pour des effets comme la fumée, le feu et la dynamique des fluides.
  - Physique des corps déformables : simuler des objets déformables comme du tissu et de la gelée.
  - Élimination : élimination par occlusion, élimination hors du volume de vue

Génération procédurale
  - Génération de terrain : créer un terrain détaillé à l'aide de fonctions de bruit.
  - Végétation et feuillage : créer des plantes et des arbres de manière procédurale.

Effets de rendu
  - Illumination globale : simuler un éclairage réaliste en approximant la manière dont la lumière rebondit dans une scène.
  - Voxélisation : créer une grille de voxels 3D à partir de données de maillage.

## Comment fonctionnent les shaders de calcul ? {#how-does-compute-shaders-work}

Dans les grandes lignes, les shaders de calcul divisent une tâche en de nombreuses tâches plus petites pouvant être exécutées simultanément. Ils s'appuient pour cela sur les concepts de groupes de travail (`work groups`) et d'invocations (`invocations`) :

Groupes de travail
: Le shader de calcul opère sur une grille de groupes de travail (`work groups`). Chaque groupe de travail contient un nombre fixe d'invocations (ou threads). La taille des groupes de travail et le nombre d'invocations sont définis dans le code du shader.

Invocations
: Chaque invocation (ou thread) exécute le programme du shader de calcul. Les invocations d'un même groupe de travail peuvent partager des données grâce à une mémoire partagée, ce qui leur permet de communiquer et de se synchroniser efficacement.

Le GPU exécute le shader de calcul en lançant de nombreuses invocations en parallèle dans plusieurs groupes de travail, ce qui offre une puissance de calcul considérable pour les tâches qui s'y prêtent.

## Création d'un programme de calcul {#creating-a-compute-program}

Pour créer un programme de calcul, <kbd>cliquez avec le bouton droit</kbd> sur un dossier cible dans le navigateur *Assets* et sélectionnez <kbd>New... ▸ Compute</kbd>. (Vous pouvez également sélectionner <kbd>File ▸ New...</kbd> dans le menu, puis <kbd>Compute</kbd>). Donnez un nom au nouveau fichier de calcul et appuyez sur <kbd>Ok</kbd>.

![Fichier de calcul](images/compute/compute_file.png)

La nouvelle ressource de calcul s'ouvre dans le *Compute Editor*.

![Éditeur de programmes de calcul](images/compute/compute.png)

Le fichier de calcul contient les informations suivantes :

Compute Program
: Le fichier du programme de shader de calcul (*`.cp`*) à utiliser. Le shader opère sur des « unités de travail abstraites », ce qui signifie qu'il n'existe pas de définition fixe des types de données en entrée et en sortie. Il revient au programmeur de définir ce que le shader de calcul doit produire.

Constants
: Les variables uniformes qui seront transmises au programme de shader de calcul. Vous trouverez ci-dessous une liste des constantes disponibles.

Samplers
: Vous pouvez, si vous le souhaitez, configurer des échantillonneurs spécifiques dans le fichier de matériau. Ajoutez un échantillonneur, donnez-lui le nom utilisé dans le programme de shader et définissez les paramètres de répétition et de filtrage à votre convenance.


## Utilisation du programme de calcul dans Defold {#using-the-compute-program-in-defold}

Contrairement aux matériaux, les programmes de calcul ne sont affectés à aucun composant (component) et ne font pas partie du déroulement normal du rendu. Un programme de calcul doit être lancé (`dispatched`) dans un script de rendu pour effectuer un travail. Avant de le lancer, vous devez toutefois vous assurer que le script de rendu possède une référence au programme de calcul. Actuellement, le seul moyen pour un script de rendu de connaître le programme de calcul est de l'ajouter au fichier .render qui contient la référence à votre script de rendu :

![Fichier de rendu avec un programme de calcul](images/compute/compute_render_file.png)

Pour utiliser le programme de calcul, vous devez d'abord le lier au contexte de rendu. Cela se fait de la même manière que pour les matériaux :

```lua
render.set_compute("my_compute")
-- Do compute work here, call render.set_compute() to unbind
render.set_compute()
```

Les constantes de calcul sont automatiquement appliquées lorsque le programme est lancé, mais il n'est pas possible de lier des ressources d'entrée ou de sortie (textures, tampons, etc.) à un programme de calcul depuis l'éditeur. Vous devez effectuer cette opération à l'aide de scripts de rendu :

```lua
render.enable_texture("blur_render_target", "tex_blur")
render.enable_texture(self.storage_texture, "tex_storage")
```

Pour exécuter le programme dans l'espace de travail que vous avez choisi, vous devez le lancer :

```lua
render.dispatch_compute(128, 128, 1)
-- dispatch_compute also accepts an options table as the last argument
-- you can use this argument table to pass in render constants to the dispatch call
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### Écriture de données depuis des programmes de calcul {#writing-data-from-compute-programs}

Actuellement, un programme de calcul ne peut produire des données de sortie qu'au moyen de textures de stockage (`storage textures`). Une texture de stockage est semblable à une « texture ordinaire », mais offre davantage de fonctionnalités et de possibilités de configuration. Comme leur nom l'indique, les textures de stockage peuvent servir de tampons génériques dans lesquels vous pouvez lire et écrire des données depuis un programme de calcul. Vous pouvez ensuite lier le même tampon à un autre programme de shader pour le lire.

Pour créer une texture de stockage dans Defold, vous devez utiliser un fichier `.script` ordinaire. Les scripts de rendu ne disposent pas de cette fonctionnalité, car les textures dynamiques doivent être créées à l'aide de l'API `resource`, qui n'est disponible que dans les fichiers `.script` ordinaires.

```lua
-- In a .script file:
function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- get the texture handle from the resource
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- notify the renderer of the backing texture, so it can be bound with render.enable_texture
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## Assemblage de tous les éléments {#putting-it-all-together}

### Programme de shader {#shader-program}

```glsl
// compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// specify the input resources
uniform vec4 color;
uniform sampler2D texture_in;

// specify the output image
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // This isn't a particularly interesting shader, but it demonstrates
    // how to read from a texture and constant buffer and write to a storage texture

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // Write the output value to the storage texture
    imageStore(texture_out, tex_coord, output_value);
}
```

### Composant script {#script-component}
```lua
-- In a .script file

-- Here we specify the input texture that we later will bind to the
-- compute program. We can assign this texture to a model component,
-- or enable it to the render context in the render script.
go.property("texture_in", resource.texture())

function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = graphics.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = graphics.TEXTURE_FORMAT_RGBA32F,
        flags  = graphics.TEXTURE_USAGE_FLAG_STORAGE + graphics.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    local textures = {
        texture_in = resource.get_texture_info(self.texture_in).handle,
        texture_out = resource.get_texture_info(t_backing).handle
    }

    -- notify the renderer of the input and output textures
    msg.post("@render:", "set_backing_texture", textures)
end
```

### Script de rendu {#render-script}
```lua
-- respond to the message "set_backing_texture"
-- to set the backing texture for the compute program
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- We can bind textures to specific named constants
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- Dispatch the compute program as many times as we have pixels.
    -- This constitutes our "working group". The shader will be invoked
    -- 128 x 128 x 1 times, or once per pixel.
    render.dispatch_compute(128, 128, 1)
    -- when we are done with the compute program, we need to unbind it
    render.set_compute()
end
```

## Compatibilité {#compatibility}

Defold prend actuellement en charge les shaders de calcul avec les adaptateurs graphiques suivants :

- Vulkan
- Metal (via MoltenVK)
- OpenGL 4.3+
- OpenGL ES 3.1+

Utilisez `graphics.get_adapter_info()` pour vérifier si l'adaptateur graphique actif prend en charge les shaders de calcul. Le champ `features` contient un tableau des constantes de fonctionnalités du contexte prises en charge par l'adaptateur :

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

local compute_shaders_supported = has_context_feature(
    graphics.CONTEXT_FEATURE_COMPUTE_SHADER
)
```

Seules les fonctionnalités prises en charge figurent dans le tableau ; il ne s'agit pas d'une table dont les clés sont les constantes de fonctionnalités. Effectuez toujours cette vérification avant d'utiliser des shaders de calcul lorsque le jeu peut s'exécuter avec différents adaptateurs graphiques ou sur des appareils dont les pilotes offrent des niveaux de prise en charge variables. La prise en charge par OpenGL et OpenGL ES dépend de la version de l'API et du pilote. Vulkan et Metal via MoltenVK prennent en charge les shaders de calcul à partir de la version 1.0. Utilisez un [manifeste d'application](/manuals/app-manifest) pour sélectionner Vulkan sur les plateformes où il n'est pas déjà le backend graphique par défaut.
