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

Pour lancer le débogueur, sélectionnez <kbd>Debug ▸ Start/Attach</kbd>. Cette commande démarre le jeu avec le débogueur attaché ou attache le débogueur à un jeu déjà en cours d'exécution.

![vue d'ensemble](images/debugging/overview.png)

Dès que le débogueur est attaché, vous pouvez contrôler l'exécution du jeu à l'aide des boutons de commande du débogueur dans la console ou du menu <kbd>Debug</kbd> :

Break
: ![pause](images/debugging/pause.svg){width=60px .left}
  Interrompez immédiatement l'exécution du jeu à l'endroit où elle se trouve. Vous pouvez alors inspecter l'état du jeu, avancer pas à pas ou poursuivre l'exécution jusqu'au prochain point d'arrêt. La position actuelle de l'exécution est indiquée dans l'éditeur de code :

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
Une ligne de code Lua ne correspond pas à une seule expression. L'exécution pas à pas dans le débogueur avance d'une expression à la fois, ce qui signifie qu'actuellement, vous devrez peut-être appuyer plusieurs fois sur le bouton de pas à pas pour passer à la ligne suivante.
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
: Lorsque le débogueur est attaché et que le jeu est arrêté à un point d'arrêt, un environnement d'exécution Lua est disponible dans le contexte actuel. Saisissez des expressions Lua en bas de la console et appuyez sur <kbd>Enter</kbd> pour les évaluer :

  ![console](images/debugging/console.png)

  Il n'est actuellement pas possible de modifier les variables au moyen de l'évaluateur.

Détachement du débogueur
: Sélectionnez <kbd>Debug ▸ Detach Debugger</kbd> pour détacher le débogueur du jeu. Le jeu reprend immédiatement son exécution.

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
