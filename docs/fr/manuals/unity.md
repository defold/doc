---
title: Defold pour les utilisateurs de Unity
brief: Ce guide vous aide à passer rapidement à Defold si vous avez déjà de l’expérience avec Unity. Il présente certains des concepts clés de Unity et explique les outils et méthodes correspondants dans Defold.
---

# Defold pour les utilisateurs de Unity {#defold-for-unity-users}

Si vous avez déjà de l’expérience avec Unity, ce guide vous aide à devenir rapidement productif dans Defold. Il se concentre sur l’essentiel et vous renvoie aux manuels officiels de Defold lorsque des explications plus approfondies sont nécessaires.

## Introduction {#introduction}

Defold est un moteur de jeu 3D entièrement gratuit et véritablement multiplateforme, avec un éditeur pour Windows, Linux et macOS. L’intégralité du code source est disponible sur [Github](https://github.com/defold/defold/).

Defold privilégie les performances, même sur les appareils peu puissants. Il utilise un modèle de composants compact, dans lequel de nombreuses interactions de jeu sont gérées par le code et l’échange de messages.

Defold est beaucoup plus léger que Unity. Le moteur avec un projet vide occupe entre 1 et 3 Mo sur toutes les plateformes. Vous pouvez retirer d’autres parties du moteur et déplacer une partie du contenu du jeu vers [Live Update](/manuals/live-update) pour le télécharger séparément plus tard. Une comparaison des tailles et d’autres raisons de choisir Defold sont présentées sur la [page Pourquoi Defold](https://defold.com/why/).

Pour adapter Defold à vos besoins, vous pouvez créer vos propres éléments ou utiliser des éléments existants :

1. Un pipeline de rendu entièrement programmable (script de rendu + matériaux/shaders), avec plusieurs backends au choix (OpenGL, Vulkan, etc.).
2. Du code et des composants sous forme d’extensions natives (C++/C#).
3. Des scripts de l’éditeur et des widgets d’interface pour personnaliser l’éditeur.
3. Un build modifié du moteur et de l’éditeur, puisque l’intégralité du code source et un pipeline de build sont disponibles.

Nous vous recommandons également de regarder la vidéo de Game From Scratch sur [Defold pour les développeurs Unity](https://www.youtube.com/watch?v=-3CzCbd4QZ0).

---

## Installation {#installation}

1. Téléchargez Defold pour votre système d’exploitation.
2. Décompressez-le et lancez-le.

C’est tout. Aucun hub, SDK supplémentaire, chaîne d’outils ou bundle de plateforme à installer. C’est pourquoi nous disons que Defold ne nécessite aucune configuration initiale.

Pour en savoir plus, consultez ce court [manuel d’installation](/manuals/install/).

### Versions {#versions}

Defold est fréquemment mis à jour et ne propose pas de branche « LTS ». Nous vous recommandons de toujours utiliser la version la plus récente. De nouvelles versions sont publiées régulièrement, généralement tous les mois, avec environ deux semaines de bêta publique. Vous pouvez mettre Defold à jour directement dans l’éditeur.

---

## Écran d’accueil {#welcome-screen}

Defold vous accueille avec un écran semblable à Unity Hub, où vous pouvez ouvrir vos projets récents :

![Comparaison des écrans d’accueil](images/unity/unity_defold_start.png)

Ou en créer un à partir des catégories suivantes :
- `Templates` - des projets vides de base pour démarrer plus rapidement sur une plateforme ou dans un genre précis,
- `Tutorials` - des parcours d’apprentissage guidés qui vous aident à faire vos premiers pas,
- `Samples` - des cas d’utilisation et des exemples officiels ou proposés par la communauté,

![Comparaison des modèles de l’écran d’accueil](images/unity/unity_defold_templates.png)

Lorsque vous créez votre premier projet et/ou l’ouvrez, il s’ouvre dans l’éditeur Defold.

## Bonjour le monde {#hello-world}

Voici une manière rapide de réaliser quelque chose dans Defold : suivez ces étapes, puis revenez lire la suite du manuel.

1. Sélectionnez un projet vide dans `Templates`, donnez-lui un nom dans `Title`, choisissez son emplacement et créez-le en cliquant sur `Create New Project`. Il s’ouvrira dans l’éditeur Defold.
![Bonjour le monde, étape 1](images/unity/helloworld_1.png)
2. À gauche, dans le panneau `Assets`, ouvrez le dossier `main` et double-cliquez sur `main.collection` pour l’ouvrir.
3. À droite, dans le panneau `Outline`, faites un clic droit sur `Collection` et sélectionnez `Add Game Object`.
![Bonjour le monde, étape 2](images/unity/helloworld_2.png)
4. Faites un clic droit sur l’objet de jeu (game object) `go` créé et sélectionnez `Add Component`, puis `Label`.
![Bonjour le monde, étape 3](images/unity/helloworld_3.png)
5. En dessous, à gauche, dans le panneau `Properties`, saisissez du texte dans la propriété `Text`.
6. Dans la vue principale de la scène, au centre, faites glisser l’étiquette pour la placer aux environs de `(480,320,0)`, ou modifiez sa position dans `Properties` : `Position`.
![Bonjour le monde, étape 4](images/unity/helloworld_4.png)
7. Après avoir modifié la position de l’étiquette, enregistrez le projet en cliquant sur `File` -> `Save All` ou avec le raccourci <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>Cmd</kbd>+<kbd>S</kbd> sur Mac).
8. Générez un build de votre projet en cliquant sur `Project` -> `Build` ou avec le raccourci <kbd>Ctrl</kbd>+<kbd>B</kbd> (<kbd>Cmd</kbd>+<kbd>B</kbd> sur Mac).
![Bonjour le monde, étape 5](images/unity/helloworld_5.png)

Vous venez de générer le build de votre premier projet dans Defold et devriez voir votre texte dans la fenêtre. Les concepts d’objet de jeu et de composant (component) devraient vous être familiers. Les collections, la hiérarchie, les propriétés et la raison pour laquelle nous avons dû déplacer légèrement l’étiquette vers le haut et la droite sont expliquées ci-dessous.

---

## Présentation de l’éditeur Defold {#defold-editor-overview}

Nous présentons ici l’éditeur Defold en nous plaçant du point de vue de ce qu’un utilisateur de Unity souhaite savoir en premier, mais nous vous encourageons à consulter ensuite le [manuel complet de présentation de l’éditeur](/manuals/editor).

### Comparaison des éditeurs {#editors-comparison}

La première différence que vous remarquerez entre Unity et Defold est la disposition par défaut de l’éditeur. Nous montrons un éditeur Unity dont la disposition a été légèrement modifiée pour correspondre à celle de Defold par défaut. Ils sont placés côte à côte pour faciliter la comparaison visuelle des principaux panneaux, car vous devriez reconnaître plus facilement les onglets de Unity.

![Comparaison des éditeurs](images/unity/defold_unity_editor.png)

Par défaut, l’éditeur Defold s’ouvre avec un aperçu orthographique 2D. Si vous travaillez sur un projet 3D ou souhaitez simplement une expérience plus proche de Unity, nous vous recommandons de passer de la 2D à la 3D en décochant le bouton `2D` dans la barre d’outils, puis d’activer la projection en perspective de la caméra en cochant le bouton `Perspective` :

![Barre d’outils de Defold](images/unity/defold_2d.png)

Vous pouvez également ajuster `Grid Settings` dans la barre d’outils pour utiliser le plan `Y`, comme dans Unity :

![Paramètres 3D de Defold](images/unity/defold_3d.png)

### Présentation des panneaux de Defold {#defold-panes-overview}

L’éditeur Defold est divisé en six panneaux principaux.

![Éditeur 2](images/editor/editor_overview.png)

Voici une comparaison de la terminologie de Defold et des différences de fonctionnement :

| Defold | Unity | Différences |
|---|---|---|
| 1. Assets | Project (Assets Browser) | Dans Defold, le panneau Assets est ancré à gauche. Defold ne crée aucun fichier `meta`. |
| 2. Main Editor | Scene View | L’éditeur Defold s’adapte au contexte (des éditeurs différents selon les types de fichiers), tandis que Unity utilise des fenêtres spécialisées distinctes (par exemple Animator et Shader Graph). Defold possède également un éditeur de code intégré. |
| 3. Outline | Hierarchy | Defold affiche uniquement le fichier actuellement ouvert ou l’élément sélectionné (objet de jeu ou composant), et non une hiérarchie globale. |
| 4. Properties | Inspector | Defold affiche uniquement les propriétés de la **sélection actuelle** dans Outline, et non celles de tous les composants de l’objet de jeu. |
| 5. Tools | Console | Defold propose des outils dans des onglets tels que Console, Curve Editor, Build Errors, Search Results, Breakpoints et Debugger. |
| 6. Changed Files | Unity Version Control (Plastic) | Dans Defold, une fois Git intégré à votre projet, les fichiers modifiés s’affichent ici. Vous pouvez toujours utiliser Git à l’extérieur de l’éditeur. |

Autres termes utiles liés à l’éditeur :

| Defold | Unity | Différences |
|---|---|---|
| Game Build | Game Preview | Affiche le jeu en cours d’exécution, compilé avec le moteur. Defold peut lancer plusieurs instances du jeu depuis l’éditeur, comme le Multiplayer Play Mode de Unity 6+. Dans Defold, le jeu s’exécute toujours dans une fenêtre séparée, non ancrée. Defold peut également exécuter le jeu sur un appareil externe (par exemple un téléphone mobile), comme Unity Remote. |
| Onglets | Onglets | Defold permet de modifier des fichiers côte à côte dans deux panneaux de la vue Main Editor. Les onglets et les panneaux sont ancrés dans une seule fenêtre de l’éditeur ; vous pouvez afficher ou masquer les panneaux (<kbd>F6</kbd>, <kbd>F7</kbd>, <kbd>F8</kbd>) et ajuster leurs dimensions. |
| Barre d’outils | Barre d’outils / Scene View Options | Ce n’est que dans les versions récentes de Unity que les outils de transformation ont été déplacés dans la vue de la scène, comme dans Defold. |
| Console | Console | La console de Defold n’est pas détachable. Les erreurs de build de Defold apparaissent dans un onglet `Build Errors` distinct. |
| Build Errors | Erreurs de compilation dans la console | Les scripts Lua sont interprétés, il n’y a donc pas d’erreurs de compilation. Cependant, votre projet fait l’objet d’un build et certaines erreurs peuvent survenir pendant ce processus. Defold utilise également un serveur de langage Lua pour l’analyse statique des scripts. |
| Search Results | Search / Project Search | Defold ne propose pas de filtrage par types et étiquettes. |
| Curve Editor | Unity Curve Editor | L’éditeur de courbes de Defold permet uniquement de modifier les courbes des propriétés des effets de particules. |
| [Debugger](/manuals/debugging/) | Visual Studio Debugger | Le débogueur est entièrement intégré à Defold dès l’installation. Un onglet supplémentaire permet de suivre, d’activer et de désactiver les points d’arrêt. |

---

## Concepts clés {#key-concepts}

À un niveau suffisamment général, les concepts clés de la plupart des moteurs de jeu sont très proches. Ils visent à aider les développeurs à créer des jeux plus facilement, comme en assemblant des blocs, tout en prenant en charge les tâches complexes et celles propres aux plateformes.

### Éléments de base {#building-blocks}

Defold fonctionne avec seulement quelques éléments de base :

![Éléments de base](images/unity/blocks.png)

Pour en savoir plus, consultez le manuel complet sur les [éléments de base de Defold](/manuals/building-blocks/).

### Objets de jeu {#game-objects}
Defold utilise des **« objets de jeu »**, comme Unity. Dans les deux moteurs, les objets de jeu sont des conteneurs de données dotés d’un identifiant, et tous possèdent des transformations : position, rotation et échelle. Dans Defold, toutefois, la transformation est intégrée au lieu de constituer un composant distinct.

Vous pouvez créer des relations parent-enfant entre les objets de jeu. Dans Defold, cela ne peut se faire que dans l’éditeur au sein d’une « collection » (expliquée ci-dessous) ou dynamiquement dans un script. Les objets de jeu ne peuvent pas contenir d’autres objets de jeu imbriqués comme dans Unity.

### Composants {#components}
Dans les deux moteurs, les objets de jeu peuvent être étendus avec des **« composants »**. Defold fournit un ensemble minimal de composants essentiels. La distinction entre 2D et 3D est moins marquée que dans Unity (par exemple pour les colliders), il y a donc moins de composants au total et certains composants de Unity pourraient vous manquer.

#### Composants de comportement {#behaviour-components}

Dans Unity, « composant » désigne généralement un `MonoBehaviour` attaché à un `GameObject`. Vous pouvez créer les vôtres en héritant de `MonoBehaviour` ou utiliser les composants intégrés, comme Light, les composants de physique et ainsi de suite.

Dans Defold, le terme composant désigne exclusivement ce qui correspondrait aux composants intégrés de Unity ou à des éléments similaires, mais Defold ne traite pas un script comme un monobehaviour et n’exige aucun « marquage » explicite pour l’attacher à un objet de jeu, à part la création d’événements d’écoute ou de callbacks.

Un comportement de jeu personnalisé n’est généralement pas ajouté sous la forme de nombreux composants script distincts sur un même objet de jeu. Il est plutôt implémenté dans des modules Lua utilisés par un `.script` hôte, ou géré par un script système plus large qui contrôle de nombreux objets. La section Écriture du code ci-dessous aborde ce sujet plus en détail.

Pour en savoir plus sur les [composants de Defold, consultez cette page](/manuals/components/).

Le tableau ci-dessous présente les composants Unity similaires pour faciliter la recherche, avec des liens vers le manuel de chaque composant Defold :

| Defold | Unity | Différences |
|---|---|---|
| [Sprite](/manuals/sprite/) | Sprite Renderer | Dans Defold, vous ne pouvez changer la teinte (propriété de couleur) que par le code. |
| [Tilemap](/manuals/tilemap/) | Tilemap / Grid | Defold possède un éditeur de tilemaps intégré qui prend en charge les grilles carrées (mais il existe des extensions, comme [Hexagon](https://github.com/selimanac/defold-hexagon/)) et ne propose pas de règles intégrées de placement automatique des tuiles. Des outils comme [Tiled](https://defold.com/assets/tiled/), [TileSetter](https://defold.com/assets/tilesetter/) ou [Sprite Fusion](https://defold.com/assets/spritefusion/) proposent des options d’exportation vers Defold. |
| [Label](/manuals/label/) | Text / TextMeshPro | Defold possède une [extension RichText](https://defold.com/assets/richtext/) pour la mise en forme enrichie (comme TextMeshPro). |
| [Sound](/manuals/sound/) | AudioSource | Defold ne possède qu’une source sonore globale (non spatiale). Il existe une [extension FMOD](https://github.com/defold/extension-fmod) officielle pour Defold. |
| [Factory](/manuals/factory/) | Prefab Instantiate() | Dans Defold, une factory est un composant associé à un prototype (prefab) précis. |
| [Collection Factory](/manuals/collection-factory/) | - (Aucun composant directement équivalent) | Un composant factory de collection dans Defold peut créer plusieurs objets de jeu avec des relations parent-enfant en une seule fois. |
| [Collision Object](/manuals/physics-objects) | Rigidbody + Collider | Dans Defold, les objets physiques et les formes de collision sont réunis dans un même composant. |
| [Formes de collision](/manuals/physics-shapes/)  | BoxCollider / SphereCollider / CapsuleCollider | Dans Defold, les formes (boîte, sphère, capsule) sont configurées dans le composant Collision Object. Les deux moteurs prennent en charge les formes de collision issues de tilemaps et de données d’enveloppes convexes. |
| [Camera](/manuals/camera/) | Camera | Dans Unity, la caméra possède davantage de paramètres intégrés de rendu et de post-traitement, tandis que Defold laisse à l’utilisateur le soin de les contrôler par le script de rendu. |
| [GUI](/manuals/gui/) | UI Toolkit / Unity UI / uGUI Canvas | Le composant GUI de Defold est puissant et permet de créer des interfaces utilisateur complètes et des modèles. Unity ne possède pas de composant d’interface unique équivalent, mais plusieurs frameworks d’interface. Defold dispose également d’une extension pour [Extension](https://github.com/britzl/extension-imgui). |
| [GUI Script](/manuals/gui-script/) | Scripts Unity UI / uGUI | L’interface graphique de Defold peut être contrôlée par des scripts d’interface graphique à l’aide de l’API dédiée `gui`. |
| [Model](/manuals/model/) | MeshRenderer + Material | Dans Defold, un composant Model regroupe un fichier de modèle 3D, des textures et un matériau avec des shaders. |
| [Mesh](/manuals/mesh/) | MeshRenderer / MeshFilter / Maillage procédural | Dans Defold, Mesh est un composant permettant de gérer un ensemble de sommets par le code. Il ressemble au composant Model de Defold, mais opère à un niveau encore plus bas. |
| [ParticleFX](/manuals/particlefx/) | Particle System | L’éditeur de particules de Defold prend en charge les effets de particules 2D/3D avec de nombreuses propriétés et permet de les animer dans le temps à l’aide de courbes dans Curve Editor. Il ne propose ni Trails ni Collisions. |
| [Script](/manuals/script/) | Script | Les différences de programmation sont expliquées plus en détail ci-dessous. |

#### Extensions et composants personnalisés {#extensions-and-custom-components}

Defold possède également des composants officiels [Spine](/extension-spine/) et [Rive](/extension-rive/), disponibles sous forme d’extensions.

Vous pouvez également créer vos propres [composants personnalisés](https://github.com/defold/extension-simpledata) à l’aide d’extensions natives, comme ce [composant d’interpolation d’objets](https://github.com/indiesoftby/defold-object-interpolation) créé par la communauté.

Certains composants Unity n’ont pas d’équivalent prêt à l’emploi dans Defold, par exemple Audio Listener, Light, Terrain, LineRenderer, TrailRenderer, Cloth ou Animator. Toutefois, toutes ces fonctionnalités peuvent être implémentées dans des scripts et des solutions existent déjà, par exemple différents pipelines d’éclairage, le composant Mesh pour générer des maillages arbitraires (y compris des terrains), ou [Hyper Trails](https://defold.com/assets/hypertrails/) pour des effets de traînée personnalisables. Defold pourrait également ajouter de nouveaux composants intégrés à l’avenir, tels que des lumières.

### Ressources {#resources}

Certains composants nécessitent des **« ressources »**, comme dans Unity ; par exemple, les sprites et les modèles ont besoin de textures. Quelques-unes sont comparées dans le tableau ci-dessous :

| Defold | Unity | Différences |
|---|---|---|
| [Atlas](/manuals/atlas/) | Sprite Atlas / Texture2D | Defold possède également une [extension pour Texture Packer](https://defold.com/extension-texturepacker/). |
| [Source de tuiles](/manuals/tilesource/) | Tile Palette + Asset | Dans Defold, une source de tuiles peut servir de texture pour les tilemaps, mais aussi pour les sprites ou les particules. |
| [Font](/manuals/font/) | Font | Utilisée par le composant Label de Defold ou par les nœuds de texte des interfaces graphiques, comme Text/TextMeshPro dans Unity. |
| [Material](/manuals/material/) | Material | Dans Defold, les shaders portent les noms de programme de sommets et de programme de fragments. |

### Collection et scène {#collection-vs-scene}

Dans Defold, les objets de jeu et les composants peuvent être placés dans des fichiers séparés, comme les prefabs de Unity, ou être définis ensemble dans un fichier **« collection »**.

Une collection dans Defold est essentiellement un fichier texte contenant une description statique d’une scène. Ce n’est **pas** un objet présent à l’exécution. Elle définit uniquement les objets de jeu à instancier dans le jeu et les relations parent-enfant à établir entre eux.

#### Mondes de jeu {#game-worlds}

Les scènes Unity partagent par défaut le même état global du jeu et la même simulation physique, et donc le même *monde de jeu* (*game world*). Dans Defold, vous avez deux possibilités :
1. Instancier des objets de jeu à partir d’un fichier d’objet de jeu unique via une `Factory`, ou d’un fichier de collection via une `Collection Factory`, dans un *monde* donné déjà instancié, comme des prefabs.
2. Créer un *monde* de jeu distinct à l’exécution, avec ses propres objets de jeu, monde physique, opérations du moteur et espace de noms (namespace) d’adressage, à partir d’une collection chargée au démarrage ou via un composant `Collection Proxy`.

Les composants factory et les proxies de collection (collection proxy) sont également expliqués ci-dessous.
Pour en savoir plus sur les collections, consultez le [manuel des éléments de base](/manuals/building-blocks/#collections).

---

## Ressources et contenu du projet {#project-resources-and-assets}

Unity et Defold stockent tous deux le contenu du jeu dans le répertoire du projet, mais leur manière de suivre et de préparer les ressources diffère.

### Ressources du projet {#assets}

Unity conserve les ressources dans `Assets/` et génère des fichiers `.meta`. Defold n’utilise pas de fichiers meta. Dans Defold, le projet est simplement votre arborescence de dossiers, exactement telle qu’elle est sur le disque, et le panneau `Assets` la reflète toujours.

### Formats des ressources {#resource-formats}

Unity importe les ressources et les convertit vers d’autres formats en arrière-plan. Dans Defold, vous travaillez directement avec les ressources sources (`.png`, `.gltf`, `.wav`, `.ogg`, etc.) et les affectez aux `Components`.

Unity peut utiliser une image seule comme sprite. Dans Defold, les images peuvent être utilisées directement pour les modèles et les maillages, mais les sprites, interfaces graphiques, tilemaps et particules nécessitent un atlas (textures regroupées) ou une source de tuiles (tuiles disposées sur une grille).

La plupart des ressources de Defold sont stockées sous forme de texte, ce qui facilite la gestion de versions.

### Cache de bibliothèque {#library-cache}

Unity génère un dossier `Library/` pour les ressources importées. Defold n’a pas de répertoire de ce type ; les ressources sont traitées lors des builds, et les résultats sont mis en cache dans le dossier de build (avec, en option, des caches de build locaux ou distants).

---

## Écriture du code {#code-writing}

L’équivalent des scripts `MonoBehaviour` dans Defold est le composant Script, mais certaines différences méritent d’être connues.

### Lua {#lua}

Les scripts Defold sont écrits en [Lua](https://www.lua.org/), un langage multiparadigme à typage dynamique.

Il existe plusieurs types de scripts Lua : `*.script`, `*.gui_script`, `*.render_script`, `*.editor_script`, ainsi que les modules `*.lua`.

### Teal {#teal}

Defold permet d’utiliser des transpileurs qui produisent du code Lua, comme [Teal](https://teal-language.org/), un dialecte de Lua à typage statique, mais cette fonctionnalité est plus limitée et nécessite une configuration supplémentaire. Des précisions sont disponibles dans le [dépôt de l’extension Teal](https://github.com/defold/extension-teal).

### Extensions natives C++/C# {#cc-native-extensions}

Dans Defold, les extensions natives peuvent être écrites dans plusieurs autres langages : C, C++, C#, Objective-C, Java ou JS, selon la plateforme cible. Si vous êtes très à l’aise avec C#, il est techniquement possible de structurer la majeure partie de la logique de votre jeu dans une extension C# et de l’appeler simplement depuis un petit script Lua de démarrage, mais cela demande une connaissance avancée de l’API et n’est pas recommandé aux débutants.

Pour en savoir plus sur les extensions, consultez le [manuel des extensions natives de Defold](/manuals/extensions/).


### Des MonoBehaviours aux modules Lua {#from-monobehaviours-to-lua-modules}

Unity possède un modèle de script ouvert. Comme `MonoBehaviour` est le principal moyen d’ajouter des comportements dans l’éditeur, de nombreux projets Unity commencent avec un script de type contrôleur par objet de jeu important : `PlayerController`, `EnemyController`, `BulletController`, `GameManager`, `EnemyManager`, etc.

Defold est plus précis quant à son architecture par défaut. Un objet de jeu peut avoir un `.script`, mais il est rarement nécessaire de créer un script pour chaque objet de jeu. En effet, un seul script Defold peut contrôler des centaines ou des milliers d’autres objets et leurs composants, même s’ils ne possèdent aucun script, grâce aux puissants mécanismes d’adressage et d’échange de messages de Defold. Créer un script pour chaque objet de jeu est rarement nécessaire et peut entraîner une complexité contre-productive.

Pour réutiliser les comportements de jeu, les développeurs Unity s’orientent souvent vers la composition : de plus petits scripts `MonoBehaviour`, comme `Health.cs`, `Attack.cs` ou `EnemyFinder.cs`, sont attachés au même objet de jeu. Dans Defold, vous conservez généralement un seul `.script` attaché qui sert d’hôte ou de coordinateur, et placez la logique réutilisable dans des modules Lua ordinaires.

Dans Unity, cette composition peut ressembler à ceci :

```text
Player
├── PlayerMovement.cs
├── PlayerAttack.cs
├── EnemyFinder.cs
└── Health.cs
```

Dans Defold, les mêmes responsabilités sont souvent réparties entre un script attaché et des modules réutilisables :

```text
player.go
├── sprite
├── collisionobject
└── player.script

modules/
├── player_movement.lua
├── player_attack.lua
├── enemy_finder.lua
└── health.lua
```

Le `.script` attaché devient l’hôte ou le coordinateur. Les modules Lua contiennent la logique réutilisable, de la même manière que les petits scripts `MonoBehaviour` remplissent souvent une seule responsabilité dans Unity.

```lua
local movement = require "modules.player_movement"
local attack = require "modules.player_attack"
local finder = require "modules.enemy_finder"
local health = require "modules.health"

function init(self)
    self.movement = movement.new(self)
    self.attack = attack.new(self)
    self.finder = finder.new(self)
    self.health = health.new(self)
end

function update(self, dt)
    self.movement:update(dt)
    self.attack:update(dt)
    self.finder:update(dt)
end

function on_message(self, message_id, message, sender)
    self.health:on_message(message_id, message, sender)
    self.attack:on_message(message_id, message, sender)
end
```

La différence importante n’est pas que Defold empêche une architecture modulaire, mais l’endroit où s’effectue la composition et la façon dont le code du jeu communique :

| Unity | Defold |
|---|---|
| Attachez plusieurs scripts `MonoBehaviour` dans Inspector | Attachez un seul `.script` et composez les modules Lua dans le code |
| Utilisez `GetComponent<T>()` ou des champs sérialisés pour relier les comportements | Stockez les instances des modules dans `self` et utilisez des adresses et des messages entre les objets |
| Chaque composant peut avoir ses propres méthodes de cycle de vie | Le script hôte transmet les appels à `init()`, `update()`, `on_message()`, `final()`, etc. |
| De nombreux styles d’architecture sont possibles | La pratique courante est une composition explicite dans le code, orientée vers l’échange de messages |

Cela peut sembler inhabituel au début, surtout si vous avez l’habitude de configurer les comportements en ajoutant des composants dans Inspector. Dans Defold, de nombreux éléments que vous configureriez visuellement dans Unity peuvent être créés, reliés, activés, désactivés ou mis à jour par le code. Le système de messagerie de Defold aide à découpler la logique : l’expéditeur envoie des données à une adresse et le destinataire décide quoi en faire.

Cette approche, bien que recommandée, n’est pas imposée. Vous pouvez toujours écrire vos scripts comme vous le souhaitez, notamment en attachant plusieurs scripts par objet de jeu ou en vous rapprochant de la programmation orientée objet. Il existe même des bibliothèques pour vous y aider ([defold-oop](https://github.com/xiyoo0812/defold-oop) ou [lua-class](https://github.com/d954mas/lua-class)).

Pour de nombreux objets du même type, comme des projectiles, des ennemis, des particules, des tuiles ou des éléments interactifs simples, il est souvent préférable de les contrôler depuis un script système ou un script gestionnaire plutôt que de donner à chacun son propre script. Utilisez des scripts par objet lorsqu’un objet possède un état et un comportement propres qui le justifient. Utilisez des modules lorsque vous souhaitez réutiliser la logique. Utilisez des scripts système lorsqu’un seul script peut contrôler efficacement de nombreux objets.

Vous trouverez [ici](https://defold.com/examples/factory/spawn_manager/) un exemple montrant comment utiliser les propriétés de script, les factories, l’adressage et l’échange de messages de Defold pour contrôler plusieurs unités.

Manuels utiles sur l’écriture du code :
- [Manuel des scripts](/manuals/script/)
- [Écriture du code](/manuals/writing-code/)
- [Débogage](/manuals/debugging/)


### Éditeur de code intégré {#built-in-code-editor}

L’éditeur Defold comprend un éditeur de code intégré avec complétion du code, coloration syntaxique, consultation rapide de la documentation, analyse du code et débogueur intégré.

![Éditeur de code de Defold](/images/editor/code-editor.png)

### VS Code et les autres éditeurs {#vs-code-and-other-editors}

Vous pouvez toujours utiliser votre propre éditeur externe si vous le préférez. Tous les composants Defold et les fichiers associés sont au format texte, vous pouvez donc les modifier avec n’importe quel éditeur de texte, mais vous devez respecter leur format et la structure des éléments, car ils reposent sur Protobuf.

Si vous avez l’habitude de VS Code et souhaitez l’utiliser pour écrire le code de votre jeu, nous vous recommandons d’installer [Defold Kit](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) ou [Defold Buddy](https://marketplace.visualstudio.com/items?itemName=mikatuo.vscode-defold-ide) depuis Visual Studio Marketplace.

Vous pouvez également configurer les préférences de l’éditeur Defold pour ouvrir par défaut les fichiers texte dans VS Code (ou tout autre éditeur externe). Consultez les [préférences de l’éditeur](/manuals/editor-preferences/) pour en savoir plus.

### Shaders - GLSL {#shaders-glsl}

Defold utilise GLSL (OpenGL Shading Language) pour les shaders, `Vertex Programs` et `Fragment Programs`, comme Unity. Bien que Defold ne propose pas de Shader Graph comme Unity (ce qui peut être un inconvénient), vous pouvez toujours créer des shaders équivalents en écrivant du code.

Pour en savoir plus sur les shaders, consultez le [manuel des shaders](/manuals/shader).

#### Matériaux {#materials}

Defold utilise un concept de `Material` qui relie les shaders `.fp` et `.vp`, les échantillonneurs (textures) et d’autres éléments comme les attributs de sommets ou les constantes.

Pour en savoir plus sur les matériaux, consultez le [manuel des matériaux](/manuals/material).

---

## Système de messagerie {#messaging-system}

Dans Defold, les objets ne conservent pas de références directes les uns aux autres. Il n’y a pas de `GetComponent`, pas d’appels de méthodes entre scripts d’objets différents, ni d’accès global à la scène comme dans Unity.

Les scripts communiquent par échange de messages : vous envoyez des messages à d’autres scripts au lieu d’appeler des méthodes ou d’accéder directement aux composants. Chaque objet décide quoi faire des messages qu’il reçoit.

Cela peut sembler peu familier au début, mais favorise un couplage faible et réduit les fortes interdépendances.


### Envoi d’un message {#sending-a-message}

Dans Unity, la communication ressemble généralement à ceci :

```c#
var enemy = GameObject.Find("Enemy");
enemy.GetComponent<EnemyAI>().TakeDamage(10);
```

Les objets peuvent donc se référencer directement les uns les autres et appeler des méthodes sur d’autres scripts. Tous se trouvent dans un même espace de scène partagé.

Dans Defold, vous envoyez un message d’un script à un autre script (ou à un autre composant) :

```lua
msg.post("#my_component", "my_message", { my_name = "Defold" })
```

Et vous pouvez traiter ces messages dans un script :

```lua
function on_message(self, message_id, messsage)
    if message_id == hash("my_message") then
        print("Hello ", message.my_name)
    end
end
```

Ignorez `#` et `hash` pour le moment, nous y reviendrons plus tard. Le reste devrait être assez simple. Vous pouvez envoyer un message à n’importe quel composant (même au script lui-même) de n’importe quel objet de jeu instancié.

#### Composants autres que les scripts {#components-other-than-scripts}

Vous envoyez parfois des messages à des composants `Sprite` ou `Collision`, par exemple pour les activer ou les désactiver. Parfois, les `Components` envoient des messages à votre script, par exemple lorsqu’une collision se produit, pour que vous puissiez la traiter. Defold utilise le même système de messagerie en interne, pour les événements du moteur et les communications du jeu. 

Le système de messagerie ressemble quelque peu à SendMessage ou aux systèmes d’événements de Unity, bien que l’adressage et les conventions diffèrent.

Vous trouverez plus de précisions dans le [manuel de l’échange de messages](/manuals/message-passing/).

### Adressage {#addressing}

Les objets et les composants de Defold sont identifiés par des adresses appelées URL.

Chaque objet et composant instancié possède sa propre adresse unique, et vous n’avez pas besoin de parcourir un graphe de scène pour les trouver. L’adressage est ainsi explicite et direct.

Une URL simple dans Defold peut ressembler à ceci :
```lua
"/player"
```

C’est *conceptuellement* similaire à :
```c#
GameObject.Find("player")
```

Il est maintenant temps d’expliquer pourquoi `"/"` ou `"#"` étaient utilisés dans les adresses.

Une URL Defold (semblable à une [URL](https://en.wikipedia.org/wiki/URL)) est composée de trois parties :

```yaml
socket: /path #fragment
```

ou, pour reprendre la terminologie de Defold :

```yaml
collection: /gameobject #component 
```
Les espaces ont été ajoutés dans les descriptions ci-dessus uniquement pour séparer visuellement ces trois parties.

Pour le dire simplement :
1. `collection:` identifie le contexte de la collection, avec `:` à la fin.
2. `/path` identifie l’objet de jeu, avec `/` devant l’identifiant.
3. `#fragment` identifie le composant précis de cet objet (comme un script, un sprite ou un composant de collision), avec `#` devant l’identifiant.

#### Adresse statique {#static-address}

Ces identifiants sont déterminés à la création de chaque élément et ne changent jamais, même si vous modifiez les relations parent-enfant. Vous pouvez les définir dans la propriété `Id` des fichiers, ou les obtenir à l’exécution lors des appels à `factory.create` ou `collectionfactory.create`, au moment de l’instanciation.

#### Adressage relatif {#relative-addressing}

Vous n’avez pas toujours besoin d’utiliser une URL complète.

Si vous envoyez des messages au sein de la même collection (du même *monde*), vous pouvez omettre la partie socket :

```yaml
/gameobject #component
```
Si vous envoyez un message à un composant du même objet de jeu, vous pouvez également omettre la partie de l’objet de jeu :

```yaml
#component
```

Voici deux raccourcis utiles :
- `#` pour envoyer à ce composant *script*
- `.` pour envoyer à tous les composants de cet *objet de jeu*

L’adressage relatif et les raccourcis permettent d’écrire des URL réutilisables dans différents contextes et objets de jeu sans préciser les chemins complets.

### Messages aux interfaces graphiques et au rendu {#messaging-to-gui-and-render}

Comme Defold sépare le monde des interfaces graphiques de celui des objets de jeu, vous pouvez également envoyer des messages depuis les `.scripts` de vos objets de jeu vers les `.gui_scripts`.

Vous pouvez également envoyer des messages à des espaces de noms système spéciaux au moyen d’un identifiant commençant par `@`. Par exemple, le système de rendu peut être adressé via `@render` : vous pouvez l’utiliser pour contrôler certaines fonctionnalités de rendu intégrées, comme le changement de projection dans le script de rendu par défaut :

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

Vous trouverez plus de précisions dans le [manuel de l’adressage](/manuals/addressing/).

---

## Prefabs et instances {#prefabs-and-instances}

Unity peut instancier n’importe quel élément dans la scène, de manière statique ou dynamique, et Defold peut en faire autant. Dans Unity, vous prenez un prefab et appelez `Instantiate(prefab)`. Dans Defold, trois composants permettent d’instancier du contenu :

- `Factory` - instancie un **seul objet de jeu** à partir d’un prototype donné : un fichier `*.go` (prefab).
- `Collection Factory` - instancie un **ensemble d’objets de jeu** avec des relations parent-enfant à partir d’un prototype donné : un fichier `*.collection`.
- `Collection Proxy` - **charge** et instancie un nouveau *monde* à partir d’un fichier `*.collection`.

### Factory {#factory}

Une fois que vous avez défini un composant `Factory` dont la propriété `Prototype` pointe vers le fichier d’objet de jeu approprié, il suffit d’un appel dans le code pour créer une instance :

```lua
factory.create("#my_factory")
```

Cet appel utilise l’adresse du composant, ici un chemin relatif utilisant l’identifiant `"#my_factory"`.

Il renvoie l’identifiant de l’instance nouvellement créée. Si vous devez l’utiliser plus tard, il est donc utile de le stocker dans une variable :

```lua
local new_instance_id = factory.create("#my_factory")
```

N’oubliez pas que dans Defold, vous n’avez pas besoin de gérer manuellement un pool d’objets : le moteur s’en charge lui-même en interne.

Vous trouverez plus de précisions dans le [manuel des factories](/manuals/factory/). 

### Factory de collection {#collection-factory}

La différence entre les composants `Factory` et `Collection Factory` est que la factory de collection peut créer **plusieurs** objets de jeu à la fois et établir à leur création les relations parent-enfant définies dans le fichier `*.collection`.

Cette distinction n’existe pas dans Unity, qui ne possède aucun concept dédié correspondant à la factory de collection de Defold. L’analogie la plus proche est simplement un prefab imbriqué qui contient une hiérarchie d’objets.

Elle renvoie une **table** contenant les identifiants de toutes les instances créées :

```lua
local spawned_instances = collectionfactory.create("#my_collectionfactory")
```

Vous trouverez plus de précisions dans le [manuel des factories de collection](/manuals/collection-factory/).

#### Propriétés personnalisées des instances {#custom-properties-of-instances}

Lorsque vous appelez `factory.create()` ou `collectionfactory.create()`, vous pouvez également préciser des paramètres facultatifs comme la position, la rotation, l’échelle et les propriétés de script. Vous contrôlez ainsi exactement comment et où l’instance apparaît, ainsi que son comportement, par exemple :

```lua
local scale_2d = vmath.vector3(0.5, 0.5, 1.0)
factory.create("#my_factory", my_position, my_rotation, my_properties, scale_2d)
```

Dans l’ordre des arguments facultatifs, les propriétés sont suivies de l’échelle. Utilisez un `vector3` dont la composante Z est explicitement définie à `1.0` lorsque vous redimensionnez uniquement les axes X et Y d’un objet 2D ; une échelle numérique s’applique uniformément aux trois axes.

#### Chargement dynamique {#dynamic-loading}

Dans les composants `Factory` et `Collection Factory`, vous pouvez marquer un prototype pour le chargement dynamique des ressources afin que ses ressources volumineuses ne soient chargées en mémoire qu’en cas de besoin, puis déchargées lorsqu’elles ne sont plus utilisées.

Vous trouverez plus de précisions dans le [manuel de gestion des ressources](/manuals/resource/). 

### Proxy de collection {#collection-proxy}

Le `Collection Proxy` fait référence à un fichier `*.collection` précis, mais au lieu d’injecter les objets dans le *monde actuel* (comme les factories), il **charge et instancie un nouveau monde de jeu**. Cela ressemble au chargement d’une scène entière dans Unity, mais avec une séparation plus stricte.

Dans Unity, vous pourriez charger une scène de façon additive comme ceci :

```c#
SceneManager.LoadSceneAsync("Level2", LoadSceneMode.Additive);
```

Dans Defold, vous chargez la nouvelle collection en envoyant simplement un message au composant `Collection Proxy` :

```lua
msg.post("#myproxy", "load")
```

1. Lorsque vous envoyez au proxy un message `"load"` (ou `"async_load"` pour un chargement asynchrone), le moteur alloue un nouveau monde, y instancie tous les éléments de cette collection et le garde isolé.
2. Une fois le chargement terminé, le proxy renvoie un message `"proxy_loaded"` indiquant que le monde est prêt.
3. Vous envoyez ensuite généralement les messages `"init"` et `"enable"` pour que les objets de ce nouveau monde commencent leur cycle de vie normal.

Pour communiquer entre les mondes chargés, vous devez utiliser des messages explicites avec des URL qui incluent le nom du monde (`collection:`, la première partie de l’URL).

Cette isolation peut être un avantage considérable pour implémenter des transitions entre niveaux, des mini-jeux ou de grands systèmes modulaires, car elle évite les interactions involontaires et permet également de contrôler séparément le rythme des mises à jour si nécessaire (par exemple pour une pause ou un ralenti).

Si vous avez déjà utilisé plusieurs scènes dans Unity et aviez besoin qu’elles se comportent de façon indépendante, considérez le `Collection Proxy` comme un moyen d’appliquer directement ce concept dans Defold.

Vous trouverez plus de précisions dans le [manuel des proxies de collection](/manuals/collection-proxy/).

---

## Cycle de vie de l’application {#application-lifecycle}

Vous connaissez les événements du cycle de vie de Unity : `Awake`, `Start`, `Update`, `FixedUpdate`, `LateUpdate`, `OnDestroy` ou `OnApplicationQuit`.

Defold possède également un cycle de vie de l’application bien défini, mais les concepts et la terminologie diffèrent. Defold expose les étapes du cycle de vie au moyen d’un ensemble de callbacks Lua prédéfinis, appelés par le moteur lors de l’initialisation, à chaque image et lors de la finalisation.

Voici une comparaison :

| Defold | Unity | Commentaire |
|-|-|-|
| `init()` | `Awake()` / `Start()` / `OnEnable()`| Defold possède un seul point d’entrée et callback d’initialisation : init(). Il est appelé pour chaque composant à sa création. |
| `on_input` | Méthodes d’entrée | Defold reçoit les entrées lorsque [le focus d’entrée est attribué au script](/manuals/input/#input-focus). Elles sont traitées en premier dans la boucle de mise à jour. |
| `fixed_update()` | `FixedUpdate()` | Appelé à pas de temps fixe. Pour l’activer dans Defold, vous devez définir `Use Fixed Timestep` - [précisions](https://defold.com/manuals/project-settings/#use-fixed-timestep). Depuis la version 1.12.0, il s’exécute avant `update()`. |
| `update()` | `Update()` | Appelé une fois par image avec le temps écoulé depuis l’image précédente. |
| `late_update()` | `LateUpdate()` | Appelé après `update()`, juste avant le rendu de l’image. Disponible depuis la version 1.12.0. |
| `on_message` | Réception des messages | Callback principal de Defold pour recevoir les messages. Il est traité dès qu’un message se trouve dans une file d’attente. |
| `final` | `OnDisable` / `OnDestroy` / `OnApplicationQuit` | Defold appelle les callbacks `final()` de chaque composant lorsque son objet de jeu est détruit à l’exécution (avec `go.delete()`) ou que le monde ou la collection est déchargé, ainsi qu’à la fermeture de l’application pour tous les objets restants. |

::: sidenote
N’oubliez pas que Defold ne garantit aucun ordre d’exécution entre les composants lorsque plusieurs sont initialisés, mis à jour ou supprimés à la fois. Une conception découplée est encouragée.

### Initialisation {#initialization}

Considérez `init()` de Defold comme une combinaison d’éléments de `Awake()`, `Start()` et `OnEnable()` de Unity en un seul point d’entrée, où le moteur a déjà tout mis en place et où vous pouvez préparer l’état de votre composant en toute sécurité.

### Quand les messages sont-ils traités ? {#when-messages-are-handled}

Comme vous pouvez déjà envoyer des messages dans `init()`, les messages sont distribués une première fois juste après l’initialisation.

Les messages sont ensuite traités après chaque boucle de traitement interne, chaque fois qu’un élément se trouve dans une file d’attente. Ainsi, `on_message()` peut, par exemple, être appelé plusieurs fois au cours d’une boucle de mise à jour.

### Boucle de mise à jour {#update-loop}

À chaque image, Defold exécute une série d’opérations : traitement des entrées, distribution des messages, déclenchement des mises à jour des scripts et des interfaces graphiques, application de la physique et des transformations, puis rendu graphique.

### Finalisation {#finalization}

Dans Defold, le nettoyage est toujours lié à la suppression ou au déchargement du monde, et votre seul hook de sortie par composant est `final()`.

Une différence subtile avec le modèle de Unity est l’absence de distinction entre la désactivation d’un composant et la fermeture de l’application entière.

### Rendu {#rendering}

Le script de rendu (`*.render_script`) fait partie du pipeline de rendu, qui participe également au cycle de vie avec ses propres callbacks `init()`, `update()` et `on_message()`. Ceux-ci opèrent toutefois sur le thread de rendu et sont distincts de la logique des scripts d’objets de jeu et d’interfaces graphiques.

Pour en savoir plus, consultez le [manuel du cycle de vie de l’application](/manuals/application-lifecycle/).

---

## Interface graphique {#gui}

L’interface graphique de Defold est un framework complet et unique consacré aux interfaces utilisateur : menus, superpositions, boîtes de dialogue et autres éléments, comme UI Toolkit ou uGUI avec Canvas.

GUI est un composant distinct des objets de jeu et des collections. Au lieu d’objets de jeu, vous utilisez des nœuds d’interface graphique organisés dans une hiérarchie et pilotés par un script d’interface graphique.

### Nœuds d’interface graphique {#gui-nodes}

Lorsque vous ouvrez un fichier de composant `*.gui` dans Defold, vous disposez d’un canevas sur lequel placer des `"GUI nodes"`. Ce sont les éléments de base de l’interface graphique. Vous pouvez ajouter des nœuds d’interface graphique des types suivants :

- Box (forme rectangulaire avec une texture)
- Text (avec n’importe quelle police)
- Pie (élément en forme de secteur avec un remplissage radial et une texture)
- ParticleFX
- Template (un autre fichier `.gui` entier imbriqué, comme un prefab d’interface graphique)
- ainsi qu’un nœud Spine, si vous utilisez l’extension Spine.

### Script d’interface graphique {#gui-script}

Le composant GUI possède une propriété spéciale pour les scripts d’interface graphique : vous lui affectez un fichier `*.gui_script` par composant, ce qui permet de modifier son comportement. Il est donc très similaire aux scripts ordinaires, sauf qu’il n’utilise pas l’espace de noms `go.*` (réservé aux scripts d’objets de jeu). Il utilise à la place l’API d’un espace de noms spécial, `gui.*`, qui fonctionne uniquement dans les scripts d’interface graphique (`*.gui_script`). Vous pouvez le voir comme une scène distincte, à la manière de Unity UI (uGUI) avec Canvas.

### Rendu de l’interface graphique {#gui-rendering}

Les éléments d’interface graphique sont rendus indépendamment de la caméra du jeu, généralement dans l’espace écran, mais ce comportement peut être modifié dans des pipelines de rendu personnalisés.

Pour en savoir plus, consultez le [manuel de l’interface graphique](/manuals/gui/).

## Où sont les Sorting Layers ? {#where-are-sorting-layers}

C’est une source de confusion très courante lors de la migration depuis Unity.

Les composants GUI possèdent des `Layers` dont le fonctionnement est presque identique aux « Sorting Layers » de Unity, mais il n’existe pas d’équivalent direct pour les autres composants, comme `Sprites`, `Tilemaps`, `Models`, etc.

Vous combinez généralement les éléments suivants :
- Un ordre fin selon l’axe Z avec une caméra par défaut, ou selon la profondeur avec un composant Camera.
- Un ordre global défini par le script de rendu à l’aide de prédicats de rendu, pour sélectionner les éléments à dessiner selon les étiquettes des matériaux.

Vous ne devriez toutefois pas reproduire les Sorting Layers de Unity avec une multitude d’étiquettes, car dans Defold, les étiquettes sont un mécanisme qui agit au niveau du rendu. En abuser peut empêcher le regroupement des appels de rendu et augmenter le surcoût du dessin.

---

## Pour aller plus loin {#where-to-go-from-here}

- [Exemples Defold](/examples)
- [Tutoriels](/tutorials)
- [Manuels](/manuals)
- [Références de l’API](/ref/go)
- [FAQ](/faq/faq)

Si vous avez des questions ou êtes bloqué, le [forum Defold](//forum.defold.com) ou [Discord](https://defold.com/discord/) sont de très bons endroits pour demander de l’aide.
