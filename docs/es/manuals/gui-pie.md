---
title: Nodos Pie de GUI en Defold
brief: Este manual explica cómo usar nodos Pie en escenas GUI de Defold.
---

# Nodos Pie de GUI

Los nodos Pie se usan para crear objetos circulares o elipsoidales, desde círculos simples hasta sectores circulares y formas de anillo cuadradas.

## Crear un nodo Pie

Haz <kbd>click derecho</kbd> en la sección *Nodes* de *Outline* y selecciona <kbd>Add ▸ Pie</kbd>. El nuevo nodo Pie queda seleccionado y puedes modificar sus propiedades.

![Create pie node](images/gui-pie/create.png)

Las siguientes propiedades son exclusivas de los nodos Pie:

Inner Radius
: El radio interior del nodo, expresado a lo largo del eje X.

Outer Bounds
: La forma de los límites exteriores del nodo.

  - `Ellipse` extenderá el nodo hasta el radio exterior.
  - `Rectangle` extenderá el nodo hasta la caja delimitadora del nodo.

Perimeter Vertices
: El número de segmentos que se usará para construir la forma, expresado como el número de vértices necesarios para circunscribir por completo el perímetro de 360 grados del nodo.

Pie Fill Angle
: Qué parte del nodo Pie debe rellenarse. Se expresa como un ángulo en sentido antihorario que empieza desde la derecha.

![Properties](images/gui-pie/properties.png)

Si asignas una textura al nodo, la imagen de la textura se aplica plana, con las esquinas de la textura correlacionadas con las esquinas de la caja delimitadora del nodo.

## Modificar nodos Pie en tiempo de ejecución

Los nodos Pie responden a cualquier función genérica de manipulación de nodos para definir tamaño, pivote, color y demás. Existen algunas funciones y propiedades específicas de nodos Pie:

```lua
local pienode = gui.get_node("my_pie_node")

-- obtener el ángulo de relleno
local fill_angle = gui.get_fill_angle(pienode)

-- aumentar los vértices del perímetro
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- cambiar los límites exteriores
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- animar el radio interior
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
