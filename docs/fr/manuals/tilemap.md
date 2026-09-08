---
title: Manuel des tilemaps de Defold
brief: Ce manuel présente en détail la prise en charge des tilemaps dans Defold.
---

# Tilemap {#tile-map}

Une *tilemap* est un composant (component) qui vous permet d'assembler ou de peindre des tuiles issues d'une *source de tuiles* (Tile Source) sur une vaste grille. Les tilemaps sont couramment utilisées pour créer les environnements des niveaux d'un jeu. Vous pouvez également utiliser les *formes de collision* de la source de tuiles dans vos cartes pour la détection des collisions et la simulation physique ([exemple](/examples/tilemap/collisions/)).

Avant de pouvoir créer une tilemap, vous devez créer une source de tuiles. Consultez le [manuel des sources de tuiles](/manuals/tilesource) pour apprendre à en créer une.

## Création d'une tilemap {#creating-a-tile-map}

Pour créer une tilemap :

- Faites un <kbd>clic droit</kbd> sur un emplacement dans le navigateur *Assets*, puis sélectionnez <kbd>New... ▸ Tile Map</kbd>.
- Nommez le fichier.
- La nouvelle tilemap s'ouvre automatiquement dans l'éditeur de tilemaps.

  ![Nouvelle tilemap](images/tilemap/tilemap.png)

- Définissez la propriété *Tile Source* sur un fichier de source de tuiles que vous avez préparé.

Pour peindre des tuiles sur votre tilemap :

1. Sélectionnez ou créez un *Layer* sur lequel peindre dans la vue *Outline*.
2. Sélectionnez une tuile à utiliser comme pinceau (appuyez sur <kbd>Space</kbd> pour afficher la palette de tuiles) ou sélectionnez plusieurs tuiles en cliquant et en faisant glisser la souris dans la palette pour créer un pinceau rectangulaire composé de plusieurs tuiles.

   ![Palette](images/tilemap/palette.png)

3. Peignez avec le pinceau sélectionné. Pour effacer une tuile, choisissez une tuile vide et utilisez-la comme pinceau, ou sélectionnez la gomme (<kbd>Edit ▸ Select Eraser</kbd>).

   ![Peinture des tuiles](images/tilemap/paint_tiles.png)

Vous pouvez prélever des tuiles directement dans un calque et utiliser la sélection comme pinceau. Maintenez <kbd>Shift</kbd> enfoncée et cliquez sur une tuile pour en faire le pinceau actuel. Tout en maintenant <kbd>Shift</kbd> enfoncée, vous pouvez également cliquer et faire glisser la souris pour sélectionner un bloc de tuiles à utiliser comme pinceau plus grand. Vous pouvez aussi couper des tuiles de la même manière en maintenant <kbd>Shift+Ctrl</kbd> enfoncées, ou les effacer en maintenant <kbd>Shift+Alt</kbd> enfoncées.

Pour faire pivoter le pinceau dans le sens des aiguilles d'une montre, utilisez <kbd>Z</kbd>. Utilisez <kbd>X</kbd> pour retourner le pinceau horizontalement et <kbd>Y</kbd> pour le retourner verticalement.

![Prélèvement de tuiles](images/tilemap/pick_tiles.png)

## Ajout d'une tilemap à votre jeu {#adding-a-tile-map-to-your-game}

Pour ajouter une tilemap à votre jeu :

1. Créez un objet de jeu (game object) pour y placer le composant tilemap. L'objet de jeu peut se trouver dans un fichier ou être créé directement dans une collection.
2. Faites un clic droit sur la racine de l'objet de jeu et sélectionnez <kbd>Add Component File</kbd>.
3. Sélectionnez le fichier de la tilemap.

![Utilisation d'une tilemap](images/tilemap/use_tilemap.png)

## Manipulation à l'exécution {#runtime-manipulation}

Vous pouvez manipuler les tilemaps à l'exécution à l'aide de différentes fonctions et propriétés (consultez la [documentation de l'API pour savoir comment les utiliser](/ref/tilemap/)).

### Modification des tuiles par script {#changing-tiles-from-script}

Vous pouvez lire et modifier dynamiquement le contenu d'une tilemap pendant l'exécution de votre jeu. Pour cela, utilisez les fonctions [`tilemap.get_tile()`](/ref/tilemap/#tilemap.get_tile) et [`tilemap.set_tile()`](/ref/tilemap/#tilemap.set_tile) :

```lua
local tile = tilemap.get_tile("/level#map", "ground", x, y)

if tile == 2 then
    -- Replace grass-tile (2) with dangerous hole tile (number 4).
    tilemap.set_tile("/level#map", "ground", x, y, 4)
end
```

## Propriétés des tilemaps {#tilemap-properties}

Outre les propriétés *Id*, *Position*, *Rotation* et *Scale*, les propriétés propres à ce composant sont les suivantes :

*Tile Source*
: La ressource tilesource à utiliser pour la tilemap.

*Material*
: Le matériau à utiliser pour le rendu de la tilemap.

*Blend Mode*
: Le mode de fusion à utiliser lors du rendu de la tilemap.

### Modes de fusion {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

### Modification des propriétés {#changing-properties}

Une tilemap possède plusieurs propriétés qui peuvent être manipulées à l'aide de `go.get()` et `go.set()` :

`tile_source`
: La source de tuiles de la tilemap (`hash`). Vous pouvez la modifier à l'aide d'une propriété de ressource de source de tuiles et de `go.set()`. Consultez la [référence de l'API pour un exemple](/ref/tilemap/#tile_source).

`material`
: Le matériau de la tilemap (`hash`). Vous pouvez le modifier à l'aide d'une propriété de ressource de matériau et de `go.set()`. Consultez la [référence de l'API pour un exemple](/ref/tilemap/#material).

### Constantes de matériau {#material-constants}

{% include shared/material-constants.md component='tilemap' variable='tint' %}

`tint`
: La teinte de la tilemap (`vector4`). Le `vector4` représente la teinte, x, y, z et w correspondant respectivement à ses composantes rouge, verte, bleue et alpha.

## Configuration du projet {#project-configuration}

Le fichier *game.project* contient quelques [paramètres du projet](/manuals/project-settings#tilemap) relatifs aux tilemaps.

## Outils externes {#external-tools}

Il existe des éditeurs externes de cartes et de niveaux qui peuvent exporter directement au format tilemap de Defold :

### Tiled {#tiled}

[Tiled](https://www.mapeditor.org/) est un éditeur de cartes bien connu et largement utilisé pour les cartes orthogonales, isométriques et hexagonales. Tiled prend en charge un large éventail de fonctionnalités et peut [exporter directement vers Defold](https://doc.mapeditor.org/en/stable/manual/export-defold/). Pour en savoir plus sur l'exportation des données de tilemap et des métadonnées supplémentaires, consultez [cet article de blog de l'utilisateur de Defold « goeshard »](https://goeshard.org/2025/01/01/using-tiled-object-layers-with-defold-tilemaps/)


### Tilesetter {#tilesetter}

[Tilesetter](https://www.tilesetter.org/docs/exporting#defold) permet de créer automatiquement des jeux de tuiles complets à partir de tuiles de base simples et dispose d'un éditeur de cartes qui peut exporter directement vers Defold.



