---
title: Programmation Lua dans Defold
brief: Ce manuel présente rapidement les bases de la programmation Lua en général et les points à prendre en compte lorsque vous utilisez Lua dans Defold.
---

# Lua dans Defold {#lua-in-defold}

Le moteur Defold intègre le langage Lua pour l'écriture de scripts. Lua est un langage dynamique léger, puissant, rapide et facile à intégrer. Il est largement utilisé comme langage de script dans les jeux vidéo. Les programmes Lua sont écrits dans une syntaxe procédurale simple. Le langage utilise un typage dynamique et s'exécute à l'aide d'un interpréteur de bytecode. Il assure une gestion automatique de la mémoire avec un ramasse-miettes incrémental.

Ce manuel présente rapidement les bases de la programmation Lua en général et les points à prendre en compte lorsque vous utilisez Lua dans Defold. Si vous avez déjà une certaine expérience de Python, Perl, Ruby, JavaScript ou d'un langage dynamique similaire, vous pourrez démarrer assez rapidement. Si vous débutez en programmation, vous souhaiterez peut-être commencer par un livre sur Lua destiné aux débutants. Le choix est vaste.

## Versions de Lua {#lua-versions}

Defold utilise [LuaJIT](https://luajit.org/), une version de Lua fortement optimisée, adaptée aux jeux et aux autres logiciels pour lesquels les performances sont essentielles. Elle assure une compatibilité ascendante complète avec Lua 5.1 et prend en charge toutes les fonctions des bibliothèques standard de Lua ainsi que l'ensemble des fonctions de l'API Lua/C.

LuaJIT ajoute également plusieurs [extensions du langage](https://luajit.org/extensions.html) et certaines fonctionnalités de Lua 5.2 et 5.3.

Nous cherchons à rendre Defold identique sur toutes les plateformes, mais il existe actuellement quelques différences mineures dans la version du langage Lua selon les plateformes :
* iOS n'autorise pas la compilation JIT.
* Nintendo Switch n'autorise pas la compilation JIT.
* HTML5 utilise Lua 5.1.4 à la place de LuaJIT.

::: important
Pour garantir que votre jeu fonctionne sur toutes les plateformes prises en charge, nous vous recommandons vivement d'utiliser UNIQUEMENT les fonctionnalités du langage Lua 5.1.
:::

### Bibliothèques standard et extensions {#standard-libraries-and-extensions}
Defold inclut toutes les [bibliothèques standard de Lua 5.1](http://www.lua.org/manual/5.1/manual.html#5), ainsi qu'une bibliothèque de sockets et une bibliothèque d'opérations sur les bits :

  - base (`assert()`, `error()`, `print()`, `ipairs()`, `require()`, etc.)
  - coroutine
  - package
  - string
  - table
  - math
  - io
  - os
  - debug
  - socket (issue de [LuaSocket](https://github.com/diegonehab/luasocket))
  - bitop (issue de [BitOp](http://bitop.luajit.org/api.html))

Toutes les bibliothèques sont décrites dans la [documentation de référence de l'API](/ref/go).

## Livres et ressources sur Lua {#lua-books-and-resources}

### Ressources en ligne {#online-resources}
* [Programming in Lua (première édition)](http://www.lua.org/pil/contents.html) Les éditions ultérieures sont disponibles au format papier.
* [Manuel de référence de Lua 5.1](http://www.lua.org/manual/5.1/)
* [Apprendre Lua en 15 minutes](http://tylerneylon.com/a/learn-lua/)
* [Awesome Lua - section des tutoriels](https://github.com/LewisJEllis/awesome-lua#tutorials)

### Livres {#books}
* [Programming in Lua](https://www.amazon.com/gp/product/8590379868/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i0) - Programming in Lua est le livre officiel consacré au langage. Il fournit des bases solides à tout programmeur qui souhaite utiliser Lua. Il a été écrit par Roberto Ierusalimschy, l'architecte principal du langage.
* [Lua programming gems](https://www.amazon.com/Programming-Gems-Luiz-Henrique-Figueiredo/dp/8590379841) - Ce recueil d'articles rassemble une partie des connaissances et des pratiques existantes pour bien programmer en Lua.
* [Manuel de référence de Lua 5.1](https://www.amazon.com/gp/product/8590379833/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i4) - Également disponible en ligne (voir ci-dessus)
* [Beginning Lua Programming](https://www.amazon.com/Beginning-Lua-Programming-Kurt-Jung/dp/0470069171)

### Vidéos {#videos}
* [Apprendre Lua en une vidéo](https://www.youtube.com/watch?v=iMacxZQMPXs)

## Syntaxe {#syntax}

Les programmes ont une syntaxe simple et facile à lire. Les instructions s'écrivent à raison d'une par ligne, et il n'est pas nécessaire d'en marquer la fin. Vous pouvez, si vous le souhaitez, utiliser des points-virgules `;` pour séparer les instructions. Les blocs de code sont délimités par des mots-clés et se terminent par le mot-clé `end`. Les commentaires peuvent être écrits sous forme de bloc ou s'étendre jusqu'à la fin de la ligne :

```lua
--[[
Here is a block of comments that can run
over several lines in the source file.
--]]

a = 10
b = 20 ; c = 30 -- two statements on one line

if my_variable == 3 then
    call_some_function(true) -- Here is a line comment
else
    call_another_function(false)
end
```

## Variables et types de données {#variables-and-data-types}

Lua utilise un typage dynamique : les variables n'ont pas de type, mais les valeurs en ont un. 
Contrairement aux langages à typage statique, vous pouvez affecter librement n'importe quelle valeur à n'importe quelle variable. 

Lua possède huit types de base :

`nil`
: Ce type ne possède que la valeur `nil`. Il représente généralement l'absence de valeur utile, par exemple pour les variables auxquelles aucune valeur n'a été affectée.

  ```lua
  print(my_var) -- will print 'nil' since 'my_var' is not yet assigned a value
  ```

boolean
: Possède soit la valeur `true`, soit la valeur `false`. Les conditions dont la valeur est `false` ou `nil` sont considérées comme fausses. Toute autre valeur les rend vraies.

  ```lua
  flag = true
  if flag then
      print("flag is true")
  else
      print("flag is false")
  end

  if my_var then
      print("my_var is not nil nor false!")
  end

  if not my_var then
      print("my_var is either nil or false!")
  end
  ```

number
: Les nombres sont représentés en interne soit par des _entiers_ de 64 bits, soit par des nombres _à virgule flottante_ de 64 bits. Lua convertit automatiquement ces représentations selon les besoins, de sorte que vous n'avez généralement pas à vous en préoccuper.

  ```lua
  print(10) --> prints '10'
  print(10.0) --> '10'
  print(10.000000000001) --> '10.000000000001'

  a = 5 -- integer
  b = 7/3 -- float
  print(a - b) --> '2.6666666666667'
  ```

string
: Les chaînes de caractères sont des séquences immuables d'octets pouvant contenir n'importe quelle valeur sur 8 bits, y compris des zéros intégrés (`\0`). Lua ne fait aucune hypothèse sur le contenu d'une chaîne, ce qui vous permet d'y stocker les données de votre choix. Les littéraux de chaîne s'écrivent entre guillemets simples ou doubles. Lua effectue des conversions entre nombres et chaînes à l'exécution. Les chaînes peuvent être concaténées avec l'opérateur `..`.

  Les chaînes peuvent contenir les séquences d'échappement suivantes, de style C :

  | Séquence | Caractère |
  | -------- | --------- |
  | `\a`     | alerte sonore       |
  | `\b`     | retour arrière |
  | `\f`     | saut de page  |
  | `\n`     | nouvelle ligne    |
  | `\r`     | retour chariot |
  | `\t`     | tabulation horizontale |
  | `\v`     | tabulation verticale   |
  | `\\`     | barre oblique inverse      |
  | `\"`     | guillemet double   |
  | `\'`     | guillemet simple   |
  | `\[`     | crochet ouvrant    |
  | `\]`     | crochet fermant   |
  | `\ddd`   | caractère désigné par sa valeur numérique, où `ddd` est une séquence contenant jusqu'à trois chiffres _décimaux_ |

  ```lua
  my_string = "hello"
  another_string = 'world'
  print(my_string .. another_string) --> "helloworld"

  print("10.2" + 1) --> 11.2
  print(my_string + 1) -- error, can't convert "hello"
  print(my_string .. 1) --> "hello1"

  print("one\nstring") --> one
                       --> string

  print("\097bc") --> "abc"

  multi_line_string = [[
  Here is a chunk of text that runs over several lines. This is all
  put into the string and is sometimes very handy.
  ]]
  ```

function
: Les fonctions sont des valeurs de première classe en Lua : vous pouvez les passer comme paramètres à des fonctions et les renvoyer comme valeurs. Les variables auxquelles une fonction est affectée contiennent une référence à cette fonction. Vous pouvez affecter des fonctions anonymes à des variables, mais Lua fournit un sucre syntaxique (`function name(param1, param2) ... end`) pour vous faciliter la tâche.

  ```lua
  -- Assign 'my_plus' to function
  my_plus = function(p, q)
      return p + q
  end

  print(my_plus(4, 5)) --> 9

  -- Convenient syntax to assign function to variable 'my_mult'
  function my_mult(p, q)
      return p * q
  end

  print(my_mult(4, 5)) --> 20

  -- Takes a function as parameter 'func'
  function operate(func, p, q)
      return func(p, q) -- Calls the provided function with parameters 'p' and 'q'
  end

  print(operate(my_plus, 4, 5)) --> 9
  print(operate(my_mult, 4, 5)) --> 20

  -- Create an adder function and return it
  function create_adder(n)
      return function(a)
          return a + n
      end
  end

  adder = create_adder(2)
  print(adder(3)) --> 5
  print(adder(10)) --> 12
  ```

table
: Les tables sont le seul type de Lua permettant de structurer les données. Ce sont des _objets_ de type tableau associatif, utilisés pour représenter des listes, des tableaux, des séquences, des tables de symboles, des ensembles, des enregistrements, des graphes, des arbres, etc. Les tables sont toujours anonymes et les variables auxquelles vous affectez une table ne contiennent pas la table elle-même, mais une référence à celle-ci. Lorsque vous initialisez une table sous forme de séquence, le premier indice est `1`, et non `0`.

  ```lua
  -- Initialize a table as a sequence
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}
  print(weekdays[1]) --> "Sunday"
  print(weekdays[5]) --> "Thursday"

  -- Initialize a table as a record with sequence values
  moons = { Earth = { "Moon" },
            Uranus = { "Puck", "Miranda", "Ariel", "Umbriel", "Titania", "Oberon" } }
  print(moons.Uranus[3]) --> "Ariel"

  -- Build a table from an empty constructor {}
  a = 1
  t = {}
  t[1] = "first"
  t[a + 1] = "second"
  t.x = 1 -- same as t["x"] = 1

  -- Iterate over the table key, value pairs
  for key, value in pairs(t) do
      print(key, value)
  end
  --> 1   first
  --> 2   second
  --> x   1

  u = t -- u now refers to the same table as t
  u[1] = "changed"

  for key, value in pairs(t) do -- still iterating over t!
      print(key, value)
  end
  --> 1   changed
  --> 2   second
  --> x   1
  ```

userdata
: Le type `userdata` permet de stocker des données C arbitraires dans des variables Lua. Defold utilise des objets Lua `userdata` pour stocker des valeurs hachées (hash), des objets URL (url), des objets mathématiques (vector3, vector4, matrix4, quaternion), des objets de jeu (game object), des nœuds d'interface graphique (node), des prédicats de rendu (predicate), des cibles de rendu (render_target) et des tampons de constantes de rendu (constant_buffer)

thread
: Les threads représentent des fils d'exécution indépendants et servent à implémenter les coroutines. Voir ci-dessous pour plus de détails.

## Opérateurs {#operators}

Opérateurs arithmétiques
: Les opérateurs mathématiques `+`, `-`, `*`, `/`, l'opérateur unaire `-` (négation) et l'opérateur de puissance `^`.

  ```lua
  a = -1
  print(a * 2 + 3 / 4^5) --> -1.9970703125
  ```

  Lua assure des conversions automatiques entre nombres et chaînes à l'exécution. Toute opération numérique appliquée à une chaîne tente de la convertir en nombre :

  ```lua
  print("10" + 1) --> 11
  ```

Opérateurs relationnels et de comparaison
: `<` (inférieur à), `>` (supérieur à), `<=` (inférieur ou égal à), `>=` (supérieur ou égal à), `==` (égal à), `~=` (différent de). Ces opérateurs renvoient toujours `true` ou `false`. Les valeurs de types différents sont considérées comme différentes. Si leurs types sont identiques, elles sont comparées selon leur valeur. Lua compare les tables, les `userdata` et les fonctions par référence. Deux valeurs de ces types ne sont considérées comme égales que si elles font référence au même objet.

  ```lua
  a = 5
  b = 6

  if a <= b then
      print("a is less than or equal to b")
  end

  print("A" < "a") --> true
  print("aa" < "ab") --> true
  print(10 == "10") --> false
  print(tostring(10) == "10") --> true
  ```

Opérateurs logiques
: `and`, `or` et `not`. `and` renvoie son premier argument s'il vaut `false`, sinon il renvoie son second argument. `or` renvoie son premier argument s'il ne vaut pas `false`, sinon il renvoie son second argument.

  ```lua
  print(true or false) --> true
  print(true and false) --> false
  print(not false) --> true

  if a == 5 and b == 6 then
      print("a is 5 and b is 6")
  end
  ```

Concaténation
: Les chaînes peuvent être concaténées avec l'opérateur `..`. Les nombres sont convertis en chaînes lors de la concaténation.

  ```lua
  print("donkey" .. "kong") --> "donkeykong"
  print(1 .. 2) --> "12"
  ```

Longueur
: L'opérateur unaire de longueur `#`. La longueur d'une chaîne est son nombre d'octets. La longueur d'une table est la longueur de sa séquence, c'est-à-dire le nombre d'indices numérotés à partir de `1` dont la valeur n'est pas `nil`. Remarque : si la séquence comporte des « trous » de valeur `nil`, la longueur peut être n'importe quel indice précédant une valeur `nil`.

  ```lua
  s = "donkey"
  print(#s) --> 6

  t = { "a", "b", "c", "d" }
  print(#t) --> 4

  u = { a = 1, b = 2, c = 3 }
  print(#u) --> 0

  v = { "a", "b", nil }
  print(#v) --> 2
  ```

## Contrôle du flux {#flow-control}

Lua fournit l'ensemble habituel de structures de contrôle du flux.

if---then---else
: Teste une condition et exécute la partie `then` si elle est vraie, sinon exécute la partie `else` (facultative). Au lieu d'imbriquer des instructions `if`, vous pouvez utiliser `elseif`. Cela remplace l'instruction switch, dont Lua ne dispose pas.

  ```lua
  a = 5
  b = 4

  if a < b then
      print("a is smaller than b")
  end

  if a == '1' then
      print("a is 1")
  elseif a == '2' then
      print("a is 2")
  elseif a == '3' then
      print("a is 3")
  else
      print("I have no idea what a is...")
  end
  ```

while
: Teste une condition et exécute le bloc tant qu'elle est vraie.

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- Print each weekday
  i = 1
  while weekdays[i] do
      print(weekdays[i])
      i = i + 1
  end
  ```

repeat---until
: Répète le bloc jusqu'à ce qu'une condition soit vraie. La condition est testée après le corps du bloc, qui s'exécute donc au moins une fois.

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- Print each weekday
  i = 0
  repeat
      i = i + 1
      print(weekdays[i])
  until weekdays[i] == "Saturday"
  ```

for
: Lua propose deux types de boucles `for` : numérique et générique. La boucle `for` numérique prend deux ou trois valeurs numériques, tandis que la boucle `for` générique parcourt toutes les valeurs renvoyées par une fonction _itérateur_.

  ```lua
  -- Print the numbers 1 to 10
  for i = 1, 10 do
      print(i)
  end

  -- Print the numbers 1 to 10 and increment with 2 each time
  for i = 1, 10, 2 do
      print(i)
  end

  -- Print the numbers 10 to 1
  for i=10, 1, -1 do
      print(i)
  end

  t = { "a", "b", "c", "d" }
  -- Iterate over the sequence and print the values
  for i, v in ipairs(t) do
      print(v)
  end
  ```

break et return
: Utilisez l'instruction `break` pour sortir d'un bloc interne d'une boucle `for`, `while` ou `repeat`. Utilisez `return` pour renvoyer une valeur depuis une fonction ou pour terminer l'exécution d'une fonction et rendre la main à l'appelant. `break` ou `return` ne peut apparaître qu'en dernière instruction d'un bloc.

  ```lua
  a = 1
  while true do
      a = a + 1
      if a >= 100 then
          break
      end
  end

  function my_add(a, b)
      return a + b
  end

  print(my_add(10, 12)) --> 22
  ```

## Variables locales, globales et portée lexicale {#locals-globals-and-lexical-scoping}

Toutes les variables que vous déclarez sont globales par défaut : elles sont accessibles dans toutes les parties du contexte d'exécution Lua. Vous pouvez déclarer explicitement des variables `local`, ce qui signifie qu'elles n'existeront qu'à l'intérieur de la portée actuelle.

Chaque fichier source Lua définit une portée distincte. Les déclarations `local` au niveau le plus externe d'un fichier rendent la variable locale à ce fichier de script Lua. Chaque fonction crée une nouvelle portée imbriquée et chaque bloc de structure de contrôle crée des portées supplémentaires. Vous pouvez créer explicitement une portée avec les mots-clés `do` et `end`. Lua utilise une portée lexicale : une portée a pleinement accès aux variables _locales_ de la portée englobante. Notez que les variables locales doivent être déclarées avant leur utilisation.

```lua
function my_func(a, b)
    -- 'a' and 'b' are local to this function and available through its scope

    do
        local x = 1
    end

    print(x) --> nil. 'x' is not available outside the do-end scope
    print(foo) --> nil. 'foo' is declared after 'my_func'
    print(foo_global) --> "value 2"
end

local foo = "value 1"
foo_global = "value 2"

print(foo) --> "value 1". 'foo' is available in the topmost scope after declaration.
```

Notez que si vous déclarez des fonctions `local` dans un fichier de script (ce qui est généralement une bonne idée), vous devez faire attention à l'ordre du code. Vous pouvez utiliser des déclarations anticipées si certaines fonctions s'appellent mutuellement.

```lua
local func2 -- Forward declare 'func2'

local function func1(a)
    print("func1")
    func2(a)
end

function func2(a) -- or func2 = function(a)
    print("func2")
    if a < 10 then
        func1(a + 1)
    end
end

function init(self)
    func1(1)
end
```

Si vous écrivez une fonction à l'intérieur d'une autre fonction, elle a elle aussi pleinement accès aux variables locales de la fonction englobante. C'est une construction très puissante.

```lua
function create_counter(x)
    -- 'x' is a local variable in 'create_counter'
    return function()
        x = x + 1
        return x
    end
end

count1 = create_counter(10)
count2 = create_counter(20)
print(count1()) --> 11
print(count2()) --> 21
print(count1()) --> 12
```

## Masquage des variables {#variable-shadowing}

Les variables locales déclarées dans un bloc masquent les variables de même nom d'un bloc englobant.

```lua
my_global = "global"
print(my_global) -->"global"

local v = "local"
print(v) --> "local"

local function test(v)
    print(v)
end

function init(self)
    v = "apple"
    print(v) --> "apple"
    test("banana") --> "banana"
end
```

## Coroutines {#coroutines}

Les fonctions s'exécutent du début à la fin, sans possibilité de les interrompre en cours de route. Les coroutines le permettent, ce qui peut être très pratique dans certains cas. Supposons que nous voulions créer une animation très précise, image par image, où nous déplaçons un objet de jeu d'une position y égale à `0` vers des positions y bien précises, de l'image 1 à l'image 5. Nous pourrions le faire avec un compteur dans la fonction `update()` (voir ci-dessous) et une liste des positions. Avec une coroutine, nous obtenons cependant une implémentation très claire, facile à étendre et à utiliser. Tout l'état est contenu dans la coroutine elle-même.

Lorsqu'une coroutine cède la main, elle rend le contrôle à l'appelant, mais mémorise son point d'exécution pour pouvoir reprendre à cet endroit plus tard.

```lua
-- This is our coroutine
local function sequence(self)
    coroutine.yield(120)
    coroutine.yield(320)
    coroutine.yield(510)
    coroutine.yield(240)
    return 440 -- return the final value
end

function init(self)
    self.co = coroutine.create(sequence) -- Create the coroutine. 'self.co' is a thread object
    go.set_position(vmath.vector3(100, 0, 0)) -- Set initial position
end

function update(self, dt)
    local status, y_pos = coroutine.resume(self.co, self) -- Continue execution of coroutine.
    if status then
        -- If the coroutine is still not terminated/dead, use its yielded return value as a new position
        go.set_position(vmath.vector3(100, y_pos, 0))
    end
end
```


## Contextes Lua dans Defold {#lua-contexts-in-defold}

Toutes les variables que vous déclarez sont globales par défaut : elles sont accessibles dans toutes les parties du contexte d'exécution Lua. Defold dispose d'un paramètre *shared_state* dans *game.project* qui contrôle ce contexte. Si cette option est activée, tous les scripts, les scripts d'interface graphique et le script de rendu sont évalués dans le même contexte Lua, et les variables globales sont visibles partout. Si l'option n'est pas activée, le moteur exécute les scripts, les scripts d'interface graphique et le script de rendu dans des contextes distincts.

![Contextes](images/lua/lua_contexts.png)

Defold vous permet d'utiliser le même fichier de script dans plusieurs composants (component) distincts d'objets de jeu. Toutes les variables déclarées localement sont partagées entre les composants qui exécutent le même fichier de script.

```lua
-- 'my_global_value' will be available from all scripts, gui_scripts, render script and modules (Lua files)
my_global_value = "global scope"

-- this value will be shared through all component instances that use this particular script file
local script_value = "script scope"

function init(self, dt)
    -- This value will be available on this script component instance
    self.foo = "self scope"

    -- this value will be available inside init() and after it's declaration
    local local_foo = "local scope"
    print(local_foo)
end

function update(self, dt)
    print(self.foo)
    print(my_global_value)
    print(script_value)
    print(local_foo) -- will print nil, since local_foo is only visible in init()
end
```

## Considérations relatives aux performances {#performance-considerations}

Dans un jeu performant conçu pour fonctionner à 60 images par seconde de façon fluide, de petites erreurs de performance peuvent avoir un impact important sur l'expérience. Certains points généraux simples méritent votre attention, tout comme certains éléments qui pourraient sembler sans problème.

Commençons par les choses simples. Il est généralement préférable d'écrire du code direct, sans boucles inutiles. Il est parfois nécessaire de parcourir des listes d'éléments, mais soyez prudent si la liste est assez longue. Cet exemple s'exécute en un peu plus de 1 milliseconde sur un ordinateur portable tout à fait correct, ce qui peut faire toute la différence lorsque chaque image ne dure que 16 millisecondes (à 60 images par seconde) et que le moteur, le script de rendu, la simulation physique, etc. en consomment déjà une partie.

```lua
local t = socket.gettime()
local table = {}
for i=1,2000 do
    table[i] = vmath.vector3(i, i, i)
end
print((socket.gettime() - t) * 1000)

-- DEBUG:SCRIPT: 0.40388
```

Utilisez la valeur renvoyée par `socket.gettime()` (secondes écoulées depuis l'époque du système) pour mesurer les performances du code suspect.

## Mémoire et ramasse-miettes {#memory-and-garbage-collection}

Par défaut, le ramasse-miettes de Lua s'exécute automatiquement en arrière-plan et récupère la mémoire allouée par l'environnement d'exécution Lua. Récupérer de nombreux déchets mémoire peut prendre du temps ; il est donc préférable de limiter le nombre d'objets à récupérer :

* Les variables locales n'ont en elles-mêmes aucun coût et ne génèrent pas de déchets mémoire. (Par exemple, `local v = 42`)
* Chaque chaîne _nouvelle et unique_ crée un nouvel objet. Écrire `local s = "some_string"` crée un nouvel objet et fait pointer `s` vers celui-ci. La variable locale `s` elle-même ne génère pas de déchets mémoire, mais l'objet chaîne en génère. Utiliser plusieurs fois la même chaîne n'ajoute aucun coût mémoire supplémentaire.
* Chaque exécution d'un constructeur de table (`{ ... }`) crée une nouvelle table.
* L'exécution d'une _instruction de fonction_ crée un objet fermeture. (Il s'agit d'exécuter l'instruction `function () ... end`, et non d'appeler une fonction définie.)
* Les fonctions variadiques (`function(v, ...) end`) créent une table pour les points de suspension chaque fois que la fonction est _appelée_ (dans Lua avant la version 5.2, ou si LuaJIT n'est pas utilisé).
* `dofile()` et `dostring()`
* Les objets userdata

Dans de nombreux cas, vous pouvez éviter de créer de nouveaux objets et réutiliser ceux que vous avez déjà. Par exemple, le code suivant se rencontre souvent à la fin de chaque `update()` :

```lua
-- Reset velocity
self.velocity = vmath.vector3()
```

Il est facile d'oublier que chaque appel à `vmath.vector3()` crée un nouvel objet. Voyons quelle quantité de mémoire utilise un `vector3` :

```lua
print(collectgarbage("count") * 1024)       -- 88634
local v = vmath.vector3()
print(collectgarbage("count") * 1024)       -- 88704. 70 bytes in total has been allocated
```

70 octets ont été ajoutés entre les appels à `collectgarbage()`, mais cela inclut des allocations au-delà du seul objet `vector3`. Chaque affichage du résultat de `collectgarbage()` construit une chaîne qui ajoute elle-même 22 octets de déchets mémoire :

```lua
print(collectgarbage("count") * 1024)       -- 88611
print(collectgarbage("count") * 1024)       -- 88633. 22 bytes allocated
```

Un `vector3` pèse donc 70-22=48 octets. Ce n'est pas beaucoup, mais si vous en créez _un_ à chaque image dans un jeu à 60 images par seconde, cela représente soudain 2,8 ko de déchets mémoire par seconde. Avec 360 composants script qui créent chacun un `vector3` à chaque image, nous arrivons à 1 Mo de déchets mémoire générés par seconde. Les chiffres peuvent augmenter très vite. Lorsque l'environnement d'exécution Lua récupère ces déchets, il peut consommer de nombreuses millisecondes précieuses---en particulier sur les plateformes mobiles.

Une façon d'éviter les allocations consiste à créer un `vector3`, puis à continuer de travailler avec le même objet. Par exemple, pour remettre un `vector3` à zéro, nous pouvons utiliser la construction suivante :

```lua
-- Instead of doing self.velocity = vmath.vector3() which creates a new object
-- we zero an existing velocity vector object's components
self.velocity.x = 0
self.velocity.y = 0
self.velocity.z = 0
```

Le fonctionnement par défaut du ramasse-miettes peut ne pas être optimal pour certaines applications soumises à des contraintes de temps. Si vous constatez des saccades dans votre jeu ou votre application, vous pouvez ajuster la façon dont Lua récupère les déchets mémoire avec la fonction Lua [`collectgarbage()`](/ref/base/#collectgarbage). Vous pouvez, par exemple, exécuter brièvement le ramasse-miettes à chaque image avec une faible valeur de `step`. Pour vous faire une idée de la mémoire consommée par votre jeu ou votre application, vous pouvez afficher la quantité actuelle de déchets mémoire en octets avec :

```lua
print(collectgarbage("count") * 1024)
```

## Bonnes pratiques {#best-practices}

Une question fréquente lors de la conception d'une implémentation est la façon de structurer le code des comportements partagés. Plusieurs approches sont possibles.

Comportements dans un module
: Encapsuler un comportement dans un module vous permet de partager facilement du code entre les composants script de différents objets de jeu (et les scripts d'interface graphique). Lorsque vous écrivez les fonctions d'un module, il est généralement préférable d'écrire du code strictement fonctionnel. Dans certains cas, conserver un état ou produire des effets de bord est nécessaire (ou conduit à une conception plus claire). Si vous devez stocker l'état interne dans le module, gardez à l'esprit que les composants partagent les contextes Lua. Consultez la [documentation sur les modules](/manuals/modules) pour plus de détails.

  ![Module](images/lua/lua_module.png)

  Même s'il est possible que le code d'un module modifie directement les éléments internes d'un objet de jeu (en passant `self` à une fonction du module), nous vous le déconseillons vivement, car cela crée un couplage très fort.

Un objet de jeu auxiliaire avec un comportement encapsulé
: Tout comme vous pouvez regrouper du code de script dans un module Lua, vous pouvez le regrouper dans un objet de jeu doté d'un composant script. La différence est que, si vous le placez dans un objet de jeu, vous pouvez communiquer avec lui uniquement par échange de messages.

  ![Objet auxiliaire](images/lua/lua_helper.png)

Regroupement d'un objet de jeu et d'un objet auxiliaire de comportement dans une collection
: Avec cette conception, vous pouvez créer un objet de jeu de comportement qui agit automatiquement sur un autre objet de jeu cible, soit en utilisant un nom prédéfini (l'utilisateur doit renommer l'objet de jeu cible pour qu'il corresponde), soit à l'aide d'une URL `go.property()` qui pointe vers l'objet de jeu cible.

  ![Collection](images/lua/lua_collection.png)

  L'avantage de cette organisation est que vous pouvez déposer un objet de jeu de comportement dans une collection contenant l'objet cible. Aucun code supplémentaire n'est nécessaire.

  Dans les situations où vous devez gérer un grand nombre d'objets de jeu, cette conception n'est pas préférable, car l'objet de comportement est dupliqué pour chaque instance et chaque objet consomme de la mémoire.
