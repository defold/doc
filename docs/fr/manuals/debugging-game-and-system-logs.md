---
title: Débogage - journaux du jeu et du système
brief: Ce manuel explique comment lire les journaux du jeu et du système.
---

# Journal du jeu et du système {#game-and-system-log}

Le journal du jeu affiche toutes les sorties du moteur, des extensions natives et de la logique de votre jeu. Les commandes [print()](/ref/stable/base/#print:...) et [pprint()](/ref/stable/builtins/?q=pprint#pprint:v) peuvent être utilisées dans vos scripts et modules Lua pour afficher des informations dans le journal du jeu. Vous pouvez utiliser les fonctions de l'[espace de noms (namespace) `dmLog`](/ref/stable/dmLog/) pour écrire dans le journal du jeu depuis les extensions natives. Le journal du jeu peut être consulté depuis l'éditeur, depuis une fenêtre de terminal, à l'aide d'outils propres à chaque plateforme ou depuis un fichier journal.

Les journaux du système sont générés par le système d'exploitation et peuvent fournir des informations supplémentaires pour vous aider à localiser un problème. Ils peuvent contenir des traces de pile en cas de plantage et des avertissements de mémoire insuffisante.

::: important
La journalisation dans la console ou à l'écran n'affiche des informations que dans les builds Debug. Dans les builds Release, le journal de la console est vide, mais vous pouvez activer la journalisation dans un fichier en Release en réglant le paramètre du projet « Write Log File » sur « Always ». Voir les détails ci-dessous.
:::

## Lire le journal du jeu depuis l'éditeur {#reading-the-game-log-from-the-editor}

Lorsque vous exécutez votre jeu localement depuis l'éditeur ou en étant connecté à l'[application de développement mobile](/manuals/dev-app), toutes les sorties s'affichent dans le panneau de console de l'éditeur :

![Éditeur 2](images/editor/editor2_overview.png)

## Lire le journal du jeu depuis le terminal {#reading-the-game-log-from-the-terminal}

Lorsque vous exécutez un jeu Defold depuis le terminal, le journal s'affiche directement dans la fenêtre du terminal. Sous Windows et Linux, saisissez le nom de l'exécutable dans le terminal pour démarrer le jeu. Sous macOS, vous devez lancer le moteur depuis l'intérieur du fichier .app :

```
$ > ./mygame.app/Contents/MacOS/mygame
```

## Lire les journaux du jeu et du système à l'aide d'outils propres à chaque plateforme {#reading-game-and-system-logs-using-platform-specific-tools}

### HTML5 {#html5}

Les journaux peuvent être consultés à l'aide des outils de développement fournis par la plupart des navigateurs.

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - Menu > More Tools > Developer Tools
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - Tools > Web Developer > Web Console
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - Develop > Show JavaScript Console

### Android {#android}

Vous pouvez utiliser l'outil Android Debug Bridge (ADB) pour consulter le journal du jeu et du système.

:[Android ADB](../shared/android-adb.md)

Une fois l'outil installé et configuré, connectez votre appareil par USB, ouvrez un terminal et exécutez :

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat
```

L'appareil enverra alors toutes les sorties au terminal actuel, y compris les messages affichés par le jeu.

Si vous souhaitez voir uniquement les sorties des applications Defold, utilisez cette commande :

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialized sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS {#ios}

Plusieurs options s'offrent à vous pour lire les journaux du jeu et du système sous iOS :

1. Vous pouvez utiliser l'[outil Console](https://support.apple.com/guide/console/welcome/mac) pour lire le journal du jeu et du système.
2. Vous pouvez utiliser le débogueur LLDB pour vous attacher à un jeu en cours d'exécution sur un appareil. Pour déboguer un jeu, celui-ci doit être signé avec un « Apple Developer Provisioning Profile » qui inclut l'appareil sur lequel vous souhaitez le déboguer. Créez un bundle du jeu depuis l'éditeur et fournissez le profil de provisionnement dans la boîte de dialogue de création du bundle (la création de bundles pour iOS n'est disponible que sous macOS).

Pour lancer le jeu et y attacher le débogueur, vous aurez besoin d'un outil appelé [ios-deploy](https://github.com/phonegap/ios-deploy). Installez et déboguez votre jeu en exécutant la commande suivante dans un terminal :

```txt
$ ios-deploy --debug --bundle <path_to_game.app> # NOTE: not the .ipa file
```

Cela installera l'application sur votre appareil, la démarrera et y attachera automatiquement un débogueur LLDB. Si vous découvrez LLDB, lisez le guide [Premiers pas avec LLDB](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html).


## Lire le journal du jeu depuis le fichier journal {#reading-the-game-log-from-the-log-file}

Utilisez le paramètre du projet « Write Log File » dans *game.project* pour contrôler la journalisation dans un fichier :

- « Never » : ne pas écrire de fichier journal.
- « Debug » : écrire un fichier journal uniquement pour les builds Debug.
- « Always » : écrire un fichier journal pour les builds Debug et Release.

Lorsque cette option est activée, toutes les sorties du jeu sont écrites sur le disque dans un fichier nommé « `log.txt` ». Voici comment extraire ce fichier si vous exécutez le jeu sur un appareil :

iOS
: Connectez votre appareil à un ordinateur sur lequel macOS et Xcode sont installés.

  Ouvrez Xcode et accédez à <kbd>Window ▸ Devices and Simulators</kbd>.

  Sélectionnez votre appareil dans la liste, puis sélectionnez l'application concernée dans la liste *Installed Apps*.

  Cliquez sur l'icône d'engrenage sous la liste et sélectionnez <kbd>Download Container...</kbd>.

  ![Télécharger le conteneur](images/debugging/download_container.png)

  Une fois le conteneur extrait, il apparaît dans le *Finder*. Faites un clic droit sur le conteneur et sélectionnez <kbd>Show Package Content</kbd>. Repérez le fichier « `log.txt` », qui devrait se trouver dans « `AppData/Documents/` ».

Android(
: La possibilité d'extraire le fichier « `log.txt` » dépend de la version du système d'exploitation et du fabricant. Voici un [guide pas à pas](https://stackoverflow.com/a/48077004/129360) court et simple.
