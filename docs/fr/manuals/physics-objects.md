---
title: Objets de collision dans Defold
brief: Un objet de collision est un composant qui permet de donner un comportement physique à un objet de jeu. Un objet de collision possède des propriétés physiques et une forme dans l'espace.
---

# Objets de collision {#collision-objects}

Un objet de collision est un composant (component) qui permet de donner un comportement physique à un objet de jeu (game object). Un objet de collision possède des propriétés physiques comme le poids, la restitution et le frottement, et son étendue dans l'espace est définie par une ou plusieurs _formes_ que vous attachez au composant. Defold prend en charge les types d'objets de collision suivants :

Objets statiques
: Les objets statiques ne se déplacent jamais, mais un objet dynamique qui entre en collision avec un objet statique réagit en rebondissant et/ou en glissant. Les objets statiques sont très utiles pour construire la géométrie immobile des niveaux (c'est-à-dire le sol et les murs). Ils sont également moins coûteux en termes de performances que les objets dynamiques. Vous ne pouvez ni déplacer ni modifier autrement les objets statiques.

Objets dynamiques
: Les objets dynamiques sont simulés par le moteur physique. Le moteur résout toutes les collisions et applique les forces qui en résultent. Les objets dynamiques conviennent aux objets qui doivent se comporter de manière réaliste. La manière la plus courante d'agir sur eux est indirecte, en [appliquant des forces](/ref/physics/#apply_force) ou en modifiant l'[amortissement](/ref/stable/physics/#angular_damping) et la [vitesse](/ref/stable/physics/#linear_velocity) angulaires ainsi que l'[amortissement](/ref/stable/physics/#linear_damping) et la [vitesse](/ref/stable/physics/#angular_velocity) linéaires. Il est également possible de manipuler directement la position et l'orientation d'un objet dynamique lorsque le [paramètre Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) est activé dans *game.project*.

Objets cinématiques
: Les objets cinématiques enregistrent les collisions avec les autres objets physiques, mais le moteur physique n'effectue aucune simulation automatique. Il vous revient de résoudre les collisions ou de les ignorer ([en savoir plus](/manuals/physics-resolving-collisions)). Les objets cinématiques conviennent très bien aux objets contrôlés par le joueur ou par un script qui nécessitent un contrôle précis des réactions physiques, comme un personnage joueur.

Déclencheurs
: Les déclencheurs sont des objets qui enregistrent des collisions simples. Ce sont des objets de collision légers. Ils sont similaires aux [lancers de rayons](/manuals/physics-ray-casts) en ce qu'ils lisent le monde physique au lieu d'interagir avec lui. Ils conviennent aux objets qui ont seulement besoin d'enregistrer un impact (comme une balle), ou à la logique du jeu lorsque vous voulez déclencher certaines actions quand un objet atteint un point précis. Les déclencheurs sont moins coûteux en calcul que les objets cinématiques et devraient leur être préférés si possible.


## Ajouter un composant objet de collision {#adding-a-collision-object-component}

Un composant objet de collision possède un ensemble de *Properties* qui définit son type et ses propriétés physiques. Il contient également une ou plusieurs *Shapes* qui définissent la forme complète de l'objet physique.

Pour ajouter un composant objet de collision à un objet de jeu :

1. Dans la vue *Outline*, <kbd>faites un clic droit</kbd> sur l'objet de jeu et sélectionnez <kbd>Add Component ▸ Collision Object</kbd> dans le menu contextuel. Cela crée un nouveau composant sans forme.
2. <kbd>Faites un clic droit</kbd> sur le nouveau composant et sélectionnez <kbd>Add Shape</kbd>, puis choisissez une forme : <kbd>Box</kbd>, <kbd>Capsule</kbd>, <kbd>Sphere</kbd>, <kbd>Hull</kbd> ou <kbd>Mesh</kbd> dans les projets utilisant la physique 3D ; <kbd>Box</kbd> ou <kbd>Circle</kbd> dans les projets utilisant la physique 2D. Les formes Hull et Mesh sont disponibles depuis Defold 1.13.2 et utilisent un maillage nommé provenant d'une scène glTF ou GLB. Vous pouvez ajouter plusieurs formes au composant. Vous pouvez également utiliser une tilemap ou une ressource `.convexshape` via la propriété *Collision Shape*.
3. Utilisez les outils de déplacement, de rotation et de mise à l'échelle pour modifier les formes.
4. Sélectionnez le composant dans la vue *Outline* et modifiez les *Properties* de l'objet de collision.

![Objet de collision physique](images/physics/collision_object.png)


## Ajouter une forme de collision {#adding-a-collision-shape}

Un composant de collision peut contenir plusieurs formes intégrées, notamment des enveloppes convexes et des maillages triangulés en physique 3D, ou utiliser une ressource tilemap ou de forme convexe. Pour en savoir plus sur les différentes formes et la manière de les ajouter à un composant de collision, consultez le [manuel des formes de collision](/manuals/physics-shapes).


## Propriétés des objets de collision {#collision-object-properties}

Id
: L'identité du composant.

Collision Shape
: Une ressource tilemap ou `.convexshape`. Pour utiliser un maillage glTF ou GLB, ajoutez plutôt une forme Hull ou Mesh au composant et définissez les propriétés *Scene* et *Mesh* de cette forme. Consultez [Formes de collision pour plus d'informations](/manuals/physics-shapes).

Type
: Le type d'objet de collision : `Dynamic`, `Kinematic`, `Static` ou `Trigger`. Si vous définissez l'objet sur `Dynamic`, vous _devez_ attribuer à la propriété *Mass* une valeur non nulle. Pour les objets `Dynamic` ou `Static`, vous devriez également vérifier que les valeurs de *Friction* et de *Restitution* conviennent à votre cas d'utilisation.

Friction
: Le frottement permet aux objets de glisser les uns contre les autres de manière réaliste. La valeur de frottement est généralement comprise entre `0` (aucun frottement — un objet très glissant) et `1` (frottement important — un objet abrasif). Cependant, toute valeur positive est valide.

  L'intensité du frottement est proportionnelle à la force normale (c'est ce qu'on appelle le frottement de Coulomb). Lorsque la force de frottement est calculée entre deux formes (`A` et `B`), les valeurs de frottement des deux objets sont combinées par la moyenne géométrique :

```math
F = sqrt( F_A * F_B )
```

  Cela signifie que si l'un des objets a un frottement nul, le contact entre eux aura un frottement nul.

Restitution
: La valeur de restitution définit la capacité de l'objet à rebondir. Elle est généralement comprise entre 0 (collision inélastique — l'objet ne rebondit pas du tout) et 1 (collision parfaitement élastique — la vitesse de l'objet est exactement réfléchie lors du rebond).

  Les valeurs de restitution de deux formes (`A` et `B`) sont combinées à l'aide de la formule suivante :

```math
R = max( R_A, R_B )
```

  Lorsqu'une forme présente plusieurs contacts, la restitution est simulée de manière approximative, car Box2D utilise un solveur itératif. Box2D utilise également des collisions inélastiques lorsque la vitesse de collision est faible pour éviter les tremblements dus aux rebonds.

Linear damping
: L'amortissement linéaire réduit la vitesse linéaire du corps. Il diffère du frottement, qui ne se produit que lors d'un contact, et peut donner aux objets une impression de flottement, comme s'ils se déplaçaient dans un milieu plus épais que l'air. Les valeurs valides sont comprises entre 0 et 1.

  Box2D calcule l'amortissement de manière approximative pour des raisons de stabilité et de performances. Pour les faibles valeurs, l'effet d'amortissement est indépendant du pas de temps, tandis que pour les valeurs d'amortissement plus élevées, il varie avec le pas de temps. Si vous exécutez votre jeu avec un pas de temps fixe, cela ne pose jamais de problème.

Angular damping
: L'amortissement angulaire fonctionne comme l'amortissement linéaire, mais réduit la vitesse angulaire du corps. Les valeurs valides sont comprises entre 0 et 1.

Locked rotation
: L'activation de cette propriété désactive totalement la rotation de l'objet de collision, quelles que soient les forces qui lui sont appliquées.

Bullet
: L'activation de cette propriété permet la détection continue des collisions (CCD) entre l'objet de collision et les autres objets de collision dynamiques. La propriété *Bullet* est ignorée si *Type* n'est pas défini sur `Dynamic`.

Group
: Le nom du groupe de collision auquel l'objet doit appartenir. Vous pouvez avoir 16 groupes différents et les nommer comme vous le souhaitez pour votre jeu. Par exemple `players`, `bullets`, `enemies` et `world`. Si *Collision Shape* est défini sur une tilemap, ce champ n'est pas utilisé et les noms des groupes proviennent de la source de tuiles. [En savoir plus sur les groupes de collision](/manuals/physics-groups).

Mask
: Les autres _groupes_ avec lesquels cet objet doit entrer en collision. Vous pouvez nommer un groupe ou en indiquer plusieurs dans une liste séparée par des virgules. Si vous laissez le champ *Mask* vide, l'objet n'entrera en collision avec rien. [En savoir plus sur les groupes de collision](/manuals/physics-groups).

Generate Collision Events
: Si cette propriété est activée, elle permet à cet objet d'envoyer des événements de collision.

Generate Contact Events
: Si cette propriété est activée, elle permet à cet objet d'envoyer des événements de contact.

Generate Trigger Events
: Si cette propriété est activée, elle permet à cet objet d'envoyer des événements de déclenchement.


## Propriétés à l'exécution {#runtime-properties}

Un objet physique possède différentes propriétés qui peuvent être lues et modifiées à l'aide de `go.get()` et `go.set()` :

`angular_damping`
: La valeur de l'amortissement angulaire du composant objet de collision (`number`). [Référence de l'API](/ref/physics/#angular_damping).

`angular_velocity`
: La vitesse angulaire actuelle du composant objet de collision (`vector3`). [Référence de l'API](/ref/physics/#angular_velocity).

`linear_damping`
: La valeur de l'amortissement linéaire de l'objet de collision (`number`). [Référence de l'API](/ref/physics/#linear_damping).

`linear_velocity`
: La vitesse linéaire actuelle du composant objet de collision (`vector3`). [Référence de l'API](/ref/physics/#linear_velocity).

`mass`
: La masse physique définie pour le composant objet de collision. EN LECTURE SEULE. (`number`). [Référence de l'API](/ref/physics/#mass).
