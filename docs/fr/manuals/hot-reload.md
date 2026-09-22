---
title: Rechargement à chaud
brief: Ce manuel explique la fonctionnalité de rechargement à chaud de Defold.
---

# Rechargement à chaud des ressources {#hot-reloading-resources}

Defold vous permet de recharger des ressources à chaud. Lors du développement d'un jeu, cette fonctionnalité permet d'accélérer considérablement certaines tâches. Elle vous permet de modifier le code et le contenu d'un jeu pendant son exécution. Voici quelques cas d'utilisation courants :

- Ajuster les paramètres de jeu dans les scripts Lua.
- Modifier et ajuster des éléments graphiques (comme des effets de particules ou des éléments d'interface graphique) et voir les résultats dans leur contexte.
- Modifier et ajuster le code des shaders et voir les résultats dans leur contexte.
- Faciliter les tests du jeu en redémarrant des niveaux, en définissant l'état du jeu, etc. — sans arrêter le jeu.

## Comment recharger à chaud {#how-to-hot-reload}

Démarrez votre jeu depuis l'éditeur (<kbd>Project ▸ Build</kbd>).

Pour recharger ensuite une ressource mise à jour, sélectionnez simplement l'élément de menu <kbd>File ▸ Hot Reload</kbd> ou appuyez sur le raccourci clavier correspondant :

![Rechargement des ressources](images/hot-reload/menu.png)

## Rechargement à chaud sur un appareil {#hot-reloading-on-device}

Le rechargement à chaud fonctionne aussi bien sur un appareil que sur un ordinateur. Pour l'utiliser sur un appareil, exécutez un build de débogage de votre jeu ou l'[application de développement](/manuals/dev-app) sur votre appareil mobile, puis sélectionnez-le comme cible dans l'éditeur :

![Appareil cible](images/hot-reload/target.png)

Désormais, lorsque vous compilez et exécutez le jeu, l'éditeur transfère toutes les ressources vers l'application en cours d'exécution sur l'appareil et démarre le jeu. Dès lors, tout fichier que vous rechargez à chaud sera mis à jour sur l'appareil.

Par exemple, pour ajouter deux boutons à une interface graphique affichée dans un jeu en cours d'exécution sur votre téléphone, ouvrez simplement le fichier GUI :

![Rechargement de l'interface graphique](images/hot-reload/gui.png)

Ajoutez les nouveaux boutons, enregistrez et rechargez à chaud le fichier GUI. Vous pouvez maintenant voir les nouveaux boutons sur l'écran du téléphone :

![Interface graphique rechargée](images/hot-reload/gui-reloaded.png)

Lorsque vous rechargez un fichier à chaud, le moteur affiche chaque fichier de ressource rechargé dans la console.

## Rechargement des scripts {#reloading-scripts}

Tout fichier de script Lua rechargé sera réexécuté dans l'environnement Lua en cours d'exécution.

```lua
local my_value = 10

function update(self, dt)
    print(my_value)
end
```

Le fait de modifier `my_value` pour lui donner la valeur 11 et de recharger le fichier à chaud aura un effet immédiat :

```text
...
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
INFO:RESOURCE: /main/hunter.scriptc was successfully reloaded.
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
...
```

Notez que le rechargement à chaud ne modifie pas l'exécution des fonctions du cycle de vie. Par exemple, `init()` n'est pas appelée lors d'un rechargement à chaud. Toutefois, si vous redéfinissez les fonctions du cycle de vie, leurs nouvelles versions seront utilisées.

## Rechargement des modules Lua {#reloading-lua-modules}

Tant que vous ajoutez des variables à la portée globale dans un fichier de module, le rechargement du fichier modifiera ces variables globales :

```lua
--- my_module.lua
my_module = {}
my_module.val = 10
```

```lua
-- user.script
require "my_module"

function update(self, dt)
    print(my_module.val) -- hot reload "my_module.lua" and the new value will print
end
```

Une pratique courante pour les modules Lua consiste à construire une table locale, à la remplir, puis à la renvoyer :

```lua
--- my_module.lua
local M = {} -- a new table object is created here
M.val = 10
return M
```

```lua
-- user.script
local mm = require "my_module"

function update(self, dt)
    print(mm.val) -- will print 10 even if you change and hot reload "my_module.lua"
end
```

Modifier et recharger `my_module.lua` ne changera _pas_ le comportement de `user.script`. Consultez [le manuel sur les modules](/manuals/modules) pour en savoir plus sur les raisons de ce comportement et sur la façon d'éviter ce piège.

## La fonction on_reload() {#the-on_reload-function}

Chaque composant (component) de type script peut définir une fonction `on_reload()`. Si elle existe, elle sera appelée à chaque rechargement du script. Cela permet d'inspecter ou de modifier des données, d'envoyer des messages, etc. :

```lua
function on_reload(self)
    print(self.velocity)

    msg.post("/level#controller", "setup")
end
```

## Rechargement du code des shaders {#reloading-shader-code}

Lors du rechargement des shaders de sommets et de fragments, le code GLSL est recompilé par le pilote graphique et transféré vers le GPU. Si le code du shader provoque un plantage, ce qui peut facilement arriver puisque le GLSL s'écrit à un très bas niveau, le moteur plantera également.
