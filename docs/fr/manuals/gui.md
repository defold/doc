---
title: Scènes d'interface graphique dans Defold
brief: Ce manuel présente l'éditeur d'interface graphique de Defold, les différents types de nœuds d'interface graphique et leur programmation par script.
---

# Interface graphique {#gui}

Defold vous propose un éditeur d'interface graphique dédié et de puissantes possibilités de programmation par script, conçus spécialement pour la création et la mise en œuvre d'interfaces utilisateur.

Dans Defold, une interface graphique est un composant (component) que vous créez, attachez à un objet de jeu (game object) et placez dans une collection. Ce composant possède les caractéristiques suivantes :

* Il offre des fonctions de mise en page simples mais puissantes, qui permettent un rendu de votre interface utilisateur indépendant de la résolution et du rapport largeur/hauteur.
* Vous pouvez lui associer un comportement logique au moyen d'un *script GUI*.
* Il est rendu (par défaut) au-dessus des autres contenus, indépendamment de la vue de la caméra. Ainsi, même si votre caméra se déplace, les éléments de votre interface graphique restent en place à l'écran. Ce comportement de rendu peut être modifié.

Les composants GUI sont rendus indépendamment de la vue du jeu. Ils ne sont donc pas placés à un emplacement particulier dans l'éditeur de collection et n'y ont pas de représentation visuelle. Toutefois, les composants GUI doivent résider dans un objet de jeu qui possède un emplacement dans une collection. Modifier cet emplacement n'a aucun effet sur l'interface graphique.

## Création d'un composant GUI {#creating-a-gui-component}

Les composants GUI sont créés à partir d'un fichier prototype de scène d'interface graphique (également appelé « prefab » ou « blueprint » dans d'autres moteurs). Pour créer un composant GUI, <kbd>faites un clic droit</kbd> sur un emplacement dans le navigateur *Assets* et sélectionnez <kbd>New ▸ Gui</kbd>. Saisissez un nom pour le nouveau fichier GUI et appuyez sur <kbd>Ok</kbd>.

![Nouveau fichier GUI](images/gui/new_gui_file.png)

Defold ouvre alors automatiquement le fichier dans l'éditeur de scène d'interface graphique.

![Nouvelle interface graphique](images/gui/new_gui.png)

La vue *Outline* répertorie tout le contenu de l'interface graphique : sa liste de nœuds et ses éventuelles dépendances (voir ci-dessous).

La zone d'édition centrale affiche l'interface graphique. La barre d'outils située dans le coin supérieur droit de cette zone contient les outils *Move*, *Rotate* et *Scale*, ainsi qu'un sélecteur de [mise en page](/manuals/gui-layouts).

![Barre d'outils](images/gui/toolbar.png)

Un rectangle blanc indique les limites de la mise en page actuellement sélectionnée, selon la largeur et la hauteur d'affichage par défaut définies dans les paramètres du projet.

## Propriétés de l'interface graphique {#gui-properties}

Sélectionnez le nœud racine « Gui » dans la vue *Outline* pour afficher les *Properties* du composant GUI :

*Script*
: Le script GUI associé à ce composant GUI.

*Material*
: Le matériau utilisé pour le rendu de cette interface graphique. Vous pouvez également ajouter plusieurs matériaux à une interface graphique depuis le panneau *Outline* et les attribuer à des nœuds individuels.

*Adjust Reference*
: Détermine comment calculer le mode *Adjust Mode* de chaque nœud :

  - `Per Node` ajuste chaque nœud par rapport à la taille ajustée du nœud parent ou à l'écran redimensionné.
  - `Disable` désactive le mode d'ajustement des nœuds. Tous les nœuds sont alors contraints de conserver la taille qui leur a été définie.

*Current Nodes*
: Le nombre de nœuds actuellement utilisés dans cette interface graphique.

*Max Nodes*
: Le nombre maximal de nœuds pour cette interface graphique.

*Max Dynamic Textures*
: Le nombre maximal de textures dynamiques suivies par ce composant GUI, soit `128` par défaut. Cela comprend les textures créées avec [`gui.new_texture()`](/ref/stable/gui/#gui.new_texture:texture_id-width-height-type-buffer-flip) et les textures externes attribuées à l'interface graphique avec `go.set(..., "textures", ...)` ou `gui.set(msg.url(), "textures", ...)`. Les projets qui remplacent de nombreuses textures externes peuvent avoir besoin d'augmenter cette limite.


## Manipulation à l'exécution {#runtime-manipulation}

Vous pouvez manipuler les propriétés de l'interface graphique à l'exécution depuis un composant script avec `go.get()` et `go.set()` :

Polices
: Obtenez ou définissez une police utilisée dans une interface graphique.

![Obtention et définition d'une police](images/gui/get_set_font.png)

```lua
go.property("mybigfont", resource.font("/assets/mybig.font"))

function init(self)
  -- get the font file currently assigned to the font with id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /builtins/fonts/default.font

  -- set the font with id 'default' to the font file assigned to the resource property 'mybigfont'
  go.set("#gui", "fonts", self.mybigfont, { key = "default" })

  -- get the new font file assigned to the font with id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /assets/mybig.font
end
```

Matériaux
: Obtenez ou définissez un matériau utilisé dans une interface graphique.

![Obtention et définition d'un matériau](images/gui/get_set_material.png)

```lua
go.property("myeffect", resource.material("/assets/myeffect.material"))

function init(self)
  -- get the material file currently assigned to the material with id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /effect.material

  -- set the material id 'effect' to the material file assigned to the resource property 'myeffect'
  go.set("#gui", "materials", self.myeffect, { key = "effect" })

  -- get the new material file assigned to the material with id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /assets/myeffect.material
end
```

Textures
: Obtenez ou définissez une texture (atlas) utilisée dans une interface graphique.

![Obtention et définition d'une texture](images/gui/get_set_texture.png)

```lua
go.property("mytheme", resource.atlas("/assets/mytheme.atlas"))

function init(self)
  -- get the texture file currently assigned to the texture with id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /theme.atlas

  -- set the texture with id 'theme' to the texture file assigned to the resource property 'mytheme'
  go.set("#gui", "textures", self.mytheme, { key = "theme" })

  -- get the new texture file assigned to the texture with id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /assets/mytheme.atlas
end
```

## Dépendances {#dependencies}

L'arborescence des ressources d'un jeu Defold est statique. Vous devez donc ajouter au composant toutes les dépendances nécessaires à vos nœuds d'interface graphique. La vue *Outline* regroupe toutes les dépendances par type dans des « dossiers » :

![Dépendances](images/gui/dependencies.png)

Pour ajouter une dépendance, faites-la glisser depuis le panneau *Asset* vers la vue de l'éditeur.

Vous pouvez aussi <kbd>faire un clic droit</kbd> sur la racine « Gui » dans la vue *Outline*, puis sélectionner <kbd>Add ▸ [type]</kbd> dans le menu contextuel.

Vous pouvez également <kbd>faire un clic droit</kbd> sur l'icône de dossier du type à ajouter, puis sélectionner <kbd>Add ▸ [type]</kbd>.

## Types de nœuds {#node-types}

Un composant GUI est constitué d'un ensemble de nœuds. Les nœuds sont des éléments simples. Vous pouvez les transformer (les déplacer, les mettre à l'échelle et les faire pivoter) et les organiser en hiérarchies parent-enfant, dans l'éditeur ou à l'exécution au moyen de scripts. Les types de nœuds suivants sont disponibles :

Nœud Box
: ![Nœud Box](images/icons/gui-box-node.png){.left}
  Nœud rectangulaire affichant une couleur unie, une texture ou une animation image par image. Consultez la [documentation du nœud Box](/manuals/gui-box) pour plus de détails.

<div style="clear: both;"></div>

Nœud Text
: ![Nœud Text](images/icons/gui-text-node.png){.left}
  Affiche du texte. Consultez la [documentation du nœud Text](/manuals/gui-text) pour plus de détails.

<div style="clear: both;"></div>

Nœud Pie
: ![Nœud Pie](images/icons/gui-pie-node.png){.left}
  Nœud circulaire ou elliptique qui peut être partiellement rempli ou inversé. Consultez la [documentation du nœud Pie](/manuals/gui-pie) pour plus de détails.

<div style="clear: both;"></div>

Nœud Template
: ![Nœud Template](images/icons/gui.png){.left}
  Les modèles permettent de créer des instances à partir d'autres fichiers de scène d'interface graphique. Consultez la [documentation du nœud Template](/manuals/gui-template) pour plus de détails.

<div style="clear: both;"></div>

Nœud ParticleFX
: ![Nœud ParticleFX](images/icons/particlefx.png){.left}
  Joue un effet de particules. Consultez la [documentation du nœud ParticleFX](/manuals/gui-particlefx) pour plus de détails.

<div style="clear: both;"></div>

Ajoutez des nœuds en faisant un clic droit sur le dossier *Nodes* et en sélectionnant <kbd>Add ▸</kbd>, puis <kbd>Box</kbd>, <kbd>Text</kbd>, <kbd>Pie</kbd>, <kbd>Template</kbd> ou <kbd>ParticleFx</kbd>.

![Ajout de nœuds](images/gui/add_node.png)

Vous pouvez aussi appuyer sur <kbd>A</kbd> et sélectionner le type à ajouter à l'interface graphique.

## Propriétés des nœuds {#node-properties}

Chaque nœud dispose d'un vaste ensemble de propriétés qui déterminent son apparence :

Id
: L'identifiant du nœud. Ce nom doit être unique au sein de la scène d'interface graphique.

Position, Rotation et Scale
: Déterminent l'emplacement, l'orientation et l'étirement du nœud. Vous pouvez utiliser les outils *Move*, *Rotate* et *Scale* pour modifier ces valeurs. Vous pouvez animer ces valeurs par script ([en savoir plus](/manuals/property-animation)).

Size (nœuds Box, Text et Pie)
: La taille du nœud est automatique par défaut, mais vous pouvez modifier sa valeur en réglant *Size Mode* sur `Manual`. La taille définit les limites du nœud et sert à détecter les entrées qui le ciblent. Vous pouvez animer cette valeur par script ([en savoir plus](/manuals/property-animation)).

Size Mode (nœuds Box et Pie)
: Avec la valeur `Automatic`, l'éditeur définit une taille pour le nœud. Avec la valeur `Manual`, vous pouvez définir vous-même sa taille.

Enabled
: Si cette option est décochée, le nœud n'est ni rendu ni animé, et ne peut pas être détecté avec `gui.pick_node()`. Utilisez `gui.set_enabled()` et `gui.is_enabled()` pour modifier et vérifier cette propriété par programmation.

Visible
: Si cette option est décochée, le nœud n'est pas rendu, mais peut toujours être animé et détecté avec `gui.pick_node()`. Utilisez `gui.set_visible()` et `gui.get_visible()` pour modifier et vérifier cette propriété par programmation.

Text (nœuds Text)
: Le texte à afficher sur le nœud.

Line Break (nœuds Text)
: Active le retour à la ligne du texte en fonction de la largeur du nœud.

Font (nœuds Text)
: La police à utiliser pour le rendu du texte.

Texture (nœuds Box et Pie)
: La texture à dessiner sur le nœud. Il s'agit d'une référence à une image ou à une animation dans un atlas ou une source de tuiles.

Material (nœuds Box, Pie, Text et ParticleFX)
: Le matériau à utiliser pour dessiner le nœud. Vous pouvez choisir un matériau ajouté à la section Materials de la vue *Outline*, ou laisser cette propriété vide pour utiliser le matériau par défaut attribué au composant GUI.

Slice 9 (nœuds Box)
: Définissez cette propriété pour préserver la taille en pixels des bords de la texture du nœud lors de son redimensionnement. Consultez la [documentation du nœud Box](/manuals/gui-box) pour plus de détails.

Inner Radius (nœuds Pie)
: Le rayon intérieur du nœud, exprimé le long de l'axe X. Consultez la [documentation du nœud Pie](/manuals/gui-pie) pour plus de détails.

Outer Bounds (nœuds Pie)
: Détermine le comportement des limites extérieures. Consultez la [documentation du nœud Pie](/manuals/gui-pie) pour plus de détails.

Perimeter Vertices (nœuds Pie)
: Le nombre de segments utilisés pour construire la forme. Consultez la [documentation du nœud Pie](/manuals/gui-pie) pour plus de détails.

Pie Fill Angle (nœuds Pie)
: La portion du secteur à remplir. Consultez la [documentation du nœud Pie](/manuals/gui-pie) pour plus de détails.

Template (nœuds Template)
: Le fichier de scène d'interface graphique à utiliser comme modèle pour le nœud. Consultez la [documentation du nœud Template](/manuals/gui-template) pour plus de détails.

ParticleFX (nœuds ParticleFX)
: L'effet de particules à utiliser sur ce nœud. Consultez la [documentation du nœud ParticleFX](/manuals/gui-particlefx) pour plus de détails.

Color
: La couleur du nœud. Si le nœud possède une texture, cette couleur teinte la texture. Vous pouvez animer la couleur par script ([en savoir plus](/manuals/property-animation)).

Alpha
: La translucidité du nœud. Vous pouvez animer la valeur alpha par script ([en savoir plus](/manuals/property-animation)).

Inherit Alpha
: Cochez cette option pour que le nœud hérite de la valeur alpha du nœud parent. La valeur alpha du nœud est alors multipliée par celle de son parent.

Leading (nœuds Text)
: Un facteur d'échelle pour l'interligne. Une valeur de `0` ne laisse aucun interligne. La valeur `1` (par défaut) correspond à un interligne normal.

Tracking (nœuds Text)
: Un facteur d'échelle pour l'espacement des caractères. La valeur par défaut est 0.

Layer
: Attribuer une couche au nœud remplace l'ordre de dessin normal par l'ordre des couches. Voir ci-dessous pour plus de détails.

Blend mode
: Détermine comment les éléments graphiques du nœud sont mélangés avec ceux de l'arrière-plan :
  - `Alpha` mélange les valeurs des pixels du nœud avec l'arrière-plan selon leur alpha. Cela correspond au mode de fusion « Normal » des logiciels graphiques.
  - `Add` additionne les valeurs des pixels du nœud à celles de l'arrière-plan. Cela correspond au mode « Linear dodge » de certains logiciels graphiques.
  - `Multiply` multiplie les valeurs des pixels du nœud par celles de l'arrière-plan.
  - `Screen` multiplie les valeurs inversées des pixels du nœud et de l'arrière-plan. Cela correspond au mode de fusion « Screen » des logiciels graphiques.

Pivot
: Définit le point de pivot du nœud. Vous pouvez le considérer comme le « point central » du nœud. Toute rotation, mise à l'échelle ou modification de taille s'effectue autour de ce point.

  Les valeurs possibles sont `Center`, `North`, `South`, `East`, `West`, `North West`, `North East`, `South West` ou `South East`.

  ![Point de pivot](images/gui/pivot.png)

  Si vous modifiez le pivot d'un nœud, le nœud est déplacé de façon à placer le nouveau pivot à la position du nœud. Pour les nœuds Text, `Center` centre le texte, `West` l'aligne à gauche et `East` l'aligne à droite.

X Anchor, Y Anchor
: L'ancrage détermine comment la position verticale et horizontale du nœud est modifiée lorsque les limites de la scène ou du nœud parent sont étirées pour s'adapter à la taille physique de l'écran.

  ![Ancrage sans ajustement](images/gui/anchoring_unadjusted.png)

  Les modes d'ancrage suivants sont disponibles :

  - `None` (pour *X Anchor* et *Y Anchor*) maintient la position du nœud par rapport au centre du nœud parent ou de la scène, relativement à sa taille *ajustée*.
  - `Left` ou `Right` (*X Anchor*) met à l'échelle la position horizontale du nœud pour maintenir sa position au même pourcentage de distance des bords gauche et droit du nœud parent ou de la scène.
  - `Top` ou `Bottom` (*Y Anchor*) met à l'échelle la position verticale du nœud pour maintenir sa position au même pourcentage de distance des bords supérieur et inférieur du nœud parent ou de la scène.

  ![Ancrage](images/gui/anchoring.png)

Adjust Mode
: Définit le mode d'ajustement du nœud. Ce réglage détermine ce qui arrive au nœud lorsque les limites de la scène ou du nœud parent sont ajustées pour s'adapter à la taille physique de l'écran.

  Un nœud créé dans une scène dont la résolution logique est une résolution classique en mode paysage :

  ![Sans ajustement](images/gui/unadjusted.png)

  Adapter la scène à un écran en mode portrait étire la scène. Le rectangle englobant de chaque nœud est étiré de la même façon. Toutefois, le réglage du mode d'ajustement permet de préserver le rapport largeur/hauteur du contenu du nœud. Les modes suivants sont disponibles :

  - `Fit` met le contenu du nœud à l'échelle jusqu'à atteindre la largeur ou la hauteur du rectangle englobant étiré, selon la plus petite de ces deux dimensions. Autrement dit, le contenu tient à l'intérieur du rectangle englobant étiré du nœud.
  - `Zoom` met le contenu du nœud à l'échelle jusqu'à atteindre la largeur ou la hauteur du rectangle englobant étiré, selon la plus grande de ces deux dimensions. Autrement dit, le contenu couvre entièrement le rectangle englobant étiré du nœud.
  - `Stretch` étire le contenu du nœud pour remplir son rectangle englobant étiré.

  ![Modes d'ajustement](images/gui/adjusted.png)

  Si la propriété *Adjust Reference* de la scène d'interface graphique est réglée sur `Disabled`, ce réglage est ignoré.

Clipping Mode (nœuds Box et Pie)
: Définit le mode de découpage du nœud :

  - `None` effectue le rendu du nœud comme d'habitude.
  - `Stencil` utilise les limites du nœud pour définir un masque de stencil servant à découper ses nœuds enfants.

  Consultez le [manuel du découpage de l'interface graphique](/manuals/gui-clipping) pour plus de détails.

Clipping Visible (nœuds Box et Pie)
: Activez cette option pour rendre le contenu du nœud dans la zone du stencil. Consultez le [manuel du découpage de l'interface graphique](/manuals/gui-clipping) pour plus de détails.

Clipping Inverted (nœuds Box et Pie)
: Inverse le masque de stencil. Consultez le [manuel du découpage de l'interface graphique](/manuals/gui-clipping) pour plus de détails.


## Pivot, ancrages et mode d'ajustement {#pivot-anchors-and-adjust-mode}

La combinaison des propriétés Pivot, Anchors et Adjust Mode permet de concevoir des interfaces graphiques très flexibles, mais leur fonctionnement peut être difficile à comprendre sans exemple concret. Prenons cette maquette d'interface graphique créée pour un écran de 640x1136 :

![](images/gui/adjustmode_example_original.png)

L'interface utilisateur est créée avec X Anchor et Y Anchor réglés sur None, et le mode Adjust Mode de chaque nœud conserve sa valeur par défaut, Fit. Le point Pivot du panneau supérieur est réglé sur North, celui du panneau inférieur sur South, et ceux des barres du panneau supérieur sur West. Les points de pivot des autres nœuds sont réglés sur Center. Voici ce qui se produit si nous élargissons la fenêtre :

![](images/gui/adjustmode_example_resized.png)

Comment faire pour que les barres du haut et du bas soient toujours aussi larges que l'écran ? Nous pouvons régler Adjust Mode sur Stretch pour les panneaux gris d'arrière-plan situés en haut et en bas :

![](images/gui/adjustmode_example_resized_stretch.png)

C'est mieux. Les panneaux gris d'arrière-plan s'étirent désormais toujours sur toute la largeur de la fenêtre, mais les barres du panneau supérieur et les deux boîtes du bas ne sont pas positionnées correctement. Pour que les barres du haut restent à gauche, nous devons faire passer X Anchor de None à Left :

![](images/gui/adjustmode_example_top_anchor_left.png)

Le panneau supérieur se comporte exactement comme prévu. Les points Pivot de ses barres étaient déjà réglés sur West : elles se positionnent donc correctement, leur bord gauche/ouest (Pivot) étant ancré au bord gauche du panneau parent (X Anchor).

Si nous réglons maintenant X Anchor sur Left pour la boîte de gauche et sur Right pour celle de droite, nous obtenons le résultat suivant :

![](images/gui/adjustmode_example_bottom_anchor_left_right.png)

Ce n'est pas tout à fait le résultat attendu. Les deux boîtes devraient rester aussi proches des bords gauche et droit que les deux barres du panneau supérieur. Ce comportement vient d'un point Pivot mal défini :

![](images/gui/adjustmode_example_bottom_pivot_center.png)

Les deux boîtes ont un point Pivot réglé sur Center. Ainsi, lorsque l'écran s'élargit, le point central (le point de pivot) des boîtes reste à la même distance relative des bords. Pour la boîte de gauche, cette distance était de 17% par rapport au bord gauche dans la fenêtre d'origine de 640x1136 :

![](images/gui/adjustmode_example_original_ratio.png)

Lorsque l'écran est redimensionné, le point central de la boîte de gauche reste à la même distance de 17% du bord gauche :

![](images/gui/adjustmode_example_resized_stretch_ratio.png)

Si nous faisons passer le point Pivot de Center à West pour la boîte de gauche et à East pour celle de droite, puis repositionnons les boîtes, nous obtenons le résultat souhaité, même lorsque l'écran est redimensionné :

![](images/gui/adjustmode_example_bottom_pivot_west_east.png)


## Ordre de dessin {#draw-order}

Tous les nœuds sont rendus dans l'ordre où ils figurent dans le dossier « Nodes ». Le nœud en tête de liste est dessiné en premier et apparaît donc derrière tous les autres. Le dernier nœud de la liste est dessiné en dernier et apparaît donc devant tous les autres. Modifier la valeur Z d'un nœud ne détermine pas son ordre de dessin ; toutefois, si vous définissez une valeur Z en dehors de la plage de rendu de votre script de rendu, le nœud n'est plus affiché à l'écran. Vous pouvez remplacer l'ordre des nœuds fondé sur leurs indices en utilisant des couches (voir ci-dessous).

![Ordre de dessin](images/gui/draw_order.png)

Sélectionnez un nœud et appuyez sur <kbd>Alt + Up/Down</kbd> pour le déplacer vers le haut ou le bas et modifier sa place dans l'ordre des indices.

Vous pouvez modifier l'ordre de dessin par script :

```lua
local bean_node = gui.get_node("bean")
local shield_node = gui.get_node("shield")

if gui.get_index(shield_node) < gui.get_index(bean_node) then
  gui.move_above(shield_node, bean_node)
end
```

## Hiérarchies parent-enfant {#parent-child-hierarchies}

Pour faire d'un nœud l'enfant d'un autre, faites-le glisser sur le nœud qui doit devenir son parent. Un nœud ayant un parent hérite de la transformation (position, rotation et échelle) appliquée au parent, relativement au pivot de celui-ci.

![Parent et enfant](images/gui/parent_child.png)

Les parents sont dessinés avant leurs enfants. Utilisez des couches pour modifier l'ordre de dessin des nœuds parents et enfants et pour optimiser le rendu des nœuds (voir ci-dessous).


## Couches et appels de dessin {#layers-and-draw-calls}

Les couches offrent un contrôle précis sur la façon dont les nœuds sont dessinés et permettent de réduire le nombre d'appels de dessin que le moteur doit créer pour dessiner une scène d'interface graphique. Lorsque le moteur s'apprête à dessiner les nœuds d'une scène d'interface graphique, il les regroupe en lots d'appels de dessin selon les conditions suivantes :

- Les nœuds doivent être du même type.
- Les nœuds doivent utiliser le même atlas ou la même source de tuiles.
- Les nœuds doivent être rendus avec le même mode de fusion.
- Ils doivent utiliser la même police.

Si un nœud diffère du précédent sur l'un de ces points, il interrompt le lot et crée un autre appel de dessin. Les nœuds de découpage interrompent toujours le lot, tout comme chaque zone d'application d'un stencil.

La possibilité d'organiser les nœuds en hiérarchies facilite leur regroupement en unités faciles à gérer. Cependant, ces hiérarchies peuvent interrompre le rendu par lots si vous mélangez différents types de nœuds :

![Hiérarchie interrompant le rendu par lots](images/gui/break_batch.png)

Lorsque le pipeline de rendu parcourt la liste des nœuds, il doit créer un lot distinct pour chaque nœud, car leurs types diffèrent. Au total, ces trois boutons nécessitent six appels de dessin.

Attribuer des couches aux nœuds permet de les ordonner différemment. Le pipeline de rendu peut ainsi les regrouper dans un nombre réduit d'appels de dessin. Commencez par ajouter à la scène les couches dont vous avez besoin. <kbd>Faites un clic droit</kbd> sur l'icône du dossier « Layers » dans la vue *Outline* et sélectionnez <kbd>Add ▸ Layer</kbd>. Sélectionnez la nouvelle couche et attribuez-lui une propriété *Name* dans la vue *Properties*.

![Couches](images/gui/layers.png)

Réglez ensuite la propriété *Layer* de chaque nœud sur la couche correspondante. L'ordre de dessin des couches est prioritaire sur l'ordre habituel des nœuds fondé sur leurs indices. Ainsi, attribuer « graphics » aux nœuds Box des éléments graphiques des boutons et « text » aux nœuds Text des boutons produit l'ordre de dessin suivant :

* D'abord, tous les nœuds de la couche « graphics », à partir du haut :

  1. "button-1"
  2. "button-2"
  3. "button-3"

* Puis, tous les nœuds de la couche « text », à partir du haut :

  4. "button-text-1"
  5. "button-text-2"
  6. "button-text-3"

Les nœuds peuvent maintenant être regroupés en deux appels de dessin au lieu de six. Un gain de performances considérable !

Un nœud enfant dont la couche n'est pas définie hérite implicitement de la couche de son parent. Ne pas définir de couche pour un nœud l'ajoute implicitement à la couche « null », qui est dessinée avant toutes les autres.
