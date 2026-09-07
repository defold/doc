---
title: Débogage avec ZeroBrane Studio
brief: Ce manuel explique comment utiliser ZeroBrane Studio pour déboguer du code Lua dans Defold.
---

# Débogage des scripts Lua avec ZeroBrane Studio {#debugging-lua-scripts-with-zerobrane-studio}

Defold dispose d'un débogueur intégré, mais vous pouvez aussi utiliser l'IDE Lua libre et gratuit _ZeroBrane Studio_ comme débogueur externe. ZeroBrane Studio doit être installé pour utiliser ses fonctionnalités de débogage. Le programme est multiplateforme et fonctionne aussi bien sur macOS que sur Windows.

Téléchargez « ZeroBrane Studio » depuis http://studio.zerobrane.com

## Configuration de ZeroBrane {#zerobrane-configuration}

Pour que ZeroBrane puisse trouver les fichiers de votre projet, vous devez lui indiquer l'emplacement du répertoire de votre projet Defold. Un moyen pratique de trouver cet emplacement consiste à utiliser l'option <kbd>Show in Desktop</kbd> sur un fichier à la racine de votre projet Defold.

1. Faites un clic droit sur *game.project*
2. Choisissez <kbd>Show in Desktop</kbd>

![Afficher dans le Finder](images/zerobrane/show_in_desktop.png)

## Configurer ZeroBrane {#to-set-up-zerobrane}

Pour configurer ZeroBrane, sélectionnez <kbd>Project ▸ Project Directory ▸ Choose...</kbd> :

![Configuration](images/zerobrane/setup.png)

Une fois le répertoire configuré pour correspondre à celui du projet Defold actuel, vous devriez pouvoir voir l'arborescence du projet Defold dans ZeroBrane, la parcourir et ouvrir les fichiers.

D'autres modifications de configuration recommandées, mais facultatives, sont présentées plus loin dans ce document.

## Démarrer le serveur de débogage {#starting-the-debugging-server}

Avant de démarrer une session de débogage, vous devez démarrer le serveur de débogage intégré à ZeroBrane. L'option permettant de le démarrer se trouve dans le menu <kbd>Project</kbd>. Sélectionnez simplement <kbd>Project ▸ Start Debugger Server</kbd> :

![Démarrer le débogueur](images/zerobrane/startdebug.png)

## Connecter votre application au débogueur {#connecting-your-application-to-the-debugger}

Le débogage peut démarrer à tout moment pendant l'exécution de l'application Defold, mais il doit être déclenché explicitement depuis un script Lua. Le code Lua permettant de démarrer une session de débogage se présente ainsi :

::: sidenote
Si votre jeu se ferme lors de l'appel à `dbg.start()`, il se peut que ZeroBrane ait détecté un problème et envoie la commande de fermeture au jeu. Pour une raison inconnue, ZeroBrane a besoin qu'un fichier soit ouvert pour démarrer la session de débogage, sinon il affiche :
"Can't start debugging without an opened file or with the current file not being saved 'untitled.lua')."
Dans ZeroBrane, ouvrez le fichier auquel vous avez ajouté `dbg.start()` pour corriger cette erreur.
:::

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start()
```

En insérant le code ci-dessus dans l'application, celle-ci se connectera au serveur de débogage de ZeroBrane (via "localhost", par défaut) et se mettra en pause à la prochaine instruction à exécuter.

```txt
Debugger server started at localhost:8172.
Mapped remote request for '/' to '/Users/my_user/Documents/Projects/Defold_project/'.
Debugging session started in '/Users/my_user/Documents/Projects/Defold_project'.
```

Vous pouvez maintenant utiliser les fonctionnalités de débogage de ZeroBrane : avancer pas à pas, inspecter, ajouter et supprimer des points d'arrêt, etc.

::: sidenote
Le débogage ne sera activé que pour le contexte Lua depuis lequel il est lancé. Activer "shared_state" dans *game.project* vous permet de déboguer toute votre application, quel que soit l'endroit où vous avez démarré le débogage.
:::

![Exécution pas à pas](images/zerobrane/code.png)

Si la tentative de connexion échoue (par exemple parce que le serveur de débogage n'est pas démarré), votre application continuera à fonctionner normalement après cette tentative.

## Débogage à distance {#remote-debugging}

Le débogage utilise des connexions réseau ordinaires (TCP), ce qui permet de déboguer à distance. Vous pouvez donc déboguer votre application pendant qu'elle s'exécute sur un appareil mobile.

La seule modification nécessaire concerne la commande qui démarre le débogage. Par défaut, `start()` tente de se connecter à localhost, mais pour le débogage à distance, nous devons indiquer manuellement l'adresse du serveur de débogage de ZeroBrane, comme ceci :

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start("192.168.5.101")
```

Il est donc important de vérifier que l'appareil distant dispose d'une connexion réseau et que les pare-feu ou logiciels similaires autorisent les connexions TCP sur le port 8172. Sinon, l'application risque de se bloquer au lancement lorsqu'elle tente de se connecter à votre serveur de débogage.

## Autre paramètre ZeroBrane recommandé {#other-recommended-zerobrane-setting}

Vous pouvez faire en sorte que ZeroBrane ouvre automatiquement les fichiers de script Lua pendant le débogage. Cela permet d'entrer pas à pas dans des fonctions définies dans d'autres fichiers source sans avoir à les ouvrir manuellement.

La première étape consiste à accéder au fichier de configuration de l'éditeur. Il est recommandé de modifier la version utilisateur de ce fichier.

- Sélectionnez <kbd>Edit ▸ Preferences ▸ Settings: User</kbd>
- Ajoutez ce qui suit au fichier de configuration :

  ```txt
  - to automatically open files requested during debugging
  editor.autoactivate = true
  ```

- Redémarrez ZeroBrane

![Autres paramètres recommandés](images/zerobrane/otherrecommended.png)
