---
title: Composants des objets de jeu
brief: Ce manuel présente les composants et explique comment les utiliser.
---

#  Composants {#components}

:[components](../shared/components.md)

## Types de composants {#component-types}

Defold prend en charge les types de composant (component) suivants :

* [Factory de collection](/manuals/collection-factory) - Créer des collections
* [Proxy de collection (collection proxy)](/manuals/collection-proxy) - Charger et décharger des collections
* [Objet de collision](/manuals/physics) - Physique 2D et 3D
* [Caméra](/manuals/camera) - Modifier la fenêtre d'affichage et la projection du monde de jeu (game world)
* [Factory](/manuals/factory) - Créer des objets de jeu (game object)
* [GUI](/manuals/gui) - Effectuer le rendu d'une interface graphique
* [Étiquette](/manuals/label) - Afficher un texte
* [Lumière](/manuals/light) - Ajouter des données d'éclairage pour les shaders
* [Maillage](/manuals/mesh) Afficher un maillage 3D (avec création et manipulation à l'exécution)
* [Modèle](/manuals/model) Afficher un modèle 3D (avec des animations facultatives)
* [Effets de particules](/manuals/particlefx) -  Créer des particules
* [Script](/manuals/script) - Ajouter la logique du jeu
* [Son](/manuals/sound) - Jouer du son ou de la musique
* [Sprite](/manuals/sprite) - Afficher une image 2D (avec une animation image par image facultative)
* [Tilemap](/manuals/tilemap) - Afficher une grille de tuiles

Des composants supplémentaires peuvent être ajoutés au moyen d'extensions :

* [Modèle Rive](/extension-rive) - Effectuer le rendu d'une animation Rive
* [Modèle Spine](/extension-spine) - Effectuer le rendu d'une animation Spine


## Activation et désactivation des composants {#enabling-and-disabling-components}

Les composants d'un objet de jeu sont activés lors de la création de cet objet de jeu. Si vous souhaitez désactiver un composant, envoyez-lui un message [`disable`](/ref/go/#disable) :

```lua
-- disable the component with id 'weapon' on the same game object as this script
msg.post("#weapon", "disable")

-- disable the component with id 'shield' on the 'enemy' game object
msg.post("enemy#shield", "disable")

-- disable all components on the current game object
msg.post(".", "disable")

-- disable all components on the 'enemy' game object
msg.post("enemy", "disable")
```

Pour réactiver un composant, vous pouvez lui envoyer un message [`enable`](/ref/go/#enable) :

```lua
-- enable the component with id 'weapon'
msg.post("#weapon", "enable")
```

## Propriétés des composants {#component-properties}

Chaque type de composant Defold possède des propriétés différentes. Le [panneau Properties](/manuals/editor/#the-editor-views) de l'éditeur affiche les propriétés du composant actuellement sélectionné dans le [panneau Outline](/manuals/editor/#the-editor-views). Consultez les manuels des différents types de composants pour en savoir plus sur les propriétés disponibles.

## Position, rotation et échelle des composants {#component-position-rotation-and-scale}

Les composants visuels possèdent généralement des propriétés de position et de rotation, et le plus souvent aussi une propriété d'échelle. Ces propriétés peuvent être modifiées depuis l'éditeur et, dans presque tous les cas, elles ne peuvent pas être modifiées à l'exécution (la seule exception est l'échelle des composants sprite et label, qui peut être modifiée à l'exécution).

Si vous avez besoin de modifier la position, la rotation ou l'échelle d'un composant à l'exécution, vous devez modifier la position, la rotation ou l'échelle de l'objet de jeu auquel il appartient. Cela a pour effet d'affecter tous les composants de cet objet de jeu. Si vous souhaitez manipuler un seul composant parmi les nombreux composants attachés à un objet de jeu, il est recommandé de déplacer le composant en question vers un objet de jeu distinct, puis d'ajouter ce dernier comme enfant de l'objet de jeu auquel le composant appartenait à l'origine.

## Ordre de rendu des composants {#component-draw-order}

L'ordre de rendu des composants visuels dépend de deux éléments :

### Prédicats du script de rendu {#render-script-predicates}
Chaque composant se voit attribuer un [matériau](/manuals/material/), et chaque matériau possède une ou plusieurs étiquettes. Le script de rendu définit à son tour un certain nombre de prédicats, chacun correspondant à une ou plusieurs étiquettes de matériau. Les [prédicats du script de rendu sont dessinés un par un](/manuals/render/#render-predicates) dans la fonction *update()* du script de rendu, et les composants correspondant aux étiquettes définies dans chaque prédicat sont dessinés. Le script de rendu par défaut dessine d'abord les sprites et les tilemaps en une passe, puis les effets de particules en une autre passe, toutes deux dans l'espace du monde. Le script de rendu dessine ensuite les composants GUI en une passe distincte dans l'espace de l'écran.

### Valeur Z du composant {#component-z-value}
Tous les objets de jeu et tous les composants sont positionnés dans un espace 3D, avec des positions exprimées sous forme d'objets `vector3`. Lorsque vous visualisez le contenu graphique de votre jeu en 2D, les valeurs X et Y déterminent la position d'un objet le long des axes de « largeur » et de « hauteur », tandis que la position Z détermine sa position le long de l'axe de « profondeur ». La position Z vous permet de contrôler la visibilité des objets qui se chevauchent : un sprite dont la valeur Z est 1 apparaît devant un sprite dont la position Z est 0. Par défaut, Defold utilise un système de coordonnées qui autorise des valeurs Z comprises entre -1 et 1 :

![modèle](images/graphics/z-order.png)

Les composants correspondant à un [prédicat de rendu](/manuals/render/#render-predicates) sont dessinés ensemble, et l'ordre dans lequel ils sont dessinés dépend de la valeur Z finale du composant. La valeur Z finale d'un composant est la somme des valeurs Z du composant lui-même, de l'objet de jeu auquel il appartient et de tous les objets de jeu parents.

::: sidenote
L'ordre dans lequel plusieurs composants GUI sont dessinés n'est **pas** déterminé par la valeur Z de ces composants. L'ordre de rendu des composants GUI est contrôlé par la fonction [gui.set_render_order()](/ref/gui/#gui.set_render_order:order).
:::

Exemple : deux objets de jeu A et B. B est un enfant de A. B possède un composant sprite.

| Élément  | Valeur Z |
|----------|---------|
| A        | 2       |
| B        | 1       |
| B#sprite | 0.5     |

![](images/graphics/component-hierarchy.png)

Avec la hiérarchie ci-dessus, la valeur Z finale du composant sprite de B est 2 + 1 + 0.5 = 3.5.

::: important
Si deux composants ont exactement la même valeur Z, leur ordre est indéfini, et ils peuvent alterner au premier plan en scintillant ou être rendus dans un certain ordre sur une plateforme et dans un autre ordre sur une autre plateforme.

Le script de rendu définit un plan proche et un plan lointain pour les valeurs Z. Tout composant dont la valeur Z se situe en dehors de cet intervalle ne sera pas rendu. L'intervalle par défaut va de -1 à 1, mais [vous pouvez facilement le modifier](/manuals/render/#default-view-projection). La précision numérique des valeurs Z avec des limites proche et lointaine de -1 et 1 est très élevée. Lorsque vous travaillez avec des ressources 3D, vous devrez peut-être modifier les limites proche et lointaine de la projection par défaut dans un script de rendu personnalisé. Consultez le [manuel du rendu](/manuals/render/) pour plus d'informations.
:::


:[Component max count optimizations](../shared/component-max-count-optimizations.md)
