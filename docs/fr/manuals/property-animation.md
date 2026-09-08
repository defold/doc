---
title: Manuel des animations de propriétés dans Defold
brief: Ce manuel décrit comment utiliser les animations de propriétés dans Defold.
---

# Animation de propriété {#property-animation}

Toutes les propriétés numériques (`numbers`, `vector3`, `vector4` et quaternions) et les constantes de shader peuvent être animées avec le système d'animation intégré, à l'aide de la fonction `go.animate()`. Le moteur calcule automatiquement les valeurs intermédiaires des propriétés selon les modes de lecture et les fonctions d'interpolation indiqués. Vous pouvez également spécifier des fonctions d'interpolation personnalisées.

  ![Animation de propriété](images/animation/property_animation.png)
  ![Rebond en boucle](images/animation/bounce.gif)

## Animation de propriété {#property-animation}

Pour animer une propriété d'un objet de jeu (game object) ou d'un composant (component), utilisez la fonction `go.animate()`. Pour les propriétés des nœuds d'interface graphique, la fonction correspondante est `gui.animate()`.

```lua
-- Set the position property y component to 200
go.set(".", "position.y", 200)
-- Then animate it
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

Pour arrêter toutes les animations d'une propriété donnée, appelez `go.cancel_animations()`, ou, pour les nœuds d'interface graphique, `gui.cancel_animations()` :

```lua
-- Stop euler z rotation animation on the current game object
go.cancel_animations(".", "euler.z")
```

Si vous annulez l'animation d'une propriété composite, comme `position`, toutes les animations de ses sous-composantes (`position.x`, `position.y` et `position.z`) seront également annulées.

Le [manuel des propriétés](/manuals/properties) présente toutes les propriétés disponibles pour les objets de jeu, les composants et les nœuds d'interface graphique.

## Animation des propriétés des nœuds d'interface graphique {#gui-node-property-animation}

Presque toutes les propriétés des nœuds d'interface graphique peuvent être animées. Vous pouvez, par exemple, rendre un nœud invisible en réglant sa propriété `color` sur une transparence totale, puis le faire apparaître progressivement en animant sa couleur vers le blanc (c'est-à-dire sans teinte).

```lua
local node = gui.get_node("button")
local color = gui.get_color(node)
-- Animate the color to white
gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_INOUTQUAD, 0.5)
-- Animate the outline red color component
gui.animate(node, "outline.x", 1, gui.EASING_INOUTQUAD, 0.5)
-- And move to x position 100
gui.animate(node, hash("position.x"), 100, gui.EASING_INOUTQUAD, 0.5)
```

## Fonctions de rappel de fin {#completion-callbacks}

Les fonctions d'animation de propriétés `go.animate()` et `gui.animate()` acceptent une fonction de rappel Lua (callback) facultative comme dernier argument. Cette fonction est appelée lorsque l'animation est arrivée à son terme. Elle n'est jamais appelée pour les animations en boucle, ni lorsqu'une animation est annulée manuellement au moyen de `go.cancel_animations()` ou de `gui.cancel_animations()`. La fonction de rappel peut servir à déclencher des événements à la fin d'une animation ou à enchaîner plusieurs animations.

## Fonctions d'interpolation {#easing}

La fonction d'interpolation définit la manière dont la valeur animée évolue au fil du temps. Les images ci-dessous décrivent les fonctions appliquées au cours du temps pour réaliser cette interpolation.

Les valeurs d'interpolation suivantes sont valides pour `go.animate()` :

|---|---|
| `go.EASING_LINEAR` | |
| `go.EASING_INBACK` | `go.EASING_OUTBACK` |
| `go.EASING_INOUTBACK` | `go.EASING_OUTINBACK` |
| `go.EASING_INBOUNCE` | `go.EASING_OUTBOUNCE` |
| `go.EASING_INOUTBOUNCE` | `go.EASING_OUTINBOUNCE` |
| `go.EASING_INELASTIC` | `go.EASING_OUTELASTIC` |
| `go.EASING_INOUTELASTIC` | `go.EASING_OUTINELASTIC` |
| `go.EASING_INSINE` | `go.EASING_OUTSINE` |
| `go.EASING_INOUTSINE` | `go.EASING_OUTINSINE` |
| `go.EASING_INEXPO` | `go.EASING_OUTEXPO` |
| `go.EASING_INOUTEXPO` | `go.EASING_OUTINEXPO` |
| `go.EASING_INCIRC` | `go.EASING_OUTCIRC` |
| `go.EASING_INOUTCIRC` | `go.EASING_OUTINCIRC` |
| `go.EASING_INQUAD` | `go.EASING_OUTQUAD` |
| `go.EASING_INOUTQUAD` | `go.EASING_OUTINQUAD` |
| `go.EASING_INCUBIC` | `go.EASING_OUTCUBIC` |
| `go.EASING_INOUTCUBIC` | `go.EASING_OUTINCUBIC` |
| `go.EASING_INQUART` | `go.EASING_OUTQUART` |
| `go.EASING_INOUTQUART` | `go.EASING_OUTINQUART` |
| `go.EASING_INQUINT` | `go.EASING_OUTQUINT` |
| `go.EASING_INOUTQUINT` | `go.EASING_OUTINQUINT` |

Les valeurs d'interpolation suivantes sont valides pour `gui.animate()` :

|---|---|
| `gui.EASING_LINEAR` | |
| `gui.EASING_INBACK` | `gui.EASING_OUTBACK` |
| `gui.EASING_INOUTBACK` | `gui.EASING_OUTINBACK` |
| `gui.EASING_INBOUNCE` | `gui.EASING_OUTBOUNCE` |
| `gui.EASING_INOUTBOUNCE` | `gui.EASING_OUTINBOUNCE` |
| `gui.EASING_INELASTIC` | `gui.EASING_OUTELASTIC` |
| `gui.EASING_INOUTELASTIC` | `gui.EASING_OUTINELASTIC` |
| `gui.EASING_INSINE` | `gui.EASING_OUTSINE` |
| `gui.EASING_INOUTSINE` | `gui.EASING_OUTINSINE` |
| `gui.EASING_INEXPO` | `gui.EASING_OUTEXPO` |
| `gui.EASING_INOUTEXPO` | `gui.EASING_OUTINEXPO` |
| `gui.EASING_INCIRC` | `gui.EASING_OUTCIRC` |
| `gui.EASING_INOUTCIRC` | `gui.EASING_OUTINCIRC` |
| `gui.EASING_INQUAD` | `gui.EASING_OUTQUAD` |
| `gui.EASING_INOUTQUAD` | `gui.EASING_OUTINQUAD` |
| `gui.EASING_INCUBIC` | `gui.EASING_OUTCUBIC` |
| `gui.EASING_INOUTCUBIC` | `gui.EASING_OUTINCUBIC` |
| `gui.EASING_INQUART` | `gui.EASING_OUTQUART` |
| `gui.EASING_INOUTQUART` | `gui.EASING_OUTINQUART` |
| `gui.EASING_INQUINT` | `gui.EASING_OUTQUINT` |
| `gui.EASING_INOUTQUINT` | `gui.EASING_OUTINQUINT` |

![Interpolation linéaire](images/properties/easing_linear.png)
![Dépassement en entrée](images/properties/easing_inback.png)
![Dépassement en sortie](images/properties/easing_outback.png)
![Dépassement en entrée puis en sortie](images/properties/easing_inoutback.png)
![Dépassement en sortie puis en entrée](images/properties/easing_outinback.png)
![Rebond en entrée](images/properties/easing_inbounce.png)
![Rebond en sortie](images/properties/easing_outbounce.png)
![Rebond en entrée puis en sortie](images/properties/easing_inoutbounce.png)
![Rebond en sortie puis en entrée](images/properties/easing_outinbounce.png)
![Élasticité en entrée](images/properties/easing_inelastic.png)
![Élasticité en sortie](images/properties/easing_outelastic.png)
![Élasticité en entrée puis en sortie](images/properties/easing_inoutelastic.png)
![Élasticité en sortie puis en entrée](images/properties/easing_outinelastic.png)
![Interpolation sinusoïdale en entrée](images/properties/easing_insine.png)
![Interpolation sinusoïdale en sortie](images/properties/easing_outsine.png)
![Interpolation sinusoïdale en entrée puis en sortie](images/properties/easing_inoutsine.png)
![Interpolation sinusoïdale en sortie puis en entrée](images/properties/easing_outinsine.png)
![Interpolation exponentielle en entrée](images/properties/easing_inexpo.png)
![Interpolation exponentielle en sortie](images/properties/easing_outexpo.png)
![Interpolation exponentielle en entrée puis en sortie](images/properties/easing_inoutexpo.png)
![Interpolation exponentielle en sortie puis en entrée](images/properties/easing_outinexpo.png)
![Interpolation circulaire en entrée](images/properties/easing_incirc.png)
![Interpolation circulaire en sortie](images/properties/easing_outcirc.png)
![Interpolation circulaire en entrée puis en sortie](images/properties/easing_inoutcirc.png)
![Interpolation circulaire en sortie puis en entrée](images/properties/easing_outincirc.png)
![Interpolation quadratique en entrée](images/properties/easing_inquad.png)
![Interpolation quadratique en sortie](images/properties/easing_outquad.png)
![Interpolation quadratique en entrée puis en sortie](images/properties/easing_inoutquad.png)
![Interpolation quadratique en sortie puis en entrée](images/properties/easing_outinquad.png)
![Interpolation cubique en entrée](images/properties/easing_incubic.png)
![Interpolation cubique en sortie](images/properties/easing_outcubic.png)
![Interpolation cubique en entrée puis en sortie](images/properties/easing_inoutcubic.png)
![Interpolation cubique en sortie puis en entrée](images/properties/easing_outincubic.png)
![Interpolation quartique en entrée](images/properties/easing_inquart.png)
![Interpolation quartique en sortie](images/properties/easing_outquart.png)
![Interpolation quartique en entrée puis en sortie](images/properties/easing_inoutquart.png)
![Interpolation quartique en sortie puis en entrée](images/properties/easing_outinquart.png)
![Interpolation quintique en entrée](images/properties/easing_inquint.png)
![Interpolation quintique en sortie](images/properties/easing_outquint.png)
![Interpolation quintique en entrée puis en sortie](images/properties/easing_inoutquint.png)
![Interpolation quintique en sortie puis en entrée](images/properties/easing_outinquint.png)

## Fonctions d'interpolation personnalisées {#custom-easing}

Vous pouvez créer des courbes d'interpolation personnalisées en définissant un `vector` contenant un ensemble de valeurs, puis en fournissant ce vecteur à la place de l'une des constantes d'interpolation prédéfinies ci-dessus. Les valeurs du vecteur décrivent une courbe allant de la valeur de départ (`0`) à la valeur cible (`1`). Le moteur d'exécution échantillonne les valeurs du vecteur et effectue une interpolation linéaire pour calculer les valeurs entre les points définis dans le vecteur.

Par exemple, le vecteur :

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5, 1 }
local my_easing = vmath.vector(values)
```

produit la courbe suivante :

![Courbe personnalisée](images/animation/custom_curve.png)

Dans l'exemple suivant, la position y d'un objet de jeu passe brusquement de la position actuelle à 200, et inversement, selon une courbe en créneaux :

```lua
local values = { 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1 }
local square_easing = vmath.vector(values)
go.animate("go", "position.y", go.PLAYBACK_LOOP_PINGPONG, 200, square_easing, 2.0)
```

![Courbe en créneaux](images/animation/square_curve.png)
