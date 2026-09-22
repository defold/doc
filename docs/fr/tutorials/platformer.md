---
title: Tutoriel Defold sur les jeux de plateforme
brief: Dans cet article, vous découvrez l'implémentation d'un jeu de plateforme 2D simple basé sur des tuiles dans Defold. Vous apprenez les mécaniques de déplacement à gauche et à droite, de saut et de chute.
---

# Jeu de plateforme {#platformer}

Dans cet article, nous découvrons l'implémentation d'un jeu de plateforme 2D simple basé sur des tuiles dans Defold. Les mécaniques que nous allons apprendre sont le déplacement à gauche et à droite, le saut et la chute.

Il existe de nombreuses façons de créer un jeu de plateforme. Rodrigo Monteiro a rédigé une analyse exhaustive sur le sujet et bien plus encore [ici](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/).

Nous vous recommandons vivement de la lire si vous débutez dans la création de jeux de plateforme, car elle contient de nombreuses informations précieuses. Nous allons approfondir quelques-unes des méthodes décrites et voir comment les implémenter dans Defold. L'ensemble devrait toutefois être facile à porter vers d'autres plateformes et langages (nous utilisons Lua dans Defold).

Nous supposons que vous avez quelques notions de mathématiques vectorielles (algèbre linéaire). Si ce n'est pas le cas, il est judicieux de vous renseigner sur le sujet, car elles sont extrêmement utiles pour le développement de jeux. David Rosen, de Wolfire, a rédigé une très bonne série d'articles à ce sujet [ici](http://blog.wolfire.com/2009/07/linear-algebra-for-game-developers-part-1/).

Si vous utilisez déjà Defold, vous pouvez créer un projet à partir du modèle _Platformer_ et faire des essais pendant la lecture de cet article.

::: sidenote
Certains lecteurs ont signalé que la méthode que nous proposons n'est pas possible avec l'implémentation par défaut de Box2D. Nous avons apporté quelques modifications à Box2D pour la faire fonctionner :

Les collisions entre les objets cinématiques et statiques sont ignorées. Modifiez les vérifications dans `b2Body::ShouldCollide` et `b2ContactManager::Collide`.

De plus, la distance de contact (appelée séparation dans Box2D) n'est pas fournie à la fonction de rappel.
Ajoutez un membre de distance à `b2ManifoldPoint` et assurez-vous qu'il est mis à jour dans les fonctions `b2Collide*`.
:::

## Détection des collisions {#collision-detection}

La détection des collisions est nécessaire pour empêcher le personnage du joueur de traverser la géométrie du niveau.
Il existe plusieurs façons de la gérer, selon votre jeu et ses exigences particulières.
L'une des plus simples, lorsque c'est possible, consiste à confier cette tâche à un moteur physique.
Dans Defold, nous utilisons le moteur physique [Box2D](http://box2d.org/) pour les jeux 2D.
L'implémentation par défaut de Box2D ne dispose pas de toutes les fonctionnalités nécessaires ; consultez la fin de cet article pour savoir comment nous l'avons modifiée.

Un moteur physique stocke l'état des objets physiques ainsi que leurs formes afin de simuler leur comportement physique. Il signale également les collisions au cours de la simulation, afin que le jeu puisse réagir lorsqu'elles se produisent. Dans la plupart des moteurs physiques, il existe trois types d'objets : les objets _statiques_, _dynamiques_ et _cinématiques_ (ces noms peuvent être différents dans d'autres moteurs physiques). Il existe aussi d'autres types d'objets, mais laissons-les de côté pour l'instant.

- Un objet *statique* ne se déplace jamais (par exemple, la géométrie du niveau).
- Un objet *dynamique* est soumis à des forces et à des couples qui sont transformés en vitesses au cours de la simulation.
- Un objet *cinématique* est contrôlé par la logique de l'application, mais agit tout de même sur les autres objets dynamiques.

Dans un jeu comme celui-ci, nous recherchons un comportement qui ressemble à la physique du monde réel, mais il est bien plus important d'avoir des commandes réactives et des mécaniques équilibrées. Un saut agréable n'a pas besoin d'être physiquement exact ni soumis à la gravité du monde réel. [Cette](http://hypertextbook.com/facts/2007/mariogravity.shtml) analyse montre toutefois que la gravité dans les jeux Mario se rapproche d'une gravité de 9,8 m/s<sup>2</sup> à chaque version. :-)

Il est important de maîtriser entièrement ce qui se passe pour pouvoir concevoir et ajuster les mécaniques afin d'obtenir l'expérience souhaitée. C'est pourquoi nous choisissons de représenter le personnage du joueur par un objet cinématique. Nous pouvons alors déplacer le personnage à notre guise, sans avoir à gérer les forces physiques. Cela signifie que nous devrons résoudre nous-mêmes la séparation entre le personnage et la géométrie du niveau (nous y reviendrons plus tard), mais c'est un inconvénient que nous acceptons. Nous représenterons le personnage du joueur par une forme de boîte dans le monde physique.

## Déplacement {#movement}

Maintenant que nous avons décidé de représenter le personnage du joueur par un objet cinématique, nous pouvons le déplacer librement en définissant sa position. Commençons par le déplacement à gauche et à droite.

Le déplacement reposera sur l'accélération, pour donner une sensation de poids au personnage. Comme pour un véhicule ordinaire, l'accélération définit la rapidité avec laquelle le personnage du joueur peut atteindre la vitesse maximale et changer de direction. L'accélération agit pendant le pas de temps de l'image---généralement fourni dans un paramètre `dt` (delta-`t`)---puis le résultat est ajouté à la vitesse. De la même manière, la vitesse agit pendant l'image et le déplacement obtenu est ajouté à la position. En mathématiques, cela s'appelle l'[intégration par rapport au temps](http://en.wikipedia.org/wiki/Integral).

![Intégration approchée de la vitesse](images/platformer/integration.png)

Les deux lignes verticales marquent le début et la fin de l'image. Leur hauteur représente la vitesse du personnage du joueur à ces deux instants. Appelons ces vitesses `v0` et `v1`. `v1` s'obtient en appliquant l'accélération (la pente de la courbe) pendant le pas de temps `dt` :

![Équation de la vitesse](images/platformer/equationofvelocity.png)

La surface orange représente le déplacement que nous devons appliquer au personnage du joueur pendant l'image courante. Géométriquement, nous pouvons approximer cette surface ainsi :

![Équation du déplacement](images/platformer/equationoftranslation.png)

Voici comment intégrer l'accélération et la vitesse pour déplacer le personnage dans la boucle de mise à jour :

1. Déterminez la vitesse cible à partir des entrées
2. Calculez la différence entre la vitesse actuelle et la vitesse cible
3. Définissez l'accélération pour qu'elle agisse dans le sens de cette différence
4. Calculez la variation de vitesse pour cette image (`dv` est l'abréviation de delta-vitesse), comme ci-dessus :

    ```lua
    local dv = acceleration * dt
    ```

5. Vérifiez si `dv` dépasse la différence de vitesse prévue et limitez-la à cette différence dans ce cas
6. Enregistrez la vitesse actuelle pour l'utiliser plus tard (`self.velocity`, qui contient pour l'instant la vitesse utilisée lors de l'image précédente) :

    ```lua
    local v0 = self.velocity
    ```

7. Calculez la nouvelle vitesse en ajoutant la variation de vitesse :

    ```lua
    self.velocity = self.velocity + dv
    ```

8. Calculez le déplacement selon x pour cette image en intégrant la vitesse, comme ci-dessus :

    ```lua
    local dx = (v0 + self.velocity) * dt * 0.5
    ```

9. Appliquez-le au personnage du joueur

Si vous ne savez pas bien comment gérer les entrées dans Defold, vous trouverez un guide à ce sujet [ici](/manuals/input).

À ce stade, nous pouvons déplacer le personnage à gauche et à droite, avec des commandes fluides qui donnent une sensation de poids. Ajoutons maintenant la gravité !

La gravité est aussi une accélération, mais elle agit sur le personnage selon l'axe y. Elle sera donc appliquée de la même manière que l'accélération de déplacement décrite ci-dessus. Il suffit de passer aux vecteurs dans les calculs précédents et de veiller à inclure la gravité dans la composante y de l'accélération à l'étape 3) pour que tout fonctionne. Vive les mathématiques vectorielles ! :-)

## Réponse aux collisions {#collision-response}

Notre personnage peut maintenant se déplacer et tomber ; il est donc temps de nous intéresser aux réponses aux collisions.
Nous devons évidemment pouvoir atterrir et nous déplacer le long de la géométrie du niveau. Nous utiliserons les points de contact fournis par le moteur physique pour nous assurer de ne jamais chevaucher quoi que ce soit.

Un point de contact contient une _normale_ du contact (qui pointe vers l'extérieur de l'objet avec lequel nous entrons en collision, mais cela peut être différent dans d'autres moteurs) ainsi qu'une _distance_, qui mesure à quelle profondeur nous avons pénétré dans l'autre objet. Cela suffit pour séparer le personnage de la géométrie du niveau.
Comme nous utilisons une boîte, nous pouvons obtenir plusieurs points de contact pendant une image. Cela se produit par exemple lorsque deux coins de la boîte coupent le sol horizontal, ou lorsque le personnage se déplace dans un angle.

![Normales de contact agissant sur le personnage du joueur](images/platformer/collision.png)

Pour éviter d'appliquer plusieurs fois la même correction, nous cumulons les corrections dans un vecteur afin de ne pas trop compenser. Une compensation excessive nous placerait trop loin de l'objet avec lequel nous sommes entrés en collision. Dans l'image ci-dessus, vous pouvez voir que nous avons deux points de contact, représentés par les deux flèches (normales). La distance de pénétration est identique pour les deux contacts ; si nous l'utilisions aveuglément à chaque fois, nous déplacerions le personnage du double de la distance prévue.

::: sidenote
Il est important de remettre les corrections cumulées au vecteur nul à chaque image.
Ajoutez quelque chose comme ceci à la fin de la fonction `update()` :
`self.corrections = vmath.vector3()`
:::

En supposant qu'une fonction de rappel soit appelée pour chaque point de contact, voici comment effectuer la séparation dans cette fonction :

```lua
local proj = vmath.dot(self.correction, normal) -- <1>
local comp = (distance - proj) * normal -- <2>
self.correction = self.correction + comp -- <3>
go.set_position(go.get_position() + comp) -- <4>
```

1. Projetez le vecteur de correction sur la normale de contact (le vecteur de correction est le vecteur nul pour le premier point de contact)
2. Calculez la compensation à appliquer pour ce point de contact
3. Ajoutez-la au vecteur de correction
4. Appliquez la compensation au personnage du joueur

Nous devons également annuler la partie de la vitesse du personnage qui le déplace vers le point de contact :

```lua
proj = vmath.dot(self.velocity, message.normal) -- <1>
if proj < 0 then
    self.velocity = self.velocity - proj * message.normal -- <2>
end
```
1. Projetez la vitesse sur la normale
2. Si la projection est négative, cela signifie qu'une partie de la vitesse pointe vers le point de contact ; supprimez cette composante dans ce cas

## Saut {#jumping}

Maintenant que nous pouvons courir sur la géométrie du niveau et tomber, il est temps de sauter ! Les sauts dans un jeu de plateforme peuvent être implémentés de nombreuses façons. Dans ce jeu, nous visons un comportement similaire à celui de Super Mario Bros et de Super Meat Boy. Lors d'un saut, le personnage du joueur est propulsé vers le haut par une impulsion, qui correspond essentiellement à une vitesse fixe.

La gravité ramène continuellement le personnage vers le bas, ce qui donne une belle trajectoire de saut en arc. En l'air, le joueur peut toujours contrôler le personnage. Si le joueur relâche le bouton de saut avant le sommet de la trajectoire, la vitesse ascendante est réduite pour interrompre le saut prématurément.

1. Lorsque le bouton est enfoncé, exécutez :

    ```lua
    -- jump_takeoff_speed is a constant defined elsewhere
    self.velocity.y = jump_takeoff_speed
    ```

    Cela ne doit se produire qu'au moment où le bouton est _enfoncé_, et non à chaque image pendant laquelle il est _maintenu enfoncé_.

2. Lorsque le bouton est relâché, exécutez :

    ```lua
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
    ```

ExciteMike a réalisé de beaux graphiques des trajectoires de saut dans [Super Mario Bros 3](http://meyermike.com/wp/?p=175) et [Super Meat Boy](http://meyermike.com/wp/?p=160), qui méritent le détour.

## Géométrie du niveau {#level-geometry}

La géométrie du niveau correspond aux formes de collision de l'environnement avec lesquelles le personnage du joueur (et éventuellement d'autres éléments) entre en collision. Dans Defold, il existe deux façons de créer cette géométrie.

Vous pouvez créer des formes de collision distinctes par-dessus les niveaux que vous construisez. Cette méthode est très souple et permet de positionner précisément les éléments graphiques. Elle est particulièrement utile si vous voulez des pentes douces.
Le jeu [Braid](http://braid-game.com/) a utilisé cette méthode de construction des niveaux, tout comme le niveau d'exemple de ce tutoriel. Voici à quoi cela ressemble dans l'éditeur Defold :

![L'éditeur Defold avec la géométrie du niveau et le personnage placés dans le monde](images/platformer/editor.png)

Une autre option consiste à construire les niveaux à partir de tuiles et à laisser l'éditeur générer automatiquement les formes physiques à partir des graphismes des tuiles. La géométrie du niveau est alors automatiquement mise à jour lorsque vous modifiez les niveaux, ce qui peut être extrêmement utile.

Les formes physiques des tuiles placées sont automatiquement fusionnées en une seule si elles sont alignées.
Cela élimine les interstices qui peuvent arrêter votre personnage ou provoquer des à-coups lorsqu'il glisse sur plusieurs tuiles horizontales. Pour cela, les polygones des tuiles sont remplacés par des formes d'arêtes dans Box2D au chargement.

![Plusieurs polygones de tuiles assemblés en un seul](images/platformer/stitching.png)

L'exemple ci-dessus présente cinq tuiles voisines que nous avons créées à partir d'un morceau des graphismes du jeu de plateforme. Dans l'image, vous pouvez voir comment les tuiles placées (en haut) correspondent à une seule forme issue de leur assemblage (contour gris en bas).

Consultez nos guides sur la [physique](/manuals/physics) et les [tuiles](/manuals/2dgraphics) pour en savoir plus.

## Pour terminer {#final-words}

Si vous souhaitez en savoir plus sur les mécaniques des jeux de plateforme, voici une quantité impressionnante d'informations sur la physique dans [Sonic](http://info.sonicretro.org/Sonic_Physics_Guide).

Si vous essayez notre modèle de projet sur un appareil iOS ou avec une souris, le saut peut sembler vraiment maladroit.
Ce n'est que notre modeste tentative de créer des commandes de jeu de plateforme avec une seule entrée tactile. :-)

Nous n'avons pas parlé de la gestion des animations dans ce jeu. Vous pouvez vous en faire une idée en consultant le fichier *player.script* ci-dessous ; cherchez la fonction `update_animations()`.

Nous espérons que ces informations vous ont été utiles !
Créez un excellent jeu de plateforme pour que nous puissions tous y jouer ! <3

## Code {#code}

Voici le contenu de *player.script* :

```lua
-- player.script

-- these are the tweaks for the mechanics, feel free to change them for a different feeling
-- the acceleration to move right/left
local move_acceleration = 3500
-- acceleration factor to use when air-borne
local air_acceleration_factor = 0.8
-- max speed right/left
local max_speed = 450
-- gravity pulling the player down in pixel units
local gravity = -1000
-- take-off speed when jumping in pixel units
local jump_takeoff_speed = 550
-- time within a double tap must occur to be considered a jump (only used for mouse/touch controls)
local touch_jump_timeout = 0.2

-- prehashing ids improves performance
local msg_contact_point_response = hash("contact_point_response")
local msg_animation_done = hash("animation_done")
local group_obstacle = hash("obstacle")
local input_left = hash("left")
local input_right = hash("right")
local input_jump = hash("jump")
local input_touch = hash("touch")
local anim_run = hash("run")
local anim_idle = hash("idle")
local anim_jump = hash("jump")
local anim_fall = hash("fall")

function init(self)
    -- this lets us handle input in this script
    msg.post(".", "acquire_input_focus")

    -- initial player velocity
    self.velocity = vmath.vector3(0, 0, 0)
    -- support variable to keep track of collisions and separation
    self.correction = vmath.vector3()
    -- if the player stands on ground or not
    self.ground_contact = false
    -- movement input in the range [-1,1]
    self.move_input = 0
    -- the currently playing animation
    self.anim = nil
    -- timer that controls the jump-window when using mouse/touch
    self.touch_jump_timer = 0
end

local function play_animation(self, anim)
    -- only play animations which are not already playing
    if self.anim ~= anim then
        -- tell the sprite to play the animation
        sprite.play_flipbook("#sprite", anim)
        -- remember which animation is playing
        self.anim = anim
    end
end

local function update_animations(self)
    -- make sure the player character faces the right way
    sprite.set_hflip("#sprite", self.move_input < 0)
    -- make sure the right animation is playing
    if self.ground_contact then
        if self.velocity.x == 0 then
            play_animation(self, anim_idle)
        else
            play_animation(self, anim_run)
        end
    else
        if self.velocity.y > 0 then
            play_animation(self, anim_jump)
        else
            play_animation(self, anim_fall)
        end
    end
end

function update(self, dt)
    -- determine the target speed based on input
    local target_speed = self.move_input * max_speed
    -- calculate the difference between our current speed and the target speed
    local speed_diff = target_speed - self.velocity.x
    -- the complete acceleration to integrate over this frame
    local acceleration = vmath.vector3(0, gravity, 0)
    if speed_diff ~= 0 then
        -- set the acceleration to work in the direction of the difference
        if speed_diff < 0 then
            acceleration.x = -move_acceleration
        else
            acceleration.x = move_acceleration
        end
        -- decrease the acceleration when air-borne to give a slower feel
        if not self.ground_contact then
            acceleration.x = air_acceleration_factor * acceleration.x
        end
    end
    -- calculate the velocity change this frame (dv is short for delta-velocity)
    local dv = acceleration * dt
    -- check if dv exceeds the intended speed difference, clamp it in that case
    if math.abs(dv.x) > math.abs(speed_diff) then
        dv.x = speed_diff
    end
    -- save the current velocity for later use
    -- (self.velocity, which right now is the velocity used the previous frame)
    local v0 = self.velocity
    -- calculate the new velocity by adding the velocity change
    self.velocity = self.velocity + dv
    -- calculate the translation this frame by integrating the velocity
    local dp = (v0 + self.velocity) * dt * 0.5
    -- apply it to the player character
    go.set_position(go.get_position() + dp)

    -- update the jump timer
    if self.touch_jump_timer > 0 then
        self.touch_jump_timer = self.touch_jump_timer - dt
    end

    update_animations(self)

    -- reset volatile state
    self.correction = vmath.vector3()
    self.move_input = 0
    self.ground_contact = false

end

local function handle_obstacle_contact(self, normal, distance)
    -- project the correction vector onto the contact normal
    -- (the correction vector is the 0-vector for the first contact point)
    local proj = vmath.dot(self.correction, normal)
    -- calculate the compensation we need to make for this contact point
    local comp = (distance - proj) * normal
    -- add it to the correction vector
    self.correction = self.correction + comp
    -- apply the compensation to the player character
    go.set_position(go.get_position() + comp)
    -- check if the normal points enough up to consider the player standing on the ground
    -- (0.7 is roughly equal to 45 degrees deviation from pure vertical direction)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- project the velocity onto the normal
    proj = vmath.dot(self.velocity, normal)
    -- if the projection is negative, it means that some of the velocity points towards the contact point
    if proj < 0 then
        -- remove that component in that case
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    -- check if we received a contact point message
    if message_id == msg_contact_point_response then
        -- check that the object is something we consider an obstacle
        if message.group == group_obstacle then
            handle_obstacle_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- only allow jump from ground
    -- (extend this with a counter to do things like double-jumps)
    if self.ground_contact then
        -- set take-off speed
        self.velocity.y = jump_takeoff_speed
        -- play animation
        play_animation(self, anim_jump)
    end
end

local function abort_jump(self)
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == input_left then
        self.move_input = -action.value
    elseif action_id == input_right then
        self.move_input = action.value
    elseif action_id == input_jump then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    elseif action_id == input_touch then
        -- move towards the touch-point
        local diff = action.x - go.get_position().x
        -- only give input when far away (more than 10 pixels)
        if math.abs(diff) > 10 then
            -- slow down when less than 100 pixels away
            self.move_input = diff / 100
            -- clamp input to [-1,1]
            self.move_input = math.min(1, math.max(-1, self.move_input))
        end
        if action.released then
            -- start timing the last release to see if we are about to jump
            self.touch_jump_timer = touch_jump_timeout
        elseif action.pressed then
            -- jump on double tap
            if self.touch_jump_timer > 0 then
                jump(self)
            end
        end
    end
end
```
