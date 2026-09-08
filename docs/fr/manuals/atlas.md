---
title: Manuel des atlas
brief: Ce manuel explique le fonctionnement des ressources atlas dans Defold.
---

# Atlas {#atlas}

Bien que des images individuelles soient souvent utilisées comme source pour les sprites, il faut, pour des raisons de performances, les regrouper dans des ensembles d'images plus grands, appelés atlas. Le regroupement de petites images dans des atlas est particulièrement important sur les appareils mobiles, où la mémoire et la puissance de calcul sont plus limitées que sur les ordinateurs de bureau ou les consoles de jeu dédiées.

Dans Defold, une ressource atlas est une liste de fichiers image distincts, qui sont automatiquement combinés en une image plus grande.

## Création d'un atlas {#creating-an-atlas}

Sélectionnez <kbd>New... ▸ Atlas</kbd> dans le menu contextuel du navigateur *Assets*. Nommez le nouveau fichier atlas. L'éditeur ouvre alors le fichier dans l'éditeur d'atlas. Les propriétés de l'atlas sont affichées dans le
panneau *Properties*, où vous pouvez les modifier (voir les détails ci-dessous).

Vous devez remplir un atlas avec des images ou des animations avant de pouvoir l'utiliser comme source graphique pour un composant (component) d'objet de jeu (game object), comme un composant sprite ou ParticleFX.

Assurez-vous d'avoir ajouté vos images au projet (glissez-déposez les fichiers image à l'emplacement voulu dans le navigateur *Assets*)

Ajout d'images individuelles

: Glissez-déposez des images du panneau *Asset* vers la vue de l'éditeur.
  
  Vous pouvez aussi faire un <kbd>clic droit</kbd> sur l'entrée racine Atlas dans le panneau *Outline*.

  Sélectionnez <kbd>Add Images</kbd> dans le menu contextuel pour ajouter des images individuelles.

  Une boîte de dialogue s'ouvre pour vous permettre de rechercher et de sélectionner les images à ajouter à l'atlas. Vous pouvez filtrer les fichiers image et sélectionner plusieurs fichiers à la fois.

  ![Création d'un atlas, ajout d'images](images/atlas/add.png)

  Les images ajoutées sont répertoriées dans *Outline* et l'atlas complet est visible dans la vue centrale de l'éditeur. Vous devrez peut-être appuyer sur <kbd>F</kbd> (<kbd>View ▸ Frame Selection</kbd> dans le menu) pour cadrer la sélection.

  ![Images ajoutées](images/atlas/single_images.png)

Ajout d'animations image par image
: Faites un <kbd>clic droit</kbd> sur l'entrée racine Atlas dans le panneau *Outline*.

  Sélectionnez <kbd>Add Animation Group</kbd> dans le menu contextuel pour créer un groupe d'animation image par image.

  Un nouveau groupe d'animation vide, portant un nom par défaut (`New Animation`), est ajouté à l'atlas.

  Glissez-déposez des images du panneau *Asset* vers la vue de l'éditeur pour les ajouter au groupe actuellement sélectionné.
  
  Vous pouvez aussi faire un <kbd>clic droit</kbd> sur le nouveau groupe et sélectionner <kbd>Add Images</kbd> dans le menu contextuel.

  Une boîte de dialogue s'ouvre pour vous permettre de rechercher et de sélectionner les images à ajouter au groupe d'animation.

  ![Création d'un atlas, ajout d'images](images/atlas/add_animation.png)

  Appuyez sur <kbd>Space</kbd> lorsque le groupe d'animation est sélectionné pour en afficher un aperçu, et sur <kbd>Ctrl/Cmd+T</kbd> pour fermer cet aperçu. Ajustez les propriétés de l'animation dans *Properties* selon vos besoins (voir ci-dessous).

  ![Groupe d'animation](images/atlas/animation_group.png)

Vous pouvez réordonner les images dans Outline en les sélectionnant et en appuyant sur <kbd>Alt + Up/down</kbd>. Vous pouvez aussi facilement créer des copies en copiant et en collant des images dans Outline (depuis le menu <kbd>Edit</kbd>, le menu contextuel accessible par un clic droit ou à l'aide de raccourcis clavier).

## Propriétés de l'atlas {#atlas-properties}

Chaque ressource atlas possède un ensemble de propriétés. Elles s'affichent dans le panneau *Properties* lorsque vous sélectionnez l'élément racine dans la vue *Outline*.

Size
: Affiche la taille totale calculée de la ressource texture obtenue. La largeur et la hauteur sont définies sur la puissance de deux la plus proche. Notez que si vous activez la compression des textures, certains formats exigent des textures carrées. Les textures non carrées seront alors redimensionnées et complétées par des espaces vides pour les rendre carrées. Consultez le [manuel des profils de texture](/manuals/texture-profiles/) pour plus de détails.

Margin
: Le nombre de pixels à ajouter entre les images.

Inner Padding
: Le nombre de pixels vides à ajouter autour de chaque image.

Extrude Borders
: Le nombre de pixels du bord à reproduire de manière répétée autour de chaque image. Lorsque le shader de fragment échantillonne des pixels au bord d'une image, des pixels d'une image voisine (sur la même texture d'atlas) peuvent déborder. L'extrusion du bord résout ce problème.

Max Page Size
: La taille maximale d'une page dans un atlas à plusieurs pages. Cela permet de diviser un atlas en plusieurs pages du même atlas afin de limiter sa taille tout en n'utilisant qu'un seul appel de dessin. Cette fonctionnalité doit être utilisée avec des matériaux prenant en charge les atlas à plusieurs pages, disponibles dans `/builtins/materials/*_paged_atlas.material`.

![Atlas à plusieurs pages](images/atlas/multipage_atlas.png)

Rename Patterns
: Une liste de motifs de recherche et de remplacement séparés par des virgules (´,´), chaque motif étant de la forme `search=replace`.
Le nom d'origine de chaque image (le nom de base du fichier) est transformé à l'aide de ces motifs. (Par exemple, le motif `hat=cat,_normal=` renomme une image nommée `hat_normal` en `cat`.) C'est utile pour faire correspondre les animations entre les atlas.

Voici des exemples des différents réglages des propriétés, avec quatre images carrées de taille 64x64 ajoutées à un atlas. Remarquez que l'atlas passe à 256x256 dès que les images ne tiennent plus dans 128x128, ce qui entraîne un gaspillage important d'espace de texture.

![Propriétés de l'atlas](images/atlas/atlas_properties.png)

## Propriétés des images {#image-properties}

Chaque image d'un atlas possède un ensemble de propriétés :

Id
: L'identifiant de l'image (en lecture seule).

Size
: La largeur et la hauteur de l'image (en lecture seule).

Pivot
: Le point de pivot de l'image (en unités). Le coin supérieur gauche correspond à (0,0) et le coin inférieur droit à (1,1). La valeur par défaut est (0.5, 0.5). Le pivot peut se trouver en dehors de l'intervalle 0-1. Le point de pivot est l'endroit sur lequel l'image est centrée lorsqu'elle est utilisée, par exemple, dans un sprite. Vous pouvez modifier le point de pivot en faisant glisser sa poignée dans la vue de l'éditeur. La poignée n'est visible que lorsqu'une seule image est sélectionnée. L'accrochage peut être activé en maintenant <kbd>Shift</kbd> enfoncé pendant le déplacement.

Sprite Trim Mode
: La manière dont le sprite est rendu. Par défaut, le sprite est rendu sous la forme d'un rectangle (Sprite Trim Mode défini sur Off). Si le sprite contient beaucoup de pixels transparents, il peut être plus efficace de le rendre sous une forme non rectangulaire utilisant entre 4 et 8 sommets. Notez que le rognage des sprites ne fonctionne pas avec les sprites à découpe en neuf zones (slice-9).

Image
: Le chemin de l'image elle-même.

![Propriétés des images](images/atlas/image_properties.png)

## Propriétés des animations {#animation-properties}

Outre la liste des images qui font partie d'un groupe d'animation, un ensemble de propriétés est disponible :

Id
: Le nom de l'animation.

Fps
: La vitesse de lecture de l'animation, exprimée en images par seconde (FPS).

Flip horizontal
: Inverse l'animation horizontalement.

Flip vertical
: Inverse l'animation verticalement.

Playback
: Indique comment l'animation doit être lue :

  - `None` ne lance aucune lecture ; la première image est affichée.
  - `Once Forward` lit l'animation une fois, de la première à la dernière image.
  - `Once Backward` lit l'animation une fois, de la dernière à la première image.
  - `Once Ping Pong` lit l'animation une fois, de la première à la dernière image, puis revient à la première image.
  - `Loop Forward` lit l'animation en boucle, de la première à la dernière image.
  - `Loop Backward` lit l'animation en boucle, de la dernière à la première image.
  - `Loop Ping Pong` lit l'animation en boucle, de la première à la dernière image, puis revient à la première image.

## Création de textures et d'atlas à l'exécution {#runtime-texture-and-atlas-creation}

Il est possible de créer une texture et un atlas à l'exécution.

### Création d'une ressource texture à l'exécution {#creating-a-texture-resource-at-runtime}

Utilisez [`resource.create_texture(path, params)`](https://defold.com/ref/stable/resource/#resource.create_texture:path-table) pour créer une nouvelle ressource texture :

```lua
  local params = {
    width  = 128,
    height = 128,
    type   = graphics.TEXTURE_TYPE_2D,
    format = graphics.TEXTURE_FORMAT_RGBA,
  }
  local my_texture_id = resource.create_texture("/my_custom_texture.texturec", params)
```

Une fois la texture créée, vous pouvez utiliser [`resource.set_texture(path, params, buffer)`](https://defold.com/ref/stable/resource/#resource.set_texture:path-table-buffer) pour définir ses pixels :

```lua
  local width = 128
  local height = 128
  local buf = buffer.create(width * height, { { name=hash("rgba"), type=buffer.VALUE_TYPE_UINT8, count=4 } } )
  local stream = buffer.get_stream(buf, hash("rgba"))

  for y=1, height do
      for x=1, width do
          local index = (y-1) * width * 4 + (x-1) * 4 + 1
          stream[index + 0] = 0xff
          stream[index + 1] = 0x80
          stream[index + 2] = 0x10
          stream[index + 3] = 0xFF
      end
  end

  local params = { width=width, height=height, x=0, y=0, type=graphics.TEXTURE_TYPE_2D, format=graphics.TEXTURE_FORMAT_RGBA, num_mip_maps=1 }
  resource.set_texture(my_texture_id, params, buf)
```

::: sidenote
Vous pouvez aussi utiliser `resource.set_texture()` pour mettre à jour une sous-région de la texture, en utilisant un tampon dont la largeur et la hauteur sont inférieures à la taille complète de la texture et en modifiant les paramètres x et y de `resource.set_texture()`.
:::

La texture peut être utilisée directement sur un [composant modèle](/manuals/model/) à l'aide de `go.set()` :

```lua
  go.set("#model", "texture0", my_texture_id)
```

### Création d'un atlas à l'exécution {#creating-an-atlas-at-runtime}

Si la texture doit être utilisée sur un [composant sprite](/manuals/sprite/), elle doit d'abord être utilisée par un atlas. Utilisez [`resource.create_atlas(path, params)`](https://defold.com/ref/stable/resource/#resource.create_atlas:path-table) pour créer un atlas :

```lua
  local params = {
    texture = texture_id,
    animations = {
      {
        id          = "my_animation",
        width       = width,
        height      = height,
        frames      = { 1 },
      }
    },
    geometries = {
      {
        vertices  = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        uvs = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        indices = {0,1,2,0,2,3}
      }
    }
  }
  local my_atlas_id = resource.create_atlas("/my_atlas.texturesetc", params)

  -- assign the atlas to the 'sprite' component on the same go
  go.set("#sprite", "image", my_atlas_id)

  -- play the "animation"
  sprite.play_flipbook("#sprite", "my_animation")

```

Les entrées de `frames` sont des indices commençant à 1 dans la table `geometries`. Une liste peut réutiliser, réordonner ou ignorer des géométries, ce qui ne peut pas être représenté par les champs d'intervalle obsolètes `frame_start` et `frame_end`. `resource.get_atlas()` renvoie `frames` ; utilisez la même représentation lorsque vous transmettez des données d'atlas à `resource.set_atlas()` ou à `resource.create_atlas()`. Les champs d'intervalle restent acceptés par les fonctions de modification et de création à des fins de compatibilité, mais le nouveau code devrait utiliser `frames`.
