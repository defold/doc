---
title: Input de teclas y texto en Defold
brief: Este manual explica cómo funciona el input de teclas y texto.
---

::: sidenote
Se recomienda que te familiarices con la forma general en que funciona el input en Defold, cómo recibir input y en qué orden se recibe en tus archivos script. Aprende más sobre el sistema de input en el [manual de visión general del input](/manuals/input).
:::

# Triggers de teclas
Los triggers de teclas permiten vincular input de teclado de una sola tecla a acciones del juego. Cada tecla se mapea por separado a una acción correspondiente. Los triggers de teclas se usan para asociar botones específicos con funciones específicas, como el movimiento del personaje con las teclas de flecha o WASD. Si necesitas leer input arbitrario de teclado, usa triggers de texto (ver abajo).

![](images/input/key_bindings.png)

```lua
function on_input(self, action_id, action)
    if action_id == hash("left") then
        if action.pressed then
            -- empezar a moverse a la izquierda
        elseif action.released then
            -- dejar de moverse a la izquierda
        end
    end
end
```

# Triggers de texto
Los triggers de texto se usan para leer input de texto arbitrario. Hay dos tipos de triggers de texto: texto y texto marcado.

![](images/input/text_bindings.png)

## Texto
`text` captura el input de texto normal. Define el campo `text` de la tabla de acción como un string que contiene el carácter escrito. La acción solo se dispara al presionar el botón; no se envía ninguna acción `release` ni `repeated`.

```lua
function on_input(self, action_id, action)
    if action_id == hash("text") then
        -- Concatena el carácter escrito al nodo "user"...
        local node = gui.get_node("user")
        local name = gui.get_text(node)
        name = name .. action.text
        gui.set_text(node, name)
    end
end
```

## Texto marcado
`marked-text` se usa principalmente para teclados asiáticos, donde varias pulsaciones de teclas pueden mapearse a una sola entrada. Por ejemplo, con el teclado "Japanese-Kana" de iOS, el usuario puede escribir combinaciones y la parte superior del teclado mostrará símbolos disponibles o secuencias de símbolos que se pueden introducir.

![Input de texto marcado](images/input/marked_text.png)

- Cada pulsación de tecla genera una acción separada y define el campo de acción `text` con la secuencia de símbolos introducida actualmente (el "texto marcado").
- Cuando el usuario selecciona un símbolo o una combinación de símbolos, se envía una acción de trigger de tipo `text` separada (siempre que se haya configurado una en la lista de bindings de input). La acción separada define el campo de acción `text` con la secuencia final de símbolos.
