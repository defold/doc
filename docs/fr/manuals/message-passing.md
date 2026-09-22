---
title: Échange de messages dans Defold
brief: L'échange de messages est le mécanisme utilisé par Defold pour permettre à des objets faiblement couplés de communiquer. Ce manuel décrit ce mécanisme en détail.
---

# Échange de messages {#message-passing}

L'échange de messages est un mécanisme qui permet aux objets de jeu (game objects) de Defold de communiquer entre eux. Ce manuel suppose que vous avez une connaissance élémentaire du [mécanisme d'adressage](/manuals/addressing) et des [éléments fondamentaux](/manuals/building-blocks) de Defold.

Defold ne repose pas sur une orientation objet dans laquelle vous définissez votre application en établissant des hiérarchies de classes avec héritage et fonctions membres dans vos objets (comme en Java, C++ ou C#). Defold étend plutôt Lua avec une conception orientée objet simple et puissante, où chaque composant (component) script conserve en interne l'état de son objet, accessible par la référence `self`. Les objets peuvent en outre être entièrement découplés en utilisant l'échange asynchrone de messages comme moyen de communication entre eux.


## Exemples d'utilisation {#usage-examples}

Examinons d'abord quelques exemples simples d'utilisation. Supposons que vous créiez un jeu composé des éléments suivants :

1. Une collection bootstrap principale contenant un objet de jeu doté d'un composant GUI (l'interface graphique se compose d'une mini-carte et d'un compteur de score). Elle contient également une collection dont l'identifiant est "level".
2. La collection nommée "level" contient deux objets de jeu : un héros contrôlé par le joueur et un ennemi.

![Structure de l'échange de messages](images/message_passing/message_passing_structure.png)

::: sidenote
Le contenu de cet exemple se trouve dans deux fichiers distincts. Il y a un fichier pour la collection bootstrap principale et un autre pour la collection dont l'identifiant est "level". Cependant, les noms de fichiers _n'ont pas d'importance_ dans Defold. C'est l'identité que vous attribuez aux instances qui compte.
:::

Le jeu contient quelques mécaniques simples qui nécessitent une communication entre les objets :

![Échange de messages](images/message_passing/message_passing.png)

① Le héros frappe l'ennemi
: Dans le cadre de cette mécanique, un message `"punch"` est envoyé du composant script "hero" au composant script "enemy". Puisque les deux objets se trouvent au même niveau dans la hiérarchie des collections, l'adressage relatif est préférable :

  ```lua
  -- Send "punch" from the "hero" script to "enemy" script
  msg.post("enemy#controller", "punch")
  ```

  Il n'y a qu'une seule puissance de coup de poing dans le jeu ; le message n'a donc pas besoin de contenir d'autre information que son nom, "punch".

  Dans le composant script de l'ennemi, vous créez une fonction pour recevoir le message :

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  Dans ce cas, le code ne tient compte que du nom du message (envoyé sous forme de chaîne hachée dans le paramètre `message_id`). Il ne tient compte ni des données du message ni de son expéditeur : *quiconque* envoie le message "punch" inflige des dégâts au pauvre ennemi.

② Le héros gagne des points
: Chaque fois que le joueur vainc un ennemi, son score augmente. Un message `"update_score"` est également envoyé du composant script de l'objet de jeu "hero" au composant "gui" de l'objet de jeu "interface".

  ```lua
  -- Enemy defeated. Increase score counter by 100.
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  Dans ce cas, il n'est pas possible d'écrire une adresse relative, car "interface" se trouve à la racine de la hiérarchie de nommage, contrairement à "hero". Le message est envoyé au composant GUI auquel un script est attaché, afin qu'il puisse réagir au message de manière appropriée. Les messages peuvent circuler librement entre les scripts, les scripts GUI et les scripts de rendu.

  Le message `"update_score"` est accompagné des données du score. Ces données sont transmises sous forme de table Lua dans le paramètre `message` :

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    end
  end
  ```

③ Position de l'ennemi sur la mini-carte
: Le joueur dispose à l'écran d'une mini-carte qui l'aide à localiser et à suivre les ennemis. Chaque ennemi est chargé de signaler sa position en envoyant un message `"update_minimap"` au composant "gui" de l'objet de jeu "interface" :

  ```lua
  -- Send the current position to update the interface minimap
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  Le code du script GUI doit suivre la position de chaque ennemi et, si le même ennemi envoie une nouvelle position, remplacer l'ancienne. L'expéditeur du message (transmis dans le paramètre `sender`) peut servir de clé dans une table Lua contenant les positions :

  ```lua
  function init(self)
    self.minimap_positions = {}
  end

  local function update_minimap(self)
    for url, pos in pairs(self.minimap_positions) do
      -- update position on map
      ...
    end
  end

  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    elseif message_id == hash("update_minimap") then
      -- update the minimap with new positions
      self.minimap_positions[sender] = message.position
      update_minimap(self)
    end
  end
  ```

## Envoi de messages {#sending-messages}

Comme nous l'avons vu plus haut, l'envoi d'un message est très simple. Vous appelez la fonction `msg.post()`, qui place votre message dans la file d'attente des messages. Ensuite, à chaque image, le moteur parcourt cette file et remet chaque message à son adresse cible. Pour certains messages système (comme `"enable"`, `"disable"`, `"set_parent"`, etc.), le code du moteur traite le message. Le moteur produit également certains messages système (comme `"collision_response"` lors de collisions physiques) qui sont remis à vos objets. Pour les messages définis par l'utilisateur et envoyés à des composants script, le moteur appelle simplement une fonction Lua spéciale de Defold nommée `on_message()`.

Vous pouvez envoyer n'importe quel message à tout objet ou composant existant ; c'est au code du destinataire de répondre au message. Si vous envoyez un message à un composant script et que le code du script l'ignore, cela ne pose aucun problème. La responsabilité du traitement des messages incombe entièrement au destinataire.

Le moteur vérifie l'adresse cible du message. Si vous essayez d'envoyer un message à un destinataire inconnu, Defold signale une erreur dans la console :

```lua
-- Try to post to a non existing object
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

La signature complète de l'appel à `msg.post()` est la suivante :

`msg.post(receiver, message_id, [message])`

receiver
: L'identifiant du composant ou de l'objet de jeu cible. Notez que si vous ciblez un objet de jeu, le message est diffusé à tous ses composants.

message_id
: Une chaîne de caractères ou une chaîne hachée contenant le nom du message.

[message]
: Une table Lua facultative contenant les données du message sous forme de paires clé-valeur. Presque tous les types de données peuvent être inclus dans la table Lua du message. Vous pouvez transmettre des nombres, des chaînes de caractères, des booléens, des URL, des valeurs hachées et des tables imbriquées. Vous ne pouvez pas transmettre de fonctions.

  ```lua
  -- Send table data containing a nested table
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
La taille de la table du paramètre `message` est soumise à une limite stricte de 2 kilooctets. Il n'existe actuellement aucun moyen simple de déterminer la quantité exacte de mémoire occupée par une table, mais vous pouvez utiliser `collectgarbage("count")` avant et après l'insertion de la table pour suivre l'utilisation de la mémoire.
:::

### Raccourcis {#shorthands}

Defold fournit deux raccourcis pratiques que vous pouvez utiliser pour envoyer des messages sans préciser une URL complète :

:[Shorthands](../shared/url-shorthands.md)


## Réception de messages {#receiving-messages}

Pour recevoir des messages, il suffit de vérifier que le composant script cible contient une fonction nommée `on_message()`. Cette fonction accepte quatre paramètres :

`function on_message(self, message_id, message, sender)`

`self`
: Une référence au composant script lui-même.

`message_id`
: Contient le nom du message. Ce nom est _haché_.

`message`
: Contient les données du message. Il s'agit d'une table Lua. S'il n'y a pas de données, la table est vide.

`sender`
: Contient l'URL complète de l'expéditeur.

```lua
function on_message(self, message_id, message, sender)
    print(message_id) --> hash: [my_message_name]

    pprint(message) --> {
                    -->   score = 100,
                    -->   value = "some string"
                    --> }

    print(sender) --> url: [main:/my_object#script]
end
```

## Échange de messages entre mondes de jeu {#messaging-between-game-worlds}

Si vous utilisez un composant proxy de collection (collection proxy) pour charger un nouveau monde de jeu (game world) dans l'environnement d'exécution, vous souhaiterez échanger des messages entre les mondes de jeu. Supposons que vous ayez chargé une collection au moyen d'un proxy et que la propriété *Name* de cette collection soit définie sur "level" :

![Nom de la collection](images/message_passing/collection_name.png)

Dès que la collection est chargée, initialisée et activée, vous pouvez envoyer des messages à tout composant ou objet du nouveau monde en précisant le nom du monde de jeu dans le champ "socket" de l'adresse du destinataire :

```lua
-- Send a message to the player in the new game world
msg.post("level:/player#controller", "wake_up")
```
Vous trouverez une description plus détaillée du fonctionnement des proxys dans la documentation sur les [proxys de collection](/manuals/collection-proxy).

## Chaînes de messages {#message-chains}

Lorsqu'un message envoyé est finalement distribué, la fonction `on_message()` de ses destinataires est appelée. Il est assez courant que le code exécuté en réaction envoie de nouveaux messages, qui sont ajoutés à la file d'attente des messages.

Lorsque le moteur commence la distribution, il parcourt la file d'attente des messages, appelle la fonction `on_message()` de chaque destinataire et continue jusqu'à ce que la file soit vide. Si le passage de distribution ajoute de nouveaux messages à la file, le moteur effectue un autre passage. Cependant, le nombre de tentatives du moteur pour vider la file est soumis à une limite stricte, ce qui limite de fait la longueur des chaînes de messages que vous pouvez espérer voir entièrement distribuées au cours d'une image. Vous pouvez facilement vérifier combien de passages de distribution le moteur effectue entre chaque appel à `update()` à l'aide du script suivant :

```lua
function init(self)
    -- We’re starting a long message chain during object init
    -- and keeps it running through a number of update() steps.
    print("INIT")
    msg.post("#", "msg")
    self.updates = 0
    self.count = 0
end

function update(self, dt)
    if self.updates < 5 then
        self.updates = self.updates + 1
        print("UPDATE " .. self.updates)
        print(self.count .. " dispatch passes before this update.")
        self.count = 0
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("msg") then
        self.count = self.count + 1
        msg.post("#", "msg")
    end
end
```

L'exécution de ce script affiche un résultat semblable à celui-ci :

```txt
DEBUG:SCRIPT: INIT
INFO:ENGINE: Defold Engine 1.2.36 (5b5af21)
DEBUG:SCRIPT: UPDATE 1
DEBUG:SCRIPT: 10 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 2
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 3
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 4
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 5
DEBUG:SCRIPT: 75 dispatch passes before this update.
```

Nous constatons que cette version précise du moteur Defold effectue 10 passages de distribution sur la file d'attente des messages entre `init()` et le premier appel à `update()`. Elle effectue ensuite 75 passages lors de chaque boucle de mise à jour suivante.
