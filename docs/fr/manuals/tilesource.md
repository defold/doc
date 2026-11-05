---
title: Manuel des sources de tuiles de Defold
brief: Ce manuel explique comment utiliser et créer une source de tuiles.
---

# Source de tuiles {#tile-source}

Une *source de tuiles* peut être utilisée par un [composant (component) tilemap](/manuals/tilemap) pour peindre des tuiles sur une grille, ou servir de source graphique pour un [sprite](/manuals/sprite) ou un [composant d'effet de particules](/manuals/particlefx). Vous pouvez également utiliser les *formes de collision* de la source de tuiles dans une tilemap pour la [détection des collisions et la simulation physique](/manuals/physics) ([exemple](/examples/tilemap/collisions/)).

## Créer une source de tuiles {#creating-a-tile-source}

Vous avez besoin d'une image contenant toutes les tuiles. Chaque tuile doit avoir exactement les mêmes dimensions et être placée dans une grille. Defold prend en charge un _espacement_ entre les tuiles et une _marge_ autour de chaque tuile.

![Image de tuiles](images/tilemap/small_map.png)

Une fois l'image source créée, vous pouvez créer une source de tuiles :

- Importez l'image dans votre projet en la faisant glisser vers un emplacement du projet dans le navigateur *Assets*.
- Créez un fichier de source de tuiles (<kbd>faites un clic droit</kbd> sur un emplacement dans le navigateur *Assets*, puis sélectionnez <kbd>New... ▸ Tile Source</kbd>).
- Nommez le nouveau fichier.
- Le fichier s'ouvre alors dans l'éditeur de sources de tuiles.
- Cliquez sur le bouton de sélection à côté de la propriété *Image* et sélectionnez votre image. L'image devrait maintenant s'afficher dans l'éditeur.
- Ajustez les *Properties* pour qu'elles correspondent à l'image source. Lorsque tout est correct, les tuiles s'alignent parfaitement.

![Création d'une source de tuiles](images/tilemap/tilesource.png)

Size
: La taille de l'image source.

Tile Width
: La largeur de chaque tuile.

Tile Height
: La hauteur de chaque tuile.

Tile Margin
: Le nombre de pixels autour de chaque tuile (en orange sur l'image ci-dessus).

Tile Spacing
: Le nombre de pixels entre chaque tuile (en bleu sur l'image ci-dessus).

Inner Padding
: Indique le nombre de pixels vides à ajouter automatiquement autour de la tuile dans la texture résultante utilisée à l'exécution du jeu.

Extrude Border
: Indique le nombre de fois que les pixels du bord doivent être automatiquement répliqués autour de la tuile dans la texture résultante utilisée à l'exécution du jeu.

Collision
: Indique l'image à utiliser pour générer automatiquement les formes de collision des tuiles.

## Animations image par image d'une source de tuiles {#tile-source-flip-book-animations}

Pour définir une animation dans une source de tuiles, sélectionnez les tuiles à lire avec la propriété *Frames* de l'animation. Les tuiles peuvent apparaître dans n'importe quel ordre, y compris avec des répétitions ; vous n'avez donc pas besoin de réorganiser l'image source. Toutes les sources de tuiles nouvellement créées possèdent une animation par défaut nommée "`anim`". Vous pouvez ajouter des animations en <kbd>faisant un clic droit</kbd> sur la racine de la source de tuiles dans l'*Outline*, puis en sélectionnant <kbd>Add ▸ Animation</kbd>.

Sélectionner une animation affiche ses *Properties*.

Id
: L'identifiant de l'animation. Il doit être unique dans la source de tuiles.

Frames
: Les numéros des tuiles dans l'ordre de l'animation, séparés par des virgules. La numérotation commence à 1 dans le coin supérieur gauche et progresse vers la droite, ligne par ligne, jusqu'au coin inférieur droit. Vous pouvez répéter les numéros de tuiles et utiliser des plages inclusives dans les deux sens.

| Frames | Séquence développée |
| --- | --- |
| `1, 3, 6, 3` | `1, 3, 6, 3` |
| `1-4, 8` | `1, 2, 3, 4, 8` |
| `4-2` | `4, 3, 2` |

L'éditeur affiche les suites consécutives d'au moins trois images sous forme de plages. Par exemple, `1, 2, 3` devient `1-3`, tandis que `1, 2` reste deux numéros de tuiles. L'ordre des images et les répétitions sont conservés. La liste doit contenir au moins une image, et chaque numéro de tuile doit exister dans l'image source.

*Frames* remplace *Start Tile* et *End Tile*. L'éditeur convertit les plages valides des anciens fichiers de source de tuiles en listes d'images. Dans les scripts de l'éditeur, utilisez le tableau d'entiers `frames` à la place de `start_tile` et `end_tile` ; consultez [Modifier des sources de tuiles](/manuals/editor-scripts/#editing-tilesources).

Playback
: Indique comment lire l'animation en suivant la liste *Frames* :

  - `None` ne lance aucune lecture ; la première image est affichée.
  - `Once Forward` lit l'animation une fois, de la première à la dernière image.
  - `Once Backward` lit l'animation une fois, de la dernière à la première image.
  - `Once Ping Pong` lit l'animation une fois, de la première à la dernière image, puis revient à la deuxième image.
  - `Loop Forward` lit l'animation en boucle, de la première à la dernière image.
  - `Loop Backward` lit l'animation en boucle, de la dernière à la première image.
  - `Loop Ping Pong` lit l'animation en boucle, de la première à la dernière image, puis revient à la première image.

Fps
: La vitesse de lecture de l'animation, exprimée en images par seconde (FPS).

Flip horizontal
: Retourne l'animation horizontalement.

Flip vertical
: Retourne l'animation verticalement.

## Formes de collision d'une source de tuiles {#tile-source-collision-shapes}

Defold utilise une image spécifiée dans la propriété *Collision* pour générer une forme _convexe_ pour chaque tuile. La forme épouse le contour de la partie de la tuile contenant des informations de couleur, c'est-à-dire qui n'est pas transparente à 100 %.

Il est souvent judicieux d'utiliser pour les collisions la même image que celle contenant les graphismes, mais vous pouvez spécifier une image distincte si vous souhaitez des formes de collision différentes des éléments visuels. Lorsque vous spécifiez une image de collision, l'aperçu est mis à jour avec un contour sur chaque tuile indiquant les formes de collision générées.

L'*Outline* de la source de tuiles répertorie les groupes de collision que vous y avez ajoutés. Les nouveaux fichiers de source de tuiles reçoivent un groupe de collision "default". Vous pouvez ajouter des groupes en <kbd>faisant un clic droit</kbd> sur la racine de la source de tuiles dans l'*Outline*, puis en sélectionnant <kbd>Add ▸ Collision Group</kbd>.

Pour sélectionner les formes de tuiles qui doivent appartenir à un groupe donné, sélectionnez le groupe dans l'*Outline*, puis cliquez sur chaque tuile que vous souhaitez lui affecter. Le contour de la tuile et de la forme prend la couleur du groupe. Cette couleur est automatiquement attribuée au groupe dans l'éditeur.

![Formes de collision](images/tilemap/collision.png)

Pour retirer une tuile de son groupe de collision, sélectionnez l'élément racine de la source de tuiles dans l'*Outline*, puis cliquez sur la tuile.
