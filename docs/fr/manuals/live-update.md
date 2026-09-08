---
title: Contenu Live Update dans Defold
brief: La fonctionnalité Live Update fournit un mécanisme qui permet au moteur d'exécution de récupérer et de stocker dans le bundle de l'application des ressources volontairement exclues du bundle lors du build. Ce manuel explique son fonctionnement.
---

# Mise à jour en direct (Live Update) {#live-update}

Lors de la création du bundle d'un jeu, Defold regroupe toutes les ressources du jeu dans le paquet propre à la plateforme cible. Dans la plupart des cas, ce comportement est préférable, car le moteur en cours d'exécution a un accès immédiat à toutes les ressources et peut les charger rapidement depuis le support de stockage. Cependant, il existe des situations où vous souhaitez reporter le chargement de certaines ressources à une étape ultérieure. Par exemple :

- Votre jeu comporte une série d'épisodes et vous souhaitez n'inclure que le premier, afin que les joueurs puissent l'essayer avant de décider s'ils veulent poursuivre le reste du jeu.
- Votre jeu cible HTML5. Dans le navigateur, charger une application depuis le stockage signifie que la totalité du paquet de l'application doit être téléchargée avant le démarrage. Sur une telle plateforme, vous pouvez souhaiter envoyer un paquet de démarrage minimal pour lancer rapidement l'application, avant de télécharger le reste des ressources du jeu.
- Votre jeu contient des ressources très volumineuses (images, vidéos, etc.) dont vous souhaitez reporter le téléchargement jusqu'au moment où elles vont apparaître dans le jeu. Cela permet de réduire la taille de l'installation.

La fonctionnalité Live Update étend le concept de proxy de collection (collection proxy) avec un mécanisme qui permet au moteur d'exécution de récupérer et de stocker dans le bundle de l'application des ressources volontairement exclues du bundle lors du build.

Elle vous permet de répartir votre contenu dans plusieurs archives :

* _Archive de base_
* Fichiers communs aux niveaux
* Lot de niveaux 1
* Lot de niveaux 2
* ...

## Préparer le contenu pour Live Update {#preparing-content-for-live-update}

Supposons que nous créions un jeu contenant des ressources d'images volumineuses en haute résolution. Le jeu conserve ces images dans des collections contenant un objet de jeu (game object) et un sprite affichant l'image :

![Collection Mona Lisa](images/live-update/mona-lisa.png)

Pour que le moteur charge une telle collection dynamiquement, nous pouvons simplement ajouter un composant (component) de type proxy de collection et le faire pointer vers *`monalisa.collection`*. Le jeu peut alors choisir quand charger le contenu de la collection depuis le stockage vers la mémoire, en envoyant un message `load` au proxy de collection. Cependant, nous voulons aller plus loin et contrôler nous-mêmes le chargement des ressources contenues dans la collection.

Pour cela, il suffit de cocher la case *Exclude* dans les propriétés du proxy de collection, afin d'indiquer à Defold d'exclure tout le contenu de *`monalisa.collection`* lors de la création du bundle de l'application.

::: important
Les ressources référencées par le paquet de base du jeu ne seront pas exclues.
:::

![Proxy de collection exclu](images/live-update/proxy-excluded.png)

## Paramètres de Live Update {#live-update-settings}

Lorsque Defold crée un bundle d'application, il doit stocker les ressources exclues quelque part. Les paramètres du projet pour Live Update déterminent l'emplacement de ces ressources. Vous les trouverez sous <kbd>Project ▸ Live update Settings...</kbd>. Un fichier de paramètres sera créé s'il n'en existe pas encore. Dans *game.project*, sélectionnez le fichier de paramètres Live Update à utiliser lors de la création du bundle. Vous pouvez ainsi utiliser des paramètres Live Update différents selon les environnements, par exemple la production, l'assurance qualité, le développement, etc.

![Paramètres de Live Update](images/live-update/05-liveupdate-settings-zip.png)

Defold propose actuellement trois méthodes de stockage des ressources. Choisissez la méthode dans la liste déroulante *Mode* de la fenêtre des paramètres :

`Zip`
: Cette option indique à Defold de créer une archive Zip contenant les ressources exclues. L'archive est enregistrée à l'emplacement indiqué par le paramètre *Export path* et peut être montée à l'exécution à l'aide d'un URI `zip:` et de `liveupdate.add_mount()`.

`Folder`  
: Cette option indique à Defold de créer un dossier contenant toutes les ressources exclues. Elle est utile lorsque vous devez effectuer un traitement supplémentaire sur les fichiers avant de les téléverser ou de les empaqueter. Un dossier de fichiers compilés individuels, placés aux chemins de ressources attendus, peut être monté à l'exécution à l'aide d'un URI `file:`.

`Amazon`
: Cette option indique à Defold de téléverser automatiquement les ressources exclues dans un compartiment S3 d'Amazon Web Service (AWS). Renseignez le nom de votre profil AWS dans *Credential profile*, sélectionnez le *Bucket* approprié et indiquez un nom dans *Prefix*. Vous trouverez plus d'informations sur la configuration d'un compte AWS dans ce [guide AWS](/manuals/live-update-aws)

## Créer un bundle avec Live Update {#bundling-with-live-update}

::: important
La compilation et l'exécution depuis l'éditeur (<kbd>Project ▸ Build</kbd>) ne prennent pas en charge Live Update. Pour tester Live Update, vous devez créer un bundle du projet.
:::

Créer un bundle avec Live Update est simple. Sélectionnez <kbd>Project ▸ Bundle ▸ ...</kbd>, puis la plateforme pour laquelle vous souhaitez créer un bundle d'application. La boîte de dialogue de création de bundle s'ouvre :

![Créer un bundle d'application avec Live Update](images/live-update/bundle-app.png)

Lors de la création du bundle, les ressources exclues sont omises du bundle de l'application. En cochant la case *Publish Live update content*, vous indiquez à Defold de téléverser les ressources exclues vers Amazon ou de créer une archive Zip, selon la configuration de vos paramètres Live Update (voir ci-dessus). Le contenu Live Update publié inclut toujours `liveupdate.game.dmanifest`, qui contient la liste complète des ressources nécessaires à la distribution à distance.

Lors de la publication du contenu Live Update, Defold supprime automatiquement du fichier `game.dmanifest` inclus dans le bundle les entrées propres à Live Update, tandis que le fichier `liveupdate.game.dmanifest` publié conserve la liste complète des ressources. Cela réduit la taille du bundle et l'utilisation de la mémoire à l'exécution. L'ancien paramètre `liveupdate.exclude_entries_from_main_manifest` a été supprimé ; toute entrée encore présente dans le projet est ignorée.

Dans le flux de travail fondé sur les archives, `collectionproxy.get_resources()` renvoie `{}` tant que l'archive concernée n'a pas été montée. Après le montage, cette fonction renvoie les hachages des ressources de ce proxy.

Cliquez sur *Package* et sélectionnez un emplacement pour le bundle de l'application. Vous pouvez maintenant démarrer l'application et vérifier que tout fonctionne comme prévu.

## Les archives .zip {#the-zip-archives}

Un fichier .zip Live Update contient les fichiers qui ont été exclus du paquet de base du jeu.

Bien que notre chaîne de traitement actuelle ne prenne en charge que la création d'un seul fichier .zip, il est possible de diviser ce fichier zip en plusieurs fichiers .zip plus petits. Cela permet de proposer des téléchargements plus petits pour un jeu : lots de niveaux, contenu saisonnier, etc. Chaque fichier .zip contient également un fichier manifeste qui décrit les métadonnées de chacune des ressources qu'il contient.

## Diviser les archives .zip {#splitting-zip-archives}

Il est souvent souhaitable de répartir le contenu exclu dans plusieurs archives plus petites pour contrôler plus finement l'utilisation des ressources. Vous pouvez, par exemple, diviser un jeu organisé en niveaux en plusieurs lots de niveaux. Vous pouvez aussi placer les décorations d'interface propres à différentes fêtes dans des archives distinctes, et ne charger et monter que le thème correspondant à la période actuelle du calendrier.

Le graphe des ressources est stocké dans `build/default/game.graph.json` et généré automatiquement à chaque création de bundle du projet. Le fichier généré contient une liste de toutes les ressources du projet et des dépendances de chacune. Exemple d'entrée :

```json
{
  "path" : "/game/player.goc",
  "hexDigest" : "caa342ec99794de45b63735b203e83ba60d7e5a1",
  "children" : [ "/game/ship.spritec", "/game/player.scriptc" ]
}
```

Chaque entrée possède un champ `path` qui représente le chemin unique de la ressource dans le projet. Le champ `hexDigest` représente l'empreinte cryptographique de la ressource et sert de nom de fichier dans l'archive .zip Live Update. Enfin, le champ `children` contient la liste des autres dépendances dont cette ressource dépend. Dans l'exemple ci-dessus, `/game/player.goc` dépend d'un sprite et d'un composant script.

Vous pouvez analyser le fichier `game.graph.json` et utiliser ces informations pour identifier des groupes d'entrées dans le graphe des ressources, puis stocker les ressources correspondantes dans des archives distinctes avec le fichier manifeste d'origine (le fichier manifeste sera réduit à l'exécution pour ne contenir que les fichiers présents dans l'archive).

## Live Update sur Android {#live-update-on-android}

Vous pouvez utiliser Play Asset Delivery pour télécharger et monter du contenu Live Update. Pour en savoir plus, consultez [le manuel officiel](https://defold.com/extension-pad/).

## Vérification du contenu {#content-verification}

L'une des principales fonctionnalités du système Live Update est de pouvoir utiliser de nombreuses archives de contenu, provenant éventuellement de différentes versions de Defold.

Par défaut, `liveupdate.add_mount()` ajoute une vérification de la version du moteur lors de l'ajout d'un point de montage.
Cela signifie que l'archive de base du jeu et les archives Live Update doivent être créées en même temps, avec la même version du moteur, à l'aide de l'option de création de bundle. Cela invalidera toutes les archives précédemment téléchargées par le client, qui devra télécharger à nouveau le contenu.

Ce comportement peut être désactivé à l'aide d'un indicateur dans les options.
Une fois cette vérification désactivée, la responsabilité de vérifier le contenu revient entièrement au développeur, qui doit garantir que chaque archive Live Update fonctionnera avec le moteur en cours d'exécution.

Nous vous recommandons de stocker des métadonnées pour chaque point de montage, afin que l'application puisse décider si le paquet doit rester monté. Validez-le après l'ajout du point de montage, y compris lorsque l'application ajoute de nouveau les points de montage dont elle a besoin au démarrage.
Une façon de procéder consiste à ajouter un fichier supplémentaire à l'archive zip après la création du bundle du jeu. Par exemple, insérez un fichier `metadata.json` contenant les informations dont le jeu a besoin, puis récupérez-le avec `sys.load_resource("/metadata.json")` après le montage. _Utilisez un chemin de ressource unique pour les données personnalisées de chaque point de montage, sinon la recherche de ressource renverra le fichier du point de montage ayant la priorité la plus élevée._

À défaut, vous risquez de vous retrouver avec du contenu totalement incompatible avec le moteur, ce qui forcera celui-ci à quitter.

## Points de montage {#mounts}

Le système Live Update peut utiliser plusieurs archives de contenu en même temps.
Chaque archive est « montée » dans le système de ressources du moteur, avec un nom et une priorité.

Si deux archives contiennent le même fichier `sprite.texturec`, le moteur chargera celui du point de montage ayant la priorité la plus élevée.

Le moteur ne conserve aucune référence à une ressource dans un point de montage. Une fois qu'une ressource est chargée en mémoire, l'archive peut être démontée. La ressource restera en mémoire jusqu'à son déchargement.

Les points de montage sont actifs uniquement pour la session actuelle du moteur. Après un redémarrage, l'application doit rappeler `liveupdate.add_mount()` pour chaque paquet dont elle a besoin. Stockez l'emplacement du paquet, le nom du point de montage et sa priorité dans des données persistantes gérées par l'application si ces choix doivent être conservés d'une session à l'autre.

::: sidenote
Monter une archive Zip ou un dossier ne copie ni ne déplace cet élément. Le contenu monté doit rester à l'emplacement indiqué tant que le point de montage est utilisé.
:::

## Utiliser Live Update dans les scripts {#scripting-with-live-update}

Pour utiliser le contenu Live Update, vous devez télécharger les données et les monter dans votre jeu.
Pour en savoir plus, consultez [l'utilisation de Live Update dans les scripts](/manuals/live-update-scripting).

## Points à prendre en compte lors du développement {#development-caveats}

Débogage
: Lorsque vous exécutez une version de votre jeu sous forme de bundle, vous n'avez pas d'accès direct à une console. Cela pose des problèmes pour le débogage. Cependant, vous pouvez lancer l'application depuis la ligne de commande ou en double-cliquant directement sur le fichier exécutable du bundle :

  ![Exécution d'une application sous forme de bundle](images/live-update/run-bundle.png)

  Le jeu démarre alors avec une fenêtre de shell qui affiche la sortie de toutes les instructions `print()` :

  ![Sortie de la console](images/live-update/run-bundle-console.png)

Forcer un nouveau téléchargement des ressources
: Le développeur peut télécharger le contenu dans le fichier ou le dossier de son choix, mais celui-ci se trouve souvent sous le chemin de l'application. L'emplacement du dossier de données de l'application dépend du système d'exploitation. Vous pouvez le trouver avec `print(sys.get_save_file("", ""))`. Pour forcer un téléchargement, supprimez le paquet téléchargé et l'entrée correspondante dans tout état géré par l'application. Il n'existe aucune liste de points de montage gérée par le moteur à supprimer ; les points de montage ne sont pas conservés après un redémarrage.

  ![Stockage local](images/live-update/local-storage.png)
