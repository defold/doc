---
title: Componentes de texto Label en Defold
brief: Este manual explica cómo usar componentes Label para mostrar texto con objetos de juego en el mundo del juego.
---

# Label

Un componente *Label* renderiza una porción de texto en pantalla, en el espacio del juego. Por defecto se ordena y dibuja junto con todos los gráficos de sprites y tiles. El componente tiene un conjunto de propiedades que controla cómo se renderiza el texto. La GUI de Defold permite usar texto, pero puede ser complicado colocar elementos GUI en el mundo del juego. Los componentes Label facilitan esto.

## Crear un label

Para crear un componente Label, haz <kbd>click derecho</kbd> en el objeto de juego y selecciona <kbd>Add Component ▸ Label</kbd>.

![Add label](images/label/add_label.png)

(Si quieres instanciar varios labels desde la misma plantilla, también puedes crear un nuevo archivo de componente Label: haz <kbd>click derecho</kbd> en una carpeta en el navegador *Assets* y selecciona <kbd>New... ▸ Label</kbd>, luego añade el archivo como componente a cualquier objeto de juego)

![New label](images/label/label.png)

Define la propiedad *Font* con la fuente que quieres usar y asegúrate de definir la propiedad *Material* con un material que coincida con el tipo de fuente:

![Font and material](images/label/font_material.png)

## Propiedades de Label

Además de las propiedades *Id*, *Position*, *Rotation* y *Scale*, existen las siguientes propiedades específicas del componente:

*Text*
: El contenido de texto del label.

*Size*
: El tamaño del cuadro delimitador del texto. Si *Line Break* está activado, el ancho especifica en qué punto debe dividirse el texto.

*Color*
: El color del texto.

*Outline*
: El color del contorno.

*Shadow*
: El color de la sombra.

::: sidenote
Ten en cuenta que el material predeterminado tiene desactivado el renderizado de sombras por razones de rendimiento.
:::

*Leading*
: Un número de escala para el interlineado. Un valor de 0 no produce interlineado. El valor predeterminado es 1.

*Tracking*
: Un número de escala para el espaciado entre letras. El valor predeterminado es 0.

*Pivot*
: El pivote del texto. Úsalo para cambiar la alineación del texto (ver abajo).

*Blend Mode*
: El modo de mezcla que se usa al renderizar el label.

*Line Break*
: La alineación del texto sigue la configuración de pivote, y activar esta propiedad permite que el texto fluya en varias líneas. El ancho del componente determina dónde se ajustará el texto. Ten en cuenta que debe haber un espacio en el texto para que pueda dividirse.

*Font*
: El recurso de fuente que se usa para este label.

*Material*
: El material que se usa para renderizar este label. Asegúrate de seleccionar un material creado para el tipo de fuente que usas (bitmap, distance field o BMFont).

### Modos de mezcla
:[blend-modes](../shared/blend-modes.md)

### Pivote y alineación

Al definir la propiedad *Pivot*, puedes cambiar el modo de alineación del texto.

*Center*
: Si el pivote está definido como `Center`, `North` o `South`, el texto queda alineado al centro.

*Left*
: Si el pivote está definido como cualquiera de los modos `West`, el texto queda alineado a la izquierda.

*Right*
: Si el pivote está definido como cualquiera de los modos `East`, el texto queda alineado a la derecha.

![Text alignment](images/label/align.png)

## Manipulación en runtime

Puedes manipular labels en runtime obteniendo y definiendo el texto del label, así como sus distintas propiedades.

`color`
: El color del label (`vector4`)

`outline`
: El color del contorno del label (`vector4`)

`shadow`
: El color de la sombra del label (`vector4`)

`scale`
: La escala del label, ya sea un `number` para escalado uniforme o un `vector3` para escalado individual a lo largo de cada eje.

`size`
: El tamaño del label (`vector3`)

```lua
function init(self)
    -- Define el texto del componente "my_label" en el mismo objeto de juego
    -- que este script.
    label.set_text("#my_label", "New text")
end
```

```lua
function init(self)
    -- Define el color del componente "my_label" en el mismo objeto de juego
    -- que este script. El color es un valor RGBA almacenado en un vector4.
    local grey = vmath.vector4(0.5, 0.5, 0.5, 1.0)
    go.set("#my_label", "color", grey)

    -- ...y elimina el contorno definiendo su alfa como 0...
    go.set("#my_label", "outline.w", 0)

    -- ...y escálalo x2 a lo largo del eje x.
    local scale_x = go.get("#my_label", "scale.x")
    go.set("#my_label", "scale.x", scale_x * 2)
end
```

## Configuración del proyecto

El archivo *game.project* tiene algunas [configuraciones del proyecto](/manuals/project-settings#label) relacionadas con labels.
