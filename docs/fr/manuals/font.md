---
title: Manuel des polices dans Defold
brief: Ce manuel décrit la gestion des polices dans Defold et leur affichage à l'écran dans vos jeux.
---

# Fichiers de police {#font-files}

Les polices servent à afficher du texte dans les composants (component) Label et les nœuds de texte de l'interface graphique. Defold prend en charge plusieurs formats de fichiers de police :

- TrueType
- OpenType
- BMFont

Depuis Defold 1.13.2, l'ancien moteur de mise en page du texte et le moteur complet prennent tous deux en charge les contours TrueType et OpenType CFF1/CFF2, y compris la génération à l'exécution à partir de ressources `.ttf` et `.otf`.

Pour savoir comment appliquer des styles à des portions de texte et utiliser des liens et des sprites intégrés au texte, consultez le [manuel du balisage de texte enrichi](/manuals/font-richtext).

Les polices ajoutées à votre projet sont automatiquement converties dans un format de texture que Defold peut afficher. Deux techniques de rendu des polices sont disponibles, chacune avec ses avantages et ses inconvénients :

- Matriciel
- Champ de distance

## Polices prégénérées ou générées à l'exécution {#offline-or-runtime-fonts}

Par défaut, la conversion des glyphes en images matricielles a lieu lors du build (hors ligne). L'inconvénient est que tous les glyphes possibles de chaque police doivent être rastérisés pendant le build, ce qui peut produire de très grandes textures qui consomment de la mémoire et augmentent également la taille du bundle.

Avec les « polices générées à l'exécution », les polices `.ttf` et `.otf` sont incluses telles quelles dans le bundle, et la rastérisation s'effectue à la demande à l'exécution. Cela minimise à la fois l'utilisation de mémoire à l'exécution et la taille du bundle.

## Prise en charge de la disposition du texte (par exemple, de droite à gauche) {#text-layout-support-eg-right-to-left}

Les polices générées à l'exécution ont également l'avantage de prendre en charge toutes les fonctions de disposition du texte, par exemple de droite à gauche.
Nous utilisons actuellement les bibliothèques [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak) et [SkriBidi](https://github.com/memononen/Skribidi).

Consultez [Activation des polices générées à l'exécution](/manuals/font#enabling-runtime-fonts)

L'éditeur utilise le moteur de rendu des polices du moteur pour les aperçus des polices et du texte des scènes. La mise en forme des glyphes et la mise en page de droite à gauche nécessitent des [polices générées à l'exécution](#enabling-runtime-fonts) et l'option **Use full text layout system** dans l'App Manifest. Pour les polices générées hors ligne, l'aperçu respecte les paramètres **Characters** et **All Chars** de la police.

## Collection de polices {#font-collection}

Le format de fichier `.fontc` est également appelé collection de polices. En mode hors ligne, une seule police lui est associée.
Lorsque vous utilisez des polices générées à l'exécution, vous pouvez associer plusieurs fichiers de police (`.ttf` ou `.otf`) à la collection de polices.

Cela permet d'utiliser une collection de polices pour afficher plusieurs textes dans différentes langues, tout en limitant l'empreinte mémoire.
Par exemple, vous pouvez charger une collection contenant la police japonaise, associer cette police à la police principale actuelle, puis décharger la collection de polices japonaise.

## Création d'une police {#creating-a-font}

Pour créer une police à utiliser dans Defold, créez un fichier Font en sélectionnant <kbd>File ▸ New...</kbd> dans le menu, puis <kbd>Font</kbd>. Vous pouvez également faire un <kbd>clic droit</kbd> sur un emplacement dans le navigateur *Assets* et sélectionner <kbd>New... ▸ Font</kbd>.

![Nom de la nouvelle police](images/font/new_font_name.png)

Donnez un nom au nouveau fichier de police et cliquez sur <kbd>Ok</kbd>. Le nouveau fichier de police s'ouvre alors dans l'éditeur.

![Nouvelle police](images/font/new_font.png)

Faites glisser la police que vous souhaitez utiliser dans le navigateur *Assets* et déposez-la à un emplacement approprié.

Définissez la propriété *Font* sur le fichier de police, puis réglez les propriétés de la police selon vos besoins.

## Propriétés {#properties}

*Font*
: Le fichier TTF, OTF ou *`.fnt`* à utiliser pour générer les données de la police.

*Material*
: Le matériau à utiliser pour le rendu de cette police. Veillez à le modifier pour les polices à champ de distance et les BMFonts (voir les détails ci-dessous).

*Output Format*
: Le type de données de police générées.

  - `TYPE_BITMAP` convertit le fichier OTF ou TTF importé en une texture de planche de glyphes dont les données matricielles servent à afficher les nœuds de texte. Les canaux de couleur servent à encoder la forme des glyphes, le contour et l'ombre portée. Pour les fichiers *`.fnt`*, la texture matricielle source est utilisée telle quelle.
  - `TYPE_DISTANCE_FIELD` La police importée est convertie en une texture de planche de glyphes dont les données représentent des distances au bord des glyphes plutôt que des pixels à l'écran. Voir les détails ci-dessous.

*Render Mode*
: Le mode de rendu à utiliser pour afficher les glyphes.

  - `MODE_SINGLE_LAYER` produit un seul quadrilatère pour chaque caractère.
  - `MODE_MULTI_LAYER` produit des quadrilatères distincts pour la forme du glyphe, le contour et les ombres. Les couches sont affichées de l'arrière vers l'avant, ce qui empêche un caractère de masquer ceux déjà affichés si le contour est plus large que la distance entre les glyphes. Ce mode de rendu permet également de décaler correctement l'ombre portée, conformément aux propriétés Shadow X/Y de la ressource de police.

*Size*
: La taille cible des glyphes en pixels.

*Antialias*
: Indique si la police doit être anticrénelée lors de sa génération dans l'image matricielle cible. Définissez cette valeur sur 0 si vous souhaitez un rendu de police au pixel près.

*Alpha*
: La transparence du glyphe. De 0.0 à 1.0, où 0.0 signifie transparent et 1.0 opaque.

*Outline Alpha*
: La transparence du contour généré. De 0.0 à 1.0.

*Outline Width*
: La largeur du contour généré en pixels. Définissez cette valeur sur 0 pour ne pas avoir de contour.

*Shadow Alpha*
: La transparence de l'ombre générée. De 0.0 à 1.0.

::: sidenote
La prise en charge des ombres est assurée par les shaders des matériaux de police intégrés et fonctionne avec les modes de rendu à une ou plusieurs couches. Si vous n'avez pas besoin du rendu de police en couches ni de la prise en charge des ombres, il est préférable d'utiliser un shader plus simple, comme *`builtins/font-singlelayer.fp`*.
:::

*Shadow Blur*
: Pour les polices matricielles, ce paramètre indique le nombre de fois qu'un petit noyau de flou sera appliqué à chaque glyphe de la police. Pour les polices à champ de distance, ce paramètre correspond à la largeur réelle du flou en pixels.

*Shadow X/Y*
: Le décalage horizontal et vertical, en pixels, de l'ombre générée. Ce paramètre n'affecte l'ombre du glyphe que si Render Mode est défini sur `MODE_MULTI_LAYER`.

*Characters*
: Les caractères à inclure dans la police. Par défaut, ce champ contient les caractères ASCII imprimables (codes de caractères 32-126). Vous pouvez ajouter ou supprimer des caractères dans ce champ pour en inclure davantage ou moins dans la police.

Pour les polices générées à l'exécution, ce texte sert à préremplir le cache avec les glyphes appropriés. Cette opération a lieu au chargement. Consultez `font.prewarm_text()`.

::: sidenote
Les caractères ASCII imprimables sont :
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Si vous cochez cette propriété, tous les glyphes disponibles dans le fichier source seront inclus dans le résultat.

*Cache Width/Height*
: Limite la taille de l'image matricielle du cache de glyphes. Lorsque le moteur affiche du texte, il recherche le glyphe dans cette image. Si le glyphe n'y figure pas, il est ajouté au cache avant le rendu. Si l'image matricielle du cache est trop petite pour contenir tous les glyphes que le moteur doit afficher, une erreur est signalée (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Si la valeur est définie sur 0, la taille du cache est déterminée automatiquement et peut augmenter jusqu'à 2048x4096 au maximum.

## Polices à champ de distance {#distance-field-fonts}

Les polices à champ de distance stockent dans la texture la distance au bord du glyphe à la place de données matricielles. Lorsque le moteur affiche la police, un shader spécial est nécessaire pour interpréter les données de distance et les utiliser pour dessiner le glyphe. Les polices à champ de distance consomment davantage de ressources que les polices matricielles, mais offrent une plus grande souplesse de redimensionnement.

![Police à champ de distance](images/font/df_font.png)

Veillez à définir la propriété *Material* de la police sur *`builtins/fonts/font-df.material`* (ou tout autre matériau capable de traiter les données de champ de distance) lors de sa création, faute de quoi la police n'utilisera pas le bon shader lors de son affichage à l'écran.

## Polices matricielles BMFont {#bitmap-bmfonts}

Outre les images matricielles générées, Defold prend en charge les polices matricielles prégénérées au format « BMFont ». Ces polices se composent d'une planche de glyphes PNG contenant tous les glyphes. Un fichier *`.fnt`* contient en complément la position de chaque glyphe sur la planche, ainsi que des informations sur la taille et le crénage. (Notez que Defold ne prend pas en charge la version XML du format *`.fnt`* utilisée par Phaser et certains autres outils.)

Ces types de polices n'améliorent pas les performances par rapport aux polices matricielles générées à partir de fichiers de police TrueType ou OpenType, mais peuvent contenir directement dans l'image des graphismes, des couleurs et des ombres de votre choix.

Ajoutez les fichiers *`.fnt`* et *`.png`* générés à votre projet Defold. Ces fichiers doivent se trouver dans le même dossier. Créez un fichier de police et définissez la propriété *font* sur le fichier *`.fnt`*. Assurez-vous que *output_format* est défini sur `TYPE_BITMAP`. Defold ne générera pas d'image matricielle, mais utilisera celle fournie dans le PNG.

::: sidenote
Pour créer une BMFont, vous devez utiliser un outil capable de générer les fichiers appropriés. Plusieurs possibilités existent :

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), un outil réservé à Windows fourni par AngelCode.
* [Shoebox](http://renderhjs.net/shoebox/), une application gratuite fondée sur Adobe Air pour Windows et macOS.
* [Hiero](https://libgdx.com/wiki/tools/hiero), un outil libre fondé sur Java.
* [Glyph Designer](https://71squared.com/glyphdesigner), un outil commercial pour macOS de 71 Squared.
* [bmGlyph](https://www.bmglyph.com), un outil commercial pour macOS de Sovapps.
:::

![BMfont](images/font/bm_font.png)

Pour que la police s'affiche correctement, n'oubliez pas de définir la propriété de matériau sur *`builtins/fonts/font-fnt.material`* lors de sa création.

## Artefacts et bonnes pratiques {#artifacts-and-best-practices}

En général, les polices matricielles conviennent le mieux lorsque la police est affichée sans changement d'échelle. Leur rendu à l'écran est plus rapide que celui des polices à champ de distance.

Les polices à champ de distance supportent très bien l'agrandissement. Les polices matricielles, en revanche, sont de simples images composées de pixels : leurs pixels grossissent lorsque la police est agrandie, ce qui produit des artefacts en blocs. Voici un exemple avec une police de 48 pixels, agrandie quatre fois.

![Polices agrandies](images/font/scale_up.png)

Lors d'une réduction, le GPU peut réduire et anticréneler les textures matricielles efficacement et avec un bon résultat visuel. Une police matricielle conserve mieux sa couleur qu'une police à champ de distance. Voici un agrandissement du même exemple de police de 48 pixels, réduite à 1/5 de sa taille :

![Polices réduites](images/font/scale_down.png)

Les polices à champ de distance doivent être générées à une taille cible suffisamment grande pour contenir les informations de distance permettant de représenter les courbes des glyphes. Voici la même police que ci-dessus, mais à une taille de 18 pixels et agrandie dix fois. Il apparaît clairement que cette taille est trop petite pour encoder les formes de cette police :

![Artefacts de champ de distance](images/font/df_artifacts.png)

Si vous ne souhaitez pas prendre en charge les ombres ou les contours, définissez leurs valeurs alpha respectives sur zéro. Sinon, les données d'ombre et de contour seront tout de même générées et occuperont inutilement de la mémoire.

## Cache de police {#font-cache}
Une ressource de police dans Defold produit deux éléments à l'exécution : une texture et les données de la police.

* Les données de la police se composent d'une liste d'entrées de glyphes, chacune contenant des informations de base sur le crénage et les données matricielles du glyphe.
* La texture est appelée en interne « texture du cache de glyphes » et sert à afficher le texte avec une police donnée.

À l'exécution, lors du rendu du texte, le moteur parcourt d'abord les glyphes à afficher pour vérifier lesquels sont disponibles dans le cache de texture. Chaque glyphe absent de la texture du cache de glyphes déclenche un transfert vers la texture à partir des données matricielles stockées dans les données de la police.

Chaque glyphe est placé en interne dans le cache en fonction de la ligne de base de la police, ce qui permet de calculer dans un shader ses coordonnées de texture locales au sein de la cellule de cache correspondante. Vous pouvez ainsi produire dynamiquement certains effets de texte, comme des dégradés ou des superpositions de textures. Le moteur expose au shader des mesures du cache par l'intermédiaire d'une constante spéciale appelée `texture_size_recip`, dont les composantes vectorielles contiennent les informations suivantes :

* `texture_size_recip.x` est l'inverse de la largeur du cache
* `texture_size_recip.y` est l'inverse de la hauteur du cache
* `texture_size_recip.z` est le rapport entre la largeur d'une cellule du cache et la largeur du cache
* `texture_size_recip.w` est le rapport entre la hauteur d'une cellule du cache et la hauteur du cache

Par exemple, pour générer un dégradé dans un shader de fragment, écrivez simplement :

`float horizontal_gradient = fract(var_texcoord0.y / texture_size_recip.w);`

Pour en savoir plus sur les variables uniformes des shaders, consultez le [manuel des shaders](/manuals/shader).

## Activation des polices générées à l'exécution {#enabling-runtime-fonts}

Il est possible de générer des polices SDF à l'exécution à partir de polices TrueType (`.ttf`) ou OpenType (`.otf`). La génération à l'exécution à partir de ressources `.otf` est prise en charge depuis Defold 1.13.2.
Cette approche peut réduire considérablement la taille du téléchargement et la consommation de mémoire à l'exécution d'un jeu Defold.
Le léger inconvénient est le caractère asynchrone de la génération de chaque glyphe.

* Activez la fonctionnalité en définissant `font.runtime_generation` dans game.project.

* Ajoutez un [manifeste d'application](/manuals/app-manifest) et activez l'option `Use full text layout system`.
Cela génère un moteur personnalisé dans lequel cette fonctionnalité est activée.

::: sidenote
Cette fonctionnalité est actuellement expérimentale, mais elle a vocation à devenir le flux de travail par défaut à l'avenir.
:::

::: important
Le paramètre `font.runtime_generation` affecte toutes les polices `.ttf` et `.otf` du projet.
:::


### Scripts de polices {#font-scripting}

#### Préremplissage du cache de glyphes {#prewarming-glyph-cache}

Pour faciliter leur utilisation, les polices générées à l'exécution prennent en charge le préremplissage du cache de glyphes.
Cela signifie que la police génère les glyphes indiqués dans sa propriété *Characters*.

::: sidenote
Si `All Chars` est sélectionné, aucun préremplissage n'a lieu, car cela annulerait l'intérêt de ne pas avoir à générer tous les glyphes en même temps.
:::

Si le champ `Characters` du fichier `.fontc` est renseigné, il sert de texte permettant de déterminer quels glyphes doivent être mis à jour dans le cache de glyphes.

Vous pouvez également mettre à jour manuellement le cache de glyphes en appelant `font.prewarm_text(font_collection, text, callback)`. Cette fonction fournit un callback pour vous avertir lorsque tous les glyphes manquants ont été ajoutés au cache de glyphes et que vous pouvez afficher le texte à l'écran sans risque.

### Ajout et suppression de polices dans une collection de polices {#addingremoving-fonts-to-a-font-collection}

Pour les polices générées à l'exécution, il est possible d'ajouter des polices (`.ttf`) à une collection de polices ou d'en supprimer.
Cela est utile lorsqu'une grande police a été répartie entre plusieurs fichiers pour différents jeux de caractères (par exemple, CJK)

::: important
L'ajout d'une police à une collection de polices ne charge ni n'affiche automatiquement tous ses glyphes.
:::

```lua
function init(self)
    -- Get the target font collection.
    self.font_collection = go.get("#label", "font")

    -- Get the first font assigned to the selected language collection.
    local language_collection = go.get("localization_japanese#label", "font")
    local font_info = font.get_info(language_collection)
    self.language_ttf_hash = font_info.fonts[1].path_hash

    -- Associate it with the target collection and increase its reference count.
    font.add_font(self.font_collection, self.language_ttf_hash)
end
```

```lua
function final(self)
    -- Remove the association and release the font reference.
    font.remove_font(self.font_collection, self.language_ttf_hash)
end
```

### Préparation des glyphes {#prewarming-glyphs}

Pour afficher correctement un texte avec une police générée à l'exécution, les glyphes doivent être résolus. La fonction `font.prewarm_text()` s'en charge pour vous.
Il s'agit d'une opération asynchrone : une fois celle-ci terminée et le callback reçu, vous pouvez afficher sans risque tout message contenant ces glyphes.

::: important
Si le cache de glyphes est plein, le glyphe le plus ancien du cache sera évincé.
:::

```lua
font.prewarm_text(self.font_collection, info.text, function (self, request_id, result, err)
    if result then
      print("PREWARMING OK!")
      go.set(self.label, "text", info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
