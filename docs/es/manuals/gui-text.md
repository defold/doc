---
title: Nodos de texto GUI de Defold
brief: Este manual describe cómo añadir texto a escenas GUI.
---

# Nodos de texto GUI

Defold admite un tipo específico de nodo GUI que permite renderizar texto en una escena GUI. Cualquier recurso de fuente añadido a un proyecto puede usarse para renderizar nodos de texto.

## Añadir nodos de texto

Las fuentes que quieras usar en nodos de texto GUI deben añadirse al componente GUI. Haz click derecho en la carpeta *Fonts*, usa el menú superior <kbd>GUI</kbd> o presiona el atajo de teclado correspondiente.

![Fonts](images/gui-text/fonts.png)

Los nodos de texto tienen un conjunto de propiedades especiales:

*Font*
: Cualquier nodo de texto que crees debe tener definida la propiedad *Font*.

*Text*
: Esta propiedad contiene el texto mostrado.

*Line Break*
: La alineación del texto sigue la configuración del pivote y activar esta propiedad permite que el texto fluya en varias líneas. El ancho del nodo determina dónde se ajustará el texto.

## Alineación

Al configurar el pivote del nodo puedes cambiar el modo de alineación del texto.

*Center*
: Si el pivote está establecido en `Center`, `North` o `South`, el texto se alinea al centro.

*Left*
: Si el pivote está establecido en cualquiera de los modos `West`, el texto se alinea a la izquierda.

*Right*
: Si el pivote está establecido en cualquiera de los modos `East`, el texto se alinea a la derecha.

![Text alignment](images/gui-text/align.png)

## Modificar nodos de texto en runtime

Los nodos de texto responden a cualquier función genérica de manipulación de nodos para definir tamaño, pivote, color, etc. Existen algunas funciones exclusivas para nodos de texto:

* Para cambiar la fuente de un nodo de texto, usa la función [`gui.set_font()`](/ref/gui/#gui.set_font).
* Para cambiar el comportamiento del salto de línea de un nodo de texto, usa la función [`gui.set_line_break()`](/ref/gui/#gui.set_line_break).
* Para cambiar el contenido de un nodo de texto, usa la función [`gui.set_text()`](/ref/gui/#gui.set_text).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("set_score") then
        local s = gui.get_node("score")
        gui.set_text(s, message.score)
    end
end
```
