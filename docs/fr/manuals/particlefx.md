---
title: Effets de particules dans Defold
brief: Ce manuel explique le fonctionnement du composant d'effets de particules et comment le modifier pour créer des effets visuels de particules.
---

# Effets de particules {#particle-fx}

Les effets de particules servent à enrichir visuellement les jeux. Vous pouvez les utiliser pour créer des explosions, des éclaboussures de sang, des traînées, des phénomènes météorologiques ou tout autre effet.

![Éditeur d'effets de particules](images/particlefx/editor.png)

Les effets de particules se composent d'un certain nombre d'émetteurs et de modificateurs facultatifs :

Émetteur
: Un émetteur est une forme positionnée qui émet des particules uniformément réparties sur cette forme. L'émetteur possède des propriétés qui contrôlent la création des particules ainsi que l'image ou l'animation, la durée de vie, la couleur, la forme et la vitesse de chaque particule.

Modificateur
: Un modificateur agit sur la vitesse des particules créées pour les accélérer ou les ralentir dans une direction donnée, les déplacer radialement ou les faire tourbillonner autour d'un point. Les modificateurs peuvent agir sur les particules d'un seul émetteur ou sur un émetteur particulier.

## Création d'un effet {#creating-an-effect}

Sélectionnez <kbd>New... ▸ Particle FX</kbd> dans le menu contextuel du navigateur *Assets*. Nommez le nouveau fichier d'effet de particules. L'éditeur ouvre alors le fichier dans l'[éditeur de scène](/manuals/editor/#the-scene-editor).

Le panneau *Outline* affiche l'émetteur par défaut. Sélectionnez l'émetteur pour afficher ses propriétés dans le panneau *Properties* situé en dessous.

![Particules par défaut](images/particlefx/default.png)

Pour ajouter un nouvel émetteur à l'effet, faites un <kbd>clic droit</kbd> sur la racine du panneau *Outline* et sélectionnez <kbd>Add Emitter ▸ [type]</kbd> dans le menu contextuel. Notez que vous pouvez changer le type de l'émetteur dans ses propriétés.

Pour ajouter un nouveau modificateur, faites un <kbd>clic droit</kbd> sur l'emplacement du modificateur dans le panneau *Outline* (la racine de l'effet ou un émetteur particulier) et sélectionnez <kbd>Add Modifier</kbd>, puis le type de modificateur.

![Ajout d'un modificateur](images/particlefx/add_modifier.png)

![Sélection du modificateur à ajouter](images/particlefx/add_modifier_select.png)

Un modificateur placé à la racine de l'effet (sans être enfant d'un émetteur) agit sur toutes les particules de l'effet.

Un modificateur ajouté comme enfant d'un émetteur agit uniquement sur cet émetteur.

## Aperçu d'un effet {#previewing-an-effect}

* Sélectionnez <kbd>View ▸ Play</kbd> dans le menu pour prévisualiser l'effet. Vous devrez peut-être dézoomer la caméra pour bien voir l'effet.
* Sélectionnez à nouveau <kbd>View ▸ Play</kbd> pour mettre l'effet en pause.
* Sélectionnez <kbd>View ▸ Stop</kbd> pour arrêter l'effet. Si vous le relancez, il repart de son état initial.

Lorsque vous modifiez un émetteur ou un modificateur, le résultat est immédiatement visible dans l'éditeur, même si l'effet est en pause :

![Modification des particules](images/particlefx/rotate.gif)

## Propriétés des émetteurs {#emitter-properties}

Id
: Identifiant de l'émetteur (utilisé pour définir des constantes de rendu pour des émetteurs spécifiques).

Position/Rotation
: Transformation de l'émetteur par rapport au composant (component) ParticleFX.

Play Mode
: Contrôle la lecture de l'émetteur :
  - `Once` arrête l'émetteur une fois sa durée écoulée.
  - `Loop` redémarre l'émetteur une fois sa durée écoulée.

Size Mode
: Contrôle le dimensionnement des animations image par image (flipbook) :
  - `Auto` conserve la taille de l'image source pour chaque image de l'animation image par image.
  - `Manual` définit la taille des particules en fonction de la propriété de taille.

Emission Space
: Espace géométrique dans lequel les particules créées existeront :
  - `World` déplace les particules indépendamment de l'émetteur.
  - `Emitter` déplace les particules par rapport à l'émetteur.

Duration
: Nombre de secondes pendant lesquelles l'émetteur doit émettre des particules.

Start Delay
: Nombre de secondes que l'émetteur doit attendre avant d'émettre des particules.

Start Offset
: Nombre de secondes écoulées dans la simulation de particules au moment où l'émetteur doit démarrer, autrement dit la durée pendant laquelle l'émetteur doit simuler l'effet au préalable.

Image
: Fichier image (Tile source ou Atlas) à utiliser pour texturer et animer les particules.

Animation
: Animation du fichier *Image* à utiliser sur les particules.

Material
: Matériau à utiliser pour le rendu des particules.

Blend Mode
: Les modes de fusion disponibles sont `Alpha`, `Add` et `Multiply`.

Max Particle Count
: Nombre de particules issues de cet émetteur qui peuvent exister simultanément.

Emitter Type
: Forme de l'émetteur
  - `Circle` émet des particules depuis une position aléatoire à l'intérieur d'un cercle. Les particules sont dirigées vers l'extérieur depuis le centre. Le diamètre du cercle est défini par *Emitter Size X*.

  - `2D Cone` émet des particules depuis une position aléatoire à l'intérieur d'un cône plat (un triangle). Les particules sont dirigées vers l'extérieur par le haut du cône. *Emitter Size X* définit la largeur du haut et *Y* définit la hauteur.

  - `Box` émet des particules depuis une position aléatoire à l'intérieur d'une boîte. Les particules sont dirigées vers le haut le long de l'axe Y local de la boîte. *Emitter Size X*, *Y* et *Z* définissent respectivement la largeur, la hauteur et la profondeur. Pour un rectangle 2D, gardez la dimension Z à zéro.

  - `Sphere` émet des particules depuis une position aléatoire à l'intérieur d'une sphère. Les particules sont dirigées vers l'extérieur depuis le centre. Le diamètre de la sphère est défini par *Emitter Size X*.

  - `Cone` émet des particules depuis une position aléatoire à l'intérieur d'un cône 3D. Les particules sont dirigées vers l'extérieur à travers le disque supérieur du cône. *Emitter Size X* définit le diamètre du disque supérieur et *Y* définit la hauteur du cône.

  ![Types d'émetteurs](images/particlefx/emitter_types.png)

Particle Orientation
: Orientation des particules émises :
  - `Default` définit l'orientation sur l'orientation identité
  - `Initial Direction` conserve l'orientation initiale des particules émises.
  - `Movement Direction` ajuste l'orientation des particules en fonction de leur vitesse.

Inherit Velocity
: Facteur qui détermine la part de la vitesse de l'émetteur dont les particules doivent hériter. Cette valeur n'est disponible que lorsque *Space* est défini sur `World`. La vitesse de l'émetteur est estimée à chaque image.

Stretch With Velocity
: Cochez cette option pour mettre à l'échelle tout étirement des particules dans la direction du mouvement.

### Modes de fusion {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

## Propriétés d'émetteur animables par images clés {#keyable-emitter-properties}

Ces propriétés possèdent deux champs : une valeur et une dispersion. La dispersion est une variation appliquée aléatoirement à chaque particule créée. Par exemple, si la valeur est 50 et la dispersion 3, chaque particule créée recevra une valeur comprise entre 47 et 53 (50 +/- 3).

![Propriété](images/particlefx/property.png)

Lorsque vous activez le bouton en forme de clé, la valeur de la propriété est contrôlée par une courbe sur la durée de l'émetteur. Pour réinitialiser une propriété animée par images clés, désactivez le bouton en forme de clé.

![Propriété animée par images clés](images/particlefx/key.png)

Le *Curve Editor* (disponible parmi les onglets de la vue inférieure) sert à modifier la courbe. Les propriétés animées par images clés ne peuvent pas être modifiées dans la vue *Properties*, mais uniquement dans le *Curve Editor*. <kbd>Cliquez et faites glisser</kbd> les points et les tangentes pour modifier la forme de la courbe. <kbd>Double-cliquez</kbd> sur la courbe pour ajouter des points de contrôle. Pour supprimer un point de contrôle, faites un <kbd>double clic</kbd> dessus.

![Éditeur de courbes d'effets de particules](images/particlefx/curve_editor.png)

Pour ajuster automatiquement le zoom du Curve Editor afin d'afficher toutes les courbes, appuyez sur <kbd>F</kbd>.

Les propriétés suivantes peuvent être animées par images clés sur la durée de lecture de l'émetteur :

Spawn Rate
: Nombre de particules à émettre par seconde.

Emitter Size X/Y/Z
: Dimensions de la forme de l'émetteur, voir *Emitter Type* ci-dessus.

Particle Life Time
: Durée de vie de chaque particule créée, en secondes.

Initial Speed
: Vitesse initiale de chaque particule créée.

Initial Size
: Taille initiale de chaque particule créée. Si vous définissez *Size Mode* sur `Automatic` et utilisez une animation image par image comme source d'image, cette propriété est ignorée.

Initial Red/Green/Blue/Alpha
: Valeurs initiales des composantes de couleur de la teinte des particules.

Initial Rotation
: Valeurs initiales de rotation (en degrés) des particules.

Initial Stretch X/Y
: Valeurs initiales d'étirement (en unités) des particules.

Initial Angular Velocity
: Vitesse angulaire initiale (en degrés/seconde) de chaque particule créée.

Les propriétés suivantes peuvent être animées par images clés sur la durée de vie des particules :

Life Scale
: Valeur d'échelle au cours de la vie de chaque particule.

Life Red/Green/Blue/Alpha
: Valeur des composantes de couleur de la teinte au cours de la vie de chaque particule.

Life Rotation
: Valeur de rotation (en degrés) au cours de la vie de chaque particule.

Life Stretch X/Y
: Valeur d'étirement (en unités) au cours de la vie de chaque particule.

Life Angular Velocity
: Vitesse angulaire (en degrés/seconde) au cours de la vie de chaque particule.

## Modificateurs {#modifiers}

Quatre types de modificateurs sont disponibles pour agir sur la vitesse des particules :

`Acceleration`
: Accélération dans une direction générale.

`Drag`
: Réduit l'accélération des particules proportionnellement à leur vitesse.

`Radial`
: Attire les particules vers une position ou les repousse depuis cette position.

`Vortex`
: Agit sur les particules dans une direction circulaire ou en spirale autour de sa position.

  ![Modificateurs](images/particlefx/modifiers.png)

## Propriétés des modificateurs {#modifier-properties}

Position/Rotation
: Transformation du modificateur par rapport à son parent.

Magnitude
: Intensité de l'effet du modificateur sur les particules.

Max Distance
: Distance maximale jusqu'à laquelle ce modificateur peut agir sur les particules. Utilisée uniquement pour Radial et Vortex.

## Contrôle d'un effet de particules {#controlling-a-particle-effect}

Pour démarrer et arrêter un effet de particules depuis un script :

```lua
-- start the effect component "particles" in the current game object
particlefx.play("#particles")

-- stop the effect component "particles" in the current game object
particlefx.stop("#particles")
```

Pour démarrer et arrêter un effet de particules depuis un script GUI, consultez le [manuel des effets de particules GUI](/manuals/gui-particlefx#controlling-the-effect) pour plus d'informations.

::: sidenote
Un effet de particules continue à émettre des particules même si l'objet de jeu (game object) auquel appartenait le composant d'effet de particules est supprimé.
:::
Consultez la [documentation de référence des effets de particules](/ref/particlefx) pour plus d'informations.

## Constantes de matériau {#material-constants}

Le matériau par défaut des effets de particules possède les constantes suivantes, qui peuvent être modifiées avec `particlefx.set_constant()` et réinitialisées avec `particlefx.reset_constant()` (consultez le [manuel des matériaux pour plus de détails](/manuals/material/#vertex-and-fragment-constants)) :

`tint`
: Teinte de l'effet de particules (`vector4`). Le vector4 représente la teinte, avec x, y, z et w correspondant respectivement au rouge, au vert, au bleu et à l'alpha. Consultez la [référence de l'API pour un exemple](/ref/particlefx/#particlefx.set_constant:url-constant-value).


## Configuration du projet {#project-configuration}

Le fichier *game.project* contient quelques [paramètres du projet](/manuals/project-settings#particle-fx) liés aux particules.
