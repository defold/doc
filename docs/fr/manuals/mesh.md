---
title: Maillages 3D dans Defold
brief: Ce manuel explique comment créer des maillages 3D à l'exécution dans votre jeu.
---

# Composant de maillage {#mesh-component}

Defold est fondamentalement un moteur 3D. Même lorsque vous travaillez uniquement avec du contenu 2D, tout le rendu est effectué en 3D, puis projeté de manière orthographique à l'écran. Defold vous permet d'exploiter pleinement du contenu 3D en ajoutant et en créant des maillages 3D à l'exécution dans vos collections. Vous pouvez créer des jeux entièrement en 3D avec uniquement des ressources 3D, ou mélanger du contenu 3D et 2D comme vous le souhaitez.

## Création d'un composant de maillage {#creating-a-mesh-component}

Les composants (components) de maillage se créent comme tout autre composant d'objet de jeu (game object). Vous pouvez procéder de deux façons :

- Créez un *fichier Mesh* en faisant un <kbd>clic droit</kbd> sur un emplacement dans le navigateur *Assets*, puis en sélectionnant <kbd>New... ▸ Mesh</kbd>.
- Créez le composant directement intégré à un objet de jeu en faisant un <kbd>clic droit</kbd> sur un objet de jeu dans la vue *Outline*, puis en sélectionnant <kbd>Add Component ▸ Mesh</kbd>.

![Maillage dans un objet de jeu](images/mesh/mesh.png)

Une fois le maillage créé, vous devez définir plusieurs propriétés :

### Propriétés du maillage {#mesh-properties}

En plus des propriétés *Id*, *Position* et *Rotation*, les propriétés suivantes sont propres au composant :

*Material*
: Le matériau à utiliser pour le rendu du maillage.

*Vertices*
: Un fichier de tampon décrivant les données du maillage par flux.

*Primitive Type*
: Lines, Triangles ou Triangle Strip.

*Position Stream*
: Cette propriété doit contenir le nom du flux *position*. Le flux est automatiquement fourni en entrée au shader de sommets.

*Normal Stream*
: Cette propriété doit contenir le nom du flux *normal*. Le flux est automatiquement fourni en entrée au shader de sommets.

*tex0*
: Définissez la texture à utiliser pour le maillage.

## Manipulation dans l'éditeur {#editor-manipulation}

Une fois le composant de maillage en place, vous pouvez modifier et manipuler le composant et/ou l'objet de jeu qui le contient avec les outils habituels du *Scene Editor*, afin de déplacer, de faire pivoter et de redimensionner le maillage à votre convenance.

## Manipulation à l'exécution {#runtime-manipulation}

Vous pouvez manipuler les maillages à l'exécution à l'aide des tampons Defold. Exemple de création d'un cube à partir de bandes de triangles :

```Lua

-- cube
local vertices = {
	0, 0, 0,
	0, 1, 0,
	1, 0, 0,
	1, 1, 0,
	1, 1, 1,
	0, 1, 0,
	0, 1, 1,
	0, 0, 1,
	1, 1, 1,
	1, 0, 1,
	1, 0, 0,
	0, 0, 1,
	0, 0, 0,
	0, 1, 0
}

-- create a buffer with a position stream
local buf = buffer.create(#vertices / 3, {
	{ name = hash("position"), type=buffer.VALUE_TYPE_FLOAT32, count = 3 }
})

-- get the position stream and write the vertices
local positions = buffer.get_stream(buf, "position")
for i, value in ipairs(vertices) do
	positions[i] = vertices[i]
end

-- set the buffer with the vertices on the mesh
local res = go.get("#mesh", "vertices")
resource.set_buffer(res, buf)
```

Consultez le [message d'annonce sur le forum pour plus d'informations](https://forum.defold.com/t/mesh-component-in-defold-1-2-169-beta/65137) sur l'utilisation du composant de maillage, avec des projets d'exemple et des extraits de code.

## Élimination hors du volume de vue {#frustum-culling}

Les composants de maillage ne sont pas automatiquement éliminés du rendu en raison de leur nature dynamique et du fait qu'il n'est pas possible de savoir avec certitude comment les données de position sont encodées. Pour permettre l'élimination d'un maillage, vous devez définir sa boîte englobante alignée sur les axes comme métadonnées du tampon, à l'aide de six nombres à virgule flottante (AABB min/max) :

```lua
buffer.set_metadata(buf, hash("AABB"), { 0, 0, 0, 1, 1, 1 }, buffer.VALUE_TYPE_FLOAT32)
```

## Constantes du matériau {#material-constants}

{% include shared/material-constants.md component='mesh' variable='tint' %}

`tint`
: La teinte de couleur du maillage (`vector4`). Le `vector4` représente la teinte, avec x, y, z et w correspondant respectivement aux composantes rouge, verte, bleue et alpha.

## Sommets dans l'espace local ou mondial {#vertex-local-vs-world-space}
Si le paramètre Vertex Space du matériau du maillage est défini sur Local Space, les données sont fournies telles quelles à votre shader et vous devez transformer les sommets/normales comme à l'habitude sur le GPU.

Si le paramètre Vertex Space du matériau du maillage est défini sur World Space, vous devez soit fournir des flux `position` et `normal` par défaut, soit les sélectionner dans la liste déroulante lors de l'édition du maillage. Le moteur peut ainsi transformer les données dans l'espace mondial pour regrouper leur rendu avec celui d'autres objets.
