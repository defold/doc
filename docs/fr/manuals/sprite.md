---
title: Affichage d'images 2D
brief: Ce manuel explique comment afficher des images et des animations 2D à l'aide du composant sprite.
---

# Sprites {#sprites}

Un composant (component) sprite est une simple image ou une animation image par image affichée à l'écran.

![sprite](images/graphics/sprite.png)

Le composant sprite peut utiliser un [atlas](/manuals/atlas) ou une [source de tuiles](/manuals/tilesource) pour ses graphismes.

## Propriétés du sprite {#sprite-properties}

Outre les propriétés *Id*, *Position* et *Rotation*, les propriétés suivantes sont propres à ce composant :

*Image*
: Si le shader possède un seul échantillonneur, ce champ s'appelle `Image`. Sinon, chaque emplacement porte le nom de l'échantillonneur de texture dans le matériau.
Chaque emplacement indique la ressource atlas ou source de tuiles à utiliser pour le sprite avec cet échantillonneur de texture.

*Default Animation*
: L'animation à utiliser pour le sprite. Les informations d'animation proviennent du premier atlas ou de la première source de tuiles.

*Material*
: Le matériau à utiliser pour le rendu du sprite.

*Blend Mode*
: Le mode de fusion à utiliser pour le rendu du sprite.

*Size Mode*
: Si la valeur est `Automatic`, l'éditeur définit la taille du sprite. Si la valeur est `Manual`, vous pouvez définir la taille vous-même.

*Slice 9*
: Définissez cette propriété pour préserver la taille en pixels de la texture du sprite sur les bords lorsque le sprite est redimensionné.

:[Slice-9](../shared/slice-9-texturing.md)

### Modes de fusion {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

## Manipulation à l'exécution {#runtime-manipulation}

Vous pouvez manipuler les sprites à l'exécution au moyen de différentes fonctions et propriétés (consultez la [documentation de l'API pour leur utilisation](/ref/sprite/)). Fonctions :

* `sprite.play_flipbook()` - Joue une animation sur un composant sprite.
* `sprite.set_hflip()` et `sprite.set_vflip()` - Définissent le retournement horizontal et vertical de l'animation d'un sprite.

Un sprite possède également différentes propriétés que vous pouvez manipuler avec `go.get()` et `go.set()` :

`cursor`
: Le curseur d'animation normalisé (`number`).

`image`
: L'image du sprite (`hash`). Vous pouvez la modifier à l'aide d'une propriété de ressource atlas ou source de tuiles et de `go.set()`. Consultez la [référence de l'API pour un exemple](/ref/sprite/#image).

`material`
: Le matériau du sprite (`hash`). Vous pouvez le modifier à l'aide d'une propriété de ressource matériau et de `go.set()`. Consultez la [référence de l'API pour un exemple](/ref/sprite/#material).

`playback_rate`
: La vitesse de lecture de l'animation (`number`).

`scale`
: L'échelle non uniforme du sprite (`vector3`).

`size`
: La taille du sprite (`vector3`). Elle ne peut être modifiée que si la propriété `Size Mode` du sprite est définie sur `Manual`.

## Constantes de matériau {#material-constants}

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: La teinte du sprite (`vector4`). Le type `vector4` représente la teinte, avec `x`, `y`, `z` et `w` correspondant aux composantes rouge, verte, bleue et alpha de la teinte.

## Attributs de matériau {#material-attributes}

Un sprite peut redéfinir les attributs de sommets du matériau actuellement assigné, qui seront transmis au shader de sommets par le composant (consultez le [manuel des matériaux pour plus de détails](/manuals/material/#attributes)).

Les attributs spécifiés dans le matériau apparaissent comme des propriétés ordinaires dans l'inspecteur et peuvent être définis individuellement sur chaque composant sprite. Si un attribut est redéfini, il apparaît comme une propriété redéfinie et est enregistré dans le fichier sprite sur le disque :

![attributs du sprite](../images/graphics/sprite-attributes.png)

## Configuration du projet {#project-configuration}

Le fichier *game.project* comporte quelques [paramètres du projet](/manuals/project-settings#sprite) liés aux sprites.

## Sprites à plusieurs textures {#multi-textured-sprites}

Lorsqu'un sprite utilise plusieurs textures, certains points sont à prendre en compte.

### Animations {#animations}

Les données d'animation (nombre d'images par seconde, noms des images) proviennent actuellement de la première texture. Nous l'appellerons « animation directrice ».

Les identifiants d'image de l'animation directrice servent à rechercher les images dans une autre texture.
Il est donc important de veiller à ce que les identifiants d'image correspondent entre les textures.

Par exemple, si votre `diffuse.atlas` contient une animation `run` comme ceci :

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

Alors les identifiants d'image seront de la forme `run/hero_run_color_1`, qu'il est peu probable de trouver, par exemple, dans un `normal.atlas` :

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

Nous utilisons donc `Rename patterns` dans l'[atlas](/manuals/material/) pour les renommer.
Définissez `_color=` et `_normal=` dans les atlas correspondants, et vous obtiendrez des noms d'image comme ceux-ci dans les deux atlas :

```
run/hero_run_1
run/hero_run_2
...
```

### Coordonnées UV {#uvs}

Les coordonnées UV proviennent de la première texture. Comme il n'y a qu'un seul ensemble de sommets, nous ne pouvons pas garantir
une bonne correspondance si les textures secondaires ont davantage de coordonnées UV ou une forme différente.

Ce point est important : veillez à ce que les images aient des formes suffisamment similaires, sinon vous risquez d'observer des bavures de texture.

Les dimensions des images dans chaque texture peuvent être différentes.
