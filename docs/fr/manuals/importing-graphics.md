---
title: Importation et utilisation de graphismes 2D
brief: Ce manuel explique comment importer et utiliser des graphismes 2D.
---

# Importation de graphismes 2D {#importing-2d-graphics}

Defold prend en charge de nombreux types de composants (components) visuels fréquemment utilisés dans les jeux 2D. Vous pouvez utiliser Defold pour créer des sprites statiques et animés, des composants d'interface utilisateur, des effets de particules, des cartes de tuiles et des polices bitmap. Avant de pouvoir créer l'un de ces composants visuels, vous devez importer des fichiers image contenant les graphismes que vous souhaitez utiliser. Pour importer des fichiers image, il vous suffit de faire glisser les fichiers depuis le système de fichiers de votre ordinateur et de les déposer à l'emplacement approprié dans le *panneau Assets* de l'éditeur Defold.

![Importation de fichiers](images/graphics/import.png)

::: sidenote
Defold prend en charge les images aux formats PNG et JPEG. Les autres formats d'image doivent être convertis avant de pouvoir être utilisés.
:::


## Création de ressources Defold {#creating-defold-assets}

Une fois importées dans Defold, les images peuvent servir à créer des ressources propres à Defold :

![atlas](images/icons/atlas.png){.icon} Atlas
: Un atlas contient une liste de fichiers image distincts, qui sont automatiquement réunis dans une image de texture plus grande. Les atlas peuvent contenir des images fixes et des *Animation Groups*, des ensembles d'images qui forment une animation image par image.

  ![atlas](images/graphics/atlas.png)

Pour en savoir plus sur la ressource atlas, consultez le [manuel des atlas](/manuals/atlas).

![source de tuiles](images/icons/tilesource.png){.icon} Source de tuiles
: Une source de tuiles référence un fichier image déjà composé de sous-images plus petites disposées sur une grille régulière. Ce type d'image composite est aussi couramment appelé _planche de sprites_. Les sources de tuiles peuvent contenir des animations image par image, définies par la première et la dernière tuile de l'animation. Il est également possible d'utiliser une image pour associer automatiquement des formes de collision aux tuiles.

  ![source de tuiles](images/graphics/tilesource.png)

Pour en savoir plus sur la ressource source de tuiles, consultez le [manuel des sources de tuiles](/manuals/tilesource).

![police bitmap](images/icons/font.png){.icon} Police bitmap
: Les glyphes d'une police bitmap sont regroupés dans une planche au format PNG. Ces types de polices n'améliorent pas les performances par rapport aux polices générées à partir de fichiers TrueType ou OpenType, mais peuvent inclure des graphismes, des couleurs et des ombres arbitraires directement dans l'image.

Pour en savoir plus sur les polices bitmap, consultez le [manuel des polices](/manuals/font/#bitmap-bmfonts).

  ![BMfont](images/font/bm_font.png)


## Utilisation des ressources Defold {#using-defold-assets}

Lorsque vous avez converti les images en fichiers d'atlas et de source de tuiles, vous pouvez les utiliser pour créer plusieurs types de composants visuels :

![sprite](images/icons/sprite.png){.icon}
: Un sprite est une image statique ou une animation image par image qui s'affiche à l'écran.

  ![sprite](images/graphics/sprite.png)

Pour en savoir plus sur les sprites, consultez le [manuel des sprites](/manuals/sprite).

![carte de tuiles](images/icons/tilemap.png){.icon} Tilemap
: Un composant tilemap assemble une carte à partir de tuiles (image et formes de collision) provenant d'une source de tuiles. Les tilemaps ne peuvent pas utiliser d'atlas comme source.

  ![tilemap](images/graphics/tilemap.png)

Pour en savoir plus sur les tilemaps, consultez le [manuel des tilemaps](/manuals/tilemap).

![effet de particules](images/icons/particlefx.png){.icon} Effet de particules
: Les particules générées par un émetteur de particules sont constituées d'une image fixe ou d'une animation image par image provenant d'un atlas ou d'une source de tuiles.

  ![particules](images/graphics/particles.png)

Pour en savoir plus sur les effets de particules, consultez le [manuel des effets de particules](/manuals/particlefx).

![interface graphique](images/icons/gui.png){.icon} GUI
: Les nœuds box et pie des interfaces graphiques peuvent utiliser des images fixes et des animations image par image provenant d'atlas et de sources de tuiles.

  ![interface graphique](images/graphics/gui.png)

Pour en savoir plus sur les interfaces graphiques, consultez le [manuel des interfaces graphiques](/manuals/gui).
