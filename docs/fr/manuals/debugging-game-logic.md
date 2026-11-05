---
title: Débogage dans Defold
brief: Ce manuel présente les outils de débogage disponibles dans Defold.
---

# Débogage de la logique du jeu {#debugging-game-logic}

Defold intègre un débogueur Lua doté de fonctions d'inspection. Associé aux [outils de profilage](/manuals/profiling) intégrés, il constitue un outil puissant qui peut vous aider à trouver la cause des bogues dans la logique de votre jeu ou à analyser les problèmes de performances.

## Débogage par affichage et débogage visuel {#print-and-visual-debugging}

La méthode la plus simple pour déboguer votre jeu dans Defold consiste à utiliser le [débogage par affichage](http://en.wikipedia.org/wiki/Debugging#Techniques). Utilisez des instructions `print()` ou [`pprint()`](/ref/builtins#pprint) pour surveiller les variables ou indiquer le déroulement de l'exécution. Si un objet de jeu (game object) sans script se comporte de façon étrange, vous pouvez simplement lui associer un script dans le seul but de le déboguer. Chacune de ces fonctions d'affichage écrit dans la vue *Console* de l'éditeur et dans le [journal du jeu](/manuals/debugging-game-and-system-logs).

En plus de l'affichage dans la console, le moteur peut également dessiner du texte de débogage et des lignes droites à l'écran. Pour cela, envoyez des messages au socket `@render` :

```lua
-- Draw value of "my_val" with debug text on the screen
msg.post("@render:", "draw_text", { text = "My value: " .. my_val, position = vmath.vector3(200, 200, 0) })

-- Draw colored text on the screen
local color_green = vmath.vector4(0, 1, 0, 1)
msg.post("@render:", "draw_debug_text", { text = "Custom color", position = vmath.vector3(200, 180, 0), color = color_green })

-- Draw debug line between player and enemy on the screen
local start_p = go.get_position("player")
local end_p = go.get_position("enemy")
local color_red = vmath.vector4(1, 0, 0, 1)
msg.post("@render:", "draw_line", { start_point = start_p, end_point = end_p, color = color_red })
```

Les messages de débogage visuel ajoutent des données à la chaîne de rendu, qui les dessine dans le cadre du rendu normal.

* `"draw_line"` ajoute des données dont le rendu est effectué par la fonction `render.draw_debug3d()` dans le script de rendu.
* `"draw_text"` est rendu avec la police `/builtins/fonts/debug/always_on_top.font`, qui utilise le matériau `/builtins/fonts/debug/always_on_top_font.material`.
* `"draw_debug_text"` fonctionne comme `"draw_text"`, mais le rendu utilise une couleur personnalisée.

Vous souhaiterez probablement mettre à jour ces données à chaque image ; il est donc judicieux d'envoyer les messages dans la fonction `update()`.

## Exécution du débogueur {#running-the-debugger}

Le débogueur Lua est disponible dans les builds natifs de débogage et sans interface graphique. Utilisez un moteur de la même version de Defold que l'éditeur. Les builds Release et Web ne permettent pas d'attacher le débogueur.

Pour lancer le débogueur, sélectionnez <kbd>Debug ▸ Start/Attach</kbd>. Cette commande démarre le jeu avec le débogueur attaché ou l'attache à un jeu déjà en cours d'exécution. Lors du démarrage d'un jeu pour le débogage, l'éditeur installe les points d'arrêt activés avant l'exécution des scripts de démarrage ; vous pouvez donc placer un point d'arrêt dans `init()` avant le lancement.

Pour l'attacher à un appareil, sélectionnez celui-ci sous <kbd>Project ▸ Targets</kbd>, puis choisissez <kbd>Debug ▸ Start/Attach</kbd>. L'attachement interrompt l'exécution à la prochaine ligne Lua. L'éditeur configure automatiquement la connexion du débogueur pour les cibles locales et distantes prises en charge. Consultez [Cibles distantes](#remote-targets) pour les conditions de connexion, ou découvrez comment [connecter un débogueur externe](#native-dap-connections).

![vue d'ensemble](images/debugging/overview.png)

Dès que le débogueur est attaché, vous pouvez contrôler l'exécution du jeu à l'aide des boutons de commande du débogueur dans la console ou du menu <kbd>Debug</kbd> :

Break
: ![pause](images/debugging/pause.svg){width=60px .left}
  Mettez en pause l'exécution de Lua à la prochaine ligne du code source. Vous pouvez alors inspecter l'état du jeu, avancer pas à pas ou poursuivre l'exécution jusqu'au prochain point d'arrêt. La position actuelle de l'exécution est indiquée dans l'éditeur de code :

  ![script](images/debugging/script.png)

Continue
: ![lecture](images/debugging/play.svg){width=60px .left}
  Reprenez l'exécution du jeu. Le code du jeu continue de s'exécuter jusqu'à ce que vous appuyiez sur le bouton de pause ou que l'exécution atteigne un point d'arrêt que vous avez défini. Si l'exécution s'interrompt à un point d'arrêt, sa position est indiquée dans l'éditeur de code, par-dessus le marqueur du point d'arrêt :

  ![point d'arrêt](images/debugging/break.png)

Stop
: ![arrêt](images/debugging/stop.svg){width=60px .left}
  Arrêtez le débogueur. Appuyer sur ce bouton arrête immédiatement le débogueur, le détache du jeu et met fin au jeu en cours d'exécution.

Step Over
: ![pas à pas principal](images/debugging/step_over.svg){width=60px .left}
  Avancez l'exécution du programme d'un pas. Si l'exécution implique l'appel d'une autre fonction Lua, elle _n'entre pas dans la fonction_, mais continue et s'arrête à la ligne suivante, sous l'appel de fonction. Dans cet exemple, si vous appuyez sur « step over », le débogueur exécute le code et s'arrête à l'instruction `end` sous la ligne contenant l'appel à la fonction `nextspawn()` :

  ![pas](images/debugging/step.png)

::: sidenote
L'exécution pas à pas suit les lignes du code source Lua. Un pas peut revenir sur la même ligne, par exemple lorsqu'une boucle se répète ; il ne passe donc pas toujours à la ligne suivante du fichier.
:::

Step Into
: ![pas à pas détaillé](images/debugging/step_in.svg){width=60px .left}
  Avancez l'exécution du programme d'un pas. Si l'exécution implique l'appel d'une autre fonction Lua, elle _entre dans la fonction_. L'appel de la fonction ajoute une entrée à la pile des appels. Vous pouvez cliquer sur chaque entrée de cette liste pour afficher le point d'entrée et le contenu de toutes les variables de cette fermeture lexicale. Ici, vous êtes entré dans la fonction `nextspawn()` :

  ![entrée dans la fonction](images/debugging/step_into.png)

Step Out
: ![sortie de la fonction](images/debugging/step_out.svg){width=60px .left}
  Poursuivez l'exécution jusqu'au retour de la fonction actuelle. Si vous êtes entré dans une fonction en exécutant le code pas à pas, appuyer sur le bouton « step out » poursuit l'exécution jusqu'au retour de la fonction.

Ajout et suppression de points d'arrêt
: Vous pouvez définir autant de points d'arrêt que vous le souhaitez dans votre code Lua. Lorsque le jeu s'exécute avec le débogueur attaché, l'exécution s'interrompt au prochain point d'arrêt rencontré et attend une nouvelle intervention de votre part.

  ![ajout d'un point d'arrêt](images/debugging/add_breakpoint.png)

  Pour ajouter ou supprimer un point d'arrêt, cliquez dans la colonne située juste à droite des numéros de ligne dans l'éditeur de code. Vous pouvez également sélectionner <kbd>Edit ▸ Toggle Breakpoint</kbd> dans le menu.

Désactivation et activation des points d'arrêt
: Vous pouvez désactiver temporairement les points d'arrêt sans les supprimer. Lorsqu'ils sont désactivés, ils sont ignorés pendant l'exécution, mais vous pouvez les réactiver à tout moment. Faites un clic droit sur le point d'arrêt dans la marge de l'éditeur de code, puis cochez ou décochez la case `Enabled`. Les points d'arrêt désactivés apparaissent creux pour indiquer qu'ils sont inactifs.

  ![désactivation d'un point d'arrêt](images/debugging/disable_breakpoint.png)

Définition de points d'arrêt conditionnels
: Vous pouvez configurer votre point d'arrêt pour qu'il contienne une condition qui doit être vraie pour le déclencher. Cette condition peut accéder aux variables locales disponibles à cette ligne pendant l'exécution du code.

  ![modification d'un point d'arrêt](images/debugging/edit_breakpoint.png)

  Pour modifier la condition du point d'arrêt, faites un clic droit dans la colonne située juste à droite des numéros de ligne dans l'éditeur de code, ou sélectionnez <kbd>Edit ▸ Edit Breakpoint</kbd> dans le menu.

Évaluation d'expressions Lua
: Lorsque le jeu est en pause, sélectionnez un cadre dans *Call Stack*, saisissez une expression ou une instruction Lua en bas de la console et appuyez sur <kbd>Enter</kbd>. L'évaluation utilise les variables locales, les upvalues et les variables globales du cadre sélectionné. Les tables renvoyées incluent leur contenu imbriqué.

  ![console](images/debugging/console.png)

  Vous pouvez également modifier les valeurs par affectation, par exemple `self.score = 100` dans un cadre où `self` est disponible. Le code évalué produit les mêmes effets sur l'état du jeu que du code exécuté par votre jeu.

Inspection des variables
: Sélectionnez un cadre dans *Call Stack* pour inspecter ses variables locales et ses upvalues dans la vue *Variables*. Développez `_G` pour inspecter les variables globales, et les tables ou `self` pour consulter leurs champs. L'éditeur conserve les chemins développés, la sélection et la position de défilement lors du pas à pas, des changements de cadre ou des rafraîchissements après évaluation, tout en récupérant les valeurs actuelles.

Détachement du débogueur
: Sélectionnez <kbd>Debug ▸ Detach Debugger</kbd> pour détacher le débogueur du jeu. Le jeu reprend immédiatement son exécution. Utilisez <kbd>Debug ▸ Start/Attach</kbd> pour l'attacher à nouveau sans redémarrer le jeu.

## Connexions DAP natives {#native-dap-connections}

Le moteur fournit un serveur natif Debug Adapter Protocol (DAP) via TCP. Pour utiliser un client DAP externe, démarrez l'écoute dans un moteur Defold natif de débogage ou sans interface graphique, puis connectez le client à l'adresse et au port du moteur. L'éditeur configure automatiquement l'écoute lorsque vous utilisez <kbd>Debug ▸ Start/Attach</kbd>.

L'éditeur actuel ne peut pas se connecter aux anciens moteurs qui prennent uniquement en charge MobDebug. Aucun appel `require "builtins.scripts.mobdebug"` n'est nécessaire ni disponible dans les versions actuelles.

### Démarrer l'écoute {#starting-the-listener}

Compilez d'abord votre projet. Depuis le répertoire du projet contenant `build/default/game.projectc`, exécutez le moteur natif de débogage avec ces [valeurs de configuration au démarrage](/manuals/project-settings/#setting-config-values-on-engine-startup) :

```sh
dmengine --config=debugger.enabled=1 \
  --config=debugger.port=8172 --config=debugger.wait=1
```

Connectez votre client DAP à `127.0.0.1:8172`. Le moteur attend que le client configure les points d'arrêt avant d'exécuter les scripts de démarrage.

| Paramètre | Valeur par défaut | Rôle |
| --- | --- | --- |
| `debugger.enabled` | `0` | Définissez-le sur `1` pour démarrer l'écoute au démarrage du moteur. |
| `debugger.address` | `127.0.0.1` | Adresse IPv4 d'écoute. La valeur par défaut accepte les connexions depuis le même ordinateur. |
| `debugger.port` | `8172` | Port d'écoute TCP. Utilisez `0` pour sélectionner un port disponible. |
| `debugger.wait` | `0` | Définissez-le sur `1` pour attendre la configuration du client de débogage avant d'exécuter les scripts de démarrage. |

Vous pouvez également ajouter ces valeurs à la [section Debugger de game.project](/manuals/project-settings/#debugger). L'éditeur configure automatiquement l'écoute pour <kbd>Debug ▸ Start/Attach</kbd> ; la configuration manuelle n'est donc nécessaire que lorsque vous démarrez vous-même l'écoute.

Le journal du moteur indique l'adresse et le port sélectionnés. Avec `debugger.wait=0`, le jeu démarre immédiatement et vous pouvez attacher le client plus tard. Avec `debugger.wait=1`, il attend que le client ait fini de configurer la session, y compris les points d'arrêt. Pour les lancements locaux de débogage, l'éditeur sélectionne automatiquement un port disponible.

La déconnexion d'un client reprend l'exécution et laisse l'écoute disponible pour une nouvelle connexion. Une déconnexion pendant l'attente de la configuration de démarrage libère également le moteur. Si l'écoute ne peut pas démarrer, le moteur consigne l'erreur et poursuit son démarrage ; vous pouvez réessayer depuis Lua avec `debugger.start(0)` pour sélectionner un port disponible.

### Activer l'écoute pendant l'exécution {#enabling-the-listener-while-running}

Pour activer l'écoute depuis un script sans redémarrer le jeu :

```lua
if debugger then
    local port = debugger.start(0)
    print("DAP listener port:", port)
end
```

`debugger.start([port [, address]])` renvoie immédiatement le port d'écoute. Cette fonction n'attend pas de client et ne met pas le jeu en pause. Les arguments omis utilisent `debugger.port` et `debugger.address` ; la valeur `0` sélectionne un port disponible. Les appels répétés renvoient le port de l'écoute existante sans modifier son adresse ni son port. Le module `debugger` est fourni par les moteurs natifs de débogage et sans interface graphique.

Le port doit être un entier compris entre `0` et `65535`. Passez `nil` comme premier argument pour ne remplacer que l'adresse. Des arguments non valides ou un échec de liaison du port d'écoute déclenchent une erreur Lua.

### Cibles distantes {#remote-targets}

Pour une connexion directe depuis un autre ordinateur, liez l'écoute à l'interface IPv4 de l'appareil ou à `0.0.0.0` (toutes les interfaces IPv4). Utilisez par exemple `debugger.start(8172, "0.0.0.0")`, ou ajoutez `--config=debugger.address=0.0.0.0` à la commande de démarrage ci-dessus. Connectez le client à l'adresse IP réelle de l'appareil et autorisez l'accès TCP au port d'écoute. `0.0.0.0` est une adresse de liaison, pas l'adresse à saisir dans le client.

L'éditeur Defold demande automatiquement cette liaison distante et utilise le port `8172 + project.instance_index` pour les cibles distantes. Il ne peut pas découvrir un port distant choisi dynamiquement. Si vous avez déjà démarré l'écoute distante sur localhost ou sur un autre port, redémarrez le moteur avant d'attacher le débogueur depuis l'éditeur.

Le débogueur peut évaluer du code Lua et ne dispose d'aucune authentification. N'activez l'accès distant que sur un réseau de développement de confiance.

### Clients externes {#external-clients}

Utilisez un client prenant en charge l'attachement direct à un serveur DAP via TCP. Configurez sa correspondance des sources vers le dossier contenant `game.project` (l'argument d'attachement DAP `localRoot`). Démarrez d'abord l'écoute du moteur, puis attachez le client.

#### VS Code {#vs-code}

Installez l'[extension Lua Debug](https://marketplace.visualstudio.com/items?itemName=actboy168.lua-debug) (`actboy168.lua-debug`), ouvrez dans VS Code le dossier contenant `game.project` et ajoutez cette configuration à `.vscode/launch.json` :

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Defold Lua",
      "type": "lua",
      "request": "attach",
      "address": "127.0.0.1:8172",
      "debugServer": 8172,
      "localRoot": "${workspaceFolder}",
      "stopOnEntry": false
    }
  ]
}
```

Si VS Code ouvre un fichier `.script`, `.gui_script` ou `.render_script` comme du texte brut, sélectionnez **Lua** dans l'indicateur de langue de la barre d'état avant de définir les points d'arrêt.

Placez un point d'arrêt, par exemple dans la fonction `init()` d'un script. Démarrez le moteur avec la [commande de démarrage ci-dessus](#starting-the-listener), puis sélectionnez **Attach to Defold Lua** dans la vue **Run and Debug** de VS Code. Avec `debugger.wait=1`, le moteur exécute les scripts de démarrage après l'installation des points d'arrêt par le client. Définissez `stopOnEntry` sur `true` si vous souhaitez aussi mettre en pause à la prochaine ligne Lua après l'attachement.

Le [paramètre `debugServer` de VS Code](https://code.visualstudio.com/api/extension-guides/debugger-extension#development-setup-for-mock-debug) se connecte directement au port d'écoute TCP local du moteur. Le champ `address` est requis par la configuration d'attachement de l'extension Lua Debug. Si vous modifiez le port d'écoute, mettez à jour les deux champs. `localRoot` doit pointer vers le dossier du projet pour permettre au client d'associer les noms des sources Lua du moteur à vos fichiers.

Pour un moteur distant, redirigez son port DAP vers localhost et indiquez le port redirigé dans les deux champs, ou utilisez un client DAP qui se connecte directement à l'hôte distant.


## Onglet Breakpoints {#breakpoints-tab}

  ![onglet Breakpoints](images/debugging/breakpoints_tab.png)

  Lorsque vous utilisez plusieurs points d'arrêt répartis dans différents scripts, l'onglet Breakpoints fournit une vue centralisée pour gérer tous vos points d'arrêt au même endroit.

##### Commandes de chaque point d'arrêt {#individual-breakpoint-controls}

  Pour agir sur un point d'arrêt en particulier :
  - Cliquez sur l'icône rouge de corbeille pour supprimer un point d'arrêt
  - Double-cliquez sur la ligne (en dehors de la zone de condition) pour accéder à cette ligne dans la vue Code View
  - Double-cliquez sur la cellule de condition ou cliquez sur l'icône de stylo pour modifier les points d'arrêt conditionnels
  - Cliquez sur le bouton d'effacement X qui apparaît au survol d'une cellule de condition pour effacer la condition

##### Opérations groupées {#batch-operations}

  Sélectionnez plusieurs points d'arrêt avec Ctrl/Cmd+click ou Shift+click, puis faites un clic droit pour effectuer des actions groupées. Vous pouvez modifier simultanément les conditions de plusieurs points d'arrêt, changer leur état actif ou les supprimer entièrement.

  Les boutons de la barre d'outils permettent d'activer, de désactiver ou d'inverser l'état de tous les points d'arrêt à la fois, ce qui est utile lorsque vous souhaitez exécuter votre jeu sans interruption tout en conservant leurs positions. Vous pouvez également tous les supprimer une fois votre session de débogage terminée.

## Bibliothèque de débogage Lua {#lua-debug-library}

Lua est livré avec une bibliothèque de débogage qui est utile dans certaines situations, en particulier si vous avez besoin d'inspecter les mécanismes internes de votre environnement Lua. Vous trouverez davantage d'informations dans [le chapitre du manuel Lua consacré à la bibliothèque de débogage](http://www.lua.org/pil/contents.html#23).

## Liste de vérification du débogage {#debugging-checklist}

Si vous rencontrez une erreur ou si votre jeu ne se comporte pas comme prévu, voici une liste de vérification pour le débogage :

1. Vérifiez la sortie de la console et assurez-vous qu'elle ne contient aucune erreur d'exécution.

2. Ajoutez des instructions `print` à votre code pour vérifier qu'il est effectivement exécuté.

3. S'il ne s'exécute pas, vérifiez que vous avez effectué dans l'éditeur la configuration nécessaire à son exécution. Le script est-il ajouté au bon objet de jeu ? Votre script a-t-il acquis le focus d'entrée ? Les déclencheurs d'entrée sont-ils corrects ? Le code du shader est-il ajouté au matériau ? Etc.

4. Si votre code dépend des valeurs de variables (dans une instruction if, par exemple), affichez ces valeurs avec `print` à l'endroit où elles sont utilisées ou vérifiées, ou inspectez-les avec le débogueur.

Trouver un bogue peut parfois être un processus difficile et long, qui vous oblige à parcourir votre code morceau par morceau, à tout vérifier, à cerner le code défectueux et à éliminer les sources d'erreur. La meilleure méthode pour y parvenir est appelée « diviser pour régner » :

1. Déterminez quelle moitié du code (ou quelle partie plus petite) doit contenir le bogue.
2. Déterminez à nouveau quelle moitié de cette moitié doit contenir le bogue.
3. Continuez à réduire la portion de code qui doit provoquer le bogue jusqu'à ce que vous le trouviez.

Bonne chasse aux bogues !

## Débogage des problèmes de physique {#debugging-problems-with-physics}

Si vous rencontrez des problèmes de physique et que les collisions ne fonctionnent pas comme prévu, il est recommandé d'activer le débogage de la physique. Cochez la case *Debug* dans la section *Physics* du fichier *game.project* :

![paramètre de débogage de la physique](images/debugging/physics_debug_setting.png)

Lorsque cette case est cochée, Defold dessine toutes les formes de collision et tous les points de contact des collisions :

![visualisation du débogage de la physique](images/debugging/physics_debug_visualisation.png)
