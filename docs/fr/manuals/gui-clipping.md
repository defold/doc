---
title: Manuel du découpage de l'interface graphique
brief: Ce manuel décrit comment créer des nœuds d'interface graphique qui masquent d'autres nœuds par découpage à l'aide d'un stencil.
---

# Découpage {#clipping}

Les nœuds d'interface graphique peuvent servir de nœuds de *découpage* : des masques qui contrôlent le rendu des autres nœuds. Ce manuel explique le fonctionnement de cette fonctionnalité.

## Création d'un nœud de découpage {#creating-a-clipping-node}

Les nœuds Box, Text et Pie peuvent servir au découpage. Pour créer un nœud de découpage, ajoutez un nœud à votre interface graphique, puis définissez ses propriétés en conséquence :

Clipping Mode
: Le mode utilisé pour le découpage.
  - `None` effectue le rendu du nœud sans aucun découpage.
  - `Stencil` fait écrire le nœud dans le masque de stencil actuel.

Clipping Visible
: Cochez cette option pour effectuer le rendu du contenu du nœud.

Clipping Inverted
: Cochez cette option pour écrire l'inverse de la forme du nœud dans le masque.

Ajoutez ensuite les nœuds que vous souhaitez découper comme enfants du nœud de découpage.

![Création d'un découpage](images/gui-clipping/create.png)

## Masque de stencil {#stencil-mask}

Le découpage fonctionne grâce à des nœuds qui écrivent dans un *tampon de stencil*. Ce tampon contient des masques de découpage : des informations qui indiquent à la carte graphique si un pixel doit être affiché ou non.

- Un nœud sans parent de découpage, mais dont le mode de découpage est défini sur `Stencil`, écrit sa forme (ou l'inverse de sa forme) dans un nouveau masque de découpage stocké dans le tampon de stencil.
- Si un nœud de découpage a un parent de découpage, il découpe alors le masque de découpage de ce parent. Un nœud enfant de découpage ne peut jamais _étendre_ le masque de découpage actuel, seulement le découper davantage.
- Les nœuds qui ne servent pas au découpage et qui sont enfants de nœuds de découpage sont affichés avec le masque de découpage créé par la hiérarchie des parents.

![Hiérarchie de découpage](images/gui-clipping/setup.png)

Ici, trois nœuds sont organisés en une hiérarchie :

- L'hexagone et le carré sont tous deux des nœuds de découpage par stencil.
- L'hexagone crée un nouveau masque de découpage, que le carré découpe davantage.
- Le nœud circulaire est un nœud Pie ordinaire ; il est donc affiché avec le masque de découpage créé par ses parents de découpage.

Quatre combinaisons de nœuds de découpage normaux et inversés sont possibles pour cette hiérarchie. La zone verte indique la partie du cercle qui est affichée. Le reste est masqué :

![Masques de stencil](images/gui-clipping/modes.png)

## Limites du stencil {#stencil-limitations}

- Le nombre total de nœuds de découpage par stencil ne peut pas dépasser 256.
- La profondeur maximale d'imbrication des nœuds enfants de _stencil_ est de huit niveaux. (Seuls les nœuds utilisant le découpage par stencil sont comptés.)
- Le nombre maximal de nœuds stencil frères est de 127. À chaque niveau supplémentaire dans une hiérarchie de stencil, cette limite est divisée par deux.
- Les nœuds inversés ont un coût plus élevé. Le nombre de nœuds de découpage inversés est limité à huit, et chacun divise par deux le nombre maximal de nœuds de découpage non inversés.
- Les stencils produisent un masque de stencil à partir de la _géométrie_ du nœud (et non de sa texture). Vous pouvez inverser le masque en définissant la propriété *Inverted clipper*.


## Couches {#layers}

Les couches permettent de contrôler l'ordre de rendu (et le regroupement des appels de rendu) des nœuds. Lorsque vous utilisez des couches et des nœuds de découpage, l'ordre habituel des couches ne s'applique plus. L'ordre des couches a toujours priorité sur l'ordre de découpage : si vous combinez l'attribution de couches avec des nœuds de découpage, le découpage peut se produire dans le désordre lorsqu'un nœud parent dont le découpage est activé appartient à une couche supérieure à celle de ses enfants. Les enfants auxquels aucune couche n'est attribuée respectent toujours la hiérarchie et sont donc dessinés et découpés après le parent.

::: sidenote
Un nœud de découpage et sa hiérarchie sont dessinés en premier si une couche lui est attribuée, et dans l'ordre habituel si aucune couche ne lui est attribuée.
:::

![Couches et découpage](images/gui-clipping/layers.png)

Dans cet exemple, les deux nœuds de découpage « `Donut BG` » et « `BG` » utilisent la même couche 1. Leur ordre de rendu suit leur ordre dans la hiérarchie, où « `Donut BG` » est dessiné avant « `BG` ». Cependant, le nœud enfant « `Donut Shadow` » est affecté à la couche 2, dont l'ordre est supérieur ; il est donc dessiné après les deux nœuds de découpage. Dans ce cas, l'ordre de rendu est le suivant :

- `Donut BG`
- `BG`
- `BG Frame`
- `Donut Shadow`

Vous pouvez voir ici que l'objet « `Donut Shadow` » est découpé par les deux nœuds de découpage en raison de l'ordre des couches, même s'il n'est l'enfant que de l'un d'entre eux.
