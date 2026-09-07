---
title: Composants de texte Label dans Defold
brief: Ce manuel explique comment utiliser les composants Label pour afficher du texte avec des objets de jeu dans le monde de jeu.
---

# Libellé {#label}

Un composant (component) *Label* affiche une portion de texte à l'écran, dans l'espace de jeu. Par défaut, il est trié et dessiné avec tous les sprites et les éléments graphiques à base de tuiles. Le composant possède un ensemble de propriétés qui déterminent le rendu du texte. L'interface graphique de Defold prend en charge le texte, mais il peut être délicat de placer des éléments d'interface graphique dans le monde de jeu (game world). Les libellés facilitent cette tâche.

## Création d'un libellé {#creating-a-label}

Pour créer un composant Label, faites un <kbd>clic droit</kbd> sur l'objet de jeu (game object) et sélectionnez <kbd>Add Component ▸ Label</kbd>.

![Ajouter un libellé](images/label/add_label.png)

(Si vous souhaitez instancier plusieurs libellés à partir du même modèle, vous pouvez aussi créer un nouveau fichier de composant Label : faites un <kbd>clic droit</kbd> sur un dossier dans le navigateur *Assets* et sélectionnez <kbd>New... ▸ Label</kbd>, puis ajoutez le fichier en tant que composant aux objets de jeu de votre choix)

![Nouveau libellé](images/label/label.png)

Définissez la propriété *Font* sur la police que vous souhaitez utiliser et veillez à définir la propriété *Material* sur un matériau correspondant au type de police :

![Police et matériau](images/label/font_material.png)

## Propriétés du libellé {#label-properties}

Outre les propriétés *Id*, *Position*, *Rotation* et *Scale*, les propriétés suivantes sont propres au composant :

*Text*
: Le contenu textuel du libellé.

*Size*
: La taille du rectangle englobant du texte. Si *Line Break* est activée, la largeur indique à quel endroit le texte doit passer à la ligne.

*Color*
: La couleur du texte.

*Outline*
: La couleur du contour.

*Shadow*
: La couleur de l'ombre.

::: sidenote
Notez que le rendu de l'ombre est désactivé dans le matériau par défaut pour des raisons de performances.
:::

*Leading*
: Un facteur d'échelle pour l'interligne. Une valeur de 0 supprime l'interligne. La valeur par défaut est 1.

*Tracking*
: Un facteur d'échelle pour l'espacement entre les lettres. La valeur par défaut est 0.

*Pivot*
: Le pivot du texte. Utilisez cette propriété pour modifier l'alignement du texte (voir ci-dessous).

*Blend Mode*
: Le mode de fusion à utiliser pour le rendu du libellé.

*Line Break*
: L'alignement du texte suit le réglage du pivot et l'activation de cette propriété permet au texte de s'étendre sur plusieurs lignes. La largeur du composant détermine l'endroit où le texte passe à la ligne. Notez que le texte doit contenir une espace pour pouvoir passer à la ligne.

*Font*
: La ressource de police à utiliser pour ce libellé.

*Material*
: Le matériau à utiliser pour le rendu de ce libellé. Veillez à sélectionner un matériau créé pour le type de police que vous utilisez (bitmap, à champ de distance ou BMFont).

### Modes de fusion {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

### Pivot et alignement {#pivot-and-alignment}

La propriété *Pivot* vous permet de modifier le mode d'alignement du texte.

*Centré*
: Si le pivot est défini sur `Center`, `North` ou `South`, le texte est centré.

*À gauche*
: Si le pivot est défini sur l'un des modes `West`, le texte est aligné à gauche.

*À droite*
: Si le pivot est défini sur l'un des modes `East`, le texte est aligné à droite.

![Alignement du texte](images/label/align.png)

## Manipulation à l'exécution {#runtime-manipulation}

Vous pouvez manipuler les libellés à l'exécution en récupérant et en définissant leur texte ainsi que leurs diverses autres propriétés.

`color`
: La couleur du libellé (`vector4`)

`outline`
: La couleur du contour du libellé (`vector4`)

`shadow`
: La couleur de l'ombre du libellé (`vector4`)

`scale`
: L'échelle du libellé, soit un `number` pour une mise à l'échelle uniforme, soit un `vector3` pour une mise à l'échelle distincte sur chaque axe.

`size`
: La taille du libellé (`vector3`)

```lua
function init(self)
    -- Set the text of the "my_label" component in the same game object
    -- as this script.
    label.set_text("#my_label", "New text")
end
```

```lua
function init(self)
    -- Set the color of the "my_label" component in the same game object
    -- as this script. Color is a RGBA value stored in a vector4.
    local grey = vmath.vector4(0.5, 0.5, 0.5, 1.0)
    go.set("#my_label", "color", grey)

    -- ...and remove the outline, by setting its alpha to 0...
    go.set("#my_label", "outline.w", 0)

    -- ...and scale it x2 along x axis.
    local scale_x = go.get("#my_label", "scale.x")
    go.set("#my_label", "scale.x", scale_x * 2)
end
```

## Configuration du projet {#project-configuration}

Le fichier *game.project* comporte quelques [paramètres du projet](/manuals/project-settings#label) liés aux libellés.
