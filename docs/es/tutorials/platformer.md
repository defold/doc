---
title: Tutorial de Platformer en Defold
brief: En este artículo, recorres la implementación de un platformer 2D básico basado en tiles en Defold. Las mecánicas que aprenderás son moverse a la izquierda/derecha, saltar y caer.
---

# Platformer

En este artículo, recorremos la implementación de un platformer 2D básico basado en tiles en Defold. Las mecánicas que aprenderemos son moverse a la izquierda/derecha, saltar y caer.

Hay muchas maneras distintas de crear un platformer. Rodrigo Monteiro ha escrito un análisis exhaustivo sobre el tema y más [aquí](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/).

Te recomendamos mucho leerlo si eres nuevo creando platformers, ya que contiene mucha información valiosa. Entraremos en un poco más de detalle sobre algunos de los métodos descritos y cómo implementarlos en Defold. Sin embargo, todo debería ser fácil de portar a otras plataformas y lenguajes (en Defold usamos Lua).

Asumimos que estás familiarizado con algo de matemática vectorial (álgebra lineal). Si no lo estás, es buena idea estudiarla, ya que es enormemente útil para el desarrollo de juegos. David Rosen de Wolfire escribió una serie muy buena sobre ello [aquí](http://blog.wolfire.com/2009/07/linear-algebra-for-game-developers-part-1/).

Si ya estás usando Defold, puedes crear un nuevo proyecto basado en el proyecto de plantilla _Platformer_ y experimentar con él mientras lees este artículo.

::: sidenote
Algunos lectores han mencionado que nuestro método sugerido no es posible con la implementación predeterminada de Box2D. Hicimos algunas modificaciones a Box2D para que esto funcione:

Las colisiones entre objetos cinemáticos y estáticos se ignoran. Cambia las comprobaciones en `b2Body::ShouldCollide` y `b2ContactManager::Collide`.

Además, la distancia de contacto (llamada separación en Box2D) no se entrega a la función callback.
Agrega un miembro de distancia a `b2ManifoldPoint` y asegúrate de que se actualice en las funciones `b2Collide*`.
:::

## Detección de colisiones

La detección de colisiones es necesaria para evitar que el jugador atraviese la geometría del nivel.
Hay varias maneras de tratar esto según tu juego y sus requisitos específicos.
Una de las formas más sencillas, si es posible, es dejar que un motor de físicas se encargue.
En Defold usamos el motor de físicas [Box2D](http://box2d.org/) para juegos 2D.
La implementación predeterminada de Box2D no tiene todas las funcionalidades necesarias; consulta el final de este artículo para ver cómo la modificamos.

Un motor de físicas almacena los estados de los objetos físicos junto con sus formas para simular comportamiento físico. También reporta colisiones mientras simula, para que el juego pueda reaccionar cuando ocurren. En la mayoría de los motores de físicas hay tres tipos de objetos: objetos _static_, _dynamic_ y _kinematic_ (estos nombres podrían ser distintos en otros motores de físicas). También hay otros tipos de objetos, pero los ignoraremos por ahora.

- Un objeto *static* nunca se moverá (por ejemplo, la geometría del nivel).
- Un objeto *dynamic* recibe la influencia de fuerzas y torques que se transforman en velocidades durante la simulación.
- Un objeto *kinematic* es controlado por la lógica de la aplicación, pero aun así afecta a otros objetos dynamic.

En un juego como este, buscamos algo que se parezca al comportamiento físico del mundo real, pero tener controles responsivos y mecánicas equilibradas es mucho más importante. Un salto que se siente bien no necesita ser físicamente preciso ni actuar bajo gravedad real. Sin embargo, [este](http://hypertextbook.com/facts/2007/mariogravity.shtml) análisis muestra que la gravedad en los juegos de Mario se acerca más a una gravedad de 9.8 m/s<sup>2</sup> con cada versión. :-)

Es importante que tengamos control total de lo que ocurre para poder diseñar y ajustar las mecánicas hasta lograr la experiencia prevista. Por eso elegimos modelar el personaje del jugador como un objeto cinemático. Así podemos mover el personaje del jugador como queramos, sin tener que tratar con fuerzas físicas. Esto significa que tendremos que resolver nosotros mismos la separación entre el personaje y la geometría del nivel (más sobre esto luego), pero es una desventaja que estamos dispuestos a aceptar. Representaremos al personaje del jugador con una forma de caja en el mundo físico.

## Movimiento

Ahora que hemos decidido que el personaje del jugador estará representado por un objeto cinemático, podemos moverlo libremente definiendo la posición. Empecemos con el movimiento izquierda/derecha.

El movimiento estará basado en aceleración, para dar una sensación de peso al personaje. Como en un vehículo normal, la aceleración define qué tan rápido puede el personaje del jugador alcanzar la velocidad máxima y cambiar de dirección. La aceleración actúa durante el paso de tiempo del frame---normalmente proporcionado en un parámetro `dt` (delta-`t`)---y luego se suma a la velocidad. De forma similar, la velocidad actúa durante el frame y la traslación resultante se suma a la posición. En matemáticas, esto se llama [integración en el tiempo](http://en.wikipedia.org/wiki/Integral).

![Approximative velocity integration](images/platformer/integration.png)

Las dos líneas verticales marcan el inicio y el final del frame. La altura de las líneas es la velocidad que tiene el personaje del jugador en esos dos instantes. Llamemos a estas velocidades `v0` y `v1` . `v1` se obtiene aplicando la aceleración (la pendiente de la curva) durante el paso de tiempo `dt`:

![Equation of velocity](images/platformer/equationofvelocity.png)

El área naranja es la traslación que debemos aplicar al personaje del jugador durante el frame actual. Geométricamente, podemos aproximar el área como:

![Equation of translation](images/platformer/equationoftranslation.png)

Así es como integramos la aceleración y la velocidad para mover el personaje en el bucle update:

1. Determina la velocidad objetivo según la entrada
2. Calcula la diferencia entre nuestra velocidad actual y la velocidad objetivo
3. Define la aceleración para trabajar en la dirección de la diferencia
4. Calcula el cambio de velocidad de este frame (`dv` es abreviatura de delta-velocity), como arriba:

    ```lua
    local dv = acceleration * dt
    ```

5. Comprueba si `dv` excede la diferencia de velocidad prevista; en ese caso, limítalo
6. Guarda la velocidad actual para usarla más tarde (`self.velocity`, que ahora mismo es la velocidad usada en el frame anterior):

    ```lua
    local v0 = self.velocity
    ```

7. Calcula la nueva velocidad sumando el cambio de velocidad:

    ```lua
    self.velocity = self.velocity + dv
    ```

8. Calcula la traslación en x de este frame integrando la velocidad, como arriba:

    ```lua
    local dx = (v0 + self.velocity) * dt * 0.5
    ```

9. Aplícala al personaje del jugador

Si no estás seguro de cómo manejar input en Defold, hay una guía sobre eso [aquí](/manuals/input).

En esta etapa, podemos mover el personaje a izquierda y derecha y tener una sensación pesada y suave en los controles. Ahora, ¡agreguemos gravedad!

La gravedad también es una aceleración, pero afecta al jugador a lo largo del eje y. Esto significa que se aplicará de la misma manera que la aceleración de movimiento descrita arriba. Si simplemente cambiamos los cálculos anteriores a vectores y nos aseguramos de incluir la gravedad en el componente y de la aceleración en el paso 3), funcionará sin más. ¡Hay que amar la matemática vectorial! :-)

## Respuesta a colisiones

Ahora nuestro personaje del jugador puede moverse y caer, así que es momento de mirar las respuestas a colisiones.
Obviamente necesitamos aterrizar y movernos a lo largo de la geometría del nivel. Usaremos los puntos de contacto proporcionados por el motor de físicas para asegurarnos de no solaparnos nunca con nada.

Un punto de contacto lleva una _normal_ del contacto (apuntando hacia afuera desde el objeto con el que chocamos, aunque podría ser diferente en otros motores) y también una _distancia_, que mide cuánto hemos penetrado el otro objeto. Esto es todo lo que necesitamos para separar al jugador de la geometría del nivel.
Como usamos una caja, podríamos obtener múltiples puntos de contacto durante un frame. Esto ocurre, por ejemplo, cuando dos esquinas de la caja intersectan el suelo horizontal, o cuando el jugador se mueve hacia una esquina.

![Contact normals acting on the player character](images/platformer/collision.png)

Para evitar hacer la misma corrección varias veces, acumulamos las correcciones en un vector para asegurarnos de no sobrecompensar. Eso haría que termináramos demasiado lejos del objeto con el que chocamos. En la imagen de arriba puedes ver que actualmente tenemos dos puntos de contacto, visualizados por las dos flechas (normales). La distancia de penetración es la misma para ambos contactos; si la usáramos a ciegas cada vez, terminaríamos moviendo al jugador el doble de la cantidad prevista.

::: sidenote
Es importante reiniciar las correcciones acumuladas cada frame al vector 0.
Pon algo como esto al final de la función `update()`:
`self.corrections = vmath.vector3()`
:::

Asumiendo que hay una función callback que se llamará para cada punto de contacto, así se hace la separación en esa función:

```lua
local proj = vmath.dot(self.correction, normal) -- <1>
local comp = (distance - proj) * normal -- <2>
self.correction = self.correction + comp -- <3>
go.set_position(go.get_position() + comp) -- <4>
```

1. Proyecta el vector de corrección sobre la normal de contacto (el vector de corrección es el vector 0 para el primer punto de contacto)
2. Calcula la compensación que necesitamos hacer para este punto de contacto
3. Súmala al vector de corrección
4. Aplica la compensación al personaje del jugador

También necesitamos cancelar la parte de la velocidad del jugador que se mueve hacia el punto de contacto:

```lua
proj = vmath.dot(self.velocity, message.normal) -- <1>
if proj < 0 then
    self.velocity = self.velocity - proj * message.normal -- <2>
end
```
1. Proyecta la velocidad sobre la normal
2. Si la proyección es negativa, significa que parte de la velocidad apunta hacia el punto de contacto; elimina ese componente en ese caso

## Saltar

Ahora que podemos correr sobre la geometría del nivel y caer, ¡es momento de saltar! El salto en platformers se puede hacer de muchas formas distintas. En este juego buscamos algo similar a Super Mario Bros y Super Meat Boy. Al saltar, el personaje del jugador es impulsado hacia arriba por un impulso, que básicamente es una velocidad fija.

La gravedad tirará continuamente del personaje hacia abajo otra vez, lo que da como resultado un arco de salto agradable. Mientras está en el aire, el jugador todavía puede controlar al personaje. Si el jugador suelta el botón de salto antes de la cima del arco de salto, la velocidad hacia arriba se escala hacia abajo para detener el salto antes de tiempo.

1. Cuando se presiona la entrada, haz:

    ```lua
    -- jump_takeoff_speed is a constant defined elsewhere
    self.velocity.y = jump_takeoff_speed
    ```

    Esto solo debe hacerse cuando la entrada se _presiona_, no en cada frame en que se mantiene _presionada_ continuamente.

2. Cuando se suelta la entrada, haz:

    ```lua
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
    ```

ExciteMike ha creado algunos gráficos muy buenos de los arcos de salto en [Super Mario Bros 3](http://meyermike.com/wp/?p=175) y [Super Meat Boy](http://meyermike.com/wp/?p=160) que vale la pena revisar.

## Geometría del nivel

La geometría del nivel son las formas de colisión del entorno con las que colisiona el personaje del jugador (y posiblemente otras cosas). En Defold hay dos maneras de crear esta geometría.

Puedes crear formas de colisión separadas sobre los niveles que construyes. Este método es muy flexible y permite posicionamiento fino de gráficos. Es especialmente útil si quieres pendientes suaves.
El juego [Braid](http://braid-game.com/) usó este método para construir niveles, y también es el método con el que se construye el nivel de ejemplo de este tutorial. Así se ve en el editor Defold:

![The Defold Editor with the level geometry and player placed into the world](images/platformer/editor.png)

Otra opción es construir niveles a partir de tiles y hacer que el editor genere automáticamente las formas físicas, basadas en los gráficos de los tiles. Esto significa que la geometría del nivel se actualizará automáticamente cuando cambies los niveles, lo que puede ser extremadamente útil.

Los tiles colocados tendrán sus formas físicas fusionadas automáticamente en una sola si se alinean.
Esto elimina los huecos que pueden hacer que tu personaje del jugador se detenga o rebote al deslizarse por varios tiles horizontales. Esto se hace reemplazando los polígonos de tiles con formas de borde en Box2D en tiempo de carga.

![Multiple tile-based polygons stitched into one](images/platformer/stitching.png)

Arriba hay un ejemplo donde creamos cinco tiles vecinos a partir de una pieza de los gráficos del platformer. En la imagen puedes ver cómo los tiles colocados (arriba) corresponden a una sola forma que ha sido unida en una (contorno gris inferior).

Consulta nuestras guías sobre [físicas](/manuals/physics) y [tiles](/manuals/2dgraphics) para más información.

## Palabras finales

Si quieres más información sobre mecánicas de platformer, aquí hay una cantidad impresionantemente enorme de información sobre las físicas en [Sonic](http://info.sonicretro.org/Sonic_Physics_Guide).

Si pruebas nuestro proyecto de plantilla en un dispositivo iOS o con mouse, el salto puede sentirse realmente incómodo.
Es solo nuestro débil intento de crear plataformas con entrada de un solo toque. :-)

No hablamos de cómo manejamos las animaciones en este juego. Puedes hacerte una idea revisando *player.script* más abajo; busca la función `update_animations()`.

¡Esperamos que hayas encontrado útil esta información!
¡Por favor crea un gran platformer para que todos podamos jugarlo! <3

## Código

Este es el contenido de *player.script*:

```lua
-- player.script

-- estos son los ajustes para las mecánicas, siéntete libre de cambiarlos para otra sensación
-- aceleración para moverse a derecha/izquierda
local move_acceleration = 3500
-- factor de aceleración a usar cuando está en el aire
local air_acceleration_factor = 0.8
-- velocidad máxima derecha/izquierda
local max_speed = 450
-- gravedad que tira del jugador hacia abajo en unidades de pixel
local gravity = -1000
-- velocidad de despegue al saltar en unidades de pixel
local jump_takeoff_speed = 550
-- tiempo dentro del cual debe ocurrir un doble toque para considerarse un salto (solo se usa para controles de mouse/toque)
local touch_jump_timeout = 0.2

-- prehashear ids mejora el rendimiento
local msg_contact_point_response = hash("contact_point_response")
local msg_animation_done = hash("animation_done")
local group_obstacle = hash("obstacle")
local input_left = hash("left")
local input_right = hash("right")
local input_jump = hash("jump")
local input_touch = hash("touch")
local anim_run = hash("run")
local anim_idle = hash("idle")
local anim_jump = hash("jump")
local anim_fall = hash("fall")

function init(self)
    -- esto nos permite manejar input en este script
    msg.post(".", "acquire_input_focus")

    -- velocidad inicial del jugador
    self.velocity = vmath.vector3(0, 0, 0)
    -- variable de apoyo para llevar registro de colisiones y separación
    self.correction = vmath.vector3()
    -- si el jugador está sobre el suelo o no
    self.ground_contact = false
    -- input de movimiento en el rango [-1,1]
    self.move_input = 0
    -- la animación que se reproduce actualmente
    self.anim = nil
    -- temporizador que controla la ventana de salto al usar mouse/toque
    self.touch_jump_timer = 0
end

local function play_animation(self, anim)
    -- solo reproduce animaciones que no se estén reproduciendo ya
    if self.anim ~= anim then
        -- dile al sprite que reproduzca la animación
        sprite.play_flipbook("#sprite", anim)
        -- recuerda qué animación se está reproduciendo
        self.anim = anim
    end
end

local function update_animations(self)
    -- asegúrate de que el personaje del jugador mire hacia el lado correcto
    sprite.set_hflip("#sprite", self.move_input < 0)
    -- asegúrate de que se esté reproduciendo la animación correcta
    if self.ground_contact then
        if self.velocity.x == 0 then
            play_animation(self, anim_idle)
        else
            play_animation(self, anim_run)
        end
    else
        if self.velocity.y > 0 then
            play_animation(self, anim_jump)
        else
            play_animation(self, anim_fall)
        end
    end
end

function update(self, dt)
    -- determina la velocidad objetivo según input
    local target_speed = self.move_input * max_speed
    -- calcula la diferencia entre nuestra velocidad actual y la velocidad objetivo
    local speed_diff = target_speed - self.velocity.x
    -- la aceleración completa que se integrará durante este frame
    local acceleration = vmath.vector3(0, gravity, 0)
    if speed_diff ~= 0 then
        -- define la aceleración para trabajar en la dirección de la diferencia
        if speed_diff < 0 then
            acceleration.x = -move_acceleration
        else
            acceleration.x = move_acceleration
        end
        -- reduce la aceleración cuando está en el aire para dar una sensación más lenta
        if not self.ground_contact then
            acceleration.x = air_acceleration_factor * acceleration.x
        end
    end
    -- calcula el cambio de velocidad de este frame (dv es abreviatura de delta-velocity)
    local dv = acceleration * dt
    -- comprueba si dv excede la diferencia de velocidad prevista; en ese caso, limítalo
    if math.abs(dv.x) > math.abs(speed_diff) then
        dv.x = speed_diff
    end
    -- guarda la velocidad actual para usarla más tarde
    -- (self.velocity, que ahora mismo es la velocidad usada en el frame anterior)
    local v0 = self.velocity
    -- calcula la nueva velocidad sumando el cambio de velocidad
    self.velocity = self.velocity + dv
    -- calcula la traslación de este frame integrando la velocidad
    local dp = (v0 + self.velocity) * dt * 0.5
    -- aplícala al personaje del jugador
    go.set_position(go.get_position() + dp)

    -- actualiza el temporizador de salto
    if self.touch_jump_timer > 0 then
        self.touch_jump_timer = self.touch_jump_timer - dt
    end

    update_animations(self)

    -- reinicia estado volátil
    self.correction = vmath.vector3()
    self.move_input = 0
    self.ground_contact = false

end

local function handle_obstacle_contact(self, normal, distance)
    -- proyecta el vector de corrección sobre la normal de contacto
    -- (el vector de corrección es el vector 0 para el primer punto de contacto)
    local proj = vmath.dot(self.correction, normal)
    -- calcula la compensación que necesitamos hacer para este punto de contacto
    local comp = (distance - proj) * normal
    -- súmala al vector de corrección
    self.correction = self.correction + comp
    -- aplica la compensación al personaje del jugador
    go.set_position(go.get_position() + comp)
    -- comprueba si la normal apunta suficientemente hacia arriba para considerar que el jugador está en el suelo
    -- (0.7 equivale aproximadamente a 45 grados de desviación desde una dirección puramente vertical)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- proyecta la velocidad sobre la normal
    proj = vmath.dot(self.velocity, normal)
    -- si la proyección es negativa, significa que parte de la velocidad apunta hacia el punto de contacto
    if proj < 0 then
        -- elimina ese componente en ese caso
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    -- comprueba si recibimos un mensaje de punto de contacto
    if message_id == msg_contact_point_response then
        -- comprueba que el objeto sea algo que consideramos un obstáculo
        if message.group == group_obstacle then
            handle_obstacle_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- solo permite saltar desde el suelo
    -- (extiende esto con un contador para hacer cosas como dobles saltos)
    if self.ground_contact then
        -- define la velocidad de despegue
        self.velocity.y = jump_takeoff_speed
        -- reproduce animación
        play_animation(self, anim_jump)
    end
end

local function abort_jump(self)
    -- corta el salto si todavía estamos subiendo
    if self.velocity.y > 0 then
        -- reduce la velocidad hacia arriba
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == input_left then
        self.move_input = -action.value
    elseif action_id == input_right then
        self.move_input = action.value
    elseif action_id == input_jump then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    elseif action_id == input_touch then
        -- muévete hacia el punto de toque
        local diff = action.x - go.get_position().x
        -- solo entrega input cuando está lejos (más de 10 pixels)
        if math.abs(diff) > 10 then
            -- desacelera cuando está a menos de 100 pixels
            self.move_input = diff / 100
            -- limita input a [-1,1]
            self.move_input = math.min(1, math.max(-1, self.move_input))
        end
        if action.released then
            -- empieza a medir el tiempo desde la última liberación para ver si estamos por saltar
            self.touch_jump_timer = touch_jump_timeout
        elseif action.pressed then
            -- salta con doble toque
            if self.touch_jump_timer > 0 then
                jump(self)
            end
        end
    end
end
```
