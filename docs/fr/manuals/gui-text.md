---
title: Nœuds de texte d'interface graphique dans Defold
brief: Ce manuel décrit comment ajouter du texte aux scènes d'interface graphique.
---

# Nœuds de texte d'interface graphique {#gui-text-nodes}

Defold prend en charge un type spécifique de nœud d'interface graphique qui permet d'afficher du texte dans une scène d'interface graphique. Toute ressource de police ajoutée à un projet peut être utilisée pour le rendu des nœuds de texte.

L'aperçu de l'éditeur prend en charge la mise en forme des glyphes et la mise en page de droite à gauche grâce au moteur de rendu des polices du moteur. Consultez [Prise en charge de la mise en page du texte](/manuals/font/#text-layout-support-eg-right-to-left) pour connaître les paramètres de police et d'App Manifest nécessaires.

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

## Polices vectorielles et émojis en couleur {#vector-fonts-and-color-emoji}

Suivez la [configuration des polices vectorielles](/manuals/font/#vector-fonts), ajoutez la ressource `.font` aux *Fonts* de la scène GUI et sélectionnez-la sur le nœud de texte. Définissez le *Material* de la ressource de police sur `/builtins/fonts/font-vector.material`. Utilisez *Font Size* du nœud pour contrôler la taille affichée.

Pour les émojis en couleur, effectuez également la [configuration de la police de repli COLRv1 et de sa mise en bundle](/manuals/font/#color-emoji). Créez un nœud de texte avec l'identifiant `text`, laissez son champ *Text* vide et ajoutez ce qui suit au `.gui_script` de la scène GUI :

```lua
function init(self)
    local node = gui.get_node("text")
    local text = "Hello 😀 🍎 🚀"
    local font_resource = gui.get_font_resource(gui.get_font(node))
    -- Add the fallback once for this shared font resource.
    font.add_font(font_resource, "/fonts/NotoColorEmoji-Regular.ttf")
    font.prewarm_text(font_resource, text, function(self, request_id, result, err)
        if result then
            gui.set_text(node, text)
        else
            print("Could not prepare GUI text:", err)
        end
    end)
end
```

[`gui.get_font()`](/ref/gui/#gui.get_font) renvoie le nom de la police dans la scène GUI ; [`gui.get_font_resource()`](/ref/gui/#gui.get_font_resource) résout ce nom en ressource de police utilisable par `font.add_font()`. Les autres nœuds et labels partageant cette ressource reçoivent aussi la police de repli ; initialisez-la donc une seule fois. Le texte est défini une fois le préchargement terminé avec succès.


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
