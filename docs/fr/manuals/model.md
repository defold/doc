---
title: Modèles 3D dans Defold
brief: Ce manuel décrit comment intégrer des modèles 3D, des squelettes et des animations à votre jeu.
---

# Composant modèle {#model-component}

Defold est fondamentalement un moteur 3D. Même lorsque vous travaillez uniquement avec du contenu 2D, tout le rendu est effectué en 3D, mais projeté à l'écran de manière orthographique. Defold vous permet d'exploiter pleinement le contenu 3D en incluant des ressources 3D, ou _modèles_, dans vos collections. Vous pouvez créer des jeux entièrement en 3D avec uniquement des ressources 3D, ou mélanger du contenu 3D et 2D comme vous le souhaitez.

## Création d'un composant modèle {#creating-a-model-component}

Les composants modèle se créent comme n'importe quel autre composant (component) d'objet de jeu (game object). Vous avez deux possibilités :

- Créez un *fichier modèle* en faisant un <kbd>clic droit</kbd> à un emplacement du navigateur *Assets*, puis en sélectionnant <kbd>New... ▸ Model</kbd>.
- Créez le composant directement intégré à un objet de jeu en faisant un <kbd>clic droit</kbd> sur un objet de jeu dans la vue *Outline*, puis en sélectionnant <kbd>Add Component ▸ Model</kbd>.

![Modèle dans un objet de jeu](images/model/model_gltf.png)

Une fois le modèle créé, vous devez définir plusieurs propriétés :

### Propriétés du modèle {#model-properties}

Outre les propriétés *Id*, *Position* et *Rotation*, les propriétés suivantes sont propres à ce composant :

*Scene*
: Le fichier glTF *.gltf* ou *.glb* qui contient la géométrie du modèle. Si le fichier contient des cibles de morphing, elles sont importées avec la scène. Cette propriété s'appelait *Mesh* avant Defold 1.13.2.

*Mesh*
: Un maillage nommé facultatif de la *Scene* sélectionnée, disponible depuis Defold 1.13.2. Laissez ce champ vide pour afficher toute la scène avec ses transformations importées. Sélectionnez un maillage pour l'afficher une fois dans ses coordonnées locales, sans les transformations des nœuds glTF. Positionnez, faites pivoter et mettez à l'échelle le composant Model ou son objet de jeu pour placer le maillage sélectionné.

*Create GO Bones*
: Cochez cette option pour créer un objet de jeu pour chaque os du modèle. Vous pouvez utiliser ces objets de jeu pour y attacher d'autres objets de jeu, par exemple des armes aux os des mains. 

*Skeleton*
: Cette propriété devrait faire référence au fichier glTF *.gltf* ou *.glb* contenant le squelette à utiliser pour l'animation. Notez que Defold exige un seul os racine dans votre hiérarchie.

*Animations*
: Définissez cette propriété sur le fichier *Animation Set File* contenant les animations que vous souhaitez utiliser sur le modèle.

*Default Animation*
: Il s'agit de l'animation (issue de l'ensemble d'animations) qui sera automatiquement jouée sur le modèle.

En plus des propriétés ci-dessus, un champ permet d'affecter un matériau à chaque maillage du modèle :

*Material*
: Définissez cette propriété sur un matériau que vous avez créé et qui convient à un objet 3D texturé. Plusieurs matériaux intégrés peuvent vous servir de point de départ :

  * Utilisez *model.material* pour les modèles statiques sans instanciation
  * Utilisez *model_instanced.material* pour les modèles statiques avec instanciation
  * Utilisez *model_skinned.material* pour les modèles déformés par squelette (animés) sans instanciation
  * Utilisez *model_skinned_instanced.material* pour les modèles déformés par squelette (animés) avec instanciation

Selon le matériau, une ou plusieurs propriétés de texture sont disponibles :

*Texture*
: Cette propriété devrait pointer vers le fichier image de la texture que vous souhaitez appliquer à l'objet.


## Manipulation dans l'éditeur {#editor-manipulation}

Une fois le composant modèle en place, vous pouvez modifier et manipuler le composant et/ou l'objet de jeu qui le contient à l'aide des outils habituels du *Scene Editor* pour déplacer, faire pivoter et redimensionner le modèle à votre guise.

## Manipulation à l'exécution {#runtime-manipulation}

Vous pouvez manipuler les modèles à l'exécution à l'aide de diverses fonctions et propriétés (consultez la [documentation de l'API pour leur utilisation](/ref/model/)).

![Wiggler dans le jeu](images/model/runtime.png)

### Animation à l'exécution {#runtime-animation}

Defold offre des fonctions puissantes pour contrôler l'animation à l'exécution. Vous trouverez plus d'informations dans le [manuel sur l'animation des modèles](/manuals/model-animation) :

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

Le curseur de lecture de l'animation peut être animé manuellement ou par le système d'animation des propriétés :

```lua
-- set the run animation
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- animate the cursor
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

Les modèles peuvent également utiliser les animations de cibles de morphing glTF. Les poids des cibles de morphing sont animés avec `model.play_anim()` comme les autres animations de modèle, et peuvent être lus ou remplacés à l'exécution à l'aide de [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) et de [`model.set_blend_weights()`](/ref/model#model.set_blend_weights). Consultez la [section sur les cibles de morphing](/manuals/model-animation#morph-targets) du manuel sur l'animation des modèles pour plus de détails.

### Modification des propriétés {#changing-properties}

Un modèle possède également diverses propriétés que vous pouvez manipuler à l'aide de `go.get()` et de `go.set()` :

`animation`
: L'animation actuelle du modèle (`hash`) (LECTURE SEULE). Vous changez d'animation à l'aide de `model.play_anim()` (voir ci-dessus).

`cursor`
: Le curseur normalisé de l'animation (`number`).

`material`
: Le matériau du modèle (`hash`). Vous pouvez le changer à l'aide d'une propriété de ressource de matériau et de `go.set()`. Consultez la [référence de l'API pour un exemple](/ref/model/#material).

`playback_rate`
: La vitesse de lecture de l'animation (`number`).

`textureN`
: Les textures du modèle, où N va de 0 à 15 (`hash`). Vous pouvez lire ces propriétés avec `go.get()` et les modifier à l'aide d'une propriété de ressource de texture et de `go.set()`. Defold prend en charge au plus 16 textures par opération de dessin, mais le nombre utilisable par un shader peut être inférieur sur les adaptateurs graphiques dont la limite d'échantillonneurs de textures est plus basse.


## Matériau {#material}

Les logiciels 3D vous permettent généralement de définir des propriétés sur les sommets de vos objets, comme la couleur et les textures. Ces informations sont enregistrées dans le fichier glTF *.gltf* ou *.glb* que vous exportez depuis votre logiciel 3D. Selon les besoins de votre jeu, vous devrez sélectionner et/ou créer des matériaux adaptés et _performants_ pour vos objets. Un matériau combine des _programmes de shader_ avec un ensemble de paramètres pour le rendu de l'objet.

Plusieurs matériaux intégrés peuvent vous servir de point de départ :

  * Utilisez *model.material* pour les modèles statiques sans instanciation
  * Utilisez *model_instanced.material* pour les modèles statiques avec instanciation
  * Utilisez *model_skinned.material* pour les modèles déformés par squelette (animés) sans instanciation
  * Utilisez *model_skinned_instanced.material* pour les modèles déformés par squelette (animés) avec instanciation

Les matériaux de modèle intégrés utilisent l'espace local des sommets. Pour les modèles déformés par squelette, l'espace local des sommets permet au shader de sommets d'effectuer la déformation sur le GPU à l'aide d'une texture de matrices d'os ; l'espace local des sommets est également requis pour l'instanciation des modèles. Un matériau personnalisé destiné aux modèles déformés par squelette sur le GPU ou utilisant l'instanciation devrait donc utiliser le paramètre *Local* pour l'espace des sommets.

Le cache des matrices d'os utilise une texture `RGBA32F`. Si l'adaptateur graphique actif ne prend pas en charge ce format de texture, Defold ne peut pas créer de composant modèle animé utilisant un matériau en espace local. Sur OpenGL ES 2.0 et WebGL 1.0, la prise en charge dépend donc de l'extension de l'adaptateur pour les textures à virgule flottante. Pour assurer la compatibilité avec un adaptateur qui n'en dispose pas, utilisez un matériau personnalisé en espace monde, qui effectue la déformation par squelette sur le CPU et ne permet pas l'instanciation des modèles. Vous pouvez ajuster les dimensions du cache à l'aide des [paramètres Model du projet](/manuals/project-settings/#model).

Si vous devez créer des matériaux personnalisés pour vos modèles, consultez la [documentation sur les matériaux](/manuals/material). Le [manuel sur les shaders](/manuals/shader) explique le fonctionnement des programmes de shader.


### Constantes de matériau {#material-constants}

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: La teinte du modèle (`vector4`). Le `vector4` représente la teinte, x, y, z et w correspondant respectivement aux composantes rouge, verte, bleue et alpha de la teinte.


## Rendu {#rendering}

Le script de rendu par défaut est conçu pour les jeux 2D et ne fonctionne pas avec les modèles 3D. Toutefois, en copiant le script de rendu par défaut et en y ajoutant quelques lignes de code, vous pouvez activer le rendu de vos modèles. Par exemple :

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- orthographic
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

Consultez la [documentation sur le rendu](/manuals/render) pour plus de détails sur le fonctionnement des scripts de rendu.
