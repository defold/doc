---
brief: Si vous débutez avec Defold, ce guide vous aidera à découvrir la logique des scripts et quelques éléments fondamentaux de Defold pour créer un clone de Snake à partir de zéro.
layout: tutorial
title: Créer un jeu Snake dans Defold
difficulty: Beginner
---

# Snake {#snake}

Ce tutoriel vous accompagne dans la création de l'un des jeux classiques les plus courants que vous pouvez tenter de recréer. Ce jeu connaît de nombreuses variantes ; celle-ci met en scène un serpent qui mange de la « nourriture » et qui ne grandit que lorsqu'il mange. Ce serpent se déplace également sur un terrain de jeu contenant des obstacles.

![Miniature](images/snake/thumbnail.png)

### Ce que vous allez apprendre {#what-youll-learn}

Dans ce tutoriel, vous apprendrez à :
- Créer un jeu à partir de zéro dans Defold
- Configurer et gérer les entrées
- Créer des tilemaps et les modifier à l'exécution
- Écrire des scripts en Lua

### Remarque pour les débutants {#a-note-for-beginners}

Ce tutoriel s'adresse aux débutants, mais si vous découvrez à la fois Defold et le développement de jeux, nous vous recommandons de commencer par quelques manuels d'introduction, notamment ceux consacrés aux [éléments fondamentaux de Defold](/manuals/building-blocks/) et au [glossaire](/manuals/glossary/). Si vous n'avez pas encore téléchargé Defold, consultez le [manuel d'installation](/manuals/install/). Nous vous recommandons également de consulter la [présentation de l'éditeur](/manuals/editor/) pour prendre rapidement en main l'éditeur lui-même, mais nous fournissons aussi ici des captures d'écran pour chaque étape.

## Création du projet {#creating-the-project}

Lancez Defold, puis :

1. Sélectionnez *Create From* ▸ *Templates* sur la gauche.
2. Sélectionnez *Empty Project*.
3. Saisissez un nom de projet dans le champ *Title*.
4. Choisissez un emplacement pour le projet dans *Location*.
5. Cliquez sur *Create New Project*.

![Démarrage](images/snake/1.png)

<input type="checkbox"/> Terminé !

## Paramètres du projet {#project-settings}

Nous allons commencer par définir la résolution du jeu.

1. Une fois l'éditeur ouvert, cherchez le fichier `game.project` sur la gauche, dans le panneau *Assets*. Double-cliquez dessus pour l'ouvrir.
2. Accédez à la section *Display* du fichier `game.project`.
3. Définissez les dimensions du jeu (`Width` et `Height`) sur 768⨉768 ou sur un autre multiple de 16.

![Affichage](images/snake/2.png)

Le jeu sera dessiné sur une grille dont chaque segment mesurera 16x16 pixels ; ce réglage évite donc que l'écran du jeu coupe des segments. Le fichier `game.project` contient tous les paramètres importants du projet : vous pouvez les découvrir dans le [manuel des paramètres du projet](/manuals/project-settings/).

<input type="checkbox"/> Terminé !

## Création de nouveaux dossiers dans le panneau Assets {#creating-new-folders-in-the-assets-pane}

Un clone minimaliste de Snake nécessite très peu de graphismes : un segment vert de 16⨉16 pour le serpent, un bloc blanc pour les obstacles et un bloc rouge plus petit pour représenter la nourriture.

Commencez par créer un répertoire pour les ressources dans l'éditeur Defold :

1. Faites un <kbd>clic droit</kbd> sur le dossier `main`
2. Sélectionnez `New Folder`.
3. Une fenêtre contextuelle vous demandant un nom apparaît : saisissez `assets` et cliquez sur `Create Folder`.

![Nouveau dossier](images/snake/3.png)

<input type="checkbox"/> Terminé !

## Ajout des graphismes au jeu {#adding-graphics-to-the-game}

L'image ci-dessous est la seule ressource dont vous avez besoin :

![Sprites de Snake](images/snake/snake.png)

1. Faites un <kbd>clic droit</kbd> sur l'image ci-dessus et enregistrez-la sur votre disque local. Ensuite, glissez-déposez (ou copiez-collez) l'image téléchargée vers le nouvel emplacement que vous venez de créer dans le dossier du projet.

![Nouveau dossier](images/snake/4.png)

Vous pouvez également en savoir plus sur [l'importation de ressources ici](/manuals/importing-graphics/).

<input type="checkbox"/> Terminé !

## Ajout d'une source de tuiles {#adding-a-tile-source}

Defold fournit un composant (component) [tilemap](/manuals/tilemap/) intégré que vous utiliserez pour créer le terrain de jeu, constitué de *tuiles* alignées sur une grille. Une tilemap permet de définir et de lire chaque tuile individuellement, ce qui convient parfaitement à ce jeu. Comme les tilemaps tirent leurs graphismes d'une [source de tuiles](/manuals/tilesource/), vous devez en créer une :

1. Faites un <kbd>clic droit</kbd> sur le dossier `assets`.
2. Sélectionnez `New` ▸ `Tile Source` dans la section « Resources ».
3. Nommez le nouveau fichier « snake » (l'éditeur l'enregistrera sous le nom `snake.tilesource`).

![Nouvelle source de tuiles](images/snake/5.png)

La source de tuiles s'ouvre dans un éditeur de sources de tuiles dédié à ce type de fichier, et vous devez lui fournir une image pour qu'elle puisse fonctionner. Le panneau `Properties` se trouve sur la droite :

4. Définissez la propriété `Image` sur le fichier graphique que vous venez d'importer.
![Source de tuiles](images/snake/6.png)

5. Les propriétés `Width` et `Height` doivent rester à 16 (valeur par défaut). L'image de 32⨉32 pixels sera ainsi découpée en quatre tuiles numérotées de 1 à 4.

![Propriétés de la source de tuiles](images/snake/7.png)

Remarquez que la propriété *Extrude Borders* est définie sur 2 pixels. Cela évite les artefacts visuels autour des tuiles dont les graphismes s'étendent jusqu'au bord.

Si vous modifiez un fichier, un astérisque `*` apparaît à côté de son nom dans son onglet. Sélectionnez `File` ▸ `Save All` ou utilisez le raccourci <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>⌘Cmd</kbd> + <kbd>S</kbd> sur Mac) pour enregistrer tous les fichiers.

<input type="checkbox"/> Terminé !

## Création de la tilemap du terrain de jeu {#creating-the-playfield-tile-map}

La source de tuiles est maintenant prête à l'emploi : il est temps de créer le composant tilemap du terrain de jeu :

1. Faites un <kbd>clic droit</kbd> sur le dossier `main` et sélectionnez <kbd>New</kbd> ▸ <kbd>Tile Map</kbd> dans la section « Components ». Nommez le nouveau fichier « grid » (l'éditeur l'enregistrera sous le nom « grid.tilemap »).
![Ajout d'une tilemap](images/snake/8.png)

2. Le fichier s'ouvre dans un éditeur de tilemaps qui signale qu'une **Tile Source** est nécessaire : définissez donc la propriété *Tile Source* sur le fichier « snake.tilesource » créé précédemment.
![Définition de la source de tuiles](images/snake/9.png)

<input type="checkbox"/> Terminé !

## Dessin des tuiles dans la tilemap {#drawing-tiles-in-the-tile-map}

Defold ne stocke que la zone de la tilemap réellement utilisée ; vous devez donc ajouter suffisamment de tuiles pour couvrir toute la surface de l'écran.

1. Sélectionnez la couche `layer1` dans le panneau `Outline` sur la droite.
2. Choisissez l'option de menu `Edit` ▸ `Select Tile...` ou le raccourci <kbd>Space</kbd> pour afficher la palette de tuiles, puis cliquez sur la tuile que vous souhaitez utiliser pour peindre.
![Tilemap](images/snake/10.png)

3. Peignez une bordure sur le pourtour de l'écran ainsi que quelques obstacles.
![Tilemap terminée](images/snake/11.png)

Vous aurez besoin d'une tilemap de 48x48 tuiles (car notre affichage mesure 768 et nos tuiles font 16px, donc 768/16 = 48) pour remplir l'écran du jeu.

Enregistrez la tilemap lorsque vous avez terminé.

<input type="checkbox"/> Terminé !

## Ajout de la tilemap au jeu {#adding-the-tile-map-to-the-game}

Nous devons maintenant ajouter notre tilemap au jeu. Si vous connaissez les éléments fondamentaux de Defold, vous savez que les composants font partie des objets de jeu (game object) et que les objets de jeu peuvent être définis dans les collections.

1. Ouvrez `main.collection` en double-cliquant dessus dans le panneau `Assets`. Dans le modèle Empty Project, il s'agit par défaut de la collection bootstrap chargée au démarrage du moteur.

2. Faites un <kbd>clic droit</kbd> sur la racine dans `Outline` et sélectionnez `Add Game Object` pour créer un nouvel objet de jeu dans la collection chargée au démarrage du jeu.
![Ajout d'un objet de jeu](images/snake/12.png)

3. Faites un <kbd>clic droit</kbd> sur le nouvel objet de jeu et sélectionnez `Add Component File`. Choisissez le fichier « grid.tilemap » que vous venez de créer.
![Ajout d'un composant](images/snake/13.png)

Notre collection de jeu contient maintenant une tilemap. Elle devrait être visible lorsque vous lancez le jeu depuis l'éditeur.

1. Sélectionnez `Project` ▸ `Build` ou utilisez le raccourci <kbd>Ctrl</kbd> + <kbd>B</kbd> (<kbd>⌘Cmd</kbd> + <kbd>B</kbd> sur Mac).

![Exécution du jeu](images/snake/14.png)

<input type="checkbox"/> Terminé !

## Ajout d'un script au jeu {#adding-a-script-to-the-game}

1. Faites un <kbd>clic droit</kbd> sur le dossier `main` dans le navigateur `Assets` et sélectionnez `New` ▸ `Script` dans la section Scripts. Nommez le nouveau fichier de script « snake » (il sera enregistré sous le nom « snake.script »). Ce fichier contiendra toute la logique du jeu.
![Ajout d'un script](images/snake/15.png)

2. Revenez à *main.collection* et faites un <kbd>clic droit</kbd> sur l'objet de jeu qui contient la tilemap. Sélectionnez <kbd>Add&nbsp;Component&nbsp;File</kbd> et choisissez le fichier « snake.script ».

![Collection principale](images/snake/16.png)

Le composant tilemap et le script sont maintenant en place.

<input type="checkbox"/> Terminé !

## Le script du jeu {#the-game-script}

Le script que vous allez écrire pilotera l'ensemble du jeu. Nous allons ajouter les fonctionnalités une par une.

### Algorithme de déplacement simple {#simple-movement-algorithm}

Voici le principe de fonctionnement :

1. Le script conserve une liste des positions des tuiles actuellement occupées par le serpent.
2. Si le joueur appuie sur une touche directionnelle, mémorisez la direction dans laquelle le serpent doit se déplacer.
3. À intervalles réguliers, avancez le serpent d'un pas dans sa direction de déplacement actuelle.

### Initialisation {#initialization}

Ouvrez *snake.script* et repérez la fonction `init()`. Le moteur appelle cette fonction lors de l'initialisation du script au démarrage du jeu. Remplacez le code par ce qui suit :

```lua
function init(self)
    self.segments = { -- <1>
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0} -- <2>
    self.speed = 7.0 -- <3>
    self.time = 0 -- <4>
end
```

Dans ce code, nous :

1. Stockons les segments du serpent dans une table Lua nommée `self.segments`, contenant une liste de tables dont chacune contient une position X et Y pour un segment.
2. Stockons la direction actuelle dans une table nommée `self.dir` contenant une direction X et Y.
3. Stockons la vitesse de déplacement actuelle dans `self.speed`, exprimée en tuiles par seconde.
4. Stockons dans `self.time` la valeur d'un chronomètre qui servira à gérer la vitesse de déplacement.

Le code du script ci-dessus est écrit en langage Lua. Quelques points méritent votre attention, mais si vous ne comprenez pas encore ce qui suit, ne vous inquiétez pas. Continuez, expérimentez et prenez le temps nécessaire : vous finirez par comprendre. Pour l'instant, retenez simplement que dans `init()`, nous avons initialisé les variables que nous allons utiliser.

- Defold réserve un ensemble de *fonctions* de rappel intégrées qui sont appelées pendant la durée de vie d'un composant script. Ce ne sont *pas* des méthodes, mais de simples fonctions.
- Le moteur d'exécution transmet une référence à l'instance actuelle du composant script par le paramètre `self`. La référence `self` sert à stocker les données de l'instance.
- La référence `self` peut être utilisée comme une table Lua dans laquelle vous pouvez stocker des données. Utilisez simplement la notation pointée comme avec n'importe quelle autre table : `self.data = "value"`. La référence reste valide pendant toute la durée de vie du script, dans ce cas du démarrage du jeu jusqu'à ce que vous le quittiez.
- Les littéraux de tables Lua s'écrivent entre accolades `{}`.
- Les entrées d'une table peuvent être des paires clé/valeur (`{x = 10, y = 20}`), des tables Lua imbriquées (`{ {a = 1}, {b = 2} }`) ou d'autres types de données.

<input type="checkbox"/> Terminé !

### Mise à jour {#update}

La fonction `init()` est appelée exactement une fois, lorsque le composant script est instancié dans le jeu en cours d'exécution. En revanche, la fonction `update()` est appelée une fois **à chaque image**. Elle est donc idéale pour la logique du jeu en temps réel.

Le principe de la mise à jour est le suivant : à un intervalle défini, effectuez les opérations suivantes :

1. Repérez la tête du serpent, puis créez une nouvelle tête à la position voisine, décalée selon la direction de déplacement actuelle. Ainsi, si le serpent se déplace de X=1 et Y=0 et que la tête actuelle se trouve en X=0 et Y=0, la nouvelle tête doit se trouver en X=1 et Y=0.
2. Enregistrez la position de la nouvelle tête dans la liste des segments qui constituent le serpent.
3. Récupérez la position de la queue dans la table des segments.
4. Effacez la tuile de la queue à cette position.
5. Dessinez tous les segments du serpent (tuiles) aux positions indiquées dans la table.

![Algorithme](images/snake/17.png)

:::sidenote
Gardez à l'esprit que la tête de notre serpent se trouve à la fin de la table, et sa queue au début.
:::

1. Repérez la fonction `update()` dans *snake.script* et remplacez le code par ce qui suit :

```lua
function update(self, dt)
    self.time = self.time + dt -- <1>
    if self.time >= 1.0 / self.speed then -- <2>
        local head = self.segments[#self.segments] -- <3>

        local newhead = {
            x = head.x + self.dir.x,
            y = head.y + self.dir.y
        } -- <4>

        table.insert(self.segments, newhead) -- <5>

        local tail = table.remove(self.segments, 1) -- <6>

        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0) -- <7>

        for i, s in ipairs(self.segments) do -- <8>
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2) -- <9>
        end

        self.time = 0 -- <10>
    end
end
```

Dans ce code, nous :

1. Faisons avancer le chronomètre du temps écoulé (en secondes) depuis le dernier appel à `update()` : ce que l'on appelle le « delta de temps », ou `dt`.
2. Si suffisamment de temps s'est écoulé :
3. Récupérons la position actuelle de la tête. `#` est l'opérateur qui permet d'obtenir la longueur d'une table lorsqu'elle est utilisée comme un tableau, ce qui est le cas ici : tous les segments sont des valeurs de la table sans clé spécifiée.
4. Créons un nouveau segment de tête à partir de la position actuelle de la tête et de la direction de déplacement (`self.dir`).
5. Ajoutons la nouvelle tête à la table des segments (à la fin).
6. Retirons la queue du début de la table des segments.
7. Effaçons la tuile à la position de la queue retirée. Notre tilemap `#grid` ne contient qu'une couche nommée `layer1`.
8. Parcourons les éléments de la table des segments. À chaque itération, `i` contient la position dans la table (à partir de 1) et `s` contient le segment actuel.
9. Définissons la tuile à la position du segment sur la valeur 2 (qui correspond à la tuile de la couleur verte du serpent).
10. Une fois ces opérations terminées, remettons le chronomètre à zéro.

Si vous lancez le jeu maintenant, vous devriez voir le serpent de quatre segments se déplacer de gauche à droite sur le terrain de jeu.

![Exécution du jeu](images/snake/snake_run_1.png)

<input type="checkbox"/> Terminé !

## Entrées du joueur {#player-input}

Avant d'ajouter du code pour réagir aux entrées du joueur, vous devez configurer les liaisons d'entrée.

### Liaisons d'entrée {#input-bindings}

1. Dans le dossier `input`, repérez le fichier `game.input_binding` et faites un <kbd>double-clic</kbd> dessus pour l'ouvrir.
2. Ajoutez des liaisons *Key Trigger* pour les déplacements vers le haut, le bas, la gauche et la droite. Dans la colonne *Input*, sélectionnez les touches du clavier, et dans les colonnes *Action*, saisissez les noms des actions.

![Entrées](images/snake/18.png)

Le fichier de liaisons d'entrée associe les entrées réelles de l'utilisateur (touches, mouvements de la souris, etc.) à des *noms* d'actions transmis aux scripts qui ont demandé à recevoir les entrées.

<input type="checkbox"/> Terminé !

### Acquisition du focus d'entrée {#acquiring-input-focus}

Une fois les liaisons en place, ouvrez *snake.script* et ajoutez la ligne suivante au début de la fonction `init()` :

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0
end
```

La ligne ajoutée :
1. Envoie un message à l'objet de jeu actuel (« . » est un raccourci pour l'objet de jeu actuel) pour lui indiquer de commencer à recevoir les entrées du moteur.

Repérez ensuite la fonction `on_input` et saisissez le code suivant :

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then -- <1>
        self.dir.x = 0 -- <2>
        self.dir.y = 1
    elseif action_id == hash("down") and action.pressed then
        self.dir.x = 0
        self.dir.y = -1
    elseif action_id == hash("left") and action.pressed then
        self.dir.x = -1
        self.dir.y = 0
    elseif action_id == hash("right") and action.pressed then
        self.dir.x = 1
        self.dir.y = 0
    end
end
```

Ces branches `if...elseif...` effectuent les opérations suivantes :
1. Si l'action d'entrée « up » est reçue, conformément à la configuration des liaisons d'entrée, et que la table `action` a son champ `pressed` défini sur `true` (le joueur a appuyé sur la touche), alors :
2. Définissez la direction de déplacement.

Relancez le jeu et vérifiez que vous pouvez diriger le serpent.

<input type="checkbox"/> Terminé !

### Amélioration de la gestion des entrées {#improving-input-handling}

Remarquez maintenant que si vous appuyez simultanément sur deux touches, cela provoque deux appels à `on_input()`, un pour chaque appui. Avec le code ci-dessus, seul le dernier appel a un effet sur la direction du serpent, car les appels successifs à `on_input()` écrasent les valeurs de `self.dir`.

Remarquez également que si le serpent se déplace vers la gauche et que vous appuyez sur la touche <kbd>right</kbd>, il se retourne sur lui-même. La correction *apparemment* évidente de ce problème consiste à ajouter une condition supplémentaire aux clauses `if` de `on_input()` :

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

Cependant, si le serpent se déplace vers la gauche et que le joueur appuie *rapidement* d'abord sur <kbd>up</kbd>, puis sur <kbd>right</kbd> avant le déplacement suivant, seul l'appui sur <kbd>right</kbd> aura un effet et le serpent se retournera sur lui-même. Avec les conditions ajoutées aux clauses `if` ci-dessus, l'entrée sera ignorée. *Ce n'est pas satisfaisant !*

Pour résoudre correctement ce problème, il faut stocker les entrées dans une file d'attente et en retirer les éléments au fur et à mesure que le serpent avance :

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0

    self.dirqueue = {} -- <1>
end
```

Cette fois-ci, nous :
1. Avons ajouté une variable `self.dirqueue`, initialisée comme une table vide.

Dans la fonction `update()`, ajoutez :

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed then
        local newdir = table.remove(self.dirqueue, 1) -- <1>
        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y -- <2>
            if not opposite then
                self.dir = newdir -- <3>
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tail = table.remove(self.segments, 1)
        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0)

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end
```

1. Retirez le premier élément de la file d'attente des directions.
2. S'il y a un élément (`newdir` n'est pas nul), vérifiez si `newdir` pointe dans la direction opposée à `self.dir`.
3. Ne définissez une nouvelle direction que si elle n'est pas opposée à la direction actuelle.

Et modifiez `on_input` pour stocker l'entrée actuelle dans la file d'attente :

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1}) -- <1>
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

1. Ajoutez la direction d'entrée à la file d'attente des directions au lieu de définir directement `self.dir`.

Lancez le jeu et vérifiez qu'il fonctionne comme prévu.

<input type="checkbox"/> Terminé !

## Nourriture et collisions avec les obstacles {#food-and-collision-with-obstacles}

Le serpent a besoin de nourriture sur la carte pour grandir et accélérer. Ajoutons-en !

### Apparition de la nourriture {#spawning-the-food}

Au-dessus de la fonction `init()`, ajoutez une nouvelle fonction :

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end
```

Dans cette fonction, nous :
1. Déclarons une nouvelle fonction appelée `put_food()` qui place un morceau de nourriture sur la carte.
2. Stockons une position X et Y aléatoire dans une variable appelée `self.food`.
3. Définissons la tuile à la position X et Y sur la valeur 3, qui correspond au graphisme de la nourriture.

Appelez-la ensuite à la fin de la fonction `init()` :
```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    math.randomseed(socket.gettime()) -- <1>
    put_food(self) -- <2>
end
```

1. Avant de commencer à tirer des valeurs aléatoires avec `math.random()`, définissez la graine aléatoire ; sinon, la même série de valeurs aléatoires sera générée. Cette graine ne doit être définie qu'une seule fois.
2. Appelez la fonction `put_food()` au démarrage du jeu pour que le joueur commence avec un morceau de nourriture sur la carte.

<input type="checkbox"/> Terminé !

### Manger la nourriture {#eating-the-food}

Pour détecter si le serpent est entré en collision avec quelque chose, il suffit maintenant de regarder ce qui se trouve sur la tilemap à l'endroit vers lequel il se dirige et de réagir en conséquence.

Ajoutez une variable qui indique si le serpent est vivant ou non :

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true -- <1>

    math.randomseed(socket.gettime())
    put_food(self)
end
```

1. Un indicateur qui précise si le serpent est vivant ou non.

Ajoutez ensuite la logique qui teste les collisions avec les murs, les obstacles et la nourriture :

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then -- <1>
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y) -- <2>

        if tile == 2 or tile == 4 then
            self.alive = false -- <3>
        elseif tile == 3 then
            self.speed = self.speed + 1 -- <4>
            put_food(self)
        else
            local tail = table.remove(self.segments, 1) -- <5>
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end
```

1. Ne faites avancer le serpent que s'il est vivant.
2. Avant de dessiner dans la tilemap, lisez ce qui se trouve à la position qu'occupera la nouvelle tête du serpent.
3. Si la tuile est un obstacle ou une autre partie du serpent, la partie est terminée !
4. Si la tuile est de la nourriture, augmentez la vitesse, puis placez un nouveau morceau de nourriture.
5. Remarquez que la queue n'est retirée que lorsqu'il n'y a pas de collision. Cela signifie que si le joueur mange de la nourriture, le serpent grandit d'un segment, puisque la queue n'est pas retirée lors de ce déplacement.

Essayez maintenant le jeu et assurez-vous qu'il fonctionne bien !

Ce tutoriel est terminé, mais continuez à expérimenter avec le jeu et essayez de réaliser quelques-uns des exercices ci-dessous !

<input type="checkbox"/> Terminé !

## Le script complet {#the-complete-script}

Voici le code complet du script pour référence :

```lua
local function put_food(self)
    self.food = {x = math.random(2, 47), y = math.random(2, 47)}
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3)        
end

function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true

    math.randomseed(socket.gettime())
    put_food(self)
end

function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y)

        if tile == 2 or tile == 4 then
            self.alive = false
        elseif tile == 3 then
            self.speed = self.speed + 1
            put_food(self)
        else
            local tail = table.remove(self.segments, 1)
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end

function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1})
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

## Exercices {#exercises}

Essayer de mettre en œuvre ces améliorations constitue un bon exercice :

1. Ajoutez la gestion d'une touche pour redémarrer le jeu lorsque la partie est terminée.
2. Ajoutez un système de points et un compteur de score, en utilisant soit un simple composant label (plus facile), soit une interface graphique complète.
3. La fonction put_food() ne tient compte ni de la position du serpent ni des obstacles. Corrigez-la pour que la nourriture n'apparaisse que sur des emplacements libres.
4. Lorsque la partie est terminée, affichez un message « Game Over » et permettez au joueur de réessayer.
5. Pour aller plus loin : ajoutez un second serpent contrôlé par un joueur.
