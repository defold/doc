---
title: Les modules Lua dans Defold
brief: Les modules Lua vous permettent de structurer votre projet et de créer du code de bibliothèque réutilisable. Ce manuel explique comment procéder dans Defold.
---

# Les modules Lua {#lua-modules}

Les modules Lua vous permettent de structurer votre projet et de créer du code de bibliothèque réutilisable. Il est généralement préférable d'éviter la duplication dans vos projets. Defold vous permet d'utiliser les modules de Lua pour inclure des fichiers de script dans d'autres fichiers de script. Vous pouvez ainsi encapsuler des fonctionnalités (et des données) dans un fichier de script externe pour les réutiliser dans les fichiers de script d'objet de jeu (game object) et d'interface graphique.

## Chargement de fichiers Lua avec require {#requiring-lua-files}

Le code Lua stocké dans des fichiers portant l'extension `.lua`, où qu'ils se trouvent dans l'arborescence de votre projet de jeu, peut être chargé avec `require` dans des fichiers de script et de script d'interface graphique. Pour créer un nouveau fichier de module Lua, faites un clic droit sur le dossier dans lequel vous voulez le créer dans la vue *Assets*, puis sélectionnez <kbd>New... ▸ Lua Module</kbd>. Donnez un nom unique au fichier et appuyez sur <kbd>Ok</kbd> :

![nouveau fichier](images/modules/new_name.png)

Supposons que le code suivant soit ajouté au fichier « `main/anim.lua` » :

```lua
function direction_animation(direction, char)
    local d = ""
    if direction.x > 0 then
        d = "right"
    elseif direction.x < 0 then
        d = "left"
    elseif direction.y > 0 then
        d = "up"
    elseif direction.y < 0 then
        d = "down"
    end
    return hash(char .. "-" .. d)
end
```

N'importe quel script peut alors charger ce fichier avec `require` et utiliser la fonction :

```lua
require "main.anim"

function update(self, dt)
    -- update position, set direction etc
    ...

    -- set animation
    local anim = direction_animation(self.dir, "player")
    if anim ~= self.current_anim then
        sprite.play_flipbook("#sprite", anim)
        self.current_anim = anim
    end
end
```

La fonction `require` charge le module indiqué. Elle commence par consulter la table `package.loaded` pour déterminer si le module est déjà chargé. Si c'est le cas, `require` renvoie la valeur stockée dans `package.loaded[module_name]`. Sinon, elle charge et évalue le fichier au moyen d'un chargeur.

La syntaxe de la chaîne de nom de fichier fournie à `require` est un peu particulière. Lua remplace les caractères `.` de cette chaîne par des séparateurs de chemin : `/` sur macOS et Linux, et `\\` sur Windows.

Notez qu'il est généralement déconseillé d'utiliser la portée globale pour stocker l'état et définir des fonctions comme nous l'avons fait ci-dessus. Vous risquez de provoquer des collisions de noms, d'exposer l'état du module ou d'introduire un couplage entre les utilisateurs du module.

## Modules {#modules}

Pour encapsuler des données et des fonctions, Lua utilise des _modules_. Un module Lua est une table Lua ordinaire qui contient des fonctions et des données. La table est déclarée locale pour ne pas polluer la portée globale :

```lua
local M = {}

-- private
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

Le module peut alors être utilisé. Là encore, il est préférable de l'affecter à une variable locale :

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## Rechargement à chaud des modules {#hot-reloading-modules}

Prenons un module simple :

```lua
-- module.lua
local M = {} -- creates a new table in the local scope
M.value = 4711
return M
```

Et un code qui utilise ce module : 

```lua
local m = require "module"
print(m.value) --> "4711" (even if "module.lua" is changed and hot reloaded)
```

Si vous rechargez à chaud le fichier du module, le code est de nouveau exécuté, mais rien ne se passe pour `m.value`. Pourquoi ?

Tout d'abord, la table créée dans `module.lua` est créée dans la portée locale et une _référence_ à cette table est renvoyée à l'utilisateur. Le rechargement de `module.lua` évalue de nouveau le code du module, mais cela crée une nouvelle table dans la portée locale au lieu de mettre à jour la table à laquelle `m` fait référence.

Ensuite, Lua met en cache les fichiers chargés avec `require`. La première fois qu'un fichier est demandé, il est placé dans la table [`package.loaded`](/ref/package/#package.loaded) pour pouvoir être lu plus rapidement lors des appels suivants à `require`. Vous pouvez forcer la relecture d'un fichier depuis le disque en définissant son entrée sur `nil` : `package.loaded["my_module"] = nil`.

Pour recharger correctement un module à chaud, vous devez recharger le module, réinitialiser le cache, puis recharger tous les fichiers qui utilisent le module. C'est loin d'être optimal.

Vous pouvez plutôt envisager une solution de contournement à utiliser _pendant le développement_ : placez la table du module dans la portée globale et faites en sorte que `M` fasse référence à cette table globale au lieu de créer une nouvelle table à chaque évaluation du fichier. Le rechargement du module modifie alors le contenu de la table globale :

```lua
--- module.lua

-- Replace with local M = {} when done
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## Modules et état {#modules-and-state}

Les modules avec état conservent un état interne partagé entre tous les utilisateurs du module et peuvent être comparés à des singletons :

```lua
local M = {}

-- all users of the module will share this table
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

Un module sans état, en revanche, ne conserve aucun état interne. Il fournit un mécanisme permettant d'externaliser l'état dans une table distincte, locale à l'utilisateur du module. Voici plusieurs façons de mettre cela en œuvre :

Utilisation d'une table d'état
: L'approche la plus simple est peut-être d'utiliser une fonction constructeur qui renvoie une nouvelle table contenant uniquement l'état. L'état est explicitement passé au module comme premier paramètre de chaque fonction qui manipule la table d'état.

  ```lua
  local M = {}
  
  function M.alter_state(the_state, v)
      the_state.value = the_state.value + v
  end
  
  function M.get_state(the_state)
      return the_state.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return state
  end
  
  return M
  ```
  
  Utilisez le module ainsi :
  
  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

Utilisation de métatables
: Une autre approche consiste à utiliser une fonction constructeur qui renvoie une nouvelle table contenant l'état et les fonctions publiques du module à chaque appel :

  ```lua
  local M = {}
  
  function M:alter_state(v)
      -- self is added as first argument when using : notation
      self.value = self.value + v
  end
  
  function M:get_state()
      return self.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return setmetatable(state, { __index = M })
  end
  
  return M
  ```

  Utilisez le module ainsi :

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- "my_state" is added as first argument when using : notation
  print(my_state:get_state()) --> 43
  ```

Utilisation de fermetures lexicales
:  Une troisième méthode consiste à renvoyer une fermeture lexicale contenant l'ensemble de l'état et des fonctions. Il n'est pas nécessaire de passer l'instance en argument (explicitement ou implicitement avec l'opérateur deux-points), comme c'est le cas avec les métatables. Cette méthode est aussi un peu plus rapide que l'utilisation de métatables, car les appels de fonctions n'ont pas besoin de passer par les métaméthodes `__index`, mais chaque fermeture contient sa propre copie des méthodes, ce qui augmente la consommation de mémoire.

  ```lua
  local M = {}
  
  function M.new(v)
      local state = {
          value = v
      }
  
      state.alter_state = function(v)
          state.value = state.value + v
      end
  
      state.get_state = function()
          return state.value
      end
  
      return state
  end
  
  return M
  ```

  Utilisez le module ainsi :

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state()) 
  ```
