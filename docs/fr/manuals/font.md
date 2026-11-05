---
title: Manuel des polices dans Defold
brief: Ce manuel décrit la gestion des polices dans Defold et leur affichage à l'écran dans vos jeux.
---

# Fichiers de police {#font-files}

Les polices servent à afficher du texte dans les composants (component) Label et les nœuds de texte de l'interface graphique. Defold prend en charge plusieurs formats de fichiers de police :

- TrueType
- OpenType
- BMFont

L'ancien moteur de mise en page du texte et le moteur complet prennent tous deux en charge les contours TrueType et OpenType CFF1/CFF2, y compris la génération à l'exécution à partir de ressources `.ttf` et `.otf`.

Pour savoir comment appliquer des styles à des portions de texte et utiliser des liens et des sprites intégrés au texte, consultez le [manuel du balisage de texte enrichi](/manuals/font-richtext).

Pour les polices TrueType et OpenType, la propriété *Mode* sélectionne la manière dont les glyphes sont rendus :

- **Bitmap** utilise des images de glyphes rastérisées.
- **SDF** (champ de distance signé) stocke les distances aux bords des glyphes dans une texture, ce qui permet des changements d'échelle plus souples que Bitmap.
- **Vector** rend les faces des glyphes à partir de données de courbes pour qu'elles restent nettes lors des changements d'échelle. Les effets de contour et d'ombre utilisent toujours des données matricielles.

Les nouvelles ressources de police utilisent le mode **Vector** et la génération de glyphes **Dynamic**. Les ressources de police existantes conservent leur mode Bitmap ou SDF. Les sources BMFont utilisent toujours l'image matricielle fournie.

Le mode Vector nécessite la prise en charge graphique des textures `RGBA16F` et `R32UI` et n'est pas pris en charge sur OpenGL ES 2 ou WebGL 1. Utilisez des polices Bitmap ou SDF avec les matériaux correspondants pour cibler des adaptateurs graphiques non compatibles ; il n'existe aucun repli automatique de Vector vers SDF. Consultez [Polices vectorielles](#vector-fonts) pour la configuration.

## Polices prégénérées ou générées à l'exécution {#offline-or-runtime-fonts}

La propriété *Glyph Generation* sélectionne le moment où les données des glyphes de chaque police sont générées :

- **Static** génère les glyphes sélectionnés lors du build (hors ligne). *Characters* et *All Chars* contrôlent les glyphes inclus. Le fichier source `.ttf` ou `.otf` n'est pas inclus dans le bundle pour la génération à l'exécution.
- **Dynamic** inclut le fichier source `.ttf` ou `.otf` dans le bundle et génère les glyphes à la demande pendant l'exécution. *Prewarm Text* prépare les glyphes au chargement de la police. D'autres glyphes peuvent être générés ultérieurement selon les besoins.

Les polices SDF et Vector prennent en charge les deux choix. Les polices Bitmap et les sources BMFont utilisent la génération Static. Chaque ressource de police est configurée indépendamment ; un projet peut donc combiner des polices Static et Dynamic.

La génération dynamique peut réduire la taille du bundle et la mémoire utilisée à l'exécution, en particulier pour les polices comportant de grands jeux de caractères. Elle nécessite le système complet de mise en page du texte dans le moteur ; consultez [Activation des polices générées à l'exécution](#enabling-runtime-fonts).

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

Faites glisser la police que vous souhaitez utiliser dans le navigateur *Assets* et déposez-la à un emplacement approprié.

Définissez la propriété *Font* sur le fichier de police. Pour une source `.ttf` ou `.otf`, sélectionnez *Mode* et *Glyph Generation*, puis configurez les autres propriétés selon les besoins. Pour la génération Dynamic, effectuez également la [configuration des polices générées à l'exécution](#enabling-runtime-fonts).

![Propriétés de police avec le mode Vector et la génération de glyphes Dynamic](images/font/font_properties.png)

Pour les polices Vector, utilisez *Font Size* sur un composant Label ou un nœud de texte GUI pour modifier la taille du texte affiché. *Outline/Shadow Bitmap Size* contrôle la résolution des images matricielles des effets indépendamment de la taille affichée du texte.

Pour les polices Bitmap et SDF, définissez *Size* dans la ressource de police pour choisir la taille des glyphes générés. La taille des BMFont provient du fichier source `.fnt`. Pour modifier la taille affichée de ces polices, changez l'échelle du composant Label ou du nœud de texte GUI.

## Propriétés {#properties}

*Font*
: Le fichier TTF, OTF ou *`.fnt`* à utiliser pour générer les données de la police.

*Material*
: Le matériau à utiliser pour le rendu de cette police. Il doit correspondre au mode de la police ; consultez [Matériaux des polices](#font-materials).

*Mode*
: La technique de rendu d'une source `.ttf` ou `.otf` : **Bitmap**, **SDF** ou **Vector**. Elle remplace l'ancienne propriété *Output Format*. Cette propriété n'est pas affichée pour les sources BMFont.

*Glyph Generation*
: **Static** génère les données des glyphes lors du build. **Dynamic** les génère à l'exécution et nécessite le [système complet de mise en page du texte](#enabling-runtime-fonts). Cette propriété est disponible pour les polices SDF et Vector. En mode Bitmap, elle est fixée à Static, et elle n'est pas affichée pour les sources BMFont.

*Render Mode*
: La disposition des couches des polices Bitmap générées. Cette propriété n'est affichée qu'en mode Bitmap pour les sources `.ttf` et `.otf`. Pour les sources SDF, Vector et BMFont, Defold sélectionne automatiquement la disposition des couches.

  - **Single Layer** produit un seul quadrilatère pour chaque caractère.
  - **Multi Layer** produit des quadrilatères distincts pour la forme du glyphe, le contour et l'ombre. Les couches sont rendues de l'arrière vers l'avant, ce qui empêche un caractère de masquer ceux déjà rendus si le contour est plus large que la distance entre les glyphes. Ce mode permet également les décalages d'ombre des propriétés *Shadow X/Y*.

*Size*
: La taille des glyphes en pixels utilisée pour générer les données de police Bitmap ou SDF. Pour les sources BMFont, la taille est lue depuis le fichier `.fnt` et n'est pas modifiable ici.

*Outline/Shadow Bitmap Size*
: En mode Vector, remplace *Size*. Cette propriété contrôle la résolution matricielle des effets de contour et d'ombre activés, pour les générations Static et Dynamic. Elle est désactivée lorsqu'aucun de ces effets n'est activé, car les faces des glyphes utilisent des données de courbes. Modifier *Font Size* d'un Label ou d'un nœud de texte GUI ne change pas cette résolution matricielle partagée.

*Antialias*
: Indique s'il faut anticréneler les glyphes lors de la génération des données de police Bitmap. Désactivez cette option pour un rendu au pixel près. Cette propriété n'est affichée qu'en mode Bitmap pour les sources `.ttf` et `.otf`.

*Alpha*
: La transparence du glyphe. De 0.0 à 1.0, où 0.0 signifie transparent et 1.0 opaque.

*Outline Alpha*
: La transparence du contour généré. De 0.0 à 1.0.

*Outline Width*
: La largeur du contour généré en pixels. Définissez cette valeur sur 0 pour ne pas avoir de contour.

*Shadow Alpha*
: La transparence de l'ombre générée. De 0.0 à 1.0.

::: sidenote
Le shader de police Bitmap intégré prend en charge les ombres dans les modes de rendu *Single Layer* et *Multi Layer*. Pour les polices Bitmap générées en *Single Layer* qui n'ont pas besoin d'ombres, un matériau personnalisé peut utiliser `/builtins/fonts/font-singlelayer.fp`. Les polices SDF et Vector nécessitent des shaders correspondant à leur mode ; consultez [Matériaux des polices](#font-materials).
:::

*Shadow Blur*
: La quantité de flou appliquée à l'ombre générée. Définissez-la sur 0 pour une ombre nette.

*Shadow X/Y*
: Le décalage horizontal et vertical, en pixels, de l'ombre générée. Pour les polices Bitmap générées, utilisez le mode de rendu *Multi Layer* pour appliquer ces décalages. Defold sélectionne automatiquement les couches appropriées pour les polices SDF et Vector.

*Characters*
: Pour la génération Static, les caractères à inclure dans la police compilée. Par défaut, ce champ contient les caractères ASCII imprimables (codes 32-126). Ajoutez ou supprimez des caractères pour contrôler les glyphes disponibles à l'exécution.

*Prewarm Text*
: Pour la génération Dynamic, remplace *Characters*. Le texte sert à générer les glyphes et à préremplir le cache lors du chargement de la police. Il ne restreint pas les caractères pouvant être générés plus tard. Vous pouvez aussi précharger du texte depuis un script avec [`font.prewarm_text()`](/ref/font/#font.prewarm_text).

::: sidenote
Les caractères ASCII imprimables sont :
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Pour la génération Static, inclut tous les glyphes disponibles dans la source au lieu de limiter la police à *Characters*. Cette propriété est masquée pour les polices Dynamic.

*Cache Width/Height*
: Limite la taille de l'image matricielle du cache de glyphes utilisée par les polices Bitmap et SDF ainsi que par les effets de contour et d'ombre Vector. Lorsque le moteur affiche du texte, il recherche le glyphe dans cette image. Si le glyphe n'y figure pas, il est ajouté au cache avant le rendu. Si l'image matricielle du cache est trop petite pour contenir tous les glyphes que le moteur doit afficher, une erreur est signalée (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Si la valeur est définie sur 0, la taille du cache est déterminée automatiquement et peut augmenter jusqu'à 2048x4096 au maximum.

## Matériaux des polices {#font-materials}

Utilisez un matériau correspondant au mode de la police. Le *Material* de la ressource de police est utilisé par les nœuds de texte GUI. Les composants Label ont une propriété *Material* distincte qui doit également correspondre à la police :

| Mode ou source de police | Matériau de police pour le texte GUI | Matériau du composant Label |
| --- | --- | --- |
| Bitmap | `/builtins/fonts/font.material` | `/builtins/fonts/label.material` |
| SDF | `/builtins/fonts/font-df.material` | `/builtins/fonts/label-df.material` |
| Vector | `/builtins/fonts/font-vector.material` | `/builtins/fonts/label-vector.material` |
| BMFont (`.fnt`) | `/builtins/fonts/font-fnt.material` | `/builtins/fonts/label-fnt.material` |

Changer *Mode* dans l'éditeur de police sélectionne le matériau intégré Bitmap, SDF ou Vector correspondant lorsqu'un de ces matériaux est déjà affecté à la police. Les matériaux personnalisés ne sont pas remplacés automatiquement. Vérifiez également la propriété *Material* des composants Label utilisant cette police.

## Polices vectorielles {#vector-fonts}

Les polices vectorielles rendent les faces des glyphes à partir de courbes pour qu'elles restent nettes lorsque la taille affichée du texte change. Pour configurer une police qui génère ses glyphes à l'exécution :

1. Créez une ressource `.font`, par exemple `/fonts/ui.font`, et sélectionnez une source TrueType ou OpenType dans sa propriété *Font*. La police intégrée `/builtins/fonts/vera_mo_bd.ttf` convient au texte ordinaire.
2. Définissez *Mode* sur **Vector**, *Glyph Generation* sur **Dynamic** et *Material* sur `/builtins/fonts/font-vector.material`. Ce sont les valeurs par défaut des nouvelles ressources de police.
3. Activez **Use full text layout system** dans un manifeste d'application affecté à votre projet. Suivez [Activation des polices générées à l'exécution](#enabling-runtime-fonts) pour configurer le moteur personnalisé.
4. Activez [Shader ▸ Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) dans *game.project*.
5. Affectez la police à un [Label](/manuals/label/) ou ajoutez-la aux *Fonts* d'une scène GUI et sélectionnez-la sur un [nœud de texte](/manuals/gui-text/). Pour un Label, définissez également le *Material* du composant sur `/builtins/fonts/label-vector.material`. Réglez *Font Size* du composant ou du nœud à la taille d'affichage souhaitée.

Les faces des glyphes Vector utilisent des textures de courbes, mais les contours et ombres activés génèrent toujours des données matricielles SDF et consomment de la mémoire de texture dans le cache de glyphes. *Outline/Shadow Bitmap Size* définit cette résolution matricielle indépendamment de *Font Size* du Label ou du nœud de texte GUI. Définissez *Outline Alpha* et *Shadow Alpha* sur `0` si ces effets ne sont pas nécessaires afin d'éviter de générer leurs données matricielles.

### Émojis en couleur {#color-emoji}

Les polices Vector peuvent rendre les émojis en couleur COLRv1, y compris les couleurs de palette et les dégradés linéaires et radiaux. Les modes Bitmap et SDF ne rendent pas les couleurs COLRv1. Utilisez la configuration Dynamic Vector ci-dessus, puis ajoutez une police d'émojis COLRv1 comme police de repli à la collection de polices. Le texte ordinaire continue d'utiliser la police d'origine.

Par exemple, copiez la version COLRv1 de la [police Noto Color Emoji](https://github.com/google/fonts/blob/main/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf) dans votre projet sous `/fonts/NotoColorEmoji-Regular.ttf`. Choisissez bien la version COLRv1 : d'autres polices d'émojis peuvent utiliser un format de couleur différent même lorsque leur nom de fichier se termine par `.ttf`.

Ajoutez `/fonts/NotoColorEmoji-Regular.ttf` à **Project ▸ Custom Resources** dans *game.project*. Sans autre ressource personnalisée, le paramètre est :

```ini
[project]
custom_resources = /fonts/NotoColorEmoji-Regular.ttf
```

Un chemin de police écrit en Lua ne provoque pas l'inclusion du fichier de police dans le bundle. [Custom Resources](/manuals/project-settings/#custom-resources) rend cette police source accessible à [`font.add_font()`](/ref/font/#font.add_font), qui la charge via le système de ressources. Passez le chemin de la police source sous forme de chaîne pour la charger depuis le bundle.

Ajoutez la police de repli une seule fois par ressource de police partagée. Le changement affecte chaque Label et nœud de texte GUI utilisant cette police, et l'ajout de la même police de repli deux fois déclenche une erreur. Si vous utilisez à la fois l'[exemple de Label](/manuals/label/#vector-fonts-and-color-emoji) et l'[exemple GUI](/manuals/gui-text/#vector-fonts-and-color-emoji) avec le même `.font`, coordonnez l'initialisation pour ajouter la police de repli une fois avant que l'un des exemples prépare ou affiche du texte. Les exemples préchargent le texte complet après l'ajout de la police de repli et l'affichent lorsque le callback réussit.

## Polices à champ de distance {#distance-field-fonts}

Les polices à champ de distance stockent dans la texture la distance au bord du glyphe à la place de données matricielles. Lorsque le moteur affiche la police, un shader spécial est nécessaire pour interpréter les données de distance et les utiliser pour dessiner le glyphe. Les polices à champ de distance consomment davantage de ressources que les polices matricielles, mais offrent une plus grande souplesse de redimensionnement.

![Police à champ de distance](images/font/df_font.png)

Sélectionnez **SDF** dans *Mode* et choisissez **Static** ou **Dynamic** dans *Glyph Generation*. Utilisez *`/builtins/fonts/font-df.material`* pour la police et *`/builtins/fonts/label-df.material`* pour les composants Label, ou des matériaux personnalisés qui traitent les données de champ de distance.

## Polices matricielles BMFont {#bitmap-bmfonts}

Outre les images matricielles générées, Defold prend en charge les polices matricielles prégénérées au format « BMFont ». Ces polices se composent d'une planche de glyphes PNG contenant tous les glyphes. Un fichier *`.fnt`* contient en complément la position de chaque glyphe sur la planche, ainsi que des informations sur la taille et le crénage. (Notez que Defold ne prend pas en charge la version XML du format *`.fnt`* utilisée par Phaser et certains autres outils.)

Ces types de polices n'améliorent pas les performances par rapport aux polices matricielles générées à partir de fichiers de police TrueType ou OpenType, mais peuvent contenir directement dans l'image des graphismes, des couleurs et des ombres de votre choix.

Ajoutez les fichiers *`.fnt`* et *`.png`* générés à votre projet Defold. Ces fichiers doivent se trouver dans le même dossier. Créez un fichier de police et définissez la propriété *Font* sur le fichier *`.fnt`*. Defold utilise l'image matricielle fournie et lit sa taille depuis le fichier `.fnt`. *Mode* et *Glyph Generation* ne sont pas affichés pour les sources BMFont.

::: sidenote
Pour créer une BMFont, vous devez utiliser un outil capable de générer les fichiers appropriés. Plusieurs possibilités existent :

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), un outil réservé à Windows fourni par AngelCode.
* [Shoebox](http://renderhjs.net/shoebox/), une application gratuite fondée sur Adobe Air pour Windows et macOS.
* [Hiero](https://libgdx.com/wiki/tools/hiero), un outil libre fondé sur Java.
* [Glyph Designer](https://71squared.com/glyphdesigner), un outil commercial pour macOS de 71 Squared.
* [bmGlyph](https://www.bmglyph.com), un outil commercial pour macOS de Sovapps.
:::

![BMfont](images/font/bm_font.png)

Définissez le *Material* de la police sur *`/builtins/fonts/font-fnt.material`*. Pour les composants Label, utilisez *`/builtins/fonts/label-fnt.material`*.

## Artefacts et bonnes pratiques {#artifacts-and-best-practices}

En général, les polices matricielles conviennent le mieux lorsque la police est affichée sans changement d'échelle. Leur rendu à l'écran est plus rapide que celui des polices à champ de distance.

Les polices à champ de distance supportent très bien l'agrandissement. Les polices matricielles, en revanche, sont de simples images composées de pixels : leurs pixels grossissent lorsque la police est agrandie, ce qui produit des artefacts en blocs. Voici un exemple avec une police de 48 pixels, agrandie quatre fois.

![Polices agrandies](images/font/scale_up.png)

Lors d'une réduction, le GPU peut réduire et anticréneler les textures matricielles efficacement et avec un bon résultat visuel. Une police matricielle conserve mieux sa couleur qu'une police à champ de distance. Voici un agrandissement du même exemple de police de 48 pixels, réduite à 1/5 de sa taille :

![Polices réduites](images/font/scale_down.png)

Les polices à champ de distance doivent être générées à une taille cible suffisamment grande pour contenir les informations de distance permettant de représenter les courbes des glyphes. Voici la même police que ci-dessus, mais à une taille de 18 pixels et agrandie dix fois. Il apparaît clairement que cette taille est trop petite pour encoder les formes de cette police :

![Artefacts de champ de distance](images/font/df_artifacts.png)

Si vous ne souhaitez pas prendre en charge les ombres ou les contours, définissez leurs valeurs alpha respectives sur zéro. Sinon, les données d'ombre et de contour seront tout de même générées et occuperont inutilement de la mémoire. En mode Vector, désactiver les deux effets évite de générer leurs données matricielles ; les faces des glyphes continuent d'utiliser les données de courbes.

## Cache de police {#font-cache}
Les ressources de police Bitmap et SDF utilisent une texture de cache de glyphes et des données de police à l'exécution. Les polices Vector stockent les faces des glyphes sous forme de données de courbes et utilisent un cache matriciel pour les effets de contour et d'ombre activés. La disposition de texture décrite ci-dessous s'applique aux polices Bitmap et SDF.

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

La génération à l'exécution se configure pour chaque ressource de police :

1. Ouvrez la ressource `.font` et sélectionnez une source TrueType (`.ttf`) ou OpenType (`.otf`).
2. Définissez *Mode* sur **SDF** ou **Vector** et *Glyph Generation* sur **Dynamic**.
3. Choisissez les [matériaux de police et de Label](#font-materials) correspondants.
4. Ajoutez un [manifeste d'application](/manuals/app-manifest), affectez-le à *Native Extensions ▸ App Manifest* dans *game.project* et activez **Use full text layout system**. Cela génère un moteur personnalisé avec la génération de polices à l'exécution et le système complet de mise en page du texte.
5. Définissez *Prewarm Text* avec le texte à afficher peu après le chargement de la police. Pour le texte nécessaire plus tard, utilisez [`font.prewarm_text()`](/ref/font/#font.prewarm_text) et attendez son callback avant de l'afficher.

Les nouvelles ressources de police utilisent déjà le mode Vector et la génération Dynamic, mais nécessitent tout de même la configuration du manifeste d'application ci-dessus.

### Scripts de polices {#font-scripting}

#### Préremplissage du cache de glyphes {#prewarming-glyph-cache}

Les polices Dynamic génèrent les glyphes nécessaires à *Prewarm Text* au chargement de la police. Le champ est interprété comme du texte à mettre en page ; le cache est donc préparé pour les glyphes dont ce texte a besoin. *All Chars* n'est pas disponible pour les polices Dynamic.

Vous pouvez également appeler `font.prewarm_text(font_collection, text, callback)` pour une police Dynamic. Le callback vous indique quand tous les glyphes manquants ont été ajoutés au cache et que vous pouvez afficher le texte. Cette fonction ne peut pas être utilisée avec les polices Static.

### Ajout et suppression de polices dans une collection de polices {#addingremoving-fonts-to-a-font-collection}

Pour les polices Dynamic, il est possible d'ajouter des polices source (`.ttf` ou `.otf`) à une collection de polices ou d'en supprimer.
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
