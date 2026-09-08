---
title: Adapter les graphismes à différentes tailles d'écran
brief: Ce manuel explique comment adapter votre jeu et ses graphismes à différentes tailles d'écran.
---

# Introduction {#introduction}

Plusieurs points sont à prendre en compte pour adapter votre jeu et ses graphismes à différentes tailles d'écran :

* S'agit-il d'un jeu rétro aux graphismes en basse résolution précis au pixel près, ou d'un jeu moderne aux graphismes de qualité HD ?
* Comment le jeu doit-il se comporter lorsqu'il est joué en plein écran sur des écrans de différentes tailles ?
  * Le joueur doit-il voir davantage de contenu du jeu sur un écran haute résolution, ou les graphismes doivent-ils ajuster leur zoom pour toujours afficher le même contenu ?
* Comment le jeu doit-il gérer les rapports largeur/hauteur différents de celui que vous avez défini dans *game.project* ?
  * Le joueur doit-il voir davantage de contenu du jeu ? Faut-il plutôt ajouter des bandes noires ? Ou peut-être redimensionner les éléments de l'interface graphique ?
* De quels types de menus et de composants (components) d'interface graphique à l'écran avez-vous besoin, et comment doivent-ils s'adapter aux différentes tailles et orientations d'écran ?
  * La disposition des menus et des autres composants d'interface graphique doit-elle changer avec l'orientation, ou rester identique quelle que soit l'orientation ?

Ce manuel abordera certains de ces points et proposera de bonnes pratiques.


## Comment modifier le rendu de votre contenu {#how-to-change-how-your-content-is-rendered}

Le script de rendu de Defold vous donne un contrôle total sur l'ensemble du pipeline de rendu. Il décide de ce qui est dessiné, de l'ordre dans lequel les éléments sont dessinés et de la manière de les dessiner. Par défaut, le script de rendu dessine toujours la même zone de pixels, définie par la largeur et la hauteur dans le fichier *game.project*, même si la fenêtre est redimensionnée ou si la résolution réelle de l'écran ne correspond pas. Le contenu sera donc étiré si le rapport largeur/hauteur change, et agrandi ou réduit si la taille de la fenêtre change. Cela peut être acceptable dans certains jeux, mais vous souhaiterez plus probablement afficher davantage ou moins de contenu du jeu si la résolution ou le rapport largeur/hauteur de l'écran diffère, ou au moins veiller à agrandir ou réduire le contenu sans modifier son rapport largeur/hauteur. Le comportement d'étirement par défaut peut être facilement modifié ; vous trouverez plus d'informations sur la façon de procéder dans le [manuel du rendu](https://www.defold.com/manuals/render/#default-view-projection).


## Graphismes rétro/8 bits {#retro8-bit-graphics}

Les graphismes rétro/8 bits désignent souvent des jeux qui reproduisent le style graphique des anciennes consoles de jeux ou des anciens ordinateurs, avec leur basse résolution et leur palette de couleurs limitée. Par exemple, la Nintendo Entertainment System (NES) avait une résolution d'écran de 256x240, le Commodore 64 de 320x200 et la Gameboy de 160x144, des dimensions qui ne représentent qu'une fraction de celles des écrans modernes. Pour que les jeux qui reproduisent ce style graphique et cette résolution d'écran soient jouables sur un écran moderne haute résolution, il faut agrandir les graphismes plusieurs fois. Une façon simple de procéder consiste à dessiner tous vos graphismes dans la basse résolution et le style que vous souhaitez reproduire, puis à les agrandir lors du rendu. Vous pouvez facilement le faire dans Defold à l'aide du script de rendu et de la [projection fixe](/manuals/render/#fixed-projection), avec une valeur de zoom adaptée.

Prenons ce jeu de tuiles et ce personnage joueur ([source](https://ansimuz.itch.io/grotto-escape-game-art-pack)) et utilisons-les dans un jeu rétro 8 bits d'une résolution de 320x200 :

![](images/screen_size/retro-player.png)

![](images/screen_size/retro-tiles.png)

En définissant une résolution de 320x200 dans le fichier *game.project* et en lançant le jeu, vous obtiendrez ceci :

![](images/screen_size/retro-original_320x200.png)

La fenêtre est vraiment minuscule sur un écran moderne haute résolution ! En multipliant ses dimensions par quatre, pour atteindre 1280x800, elle devient plus adaptée à un écran moderne :

![](images/screen_size/retro-original_1280x800.png)

Maintenant que la taille de la fenêtre est plus raisonnable, nous devons également adapter les graphismes. Ils sont si petits qu'il est très difficile de voir ce qui se passe dans le jeu. Nous pouvons utiliser le script de rendu pour définir une projection fixe avec un zoom :

```Lua
msg.post("@render:", "use_fixed_projection", { zoom = 4 })
```

::: sidenote
Vous pouvez obtenir le même résultat en attachant un [composant caméra](/manuals/camera/) à un objet de jeu (game object), en cochant *Orthographic Projection* et en réglant *Orthographic Zoom* sur 4.0 :

![](images/screen_size/retro-camera_zoom.png)
:::

Vous obtiendrez le résultat suivant :

![](images/screen_size/retro-zoomed_1280x800.png)

C'est mieux. La fenêtre et les graphismes ont maintenant une taille convenable, mais en regardant de plus près, un problème évident apparaît :

![](images/screen_size/retro-zoomed_linear.png)

Les graphismes sont flous ! Cela vient de la façon dont les graphismes agrandis sont échantillonnés à partir de la texture lors du rendu par le GPU. Dans la section *Graphics* du fichier *game.project*, le réglage par défaut est *linear* :

![](images/screen_size/retro-settings_linear.png)

En le remplaçant par *nearest*, vous obtiendrez le résultat recherché :

![](images/screen_size/retro-settings_nearest.png)

![](images/screen_size/retro-zoomed_nearest.png)

Nous avons maintenant des graphismes nets et précis *au pixel près* pour notre jeu rétro. D'autres points sont à prendre en compte, comme la désactivation des sous-pixels pour les sprites dans *game.project* :

![](images/screen_size/retro-subpixels.png)

Lorsque l'option *Subpixels* est désactivée, les sprites ne sont jamais dessinés sur des demi-pixels : ils sont toujours alignés sur le pixel entier le plus proche.

## Graphismes haute résolution {#high-resolution-graphics}

Avec des graphismes haute résolution, nous devons aborder la configuration du projet et du contenu différemment de celle des graphismes rétro/8 bits. Avec des images matricielles, vous devez créer votre contenu de façon à ce qu'il ait un bon rendu sur un écran haute résolution lorsqu'il est affiché à l'échelle 1:1.

Comme pour les graphismes rétro/8 bits, vous devez modifier le script de rendu. Dans ce cas, les graphismes doivent être mis à l'échelle en fonction de la taille de l'écran tout en conservant leur rapport largeur/hauteur d'origine :

```Lua
msg.post("@render:", "use_fixed_fit_projection")
```

L'écran sera ainsi redimensionné de façon à toujours afficher la même quantité de contenu que celle définie dans le fichier *game.project*, avec éventuellement du contenu supplémentaire au-dessus et en dessous ou sur les côtés, selon que le rapport largeur/hauteur diffère ou non.

Vous devriez définir la largeur et la hauteur dans le fichier *game.project* à des dimensions qui permettent d'afficher le contenu de votre jeu sans mise à l'échelle.

### Paramètre de haute densité de pixels et écrans retina {#high-dpi-setting-and-retina-screens}

Si vous souhaitez également prendre en charge les écrans retina haute résolution, vous pouvez activer cette option dans la section Display du fichier *game.project* :

![](images/screen_size/highdpi-enabled.png)

Cela crée un tampon arrière à haute densité de pixels sur les écrans qui le prennent en charge. Le rendu du jeu utilisera une résolution deux fois supérieure à celle définie dans les paramètres Width et Height, qui restera la résolution logique utilisée dans les scripts et les propriétés. Toutes les mesures restent donc identiques, et tout contenu rendu à l'échelle 1x aura la même apparence. En revanche, si vous importez des images haute résolution et que vous les réduisez à l'échelle 0.5x, elles seront affichées à haute densité de pixels à l'écran.


## Créer une interface graphique adaptative {#creating-an-adaptive-gui}

Le système de création de composants d'interface graphique repose sur un ensemble d'éléments de base, ou [nœuds](/manuals/gui/#node-types). Même s'il peut sembler trop simple, il permet de créer aussi bien des boutons que des menus et des fenêtres contextuelles complexes. Les interfaces graphiques que vous créez peuvent être configurées pour s'adapter automatiquement aux changements de taille et d'orientation de l'écran. Vous pouvez par exemple maintenir des *nœuds* ancrés en haut, en bas ou sur les côtés de l'écran, et les nœuds peuvent conserver leur taille ou s'étirer. Les relations entre les *nœuds*, ainsi que leur taille et leur apparence, peuvent également être configurées pour changer lorsque la taille ou l'orientation de l'écran change.

### Propriétés des *nœuds* {#node-properties}

Chaque *nœud* d'une interface graphique possède un point de pivot, un ancrage horizontal et vertical, ainsi qu'un mode d'ajustement.

* Le point de pivot définit le point central d'un nœud.
* Le mode d'ancrage contrôle la façon dont la position verticale et horizontale du nœud est modifiée lorsque les limites de la scène, ou celles du nœud parent, sont étirées pour correspondre à la taille physique de l'écran.
* Le mode d'ajustement contrôle ce qui arrive à un nœud lorsque les limites de la scène, ou celles du nœud parent, sont ajustées pour correspondre à la taille physique de l'écran.

Vous trouverez plus d'informations sur ces propriétés [dans le manuel de l'interface graphique](/manuals/gui/#node-properties).

### Dispositions {#layouts}

Defold prend en charge les interfaces graphiques qui s'adaptent automatiquement aux changements d'orientation de l'écran sur les appareils mobiles. Grâce à cette fonctionnalité, vous pouvez concevoir une interface graphique capable de s'adapter à l'orientation et au rapport largeur/hauteur de différentes tailles d'écran. Vous pouvez également créer des dispositions adaptées à des modèles d'appareils particuliers. Vous trouverez plus d'informations sur ce système dans le [manuel des dispositions d'interface graphique](/manuals/gui-layouts/)


## Tester différentes tailles d'écran {#testing-different-screen-sizes}

Le menu *Debug* contient une option permettant de simuler la résolution d'un modèle d'appareil donné ou une résolution personnalisée. Pendant l'exécution de l'application, vous pouvez sélectionner <kbd>Debug->Simulate Resolution</kbd> et choisir l'un des modèles d'appareils de la liste. La fenêtre de l'application en cours d'exécution sera redimensionnée et vous pourrez voir à quoi ressemble votre jeu avec une autre résolution ou un autre rapport largeur/hauteur.

![](images/screen_size/simulate-resolution.png)
