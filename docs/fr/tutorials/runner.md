---
title: Tutoriel de jeu de course sans fin
brief: Dans ce tutoriel, vous partez d'un projet vide pour créer un jeu de course complet avec un personnage animé, des collisions physiques, des objets à ramasser et un score.
---

# Tutoriel de jeu de course {#runner-tutorial}

Dans ce tutoriel, nous partons d'un projet vide pour créer un jeu de course complet avec un personnage animé, des collisions physiques, des objets à ramasser et un score.

Il y a beaucoup à assimiler lorsque l'on découvre un nouveau moteur de jeu. Nous avons donc créé ce tutoriel pour vous aider à démarrer. Assez complet, il vous accompagne dans la découverte du fonctionnement du moteur et de l'éditeur. Nous supposons que vous avez quelques notions de programmation.

Si vous avez besoin d'une introduction à la programmation Lua, consultez notre [manuel sur Lua dans Defold](/manuals/lua).

Si ce tutoriel vous semble un peu trop chargé pour commencer, consultez notre [page de tutoriels](//www.defold.com/tutorials), qui propose une sélection de tutoriels de différentes difficultés.

Si vous préférez les tutoriels vidéo, consultez [la version vidéo sur Youtube](https://www.youtube.com/playlist?list=PLXsXu5srjNlxtYPQ_YJQSxJG2AN9OVS5b).

Nous utilisons des ressources de jeu provenant de deux autres tutoriels, avec quelques petites modifications. Ce tutoriel est divisé en plusieurs étapes, chacune nous rapprochant sensiblement du jeu final.

Au terme de ce tutoriel, vous aurez un jeu dans lequel vous contrôlez un héros qui court dans un environnement, ramasse des pièces et évite des obstacles. Le héros court à une vitesse fixe et le joueur contrôle uniquement ses sauts, en appuyant sur un seul bouton (ou en touchant l'écran sur un appareil mobile). Le niveau se compose d'une succession infinie de plateformes sur lesquelles sauter et de pièces à ramasser.

Si vous êtes bloqué à un moment quelconque de ce tutoriel ou lors de la création de votre jeu, n'hésitez pas à nous demander de l'aide sur le [forum Defold](//forum.defold.com). Vous pouvez y discuter de Defold, demander de l'aide à l'équipe Defold, découvrir comment d'autres développeurs de jeux ont résolu leurs problèmes et trouver de nouvelles sources d'inspiration. Lancez-vous dès maintenant.

::: sidenote
Tout au long du tutoriel, les descriptions détaillées de concepts et de certaines opérations sont présentées comme ce paragraphe. Si ces sections vous semblent trop détaillées, vous pouvez les passer.
:::

Commençons donc. Nous espérons que vous prendrez beaucoup de plaisir à suivre ce tutoriel et qu'il vous aidera à démarrer avec Defold.

> Téléchargez les ressources de ce tutoriel [ici](https://github.com/defold/sample-runner/tree/main/def-runner).

## Étape 1 - Installation et configuration {#step-1-installation-and-setup}

La première étape consiste à [télécharger les fichiers suivants](https://github.com/defold/sample-runner/tree/main/def-runner).

Si vous n'avez pas encore téléchargé et installé l'éditeur Defold, c'est le moment de le faire :

:[install](../shared/install.md)

Une fois l'éditeur installé et lancé, il est temps de créer un projet et de le préparer. Créez un [nouveau projet](/manuals/project-setup/#creating-a-new-project) à partir du modèle "Empty Project".

::: sidenote
Ce tutoriel utilise les fonctionnalités Spine de l'[extension Spine](https://github.com/defold/extension-spine). Ajoutez l'extension à la section des dépendances de *game.project*.
:::

## L'éditeur {#the-editor}

Au premier démarrage, l'éditeur s'affiche vide, sans projet ouvert. Choisissez donc <kbd>Open Project</kbd> dans le menu et sélectionnez le projet que vous venez de créer. Il vous sera également demandé de créer une « branche » pour le projet.

Le panneau *Assets pane* affiche maintenant tous les fichiers du projet. Si vous double-cliquez sur le fichier "main/main.collection", il s'ouvre dans la vue de l'éditeur au centre :

![Vue d'ensemble de l'éditeur](images/runner/1/editor2_overview.png)

L'éditeur se compose des principales zones suivantes :

Assets pane
: Cette vue affiche tous les fichiers de votre projet. Chaque type de fichier possède sa propre icône. Double-cliquez sur un fichier pour l'ouvrir dans l'éditeur correspondant à son type. Le dossier spécial *builtins*, en lecture seule, est commun à tous les projets et contient des éléments utiles, notamment un script de rendu par défaut, une police et des matériaux pour le rendu de différents types de composant (component).

Vue principale de l'éditeur
: Cette vue affiche un éditeur adapté au type de fichier que vous modifiez. Le plus couramment utilisé est l'éditeur de scène que vous voyez ici. Chaque fichier ouvert apparaît dans un onglet distinct.

Changed Files
: Contient les fichiers ajoutés, modifiés, renommés ou supprimés localement par rapport au commit Git actuel. Vous pouvez afficher les différences d'un fichier texte modifié ou renommé à la fois ; vous pouvez aussi annuler les modifications locales sélectionnées ici. Utilisez un client Git externe ou la ligne de commande pour synchroniser le projet avec un dépôt distant.

Outline
: Le contenu du fichier en cours de modification, sous forme hiérarchique. Vous pouvez ajouter, supprimer, modifier et sélectionner des objets et des composants dans cette vue.

Properties
: Les propriétés définies sur l'objet ou le composant actuellement sélectionné.

Console
: Lorsque le jeu est en cours d'exécution, cette vue recueille la sortie du moteur de jeu (journaux, erreurs, informations de débogage, etc.), ainsi que les messages de débogage personnalisés `print()` et `pprint()` de vos scripts. Si votre application ou votre jeu ne démarre pas, la console est le premier endroit à vérifier. Derrière la console se trouvent des onglets affichant des informations sur les erreurs, ainsi qu'un éditeur de courbes utilisé pour créer des effets de particules.

## Exécuter le jeu {#running-the-game}

Le modèle de projet "Empty" est effectivement complètement vide. Sélectionnez tout de même <kbd>Project ▸ Build</kbd> pour compiler le projet et lancer le jeu.

![Compilation](images/runner/1/build_and_launch.png)

Un écran noir n'a peut-être rien de passionnant, mais il s'agit bien d'une application de jeu Defold en cours d'exécution, et nous pouvons facilement la transformer en quelque chose de plus intéressant. Faisons-le.

::: sidenote
L'éditeur Defold travaille sur des fichiers. En double-cliquant sur un fichier dans le panneau *Assets pane*, vous l'ouvrez dans un éditeur adapté. Vous pouvez alors travailler sur son contenu.

Lorsque vous avez terminé de modifier un fichier, vous devez l'enregistrer. Sélectionnez <kbd>File ▸ Save</kbd> dans le menu principal. L'éditeur vous le rappelle en ajoutant un astérisque '\*' au nom du fichier dans l'onglet de chaque fichier qui contient des modifications non enregistrées.

![Fichier contenant des modifications non enregistrées](images/runner/1/file_changed.png)
:::

## Configurer le projet {#setting-up-the-project}

Avant de commencer, définissons quelques paramètres du projet. Ouvrez la ressource *game.project* dans `Assets Pane` et faites défiler jusqu'à la section Display. Définissez les propriétés `width` et `height` du projet sur `1280` et `720` respectivement.

Vous devez également ajouter l'extension Spine au projet pour que nous puissions animer le héros. Ajoutez une version de l'extension Spine compatible avec la version de l'éditeur Defold que vous avez installée. Les versions disponibles de Spine sont indiquées ici :

[https://github.com/defold/extension-spine/releases](https://github.com/defold/extension-spine/releases)

Faites un clic droit sur le lien vers le fichier zip de la version que vous souhaitez utiliser :

![Clic droit et copie du lien vers la version](images/runner/extension-spine-releases.png)

Ajoutez le lien vers cette version à votre liste de [dépendances de game.project](/manuals/libraries/#setting-up-library-dependencies). Une fois l'extension Spine ajoutée, vous devez également redémarrer l'éditeur pour activer l'intégration à l'éditeur incluse dans l'extension Spine.


## Étape 2 - Créer le sol {#step-2-creating-the-ground}

Faisons nos premiers pas en créant un terrain pour notre personnage, ou plus exactement une portion de sol qui défile. Nous allons procéder en quelques étapes.

1. Importez les images dans le projet en faisant glisser les fichiers "ground01.png" et "ground02.png" (du sous-dossier "level-images" du lot de ressources) vers un emplacement adapté dans le projet, par exemple le dossier "images" à l'intérieur du dossier "main".
2. Créez un fichier *Atlas* pour contenir les textures du sol (faites un clic droit sur un dossier adapté, par exemple le dossier *main*, dans le panneau *Assets pane* et sélectionnez <kbd>New ▸ Atlas File</kbd>). Nommez le fichier d'atlas *level.atlas*.

  ::: sidenote
  Un *atlas* est un fichier qui réunit plusieurs images distinctes dans un seul fichier image plus grand. Cela permet d'économiser de l'espace et d'améliorer les performances. Pour en savoir plus sur les atlas et les autres fonctionnalités graphiques 2D, consultez la [documentation sur les graphismes 2D](/manuals/2dgraphics).
  :::

3. Ajoutez les images du sol au nouvel atlas en faisant un clic droit sur sa racine dans *Outline*, puis en sélectionnant <kbd>Add Images</kbd>. Sélectionnez les images importées et cliquez sur *OK*. Chaque image de l'atlas est désormais accessible sous forme d'animation à une seule image (image fixe), utilisable dans les sprites, les effets de particules et d'autres éléments visuels. Enregistrez le fichier.

  ![Création d'un atlas](images/runner/1/new_atlas.png)

  ![Ajout d'images à l'atlas](images/runner/1/add_images_to_atlas.png)

  ::: sidenote
  *Pourquoi cela ne fonctionne-t-il pas !?* L'oubli d'enregistrer est un problème fréquent lorsque l'on débute avec Defold ! Après avoir ajouté des images à un atlas, vous devez enregistrer le fichier pour pouvoir accéder à ces images.
  :::

4. Créez un fichier de collection *ground.collection* pour le sol et ajoutez-y sept objets de jeu (game objects) (faites un clic droit sur la racine de la collection dans la vue *Outline* et sélectionnez <kbd>Add Game Object</kbd>). Nommez les objets "ground0", "ground1", "ground2", etc., en modifiant la propriété *Id* dans la vue *Properties*. Notez que Defold attribue automatiquement un identifiant unique aux nouveaux objets de jeu.

5. Dans chaque objet, ajoutez un composant sprite (faites un clic droit sur l'objet de jeu dans la vue *Outline* et sélectionnez <kbd>Add Component</kbd>, puis sélectionnez *Sprite* et cliquez sur *OK*), définissez la propriété *Image* du composant sprite sur l'atlas que vous venez de créer et choisissez l'une des deux images du sol comme animation par défaut du sprite. Définissez la position X du _composant sprite_ (et non de l'objet de jeu) sur 190 et sa position Y sur 40. Comme l'image mesure 380 pixels de large et que nous la décalons horizontalement de la moitié de cette distance, le pivot de l'objet de jeu se trouve sur le bord gauche de l'image du sprite.

  ![Création de la collection du sol](images/runner/1/ground_collection.png)

6. Les graphismes que nous utilisons sont un peu trop grands : réduisez donc chaque objet de jeu à 60 % (échelle de 0.6 en X et en Y, ce qui donne des portions de sol de 228 pixels de large).

  ![Mise à l'échelle du sol](images/runner/1/scale_ground.png)

7. Alignez tous les _objets de jeu_. Définissez les positions X des _objets de jeu_ (et non des composants sprite) sur 0, 228, 456, 684, 912, 1140 et 1368 (des multiples de la largeur de 228 pixels).

  ::: sidenote
  Le plus simple est probablement de créer un objet de jeu complet avec un composant sprite, de régler son échelle, puis de le copier. Sélectionnez-le dans la vue *Outline*, puis sélectionnez <kbd>Edit ▸ Copy</kbd> et ensuite <kbd>Edit ▸ Paste</kbd>.

  Si vous souhaitez des tuiles plus grandes ou plus petites, il suffit de modifier leur échelle. Vous devrez toutefois aussi modifier les positions X de tous les objets de jeu du sol pour qu'elles soient des multiples de la nouvelle largeur.
  :::

8. Enregistrez le fichier, puis ajoutez *ground.collection* au fichier *main.collection* : double-cliquez d'abord sur *main.collection*, puis faites un clic droit sur l'objet racine dans la vue *Outline* et sélectionnez <kbd>Add Collection From File</kbd>. Dans la boîte de dialogue, sélectionnez *ground.collection* et cliquez sur *OK*. Veillez à placer *ground.collection* à la position 0, 0, 0, sinon elle sera décalée visuellement. Enregistrez le fichier.

9. Lancez le jeu (<kbd>Project ▸ Build</kbd>) pour vérifier que tout est en place.

  ![Sol immobile](images/runner/1/still_ground.png)

Vous vous demandez peut-être à présent ce que sont exactement tous ces éléments que nous avons créés. Prenons donc un instant pour examiner les éléments de base de tout projet Defold :

Objets de jeu
: Ce sont les éléments qui existent dans le jeu en cours d'exécution. Chaque objet de jeu possède une position dans l'espace 3D, une rotation et une échelle. Il n'est pas nécessairement visible. Un objet de jeu contient autant de _composants_ que nécessaire pour lui apporter des fonctionnalités comme les graphismes (sprites, tilemaps, modèles, modèles Spine et effets de particules), les sons, la physique, les factories (pour créer des instances), etc. Des _composants script_ Lua peuvent également lui être ajoutés pour définir son comportement. Chaque objet de jeu de vos jeux possède un *identifiant*, dont vous avez besoin pour communiquer avec lui par échange de messages.

Collections
: Les collections n'existent pas par elles-mêmes dans un jeu en cours d'exécution, mais servent à donner des noms statiques aux objets de jeu tout en permettant plusieurs instances d'un même objet de jeu. En pratique, elles servent de conteneurs pour les objets de jeu et d'autres collections. Vous pouvez utiliser les collections comme des prototypes (également appelés « prefabs » ou « blueprints » dans d'autres moteurs) de hiérarchies complexes d'objets de jeu et de collections. Au démarrage, le moteur charge une collection principale et donne vie à tout ce que vous y avez placé. Par défaut, il s'agit du fichier *main.collection* dans le dossier *main* de votre projet, mais vous pouvez le changer dans les paramètres du projet.

Pour le moment, ces descriptions devraient suffire. Vous trouverez toutefois une présentation bien plus complète dans le [manuel des éléments de base](/manuals/building-blocks). Il est conseillé de consulter ce manuel plus tard pour mieux comprendre le fonctionnement de Defold.

## Étape 3 - Faire défiler le sol {#step-3-making-the-ground-move}

Maintenant que toutes les portions de sol sont en place, il est assez simple de les mettre en mouvement. Le principe est le suivant : déplacer les portions de droite à gauche et, lorsqu'une portion atteint le bord gauche à l'extérieur de l'écran, la déplacer tout à droite. Un script Lua est nécessaire pour déplacer tous ces objets de jeu. Créons-en donc un :

1. Faites un clic droit sur le dossier *main* dans le panneau *Assets pane* et sélectionnez <kbd>New ▸ Script File</kbd>. Nommez le nouveau fichier *ground.script*.
2. Double-cliquez sur le nouveau fichier pour ouvrir l'éditeur de scripts Lua.
3. Supprimez le contenu par défaut du fichier, copiez-y le code Lua suivant, puis enregistrez le fichier.

```lua
-- ground.script
local pieces = { "ground0", "ground1", "ground2", "ground3",
                    "ground4", "ground5", "ground6" } -- <1>

function init(self) -- <2>
    self.speed = 360  -- Speed in pixels/s
end

function update(self, dt) -- <3>
    for i, p in ipairs(pieces) do -- <4>
        local pos = go.get_position(p)
        if pos.x <= -228 then -- <5>
            pos.x = 1368 + (pos.x + 228)
        end
        pos.x = pos.x - self.speed * dt -- <6>
        go.set_position(pos, p) -- <7>
    end
end
```
1. Stockez les identifiants des objets de jeu du sol dans une table Lua afin de pouvoir les parcourir.
2. La fonction `init()` est appelée lorsque l'objet de jeu prend vie dans le jeu. Nous initialisons une variable membre propre à l'objet qui contient la vitesse du sol.
3. `update()` est appelée une fois par image, généralement 60 fois par seconde. `dt` contient le nombre de secondes écoulées depuis le dernier appel.
4. Parcourez tous les objets de jeu du sol.
5. Stockez la position actuelle dans une variable locale, puis, si l'objet actuel se trouve sur le bord gauche, déplacez-le vers le bord droit.
6. Diminuez la position X actuelle selon la vitesse définie. Multipliez par `dt` pour obtenir une vitesse en pixels/s indépendante de la fréquence d'images.
7. Mettez à jour la position de l'objet avec la nouvelle vitesse.

::: sidenote
Defold est un cœur de moteur rapide qui gère vos données et vos objets de jeu. Toute la logique et tous les comportements nécessaires à votre jeu sont créés en langage Lua. Lua est un langage de programmation rapide et léger, particulièrement adapté à l'écriture de la logique des jeux. D'excellentes ressources permettent d'apprendre ce langage, comme le livre [Programming in Lua](http://www.lua.org/pil/) et le [manuel de référence officiel de Lua](http://www.lua.org/manual/5.3/).

Defold ajoute un ensemble d'API à Lua, ainsi qu'un système d'_échange de messages_ qui vous permet de programmer les communications entre objets de jeu. Consultez le [manuel sur l'échange de messages](/manuals/message-passing) pour en savoir plus sur son fonctionnement.
:::

::: sidenote
Vous pouvez afficher ou masquer les sections Assets Pane, Console et Outline de l'éditeur à l'aide des touches <kbd>F6</kbd>, <kbd>F7</kbd> et <kbd>F8</kbd> respectivement.
:::

Maintenant que nous avons un fichier de script, nous devons ajouter une référence à ce fichier dans un composant d'un objet de jeu. Le script sera ainsi exécuté dans le cadre du cycle de vie de l'objet de jeu. Pour cela, nous créons un nouvel objet de jeu dans *ground.collection* et lui ajoutons un composant *Script* qui fait référence au fichier de script Lua que nous venons de créer :

1. Faites un clic droit sur la racine de la collection et sélectionnez <kbd>Add Game Object</kbd>. Définissez la propriété *id* de l'objet sur "controller".
2. Faites un clic droit sur l'objet "controller" et sélectionnez <kbd>Add Component from file</kbd>, puis sélectionnez le fichier *ground.script*.

![Contrôleur du sol](images/runner/1/ground_controller.png)

Lorsque vous exécutez le jeu, l'objet de jeu "controller" exécute maintenant le script de son composant *Script*, ce qui fait défiler le sol de façon fluide à travers l'écran.

## Étape 4 - Créer un héros {#step-4-creating-a-hero-character}

Le héros sera un objet de jeu constitué des composants suivants :

Un *Spine Model*
: Il nous donne un petit héros semblable à une poupée de papier, dont les parties du corps peuvent être animées avec fluidité (et à faible coût).

Un *Collision Object*
: Il détecte les collisions entre le héros et les éléments du niveau sur lesquels il peut courir, qui sont dangereux ou qu'il peut ramasser.

Un *Script*
: Il reçoit les entrées de l'utilisateur et y réagit, fait sauter le héros, l'anime et gère les collisions.

Commencez par importer les images des parties du corps, puis ajoutez-les à un nouvel atlas que nous appelons *hero.atlas* :

1. Créez un dossier en faisant un clic droit dans le panneau *Assets pane* et en sélectionnant <kbd>New ▸ Folder</kbd>. Veillez à ne sélectionner aucun dossier avant de cliquer, sinon le nouveau dossier sera créé à l'intérieur de celui qui est sélectionné. Nommez le dossier "hero".
2. Créez un fichier d'atlas en faisant un clic droit sur le dossier *hero* et en sélectionnant <kbd>New ▸ Atlas File</kbd>. Nommez le fichier *hero.atlas*.
3. Créez un sous-dossier *images* dans le dossier *hero*. Faites un clic droit sur le dossier *hero* et sélectionnez <kbd>New ▸ Folder</kbd>.
4. Faites glisser les images des parties du corps du dossier *hero-images* du lot de ressources vers le dossier *images* que vous venez de créer dans le panneau *Assets pane*.
5. Ouvrez *hero.atlas*, faites un clic droit sur le nœud racine dans *Outline* et sélectionnez <kbd>Add Images</kbd>. Sélectionnez toutes les images des parties du corps et cliquez sur *OK*.
6. Enregistrez le fichier d'atlas.

![Atlas du héros](images/runner/2/hero_atlas.png)

Nous devons également importer les données d'animation Spine et préparer une *Spine Scene* pour les utiliser :

1. Faites glisser le fichier *hero.spinejson* (inclus dans le lot de ressources) vers le dossier *hero* dans le panneau *Assets pane*.
2. Créez un fichier *Spine Scene*. Faites un clic droit sur le dossier *hero* et sélectionnez <kbd>New ▸ Spine Scene File</kbd>. Nommez le fichier *hero.spinescene*.
3. Double-cliquez sur le nouveau fichier pour ouvrir et modifier la *Spine Scene*.
4. Définissez la propriété *spine_json* sur le fichier JSON importé *hero.spinejson*. Cliquez sur la propriété, puis sur le bouton de sélection de fichier *...* pour ouvrir le navigateur de ressources.
5. Définissez la propriété *atlas* pour qu'elle fasse référence au fichier *hero.atlas*.
6. Enregistrez le fichier.

![Scène Spine du héros](images/runner/2/hero_spinescene.png)

::: sidenote
Le fichier *hero.spinejson* a été exporté au format Spine JSON. Vous aurez besoin du logiciel d'animation Spine pour créer de tels fichiers. Si vous souhaitez utiliser un autre logiciel d'animation, vous pouvez exporter vos animations sous forme de feuilles de sprites et les utiliser comme animations image par image à partir de ressources *Tile Source* ou *Atlas*. Consultez le manuel sur l'[animation](/manuals/animation) pour en savoir plus.
:::

### Construire l'objet de jeu {#building-the-game-object}

Nous pouvons maintenant commencer à construire l'objet de jeu du héros :

1. Créez un fichier *hero.go* (faites un clic droit sur le dossier *hero* et sélectionnez <kbd>New ▸ Game Object File</kbd>).
2. Ouvrez le fichier d'objet de jeu.
3. Ajoutez-lui un composant *Spine Model*. (Faites un clic droit sur la racine dans *Outline* et sélectionnez <kbd>Add Component</kbd>, puis sélectionnez "Spine Model".)
4. Définissez la propriété *Spine Scene* du composant sur le fichier *hero.spinescene* que vous venez de créer et sélectionnez "run_right" comme animation par défaut (nous réglerons correctement l'animation plus tard).
5. Enregistrez le fichier.

![Propriétés du modèle Spine](images/runner/2/spinemodel_properties.png)

Il est maintenant temps d'ajouter la physique pour que les collisions fonctionnent :

1. Ajoutez un composant *Collision Object* à l'objet de jeu du héros. (Faites un clic droit sur la racine dans *Outline* et sélectionnez <kbd>Add Component</kbd>, puis sélectionnez "Collision Object".)
2. Faites un clic droit sur le nouveau composant et sélectionnez <kbd>Add Shape</kbd>. Ajoutez deux formes pour couvrir le corps du personnage. Une sphère et une boîte suffiront.
3. Cliquez sur les formes et utilisez l'outil *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) pour les placer correctement.
4. Sélectionnez le composant *Collision Object* et définissez sa propriété *Type* sur "Kinematic".

::: sidenote
Le type de collision "Kinematic" signifie que nous voulons détecter les collisions, mais que le moteur physique ne les résoudra pas automatiquement et ne simulera pas les objets. Le moteur physique prend en charge plusieurs types d'objets de collision. Vous pouvez en savoir plus dans la [documentation sur la physique](/manuals/physics).
:::

Il est essentiel de préciser avec quoi l'objet de collision doit interagir :

1. Définissez la propriété *Group* sur un nouveau groupe de collision nommé "hero".
2. Définissez la propriété *Mask* sur un autre groupe, "geometry", avec lequel cet objet de collision doit détecter les collisions. Notez que le groupe "geometry" n'existe pas encore, mais nous ajouterons bientôt des objets de collision qui lui appartiennent.

Enfin, créez un fichier *hero.script* et ajoutez-le à l'objet de jeu.

1. Faites un clic droit sur le dossier *hero* dans le panneau *Assets pane* et sélectionnez <kbd>New ▸ Script File</kbd>. Nommez le nouveau fichier *hero.script*.
2. Ouvrez le nouveau fichier, copiez et collez le code suivant dans le fichier de script, puis enregistrez-le. (Le code est assez simple, à l'exception du solveur qui sépare la forme de collision du héros de ce qu'elle heurte. C'est le rôle de la fonction `handle_geometry_contact()`.)

![Objet de jeu du héros](images/runner/2/hero_game_object.png)

::: sidenote
Nous gérons nous-mêmes les collisions parce que, si nous définissions plutôt le type de l'objet de collision du personnage comme dynamique, le moteur effectuerait une simulation newtonienne des corps concernés. Pour un jeu comme celui-ci, une telle simulation est loin d'être optimale. Nous prenons donc le contrôle complet au lieu de lutter contre le moteur physique en appliquant diverses forces.

Cela nécessite toutefois un peu de calcul vectoriel pour gérer correctement les collisions. Vous trouverez une explication détaillée de la résolution des collisions cinématiques dans la [documentation sur la physique](/manuals/physics-resolving-collisions/).
:::

```lua
-- gravity pulling the player down in pixel units/sˆ2
local gravity = -20

-- take-off speed when jumping in pixel units/s
local jump_takeoff_speed = 900

function init(self)
    -- this tells the engine to send input to on_input() in this script
    msg.post(".", "acquire_input_focus")

    -- save the starting position
    self.position = go.get_position()

    -- keep track of movement vector and if there is ground contact
    self.velocity = vmath.vector3(0, 0, 0)
    self.ground_contact = false
end

function final(self)
    -- Return input focus when the object is deleted
    msg.post(".", "release_input_focus")
end

function update(self, dt)
    local gravity = vmath.vector3(0, gravity, 0)

    if not self.ground_contact then
        -- Apply gravity if there's no ground contact
        self.velocity = self.velocity + gravity
    end

    -- apply velocity to the player character
    go.set_position(go.get_position() + self.velocity * dt)

    -- reset volatile state
    self.correction = vmath.vector3()
    self.ground_contact = false
end

local function handle_geometry_contact(self, normal, distance)
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
    if message_id == hash("contact_point_response") then
        -- check if we received a contact point message. One message for each contact point
        if message.group == hash("geometry") then
            handle_geometry_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- only allow jump from ground
    if self.ground_contact then
        -- set take-off speed
        self.velocity.y = jump_takeoff_speed
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
    if action_id == hash("jump") or action_id == hash("touch") then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    end
end
```

1. Ajoutez le script à l'objet du héros en tant que composant *Script* (faites un clic droit sur la racine de *hero.go* dans *Outline* et sélectionnez <kbd>Add Component from File</kbd>, puis sélectionnez le fichier *hero.script*).

Si vous le souhaitez, vous pouvez maintenant ajouter temporairement le héros à la collection principale et lancer le jeu pour le voir tomber à travers le monde.

Le dernier élément nécessaire pour que le héros soit fonctionnel est la gestion des entrées. Le script ci-dessus contient déjà une fonction `on_input()` qui réagit aux actions "jump" et "touch" (pour les écrans tactiles). Ajoutons des liaisons d'entrée pour ces actions.

1. Ouvrez "input/game.input_bindings".
2. Ajoutez un déclencheur clavier pour "KEY_SPACE" et nommez l'action "jump".
3. Ajoutez un déclencheur tactile pour "TOUCH_MULTI" et nommez l'action "touch". (Les noms des actions sont arbitraires, mais doivent correspondre à ceux de votre script. Notez que plusieurs déclencheurs ne peuvent pas utiliser le même nom d'action.)
4. Enregistrez le fichier.

![Liaisons d'entrée](images/runner/2/input_bindings.png)

## Étape 5 - Réorganiser le niveau {#step-5-refactoring-the-level}

Maintenant que notre héros est configuré avec ses collisions et tout le nécessaire, nous devons aussi ajouter des collisions au sol pour qu'il ait quelque chose à heurter (ou sur quoi courir). Nous allons le faire dans un instant, mais commençons par une petite réorganisation : plaçons tous les éléments du niveau dans une collection distincte et rangeons un peu la structure des fichiers :

1. Créez un fichier *level.collection* (faites un clic droit sur *main* dans le panneau *Assets pane* et sélectionnez <kbd>New ▸ Collection File</kbd>).
2. Ouvrez le nouveau fichier, faites un clic droit sur la racine dans *Outline*, sélectionnez <kbd>Add Collection from File</kbd> et choisissez *ground.collection*.
3. Dans *level.collection*, faites un clic droit sur la racine dans *Outline*, sélectionnez <kbd>Add Game Object File</kbd> et choisissez *hero.go*.
4. Créez maintenant un dossier nommé *level* à la racine du projet (faites un clic droit sur l'espace blanc sous *game.project* et sélectionnez <kbd>New ▸ Folder</kbd>), puis déplacez-y les ressources du niveau créées jusqu'ici : les fichiers *level.collection* et *level.atlas*, le dossier "images" contenant les images de l'atlas du niveau, ainsi que les fichiers *ground.collection* et *ground.script*.
5. Ouvrez *main.collection*, supprimez *ground.collection* et ajoutez à sa place *level.collection* (faites un clic droit et sélectionnez <kbd>Add Collection from File</kbd>), qui contient maintenant *ground.collection*. Veillez à placer la collection à la position 0, 0, 0.

::: sidenote
Comme vous l'avez peut-être remarqué, la hiérarchie des fichiers affichée dans le panneau *Assets pane* est indépendante de la structure du contenu que vous construisez dans vos collections. Les fichiers individuels sont référencés dans les fichiers de collection et d'objet de jeu, mais leur emplacement est totalement libre.

Si vous souhaitez déplacer un fichier, Defold vous aide en mettant automatiquement à jour les références à ce fichier (refactorisation). Lorsque vous créez un logiciel complexe, comme un jeu, il est extrêmement utile de pouvoir modifier la structure du projet à mesure qu'il grandit et évolue. Defold encourage cette pratique et facilite l'opération : n'ayez donc pas peur de déplacer vos fichiers !
:::

Nous devons également ajouter à la collection du niveau un objet de jeu contrôleur doté d'un composant script :

1. Créez un fichier de script. Faites un clic droit sur le dossier *level* dans le panneau *Assets pane* et sélectionnez <kbd>New ▸ Script File</kbd>. Nommez le fichier *controller.script*.
2. Ouvrez le fichier de script, copiez-y le code suivant et enregistrez-le :

    ```lua
    -- controller.script
    go.property("speed", 360) -- <1>

    function init(self)
        msg.post("ground/controller#ground", "set_speed", { speed = self.speed })
    end
    ```
    1. Il s'agit d'une propriété de script. Nous lui donnons une valeur par défaut, mais chaque instance du script placée dans le jeu peut remplacer cette valeur directement dans la vue des propriétés de l'éditeur.

3. Ouvrez le fichier *level.collection*.
4. Faites un clic droit sur la racine dans *Outline* et sélectionnez <kbd>Add Game Object</kbd>.
5. Définissez *Id* sur "controller".
6. Faites un clic droit sur l'objet de jeu "controller" dans *Outline*, sélectionnez <kbd>Add Component from File</kbd>, puis le fichier *controller.script* dans le dossier *level*.
7. Enregistrez le fichier.

![Propriété de script](images/runner/2/script_property.png)

::: sidenote
L'objet de jeu "controller" n'existe pas dans un fichier distinct : il est créé directement dans la collection du niveau. Son instance est donc créée à partir des données définies sur place. Cela convient aux objets de jeu à usage unique comme celui-ci. Si vous avez besoin de plusieurs instances d'un objet de jeu et souhaitez pouvoir modifier le prototype ou modèle utilisé pour créer chaque instance, créez simplement un fichier d'objet de jeu et ajoutez l'objet à la collection à partir de ce fichier. Vous obtenez ainsi un objet de jeu qui référence le fichier comme prototype ou modèle.

Cet objet de jeu "controller" a pour rôle de contrôler tout ce qui concerne le niveau en cours d'exécution. Bientôt, ce script sera chargé de faire apparaître des plateformes et des pièces avec lesquelles le héros pourra interagir, mais pour l'instant, il se contente de définir la vitesse du niveau.
:::

Dans sa fonction `init()`, le script du contrôleur du niveau envoie un message au composant script de l'objet contrôleur du sol, en l'adressant par son identifiant :

```lua
msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
```

L'identifiant de l'objet de jeu contrôleur est `"ground/controller"`, car il se trouve dans la collection "ground". Nous ajoutons ensuite l'identifiant du composant, `"controller"`, après le caractère dièse `"#"`, qui sépare l'identifiant de l'objet de celui du composant. Notez que le script du sol ne contient pas encore de code pour réagir au message `set_speed` : nous devons donc ajouter une fonction `on_message()` à *ground.script* et la logique nécessaire.

1. Ouvrez *ground.script*.
2. Ajoutez le code suivant et enregistrez le fichier :

```lua
-- ground.script
function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then -- <1>
        self.speed = message.speed -- <2>
    end
end
```
1. Tous les messages sont hachés en interne lors de leur envoi et doivent être comparés à la valeur hachée.
2. Les données du message sont une table Lua contenant les données envoyées avec le message.

![Ajout du code du sol](images/runner/insert_ground_code.png)

## Étape 6 - Physique du sol et plateformes {#step-6-ground-physics-and-platforms}

À ce stade, nous devons ajouter les collisions physiques du sol :

1. Ouvrez le fichier *ground.collection*.
2. Ajoutez un composant *Collision Object* à un objet de jeu adapté. Comme le script du sol ne réagit pas aux collisions (toute cette logique se trouve dans le script du héros), nous pouvons le placer dans n'importe quel objet de jeu _immobile_ (les objets des tuiles du sol ne sont pas immobiles, évitez-les donc). L'objet de jeu "controller" convient bien, mais vous pouvez créer un objet distinct si vous préférez. Faites un clic droit sur l'objet de jeu, sélectionnez <kbd>Add Component</kbd>, puis *Collision Object*.
3. Ajoutez une forme de boîte en faisant un clic droit sur le composant *Collision Object*, puis en sélectionnant <kbd>Add Shape</kbd> et enfin *Box*.
4. Utilisez les outils *Move Tool* et *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> et <kbd>Scene ▸ Scale Tool</kbd>) pour que la boîte couvre toutes les tuiles du sol.
5. Définissez la propriété *Type* de l'objet de collision sur "Static", car la physique du sol ne se déplacera pas.
6. Définissez la propriété *Group* de l'objet de collision sur "geometry" et *Mask* sur "hero". L'objet de collision du héros et celui-ci détecteront désormais leurs collisions mutuelles.
7. Enregistrez le fichier.

![Collision du sol](images/runner/2/ground_collision.png)

Vous devriez maintenant pouvoir exécuter le jeu (<kbd>Project ▸ Build</kbd>). Le héros devrait courir sur le sol et pouvoir sauter avec la touche <kbd>Space</kbd>. Si vous exécutez le jeu sur un appareil mobile, vous pouvez sauter en touchant l'écran.

Pour rendre la vie un peu moins monotone dans notre monde de jeu (game world), nous devons ajouter des plateformes sur lesquelles sauter.

1. Faites glisser le fichier image *rock_planks.png* du lot de ressources vers le sous-dossier *level/images*.
2. Ouvrez *level.atlas* et ajoutez la nouvelle image à l'atlas (faites un clic droit sur la racine dans *Outline* et sélectionnez <kbd>Add Images</kbd>).
3. Enregistrez le fichier.
4. Créez un fichier *Game Object* nommé *platform.go* dans le dossier *level*. (Faites un clic droit sur *level* dans le panneau *Assets pane*, puis sélectionnez <kbd>New ▸ Game Object File</kbd>.)
5. Ajoutez un composant *Sprite* à l'objet de jeu (faites un clic droit sur la racine dans la vue *Outline* et sélectionnez <kbd>Add Component</kbd>, puis *Sprite*).
6. Définissez la propriété *Image* pour qu'elle fasse référence au fichier *level.atlas* et définissez *Default Animation* sur "rock_planks". Pour plus de commodité, rangez les objets du niveau dans un sous-dossier "level/objects".
7. Ajoutez un composant *Collision Object* à l'objet de jeu de la plateforme (faites un clic droit sur la racine dans la vue *Outline* et sélectionnez <kbd>Add Component</kbd>).
8. Veillez à définir le *Type* du composant sur "Kinematic", ainsi que *Group* et *Mask* sur "geometry" et "hero" respectivement.
9. Ajoutez une *Box Shape* au composant *Collision Object*. (Faites un clic droit sur le composant dans *Outline* et sélectionnez <kbd>Add Shape</kbd>, puis choisissez *Box*.)
10. Utilisez les outils *Move Tool* et *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> et <kbd>Scene ▸ Scale Tool</kbd>) pour que la forme du composant *Collision Object* couvre la plateforme.
11. Créez un fichier *Script* nommé *platform.script* (faites un clic droit dans le panneau *Assets pane*, puis sélectionnez <kbd>New ▸ Script File</kbd>), insérez le code suivant dans le fichier et enregistrez-le :

    ```lua
    -- platform.script
    function init(self)
        self.speed = 540      -- Default speed in pixels/s
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            go.delete() -- <1>
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        end
    end
    ```
    1. Supprimez simplement la plateforme lorsqu'elle a dépassé le bord droit de l'écran.

12. Ouvrez *platform.go* et ajoutez le nouveau script en tant que composant (faites un clic droit sur la racine dans la vue *Outline* et sélectionnez <kbd>Add Component From File</kbd>, puis *platform.script*).
13. Copiez *platform.go* dans un nouveau fichier (faites un clic droit sur le fichier dans le panneau *Assets pane* et sélectionnez <kbd>Copy</kbd>, puis faites de nouveau un clic droit et sélectionnez <kbd>Paste</kbd>) et nommez ce nouveau fichier *platform_long.go*.
14. Ouvrez *platform_long.go* et ajoutez un deuxième composant *Sprite* (faites un clic droit sur la racine dans la vue *Outline* et sélectionnez <kbd>Add Component</kbd>). Vous pouvez aussi copier le *Sprite* existant.
15. Utilisez l'outil *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) pour placer les composants *Sprite* côte à côte.
16. Utilisez les outils *Move Tool* et *Scale Tool* pour que la forme du composant *Collision Object* couvre les deux plateformes.

![Plateforme](images/runner/2/platform_long.png)

::: sidenote
Notez que *platform.go* et *platform_long.go* possèdent tous deux des composants *Script* qui font référence au même fichier de script. C'est un avantage : toute modification de ce fichier influencera le comportement des plateformes normales comme des plateformes longues.
:::

## Faire apparaître des plateformes {#spawning-platforms}

L'idée est de créer un jeu de course sans fin simple. Les objets de jeu des plateformes ne peuvent donc pas être placés dans une collection dans l'éditeur. Nous devons les faire apparaître dynamiquement :

1. Ouvrez *level.collection*.
2. Ajoutez deux composants *Factory* à l'objet de jeu "controller" (faites un clic droit dessus et sélectionnez <kbd>Add Component</kbd>, puis *Factory*).
3. Définissez les propriétés *Id* des composants sur "platform_factory" et "platform_long_factory".
4. Définissez la propriété *Prototype* de "platform_factory" sur le fichier */level/objects/platform.go*.
5. Définissez la propriété *Prototype* de "platform_long_factory" sur le fichier */level/objects/platform_long.go*.
6. Enregistrez le fichier.
7. Ouvrez le fichier *controller.script*, qui gère le niveau.
8. Modifiez le script pour qu'il contienne le code suivant, puis enregistrez le fichier :

```lua
-- controller.script
go.property("speed", 360)

local grid = 460
local platform_heights = { 100, 200, 350 } -- <1>

function init(self)
    msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
    self.gridw = 0
end

function update(self, dt) -- <2>
    self.gridw = self.gridw + self.speed * dt

    if self.gridw >= grid then
        self.gridw = 0

        -- Maybe spawn a platform at random height
        if math.random() > 0.2 then
            local h = platform_heights[math.random(#platform_heights)]
            local f = "#platform_factory"
            if math.random() > 0.5 then
                f = "#platform_long_factory"
            end

            local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, vmath.vector3(0.6, 0.6, 1))
            msg.post(p, "set_speed", { speed = self.speed })
        end
    end
end
```
1. Valeurs prédéfinies de la position Y à laquelle faire apparaître les plateformes.
2. La fonction `update()` est appelée une fois par image. Nous nous en servons pour décider de faire apparaître une plateforme normale ou longue à certains intervalles (pour éviter les chevauchements) et à certaines hauteurs. Il est facile d'expérimenter différents algorithmes d'apparition pour varier la jouabilité.

Exécutez maintenant le jeu (<kbd>Project ▸ Build</kbd>).

Voilà, cela commence à devenir (presque) jouable...

![Exécution du jeu](images/runner/2/run_game.png)

## Étape 7 - Animation et mort {#step-7-animation-and-death}

Nous allons commencer par donner vie au héros. Pour le moment, le pauvre est bloqué dans une boucle de course et ne réagit correctement ni aux sauts ni au reste. Le fichier Spine que nous avons ajouté depuis le lot de ressources contient justement un ensemble d'animations prévues pour cela.

1. Ouvrez le fichier *hero.script* et ajoutez les fonctions suivantes _avant_ la fonction `update()` existante :

```lua
    -- hero.script
    local function play_animation(self, anim)
        -- only play animations which are not already playing
        if self.anim ~= anim then
            -- tell the spine model to play the animation
            local anim_props = { blend_duration = 0.15 }
            spine.play_anim("#spinemodel", anim, go.PLAYBACK_LOOP_FORWARD, anim_props)
            -- remember which animation is playing
            self.anim = anim
        end
    end

    local function update_animation(self)
        -- make sure the right animation is playing
        if self.ground_contact then
            play_animation(self, hash("run"))
        else
            play_animation(self, hash("jump"))

        end
    end
```

2. Trouvez la fonction `update()` et ajoutez un appel à `update_animation` :

```lua
    ...
    -- apply it to the player character
    go.set_position(go.get_position() + self.velocity * dt)

    update_animation(self)
    ...
  ```

![Insertion du code du héros](images/runner/insert_hero_code.png)

::: sidenote
En Lua, les variables locales ont une « portée lexicale », et l'ordre dans lequel vous placez les fonctions `local` est significatif. La fonction `update()` appelle les fonctions locales `update_animation()` et `play_animation()`, ce qui signifie que l'environnement d'exécution doit avoir rencontré ces fonctions locales pour pouvoir les appeler. C'est pourquoi nous devons les placer avant `update()`. Si vous inversez l'ordre des fonctions, vous obtiendrez une erreur. Notez que cela s'applique uniquement aux variables `local`. Vous pouvez en savoir plus sur les règles de portée et les fonctions locales de Lua à l'adresse http://www.lua.org/pil/6.2.html
:::

Cela suffit pour ajouter des animations de saut et de chute au héros. Si vous exécutez le jeu, vous remarquerez qu'il est beaucoup plus agréable à jouer. Vous constaterez peut-être aussi que les plateformes peuvent malheureusement pousser le héros hors de l'écran. C'est un effet secondaire de la gestion des collisions, mais le remède est simple : ajoutons un peu de violence et rendons les bords des plateformes dangereux !

1. Faites glisser *spikes.png* du lot de ressources vers le dossier "level/images" dans le panneau *Assets pane*.
2. Ouvrez *level.atlas* et ajoutez l'image (faites un clic droit et sélectionnez <kbd>Add Images</kbd>).
3. Ouvrez *platform.go* et ajoutez quelques composants *Sprite*. Définissez *Image* sur *level.atlas* et *Default Animation* sur "spikes".
4. Utilisez les outils *Move Tool* et *Rotate Tool* pour placer les pointes le long des bords de la plateforme.
5. Pour afficher les pointes derrière la plateforme, définissez la position *Z* de leurs sprites sur -0.1.
6. Ajoutez un composant *Collision Object* aux plateformes (faites un clic droit sur la racine dans *Outline* et sélectionnez <kbd>Add Component</kbd>). Définissez la propriété *Group* sur "danger". Définissez également *Mask* sur "hero".
7. Ajoutez une forme de boîte au *Collision Object* (faites un clic droit et sélectionnez <kbd>Add Shape</kbd>), puis utilisez l'outil *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) et l'outil *Scale Tool* pour placer la forme de façon que le héros entre en collision avec l'objet "danger" lorsqu'il heurte la plateforme par le côté ou par le dessous.
8. Enregistrez le fichier.

    ![Pointes de la plateforme](images/runner/3/danger_edges.png)

9. Ouvrez *hero.go*, sélectionnez le *Collision Object* et ajoutez le nom "danger" à la propriété *Mask*. Enregistrez ensuite le fichier.

    ![Collision du héros](images/runner/3/hero_collision.png)

10. Ouvrez *hero.script* et modifiez la fonction `on_message()` pour obtenir une réaction lorsque le héros entre en collision avec un bord "danger" :

    ```lua
    -- hero.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            self.velocity = vmath.vector3(0, 0, 0)
            self.correction = vmath.vector3()
            self.ground_contact = false
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- check if we received a contact point message
            if message.group == hash("danger") then
                -- Die and restart
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("#", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end
    ```
    1. Ajoutez un mouvement de rotation et de chute au héros lorsqu'il meurt. Il reste beaucoup de possibilités d'amélioration !

11. Modifiez la fonction `init()` pour qu'elle envoie un message "reset" afin d'initialiser l'objet, puis enregistrez le fichier :

    ```lua
    -- hero.script
    function init(self)
        -- this lets us handle input in this script
        msg.post(".", "acquire_input_focus")
        -- save position
        self.position = go.get_position()
        msg.post("#", "reset")
    end
    ```

## Étape 8 - Réinitialiser le niveau {#step-8-resetting-the-level}

Si vous essayez le jeu maintenant, vous constaterez rapidement que le mécanisme de réinitialisation ne fonctionne pas. La réinitialisation du héros se passe bien, mais vous pouvez facilement réapparaître dans une situation où vous retombez immédiatement sur le bord d'une plateforme et mourez de nouveau. Nous voulons réinitialiser correctement tout le niveau à chaque mort. Comme le niveau n'est qu'une série de plateformes créées dynamiquement, il suffit de garder la trace de toutes ces plateformes, puis de les supprimer lors de la réinitialisation :

1. Ouvrez le fichier *controller.script* et modifiez le code pour stocker les identifiants de toutes les plateformes créées :

    ```lua
    -- controller.script
    go.property("speed", 360)

    local grid = 460
    local platform_heights = { 100, 200, 350 }

    function init(self)
        msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
        self.gridw = 0
        self.spawns = {} -- <1>
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= grid then
            self.gridw = 0

            -- Maybe spawn a platform at random height
            if math.random() > 0.2 then
                local h = platform_heights[math.random(#platform_heights)]
                local f = "#platform_factory"
                if math.random() > 0.5 then
                    f = "#platform_long_factory"
                end

                local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, vmath.vector3(0.6, 0.6, 1))
                msg.post(p, "set_speed", { speed = self.speed })
                table.insert(self.spawns, p) -- <1>
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then -- <2>
            -- Tell the hero to reset.
            msg.post("hero#hero", "reset")
            -- Delete all platforms
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then -- <3>
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```
    1. Nous utilisons une table pour stocker toutes les plateformes créées.
    2. Le message "reset" supprime toutes les plateformes stockées dans la table.
    3. Le message "delete_spawn" supprime une plateforme particulière et la retire de la table.

2. Enregistrez le fichier.
3. Ouvrez *platform.script* et modifiez-le pour qu'au lieu de simplement supprimer une plateforme qui a atteint le bord gauche, il envoie un message au contrôleur du niveau lui demandant de retirer la plateforme :

    ```lua
    -- platform.script
    ...
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    ...
    ```

    ![Insertion du code de la plateforme](images/runner/insert_platform_code.png)

4. Enregistrez le fichier.
5. Ouvrez *hero.script*. La dernière chose à faire est de demander au niveau de se réinitialiser. Nous avons déplacé le message demandant au héros de se réinitialiser dans le script du contrôleur du niveau. Centraliser ainsi le contrôle de la réinitialisation est utile, car cela nous permet, par exemple, d'introduire plus facilement une séquence de mort plus longue avec une durée définie :

```lua
-- hero.script
...
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
    function()
        msg.post("controller#controller", "reset")
    end)
...
```

![Insertion du code du héros](images/runner/insert_hero_code_2.png)

La boucle principale de redémarrage et de mort est maintenant en place !

Passons à une raison de rester en vie : les pièces !

## Étape 9 - Des pièces à ramasser {#step-9-coins-to-collect}

L'idée est de placer dans le niveau des pièces que le joueur pourra ramasser. La première question est de savoir comment les y placer. Nous pourrions, par exemple, développer un mécanisme d'apparition coordonné d'une manière ou d'une autre avec l'algorithme d'apparition des plateformes. Nous avons finalement choisi une approche beaucoup plus simple : laisser les plateformes elles-mêmes faire apparaître les pièces :

1. Faites glisser l'image *coin.png* du lot de ressources vers "level/images" dans le panneau *Assets pane*.
2. Ouvrez *level.atlas* et ajoutez l'image (faites un clic droit et sélectionnez <kbd>Add Images</kbd>).
3. Créez un fichier *Game Object* nommé *coin.go* dans le dossier *level* (faites un clic droit sur *level* dans le panneau *Assets pane* et sélectionnez <kbd>New ▸ Game Object File</kbd>).
4. Ouvrez *coin.go* et ajoutez un composant *Sprite* (faites un clic droit dans *Outline* et sélectionnez <kbd>Add Component</kbd>). Définissez *Image* sur *level.atlas* et *Default Animation* sur "coin".
5. Ajoutez un *Collision Object* (faites un clic droit dans *Outline* et sélectionnez <kbd>Add Component</kbd>)
et ajoutez une forme *Sphere* qui couvre l'image (faites un clic droit sur le composant et sélectionnez <kbd>Add Shape</kbd>).
6. Utilisez l'outil *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) et l'outil *Scale Tool* pour que la sphère couvre l'image de la pièce.
7. Définissez le *Type* de l'objet de collision sur "Kinematic", son *Group* sur "pickup" et son *Mask* sur "hero".
8. Ouvrez *hero.go* et ajoutez "pickup" à la propriété *Mask* du composant *Collision Object*, puis enregistrez le fichier.
9. Créez un fichier de script *coin.script* (faites un clic droit sur *level* dans le panneau *Assets pane* et sélectionnez <kbd>New ▸ Script File</kbd>). Remplacez le code du modèle par le suivant :

    ```lua
    -- coin.script
    function init(self)
        self.collected = false
    end

    function on_message(self, message_id, message, sender)
        if self.collected == false and message_id == hash("collision_response") then
            self.collected = true
            msg.post("#sprite", "disable")
        elseif message_id == hash("start_animation") then
            pos = go.get_position()
            go.animate(go.get_id(), "position.y", go.PLAYBACK_LOOP_PINGPONG, pos.y + 24, go.EASING_INOUTSINE, 0.75, message.delay)
        end
    end
    ```

10. Ajoutez le fichier de script à l'objet de la pièce en tant que composant *Script* (faites un clic droit sur la racine dans *Outline* et sélectionnez <kbd>Add Component from File</kbd>).

    ![Objet de jeu de la pièce](images/runner/3/coin.png)

Nous prévoyons de faire apparaître les pièces à partir des objets de plateforme. Ajoutez donc des factories pour les pièces dans *platform.go* et *platform_long.go*.

1. Ouvrez *platform.go* et ajoutez un composant *Factory* (faites un clic droit dans *Outline* et sélectionnez <kbd>Add Component</kbd>).
2. Définissez l'*Id* de la *Factory* sur "coin_factory" et son *Prototype* sur le fichier *coin.go*.
3. Ouvrez maintenant *platform_long.go* et créez un composant *Factory* identique.
4. Enregistrez les deux fichiers.

![Factory des pièces](images/runner/3/coin_factory.png)

Nous devons maintenant modifier *platform.script* pour qu'il fasse apparaître les pièces et les supprime :

```lua
-- platform.script
function init(self)
    self.speed = 540     -- Default speed in pixels/s
    self.coins = {}
end

function final(self)
    for i,p in ipairs(self.coins) do
        go.delete(p)
    end
end

function update(self, dt)
    local pos = go.get_position()
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    pos.x = pos.x - self.speed * dt
    go.set_position(pos)
end

function create_coins(self, params)
    local spacing = 56
    local pos = go.get_position()
    local x = pos.x - params.coins * (spacing*0.5) - 24
    for i = 1, params.coins do
        local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
        msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
        msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
        table.insert(self.coins, coin)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then
        self.speed = message.speed
    elseif message_id == hash("create_coins") then
        create_coins(self, message)
    end
end
```
1. En définissant la plateforme comme parent de la pièce créée, celle-ci se déplace avec la plateforme.
2. L'animation fait monter et descendre les pièces par rapport à la plateforme, qui est désormais leur parent.

::: sidenote
Les relations parent-enfant modifient uniquement le _graphe de scène_. Un enfant subit les transformations (déplacement, mise à l'échelle ou rotation) de son parent. Si vous avez besoin de relations d'« appartenance » supplémentaires entre les objets de jeu, vous devez les gérer explicitement dans le code.
:::

La dernière étape de ce tutoriel consiste à ajouter quelques lignes à *controller.script* :

```lua
-- controller.script
...
local platform_heights = { 100, 200, 350 }
local coins = 3 -- <1>
...
```
1. Le nombre de pièces à faire apparaître sur une plateforme normale.

```lua
-- controller.script
...
local coins = coins
if math.random() > 0.5 then
    f = "#platform_long_factory"
    coins = coins * 2 -- Twice the number of coins on long platforms
end
...
```

```lua
-- controller.script
...
msg.post(p, "set_speed", { speed = self.speed })
msg.post(p, "create_coins", { coins = coins })
table.insert(self.spawns, p)
...
```

![Insertion du code du contrôleur](images/runner/insert_controller_code.png)

Nous avons maintenant un jeu simple, mais fonctionnel ! Si vous êtes arrivé jusqu'ici, vous aurez peut-être envie de poursuivre par vous-même et d'ajouter les éléments suivants :

1. Des compteurs de score et de vies
2. Des effets de particules pour le ramassage des objets et la mort
3. De belles images d'arrière-plan

> Téléchargez la version terminée du projet [ici](images/runner/sample-runner.zip).

Ce tutoriel d'introduction est terminé. À vous maintenant de vous plonger dans Defold. Nous avons préparé de nombreux [manuels et tutoriels](//www.defold.com/learn) pour vous guider et, si vous êtes bloqué, vous êtes le bienvenu sur le [forum](//forum.defold.com).

Amusez-vous bien avec Defold !
