---
title: Propriétés dans Defold
brief: Ce manuel explique les types de propriétés disponibles dans Defold et comment les utiliser et les animer.
---

# Propriétés {#properties}

Defold expose des propriétés pour les objets de jeu (game objects), les composants (components) et les nœuds d'interface graphique, que vous pouvez lire, définir et animer. Les types de propriétés suivants sont disponibles :

* Transformations des objets de jeu définies par le système (position, rotation et échelle) et propriétés propres aux composants (par exemple, la taille en pixels d'un sprite ou la masse d'un objet de collision)
* Propriétés des composants script définies par l'utilisateur dans des scripts Lua (consultez la [documentation des propriétés de script](/manuals/script-properties) pour plus de détails)
* Propriétés des nœuds d'interface graphique
* Constantes de shader définies dans les shaders et les fichiers de matériau (consultez la [documentation des matériaux](/manuals/material) pour plus de détails)

Les propriétés numériques affichent une poignée de déplacement lorsque vous survolez leur champ de saisie. Vous pouvez augmenter ou diminuer leur valeur en faisant glisser la poignée respectivement vers la droite ou la gauche, ou vers le haut ou le bas.

Selon l'emplacement d'une propriété, vous y accédez au moyen d'une fonction générique ou d'une fonction propre à cette propriété. De nombreuses propriétés peuvent être animées automatiquement. Il est vivement recommandé d'animer les propriétés à l'aide du système intégré plutôt que de les manipuler vous-même (dans une fonction `update()`), aussi bien pour les performances que pour la simplicité d'utilisation.

Les propriétés composites de type `vector3`, `vector4` ou `quaternion` exposent également leurs sous-composantes (`x`, `y`, `z` et `w`). Vous pouvez accéder aux composantes individuellement en ajoutant au nom un point (`.`) suivi du nom de la composante. Par exemple, pour définir la composante x de la position d'un objet de jeu :

```lua
-- Set the x position of "game_object" to 10.
go.set("game_object", "position.x", 10)
```

Les fonctions `go.get()`, `go.set()` et `go.animate()` prennent une référence comme premier paramètre et un identifiant de propriété comme deuxième paramètre. La référence identifie l'objet de jeu ou le composant et peut être une chaîne de caractères, une valeur hachée ou une URL. Les URL sont expliquées en détail dans le [manuel d'adressage](/manuals/addressing). L'identifiant de propriété est une chaîne de caractères ou une valeur hachée qui désigne la propriété :

```lua
-- Set the x-scale of the sprite component
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

Pour les nœuds d'interface graphique, le nœud est fourni comme premier paramètre soit à une fonction propre à une propriété, soit aux fonctions génériques `gui.get()` et `gui.set()` :

```lua
-- Get the color of the button
local node = gui.get_node("button")
local color = gui.get_color(node)
local same_color = gui.get(node, "color")
gui.set(node, "color.x", 1)
```

## Propriétés des objets de jeu et des composants {#game-object-and-component-properties}

Tous les objets de jeu et certains types de composants possèdent des propriétés que vous pouvez lire et manipuler à l'exécution. Lisez ces valeurs avec [`go.get()`](/ref/go#go.get) et modifiez-les avec [`go.set()`](/ref/go#go.set). Selon le type de valeur de la propriété, vous pouvez animer les valeurs avec [`go.animate()`](/ref/go#go.animate). Un petit nombre de propriétés sont en lecture seule.

`get`{.mark}
: Peut être lue avec [`go.get()`](/ref/go#go.get).

`get+set`{.mark}
: Peut être lue avec [`go.get()`](/ref/go#go.get) et modifiée avec [`go.set()`](/ref/go#go.set). Les valeurs numériques peuvent être animées avec [`go.animate()`](/ref/go#go.animate).

*Propriétés des objets de jeu*

| propriété   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | La position locale de l'objet de jeu. | `vector3`      | `get+set`{.mark} |
| *rotation* | La rotation locale de l'objet de jeu, exprimée sous forme de `quaternion`.  | `quaternion` | `get+set`{.mark} |
| *euler*    | La rotation locale de l'objet de jeu, en angles d'Euler. | `vector3` | `get+set`{.mark} |
| *scale*    | L'échelle locale non uniforme de l'objet de jeu, exprimée sous forme de vecteur dont chaque composante contient un multiplicateur sur chaque axe. Pour doubler la taille en X et Y sans modifier Z, utilisez `vmath.vector3(2.0, 2.0, 1.0)`. | `vector3` | `get+set`{.mark} |
| *scale.xy*    | L'échelle locale non uniforme de l'objet de jeu sur les axes X et Y. Utilisez cette propriété ou `go.set_scale_xy()` lorsque vous ne souhaitez pas modifier l'échelle en Z. | `vector3` | `get+set`{.mark} |

::: sidenote
Il existe également des fonctions spécifiques pour manipuler la transformation d'un objet de jeu : `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`,  `go.get_scale()`, `go.set_scale()` et `go.set_scale_xy()`.
:::

*Propriétés des composants sprite*

| propriété   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | La taille du sprite avant mise à l'échelle, telle qu'elle est définie dans l'atlas source. | `vector3` | `get`{.mark} |
| *image* | Le hachage du chemin de la texture du sprite. | `hash` | `get`{.mark}|
| *scale* | L'échelle non uniforme du sprite. | `vector3` | `get+set`{.mark}|
| *scale.xy* | L'échelle non uniforme du sprite sur les axes X et Y. | `vector3` | `get+set`{.mark}|
| *material* | Le matériau utilisé par le sprite. | `hash` | `get+set`{.mark}|
| *cursor* | La position (entre 0 et 1) du curseur de lecture. | `number` | `get+set`{.mark}|
| *playback_rate* | La fréquence d'images de l'animation par images successives (flipbook). | `number` | `get+set`{.mark}|

*Propriétés des composants objet de collision*

| propriété   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | La masse de l'objet de collision. | `number` | `get`{.mark} |
| *linear_velocity* | La vitesse linéaire actuelle de l'objet de collision. | `vector3` | `get`{.mark} |
| *angular_velocity* | La vitesse angulaire actuelle de l'objet de collision. | `vector3` | `get`{.mark} |
| *linear_damping* | L'amortissement linéaire de l'objet de collision. | `vector3` | `get+set`{.mark} |
| *angular_damping* | L'amortissement angulaire de l'objet de collision. | `vector3` | `get+set`{.mark} |

*Propriétés des composants modèle (3D)*

| propriété   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | L'animation actuelle.                | `hash`          | `get`{.mark}     |
| *texture0*--*texture15* | Les hachages des chemins des textures du modèle. | `hash` | `get+set`{.mark}|
| *cursor*  | La position (entre 0 et 1) du curseur de lecture. | `number`   | `get+set`{.mark} |
| *playback_rate* | La vitesse de lecture de l'animation. Un multiplicateur de la vitesse de lecture de l'animation. | `number` | `get+set`{.mark} |
| *material* | Le matériau utilisé par le modèle. | `hash` | `get+set`{.mark}|

*Propriétés des composants label*

| propriété   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *text* | Le contenu textuel du label. Disponible depuis Defold 1.13.2. | `string` | `get+set`{.mark} |
| *scale* | L'échelle du label. | `vector3` | `get+set`{.mark} |
| *scale.xy* | L'échelle du label sur les axes X et Y. | `vector3` | `get+set`{.mark}|
| *color*     | La couleur du label. | `vector4` | `get+set`{.mark} |
| *outline* | La couleur du contour du label. | `vector4` | `get+set`{.mark} |
| *shadow* | La couleur de l'ombre du label. | `vector4` | `get+set`{.mark} |
| *size* | La taille du label. Cette taille limite le texte si le retour à la ligne est activé. | `vector3` | `get+set`{.mark} |
| *material* | Le matériau utilisé par le label. | `hash` | `get+set`{.mark}|
| *font* | La police utilisée par le label. | `hash` | `get+set`{.mark}|


## Propriétés des nœuds d'interface graphique {#gui-node-properties}

Les nœuds d'interface graphique possèdent des fonctions de lecture et d'écriture propres à chaque propriété, comme `gui.get_position()` et `gui.set_position()`. Les propriétés intégrées répertoriées ci-dessous peuvent également être lues et modifiées avec `gui.get(node, property)` et `gui.set(node, property, value)`. D'autres valeurs des nœuds peuvent encore nécessiter leurs fonctions dédiées. Les constantes de matériau des nœuds d'interface graphique utilisent également les fonctions génériques. Pour accéder à une composante d'une propriété vectorielle, ajoutez son nom, par exemple `gui.set(node, "color.x", 1)`.

Les fonctions génériques et les fonctions propres aux propriétés n'utilisent pas toujours des types de valeurs identiques. `gui.get()` renvoie un `vector4` pour les propriétés complètes `position`, `scale`, `size` et `euler`, tandis que les fonctions correspondantes propres à ces propriétés renvoient un `vector3`. `gui.set()` accepte un `vector3` ou un `vector4` pour ces propriétés. La propriété générique `rotation` utilise un quaternion ; utilisez `euler` pour définir la rotation en degrés.

* `position` (ou `gui.PROP_POSITION`)
* `rotation` (ou `gui.PROP_ROTATION`)
* `euler` (ou `gui.PROP_EULER`)
* `scale` (ou `gui.PROP_SCALE`)
* `color` (ou `gui.PROP_COLOR`)
* `outline` (ou `gui.PROP_OUTLINE`)
* `shadow` (ou `gui.PROP_SHADOW`)
* `size` (ou `gui.PROP_SIZE`)
* `fill_angle` (ou `gui.PROP_FILL_ANGLE`)
* `inner_radius` (ou `gui.PROP_INNER_RADIUS`)
* `leading` (ou `gui.PROP_LEADING`)
* `tracking` (ou `gui.PROP_TRACKING`)
* `slice9` (ou `gui.PROP_SLICE9`)

Toutes les valeurs de couleur sont encodées dans un `vector4` dont les composantes correspondent aux valeurs RGBA :

`x`
: La composante rouge

`y`
: La composante verte

`z`
: La composante bleue

`w`
: La composante alpha

*Propriétés des nœuds d'interface graphique*

| propriété   | description                            | type            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*   | La couleur de la face du nœud.            | `vector4`      | `gui.get_color()` `gui.set_color()` |
| *outline* | La couleur du contour du nœud.         | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | La position du nœud. | `vector3` | `gui.get_position()` `gui.set_position()` |
| *rotation* | La rotation du nœud. La fonction de lecture renvoie un quaternion ; la fonction d'écriture accepte un quaternion ou des angles d'Euler sous forme de vecteur. | `quaternion`, `vector3` ou `vector4` | `gui.get_rotation()` `gui.set_rotation()` |
| *euler* | La rotation du nœud exprimée en angles d'Euler en degrés. | `vector3` | `gui.get_euler()` `gui.set_euler()` |
| *scale* | L'échelle du nœud exprimée sous forme de multiplicateur sur chaque axe. | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | La couleur de l'ombre du nœud. | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | La taille du nœud avant mise à l'échelle. | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | L'angle de remplissage d'un nœud pie exprimé en degrés dans le sens inverse des aiguilles d'une montre. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | Le rayon intérieur d'un nœud pie. | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *leading* | Le facteur d'échelle de l'interligne d'un nœud texte. | `number` | `gui.get_leading()` `gui.set_leading()` |
| *tracking* | Le facteur d'échelle de l'espacement des lettres d'un nœud texte. | `number` | `gui.get_tracking()` `gui.set_tracking()` |
| *slice9* | Les distances des bords d'un nœud slice9. | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
