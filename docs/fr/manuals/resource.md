---
title: Gestion des ressources dans Defold
brief: Ce manuel explique comment Defold gère automatiquement les ressources et comment vous pouvez gérer manuellement leur chargement pour respecter les contraintes d'empreinte mémoire et de taille du bundle.
---

# Gestion des ressources {#resource-management}

Si vous créez un tout petit jeu, les limitations de la plateforme cible (empreinte mémoire, taille du bundle, puissance de calcul et consommation de la batterie) ne vous poseront peut-être jamais de problème. En revanche, pour des jeux plus volumineux, en particulier sur les appareils portables, la consommation de mémoire sera probablement l'une des contraintes les plus importantes. Une équipe expérimentée établira soigneusement des budgets de ressources en fonction des contraintes de la plateforme. Defold propose un ensemble de fonctionnalités pour vous aider à gérer la mémoire et la taille du bundle. Ce manuel présente ces fonctionnalités.

## L'arborescence statique des ressources {#the-static-resource-tree}

Lorsque vous compilez un jeu dans Defold, vous déclarez statiquement l'arborescence des ressources. Chaque élément du jeu est relié à cette arborescence, à partir de la collection bootstrap (généralement nommée "main.collection"). L'arborescence des ressources suit chaque référence et inclut toutes les ressources associées à ces références :

- Données des objets de jeu (game object) et des composants (component) (atlas, sons, etc.).
- Prototypes des composants factory (objets de jeu et collections).
- Références des composants proxy de collection (collection proxy) (collections).
- [Ressources personnalisées](/manuals/project-settings/#custom-resources) déclarées dans *game.project*.

![Arborescence des ressources](images/resource/resource_tree.png)

::: sidenote
Defold propose également le concept de [ressources du bundle](/manuals/project-settings/#bundle-resources). Ces ressources sont incluses dans le bundle de l'application, mais ne font pas partie de l'arborescence des ressources. Elles peuvent aller de fichiers auxiliaires propres à une plateforme à des fichiers externes [chargés depuis le système de fichiers](/manuals/file-access/#how-to-access-files-bundled-with-the-application) et utilisés par votre jeu (par exemple, des banques de sons FMOD).
:::

Lorsque le jeu est *regroupé dans un bundle*, seul ce qui figure dans l'arborescence des ressources est inclus. Tout ce qui n'est pas référencé dans l'arborescence est exclu. Il n'est pas nécessaire de sélectionner manuellement les éléments à inclure dans le bundle ou à en exclure.

Lorsque le jeu est *exécuté*, le moteur part de la racine bootstrap de l'arborescence et charge les ressources en mémoire :

- Chaque collection référencée et son contenu.
- Les objets de jeu et les données des composants.
- Les prototypes des composants factory (objets de jeu et collections).

Cependant, le moteur ne charge pas automatiquement les types de ressources référencées suivants à l'exécution :

- Les collections de mondes de jeu (game world) référencées par des proxys de collection. Les mondes de jeu sont relativement volumineux, vous devrez donc déclencher manuellement leur chargement et leur déchargement dans le code. Consultez [le manuel des proxys de collection](/manuals/collection-proxy) pour plus de détails.
- Les fichiers ajoutés via le paramètre *Custom Resources* dans *game.project*. Ces fichiers sont chargés manuellement avec la fonction [`sys.load_resource()`](/ref/sys/#sys.load_resource).

Vous pouvez modifier la manière dont Defold inclut les ressources dans le bundle et les charge par défaut afin de contrôler précisément comment et quand elles entrent en mémoire.

![Chargement des ressources](images/resource/loading.png)

## Chargement dynamique des ressources des factories {#dynamically-loading-factory-resources}

Les ressources référencées par les composants factory sont normalement chargées en mémoire au chargement du composant. Elles sont alors prêtes à être instanciées dans le jeu dès que la factory existe dans l'environnement d'exécution. Pour modifier ce comportement par défaut et différer le chargement des ressources d'une factory, il vous suffit de cocher sa case *Load Dynamically*.

![Chargement dynamique](images/resource/load_dynamically.png)

Lorsque cette case est cochée, le moteur inclut toujours les ressources référencées dans le bundle du jeu, mais il ne charge pas automatiquement les ressources de la factory. Vous avez alors deux possibilités :

1. Appelez [`factory.create()`](/ref/factory/#factory.create) ou [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create) lorsque vous souhaitez créer des objets. Cela charge les ressources de manière synchrone, puis crée de nouvelles instances.
2. Appelez [`factory.load()`](/ref/factory/#factory.load) ou [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load) pour charger les ressources de manière asynchrone. Lorsque les ressources sont prêtes à être instanciées, vous recevez un callback.

Consultez le [manuel des factories](/manuals/factory) et le [manuel des factories de collection](/manuals/collection-factory) pour en savoir plus sur ce fonctionnement.

## Déchargement des ressources chargées dynamiquement {#unloading-dynamically-loaded-resources}

Defold maintient un compteur de références pour chaque ressource. Si le compteur d'une ressource atteint zéro, cela signifie que plus rien n'y fait référence. La ressource est alors automatiquement déchargée de la mémoire. Par exemple, si vous supprimez tous les objets créés par une factory et que vous supprimez aussi l'objet contenant le composant factory, les ressources précédemment référencées par la factory sont déchargées de la mémoire.

Pour les factories dont la case *Load Dynamically* est cochée, vous pouvez appeler la fonction [`factory.unload()`](/ref/factory/#factory.unload) ou [`collectionfactory.unload()`](/ref/collectionfactory/#collectionfactory.unload). Cet appel supprime la référence du composant factory à la ressource. Si plus rien d'autre ne fait référence à cette ressource (par exemple, si tous les objets créés ont été supprimés), elle est déchargée de la mémoire.

## Exclusion de ressources du bundle {#excluding-resources-from-bundle}

Avec les proxys de collection, vous pouvez exclure du processus de création du bundle toutes les ressources auxquelles le composant fait référence. Cela est utile si vous devez réduire au minimum la taille du bundle. Par exemple, lorsque vous exécutez des jeux sur le Web en HTML5, le navigateur télécharge l'intégralité du bundle avant d'exécuter le jeu.

![Exclusion](images/resource/exclude.png)

En cochant *Exclude* pour un proxy de collection, vous excluez la ressource référencée du bundle du jeu. Vous pouvez alors stocker les collections exclues sur un service de stockage cloud de votre choix. Le [manuel de mise à jour à chaud](/manuals/live-update/) explique le fonctionnement de cette fonctionnalité.
