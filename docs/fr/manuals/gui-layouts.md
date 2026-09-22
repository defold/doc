---
title: Mises en page des interfaces graphiques dans Defold
brief: Defold prend en charge les interfaces graphiques qui s'adaptent automatiquement aux changements d'orientation de l'écran sur les appareils mobiles. Ce document explique le fonctionnement de cette fonctionnalité.
---

# Mises en page {#layouts}

Defold prend en charge les interfaces graphiques qui s'adaptent automatiquement aux changements d'orientation de l'écran sur les appareils mobiles. Cette fonctionnalité vous permet de concevoir des interfaces graphiques qui s'adaptent à l'orientation et au rapport largeur/hauteur d'écrans de différentes tailles. Vous pouvez également créer des mises en page qui correspondent à des modèles d'appareils particuliers.

## Création de profils d'affichage {#creating-display-profiles}

Par défaut, les paramètres de *game.project* spécifient l'utilisation d'un fichier intégré de paramètres de profils d'affichage ("builtins/render/default.display_profiles"). Les profils par défaut sont "Landscape" (1280 pixels de large et 720 pixels de haut) et "Portrait" (720 pixels de large et 1280 pixels de haut). Aucun modèle d'appareil n'est défini dans ces profils, ils correspondent donc à tous les appareils.

Pour créer un nouveau fichier de paramètres de profils, copiez celui du dossier "builtins" ou <kbd>faites un clic droit</kbd> sur un emplacement approprié dans la vue *Assets* et sélectionnez <kbd>New... ▸ Display Profiles</kbd>. Donnez un nom approprié au nouveau fichier et cliquez sur <kbd>Ok</kbd>.

L'éditeur ouvre alors le nouveau fichier pour vous permettre de le modifier. Ajoutez de nouveaux profils en cliquant sur le <kbd>+</kbd> dans la liste *Profiles*. Pour chaque profil, ajoutez un ensemble de *critères* :

Width
: La largeur en pixels du critère.

Height
: La hauteur en pixels du critère.

Device Models
: Une liste de modèles d'appareils séparés par des virgules. Le modèle d'appareil indiqué est comparé au début du nom de modèle de l'appareil. Par exemple, `iPhone10` correspond aux modèles "iPhone10,\*". Les noms de modèles qui contiennent des virgules doivent être placés entre guillemets. Ainsi, `"iPhone10,3", "iPhone10,6"` correspond aux modèles iPhone X (voir le [wiki iPhone](https://www.theiphonewiki.com/wiki/Models)). Notez qu'Android et iOS sont les seules plateformes qui indiquent un modèle d'appareil lors de l'appel à `sys.get_sys_info()`. Les autres plateformes renvoient une chaîne vide et ne sélectionneront donc jamais un profil d'affichage qui comporte un critère de modèle d'appareil.

![Nouveaux profils d'affichage](images/gui-layouts/new_profiles.png)

Vous devez également indiquer au moteur d'utiliser vos nouveaux profils. Ouvrez *game.project* et sélectionnez le fichier de profils d'affichage dans le paramètre *Display Profiles*, sous *display* :

![Paramètres](images/gui-layouts/settings.png)

Si vous souhaitez que le moteur alterne automatiquement entre les mises en page portrait et paysage lors de la rotation de l'appareil, cochez la case *Dynamic Orientation*. Le moteur sélectionnera dynamiquement une mise en page correspondante et modifiera également cette sélection si l'appareil change d'orientation.

### Sélection automatique de la mise en page (profils d'affichage) {#auto-layout-selection-display-profiles}

La ressource Display Profiles possède une option « Auto Layout Selection » (sur ON par défaut). Lorsqu'elle est sur ON, le moteur sélectionne automatiquement la mise en page d'interface graphique la plus adaptée à la création de la scène et lorsque la taille de la fenêtre ou de l'écran change. Lorsqu'elle est sur OFF, le moteur ne change pas automatiquement de mise en page : utilisez `gui.set_layout()` dans votre script GUI pour changer de mise en page manuellement. Ce paramètre est enregistré dans le fichier Display Profiles et s'applique à toutes les scènes d'interface graphique.

## Mises en page d'interface graphique {#gui-layouts}

L'ensemble actuel de profils d'affichage peut servir à créer des variantes de mise en page pour la disposition des nœuds de votre interface graphique. Pour ajouter une nouvelle mise en page à une scène d'interface graphique, faites un clic droit sur l'icône *Layouts* dans la vue *Outline* et sélectionnez <kbd>Add ▸ Layout ▸ ...</kbd> :

![Ajout d'une mise en page à la scène](images/gui-layouts/add_layout.png)

Lorsque vous modifiez une scène d'interface graphique, tous les nœuds sont modifiés dans une mise en page particulière. La mise en page actuellement sélectionnée est indiquée dans la liste déroulante des mises en page de la scène d'interface graphique, dans la barre d'outils. Si aucune mise en page n'est choisie, les nœuds sont modifiés dans la mise en page *Default*.

![Barre d'outils des mises en page](images/gui-layouts/toolbar.png)

![Modification en mode portrait](images/gui-layouts/portrait.png)

Chaque modification d'une propriété de nœud que vous effectuez lorsqu'une mise en page est sélectionnée _redéfinit_ la propriété par rapport à la mise en page *Default*. Les propriétés redéfinies sont indiquées en bleu. Les nœuds dont des propriétés sont redéfinies sont également indiqués en bleu. Vous pouvez cliquer sur le bouton de réinitialisation à côté de toute propriété redéfinie pour rétablir sa valeur d'origine.

![Modification en mode paysage](images/gui-layouts/landscape.png)

Une mise en page ne peut ni supprimer ni créer de nouveaux nœuds, elle peut seulement redéfinir des propriétés. Si vous devez retirer un nœud d'une mise en page, vous pouvez le déplacer hors de l'écran ou le supprimer par la logique d'un script. Vous devez également prêter attention à la mise en page actuellement sélectionnée. Si vous ajoutez une mise en page à votre projet, la nouvelle mise en page sera configurée d'après la mise en page actuellement sélectionnée. De même, le copier-coller de nœuds tient compte de la mise en page actuellement sélectionnée, lors de la copie *et* du collage.

## Sélection dynamique des profils {#dynamic-profile-selection}

Lorsque l'option Auto Layout Selection est activée, le moteur sélectionne automatiquement la mise en page la plus adaptée. La recherche dynamique de correspondance des mises en page attribue un score à chaque critère de profil d'affichage selon les règles suivantes :

1. Si aucun modèle d'appareil n'est défini, ou si le modèle d'appareil correspond, un score (S) est calculé pour le critère.

2. Le score (S) est calculé à partir de la surface de l'écran (A), de la surface définie par le critère (A_Q), du rapport largeur/hauteur de l'écran (R) et du rapport largeur/hauteur du critère (R_Q) :

<img src="https://latex.codecogs.com/svg.latex?\inline&space;S=\left|1&space;-&space;\frac{A}{A_Q}\right|&space;&plus;&space;\left|1&space;-&space;\frac{R}{R_Q}\right|" title="S=\left|1 - \frac{A}{A_Q}\right| + \left|1 - \frac{R}{R_Q}\right|" />

3. Le profil dont le critère a le score le plus faible est sélectionné, si l'orientation (paysage ou portrait) du critère correspond à celle de l'écran.

4. Si aucun profil comportant un critère de la même orientation n'est trouvé, le profil dont le critère obtient le meilleur score dans l'autre orientation est sélectionné.

5. Si aucun profil ne peut être sélectionné, le profil de repli *Default* est utilisé.

Puisque la mise en page *Default* sert de solution de repli à l'exécution lorsqu'aucune mise en page ne correspond mieux, si vous ajoutez une mise en page "Landscape", elle sera la plus adaptée à *toutes* les orientations tant que vous n'aurez pas également ajouté une mise en page "Portrait".

## Messages de changement de mise en page {#layout-change-messages}

Lorsque la mise en page change, un message `layout_changed` est envoyé au script du composant (component) d'interface graphique. Cela se produit lorsque le moteur change automatiquement de mise en page (Auto Layout Selection sur ON) ou lorsque votre script appelle `gui.set_layout()` et que la mise en page change effectivement. Le message contient l'identifiant haché de la mise en page, ce qui permet au script d'exécuter une logique en fonction de la mise en page sélectionnée :

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("layout_changed") and message.id == hash("My Landscape") then
    -- switching layout to landscape
  elseif message_id == hash("layout_changed") and message.id == hash("My Portrait") then
    -- switching layout to portrait
  end
end
```

En outre, le script de rendu actuel reçoit un message chaque fois que la fenêtre (vue du jeu) change, y compris lors des changements d'orientation.

```lua
function on_message(self, message_id, message)
  if message_id == hash("window_resized") then
    -- The window was resized. message.width and message.height contain the
    -- new dimensions of the window.
  end
end
```

Lorsque l'orientation change, le gestionnaire de mises en page de l'interface graphique redimensionne et repositionne automatiquement les nœuds de l'interface graphique selon les propriétés de votre mise en page et de vos nœuds. Le contenu du jeu est toutefois rendu dans une passe distincte (par défaut), avec une projection étirée pour remplir la fenêtre actuelle. Pour modifier ce comportement, fournissez votre propre script de rendu modifié ou utilisez une [bibliothèque](/assets/) de caméra.

## Sélection manuelle de la mise en page (Lua) {#manual-layout-selection-lua}

Lorsque l'option Auto Layout Selection est sur OFF pour la ressource Display Profiles utilisée, le moteur ne change pas automatiquement de mise en page. Utilisez les fonctions suivantes dans un script GUI pour gérer les mises en page manuellement :

### gui.set_layout(layout) {#guiset_layoutlayout}

- Accepte une chaîne de caractères ou un hachage (identifiant de mise en page).
- Renvoie un booléen : `true` si la mise en page existe dans la scène et a été appliquée ; `false` sinon.
- Si la mise en page existe dans Display Profiles, met à jour la résolution de la scène selon la largeur et la hauteur du profil.
- Émet `layout_changed` lorsque la mise en page change effectivement.

Exemple :

```lua
function init(self)
    -- Manually apply the "Portrait" layout
    local ok = gui.set_layout("Portrait")
    if not ok then
        print("Portrait layout not found in this scene")
    end
end
```

### gui.get_layouts() {#guiget_layouts}

- Renvoie une table qui associe à chaque hachage d'identifiant de mise en page un `vmath.vector3(width, height, 0)`.
- Pour la mise en page par défaut, renvoie la résolution actuelle de la scène.

Exemple :

```lua
local layouts = gui.get_layouts()
for id, size in pairs(layouts) do
    print(id, size.x, size.y)
end
```

Remarque : si une mise en page d'interface graphique existe dans la scène mais n'est pas présente dans Display Profiles, `gui.set_layout()` applique tout de même les propriétés de nœuds redéfinies pour cette mise en page, mais ne modifie pas la résolution de la scène.
