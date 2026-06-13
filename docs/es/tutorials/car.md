---
title: Crear un auto sencillo en Defold.
brief: Si eres nuevo en Defold, esta guía te ayudará a orientarte correctamente en el editor. También explica las ideas básicas y los bloques de construcción más comunes en Defold: objetos de juego, colecciones, scripts y sprites.
---

# Crear un auto

Si eres nuevo en Defold, esta guía te ayudará a orientarte correctamente en el editor. También explica las ideas básicas y los bloques de construcción más comunes en Defold: objetos de juego, colecciones, scripts y sprites.

Vamos a empezar desde un proyecto vacío y trabajar paso a paso hasta una aplicación muy pequeña y jugable. Al final, con suerte tendrás una idea de cómo funciona Defold y estarás listo para abordar un tutorial más extenso o entrar directamente en los manuales.

::: sidenote
A lo largo del tutorial, las descripciones detalladas sobre conceptos y cómo hacer ciertos momentos se marcan como este párrafo. Si sientes que estas secciones entran en demasiado detalle, puedes saltarlas.
:::

## Crear un proyecto nuevo

![New Project](images/new_empty.png)

1. Inicia Defold.
2. Selecciona *New Project* a la izquierda.
3. Selecciona la pestaña *From Template*.
4. Selecciona *Empty Project*
5. Selecciona una ubicación para el proyecto en tu disco local.
6. Haz click en *Create New Project*.

## El editor

Empieza creando un [proyecto nuevo](/manuals/project-setup/) y abriéndolo en el editor. Si haces doble click en el archivo *main/main.collection*, el archivo se abrirá:

![Editor overview](../manuals/images/editor/editor2_overview.png)

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

![Build](images/car/start_build_and_launch.png)

Una pantalla negra quizá no sea muy emocionante, pero es una aplicación de juego Defold en ejecución y podemos modificarla fácilmente para convertirla en algo más interesante. Así que hagamos eso.

::: sidenote
El editor Defold trabaja con archivos. Al hacer doble click en un archivo en el *Assets pane*, lo abres en un editor adecuado. Luego puedes trabajar con el contenido del archivo.

Cuando termines de editar un archivo, tienes que guardarlo. Selecciona <kbd>File ▸ Save</kbd> en el menú principal. El editor da una pista agregando un asterisco '\*' al nombre del archivo en la pestaña para cualquier archivo que contenga cambios sin guardar.

![File with unsaved changes](images/car/file_changed.png)
:::

## Armar el auto

Lo primero que haremos es crear una colección nueva. Una colección es un contenedor de objetos de juego que has colocado y posicionado. Las colecciones se usan con mayor frecuencia para construir niveles de juego, pero son muy útiles siempre que necesites reutilizar grupos y/o jerarquías de objetos de juego que pertenecen juntos. Puede ser útil pensar en las colecciones como una especie de prefab.

Haz click en la carpeta *main* en el *Assets pane*, luego haz click derecho y selecciona <kbd>New ▸ Collection File</kbd>. También puedes seleccionar <kbd>File ▸ New ▸ Collection File</kbd> desde el menú principal.

![New Collection file](images/car/start_new_collection.png)

Nombra el nuevo archivo de colección *car.collection* y ábrelo. Vamos a usar esta colección nueva y vacía para construir un auto pequeño a partir de un par de objetos de juego. Un objeto de juego es un contenedor de componentes (como sprites, sonidos, scripts de lógica, etc.) que usas para construir tu juego. Cada objeto de juego se identifica de forma única en el juego por su id. Los objetos de juego pueden comunicarse entre sí mediante paso de mensajes, pero hablaremos de eso más adelante.

Además, es posible crear un objeto de juego en el lugar dentro de una colección, como hicimos aquí. Eso da como resultado un objeto único. Puedes copiar ese objeto, pero cada copia es separada---cambiar una no afecta a las demás. Esto significa que si creas 10 copias de un objeto de juego y te das cuenta de que quieres cambiarlas todas, tendrás que editar las 10 instancias del objeto. Por lo tanto, los objetos de juego creados en el lugar deben usarse para objetos de los que no pretendes hacer muchas copias.

Sin embargo, un objeto de juego almacenado en un _archivo_ funciona como prototipo (también conocido como "prefabs" o "blueprints" en otros motores). Cuando colocas instancias de un objeto de juego almacenado en archivo en una colección, cada objeto se coloca _por referencia_---es un clon basado en el prototipo. Si decides que necesitas cambiar el prototipo, cada objeto de juego colocado basado en ese prototipo se actualiza al instante.

![Add car gameobject](images/car/start_add_car_gameobject.png)

Selecciona el nodo raíz "Collection" en la vista *Outline*, haz click derecho y selecciona <kbd>Add Game Object</kbd>. Aparecerá un nuevo objeto de juego con el id "go" en la colección. Márcalo y define su id como "car" en la vista *Properties*. Hasta ahora, "car" no es nada interesante. Está vacío, no tiene representación visual ni lógica. Para agregar una representación visual, necesitamos agregar un _componente_ sprite.

Los componentes se usan para extender objetos de juego con presencia (gráficos, sonido) y funcionalidad (spawn factories, colisiones, comportamientos con script). Un componente no puede existir por sí mismo, sino que debe residir dentro de un objeto de juego. Los componentes normalmente se definen en el lugar en el mismo archivo que el objeto de juego. Sin embargo, si quieres reutilizar un componente puedes almacenarlo en un archivo separado (como puedes hacer con los objetos de juego) e incluirlo como referencia en cualquier archivo de objeto de juego. Algunos tipos de componente (scripts Lua, por ejemplo) deben colocarse en un archivo de componente separado y luego incluirse como referencia en tus objetos.

Ten en cuenta que no manipulas componentes directamente---puedes mover, rotar, escalar y animar propiedades de objetos de juego que a su vez contienen componentes.

![Add car component](images/car/start_add_car_component.png)

Selecciona el objeto de juego "car", haz click derecho y selecciona <kbd>Add Component</kbd>, luego selecciona *Sprite* y haz click en *Ok*. Si marcas el sprite en la vista *Outline*, verás que necesita que se definan algunas propiedades:

Image
: Esto requiere una fuente de imagen para el sprite. Crea un archivo de imagen de atlas marcando "main" en la vista *Assets pane*, haciendo click derecho y seleccionando <kbd>New ▸ Atlas File</kbd>. Nombra el nuevo archivo de atlas *sprites.atlas* y haz doble click en él para abrirlo en el editor de atlas. Guarda los siguientes dos archivos de imagen en tu computadora y arrástralos a *main* en la vista *Assets pane*. Ahora puedes marcar el nodo raíz Atlas en el editor de atlas, hacer click derecho y seleccionar <kbd>Add Images</kbd>. Agrega la imagen del auto y la del neumático al atlas y guarda. Ahora puedes seleccionar *sprites.atlas* como fuente de imagen para el componente sprite en el objeto de juego "car" de la colección "car".

Imágenes para nuestro juego:

![Car image](images/car/start_car.png)
![Tire image](images/car/start_tire.png)

Agrega estas imágenes al atlas:

![Sprites atlas](images/car/start_sprites_atlas.png)

![Sprite properties](images/car/start_sprite_properties.png)

Default Animation
: Define esto como "car" (o como hayas nombrado la imagen del auto). Cada sprite necesita una animación predeterminada que se reproduce cuando se muestra en el juego. Cuando agregas imágenes a un atlas, Defold crea convenientemente animaciones de un frame (estáticas) para cada archivo de imagen.

## Completar el auto

Continúa agregando dos objetos de juego más en la colección. Llámalos "left_wheel" y "right_wheel" y pon un componente sprite en cada uno, mostrando la imagen del neumático que agregamos a *sprites.atlas*. Luego toma los objetos de juego de las ruedas y suéltalos sobre "car" para hacerlos hijos de "car". Los objetos de juego que son hijos de otros objetos de juego estarán adjuntos a su padre cuando el padre se mueva. También se pueden mover individualmente, pero todo el movimiento ocurre relativo al objeto padre. Para los neumáticos esto es perfecto, ya que queremos que se queden pegados al auto y podemos simplemente rotarlos ligeramente a izquierda y derecha cuando dirigimos el auto. Una colección puede contener cualquier número de objetos de juego, lado a lado u organizados en árboles padre-hijo complejos, o una mezcla.

Mueve los objetos de juego de los neumáticos a su lugar seleccionándolos y luego eligiendo <kbd>Scene ▸ Move Tool</kbd>. Toma las flechas de los ejes, o el cuadrado verde central, para mover el objeto a una buena posición. Lo último que necesitamos hacer es asegurarnos de que los neumáticos se dibujen debajo del auto. Lo hacemos definiendo el componente Z de la posición en -0.5. Cada elemento visual en un juego se dibuja de atrás hacia adelante, ordenado por su valor Z. Un objeto con un valor Z de 0 se dibujará encima de un objeto con un valor Z de -0.5. Como el valor Z predeterminado del objeto de juego del auto es 0, el nuevo valor en los objetos de neumático los pondrá debajo de la imagen del auto.

![Car collection complete](images/car/start_car_collection_complete.png)

## El script del auto

La última pieza del puzzle es un _script_ para controlar el auto. Un script es un componente que contiene un programa que define comportamientos de objetos de juego. Con scripts puedes especificar las reglas de tu juego, cómo deben responder los objetos a varias interacciones (con el jugador y también con otros objetos). Todos los scripts se escriben en el lenguaje de programación Lua. Para poder trabajar con Defold, tú o alguien de tu equipo necesita aprender a programar en Lua.

Marca "main" en el *Assets pane*, haz click derecho y selecciona <kbd>New ▸ Script File</kbd>. Nombra el nuevo archivo *car.script*, luego agrégalo al objeto de juego "car" marcando "car" en la vista *Outline*, haciendo click derecho y seleccionando <kbd>Add Component File</kbd>. Selecciona *car.script* y haz click en *OK*. Guarda el archivo de colección.

Haz doble click en *car.script* para abrirlo.

::: sidenote
Defold proporciona varias funciones de ciclo de vida para programar lógica de juego. Lee más sobre ellas en el [manual de Script](/manuals/script).
:::

Empieza eliminando las funciones `final`, `on_message` y `on_reload`, ya que no las necesitaremos
para este tutorial.

Luego, agrega las siguientes líneas de código antes de que empiece la función init.

```lua
-- Constantes
local turn_speed = 0.1                           									  -- Factor de Slerp
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)     -- 30 grados
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 grados
local steer_angle_zero = vmath.quat_rotation_z(0)									  -- Cero grados
local wheels_vector = vmath.vector3(0, 72, 0)         		        	-- Vector desde el centro de los pares de ruedas traseras y delanteras

local acceleration = 100 																						-- La aceleración del auto

-- prehashea los inputs
local left = hash("left")
local right = hash("right")
local accelerate = hash("accelerate")
local brake = hash("brake")
```

Los cambios hechos aquí son bastante simples: solo agregamos un montón de `constants` a nuestro script que usaremos más adelante para programar nuestro auto.

::: sidenote
Presta atención a cómo almacenamos los hashes de antemano en variables. De hecho, es una buena práctica hacerlo, ya que hace que tu código sea más legible y eficiente.
:::

Luego, edita la función `init` para que contenga lo siguiente:

```lua
function init(self)
	-- Envía un mensaje al script de render (ver builtins/render/default.render_script) para definir el color de limpieza.
	-- Esto cambia el color de fondo del juego. El vector4 contiene información de color
	-- por canal de 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 y Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )		--<1>

	-- Adquiere foco de input para que podamos reaccionar al input
	msg.post(".", "acquire_input_focus")		-- <2>

	-- Algunas variables
	self.steer_angle = vmath.quat()				 -- <3>
	self.direction = vmath.quat()

	-- Velocidad y aceleración son relativas al auto (no rotadas)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Vector de input. Esto se modifica luego en la función on_input
	-- para almacenar el input.
	self.input = vmath.vector3()
end
```

¿Te preguntas qué acabamos de cambiar? Aquí hay una explicación.

1. Envía un mensaje a nuestro script de render pidiéndole que defina el color de fondo en gris. Los scripts de render son scripts especiales en Defold que controlan cómo se muestran los objetos en la pantalla.
2. Para escuchar acciones de input en un componente script o script GUI, el mensaje `acquire_input_focus` debe enviarse al objeto de juego que contiene el componente. En nuestro caso enviamos este mensaje al gameobject que contiene el script del auto.
3. Luego declaramos algunas variables que usaremos para seguir el estado actual de nuestro auto.

Eso fue fácil, ¿no? Continuaremos ahora editando la función `update` para que contenga lo siguiente:

```lua
function update(self, dt)
	-- Define la aceleración al input y
	self.acceleration.y = self.input.y * acceleration				-- <1>

	-- Calcula las nuevas posiciones de las ruedas delanteras y traseras
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)								-- <2>

	-- Calcula la nueva dirección del auto
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)			-- <3>

	-- Calcula la nueva velocidad según la aceleración actual
	self.velocity = self.velocity + self.acceleration * dt			-- <4>

	-- Actualiza la posición según la velocidad y dirección actuales
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)																			-- <5>

	-- Interpola las ruedas usando vmath.slerp
	if self.input.x > 0 then																		-- <6>
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Actualiza la rotación de las ruedas
	go.set_rotation(self.steer_angle, "left_wheel")					-- <7>
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Define la rotación del objeto de juego a la dirección
	go.set_rotation(self.direction)

	-- reinicia aceleración e input
	self.acceleration = vmath.vector3()								-- <8>
	self.input = vmath.vector3()
end
```

¡Esa fue una función enorme! Pero no te preocupes, así funciona todo:

1. Primero definimos nuestro vector de aceleración según nuestro vector de input. Esto asegura que la aceleración del auto esté en la dirección del input.
2. Luego, el desplazamiento de ambas ruedas se calcula según la lógica simple de que, mientras las ruedas traseras del auto siempre se mueven hacia adelante, la rueda delantera se mueve en la dirección hacia la que está girada.
3. Según el desplazamiento de ambas ruedas, se calcula la nueva dirección de movimiento de nuestro auto.
4. Aquí agregamos la aceleración calculada a la velocidad.
5. Finalmente, actualizamos la posición del auto según nuestra velocidad actual.
6. Hacemos slerp del ángulo de dirección según nuestro input izquierda/derecha. Esto se hace para que las ruedas no cambien bruscamente cada vez que cambia el input.
7. La rotación de las ruedas se define entonces según el ángulo de dirección actual del auto. De forma similar, la rotación del auto se define según la dirección en la que se mueve actualmente.
8. Finalmente, reiniciamos los vectores de aceleración e input.

Finalmente, es momento de hacer que nuestro auto reaccione al input. Actualiza la función `on_input` para que se vea así:

```lua
function on_input(self, action_id, action)
	-- define el vector de input para corresponder a la pulsación de tecla
	if action_id == left then
		self.input.x = -1
	elseif action_id == right then
		self.input.x = 1
	elseif action_id == accelerate then
		self.input.y = 1
	elseif action_id == brake then
		self.input.y = -1
	end
end
```

Esta función en realidad es bastante simple: solo aceptamos el input y definimos nuestro vector de input.

No olvides guardar tus ediciones.

## Input

Todavía no hay acciones de input configuradas, así que arreglemos eso. Abre el archivo */input/game.input_bindings* y agrega bindings *key_trigger* para "accelerate", "brake", "left" y "right". Las asignamos a las teclas de flecha (KEY_LEFT, KEY_RIGHT, KEY_UP y KEY_DOWN):

![Input bindings](images/car/start_input_bindings.png)

## Agregar el auto al juego

Ahora el auto está listo para rodar. Lo hemos creado dentro de "car.collection", pero todavía no existe en el juego. Eso es porque el motor actualmente carga "main.collection" al iniciar. Para arreglarlo, simplemente tenemos que agregar *car.collection* a *main.collection*. Abre *main.collection*, marca el nodo raíz "Collection" en la vista *Outline*, haz click derecho y selecciona <kbd>Add Collection From File</kbd>, selecciona *car.collection* y haz click en *OK*. Ahora el contenido de *car.collection* se colocará en *main.collection* como nuevas instancias. Si cambias el contenido de *car.collection*, cada instancia de la colección se actualizará automáticamente cuando se compile el juego.

![Adding the car collection](images/car/start_adding_car_collection.png)

Ahora, selecciona <kbd>Project ▸ Build</kbd> y lleva tu nuevo auto a dar una vuelta.
Notarás que ahora puedes moverte para hacer que el auto se mueva a tu voluntad. Pero algo todavía no está bien. Cuando sueltas los controles, el auto no se detiene, como debería. ¡Es momento de agregar eso!

## Drag al rescate

Siempre que un objeto se mueve en el mundo real, la fuerza de drag actúa contra el objeto y hace que desacelere. Esta fuerza cae casi proporcional al cuadrado de la velocidad del objeto en movimiento y, por lo tanto, puede describirse como `D = k * |V| * V`, donde `k` es una constante, `V` es la velocidad y `|V|` su magnitud (rapidez). Agreguemos eso.

En la sección de constantes en la parte superior del script, agrega la siguiente constante

```lua
local drag = 1.1	        --la constante de drag <1>
```

Luego, en la función update, justo encima de esta línea, agrega las siguientes líneas y guarda el archivo.

```lua
function update(self, dt)
	...
  -- Calcula la nueva velocidad según la aceleración actual
	self.velocity = self.velocity + self.acceleration * dt
	...
end
```

```lua
function update(self, dt)
	...
	-- La rapidez es la magnitud de la velocidad
	local speed = vmath.length_sqr(self.velocity)

	-- Aplica drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Detén si ya vamos suficientemente lento
	if speed < 0.5 then self.velocity = vmath.vector3(0) end
	...
end
```

1. Declara el valor de drag como constante.
2. Calcula la rapidez con la que nos movemos.
3. Aplica el drag a la aceleración actual según la fórmula
4. Detén si el auto ya va suficientemente lento.

## El script completo del auto

Después de completar los pasos anteriores, tu *car.script* debería verse así:

```lua
local turn_speed = 0.1                           				          	-- Factor de Slerp
local max_steer_angle_left = vmath.quat_rotation_z(math.pi / 6)	    -- 30 grados
local max_steer_angle_right = vmath.quat_rotation_z(-math.pi / 6)   -- -30 grados
local steer_angle_zero = vmath.quat_rotation_z(0)				          	-- Cero grados
local wheels_vector = vmath.vector3(0, 72, 0)         				      -- Vector desde el centro de los pares de ruedas traseras y delanteras

local acceleration = 100 		                      									-- La aceleración del auto
local drag = 1.1                                                  	-- la constante de drag

function init(self)
	-- Envía un mensaje al script de render (ver builtins/render/default.render_script) para definir el color de limpieza.
	-- Esto cambia el color de fondo del juego. El vector4 contiene información de color
	-- por canal de 0-1: Red = 0.2. Green = 0.2, Blue = 0.2 y Alpha = 1.0
	msg.post("@render:", "clear_color", { color = vmath.vector4(0.2, 0.2, 0.2, 1.0) } )

	-- Adquiere foco de input para que podamos reaccionar al input
	msg.post(".", "acquire_input_focus")

	-- Algunas variables
	self.steer_angle = vmath.quat()
	self.direction = vmath.quat()

	-- Velocidad y aceleración son relativas al auto (no rotadas)
	self.velocity = vmath.vector3()
	self.acceleration = vmath.vector3()

	-- Vector de input. Esto se modifica luego en la función on_input
	-- para almacenar el input.
	self.input = vmath.vector3()
end

function update(self, dt)
	-- Define la aceleración al input y
	self.acceleration.y = self.input.y * acceleration

	-- Calcula las nuevas posiciones de las ruedas delanteras y traseras
	local front_vel = vmath.rotate(self.steer_angle, self.velocity)
	local new_front_pos = vmath.rotate(self.direction, wheels_vector + front_vel)
	local new_back_pos = vmath.rotate(self.direction, self.velocity)

	-- Calcula la nueva dirección del auto
	local new_dir = vmath.normalize(new_front_pos - new_back_pos)
	self.direction = vmath.quat_rotation_z(math.atan2(new_dir.y, new_dir.x) - math.pi / 2)

	-- La rapidez es la magnitud de la velocidad
	local speed = vmath.length(self.velocity)

	-- Aplica drag
	self.acceleration = self.acceleration - speed * self.velocity * drag

	-- Detén si ya vamos suficientemente lento
	if speed < 0.5 then self.velocity = vmath.vector3() end

	-- Calcula la nueva velocidad según la aceleración actual
	self.velocity = self.velocity + self.acceleration * dt

	-- Actualiza la posición según la velocidad y dirección actuales
	local pos = go.get_position()
	pos = pos + vmath.rotate(self.direction, self.velocity)
	go.set_position(pos)

	-- Interpola las ruedas usando vmath.slerp
	if self.input.x > 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_right)
	elseif self.input.x < 0 then
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, max_steer_angle_left)
	else
		self.steer_angle = vmath.slerp(turn_speed, self.steer_angle, steer_angle_zero)
	end

	-- Actualiza la rotación de las ruedas
	go.set_rotation(self.steer_angle, "left_wheel")
	go.set_rotation(self.steer_angle, "right_wheel")

	-- Define la rotación del objeto de juego a la dirección
	go.set_rotation(self.direction)

	-- reinicia aceleración e input
	self.acceleration = vmath.vector3()
	self.input = vmath.vector3()
end

function on_input(self, action_id, action)
	-- define el vector de input para corresponder a la pulsación de tecla
	if action_id == hash("left") then
		self.input.x = -1
	elseif action_id == hash("right") then
		self.input.x = 1
	elseif action_id == hash("accelerate") then
		self.input.y = 1
	elseif action_id == hash("brake") then
		self.input.y = -1
	end
end
```

## Probar el juego final

Ahora, selecciona <kbd>Project ▸ Build</kbd> desde el menú principal y lleva tu nuevo auto a dar una vuelta.

Esto concluye este tutorial introductorio. Aquí tienes un conjunto de desafíos que quizá quieras abordar por tu cuenta:

1. Actualmente el auto se mueve con la misma aceleración hacia adelante y hacia atrás. Quizá quieras cambiar esto para que el auto se mueva más lento cuando va hacia atrás.
2. Convierte algunas de las constantes (como acceleration) en `properties` para que puedan cambiarse en distintas instancias del auto.
3. Agrega sonidos a tu auto y haz que haga vroom. ([Pista](/manuals/sound/))

Ahora sigue adelante y sumérgete en Defold. Tenemos muchos [manuales y tutoriales](/learn) preparados para guiarte, y si te quedas atascado, eres muy bienvenido al [foro](//forum.defold.com).

¡Feliz Defolding!
