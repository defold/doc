---
title: Travailler hors ligne
brief: Ce manuel décrit comment travailler hors ligne sur des projets comportant des dépendances, en particulier des extensions natives
---

# Travailler hors ligne {#working-offline}

Dans la plupart des cas, Defold ne nécessite pas de connexion Internet pour fonctionner. Il existe cependant quelques situations dans lesquelles une connexion Internet est nécessaire :

* Mises à jour automatiques
* Signalement de problèmes
* Récupération des dépendances
* Compilation d'extensions natives


## Mises à jour automatiques {#automatic-updates}

Defold vérifie régulièrement si de nouvelles mises à jour sont disponibles. Ces vérifications s'effectuent auprès du [site officiel de téléchargement](https://d.defold.com). Si une mise à jour est détectée, elle est téléchargée automatiquement.

Si vous ne disposez d'une connexion Internet que pendant des périodes limitées et ne souhaitez pas attendre le déclenchement de la mise à jour automatique, vous pouvez télécharger manuellement les nouvelles versions de Defold depuis le [site officiel de téléchargement](https://d.defold.com).


## Signalement de problèmes {#reporting-issues}

Si un problème est détecté dans l'éditeur, vous avez la possibilité de le signaler dans le système de suivi des problèmes de Defold. Ce système est [hébergé sur GitHub](https://www.github.com/defold/editor2-issues), ce qui signifie que vous avez besoin d'une connexion Internet pour signaler le problème.

Si vous rencontrez un problème hors ligne, vous pouvez le signaler manuellement plus tard à l'aide de [l'option Report Issue du menu Help](/manuals/getting-help/#report-a-problem-from-the-editor) de l'éditeur.


## Récupération des dépendances {#fetching-dependencies}

Defold propose un système permettant aux développeurs de partager du code et des ressources à l'aide de ce que l'on appelle des [projets de bibliothèque](/manuals/libraries/). Les bibliothèques sont des fichiers zip qui peuvent être hébergés n'importe où en ligne. Vous trouverez généralement les projets de bibliothèque Defold sur GitHub et dans d'autres dépôts de code source en ligne.

Un projet peut ajouter une bibliothèque en tant que [dépendance dans les paramètres du projet](/manuals/project-settings/#dependencies). Les dépendances sont téléchargées ou mises à jour à l'ouverture du projet, ou à tout moment lorsque l'option *Fetch Libraries* est sélectionnée dans le menu *Project*.

Si vous devez travailler hors ligne sur plusieurs projets, vous pouvez télécharger les dépendances à l'avance, puis les partager à l'aide d'un serveur local. Les dépendances hébergées sur GitHub sont généralement disponibles dans l'onglet Releases du dépôt du projet :

![URL d'une bibliothèque sur GitHub](images/libraries/libraries_library_url_github.png)

Vous pouvez utiliser Python pour créer facilement un serveur local :

    python -m SimpleHTTPServer

Cela crée un serveur dans le répertoire courant qui sert les fichiers sur `localhost:8000`. Si le répertoire courant contient des dépendances téléchargées, vous pouvez les ajouter à votre fichier *game.project* :

    http://localhost:8000/extension-fbinstant-4.1.1.zip


## Compilation d'extensions natives {#building-native-extensions}

Defold propose un système permettant aux développeurs d'ajouter du code natif pour étendre les fonctionnalités du moteur, appelé [extensions natives](/manuals/extensions/). Defold permet de commencer à utiliser les extensions natives sans aucune configuration grâce à une solution de build dans le cloud.

La première fois que vous compilez un projet contenant une extension native, le code natif est compilé dans un moteur de jeu Defold personnalisé sur les serveurs de build de Defold, puis ce moteur est renvoyé à votre PC. Le moteur personnalisé est mis en cache dans votre projet et réutilisé pour les builds suivants tant que vous n'ajoutez, ne supprimez ni ne modifiez aucune extension native et que vous ne mettez pas à jour l'éditeur.

Si vous devez travailler hors ligne et que votre projet contient des extensions natives, vous devez vous assurer de réussir au moins un build afin que votre projet contienne une copie en cache du moteur personnalisé.
