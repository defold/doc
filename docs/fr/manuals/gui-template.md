---
title: Manuel des modèles d'interface graphique
brief: Ce manuel explique le système de modèles d'interface graphique de Defold, qui permet de créer des composants visuels d'interface graphique réutilisables à partir de modèles partagés ou de « prefabs ».
---

# Nœuds de modèle d'interface graphique {#gui-template-nodes}

Les nœuds de modèle d'interface graphique offrent un mécanisme puissant pour créer des composants (components) d'interface graphique réutilisables à partir de modèles partagés ou de « prefabs ». Ce manuel explique cette fonctionnalité et son utilisation.

Un modèle d'interface graphique est une scène d'interface graphique instanciée, nœud par nœud, dans une autre scène d'interface graphique. Vous pouvez ensuite remplacer n'importe quelle valeur de propriété des nœuds du modèle d'origine.

## Création d'un modèle {#creating-a-template}

Un modèle d'interface graphique est une scène d'interface graphique ordinaire et se crée donc comme toute autre scène d'interface graphique. <kbd>Faites un clic droit</kbd> à un emplacement dans le panneau *Assets* et sélectionnez <kbd>New... ▸ Gui</kbd>.

![Création d'un modèle](images/gui-templates/create.png)

Créez le modèle et enregistrez-le. Notez que les nœuds de l'instance seront placés par rapport à l'origine ; il est donc préférable de créer le modèle à la position 0, 0, 0.

## Création d'instances à partir d'un modèle {#creating-instances-from-a-template}

Vous pouvez créer autant d'instances que vous le souhaitez à partir de l'instance. Créez ou ouvrez la scène d'interface graphique dans laquelle vous souhaitez placer le modèle, puis <kbd>faites un clic droit</kbd> sur la section *Nodes* de la vue *Outline* et sélectionnez <kbd>Add ▸ Template</kbd>.

![Création d'une instance](images/gui-templates/create_instance.png)

Définissez la propriété *Template* sur le fichier de scène d'interface graphique du modèle.

Vous pouvez ajouter autant d'instances de modèle que vous le souhaitez et, pour chaque instance, remplacer les propriétés de chaque nœud et modifier la position, la couleur, la taille, la texture, etc. des nœuds de l'instance.

![Instances](images/gui-templates/instances.png)

Toute propriété que vous modifiez est marquée en bleu dans l'éditeur. Appuyez sur le bouton de réinitialisation à côté de la propriété pour lui redonner la valeur du modèle :

![Propriétés](images/gui-templates/properties.png)

Tout nœud dont certaines propriétés ont été remplacées apparaît également en bleu dans la vue *Outline* :

![Vue d'ensemble](images/gui-templates/outline.png)

L'instance de modèle apparaît sous la forme d'une entrée repliable dans la vue *Outline*. Il est toutefois important de noter que cet élément de la vue *n'est pas un nœud*. L'instance de modèle n'existe pas non plus à l'exécution, mais tous les nœuds qui en font partie existent.

Les nœuds qui font partie d'une instance de modèle sont automatiquement nommés en ajoutant un préfixe et une barre oblique (`"/"`) devant leur *Id*. Le préfixe est l'*Id* défini dans l'instance de modèle.

## Modification des modèles à l'exécution {#modifying-templates-in-runtime}

Les scripts qui manipulent ou interrogent les nœuds ajoutés au moyen du mécanisme de modèles doivent seulement tenir compte du nommage des nœuds de l'instance et inclure l'*Id* de l'instance de modèle comme préfixe du nom du nœud :

```lua
if gui.pick_node(gui.get_node("button_1/button"), x, y) then
    -- Do something...
end
```

Il n'existe aucun nœud correspondant à l'instance de modèle elle-même. Si vous avez besoin d'un nœud racine pour une instance, ajoutez-le au modèle.

Si un script est associé à une scène d'interface graphique utilisée comme modèle, ce script ne fait pas partie de l'arborescence des nœuds de l'instance. Vous ne pouvez attacher qu'un seul script à chaque scène d'interface graphique ; la logique de votre script doit donc se trouver dans la scène d'interface graphique où vous avez instancié vos modèles.
