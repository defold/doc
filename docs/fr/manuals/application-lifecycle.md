---
title: Manuel du cycle de vie des applications Defold
brief: Ce manuel décrit en détail le cycle de vie des jeux et des applications Defold.
---

# Cycle de vie de l’application {#application-lifecycle}

Le cycle de vie d’une application ou d’un jeu Defold est simple dans ses grandes lignes. Le moteur passe par trois étapes d’exécution : l’initialisation, la boucle de mise à jour (où les applications et les jeux passent la majeure partie de leur temps) et la finalisation.

::: sidenote
Ce manuel concerne les versions de Defold à partir de la version 1.12.0. Cette version a introduit des changements dans le cycle de vie ainsi que la nouvelle fonction `late_update()`.
:::

![Vue d’ensemble du cycle de vie](images/application_lifecycle/application_lifecycle.png)

Dans de nombreux cas, une compréhension élémentaire du fonctionnement interne de Defold suffit. Vous pouvez toutefois rencontrer des cas particuliers dans lesquels l’ordre exact d’exécution des tâches par Defold devient crucial. Ce document décrit comment le moteur exécute une application du début à la fin.

L’application commence par initialiser tout ce qui est nécessaire au fonctionnement du moteur. Elle charge la collection principale et appelle [`init()`](/ref/go#init) sur chaque composant (component) chargé qui possède une fonction Lua `init()` (composants script et composants d’interface graphique dotés de scripts GUI). Cela vous permet d’effectuer une initialisation personnalisée.

L’application entre ensuite dans la boucle de mise à jour, où elle passe la majeure partie de sa durée de vie. À chaque image, les objets de jeu (game object) et les composants qu’ils contiennent sont mis à jour. Toutes les fonctions [`update()`](/ref/go#update) des scripts et des scripts GUI sont appelées. Durant la boucle de mise à jour, les messages sont distribués à leurs destinataires, les sons sont joués et tous les éléments graphiques sont rendus.

À un moment donné, le cycle de vie de l’application touche à sa fin. Avant que l’application ne se ferme, le moteur sort de la boucle de mise à jour et entre dans une étape de finalisation. Il prépare la suppression de tous les objets de jeu chargés. Les fonctions [`final()`](/ref/go#final) de tous les composants des objets sont appelées, ce qui permet d’effectuer un nettoyage personnalisé. Les objets sont ensuite supprimés et la collection principale est déchargée.

Par souci de clarté, les étapes de la passe de [« distribution des messages »](#dispatching-messages) sont présentées dans un diagramme distinct à la fin de ce manuel et sont signalées dans les diagrammes par une petite icône « enveloppe avec une flèche » 📩.

## Initialisation {#initialization}

C’est ici que votre jeu démarre : il s’agit de la première étape du jeu en cours d’exécution. Elle peut être divisée en trois phases :

![Initialisation](images/application_lifecycle/initialization.png)

### Préinitialisation {#preinitialization}

Durant la phase `Preinitialization`, le moteur effectue de nombreuses opérations avant de charger la collection principale (bootstrap). Le profileur de mémoire, les sockets, les graphismes, les HID (périphériques d’entrée), le son, la physique et bien d’autres éléments sont configurés. La configuration de l’application (*game.project*) est également chargée et mise en place.

![Préinitialisation](images/application_lifecycle/pre_init.png)

Le premier point d’entrée que vous pouvez contrôler, à la fin de l’initialisation du moteur, est l’appel à la fonction `init()` du script de rendu actuel.

La collection principale est ensuite chargée et initialisée.

### Initialisation de la collection {#collection-init}

Durant la phase `Collection Init`, tous les objets de jeu de la collection appliquent leurs transformations à leurs enfants : translation (changement de position), rotation et mise à l’échelle. Toutes les fonctions `init()` existantes des composants sont ensuite appelées.

![Initialisation de la collection](images/application_lifecycle/collection_init.png)

::: sidenote
L’ordre d’appel des fonctions `init()` des composants des objets de jeu n’est pas défini. Vous ne devez pas supposer que le moteur initialise les objets d’une même collection dans un ordre particulier.
:::

### Après la mise à jour durant l’initialisation {#post-update-in-initialization}

Le moteur effectue ensuite une passe `Post Update` complète, identique à celle qui sera exécutée après chaque étape de la `Update Loop`. Elle est effectuée à la fin de l’initialisation, car votre code `init()` peut envoyer de nouveaux messages, demander à des factories de créer de nouveaux objets, marquer des objets pour suppression et effectuer d’autres actions.

![Après la mise à jour](images/application_lifecycle/post_init.png)

Cette passe assure la livraison des messages, la création effective des objets de jeu par les factories et la suppression des objets. Notez que la passe `Post Update` comprend une séquence de « distribution des messages » qui livre les messages en attente et traite également ceux envoyés aux proxies de collection (collection proxy). Toutes les mises à jour des proxies qui en découlent (activation, désactivation, initialisation, finalisation, chargement et marquage pour déchargement) sont effectuées durant ces étapes.

Il est tout à fait possible de charger un [proxy de collection](/manuals/collection-proxy) durant `init()`, de s’assurer que tous les objets qu’il contient sont initialisés, puis de décharger la collection par l’intermédiaire du proxy, le tout avant le premier appel à `update()` d’un composant, c’est-à-dire avant que le moteur n’ait quitté l’étape d’initialisation pour entrer dans la boucle de mise à jour :

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- The proxy collection is unloaded before this code is reached.
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- The proxy collection objects’ init() and final() functions
        -- are called before we reach this object’s update()
    end
end
```

## Boucle de mise à jour {#update-loop}

La `Update Loop` exécute une séquence précise une fois par image. Cette séquence peut être divisée en cinq phases principales :

![Boucle de mise à jour](images/application_lifecycle/update_loop.png)

1. Entrées (traitement et gestion)
2. Mise à jour (comprenant les mises à jour fixes, régulières, tardives et celles des composants du moteur)
3. Mise à jour du rendu
4. Après la mise à jour (déchargement des proxies de collection, création et suppression des objets de jeu)
5. Rendu de l’image (rendu final des éléments graphiques)

### Phase des entrées {#input-phase}

Les entrées sont lues depuis les périphériques disponibles, associées aux [liaisons d’entrée](/manuals/input), puis distribuées. Tout objet de jeu qui a acquis le focus d’entrée reçoit les entrées dans les fonctions `on_input()` de tous ses composants. Un objet de jeu possédant un composant script et un composant d’interface graphique doté d’un script GUI reçoit les entrées dans les fonctions `on_input()` de ces deux composants, à condition que ces fonctions soient définies et que les composants aient acquis le focus d’entrée.

![Phase des entrées](images/application_lifecycle/input_phase.png)

Tout objet de jeu qui a acquis le focus d’entrée et qui contient des composants proxy de collection distribue les entrées aux composants de la collection du proxy. Ce processus se poursuit récursivement dans les proxies de collection activés qui se trouvent au sein d’autres proxies de collection activés.

### Phase de mise à jour {#update-phase}

La phase `Update` fait partie de la `Update Loop`. Elle démarre une fois pour la collection racine, puis s’exécute récursivement pour chaque proxy de collection activé.

Au sein d’une collection, Defold traite les fonctions de rappel par type de composant : il parcourt toutes les instances d’un type de composant qui implémente l’étape concernée, appelle la fonction de rappel Lua de chaque instance, distribue les messages en attente, puis passe au type de composant suivant.

L’ordre général des étapes des fonctions de rappel Lua des composants *script* est le suivant :

1. `fixed_update()` - appelée 0..N fois par image (si un pas de temps fixe est utilisé)
2. `update()` - appelée une fois par image
3. `late_update()` - appelée une fois par image

![Phase de mise à jour](images/application_lifecycle/update_phase.png)


Chaque composant d’objet de jeu de la collection principale est parcouru. Si l’un de ces composants possède un script doté d’une fonction `fixed_update()`/`update()`/`late_update()`, celle-ci est appelée. Si le composant est un proxy de collection, chaque composant de la collection du proxy est mis à jour récursivement en suivant toutes les étapes de la phase `Update`.

::: sidenote
L’ordre d’appel des fonctions `update()` des composants des objets de jeu n’est pas défini. Vous ne devez pas supposer que le moteur met à jour les objets d’une même collection dans un ordre particulier. Il en va de même pour `fixed_update()` et `late_update()` (depuis la version 1.12.0).
:::

#### Physique {#physics}

Pour les composants objet de collision, les messages de physique (collisions, déclencheurs, réponses aux lancers de rayons, etc.) sont distribués dans l’ensemble de l’objet de jeu qui les contient, à tous les composants dotés d’un script possédant la fonction `on_message()`.

Si un [pas de temps fixe](/manuals/physics/#physics-updates) est utilisé pour la simulation physique, la fonction `fixed_update()` peut également être appelée dans tous les composants script. Cette fonction est utile dans les jeux fondés sur la physique lorsque vous souhaitez manipuler les objets physiques à intervalles réguliers pour obtenir une simulation physique stable.

#### Transformations {#transforms}

Avant **chaque** mise à jour d’un type de composant, à plusieurs reprises durant la `Update Loop`, les transformations sont mises à jour si nécessaire : tout déplacement, rotation et mise à l’échelle d’un objet de jeu sont appliqués à chacun de ses composants ainsi qu’aux composants de ses objets de jeu enfants.

Une dernière mise à jour supplémentaire des transformations est effectuée à la fin de la `Update Loop`, si nécessaire.

#### Phase de mise à jour du moteur (sans mises à jour fixes) {#engine-update-phase-no-fixed-updates}

Les tableaux ci-dessous décrivent les passes de mise à jour *au niveau du moteur*. Ils omettent délibérément l’ordre de priorité interne exact des composants (qui est un détail d’implémentation du moteur), mais reflètent les garanties d’ordre pertinentes pour les scripts :

- `fixed_update()` s’exécute avant `update()`
- `late_update()` s’exécute après `update()`
- les messages envoyés sont distribués entre les mises à jour des types de composants, ainsi qu’entre les étapes des fonctions de rappel des scripts

Lorsque `Use Fixed Timestep` vaut `false` et/ou que Fixed Update Frequency vaut `0`, le moteur prépare `dt` au début de la phase, puis suit le déroulement présenté dans le tableau ci-dessous :

:::sidenote
Notez qu’après la mise à jour de **chaque** type de composant, tous les messages sont distribués ; cela n’est pas indiqué dans le tableau ci-dessous pour en préserver la lisibilité.
:::

| Étape | Phase du moteur | Fonction de rappel Lua | Commentaire |
|-|-|-|-|
| 1 | **Mise à jour** | `update()` | Appelée une fois par image pour chaque type de composant qui implémente la mise à jour, dans l’ordre de priorité interne. Les animations de propriétés d’objets de jeu démarrées avec `go.animate()` sont également mises à jour ici, en tant que type de composant distinct. Les composants de **physique** sont mis à jour ici. Pour chaque proxy de collection activé, la phase `Update` entière est appelée récursivement à partir de l’étape 1. |
| 2 | **Mise à jour tardive** | `late_update()` | Appelée une fois par image pour chaque type de composant qui implémente la mise à jour tardive, dans l’ordre de priorité interne. |
| 3 | **Transformations** | | Une dernière mise à jour supplémentaire des transformations est effectuée à la fin pour chaque composant, si nécessaire. |

#### Phase de mise à jour du moteur avec un pas de temps fixe {#engine-update-phase-with-fixed-timestep}

Lorsque `Use Fixed Timestep` vaut `true` et que Fixed Update Frequency est non nul, le moteur prépare au début de la phase `dt` (temps écoulé), `fixed_dt` et `num_fixed_steps` (`0..N`), c’est-à-dire le nombre d’appels à la mise à jour fixe, déterminé par le temps écoulé depuis la dernière mise à jour afin de garantir un nombre fixe de mises à jour.

:::sidenote
Notez qu’après la mise à jour de **chaque** type de composant, tous les messages sont distribués ; cela n’est pas indiqué dans le tableau ci-dessous pour en préserver la lisibilité.
:::

Le moteur exécute ensuite la boucle suivante :

| Étape | Phase du moteur | Fonction de rappel Lua | Commentaire |
|-|-|-|-|
| 1 | **Mise à jour fixe** | `fixed_update()` | Appelée `0..N` fois par image selon le temps écoulé, pour chaque type de composant qui implémente la mise à jour fixe, dans l’ordre de priorité interne. Cela comprend les étapes de mise à jour fixe des composants de *physique*. |
| 2 | **Mise à jour** | `update()` | Appelée une fois par image pour chaque type de composant qui implémente la mise à jour, dans l’ordre de priorité interne. Les animations de propriétés d’objets de jeu démarrées avec `go.animate()` sont également mises à jour ici, en tant que type de composant distinct. Pour chaque proxy de collection activé, la phase `Update` est appelée récursivement à partir de l’étape 1. |
| 3 | **Mise à jour tardive** | `late_update()` | Appelée une fois par image pour chaque type de composant qui implémente la mise à jour tardive, dans l’ordre de priorité interne. |
| 4 | **Transformations** | | Une dernière mise à jour supplémentaire des transformations est effectuée à la fin pour chaque composant, si nécessaire. |

Si vous avez besoin de davantage de détails sur le fonctionnement interne de Defold durant la phase de mise à jour, il est utile de lire directement le code de [`gameobject.cpp`](https://github.com/defold/defold/blob/dev/engine/gameobject/src/gameobject/gameobject.cpp).

### Phase de mise à jour du rendu {#render-update-phase}

Le bloc de mise à jour du rendu distribue d’abord tous les messages envoyés au socket `@render` (par exemple, les messages `set_view_projection` des composants caméra, les messages `set_clear_color`, etc.). La fonction `update()` du script de rendu est ensuite appelée.

![Phase de mise à jour du rendu](images/application_lifecycle/render_update_phase.png)

### Phase après la mise à jour {#post-update-phase}

Après les mises à jour, une séquence de traitement complémentaire est exécutée. Elle décharge de la mémoire les proxies de collection marqués pour déchargement (cela se produit durant la séquence de « distribution des messages »). Pour chaque objet de jeu marqué pour suppression, toutes les fonctions `final()` de ses composants sont appelées, s’il y en a. Le code des fonctions `final()` ajoute souvent de nouveaux messages à la file d’attente ; la passe de « distribution des messages » est donc exécutée ensuite.

![Phase après la mise à jour](images/application_lifecycle/post_update_phase.png)

Tout composant factory ayant reçu l’instruction de créer un objet de jeu le fait ensuite. Enfin, les objets de jeu marqués pour suppression sont effectivement supprimés.

### Phase de rendu {#render-phase}

La dernière étape de la boucle de mise à jour consiste à distribuer les messages `@system` (messages `exit`, `reboot`, activation ou désactivation du profileur, démarrage et arrêt de la capture vidéo, etc.).

![Phase de rendu](images/application_lifecycle/render_phase.png)

Les éléments graphiques sont ensuite rendus, ainsi que le profileur visuel le cas échéant (voir la [documentation sur le débogage](/manuals/debugging)). Après le rendu graphique, une capture vidéo est effectuée.

#### Fréquence d’images et pas de temps des collections {#frame-rate-and-collection-time-step}

Le nombre de mises à jour d’image par seconde (qui correspond au nombre d’exécutions de la boucle de mise à jour par seconde) peut être défini dans les paramètres du projet, ou par programmation en envoyant un message `set_update_frequency` au socket `@system`. Il est également possible de définir le _pas de temps_ de chaque proxy de collection individuellement en lui envoyant un message `set_time_step`. Modifier le pas de temps d’une collection n’affecte pas la fréquence d’images. Cela affecte le pas de temps de la mise à jour physique ainsi que la variable `dt` transmise à `update().` Notez également que modifier le pas de temps ne change pas le nombre d’appels à `update()` par image : cette fonction est toujours appelée exactement une fois.

(Consultez le [manuel des proxies de collection](/manuals/collection-proxy) et [`set_time_step`](/ref/collectionproxy#set-time-step) pour plus de détails)

#### Réduction de l’activité du moteur {#engine-throttling}

Defold 1.12.0 a introduit une API de réduction de l’activité du moteur qui peut suspendre entièrement les mises à jour du moteur et le rendu tout en continuant à détecter les entrées. Toute entrée réactive le moteur, qui peut à nouveau réduire son activité après un délai.

Consultez l’API `sys.set_engine_throttle()` pour plus de détails et des exemples d’utilisation.

## Finalisation {#finalization}

Lorsque l’application se ferme, elle termine d’abord la dernière séquence de la boucle de mise à jour, qui décharge tous les proxies de collection : tous les objets de jeu de chaque collection de proxy sont finalisés et supprimés.

Une fois cela terminé, le moteur entre dans une séquence de finalisation qui traite la collection principale et ses objets :

![Finalisation](images/application_lifecycle/finalization.png)

Les fonctions `final()` des composants sont appelées en premier. Une distribution des messages s’ensuit. Enfin, tous les objets de jeu sont supprimés et la collection principale est déchargée.

Le moteur procède ensuite à l’arrêt interne des sous-systèmes : la configuration du projet est supprimée, le profileur de mémoire est arrêté, et ainsi de suite.

L’application est maintenant complètement arrêtée.

## Distribution des messages {#dispatching-messages}

La **distribution des messages** est une passe spéciale effectuée après la mise à jour de **chaque** type de composant, par exemple les sprites ou les scripts, et après toute autre action susceptible d’envoyer des messages. Durant son exécution, tous les messages envoyés qui ont été rassemblés dans une file d’attente sont distribués. Ces passes sont signalées dans les diagrammes par de petites icônes « enveloppe avec une flèche » 📩.

![Distribution des messages](images/application_lifecycle/dispatch_messages.png)

Une fois tous les **messages utilisateur** distribués par l’appel à `on_message()` pour chaque composant, les messages spéciaux de Defold sont traités dans l’ordre suivant (également présenté dans le diagramme), pour chaque proxy de collection :

1. Messages `load` - chargent les proxies de collection marqués pour chargement et renvoient un message `proxy_loaded`.
2. Messages `unload` - déchargent les proxies de collection marqués pour déchargement et renvoient un message `proxy_unloaded`.
3. Messages `init` - déclenchent la phase `Collection Init` pour tous les proxies de collection à initialiser.
4. Messages `final` - déclenchent `final()` sur tous les composants du proxy marqué pour finalisation.
5. Messages `enable` - activent le proxy de collection afin que la `Update Loop` soit exécutée pour lui à l’image suivante ; cela déclenche implicitement `init()` pour chaque composant de la collection.
6. Messages `disable` - désactivent le proxy de collection afin que la `Update Loop` **ne soit pas** exécutée pour lui à l’image suivante ; l’exécution de la `Update Loop` pour ce proxy est complètement arrêtée.

Comme le code `on_message()` de tout composant destinataire peut envoyer des messages supplémentaires, le répartiteur de messages continue à distribuer récursivement les messages envoyés jusqu’à ce que la file d’attente soit vide. Le nombre de parcours de la file d’attente effectués par le répartiteur est toutefois limité. Consultez les [chaînes de messages](/manuals/message-passing) pour plus de détails.
