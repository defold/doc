---
title: Optimización del rendimiento en tiempo de ejecución de un juego Defold
brief: Este manual describe cómo optimizar un juego Defold para que se ejecute a una tasa de frames alta y estable.
---

# Optimización de la velocidad en tiempo de ejecución
Antes de intentar optimizar un juego con el objetivo de que se ejecute a una tasa de frames alta y estable, necesitas saber dónde están tus cuellos de botella. ¿Qué está consumiendo realmente la mayor parte del tiempo en un frame de tu juego? ¿Es el renderizado? ¿Es la lógica del juego? ¿Es el gráfico de la escena? Para averiguarlo, se recomienda usar las herramientas de profiling integradas. Usa el [profiler en pantalla o web](/manuals/profiling/) para tomar muestras del rendimiento de tu juego y luego decidir si debes optimizar algo y qué optimizar. Cuando entiendas mejor qué consume tiempo, puedes empezar a abordar los problemas.

## Reduce el tiempo de ejecución de scripts
Reducir el tiempo de ejecución de scripts es necesario si el profiler muestra valores altos para el scope `Script`. Como regla general, por supuesto deberías intentar ejecutar la menor cantidad de código posible en cada frame. Ejecutar mucho código en `update()` y `on_input()` en cada frame probablemente afectará al rendimiento de tu juego, especialmente en dispositivos de gama baja. Algunas recomendaciones:

### Usa patrones de código reactivo
No consultes cambios constantemente si puedes recibir un callback. No animes algo manualmente ni realices una tarea que pueda delegarse al motor (por ejemplo, `go.animate)()` frente a animar algo manualmente).

### Reduce la recolección de basura
Si creas muchos objetos de vida corta, como tablas Lua, en cada frame, esto acabará activando el recolector de basura de Lua. Cuando esto ocurre, puede manifestarse como pequeños tirones o picos en el tiempo de frame. Reutiliza tablas cuando puedas e intenta de verdad evitar crear tablas Lua dentro de bucles y construcciones similares si es posible.

### Precalcula el hash de los ids de mensajes y acciones
Si haces mucho manejo de mensajes o tienes muchos eventos de input que gestionar, se recomienda precalcular el hash de las strings. Considera este fragmento de código:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

En el escenario anterior, la string con hash se volvería a crear cada vez que se recibe un mensaje. Esto se puede mejorar creando las versiones con hash una sola vez y usando esas versiones al manejar mensajes:

```lua
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

### Prefiere y almacena en caché las URL
El paso de mensajes o el direccionamiento de un objeto de juego (Game Object) o componente (Component) se puede hacer proporcionando un id como string o hash, o como una URL. Si se usa una string o un hash, internamente se traducirá a una URL. Por lo tanto, se recomienda almacenar en caché las URL que se usan con frecuencia para obtener el mejor rendimiento posible del sistema. Considera lo siguiente:

```lua
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- hacer algo con pos
```

En los tres casos se obtendría la posición de un objeto de juego con el id `enemy`. En el primer y segundo caso, el id (string o hash) se convertiría en una URL antes de usarse. Esto nos indica que es mejor almacenar las URL en caché y usar la versión en caché para obtener el mejor rendimiento posible:

```lua
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- hacer algo con pos
    end
```

## Reduce el tiempo que tarda en renderizarse un frame
Reducir el tiempo que tarda en renderizarse un frame es necesario si el profiler muestra valores altos en los scopes `Render` y `Render Script`. Hay varias cosas que considerar al intentar reducir el tiempo que tarda en renderizarse un frame:

* Reduce las draw calls: lee más sobre cómo reducir las draw calls en [esta publicación del foro](https://forum.defold.com/t/draw-calls-and-defold/4674)
* Reduce el overdraw
* Reduce la complejidad de los shaders: lee sobre optimizaciones GLSL en [este artículo de Khronos](https://www.khronos.org/opengl/wiki/GLSL_Optimizations). También puedes modificar los shaders predeterminados que usa Defold (se encuentran en `builtins/materials`) y reducir la precisión de los shaders para ganar algo de velocidad en dispositivos de gama baja. Todos los shaders usan precisión `highp` y cambiarla, por ejemplo, a `mediump` puede mejorar ligeramente el rendimiento en algunos casos.

## Reduce la complejidad del gráfico de la escena
Reducir la complejidad del gráfico de la escena es necesario si el profiler muestra valores altos en el scope `GameObject` y, más específicamente, en la muestra `UpdateTransform`. Algunas acciones que puedes tomar:

* Culling: desactiva objetos de juego (y sus componentes) si no están visibles actualmente. Cómo se determina esto depende mucho del tipo de juego. Para un juego 2D puede ser tan simple como desactivar siempre los objetos de juego que estén fuera de un área rectangular. Puedes usar un trigger de física para detectarlo o particionar tus objetos en buckets. Cuando sepas qué objetos desactivar o activar, hazlo enviando un mensaje `disable` o `enable` a cada objeto de juego.

## Frustum culling
El render script puede ignorar automáticamente el renderizado de componentes de objetos de juego que están fuera de una caja delimitadora definida (frustum). Aprende más sobre Frustum Culling en el [manual de Render Pipeline](/manuals/render/#frustum-culling).

# Optimizaciones específicas de plataforma

## Android Device Performance Framework
Android Dynamic Performance Framework es un conjunto de API que permite a los juegos interactuar de forma más directa con los sistemas de energía y temperatura de los dispositivos Android. Es posible monitorizar el comportamiento dinámico en sistemas Android y optimizar el rendimiento del juego a un nivel sostenible que no sobrecaliente los dispositivos. Usa la [extensión Android Dynamic Performance Framework](https://defold.com/extension-adpf/) para monitorizar y optimizar el rendimiento de tu juego Defold para dispositivos Android.
