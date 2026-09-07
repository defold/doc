## Texturage en neuf tranches {#slice-9-texturing}

Les nœuds Box de l'interface graphique et les composants sprite (sprite components) comportent parfois des éléments dont la taille dépend du contexte : des panneaux et des boîtes de dialogue qui doivent être redimensionnés pour s'adapter à leur contenu, ou une barre de vie qui doit être redimensionnée pour indiquer les points de vie restants d'un ennemi. Cela peut entraîner des problèmes visuels lorsque vous appliquez une texture au nœud ou au sprite redimensionné.

Normalement, le moteur met la texture à l'échelle pour l'adapter aux limites du rectangle, mais la définition de zones de bordure pour le découpage en neuf tranches (slice-9) permet de limiter les parties de la texture qui doivent être mises à l'échelle :

![Mise à l'échelle de l'interface graphique](../shared/images/gui_slice9_scaling.png)

Le paramètre *Slice9* du nœud Box se compose de quatre nombres qui indiquent le nombre de pixels des marges gauche, supérieure, droite et inférieure qui ne doivent pas être mises à l'échelle de la manière habituelle :

![Propriétés du découpage en neuf tranches](../shared/images/gui_slice9_properties.png)

Les marges sont définies dans le sens des aiguilles d'une montre, en partant du bord gauche :

![Sections du découpage en neuf tranches](../shared/images/gui_slice9.png)

- Les segments des coins ne sont jamais mis à l'échelle.
- Les segments des bords sont mis à l'échelle selon un seul axe. Les segments des bords gauche et droit sont mis à l'échelle verticalement. Les segments des bords supérieur et inférieur sont mis à l'échelle horizontalement.
- La zone centrale de la texture est mise à l'échelle horizontalement et verticalement selon les besoins.

La mise à l'échelle de la texture avec *Slice9* décrite ci-dessus s'applique uniquement lorsque vous modifiez la taille du nœud Box ou du sprite :

![Taille du nœud Box de l'interface graphique](../shared/images/gui_slice9_size.png)

![Taille du sprite](../shared/images/sprite_slice9_size.png)

::: important
Si vous modifiez le paramètre d'échelle du nœud Box, du sprite ou de l'objet de jeu (game object), le nœud ou le sprite et la texture sont mis à l'échelle sans appliquer les paramètres *Slice9*.
:::

::: important
Lorsque vous utilisez le texturage en neuf tranches sur des sprites, le [paramètre Sprite Trim Mode de l'image](https://defold.com/manuals/atlas/#image-properties) doit être réglé sur Off.
:::


### Mipmaps et découpage en neuf tranches {#mipmaps-and-slice-9}
En raison du fonctionnement du mipmapping dans le moteur de rendu, la mise à l'échelle des segments de texture peut parfois présenter des artefacts. Cela se produit lorsque vous _réduisez la taille_ des segments en dessous de la taille de la texture d'origine. Le moteur de rendu sélectionne alors un mipmap de résolution inférieure pour le segment, ce qui entraîne des artefacts visuels.

![Mipmapping du découpage en neuf tranches](../shared/images/gui_slice9_mipmap.png)

Pour éviter ce problème, assurez-vous que les segments de la texture qui seront mis à l'échelle sont suffisamment petits pour ne jamais devoir être réduits, mais uniquement agrandis.
