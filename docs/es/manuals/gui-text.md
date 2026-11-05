---
title: Nodos de texto GUI de Defold
brief: Este manual describe cómo añadir texto a escenas GUI.
---

# Nodos de texto GUI {#gui-text-nodes}

Defold admite un tipo específico de nodo GUI que permite renderizar texto en una escena GUI. Cualquier recurso de fuente añadido a un proyecto puede usarse para renderizar nodos de texto.

La vista previa del editor admite la conformación del texto y el layout de derecha a izquierda mediante el renderizador de fuentes del motor. Consulta [compatibilidad con layout de texto](/manuals/font/#text-layout-support-eg-right-to-left) para conocer los ajustes necesarios de fuentes y App Manifest.

## Añadir nodos de texto {#adding-text-nodes}

Las fuentes que quieras usar en nodos de texto GUI deben añadirse al componente GUI. Haz click derecho en la carpeta *Fonts*, usa el menú superior <kbd>GUI</kbd> o presiona el atajo de teclado correspondiente.

![Fonts](images/gui-text/fonts.png)

Los nodos de texto tienen un conjunto de propiedades especiales:

*Font*
: Cualquier nodo de texto que crees debe tener definida la propiedad *Font*.

*Text*
: Esta propiedad contiene el texto mostrado.

*Line Break*
: La alineación del texto sigue la configuración del pivote y activar esta propiedad permite que el texto fluya en varias líneas. El ancho del nodo determina dónde se ajustará el texto.

## Fuentes vectoriales y emoji a color {#vector-fonts-and-color-emoji}

Sigue la [configuración de fuentes vectoriales](/manuals/font/#vector-fonts), agrega el recurso `.font` a *Fonts* de la escena GUI y selecciónalo en el nodo de texto. Establece el *Material* del recurso de fuente en `/builtins/fonts/font-vector.material`. Usa *Font Size* del nodo para controlar el tamaño mostrado.

Para emoji a color, completa también la [configuración de la fuente alternativa COLRv1 y su inclusión en el bundle](/manuals/font/#color-emoji). Crea un nodo de texto con el id `text`, deja su *Text* vacío y agrega lo siguiente al `.gui_script` de la escena GUI:

```lua
function init(self)
    local node = gui.get_node("text")
    local text = "Hello 😀 🍎 🚀"
    local font_resource = gui.get_font_resource(gui.get_font(node))
    -- Agrega la fuente alternativa una sola vez para este recurso de fuente compartido.
    font.add_font(font_resource, "/fonts/NotoColorEmoji-Regular.ttf")
    font.prewarm_text(font_resource, text, function(self, request_id, result, err)
        if result then
            gui.set_text(node, text)
        else
            print("Could not prepare GUI text:", err)
        end
    end)
end
```

[`gui.get_font()`](/ref/gui/#gui.get_font) devuelve el nombre de la fuente dentro de la escena GUI; [`gui.get_font_resource()`](/ref/gui/#gui.get_font_resource) resuelve ese nombre al recurso de fuente que usa `font.add_font()`. Los demás nodos y Label que comparten el recurso también reciben la fuente alternativa, por lo que debes inicializarla una sola vez. El texto se establece cuando la preparación termina correctamente.

## Alineación {#alignment}

Al configurar el pivote del nodo puedes cambiar el modo de alineación del texto.

*Center*
: Si el pivote está establecido en `Center`, `North` o `South`, el texto se alinea al centro.

*Left*
: Si el pivote está establecido en cualquiera de los modos `West`, el texto se alinea a la izquierda.

*Right*
: Si el pivote está establecido en cualquiera de los modos `East`, el texto se alinea a la derecha.

![Text alignment](images/gui-text/align.png)

## Modificar nodos de texto en runtime {#modifying-text-nodes-in-runtime}

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
