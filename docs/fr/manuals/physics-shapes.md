---
title: Formes de collision
brief: Les objets de collision peuvent contenir des formes primitives, des enveloppes convexes ou des maillages triangulés, ou utiliser des ressources tilemap et de forme convexe.
---

# Formes de collision {#collision-shapes}

Un objet de collision peut contenir plusieurs formes intégrées. En physique 3D, celles-ci peuvent inclure des enveloppes convexes et des maillages triangulés provenant de fichiers glTF ou GLB. Vous pouvez également utiliser une tilemap ou une ressource de forme convexe via la propriété *Collision Shape* de l'objet de collision.

### Formes primitives {#primitive-shapes}
Les formes primitives sont la *boîte*, la *sphère* et la *capsule*. Pour ajouter une forme primitive, <kbd>faites un clic droit</kbd> sur l'objet de collision et sélectionnez <kbd>Add Shape</kbd> :

![Ajouter une forme primitive](images/physics/add_shape.png)

## Forme de boîte {#box-shape}
Une boîte possède une position, une rotation et des dimensions (largeur, hauteur et profondeur) :

![Forme de boîte](images/physics/box.png)

## Forme de sphère {#sphere-shape}
Une sphère possède une position, une rotation et un diamètre :

![Forme de sphère](images/physics/sphere.png)

## Forme de capsule {#capsule-shape}
Une capsule possède une position, une rotation, un diamètre et une hauteur :

![Forme de sphère](images/physics/capsule.png)

::: important
Les formes de capsule sont prises en charge uniquement avec la physique 3D (configurée dans la section Physics du fichier *game.project*).
:::

### Formes complexes {#complex-shapes}
Les formes complexes peuvent utiliser la géométrie d'une tilemap ou les données d'une enveloppe convexe. Depuis Defold 1.13.2, les objets de collision 3D peuvent également créer des enveloppes convexes et des formes de maillage triangulé à partir des maillages de scènes glTF ou GLB.

## Formes Hull et Mesh en 3D {#hull-and-mesh-shapes-in-3d}

Utilisez une forme *Hull* pour une approximation convexe d'un maillage, ou une forme *Mesh* lorsque les collisions doivent suivre ses triangles, y compris les zones concaves comme les ouvertures dans la géométrie d'un niveau.

1. Définissez **Physics ▸ Type** sur `3D` dans *game.project*.
2. Faites un clic droit sur l'objet de collision dans l'*Outline* et sélectionnez <kbd>Add Shape ▸ Hull</kbd> ou <kbd>Add Shape ▸ Mesh</kbd>.
3. Sélectionnez la nouvelle forme et définissez sa propriété *Scene* sur un fichier *.gltf* ou *.glb*.
4. Sélectionnez un maillage nommé dans le champ *Mesh*. S'il ne figure pas dans la liste, nommez le maillage dans votre outil de modélisation et exportez à nouveau la scène.
5. Positionnez et faites pivoter la forme pour l'aligner sur la géométrie visible de l'objet de jeu. Répétez ces étapes pour ajouter d'autres formes si nécessaire.

Le maillage sélectionné fournit sa géométrie locale ; les transformations des nœuds glTF ne sont pas appliquées. Les formes de collision Mesh sont prises en charge par le moteur physique Bullet 3D, y compris pour les objets de collision statiques et non statiques. Elles ne sont pas prises en charge par les moteurs physiques 2D.

La géométrie des maillages triangulés est accessible en lecture seule via les API de formes à l'exécution. Modifiez le maillage source et recréez un build pour changer ses triangles. Consultez [Mise à l'échelle des formes de collision](#scaling-collision-shapes) pour l'échelle de l'objet de jeu.

## Forme de collision de tilemap {#tilemap-collision-shape}
Defold propose une fonctionnalité qui permet de générer facilement des formes physiques pour la source de tuiles utilisée par une tilemap. Le [manuel des sources de tuiles](/manuals/tilesource/#tile-source-collision-shapes) explique comment ajouter des groupes de collision à une source de tuiles et affecter des tuiles à ces groupes ([exemple](/examples/tilemap/collisions/)).

Pour ajouter des collisions à une tilemap :

1. Ajoutez la tilemap à un objet de jeu (game object) en <kbd>faisant un clic droit</kbd> sur l'objet de jeu et en sélectionnant <kbd>Add Component File</kbd>. Sélectionnez le fichier de tilemap.
2. Ajoutez un composant d'objet de collision à l'objet de jeu en <kbd>faisant un clic droit</kbd> sur l'objet de jeu et en sélectionnant <kbd>Add Component ▸ Collision Object</kbd>.
3. Au lieu d'ajouter des formes au composant, définissez la propriété *Collision Shape* sur le fichier *tilemap*.
4. Configurez les *Properties* du composant d'objet de collision comme d'habitude.

![Collision de source de tuiles](images/physics/collision_tilemap.png)

::: important
Notez que la propriété *Group* n'est **pas** utilisée ici, car les groupes de collision sont définis dans la source de tuiles de la tilemap.
:::

## Forme d'enveloppe convexe {#convex-hull-shape}
En physique 3D, vous pouvez créer une enveloppe convexe directement à partir d'un maillage avec le [flux de travail de l'éditeur décrit ci-dessus](#hull-and-mesh-shapes-in-3d). L'ancienne ressource `.convexshape` est également prise en charge et peut être créée à partir de points avec un éditeur externe :

1. Créez un fichier de forme d'enveloppe convexe (extension de fichier `.convexshape`) à l'aide d'un éditeur externe.
2. Modifiez le fichier manuellement à l'aide d'un éditeur de texte ou d'un outil externe (voir ci-dessous)
3. Au lieu d'ajouter des formes au composant d'objet de collision, définissez la propriété *Collision Shape* sur le fichier de *forme convexe*.

### Format du fichier {#file-format}
Le format de fichier d'enveloppe convexe utilise le même format de données que tous les autres fichiers Defold, à savoir le format texte protobuf. Une forme d'enveloppe convexe définit les points de l'enveloppe. En physique 2D, les points doivent être fournis dans le sens inverse des aiguilles d'une montre. Un nuage de points abstrait est utilisé en mode physique 3D. Exemple en 2D :

```
shape_type: TYPE_HULL
data: 200.000
data: 100.000
data: 0.0
data: 400.000
data: 100.000
data: 0.0
data: 400.000
data: 300.000
data: 0.0
data: 200.000
data: 300.000
data: 0.0
```

L'exemple ci-dessus définit les quatre coins d'un rectangle :

```
 200x300   400x300
    4---------3
    |         |
    |         |
    |         |
    |         |
    1---------2
 200x100   400x100
```

## Outils externes {#external-tools}

Plusieurs outils externes peuvent être utilisés pour créer des formes de collision :

* [Physics Editor](https://www.codeandweb.com/physicseditor/tutorials/how-to-create-physics-shapes-for-defold) de CodeAndWeb permet de créer des objets de jeu avec des sprites et les formes de collision correspondantes.
* [Defold Polygon Editor](https://rossgrams.itch.io/defold-polygon-editor) permet de créer des formes d'enveloppe convexe.
* [Physics Body Editor](https://selimanac.github.io/physics-body-editor/) permet de créer des formes d'enveloppe convexe.


# Mise à l'échelle des formes de collision {#scaling-collision-shapes}
L'objet de collision et ses formes héritent de l'échelle de l'objet de jeu. Pour désactiver ce comportement, décochez la case [Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) dans la section Physics de *game.project*. Notez que seule la mise à l'échelle uniforme est prise en charge et que la plus petite valeur d'échelle sera utilisée si l'échelle n'est pas uniforme.

# Redimensionnement des formes de collision {#resizing-collision-shapes}
Les formes primitives peuvent être redimensionnées à l'exécution avec `physics.set_shape()`. Cette fonction ne remplace ni les sommets des enveloppes convexes ni la géométrie des maillages triangulés. Exemple :

```lua
-- set capsule shape data
local capsule_data = {
  type = physics.SHAPE_TYPE_CAPSULE,
  diameter = 10,
  height = 20,
}
physics.set_shape("#collisionobject", "my_capsule_shape", capsule_data)

-- set sphere shape data
local sphere_data = {
  type = physics.SHAPE_TYPE_SPHERE,
  diameter = 10,
}
physics.set_shape("#collisionobject", "my_sphere_shape", sphere_data)

-- set box shape data
local box_data = {
  type = physics.SHAPE_TYPE_BOX,
  dimensions = vmath.vector3(10, 10, 5),
}
physics.set_shape("#collisionobject", "my_box_shape", box_data)
```

::: sidenote
Une forme du type approprié et portant l'identifiant spécifié doit déjà exister sur l'objet de collision.
:::

# Rotation des formes de collision {#rotating-collision-shapes}

## Rotation des formes de collision en physique 3D {#rotating-collision-shapes-in-3d-physics}
Les formes de collision en physique 3D peuvent être tournées autour de tous les axes.


## Rotation des formes de collision en physique 2D {#rotating-collision-shapes-in-2d-physics}
Les formes de collision en physique 2D ne peuvent être tournées qu'autour de l'axe z. Une rotation autour de l'axe x ou y produira des résultats incorrects et doit être évitée, même pour une rotation de 180 degrés destinée à retourner la forme suivant l'axe x ou y. Pour retourner une forme physique, il est recommandé d'utiliser [`physics.set_hlip(url, flip)`](/ref/stable/physics/?#physics.set_hflip:url-flip) et [`physics.set_vlip(url, flip)`](/ref/stable/physics/?#physics.set_vflip:url-flip).


# Débogage {#debugging}
Vous pouvez [activer le débogage de la physique](/manuals/debugging-game-logic/#debugging-problems-with-physics) pour voir les formes de collision à l'exécution.
