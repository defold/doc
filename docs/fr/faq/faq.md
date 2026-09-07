---
title: FAQ du moteur et de l'éditeur Defold
brief: Questions fréquentes sur le moteur de jeu, l'éditeur et la plateforme Defold.
---

# Questions fréquentes {#frequently-asked-questions}

## Questions générales {#general-questions}

#### Q : Defold est-il vraiment gratuit ? {#q-is-defold-really-free}

R : Oui, le moteur et l'éditeur Defold, avec toutes leurs fonctionnalités, sont entièrement gratuits. Il n'y a ni coûts cachés, ni frais, ni redevances. C'est tout simplement gratuit.


#### Q : Pourquoi la Defold Foundation propose-t-elle Defold gratuitement ? {#q-why-on-earth-would-the-defold-foundation-give-defold-away}

R : L'un des objectifs de la [Defold Foundation](/foundation) est de garantir que le logiciel Defold soit accessible aux développeurs du monde entier et que son code source soit disponible gratuitement.


#### Q : Pendant combien de temps assurerez-vous la prise en charge de Defold ? {#q-how-long-will-you-support-defold}

R : Nous sommes profondément engagés envers Defold. La [Defold Foundation](/foundation) a été créée de manière à garantir qu'elle restera un propriétaire responsable de Defold pendant de nombreuses années. Elle est là pour durer.


#### Q : Puis-je faire confiance à Defold pour un développement professionnel ? {#q-can-i-trust-defold-for-professional-development}

R : Absolument. Defold est utilisé par un nombre croissant de développeurs de jeux professionnels et de studios de jeux. Consultez la [vitrine de jeux](/showcase) pour découvrir des exemples de jeux créés avec Defold.


#### Q : Quel type de suivi des utilisateurs effectuez-vous ? {#q-what-kind-of-user-tracking-are-you-doing}

R : Nous enregistrons des données d'utilisation anonymes provenant de nos sites web et de l'éditeur Defold afin d'améliorer nos services et notre produit. Aucun suivi des utilisateurs n'est effectué dans les jeux que vous créez (sauf si vous ajoutez vous-même un service d'analyse). Pour en savoir plus, consultez notre [politique de confidentialité](/privacy-policy).


#### Q : Qui a créé Defold ? {#q-who-made-defold}

R : Defold a été créé par Ragnar Svensson et Christian Murray. Ils ont commencé à travailler sur le moteur, l'éditeur et les serveurs en 2009. King et Defold ont établi un partenariat en 2013, puis King a acquis Defold en 2014. Découvrez toute l'histoire [ici](/about).


## Questions sur le développement de jeux {#game-development-questions}

#### Q : Puis-je créer des jeux 3D avec Defold ? {#q-can-i-do-3d-games-in-defold}

R : Absolument ! Le moteur est un moteur 3D à part entière. Cependant, les outils sont conçus pour la 2D, vous devrez donc réaliser vous-même une grande partie du travail. Une meilleure prise en charge de la 3D est prévue.


## Questions sur les langages de programmation {#programming-language-questions}

#### Q : Quel langage de programmation utilise-t-on dans Defold ? {#q-what-programming-language-do-i-work-with-in-defold}

R : La logique du jeu de votre projet Defold est principalement écrite en Lua (plus précisément Lua 5.1/LuaJIT ; consultez le [manuel Lua](/manuals/lua) pour plus de détails). Lua est un langage dynamique léger, rapide et très puissant. Defold prend en charge les transpileurs qui produisent du code Lua. Une fois une extension de transpilation installée, vous pouvez utiliser d'autres langages — comme [Teal](https://github.com/defold/extension-teal) — pour écrire du Lua vérifié statiquement. Vous pouvez également utiliser du code natif (C/C++, Objective-C, Java et JavaScript selon la plateforme) pour [ajouter de nouvelles fonctionnalités au moteur Defold](/manuals/extensions/). Lors de la création de [matériaux personnalisés](/manuals/material/), le langage de shaders OpenGL ES SL est utilisé pour écrire les shaders de sommets et de fragments.


#### Q : Puis-je utiliser C++ pour écrire la logique du jeu ? {#q-can-i-use-c-to-write-game-logic}

R : La prise en charge de C++ dans Defold sert principalement à écrire des extensions natives qui interagissent avec des SDK tiers ou des API propres à une plateforme. Le [dmSDK](https://defold.com/ref/stable/dmGameObject/) (l'API C++ de Defold utilisée dans les extensions natives) sera progressivement enrichi de nouvelles fonctionnalités afin de permettre aux développeurs qui le souhaitent d'écrire toute la logique du jeu en C++. Lua restera le langage principal pour la logique du jeu, mais l'API C++ enrichie permettra également de l'écrire en C++. Le travail d'enrichissement de l'API C++ consiste surtout à déplacer les fichiers d'en-tête privés existants vers la partie publique et à remanier les API pour un usage public.


#### Q : Puis-je utiliser TypeScript avec Defold ? {#q-can-i-use-typescript-with-defold}

R : TypeScript n'est pas officiellement pris en charge. La communauté maintient une boîte à outils, [ts-defold](https://ts-defold.dev/), qui permet d'écrire du TypeScript et de le transpiler en Lua directement depuis VSCode.


#### Q : Puis-je utiliser Haxe avec Defold ? {#q-can-i-use-haxe-with-defold}

R : Haxe n'est pas officiellement pris en charge. La communauté maintient [hxdefold](https://github.com/hxdefold/hxdefold), qui permet d'écrire du Haxe et de le transpiler en Lua.


#### Q : Puis-je utiliser C# avec Defold ? {#q-can-i-use-c-with-defold}

R : La Defold Foundation a ajouté la prise en charge de C# et l'a rendue disponible sous forme de dépendance de bibliothèque. C# est un langage de programmation largement adopté, et sa prise en charge aidera les studios et les développeurs qui ont beaucoup investi dans C# à passer à Defold.


#### Q : Je crains que l'ajout de C# ait un impact négatif sur Defold. Dois-je m'inquiéter ? {#q-i-am-concerned-that-adding-c-support-will-have-a-negative-impact-on-defold-should-i-be-worried}

Defold n'abandonne PAS Lua comme langage de script principal. C# est ajouté comme nouveau langage pour les extensions. Cela n'aura aucune incidence sur le moteur, sauf si vous choisissez d'utiliser des extensions C# dans votre projet.

La prise en charge de C# aura un coût (taille de l'exécutable, performances à l'exécution, etc.), mais il revient à chaque développeur ou studio de décider si cela lui convient.

Quant à C# lui-même, il s'agit d'un changement relativement mineur, puisque le système d'extensions prend déjà en charge de nombreux langages (C/C++/Java/Objective-C/Zig). Les SDK resteront synchronisés grâce à la génération des liaisons C#. Cela permettra de maintenir ces liaisons à jour avec un minimum d'efforts.

La Defold Foundation était auparavant opposée à l'ajout de C# dans Defold, mais elle a changé d'avis pour plusieurs raisons :

* Les studios et les développeurs continuent de demander la prise en charge de C#.
* La portée de la prise en charge de C# a été réduite aux seules extensions (ce qui demande peu d'efforts).
* Le cœur du moteur ne sera pas affecté.
* Les API C# peuvent rester synchronisées avec un minimum d'efforts si elles sont générées.
* La prise en charge de C# reposera sur DotNet 9 avec NativeAOT, produisant ainsi des bibliothèques statiques que la chaîne de build existante peut intégrer lors de l'édition de liens (comme pour toute autre extension Defold).


## Questions sur les plateformes {#platform-questions}

#### Q : Sur quelles plateformes Defold fonctionne-t-il ? {#q-what-platforms-does-defold-run-on}

R : Les plateformes suivantes sont prises en charge par l'éditeur et les outils, ainsi que par le moteur d'exécution :

  | Système            | Version            | Architectures      | Prise en charge    |
  | ------------------ | ------------------ | ------------------ | ------------------ |
  | macOS              | 11 Big Sur         | `x86-64`, `arm-64` | Éditeur et moteur  |
  | Windows            | Vista              | `x86-32`, `x86-64` | Éditeur et moteur  |
  | Ubuntu (1)         | 22.04 LTS          | `x86-64`           | Éditeur            |
  | Linux (2)          | Toutes             | `x86-64`, `arm-64` | Moteur             |
  | iOS                | 15.0               | `arm-64`  `x86_64` | Moteur             |
  | Android            | 5.0 (niveau d'API 21) | `arm-32`, `arm-64` | Moteur          |
  | HTML5              |                    | `wasm-web`, `wasm_pthread-web` | Moteur       |

  (1 L'éditeur est compilé et testé pour Ubuntu 64 bits. Il devrait également fonctionner sur d'autres distributions, mais nous ne donnons aucune garantie.)

  (2 Le moteur d'exécution devrait fonctionner sur la plupart des distributions Linux 64 bits tant que les pilotes graphiques sont à jour. Voir ci-dessous pour plus d'informations sur les API graphiques.)


#### Q : Pour quelles plateformes cibles puis-je développer des jeux avec Defold ? {#q-what-target-platforms-can-i-develop-games-for-with-defold}

R : En un clic, vous pouvez publier sur PS4™, PS5™, Nintendo Switch, iOS (64 bits), Android (32 bits et 64 bits) et HTML5, ainsi que sur macOS (x86-64 et arm64), Windows (32 bits et 64 bits) et Linux (x86-64 et arm64). Une seule base de code permet réellement de prendre en charge plusieurs plateformes.


#### Q : Sur quelle API de rendu Defold repose-t-il ? {#q-what-rendering-api-does-defold-rely-on}

R : En tant que développeur, vous n'avez à vous soucier que d'une seule API de rendu utilisant une [chaîne de rendu entièrement programmable par script](/manuals/render/). L'API des scripts de rendu de Defold traduit les opérations de rendu vers les API graphiques suivantes :

:[Graphics API](../shared/graphics-api.md)

#### Q : Existe-t-il un moyen de connaître la version que j'utilise ? {#q-is-there-a-way-to-know-what-version-im-running}

R : Oui, sélectionnez l'option « About » dans le menu Help. La fenêtre qui s'affiche indique clairement la version bêta de Defold et, surtout, le SHA1 de cette version précise. Pour obtenir la version à l'exécution, utilisez [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info).

Vous pouvez vérifier la dernière version bêta disponible au téléchargement sur [http://d.defold.com/beta](http://d.defold.com/beta) en ouvrant [http://d.defold.com/beta/info.json](http://d.defold.com/beta/info.json) (le même fichier existe également pour les versions stables : [http://d.defold.com/stable/info.json](http://d.defold.com/stable/info.json)).


#### Q : Existe-t-il un moyen de connaître la plateforme sur laquelle le jeu s'exécute ? {#q-is-there-a-way-to-know-what-platform-the-game-is-running-on-at-runtime}

R : Oui, consultez [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info).


## Questions sur l'éditeur {#editor-questions}
:[Editor FAQ](../shared/editor-faq.md)


## Questions sur Linux {#linux-questions}
:[Linux FAQ](../shared/linux-faq.md)


## Questions sur Android {#android-questions}
:[Android FAQ](../shared/android-faq.md)


## Questions sur HTML5 {#html5-questions}
:[HTML5 FAQ](../shared/html5-faq.md)


## Questions sur iOS {#ios-questions}
:[iOS FAQ](../shared/ios-faq.md)


## Questions sur Windows {#windows-questions}
:[Windows FAQ](../shared/windows-faq.md)


## Questions sur les consoles {#console-questions}
:[Consoles FAQ](../shared/consoles-faq.md)


## Publication de jeux {#publishing-games}

#### Q : J'essaie de publier mon jeu sur l'AppStore. Que dois-je répondre au sujet de l'IDFA ? {#q-im-trying-to-publish-my-game-to-appstore-how-should-i-respond-to-idfa}

R : Lors de la soumission, Apple propose trois cases à cocher pour les trois cas d'utilisation autorisés de l'IDFA :

  1. Diffuser des publicités dans l'application
  2. Attribuer les installations aux publicités
  3. Attribuer les actions des utilisateurs aux publicités

  Si vous cochez l'option 1, la personne chargée d'examiner l'application vérifiera que des publicités s'y affichent. Si votre jeu n'affiche pas de publicités, il risque d'être rejeté. Defold lui-même n'utilise pas d'identifiant publicitaire.


#### Q : Comment monétiser mon jeu ? {#q-how-do-i-monetize-my-game}

R : Defold prend en charge les achats intégrés et diverses solutions publicitaires. Consultez la [catégorie Monetization de l'Asset Portal](https://defold.com/tags/stars/monetization/) pour obtenir une liste à jour des options de monétisation disponibles.


## Erreurs lors de l'utilisation de Defold {#errors-using-defold}

#### Q : Je n'arrive pas à démarrer le jeu, mais aucune erreur de build n'apparaît. Que se passe-t-il ? {#q-i-cant-start-the-game-and-there-is-no-build-error-whats-wrong}

R : Dans de rares cas, le processus de build peut ne pas recompiler les fichiers après avoir rencontré des erreurs de build que vous avez corrigées. Forcez une recompilation complète en sélectionnant *Project > Rebuild And Launch* dans le menu.



## Contenu du jeu {#game-content}

#### Q : Defold prend-il en charge les prefabs ? {#q-does-defold-support-prefabs}

R : Oui. Ils sont appelés [collections](/manuals/building-blocks/#collections). Ils permettent de créer des hiérarchies complexes d'objets de jeu (game objects) et de les enregistrer comme des éléments distincts que vous pouvez instancier dans l'éditeur ou à l'exécution (par création dynamique de collections). Les nœuds d'interface graphique prennent en charge les modèles d'interface graphique.


#### Q : Je n'arrive pas à ajouter un objet de jeu comme enfant d'un autre objet de jeu. Pourquoi ? {#q-i-cant-add-a-game-object-as-a-child-to-another-game-object-why}

R : Vous essayez probablement d'ajouter un enfant dans le fichier de l'objet de jeu, ce qui n'est pas possible. Cette opération n'est possible que dans le fichier de collection. Pour comprendre pourquoi, rappelez-vous que les hiérarchies parent-enfant sont strictement des hiérarchies de transformations du _graphe de scène_. Un objet de jeu qui n'a pas été placé (ou créé dynamiquement) dans une scène (collection) ne fait pas partie d'un graphe de scène et ne peut donc pas appartenir à une hiérarchie de graphe de scène. Vous pouvez obtenir l'identifiant du parent de l'objet de jeu à l'aide de [`go.get_parent()`](https://defold.com/ref/stable/go-lua/#go.get_parent:id).


#### Q : Pourquoi ne puis-je pas diffuser des messages à tous les enfants d'un objet de jeu ? {#q-why-cant-i-broadcast-messages-to-all-children-of-a-game-object}

R : Les relations parent-enfant expriment uniquement les relations de transformation du graphe de scène et ne doivent pas être confondues avec les agrégations de la programmation orientée objet. Si vous vous concentrez sur les données de votre jeu et sur la meilleure façon de les transformer lorsque son état change, vous aurez probablement moins besoin d'envoyer constamment des messages contenant des données d'état à de nombreux objets. Lorsque vous avez besoin de hiérarchies de données, celles-ci sont faciles à construire et à gérer en Lua.


#### Q : Pourquoi des artefacts visuels apparaissent-ils sur les bords de mes sprites ? {#q-why-am-i-experiencing-visual-artifacts-around-the-edges-of-my-sprites}

R : Il s'agit d'un artefact visuel appelé « débordement des bords » (edge bleeding), dans lequel les pixels situés sur les bords d'éléments voisins dans un atlas débordent sur l'image attribuée à votre sprite. La solution consiste à ajouter une ou plusieurs lignes et colonnes de pixels identiques sur les bords des images de votre atlas. Heureusement, l'éditeur d'atlas de Defold peut le faire automatiquement. Ouvrez votre atlas et définissez la valeur *Extrude Borders* sur 1.


#### Q : Puis-je teinter mes sprites ou les rendre transparents, ou dois-je écrire mon propre shader pour cela ? {#q-can-i-tint-my-sprites-or-make-them-transparent-or-do-i-have-to-write-my-own-shader-for-it}

R : Le shader de sprite intégré, utilisé par défaut pour tous les sprites, définit une constante « tint » :

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### Q : Si je définis la coordonnée z d'un sprite sur 100, il n'est plus affiché. Pourquoi ? {#q-if-i-set-the-z-coordinate-of-a-sprite-to-100-then-its-not-rendered-why}

R : La position Z d'un objet de jeu détermine l'ordre de rendu. Les valeurs faibles sont dessinées avant les valeurs élevées. Dans le script de rendu par défaut, les objets de jeu dont la profondeur est comprise entre -1 et 1 sont dessinés ; tout ce qui se trouve en dessous ou au-dessus ne l'est pas. Vous trouverez plus d'informations sur le script de rendu dans la [documentation officielle sur le rendu](/manuals/render). Pour les nœuds d'interface graphique, la valeur Z est ignorée et n'a aucune incidence sur l'ordre de rendu. Les nœuds sont rendus dans l'ordre où ils apparaissent dans la liste et selon les hiérarchies d'enfants (et les couches). Pour en savoir plus sur le rendu de l'interface graphique et l'optimisation des appels de dessin à l'aide des couches, consultez la [documentation officielle sur l'interface graphique](/manuals/gui).


#### Q : Remplacer la plage Z de la projection de vue par -100 à 100 aurait-il un impact sur les performances ? {#q-would-changing-the-view-projection-z-range-to-100-to-100-impact-performance}

R : Non. Le seul effet concerne la précision. Le tampon de profondeur est logarithmique et offre une résolution très fine pour les valeurs z proches de 0, mais une résolution plus faible loin de 0. Par exemple, avec un tampon de 24 bits, les valeurs 10.0 et 10.000005 peuvent être distinguées, contrairement à 10000 et 10005.


#### Q : Pourquoi la représentation des angles n'est-elle pas cohérente ? {#q-there-is-no-consistency-to-how-angles-are-represented-why}

R : Elle est en réalité cohérente. Les angles sont exprimés en degrés partout dans l'éditeur et les API du jeu. Les bibliothèques mathématiques utilisent les radians. Cette convention n'est actuellement pas respectée pour la propriété physique `angular_velocity`, qui est exprimée en radians/s. Cela devrait changer.


#### Q : Comment un nœud de type boîte d'interface graphique avec une couleur seule (sans texture) est-il rendu ? {#q-when-creating-a-gui-box-node-with-only-color-no-texture-how-will-it-be-rendered}

R : Il s'agit simplement d'une forme dont les sommets sont colorés. Gardez à l'esprit qu'elle consomme tout de même de la capacité de remplissage des pixels.


#### Q : Si je change les ressources à la volée, le moteur les déchargera-t-il automatiquement ? {#q-if-i-change-assets-on-the-fly-will-the-engine-automatically-unload-them}

R : Toutes les ressources disposent en interne d'un compteur de références. Dès que ce compteur atteint zéro, la ressource est libérée.


#### Q : Est-il possible de lire de l'audio sans utiliser un composant audio rattaché à un objet de jeu ? {#q-is-it-possible-to-play-audio-without-the-use-of-an-audio-component-attached-to-a-game-object}

R : Tout repose sur des composants (components). Il est possible de créer un objet de jeu sans interface graphique avec plusieurs sons, puis de lire ces sons en envoyant des messages à l'objet qui contrôle le son.


#### Q : Est-il possible de changer à l'exécution le fichier audio associé à un composant audio ? {#q-is-it-possible-to-change-the-audio-file-associated-with-an-audio-component-at-run-time}

R : En général, toutes les ressources sont déclarées statiquement, ce qui présente l'avantage de bénéficier automatiquement de leur gestion. Vous pouvez utiliser les [propriétés de ressource](/manuals/script-properties/#resource-properties) pour changer la ressource attribuée à un composant.


#### Q : Existe-t-il un moyen d'accéder aux propriétés des formes de collision physiques ? {#q-is-there-a-way-to-access-the-physics-collision-shape-properties}

R : Oui, consultez l'API de physique, en particulier [`physics.get_shape()`](https://defold.com/ref/stable/physics-lua/#physics.get_shape:url-shape) et [`physics.set_shape()`](https://defold.com/ref/stable/physics-lua/#physics.set_shape:url-shape-table). 


#### Q : Existe-t-il un moyen rapide d'afficher les objets de collision de ma scène ? (comme l'affichage de débogage de Box2D) {#q-is-there-any-quick-way-to-render-the-collision-objects-in-my-scene-like-box2ds-debug-draw}

R : Oui, activez le paramètre *physics.debug* dans *game.project*. (Consultez la [documentation officielle sur les paramètres du projet](/manuals/project-settings/#debug).)


#### Q : Quel est le coût en performances d'un grand nombre de contacts et de collisions ? {#q-what-are-the-performance-costs-of-having-many-contactscollisions}

R : Defold utilise une version modifiée de Box2D en arrière-plan, et le coût en performances devrait être assez similaire. Vous pouvez à tout moment voir combien de temps le moteur consacre à la physique en ouvrant le [profileur](/manuals/debugging). Vous devez également tenir compte du type d'objets de collision utilisé. Par exemple, les objets statiques coûtent moins cher en performances. Consultez la [documentation officielle sur la physique](/manuals/physics) de Defold pour plus de détails.


#### Q : Quel est l'impact sur les performances d'un grand nombre de composants d'effets de particules ? {#q-whats-the-performance-impact-of-having-many-particle-effect-components}

R : Cela dépend de leur activité. Un ParticleFx qui ne joue pas n'a aucun coût en performances. Les conséquences d'un ParticleFx en cours de lecture sur les performances doivent être évaluées à l'aide du profileur, car son impact dépend de sa configuration. Comme pour la plupart des autres éléments, la mémoire est allouée à l'avance pour le nombre de ParticleFx défini par max_count dans *game.project*.


#### Q : Comment un objet de jeu situé dans une collection chargée via un proxy de collection peut-il recevoir des entrées ? {#q-how-do-i-receive-input-to-a-game-object-inside-a-collection-loaded-via-a-collection-proxy}

R : Chaque collection chargée par un proxy de collection (collection proxy) possède sa propre pile d'entrées. Les entrées sont acheminées depuis la pile d'entrées de la collection principale, via le composant proxy, jusqu'aux objets de la collection. Cela signifie qu'il ne suffit pas que l'objet de jeu de la collection chargée acquière le focus d'entrée : l'objet de jeu qui _contient_ le composant proxy doit également l'acquérir. Consultez la [documentation sur les entrées](/manuals/input) pour plus de détails.


#### Q : Puis-je utiliser des propriétés de script de type chaîne de caractères ? {#q-can-i-use-string-type-script-properties}

R : Non. Defold prend en charge les propriétés de type [hash](/ref/builtins#hash). Elles peuvent servir à indiquer des types, des identifiants d'état ou des clés de toute nature. Les valeurs hachées peuvent également servir à stocker les identifiants (chemins) d'objets de jeu, même si les propriétés de type [url](/ref/msg#msg.url) sont souvent préférables, car l'éditeur remplit automatiquement une liste déroulante avec les URL pertinentes. Consultez la [documentation sur les propriétés de script](/manuals/script-properties) pour plus de détails.


#### Q : Comment accéder aux cellules individuelles d'une matrice (créée avec [`vmath.matrix4()`](/ref/vmath/#vmath.matrix4:m1) ou une fonction similaire) ? {#q-how-do-i-access-the-individual-cells-of-a-matrix-created-using-vmathmatrix4refvmathvmathmatrix4m1-or-similar}

R : Vous accédez aux cellules à l'aide de `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21`, etc.


#### Q : J'obtiens `Not enough resources to clone the node` lorsque j'utilise [gui.clone()](/ref/gui/#gui.clone:node) ou [gui.clone_tree()](/ref/gui/#gui.clone_tree:node) {#q-i-am-getting-not-enough-resources-to-clone-the-node-when-using-guiclonerefguiguiclonenode-or-guiclone_treerefguiguiclone_treenode}

R : Augmentez la valeur `Max Nodes` du composant d'interface graphique. Vous trouverez cette valeur dans le panneau Properties en sélectionnant la racine du composant dans Outline.


## Le forum {#the-forum}

#### Q : Puis-je publier un sujet pour promouvoir mon travail ? {#q-can-i-post-a-thread-where-i-advertise-my-work}

R : Bien sûr ! Nous avons une [catégorie « Work for hire »](https://forum.defold.com/c/work-for-hire) spécialement prévue pour cela. Nous encouragerons toujours tout ce qui profite à la communauté, et lui proposer vos services — rémunérés ou non — en est un bon exemple.


#### Q : J'ai créé un sujet et présenté mon travail. Puis-je en ajouter davantage ? {#q-i-made-a-thread-and-added-my-workcan-i-add-more}

R : Pour limiter les remontées des sujets « Work for hire », vous ne pouvez pas publier plus d'un message tous les 14 jours dans votre propre sujet (sauf pour répondre directement à un commentaire du sujet, auquel cas vous pouvez répondre). Si vous souhaitez présenter d'autres travaux dans votre sujet pendant cette période de 14 jours, vous devez modifier vos messages existants pour y ajouter le contenu.


#### Q : Puis-je utiliser la catégorie Work for Hire pour publier des offres d'emploi ? {#q-can-i-use-the-work-for-hire-category-to-post-job-offerings}

R : Bien sûr, allez-y ! Elle peut servir aussi bien pour les offres que pour les demandes, par exemple : « Programmeur recherche artiste pixel art 2D ; je suis riche et je vous paierai bien ».
