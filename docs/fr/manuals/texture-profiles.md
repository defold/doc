---
title: Profils de texture dans Defold
brief:  Defold prend en charge le traitement automatique des textures et la compression des données d'image. Ce manuel décrit les fonctionnalités disponibles.
---

# Profils de texture {#texture-profiles}

Defold prend en charge le traitement automatique des textures et la compression des données d'image (dans les *Atlas*, *Tile sources*, *Cubemaps* et les textures autonomes utilisées pour les modèles, les interfaces graphiques, etc.).

Il existe deux types de compression : la compression logicielle d'image et la compression matérielle de texture.

1. La compression logicielle (comme PNG et JPEG) réduit la taille de stockage des ressources d'image. Cela réduit la taille du bundle final. Toutefois, les fichiers image doivent être décompressés lors de leur chargement en mémoire : même si une image occupe peu de place sur le disque, son empreinte mémoire peut être importante.

2. La compression matérielle de texture réduit également la taille de stockage des ressources d'image. Mais, contrairement à la compression logicielle, elle réduit l'empreinte mémoire des textures. En effet, le matériel graphique peut gérer directement les textures compressées sans avoir à les décompresser au préalable.

Le traitement des textures se configure au moyen d'un profil de texture spécifique. Dans ce fichier, vous créez des _profils_ qui indiquent le ou les formats compressés et le type à utiliser lors de la création de bundles pour une plateforme donnée. Les _profils_ sont ensuite associés à des _motifs de chemin_ correspondant aux fichiers, ce qui permet de contrôler précisément quels fichiers du projet doivent être compressés et de quelle manière.

Toutes les méthodes de compression matérielle de texture disponibles étant avec perte, des artefacts apparaîtront dans vos données de texture. Ces artefacts dépendent fortement de l'aspect de vos images sources et de la méthode de compression utilisée. Vous devriez tester vos images sources et expérimenter pour obtenir les meilleurs résultats. Google peut vous y aider.

Vous pouvez sélectionner la compression logicielle d'image appliquée aux données de texture finales (compressées ou brutes) dans les archives du bundle. Defold prend en charge les formats de compression [Basis Universal](https://github.com/BinomialLLC/basis_universal) et [ASTC](https://www.khronos.org/opengl/wiki/ASTC_Texture_Compression).

::: sidenote
La compression est une opération coûteuse en ressources et en temps, qui peut entraîner des durées de build _très_ longues selon le nombre d'images de texture à compresser, les formats de texture choisis et le type de compression logicielle.
:::

### Basis Universal {#basis-universal}

Basis Universal (ou BasisU en abrégé) compresse l'image dans un format intermédiaire, transcodé à l'exécution vers un format matériel adapté au GPU de l'appareil utilisé. Le format Basis Universal offre une grande qualité, mais reste un format avec perte.
Toutes les images sont également compressées avec LZ4 pour réduire davantage la taille des fichiers lors de leur stockage dans l'archive du jeu.

### ASTC {#astc}

ASTC est un format de compression de texture souple et efficace, développé par ARM et normalisé par le Khronos Group. Il offre un large choix de tailles de bloc et de débits binaires, permettant aux développeurs d'équilibrer efficacement la qualité de l'image et l'utilisation de la mémoire. ASTC prend en charge différentes tailles de bloc, de 4×4 à 12×12 texels, correspondant à des débits binaires allant de 8 bits par texel à 0,89 bit par texel. Cette souplesse permet de contrôler précisément le compromis entre la qualité des textures et les besoins de stockage.

ASTC prend en charge différentes tailles de bloc, de 4×4 à 12×12 texels, correspondant à des débits binaires allant de 8 bits par texel à 0,89 bit par texel. Cette souplesse permet de contrôler précisément le compromis entre la qualité des textures et les besoins de stockage. Le tableau suivant présente les tailles de bloc prises en charge et les débits binaires correspondants :

| Taille de bloc (largeur x hauteur) | Bits par pixel |
| --------------------------- | -------------- |
| 4x4                         | 8.00           |
| 5x4                         | 6.40           |
| 5x5                         | 5.12           |
| 6x5                         | 4.27           |
| 6x6                         | 3.56           |
| 8x5                         | 3.20           |
| 8x6                         | 2.67           |
| 10x5                        | 2.56           |
| 10x6                        | 2.13           |
| 8x8                         | 2.00           |
| 10x8                        | 1.60           |
| 10x10                       | 1.28           |
| 12x10                       | 1.07           |
| 12x12                       | 0.89           |


#### Appareils pris en charge {#supported-devices}

Bien qu'ASTC donne d'excellents résultats, toutes les cartes graphiques ne le prennent pas en charge. Voici une courte liste des appareils compatibles par fabricant :

| Fabricant du GPU   | Prise en charge                                                       |
| ------------------ | --------------------------------------------------------------------- |
| ARM (Mali)         | Tous les GPU ARM Mali prenant en charge OpenGL ES 3.2 ou Vulkan prennent en charge ASTC. |
| Qualcomm (Adreno)  | Les GPU Adreno prenant en charge OpenGL ES 3.2 ou Vulkan prennent en charge ASTC. |
| Apple              | Les GPU Apple prennent en charge ASTC depuis la puce A8.              |
| NVIDIA             | La prise en charge d'ASTC concerne surtout les GPU mobiles (par exemple, les puces basées sur Tegra). |
| AMD (Radeon)       | Les GPU AMD prenant en charge Vulkan prennent généralement en charge ASTC par voie logicielle. |
| Intel (intégré)    | Les GPU Intel modernes prennent en charge ASTC par voie logicielle.   |

## Profils de texture {#texture-profiles}

Chaque projet contient un fichier *.texture_profiles* spécifique qui définit la configuration utilisée pour compresser les textures. Par défaut, il s'agit du fichier *builtins/graphics/default.texture_profiles*. Sa configuration associe chaque ressource de texture à un profil utilisant RGBA sans compression matérielle de texture, avec la compression de fichier ZLib par défaut.

Pour ajouter la compression de texture :

- Sélectionnez <kbd>File ▸ New...</kbd> et choisissez *Texture Profiles* pour créer un fichier de profils de texture. (Vous pouvez aussi copier *default.texture_profiles* à un emplacement en dehors de *builtins*)
- Choisissez un nom et un emplacement pour le nouveau fichier.
- Modifiez l'entrée *texture_profiles* dans *game.project* pour qu'elle pointe vers le nouveau fichier.
- Ouvrez le fichier *.texture_profiles* et configurez-le selon vos besoins.

![Nouveau fichier de profils](images/texture_profiles/texture_profiles_new_file.png)

![Définition du profil de texture](images/texture_profiles/texture_profiles_game_project.png)

Vous pouvez activer ou désactiver l'utilisation des profils de texture dans les préférences de l'éditeur. Sélectionnez <kbd>File ▸ Preferences...</kbd>. L'onglet *General* contient la case à cocher *Enable texture profiles*.

![Préférences des profils de texture](images/texture_profiles/texture_profiles_preferences.png)

## Paramètres de chemin {#path-settings}

La section *Path Settings* du fichier de profils de texture contient une liste de motifs de chemin et le profil (*profile*) à utiliser pour traiter les ressources dont le chemin correspond. Les chemins sont exprimés sous forme de motifs « Ant Glob » (consultez la [documentation](http://ant.apache.org/manual/dirtasks.html#patterns) pour plus de détails). Les motifs peuvent utiliser les caractères génériques suivants :

`*`
: Correspond à zéro ou plusieurs caractères. Par exemple, `sprite*.png` correspond aux fichiers *`sprite.png`*, *`sprite1.png`* et *`sprite_with_a_long_name.png`*.

`?`
: Correspond à exactement un caractère. Par exemple, `sprite?.png` correspond aux fichiers *sprite1.png*, *`spriteA.png`*, mais pas à *`sprite.png`* ni à *`sprite_with_a_long_name.png`*.

`**`
: Correspond à une arborescence complète de répertoires ou, lorsqu'il est utilisé comme nom de répertoire, à zéro ou plusieurs répertoires. Par exemple, `/gui/**` correspond à tous les fichiers du répertoire */gui* et de tous ses sous-répertoires.

![Chemins](images/texture_profiles/texture_profiles_paths.png)

Cet exemple contient deux motifs de chemin et les profils correspondants.

`/gui/**/*.atlas`
: Tous les fichiers *.atlas* du répertoire *`/gui`* ou de l'un de ses sous-répertoires seront traités selon le profil « gui_atlas ».

`/**/*.atlas`
: Tous les fichiers *.atlas*, où qu'ils se trouvent dans le projet, seront traités selon le profil « atlas ».

Notez que le chemin le plus générique est placé en dernier. L'algorithme de correspondance parcourt la liste de haut en bas. La première occurrence qui correspond au chemin de la ressource est utilisée. Une expression de chemin correspondante située plus bas dans la liste ne remplace jamais la première correspondance. Si les chemins avaient été placés dans l'ordre inverse, tous les atlas auraient été traités avec le profil « atlas », même ceux du répertoire *`/gui`*.

Les ressources de texture qui _ne correspondent à aucun_ chemin du fichier de profils seront compilées et redimensionnées à la puissance de 2 la plus proche, mais resteront intactes par ailleurs.

## Profils {#profiles}

La section *profiles* du fichier de profils de texture contient une liste de profils nommés. Chaque profil contient une ou plusieurs plateformes (*platforms*), chacune étant décrite par une liste de propriétés.

![Profils](images/texture_profiles/texture_profiles_profiles.png)

*Platforms*
: Spécifie une plateforme correspondante. `OS_ID_GENERIC` correspond à toutes les plateformes, `OS_ID_WINDOWS` aux bundles ciblant Windows, `OS_ID_IOS` aux bundles iOS, et ainsi de suite. Notez que si `OS_ID_GENERIC` est spécifié, il sera inclus pour toutes les plateformes.

::: important
Si deux [paramètres de chemin](#path-settings) correspondent au même fichier et que les chemins utilisent des profils différents avec des plateformes différentes, **les deux** profils seront utilisés et **deux** textures seront générées.
:::

*Formats*
: Un ou plusieurs formats de texture à générer. Si plusieurs formats sont spécifiés, des textures sont générées dans chaque format et incluses dans le bundle. Le moteur sélectionne les textures dont le format est pris en charge par la plateforme d'exécution.

*Mipmaps*
: Si cette case est cochée, des mipmaps sont générées pour la plateforme. Décochée par défaut.

*Premultiply alpha*
: Si cette case est cochée, l'alpha est prémultiplié dans les données de texture. Cochée par défaut.

*Max Texture Size*
: Si cette propriété est définie sur une valeur non nulle, les dimensions des textures en pixels sont limitées au nombre spécifié. Toute texture dont la largeur ou la hauteur dépasse la valeur spécifiée sera réduite.

Chaque entrée *Formats* ajoutée à un profil possède les propriétés suivantes :

*Format*
: Le format à utiliser pour encoder la texture. Vous trouverez ci-dessous tous les formats de texture disponibles.

*Compressor*
: Le compresseur à utiliser pour encoder la texture.

*Compressor Preset*
: Sélectionne un préréglage de compression à utiliser pour encoder l'image compressée résultante. Chaque préréglage de compresseur est propre au compresseur et ses paramètres dépendent du compresseur lui-même. Pour simplifier ces paramètres, les préréglages de compression actuels se déclinent en quatre niveaux :

| Préréglage | Remarque                                     |
| --------- | --------------------------------------------- |
| `LOW`     | Compression la plus rapide. Faible qualité d'image |
| `MEDIUM`  | Compression par défaut. Meilleure qualité d'image |
| `HIGH`    | Compression la plus lente. Taille de fichier réduite |
| `HIGHEST` | Compression lente. Taille de fichier minimale |

Notez que le compresseur `uncompressed` ne possède qu'un seul préréglage, appelé `uncompressed`, qui signifie qu'aucune compression ne sera appliquée aux textures.
Pour consulter la liste des compresseurs disponibles, reportez-vous à [Compresseurs](#compressors)

## Formats de texture {#texture-formats}

Les textures destinées au matériel graphique peuvent être traitées sous forme de données non compressées ou compressées *avec perte*, avec différents nombres de canaux et différentes profondeurs de bits. Une compression matérielle fixe signifie que l'image résultante aura une taille fixe, quel que soit son contenu. La perte de qualité lors de la compression dépend donc du contenu de la texture d'origine.

Le transcodage de la compression Basis Universal dépendant des capacités du GPU de l'appareil, les formats recommandés avec cette compression sont les formats génériques tels que :
`TEXTURE_FORMAT_RGB`, `TEXTURE_FORMAT_RGBA`, `TEXTURE_FORMAT_RGB_16BPP`, `TEXTURE_FORMAT_RGBA_16BPP`, `TEXTURE_FORMAT_LUMINANCE` et `TEXTURE_FORMAT_LUMINANCE_ALPHA`.

Le transcodeur Basis Universal prend en charge de nombreux formats de sortie, comme `ASTC4x4`, `BCx`, `ETC2`, `ETC1` et `PVRTC1`.

Les formats de compression avec perte suivants sont actuellement pris en charge :

| Format                            | Compression | Détails  |
| --------------------------------- | ----------- | -------------------------------- |
| `TEXTURE_FORMAT_RGB`              | aucune      | Couleur sur 3 canaux. L'alpha est supprimé |
| `TEXTURE_FORMAT_RGBA`             | aucune      | Couleur sur 3 canaux et alpha complet. |
| `TEXTURE_FORMAT_RGB_16BPP`        | aucune      | Couleur sur 3 canaux. 5+6+5 bits. |
| `TEXTURE_FORMAT_RGBA_16BPP`       | aucune      | Couleur sur 3 canaux et alpha complet. 4+4+4+4 bits. |
| `TEXTURE_FORMAT_LUMINANCE`        | aucune      | Niveaux de gris sur 1 canal, sans alpha. Les canaux RGB sont multipliés pour n'en former qu'un. L'alpha est supprimé. |
| `TEXTURE_FORMAT_LUMINANCE_ALPHA`  | aucune      | Niveaux de gris sur 1 canal et alpha complet. Les canaux RGB sont multipliés pour n'en former qu'un. |

Pour ASTC, le nombre de canaux est toujours de 4 (RGB + alpha), et le format lui-même définit la taille des blocs de compression.
Notez que ces formats ne sont compatibles qu'avec un compresseur ASTC : toute autre combinaison produit une erreur de build.

`TEXTURE_FORMAT_RGBA_ASTC_4X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X5`
`TEXTURE_FORMAT_RGBA_ASTC_8X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X5`
`TEXTURE_FORMAT_RGBA_ASTC_10X6`
`TEXTURE_FORMAT_RGBA_ASTC_10X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X12`


## Compresseurs {#compressors}

Les compresseurs de texture suivants sont pris en charge par défaut. Les données sont décompressées lorsque le fichier de texture est chargé en mémoire.

| Nom                               | Formats                   | Remarque                                                                                      |
| --------------------------------- | ------------------------- | --------------------------------------------------------------------------------------------- |
| `Uncompressed`                    | Tous les formats          | Aucune compression ne sera appliquée. Par défaut.                                             |
| `BasisU`                          | Tous les formats RGB/RGBA | Compression Basis Universal avec perte de grande qualité. Un niveau de qualité inférieur réduit la taille. |
| `ASTC`                            | Tous les formats ASTC     | Compression ASTC avec perte. Un niveau de qualité inférieur réduit la taille.                  |

::: sidenote
Defold prend en charge les compresseurs installables dans la chaîne de compression des textures. Cela permet d'implémenter un algorithme de compression de texture dans une extension, comme WEBP ou une solution entièrement personnalisée.
:::

## Image d'exemple {#example-image}

Voici un exemple pour mieux comprendre le résultat.
Notez que la qualité de l'image, le temps de compression et la taille après compression dépendent toujours de l'image d'entrée et peuvent varier.

Image de base (1024x512) :
![Nouveau fichier de profils](images/texture_profiles/kodim03_pow2.png)

### Temps de compression {#compression-times}

| Préréglage | Temps de compression | Temps relatif |
| --------- | ---------------- | ------------- |
| `LOW`     | 0m0.143s         | 0.5x            |
| `MEDIUM`  | 0m0.294s         | 1.0x            |
| `HIGH`    | 0m1.764s         | 6.0x            |
| `HIGHEST` | 0m1.109s         | 3.8x            |

### Perte de signal {#signal-loss}

La comparaison est effectuée avec l'outil `basisu` (en mesurant le PSNR)
100 dB signifie qu'il n'y a aucune perte de signal (c'est-à-dire que l'image est identique à l'originale).

| Préréglage | Signal                                          |
| --------- | ------------------------------------------------ |
| `LOW`     | Max:  34 Mean: 0.470 RMS: 1.088 PSNR: 47.399 dB |
| `MEDIUM`  | Max:  35 Mean: 0.439 RMS: 1.061 PSNR: 47.620 dB |
| `HIGH`    | Max:  37 Mean: 0.898 RMS: 1.606 PSNR: 44.018 dB |
| `HIGHEST` | Max:  51 Mean: 1.298 RMS: 2.478 PSNR: 40.249 dB |

### Tailles des fichiers compressés {#compression-file-sizes}

La taille du fichier d'origine est de 1572882 octets.

| Préréglage | Tailles des fichiers | Rapport |
| --------- | ---------- | ------- |
| `LOW`     | 357225     | 22.71 %  |
| `MEDIUM`  | 365548     | 23.24 %  |
| `HIGH`    | 277186     | 17.62 %  |
| `HIGHEST` | 254380     | 16.17 %  |


### Qualité d'image {#image-quality}

Voici les images obtenues (récupérées à partir de l'encodage ASTC avec l'outil `basisu`)

`LOW`
![Préréglage de compression faible](images/texture_profiles/kodim03_pow2.fast.png)

`MEDIUM`
![Préréglage de compression moyen](images/texture_profiles/kodim03_pow2.normal.png)

`HIGH`
![Préréglage de compression élevé](images/texture_profiles/kodim03_pow2.high.png)

`HIGHEST`
![Meilleur préréglage de compression](images/texture_profiles/kodim03_pow2.best.png)
