---
title: Nœuds de texte d'interface graphique dans Defold
brief: Ce manuel décrit comment ajouter du texte aux scènes d'interface graphique.
---

# Nœuds de texte d'interface graphique {#gui-text-nodes}

Defold prend en charge un type spécifique de nœud d'interface graphique qui permet d'afficher du texte dans une scène d'interface graphique. Toute ressource de police ajoutée à un projet peut être utilisée pour le rendu des nœuds de texte.

## Ajout de nœuds de texte {#adding-text-nodes}

Les polices que vous souhaitez utiliser dans les nœuds de texte d'interface graphique doivent être ajoutées au composant (component) d'interface graphique. Faites un clic droit sur le dossier *Fonts*, utilisez le menu supérieur <kbd>GUI</kbd> ou appuyez sur le raccourci clavier correspondant.

![Polices](images/gui-text/fonts.png)

Les nœuds de texte possèdent un ensemble de propriétés spécifiques :

*Font*
: Tout nœud de texte que vous créez doit avoir une valeur définie pour la propriété *Font*.

*Text*
: Cette propriété contient le texte affiché.

*Line Break*
: L'alignement du texte suit le réglage du pivot et l'activation de cette propriété permet au texte de s'étendre sur plusieurs lignes. La largeur du nœud détermine les endroits où le texte passe à la ligne.

## Alignement {#alignment}

En définissant le pivot du nœud, vous pouvez modifier le mode d'alignement du texte.

*Centré*
: Si le pivot est défini sur `Center`, `North` ou `South`, le texte est centré.

*À gauche*
: Si le pivot est défini sur l'un des modes `West`, le texte est aligné à gauche.

*À droite*
: Si le pivot est défini sur l'un des modes `East`, le texte est aligné à droite.

![Alignement du texte](images/gui-text/align.png)

## Modification des nœuds de texte à l'exécution {#modifying-text-nodes-in-runtime}

Les nœuds de texte répondent à toutes les fonctions génériques de manipulation des nœuds permettant de définir la taille, le pivot, la couleur, etc. Quelques fonctions sont propres aux nœuds de texte :

* Pour modifier la police d'un nœud de texte, utilisez la fonction [`gui.set_font()`](/ref/gui/#gui.set_font).
* Pour modifier le comportement de retour à la ligne d'un nœud de texte, utilisez la fonction [`gui.set_line_break()`](/ref/gui/#gui.set_line_break).
* Pour modifier le contenu d'un nœud de texte, utilisez la fonction [`gui.set_text()`](/ref/gui/#gui.set_text).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("set_score") then
        local s = gui.get_node("score")
        gui.set_text(s, message.score)
    end
end
```

