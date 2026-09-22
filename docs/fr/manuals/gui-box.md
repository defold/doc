---
title: Nœuds de boîte d'interface graphique dans Defold
brief: Ce manuel explique comment utiliser les nœuds de boîte d'interface graphique.
---

# Nœuds de boîte d'interface graphique {#gui-box-nodes}

Un nœud de boîte est un rectangle rempli d'une couleur, d'une texture ou d'une animation.

## Ajout de nœuds de boîte {#adding-box-nodes}

Ajoutez de nouveaux nœuds de boîte en effectuant un <kbd>clic droit</kbd> dans l'*Outline* et en sélectionnant <kbd>Add ▸ Box</kbd>, ou appuyez sur <kbd>A</kbd> et sélectionnez <kbd>Box</kbd>.

Vous pouvez utiliser des images et des animations provenant d'atlas ou de sources de tuiles qui ont été ajoutés à l'interface graphique. Pour ajouter des textures, effectuez un <kbd>clic droit</kbd> sur l'icône du dossier *Textures* dans l'*Outline* et sélectionnez <kbd>Add ▸ Textures...</kbd>. Définissez ensuite la propriété *Texture* du nœud de boîte :

![Textures](images/gui-box/create.png)

Notez que la couleur du nœud de boîte teinte les éléments graphiques. La couleur de teinte est multipliée par les données de l'image, ce qui signifie que si vous définissez la couleur sur blanc (la valeur par défaut), aucune teinte n'est appliquée.

![Texture teintée](images/gui-box/tinted.png)

Les nœuds de boîte sont toujours rendus, même si aucune texture ne leur est attribuée, si leur alpha vaut `0` ou si leur taille vaut `0, 0, 0`. Vous devriez toujours attribuer une texture aux nœuds de boîte afin que le moteur de rendu puisse les regrouper correctement et réduire le nombre d'appels de rendu.

## Lecture d'animations {#playing-animations}

Les nœuds de boîte peuvent lire des animations provenant d'atlas ou de sources de tuiles. Consultez le [manuel sur l'animation flipbook](/manuals/flipbook-animation) pour en savoir plus.

:[Slice-9](../shared/slice-9-texturing.md)
