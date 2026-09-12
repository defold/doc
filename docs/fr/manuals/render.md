---
title: Le pipeline de rendu dans Defold
brief: Ce manuel explique le fonctionnement du pipeline de rendu de Defold et comment le programmer.
---

# Rendu {#render}

Tous les objets affichés à l'écran par le moteur, qu'il s'agisse de sprites, de modèles, de tuiles, de particules ou de nœuds GUI, sont dessinés par un système de rendu. Au cœur de ce système se trouve un script de rendu qui contrôle le pipeline de rendu. Par défaut, chaque objet 2D est dessiné avec la bonne image bitmap, le mélange spécifié et la bonne profondeur Z : vous n'aurez donc peut-être jamais à vous préoccuper du rendu au-delà de l'ordre de dessin et d'un mélange simple. Le pipeline par défaut convient à la plupart des jeux 2D, mais votre jeu peut avoir des besoins particuliers. Dans ce cas, Defold vous permet d'écrire un pipeline de rendu sur mesure.

### Pipeline de rendu : quoi, quand et où ? {#render-pipeline-what-when-and-where}

Le pipeline de rendu contrôle les éléments à dessiner, le moment où les dessiner et l'endroit où les dessiner. Les éléments à dessiner sont contrôlés par les [prédicats de rendu](#render-predicates). Le moment où dessiner un prédicat est contrôlé dans le [script de rendu](#the-render-script), et l'endroit où le dessiner est contrôlé par la [projection de vue](#default-view-projection). Le pipeline de rendu peut également éliminer les éléments graphiques dessinés par un prédicat de rendu qui se trouvent en dehors d'une boîte englobante ou d'un volume de visibilité définis. Ce processus s'appelle l'élimination hors du volume de visibilité (frustum culling).


## Le rendu par défaut {#the-default-render}

Le fichier de rendu contient une référence au script de rendu actuel ainsi que les matériaux personnalisés qui doivent être accessibles dans le script de rendu (à utiliser avec [`render.enable_material()`](/ref/render/#render.enable_material))

Au cœur du pipeline de rendu se trouve le _script de rendu_. Il s'agit d'un script Lua contenant les fonctions `init()`, `update()` et `on_message()`, principalement utilisé pour interagir avec l'API graphique sous-jacente. Le script de rendu occupe une place particulière dans le cycle de vie de votre jeu. Vous trouverez des précisions dans la [documentation sur le cycle de vie de l'application](/manuals/application-lifecycle).

Dans le dossier "Builtins" de vos projets, vous trouverez la ressource de rendu par défaut ("default.render") et le script de rendu par défaut ("default.render_script").

![Rendu intégré](images/render/builtin.png)

Pour configurer un système de rendu personnalisé :

1. Copiez les fichiers "default.render" et "default.render_script" à un emplacement dans la hiérarchie de votre projet. Vous pouvez bien sûr créer un script de rendu à partir de zéro, mais il est préférable de commencer par une copie du script par défaut, surtout si vous débutez avec Defold et/ou la programmation graphique.

2. Modifiez votre copie du fichier "default.render" et changez la propriété *Script* pour qu'elle fasse référence à votre copie du script de rendu.

3. Changez la propriété *Render* (sous *bootstrap*) dans le fichier de paramètres *game.project* pour qu'elle fasse référence à votre copie du fichier "default.render".


## Prédicats de rendu {#render-predicates}

Pour contrôler l'ordre de dessin des objets, vous créez des _prédicats_ de rendu. Un prédicat déclare les éléments à dessiner à partir d'une sélection d'_étiquettes_ de matériau.

Chaque objet dessiné à l'écran possède un matériau qui contrôle la manière dont il doit être dessiné. Dans le matériau, vous spécifiez une ou plusieurs _étiquettes_ à associer au matériau.

Dans votre script de rendu, vous pouvez ensuite créer un *prédicat de rendu* et spécifier les étiquettes qui doivent lui appartenir. Lorsque vous demandez au moteur de dessiner le prédicat, chaque objet dont le matériau contient toutes les étiquettes spécifiées pour ce prédicat est dessiné.

```
Sprite 1        Sprite 2        Sprite 3        Sprite 4
Material A      Material A      Material B      Material C
  outlined        outlined        greyscale       outlined
  tree            tree            tree            house
```

```lua
-- a predicate matching all sprites with tag "tree"
local trees = render.predicate({"tree"})
-- will draw Sprite 1, 2 and 3
render.draw(trees)

-- a predicate matching all sprites with tag "outlined"
local outlined = render.predicate({"outlined"})
-- will draw Sprite 1, 2 and 4
render.draw(outlined)

-- a predicate matching all sprites with tags "outlined" AND "tree"
local outlined_trees = render.predicate({"outlined", "tree"})
-- will draw Sprite 1 and 2
render.draw(outlined_trees)
```


Vous trouverez une description détaillée du fonctionnement des matériaux dans la [documentation sur les matériaux](/manuals/material).


## Projection de vue par défaut {#default-view-projection}

Le script de rendu par défaut est configuré pour utiliser une projection orthographique adaptée aux jeux 2D. Il propose trois projections orthographiques différentes : `Stretch` (par défaut), `Fixed Fit` et `Fixed`. Au lieu des projections orthographiques du script de rendu par défaut, vous pouvez également utiliser la matrice de projection fournie par un composant (component) caméra.

### Projection étirée {#stretch-projection}

La projection étirée dessine toujours une zone de votre jeu correspondant aux dimensions définies dans *game.project*, même lorsque la fenêtre est redimensionnée. Si le rapport largeur/hauteur change, le contenu du jeu est étiré verticalement ou horizontalement :

![Projection étirée](images/render/stretch_projection.png)

*Projection étirée avec la taille de fenêtre d'origine*

![Projection étirée après redimensionnement](images/render/stretch_projection_resized.png)

*Projection étirée avec la fenêtre étirée horizontalement*

La projection étirée est la projection par défaut, mais si vous en avez choisi une autre et souhaitez y revenir, envoyez un message au script de rendu :

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

### Projection à ajustement fixe {#fixed-fit-projection}

Comme la projection étirée, la projection à ajustement fixe affiche toujours une zone du jeu correspondant aux dimensions définies dans *game.project*. Toutefois, si la fenêtre est redimensionnée et que le rapport largeur/hauteur change, le contenu du jeu conserve son rapport largeur/hauteur d'origine et une plus grande partie du jeu s'affiche verticalement ou horizontalement :

![Projection à ajustement fixe](images/render/fixed_fit_projection.png)

*Projection à ajustement fixe avec la taille de fenêtre d'origine*

![Projection à ajustement fixe après redimensionnement](images/render/fixed_fit_projection_resized.png)

*Projection à ajustement fixe avec la fenêtre étirée horizontalement*

![Projection à ajustement fixe après réduction](images/render/fixed_fit_projection_resized_smaller.png)

*Projection à ajustement fixe avec la fenêtre réduite à 50 % de sa taille d'origine*

Pour activer la projection à ajustement fixe, envoyez un message au script de rendu :

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

### Projection fixe {#fixed-projection}

La projection fixe conserve le rapport largeur/hauteur d'origine et dessine le contenu de votre jeu avec un niveau de zoom fixe. Cela signifie que, si le niveau de zoom est différent de 100 %, elle affiche une zone du jeu plus grande ou plus petite que celle définie par les dimensions dans *game.project* :

![Projection fixe](images/render/fixed_projection_zoom_2_0.png)

*Projection fixe avec un zoom réglé sur 2*

![Projection fixe](images/render/fixed_projection_zoom_0_5.png)

*Projection fixe avec un zoom réglé sur 0.5*

![Projection fixe](images/render/fixed_projection_zoom_2_0_resized.png)

*Projection fixe avec un zoom réglé sur 2 et la fenêtre réduite à 50 % de sa taille d'origine*

Pour activer la projection fixe, envoyez un message au script de rendu :

```lua
msg.post("@render:", "use_fixed_projection", { near = -1, far = 1, zoom = 2 })
```

### Projection de caméra {#camera-projection}

Lorsque vous utilisez le script de rendu par défaut et que des [composants caméra](/manuals/camera) sont activés dans le projet, ils ont priorité sur toute autre vue ou projection définie dans le script de rendu. Pour en savoir plus sur l'utilisation des composants caméra dans les scripts de rendu, consultez la [documentation sur les caméras](/manuals/camera).

Les caméras orthographiques prennent en charge un paramètre `Orthographic Mode` qui contrôle la façon dont la caméra s'adapte à la fenêtre :
- `Fixed` utilise la valeur `Orthographic Zoom` de la caméra.
- `Auto Fit` (contenir) garde toute la zone de conception visible.
- `Auto Cover` (couvrir) remplit la fenêtre et peut recadrer le contenu.

Vous pouvez changer de mode dans l'éditeur ou à l'exécution via l'API Camera :

```lua
-- Use auto-fit behavior with an orthographic camera
camera.set_orthographic_mode("main:/go#camera", camera.ORTHO_MODE_AUTO_FIT)
-- Query current mode
local mode = camera.get_orthographic_mode("main:/go#camera")
```

## Élimination hors du volume de visibilité {#frustum-culling}

L'API de rendu de Defold permet aux développeurs d'effectuer ce que l'on appelle l'élimination hors du volume de visibilité. Lorsque cette élimination est activée, tout élément graphique situé en dehors d'une boîte englobante ou d'un volume de visibilité définis est ignoré. Dans un grand monde de jeu (game world) dont seule une partie est visible à la fois, l'élimination hors du volume de visibilité peut réduire considérablement la quantité de données à envoyer au GPU pour le rendu, ce qui améliore les performances et économise la batterie (sur les appareils mobiles). Il est courant d'utiliser la vue et la projection de la caméra pour créer la boîte englobante. Le script de rendu par défaut utilise la vue et la projection (de la caméra) pour calculer un volume de visibilité.

Activez l'élimination hors du volume de visibilité pour un appel de dessin en passant une matrice de vue-projection dans l'option `frustum` de `render.draw()` :

```lua
local frustum = self.proj * self.view
render.draw(predicates.particle, { frustum = frustum })
```

Lors du rendu avec un composant caméra, `render.set_camera()` peut utiliser automatiquement la matrice de vue-projection de la caméra pour les appels de dessin suivants :

```lua
render.set_camera("main:/go#camera", { use_frustum = true })
render.draw(predicates.particle)
render.set_camera()
```

Lorsque l'une ou l'autre de ces méthodes est utilisée, les émetteurs Particle FX sont éliminés en fonction de leurs limites.

L'élimination hors du volume de visibilité est implémentée dans le moteur par type de composant. État actuel :

| Composant   | Pris en charge |
|-------------|-----------|
| Sprite      | OUI       |
| Model       | OUI       |
| Mesh        | OUI (1)   |
| Label       | OUI       |
| Spine       | OUI       |
| Particle fx | OUI       |
| Tilemap     | OUI       |
| Rive        | NON       |

1 = La boîte englobante du composant Mesh doit être définie par le développeur. [En savoir plus](/manuals/mesh/#frustum-culling).


::: sidenote
À partir de Defold 1.13.0, les sommets des primitives des composants sont ordonnés dans le sens antihoraire, avec la normale de la primitive dirigée vers la caméra. Les sprites, les nœuds GUI, les tilemaps (grilles de tuiles) et les Particle FX utilisent le même ordre que les autres types de composants ; les mêmes paramètres d'élimination des faces peuvent donc être utilisés pour tous les composants.

Cela peut affecter les projets qui configurent l'élimination des faces pour des composants autres que les modèles. Si un composant est éliminé de manière inattendue, assurez-vous que les faces arrière sont sélectionnées avec `render.set_cull_face(graphics.FACE_TYPE_BACK)`, ou supprimez l'appel à `render.set_cull_face()` pour utiliser le mode par défaut `graphics.FACE_TYPE_BACK`.
:::

## Systèmes de coordonnées {#coordinate-systems}

Lorsque des composants sont dessinés, on précise généralement le système de coordonnées dans lequel ils le sont. Dans la plupart des jeux, certains composants sont dessinés dans l'espace du monde et d'autres dans l'espace de l'écran.

Les composants GUI et leurs nœuds sont généralement dessinés dans le système de coordonnées de l'espace de l'écran, où le coin inférieur gauche de l'écran a pour coordonnées (0,0) et le coin supérieur droit (largeur de l'écran, hauteur de l'écran). Le système de coordonnées de l'espace de l'écran n'est jamais décalé ni translaté d'une autre manière par une caméra. Les nœuds GUI restent ainsi toujours dessinés à l'écran, quel que soit le rendu du monde.

Les sprites, les tilemaps et les autres composants utilisés par les objets de jeu (game objects) de votre monde de jeu sont généralement dessinés dans le système de coordonnées de l'espace du monde. Si vous ne modifiez pas votre script de rendu et n'utilisez aucun composant caméra pour changer la projection de vue, ce système de coordonnées est identique à celui de l'espace de l'écran. Dès que vous ajoutez une caméra et la déplacez ou changez la projection de vue, les deux systèmes de coordonnées divergent. Lorsque la caméra se déplace, le coin inférieur gauche de l'écran est décalé par rapport à (0, 0), de sorte que d'autres parties du monde sont dessinées. Si la projection change, les coordonnées sont à la fois translatées (c'est-à-dire décalées par rapport à 0, 0) et modifiées par un facteur d'échelle.


## Le script de rendu {#the-render-script}

Voici le code d'un script de rendu personnalisé qui est une version légèrement modifiée du script intégré.

init()
: La fonction `init()` sert à configurer les prédicats, la vue et la couleur d'effacement. Ces variables seront utilisées lors du rendu proprement dit.

```lua
function init(self)
    -- Define the render predicates. Each predicate is drawn by itself and
    -- that allows us to change the state of OpenGL between the draws.
    self.predicates = create_predicates("tile", "gui", "text", "particle", "model")

    -- Create and fill data tables will be used in update()
    local state = create_state()
    self.state = state
    local camera_world = create_camera(state, "camera_world", true)
    init_camera(camera_world, get_stretch_projection)
    local camera_gui = create_camera(state, "camera_gui")
    init_camera(camera_gui, get_gui_projection)
    update_state(state)
end
```

update()
: La fonction `update()` est appelée une fois par image. Elle effectue le dessin proprement dit en appelant les API OpenGL ES sous-jacentes (OpenGL Embedded Systems API). Pour bien comprendre ce qui se passe dans la fonction `update()`, vous devez comprendre le fonctionnement d'OpenGL. Il existe de nombreuses ressources de qualité sur OpenGL ES. Le site officiel est un bon point de départ. Vous le trouverez à l'adresse https://www.khronos.org/opengles/

  Cet exemple contient la configuration nécessaire pour dessiner des modèles 3D. La fonction `init()` a défini un prédicat `self.predicates.model`. Ailleurs, un matériau portant l'étiquette "model" a été créé. Certains composants de modèle utilisent également ce matériau :

```lua
function update(self)
    local state = self.state
     if not state.valid then
        if not update_state(state) then
            return
        end
    end

    local predicates = self.predicates
    -- clear screen buffers
    --
    render.set_depth_mask(true)
    render.set_stencil_mask(0xff)
    render.clear(state.clear_buffers)

    local camera_world = state.cameras.camera_world
    render.set_viewport(0, 0, state.window_width, state.window_height)
    render.set_view(camera_world.view)
    render.set_projection(camera_world.proj)


    -- render models
    --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_CULL_FACE)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_depth_mask(true)
    render.draw(predicates.model_pred)
    render.set_depth_mask(false)
    render.disable_state(graphics.STATE_DEPTH_TEST)
    render.disable_state(graphics.STATE_CULL_FACE)

     -- render world (sprites, tilemaps, particles etc)
     --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.enable_state(graphics.STATE_BLEND)
    render.draw(predicates.tile)
    render.draw(predicates.particle)
    render.disable_state(graphics.STATE_STENCIL_TEST)
    render.disable_state(graphics.STATE_DEPTH_TEST)

    -- debug
    render.draw_debug3d()

    -- render GUI
    --
    local camera_gui = state.cameras.camera_gui
    render.set_view(camera_gui.view)
    render.set_projection(camera_gui.proj)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.draw(predicates.gui, camera_gui.frustum)
    render.draw(predicates.text, camera_gui.frustum)
    render.disable_state(graphics.STATE_STENCIL_TEST)
end
```

Jusqu'ici, ce script de rendu est simple et direct. Il dessine de la même manière à chaque image. Cependant, il est parfois souhaitable de pouvoir introduire un état dans le script de rendu et d'effectuer différentes opérations en fonction de cet état. Il peut aussi être souhaitable de communiquer avec le script de rendu depuis d'autres parties du code du jeu.

on_message()
: Un script de rendu peut définir une fonction `on_message()` et recevoir des messages d'autres parties de votre jeu ou de votre application. La _caméra_ est un exemple courant de composant externe qui envoie des informations au script de rendu. Un composant caméra qui a obtenu le focus de la caméra envoie automatiquement sa vue et sa projection au script de rendu à chaque image. Ce message s'appelle `"set_view_projection"` :

```lua
local MSG_CLEAR_COLOR =         hash("clear_color")
local MSG_WINDOW_RESIZED =      hash("window_resized")
local MSG_SET_VIEW_PROJ =       hash("set_view_projection")

function on_message(self, message_id, message)
    if message_id == MSG_CLEAR_COLOR then
        -- Someone sent us a new clear color to be used.
        update_clear_color(state, message.color)
    elseif message_id == MSG_SET_VIEW_PROJ then
        -- The camera component that has camera focus will sent set_view_projection
        -- messages to the @render socket. We can use the camera information to
        -- set view (and possibly projection) of the rendering.
        camera.view = message.view
        self.camera_projection = message.projection or vmath.matrix4()
        update_camera(camera, state)
    end
end
```

Cependant, n'importe quel script ou script GUI peut envoyer des messages au script de rendu via le socket spécial `@render` :

```lua
-- Change the clear color.
msg.post("@render:", "clear_color", { color = vmath.vector4(0.3, 0.4, 0.5, 0) })
```

## Ressources de rendu {#render-resources}
Pour transmettre certaines ressources du moteur au script de rendu, vous pouvez les ajouter au tableau `Render Resources` du fichier `.render` affecté au projet :

![Ressources de rendu](images/render/render_resources.png)

Utilisation de ces ressources dans un script de rendu :

```lua
-- "my_material" will now be used for all draw calls associated with the predicate
render.enable_material("my_material")
-- anything drawn by the predicate will end up in "my_render_target"
render.set_render_target("my_render_target")
render.draw(self.my_full_screen_predicate)
render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.disable_material()

-- bind the render target result texture to whatever is getting rendered via the predicate
render.enable_texture(0, "my_render_target", graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.my_tile_predicate)
```

::: sidenote
Defold ne prend actuellement en charge que `Materials` et `Render Targets` comme ressources de rendu référencées, mais ce système prendra en charge davantage de types de ressources à l'avenir.
:::

### Cibles de rendu multi-échantillonnées {#multisampled-render-targets}

Les cibles de rendu prennent en charge l'anticrénelage multi-échantillons (MSAA). Il lisse les bords de la géométrie lors d'une passe de rendu hors écran. Le nombre d'échantillons de la cible est indépendant de [Display ▸ Samples](/manuals/project-settings/#samples), qui contrôle l'anticrénelage de la fenêtre.

Pour une ressource `.render_target`, définissez **Sample Count** dans l'éditeur sur `1`, `2`, `4`, `8` ou `16`. Une valeur de `1` désactive le multi-échantillonnage. Ajoutez la ressource au tableau **Render Resources** de votre fichier `.render` et utilisez le nom qui lui est attribué avec `render.set_render_target()`, comme dans l'exemple ci-dessus.

Vous pouvez aussi créer une cible dans la fonction `init()` de votre script de rendu. Placez `sample_count` dans la table de paramètres extérieure, à côté des tampons attachés :

```lua
self.offscreen = render.render_target({
    sample_count = 4,
    [graphics.BUFFER_TYPE_COLOR0_BIT] = {
        format = graphics.TEXTURE_FORMAT_RGBA,
        width = 1024,
        height = 1024,
        min_filter = graphics.TEXTURE_FILTER_LINEAR,
        mag_filter = graphics.TEXTURE_FILTER_LINEAR,
        u_wrap = graphics.TEXTURE_WRAP_CLAMP_TO_EDGE,
        v_wrap = graphics.TEXTURE_WRAP_CLAMP_TO_EDGE,
    },
})
self.scene_predicate = render.predicate({"scene"})
self.present_predicate = render.predicate({"present"})
```

Cet exemple utilise une cible contenant uniquement un tampon attaché de couleur. Tous les tampons attachés de couleur, de profondeur et de stencil d'une cible partagent son nombre d'échantillons. Ajoutez un tampon attaché de profondeur et l'état habituel du test de profondeur si la passe nécessite ce test.

Pour l'extrait de `update()` suivant, attribuez le tag `scene` aux matériaux de la scène et le tag `present` au matériau d'un quadrilatère plein écran. Le matériau du quadrilatère doit échantillonner l'unité de texture `0`. Définissez la vue et la projection appropriées pour chaque passe :

```lua
render.set_render_target(self.offscreen)
render.set_viewport(0, 0, 1024, 1024)
render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = vmath.vector4(0, 0, 0, 1)})
-- Set the scene view and projection here.
render.draw(self.scene_predicate)

render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.set_viewport(0, 0, render.get_window_width(), render.get_window_height())
-- Set the full-screen quad view and projection here.
render.enable_texture(0, self.offscreen, graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.present_predicate)
render.disable_texture(0)
```

Changer de cible termine la passe et résout automatiquement ses tampons de couleur attachés multi-échantillonnés. `render.enable_texture()` lie la texture de couleur résolue ; le quadrilatère utilise donc un échantillonneur de texture ordinaire. Aucune commande de résolution distincte n'est nécessaire.

Le nombre d'échantillons demandé vaut `1` par défaut et doit être un entier positif. Les moteurs de rendu ramènent les demandes non prises en charge à un nombre pris en charge qui est une puissance de deux, avec un repli sur `1` si nécessaire, et consignent un avertissement lorsque ce nombre change. Un nombre d'échantillons plus élevé augmente la mémoire nécessaire aux tampons attachés.

Lorsque vous utilisez une ressource de cible de rendu, inspectez son nombre effectif depuis un `.script` d'objet de jeu avec `resource.get_render_target_info()`. Par exemple, après avoir ajouté `/render/offscreen.render_target` à **Render Resources** :

```lua
function init(self)
    local info = resource.get_render_target_info("/render/offscreen.render_targetc")
    print("Render target sample count:", info.sample_count)
end
```

Utilisez ce nombre effectif pour vérifier la prise en charge sur l'appareil au lieu de supposer que le nombre demandé était disponible. Consultez [`render.render_target()`](/ref/beta/render/#render.render_target:parameters) et [`resource.get_render_target_info()`](/ref/beta/resource/#resource.get_render_target_info:path) pour les tables complètes de paramètres et de résultats.

## Identifiants de texture {#texture-handles}

Dans Defold, les textures sont représentées en interne par un identifiant opaque (handle), qui correspond essentiellement à un nombre devant identifier de manière unique un objet texture partout dans le moteur. Vous pouvez ainsi relier le monde des objets de jeu à celui du rendu en transmettant ces identifiants entre le système de rendu et un script d'objet de jeu. Par exemple, un script attaché à un objet de jeu peut créer une texture dynamique et l'envoyer au système de rendu pour qu'elle soit utilisée comme texture globale dans une commande de dessin.

Dans un fichier `.script` :

```lua
local my_texture_resource = resource.create_texture("/my_texture.texture", tparams)
-- note: my_texture_resource is a hash to the resource path, which can't be used as a handle!
local my_texture_handle = resource.get_texture_info(my_texture_resource)
-- my_texture_handle contains information about the texture, such as width, height and so on
-- it does also contain the handle, which is what we are after
msg.post("@render:", "set_texture", { handle = my_texture_handle.handle })
```

Dans un fichier `.render_script` :

```lua
function on_message(self, message_id, message)
    if message_id == hash("set_texture") then
        self.my_texture = message.handle
    end
end

function update(self)
    -- bind the custom texture to the draw state
    render.enable_texture(0, self.my_texture)
    -- do drawing..
end
```

::: sidenote
Il n'existe actuellement aucun moyen de changer la texture vers laquelle une ressource doit pointer ; vous pouvez uniquement utiliser des identifiants bruts de cette manière dans le script de rendu.
:::

## API graphiques prises en charge {#supported-graphics-apis}
L'API des scripts de rendu de Defold traduit les opérations de rendu vers les API graphiques suivantes :

:[Graphics API](../shared/graphics-api.md)


## Messages système {#system-messages}

`"set_view_projection"`
: Ce message est envoyé par les composants caméra qui ont obtenu le focus de la caméra.

`"window_resized"`
: Le moteur envoie ce message lorsque la taille de la fenêtre change. Vous pouvez écouter ce message pour modifier le rendu lorsque la taille de la fenêtre cible change. Sur ordinateur, cela signifie que la fenêtre du jeu a été redimensionnée ; sur les appareils mobiles, ce message est envoyé à chaque changement d'orientation.

```lua
local MSG_WINDOW_RESIZED =      hash("window_resized")

function on_message(self, message_id, message)
  if message_id == MSG_WINDOW_RESIZED then
    -- The window was resized. message.width and message.height contain the new dimensions.
    ...
  end
end
```

`"draw_line"`
: Dessine une ligne de débogage. Utilisez-la pour visualiser des `ray_casts`, des vecteurs et d'autres éléments. Les lignes sont dessinées par l'appel à `render.draw_debug3d()`.

```lua
-- draw a white line
local p1 = vmath.vector3(0, 0, 0)
local p2 = vmath.vector3(1000, 1000, 0)
local col = vmath.vector4(1, 1, 1, 1)
msg.post("@render:", "draw_line", { start_point = p1, end_point = p2, color = col } )  
```

`"draw_text"`
: Dessine du texte de débogage. Utilisez-le pour afficher des informations de débogage. Le texte est dessiné avec la police intégrée `always_on_top.font`. La police système possède un matériau portant l'étiquette `debug_text` et est dessinée avec les autres textes dans le script de rendu par défaut.

```lua
-- draw a text message
local pos = vmath.vector3(500, 500, 0)
msg.post("@render:", "draw_text", { text = "Hello world!", position = pos })  
```

Le profileur visuel, accessible via le message `"toggle_profile"` envoyé au socket `@system`, ne fait pas partie du système de rendu programmable. Il est dessiné séparément de votre script de rendu.


## Appels de dessin et regroupement par lots {#draw-calls-and-batching}

Un appel de dessin désigne le processus de configuration du GPU pour dessiner un objet à l'écran à l'aide d'une texture et d'un matériau, avec éventuellement des paramètres supplémentaires. Ce processus consomme généralement beaucoup de ressources, et il est recommandé de réduire au minimum le nombre d'appels de dessin. Vous pouvez mesurer le nombre d'appels de dessin et le temps nécessaire à leur rendu à l'aide du [profileur intégré](/manuals/profiling/).

Defold tente de regrouper les opérations de rendu par lots pour réduire le nombre d'appels de dessin selon un ensemble de règles définies ci-dessous. Ces règles diffèrent entre les composants GUI et tous les autres types de composants.


### Règles de regroupement pour les composants autres que GUI {#batch-rules-for-non-gui-components}

Chaque appel à `render.draw()` contrôle le tri des entrées correspondantes ordonnées dans l'espace du monde. L'ordre par défaut est `render.SORT_BACK_TO_FRONT` ; utilisez `render.SORT_FRONT_TO_BACK` pour dessiner du plus proche au plus éloigné, ou `render.SORT_NONE` pour conserver l'ordre d'insertion :

```lua
render.draw(self.opaque_predicate, {
    sort_order = render.SORT_FRONT_TO_BACK
})
render.draw(self.transparent_predicate, {
    sort_order = render.SORT_BACK_TO_FRONT
})
```

L'ordre choisi détermine les entrées adjacentes et peut donc affecter le regroupement par lots. Dans cette liste ordonnée, chaque objet est regroupé dans le même appel de dessin que l'objet précédent si les conditions suivantes sont réunies :

* Appartient au même proxy de collection (collection proxy)
* Est du même type de composant (sprite, effets de particules, tilemap, etc.)
* Utilise la même texture (atlas ou source de tuiles)
* Possède le même matériau
* Possède les mêmes constantes de shader (comme la teinte)

Cela signifie que, si deux composants sprite du même proxy de collection sont adjacents après le tri choisi et utilisent la même texture, le même matériau et les mêmes constantes, ils sont regroupés dans le même appel de dessin.


### Règles de regroupement pour les composants GUI {#batch-rules-for-gui-components}

Le rendu des nœuds d'un composant GUI se fait du haut vers le bas de la liste des nœuds. Chaque nœud de la liste est regroupé dans le même appel de dessin que le nœud précédent si les conditions suivantes sont réunies :

* Est du même type (boîte, texte, disque, etc.)
* Utilise la même texture (atlas ou source de tuiles)
* Possède le même mode de mélange.
* Possède la même police (uniquement pour les nœuds de texte)
* Possède les mêmes paramètres de pochoir

::: sidenote
Le rendu des nœuds se fait par composant. Cela signifie que les nœuds de différents composants GUI ne sont pas regroupés par lots.
:::

La possibilité d'organiser les nœuds en hiérarchies permet de les regrouper facilement en unités gérables. Toutefois, les hiérarchies peuvent empêcher le rendu par lots si vous mélangez différents types de nœuds. Les couches GUI permettent de regrouper plus efficacement les nœuds GUI par lots tout en conservant leur hiérarchie. Pour en savoir plus sur les couches GUI et leur effet sur les appels de dessin, consultez le [manuel de l'interface graphique](/manuals/gui#layers-and-draw-calls).
