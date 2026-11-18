---
title: Defold para usuarios de Godot
brief: Esta guía te presenta Defold a partir de conceptos que ya conoces de Godot y te enseña a usar las herramientas y las API equivalentes.
---

# Defold para usuarios de Godot {#defold-for-godot-users}

Si tienes experiencia con Godot, ya sabes buena parte de lo que necesitas para crear un juego en Defold. Esta guía te muestra cómo aprovechar lo que ya conoces para empezar enseguida y qué diferencias conviene tener en cuenta para evitar errores frecuentes. Para esta guía usamos Godot 4.7.

## Introducción {#introduction}

Defold es un motor de videojuegos gratuito y multiplataforma para juegos 2D y 3D, con un editor para Windows, Linux y macOS. El código fuente completo del motor y del editor está disponible en [GitHub](https://github.com/defold/defold/). Puedes compilarlo tú mismo o descargar una versión para tu sistema operativo.

A primera vista, Defold se parece mucho a Godot. Ambos motores te permiten crear juegos a partir de piezas reutilizables y añadirles comportamiento con scripts. Godot ofrece muchos nodos especializados. Defold cuenta con menos componentes (Components), de uso más general, y la lógica del juego se implementa con scripts y módulos Lua. Por ejemplo, en Defold el personaje del jugador puede ser un objeto de juego (Game Object) con un sprite o un modelo, un objeto de colisión y un script.

Defold procura mantener pequeño el motor de ejecución y hacer un uso eficiente de los recursos, algo especialmente útil para juegos web y móviles. Algunos límites del motor se fijan de antemano para poder reservar la memoria necesaria.

Encontrarás menos elementos de juego y de interfaz listos para usar que en Godot, pero puedes combinar o ampliar los componentes de Defold para conseguir los mismos resultados. El núcleo del motor está diseñado para ser lo más ligero posible. Puedes reducir aún más su tamaño excluyendo funciones que no necesitas o ampliarlo con extensiones nativas y módulos Lua. El [Defold Asset Portal](https://defold.com/assets/) contiene cientos de módulos, bibliotecas y extensiones que te ayudan, por ejemplo, a crear interfaces complejas, diseñar pipelines de renderizado más avanzados y simplificar tareas de desarrollo.

Encontrarás más información sobre las funciones de Defold en la [página del producto](https://defold.com/product/).

## Instalación {#installation}

1. Descarga Defold para tu sistema operativo desde la [página de descargas](https://defold.com/download/).
2. Descomprime el archivo y abre el editor.

Puedes crear y ejecutar tu primer proyecto sin instalar un gestor independiente ni plantillas de exportación. Consulta las instrucciones para cada plataforma en el [manual de instalación](/manuals/install/).

Puedes actualizar Defold desde el propio editor. Cuando actualices un proyecto existente, revisa las notas de la versión y prueba el juego en las plataformas a las que va destinado.

## Pantalla de bienvenida {#welcome-screen}

Al abrir Defold aparece una pantalla de bienvenida desde la que puedes abrir proyectos recientes o crear uno nuevo. Cumple una función similar a la del gestor de proyectos de Godot.

![Gestor de proyectos de Godot y pantalla de bienvenida de Defold](images/godot/godot_1.png)

Para crear un proyecto en Defold puedes elegir entre estas opciones.

- **Templates** ofrece plantillas de proyectos vacíos o específicos de una plataforma.
- **Tutorials** contiene proyectos que te guían en tus primeros pasos.
- **Samples** incluye ejemplos y proyectos de partida que puedes ejecutar y explorar.

![Plantillas de proyecto en Godot y Defold](images/godot/godot_2.png)

En la sección Samples de Defold encontrarás proyectos de partida y ejemplos similares a los de la tienda de recursos de Godot.

![Ejemplos y proyectos de partida en Godot y Defold](images/godot/godot_3.png)

:[Hello World](../shared/hello-world.md)

---

## Visión general del editor Defold {#defold-editor-overview}

Reconocerás los paneles principales, aunque sus nombres y posiciones difieren. Para facilitar la comparación, hemos dispuesto los paneles del editor de Godot de forma similar a la vista predeterminada de Defold.

![Visión general del editor de Godot](images/godot/godot_4.png)
![Visión general del editor Defold](images/godot/godot_5.png)

| Godot | Defold | Función en el editor Defold |
|---|---|---|
| Panel FileSystem | Assets | Permite gestionar los archivos y carpetas del proyecto y refleja la estructura de su directorio en el disco. |
| Vista 2D/3D y editores de recursos | Main editor | Cambia según el archivo que abras, ya sea una colección, una GUI, un atlas, un script u otro recurso. Puedes dividirlo en dos paneles. |
| Panel Scene | Outline | Muestra la estructura del recurso actual. El árbol de escena global en tiempo de ejecución no aparece en este panel. |
| Inspector | Properties | Muestra las propiedades del objeto, componente o recurso seleccionado. |
| Output y Debugger | Tools | Incluye Console, Build Errors, Search Results y el depurador. |
| Integración del control de versiones | Changed Files | Muestra los cambios si el proyecto usa Git. |

En la esquina superior derecha del editor 3D de Defold también encontrarás una barra de herramientas. Puedes consultar sus funciones en el [manual de edición de escenas](/manuals/scene-editing/#toolbar-overview).

### Orientación de escena 2D y 3D {#2d-and-3d-scene-orientation}

:[Orientación de escena 2D y 3D](../shared/2d-and-3d-scene-orientation.md)

### Paneles {#panes}

Los paneles de Defold están acoplados a una sola ventana. Puedes cambiar su tamaño arrastrando los bordes y mostrarlos u ocultarlos con `F6`, `F7` y `F8` o desde el menú `View`.

![Cómo mostrar y ocultar los paneles](images/editor/editor_panes.png)

### Coordenadas {#coordinates}

En una escena 2D, si usas el script de render predeterminado y tu colección de Defold no contiene una cámara, las coordenadas `(0, 0)` corresponden a la esquina inferior izquierda de la ventana del juego. El eje Y positivo apunta hacia **arriba** y el X positivo, hacia la derecha.

En las coordenadas de pantalla 2D que suele usar Godot, el eje Y positivo apunta hacia **abajo**. Tenlo en cuenta al trasladar posiciones o código de movimiento.

![Diferencia entre las coordenadas 2D de Defold y Godot](images/godot/godot_6.png)

En el sistema de coordenadas 3D de Godot, el eje Y positivo apunta hacia arriba, igual que en Defold. Defold usa el mismo sistema de coordenadas 3D para los juegos 2D y 3D. En 2D, lo habitual es trabajar en el plano XY con una proyección ortográfica. Puedes configurar la cámara de otra manera si lo necesitas.

![Coincidencia de los ejes de Defold y Godot en 3D](images/godot/godot_7.png)

Encontrarás más detalles en el [manual de visión general del editor](/manuals/editor/).

---

## Conceptos clave {#key-concepts}

En Godot construyes **escenas** a partir de nodos. En Defold trabajas con componentes, objetos de juego y colecciones (Collections) de objetos de juego.

Por ejemplo, en Godot puedes crear un jugador a partir de un `Node2D` que tenga un `Sprite2D` como hijo, adjuntar un script al nodo raíz y añadir el jugador a tu primera escena (`Scene`).
En Defold puedes crear el jugador como un objeto de juego con componentes `Sprite` y `Script` y añadirlo a una colección.

![Comparación entre los nodos de Godot y los objetos de juego y componentes de Defold](images/godot/key_concepts.png)

El [manual de bloques de construcción](/manuals/building-blocks/) explica estos conceptos con más detalle.

### Objetos de juego {#game-objects}

En Defold, un **objeto de juego** es un *contenedor* de componentes y tiene dos características básicas.

- Una **identidad**.
- Una **transformación** (posición, rotación y escala).

Un objeto de juego puede cumplir una función parecida a la de un `Node2D` o un `Node3D` en Godot. En Defold todos los objetos de juego usan una transformación 3D, incluidos los de los juegos 2D, por lo que no hay un tipo específico de objeto de juego 2D.

En Defold puedes hacer que un objeto de juego sea hijo de otro para que herede su transformación. Puedes definir estas relaciones en una colección o cambiarlas durante la ejecución. Cambiar el padre de un objeto de juego no afecta a su dirección.

Puedes definir un objeto de juego directamente en el archivo `.collection` como objeto **integrado**, o añadir una referencia a un prototipo `.go` reutilizable. Si cambias la definición de un objeto integrado, modificas esa colección. Los objetos definidos por separado conservan sus propios valores. Si modificas un prototipo `.go`, las instancias que lo usan se actualizan, salvo en las propiedades sobrescritas en cada instancia. Varios objetos, incluso los integrados, pueden hacer referencia al mismo recurso de componente. Si lo editas, el cambio puede afectar a todos los que lo usan. Cuando reutilizas una colección, los cambios en sus objetos integrados se reflejan en todos los lugares que hacen referencia a esa colección.

### Componentes {#components}

Los componentes son bloques de construcción especializados. Pueden definir, entre otras cosas, el aspecto, la física, el sonido y el comportamiento de un objeto de juego.

Añade un componente `Sprite` a un objeto de juego para mostrar una imagen, un componente `Sound` para reproducir audio o un componente `Script` para ejecutar código Lua.

Los componentes pertenecen a objetos de juego y no pueden tener componentes hijos. Para crear una jerarquía, establece relaciones padre-hijo entre los objetos de juego de una colección.

Tampoco puedes cambiar el comportamiento de un componente adjuntándole un script como en Godot. Puedes ajustarlo en el panel Properties y crear componentes personalizados mediante extensiones nativas, de forma similar a GDExtension. Algunos ejemplos de componentes personalizados son los oficiales de [Rive](https://github.com/defold/extension-rive) y [Spine](https://github.com/defold/extension-spine), y los de [Sprite Loop](https://github.com/Balkan-Ram-Games/spriteloop-defold) y [Object Interpolation](https://github.com/indiesoftby/defold-object-interpolation), creados por la comunidad.

Un script de Defold es un componente independiente que puedes añadir a cualquier objeto de juego. Un mismo objeto puede tener varios componentes, incluso varios scripts.

Como los componentes carecen de jerarquía propia y son independientes de los scripts personalizados, Defold puede aprovechar su diseño orientado a datos para almacenarlos en memoria de forma eficiente.

| Nodo de Godot | Componente de Defold | Notas |
|---|---|---|
| `Sprite2D` / `AnimatedSprite2D` | [Sprite](/manuals/sprite/) | Muestra texturas 2D y animaciones por fotogramas a partir de un atlas (una textura con varias imágenes) o de un tile source. |
| `Area2D` / `RigidBody2D` / `StaticBody2D` y sus equivalentes 3D | [Objeto de colisión](/manuals/physics-objects/) | Gestiona la física y los disparadores. Las formas de colisión se definen dentro del propio componente y no requieren nodos hijos. Puedes elegir un objeto estático, dinámico, cinemático o de tipo disparador. |
| Script `.gd` adjunto a un nodo | Script | Contiene el código Lua que implementa la lógica del juego, gestiona la entrada y controla otros componentes y objetos de juego. |
| `TileMapLayer` | [Tilemap](/manuals/tilemap/) | Dibuja un mapa en cuadrícula a partir de un tile source y las capas del tilemap. |
| `Label` | [Nodo de texto GUI](/manuals/gui-text/) | Usa nodos de texto GUI para el texto de la interfaz. Para mostrar texto en el mundo del juego, usa un [componente Label](/manuals/label/). |
| `AudioStreamPlayer` | [Sound](/manuals/sound/) | Reproduce audio. Puedes ajustar Speed, Pan y Gain. |
| `Camera2D` / `Camera3D` | [Camera](/manuals/camera/) | Admite proyecciones ortográficas y en perspectiva. |
| Jerarquía de `Control` / `CanvasLayer` | [GUI](/manuals/gui/) | Cada componente GUI de Defold contiene su propia jerarquía de nodos (por ejemplo, Box, Text o Pie) y usa un `.gui_script` específico para controlar la interfaz. |
| `MeshInstance3D` | [Model](/manuals/model/) o [Mesh](/manuals/mesh/) | Model permite usar contenido 3D importado, y Mesh permite dibujar geometría personalizada a partir de un búfer. |
| `CPUParticles2D` / `GPUParticles2D` y sus equivalentes 3D | [ParticleFX](/manuals/particlefx/) | Emite partículas 2D o 3D que puedes configurar en el editor de partículas de Defold. |
| `PackedScene.instantiate()` | Factory / Collection Factory | Defold ofrece componentes distintos para definir qué objetos de juego o colecciones puedes crear durante la ejecución. |

### Colecciones y mundos {#collections-and-worlds}

Una **colección** describe objetos de juego, sus componentes y sus relaciones padre-hijo. Puedes incluir colecciones dentro de otras para reutilizar un grupo de objetos, de forma similar a las escenas anidadas de Godot. Defold no cuenta con el sistema general de herencia de escenas de Godot. Para reutilizar estructuras, usa prototipos y colecciones y personaliza sus instancias mediante propiedades o scripts.

El archivo de una colección no se convierte en una entidad en tiempo de ejecución. No hay ningún objeto que represente a la propia colección y en el que puedas llamar métodos, ni un nodo raíz que le corresponda. Defold lee las definiciones del archivo para crear los objetos de juego, sus componentes y la jerarquía entre ellos.

Al iniciar el juego, Defold lee el archivo `game.project` y carga la colección indicada en **Bootstrap ▸ Main Collection**. Así se crea el mundo inicial del juego. Los objetos de las colecciones anidadas forman parte de ese mismo mundo.

Un componente de fábrica de colecciones (**Collection Factory**) crea instancias de un grupo de objetos de juego, con sus componentes, en el **mundo existente** que contiene la fábrica.

Un proxy de colección (**Collection Proxy**) carga una colección aparte y crea un **mundo nuevo** con su propio espacio de direcciones y su propia simulación física. Esta diferencia importa, por ejemplo, al elegir cómo crear un enemigo que interactúe con la geometría del nivel actual o cómo cargar un nivel completamente nuevo, quizá de forma asíncrona. Más adelante veremos ambas operaciones.

Godot usa `PackedScene` tanto para crear instancias como para cambiar de escena. Cambiar de escena con `SceneTree` se parece a cargar un mundo independiente mediante un proxy de colección.

La tabla resume las equivalencias entre ambos motores.

| Godot | Defold | Notas |
|---|---|---|
| `Node3D` con nodos hijos | Objeto de juego con componentes | Los componentes aportan las capacidades y el comportamiento. Los objetos de juego proporcionan la transformación y la identidad. |
| Transformación de `Node2D` / `Node3D` | Transformación del objeto de juego | Está integrada en todos los objetos de juego. |
| Escena / `PackedScene` | Prototipo de objeto de juego (`.go`) o colección (`.collection`) | Un prototipo describe un objeto. Una colección describe un grupo de objetos y su jerarquía. |
| `PackedScene.instantiate()` | Fábrica o fábrica de colecciones | Crea un objeto de juego o un grupo de objetos en el mundo actual y devuelve sus identificadores. |
| Cambio de escena con `SceneTree` + `PackedScene.instantiate()` | Proxy de colección | Carga y crea un mundo independiente y genera en él los objetos de juego. |

---

## Escritura de código {#code-writing}

Defold incluye un editor para todos los archivos de texto y scripts del proyecto. Ofrece autocompletado, formato de código y una vista Structure que muestra los datos y las funciones del archivo, entre otras herramientas. Consulta la sección sobre [cómo usar el editor de código integrado](/manuals/writing-code/#using-the-built-in-code-editor).

También puedes abrir los scripts y los demás archivos de texto de Defold en un editor externo. Defold ofrece varias funciones que facilitan su integración con herramientas como VS Code. Para más detalles, consulta [cómo usar un editor de código externo](/manuals/writing-code/#using-an-external-code-editor).

### Lua y los scripts {#lua-and-scripts}

En Defold, la lógica del juego se programa en Lua. Si conoces GDScript, te resultará familiar, aunque hay algunas diferencias importantes. Defold también admite Teal, un dialecto de Lua con tipado estático. Al igual que con GDExtension, puedes usar extensiones nativas escritas en C, C++, C#, Objective-C, Java o JavaScript, según la plataforma de destino. Más adelante veremos estas extensiones.

En Defold trabajarás principalmente con los siguientes tipos de archivo Lua.

| Archivo | Uso |
|---|---|
| `.script` | Implementa la lógica y el comportamiento del juego. Usa API como `go`, `factory`, `sprite`, `tilemap` o `physics` para controlar otros objetos de juego y componentes. |
| `.gui_script` | Define el comportamiento de la interfaz mediante la API `gui`. |
| `.render_script` | Controla el renderizado con la API `render`. |
| `.lua` | Contiene módulos Lua reutilizables que se cargan con `require()`, como bibliotecas de código o scripts de utilidades. |

Las tablas de Lua pueden contener datos, funciones o ambas cosas. Para organizar tu código no necesitas reproducir la jerarquía de clases de GDScript. Guarda la lógica reutilizable en módulos y llama a sus funciones desde el script responsable del comportamiento correspondiente.

Los scripts de Defold son compatibles con Lua 5.1. Para conocer las particularidades del lenguaje y las diferencias entre plataformas, consulta [Lua en Defold](/manuals/lua/).

### Ciclo de vida de la aplicación {#application-lifecycle}

Por lo general, un juego de Defold empieza con una fase de inicialización y termina con una fase de finalización. Entre ambas se ejecuta un bucle en cada fotograma que actualiza las transformaciones y los componentes, ejecuta el código y procesa los mensajes.

![Ciclo de vida de la aplicación en Defold](images/application_lifecycle/application_lifecycle.png)

Como en Godot y otros motores, los scripts de Defold definen funciones que el motor invoca en distintos momentos del ciclo de vida de la aplicación. En Defold, estos callbacks de Lua tienen nombres diferentes, pero sus funciones te resultarán familiares.

| Godot | Defold | Notas |
|---|---|---|
| `_ready()` | `init(self)` | Inicializa los datos de la instancia y adquiere el foco de entrada si lo necesitas. |
| `_process(delta)` | `update(self, dt)` | Actualiza la instancia una vez por fotograma. |
| `_physics_process(delta)` | `fixed_update(self, dt)` | Actualiza la instancia a intervalos fijos si está activada esta opción. |
| `_input(event)` | `on_input(self, action_id, action)` | Procesa la entrada que reciben los componentes del objeto que la escuchan. |
| Callback de señal | `on_message(self, message_id, message, sender)` | Recibe mensajes de scripts o componentes del motor. |
| `_exit_tree()` | `final(self)` | Libera los recursos cuando finaliza la instancia del script. |

Godot llama a `_ready()` en los hijos antes que en el padre. Defold no garantiza un orden de inicialización ni de actualización entre objetos de juego y componentes. Coordínalos mediante mensajes para que ninguno dependa de que el `init()` de otro se ejecute primero.

Si vas a usar `fixed_update()`, asigna un valor positivo, por ejemplo 60, a **Engine ▸ Fixed Update Frequency** en `game.project` y activa **Physics ▸ Use Fixed Timestep**.

Defold también ofrece `late_update(self, dt)` para tareas que deben ejecutarse después de las actualizaciones normales y antes del renderizado, como ajustar una cámara. Si hace falta, el motor aún puede actualizar las transformaciones una última vez tras este callback.

Deshabilitar un componente y eliminarlo son operaciones distintas.

Consulta el [manual del ciclo de vida de la aplicación](/manuals/application-lifecycle/) para ver la secuencia completa y los callbacks disponibles para cada tipo de script.

### Datos de instancia y datos locales {#instance-data-vs-local-data}

Cada instancia de un componente de script recibe su propio `self` en los callbacks. En él puedes guardar el estado de la instancia, como `self.health` o `self.target`. Incluso dos componentes de script del mismo objeto de juego tienen valores de `self` independientes. `self` es un valor de tipo userdata cuyos campos se consultan como los de una tabla, aunque no admite operaciones propias de las tablas Lua como `pairs(self)`. En Godot, las variables de instancia (`var`) cumplen una función similar.

Para Godot, cada archivo `.gd` define una clase. Si adjuntas el mismo archivo `.gd` a 10 enemigos, Godot crea 10 instancias de esa clase. Cada enemigo tiene su propia copia de las variables declaradas en el ámbito de la clase mediante var.

Cuando se carga el recurso de un script, Defold ejecuta el archivo `.script` como un bloque de código Lua. Cada instancia del componente de script recibe su propio `self` en los callbacks del ciclo de vida, como `init(self)` y `update(self, dt)`.

En cambio, una variable local declarada en el ámbito del archivo `.script` se comparte entre **todas las instancias** de ese script. En Godot, el equivalente de las variables locales de archivo de Defold son las variables estáticas (`static var`).

![Diferencia entre los datos de instancia y los datos locales en Defold](images/lua/self_local.png)

En el ejemplo, si cambias `self.has_shield` a `true` en una instancia, las demás conservan su valor. Sin embargo, todas las instancias que usan este archivo de script comparten la variable local `color`, de modo que cambiarla puede afectarlas a todas.

### Propiedades {#properties}

Para definir una **propiedad** de instancia editable, usa `go.property()`. Podrás acceder a ella desde `self`. Como ocurre con `@export`, el valor también se muestra en el editor. En Defold lo verás en el panel `Properties`.

![Propiedades en el editor Defold](images/script-properties/properties.png)

Así se hace en **GDScript** con un script adjunto a un `Node3D` de Godot.

```gdscript
extends Node3D

@export var speed: float = 100.0

func _process(delta):
    position.x += speed * delta
```

El equivalente en **Lua** se añade como componente de script en Defold.

```lua
go.property("speed", 100)

function update(self, dt)
    local position = go.get_position()
    position.x = position.x + self.speed * dt
    go.set_position(position)
end
```

Puedes leer la propiedad Lua con `self.speed` y también asignarla al crear una instancia del objeto. Las transformaciones de Defold usan `vector3` incluso en 2D, por lo que debes indicar una coordenada Z.

En [Propiedades de script](/manuals/script-properties/) encontrarás los tipos de propiedad admitidos, y en [Scripts](/manuals/script/) puedes ver más ejemplos.

---

## Mensajes y direccionamiento {#messages-and-addressing}

Las señales de Godot permiten que un objeto anuncie un evento a quienes se hayan conectado a él. En Defold, los scripts suelen comunicarse enviando mensajes a la dirección de un objeto o componente.

En Defold puedes enviar un mensaje desde cualquier script con la función `msg.post()`. Para recibir y procesar los mensajes, implementa el callback `on_message()` en el script destinatario.

![Mensajes en Defold](images/message_passing/messages_overview.png)

Por ejemplo, el jugador puede avisar al HUD de que ha cambiado la puntuación.

En Godot, el nodo `Player` (`Node2D`) usa `player.gd`. Su hermano `GUI` (`CanvasLayer`) usa `gui.gd` y contiene una etiqueta Label llamada `ScoreText`.

![Configuración de señales en Godot](images/godot/godot_signals.png)

En Defold, el objeto de juego `player` usa `player.script`. El objeto de juego `hud` tiene un componente `gui` que contiene el nodo de texto `score` y usa `hud.gui_script`.

![Configuración de mensajes en Defold](images/godot/defold_messages.png)

### Enviar mensajes {#sending-messages}

En Godot, Player y GUI son nodos hermanos. Player conecta su señal `score_changed` a un método del script de GUI, que se encarga de actualizar la etiqueta.

**GDScript** en `player.gd`

```gdscript
extends Node2D

signal score_changed(value: int)
var score: int = 0

func _ready() -> void:
    score_changed.connect(get_node("../GUI").set_score)

func collect() -> void:
    score += 1
    score_changed.emit(score)

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        if event.keycode == KEY_SPACE:
            collect()
```

En Godot, `Player` define una señal llamada `score_changed`. Durante `_ready()`, la conecta al método `set_score()` del script de GUI. Cada vez que se llama a `collect()`, aumenta la puntuación y la señal emite el nuevo valor.

En Defold, vincula la tecla **Space** a la acción `collect` en los enlaces de entrada. El objeto `player` inicializa su puntuación en `init()` y solicita el foco de entrada para recibir los eventos. Cuando se llama a `collect(self)`, incrementa la puntuación y envía el mensaje `score_changed` a `/hud#gui` con la nueva puntuación en la tabla del mensaje.

**Lua** en `player.script`

```lua
function init(self)
    self.score = 0
    msg.post(".", "acquire_input_focus")
end

local function collect(self)
    self.score = self.score + 1
    msg.post("/hud#gui", "score_changed", { value = self.score })
end

function on_input(self, action_id, action)
    if action_id == hash("collect") and action.pressed then
        collect(self)
    end
end
```

En Defold, el jugador puede enviar el mensaje directamente a la dirección del receptor sin conectar antes una señal a la GUI como en Godot. Si utilizas el direccionamiento relativo de Defold, puedes reutilizar las funciones y los scripts que envían esos mensajes.

### Recibir y procesar mensajes {#receiving-and-handling-messages}

La GUI recibe el valor y actualiza el texto de la puntuación.

**GDScript** en `gui.gd`, adjunto a `GUI` (`CanvasLayer`)

```gdscript
extends CanvasLayer

func set_score(value: int) -> void:
    $ScoreText.text = str(value)
```

El script de GUI recibe el valor emitido a través de `set_score()` y actualiza su etiqueta hija `ScoreText`. El jugador no necesita acceder a la etiqueta ni modificarla directamente.

El script de la GUI de Defold obtiene primero el nodo de texto de la puntuación con `gui.get_node()`. Cuando el componente GUI recibe un mensaje, `on_message()` comprueba su identificador. Si es `score_changed`, el script lee `message.value` y actualiza el texto con `gui.set_text()`.

**Lua** en `hud.gui_script`, asignado al componente GUI

```lua
function init(self)
    self.score_node = gui.get_node("score")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("score_changed") then
        gui.set_text(self.score_node, tostring(message.value))
    end
end
```

En Defold, el destinatario del mensaje es el **componente** GUI. El script de la GUI que lo recibe decide cómo usarlo y qué nodo de texto actualizar. Por eso el mensaje no se envía directamente al nodo de la puntuación.

Ambas capturas muestran el texto inicial `Score: 0`. En estos ejemplos, cuando cambia la puntuación los scripts reemplazan todo el texto por el valor numérico.

La función `msg.post()` pone el mensaje en cola para que se entregue más tarde. No invoca al receptor de inmediato ni devuelve un resultado de su script. A menudo los mensajes se entregan en el mismo fotograma, pero el número de rondas de entrega tiene un límite y una cadena larga puede continuar en el siguiente. Si necesita responder, el receptor puede enviar otro mensaje a la URL del remitente original que recibe en `on_message()`. Para más detalles, consulta [Cadenas de mensajes](/manuals/message-passing/#message-chains).

La comunicación con varios receptores también es distinta. Una señal de Godot puede conectarse a varios métodos y, cuando se emite, avisa a todos los receptores conectados. Cada mensaje de Defold se envía a una dirección concreta. Para avisar a varios destinatarios, puedes enviarles mensajes individuales o implementar un sistema de suscripción en el juego.

### Cómo encontrar un objeto mediante el direccionamiento de Defold {#finding-an-object-addressing-in-defold}

Defold no tiene un equivalente general de `get_node()` que devuelva un objeto Lua que represente a otra instancia de script. Usas un identificador o una **URL** con una función de la API del motor, como `go.get_position()`, `go.set()` o `msg.post()`.

Una URL de Defold consta de tres partes.

```lua
socket:/path#component
```

- El **socket** identifica un mundo, como el de la colección principal que se carga al inicio o el de una colección cargada mediante un proxy.
- La **ruta** identifica un objeto de juego dentro de ese mundo.
- El **componente** identifica uno de los componentes de ese objeto.

Puedes usar la URL completa u omitir partes para formar una dirección relativa. Por ejemplo, para dirigirte a un componente del mismo objeto de juego basta con especificar la parte que identifica al componente. La tabla recoge algunas formas habituales.

| Dirección | Significado |
|---|---|
| `"#sprite"` | El componente sprite del objeto de juego actual. |
| `"/player#controller"` | El componente controller del objeto player en el mundo actual. |
| `"level:/player#controller"` | El componente controller del jugador en el mundo cargado que se llama level. |
| `"."` | Abreviatura para el objeto de juego actual (`Game Object`). El mensaje se entrega a sus componentes. |
| `"#"` | Abreviatura para el componente `Script` actual. |

En las colecciones anidadas, las rutas de los objetos pueden llevar prefijos. Cambiar el padre del que un objeto hereda su transformación no cambia su dirección.

Para los objetos que crees dinámicamente, guarda en tu código los identificadores que devuelven `factory.create()` o `collectionfactory.create()`.

Los grupos de Godot que permiten consultar conjuntos de objetos del juego o llamar a `call_group()` no tienen equivalente integrado en Defold. Para conseguir ese comportamiento, debes llevar tu propio registro de objetos o distribuir los mensajes desde tu código.

Los grupos de física de los objetos de colisión de Defold filtran las colisiones. La máscara de cada objeto especifica con qué grupos puede colisionar. Estos grupos son independientes del sistema de mensajes.

Conviene leer pronto los manuales de [direccionamiento](/manuals/addressing/) y [paso de mensajes](/manuals/message-passing/). Allí encontrarás respuesta a muchas dudas que surgen en un primer proyecto.

---

## Autoloads y estado compartido {#autoloads-and-shared-state}

También puedes agrupar funciones en módulos Lua y llamarlas directamente cuando no necesites comunicarte mediante el sistema de mensajes de Defold.

Si usas un **Autoload** en Godot para guardar datos compartidos, puedes usar un módulo Lua con el mismo fin en Defold. Por ejemplo, guarda el módulo en `modules/game_state.lua` y cárgalo con `require "modules.game_state"`.

**GDScript** con `game_state.gd` registrado como Autoload con el nombre `GameState`

```gdscript
extends Node
var score: int = 0
```

Su equivalente en **Lua**, en `modules/game_state.lua`

```lua
local M = { score = 0 }
return M
```

Otro script puede acceder a los datos compartidos de la siguiente manera.

En **GDScript**

```gdscript
func add_point():
    GameState.score += 1
```

En **Lua**

```lua
local game_state = require "modules.game_state"

local function add_point()
    game_state.score = game_state.score + 1
end
```

La función `require()` guarda el módulo en caché, por lo que todos los scripts que lo cargan comparten la tabla que devuelve. Los scripts de objeto de juego, de GUI y de render comparten el estado de Lua. Descargar un proxy de colección no restablece los datos del módulo. Si lo necesitas, puedes restablecerlos de forma explícita al iniciar una partida.

Un módulo Lua de Defold no es un objeto de juego y no recibe callbacks del ciclo de vida, de mensajes ni de entrada. Si usas un Autoload para ejecutar lógica en cada fotograma, reproducir sonidos o controlar las transiciones de nivel, implementa ese comportamiento en el script de un objeto de la colección. También puedes definir una función en el módulo e invocarla explícitamente desde los callbacks del ciclo de vida de tus scripts.

Módulo Lua `my_module`

```lua
local M = {}

function M.init(self)
    print("My init")
end

return M
```

Script Lua
```lua
local my_module = require "my_module"

function init(self)
    my_module.init(self)
end
```

Si necesitas datos por instancia, puedes hacer que un módulo devuelva una función que cree una tabla nueva y guardar esa tabla en `self`. Encontrarás más detalles, incluidas las particularidades de la recarga en caliente, en el [manual de módulos](/manuals/modules/).

---

## Creación de objetos y carga de niveles {#spawning-objects-and-loading-levels}

### Fábricas {#factories}

Para crear una instancia de un objeto de juego en Defold, añade un componente de fábrica (**Factory**) y selecciona el archivo `.go` correspondiente en su propiedad **Prototype**.

Para las colecciones, añade una **Collection Factory** y asígnale un archivo `.collection`. Al crear el grupo de objetos se conservan sus relaciones padre-hijo.

En este ejemplo de Godot, el objeto que genera las balas es un `Node2D` situado en el origen de la escena. Su script crea una instancia para cada bala.

En **GDScript**

```gdscript
extends Node2D

const BULLET = preload("res://bullet.tscn")

func spawn_bullet():
    var bullet = BULLET.instantiate()
    bullet.position = Vector2(200, 100)
    add_child(bullet)
    return bullet
```

En Defold tenemos un objeto de juego con un componente de fábrica cuyo identificador es `bullet_factory`. Con la función `factory.create()` podemos crear el objeto de juego al que hace referencia su propiedad `Prototype`.

![Configuración de una fábrica en Defold](images/godot/defold_factory.png)

En la captura se llama a la fábrica desde `init()`. La siguiente función muestra cómo indicar la posición inicial y devolver el identificador de la instancia.

En **Lua**

```lua
local function spawn_bullet()
    local position = vmath.vector3(200, 100, 0)
    local id = factory.create("#bullet_factory", position)
    return id
end
```

La función de Defold devuelve el **identificador** del objeto. No puedes invocar métodos en ese identificador. Pásalo a las funciones de `go` o, si el objeto creado tiene un componente de script llamado `controller`, construye la URL de ese componente con `msg.url(nil, id, "controller")`.

Una fábrica de colecciones devuelve una tabla que asocia el identificador de cada objeto del prototipo con el de la instancia creada. Guarda esa tabla para poder eliminar los objetos más adelante.

```lua
local ids = collectionfactory.create("#collection_factory")
-- Later, when the spawned objects are no longer needed:
go.delete(ids)
```

En Godot, `queue_free()` elimina los hijos de forma recursiva. En Defold, `go.delete(id)` los conserva de forma predeterminada. Usa `go.delete(id, true)` para eliminar un objeto y sus descendientes actuales. Si pasas la tabla de la fábrica a `go.delete(ids)`, se eliminan los objetos que figuran en ella y se conservan los demás objetos que hayas añadido después como hijos. Si eliminas de forma recursiva un objeto raíz conocido, también se eliminarán todos los objetos que en ese momento desciendan de él. Consulta [`go.delete()`](/ref/go/#go.delete).

Defold reserva de antemano memoria para un número determinado de objetos de juego y componentes. Si no puedes crear una instancia porque has alcanzado un límite, revisa **Collection ▸ Max Instances** y los límites de los componentes correspondientes en `game.project`. Aumentar todos los límites también aumenta el consumo de memoria.

Los manuales de [fábricas](/manuals/factory/) y [fábricas de colecciones](/manuals/collection-factory/) explican cómo funcionan las propiedades, las transformaciones y la carga dinámica.

### Proxies de colección {#collection-proxies}

Para cargar una colección en Defold, por ejemplo al cargar un nivel, añade un componente **Collection Proxy** a un objeto que persista entre niveles y asigna el archivo `.collection` correspondiente a la propiedad **Collection**.

![Configuración de un proxy de colección en Defold](images/godot/defold_proxy.png)

Solicita la carga enviando `"load"` o `"async_load"` con `msg.post()`. Cuando termine, el proxy responderá con el mensaje `"proxy_loaded"`. A continuación puedes enviar `"init"` y `"enable"` para inicializar y poner en marcha el mundo de la colección cargada. Usa la dirección que recibe on_message en el argumento `sender`.

Así controlas qué mundos están cargados y en ejecución. En Godot, un cambio de escena reemplaza la escena actual automáticamente. En Defold, si también quieres descargar otras colecciones, tienes que pedirlo con el mensaje `"unload"`. El proxy deshabilita y finaliza el mundo antes de descargarlo y responde con `"proxy_unloaded"`. Si necesitas controlar cuándo se ejecuta cada fase, también puedes enviar `"disable"` y `"final"` por separado.

Los objetos de colisión de mundos cargados con distintos proxies no colisionan entre sí, aunque ambos mundos estén cargados al mismo tiempo y sean visibles en la pantalla. En cambio, los objetos de juego y componentes sí pueden intercambiar mensajes si sus URL incluyen el socket de destino.

Antes de implementar las transiciones, lee el [manual de proxies de colección](/manuals/collection-proxy/). Explica cómo cargar y descargar mundos, reenviar la entrada y controlar la frecuencia de actualización de un mundo cargado.

## Recursos y assets del proyecto {#project-resources-and-assets}

Un proyecto de Defold es una carpeta que contiene `game.project`, scripts y recursos. El panel **Assets** reproduce su estructura de carpetas. Como la mayoría de los recursos de Defold se definen en archivos de texto, puedes revisar los cambios en tu sistema de control de versiones.

Al compilar o empaquetar el juego, Defold convierte los recursos de origen a sus formatos de ejecución. Las referencias de la colección principal, las fábricas y los proxies de colección forman un árbol de dependencias. Si añades a la carpeta del proyecto un archivo al que nada hace referencia, el paquete no lo incluirá.

En Defold no existe un equivalente de uso general a las clases `Resource` personalizadas ni a los archivos `.tres` de Godot. Usa los tipos de recursos de Defold para el contenido del motor, y tablas Lua o archivos de datos para los datos propios del juego. La [API `resource`](/ref/resource/) permite crear o modificar los tipos de recursos admitidos en tiempo de ejecución.

Los recursos de una fábrica normal se cargan junto con ella. Activa **Load Dynamically** si quieres aplazar la carga y usa `factory.load()` o `collectionfactory.load()` para prepararlos de forma asíncrona. El contenido de un proxy de colección se carga cuando lo solicitas.

Aplazar la carga de contenido que ya está en el paquete y descargar contenido más adelante son operaciones distintas. Con [Live Update](/manuals/live-update/) puedes excluir contenido del paquete inicial y distribuirlo por separado.

Encontrarás más información en el [manual de gestión de recursos](/manuals/resource/).

---

## Entrada {#input}

El archivo `.input_binding` de Defold cumple la misma función que `InputMap` en Godot. Puedes asignar un disparador de entrada (teclado, mando, ratón, pantalla táctil o texto) al nombre de una acción. Elige el archivo de enlaces de entrada en **Input ▸ Game Binding** dentro de `game.project`.

![Enlaces de entrada](images/input/defold_input.png)

En Defold, el objeto de juego que va a recibir los eventos debe **adquirir el foco de entrada**. Esto lo coloca en la pila de entrada y permite que sus componentes de script y GUI reciban llamadas a `on_input()`.

En la captura, la tecla de espacio está vinculada a `collect`. El siguiente ejemplo es independiente y usa una acción llamada `fire` que también tendrás que añadir a los enlaces de entrada.

En **GDScript**

```gdscript
extends Node

func _input(event):
    if event.is_action_pressed("fire"):
        print("Fire")
```

En **Lua**

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("fire") and action.pressed then
        print("Fire")
    end
end
```

Según el tipo de entrada, la tabla `action` incluye campos como `pressed`, `released` y `value`.

La entrada recorre la pila empezando por el último receptor que adquirió el foco. Devuelve `true` desde `on_input()` para consumir una acción, por ejemplo, cuando un menú ya ha procesado un clic.

En un mundo cargado mediante un proxy, tanto el objeto que contiene el proxy como los receptores de ese mundo deben adquirir el foco de entrada. Si falta uno de los dos pasos, un script de entrada que funcionaba puede dejar de recibir eventos al cambiar de nivel.

Para más detalles, consulta los manuales de [entrada](/manuals/input/), [ratón y entrada táctil](/manuals/input-mouse-and-touch/) y [mandos](/manuals/input-gamepads/).

---

## Física y colisiones {#physics-and-collisions}

El objeto de colisión (**Collision Object**) de Defold equivale a los cuerpos físicos de Godot. Reúne la configuración física **y** las formas de colisión en un solo componente. En `game.project` puedes elegir entre física 2D y 3D. En el App Manifest puedes elegir además la versión del motor de física o desactivar la física por completo.

Defold ofrece cuatro tipos de objetos de colisión.

| Godot | Tipo en Defold | Notas |
|---|---|---|
| `StaticBody2D` / `3D` | `Static` | Permanece inmóvil. Los objetos dinámicos reaccionan al contacto con él. |
| `RigidBody2D` / `3D` | `Dynamic` | El motor de física simula el movimiento y resuelve las colisiones. |
| `CharacterBody2D` / `3D` | `Kinematic` | El motor de física proporciona todos los datos de la colisión. Tu código debe reaccionar y resolverla. |
| `Area2D` | `Trigger` | Solo notifica las entradas y salidas, sin producir una respuesta física. |

Un objeto cinemático de Defold se comporta de manera distinta a un `CharacterBody2D` que usa `move_and_slide()`. Defold detecta los contactos y envía los datos en el mensaje de respuesta a la colisión. Tu script se encarga del movimiento y decide cómo responder al contacto. Si estás programando el control de un personaje, consulta el [manual de resolución de colisiones](/manuals/physics-resolving-collisions/).

Los grupos y las máscaras se identifican con nombres en lugar de números de capa. Para que se registre una colisión, **la máscara de cada objeto debe incluir el grupo del otro**.

![Grupos y máscaras de colisión en Defold](images/physics/collision_groups.png)

En la captura, el objeto de juego llamado `danger` pertenece al grupo `player`, mientras que el objeto llamado `player` pertenece al grupo `danger`. Los nombres de los grupos pueden diferir de los identificadores de los objetos. En este ejemplo, las máscaras permiten que ambos grupos interactúen.

De forma predeterminada, los objetos de colisión envían mensajes a los scripts de su propio objeto de juego. Procesa `"collision_response"`, `"contact_point_response"` o `"trigger_response"` en `on_message()`. Los mensajes de disparador incluyen el campo `enter` para distinguir las entradas de las salidas. Los mensajes de colisión y contacto pueden repetirse mientras los objetos sigan en contacto, así que no cuentes cada mensaje como un golpe nuevo.

También puedes procesar los eventos de física con un [receptor de eventos de colisión](/manuals/physics-events/). Debes elegir uno de los dos mecanismos, ya que registrar un receptor sustituye el envío predeterminado de mensajes de física y el motor deja de enviarlos.

Defold admite varias formas de colisión primitivas y complejas. Encontrarás más detalles en el [manual de formas de colisión](/manuals/physics-shapes).

![Forma de colisión de malla](images/physics/mesh.png)

Para conocer las API y profundizar en el tema, consulta [Introducción a la física](/manuals/physics/), [Objetos de colisión](/manuals/physics-objects/), [Mensajes de colisión](/manuals/physics-messages/) y [Lanzamiento de rayos](/manuals/physics-ray-casts/).

---

## GUI

La interfaz de Defold se construye dentro de un **componente GUI** creado a partir de un archivo `.gui`. En él puedes colocar nodos de caja, de texto o de sector circular, entre otros. Un `.gui_script` controla el componente GUI, de forma similar a un script adjunto a un `CanvasLayer` en Godot.

Estos nodos pertenecen a la GUI y tienen una jerarquía propia, independiente de las transformaciones del objeto de juego. De forma predeterminada, la GUI se dibuja encima del juego y permanece en el mismo lugar aunque se muevan la cámara o el objeto que contiene el componente GUI.

Asigna un `.gui_script` para controlar los nodos con `gui.get_node()`, `gui.set_text()` y otras funciones de `gui`. La API `gui` está disponible solo en los scripts de GUI, y la API `go` solo en los scripts de objetos de juego. Usa mensajes para comunicar ambos tipos de script, como en el ejemplo de la puntuación.

Las plantillas te permiten reutilizar la jerarquía de nodos de otra GUI, de forma parecida a reutilizar un nodo en Godot.

Defold proporciona nodos sencillos con los que puedes construir los controles de la interfaz. En Godot dispones de controles ya preparados, como Button o los contenedores de diseño. Para crear un botón en Defold puedes combinar una caja y un texto, gestionar la entrada en el script de GUI y usar `gui.pick_node()` para comprobar si el puntero está sobre el nodo.

Defold también admite capas (**Layers**) en la GUI que se asemejan a las de `CanvasLayer` en Godot. En Defold se identifican con nombres en lugar de números. Su orden en la lista Layers determina el orden de dibujo.

Los anclajes, los pivotes, los modos de ajuste y los [diseños de GUI](/manuals/gui-layouts/) te ayudan a adaptar la interfaz a distintas pantallas. Tienen algunas funciones en común con los contenedores de diseño de Godot, aunque no son equivalentes exactos.

Para una interfaz más grande o compleja, puedes programar tus propios controles y reglas de diseño o usar una biblioteca de la comunidad como [Druid](https://defold.com/assets/druid/).

Encontrarás más información en los manuales de [GUI](/manuals/gui/) y [scripts de GUI](/manuals/gui-script/).

## Animación {#animation}

Las funciones que en Godot reúne `AnimationPlayer` se reparten en Defold entre varias herramientas de animación.

- La **animación por fotogramas** (flipbook) reproduce secuencias de imágenes en sprites y nodos de caja de la GUI.
- La **animación de modelos** reproduce animaciones esqueléticas importadas en modelos 3D.
- La **animación de propiedades** interpola valores con `go.animate()` o `gui.animate()`.
- **[Spine](https://github.com/defold/extension-spine)**, **[Rive](https://github.com/defold/extension-rive)** y **[SpriteLoop](https://github.com/Balkan-Ram-Games/spriteloop-defold)** son otros formatos de animación disponibles mediante extensiones.

### Tweens y animaciones de propiedades de Defold {#tweens-defold-property-animations}

Un Tween sencillo de Godot equivale a una animación de propiedades de Defold. Los dos ejemplos siguientes mueven un objeto hasta `X = 200` en medio segundo.

En **GDScript**, en un `Node2D`

```gdscript
func move_to_target():
    var tween = create_tween()
    tween.set_trans(Tween.TRANS_QUAD)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(self, "position:x", 200.0, 0.5)
```

En **Lua**, en un script de objeto de juego

```lua
local function move_to_target()
    go.animate(".", "position.x", go.PLAYBACK_ONCE_FORWARD,
        200, go.EASING_OUTQUAD, 0.5)
end
```

Para crear una secuencia que cambie varias propiedades, reproduzca sonidos o active eventos del juego, coordina los pasos en Lua. Defold todavía no tiene un editor de líneas de tiempo específico para animación. El Curve Editor del panel Tools sirve para editar las curvas que definen cómo cambian las propiedades de ParticleFX a lo largo de la vida de una partícula.

Consulta [Animación](/manuals/animation/), [Animación de propiedades](/manuals/property-animation/), [Animación por fotogramas](/manuals/flipbook-animation/) y [Animación de modelos](/manuals/model-animation/). El manual general también enlaza con las extensiones de Spine y Rive.

## Tilemaps

El componente `Tilemap` de Defold usa un **tile source** que contiene una cuadrícula de tiles. Puedes pintar los tiles en varias capas con el editor de tilemaps integrado y modificarlos durante la ejecución mediante la API `tilemap`.

El tilemap integrado de Defold usa una cuadrícula rectangular. Por ahora no puedes trasladar directamente a Defold los conjuntos de terrenos ni las reglas de colocación automática de tiles de Godot. Puedes reproducir el comportamiento que necesites con código o usar una herramienta externa que exporte mapas a Defold, como [Tiled](https://doc.mapeditor.org/en/stable/manual/export-defold/?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website) o [TileSetter](https://www.tilesetter.org/docs/exporting?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website#defold).

Consulta el [manual de tilemaps](/manuals/tilemap/).

---

## Pipeline de renderizado {#rendering-pipeline}

Defold ofrece un pipeline de renderizado totalmente programable, con un archivo `.render` personalizado, un `.render_script` y compatibilidad con shaders. El pipeline predeterminado que incorpora el motor es suficiente para la mayoría de los juegos.

El script de render predeterminado de Defold dibuja el contenido 2D y 3D habitual. Un `.render_script` personalizado controla las pasadas de dibujo, los destinos de renderizado y otras operaciones de renderizado. Las etiquetas de los materiales le permiten seleccionar grupos de componentes mediante predicados de render. Defold incluye renderizado basado en física (PBR) y la comunidad ofrece numerosos pipelines y shaders personalizados.


Defold usa shaders GLSL, con archivos distintos para los programas de vértices y de fragmentos. Godot usa un lenguaje de sombreado parecido a GLSL con funciones y variables propias del motor, por lo que los shaders que procedan de Godot o de otras fuentes como Shadertoy pueden necesitar adaptaciones. Consulta los requisitos de Defold en el [manual de shaders](/manuals/shader/).

Los **materiales** de Defold asocian los programas de vértices y de fragmentos (shaders) con sus texturas, constantes y atributos. La carpeta `builtins` contiene los materiales predeterminados, que puedes usar como punto de partida.

Cuando necesites modificar el comportamiento predeterminado, consulta [Renderizado](/manuals/render/), [Materiales](/manuals/material/) y [Shaders](/manuals/shader/).

### Orden de dibujo y capas {#draw-order-and-layers}

El entero `z_index` de Godot no se corresponde directamente con una propiedad de Defold. Defold usa internamente un motor 3D y el eje Z representa una coordenada espacial real. Según la configuración de renderizado, desplazar un objeto en Z puede tener un efecto distinto al de cambiar su profundidad de dibujo. En Godot, en cambio, ese entero sirve específicamente para ordenar elementos en 2D.

En la configuración ortográfica **predeterminada** de Defold solo se dibujan los objetos cuya posición Z está entre -1.0 y 1.0. Puedes usar valores como 0.1 o 0.2 para las capas y cambiar el intervalo enviando un mensaje al script de render. Dentro de ese intervalo, la configuración básica usa la posición Z del objeto de juego o del componente Sprite para ordenar el dibujo. Los elementos con un valor Z mayor aparecen encima de los que tienen un valor menor, un efecto parecido al de `z_index` en Godot. El resultado puede cambiar si pasas a una cámara en perspectiva o modificas el `.render_script`.

Los nodos GUI de Defold ignoran la coordenada Z del mundo. De forma predeterminada, los componentes GUI se dibujan en una pasada independiente después de los sprites del mundo, por lo que cambiar la posición Z de un nodo GUI no afecta a su orden de dibujo. El orden de dibujo en la GUI depende de la jerarquía de los nodos (de arriba abajo en el panel Outline) y de las capas `Layers`. Estas tienen prioridad sobre el orden de los nodos y permiten agrupar las llamadas de dibujo, de forma parecida a las capas de `CanvasLayer`.

### Cámaras y coordenadas {#cameras-and-coordinates}

Añade un componente `Camera` a un objeto de juego. Al mover el objeto, también moverás la cámara. Para una vista 2D típica, configura una proyección ortográfica. Para 3D puedes usar una proyección en perspectiva.

El script de render predeterminado selecciona automáticamente la última cámara habilitada. Si no hay cámaras, usa una vista ortográfica 2D. Si hay una sola cámara, se usa esa. Puedes empezar con esta configuración y personalizar el renderizado cuando tu juego lo necesite.

La cámara cambia la correspondencia entre las coordenadas del mundo y las de la pantalla. Cuando proceses la entrada del puntero en el mundo, usa las funciones de conversión de la [API de cámara](/ref/camera/) para obtener la posición en el mundo a partir de la posición del puntero. De forma predeterminada, la detección de nodos GUI bajo el puntero sigue usando coordenadas de la GUI.

Consulta el [manual de cámara](/manuals/camera/) para más detalles sobre la proyección, el zoom y la conversión de coordenadas.

---

## Exportar un juego {#exporting-a-game}

En Defold, exportar el juego se llama **empaquetar** (bundling). Elige **Project ▸ Bundle**, selecciona la plataforma de destino y configura las opciones del paquete. El editor incluye todas las herramientas de compilación, así que no necesitas instalar por separado plantillas de exportación como las de Godot.

El archivo `game.project` contiene los ajustes del proyecto y de las plataformas, como la colección principal, los enlaces de entrada y el tamaño de la pantalla. Es posible que también tengas que cumplir requisitos de la tienda y de firma para cada plataforma. Si tu proyecto incluye extensiones nativas, necesitas conexión de red para compilar el motor personalizado con el servicio de compilación en la nube, salvo que configures el servicio para que funcione en local.

El tamaño final del paquete depende de los assets, las extensiones y las opciones de compilación. Genera un informe `Build Report` para ver qué incluye tu juego.

Consulta [Empaquetado](/manuals/bundling/), [Configuración del proyecto](/manuals/project-settings/) y [HTML5](/manuals/html5/). Conviene probar pronto un paquete en la plataforma de destino, especialmente si el juego usa shaders, extensiones nativas o servicios de la plataforma.

## Bibliotecas y extensiones {#libraries-and-extensions}

Puedes añadir dependencias de bibliotecas (**Library Dependencies**) a un proyecto de Defold para reutilizar scripts y recursos. Añade las URL de sus archivos comprimidos en `game.project` y descarga las bibliotecas. Un buen lugar para buscarlas es el [Asset Portal](https://defold.com/assets/) de Defold. La extensión del editor **Asset Store** también permite buscar y descargar assets directamente desde el editor, como en Godot.

Para personalizar el editor, puedes usar **Editor Scripts and UI**. Permite añadir comandos, automatizar tareas y crear interfaces propias, por ejemplo para agilizar la edición de niveles, crear recursos o colocar tiles automáticamente. Cumple algunas de las funciones de `EditorPlugin` y `@tool` en Godot, pero usa el ciclo de vida y la API `editor` de Defold.

Las extensiones nativas (**Native Extensions**) permiten exponer código nativo a los scripts y añadir componentes e integraciones con las plataformas cuando necesitas ampliar el motor más allá de Lua. Cumplen una función similar a GDExtension, con una API y un proceso de compilación distintos.

Consulta [Bibliotecas](/manuals/libraries/), [Scripts de editor](/manuals/editor-scripts/) y [Extensiones nativas](/manuals/extensions/).

## Recarga en caliente {#hot-reload}

En Defold puedes recargar recursos mientras el juego está en ejecución. Compila y ejecuta el juego, modifica un recurso que admita la recarga, guarda el cambio y selecciona **File ▸ Hot Reload** para actualizarlo. La recarga en caliente también funciona si seleccionas como destino una compilación de depuración que se ejecuta en un dispositivo.

Al recargar un script no se vuelve a llamar a `init()`. Los datos de las instancias se conservan, así que los nuevos valores de inicialización no aparecerán de forma automática en `self`. Usa `on_reload(self)` para ajustar el estado existente o vuelve a compilar si quieres empezar desde cero. Si recargas un módulo Lua que devuelve una tabla nueva, los demás scripts pueden seguir haciendo referencia a la tabla anterior. Consulta el [manual de módulos](/manuals/modules/) para más detalles.

Consulta el [manual de recarga en caliente](/manuals/hot-reload/).

## Puntos de interrupción y depuración {#breakpoints-and-debugging}

El depurador integrado del editor permite establecer puntos de interrupción, avanzar paso a paso e inspeccionar valores. Usa Console para ver la salida durante la ejecución y Build Errors para consultar los problemas de compilación. El perfilador te permite examinar el tiempo por fotograma, el consumo de memoria y el renderizado. Los informes de compilación muestran qué recursos contribuyen al tamaño del paquete.

Consulta [Depuración de la lógica del juego](/manuals/debugging-game-logic/) y [Análisis de rendimiento](/manuals/profiling/).

## Flujos de trabajo automatizados {#automated-workflows}

Defold ofrece varias interfaces para automatizar tareas y trabajar con herramientas de desarrollo asistido por IA. Los scripts de editor permiten automatizar tareas repetitivas. La API HTTP del editor, documentada mediante OpenAPI, permite que herramientas externas y agentes de IA inspeccionen proyectos, ejecuten comandos e inicien compilaciones. El servicio HTTP del motor y la extensión Automation Bridge permiten inspeccionar el juego en ejecución, simular entradas y capturar pantallas. Con estas herramientas, agentes de programación como Codex, Claude Code o Cursor pueden modificar un proyecto, compilar el juego, probar su comportamiento y repetir el ciclo hasta resolver un problema.

Encontrarás más detalles en [Automatización](/manuals/automation/), [API HTTP del editor](/manuals/editor-http-api/), [Servicio del motor](/manuals/engine-service/) y [Pruebas automatizadas](/manuals/automated-testing/).

---

## Errores frecuentes {#common-pitfalls}

### Tratar una colección como un nodo raíz {#treating-a-collection-as-a-root-node}

Una colección de Defold describe los objetos de juego y sus relaciones. No se convierte en un objeto raíz durante la ejecución. Para coordinar los objetos de un nivel, añade un objeto de juego con su propio script. Consulta [Colecciones y mundos](#collections-and-worlds).

### Eliminar una jerarquía {#deleting-a-hierarchy}

En Godot, `queue_free()` también elimina los descendientes del nodo. En Defold, `go.delete(id)` conserva los objetos hijos a menos que solicites eliminarlos de forma recursiva. En [Fábricas](#factories) encontrarás un ejemplo y verás cómo eliminar los objetos que crea una fábrica de colecciones.

### Dar por sentada la herencia de escenas {#expecting-scene-inheritance}

Defold no tiene el mismo sistema de herencia de escenas que Godot, por lo que no puedes modificar libremente la estructura de una escena derivada de la misma manera. Puedes reutilizar prototipos y colecciones y personalizar sus instancias con propiedades o scripts. Consulta [Colecciones y mundos](#collections-and-worlds).

### Llamar a otro script mediante una referencia al objeto {#calling-another-script-through-an-object-reference}

El identificador de un objeto de juego en Defold no da acceso general a las funciones de otra instancia de script. Usa mensajes para comunicar componentes o guarda las funciones compartidas en un módulo Lua. Consulta [Mensajes y direccionamiento](#messages-and-addressing) y [Autoloads y estado compartido](#autoloads-and-shared-state).

### Guardar el estado de una instancia en una variable local de archivo {#keeping-instance-state-in-a-top-level-local}

Las instancias que usan un mismo archivo de script comparten las variables locales declaradas en el ámbito del archivo. Si cambias una de esas variables para una instancia, el cambio puede afectar a las demás. Guarda el estado propio de cada instancia en `self`, como se explica en [Datos de instancia y datos locales](#instance-data-vs-local-data).

### Suponer que la entrada se habilita automáticamente {#assuming-input-is-enabled-automatically}

Un objeto de juego de Defold debe adquirir el foco de entrada para que sus componentes puedan recibirla. Si el mundo se carga con un proxy, el objeto que contiene ese proxy también necesita el foco. En [Entrada](#input) se explican los enlaces de entrada, el foco y el funcionamiento de la pila.

### Esperar que un objeto cinemático se deslice automáticamente {#expecting-automatic-sliding-from-a-kinematic-collider}

Defold detecta los contactos de los objetos de colisión cinemáticos. Para reproducir el comportamiento de `move_and_slide()` de Godot, tu script debe encargarse del movimiento y de la respuesta a las colisiones. Consulta [Física y colisiones](#physics-and-collisions).

### Configurar solo una de las máscaras de colisión {#configuring-only-one-collision-mask}

Si solo uno de los dos objetos está configurado para interactuar con el otro, la colisión no se registrará. La máscara de cada objeto debe incluir el grupo del otro. Consulta [Física y colisiones](#physics-and-collisions).

### Copiar las coordenadas 2D sin adaptarlas {#copying-2d-coordinates-unchanged}

En Godot y en la configuración 2D habitual de Defold, el eje Y apunta en sentidos opuestos. Si copias código de movimiento, puede que el objeto avance en la dirección equivocada. Además, si hay una cámara, las posiciones de pantalla y del mundo pueden diferir. Consulta [Coordenadas](#coordinates) y [Cámaras y coordenadas](#cameras-and-coordinates).

### Usar la coordenada Z del mundo para ordenar los nodos GUI {#using-world-z-to-sort-gui-nodes}

En Defold, cambiar la posición Z de un nodo GUI no altera su orden de dibujo. Usa el orden de los nodos y las capas de la GUI como se explica en [Orden de dibujo y capas](#draw-order-and-layers).

### Esperar que la recarga en caliente reinicie el objeto {#expecting-hot-reload-to-restart-the-object}

Al recargar un script en caliente no se vuelve a ejecutar `init()`, por lo que las instancias pueden conservar los valores que ya tenían. En [Recarga en caliente](#hot-reload) se explica cómo gestionar el estado y la recarga de módulos.

### Esperar que descargar un nivel borre el estado compartido {#expecting-a-level-unload-to-clear-shared-state}

Tanto el estado de un Autoload en Godot como los datos en caché de un módulo Lua pueden persistir entre niveles. Restablece los datos compartidos de forma explícita cuando sea necesario. A diferencia de un nodo Autoload, un módulo Lua no recibe callbacks automáticamente. Consulta [Autoloads y estado compartido](#autoloads-and-shared-state).

## ¿A dónde ir desde aquí? {#where-to-go-from-here}

En el [centro de aprendizaje de Defold](https://defold.com/learn/) encontrarás manuales, ejemplos, tutoriales, videos y cursos que te ayudarán a dar los primeros pasos y a conocer el motor más a fondo. Puedes empezar por estos recursos.

- [Bloques de construcción](/manuals/building-blocks/)
- [Direccionamiento](/manuals/addressing/)
- [Paso de mensajes](/manuals/message-passing/)
- [Ejemplos de Defold](/examples/)
- [Tutoriales](/tutorials/)
- [Referencia de la API](/ref/go/)

Si te atascas, pide ayuda en el [foro de Defold](https://forum.defold.com/) o en [Discord](https://defold.com/discord/). Comparte un proyecto pequeño y describe el comportamiento de Godot que intentas reproducir para que a los demás les resulte más fácil ayudarte.
