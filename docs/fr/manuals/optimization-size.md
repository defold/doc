---
title: Optimiser la taille d'un jeu Defold
brief: Ce manuel décrit comment optimiser la taille d'un jeu Defold.
---

# Optimiser la taille d'un jeu {#optimizing-game-size}

La taille de votre jeu peut être un facteur déterminant pour son succès sur les plateformes web et mobiles, tandis qu'elle a moins d'importance sur les ordinateurs et les consoles, où l'espace disque est peu coûteux et souvent abondant.

### iOS et Android {#ios-and-android}
Apple et Google ont défini des limites de taille des applications pour les téléchargements sur les réseaux mobiles (par opposition aux téléchargements en Wi-Fi). Sur Android, cette limite est de 200 Mo pour les applications publiées sous forme de [bundles d'application](https://developer.android.com/guide/app-bundle#size_restrictions). Sur iOS, les utilisateurs reçoivent un avertissement si l'application dépasse 200 Mo, mais peuvent tout de même la télécharger.

::: sidenote
Une étude de 2017 a montré que « chaque augmentation de 6 Mo de la taille d'un APK entraîne une baisse de 1 % du taux de conversion en installations. » ([source](https://medium.com/googleplaydev/shrinking-apks-growing-installs-5d3fcba23ce2))
:::

### HTML5 {#html5}
Poki et de nombreuses autres plateformes de jeux web recommandent que le téléchargement initial ne dépasse pas 5 Mo.

Facebook recommande qu'un jeu Facebook Instant Game démarre en moins de 5 secondes et, de préférence, en moins de 3 secondes. La taille réelle de l'application que cela implique n'est pas clairement définie, mais il s'agit de tailles pouvant aller jusqu'à 20 Mo.

Les publicités jouables sont généralement limitées à une taille comprise entre 2 et 5 Mo selon le réseau publicitaire.

## Stratégies d'optimisation de la taille {#size-optimization-strategies}
Vous pouvez optimiser la taille de l'application de deux façons : en réduisant la taille du moteur et/ou celle des ressources du jeu.

Pour mieux comprendre ce qui contribue à la taille de votre application, vous pouvez [générer un rapport de build](/manuals/bundling/#build-reports) lors de la création du bundle. Les sons et les éléments graphiques représentent très souvent la majeure partie de la taille d'un jeu.

::: important
Defold crée un arbre de dépendances lors du build et de la création du bundle de votre application. Le système de build part de la collection bootstrap spécifiée dans le fichier *game.project* et inspecte chaque collection, objet de jeu (game object) et composant (component) référencé pour établir la liste des ressources utilisées. Seules ces ressources sont incluses dans le bundle final de l'application. Tout ce qui n'est pas directement référencé est exclu. Bien qu'il soit utile de savoir que les ressources inutilisées ne seront pas incluses, vous devez tout de même, en tant que développeur, tenir compte du contenu de l'application finale, de la taille de chaque ressource et de la taille totale du bundle de l'application. 
:::

## Optimiser la taille du moteur {#optimize-engine-size}
Un moyen rapide de réduire la taille du moteur consiste à supprimer les fonctionnalités du moteur que vous n'utilisez pas. Cela se fait dans le [fichier manifeste de l'application](https://defold.com/manuals/app-manifest/), qui permet de supprimer les composants du moteur dont vous n'avez pas besoin. Exemples :

* Physique - Si votre jeu n'utilise pas la physique de Box2D ou de Bullet3D, il est fortement conseillé de supprimer les moteurs physiques
* GUI, effets de particules et tilemaps - Ces composants peuvent être exclus séparément avec les [options de composants de l'App Manifest](/manuals/app-manifest/#exclude-gui). Supprimez les références aux composants et les appels d'API de toute fonctionnalité exclue. Exclure les effets de particules supprime également la prise en charge des nœuds de particules dans les scènes GUI.
* Texte enrichi - Désactivez [Use Rich Text](/manuals/app-manifest/#use-rich-text) si les labels et le texte GUI n'ont besoin que de texte brut. Cela supprime l'analyse du balisage de texte enrichi et les effets de style tout en conservant le rendu du texte ordinaire.
* LiveUpdate - Si votre jeu n'utilise pas LiveUpdate, vous pouvez le supprimer
* Chargeur d'images - Si votre jeu ne charge et ne décode pas manuellement des images avec `image.load()`
* BasisU - Si votre jeu contient peu de textures, comparez la taille d'un build sans BasisU (supprimé via le manifeste de l'application) et sans compression des textures à celle d'un build avec BasisU et des textures compressées. Pour les jeux qui comportent peu de textures, il peut être plus avantageux de réduire la taille du binaire et de renoncer à la compression des textures. De plus, ne pas utiliser le transcodeur peut réduire la quantité de mémoire nécessaire à l'exécution de votre jeu.

## Optimiser la taille des ressources {#optimize-asset-size}
Les gains les plus importants en matière d'optimisation de la taille des ressources sont généralement obtenus en réduisant la taille des sons et des textures.

### Optimiser les sons {#optimize-sounds}
Defold prend en charge les formats suivants :
* .wav
* .ogg
* .opus

Defold prend en charge les fichiers Wave PCM de 8 et 16 bits. Ogg Vorbis et Ogg Opus utilisent leurs formats compressés respectifs, sans imposer une profondeur de bits PCM. Le décodeur Opus n'est pas inclus par défaut ; activez **Include Sound Decoder: Opus** dans le [manifeste de l'application](/manuals/app-manifest/#sound) avant d'utiliser des ressources `.opus`.
Nos décodeurs audio augmentent ou diminuent la fréquence d'échantillonnage des sons selon les besoins du périphérique audio actuel.

Les sons courts, comme les effets sonores, sont souvent compressés plus fortement, tandis que les fichiers musicaux sont moins compressés.
Defold n'applique aucune compression : le développeur doit donc s'en charger spécifiquement pour chaque format audio.

Vous pouvez modifier les sons dans un logiciel d'édition audio externe (ou en ligne de commande, par exemple avec [ffmpeg](https://ffmpeg.org)) pour réduire la qualité ou les convertir d'un format à un autre. Pensez également à convertir les sons stéréo en mono pour réduire encore la taille du contenu.

### Optimiser les textures {#optimize-textures}
Plusieurs options s'offrent à vous pour optimiser les textures utilisées par votre jeu, mais la première étape consiste à vérifier la taille des images ajoutées à un atlas ou utilisées comme tilesource. Vous ne devez jamais utiliser des images plus grandes que nécessaire dans votre jeu. Importer de grandes images et les réduire à la taille appropriée gaspille de la mémoire de texture et doit être évité. Commencez par ajuster la taille des images à celle réellement nécessaire dans votre jeu à l'aide d'un logiciel d'édition d'images externe. Pour les images d'arrière-plan, par exemple, il peut également être acceptable d'utiliser une petite image et de l'agrandir à la taille souhaitée. Une fois les images ramenées à la bonne taille et ajoutées à des atlas ou utilisées dans des tilesources, vous devez aussi tenir compte de la taille des atlas eux-mêmes. La taille maximale utilisable d'un atlas varie selon les plateformes et le matériel graphique.

::: sidenote
[Ce message du forum](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl) propose plusieurs astuces pour redimensionner plusieurs images à l'aide de scripts ou de logiciels tiers.
:::

* Taille maximale des textures sur HTML5 signalée au [projet Web3D Survey](https://web3dsurvey.com/webgl/parameters/MAX_TEXTURE_SIZE)
* Taille maximale des textures sur iOS :
  * iPad : 2048x2048
  * iPhone 4 : 2048x2048
  * iPad 2, 3, Mini, Air, Pro : 4096x4096
  * iPhone 4s, 5, 6+, 6s : 4096x4096
* La taille maximale des textures sur Android varie considérablement, mais, en général, tous les appareils relativement récents prennent en charge au moins 4096x4096.

Si un atlas est trop grand, vous devez soit le diviser en plusieurs atlas plus petits, soit utiliser des atlas à plusieurs pages, soit redimensionner l'atlas entier à l'aide d'un profil de texture. Le système de profils de texture de Defold vous permet non seulement de redimensionner des atlas entiers, mais aussi d'appliquer des algorithmes de compression pour réduire leur taille sur le disque. Vous pouvez [en savoir plus sur les profils de texture dans le manuel](/manuals/texture-profiles/). Si vous ne savez pas quels réglages utiliser, essayez de commencer par ceux-ci, puis adaptez-les à vos besoins :

* mipmaps: false
* premultiply_alpha: true
* format: TEXTURE_FORMAT_RGBA
* compression_level: NORMAL
* compression_type: COMPRESSION_TYPE_BASIS_UASTC

::: sidenote
Vous pouvez en savoir plus sur l'optimisation et la gestion des textures dans [ce message du forum](https://forum.defold.com/t/texture-management-in-defold/8921).
:::

### Optimiser les polices {#optimize-fonts}
La taille de vos polices sera plus petite si vous précisez les symboles que vous allez utiliser dans [Characters](/manuals/font/#properties) au lieu de cocher All Chars.

### Exclure du contenu pour le télécharger à la demande {#exclude-content-for-download-on-demand}
Une autre façon de réduire la taille initiale de l'application consiste à exclure une partie du contenu du jeu du bundle de l'application et à la télécharger à la demande. Defold propose un système appelé Live Update qui permet d'exclure du contenu pour le télécharger à la demande.

Le contenu exclu peut aller de niveaux entiers à des personnages, des apparences, des armes ou des véhicules à débloquer. Si votre jeu contient beaucoup de contenu, organisez le processus de chargement de sorte que la collection bootstrap et la collection du premier niveau incluent uniquement le strict minimum de ressources nécessaires à ce niveau. Pour cela, utilisez des proxys de collection (collection proxies) ou des factories avec la case « Exclude » cochée. Répartissez les ressources en fonction de la progression du joueur. Cette approche assure un chargement efficace des ressources et maintient une faible consommation de mémoire initiale. Pour en savoir plus, consultez le [manuel Live Update](/manuals/live-update/).

## Optimisations de taille propres à Android {#android-specific-size-optimizations}
Les builds Android doivent prendre en charge les architectures de processeur 32 et 64 bits. Lorsque vous [créez un bundle pour Android](/manuals/android), vous pouvez spécifier les architectures de processeur à inclure :

![Signature du bundle Android](images/android/sign_bundle.png)

Par défaut, un bundle inclut les architectures `armv7-android` et `arm64-android`. Une troisième architecture, `x86_64-android`, est disponible, mais n'est pas incluse par défaut, car elle est surtout utile pour les émulateurs Android, ChromeOS et Windows Subsystem for Android plutôt que pour les appareils physiques. Laissez-la décochée pour limiter la taille du bundle, sauf si vous devez spécifiquement cibler l'un de ces environnements.

Google Play prend en charge [plusieurs APK](https://developer.android.com/google/play/publishing/multiple-apks) par version publiée d'un jeu, ce qui vous permet de réduire la taille de l'application en générant deux APK, un par architecture de processeur, et en les important tous les deux dans Google Play.

Vous pouvez également combiner les [fichiers d'extension APK](https://developer.android.com/google/play/expansion-files) et le [contenu Live Update](/manuals/live-update) grâce à [l'extension APKX disponible dans l'Asset Portal](https://defold.com/assets/apkx/).
