---
title: Écrire du code
brief: Ce manuel explique brièvement comment travailler avec du code dans Defold.
---

# Écrire du code {#writing-code}

Bien que Defold vous permette de créer une grande partie du contenu de votre jeu à l'aide d'outils visuels tels que les éditeurs de tilemaps et d'effets de particules, vous devez toujours créer la logique du jeu dans un éditeur de code. La logique du jeu est écrite dans le [langage de programmation Lua](https://www.lua.org/), tandis que les extensions du moteur lui-même sont écrites dans le ou les langages natifs de la plateforme cible.

## Écrire du code Lua {#writing-lua-code}

Defold utilise Lua 5.1 et LuaJIT (selon la plateforme cible), et vous devez respecter les spécifications du langage pour ces versions précises de Lua lorsque vous écrivez la logique de votre jeu. Pour plus de détails sur l'utilisation de Lua dans Defold, consultez notre [manuel Lua dans Defold](/manuals/lua).

## Utiliser d'autres langages transpilés en Lua {#using-other-languages-that-transpile-to-lua}

Defold prend en charge l'utilisation de transpileurs qui génèrent du code Lua. Lorsqu'une extension de transpilation est installée, vous pouvez utiliser d'autres langages, tels que [Teal](https://github.com/defold/extension-teal), pour écrire du code Lua soumis à une vérification statique. Cette fonctionnalité en préversion présente des limites : la prise en charge actuelle des transpileurs ne donne pas accès aux informations sur les modules et les fonctions définis dans l'environnement d'exécution Lua de Defold. Cela signifie que pour utiliser des API Defold telles que `go.animate`, vous devrez écrire vous-même des définitions externes.

## Écrire du code natif {#writing-native-code}

Defold vous permet d'étendre le moteur de jeu avec du code natif pour accéder à des fonctionnalités propres à une plateforme que le moteur lui-même ne fournit pas. Vous pouvez également utiliser du code natif lorsque les performances de Lua ne suffisent pas (calculs gourmands en ressources, traitement d'images, etc.). Consultez nos [manuels sur les extensions natives](/manuals/extensions/) pour en savoir plus.

## Utiliser l'éditeur de code intégré {#using-the-built-in-code-editor}

Defold dispose d'un éditeur de code intégré qui vous permet d'ouvrir et de modifier des fichiers Lua (.lua), des fichiers de script Defold (.script, .gui_script et .render_script), ainsi que tout autre fichier dont l'extension n'est pas prise en charge nativement par l'éditeur. De plus, l'éditeur propose la coloration syntaxique pour les fichiers Lua et les fichiers de script.

![](/images/editor/code-editor.png)

### Complétion de code {#code-completion}

L'éditeur de code intégré propose la complétion des fonctions pendant que vous écrivez du code :

![](/images/editor/codecompletion.png)

Appuyez sur <kbd>CTRL</kbd> + <kbd>Space</kbd> pour afficher des informations supplémentaires sur les fonctions, les arguments et les valeurs de retour :

![](/images/editor/apireference.png)

### Accéder à un symbole {#jump-to-symbol}

L'éditeur de code intégré peut afficher une liste des symboles du fichier de code actuel, tels que les fonctions, les objets et les variables, dans laquelle vous pouvez effectuer une recherche. Sélectionnez <kbd>View ▸ Jump to Symbol…</kbd>, ou appuyez sur <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd> sous Windows et Linux, ou sur <kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd> sous macOS.

Commencez à saisir du texte pour effectuer une recherche approximative parmi les symboles, utilisez les touches fléchées pour parcourir les résultats et prévisualiser leur emplacement dans l'éditeur, puis appuyez sur <kbd>Enter</kbd> pour accéder au symbole sélectionné. Appuyez sur <kbd>Esc</kbd> pour fermer la boîte de dialogue et revenir aux positions précédentes du curseur et du défilement.

![](/images/editor/jump-to-symbol.png)

### Configuration de l'analyse statique {#linting-configuration}

L'éditeur de code intégré effectue une analyse statique du code à l'aide de [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) et du [serveur de langage Lua](https://luals.github.io/wiki/diagnostics/). Pour configurer Luacheck, créez un fichier `.luacheckrc` à la racine du projet. Vous pouvez consulter la [page de configuration de Luacheck](https://luacheck.readthedocs.io/en/stable/config.html) pour connaître la liste des options disponibles. Defold utilise les paramètres par défaut suivants pour la configuration de Luacheck :

```lua
unused_args = false      -- don't warn on unused arguments (common for .script files)
max_line_length = false  -- don't warn on long lines
ignore = {
    "611",               -- line contains only whitespace
    "612",               -- line contains trailing whitespace
    "614"                -- trailing whitespace in a comment
},
```

## Utiliser un éditeur de code externe {#using-an-external-code-editor}

L'éditeur de code de Defold fournit les fonctionnalités de base nécessaires pour écrire du code. Toutefois, pour les cas d'utilisation plus avancés ou pour les utilisateurs expérimentés qui ont un éditeur de code favori, il est possible de demander à Defold d'ouvrir les fichiers dans un éditeur externe. Dans l'[onglet Code de la fenêtre Preferences](/manuals/editor-preferences/#code), vous pouvez définir l'éditeur externe à utiliser pour modifier le code.

### Visual Studio Code - Defold Kit {#visual-studio-code-defold-kit}

Defold Kit est un plugin pour Visual Studio Code qui propose les fonctionnalités suivantes :

* Installation des extensions recommandées
* Coloration syntaxique, complétion automatique et analyse statique de Lua
* Application des paramètres appropriés à l'espace de travail
* Annotations Lua pour l'API Defold
* Annotations Lua pour les dépendances
* Compilation et lancement
* Débogage avec points d'arrêt
* Création de bundles pour toutes les plateformes
* Déploiement sur les appareils mobiles connectés

Pour en savoir plus et installer Defold Kit, consultez le [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).


## Logiciels de documentation {#documentation-software}

Des paquets de documentation de référence de l'API créés par la communauté sont disponibles pour [Dash et Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
