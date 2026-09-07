---
title: Créer un jeu de taquin dans Defold
brief: Si vous débutez avec Defold, ce guide vous aidera à faire des essais avec quelques éléments de base de Defold et à exécuter la logique d'un script.
---

# Le jeu de taquin classique {#the-classic-15-puzzle}

Ce casse-tête bien connu est devenu populaire en Amérique dans les années 1870. Le but du jeu est de remettre les tuiles du plateau en ordre en les faisant glisser horizontalement et verticalement. Au début du jeu, les tuiles sont mélangées.

La version la plus courante du taquin présente les nombres de 1 à 15 sur les tuiles. Vous pouvez toutefois rendre le jeu un peu plus difficile en utilisant des fragments d'une image comme tuiles. Avant de commencer, essayez de résoudre le taquin. Cliquez sur une tuile adjacente à la case vide pour la faire glisser vers cette case.

## Création du projet {#creating-the-project}

1. Lancez Defold.
2. Sélectionnez *New Project* sur la gauche.
3. Sélectionnez l'onglet *From Template*.
4. Sélectionnez *Empty Project*
5. Sélectionnez un emplacement pour le projet sur votre disque local.
6. Cliquez sur *Create New Project*.

Ouvrez le fichier de paramètres *game.project* et définissez les dimensions du jeu sur 512⨉512. Ces dimensions correspondront à l'image que vous allez utiliser.

![Paramètres d'affichage](images/15-puzzle/display_settings.png)

L'étape suivante consiste à télécharger une image adaptée au taquin. Choisissez n'importe quelle image carrée, mais veillez à la redimensionner à 512 par 512 pixels. Si vous ne souhaitez pas chercher une image, en voici une :

![La Joconde](images/15-puzzle/monalisa.png)

Téléchargez l'image, puis faites-la glisser dans le dossier *main* de votre projet.

## Représentation de la grille {#representing-the-grid}

Defold contient un composant (component) *Tilemap* intégré, idéal pour représenter le plateau du taquin. Les tilemaps vous permettent de définir et de lire les tuiles individuellement, ce qui suffit pour ce projet.

Mais avant de créer la tilemap, vous avez besoin d'une *Tilesource* dans laquelle elle puisera les images de ses tuiles.

<kbd>Faites un clic droit</kbd> sur le dossier *main* et sélectionnez <kbd>New ▸ Tile Source</kbd>. Nommez le nouveau fichier `monalisa.tilesource`.

Définissez les propriétés *Width* et *Height* des tuiles sur 128. L'image de 512⨉512 pixels sera ainsi découpée en 16 tuiles. Les tuiles seront numérotées de 1 à 16 lorsque vous les placerez sur la tilemap.

![Source de tuiles](images/15-puzzle/tilesource.png)

Ensuite, <kbd>faites un clic droit</kbd> sur le dossier *main* et sélectionnez <kbd>New ▸ Tile Map</kbd>. Nommez le nouveau fichier "grid.tilemap".

Defold exige que vous initialisiez la grille. Pour cela, sélectionnez le calque "layer1" et peignez la grille de 4⨉4 tuiles juste au-dessus et à droite de l'origine. Les tuiles choisies n'ont pas vraiment d'importance. Vous écrirez bientôt du code qui définira automatiquement le contenu de ces tuiles.

![Carte de tuiles](images/15-puzzle/tilemap.png)

## Assemblage des éléments {#putting-the-pieces-together}

Ouvrez *main.collection*. <kbd>Faites un clic droit</kbd> sur le nœud racine dans *Outline* et sélectionnez <kbd>Add Game Object</kbd>. Définissez la propriété *Id* du nouvel objet de jeu (game object) sur "game".

<kbd>Faites un clic droit</kbd> sur l'objet de jeu et sélectionnez <kbd>Add Component File</kbd>. Sélectionnez le fichier *grid.tilemap*. Définissez la propriété *Id* sur "tilemap".

<kbd>Faites un clic droit</kbd> sur l'objet de jeu et sélectionnez <kbd>Add Component ▸ Label</kbd>. Définissez la propriété *Id* de l'étiquette sur "done" et sa propriété *Text* sur "Well done". Déplacez l'étiquette au centre de la tilemap.

Définissez la position Z de l'étiquette sur 1 pour vous assurer qu'elle s'affiche par-dessus la grille.

![Collection principale](images/15-puzzle/main_collection.png)

Créez ensuite un fichier de script Lua pour la logique du taquin : <kbd>faites un clic droit</kbd> sur le dossier *main* et sélectionnez <kbd>New ▸ Script</kbd>. Nommez le nouveau fichier "game.script".

Puis <kbd>faites un clic droit</kbd> sur l'objet de jeu nommé "game" dans *main.collection* et sélectionnez <kbd>Add Component File</kbd>. Sélectionnez le fichier *game.script*.

Lancez le jeu. Vous devriez voir la grille telle que vous l'avez dessinée, avec l'étiquette affichant le message "Well done" par-dessus.

## La logique du taquin {#the-puzzle-logic}

Tous les éléments sont maintenant en place ; la suite du tutoriel sera donc consacrée à la mise en œuvre de la logique du taquin.

Le script conservera sa propre représentation des tuiles du plateau, distincte de la tilemap, afin de faciliter leur manipulation. Au lieu de stocker les tuiles dans un tableau à deux dimensions, nous les stockons sous forme de liste à une dimension dans une table Lua. La liste contient les numéros des tuiles dans l'ordre, du coin supérieur gauche de la grille jusqu'au coin inférieur droit :

```lua
-- The completed board looks like this:
self.board = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}
```

Le code qui prend une telle liste de tuiles et l'affiche sur notre tilemap est assez simple, mais il doit convertir la position dans la liste en coordonnées x et y :

```lua
-- Draw a table list of tiles onto a 4x4 tilemap
local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4) -- <1>
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end
```
1. Dans les tilemaps, la tuile dont les coordonnées x et y valent 1 se trouve en bas à gauche. Il faut donc inverser la position y.

Vous pouvez vérifier que la fonction se comporte comme prévu en créant une fonction `init()` de test :

```lua
function init(self)
    -- An inverted board, for test
    self.board = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    draw(self.board)
end
```

Avec les tuiles stockées sous forme de liste dans une table Lua, il est très facile de les mélanger. Le code parcourt simplement chaque élément de la liste et échange chaque tuile avec une autre choisie au hasard :

```lua
-- Swap two items in a table list
local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

-- Randomize the order of a the elements in a table list
local function scramble(t)
    local n = #t
    for i = 1, n - 1 do
        t = swap(t, i, math.random(i, n))
    end
    return t
end
```

Avant de poursuivre, vous devez absolument tenir compte d'une particularité du taquin : si vous mélangez les tuiles aléatoirement comme ci-dessus, il y a 50 % de chances que le taquin soit *impossible* à résoudre.

C'est une mauvaise nouvelle, car vous ne voulez certainement pas proposer au joueur un taquin qui ne peut pas être résolu.

Heureusement, il est possible de déterminer si une configuration peut être résolue ou non. Voici comment :

## Possibilité de résolution {#solvability}

Pour déterminer si une configuration d'un taquin de 4⨉4 cases peut être résolue, deux informations sont nécessaires :

1. Le nombre d'« inversions » dans la configuration. Il y a inversion lorsqu'une tuile précède une autre tuile portant un nombre inférieur. Par exemple, la liste `{1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 0}` comporte trois inversions :

    - le nombre 12 est suivi de 11 et de 10, ce qui donne deux inversions.
    - le nombre 11 est suivi de 10, ce qui donne une inversion supplémentaire.

    (Notez que le taquin résolu ne comporte aucune inversion)

2. La ligne où se trouve la case vide (représentée par `0` dans la liste).

Ces deux nombres peuvent être calculés à l'aide des fonctions suivantes :

```lua
-- Count the number of inversions in a list of tiles
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then -- <1>
                inv = inv + 1
            end
        end
    end
    return inv
end
```
1. Notez que la case vide ne compte pas.

```lua
-- Find the x and y position of a given tile
local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4) -- <1>
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end
```
1. Position Y à partir du bas.

À partir de ces deux nombres, il est maintenant possible de déterminer si une configuration du taquin peut être résolue ou non. Une configuration d'un plateau de 4⨉4 cases peut être *résolue* si :

- La case vide se trouve sur une ligne *impaire* (1 ou 3 en comptant à partir du bas) et le nombre d'inversions est *pair*.
- La case vide se trouve sur une ligne *paire* (2 ou 4 en comptant à partir du bas) et le nombre d'inversions est *impair*.

## Comment cela fonctionne-t-il ? {#how-does-this-work}

Chaque déplacement autorisé consiste à échanger la place d'une pièce avec celle de la case vide, horizontalement ou verticalement.

Déplacer une pièce horizontalement ne modifie ni le nombre d'inversions ni le numéro de la ligne où se trouve la case vide.

Déplacer une pièce verticalement, en revanche, change la parité du nombre d'inversions (d'impair à pair, ou de pair à impair). Cela change également la parité de la ligne de la case vide.

Par exemple :

![Glissement d'une pièce](images/15-puzzle/slide.png)

Ce déplacement fait passer l'ordre des tuiles de :

`{ ... 0, 11, 2, 13, 6 ... }`

à

`{ ... 6, 11, 2, 13, 0 ... }`

Le nouvel état ajoute trois inversions de la manière suivante :

- Le nombre 6 ajoute une inversion (le nombre 2 se trouve maintenant après 6)
- Le nombre 11 perd une inversion (le nombre 6 se trouve maintenant avant 11)
- Le nombre 13 perd une inversion (le nombre 6 se trouve maintenant avant 13)

Un glissement vertical peut faire varier le nombre d'inversions de ±1 ou de ±3.

Un glissement vertical peut faire varier le numéro de la ligne de la case vide de ±1.

Dans l'état final du taquin, la case vide se trouve dans le coin inférieur droit (la ligne *impaire* 1) et le nombre d'inversions est la valeur *paire* 0. Chaque déplacement autorisé laisse ces deux valeurs intactes (déplacement horizontal) ou inverse leur parité (déplacement vertical). Aucun déplacement autorisé ne peut rendre les parités du nombre d'inversions et de la ligne de la case vide *impaire*, *impaire* ou *paire*, *paire*.

Toute configuration du taquin où les deux nombres sont tous deux impairs ou tous deux pairs est donc impossible à résoudre.

Voici le code qui vérifie si le taquin peut être résolu :

```lua
-- Is the given table list of 4x4 tiles solvable?
local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end
```

## Entrées utilisateur {#user-input}

Il ne reste maintenant qu'à rendre le taquin interactif.

Créez une fonction `init()` qui effectue toute l'initialisation à l'exécution en utilisant les fonctions créées précédemment :

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>
    math.randomseed(socket.gettime()) -- <2>
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}) -- <3>
    while not solvable(self.board) do -- <4>
        self.board = scramble(self.board)
    end
    draw(self.board) -- <5>
    self.done = false -- <6>
    msg.post("#done", "disable") -- <7>
end
```
1. Indiquez au moteur que cet objet de jeu doit recevoir les entrées.
2. Initialisez la graine du générateur de nombres aléatoires.
3. Créez un état initial aléatoire pour le plateau.
4. Si cet état ne peut pas être résolu, mélangez à nouveau les tuiles.
5. Affichez le plateau.
6. Définissez un indicateur de réussite pour suivre l'état de victoire.
7. Désactivez l'étiquette du message de réussite.

Ouvrez */input/game.input_bindings* et ajoutez un nouveau *Mouse Trigger*. Définissez le nom de l'action sur "press" :

![Entrées](images/15-puzzle/input.png)

Revenez au script et créez une fonction `on_input()`.

```lua
-- Deal with user input
function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then -- <1>
        local x = math.ceil(action.x / 128) -- <2>
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0) -- <3>
        if math.abs(x - ex) + math.abs(y - ey) == 1 then -- <4>
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x) -- <5>
            draw(self.board) -- <6>
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then -- <7>
            self.done = true
            msg.post("#done", "enable")
        end
    end
end
```
1. Si un bouton de la souris est pressé et que la partie est encore en cours, effectuez les opérations suivantes.
2. Calculez les coordonnées x et y de la case sur laquelle l'utilisateur a cliqué.
3. Trouvez l'emplacement actuel de la case vide (0).
4. Si la case sur laquelle le joueur a cliqué se trouve juste au-dessus, au-dessous, à gauche ou à droite de la case vide, effectuez les opérations suivantes :
5. Échangez les tuiles de la case sur laquelle le joueur a cliqué et de la case vide.
6. Réaffichez le plateau mis à jour.
7. Si le nombre d'inversions sur le plateau est de 0, ce qui signifie que tout est dans le bon ordre, et que la case vide se trouve dans la colonne la plus à droite (elle doit se trouver sur la dernière ligne pour que le nombre d'inversions soit de 0), alors le taquin est résolu ; effectuez donc les opérations suivantes :
8. Définissez l'indicateur de réussite.
9. Activez/affichez le message de réussite.

Et voilà ! Vous avez terminé, le jeu de taquin est complet !

## Le script complet {#the-complete-script}

Voici le code complet du script à titre de référence :

```lua
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then
                inv = inv + 1
            end
        end
    end
    return inv
end

local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4)
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end

local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end

local function scramble(t)
    for i=1, #t do
        local tmp = t[i]
        local r = math.random(#t)
        t[i] = t[r]
        t[r] = tmp
    end
    return t
end

local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4)
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end

function init(self)
    msg.post(".", "acquire_input_focus")
    math.randomseed(socket.gettime())
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0})   
    while not solvable(self.board) do
        self.board = scramble(self.board)
    end
    draw(self.board)
    self.done = false
    msg.post("#done", "disable")
end

function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then
        local x = math.ceil(action.x / 128)
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0)
        if math.abs(x - ex) + math.abs(y - ey) == 1 then
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x)
            draw(self.board)
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then
            self.done = true
            msg.post("#done", "enable")
        end
    end
end

function on_reload(self)
    self.done = false
    msg.post("#done", "disable")
end
```

## Exercices supplémentaires {#further-exercises}

1. Créez un taquin de 5⨉5 cases, puis un autre de 6⨉5 cases. Assurez-vous que les vérifications de la possibilité de résolution fonctionnent dans le cas général.
2. Ajoutez des animations de glissement. Les tuiles ne peuvent pas être déplacées séparément de la tilemap ; vous devrez donc trouver une solution. Peut-être une tilemap distincte qui ne contient que la pièce en mouvement ?
