---
brief: Dans ce tutoriel, vous adapterez un shader de shadertoy.com à Defold.
layout: tutorial
locale: fr
title: Tutoriel de Shadertoy à Defold
---

# Tutoriel Shadertoy {#shadertoy-tutorial}

[Shadertoy.com](https://www.shadertoy.com/) est un site qui rassemble des shaders GL proposés par les utilisateurs. C'est une excellente ressource pour trouver du code de shader et de l'inspiration. Dans ce tutoriel, nous allons prendre un shader de Shadertoy et le faire fonctionner dans Defold. Nous supposons que vous avez quelques notions de base sur les shaders. Si vous avez besoin de vous documenter, [le manuel des shaders](/manuals/shader/) constitue un bon point de départ.

Le shader que nous utiliserons est [Star Nest](https://www.shadertoy.com/view/XlfGRj) de Pablo Andrioli (l'utilisateur "Kali" sur Shadertoy). C'est un shader de fragments entièrement procédural, dont les mathématiques tiennent de la magie noire et qui produit un superbe effet de champ d'étoiles.

![Star Nest](../images/shadertoy/starnest.png)

Le shader ne compte que 65 lignes de code GLSL assez compliqué, mais ne vous inquiétez pas. Nous allons le traiter comme une boîte noire qui remplit son rôle à partir de quelques entrées simples. Notre tâche consiste à modifier le shader pour qu'il s'interface avec Defold au lieu de Shadertoy.

## Un support à texturer {#something-to-texture}

Le shader Star Nest est un pur shader de fragments : nous avons donc seulement besoin d'un support à texturer. Plusieurs options sont possibles : un sprite, une tilemap, une interface graphique ou un modèle. Pour ce tutoriel, nous allons utiliser un simple modèle 3D. La raison est que nous pouvons facilement transformer le rendu du modèle en effet plein écran, ce qui est nécessaire si nous voulons effectuer un post-traitement visuel, par exemple.

Nous pouvons partir d'un projet vide.

1. Ouvrez Defold et sélectionnez Create From *Templates*.
2. Sélectionnez *Empty Project*.
3. Définissez le *Title* et sélectionnez l'emplacement *Location* sur votre disque.
4. Cliquez sur <kbd>Create New Project</kbd>.

![Démarrage](../images/shadertoy/empty_project.png)

Vous pouvez utiliser le maillage intégré `quad.gltf` du dossier `builtins/assets/meshes`.

Vous pouvez également créer un maillage plan carré dans Blender ou dans tout autre logiciel de modélisation 3D. Pour simplifier, les coordonnées des quatre sommets sont à -1 et 1 sur l'axe X et à -1 et 1 sur l'axe Y. Dans Blender, l'axe Z pointe vers le haut par défaut : vous devez donc faire pivoter le maillage de 90° autour de l'axe X. Vous devez aussi vous assurer de générer des coordonnées UV correctes pour le maillage. Dans Blender, sélectionnez le maillage, passez en *Edit Mode*, puis sélectionnez <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>.

<div class='sidenote' markdown='1'>
Blender est un logiciel 3D libre et gratuit que vous pouvez télécharger depuis [blender.org](https://www.blender.org).
</div>

![Quadrilatère dans Blender](../images/shadertoy/quad_blender.png)

1. Ouvrez votre fichier "main.collection" dans Defold et créez un nouvel objet de jeu (game object) "star-nest".
2. Ajoutez un composant (component) *Model* à l'objet de jeu "star-nest".
3. Définissez la propriété *Mesh* sur notre `quad.gltf`.
4. Nous devons définir le matériau du modèle : pour le moment, sélectionnez donc le matériau intégré `model.material`.

Le modèle devrait apparaître dans l'éditeur de scène, mais son rendu est entièrement noir. Cela vient du fait qu'aucune texture ne lui est encore attribuée :

![Quadrilatère dans Defold](../images/shadertoy/quad_default_material.png)

## Création du matériau {#creating-the-material}

1. Créez un nouveau fichier de matériau *`star-nest.material`* en cliquant avec le <kbd>bouton droit de la souris</kbd> sur le dossier `main` dans le panneau `Assets`, puis en sélectionnant <kbd>New</kbd>▸<kbd>Material</kbd> et en le nommant `star-nest`.

 ![Matériau](../images/shadertoy/new_material.png)

2. De la même manière, créez un programme de shader de sommets `star-nest.vp` et un programme de shader de fragments `star-nest.fp` :
3. Ouvrez *star-nest.material*.
4. Définissez *Vertex Program* sur `star-nest.vp`.
5. Définissez *Fragment Program* sur `star-nest.fp`.
6. Ajoutez une *Vertex Constant*, nommez-la "`view_proj`" et choisissez le type `Viewproj` (pour la projection de la vue).
8. Ajoutez une étiquette "tile" dans *Tags*. Ainsi, le quadrilatère sera inclus dans la passe de rendu qui dessine les sprites et les tuiles.

 ![Matériau](../images/shadertoy/material.png)

### Programme de sommets {#vertex-program}

1. Ouvrez le fichier du programme de shader de sommets `star-nest.vp`. Il devrait contenir le code suivant :

    ```glsl
    #version 140

    // positions are in world space
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### Programme de fragments {#fragment-program}

1. Ouvrez le fichier du programme de shader de fragments `star-nest.fp` et modifiez le code afin que la couleur du fragment soit définie en fonction des composantes X et Y des coordonnées UV (`var_texcoord0`). Cela nous permet de vérifier que le modèle est correctement configuré :

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. Définissez la propriété `Material` sur le matériau `star-nest` que nous venons de créer, pour le composant modèle de l'objet de jeu `star-nest` dans `main.collection`.

L'éditeur devrait maintenant afficher le modèle avec le nouveau shader, et nous pouvons voir clairement si les coordonnées UV sont correctes ; le coin inférieur gauche devrait être noir (0, 0, 0), le coin supérieur gauche vert (0, 1, 0), le coin supérieur droit jaune (1, 1, 0) et le coin inférieur droit rouge (1, 0, 0) :

![Quadrilatère dans Defold](../images/shadertoy/quad_material.png)

## Caméra {#camera}

Nous pouvons maintenant exécuter notre projet (<kbd>Project</kbd>▸<kbd>Build</kbd> ou le raccourci <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>), mais nous verrons un écran noir (ou presque, à l'exception peut-être d'un minuscule pixel dans le coin inférieur gauche). En effet, il n'y a pas de caméra, et le script de rendu par défaut utilise une solution de repli simple qui affiche un immense espace 2D, alors que notre modèle se trouve à la position (0,0,0) et ne mesure que 1 en largeur.

Ajoutons un objet de jeu doté d'un composant caméra pour définir ce que nous verrons dans le jeu.

1. Ajoutez un objet de jeu nommé `camera` à la position (0,0,1). (Il est important de définir la coordonnée Z sur 1 pour que cet objet de jeu se trouve devant notre modèle, car dans la configuration 2D par défaut, l'axe Z pointe vers nous.)
2. Ajoutez un composant `Camera` : vous verrez un aperçu de la caméra contenant notre quadrilatère. Dans cette configuration, nous avons la chance de ne rien avoir à modifier dans les propriétés par défaut, et nous devrions déjà voir le résultat attendu, à une exception près : nous n'avons pas besoin d'un volume de vue aussi grand pour la caméra, nous pouvons donc réduire `Far Z` à `2`.

![Caméra](../images/shadertoy/camera.png)

Nous pouvons aussi changer le type de caméra en définissant `Orthographic Projection` sur `true`, puis en réglant `Orthographic Zoom` sur une valeur comme 600. Dans ce cas, toutefois, le rapport largeur/hauteur ne sera pas automatique et notre modèle ne remplira donc pas l'écran.

## Le shader Star Nest {#the-star-nest-shader}

Maintenant que tout est en place, commençons à travailler sur le code du shader lui-même. Examinons d'abord le code d'origine. Il se compose de plusieurs sections :

![Code du shader Star Nest](../images/shadertoy/starnest_code.png)

Nous allons utiliser un pipeline moderne avec GLSL en version 140 : pour cela, nous déclarerons la version en haut du fichier avec `#version 140`.

1. Les lignes 5--18 définissent plusieurs constantes. Nous pouvons les laisser telles quelles. Ce sont de simples constantes GLSL qui ne dépendent spécifiquement ni de Shadertoy ni de Defold.

2. Les lignes 21 et 63 contiennent les coordonnées de texture X et Y du fragment en entrée dans l'espace écran (`in vec2 fragCoord`) et la couleur du fragment en sortie (`out vec4 fragColor`).

    Defold transmet les coordonnées de texture du shader de sommets au shader de fragments par une variable interpolée, sous forme de coordonnées UV (dans l'intervalle 0--1). Dans notre shader de sommets, cette variable est déclarée avec le qualificatif `out` :

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     Dans le shader de fragments, la même valeur est reçue avec le qualificatif `in` :

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    Ensuite, en GLSL 140, nous déclarons explicitement une sortie de fragment avec le qualificatif `out` :

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    Ainsi, là où le code Shadertoy d'origine écrit dans `fragColor`, notre shader Defold écrit dans `out_fragColor`.

3. Les lignes 23--27 définissent les dimensions de la texture ainsi que la direction du mouvement et le temps mis à l'échelle. Dans Shadertoy, le shader reçoit la position du pixel via `fragCoord`, et la résolution de la fenêtre d'affichage ou de la texture lui est transmise sous la forme `uniform vec3 iResolution`. Le shader calcule des coordonnées de type UV avec le bon rapport largeur/hauteur à partir des coordonnées du fragment et de la résolution. Des décalages liés à la résolution sont également appliqués pour obtenir un cadrage plus agréable.

    Dans Defold, nous ne partons pas des coordonnées des pixels. Nous recevons directement les coordonnées UV normalisées du shader de sommets via `var_texcoord0`. Ces coordonnées vont de `0.0` à `1.0` sur le quadrilatère affiché.

    La version Defold doit modifier ces calculs pour utiliser les coordonnées UV de `var_texcoord0`.
    Voici à quoi ressemble une conversion typique :

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    La valeur exacte de `aspect` dépend de la configuration de l'exemple. Si l'effet est rendu sur un quadrilatère plein écran dont la taille d'affichage est connue, le rapport largeur/hauteur peut être codé en dur pour le tutoriel. Si l'effet doit prendre en charge des tailles de fenêtre quelconques, transmettez la résolution sous forme de constante de fragment et placez-la dans un bloc uniforme GLSL 140.

    Le temps est également défini ici. Il est transmis au shader sous la forme `uniform float iGlobalTime`. Depuis la version 1.12.3, Defold fournit le temps aux shaders au moyen d'une constante spéciale `Time` que nous allons utiliser.

    Dans les versions modernes de Defold, les variables uniformes non opaques sont déclarées dans des blocs uniformes.
    Dans le shader de fragments, nous déclarons cette valeur ainsi :

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    Ensuite, dans `star-nest.material`, nous ajouterons une Fragment Constant nommée `time` et définirons son type sur `Time`.

    La valeur peut alors être utilisée ainsi :

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    où `time.x` est le temps écoulé depuis le démarrage du moteur et `time.y` le temps écoulé depuis l'image précédente.

4. Les lignes 29--39 définissent la rotation du rendu volumétrique, la position de la souris influant sur cette rotation. Les coordonnées de la souris sont transmises au shader sous la forme `uniform vec4 iMouse`.

    Pour ce tutoriel, nous allons laisser de côté les entrées de la souris.

5. Les lignes 41--62 constituent le cœur du shader. Nous pouvons laisser ce code tel quel.

## Le shader Star Nest modifié {#the-modified-star-nest-shader}

En parcourant les sections ci-dessus et en effectuant les modifications nécessaires, nous obtenons le code de shader suivant. Il a été légèrement réorganisé pour le rendre plus lisible. Les différences entre les versions Defold et Shadertoy sont indiquées :

```glsl
#version 140 // <1>

// Star Nest by Pablo Román Andrioli
// This content is under the MIT License.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// get coords and direction
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// volumetric rendering
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// tiling fold
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// the magic formula
			p = abs(p) / dot(p, p) - formuparam;

			// absolute sum of average change
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// dark matter
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// dark matter, don't render near
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// coloring based on distance
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// color adjust
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```

1. Nous déclarons #version 140 en haut du fichier pour utiliser le pipeline GLSL moderne de Defold. Nous laissons ensuite les définitions telles quelles.
2. Le shader de sommets transmet les coordonnées UV au shader de fragments via var_texcoord0. En GLSL 140, le shader de fragments reçoit cette valeur interpolée avec le qualificatif in.
3. En GLSL 140, le shader de fragments devrait déclarer une variable de sortie explicite au lieu d'écrire dans gl_FragColor. Ici, nous utilisons out vec4 out_fragColor.
4. La constante de matériau Time de Defold est exposée au shader par un bloc uniforme. Dans star-nest.material, ajoutez une Fragment Constant nommée time et définissez son type sur Time.
5. Shadertoy utilise mainImage(out vec4 fragColor, in vec2 fragCoord). Dans Defold, nous utilisons le point d'entrée habituel void main(), lisons les coordonnées UV interpolées depuis var_texcoord0 et écrivons la couleur finale dans out_fragColor.
6. Pour ce tutoriel, nous définissons une valeur statique de résolution et de rapport largeur/hauteur pour le rendu. Le modèle étant actuellement carré, nous pouvons utiliser vec2 res = vec2(1.0, 1.0);. Avec un modèle rectangulaire de taille 1280×720, nous pourrions utiliser à la place vec2 res = vec2(1.78, 1.0); et multiplier les coordonnées UV par cette valeur pour préserver le bon rapport largeur/hauteur.
7. Le shader Shadertoy d'origine utilise iGlobalTime. Dans cette version Defold, time.x contient le temps écoulé depuis le démarrage du moteur : nous l'affectons donc à une variable locale iGlobalTime et l'utilisons pour animer le mouvement de la caméra dans le champ d'étoiles.
8. Pour garder ce tutoriel simple, nous supprimons complètement les valeurs iMouse. La rotation elle-même est conservée, car elle réduit la symétrie visuelle du rendu volumétrique.
9. Enfin, le shader écrit la couleur de fragment obtenue dans out_fragColor.

Enregistrez le programme de shader de fragments. Le modèle devrait maintenant être joliment texturé avec un champ d'étoiles dans l'éditeur de scène et à l'exécution :

![Quadrilatère avec Star Nest](../images/shadertoy/quad_starnest.png)


## Animation {#animation}

La dernière pièce du puzzle consiste à introduire le temps pour faire bouger les étoiles. Depuis la version 1.12.3, Defold le fournit automatiquement grâce à une constante de fragment de type `Time`.

1. Ouvrez *star-nest.material*.
2. Ajoutez une *Fragment Constant* et nommez-la "time".
3. Définissez son *Type* sur `Time`.

![Constante de temps](../images/shadertoy/time_constant.png)

Et voilà ! Nous gérons déjà cette valeur `time` dans le shader de fragments. Nous avons terminé !

## Exercices {#exercises}

Pour poursuivre avec un exercice amusant, ajoutez au shader les entrées d'origine correspondant aux mouvements de la souris. Vous devrez créer une nouvelle Fragment Constant, cette fois de type `User`, puis la mettre à jour dans `on_input`, au sein d'un script qui détecte les mouvements de la souris, en utilisant la fonction `go.set()` pour affecter les coordonnées d'entrée à la nouvelle constante.

Amusez-vous bien avec Defold !
