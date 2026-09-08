---
title: Préférences de l'éditeur
brief: Vous pouvez modifier les paramètres de l'éditeur dans la fenêtre Preferences.
---

# Préférences de l'éditeur {#editor-preferences}

Vous pouvez modifier les paramètres de l'éditeur dans la fenêtre Preferences. Pour ouvrir cette fenêtre, utilisez le menu <kbd>File -> Preferences</kbd>.

## Général {#general}

![](images/editor/preferences_general.png)

Load External Changes on App Focus
: Active la recherche de modifications externes lorsque l'éditeur reçoit le focus.

Open Bundle Target Folder
: Active l'ouverture du dossier de destination du bundle une fois la création du bundle terminée.

Enable Texture Compression
: Active la [compression des textures](/manuals/texture-profiles) pour tous les builds créés depuis l'éditeur.

Escape Quits Game
: Arrêtez un build de votre jeu en cours d'exécution à l'aide de la touche <kbd>Esc</kbd>.

Track Active Tab in Asset Browser
: Le fichier modifié dans l'onglet sélectionné du panneau *Editor* sera sélectionné dans l'Asset Browser (également appelé panneau *Asset*).

Lint Code on Build
: Active l'[analyse statique du code](/manuals/writing-code/#linting-configuration) lors du build du projet. Cette option est activée par défaut, mais vous pouvez la désactiver si l'analyse d'un projet volumineux prend trop de temps.

Engine Arguments
: Arguments transmis à l'exécutable dmengine lorsque l'éditeur compile et exécute le projet.
 Utilisez un argument par ligne. Par exemple :
 ```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```


## Code {#code}

![](images/editor/preferences_code.png)

Custom Editor
: Chemin absolu vers un éditeur externe. Sur macOS, il doit s'agir du chemin vers l'exécutable à l'intérieur du .app (par exemple, `/Applications/Atom.app/Contents/MacOS/Atom`).

Open File
: Modèle utilisé par l'éditeur personnalisé pour indiquer le fichier à ouvrir. Le modèle `{file}` sera remplacé par le nom du fichier à ouvrir.

Open File at Line
: Modèle utilisé par l'éditeur personnalisé pour indiquer le fichier à ouvrir et le numéro de ligne. Le modèle `{file}` sera remplacé par le nom du fichier à ouvrir et `{line}` par le numéro de ligne.

Code editor font
: Nom d'une police installée sur le système à utiliser dans l'éditeur de code.

Zoom on Scroll
: Indique s'il faut modifier la taille de la police lors du défilement dans l'éditeur de code tout en maintenant la touche Cmd/Ctrl enfoncée.

Auto-insert closing parens
: Insère automatiquement les caractères fermants correspondants lors de la modification du code. Cette option est activée par défaut.


### Ouvrir les fichiers de script dans Visual Studio Code {#open-script-files-in-visual-studio-code}

![](images/editor/preferences_vscode.png)

Pour ouvrir les fichiers de script depuis l'éditeur Defold directement dans Visual Studio Code, vous devez définir les paramètres suivants en indiquant le chemin vers le fichier exécutable :

- MacOS : `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux : `/usr/bin/code`
- Windows : `C:\Program Files\Microsoft VS Code\Code.exe`

 Définissez ces paramètres pour ouvrir des fichiers et des lignes spécifiques :

- Open File : `. {file}`
- Open File at Line : `. -g {file}:{line}`

Le caractère `.` est nécessaire ici pour ouvrir l'espace de travail entier, et non un fichier individuel.


## Extensions {#extensions}

![](images/editor/preferences_extensions.png)

Build Server
: URL du serveur de build utilisé lors du build d'un projet contenant des [extensions natives](/manuals/extensions). Vous pouvez ajouter un nom d'utilisateur et un jeton d'accès à l'URL pour accéder au serveur de build avec authentification. Utilisez la notation suivante pour indiquer le nom d'utilisateur et le jeton d'accès : `username:token@build.defold.com`. L'accès avec authentification est obligatoire pour les builds Nintendo Switch et lorsque vous exécutez votre propre instance de serveur de build avec l'authentification activée ([consultez la documentation du serveur de build](https://github.com/defold/extender/blob/dev/README_SECURITY.md) pour plus d'informations). Le nom d'utilisateur et le mot de passe peuvent également être définis dans les variables d'environnement du système `DM_EXTENDER_USERNAME` et `DM_EXTENDER_PASSWORD`.

Build Server Username
: Nom d'utilisateur pour l'authentification.

Build Server Password
: Mot de passe pour l'authentification, qui sera stocké sous forme chiffrée dans le fichier des préférences.

Build Server Headers
: En-têtes supplémentaires envoyés au serveur de build lors du build des extensions natives. Ils sont importants pour utiliser le service CloudFlare ou des services similaires avec extender.

## Outils {#tools}

![](images/editor/preferences_tools.png)

ADB path
: Chemin vers l'outil en ligne de commande [ADB](https://developer.android.com/tools/adb) installé sur ce système. Si ADB est installé sur votre système, l'éditeur Defold l'utilisera pour installer et exécuter les APK Android générés lors de la création de bundles sur un appareil Android connecté. Par défaut, l'éditeur vérifie si ADB est installé aux emplacements habituels ; vous ne devez donc indiquer le chemin que si ADB est installé à un emplacement personnalisé.

ios-deploy path
: Chemin vers les outils en ligne de commande [ios-deploy](https://github.com/ios-control/ios-deploy) installés sur ce système (concerne uniquement macOS). Comme pour le chemin d'ADB, l'éditeur Defold utilisera cet outil pour installer et exécuter les applications iOS générées lors de la création de bundles sur un iPhone connecté. Par défaut, l'éditeur vérifie si ios-deploy est installé aux emplacements habituels ; vous ne devez donc indiquer le chemin que si vous utilisez une installation personnalisée d'ios-deploy.

## Raccourcis {#keymap}

![](images/editor/preferences_keymap.png)

Vous pouvez configurer les raccourcis clavier et les commandes de la souris de l'éditeur dans l'onglet Keymap. Pour modifier une commande, double-cliquez dessus, appuyez sur <kbd>Enter</kbd> ou <kbd>Space</kbd>, ou utilisez le menu contextuel de la ligne.

Les raccourcis clavier apparaissent sous forme de combinaisons de touches dans la colonne *Shortcuts*. Les commandes de la souris apparaissent dans la même liste avec un badge :

- <kbd>MB</kbd> désigne une affectation de bouton de souris, éventuellement combinée à <kbd>Shift</kbd>, <kbd>Ctrl</kbd>/<kbd>Control</kbd> ou <kbd>Alt</kbd>.
- <kbd>MM</kbd> désigne une touche de modification utilisée par une action de la souris.

Certaines commandes de la souris réutilisent les affectations de la Scene 2D Camera par défaut ; une ligne peut donc afficher une affectation avant que vous ne la personnalisiez. Ces affectations sont généralement affichées dans une couleur plus sombre. Si vous définissez une affectation personnalisée pour cette ligne, Defold utilise celle-ci à la place. Utilisez *Reset to Defaults* pour supprimer votre modification et revenir au comportement intégré ou hérité.

Les avertissements sont affichés en orange. Survolez un avertissement pour en voir les détails. Les avertissements indiquent généralement que :
- le raccourci permet de saisir du texte et peut interférer avec les champs de texte.
- le même raccourci ou la même affectation de souris est déjà utilisé par une autre commande.
