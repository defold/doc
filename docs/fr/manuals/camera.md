---
title: Manuel du composant caméra
brief: Ce manuel décrit les fonctionnalités du composant caméra de Defold.
---

# Caméras {#cameras}

Une caméra dans Defold est un composant (component) qui modifie la fenêtre d'affichage et la projection du monde de jeu (game world). Le composant caméra définit une caméra élémentaire en perspective ou orthographique, qui fournit au script de rendu une matrice de vue et une matrice de projection.

Une caméra en perspective est généralement utilisée pour les jeux 3D, dans lesquels la vue de la caméra ainsi que la taille et la perspective des objets dépendent d'un volume de visualisation (view frustum), de la distance et de l'angle de vue entre la caméra et les objets du jeu.

Pour les jeux 2D, il est souvent souhaitable d'effectuer le rendu de la scène avec une projection orthographique. Cela signifie que la vue de la caméra n'est plus définie par un volume de visualisation en perspective, mais par une boîte. La projection orthographique n'est pas réaliste, car elle ne modifie pas la taille des objets en fonction de leur distance. Un objet situé à 1000 unités sera affiché à la même taille qu'un objet placé juste devant la caméra.

![projections](images/camera/projections.png)


## Création d'une caméra {#creating-a-camera}

Pour créer une caméra, <kbd>faites un clic droit</kbd> sur un objet de jeu (game object) et sélectionnez <kbd>Add Component ▸ Camera</kbd>. Vous pouvez également créer un fichier de composant dans la hiérarchie de votre projet et l'ajouter à l'objet de jeu.

![création d'un composant caméra](images/camera/create.png)

Le composant caméra possède les propriétés suivantes, qui définissent le *volume de visualisation* de la caméra :

![paramètres de la caméra](images/camera/settings.png)

Id
: L'identifiant du composant

Aspect Ratio
: (**Caméra en perspective uniquement**) - Le rapport entre la largeur et la hauteur du volume de visualisation. 1.0 correspond à une vue carrée. 1.33 convient à une vue 4:3, comme 1024x768. 1.78 convient à une vue 16:9. Ce paramètre est ignoré si *Auto Aspect Ratio* est activé.

Fov
: (**Caméra en perspective uniquement**) - Le champ de vision *vertical* de la caméra, exprimé en _radians_. Plus le champ de vision est large, plus la caméra voit d'éléments.

Near Z
: La valeur Z du plan de découpage proche.

Far Z
: La valeur Z du plan de découpage lointain.

Auto Aspect Ratio
: (**Caméra en perspective uniquement**) - Activez ce paramètre pour laisser la caméra calculer automatiquement le rapport largeur/hauteur.

Orthographic Projection
: Activez ce paramètre pour passer la caméra en projection orthographique (voir ci-dessous).

Orthographic Zoom
: (**Caméra orthographique uniquement**) - Un multiplicateur de zoom contrôlé par l'utilisateur (> 1 = zoom avant, < 1 = zoom arrière). En mode `Fixed`, il s'agit du zoom effectif. Dans les modes `Auto Fit` et `Auto Cover`, il est multiplié par le zoom calculé automatiquement, ce qui permet d'ajouter un zoom supplémentaire sans désactiver le dimensionnement automatique.

Orthographic Mode
: (**Caméra orthographique uniquement**) - Détermine comment la caméra orthographique calcule le zoom par rapport à la taille de la fenêtre et à votre résolution de conception (les valeurs de `game.project` → `display.width/height`).
  - `Fixed` (utilise un zoom constant) : utilise la valeur actuelle de `Orthographic Zoom` telle quelle.
  - `Auto Fit` (contenir) : calcule automatiquement le zoom pour que toute la zone de conception tienne dans la fenêtre, puis le multiplie par `Orthographic Zoom`. Peut afficher du contenu supplémentaire sur les côtés ou en haut et en bas.
  - `Auto Cover` (couvrir) : calcule automatiquement le zoom pour que la zone de conception couvre toute la fenêtre, puis le multiplie par `Orthographic Zoom`. Peut rogner le contenu sur les côtés ou en haut et en bas.
  Disponible uniquement lorsque `Orthographic Projection` est activé.


## Utilisation de la caméra {#using-the-camera}

Toutes les caméras sont automatiquement activées et mises à jour à chaque image, et le module Lua `camera` est disponible dans tous les contextes de script. Depuis Defold 1.8.1, il n'est plus nécessaire d'activer explicitement une caméra en envoyant un message `acquire_camera_focus` au composant caméra. Les anciens messages d'acquisition et de libération sont toujours disponibles, mais il est recommandé d'utiliser les messages `enable` et `disable`, comme pour tout autre composant que vous souhaitez activer ou désactiver :

```lua
msg.post("#camera", "disable")
msg.post("#camera", "enable")
```

Pour lister toutes les caméras actuellement disponibles, vous pouvez utiliser `camera.get_cameras()` :

```lua
-- Note: The render calls are only available in a render script.
--       The camera.get_cameras() function can be used anywhere,
--       but render.set_camera can only be used in a render script.

for k,v in pairs(camera.get_cameras()) do
    -- the camera table contains the URLs of all cameras
    render.set_camera(v)
    -- do rendering here - anything rendered here that uses materials with
    -- view and projection matrices specified, will use matrices from the camera.
end
-- to disable a camera, pass in nil (or no arguments at all) to render.set_camera.
-- after this call, all render calls will use the view and projection matrices
-- that are specified on the render context (render.set_view and render.set_projection)
render.set_camera()
```

Le module de script `camera` propose plusieurs fonctions permettant de manipuler la caméra. Voici quelques-unes de ces fonctions ; pour consulter toutes les fonctions disponibles, reportez-vous à la [documentation de l'API](/ref/camera/)).

```lua
camera.get_aspect_ratio(camera) -- get aspect ratio
camera.get_far_z(camera) -- get far z
camera.get_fov(camera) -- get field of view
camera.get_orthographic_mode(camera) -- get orthographic mode (one of camera.ORTHO_MODE_*)
camera.get_orthographic_zoom(camera) -- get the user-controlled zoom multiplier
camera.get_orthographic_auto_zoom(camera) -- get the automatically calculated zoom
camera.set_aspect_ratio(camera, ratio) -- set aspect ratio
camera.set_far_z(camera, far_z) -- set far z
camera.set_near_z(camera, near_z) -- set near z
camera.set_orthographic_mode(camera, camera.ORTHO_MODE_AUTO_FIT) -- set orthographic mode
... And so forth
```

Une caméra est identifiée par une URL, qui correspond au chemin complet du composant dans la scène et comprend la collection, l'objet de jeu auquel il appartient et l'identifiant du composant. Dans cet exemple, vous utiliseriez l'URL `/go#camera` pour identifier le composant caméra depuis la même collection, et `main:/go#camera` pour accéder à une caméra depuis une autre collection ou depuis le script de rendu.

![création d'un composant caméra](images/camera/create.png)

```lua
-- Accessing a camera from a script in the same collection:
camera.get_fov("/go#camera")

-- Accessing a camera from a script in a different collection:
camera.get_fov("main:/go#camera")

-- Accessing a camera from the render script:
render.set_camera("main:/go#camera")
```

À chaque image, le composant caméra qui possède actuellement le focus caméra envoie un message `set_view_projection` au socket `@render` :

```lua
-- builtins/render/default.render_script
--
function on_message(self, message_id, message)
    if message_id == hash("set_view_projection") then
        self.view = message.view                    -- [1]
        self.projection = message.projection
    end
end
```
1. Le message envoyé par le composant caméra contient une matrice de vue et une matrice de projection.

Le composant caméra fournit au script de rendu une matrice de projection en perspective ou orthographique, selon la propriété *Orthographic Projection* de la caméra. La matrice de projection tient également compte des plans de découpage proche et lointain définis, du champ de vision et du rapport largeur/hauteur de la caméra.

La matrice de vue fournie par la caméra définit sa position et son orientation. Une caméra avec une *Orthographic Projection* centre la vue sur la position de l'objet de jeu auquel elle est attachée, tandis qu'une caméra avec une *Perspective Projection* place le coin inférieur gauche de la vue sur l'objet de jeu auquel elle est attachée.


### Script de rendu {#render-script}

Lorsque vous utilisez le script de rendu par défaut, Defold sélectionne automatiquement la dernière caméra activée pour le rendu. Avant ce changement, un script du projet devait envoyer explicitement le message `use_camera_projection` au moteur de rendu pour lui indiquer d'utiliser la vue et la projection des composants caméra. Cela n'est plus nécessaire, mais reste possible à des fins de rétrocompatibilité.

Vous pouvez également sélectionner dans un script de rendu une caméra précise à utiliser pour le rendu. Cela peut être utile lorsque vous devez contrôler plus précisément la caméra utilisée pour le rendu, par exemple dans un jeu multijoueur.

```lua
-- render.set_camera will automatically use the view and projection matrices
-- for any rendering happening until render.set_camera() is called.
render.set_camera("main:/my_go#camera")
```

Pour vérifier si une caméra est active ou non, vous pouvez utiliser la fonction `get_enabled` de l'[API caméra](https://defold.com/ref/alpha/camera/#camera.get_enabled:camera) :

```lua
if camera.get_enabled("main:/my_go#camera") then
    -- camera is enabled, use it for rendering!
    render.set_camera("main:/my_go#camera")
end
```

::: sidenote
Pour utiliser la fonction `set_camera` avec l'élimination des éléments hors du volume de visualisation, vous devez passer cette option à la fonction :
`render.set_camera("main:/my_go#camera", {use_frustum = true})`
:::

### Déplacement de la caméra {#panning-the-camera}

Vous déplacez la caméra dans le monde de jeu en déplaçant l'objet de jeu auquel le composant caméra est attaché. Le composant caméra envoie automatiquement une matrice de vue mise à jour en fonction de la position actuelle de la caméra sur les axes x et y.

### Zoom de la caméra {#zooming-the-camera}

Avec une caméra en perspective, vous pouvez effectuer un zoom avant ou arrière en déplaçant l'objet de jeu auquel la caméra est attachée le long de l'axe z. Le composant caméra envoie automatiquement une matrice de vue mise à jour en fonction de la position actuelle de la caméra sur l'axe z.

Avec une caméra orthographique, vous pouvez effectuer un zoom avant ou arrière en modifiant la propriété *Orthographic Zoom* de la caméra, dans l'éditeur ou en cours d'exécution :

```lua
-- In Fixed mode, this is the effective zoom.
go.set("#camera", "orthographic_zoom", 2)
```

Dans les modes `Auto Fit` et `Auto Cover`, *Orthographic Zoom* s'applique au zoom calculé automatiquement ; il n'est pas ignoré. Par exemple, réglez *Orthographic Mode* sur `Auto Fit` et *Orthographic Zoom* sur `1.25` dans l'éditeur pour adapter la zone de conception à la fenêtre, puis effectuer un zoom avant supplémentaire de 25 %. La configuration équivalente à l'exécution est la suivante :

```lua
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)
go.set("#camera", "orthographic_zoom", 1.25)

local auto_zoom = camera.get_orthographic_auto_zoom("#camera")
local zoom_multiplier = camera.get_orthographic_zoom("#camera")
local effective_zoom = auto_zoom * zoom_multiplier
```

`camera.get_orthographic_auto_zoom()` renvoie le zoom calculé à partir des dimensions actuelles de la fenêtre et du projet dans les modes `Auto Fit` et `Auto Cover`. Cette fonction renvoie `1.0` en mode `Fixed`. La même valeur est disponible via la propriété du composant `orthographic_auto_zoom`, accessible en lecture seule :

```lua
local auto_zoom = go.get("#camera", "orthographic_auto_zoom")
```

Avec une caméra orthographique, vous pouvez également changer la façon dont le zoom est déterminé à l'aide du paramètre `Orthographic Mode` ou par script :

```lua
-- get current mode (one of camera.ORTHO_MODE_FIXED, _AUTO_FIT, _AUTO_COVER)
local mode = camera.get_orthographic_mode("#camera")

-- switch to auto-fit (contain) to always keep the full design area visible
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)

-- switch to auto-cover to ensure the design area covers the window
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_COVER)

-- switch to fixed mode to use orthographic_zoom without automatic sizing
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_FIXED)
```

### Zoom adaptatif {#adaptive-zoom}

Le principe du zoom adaptatif consiste à ajuster la valeur du zoom de la caméra lorsque la résolution de l'affichage diffère de la résolution initiale définie dans *game.project*.

Deux approches courantes du zoom adaptatif sont les suivantes :

1. Zoom maximal - Calculez une valeur de zoom telle que le contenu couvert par la résolution initiale dans *game.project* remplisse l'écran et dépasse ses limites, ce qui peut masquer une partie du contenu sur les côtés ou en haut et en bas.
2. Zoom minimal - Calculez une valeur de zoom telle que le contenu couvert par la résolution initiale dans *game.project* tienne entièrement dans les limites de l'écran, ce qui peut afficher du contenu supplémentaire sur les côtés ou en haut et en bas.

Exemple :

```lua
local DISPLAY_WIDTH = sys.get_config_int("display.width")
local DISPLAY_HEIGHT = sys.get_config_int("display.height")

function init(self)
    local initial_zoom = go.get("#camera", "orthographic_zoom")
    local display_scale = window.get_display_scale()
    window.set_listener(function(self, event, data)
        if event == window.WINDOW_EVENT_RESIZED then
            local window_width = data.width
            local window_height = data.height
            local design_width = DISPLAY_WIDTH / initial_zoom
            local design_height = DISPLAY_HEIGHT / initial_zoom

            -- max zoom: ensure that the initial design dimensions will fill and expand beyond the screen bounds
            local zoom = math.max(window_width / design_width, window_height / design_height) / display_scale

            -- min zoom: ensure that the initial design dimensions will shrink and be contained within the screen bounds
            --local zoom = math.min(window_width / design_width, window_height / design_height) / display_scale
            
            go.set("#camera", "orthographic_zoom", zoom)
        end
    end)
end
```

Vous trouverez un exemple complet de zoom adaptatif dans [ce projet d'exemple](https://github.com/defold/sample-adaptive-zoom).

Remarque : avec une caméra orthographique, vous pouvez désormais obtenir un affichage entièrement contenu dans la fenêtre ou couvrant toute la fenêtre sans code personnalisé, en réglant `Orthographic Mode` sur `Auto Fit` (contenir) ou `Auto Cover` (couvrir). Dans ces modes, le zoom calculé à partir de la taille de la fenêtre et de la résolution de conception est multiplié par `Orthographic Zoom`.


### Suivi d'un objet de jeu {#following-a-game-object}

Vous pouvez faire suivre un objet de jeu par la caméra en définissant l'objet de jeu auquel le composant caméra est attaché comme enfant de l'objet de jeu à suivre :

![suivi d'un objet de jeu](images/camera/follow.png)

Une autre méthode consiste à mettre à jour, à chaque image, la position de l'objet de jeu auquel le composant caméra est attaché, à mesure que l'objet de jeu à suivre se déplace.

### Conversion entre les coordonnées écran et monde {#converting-mouse-to-world-coordinates}

Lorsque la caméra s'est déplacée, a zoomé ou a changé de projection, les coordonnées d'entrée ne correspondent plus directement aux coordonnées du monde. Utilisez les fonctions de conversion de la caméra avec `action.screen_x` et `action.screen_y`. Si l'URL facultative de la caméra est omise, la dernière caméra activée est utilisée.

Pour une caméra orthographique, [`camera.screen_xy_to_world()`](/ref/camera/#camera.screen_xy_to_world:x-y-[camera]) renvoie, pour un pixel de l'écran, le point situé sur le plan proche de la caméra dans l'espace du monde :

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local world_position = camera.screen_xy_to_world(
            action.screen_x, action.screen_y, "#camera")
        go.set_position(world_position, "/marker")
    end
end
```

Pour une caméra en perspective, [`camera.screen_to_world()`](/ref/camera/#camera.screen_to_world:pos-[camera]) prend un `vector3` dont la composante Z représente la profondeur de vue en unités du monde, mesurée depuis le plan de la caméra :

```lua
local depth = 10
local world_position = camera.screen_to_world(
    vmath.vector3(action.screen_x, action.screen_y, depth), "#camera")
```

[`camera.world_to_screen()`](/ref/camera/#camera.world_to_screen:world_pos-[camera]) effectue la conversion inverse. Cette fonction renvoie X et Y en pixels écran et utilise la même convention de profondeur de vue pour Z, ce qui permet de transmettre son résultat à `camera.screen_to_world()` :

```lua
-- Update the cached world transform first if the object moved this frame.
go.update_world_transform("/marker")
local world_position = go.get_world_position("/marker")
local screen_position = camera.world_to_screen(world_position, "#camera")
```

Consultez la [page d'exemples](https://defold.com/examples/render/screen_to_world/) pour voir la conversion de coordonnées en action. Un [projet d'exemple](https://github.com/defold/sample-screen-to-world-coordinates/) illustre également les mêmes API.

::: sidenote
Les [solutions de caméra tierces mentionnées dans ce manuel](/manuals/camera/#third-party-camera-solutions) proposent des fonctions de conversion depuis et vers les coordonnées écran.
:::

## Manipulation à l'exécution {#runtime-manipulation}
Vous pouvez manipuler les caméras en cours d'exécution au moyen de différents messages et propriétés (consultez la [documentation de l'API pour leur utilisation](/ref/camera/)).

Une caméra possède plusieurs propriétés que vous pouvez manipuler avec `go.get()` et `go.set()` :

`fov`
: Le champ de vision de la caméra (`number`).

`near_z`
: La valeur Z proche de la caméra (`number`).

`far_z`
: La valeur Z lointaine de la caméra (`number`).

`orthographic_zoom`
: Le multiplicateur de zoom de la caméra orthographique contrôlé par l'utilisateur. Dans les modes `Auto Fit` et `Auto Cover`, il est multiplié par `orthographic_auto_zoom`. (`number`).

`orthographic_auto_zoom`
: Le zoom orthographique calculé pour les modes `Auto Fit` et `Auto Cover`, ou `1.0` en mode `Fixed`. LECTURE SEULE. (`number`).

`aspect_ratio`
: Le rapport entre la largeur et la hauteur du volume de visualisation. Utilisé lors du calcul de la projection d'une caméra en perspective. (`number`).

`view`
: La matrice de vue calculée de la caméra. LECTURE SEULE. (`matrix4`).

`projection`
: La matrice de projection calculée de la caméra. LECTURE SEULE. (`matrix4`).


## Solutions de caméra tierces {#third-party-camera-solutions}

Des solutions de caméra créées par la communauté proposent des fonctionnalités courantes telles que les secousses de l'écran, le suivi d'objets de jeu, la conversion des coordonnées écran en coordonnées du monde et bien d'autres encore. Vous pouvez les télécharger depuis le portail de ressources Defold :

- [Caméra orthographique](https://defold.com/assets/orthographic/) (2D uniquement) de Björn Ritzl.
- [Defold Rendy](https://defold.com/assets/defold-rendy/) (2D et 3D) de Klayton Kowalski.
