---
title: Optimiser les performances d'un jeu Defold à l'exécution
brief: Ce manuel décrit comment optimiser un jeu Defold pour obtenir une fréquence d'images élevée et stable.
---

# Optimiser la vitesse d'exécution {#optimizing-runtime-speed}
Avant d'essayer d'optimiser un jeu pour obtenir une fréquence d'images élevée et stable, vous devez savoir où se trouvent les goulots d'étranglement. Qu'est-ce qui prend réellement le plus de temps dans une image de votre jeu ? Le rendu ? La logique du jeu ? Le graphe de scène ? Pour le déterminer, il est recommandé d'utiliser les outils de profilage intégrés. Utilisez le [profileur à l'écran ou le profileur web](/manuals/profiling/) pour mesurer les performances de votre jeu et décider ensuite s'il faut optimiser quelque chose, et quoi. Une fois que vous comprenez mieux ce qui prend du temps, vous pouvez commencer à résoudre les problèmes.

## Réduire le temps d'exécution des scripts {#reduce-script-execution-time}
Il est nécessaire de réduire le temps d'exécution des scripts si le profileur affiche des valeurs élevées pour la section `Script`. En règle générale, vous devez bien sûr essayer d'exécuter le moins de code possible à chaque image. Exécuter beaucoup de code dans `update()` et `on_input()` à chaque image risque d'affecter les performances de votre jeu, en particulier sur les appareils d'entrée de gamme. Voici quelques recommandations :

### Utiliser une approche réactive dans votre code {#use-reactive-code-patterns}
Ne vérifiez pas constamment si des changements se sont produits lorsque vous pouvez recevoir un callback. N'animez pas un élément manuellement et n'effectuez pas une tâche qui peut être confiée au moteur (par exemple, utilisez `go.animate)()` au lieu d'animer un élément manuellement).

### Réduire le travail du ramasse-miettes {#reduce-garbage-collection}
Si vous créez beaucoup d'objets de courte durée de vie, comme des tables Lua, à chaque image, cela finira par déclencher le ramasse-miettes de Lua. Cela peut se traduire par de petites saccades ou des pics dans le temps de traitement d'une image. Réutilisez les tables lorsque vous le pouvez et efforcez-vous d'éviter de créer des tables Lua dans les boucles et les constructions similaires, si possible.

### Précalculer les hachages des identifiants de messages et d'actions {#prehash-message-and-action-ids}
Si vous traitez beaucoup de messages ou devez gérer de nombreux événements d'entrée, il est recommandé de précalculer les hachages des chaînes de caractères. Prenons ce morceau de code :

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

Dans l'exemple ci-dessus, la valeur hachée de la chaîne serait recréée à chaque réception d'un message. Vous pouvez améliorer cela en créant les valeurs hachées une seule fois et en les utilisant lors du traitement des messages :

```lua
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

### Privilégier les URL et les mettre en cache {#prefer-and-cache-urls}
Pour envoyer un message ou adresser un objet de jeu (game object) ou un composant (component) d'une autre manière, vous pouvez fournir un identifiant sous forme de chaîne de caractères, de valeur hachée ou d'URL. Si vous utilisez une chaîne ou une valeur hachée, elle sera convertie en URL en interne. Il est donc recommandé de mettre en cache les URL souvent utilisées pour obtenir les meilleures performances possibles du système. Prenons l'exemple suivant :

```lua
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- do something with pos
```

Dans les trois cas, la position d'un objet de jeu dont l'identifiant est `enemy` serait récupérée. Dans les deux premiers cas, l'identifiant (chaîne ou valeur hachée) serait converti en URL avant d'être utilisé. Il vaut donc mieux mettre les URL en cache et utiliser la version en cache pour obtenir les meilleures performances possibles :

```lua
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- do something with pos
    end
```

## Réduire le temps de rendu d'une image {#reduce-time-it-takes-to-render-a-frame}
Il est nécessaire de réduire le temps de rendu d'une image si le profileur affiche des valeurs élevées dans les sections `Render` et `Render Script`. Plusieurs éléments sont à prendre en compte lorsque vous cherchez à réduire le temps de rendu d'une image :

* Réduisez le nombre d'appels de dessin - Pour en savoir plus sur la réduction des appels de dessin, consultez [ce message sur le forum](https://forum.defold.com/t/draw-calls-and-defold/4674)
* Réduisez les dessins superposés sur les mêmes pixels
* Réduisez la complexité des shaders - Renseignez-vous sur les optimisations GLSL dans [cet article de Khronos](https://www.khronos.org/opengl/wiki/GLSL_Optimizations). Vous pouvez également modifier les shaders par défaut utilisés par Defold (situés dans `builtins/materials`) et choisir une précision inférieure lorsque le shader n'a pas besoin de `highp`. Les shaders GLSL ES issus d'une compilation croisée utilisent par défaut `mediump` pour les valeurs à virgule flottante et `highp` pour les entiers, et ces valeurs par défaut peuvent être modifiées dans la section Shader des paramètres du projet. Les qualificatifs explicites définis pour chaque variable sont prioritaires. Consultez la [documentation sur la précision des shaders](/manuals/shader/#precision).

## Réduire la complexité du graphe de scène {#reduce-scene-graph-complexity}
Il est nécessaire de réduire la complexité du graphe de scène si le profileur affiche des valeurs élevées dans la section `GameObject`, et plus particulièrement pour l'échantillon `UpdateTransform`. Voici quelques mesures à prendre :

* Élimination des éléments invisibles - Désactivez les objets de jeu (et leurs composants) s'ils ne sont pas visibles à l'instant présent. La façon de le déterminer dépend beaucoup du type de jeu. Pour un jeu en 2D, il peut suffire de toujours désactiver les objets de jeu situés en dehors d'une zone rectangulaire. Vous pouvez le détecter à l'aide d'un déclencheur physique ou en répartissant vos objets en groupes. Une fois que vous savez quels objets désactiver ou activer, envoyez un message `disable` ou `enable` à chaque objet de jeu.

## Élimination des éléments hors du volume de vue {#frustum-culling}
Le script de rendu peut automatiquement ignorer le rendu des composants d'objets de jeu situés en dehors d'une boîte englobante définie (frustum). Pour en savoir plus sur l'élimination des éléments hors du volume de vue, consultez le [manuel sur le pipeline de rendu](/manuals/render/#frustum-culling).

# Optimisations propres aux plateformes {#platform-specific-optimizations}

## Framework de performances des appareils Android {#android-device-performance-framework}
Android Dynamic Performance Framework est un ensemble d'API qui permettent aux jeux d'interagir plus directement avec les systèmes de gestion de l'énergie et de la température des appareils Android. Il est possible de surveiller le comportement dynamique des systèmes Android et d'optimiser les performances du jeu à un niveau durable qui ne provoque pas de surchauffe des appareils. Utilisez l'[extension Android Dynamic Performance Framework](https://defold.com/extension-adpf/) pour surveiller et optimiser les performances de votre jeu Defold sur les appareils Android.
