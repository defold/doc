---
title: Balisage de texte enrichi dans Defold
brief: Ce manuel explique comment appliquer des styles aux composants Label et aux nœuds de texte GUI avec un balisage de texte enrichi, et comment inspecter les liens et les sprites depuis Lua.
---

# Balisage de texte enrichi {#rich-text-markup}

Utilisez le balisage dans les composants Label et les nœuds de texte GUI pour appliquer des styles visuels et des effets imbriqués, et inspecter les liens et les sprites depuis Lua.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

Vous pouvez aussi définir sur la police un style d'objet nommé réutilisable et le sélectionner depuis un lien :

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## Référence des balises {#tag-reference}

| Balise | Fonction | Exemple |
| --- | --- | --- |
| [`color`](#color) | Définit la couleur de remplissage des glyphes. | <img src="/manuals/images/richtext/color_green.webp" alt="Texte vert" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | Modifie la taille utilisée pour la mise en forme des glyphes et la mise en page. | <img src="/manuals/images/richtext/size_24.webp" alt="Texte de 24 pixels" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | Applique un dégradé de couleurs statique ou animé. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="Texte avec un dégradé horizontal" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | Souligne le texte. | <img src="/manuals/images/richtext/underline_solid.webp" alt="Texte souligné" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | Barre le texte. | <img src="/manuals/images/richtext/strike_solid.webp" alt="Texte barré" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | Définit la largeur et la couleur du contour des glyphes. | <img src="/manuals/images/richtext/outline.webp" alt="Texte avec un contour" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | Ajoute une ombre au texte. | <img src="/manuals/images/richtext/shadow.webp" alt="Texte avec une ombre" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | Applique un décalage aléatoire animé. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="Texte qui tremble" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | Anime le texte selon une onde sinusoïdale. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="Texte ondulant" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | Ajoute un objet sprite intégré au texte. | <img src="/manuals/images/richtext/sprite.webp" alt="Sprite intégré au texte" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | Ajoute un objet lien interactif. | <img src="/manuals/images/richtext/link.webp" alt="Texte de lien" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## Syntaxe {#syntax}

Les noms de balises et d'attributs sont sensibles à la casse. Une paire de balises s'applique au texte UTF-32 visible qu'elle contient. Les objets sprite utilisent des balises autofermantes.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### Attributs {#attributes}

Les valeurs d'attributs peuvent être écrites sans guillemets lorsqu'elles ne contiennent aucun espace, ou entourées de guillemets simples ou doubles. `color` et `size` acceptent une première valeur abrégée ainsi que la forme nommée `value`.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### Imbrication {#nesting}

Les balises doivent se fermer dans l'ordre inverse de leur ouverture. Les valeurs d'un style intérieur remplacent les mêmes propriétés d'un style extérieur. Les propriétés différentes se combinent. Les effets de chaque portion de texte restent actifs indépendamment : les dégradés imbriqués multiplient donc les couleurs et les effets de position imbriqués additionnent leurs décalages.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### Entités {#entities}

Utilisez `&amp;`, `&apos;`, `&gt;`, `&lt;` et `&quot;` pour les caractères réservés dans le texte visible. Les entités numériques ne sont pas prises en charge actuellement.

## Balises {#tags}

Les balises de texte enrichi appliquent un style à la portion de texte qu'elles entourent ou décrivent un objet qui peut être inspecté depuis Lua. Les balises de style utilisent une balise de fermeture correspondante. L'objet `sprite` est autofermant, tandis que `link` entoure le texte du lien.

### `color` {#color}

Définit la couleur de remplissage des glyphes. Les couleurs utilisent `#RRGGBB` ou `#RRGGBBAA`. Le préfixe dièse est obligatoire ; `0xFF0000` et `FF0000` ne sont pas valides. Le résultat multiplie la couleur de base du label ou du moteur de rendu.

| Attribut | Obligatoire | Valeur par défaut | Signification |
| --- | --- | --- | --- |
| `=color` ou `value=color` | Oui | Aucune valeur par défaut | Couleur de remplissage au format hexadécimal RGB ou RGBA. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![Texte d'exemple affiché en vert opaque](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![Texte d'exemple affiché en vert à demi-opacité](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size` {#size}

Modifie la taille utilisée pour la mise en forme des glyphes et la mise en page, et pas seulement l'échelle des sommets. Les valeurs relatives utilisent toujours la taille de base de la police de la mise en page. Elles ne se cumulent pas avec une balise `size` extérieure.

| Attribut | Obligatoire | Valeur par défaut | Signification |
| --- | --- | --- | --- |
| `=size` ou `value=size` | Oui | Aucune valeur par défaut | Taille absolue, pourcentage, multiple de la taille de base ou décalage signé par rapport à celle-ci, sous l'une des formes ci-dessous. |

| Forme | Exemple pour 32 px | Taille résolue |
| --- | --- | --- |
| Nombre seul ou `px` | `24`, `24px` | 24 px |
| Pourcentage de la taille de base | `120%` | 38.4 px |
| Multiple de la taille de base | `2em` | 64 px |
| Décalage signé par rapport à la taille de base | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![Texte d'exemple affiché en 24 pixels](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*120% de 32px*

![Texte d'exemple affiché à 120 pour cent de 32 pixels](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*2em pour 32px*

![Texte d'exemple affiché au double de la taille de base de 32 pixels](images/richtext/size_2em.webp)

</div>
</div>

### `gradient` {#gradient}

Un dégradé accepte exactement un ensemble complet d'attributs. Mélanger des ensembles ou omettre l'un de leurs membres n'est pas valide.

| Mode | Attributs obligatoires | Interpolation |
| --- | --- | --- |
| Horizontal | `left`, `right` | Interpole entre les deux couleurs horizontales. |
| Vertical | `bottom`, `top` | Interpole entre les couleurs du bas et du haut. |
| Quatre coins | `tl`, `tr`, `bl`, `br` | Interpole entre les couleurs des quatre sommets. |

| Attribut | Obligatoire | Valeur par défaut | Signification |
| --- | --- | --- | --- |
| `left`, `right` | Pour le mode horizontal | Aucune | Couleurs des extrémités horizontales au format `#RRGGBB` ou `#RRGGBBAA`. Les deux doivent être présentes. |
| `bottom`, `top` | Pour le mode vertical | Aucune | Couleurs des extrémités verticales. Les deux doivent être présentes. |
| `tl`, `tr`, `bl`, `br` | Pour le mode quatre coins | Aucune | Couleurs des coins supérieur gauche, supérieur droit, inférieur gauche et inférieur droit. Les quatre doivent être présentes. |
| `fit` | Non | `span` | `glyph` échantillonne chaque position de texte après mise en forme ; `span` répartit le dégradé sur tout le texte entouré par la balise. |
| `hz` | Non | `0` | Nombre de cycles complets de défilement par seconde dans `[0,)` ; zéro conserve un dégradé statique. |
| `direction` | Non | `forward` | `forward` ou `reverse`. Contrôle le sens du défilement lorsque `hz` est non nul. |

Lorsque `fit` est omis, `fit=span` répartit le dégradé sur tout le texte entouré par la balise. `fit=glyph` échantillonne indépendamment chaque position de texte après mise en forme. L'attribut facultatif `hz` définit le nombre de cycles complets d'animation du défilement par seconde ; sa valeur par défaut de zéro conserve un dégradé statique. La rampe de couleurs répétée en miroir défile en continu et boucle sans saut de couleur. `direction=forward` est la valeur par défaut ; utilisez `direction=reverse` pour inverser le défilement.

```text
<gradient left=#FF00FF right=#FFFFFF>Horizontal Gradient</gradient>

<gradient hz=0.25 fit=glyph bottom=#182848 top=#4B6CB7>Animated vertical glyphs</gradient>

<gradient hz=0.25 direction=reverse left=#FF0000 right=#0000FF>Reverse flow</gradient>

<gradient hz=0.25 direction=reverse fit=span left=#FF0000 right=#0000FF>One animated span color</gradient>

<gradient fit=glyph tl=#FF0000 tr=#00FF00 bl=#0000FF br=#FFFFFF>
    Four corners
</gradient>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Horizontal*

![Texte d'exemple avec un dégradé horizontal du magenta au blanc](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Vertical*

![Texte d'exemple avec un dégradé bleu vertical](images/richtext/gradient_vertical.webp)

</div>
</div>

**Quatre coins**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Texte d'exemple avec un dégradé à quatre coins ajusté à chaque glyphe](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Texte d'exemple avec un dégradé à quatre coins ajusté à la portion de texte](images/richtext/gradient_four_text.webp)

</div>
</div>

**Animé**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Dégradé à défilement animé ajusté à chaque glyphe](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Dégradé à défilement animé ajusté à la portion de texte](images/richtext/gradient_flow_span.webp)

</div>
</div>

Les couleurs du dégradé multiplient la couleur de remplissage actuelle. Un dégradé à l'intérieur de `color=#808080` ne peut donc produire aucun canal plus lumineux que ce multiplicateur de base.

### `ul` {#ul}

Trace un soulignement en utilisant les métriques de soulignement de la police lorsqu'elles sont disponibles. La balise n'a pas de couleur indépendante : la ligne hérite de la couleur de remplissage effective, y compris les dégradés horizontaux, verticaux et à quatre coins.

| Attribut | Obligatoire | Valeur par défaut | Signification |
| --- | --- | --- | --- |
| `pattern` | Non | `solid` | `solid` ou `dashed`. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Continu*

![Texte d'exemple avec un soulignement continu](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Tirets*

![Texte d'exemple avec un soulignement en tirets](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Dégradé*

![Texte d'exemple avec un soulignement en dégradé](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike` {#strike}

Trace une ligne à travers le texte entouré par la balise. Accepte les mêmes valeurs de `pattern` que `ul` et hérite également de la couleur de remplissage effective.

| Attribut | Obligatoire | Valeur par défaut | Signification |
| --- | --- | --- | --- |
| `pattern` | Non | `solid` | `solid` ou `dashed`. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Continu*

![Texte d'exemple barré d'un trait continu](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Tirets*

![Texte d'exemple barré d'un trait en tirets](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline` {#outline}

Définit la largeur du contour, sa couleur ou les deux. Au moins un attribut est obligatoire. Une largeur nulle désactive explicitement le contour pour la portion de texte.

| Attribut | Obligatoire | Valeur par défaut | Signification |
| --- | --- | --- | --- |
| `size` | L'un des attributs size/color | Héritée ; `0` sur une police par défaut | Largeur en unités de mise en page, dans l'intervalle `[0,)`. Les suffixes d'unité ne sont pas acceptés. |
| `color` | L'un des attributs size/color | Héritée ; `#000000` sur un label par défaut | Couleur unique du contour au format hexadécimal RGB (`#RRGGBB`) ou RGBA (`#RRGGBBAA`) ; la composante alpha contrôle l'opacité. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Contour noir extérieur*

![Texte d'exemple avec un contour noir extérieur](images/richtext/outline.webp)

</div>
</div>

### `shadow` {#shadow}

Ajoute une ombre nette au texte entouré par la balise. Au moins un attribut est obligatoire. Les attributs omis par une balise imbriquée conservent la valeur de l'ombre extérieure ; ceux omis par la balise la plus extérieure conservent la valeur de base de l'ombre de la police.

| Attribut | Obligatoire | Valeur par défaut | Signification |
| --- | --- | --- | --- |
| `color` | Non | Héritée ; `#000000` sur un label par défaut | Couleur de l'ombre au format `#RRGGBB` ou `#RRGGBBAA`. |
| `x` | Non | Hérité ; `0` sur une police par défaut | Décalage horizontal de l'ombre en unités de mise en page. Les valeurs positives la déplacent vers la droite. |
| `y` | Non | Hérité ; `0` sur une police par défaut | Décalage vertical de l'ombre en unités de mise en page. Les valeurs positives la déplacent vers le haut. |
| `blur` | Non | Hérité ; `0` sur une police par défaut | Rayon du flou en unités de mise en page, dans l'intervalle `[0,)`. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![Texte d'exemple avec une ombre décalée](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
Le flou de l'ombre est généré et stocké dans l'atlas de glyphes. Une portion de texte peut demander un flou plus petit que celui précalculé pour la police ; les valeurs plus élevées sont conservées dans la mise en page, mais leur rendu utilise actuellement le flou maximal disponible dans l'atlas.
:::

### `shake` {#shake}

Applique un décalage aléatoire animé déterministe sans modifier les sauts de ligne ni les limites de la mise en page. L'effet gère le temps en interne ; les scripts n'ont pas besoin de modifier le texte du label à chaque image de l'animation.

| Attribut | Obligatoire | Valeur par défaut | Valeurs valides | Signification |
| --- | --- | --- | --- | --- |
| `hz` | Non | 20 | `[0,)` | Nombre de transitions vers une cible aléatoire par seconde. Zéro met l'effet en pause. |
| `amplitude` | Non | 0.5 | `[0,)` | Déplacement maximal en unités de mise en page. |
| `fit` | Non | `glyph` | `glyph` ou `span` | `glyph` calcule un décalage respectant les groupes de caractères pour chaque unité de glyphe mise en forme. `span` déplace toute la portion de texte entourée par la balise comme un seul bloc rigide. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Texte d'exemple avec un tremblement animé par glyphe](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Texte d'exemple avec un tremblement animé de toute la portion de texte](images/richtext/shake_span.webp)

</div>
</div>

### `wave` {#wave}

Déplace les caractères de haut en bas selon une onde sinusoïdale animée sans modifier les sauts de ligne ni les limites de la mise en page. La mise en page accumule le temps d'animation lors de ses mises à jour.

| Attribut | Obligatoire | Valeur par défaut | Signification |
| --- | --- | --- | --- |
| `amplitude` | Non | 1 | Déplacement vertical maximal en unités de mise en page, dans l'intervalle `[0,)`. |
| `hz` | Non | 1 | Nombre de cycles temporels complets par seconde, dans l'intervalle `[0,)`. Zéro met l'onde en pause. |
| `wavelength` | Non | 6 | Nombre de positions de texte UTF-32 visible par cycle spatial complet, dans l'intervalle `[1,)`. Les caractères que la police met en forme ensemble, comme un caractère de base et son accent combinatoire, se déplacent comme une seule unité. |
| `fit` | Non | `glyph` | `glyph` applique l'onde spatiale sur le texte. `span` donne à toute la portion de texte entourée par la balise un même décalage sinusoïdal vertical. |
| `direction` | Non | `forward` | `forward` fait progresser l'onde normalement. `reverse` inverse son sens de propagation. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Texte d'exemple avec une onde animée par glyphe](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Texte d'exemple animé comme une seule portion de texte](images/richtext/wave_span.webp)

</div>
</div>

### `sprite` {#sprite}

Ajoute un objet sprite autofermant à la position actuelle dans le texte visible. Ses attributs sont préservés comme métadonnées pour `label.get_layout_objects()` et `gui.get_layout_objects()`.

| Attribut | Obligatoire | Valeur par défaut | Signification |
| --- | --- | --- | --- |
| `id` | Non | Généré | Identifiant stable haché dans le champ `id` de l'objet de mise en page renvoyé. |
| `src` | Non | Aucune | Identifiant de ressource sprite défini par l'application, par exemple le chemin d'une image ou d'un atlas du projet. |
| `animation` | Non | Aucune | Identifiant d'animation défini par l'application au sein de la ressource. |
| `width` | Non | `1em` | Largeur résolue du sprite. |
| `height` | Non | `1em` | Hauteur résolue du sprite. |
| Tout autre attribut | Non | Absent | Métadonnées définies par l'application, conservées pour le résolveur d'objets et les API d'objets de mise en page. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Sprite résolu intégré au texte*

![Logo Defold affiché dans le texte](images/richtext/sprite.webp)

</div>
</div>

Les dimensions acceptent des unités de mise en page positives sans suffixe, `px`, `em` ou `%`. `em` et `%` utilisent tous deux la taille de base de la police de la mise en page du texte.

Chaque dimension manquante vaut indépendamment `1em` par défaut. Omettre les deux produit un objet de `1em × 1em` ; préciser uniquement la largeur ne déduit pas automatiquement la hauteur à partir du rapport largeur/hauteur d'une ressource.

::: important
La balise sprite n'est qu'un emplacement réservé où le développeur peut insérer l'objet de son choix !
:::

### `link` {#link}

Décrit une plage de texte visible comme un objet lien. Le texte entouré par la balise est mis en page normalement et reçoit par défaut le style nommé `link`. Les composants Label et GUI sélectionnent `link:hover` et `link:active` en réponse aux entrées, sans refaire la mise en forme des glyphes. Consultez [Messages d'interaction](#interaction-messages) pour les messages produits par les entrées sur les liens.

| Attribut | Obligatoire | Valeur par défaut | Signification |
| --- | --- | --- | --- |
| `src` | Non | Aucune | Cible du lien définie par l'application. La valeur est renvoyée sous forme de chaîne sans validation ni navigation automatique. |
| `id` | Non | Généré | Identifiant stable haché dans le champ `id` de l'objet de mise en page renvoyé. |
| `style` | Non | `link` | Style par défaut nommé pour le texte du lien. |
| Tout autre attribut | Non | Absent | Métadonnées définies par l'application, par exemple un identifiant, une action, une infobulle ou une valeur d'analyse d'usage. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![www.defold.com affiché avec le style de lien par défaut et un soulignement](images/richtext/link.webp)

</div>
</div>

Le composant suit l'état du pointeur pour chaque lien. Il applique `link:hover` lorsque le pointeur survole le lien et `link:active` lorsque le pointeur est pressé. Lorsqu'aucun de ces états ne s'applique, le composant restaure le style nommé par l'attribut `style` du lien, ou `link` lorsque cet attribut est absent.

### Messages d'interaction {#interaction-messages}

Les interactions avec les liens utilisent le système d'entrée habituel de Defold. Ajoutez une liaison Mouse Trigger pour `MOUSE_BUTTON_LEFT`, ce qui active également les entrées tactiles à un doigt, et acquérez le focus d'entrée dans le script de l'objet de jeu ou le script GUI :

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

Consultez [Focus d'entrée](/manuals/input/#input-focus) et [Entrées de la souris et tactiles](/manuals/input-mouse-and-touch) pour les détails de configuration.

Lorsqu'un composant Label ou GUI reçoit des entrées du pointeur, les liens produisent les messages suivants. Les messages des labels sont envoyés à l'objet de jeu auquel ils appartiennent ; les messages GUI sont envoyés au script GUI.

| Message | Moment de l'envoi |
| --- | --- |
| `text_object_hovered` | Le pointeur entre sur un lien. |
| `text_object_unhovered` | Le pointeur quitte un lien. |
| `text_object_clicked` | Un appui est relâché sur le même lien. |

Chaque message contient ces champs :

| Champ | Type | Description |
| --- | --- | --- |
| `id` | `hash` | L'attribut `id` de l'objet, ou son identifiant d'objet de mise en page généré. |
| `type` | `hash` | Le type de l'objet de mise en page, actuellement `hash("link")`. |
| `src` | `string` | La valeur de l'attribut `src` de l'objet définie par l'application, ou une chaîne vide si elle est absente. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## Styles nommés {#named-styles}

Chaque collection de polices contient des styles d'objets nommés qui agissent uniquement sur le rendu. Un lien utilise le style nommé par son attribut `style`, ou `link` lorsque cet attribut est absent. Il n'existe pas de balise générique `<style>` pour les portions de texte.

Defold fournit les valeurs par défaut suivantes :

| Style | Multiplicateur de couleur de remplissage | Décoration |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | Soulignement continu |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | Aucune |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | Aucune |

Définissez un style avec une chaîne de texte contenant des balises d'ouverture. Les balises sont implicitement fermées dans l'ordre inverse ; les balises de fermeture et le texte visible ne sont donc pas autorisés.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

Les balises sont appliquées de gauche à droite, comme si elles étaient imbriquées autour du texte de l'objet. Un style d'objet sélectionné par l'appelant est appliqué après le style par défaut. Lorsque plusieurs balises définissent la même propriété de rendu, la valeur appliquée en dernier remplace les précédentes. Les effets sont ajoutés de gauche à droite.

::: sidenote
L'appel de `font.set_style()` remplace les propriétés de rendu et les effets de ce style nommé. Les décorations définies par la ressource restent inchangées ; redéfinir `link` ne supprime donc pas son soulignement par défaut. Les styles nommés acceptent les balises agissant uniquement sur le rendu, telles que `color`, `outline`, `shadow`, `gradient`, `wave` et `shake`. Les balises modifiant la mise en page, les balises de décoration et les balises d'objet sont rejetées.
:::

## API des objets de mise en page {#layout-object-api}

Utilisez `label.get_layout_objects()` ou `gui.get_layout_objects()` pour récupérer les objets `sprite` et `link` du texte mis en page.

### `label.get_layout_objects()` {#labelget_layout_objects}

```lua
objects = label.get_layout_objects(url)
```

| Argument | Type | Description |
| --- | --- | --- |
| `url` | `string`, `hash` ou `url` | Le composant Label à inspecter, par exemple `"#label"`. |

### `gui.get_layout_objects()` {#guiget_layout_objects}

```lua
objects = gui.get_layout_objects(node)
```

| Argument | Type | Description |
| --- | --- | --- |
| `node` | `node` | Le nœud de texte GUI à inspecter, par exemple `gui.get_node("rich_text")`. |

Les deux fonctions renvoient un tableau nouvellement créé contenant les objets de mise en page actuels dans l'ordre de la source. Elles renvoient un tableau vide lorsque le texte ne contient aucune balise d'objet. Comme les objets et leurs attributs sont copiés dans Lua à chaque appel, mettez le résultat en cache et interrogez à nouveau après avoir modifié le texte ou une autre propriété qui change sa mise en page.

### Champs des objets renvoyés {#returned-object-fields}

| Champ | Type | Description |
| --- | --- | --- |
| `type` | `string` | `"sprite"` ou `"link"`. |
| `id` | `hash` | Identifiant de l'objet utilisé dans les messages d'interaction. |
| `text_offset` | `number` | Position commençant à zéro dans le texte visible, mesurée en points de code Unicode. Le balisage est exclu, et les entités comptent comme les caractères qu'elles représentent après décodage. Pour un sprite, il s'agit de son point d'insertion. |
| `text_length` | `number` | Longueur du texte visible entouré par la balise, en points de code Unicode. Un sprite a une longueur de un pour son point de code de remplacement d'objet U+FFFC inséré. |
| `width` | `number` | Largeur résolue en unités de mise en page du texte. Les liens ont actuellement une largeur nulle. |
| `height` | `number` | Hauteur résolue en unités de mise en page du texte. Les liens ont actuellement une hauteur nulle. |
| `x` | `number` | Position horizontale du coin inférieur gauche de l'objet par rapport à l'origine supérieure gauche de la mise en page du texte. |
| `y` | `number` | Position verticale du coin inférieur gauche de l'objet par rapport à l'origine supérieure gauche de la mise en page du texte. |
| `attributes` | `table` | Tous les attributs de la balise sous forme de paires clé/valeur de chaînes. Les valeurs des attributs conservent leur représentation source, comme `"2em"`. Une valeur abrégée sans nom est stockée sous la clé `value`. |

::: sidenote
`text_offset` et `text_length` ne sont pas des décalages en octets UTF-8. Un caractère non ASCII comme `å` ou `猫` compte pour une position.
:::

### Exemple Lua {#lua-example}

```lua
local text = [[
Read the <link src=https://defold.com/manuals/ id=manual>manual</link>
or inspect <sprite src=images/info.png width=2em/> for more information.
]]

go.set("#label", "text", text)

local objects = label.get_layout_objects("#label")
for _, object in ipairs(objects) do
    if object.type == "link" then
        print("link", object.attributes.src)
        print("visible range", object.text_offset, object.text_length)
        print("position", object.x, object.y)
    elseif object.type == "sprite" then
        print("sprite", object.x, object.y, object.width, object.height)
        pprint(object.attributes)
    end
end

local gui_objects = gui.get_layout_objects(gui.get_node("rich_text"))
```

## Combinaisons utiles {#useful-combinations}

### Contour coloré avec un dégradé horizontal {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

Le dégradé multiplie uniquement la couleur de remplissage ; le contour conserve sa propre couleur.

### Faire trembler une phrase et appliquer un dégradé à un mot {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

L'effet de position extérieur s'applique à chaque glyphe. L'effet de couleur imbriqué s'applique uniquement à « whole ».

### Remplacer une propriété sans perdre les autres {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

La couleur intérieure modifie le remplissage tout en conservant la largeur et la couleur de contour héritées.
