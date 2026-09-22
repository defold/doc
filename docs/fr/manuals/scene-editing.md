---
title: L'éditeur de scène Defold
brief: L'éditeur de scène permet de modifier les collections, les objets de jeu, les interfaces graphiques, les effets de particules et d'autres ressources visuelles. Ce manuel explique la sélection, les outils et la navigation dans la vue de scène en 2D et en 3D, y compris le mode caméra libre et les paramètres de la caméra.
---

# L'éditeur de scène Defold {#the-defold-scene-editor}

L'**éditeur de scène** est l'éditeur visuel utilisé pour créer et modifier des scènes, telles que les collections, les objets de jeu (game objects) et d'autres ressources visuelles.

La vue initiale de la caméra dépend de la ressource. Les ressources 3D telles que les modèles et les scènes glTF utilisent par défaut une projection **en perspective**, tandis que les ressources 2D telles que les sprites, les tilemaps et les scènes GUI utilisent une projection **orthographique**. Vous pouvez modifier l'orientation de la caméra, la projection et la grille depuis la barre d'outils de la scène.

## Ouvrir l'éditeur de scène {#opening-the-scene-editor}

Ouvrez l'éditeur de scène en double-cliquant sur une ressource visuelle dans le panneau *Assets*, par exemple :

- **Structure de scène** — collections (`.collection`), objets de jeu (`.go`)
- **Ressources 2D** — atlas (`.atlas`), tilemaps (`.tilemap`), sprites (`.sprite`), sources de tuiles (`.tilesource`)
- **Ressources 3D** — modèles (`.model`, `.glb`, `.gltf`)
- **Interface utilisateur** — scènes GUI (`.gui`)
- **Effets** — effets de particules (`.particlefx`)
- Et d'autres ressources

## Mémorisation des vues de scène {#remembered-scene-views}

L'éditeur mémorise l'état de la caméra de chaque ressource de scène lorsque son onglet est fermé ou que vous quittez l'éditeur. Rouvrir la même ressource restaure sa vue ; différentes collections ou différents modèles peuvent donc conserver des positions, orientations et projections de caméra distinctes.

Les filtres de visibilité sont également mémorisés pour chaque scène. Masquer les modèles ou les guides de composants dans une scène n'impose pas les mêmes filtres dans une autre. Ces paramètres concernent l'affichage dans l'éditeur et ne changent ni la caméra du jeu ni la visibilité à l'exécution.

En l'absence d'état de caméra enregistré, les ressources de modèle, de maillage et glTF s'ouvrent en perspective. Les objets de collision choisissent leur vue d'après le paramètre de physique 2D/3D du projet ; les collections et les objets de jeu choisissent une vue initiale d'après la géométrie de leur scène.

## Navigation dans la vue de scène (commandes de caméra) {#scene-view-navigation-camera-controls}

La caméra de l'éditeur de scène se commande à la souris et au clavier. Les commandes disponibles dépendent du mode utilisé : navigation standard ou **mode caméra libre**.

### Navigation standard (tous les éditeurs visuels) {#standard-navigation-all-visual-editors}

Ces commandes sont disponibles dans les éditeurs visuels :

- **Déplacement panoramique**
  - <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Zoom**
  - <kbd>Mouse Wheel</kbd>, ou
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Rotation/orbite (3D) autour de la sélection**
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Left Mouse Button</kbd>

Vous pouvez aussi utiliser **Frame Selection** (<kbd>F</kbd>) pour centrer la caméra sur la sélection actuelle.

## Orientation de la scène en 2D et en 3D {#2d-and-3d-scene-orientation}

La vue de scène peut être utilisée dans les flux de travail en 2D comme en 3D :

- En **2D**, vous travaillez généralement dans une vue orthographique avec une grille orientée pour la 2D.
- En **3D**, vous effectuez généralement les opérations suivantes :
  - Réaligner la vue selon une orientation 3D,
  - Utiliser une caméra **en perspective**,
  - Choisir un plan de grille approprié (souvent **Y** pour le « sol »).

Vous pouvez accéder à ces fonctions depuis la barre d'outils et le menu **View**.

![Éditeur de scène en 3D](images/editor/3d_scene.png)

## Présentation de la barre d'outils {#toolbar-overview}

En haut à droite de la vue de scène, une barre d'outils rassemble les outils et les options d'affichage courants (de gauche à droite) :

- **Move tool** (<kbd>W</kbd>)
- **Rotate tool** (<kbd>E</kbd>)
- **Scale tool** (<kbd>R</kbd>)
- **Grid Settings** (`▦`)
- **Align/Realign Camera 2D/3D** (`2D`) — bascule entre les orientations 2D et 3D (raccourci <kbd>.</kbd>)
- **Camera Perspective/Orthographic**
- **Visibility Filters** (`👁`)

![Barre d'outils](images/editor/toolbar.png)

## Sélectionner et manipuler des objets {#manipulating-objects}

### Sélectionner des objets {#selecting-objects}

<kbd>Cliquez avec le bouton gauche de la souris</kbd> sur les objets dans la fenêtre principale pour les sélectionner. Le rectangle (ou parallélépipède rectangle) entourant l'objet dans la vue de l'éditeur apparaît en cyan pour indiquer l'élément sélectionné. L'objet sélectionné est également mis en évidence dans la vue `Outline`, comme sur l'image ci-dessus.

  Vous pouvez aussi sélectionner des objets de ces façons :

- <kbd>Cliquez avec le bouton gauche de la souris</kbd> et <kbd>faites glisser</kbd> pour sélectionner tous les objets à l'intérieur de la zone de sélection.
- <kbd>Cliquez avec le bouton gauche de la souris</kbd> sur les objets dans `Outline` ; en maintenant <kbd>⇧ Shift</kbd>, vous pouvez étendre la sélection, ou en maintenant <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd>, vous pouvez sélectionner ou désélectionner les objets sur lesquels vous cliquez.

#### Outil de déplacement {#move-tool}

![Outil de déplacement](images/editor/icon_move.png){.left}

Pour déplacer des objets, utilisez l'outil *Move Tool*. Vous le trouverez dans la barre d'outils en haut à droite de l'éditeur de scène, ou en appuyant sur la touche <kbd>W</kbd>.

![Déplacer un objet](images/editor/move.png){.inline}![Déplacer un objet en 3D](images/editor/move_3d.png){.inline}

Le gizmo change et affiche un ensemble de poignées de manipulation — carrés et flèches (la poignée sélectionnée devient orange) — que vous pouvez <kbd>faire glisser</kbd> pour déplacer l'objet :

- une poignée carrée cyan au centre pour déplacer l'objet uniquement dans l'espace de l'écran,
- trois flèches rouge, verte et bleue le long de chaque axe pour déplacer l'objet uniquement selon l'axe X, Y ou Z correspondant.
- trois poignées carrées rouge, verte et bleue (avec un contour et un remplissage transparent) pour déplacer l'objet uniquement dans le plan correspondant, par exemple X-Y (bleu) et (visibles si vous faites pivoter la caméra en 3D) les plans X-Z (vert) et Y-Z (rouge).

#### Outil de rotation {#rotate-tool}

![Outil de rotation](images/editor/icon_rotate.png){.left}

Pour faire pivoter des objets, utilisez l'outil *Rotate Tool* en le sélectionnant dans la barre d'outils, ou en appuyant sur la touche <kbd>E</kbd>.

![Faire pivoter un objet](images/editor/rotate.png){.inline}![Faire pivoter un objet en 3D](images/editor/rotate_3d.png){.inline}

Cet outil comprend quatre poignées de manipulation circulaires (la poignée sélectionnée devient orange) que vous pouvez <kbd>faire glisser</kbd> pour faire pivoter l'objet :

- une poignée cyan (le plus grand cercle, à l'extérieur) qui fait pivoter l'objet dans l'espace de l'écran
- trois poignées circulaires plus petites, rouge, verte et bleue, qui permettent une rotation autour de chacun des axes X, Y et Z séparément. Dans une vue orthographique 2D, deux d'entre elles sont perpendiculaires aux axes X et Y, de sorte que les cercles n'apparaissent que sous la forme de deux lignes traversant l'objet.

#### Outil de mise à l'échelle {#scale-tool}

![Outil de mise à l'échelle](images/editor/icon_scale.png){.left}

Pour mettre des objets à l'échelle, utilisez l'outil *Scale Tool* en le sélectionnant dans la barre d'outils, ou en appuyant sur la touche <kbd>R</kbd>.

![Mettre un objet à l'échelle](images/editor/scale.png){.inline}![Mettre un objet à l'échelle en 3D](images/editor/scale_3d.png){.inline}

Cet outil comprend un ensemble de poignées de manipulation carrées ou cubiques (la poignée sélectionnée devient orange) que vous pouvez <kbd>faire glisser</kbd> pour mettre l'objet à l'échelle :

- un cube cyan au centre met l'objet à l'échelle uniformément sur tous les axes (y compris Z).
- trois poignées cubiques rouge, bleue et verte mettent l'objet à l'échelle selon chacun des axes X, Y et Z séparément.
- trois poignées carrées rouge, verte et bleue (avec un contour et un remplissage transparent) mettent l'objet à l'échelle dans les plans X-Y, X-Z ou Y-Z séparément.

### Filtres de visibilité {#visibility-filters}

Cliquez sur l'**icône en forme d'œil** (`👁`) dans la barre d'outils pour afficher ou masquer différents types de composants (components), ainsi que les boîtes englobantes et les lignes de repère (`Component Guides` ou le raccourci <kbd>Ctrl</kbd> + <kbd>H</kbd> (Win/Linux) ou <kbd>^ Ctrl</kbd> + <kbd>⌘ Cmd</kbd> + <kbd>H</kbd>(Mac)).

![Filtres de visibilité](images/editor/visibilityfilters.png)

## Paramètres de la grille {#grid-settings}

Vous pouvez personnaliser la grille pour l'adapter à votre flux de travail (particulièrement utile en 3D). Cliquez sur le bouton **Grid Settings** (`▦`) pour ouvrir la fenêtre contextuelle des paramètres de la grille.

L'éditeur conserve des paramètres de grille distincts pour les vues 2D et 3D. Définissez la taille, le plan et l'apparence lorsque le mode voulu est actif ; changer de mode restaure les paramètres de grille de ce mode. **Reset to Defaults** réinitialise les paramètres du mode actif.

![Paramètres de la grille](images/editor/grid_popup.png)

Les paramètres comprennent :

- **Grid size (X/Y/Z)**
  Définit l'espacement entre les lignes de la grille selon chaque axe. Utilisez de petites valeurs pour placer précisément de petits objets, ou de grandes valeurs pour une vue d'ensemble plus large.
- **Active plane (X/Y/Z)**
  Sélectionne le plan sur lequel la grille est tracée. Dans les flux de travail en 2D, il s'agit généralement de **Z** (le plan X-Y par défaut). Dans les flux de travail en 3D, **Y** est couramment utilisé pour représenter un plan de sol ou de plancher.
- **Grid color**
  Définit la couleur des lignes de la grille. Utile pour obtenir un contraste adapté aux différents arrière-plans de scène.
- **Grid opacity**
  Contrôle la transparence des lignes de la grille. Des valeurs plus faibles rendent la grille plus discrète tout en conservant un repère.
- Un bouton **Reset to Defaults**
  Rétablit les valeurs d'origine de tous les paramètres de la grille.

## Type de caméra : perspective ou orthographique {#camera-type-perspective-vs-orthographic}

L'éditeur de scène prend en charge les deux types :

- Caméra **Orthographic** (courante dans les flux de travail en 2D)
- Caméra **Perspective** (courante dans les flux de travail en 3D)

Utilisez le bouton de bascule de la caméra dans la barre d'outils pour passer de l'un à l'autre. Dans les scènes 3D, la navigation en perspective semble généralement plus naturelle.

## Mode caméra libre {#free-camera-mode}

Pour naviguer rapidement en 3D, l'éditeur de scène propose un **mode caméra libre**, une caméra à la première personne, de type « FPS ».

### Activer le mode caméra libre {#activating-free-camera-mode}

- Maintenez <kbd>Right Mouse Button</kbd> enfoncé — le mode caméra libre est actif tant que le bouton reste enfoncé
- <kbd>Shift</kbd> + <kbd>`</kbd> (accent grave) — active le mode caméra libre, qui reste actif après le relâchement des touches

::: sidenote
Sur certaines dispositions de clavier (par exemple suédoises), la touche d'accent grave est une touche morte et peut ne pas déclencher le raccourci comme prévu. Vous
pouvez réattribuer ce raccourci dans `File ▸ Preferences ▸ Keys` et saisir un raccourci pour `Scene -> Free Camera -> Activate`
:::

Lorsque le mode caméra libre est actif, une ligne souligne les bords de la vue de scène.

### Quitter le mode caméra libre {#exiting-free-camera-mode}

- Relâchez <kbd>Right Mouse Button</kbd> (si le mode a été activé en maintenant le bouton enfoncé), ou
- Appuyez sur <kbd>Left Mouse Button</kbd> ou sur <kbd>Right Mouse Button</kbd> (puis relâchez-le), ou appuyez sur <kbd>Esc</kbd> si le mode caméra libre a été activé par bascule.

### Regarder autour de soi (orientation à la souris) {#looking-around-mouse-look}

Lorsque le mode caméra libre est actif, ces commandes contrôlent le mouvement de la caméra (au lieu des outils de l'éditeur) :

- Déplacez la souris pour contrôler le **lacet** (gauche/droite) et le **tangage** (haut/bas)
- Le tangage est limité pour éviter de retourner la caméra

Vous pouvez aussi inverser l'axe Y si vous le souhaitez (voir les **paramètres de la caméra libre** ci-dessous).

### Se déplacer {#moving}

Lorsque le mode caméra libre est actif :

- <kbd>W</kbd> — avancer
- <kbd>S</kbd> — reculer
- <kbd>A</kbd> — aller à gauche
- <kbd>D</kbd> — aller à droite
- <kbd>E</kbd> — monter
- <kbd>Q</kbd> — descendre

::: sidenote
Toutes les touches de déplacement peuvent être réattribuées dans `File ▸ Preferences ▸ Keys`. Recherchez ensuite `Scene -> Free Camera`
:::

Modificateurs de vitesse :

- Maintenez <kbd>Shift</kbd> enfoncé — déplacement plus rapide
- Maintenez <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> enfoncé — déplacement plus lent et plus précis

### Mode marche (facultatif) {#walking-mode-optional}

Le mode caméra libre prend en charge le **mode marche**.

Lorsqu'il est activé :
- Le déplacement vertical est limité pour se rapprocher d'une marche à la première personne sur un plan de sol.
- Cela est utile lorsque vous explorez un niveau et souhaitez un déplacement cohérent « au sol ».

## Fenêtre contextuelle des paramètres de la caméra {#camera-settings-popup}

Le bouton de caméra en perspective de la barre d'outils possède une fenêtre contextuelle de paramètres pour les préférences relatives à la caméra.

![Paramètres de la caméra en perspective](images/editor/camera_popup.png)

La fenêtre contextuelle contient :

- **Move Speed**
  Règle la vitesse de déplacement de la caméra libre.

- **Look Sensitivity**
  Règle la vitesse de rotation de la caméra en réponse aux mouvements de la souris.

- **Invert Y**
  Inverse l'orientation verticale à la souris.

- **Walking Mode**
  Limite les déplacements pour une navigation semblable à une marche au sol.

- **Reset to Defaults**
  Rétablit les paramètres par défaut de la caméra.
