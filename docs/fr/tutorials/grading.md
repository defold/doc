---
title: Tutoriel sur un shader d'étalonnage des couleurs
brief: Dans ce tutoriel, vous allez créer un effet de post-traitement plein écran dans Defold.
---

# Tutoriel sur l'étalonnage des couleurs {#grading-tutorial}

Dans ce tutoriel, nous allons créer un effet de post-traitement plein écran pour l'étalonnage des couleurs. La méthode de rendu de base employée convient à de nombreux types d'effets de post-traitement, tels que le flou, les traînées, la lueur, les réglages des couleurs, etc.

Nous supposons que vous savez utiliser l'éditeur Defold et que vous avez une compréhension de base des shaders GL et du pipeline de rendu de Defold. Si vous avez besoin d'approfondir ces sujets, consultez [notre manuel sur les shaders](/manuals/shader/) et le [manuel sur le rendu](/manuals/render/).

## Cibles de rendu {#render-targets}

Avec le script de rendu par défaut, chaque composant (component) visuel (sprite, tilemap, effet de particules, interface graphique, etc.) est rendu directement dans le *tampon d'image* de la carte graphique. Le matériel fait ensuite apparaître les éléments graphiques à l'écran. Le dessin des pixels d'un composant est effectué par un *programme de shader* GL. Defold fournit un programme de shader par défaut pour chaque type de composant, qui dessine les données des pixels à l'écran sans les modifier. En général, c'est le comportement souhaité : vos images doivent apparaître à l'écran telles qu'elles ont été conçues.

Vous pouvez remplacer le programme de shader d'un composant par un autre qui modifie les données des pixels ou crée des couleurs de pixels entièrement nouvelles par programmation. Le [tutoriel Shadertoy](/tutorials/shadertoy) vous apprend à le faire.

Supposons maintenant que vous souhaitiez afficher tout votre jeu en noir et blanc. Une solution possible consiste à modifier le programme de shader de chaque type de composant pour que chaque shader désature les couleurs des pixels. Actuellement, Defold fournit six matériaux intégrés et six paires de programmes de shaders de sommets et de fragments, ce qui représente donc un travail assez conséquent. De plus, toute modification ou tout ajout d'effet ultérieur doit être effectué dans chaque programme de shader.

Une approche beaucoup plus souple consiste à effectuer le rendu en deux étapes distinctes :

![Cible de rendu](images/grading/render_target.png)

1. Dessinez tous les composants comme d'habitude, mais dans un tampon hors écran au lieu du tampon d'image habituel. Pour cela, vous dessinez dans ce que l'on appelle une *cible de rendu*.
2. Dessinez un polygone carré dans le tampon d'image et utilisez les données des pixels stockées dans la cible de rendu comme source de texture du polygone. Assurez-vous également que le polygone carré est étiré pour couvrir tout l'écran.

Cette méthode nous permet de lire les données visuelles obtenues et de les modifier avant leur affichage à l'écran. En ajoutant des programmes de shaders à l'étape 2 ci-dessus, nous pouvons facilement obtenir des effets plein écran. Voyons comment mettre cela en place dans Defold.

## Mise en place d'un moteur de rendu personnalisé {#setting-up-a-custom-renderer}

Nous devons modifier le script de rendu intégré et ajouter la nouvelle fonctionnalité de rendu. Le script de rendu par défaut est un bon point de départ ; commencez donc par le copier :

1. Copiez */builtins/render/default.render_script* : dans la vue *Asset*, faites un clic droit sur *default.render_script*, sélectionnez <kbd>Copy</kbd>, puis faites un clic droit sur *main* et sélectionnez <kbd>Paste</kbd>. Faites un clic droit sur la copie, sélectionnez <kbd>Rename...</kbd> et donnez-lui un nom adapté, par exemple « grade.render_script ».
2. Créez un nouveau fichier de rendu nommé */main/grade.render* en faisant un clic droit sur *main* dans la vue *Asset* et en sélectionnant <kbd>New ▸ Render</kbd>.
3. Ouvrez *grade.render* et définissez sa propriété *Script* sur « /main/grade.render_script ».

   ![grade.render](images/grading/grade_render.png)

4. Ouvrez *game.project* et définissez *Render* sur « /main/grade.render ».

   ![game.project](images/grading/game_project.png)

Le jeu est maintenant configuré pour fonctionner avec un nouveau pipeline de rendu que nous pouvons modifier. Pour vérifier que le moteur utilise notre copie du script de rendu, lancez votre jeu, apportez au script de rendu une modification qui produira un résultat visible, puis rechargez le script. Par exemple, vous pouvez désactiver le dessin des tuiles et des sprites, puis appuyer sur <kbd>⌘ + R</kbd> pour recharger à chaud le script de rendu « défectueux » dans le jeu en cours d'exécution :

```lua
...

render.set_projection(vmath.matrix4_orthographic(0, render.get_width(), 0, render.get_height(), -1, 1))

-- render.draw(self.tile_pred) -- <1>
render.draw(self.particle_pred)
render.draw_debug3d()

...
```
1. Commentez le dessin du prédicat « tile », qui inclut tous les sprites et toutes les tuiles. Cette ligne de code se trouve vers la ligne 33 du fichier de script de rendu.

Si les sprites et les tuiles disparaissent lors de ce simple test, vous savez que le jeu exécute votre script de rendu. Si tout fonctionne comme prévu, vous pouvez annuler la modification du script de rendu.

## Dessin dans une cible hors écran {#drawing-to-an-off-screen-target}

Modifions maintenant le script de rendu pour qu'il dessine dans la cible de rendu hors écran au lieu du tampon d'image. Nous devons d'abord créer la cible de rendu :

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})

    self.clear_color = vmath.vector4(0, 0, 0, 1)
    self.clear_color.x = sys.get_config_number("render.clear_color_red", 0)
    self.clear_color.y = sys.get_config_number("render.clear_color_green", 0)
    self.clear_color.z = sys.get_config_number("render.clear_color_blue", 0)
    self.clear_color.w = sys.get_config_number("render.clear_color_alpha", 1)

    self.view = vmath.matrix4()

    local color_params = { format = graphics.TEXTURE_FORMAT_RGBA,
                       width = render.get_width(),
                       height = render.get_height() } -- <1>
    local target_params = {[graphics.BUFFER_TYPE_COLOR0_BIT] = color_params }

    self.target = render.render_target("original", target_params) -- <2>
end
```
1. Définissez les paramètres du tampon de couleur de la cible de rendu. Nous utilisons la résolution cible du jeu.
2. Créez la cible de rendu avec les paramètres du tampon de couleur.

Il nous suffit maintenant d'encadrer le code de rendu d'origine par des appels à `render.set_render_target()`, comme ceci :

```lua
function update(self)
  render.set_render_target(self.target) -- <1>

  render.set_depth_mask(true)
  render.set_stencil_mask(0xff)
  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color, [graphics.BUFFER_TYPE_DEPTH_BIT] = 1, [graphics.BUFFER_TYPE_STENCIL_BIT] = 0})

  render.set_viewport(0, 0, render.get_width(), render.get_height()) -- <2>
  render.set_view(self.view)
  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT) -- <3>
end
```
1. Activez la cible de rendu. Désormais, chaque appel à `render.draw()` dessinera dans les tampons de notre cible de rendu hors écran.
2. Tout le code de dessin d'origine dans `update()` reste inchangé, à l'exception de la fenêtre d'affichage, qui est définie à la résolution de la cible de rendu.
3. À ce stade, tous les éléments graphiques du jeu ont été dessinés dans la cible de rendu. Il est donc temps de la désactiver en sélectionnant la cible de rendu par défaut.

C'est tout ce que nous avons à faire. Si vous lancez le jeu maintenant, il dessinera tout dans la cible de rendu. Mais comme nous ne dessinons plus rien dans le tampon d'image, nous ne verrons qu'un écran noir.

## Un élément pour remplir l'écran {#something-to-fill-the-screen-with}

Pour dessiner à l'écran les pixels du tampon de couleur de la cible de rendu, nous devons mettre en place un élément auquel nous pourrons appliquer les données des pixels comme texture. Pour cela, nous allons utiliser un modèle 3D plat et carré.

1. Ouvrez *`main.collection`* et créez un nouvel objet de jeu (game object) nommé « `grade` ».
2. Ajoutez un composant Model à l'objet de jeu « `grade` ».
3. Définissez la propriété *Mesh* du composant modèle sur le fichier *`quad.gltf`* situé dans `builtins/assets/meshes`.

Laissez l'objet de jeu à l'origine, sans modifier son échelle. Plus tard, lors du rendu du quadrilatère, nous le projetterons pour qu'il remplisse tout l'écran. Mais nous avons d'abord besoin d'un matériau et de programmes de shaders pour le quadrilatère :

1. Créez un nouveau matériau et nommez-le *`grade.material`* en faisant un clic droit sur *main* dans la vue *Asset* et en sélectionnant <kbd>New ▸ Material</kbd>.
2. Créez un programme de shader de sommets nommé *`grade.vp`* et un programme de shader de fragments nommé *`grade.fp`* en faisant un clic droit sur *main* dans la vue *Asset* et en sélectionnant <kbd>New ▸ Vertex program</kbd> et <kbd>New ▸ Fragment program</kbd>.
3. Ouvrez *grade.material* et définissez les propriétés *Vertex program* et *Fragment program* sur les nouveaux fichiers de programmes de shaders.
4. Ajoutez une *Vertex constant* nommée « `view_proj` » de type `CONSTANT_TYPE_VIEWPROJ`. Il s'agit de la matrice de vue et de projection utilisée dans le programme de sommets pour les sommets du quadrilatère.
5. Ajoutez un *Sampler* nommé « `original` ». Il servira à échantillonner les pixels du tampon de couleur de la cible de rendu hors écran.
6. Ajoutez un *Tag* nommé « `grade` ». Nous créerons dans le script de rendu un nouveau *prédicat de rendu* correspondant à cette étiquette pour dessiner le quadrilatère.

   ![grade.material](images/grading/grade_material.png)

7. Ouvrez *`main.collection`*, sélectionnez le composant modèle de l'objet de jeu « `grade` » et définissez sa propriété *Material* sur « `/main/grade.material` ».

   ![Propriétés du modèle](images/grading/model_properties.png)

8. Le programme de shader de sommets peut rester tel qu'il a été créé à partir du modèle de base :

    ```glsl
    // grade.vp
    uniform mediump mat4 view_proj;

    // positions are in world space
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
      gl_Position = view_proj * vec4(position.xyz, 1.0);
      var_texcoord0 = texcoord0;
    }
    ```

9. Dans le programme de shader de fragments, au lieu de définir directement `gl_FragColor` sur la valeur de couleur échantillonnée, effectuons une simple manipulation des couleurs. Cela sert surtout à vérifier que tout fonctionne comme prévu jusqu'ici :

    ```glsl
    // grade.fp
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;

    void main()
    {
      vec4 color = texture2D(original, var_texcoord0.xy);
      // Desaturate the color sampled from the original texture
      float grey = color.r * 0.3 + color.g * 0.59 + color.b * 0.11;
      gl_FragColor = vec4(grey, grey, grey, 1.0);
    }
    ```

Le modèle de quadrilatère est maintenant en place avec son matériau et ses shaders. Il ne nous reste plus qu'à le dessiner dans le tampon d'image de l'écran.

## Application d'une texture à partir du tampon hors écran {#texturing-with-the-off-screen-buffer}

Nous devons ajouter un prédicat de rendu au script de rendu pour pouvoir dessiner le modèle de quadrilatère. Ouvrez *`grade.render_script`* et modifiez la fonction `init()` :

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})
    self.grade_pred = render.predicate({"grade"}) -- <1>

    ...
end
```
1. Ajoutez un nouveau prédicat correspondant à l'étiquette « grade » que nous avons définie dans *`grade.material`*.

Une fois le tampon de couleur de la cible de rendu rempli dans `update()`, nous définissons une vue et une projection pour que le modèle de quadrilatère remplisse tout l'écran. Nous utilisons ensuite le tampon de couleur de la cible de rendu comme texture du quadrilatère :

```lua
function update(self)
  render.set_render_target(self.target)

  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT)

  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color}) -- <1>

  render.set_viewport(0, 0, render.get_window_width(), render.get_window_height()) -- <2>
  render.set_view(vmath.matrix4()) -- <3>
  render.set_projection(vmath.matrix4())

  render.enable_texture(0, self.target, graphics.BUFFER_TYPE_COLOR0_BIT) -- <4>
  render.draw(self.grade_pred) -- <5>
  render.disable_texture(0, self.target) -- <6>
end
```
1. Effacez le tampon d'image. Notez que l'appel précédent à `render.clear()` affecte la cible de rendu, pas le tampon d'image de l'écran.
2. Définissez la fenêtre d'affichage pour qu'elle corresponde à la taille de la fenêtre.
3. Définissez la vue sur la matrice identité. Cela signifie que la caméra se trouve à l'origine et regarde directement le long de l'axe Z. Définissez également la projection sur la matrice identité afin que le quadrilatère soit projeté à plat sur tout l'écran.
4. Affectez le tampon de couleur de la cible de rendu à l'emplacement de texture 0. L'échantillonneur « original » se trouve à l'emplacement 0 dans notre *`grade.material`*, donc le shader de fragments échantillonnera la cible de rendu.
5. Dessinez le prédicat que nous avons créé, qui correspond à tout matériau portant l'étiquette « grade ». Le modèle de quadrilatère utilise *`grade.material`*, qui définit cette étiquette : le quadrilatère sera donc dessiné.
6. Après le dessin, désactivez l'emplacement de texture 0, puisque nous avons terminé de dessiner avec celui-ci.

Lançons maintenant le jeu pour voir le résultat :

![Jeu désaturé](images/grading/desaturated_game.png)

## Étalonnage des couleurs {#color-grading}

Les couleurs s'expriment par les valeurs de trois composantes, chacune déterminant la quantité de rouge, de vert ou de bleu qui compose une couleur. L'ensemble du spectre des couleurs, du noir au blanc en passant par le rouge, le vert, le bleu, le jaune et le rose, peut être contenu dans un cube :

![Cube de couleurs](images/grading/color_cube.png)

Toute couleur pouvant être affichée à l'écran se trouve dans ce cube de couleurs. Le principe de l'étalonnage des couleurs consiste à utiliser un tel cube, mais avec des couleurs modifiées, comme *table de correspondance* 3D.

Pour chaque pixel :

1. Recherchez la position de sa couleur dans le cube de couleurs (à partir des valeurs de rouge, de vert et de bleu).
2. *Lisez* la couleur stockée à cet emplacement dans le cube étalonné.
3. Dessinez le pixel avec la couleur lue au lieu de la couleur d'origine.

Nous pouvons le faire dans notre shader de fragments :

1. Échantillonnez la valeur de couleur de chaque pixel dans le tampon hors écran.
2. Recherchez la position de la couleur du pixel échantillonné dans un cube de couleurs étalonné.
3. Définissez la couleur du fragment de sortie sur la valeur trouvée.

![Étalonnage de la cible de rendu](images/grading/render_target_grading.png)

## Représentation de la table de correspondance {#representing-the-lookup-table}

Open GL ES 2.0 ne prend pas en charge les textures 3D ; nous devons donc trouver une autre façon de représenter le cube de couleurs 3D. Une méthode courante consiste à découper le cube en tranches le long de l'axe Z (bleu) et à placer chaque tranche côte à côte dans une grille bidimensionnelle. Chacune des 16 tranches contient une grille de 16⨉16 pixels. Nous stockons cela dans une texture que nous pouvons lire dans le shader de fragments à l'aide d'un échantillonneur :

![Texture de correspondance](images/grading/lut.png)

La texture obtenue contient 16 cellules (une pour chaque intensité de bleu) et, dans chaque cellule, 16 couleurs rouges le long de l'axe X et 16 couleurs vertes le long de l'axe Y. La texture représente l'ensemble des 16 millions de couleurs de l'espace colorimétrique RVB en seulement 4096 couleurs, soit une profondeur de couleur de 4 bits à peine. Selon la plupart des critères, c'est médiocre, mais une fonctionnalité du matériel graphique GL nous permet de retrouver une très grande précision des couleurs. Voyons comment.

## Recherche des couleurs {#looking-up-colors}

Rechercher une couleur consiste à examiner la composante bleue pour déterminer dans quelle cellule choisir les valeurs de rouge et de vert. La formule permettant de trouver la cellule contenant le bon ensemble de couleurs rouge-vert est simple :

```math
cell = \left \lfloor{B \times (N - 1)} \right \rfloor
```

Ici, `B` est la valeur de la composante bleue entre 0 et 1, et `N` est le nombre total de cellules. Dans notre cas, le numéro de cellule sera dans l'intervalle `0`--`15`, la cellule `0` contenant toutes les couleurs dont la composante bleue vaut `0`, et la cellule `15` toutes celles dont la composante bleue vaut `1`.

Par exemple, la valeur RVB `(0.63, 0.83, 0.4)` se trouve dans la cellule contenant toutes les couleurs dont la valeur de bleu est `0.4`, c'est-à-dire la cellule numéro 6. Sachant cela, il est facile de trouver les coordonnées de texture finales à partir des valeurs de vert et de rouge :

![Table de correspondance](images/grading/lut_lookup.png)

Notez que nous devons considérer les valeurs de rouge et de vert `(0, 0)` comme étant au *centre* du pixel en bas à gauche et les valeurs `(1.0, 1.0)` comme étant au *centre* du pixel en haut à droite.

::: sidenote
Nous lisons à partir du centre du pixel en bas à gauche jusqu'au centre du pixel en haut à droite afin qu'aucun pixel situé à l'extérieur de la cellule actuelle n'affecte la valeur échantillonnée. Consultez les explications sur le filtrage ci-dessous.
:::

Lorsque nous échantillonnons la texture à ces coordonnées précises, nous constatons que nous nous trouvons exactement entre quatre pixels. Quelle valeur de couleur GL nous donnera-t-il pour ce point ?

![Filtrage de la table de correspondance](images/grading/lut_filtering.png)

La réponse dépend du *filtrage* que nous avons défini pour l'échantillonneur dans le matériau.

- Si le filtrage de l'échantillonneur est `NEAREST`, GL renverra la valeur de couleur du pixel le plus proche (valeur de position arrondie à l'entier inférieur). Dans le cas ci-dessus, GL renverra la valeur de couleur à la position `(0.60, 0.80)`. Pour notre texture de correspondance de 4 bits, cela signifie que nous quantifierons les valeurs de couleur en seulement 4096 couleurs au total.

- Si le filtrage de l'échantillonneur est `LINEAR`, GL renverra la valeur de couleur *interpolée*. GL mélangera les couleurs en fonction de la distance aux pixels entourant la position d'échantillonnage. Dans le cas ci-dessus, GL renverra une couleur composée de 25 % de chacun des quatre pixels entourant le point d'échantillonnage.

En utilisant le filtrage linéaire, nous éliminons ainsi la quantification des couleurs et obtenons une très bonne précision des couleurs à partir d'une table de correspondance assez petite.

## Implémentation de la recherche {#implementing-the-lookup}

Implémentons la recherche dans la texture au sein du shader de fragments :

1. Ouvrez *`grade.material`*.
2. Ajoutez un deuxième échantillonneur nommé « `lut` » (pour lookup table, table de correspondance).
3. Définissez la propriété *`Filter min`* sur `FILTER_MODE_MIN_LINEAR` et la propriété *`Filter mag`* sur `FILTER_MODE_MAG_LINEAR`.

    ![Échantillonneur de la table de correspondance](images/grading/material_lut_sampler.png)

4. Téléchargez la texture de table de correspondance suivante (*`lut16.png`*) et ajoutez-la à votre projet.

    ![Table de correspondance de 16 couleurs](images/grading/lut16.png)

5. Ouvrez *`main.collection`* et définissez la propriété de texture *`lut`* sur la texture de correspondance téléchargée.

    ![Table de correspondance du modèle de quadrilatère](images/grading/quad_lut.png)

6. Enfin, ouvrez *`grade.fp`* pour que nous puissions ajouter la prise en charge de la recherche des couleurs :

    ```glsl
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;
    uniform lowp sampler2D lut; // <1>

    #define MAXCOLOR 15.0 // <2>
    #define COLORS 16.0
    #define WIDTH 256.0
    #define HEIGHT 16.0

    void main()
    {
        vec4 px = texture2D(original, var_texcoord0.xy); // <3>

        float cell = floor(px.b * MAXCOLOR); // <4>

        float half_px_x = 0.5 / WIDTH; // <5>
        float half_px_y = 0.5 / HEIGHT;

        float x_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
        float y_offset = half_px_y + px.g * (MAXCOLOR / COLORS); // <6>

        vec2 lut_pos = vec2(cell / COLORS + x_offset, y_offset); // <7>

        vec4 graded_color = texture2D(lut, lut_pos); // <8>

        gl_FragColor = graded_color; // <9>
    }
    ```
    1. Déclarez l'échantillonneur `lut`.
    2. Constantes pour la valeur de couleur maximale (15 puisque nous commençons à 0), le nombre de couleurs par canal ainsi que la largeur et la hauteur de la texture de correspondance.
    3. Échantillonnez la couleur d'un pixel (nommée `px`) dans la texture d'origine (le tampon de couleur de la cible de rendu hors écran).
    4. Calculez dans quelle cellule lire la couleur en fonction de la valeur du canal bleu de `px`.
    5. Calculez les décalages d'un demi-pixel pour lire au centre des pixels.
    6. Calculez les décalages X et Y dans la texture à partir des valeurs de rouge et de vert de `px`.
    7. Calculez la position d'échantillonnage finale dans la texture de correspondance.
    8. Échantillonnez la couleur obtenue dans la texture de correspondance.
    9. Utilisez la couleur obtenue sur la texture du quadrilatère.

Pour le moment, la texture de la table de correspondance renvoie simplement les mêmes valeurs de couleur que celles que nous recherchons. Cela signifie que le jeu devrait être rendu avec ses couleurs d'origine :

![Aspect d'origine du monde](images/grading/world_original.png)

Jusqu'ici, tout semble correct, mais un problème se cache sous la surface. Regardez ce qui se passe lorsque nous ajoutons un sprite avec une texture de test en dégradé :

![Bandes dans le dégradé bleu](images/grading/blue_banding.png)

Le dégradé bleu présente des bandes très disgracieuses. Pourquoi ?

## Interpolation du canal bleu {#interpolating-the-blue-channel}

Le problème des bandes dans le canal bleu vient du fait que GL ne peut pas effectuer d'interpolation du canal bleu lors de la lecture de la couleur dans la texture. Nous présélectionnons une cellule particulière à lire en fonction de la valeur de bleu, et c'est tout. Par exemple, si le canal bleu contient une valeur quelconque dans l'intervalle `0.400`--`0.466`, la valeur exacte n'a pas d'importance : nous échantillonnerons toujours la couleur finale dans la cellule numéro 6, où le canal bleu vaut `0.400`.

Pour obtenir une meilleure résolution du canal bleu, nous pouvons implémenter nous-mêmes l'interpolation. Si la valeur de bleu se situe entre les valeurs de deux cellules adjacentes, nous pouvons échantillonner ces deux cellules, puis mélanger les couleurs. Par exemple, si la valeur de bleu est `0.420`, nous devrions échantillonner la cellule numéro 6 *et* la cellule numéro 7, puis mélanger les couleurs.

Nous devons donc lire deux cellules :

```math
cell_{low} = \left \lfloor{B \times (N - 1)} \right \rfloor
```

et :

```math
cell_{high} = \left \lceil{B \times (N - 1)} \right \rceil
```

Nous échantillonnons ensuite les valeurs de couleur dans chacune de ces cellules et interpolons les couleurs de façon linéaire, selon la formule :

```math
color = color_{low} \times (1 - C_{frac}) + color_{high} \times C_{frac}
```

Ici, `color`~low~ est la couleur échantillonnée dans la cellule inférieure (la plus à gauche), et `color`~high~ est la couleur échantillonnée dans la cellule supérieure (la plus à droite). La fonction GLSL `mix()` effectue cette interpolation linéaire pour nous.

La valeur `C~frac~` ci-dessus est la partie fractionnaire de la valeur du canal bleu ramenée à l'intervalle de couleurs `0`--`15` :

```math
C_{frac} = B \times (N - 1) - \left \lfloor{B \times (N - 1)} \right \rfloor
```

Là encore, une fonction GLSL nous donne la partie fractionnaire d'une valeur. Elle s'appelle `frac()`. L'implémentation finale dans le shader de fragments (*`grade.fp`*) est assez simple :

```glsl
varying mediump vec4 position;
varying mediump vec2 var_texcoord0;

uniform lowp sampler2D original;
uniform lowp sampler2D lut;

#define MAXCOLOR 15.0
#define COLORS 16.0
#define WIDTH 256.0
#define HEIGHT 16.0

void main()
{
  vec4 px = texture2D(original, var_texcoord0.xy);

    float cell = px.b * MAXCOLOR;

    float cell_l = floor(cell); // <1>
    float cell_h = ceil(cell);

    float half_px_x = 0.5 / WIDTH;
    float half_px_y = 0.5 / HEIGHT;
    float r_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
    float g_offset = half_px_y + px.g * (MAXCOLOR / COLORS);

    vec2 lut_pos_l = vec2(cell_l / COLORS + r_offset, g_offset); // <2>
    vec2 lut_pos_h = vec2(cell_h / COLORS + r_offset, g_offset);

    vec4 graded_color_l = texture2D(lut, lut_pos_l); // <3>
    vec4 graded_color_h = texture2D(lut, lut_pos_h);

    // <4>
    vec4 graded_color = mix(graded_color_l, graded_color_h, fract(cell));

    gl_FragColor = graded_color;
}
```

1. Calculez les deux cellules adjacentes à lire.
2. Calculez deux positions de recherche distinctes, une pour chaque cellule.
3. Échantillonnez les deux couleurs aux positions des cellules.
3. Mélangez les couleurs de façon linéaire selon la partie fractionnaire de `cell`, qui est la valeur de bleu mise à l'échelle.

Lancer à nouveau le jeu avec la texture de test donne maintenant de bien meilleurs résultats. Les bandes du canal bleu ont disparu :

![Dégradé bleu sans bandes](images/grading/blue_no_banding.png)

## Étalonnage de la texture de correspondance {#grading-the-lookup-texture}

Cela a demandé beaucoup de travail pour dessiner quelque chose qui ressemble exactement au monde de jeu (game world) d'origine. Mais cette configuration nous permet de faire quelque chose de vraiment intéressant. Accrochez-vous !

1. Faites une capture d'écran du jeu dans sa forme non modifiée.
2. Ouvrez la capture d'écran dans votre logiciel de retouche d'images préféré.
3. Appliquez autant de réglages des couleurs que vous le souhaitez (luminosité, contraste, courbes de couleur, balance des blancs, exposition, etc.).

![Monde dans Affinity](images/grading/world_graded_affinity.png)

4. Appliquez les mêmes réglages des couleurs au fichier de texture de la table de correspondance (*`lut16.png`*).
5. Enregistrez le fichier de texture de la table de correspondance dont les couleurs ont été ajustées.
6. Remplacez la texture *`lut16.png`* utilisée dans votre projet Defold par celle dont les couleurs ont été ajustées.
7. Lancez le jeu !

![Monde étalonné](images/grading/world_graded.png)

Quel bonheur !
