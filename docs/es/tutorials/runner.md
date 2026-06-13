---
title: Tutorial Endless runner
brief: En este tutorial comienzas con un proyecto vacío y construyes un juego runner completo con un personaje animado, colisión física, pickups y puntuación.
---

# Tutorial Runner

En este tutorial empezamos con un proyecto vacío y construimos un juego runner completo con un personaje animado, colisión física, pickups y puntuación.

Hay mucho que asimilar al aprender un motor de juegos nuevo, así que creamos este tutorial para ayudarte a empezar. Es un tutorial bastante completo que recorre cómo funcionan el motor y el editor. Asumimos que tienes cierta familiaridad con la programación.

Si necesitas una introducción a la programación Lua, revisa nuestro [manual Lua en Defold](/manuals/lua).

Si sientes que este tutorial es demasiado para empezar, revisa nuestra [página de tutoriales](//www.defold.com/tutorials), donde tenemos una selección de tutoriales de dificultad variada.

Si prefieres ver tutoriales en video, revisa [la versión en video en Youtube](https://www.youtube.com/playlist?list=PLXsXu5srjNlxtYPQ_YJQSxJG2AN9OVS5b).

Usamos assets de juego de otros dos tutoriales, con algunas modificaciones pequeñas. El tutorial se divide en varios pasos, donde cada parte nos lleva un paso importante hacia el juego final.

El resultado final será un juego donde controlas un personaje héroe que corre por un entorno, recogiendo monedas y evitando obstáculos. El personaje héroe corre a velocidad fija y el jugador controla solo el salto del héroe pulsando un único botón (o tocando la pantalla en un dispositivo móvil). El nivel consiste en un flujo interminable de plataformas sobre las que saltar, y monedas para recoger.

Si en algún punto te quedas atascado en este tutorial o al crear tu juego, no dudes en pedirnos ayuda en el [Defold Forum](//forum.defold.com). En el foro puedes discutir sobre Defold, pedir ayuda al equipo de Defold, ver cómo otros desarrolladores de juegos resolvieron sus problemas y encontrar nueva inspiración. Empieza ahora.

::: sidenote
A lo largo del tutorial, las descripciones detalladas sobre conceptos y cómo hacer ciertos momentos se marcan como este párrafo. Si sientes que estas secciones entran en demasiado detalle, puedes saltarlas.
:::

Así que empecemos. Esperamos que te diviertas mucho recorriendo este tutorial y que te ayude a ponerte en marcha con Defold.

> Descarga los assets para este tutorial [aquí](https://github.com/defold/sample-runner/tree/main/def-runner).

## PASO 1 - Instalación y configuración

El primer paso es [descargar los siguientes archivos](https://github.com/defold/sample-runner/tree/main/def-runner).

Ahora, si todavía no has descargado e instalado el editor Defold, es momento de hacerlo:

:[install](../shared/install.md)

Cuando el editor esté instalado e iniciado, es momento de crear un proyecto nuevo y dejarlo listo. Crea un [proyecto nuevo](/manuals/project-setup/#creating-a-new-project) desde la plantilla "Empty Project".

::: sidenote
Este tutorial usa funcionalidades de Spine de la [Spine Extension](https://github.com/defold/extension-spine). Agrega la extensión a la sección de dependencias de *game.project*.
:::

## El editor

La primera vez que inicias el editor, el editor empieza en blanco, sin ningún proyecto abierto, así que elige <kbd>Open Project</kbd> desde el menú y selecciona tu proyecto recién creado. También se te pedirá crear una "branch" para el proyecto.

Ahora, en el *Assets pane* verás todos los archivos que forman parte del proyecto. Si haces doble click en el archivo "main/main.collection", el archivo se abrirá en la vista del editor en el centro:

![Editor overview](images/runner/1/editor2_overview.png)

El editor consta de las siguientes áreas principales:

Assets pane
: Esta es una vista de todos los archivos de tu proyecto. Distintos tipos de archivo tienen distintos iconos. Haz doble click en un archivo para abrirlo en un editor designado para ese tipo de archivo. La carpeta especial de solo lectura *builtins* es común para todos los proyectos e incluye elementos útiles como un script de render predeterminado, una fuente, materiales para renderizar varios componentes y otras cosas.

Main Editor View
: Según el tipo de archivo que estés editando, esta vista mostrará un editor para ese tipo. El más usado es el editor de escena que ves aquí. Cada archivo abierto se muestra en una pestaña separada.

Changed Files
: Contiene una lista de todas las ediciones que has hecho en tu rama desde la última sincronización. Así que si ves algo en este panel, tienes cambios que todavía no están en el servidor. Puedes abrir un diff solo de texto y revertir cambios desde esta vista.

Outline
: El contenido del archivo que se está editando actualmente en una vista jerárquica. Puedes agregar, eliminar, modificar y seleccionar objetos y componentes desde esta vista.

Properties
: Las propiedades definidas en el objeto o componente actualmente seleccionado.

Console
: Al ejecutar el juego, esta vista captura la salida (logging, errores, información de debug, etc.) que viene del motor de juego, y también cualquier mensaje de debug personalizado de `print()` y `pprint()` desde tus scripts. Si tu app o juego no inicia, la consola es lo primero que debes revisar. Detrás de la consola hay un conjunto de pestañas que muestran información de errores, así como un editor de curvas que se usa al crear efectos de partículas.

## Ejecutar el juego

La plantilla de proyecto "Empty" en realidad está completamente vacía. Aun así, selecciona <kbd>Project ▸ Build</kbd> para compilar el proyecto y lanzar el juego.

![Build](images/runner/1/build_and_launch.png)

Una pantalla negra quizá no sea muy emocionante, pero es una aplicación de juego Defold en ejecución y podemos modificarla fácilmente para convertirla en algo más interesante. Así que hagamos eso.

::: sidenote
El editor Defold trabaja con archivos. Al hacer doble click en un archivo en el *Assets pane*, lo abres en un editor adecuado. Luego puedes trabajar con el contenido del archivo.

Cuando termines de editar un archivo, tienes que guardarlo. Selecciona <kbd>File ▸ Save</kbd> en el menú principal. El editor da una pista agregando un asterisco '\*' al nombre del archivo en la pestaña para cualquier archivo que contenga cambios sin guardar.

![File with unsaved changes](images/runner/1/file_changed.png)
:::

## Configurar el proyecto

Antes de empezar, configuremos varios ajustes para nuestro proyecto. Abre el asset *game.project* desde el `Assets Pane` y desplázate hacia abajo hasta la sección Display. Define `width` y `height` del proyecto en `1280` y `720`, respectivamente.

También necesitas agregar la extensión Spine al proyecto para que podamos animar el personaje héroe. Agrega una versión de la extensión Spine que sea compatible con la versión del editor Defold que tienes instalada. Las versiones disponibles de Spine se pueden ver aquí:

[https://github.com/defold/extension-spine/releases](https://github.com/defold/extension-spine/releases)

Haz click derecho en el enlace al archivo zip del release que quieras usar:

![Right click and copy link to release](images/runner/extension-spine-releases.png)

Agrega el enlace al release a tu lista de [dependencias de game.project](/manuals/libraries/#setting-up-library-dependencies). Cuando se haya agregado la extensión Spine, también necesitas reiniciar el editor para activar la integración del editor incluida con la extensión Spine.


## PASO 2 - Crear el suelo

Demos los primeros pasos y creemos una arena para nuestro personaje, o más bien una pieza de suelo con desplazamiento. Lo hacemos en unos pocos pasos.

1. Importa los assets de imagen al proyecto arrastrando los archivos "ground01.png" y "ground02.png" (desde la subcarpeta "level-images" en el paquete de assets) a una ubicación adecuada del proyecto, por ejemplo la carpeta "images" dentro de la carpeta "main".
2. Crea un nuevo archivo *Atlas* para contener las texturas del suelo (haz click derecho en una carpeta adecuada, por ejemplo la carpeta *main*, en el *Assets pane* y selecciona <kbd>New ▸ Atlas File</kbd>). Nombra el archivo de atlas *level.atlas*.

  ::: sidenote
  Un *Atlas* es un archivo que combina un conjunto de imágenes separadas en un archivo de imagen más grande. La razón para hacer esto es ahorrar espacio y también ganar rendimiento. Puedes leer más sobre Atlas y otras funcionalidades de gráficos 2D en la [documentación de gráficos 2D](/manuals/2dgraphics).
  :::

3. Agrega las imágenes del suelo al nuevo atlas haciendo click derecho en la raíz del atlas en *Outline* y seleccionando <kbd>Add Images</kbd>. Selecciona las imágenes importadas y haz click en *OK*. Cada imagen en el atlas ahora es accesible como una animación de un frame (imagen estática) para usar en sprites, efectos de partículas y otros elementos visuales. Guarda el archivo.

  ![Create new atlas](images/runner/1/new_atlas.png)

  ![Add images to atlas](images/runner/1/add_images_to_atlas.png)

  ::: sidenote
  *¿Por qué no funciona!?* Un problema común que tienen las personas al empezar con Defold es olvidarse de guardar. Después de agregar imágenes a un atlas, necesitas guardar el archivo antes de poder acceder a esa imagen.
  :::

4. Crea un archivo de colección *ground.collection* para el suelo y agrégale 7 objetos de juego (haz click derecho en la raíz de la colección en la vista *Outline* y selecciona <kbd>Add Game Object</kbd>). Nombra los objetos "ground0", "ground1", "ground2", etc., cambiando la propiedad *Id* en la vista *Properties*. Ten en cuenta que Defold asigna automáticamente un id único a los objetos de juego nuevos.

5. En cada objeto, agrega un componente sprite (haz click derecho en el objeto de juego en la vista *Outline* y selecciona <kbd>Add Component</kbd>, luego selecciona *Sprite* y haz click en *OK*), define la propiedad *Image* del componente sprite al atlas que acabas de crear y define la animación predeterminada del sprite como una de las dos imágenes de suelo. Define la posición X del _componente sprite_ (no del objeto de juego) en 190 y la posición Y en 40. Como el ancho de la imagen es 380 pixels y la desplazamos lateralmente la mitad de esos pixels, el pivote del objeto de juego quedará en el borde más izquierdo de la imagen del sprite.

  ![Create ground collection](images/runner/1/ground_collection.png)

6. Los gráficos que usamos son un poco grandes, así que escala cada objeto de juego al 60% (escala 0.6 en X e Y, lo que da piezas de suelo de 228 pixels de ancho).

  ![Scale ground](images/runner/1/scale_ground.png)

7. Posiciona todos los _objetos de juego_ en línea. Define las posiciones X de los _objetos de juego_ (no los componentes sprite) en 0, 228, 456, 684, 912, 1140 y 1368 (múltiplos del ancho de 228 pixels).

  ::: sidenote
  Probablemente lo más fácil sea crear un objeto de juego completo escalado con un componente sprite y luego copiarlo. Márcalo en la vista *Outline*, luego selecciona <kbd>Edit ▸ Copy</kbd> y después <kbd>Edit ▸ Paste</kbd>.

  Vale la pena notar que si quieres tiles más grandes o más pequeños, puedes simplemente cambiar la escala. Sin embargo, al hacerlo también tendrás que cambiar las posiciones X de todos los objetos de juego del suelo a múltiplos del nuevo ancho.
  :::

8. Guarda el archivo, luego agrega *ground.collection* al archivo *main.collection*: primero haz doble click en el archivo *main.collection*, luego haz click derecho en el objeto raíz en la vista *Outline* y selecciona <kbd>Add Collection From File</kbd>. En el diálogo, selecciona *ground.collection* y haz click en *OK*. Asegúrate de colocar *ground.collection* en la posición 0, 0, 0 o se desplazará visualmente. Guárdalo.

9. Inicia el juego (<kbd>Project ▸ Build</kbd> para ver que todo está en su lugar.

  ![Still ground](images/runner/1/still_ground.png)

A estas alturas quizá estés confundido y te preguntes qué son realmente todas estas cosas que hemos estado creando, así que tomemos un momento para ver los bloques de construcción más básicos en cualquier proyecto Defold:

Game objects
: Son cosas que existen en el juego en ejecución. Cada objeto de juego tiene una ubicación en el espacio 3D, una rotación y escala. No necesariamente tiene que ser visible. Un objeto de juego contiene cualquier número de _componentes_ que agregan capacidades como gráficos (sprites, tilemaps, modelos, modelos spine y efectos de partículas), sonidos, físicas, factories (para spawning) y más. También se pueden agregar _componentes script_ Lua para dar comportamientos a un objeto de juego. Cada objeto de juego que existe en tus juegos tiene un *id* que necesitas para comunicarte con él mediante paso de mensajes.

Collections
: Las colecciones no existen por sí mismas en un juego en ejecución, pero se usan para habilitar nombres estáticos de objetos de juego y al mismo tiempo permitir múltiples instancias del mismo objeto de juego. En la práctica, las colecciones se usan como contenedores de objetos de juego y otras colecciones. Puedes usar colecciones de forma parecida a prototipos (también conocidos como "prefabs" o "blueprints" en otros motores) de jerarquías complejas de objetos de juego y colecciones. Al iniciar, el motor carga una colección principal y da vida a todo lo que hayas puesto dentro de ella. Por defecto, este es el archivo *main.collection* en la carpeta *main* de tu proyecto, pero puedes cambiarlo en la configuración del proyecto.

Por ahora estas descripciones probablemente sean suficientes. Sin embargo, puedes encontrar un recorrido mucho más completo por estas cosas en el [manual de bloques de construcción](/manuals/building-blocks). Es buena idea visitar ese manual más adelante para obtener una comprensión más profunda de cómo funcionan las cosas en Defold.

## PASO 3 - Hacer que el suelo se mueva

Ahora que tenemos todas las piezas del suelo en su lugar, es bastante simple hacer que se muevan. La idea es esta: mover las piezas de derecha a izquierda y, cuando una pieza llegue al borde izquierdo fuera de la pantalla, moverla a la posición más a la derecha. Mover todos estos objetos de juego requiere un script Lua, así que creemos uno:

1. Haz click derecho en la carpeta *main* en el *Assets pane* y selecciona <kbd>New ▸ Script File</kbd>. Nombra el nuevo archivo *ground.script*.
2. Haz doble click en el nuevo archivo para abrir el editor de scripts Lua.
3. Elimina el contenido predeterminado del archivo y copia el siguiente código Lua en él, luego guarda el archivo.

```lua
-- ground.script
local pieces = { "ground0", "ground1", "ground2", "ground3",
                    "ground4", "ground5", "ground6" } -- <1>

function init(self) -- <2>
    self.speed = 360  -- Velocidad en pixels/s
end

function update(self, dt) -- <3>
    for i, p in ipairs(pieces) do -- <4>
        local pos = go.get_position(p)
        if pos.x <= -228 then -- <5>
            pos.x = 1368 + (pos.x + 228)
        end
        pos.x = pos.x - self.speed * dt -- <6>
        go.set_position(pos, p) -- <7>
    end
end
```
1. Almacena los ids de los objetos de juego del suelo en una tabla Lua para poder iterar sobre ellos.
2. La función `init()` se llama cuando el objeto de juego cobra vida en el juego. Iniciamos una variable miembro local del objeto que contiene la velocidad del suelo.
3. `update()` se llama una vez por frame, típicamente 60 veces por segundo. `dt` contiene el número de segundos desde la última llamada.
4. Itera sobre todos los objetos de juego del suelo.
5. Almacena la posición actual en una variable local, luego si el objeto actual está en el borde más izquierdo, muévelo al borde más derecho.
6. Disminuye la posición X actual con la velocidad definida. Multiplica por `dt` para obtener velocidad independiente del framerate en pixels/s.
7. Actualiza la posición del objeto con la nueva velocidad.

::: sidenote
Defold es un núcleo de motor rápido que gestiona tus datos y objetos de juego. Cualquier lógica o comportamiento que necesites para tu juego se crea en el lenguaje Lua. Lua es un lenguaje de programación rápido y ligero que es excelente para escribir lógica de juego. Hay grandes recursos disponibles para aprender el lenguaje, como el libro [Programming in Lua](http://www.lua.org/pil/) y el [manual de referencia oficial de Lua](http://www.lua.org/manual/5.3/).

Defold agrega un conjunto de API encima de Lua, así como un sistema de _paso de mensajes_ que te permite programar comunicaciones entre objetos de juego. Consulta el [manual de paso de mensajes](/manuals/message-passing) para detalles sobre cómo funciona.
:::

::: sidenote
Puedes alternar las secciones Assets Pane, Console y Outline del editor usando las teclas <kbd>F6</kbd>, <kbd>F7</kbd> y <kbd>F8</kbd>, respectivamente
:::

Ahora que tenemos un archivo script, debemos agregar una referencia a él en un componente de un objeto de juego. De esa manera, el script se ejecutará como parte del ciclo de vida del objeto de juego. Hacemos esto creando un nuevo objeto de juego en *ground.collection* y agregando un componente *Script* al objeto que se refiere al archivo script Lua que acabamos de crear:

1. Haz click derecho en la raíz de la colección y selecciona <kbd>Add Game Object</kbd>. Define el *id* del objeto como "controller".
2. Haz click derecho en el objeto "controller" y selecciona <kbd>Add Component from file</kbd>, luego selecciona el archivo *ground.script*.

![Ground controller](images/runner/1/ground_controller.png)

Ahora, cuando ejecutes el juego, el objeto de juego "controller" ejecutará el script en su componente *Script*, haciendo que el suelo se desplace suavemente por la pantalla.

## PASO 4 - Crear un personaje héroe

El personaje héroe será un objeto de juego formado por los siguientes componentes:

Un *Spine Model*
: Esto nos da un pequeño personaje héroe tipo paper-doll cuyas partes del cuerpo pueden animarse suavemente (y de forma barata).

Un *Collision Object*
: Esto detectará colisiones entre el personaje héroe y las cosas del nivel sobre las que puede correr, que son peligrosas o que se pueden recoger.

Un *Script*
: Esto adquiere input del usuario y reacciona a él, hace que el personaje héroe salte, se anime y maneje colisiones.

Empieza importando las imágenes de las partes del cuerpo, luego agrégalas a un atlas nuevo que llamaremos *hero.atlas*:

1. Crea una nueva carpeta haciendo click derecho en el *Assets pane* y seleccionando <kbd>New ▸ Folder</kbd>. Asegúrate de no seleccionar una carpeta antes de hacer click o la nueva carpeta se creará dentro de la marcada. Nombra la carpeta "hero".
2. Crea un nuevo archivo de atlas haciendo click derecho en la carpeta *hero* y seleccionando <kbd>New ▸ Atlas File</kbd>. Nombra el archivo *hero.atlas*.
3. Crea una nueva subcarpeta *images* en la carpeta *hero*. Haz click derecho en la carpeta *hero* y selecciona <kbd>New ▸ Folder</kbd>.
4. Arrastra las imágenes de partes del cuerpo desde la carpeta *hero-images* en el paquete de assets a la carpeta *images* que acabas de crear en el *Assets pane*.
5. Abre *hero.atlas*, haz click derecho en el nodo raíz en *Outline* y selecciona <kbd>Add Images</kbd>. Marca todas las imágenes de partes del cuerpo y haz click en *OK*.
6. Guarda el archivo de atlas.

![Hero atlas](images/runner/2/hero_atlas.png)

También necesitamos importar los datos de animación Spine y configurar una *Spine Scene* para ellos:

1. Arrastra el archivo *hero.spinejson* (incluido en el paquete de assets) a la carpeta *hero* en el *Assets pane*.
2. Crea un archivo *Spine Scene*. Haz click derecho en la carpeta *hero* y selecciona <kbd>New ▸ Spine Scene File</kbd>. Nombra el archivo *hero.spinescene*.
3. Haz doble click en el nuevo archivo para abrir y editar la *Spine Scene*.
4. Define la propiedad *spine_json* al archivo JSON importado *hero.spinejson*. Haz click en la propiedad, luego haz click en el botón selector de archivo *...* para abrir el navegador de recursos.
5. Define la propiedad *atlas* para referirse al archivo *hero.atlas*.
6. Guarda el archivo.

![Hero spinescene](images/runner/2/hero_spinescene.png)

::: sidenote
El archivo *hero.spinejson* ha sido exportado en formato Spine JSON. Necesitarás el software de animación Spine para poder crear dichos archivos. Si quieres usar otro software de animación, puedes exportar tus animaciones como sprite-sheets y usarlas como animaciones flip-book desde recursos *Tile Source* o *Atlas*. Consulta el manual sobre [Animación](/manuals/animation) para más información.
:::

### Construir el objeto de juego

Ahora podemos empezar a construir el gameobject del héroe:

1. Crea un nuevo archivo *hero.go* (haz click derecho en la carpeta *hero* y selecciona <kbd>New ▸ Game Object File</kbd>).
2. Abre el archivo de objeto de juego.
3. Agrega un componente *Spine Model* a él. (Haz click derecho en la raíz en *Outline* y selecciona <kbd>Add Component</kbd>, luego selecciona "Spine Model".)
4. Define la propiedad *Spine Scene* del componente al archivo *hero.spinescene* que acabas de crear y selecciona "run_right" como animación predeterminada (arreglaremos la animación correctamente más adelante)
5. Guarda el archivo.

![Spinemodel properties](images/runner/2/spinemodel_properties.png)

Ahora es momento de agregar físicas para que funcione la colisión:

1. Agrega un componente *Collision Object* al objeto de juego del héroe. (Haz click derecho en la raíz en *Outline* y selecciona <kbd>Add Component</kbd>, luego selecciona "Collision Object")
2. Haz click derecho en el nuevo componente y selecciona <kbd>Add Shape</kbd>. Agrega dos formas para cubrir el cuerpo del personaje. Una esfera y una caja servirán.
3. Haz click en las formas y usa el *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) para mover las formas a buenas posiciones.
4. Marca el componente *Collision Object* y define la propiedad *Type* como "Kinematic".

::: sidenote
Colisión "Kinematic" significa que queremos que las colisiones se registren, pero que el motor de físicas no resuelva las colisiones automáticamente ni simule los objetos. El motor de físicas soporta varios tipos distintos de objetos de colisión. Puedes leer más sobre ellos en la [documentación de Physics](/manuals/physics).
:::

Es importante que especifiquemos con qué debe interactuar el objeto de colisión:

1. Define la propiedad *Group* como un nuevo grupo de colisión llamado "hero".
2. Define la propiedad *Mask* a otro grupo "geometry" con el que este objeto de colisión debe registrar colisiones. Ten en cuenta que el grupo "geometry" todavía no existe, pero pronto agregaremos objetos de colisión que pertenecen a él.

Finalmente, crea un nuevo archivo *hero.script* y agrégalo al objeto de juego.

1. Haz click derecho en la carpeta *hero* en el *Assets pane* y selecciona <kbd>New ▸ Script File</kbd>. Nombra el nuevo archivo *hero.script*.
2. Abre el nuevo archivo, luego copia y pega el siguiente código en el archivo script y guárdalo. (El código es bastante directo, aparte del solver que separa la forma de colisión del héroe de aquello con lo que colisiona. Eso lo hace la función `handle_geometry_contact()`.)

![Hero game object](images/runner/2/hero_game_object.png)

::: sidenote
La razón por la que manejamos la colisión nosotros mismos es que si en su lugar definiéramos el tipo del objeto de colisión del personaje como dynamic, el motor realizaría una simulación newtoniana de los cuerpos involucrados. Para un juego como este, dicha simulación está lejos de ser óptima, así que en lugar de pelear con el motor de físicas usando varias fuerzas, tomamos control total.

Ahora, para hacer eso y manejar bien la colisión se necesita un poco de matemática vectorial. En la [documentación de Physics](/manuals/physics#resolving-kinematic-collisions) se da una explicación detallada sobre cómo resolver colisiones cinemáticas.
:::

```lua
-- gravedad que tira del jugador hacia abajo en unidades de pixel/sˆ2
local gravity = -20

-- velocidad de despegue al saltar en unidades de pixel/s
local jump_takeoff_speed = 900

function init(self)
    -- esto le dice al motor que envíe input a on_input() en este script
    msg.post(".", "acquire_input_focus")

    -- guarda la posición inicial
    self.position = go.get_position()

    -- lleva registro del vector de movimiento y de si hay contacto con el suelo
    self.velocity = vmath.vector3(0, 0, 0)
    self.ground_contact = false
end

function final(self)
    -- Devuelve el foco de input cuando se elimina el objeto
    msg.post(".", "release_input_focus")
end

function update(self, dt)
    local gravity = vmath.vector3(0, gravity, 0)

    if not self.ground_contact then
        -- Aplica gravedad si no hay contacto con el suelo
        self.velocity = self.velocity + gravity
    end

    -- aplica velocidad al personaje del jugador
    go.set_position(go.get_position() + self.velocity * dt)

    -- reinicia estado volátil
    self.correction = vmath.vector3()
    self.ground_contact = false
end

local function handle_geometry_contact(self, normal, distance)
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
    if message_id == hash("contact_point_response") then
        -- comprueba si recibimos un mensaje de punto de contacto. Un mensaje por cada punto de contacto
        if message.group == hash("geometry") then
            handle_geometry_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- solo permite saltar desde el suelo
    if self.ground_contact then
        -- define la velocidad de despegue
        self.velocity.y = jump_takeoff_speed
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
    if action_id == hash("jump") or action_id == hash("touch") then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    end
end
```

1. Agrega el script como un componente *Script* al objeto héroe (haz click derecho en la raíz de *hero.go* en *Outline* y selecciona <kbd>Add Component from File</kbd>, luego selecciona el archivo *hero.script*).

Si quieres, ahora puedes probar y agregar temporalmente el personaje héroe a la colección principal y ejecutar el juego para verlo caer a través del mundo.

Lo último que necesitamos para que el héroe sea funcional es input. El script anterior ya contiene una función `on_input()` que responde a las acciones "jump" y "touch" (para pantallas táctiles). Agreguemos input bindings para estas acciones.

1. Abre "input/game.input_bindings"
2. Agrega un key trigger para "KEY_SPACE" y llama a la acción "jump"
3. Agrega un touch trigger para "TOUCH_MULTI" y llama a la acción "touch". (Los nombres de acción son arbitrarios pero deben coincidir con los nombres en tu script. Ten en cuenta que no puedes tener el mismo nombre de acción en varios triggers)
4. Guarda el archivo.

![Input bindings](images/runner/2/input_bindings.png)

## PASO 5 - Refactorizar el nivel

Ahora que tenemos un personaje héroe configurado con colisión y todo, también necesitamos agregar colisión al suelo para que el personaje héroe tenga algo con lo que colisionar (o sobre lo que correr). Lo haremos en un segundo, pero primero deberíamos hacer un pequeño refactor y poner todo lo del nivel en una colección separada y limpiar un poco la estructura de archivos:

1. Crea un nuevo archivo *level.collection* (haz click derecho en *main* en el *Assets pane* y selecciona <kbd>New ▸ Collection File</kbd>).
2. Abre el nuevo archivo, haz click derecho en la raíz en *Outline* y selecciona <kbd>Add Collection from File</kbd> y elige *ground.collection*.
3. En *level.collection*, haz click derecho en la raíz en *Outline* y selecciona <kbd>Add Game Object File</kbd> y elige *hero.go*.
4. Ahora, crea una nueva carpeta llamada *level* en la raíz del proyecto (haz click derecho en el espacio blanco debajo de *game.project* y selecciona <kbd>New ▸ Folder</kbd>), luego mueve a ella los assets de nivel que has creado hasta ahora: los archivos *level.collection*, *level.atlas*, la carpeta "images" que contiene las imágenes para el atlas de nivel, y los archivos *ground.collection* y *ground.script*.
5. Abre *main.collection*, elimina *ground.collection* y en su lugar agrega *level.collection* (click derecho y <kbd>Add Collection from File</kbd>), que ahora contiene *ground.collection*. Asegúrate de colocar la colección en la posición 0, 0, 0.

::: sidenote
Como quizá ya hayas notado, la jerarquía de archivos que se ve en el *Assets pane* está desacoplada de la estructura de contenido que construyes en tus colecciones. Los archivos individuales se referencian desde archivos de colección y de objetos de juego, pero su ubicación es completamente arbitraria.

Si quieres mover un archivo a una nueva ubicación, Defold ayuda actualizando automáticamente las referencias al archivo (refactoring). Al crear una pieza de software compleja, como un juego, es extremadamente útil poder cambiar la estructura del proyecto a medida que crece y cambia. Defold fomenta eso y hace que el proceso sea fluido, así que no tengas miedo de mover tus archivos.
:::

También debemos agregar un objeto de juego controller con un componente script a la colección de nivel:

1. Crea un nuevo archivo script. Haz click derecho en la carpeta *level* en el *Assets pane* y selecciona <kbd>New ▸ Script File</kbd>. Nombra el archivo *controller.script*.
2. Abre el archivo script, copia el siguiente código en él y guarda el archivo:

    ```lua
    -- controller.script
    go.property("speed", 360) -- <1>

    function init(self)
        msg.post("ground/controller#ground", "set_speed", { speed = self.speed })
    end
    ```
    1. Esta es una propiedad de script. La definimos con un valor predeterminado, pero cualquier instancia colocada del script puede sobrescribir este valor directamente en la vista de propiedades del editor.

3. Abre el archivo *level.collection*.
4. Haz click derecho en la raíz en *Outline* y selecciona <kbd>Add Game Object</kbd>.
5. Define el *Id* como "controller".
6. Haz click derecho en el objeto de juego "controller" en *Outline* y selecciona <kbd>Add Component from File</kbd> y selecciona el archivo *controller.script* en la carpeta *level*.
7. Guarda el archivo.

![Script property](images/runner/2/script_property.png)

::: sidenote
El objeto de juego "controller" no existe en un archivo sino que se crea in-place en la colección de nivel. Esto significa que la instancia del objeto de juego se crea a partir de los datos in-place. Eso está bien para objetos de juego de propósito único como este. Si necesitas múltiples instancias de algún objeto de juego y quieres poder modificar el prototipo/plantilla usado para crear cada instancia, simplemente crea un archivo de objeto de juego y agrega el objeto de juego desde archivo a la colección. Eso crea un objeto de juego con una referencia al archivo como prototipo/plantilla.

Ahora, el propósito de este objeto de juego "controller" es controlar todo lo relacionado con el nivel en ejecución. Pronto, este script se encargará de generar plataformas y monedas con las que el héroe interactuará, pero por ahora solo definirá la velocidad del nivel.
:::

En la función `init()` del script controller del nivel, envía un mensaje al componente script del objeto controller del suelo, direccionado por su id:

```lua
msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
```

El id del objeto de juego controller está definido como `"ground/controller"` ya que vive en la colección "ground". Luego agregamos el id de componente `"controller"` después del carácter hash `"#"` que separa el id de objeto del id de componente. Ten en cuenta que el script de suelo todavía no tiene ningún código para reaccionar al mensaje `set_speed`, así que debemos agregar una función `on_message()` a *ground.script* y agregar lógica para eso.

1. Abre *ground.script*.
2. Agrega el siguiente código y guarda el archivo:

```lua
-- ground.script
function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then -- <1>
        self.speed = message.speed -- <2>
    end
end
```
1. Todos los mensajes se convierten internamente a hash al enviarse y deben compararse con el valor hash.
2. Los datos del mensaje son una tabla Lua con los datos que se envían con el mensaje.

![Add ground code](images/runner/insert_ground_code.png)

## PASO 6 - Físicas del suelo y plataformas

En este punto deberíamos agregar colisión física para el suelo:

1. Abre el archivo *ground.collection*.
2. Agrega un nuevo componente *Collision Object* a un objeto de juego adecuado. Como el script del suelo no responde a colisiones (toda esa lógica está en el script del héroe), podemos ponerlo en cualquier objeto de juego _estacionario_ (los objetos de tile de suelo no son estacionarios, así que evítalos). Un buen candidato es el objeto de juego "controller", pero puedes hacer un objeto separado para ello si quieres. Haz click derecho en el objeto de juego, selecciona <kbd>Add Component</kbd> y selecciona *Collision Object*.
3. Agrega una forma de caja haciendo click derecho en el componente *Collision Object* y seleccionando <kbd>Add Shape</kbd> y luego *Box*.
4. Usa el *Move Tool* y el *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> y <kbd>Scene ▸ Scale Tool</kbd>) para hacer que la caja cubra todos los tiles del suelo.
5. Define la propiedad *Type* del objeto de colisión como "Static", ya que las físicas del suelo no se moverán.
6. Define la propiedad *Group* del objeto de colisión como "geometry" y *Mask* como "hero". Ahora el objeto de colisión del héroe y este registrarán colisiones entre ellos.
7. Guarda el archivo.

![Ground collision](images/runner/2/ground_collision.png)

Ahora deberías poder probar ejecutar el juego (<kbd>Project ▸ Build</kbd>). El personaje héroe debería correr sobre el suelo y debería ser posible saltar con el botón <kbd>Space</kbd>. Si ejecutas el juego en un dispositivo móvil, puedes saltar tocando la pantalla.

Para hacer la vida en nuestro mundo de juego un poco menos aburrida, debemos agregar plataformas a las que saltar.

1. Arrastra el archivo de imagen *rock_planks.png* desde el paquete de assets a la subcarpeta *level/images*.
2. Abre *level.atlas* y agrega la nueva imagen al atlas (click derecho en la raíz en *Outline* y selecciona <kbd>Add Images</kbd>).
3. Guarda el archivo.
4. Crea un nuevo archivo *Game Object* llamado *platform.go* en la carpeta *level*. (Haz click derecho en *level* en el *Assets pane* y luego selecciona <kbd>New ▸ Game Object File</kbd>.)
5. Agrega un componente *Sprite* al objeto de juego (haz click derecho en la raíz en la vista *Outline* y selecciona <kbd>Add Component</kbd> y luego *Sprite*).
6. Define la propiedad *Image* para referirse al archivo *level.atlas* y define *Default Animation* como "rock_planks". Por comodidad, mantén los objetos de nivel en una subcarpeta "level/objects".
7. Agrega un componente *Collision Object* al objeto de juego de la plataforma (haz click derecho en la raíz en la vista *Outline* y selecciona <kbd>Add Component</kbd>).
8. Asegúrate de definir el *Type* del componente como "Kinematic" y *Group* y *Mask* como "geometry" y "hero", respectivamente.
9. Agrega una *Box Shape* al componente *Collision Object*. (Haz click derecho en el componente en *Outline* y selecciona <kbd>Add Shape</kbd>, luego elige *Box*).
10. Usa el *Move Tool* y el *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> y <kbd>Scene ▸ Scale Tool</kbd>) para hacer que la forma en el componente *Collision Object* cubra la plataforma.
11. Crea un archivo *Script* *platform.script* (haz click derecho en el *Assets pane* y luego selecciona <kbd>New ▸ Script File</kbd>) y pon el siguiente código en el archivo, luego guárdalo:

    ```lua
    -- platform.script
    function init(self)
        self.speed = 540      -- Velocidad predeterminada en pixels/s
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            go.delete() -- <1>
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        end
    end
    ```
    1. Simplemente elimina la plataforma cuando se ha movido fuera del borde derecho de la pantalla

12. Abre *platform.go* y agrega el nuevo script como componente (haz click derecho en la raíz en la vista *Outline* y selecciona <kbd>Add Component From File</kbd> y selecciona *platform.script*).
13. Copia *platform.go* a un nuevo archivo (haz click derecho en el archivo en el *Assets pane* y selecciona <kbd>Copy</kbd>, luego haz click derecho otra vez y selecciona <kbd>Paste</kbd>) y llama al nuevo archivo *platform_long.go*.
14. Abre *platform_long.go* y agrega un segundo componente *Sprite* (haz click derecho en la raíz en la vista *Outline* y selecciona <kbd>Add Component</kbd>). Alternativamente puedes copiar el *Sprite* existente.
15. Usa el *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) para colocar los componentes *Sprite* lado a lado.
16. Usa el *Move Tool* y el *Scale Tool* para hacer que la forma en el componente *Collision Object* cubra ambas plataformas.

![Platform](images/runner/2/platform_long.png)

::: sidenote
Ten en cuenta que tanto *platform.go* como *platform_long.go* tienen componentes *Script* que se refieren al mismo archivo script. Esto es bueno, ya que cualquier cambio que hagamos al archivo script afectará el comportamiento de las plataformas normales y largas.
:::

## Generar plataformas

La idea del juego es que sea un endless runner simple. Esto significa que los objetos de juego de plataforma no se pueden colocar en una colección en el editor. En su lugar debemos generarlos dinámicamente:

1. Abre *level.collection*.
2. Agrega dos componentes *Factory* al objeto de juego "controller" (haz click derecho en él y selecciona <kbd>Add Component</kbd>, luego selecciona *Factory*)
3. Define las propiedades *Id* de los componentes como "platform_factory" y "platform_long_factory".
4. Define la propiedad *Prototype* de "platform_factory" al archivo */level/objects/platform.go*.
5. Define la propiedad *Prototype* de "platform_long_factory" al archivo */level/objects/platform_long.go*.
6. Guarda el archivo.
7. Abre el archivo *controller.script*, que gestiona el nivel.
8. Modifica el script para que contenga lo siguiente y luego guarda el archivo:

```lua
-- controller.script
go.property("speed", 360)

local grid = 460
local platform_heights = { 100, 200, 350 } -- <1>

function init(self)
    msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
    self.gridw = 0
end

function update(self, dt) -- <2>
    self.gridw = self.gridw + self.speed * dt

    if self.gridw >= grid then
        self.gridw = 0

        -- Quizá generar una plataforma a una altura aleatoria
        if math.random() > 0.2 then
            local h = platform_heights[math.random(#platform_heights)]
            local f = "#platform_factory"
            if math.random() > 0.5 then
                f = "#platform_long_factory"
            end

            local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, 0.6)
            msg.post(p, "set_speed", { speed = self.speed })
        end
    end
end
```
1. Valores predefinidos para la posición Y en la que generar plataformas.
2. La función `update()` se llama una vez en cada frame y la usamos para decidir si generar una plataforma normal o larga en ciertos intervalos (para evitar solapamientos) y alturas. Es fácil experimentar con varios algoritmos de spawning para crear gameplay diferente.

Ahora ejecuta el juego (<kbd>Project ▸ Build</kbd>).

Vaya, esto empieza a convertirse en algo (casi) jugable...

![Running the game](images/runner/2/run_game.png)

## PASO 7 - Animación y muerte

Lo primero que vamos a hacer es dar vida al personaje héroe. Ahora mismo el pobre está atrapado en un bucle de correr y no responde bien a los saltos ni a nada. El archivo spine que agregamos desde el paquete de assets en realidad contiene un conjunto de animaciones justo para eso.

1. Abre el archivo *hero.script* y agrega las siguientes funciones _antes_ de la función `update()` existente:

```lua
    -- hero.script
    local function play_animation(self, anim)
        -- solo reproduce animaciones que no se estén reproduciendo ya
        if self.anim ~= anim then
            -- dile al modelo spine que reproduzca la animación
            local anim_props = { blend_duration = 0.15 }
            spine.play_anim("#spinemodel", anim, go.PLAYBACK_LOOP_FORWARD, anim_props)
            -- recuerda qué animación se está reproduciendo
            self.anim = anim
        end
    end

    local function update_animation(self)
        -- asegúrate de que se esté reproduciendo la animación correcta
        if self.ground_contact then
            play_animation(self, hash("run"))
        else
            play_animation(self, hash("jump"))

        end
    end
```

2. Encuentra la función `update()` y agrega una llamada a `update_animation`:

```lua
    ...
    -- aplícala al personaje del jugador
    go.set_position(go.get_position() + self.velocity * dt)

    update_animation(self)
    ...
  ```

![Insert hero code](images/runner/insert_hero_code.png)

::: sidenote
Lua tiene "alcance léxico" para variables locales y es sensible al orden en que colocas funciones `local`. La función `update()` llama a las funciones locales `update_animation()` y `play_animation()`, lo que significa que el runtime debe haber visto las funciones locales para poder llamarlas. Por eso debemos poner las funciones antes de `update()`. Si cambias el orden de las funciones, obtendrás un error. Ten en cuenta que esto se aplica solo a variables `local`. Puedes leer más sobre las reglas de alcance y funciones locales de Lua en http://www.lua.org/pil/6.2.html
:::

Eso es todo lo necesario para agregar animaciones de salto y caída al héroe. Si ejecutas el juego, notarás que se siente mucho mejor jugarlo. Quizá también notes que las plataformas desafortunadamente pueden empujar al héroe fuera de la pantalla. Ese es un efecto secundario del manejo de colisiones, pero el remedio es fácil: ¡agregar violencia y hacer peligrosos los bordes de las plataformas!

1. Arrastra *spikes.png* desde el paquete de assets a la carpeta "level/images" en el *Assets pane*.
2. Abre *level.atlas* y agrega la imagen (click derecho y selecciona <kbd>Add Images</kbd>).
3. Abre *platform.go* y agrega algunos componentes *Sprite*. Define *Image* como *level.atlas* y *Default Animation* como "spikes".
4. Usa el *Move Tool* y el *Rotate Tool* para colocar los spikes a lo largo de los bordes de la plataforma.
5. Para hacer que los spikes se rendericen detrás de la plataforma, define la posición *Z* de los sprites de spikes en -0.1.
6. Agrega un nuevo componente *Collision Object* a las plataformas (haz click derecho en la raíz en *Outline* y selecciona <kbd>Add Component</kbd>). Define la propiedad *Group* como "danger". Define también *Mask* como "hero".
7. Agrega una forma de caja al *Collision Object* (click derecho y selecciona <kbd>Add Shape</kbd>) y usa el *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) y el *Scale Tool* para colocar la forma de modo que el personaje héroe colisione con el objeto "danger" al golpear la plataforma desde el lado o desde abajo.
8. Guarda el archivo.

    ![Platform spikes](images/runner/3/danger_edges.png)

9. Abre *hero.go*, marca el *Collision Object* y agrega el nombre "danger" a la propiedad *Mask*. Luego guarda el archivo.

    ![Hero collision](images/runner/3/hero_collision.png)

10. Abre *hero.script* y cambia la función `on_message()` para que tengamos una reacción si el personaje héroe colisiona con un borde "danger":

    ```lua
    -- hero.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            self.velocity = vmath.vector3(0, 0, 0)
            self.correction = vmath.vector3()
            self.ground_contact = false
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- comprueba si recibimos un mensaje de punto de contacto
            if message.group == hash("danger") then
                -- Morir y reiniciar
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("#", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end
    ```
    1. Agrega rotación y movimiento de caída al héroe cuando muere. ¡Esto se puede mejorar mucho!

11. Cambia la función `init()` para enviar un mensaje "reset" que inicialice el objeto, luego guarda el archivo:

    ```lua
    -- hero.script
    function init(self)
        -- esto nos permite manejar input en este script
        msg.post(".", "acquire_input_focus")
        -- guarda posición
        self.position = go.get_position()
        msg.post("#", "reset")
    end
    ```

## PASO 8 - Reiniciar el nivel

Si pruebas el juego ahora, rápidamente se vuelve evidente que el mecanismo de reset no funciona. El reset del héroe está bien, pero puedes reiniciar fácilmente en una situación donde caerás instantáneamente sobre un borde de plataforma y morirás otra vez. Lo que queremos hacer es reiniciar correctamente todo el nivel al morir. Como el nivel es solo una serie de plataformas generadas, solo necesitamos llevar registro de todas las plataformas generadas y luego eliminarlas al hacer reset:

1. Abre el archivo *controller.script* y edita el código para almacenar los ids de todas las plataformas generadas:

    ```lua
    -- controller.script
    go.property("speed", 360)

    local grid = 460
    local platform_heights = { 100, 200, 350 }

    function init(self)
        msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
        self.gridw = 0
        self.spawns = {} -- <1>
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= grid then
            self.gridw = 0

            -- Quizá generar una plataforma a una altura aleatoria
            if math.random() > 0.2 then
                local h = platform_heights[math.random(#platform_heights)]
                local f = "#platform_factory"
                if math.random() > 0.5 then
                    f = "#platform_long_factory"
                end

                local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, 0.6)
                msg.post(p, "set_speed", { speed = self.speed })
                table.insert(self.spawns, p) -- <1>
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then -- <2>
            -- Dile al héroe que se reinicie.
            msg.post("hero#hero", "reset")
            -- Elimina todas las plataformas
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then -- <3>
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```
    1. Usamos una tabla para almacenar todas las plataformas generadas
    2. El mensaje "reset" elimina todas las plataformas almacenadas en la tabla
    3. El mensaje "delete_spawn" elimina una plataforma particular y la quita de la tabla

2. Guarda el archivo.
3. Abre *platform.script* y modifícalo para que, en lugar de simplemente eliminar una plataforma que alcanzó el borde más izquierdo, envíe un mensaje al controller del nivel pidiendo eliminar la plataforma:

    ```lua
    -- platform.script
    ...
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    ...
    ```

    ![Insert platform code](images/runner/insert_platform_code.png)

4. Guarda el archivo.
5. Abre *hero.script*. Ahora, lo último que necesitamos hacer es decirle al nivel que haga el reset. Hemos movido el mensaje que pide al héroe reiniciarse al script controller del nivel. Tiene sentido centralizar el control del reinicio así porque nos permite, por ejemplo, introducir una secuencia de muerte temporizada más larga con mayor facilidad:

```lua
-- hero.script
...
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
    function()
        msg.post("controller#controller", "reset")
    end)
...
```

![Insert hero code](images/runner/insert_hero_code_2.png)

¡Y ahora el bucle principal de reiniciar-morir está en su lugar!

Lo siguiente: algo por lo que vivir: ¡monedas!

## PASO 9 - Monedas para recoger

La idea es poner monedas en el nivel para que el jugador las recoja. La primera pregunta que hay que hacer es cómo ponerlas en el nivel. Podemos, por ejemplo, desarrollar un esquema de spawning que esté de algún modo en sintonía con el algoritmo de generación de plataformas. Sin embargo, al final elegimos un enfoque mucho más fácil: que las propias plataformas generen monedas:

1. Arrastra la imagen *coin.png* desde el paquete de assets a "level/images" en el *Assets pane*.
2. Abre *level.atlas* y agrega la imagen (click derecho y selecciona <kbd>Add Images</kbd>).
3. Crea un archivo *Game Object* llamado *coin.go* en la carpeta *level* (haz click derecho en *level* en el *Assets pane* y selecciona <kbd>New ▸ Game Object File</kbd>).
4. Abre *coin.go* y agrega un componente *Sprite* (click derecho y selecciona <kbd>Add Component</kbd> en *Outline*). Define *Image* como *level.atlas* y *Default Animation* como "coin".
5. Agrega un *Collision Object* (click derecho en *Outline* y selecciona <kbd>Add Component</kbd>)
y agrega una forma *Sphere* que cubra la imagen (haz click derecho en el componente y selecciona <kbd>Add Shape</kbd>).
6. Usa el *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) y el *Scale Tool* para hacer que la esfera cubra la imagen de la moneda.
7. Define el *Type* del objeto de colisión como "Kinematic", su *Group* como "pickup" y su *Mask* como "hero".
8. Abre *hero.go* y agrega "pickup" a la propiedad *Mask* del componente *Collision Object*, luego guarda el archivo.
9. Crea un nuevo archivo script *coin.script* (haz click derecho en *level* en el *Assets pane* y selecciona <kbd>New ▸ Script File</kbd>). Reemplaza el código de plantilla con lo siguiente:

    ```lua
    -- coin.script
    function init(self)
        self.collected = false
    end

    function on_message(self, message_id, message, sender)
        if self.collected == false and message_id == hash("collision_response") then
            self.collected = true
            msg.post("#sprite", "disable")
        elseif message_id == hash("start_animation") then
            pos = go.get_position()
            go.animate(go.get_id(), "position.y", go.PLAYBACK_LOOP_PINGPONG, pos.y + 24, go.EASING_INOUTSINE, 0.75, message.delay)
        end
    end
    ```

10. Agrega el archivo script como componente *Script* al objeto coin (haz click derecho en la raíz en *Outline* y selecciona <kbd>Add Component from File</kbd>).

    ![Coin game object](images/runner/3/coin.png)

El plan es generar las monedas desde los objetos plataforma, así que pon factories para las monedas en *platform.go* y *platform_long.go*.

1. Abre *platform.go* y agrega un componente *Factory* (click derecho en *Outline* y selecciona <kbd>Add Component</kbd>).
2. Define el *Id* del *Factory* como "coin_factory" y define su *Prototype* al archivo *coin.go*.
3. Ahora abre *platform_long.go* y crea un componente *Factory* idéntico.
4. Guarda los dos archivos.

![Coin factory](images/runner/3/coin_factory.png)

Ahora necesitamos modificar *platform.script* para que genere y elimine las monedas:

```lua
-- platform.script
function init(self)
    self.speed = 540     -- Velocidad predeterminada en pixels/s
    self.coins = {}
end

function final(self)
    for i,p in ipairs(self.coins) do
        go.delete(p)
    end
end

function update(self, dt)
    local pos = go.get_position()
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    pos.x = pos.x - self.speed * dt
    go.set_position(pos)
end

function create_coins(self, params)
    local spacing = 56
    local pos = go.get_position()
    local x = pos.x - params.coins * (spacing*0.5) - 24
    for i = 1, params.coins do
        local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
        msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
        msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
        table.insert(self.coins, coin)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then
        self.speed = message.speed
    elseif message_id == hash("create_coins") then
        create_coins(self, message)
    end
end
```
1. Al definir el padre de la moneda generada como la plataforma, se moverá junto con la plataforma.
2. La animación hace que las monedas bailen arriba y abajo, relativas a la plataforma que ahora es el padre de las monedas.

::: sidenote
Las relaciones padre-hijo son estrictamente una modificación del _scene graph_. Un hijo se transformará (moverá, escalará o rotará) junto con su padre. Si necesitas relaciones de "ownership" adicionales entre objetos de juego, debes rastrearlas específicamente en código.
:::

El último paso de este tutorial es agregar un par de líneas a *controller.script*:

```lua
-- controller.script
...
local platform_heights = { 100, 200, 350 }
local coins = 3 -- <1>
...
```
1. La cantidad de monedas que se generarán en una plataforma normal.

```lua
-- controller.script
...
local coins = coins
if math.random() > 0.5 then
    f = "#platform_long_factory"
    coins = coins * 2 -- El doble de monedas en plataformas largas
end
...
```

```lua
-- controller.script
...
msg.post(p, "set_speed", { speed = self.speed })
msg.post(p, "create_coins", { coins = coins })
table.insert(self.spawns, p)
...
```

![Insert controller code](images/runner/insert_controller_code.png)

¡Y ahora tenemos un juego simple, pero funcional! Si llegas hasta aquí quizá quieras continuar por tu cuenta y agregar lo siguiente:

1. Contadores de puntuación y vidas
2. Efectos de partículas para los pickups y la muerte
3. Buenas imágenes de fondo

> Descarga la versión completa del proyecto [aquí](images/runner/sample-runner.zip)

Esto concluye este tutorial introductorio. Ahora sigue adelante y sumérgete en Defold. Tenemos muchos [manuales y tutoriales](//www.defold.com/learn) preparados para guiarte, y si te quedas atascado, eres bienvenido al [foro](//forum.defold.com).

¡Feliz Defolding!
