---
title: Écrire la logique du jeu dans des scripts
brief: Ce manuel décrit comment ajouter de la logique au jeu à l'aide de composants script.
---

# Scripts {#scripts}

Les composants script (script components) vous permettent de créer la logique du jeu avec le [langage de programmation Lua](/manuals/lua).


## Types de scripts {#script-types}

Defold propose trois types de scripts Lua, chacun ayant accès à des bibliothèques Defold différentes.

Scripts d'objet de jeu (game object)
: Extension _.script_. Ces scripts s'ajoutent aux objets de jeu exactement comme tout autre [composant](/manuals/components), et Defold exécute le code Lua dans le cadre des fonctions du cycle de vie du moteur. Les scripts d'objet de jeu servent généralement à contrôler les objets de jeu et la logique qui assure la cohérence du jeu, avec le chargement des niveaux, les règles du jeu, etc. Les scripts d'objet de jeu ont accès aux fonctions [GO](/ref/go) et à toutes les fonctions des bibliothèques Defold, à l'exception des fonctions [GUI](/ref/gui) et [Render](/ref/render).


Scripts d'interface graphique
: Extension _.gui_script_. Ces scripts sont exécutés par les composants d'interface graphique et contiennent généralement la logique nécessaire pour afficher les éléments d'interface graphique, comme les affichages tête haute, les menus, etc. Defold exécute le code Lua dans le cadre des fonctions du cycle de vie du moteur. Les scripts d'interface graphique ont accès aux fonctions [GUI](/ref/gui) et à toutes les fonctions des bibliothèques Defold, à l'exception des fonctions [GO](/ref/go) et [Render](/ref/render).


Scripts de rendu
: Extension _.render_script_. Ces scripts sont exécutés par le pipeline de rendu et contiennent la logique nécessaire pour effectuer le rendu de tous les graphismes de l'application ou du jeu à chaque image. Le script de rendu occupe une place particulière dans le cycle de vie de votre jeu. Vous trouverez plus de détails dans la [documentation sur le cycle de vie de l'application](/manuals/application-lifecycle). Les scripts de rendu ont accès aux fonctions [Render](/ref/render) et à toutes les fonctions des bibliothèques Defold, à l'exception des fonctions [GO](/ref/go) et [GUI](/ref/gui).


## Exécution des scripts, fonctions de rappel et self {#script-execution-callbacks-and-self}

Defold exécute les scripts Lua dans le cadre du cycle de vie du moteur et donne accès à ce cycle de vie au moyen d'un ensemble de fonctions de rappel (callbacks) prédéfinies. Lorsque vous ajoutez un composant script à un objet de jeu, le script s'intègre au cycle de vie de l'objet de jeu et de ses composants. Le script est évalué dans le contexte Lua au moment de son chargement, puis le moteur exécute les fonctions suivantes en leur passant comme paramètre une référence à l'instance actuelle du composant script. Vous pouvez utiliser cette référence `self` pour stocker l'état dans l'instance du composant.

::: important
`self` est un objet `userdata` qui se comporte comme une table Lua, mais vous ne pouvez pas le parcourir avec `pairs()` ou `ipairs()`, ni l'afficher avec `pprint()`.
:::

#### `init(self)` {#initself}
Appelée lorsque le composant est initialisé.

```lua
function init(self)
  -- These variables are available through the lifetime of the component instance
  self.my_var = "something"
  self.age = 0
end
```

#### `final(self)` {#finalself}
Appelée lorsque le composant est supprimé. Cette fonction permet d'effectuer des opérations de nettoyage, par exemple si vous avez créé des objets de jeu qui doivent être supprimés en même temps que le composant.

```lua
function final(self)
  if self.my_var == "something" then
      -- do some cleanup
  end
end
```

#### `fixed_update(self, dt)` {#fixed_updateself-dt}
Mise à jour indépendante de la fréquence d'images. Le paramètre `dt` contient le temps écoulé depuis la dernière mise à jour. Cette fonction est appelée `0-N` fois selon la durée d'une image et la fréquence de mise à jour fixe. Elle n'est appelée que lorsque `Physics`-->`Use Fixed Timestep` est activé et que `Engine`-->`Fixed Update Frequency` est supérieur à 0 dans *game.project*. Elle est utile lorsque vous souhaitez manipuler des objets physiques à intervalles réguliers pour obtenir une simulation physique stable.

```lua
function fixed_update(self, dt)
  msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
end
```

#### `update(self, dt)` {#updateself-dt}
Appelée une fois par image après le callback `fixed_update` de tous les scripts (si Fixed Timestep est activé). Le paramètre `dt` contient le temps écoulé depuis l'image précédente.

```lua
function update(self, dt)
  self.age = self.age + dt -- increase age with the timestep
end
```

#### `late_update(self, dt)` {#late_updateself-dt}
Appelée une fois par image après le callback `update` de tous les scripts, mais juste avant le rendu. Le paramètre `dt` contient le temps écoulé depuis l'image précédente.

```lua
function late_update(self, dt)
  go.set_position("/camera", self.final_camera_position)
end
```

#### on_message(self, message_id, message, sender) {#on_messageself-message_id-message-sender}
Lorsque des messages sont envoyés au composant script avec [`msg.post()`](/ref/msg#msg.post), le moteur appelle cette fonction du composant destinataire. Pour en savoir [plus sur l'échange de messages](/manuals/message-passing).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("increase_score") then
        self.total_score = self.total_score + message.score
    end
end
```

#### `on_input(self, action_id, action)` {#on_inputself-action_id-action}
Si ce composant a acquis le focus d'entrée (voir [`acquire_input_focus`](/ref/go/#acquire_input_focus)), le moteur appelle cette fonction lorsqu'une entrée est détectée. Pour en savoir [plus sur la gestion des entrées](/manuals/input).

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        print("Touch", action.x, action.y)
    end
end
```

#### `on_reload(self)` {#on_reloadself}
Cette fonction est appelée lorsque le script est rechargé au moyen de la fonction de rechargement à chaud de l'éditeur (<kbd>Edit ▸ Reload Resource</kbd>). Elle est très utile pour le débogage, les tests et les ajustements. Pour en savoir [plus sur le rechargement à chaud](/manuals/hot-reload).

```lua
function on_reload(self)
  print(self.age) -- print the age of this game object
end
```


## Logique réactive {#reactive-logic}

Un objet de jeu doté d'un composant script implémente une certaine logique. Souvent, cette logique dépend d'un facteur externe. L'IA d'un ennemi peut réagir à la présence du joueur dans un certain rayon autour d'elle ; une porte peut se déverrouiller et s'ouvrir à la suite d'une interaction du joueur, etc.

La fonction `update()` vous permet d'implémenter des comportements complexes définis par une machine à états exécutée à chaque image — cette approche est parfois adaptée. Mais chaque appel à `update()` a un coût. À moins d'avoir réellement besoin de cette fonction, vous devriez la supprimer et essayer de construire votre logique _de manière réactive_. Attendre passivement qu'un message déclenche une réponse coûte moins cher que d'interroger activement le monde de jeu (game world) à la recherche de données auxquelles réagir. De plus, résoudre un problème de conception de manière réactive conduit souvent à une conception et à une implémentation plus claires et plus stables.

Prenons un exemple concret. Supposons que vous souhaitiez qu'un composant script envoie un message 2 secondes après son initialisation. Il doit ensuite attendre un message de réponse particulier puis, après avoir reçu cette réponse, envoyer un autre message 5 secondes plus tard. Le code non réactif correspondant ressemblerait à ceci :

```lua
function init(self)
    -- Counter to keep track of time.
    self.counter = 0
    -- We need this to keep track of our state.
    self.state = "first"
end

function update(self, dt)
    self.counter = self.counter + dt
    if self.counter >= 2.0 and self.state == "first" then
        -- send message after 2 seconds
        msg.post("some_object", "some_message")
        self.state = "waiting"
    end
    if self.counter >= 5.0 and self.state == "second" then
        -- send message 5 seconds after we received "response"
        msg.post("another_object", "another_message")
        -- Nil the state so we don’t reach this state block again.
        self.state = nil
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("response") then
        -- “first” state done. enter next
        self.state = "second"
        -- zero the counter
        self.counter = 0
    end
end
```

Même dans ce cas assez simple, la logique devient plutôt enchevêtrée. Il est possible de la rendre plus claire à l'aide de coroutines dans un module (voir ci-dessous), mais essayons plutôt de la rendre réactive en utilisant un mécanisme de temporisation intégré.

```lua
local function send_first()
	msg.post("some_object", "some_message")
end

function init(self)
	-- Wait 2s then call send_first()
	timer.delay(2, false, send_first)
end

local function send_second()
	msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
	if message_id == hash("response") then
		-- Wait 5s then call send_second()
		timer.delay(5, false, send_second)
	end
end
```

Ce code est plus clair et plus facile à suivre. Nous supprimons les variables d'état internes, dont l'évolution est souvent difficile à suivre dans la logique et qui peuvent entraîner des bugs subtils. Nous supprimons aussi complètement la fonction `update()`. Le moteur n'a donc plus à appeler notre script 60 fois par seconde, même lorsqu'il ne fait qu'attendre.


## Prétraitement {#preprocessing}

Il est possible d'utiliser un préprocesseur Lua et un balisage spécial pour inclure du code de manière conditionnelle selon la variante du build. Exemple :

```lua
-- Use one of the following keywords: RELEASE, DEBUG or HEADLESS
--#IF DEBUG
local lives_num = 999
--#ELSE 
local lives_num = 3
--#ENDIF
```

Le préprocesseur est disponible sous forme d'extension de build. Vous trouverez plus d'informations sur son installation et son utilisation sur la [page de l'extension sur GitHub](https://github.com/defold/extension-lua-preprocessor).


## Prise en charge dans l'éditeur {#editor-support}

L'éditeur Defold prend en charge l'édition de scripts Lua avec la coloration syntaxique et la saisie semi-automatique. Pour compléter les noms de fonctions Defold, appuyez sur *Ctrl+Space* afin d'afficher la liste des fonctions correspondant à ce que vous saisissez.

![Saisie semi-automatique](images/script/completion.png)
