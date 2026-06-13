---
title: Manual de animaciones flipbook en Defold
brief: Este manual describe cómo usar animaciones flipbook en Defold.
---

# Animación flipbook

Una animación flipbook consiste en una serie de imágenes estáticas que se muestran en sucesión. La técnica es muy similar a la animación tradicional en celuloide (ver http://en.wikipedia.org/wiki/Traditional_animation). La técnica ofrece oportunidades ilimitadas, ya que cada fotograma se puede manipular individualmente. Sin embargo, como cada fotograma se almacena en una imagen única, el consumo de memoria puede ser alto. La fluidez de la animación también depende del número de imágenes que se muestran por segundo, pero aumentar el número de imágenes normalmente también aumenta la cantidad de trabajo. Las animaciones flipbook de Defold se almacenan como imágenes individuales agregadas a un [Atlas](/manuals/atlas), o como un [Tile Source](/manuals/tilesource) con todos los fotogramas dispuestos en una secuencia horizontal.

  ![Animation sheet](images/animation/animsheet.png){.inline}
  ![Run loop](images/animation/runloop.gif){.inline}

## Reproducir animaciones flipbook

Los sprites y los nodos caja GUI pueden reproducir animaciones flipbook, y tienes mucho control sobre ellas en tiempo de ejecución.

Sprites
: Para ejecutar una animación durante el tiempo de ejecución, usa la función [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]). Consulta un ejemplo más abajo.

Nodos caja GUI
: Para ejecutar una animación durante el tiempo de ejecución, usa la función [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]). Consulta un ejemplo más abajo.

::: sidenote
El modo de reproducción once ping-pong reproducirá la animación hasta el último fotograma, luego invertirá el orden y reproducirá de vuelta hasta el **segundo** fotograma de la animación, no hasta el primer fotograma. Esto se hace para que encadenar animaciones sea más fácil.
:::

### Ejemplo de sprite

Supón que tu juego tiene una funcionalidad de "dodge" que permite al jugador presionar un botón específico para esquivar. Has creado cuatro animaciones para apoyar la funcionalidad con retroalimentación visual:

"idle"
: Una animación en bucle del personaje del jugador en reposo.

"dodge_idle"
: Una animación en bucle del personaje del jugador en reposo mientras está en la postura de esquivar.

"start_dodge"
: Una animación de transición que se reproduce una vez y lleva al personaje del jugador de estar de pie a esquivar.

"stop_dodge"
: Una animación de transición que se reproduce una vez y lleva al personaje del jugador de esquivar a estar de pie.

El siguiente script proporciona la lógica:

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" es nuestra acción de entrada
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- recuerda que estamos esquivando
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- ya no estamos esquivando
            self.dodge = false
        end
    end
end
```

### Ejemplo de nodo caja GUI

Al seleccionar una animación o imagen para un nodo, en realidad estás asignando la fuente de imagen (atlas o tile source) y la animación predeterminada de una sola vez. La fuente de imagen se define de forma estática en el nodo, pero la animación actual que se reproduce se puede cambiar en tiempo de ejecución. Las imágenes estáticas se tratan como animaciones de un fotograma, por lo que cambiar una imagen en tiempo de ejecución equivale a reproducir una animación flipbook distinta para el nodo:

```lua
function init(self)
    local character_node = gui.get_node("character")
    -- Esto requiere que el nodo tenga una animación predeterminada en el mismo atlas o tile source que
    -- la nueva animación/imagen que estamos reproduciendo.
    gui.play_flipbook(character_node, "jump_left")
end
```


## Callbacks de finalización

Las funciones `sprite.play_flipbook()` y `gui.play_flipbook()` admiten una función callback Lua opcional como último argumento. Esta función se llamará cuando la animación haya llegado al final. La función nunca se llama en animaciones en bucle. El callback se puede usar para activar eventos al finalizar una animación o para encadenar varias animaciones. Ejemplos:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    sprite.play_flipbook("#character", "jump_left", flipbook_done)
end
```

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    gui.play_flipbook(gui.get_node("character"), "jump_left", flipbook_done)
end
```
