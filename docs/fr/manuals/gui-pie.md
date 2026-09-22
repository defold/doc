---
title: Nœuds Pie d'interface graphique dans Defold
brief: Ce manuel explique comment utiliser les nœuds Pie dans les scènes d'interface graphique de Defold.
---

# Nœuds Pie d'interface graphique {#gui-pie-nodes}

Les nœuds Pie permettent de créer des objets circulaires ou ellipsoïdaux, allant de simples cercles à des secteurs ou à des anneaux carrés.

## Créer un nœud Pie {#creating-a-pie-node}

<kbd>Faites un clic droit</kbd> sur la section *Nodes* dans la vue *Outline* et sélectionnez <kbd>Add ▸ Pie</kbd>. Le nouveau nœud Pie est sélectionné et vous pouvez modifier ses propriétés.

![Créer un nœud Pie](images/gui-pie/create.png)

Les propriétés suivantes sont propres aux nœuds Pie :

Inner Radius
: Le rayon intérieur du nœud, exprimé le long de l'axe X.

Outer Bounds
: La forme des limites extérieures du nœud.

  - `Ellipse` étendra le nœud jusqu'au rayon extérieur.
  - `Rectangle` étendra le nœud jusqu'à sa boîte englobante.

Perimeter Vertices
: Le nombre de segments qui serviront à construire la forme, exprimé par le nombre de sommets nécessaires pour délimiter entièrement le périmètre de 360 degrés du nœud.

Pie Fill Angle
: La portion du secteur à remplir. Elle est exprimée par un angle mesuré dans le sens inverse des aiguilles d'une montre à partir de la droite.

![Propriétés](images/gui-pie/properties.png)

Si vous définissez une texture sur le nœud, l'image de la texture est appliquée à plat, les coins de la texture correspondant aux coins de la boîte englobante du nœud.

## Modifier les nœuds Pie à l'exécution {#modify-pie-nodes-at-runtime}

Les nœuds Pie répondent à toutes les fonctions génériques de manipulation des nœuds pour définir la taille, le pivot, la couleur, etc. Quelques fonctions et propriétés sont propres aux nœuds Pie :

```lua
local pienode = gui.get_node("my_pie_node")

-- get the outer bounds
local fill_angle = gui.get_fill_angle(pienode)

-- increase perimeter vertices
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- change outer bounds
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- animate the inner radius
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
