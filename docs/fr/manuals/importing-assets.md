---
title: Importation et modification des ressources
brief: Ce manuel explique comment importer et modifier des ressources.
---

# Importation et modification des ressources {#importing-and-editing-assets}

Un projet de jeu se compose généralement d'un grand nombre de ressources externes produites dans différents logiciels spécialisés dans la création d'éléments graphiques, de modèles 3D, de fichiers audio, d'animations, etc. Defold est conçu pour un flux de travail dans lequel vous utilisez vos outils externes, puis importez les ressources dans Defold une fois qu'elles sont finalisées.


## Importation des ressources {#importing-assets}

Defold exige que toutes les ressources utilisées dans votre projet se trouvent dans la hiérarchie du projet. Vous devez donc importer toutes les ressources avant de pouvoir les utiliser. Pour importer des ressources, faites simplement glisser les fichiers depuis le système de fichiers de votre ordinateur et déposez-les à l'emplacement approprié dans le *panneau Assets* de l'éditeur Defold.

![Importation de fichiers](images/graphics/import.png)

::: sidenote
Defold prend en charge les images aux formats PNG et JPEG. Les images PNG doivent être au format RGBA 32 bits. Les autres formats d'image doivent être convertis avant de pouvoir être utilisés.
:::


## Utilisation des ressources {#using-assets}

Une fois les ressources importées dans Defold, elles peuvent être utilisées par les différents types de composant (component) pris en charge par Defold :

* Les images peuvent servir à créer de nombreux types de composants visuels fréquemment utilisés dans les jeux 2D. Pour en savoir plus, consultez [les instructions d'importation et d'utilisation des éléments graphiques 2D](/manuals/importing-graphics).
* Les sons peuvent être utilisés par le [composant Sound](/manuals/sound) pour lire des sons.
* Les polices sont utilisées par le [composant Label](/manuals/label) et par les [nœuds de texte](/manuals/gui-text) dans une interface graphique.
* Les modèles glTF (*.gltf* et *.glb*) peuvent être utilisés par le [composant Model](/manuals/model) pour afficher des modèles 3D avec des animations. Importez toutes les images de texture utilisées par le modèle en tant que ressources distinctes et affectez-les aux propriétés de texture du matériau du composant Model. Pour en savoir plus, consultez [les instructions d'importation et d'utilisation des modèles 3D](/manuals/importing-models).


## Modification des ressources externes {#editing-external-assets}

Defold ne fournit pas d'outils de modification pour les images, les fichiers audio, les modèles ou les animations. Ces ressources doivent être créées en dehors de Defold avec des outils spécialisés, puis importées dans Defold. Defold détecte automatiquement les modifications apportées à toute ressource parmi les fichiers de votre projet et met à jour la vue de l'éditeur en conséquence.


## Modification des ressources Defold {#editing-defold-assets}

L'éditeur enregistre toutes les ressources Defold dans des fichiers texte qui facilitent les fusions. Ces fichiers sont également faciles à créer et à modifier à l'aide de scripts simples. Consultez [cette discussion sur le forum](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210) pour plus d'informations. Notez toutefois que nous ne publions pas les détails de nos formats de fichiers, car ils changent de temps à autre. Vous pouvez également utiliser les [scripts de l'éditeur](/manuals/editor-scripts/) pour réagir à certains événements du cycle de vie de l'éditeur et exécuter des scripts qui génèrent ou modifient des ressources.

Faites particulièrement attention lorsque vous manipulez des fichiers de ressources Defold à l'aide d'un éditeur de texte ou d'un outil externe. Si vous introduisez des erreurs, elles peuvent empêcher l'ouverture du fichier dans l'éditeur Defold.

Certains outils externes tels que [Tiled](/assets/tiled/) et [Tilesetter](https://www.tilesetter.org/beta) peuvent être utilisés pour générer automatiquement des ressources Defold.
