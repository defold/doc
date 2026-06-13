---
title: Formas de colisión
brief: Un componente de colisión puede usar varias formas primitivas o una sola forma compleja.
---

# Formas de colisión

Un componente de colisión puede usar varias formas primitivas o una sola forma compleja.

### Formas primitivas
Las formas primitivas son *box*, *sphere* y *capsule*. Agrega una forma primitiva haciendo <kbd>click derecho</kbd> en el objeto de colisión y seleccionando <kbd>Add Shape</kbd>:

![Agregar una forma primitiva](images/physics/add_shape.png)

## Forma de caja
Una caja tiene posición, rotación y dimensiones (ancho, alto y profundidad):

![Forma de caja](images/physics/box.png)

## Forma de esfera
Una esfera tiene posición, rotación y diámetro:

![Forma de esfera](images/physics/sphere.png)

## Forma de cápsula
Una cápsula tiene posición, rotación, diámetro y altura:

![Forma de esfera](images/physics/capsule.png)

::: important
Las formas de cápsula solo tienen soporte cuando se usan físicas 3D (configuradas en la sección Physics del archivo *game.project*).
:::

### Formas complejas
Una forma compleja se puede crear desde un componente tilemap o desde una forma de envolvente convexa.

## Forma de colisión de tilemap
Defold incluye una funcionalidad que te permite generar fácilmente formas físicas para el tile source usado por un tile map. El [manual de Tilesource](/manuals/tilesource/#tile-source-collision-shapes) explica cómo agregar grupos de colisión a un tile source y asignar tiles a grupos de colisión ([ejemplo](/examples/tilemap/collisions/)).

Para agregar colisión a un tile map:

1. Agrega el tilemap a un objeto de juego haciendo <kbd>click derecho</kbd> en el objeto de juego y seleccionando <kbd>Add Component File</kbd>. Selecciona el archivo de tile map.
2. Agrega un componente de objeto de colisión al objeto de juego haciendo <kbd>click derecho</kbd> en el objeto de juego y seleccionando <kbd>Add Component ▸ Collision Object</kbd>.
3. En lugar de agregar formas al componente, define la propiedad *Collision Shape* con el archivo *tilemap*.
4. Configura las *Properties* del componente de objeto de colisión como de costumbre.

![Colisión de tilesource](images/physics/collision_tilemap.png)

::: important
Ten en cuenta que la propiedad *Group* **no** se usa aquí, ya que los grupos de colisión se definen en el tile source del tile map.
:::

## Forma de envolvente convexa
Defold incluye una funcionalidad que te permite crear una forma de envolvente convexa a partir de tres o más puntos.

1. Crea un archivo de forma de envolvente convexa (extensión de archivo `.convexshape`) usando un editor externo.
2. Edita el archivo manualmente con un editor de texto o una herramienta externa (ver abajo).
3. En lugar de agregar formas al componente de objeto de colisión, define la propiedad *Collision Shape* con el archivo *convex shape*.

### Formato de archivo
El formato de archivo de envolvente convexa usa el mismo formato de datos que todos los demás archivos de Defold, es decir, el formato de texto protobuf. Una forma de envolvente convexa define los puntos de la envolvente. En físicas 2D, los puntos deben proporcionarse en sentido antihorario. En el modo de físicas 3D se usa una nube de puntos abstracta. Ejemplo 2D:

```
shape_type: TYPE_HULL
data: 200.000
data: 100.000
data: 0.0
data: 400.000
data: 100.000
data: 0.0
data: 400.000
data: 300.000
data: 0.0
data: 200.000
data: 300.000
data: 0.0
```

El ejemplo anterior define las cuatro esquinas de un rectángulo:

```
 200x300   400x300
    4---------3
    |         |
    |         |
    |         |
    |         |
    1---------2
 200x100   400x100
```

## Herramientas externas

Hay varias herramientas externas distintas que se pueden usar para crear formas de colisión:

* [Physics Editor](https://www.codeandweb.com/physicseditor/tutorials/how-to-create-physics-shapes-for-defold), de CodeAndWeb, se puede usar para crear objetos de juego con sprites y formas de colisión coincidentes.
* [Defold Polygon Editor](https://rossgrams.itch.io/defold-polygon-editor) se puede usar para crear formas de envolvente convexa.
* [Physics Body Editor](https://selimanac.github.io/physics-body-editor/) se puede usar para crear formas de envolvente convexa.


# Escalar formas de colisión
El objeto de colisión y sus formas heredan la escala del objeto de juego. Para desactivar este comportamiento, desmarca la casilla [Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) en la sección Physics de *game.project*. Ten en cuenta que solo se admite el escalado uniforme y que se usará el valor de escala más pequeño si la escala no es uniforme.

# Redimensionar formas de colisión
Las formas de un objeto de colisión se pueden redimensionar en tiempo de ejecución usando `physics.set_shape()`. Ejemplo:

```lua
-- definir datos de la forma de cápsula
local capsule_data = {
  type = physics.SHAPE_TYPE_CAPSULE,
  diameter = 10,
  height = 20,
}
physics.set_shape("#collisionobject", "my_capsule_shape", capsule_data)

-- definir datos de la forma de esfera
local sphere_data = {
  type = physics.SHAPE_TYPE_SPHERE,
  diameter = 10,
}
physics.set_shape("#collisionobject", "my_sphere_shape", sphere_data)

-- definir datos de la forma de caja
local box_data = {
  type = physics.SHAPE_TYPE_BOX,
  dimensions = vmath.vector3(10, 10, 5),
}
physics.set_shape("#collisionobject", "my_box_shape", box_data)
```

::: sidenote
Ya debe existir una forma del tipo correcto con el id especificado en el objeto de colisión.
:::

# Rotar formas de colisión

## Rotar formas de colisión en físicas 3D
Las formas de colisión en físicas 3D se pueden rotar alrededor de todos los ejes.


## Rotar formas de colisión en físicas 2D
Las formas de colisión en físicas 2D solo se pueden rotar alrededor del eje z. La rotación alrededor del eje x o y dará resultados incorrectos y debe evitarse, incluso al rotar 180 grados para básicamente voltear la forma a lo largo del eje x o y. Para voltear una forma física, se recomienda usar [`physics.set_hlip(url, flip)`](/ref/stable/physics/?#physics.set_hflip:url-flip) y [`physics.set_vlip(url, flip)`](/ref/stable/physics/?#physics.set_vflip:url-flip).


# Depuración
Puedes [activar la depuración de físicas](/manuals/debugging/#debugging-problems-with-physics) para ver las formas de colisión en tiempo de ejecución.
