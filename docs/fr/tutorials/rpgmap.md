---
title: Exemple de carte de RPG
brief: Cet exemple de projet vous présente une méthode pour créer de très grandes cartes de RPG.
---
# Carte de RPG - exemple de projet {#rpg-map-sample-project}

Dans cet exemple de projet, que vous pouvez [ouvrir depuis l'éditeur](/manuals/project-setup/) ou [télécharger depuis GitHub](https://github.com/defold/sample-rpgmap), nous présentons une méthode pour créer de très grandes cartes de RPG dans Defold. La conception repose sur les hypothèses suivantes :

1. Le monde est présenté un écran à la fois. Cela permet au jeu de maintenir naturellement les ennemis et les personnages non joueurs dans les limites d'un seul écran. Le concepteur de niveaux maîtrise entièrement la présentation du monde sur l'écran du joueur.
2. Le personnage du joueur doit pouvoir parcourir une distance arbitrairement grande sans que le jeu présente de problèmes de précision des nombres à virgule flottante. Ces problèmes font généralement trembler les objets de manière étrange lorsqu'ils s'éloignent de l'origine.
3. Les déplacements du joueur sont limités par les obstacles sur la carte, ce qui permet au concepteur de niveaux de guider le joueur d'un écran à l'autre à l'aide d'arbres, de rochers, d'eau et d'autres obstacles.
4. Il doit être possible de combiner librement des tilemaps, des sprites et d'autres contenus visuels.

Commencez par exécuter l'exemple et parcourez le monde de 3x3 écrans pour vous familiariser avec son organisation. Vous contrôlez le personnage à l'aide des touches fléchées.

## La collection principale {#the-main-collection}

Ouvrez "/main/main.collection" pour afficher la collection bootstrap de cet exemple.

![](images/rpgmap/main_collection.png)

La collection principale contient l'objet de jeu (game object) du personnage du joueur, contrôlé dans huit directions avec les touches fléchées, et un second objet de jeu appelé "game" qui contrôle le déroulement du jeu. L'objet "game" se compose d'un script et d'une factory de collection pour chaque écran du jeu. Les factories sont nommées selon le schéma de nommage de la grille d'écrans.

Le script "/main/game.script" suit l'écran sur lequel le joueur se trouve actuellement. Il réagit également à un message personnalisé appelé "load_screen". Ce message charge un nouvel écran et le fait remplacer l'écran actuel dans la direction où le héros se déplace. Au départ, un écran est chargé au centre de l'affichage et il n'y a aucun autre écran avec lequel échanger sa place.

## Changement d'écran {#changing-screens}

Le héros est contrôlé par le script "/main/hero.script". Le script vérifie si l'objet de jeu du héros franchit une ligne en haut, en bas, à gauche ou à droite, près du bord de l'écran :

![](images/rpgmap/change_screen.png)

1. Si le héros s'approche suffisamment d'un bord de l'écran, un message est envoyé au script de l'objet "game" pour charger l'écran suivant.
2. La collection de l'écran suivant est créée en appelant `factory.create()` sur le composant (component) collectionfactory approprié. Le contenu de la collection est positionné hors de l'écran.
3. L'écran suivant défile jusqu'au centre de l'affichage et l'écran actuel en sort en défilant dans la direction opposée. Le personnage du joueur défile également sur la même distance et à la même vitesse.
4. L'ancien écran actuel, qui se trouve maintenant hors de l'affichage, est supprimé et l'écran suivant devient le nouvel écran actuel.
5. Une animation fait entrer le héros dans le champ de vision sur le nouvel écran, puis le joueur reprend le contrôle.

Tout cela se déroule en moins d'une seconde, ce qui rend la transition fluide et sans à-coup.

## Écrans {#screens}

Chaque écran du monde de jeu (game world) est construit dans une collection distincte contenant la tilemap, l'objet de collision et les autres objets de jeu propres à cet écran. Pour faciliter la gestion et le chargement des écrans, leurs collections sont nommées selon un schéma simple :

![](images/rpgmap/screens.png)

Chaque collection d'écran est nommée selon sa position dans la grille du monde. Le premier nombre correspond à la position X dans la grille et le second à la position Y.

Dans la vue *Assets*, recherchez et ouvrez la collection "/main/screens/0-0.collection", qui décrit l'écran situé dans le coin inférieur gauche de la carte :

![](images/rpgmap/screen_collection.png)

Remarquez qu'un objet de jeu nommé "root" est le parent de tout le contenu de l'écran. Il s'agit d'une autre convention utilisée dans cet exemple, qui joue un rôle très important : lorsqu'un écran entre dans le champ de vision, seul l'objet de jeu "root" doit être déplacé. Tous les objets enfants sont automatiquement déplacés avec le parent racine. Si un écran contient des objets de jeu particuliers, ceux-ci peuvent également être animés librement, car leur mouvement est relatif au parent racine. Lorsque l'écran entre ou sort de l'affichage par défilement, ces enfants se déplacent avec lui. Du code spécifique n'est nécessaire que si un objet doit passer d'un écran à l'autre.

Les abeilles de l'écran 0-1 illustrent simplement cette idée :

![](images/rpgmap/bees.png)

## Modification des écrans dans le contexte du monde {#editing-screens-in-the-world-context}

Chaque écran possède sa propre tilemap, qui peut être modifiée dans l'éditeur de tilemap intégré. Cependant, le principal inconvénient de la modification de chaque écran séparément est qu'il est difficile de voir comment il se raccorde aux écrans adjacents, ce qui est un aspect important pour assurer la continuité du monde de jeu.

Une collection spéciale a été créée à cet effet. Ouvrez "/main/map/test_layout.collection" pour afficher cette collection de test de l'agencement du monde :

![](images/rpgmap/test_layout.png)

Cette collection sert uniquement d'outil d'édition pendant le développement. Modifier un écran en l'affichant à côté de la collection de test de l'agencement vous permet de le voir dans son contexte et rend l'édition bien plus agréable :

![](images/rpgmap/side_by_side.png)

Toutes les modifications de la tilemap de l'écran (ici dans le volet de droite) sont immédiatement répercutées dans la collection de test (dans le volet de gauche). Notez également que la collection de test de l'agencement n'est pas ajoutée à la hiérarchie statique : elle est donc automatiquement exclue de tous les builds.

## Résumé {#summary}

Comme vous l'avez vu, cet exemple est construit selon des contraintes précises concernant le monde de jeu et la façon dont le héros le parcourt. Si votre jeu a des exigences différentes, vous devrez probablement trouver une autre solution. Par exemple, si votre jeu exige que la caméra se déplace sans transition sur la carte du monde, vous aurez besoin d'une autre façon de diviser votre contenu, d'un autre mécanisme de chargement et d'autres outils pour vous aider à créer votre monde de jeu.

Voilà qui conclut la présentation de l'exemple de carte de RPG. Comme toujours, vous êtes libre d'utiliser le contenu de l'exemple comme bon vous semble. Pour en savoir plus sur Defold, consultez nos [pages de documentation](https://defold.com/learn), où vous trouverez d'autres exemples, tutoriels, manuels et documents d'API.

Si vous rencontrez des difficultés ou avez des questions, [rendez-vous sur notre forum](https://forum.defold.com/).

Amusez-vous bien avec Defold !
