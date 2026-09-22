---
title: Présentation de l'éditeur
brief: Ce manuel présente l'apparence et le fonctionnement de l'éditeur Defold, ainsi que la façon d'y naviguer.
---

# Présentation de l'éditeur {#editor-overview}

L'éditeur vous permet de parcourir et de manipuler efficacement tous les fichiers et dossiers de votre projet de jeu. Lorsque vous ouvrez un fichier pour le modifier, l'éditeur adapté s'affiche et présente toutes les informations pertinentes sur ce fichier dans des vues distinctes.

## Démarrage de l'éditeur {#starting-the-editor}

Lorsque vous lancez l'éditeur Defold, un écran de sélection et de création de projets s'affiche. Cliquez pour sélectionner l'action souhaitée :

MY PROJECTS
: Vous trouverez ici vos projets récemment ouverts pour y accéder rapidement. Il s'agit de la vue par défaut de l'écran de démarrage.

  Si vous n'avez encore ouvert aucun projet (ou si vous les avez tous retirés), deux boutons s'affichent : cliquez sur `Open From Disk…` pour en rechercher et en ouvrir un à l'aide du navigateur de fichiers du système, ou sur le bouton `Create New Project` pour passer à l'onglet `TEMPLATES`.

  ![Mes projets](images/editor/start_no_projects.png)


  Si vous avez déjà ouvert des projets, la liste de vos projets s'affiche, comme sur l'image ci-dessous :

  ![Mes projets](images/editor/start_my_projects.png)

TEMPLATES
: Contient des projets de base vides ou presque vides, conçus pour démarrer rapidement un nouveau projet Defold destiné à certaines plateformes ou utilisant certaines extensions.


TUTORIALS
: Contient des projets accompagnés de tutoriels guidés pour apprendre, jouer et les modifier, si vous souhaitez suivre un tutoriel.


SAMPLES
: Contient des projets préparés pour illustrer des cas d'utilisation particuliers.

  ![Nouveau projet](images/editor/start_templates.png)

Lorsque vous créez un nouveau projet, il est stocké sur votre disque local et toutes vos modifications sont enregistrées localement.

Pour en savoir plus sur les différentes options, consultez le [manuel de configuration d'un projet](https://www.defold.com/manuals/project-setup/).

## Langue de l'éditeur {#editor-language}

Dans le coin inférieur gauche de l'écran de démarrage, un sélecteur de langue vous permet de choisir parmi les traductions actuellement disponibles. Ce réglage est également accessible dans l'éditeur sous `File ▸ Preferences ▸ General ▸ Editor Language`.

![Langues](images/editor/languages.png)

## Les volets de l'éditeur {#the-editor-views}

L'éditeur Defold est divisé en plusieurs volets, ou vues, qui affichent des informations spécifiques.

![Éditeur 2](images/editor/editor_overview.png)

### 1. Volet Assets {#1-assets-pane}
Présente tous les fichiers et dossiers de votre projet dans une arborescence qui correspond à leur organisation sur votre disque. Cliquez et faites défiler pour parcourir la liste. Toutes les opérations sur les fichiers peuvent être effectuées dans cette vue :

   - Effectuez un <kbd>clic gauche</kbd> pour sélectionner un fichier ou un dossier ; maintenez <kbd>⇧ Shift</kbd> pour étendre la sélection, ou <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> pour sélectionner ou désélectionner l'élément sur lequel vous cliquez.
   - Effectuez un <kbd>double-clic</kbd> sur un fichier pour l'ouvrir dans l'éditeur propre à ce type de fichier.
   - Utilisez le <kbd>glisser-déposer</kbd> pour ajouter au projet des fichiers situés ailleurs sur votre disque, ou pour déplacer des fichiers et dossiers vers de nouveaux emplacements dans le projet.
   - Effectuez un <kbd>clic droit</kbd> pour ouvrir un _menu contextuel_ qui vous permet de créer des fichiers ou des dossiers, de les renommer, de les supprimer, de suivre les dépendances des fichiers et plus encore.

Les fichiers et dossiers supprimés depuis le volet *Assets* sont déplacés dans la corbeille du système lorsque la plateforme le permet. Si le déplacement vers la corbeille n'est pas pris en charge ou échoue, l'éditeur les supprime définitivement.

### 2. Volet Scene Editor {#the-scene-editor}

Un double-clic sur un fichier de collection, d'objet de jeu (game object) ou de composant (component) visuel ouvre le *Scene Editor*, l'éditeur visuel qui permet de créer et de modifier des scènes. Les fichiers de script et les autres ressources non visuelles s'ouvrent dans leurs propres éditeurs dédiés.

![Éditeur de scène](images/editor/2d_scene.png)

Voici quelques-unes des principales fonctionnalités de l'éditeur de scène :

- [Navigation dans les scènes 2D et 3D](/manuals/scene-editing/#2d-and-3d-scene-orientation) avec des modes de caméra orthographique et en perspective
- [Outils de transformation](/manuals/scene-editing/#manipulating-objects) pour déplacer, faire pivoter et redimensionner les objets
- [Mode caméra libre](/manuals/scene-editing/#free-camera-mode) pour une navigation 3D à la première personne
- [Réglages de la grille](/manuals/scene-editing/#grid-settings) avec une taille, un plan et une apparence configurables
- [Filtres de visibilité](/manuals/scene-editing/#visibility-filters) pour afficher ou masquer les types de composants et les repères

Pour en savoir plus, consultez le [manuel de l'éditeur de scène](/manuals/scene-editing/).

### 3. Volet Outline {#3-outline-pane}

Cette vue présente le contenu du fichier en cours de modification sous la forme d'une arborescence hiérarchique. Le volet Outline reflète la vue de l'éditeur et vous permet d'effectuer des opérations sur vos éléments :

   - Effectuez un <kbd>clic gauche</kbd> pour sélectionner un élément ; maintenez <kbd>⇧ Shift</kbd> pour étendre la sélection, ou <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> pour sélectionner ou désélectionner l'élément sur lequel vous cliquez.
   - Utilisez le <kbd>glisser-déposer</kbd> pour déplacer les éléments. Déposez un objet de jeu sur un autre objet de jeu dans une collection pour créer une relation parent-enfant.
   - Effectuez un <kbd>clic droit</kbd> pour ouvrir un _menu contextuel_ qui vous permet d'ajouter des éléments, de supprimer les éléments sélectionnés, etc.

Vous pouvez afficher ou masquer les objets de jeu et les composants visuels en cliquant sur la petite icône en forme d'œil `👁` à droite d'un élément de la liste.

![Arborescence](images/editor/outline.png)

### 4. Volet Properties {#4-properties-pane}

Cette vue affiche les propriétés associées à l'élément sélectionné, comme Id, URL, Position, Rotation, Scale et/ou d'autres propriétés propres au composant, ainsi que les propriétés personnalisées des scripts.

Vous pouvez également <kbd>faire glisser</kbd> la flèche verticale `↕` en déplaçant la souris pour modifier la valeur de la propriété numérique correspondante.

![Propriétés](images/editor/properties.png)

### 5. Volet Tools {#5-tools-pane}

Cette vue comporte plusieurs onglets.

L'onglet *Console* : affiche les erreurs, avertissements et informations émis par le moteur, ainsi que les messages que vous choisissez d'afficher pendant l'exécution de votre jeu,

*Build Errors* : affiche les erreurs survenues lors du build,

*Search Results* : affiche les résultats de la recherche (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>) dans l'ensemble du projet si vous cliquez sur `Keep Results`

*Curve Editor* : sert à modifier les courbes dans l'[éditeur de particules](/manuals/particlefx/).

Le volet Tools sert également à interagir avec le débogueur intégré. Pour en savoir plus, consultez le [manuel de débogage](/manuals/debugging/).

### 6. Volet Changed Files {#6-changed-files-pane}

Si votre projet utilise Git, cette vue répertorie les fichiers qui ont été modifiés, ajoutés, renommés ou supprimés localement par rapport au commit actuel (`HEAD`). Utilisez un client Git externe ou la ligne de commande pour synchroniser le projet avec un dépôt distant. Pour en savoir plus, consultez le [manuel de gestion de versions](/manuals/version-control/). Certaines opérations sur les fichiers peuvent être effectuées dans cette vue :

   - Effectuez un <kbd>clic gauche</kbd> pour sélectionner un fichier ; maintenez <kbd>⇧ Shift</kbd> pour étendre la sélection, ou <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> pour sélectionner ou désélectionner l'élément sur lequel vous cliquez. Si un seul fichier modifié est sélectionné, vous pouvez cliquer sur `Diff` pour afficher les différences. Cliquez sur `Revert` pour annuler les modifications de tous les fichiers sélectionnés.
   - Effectuez un <kbd>double-clic gauche</kbd> sur un fichier pour l'ouvrir dans une vue. L'éditeur ouvre le fichier dans un éditeur adapté, comme dans la vue des ressources.
   - Effectuez un <kbd>clic droit</kbd> sur un fichier pour ouvrir un menu contextuel qui vous permet d'afficher les différences, d'annuler toutes les modifications apportées au fichier, de retrouver le fichier dans le système de fichiers et plus encore.

### Barre de menus {#menu-bar}

En haut de la vue de l'éditeur, ou dans la barre système sur Mac, vous trouverez une barre de menus comprenant six menus : `File`, `Edit`, `View`, `Project`, `Debug`, `Help`. Leurs fonctions sont expliquées dans les manuels.

### Barre d'état {#status-bar}

Dans la barre inférieure de l'éditeur, un espace étroit affiche l'état des opérations, par exemple :
- lorsqu'une nouvelle mise à jour est disponible, un bouton cliquable `Update Available` apparaît ; consultez la section Mise à jour de l'éditeur plus bas dans ce manuel.
- lors de la création d'un build ou d'un bundle, la progression s'y affiche.

## Taille et visibilité des volets {#panes-size-and-visibility}

Vous pouvez ajuster la taille des volets dans l'éditeur en <kbd>faisant glisser</kbd> les bordures qui séparent les six volets décrits ci-dessus.

Vous pouvez afficher ou masquer les volets dans l'éditeur à l'aide des options du menu `View` ou des raccourcis correspondants :
- `Toggle Assets Pane` (<kbd>F6</kbd>) pour afficher ou masquer les volets Assets et Changed Files
- `Toggle Changed Files` pour afficher ou masquer uniquement le volet Changed Files
- `Toggle Tools Pane` (<kbd>F7</kbd>) pour afficher ou masquer le volet Tools
- `Toggle Properties Pane` (<kbd>F8</kbd>) pour afficher ou masquer les volets Outline et Properties

![Visibilité des volets](images/editor/editor_panes.png)

Dans le menu `View`, vous pouvez également activer, désactiver ou modifier d'autres réglages liés à la visibilité, tels que Grid, Guides ou Camera, ajuster la vue à la sélection (`Frame Selection` ou la touche <kbd>F</kbd>) et basculer entre les vues 2D et 3D par défaut (`Realign Camera` ou la touche <kbd>.</kbd>). Beaucoup de ces réglages sont également accessibles depuis la barre d'outils ou par des raccourcis.

## Onglets {#tabs}

Si plusieurs fichiers sont ouverts, un onglet distinct pour chaque fichier s'affiche en haut de la vue de l'éditeur.  Les onglets d'un même volet peuvent être réorganisés : utilisez le <kbd>glisser-déposer</kbd> pour permuter leurs positions dans la barre d'onglets. Vous pouvez également :

- Effectuer un <kbd>clic droit</kbd> sur un onglet pour ouvrir un _menu contextuel_,
- Cliquer sur `Close` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>W</kbd>) pour fermer un seul onglet,
- Cliquer sur `Close Others` pour fermer tous les onglets sauf celui qui est sélectionné,
- Cliquer sur `Close All` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd>+<kbd>W</kbd>) pour fermer tous les onglets du volet actif,
- Sélectionner `➝| Open As` pour utiliser un autre éditeur que celui par défaut, ou l'outil externe associé défini dans `File ▸ Preferences ▸ Code ▸ Custom Editor`. Pour en savoir plus, consultez le [manuel des préférences](/manuals/editor-preferences).

![Onglets](images/editor/tabs_custom.png)

## Édition côte à côte {#side-by-side-editing}

Vous pouvez ouvrir deux vues de l'éditeur côte à côte.

- Effectuez un <kbd>clic droit</kbd> sur l'onglet de l'éditeur que vous souhaitez déplacer et sélectionnez `Move to Other Tab Pane`.

![Deux volets](images/editor/2-panes.png)

Vous pouvez également utiliser le menu de l'onglet pour choisir `Swap with Other Tab Pane` afin de déplacer cet onglet entre les volets, ou `Join Tab Panes` pour les réunir en un seul volet.

## Création de fichiers dans le projet {#creating-new-project-files}

Pour créer des fichiers de ressources, sélectionnez `File ▸ New…` puis choisissez le type de fichier dans le menu, ou utilisez le menu contextuel :

Effectuez un <kbd>clic droit</kbd> sur l'emplacement cible dans le navigateur `Assets`, puis sélectionnez `New… ▸ [file type]` :

![Création d'un fichier](images/editor/create_file.png)

Saisissez un nom approprié dans *Name* pour le nouveau fichier et modifiez au besoin *Location*. Le nom complet du fichier, avec le suffixe correspondant à son type, s'affiche sous *Preview* dans la boîte de dialogue :

![Nom du fichier à créer](images/editor/create_file_name.png)

## Modèles {#templates}

Vous pouvez définir des modèles personnalisés pour chaque projet. Pour cela, créez un dossier nommé `templates` dans le répertoire racine du projet et ajoutez des fichiers nommés `default.*` avec les extensions souhaitées, comme `/templates/default.gui` ou `/templates/default.script`. De plus, si le marqueur `{{NAME}}` est utilisé dans ces fichiers, il sera remplacé par le nom de fichier indiqué dans la fenêtre de création de fichier.

Si un modèle est disponible pour un type de fichier donné, chaque nouveau fichier de ce type est initialisé avec le contenu du fichier correspondant dans `templates`.


![Modèles](images/editor/templates.png)

## Importation de fichiers dans votre projet {#importing-files-to-your-project}

Pour ajouter des fichiers de ressources (images, sons, modèles, etc.) à votre projet, faites-les simplement glisser à l'emplacement voulu dans le navigateur *Assets*. Cela crée des _copies_ des fichiers à l'emplacement sélectionné dans l'arborescence du projet. Pour en savoir plus, consultez notre [manuel sur l'importation de ressources](/manuals/importing-assets/).

![Importation de fichiers](images/editor/import.png)

## Mise à jour de l'éditeur {#updating-the-editor}

L'éditeur recherche automatiquement les mises à jour lorsqu'il est connecté à Internet. Lorsqu'une mise à jour est détectée, un lien bleu cliquable `Update Available` s'affiche dans le coin inférieur gauche de l'écran de sélection de projets ou dans le coin inférieur droit de la fenêtre de l'éditeur.

![Mise à jour depuis la sélection de projets](images/editor/update_start.png)
![Mise à jour depuis l'éditeur](images/editor/update_available.png)

Cliquez sur le lien `Update Available` pour télécharger et installer la mise à jour. Une fenêtre de confirmation contenant des informations s'affiche : cliquez sur `Download Update` pour continuer.

![Fenêtre de mise à jour de l'éditeur](images/editor/update.png)

La progression du téléchargement s'affiche dans la barre d'état inférieure :

![Progression du téléchargement](images/editor/download_status.png)

Une fois la mise à jour téléchargée, le lien bleu devient `Restart to Update`. Cliquez dessus pour redémarrer et ouvrir l'éditeur mis à jour.

![Redémarrage pour la mise à jour](images/editor/restart_to_update.png)

## Préférences {#preferences}

Vous pouvez modifier les réglages de l'éditeur dans la fenêtre `Preferences`. Pour l'ouvrir, cliquez sur `File ▸ Preferences…` ou utilisez le raccourci <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>,</kbd>

Pour en savoir plus, consultez le [manuel des préférences](/manuals/editor-preferences)

![Préférences](images/editor/preferences.png)

## Journaux de l'éditeur {#editor-logs}
Si vous rencontrez un problème avec l'éditeur et devez le signaler (`Help  ▸ Report Issue`), il est utile de fournir les fichiers journaux de l'éditeur lui-même. Pour ouvrir l'emplacement des journaux dans le navigateur de fichiers de votre système, cliquez sur `Help ▸ Show Logs`.

Pour en savoir plus, consultez le [manuel pour obtenir de l'aide](/manuals/getting-help/#getting-help).

![Affichage des journaux](images/editor/show_logs.png)

Les fichiers journaux de l'éditeur se trouvent ici :

  * Windows : `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS : `/Users/ **Your Username** /Library/Application Support/` ou `~/Library/Application Support/Defold`
  * Linux : `$XDG_STATE_HOME/Defold` ou `~/.local/state/Defold`

Vous pouvez également accéder aux journaux de l'éditeur pendant son exécution s'il a été lancé depuis un terminal ou une invite de commandes. Pour lancer l'éditeur, utilisez la commande :

```shell
# Linux:
$ ./path/to/Defold/Defold

# macOS:
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## Serveur de l'éditeur {#editor-server}

Lorsque l'éditeur ouvre un projet, il démarre un serveur web sur un port aléatoire. Ce serveur peut être utilisé pour interagir avec l'éditeur depuis d'autres applications. Le port est écrit dans le fichier `.internal/editor.port`.

Le serveur fournit une spécification OpenAPI à l'adresse `http://localhost:$(cat .internal/editor.port)/openapi.json`. Elle constitue un point de départ minimal utile pour les flux de travail agentiques.

L'exécutable de l'éditeur propose également l'option de ligne de commande `--port` (ou `-p`), qui permet de spécifier le port au lancement, par exemple :
```shell
# Windows
.\path\to\Defold\Defold.exe --port 8181

# Linux:
./path/to/Defold/Defold --port 8181

# macOS:
./path/to/Defold/Defold.app/Contents/MacOS/Defold --port 8181
```

## Métadonnées d'installation de l'éditeur {#editor-installation-metadata}

Au démarrage, l'éditeur écrit des informations sur les chemins du lanceur et de l'installation à un emplacement prédéfini. Les intégrations d'IDE tiers et d'autres outils peuvent les utiliser pour trouver les éditeurs Defold installés :

| Système d'exploitation | Emplacement |
|---------|----------|
| macOS   | `~/Library/Application Support/Defold/installations.json` |
| Linux   | `${XDG_STATE_HOME:-~/.local/state}/Defold/installations.json` |
| Windows | `%LOCALAPPDATA%\Defold\installations.json` |

Le fichier contient un tableau JSON avec un objet par installation connue :

```json
[
  {
    "launcherPath": "/Applications/Defold.app/Contents/MacOS/Defold",
    "installPath": "/Applications/Defold.app",
    "lastLaunchedAt": "2026-07-06T12:34:56.789Z"
  }
]
```

## Personnalisation de l'apparence de l'éditeur {#editor-styling}

L'apparence de l'éditeur peut être modifiée à l'aide de styles personnalisés. Pour en savoir plus, consultez le [manuel de personnalisation de l'apparence de l'éditeur](/manuals/editor-styling).

## FAQ {#faq}
:[Editor FAQ](../shared/editor-faq.md)
