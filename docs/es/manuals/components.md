---
title: Componentes de objetos de juego
brief: Este manual ofrece una visión general de los componentes y de cómo usarlos.
---

#  Componentes

:[components](../shared/components.md)

## Tipos de componentes

Defold admite los siguientes tipos de componentes:

* [Collection factory](/manuals/collection-factory) - Genera colecciones
* [Collection proxy](/manuals/collection-proxy) - Carga y descarga colecciones
* [Collision object](/manuals/physics) - Físicas 2D y 3D
* [Camera](/manuals/camera) - Cambia la ventana de visualización y la proyección del mundo del juego
* [Factory](/manuals/factory) - Genera objetos de juego
* [GUI](/manuals/gui) - Renderiza una interfaz gráfica de usuario
* [Label](/manuals/label) - Renderiza un fragmento de texto
* [Light](/manuals/light) - Añade datos de iluminación para los shaders
* [Mesh](/manuals/mesh) Muestra un mesh 3D (con creación y manipulación en tiempo de ejecución)
* [Model](/manuals/model) Muestra un modelo 3D (con animaciones opcionales)
* [Particle FX](/manuals/particlefx) - Genera partículas
* [Script](/manuals/script) - Añade lógica del juego
* [Sound](/manuals/sound) - Reproduce sonido o música
* [Sprite](/manuals/sprite) - Muestra una imagen 2D (con animación flipbook opcional)
* [Tilemap](/manuals/tilemap) - Muestra una cuadrícula de tiles

Se pueden añadir componentes adicionales mediante extensiones:

* [Rive model](/extension-rive) - Renderiza una animación Rive
* [Spine model](/extension-spine) - Renderiza una animación Spine


## Habilitar y deshabilitar componentes

Los componentes de un objeto de juego se habilitan cuando se crea el objeto de juego. Si quieres deshabilitar un componente, esto se hace enviando un mensaje [`disable`](/ref/go/#disable) al componente:

```lua
-- deshabilita el componente con id 'weapon' en el mismo objeto de juego que este script
msg.post("#weapon", "disable")

-- deshabilita el componente con id 'shield' en el objeto de juego 'enemy'
msg.post("enemy#shield", "disable")

-- deshabilita todos los componentes del objeto de juego actual
msg.post(".", "disable")

-- deshabilita todos los componentes del objeto de juego 'enemy'
msg.post("enemy", "disable")
```

Para volver a habilitar un componente, puedes enviar un mensaje [`enable`](/ref/go/#enable) al componente:

```lua
-- habilita el componente con id 'weapon'
msg.post("#weapon", "enable")
```

## Propiedades de los componentes

Todos los tipos de componentes de Defold tienen propiedades diferentes. El [panel Properties](/manuals/editor/#the-editor-views) del editor mostrará las propiedades del componente seleccionado actualmente en el [panel Outline](/manuals/editor/#the-editor-views). Consulta los manuales de los distintos tipos de componentes para aprender más sobre las propiedades disponibles.

## Posición, rotación y escala de los componentes

Los componentes visuales suelen tener una propiedad de posición y una de rotación, y con frecuencia también una propiedad de escala. Estas propiedades se pueden cambiar desde el editor y, en casi todos los casos, no se pueden cambiar en tiempo de ejecución (la única excepción es la escala de los componentes sprite y label, que se puede cambiar en tiempo de ejecución).

Si necesitas cambiar la posición, la rotación o la escala de un componente en tiempo de ejecución, modifica en su lugar la posición, la rotación o la escala del objeto de juego al que pertenece el componente. Esto tiene el efecto secundario de que todos los componentes del objeto de juego se verán afectados. Si quieres manipular solo un componente de entre muchos adjuntos a un objeto de juego, se recomienda mover el componente en cuestión a un objeto de juego separado y añadirlo como objeto de juego hijo al objeto de juego al que pertenecía originalmente.

## Orden de dibujo de los componentes

El orden de dibujo de los componentes visuales depende de dos cosas:

### Predicados del script de render
A cada componente se le asigna un [material](/manuals/material/) y cada material tiene una o más etiquetas (tags). El script de render, a su vez, define una serie de predicados, cada uno coincidente con una o más etiquetas de material. En la función *update()* del script de render, [los predicados se dibujan uno por uno](/manuals/render/#render-predicates) y se dibujarán los componentes que coincidan con las etiquetas definidas en cada predicado. El script de render predeterminado primero dibujará sprites y tilemaps en una pasada, luego efectos de partículas en otra pasada, ambos en espacio del mundo. Después, el script de render procederá a dibujar componentes GUI en una pasada separada en espacio de pantalla.

### Valor Z del componente
Todos los objetos de juego y componentes se posicionan en espacio 3D, con posiciones expresadas como objetos `vector3`. Cuando ves el contenido gráfico de tu juego en 2D, los valores X e Y determinan la posición de un objeto sobre los ejes de "anchura" y "altura", y la posición Z determina la posición sobre el eje de "profundidad". La posición Z te permite controlar la visibilidad de objetos superpuestos: un sprite con un valor Z de 1 aparecerá delante de un sprite en la posición Z 0. De forma predeterminada, Defold usa un sistema de coordenadas que permite valores Z entre -1 y 1:

![modelo](images/graphics/z-order.png)

Los componentes que coinciden con un [predicado de render](/manuals/render/#render-predicates) se dibujan juntos, y el orden en que se dibujan depende del valor Z final del componente. El valor Z final de un componente es la suma de los valores Z del propio componente, del objeto de juego al que pertenece y del valor Z de cualquier objeto de juego padre.

::: sidenote
El orden en que se dibujan múltiples componentes GUI **no** lo determina el valor Z de los componentes GUI. El orden de dibujo de los componentes GUI se controla con la función [gui.set_render_order()](/ref/gui/#gui.set_render_order:order).
:::

Ejemplo: Dos objetos de juego A y B. B es hijo de A. B tiene un componente sprite.

| Elemento | Valor Z |
|----------|---------|
| A        | 2       |
| B        | 1       |
| B#sprite | 0.5     |

![](images/graphics/component-hierarchy.png)

Con la jerarquía anterior, el valor Z final del componente sprite en B es 2 + 1 + 0.5 = 3.5.

::: important
Si dos componentes tienen exactamente el mismo valor Z, el orden no está definido y puedes acabar con componentes que parpadean alternándose, o con componentes que se renderizan en un orden en una plataforma y en otro orden en otra plataforma.

El script de render define un plano cercano y uno lejano para los valores Z. Cualquier componente con un valor Z que quede fuera de este rango no se renderizará. El rango predeterminado es de -1 a 1, pero [se puede cambiar fácilmente](/manuals/render/#default-view-projection). La precisión numérica de los valores Z con un límite cercano y lejano de -1 y 1 es muy alta. Al trabajar con assets 3D, puede que necesites cambiar los límites cercano y lejano de la proyección predeterminada en un script de render personalizado. Consulta el [manual de render](/manuals/render/) para más información.
:::


:[Component max count optimizations](../shared/component-max-count-optimizations.md)
