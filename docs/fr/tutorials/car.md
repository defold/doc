---
title: Construire une voiture simple dans Defold.
brief: "Si vous découvrez Defold, ce guide vous aidera à prendre vos repères dans l'éditeur. Il explique également les concepts de base et les éléments les plus courants de Defold : objets de jeu, collections, scripts et sprites."
---

# Construire une voiture {#building-a-car}

Si vous découvrez Defold, ce guide vous aidera à prendre vos repères dans l'éditeur. Il explique également les concepts de base et les éléments les plus courants de Defold : objets de jeu (game object), collections, scripts et sprites.

Nous allons partir d'un projet vide et avancer étape par étape jusqu'à obtenir une toute petite application jouable. À la fin, vous devriez avoir une idée du fonctionnement de Defold et être prêt à aborder un tutoriel plus complet ou à vous plonger directement dans les manuels.

::: sidenote
Tout au long du tutoriel, les descriptions détaillées des concepts et de la manière d'effectuer certaines opérations sont présentées comme ce paragraphe. Si vous trouvez que ces sections entrent trop dans les détails, vous pouvez les passer.
:::

## Créer un nouveau projet {#creating-a-new-project}

![Nouveau projet](images/new_empty.png)

1. Lancez Defold.
2. Sélectionnez *New Project* à gauche.
3. Sélectionnez l'onglet *From Template*.
4. Sélectionnez *Empty Project*
5. Choisissez un emplacement pour le projet sur votre disque local.
6. Cliquez sur *Create New Project*.

## L'éditeur {#the-editor}

Commencez par créer un [nouveau projet](/manuals/project-setup/) et ouvrez-le dans l'éditeur. Double-cliquez sur le fichier *main/main.collection* pour l'ouvrir :

![Vue d'ensemble de l'éditeur](../manuals/images/editor/editor2_overview.png)

L'éditeur se compose des principales zones suivantes :

Assets pane
: Cette vue présente tous les fichiers de votre projet. Les différents types de fichiers ont des icônes différentes. Double-cliquez sur un fichier pour l'ouvrir dans l'éditeur adapté à son type. Le dossier spécial *builtins*, en lecture seule, est commun à tous les projets et contient des éléments utiles comme un script de rendu par défaut, une police, des matériaux pour le rendu de divers composants (component), ainsi que d'autres éléments.

Main Editor View
: Selon le type de fichier que vous modifiez, cette vue affiche l'éditeur correspondant. Le plus couramment utilisé est l'éditeur de scène que vous voyez ici. Chaque fichier ouvert est affiché dans un onglet distinct.

Changed Files
: Contient les fichiers ajoutés, modifiés, renommés ou supprimés localement par rapport au commit Git actuel. Vous pouvez y consulter les différences textuelles et annuler les modifications locales. Utilisez un client Git externe ou la ligne de commande pour vous synchroniser avec un dépôt distant.

Outline
: Le contenu du fichier en cours de modification, présenté sous forme hiérarchique. Vous pouvez ajouter, supprimer, modifier et sélectionner des objets et des composants dans cette vue.

Properties
: Les propriétés définies pour l'objet ou le composant actuellement sélectionné.

Console
: Lorsque le jeu est en cours d'exécution, cette vue recueille les sorties du moteur de jeu (journaux, erreurs, informations de débogage, etc.), ainsi que les messages de débogage personnalisés `print()` et `pprint()` de vos scripts. Si votre application ou votre jeu ne démarre pas, la console est le premier endroit à vérifier. Derrière la console se trouvent plusieurs onglets affichant des informations sur les erreurs, ainsi qu'un éditeur de courbes utilisé pour créer des effets de particules.

## Exécuter le jeu {#running-the-game}

Le modèle de projet "Empty" est effectivement entièrement vide. Sélectionnez tout de même <kbd>Project ▸ Build</kbd> pour compiler le projet et lancer le jeu.

![Compilation](images/car/start_build_and_launch.png)

Un écran noir n'est peut-être pas très passionnant, mais il s'agit bien d'un jeu Defold en cours d'exécution, et nous pouvons facilement le transformer en quelque chose de plus intéressant. Allons-y.

::: sidenote
L'éditeur Defold travaille sur des fichiers. En double-cliquant sur un fichier dans le panneau *Assets pane*, vous l'ouvrez dans l'éditeur approprié. Vous pouvez alors travailler sur son contenu.

Lorsque vous avez terminé de modifier un fichier, vous devez l'enregistrer. Sélectionnez <kbd>File ▸ Save</kbd> dans le menu principal. L'éditeur vous le rappelle en ajoutant un astérisque '\*' au nom du fichier dans l'onglet de chaque fichier contenant des modifications non enregistrées.

![Fichier avec des modifications non enregistrées](images/car/file_changed.png)
:::

## Assembler la voiture {#assembling-the-car}

Nous allons commencer par créer une nouvelle collection. Une collection est un conteneur d'objets de jeu que vous avez placés et positionnés. Les collections servent le plus souvent à construire les niveaux d'un jeu, mais elles sont très utiles dès que vous devez réutiliser des groupes et/ou des hiérarchies d'objets de jeu qui vont ensemble. Il peut être utile de considérer les collections comme une sorte de prefab.

Cliquez sur le dossier *main* dans le panneau *Assets pane*, puis faites un clic droit et sélectionnez <kbd>New ▸ Collection File</kbd>. Vous pouvez aussi sélectionner <kbd>File ▸ New ▸ Collection File</kbd> dans le menu principal.

![Nouveau fichier de collection](images/car/start_new_collection.png)

Nommez le nouveau fichier de collection *car.collection* et ouvrez-le. Nous allons utiliser cette nouvelle collection vide pour construire une petite voiture à partir de quelques objets de jeu. Un objet de jeu est un conteneur de composants (comme des sprites, des sons, des scripts de logique, etc.) que vous utilisez pour construire votre jeu. Chaque objet de jeu est identifié de manière unique dans le jeu par son identifiant. Les objets de jeu peuvent communiquer entre eux par échange de messages, mais nous y reviendrons plus tard.

Il est aussi possible de créer un objet de jeu directement dans une collection, comme nous l'avons fait ici. Cela produit un objet unique. Vous pouvez copier cet objet, mais chaque copie est indépendante : modifier l'une n'affecte pas les autres. Ainsi, si vous créez 10 copies d'un objet de jeu et décidez de toutes les modifier, vous devrez modifier les 10 instances de l'objet. Il convient donc de créer directement dans une collection les objets de jeu dont vous ne prévoyez pas de faire beaucoup de copies.

En revanche, un objet de jeu enregistré dans un _fichier_ sert de prototype (également appelé « prefab » ou « blueprint » dans d'autres moteurs). Lorsque vous placez dans une collection des instances d'un objet de jeu enregistré dans un fichier, chaque objet est placé _par référence_ : c'est un clone basé sur le prototype. Si vous décidez de modifier le prototype, tous les objets de jeu placés à partir de ce prototype sont immédiatement mis à jour.

![Ajouter l'objet de jeu de la voiture](images/car/start_add_car_gameobject.png)

Sélectionnez le nœud racine "Collection" dans la vue *Outline*, faites un clic droit et sélectionnez <kbd>Add Game Object</kbd>. Un nouvel objet de jeu portant l'identifiant "go" apparaît dans la collection. Sélectionnez-le et définissez son identifiant sur "car" dans la vue *Properties*. Pour l'instant, "car" n'a rien de très intéressant. Il est vide, sans représentation visuelle ni logique. Pour lui donner une représentation visuelle, nous devons ajouter un _composant_ sprite.

Les composants servent à donner aux objets de jeu une présence (graphismes, son) et des fonctionnalités (factories de création d'objets, collisions, comportements définis par script). Un composant ne peut pas exister seul : il doit se trouver à l'intérieur d'un objet de jeu. Les composants sont généralement définis directement dans le même fichier que l'objet de jeu. Toutefois, si vous souhaitez réutiliser un composant, vous pouvez l'enregistrer dans un fichier distinct (comme pour les objets de jeu) et l'inclure par référence dans n'importe quel fichier d'objet de jeu. Certains types de composants (les scripts Lua, par exemple) doivent être placés dans un fichier de composant distinct, puis inclus par référence dans vos objets.

Notez que vous ne manipulez pas directement les composants : vous pouvez déplacer, faire pivoter, redimensionner les objets de jeu qui les contiennent et animer les propriétés de ces objets.

![Ajouter un composant à la voiture](images/car/start_add_car_component.png)

Sélectionnez l'objet de jeu "car", faites un clic droit et sélectionnez <kbd>Add Component</kbd>, puis sélectionnez *Sprite* et cliquez sur *Ok*. Si vous sélectionnez le sprite dans la vue *Outline*, vous verrez que quelques propriétés doivent être définies :

Image
: Il faut ici une source d'image pour le sprite. Créez un fichier d'atlas d'images en sélectionnant "main" dans la vue *Assets pane*, puis en faisant un clic droit et en sélectionnant <kbd>New ▸ Atlas File</kbd>. Nommez le nouveau fichier d'atlas *sprites.atlas* et double-cliquez dessus pour l'ouvrir dans l'éditeur d'atlas. Enregistrez les deux fichiers image suivants sur votre ordinateur et faites-les glisser dans *main* dans la vue *Assets pane*. Vous pouvez maintenant sélectionner le nœud racine Atlas dans l'éditeur d'atlas, faire un clic droit et sélectionner <kbd>Add Images</kbd>. Ajoutez l'image de la voiture et celle du pneu à l'atlas, puis enregistrez. Vous pouvez maintenant sélectionner *sprites.atlas* comme source d'image du composant sprite de l'objet de jeu "car" dans la collection "car".

Images pour notre jeu :

![Image de la voiture](images/car/start_car.png)
![Image du pneu](images/car/start_tire.png)

Ajoutez ces images à l'atlas :

![Atlas des sprites](images/car/start_sprites_atlas.png)

![Propriétés du sprite](images/car/start_sprite_properties.png)

Default Animation
: Définissez cette propriété sur "car" (ou sur le nom que vous avez donné à l'image de la voiture). Chaque sprite a besoin d'une animation par défaut, jouée lorsqu'il est affiché dans le jeu. Lorsque vous ajoutez des images à un atlas, Defold crée automatiquement des animations à une seule image (fixes) pour chaque fichier image.

## Terminer la voiture {#completing-the-car}

Continuez en ajoutant deux autres objets de jeu dans la collection. Nommez-les "left_wheel" et "right_wheel" et placez dans chacun un composant sprite affichant l'image du pneu que nous avons ajoutée à *sprites.atlas*. Faites ensuite glisser les objets de jeu des roues sur "car" pour en faire ses enfants. Les objets de jeu enfants d'autres objets de jeu restent attachés à leur parent lorsque celui-ci se déplace. Ils peuvent aussi être déplacés individuellement, mais tous leurs mouvements sont relatifs à l'objet parent. C'est parfait pour les pneus, puisque nous voulons qu'ils restent attachés à la voiture et qu'il suffise de les faire pivoter légèrement à gauche et à droite lorsque nous dirigeons la voiture. Une collection peut contenir un nombre quelconque d'objets de jeu, côte à côte, organisés en arborescences parent-enfant complexes, ou les deux.

Placez les objets de jeu des pneus à l'endroit voulu en les sélectionnant, puis en choisissant <kbd>Scene ▸ Move Tool</kbd>. Saisissez les poignées en forme de flèche ou le carré vert central pour déplacer l'objet au bon endroit. Il nous reste à faire en sorte que les pneus soient dessinés sous la voiture. Pour cela, nous définissons la composante Z de leur position sur -0.5. Chaque élément visuel d'un jeu est dessiné de l'arrière vers l'avant, selon sa valeur Z. Un objet dont la valeur Z est 0 sera dessiné par-dessus un objet dont la valeur Z est -0.5. Puisque la valeur Z par défaut de l'objet de jeu de la voiture est 0, la nouvelle valeur des objets des pneus les placera sous l'image de la voiture.

![Collection de la voiture terminée](images/car/start_car_collection_complete.png)

## Le script de la voiture {#the-car-script}

La dernière pièce du puzzle est un _script_ pour contrôler la voiture. Un script est un composant contenant un programme qui définit les comportements des objets de jeu. Avec les scripts, vous pouvez définir les règles de votre jeu et la manière dont les objets doivent réagir aux différentes interactions (avec le joueur comme avec les autres objets). Tous les scripts sont écrits dans le langage de programmation Lua. Pour travailler avec Defold, vous ou un membre de votre équipe devez apprendre à programmer en Lua.

Sélectionnez "main" dans le panneau *Assets pane*, faites un clic droit et sélectionnez <kbd>New ▸ Script File</kbd>. Nommez le nouveau fichier *car.script*, puis ajoutez-le à l'objet de jeu "car" en sélectionnant "car" dans la vue *Outline*, puis en faisant un clic droit et en sélectionnant <kbd>Add Component File</kbd>. Sélectionnez *car.script* et cliquez sur *OK*. Enregistrez le fichier de collection.

Double-cliquez sur *car.script* pour l'ouvrir.

::: sidenote
Defold fournit plusieurs fonctions de cycle de vie pour programmer la logique du jeu. Vous trouverez plus d'informations à leur sujet dans le [manuel des scripts](/manuals/script).
:::

Commencez par supprimer les fonctions `final`, `on_message` et `on_reload`, car nous n'en aurons pas besoin
pour ce tutoriel.

Ajoutez ensuite les lignes de code suivantes avant le début de la fonction `init`.

```lua
-- Constants
local turn_speed = 0.1                           									  -- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)     -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)									  -- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         		        	-- Vector from center of back and front wheel pairs

local acceleration = 100 																						-- The acceleration of the car

-- prehash the inputs
local left = hash("left")
local right = hash("right")
local accelerate = hash("accelerate")
local brake = hash("brake")
```

Les modifications apportées ici sont assez simples : nous avons seulement ajouté à notre script plusieurs constantes (`constants`) que nous utiliserons plus tard pour programmer notre voiture.

::: sidenote
Remarquez que nous stockons à l'avance les valeurs hachées dans des variables. C'est une bonne pratique, car elle rend votre code plus lisible et plus performant.
:::

Modifiez ensuite la fonction `init` pour qu'elle contienne ce qui suit :

```lua
function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )		--<1>

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")		-- <2>

	-- Some variables
	self.steer_angle = vmath.quat()				 -- <3>
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end
```

Vous vous demandez ce que nous venons de modifier ? Voici une explication.

1. Nous envoyons un message à notre script de rendu pour lui demander de définir la couleur d'arrière-plan sur du gris. Les scripts de rendu sont des scripts spéciaux de Defold qui contrôlent la manière dont les objets sont affichés à l'écran.
2. Pour recevoir les actions d'entrée dans un composant script ou un script d'interface graphique, le message `acquire_input_focus` doit être envoyé à l'objet de jeu qui contient le composant. Dans notre cas, nous envoyons ce message à l'objet de jeu qui contient le script de la voiture.
3. Nous déclarons ensuite quelques variables que nous utiliserons pour suivre l'état actuel de notre voiture.

C'était facile, n'est-ce pas ? Continuons en modifiant la fonction `update` pour qu'elle contienne maintenant ce qui suit :

```lua
function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration				-- <1>

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)								-- <2>

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)			-- <3>

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt			-- <4>

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)																			-- <5>

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then																		-- <6>
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")					-- <7>
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()								-- <8>
	self.input = vmath.vector3()
end
```

Voilà une longue fonction ! Ne vous inquiétez pas, voici comment elle fonctionne :

1. Nous définissons d'abord notre vecteur d'accélération à partir de notre vecteur d'entrée. Cela garantit que l'accélération de la voiture suit la direction de l'entrée.
2. Ensuite, le déplacement des roues avant et arrière est calculé selon une logique simple : les roues arrière de la voiture avancent toujours tout droit, tandis que les roues avant se déplacent dans la direction vers laquelle elles sont tournées.
3. La nouvelle direction de déplacement de notre voiture est calculée à partir du déplacement des roues avant et arrière.
4. Ici, nous ajoutons l'accélération calculée à la vitesse.
5. Enfin, nous mettons à jour la position de la voiture à partir de notre vitesse actuelle.
6. Nous appliquons une interpolation sphérique (slerp) à l'angle de braquage en fonction de notre entrée gauche/droite. Cela évite que les roues changent instantanément d'orientation chaque fois que l'entrée change.
7. La rotation des roues est ensuite définie en fonction de l'angle de braquage actuel de la voiture. De même, la rotation de la voiture est définie en fonction de la direction dans laquelle elle se déplace actuellement.
8. Enfin, nous réinitialisons les vecteurs d'accélération et d'entrée.

Il est enfin temps de faire réagir notre voiture aux entrées. Modifiez la fonction `on_input` pour qu'elle ressemble à ceci :

```lua
function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == left then
		self.input.x = -1
	elseif action_id == right then
		self.input.x = 1
	elseif action_id == accelerate then
		self.input.y = 1
	elseif action_id == brake then
		self.input.y = -1
	end
end
```

Cette fonction est en fait assez simple : nous recevons l'entrée et définissons notre vecteur d'entrée.

N'oubliez pas d'enregistrer vos modifications.

## Les entrées {#input}

Aucune action d'entrée n'est encore configurée, alors remédions-y. Ouvrez le fichier */input/game.input_bindings* et ajoutez des liaisons *key_trigger* pour "accelerate", "brake", "left" et "right". Nous les associons aux touches fléchées (KEY_LEFT, KEY_RIGHT, KEY_UP et KEY_DOWN) :

![Liaisons d'entrée](images/car/start_input_bindings.png)

## Ajouter la voiture au jeu {#adding-the-car-to-the-game}

La voiture est maintenant prête à rouler. Nous l'avons créée dans "car.collection", mais elle n'existe pas encore dans le jeu. En effet, le moteur charge actuellement "main.collection" au démarrage. Pour y remédier, il suffit d'ajouter *car.collection* à *main.collection*. Ouvrez *main.collection*, sélectionnez le nœud racine "Collection" dans la vue *Outline*, faites un clic droit et sélectionnez <kbd>Add Collection From File</kbd>, puis sélectionnez *car.collection* et cliquez sur *OK*. Le contenu de *car.collection* est alors placé dans *main.collection* sous forme de nouvelles instances. Si vous modifiez le contenu de *car.collection*, chaque instance de la collection sera mise à jour automatiquement lors de la compilation du jeu.

![Ajouter la collection de la voiture](images/car/start_adding_car_collection.png)

Sélectionnez maintenant <kbd>Project ▸ Build</kbd> et faites un tour avec votre nouvelle voiture !
Vous remarquerez que vous pouvez désormais déplacer la voiture à votre guise. Mais quelque chose ne va pas encore. Lorsque vous relâchez les commandes, la voiture ne s'arrête pas comme elle le devrait. Il est temps d'ajouter ce comportement !

## La traînée à la rescousse {#drag-to-the-rescue}

Lorsqu'un objet se déplace dans le monde réel, la force de traînée s'oppose à son mouvement et le ralentit. Cette force est approximativement proportionnelle au carré de la vitesse de l'objet en mouvement et peut donc s'écrire `D = k * |V| * V`, où `k` est une constante, `V` est le vecteur vitesse et `|V|` sa norme (la vitesse). Ajoutons cela.

Dans la section des constantes, en haut du script, ajoutez la constante suivante

```lua
local drag = 1.1	        --the drag constant <1>
```

Puis, dans la fonction `update`, ajoutez les lignes suivantes juste au-dessus de cette ligne et enregistrez le fichier.

```lua
function update(self, dt)
	...
  -- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt
	...
end
```

```lua
function update(self, dt)
	...
	-- Speed is the magnitude of the velocity
	local speed = vmath.length_sqr(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3(0) end
	...
end
```

1. Déclarez la valeur de la traînée comme une constante.
2. Calculez la vitesse à laquelle nous nous déplaçons.
3. Appliquez la traînée à l'accélération actuelle selon la formule
4. Arrêtez la voiture si sa vitesse est déjà suffisamment faible.

## Le script complet de la voiture {#the-complete-car-script}

Une fois les étapes ci-dessus terminées, votre fichier *car.script* devrait ressembler à ceci :

```lua
local turn_speed = 0.1                           				          	-- Slerp factor
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)	    -- 30 degrees
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 degrees
local steer_angle_zero = vmath.quat_rotation_z(0)				          	-- Zero degrees
local wheels_vector = vmath.vector3(0, 72, 0)         				      -- Vector from center of back and front wheel pairs

local acceleration = 100 		                      									-- The acceleration of the car
local drag = 1.1                                                  	-- the drag constant

function init(self)
	-- Send a message to the render script (see builtins/render/default.render_script) to set the clear color.
	-- This changes the background color of the game. The vector4 contains color information
	-- by channel from 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 and Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )

	-- Acquire input focus so we can react to input
	msg.post(".", "acquire_input_focus")

	-- Some variables
	self.steer_angle = vmath.quat()
	self.direction = vmath.quat()

	-- Velocity and acceleration are car relative (not rotated)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Input vector. This is modified later in the on_input function
	-- to store the input.
	self.input = vmath.vector3()
end

function update(self, dt)
	-- Set acceleration to the y input
	self.acceleration.y = self.input.y * acceleration

	-- Calculate the new positions of front and back wheels
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)

	-- Calculate the car's new direction
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)

	-- Speed is the magnitude of the velocity
	local speed = vmath.length(self.velocity)

	-- Apply drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Stop if we are already slow enough
	if speed < 0.5 then self.velocity = vmath.vector3() end

	-- Calculate new velocity based on current acceleration
	self.velocity = self.velocity + self.acceleration * dt

	-- Update position based on current velocity and direction
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)

	-- Interpolate the wheels using vmath.slerp
	if self.input.x > 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Update the wheel rotation
	go.set_rotation(self.steer_angle, "left_wheel")
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Set the game object's rotation to the direction
	go.set_rotation(self.direction)

	-- reset acceleration and input
	self.acceleration = vmath.vector3()
	self.input = vmath.vector3()
end

function on_input(self, action_id, action)
	-- set the input vector to correspond to the key press
	if action_id == hash("left") then
		self.input.x = -1
	elseif action_id == hash("right") then
		self.input.x = 1
	elseif action_id == hash("accelerate") then
		self.input.y = 1
	elseif action_id == hash("brake") then
		self.input.y = -1
	end
end
```

## Essayer le jeu terminé {#trying-the-final-game}

Sélectionnez maintenant <kbd>Project ▸ Build</kbd> dans le menu principal et faites un tour avec votre nouvelle voiture !

Ce tutoriel d'introduction est terminé. Voici quelques défis que vous pouvez essayer de relever par vous-même :

1. Actuellement, la voiture se déplace avec la même accélération en marche avant et en marche arrière. Vous pouvez modifier ce comportement pour qu'elle se déplace plus lentement en marche arrière.
2. Transformez certaines constantes (comme l'accélération) en propriétés (`properties`) afin de pouvoir les modifier pour différentes instances de la voiture.
3. Ajoutez des sons à votre voiture et faites-la vrombir ! ([Indice](/manuals/sound/))

À présent, lancez-vous et plongez dans Defold. Nous avons préparé de nombreux [manuels et tutoriels](/learn) pour vous guider et, si vous êtes bloqué, vous êtes les bienvenus sur le [forum](//forum.defold.com).

Amusez-vous bien avec Defold !
