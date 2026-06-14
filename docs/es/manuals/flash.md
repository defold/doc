---
title: Defold para usuarios de Flash
brief: Esta guía presenta Defold como una alternativa para desarrolladores de juegos en Flash. Cubre algunos de los conceptos clave usados en el desarrollo de juegos en Flash y explica las herramientas y métodos correspondientes en Defold.
---

# Defold para usuarios de Flash

Esta guía presenta Defold como una alternativa para desarrolladores de juegos en Flash. Cubre algunos de los conceptos clave usados en el desarrollo de juegos en Flash y explica las herramientas y métodos correspondientes en Defold.

## Introducción

Algunas de las ventajas clave de Flash eran la accesibilidad y las pocas barreras de entrada. Los usuarios nuevos podían aprender el programa rápidamente y podían crear juegos básicos con una inversión de tiempo limitada. Defold ofrece una ventaja similar al proporcionar un conjunto de herramientas dedicadas al diseño de juegos, mientras permite que los desarrolladores avanzados creen soluciones avanzadas para requisitos más sofisticados (por ejemplo, permitiendo que los desarrolladores editen el script de render predeterminado).

Los juegos Flash se programan en ActionScript (la versión 3.0 es la más reciente), mientras que los scripts de Defold se escriben en Lua. Esta guía no hará una comparación detallada entre Lua y ActionScript 3.0. El [manual de Defold](/manuals/lua) proporciona una buena introducción a la programación en Lua en Defold y hace referencia al muy útil [Programming in Lua](https://www.lua.org/pil/) (primera edición), que está disponible gratuitamente en línea.

Un artículo de Jesse Warden proporciona una [comparación básica entre ActionScript y Lua](http://jessewarden.com/2011/01/lua-for-actionscript-developers.html), que puede servir como buen punto de partida. Ten en cuenta, sin embargo, que hay diferencias más profundas en cómo están construidos Defold y Flash que lo que se ve a nivel del lenguaje. ActionScript y Flash están orientados a objetos en el sentido clásico, con clases y herencia. Defold no tiene clases ni herencia. Incluye el concepto de *objeto de juego (Game object)*, que puede contener representación audiovisual, comportamiento y datos. Las operaciones sobre objetos de juego se realizan con *funciones* disponibles en las API de Defold. Además, Defold fomenta el uso de *mensajes* para comunicarse entre objetos. Los mensajes son una construcción de nivel más alto que las llamadas a métodos y no están pensados para usarse como tales. Estas diferencias son importantes y lleva un tiempo acostumbrarse a ellas, pero no se cubrirán en detalle en esta guía.

En su lugar, esta guía explora algunos de los conceptos clave del desarrollo de juegos en Flash y describe cuáles son los equivalentes más cercanos en Defold. Se tratan similitudes y diferencias, junto con errores comunes, para que puedas empezar con buen pie la transición de Flash a Defold.

## Movie clips y objetos de juego

Los movie clips son un componente clave del desarrollo de juegos en Flash. Son símbolos, cada uno con una línea de tiempo única. El concepto equivalente más cercano en Defold es un objeto de juego.

![game object and movieclip](images/flash/go_movieclip.png)

A diferencia de los movie clips de Flash, los objetos de juego de Defold no tienen líneas de tiempo. En su lugar, un objeto de juego consiste en varios componentes. Los componentes incluyen sprites, sonidos y scripts, entre muchos otros (para más detalles sobre los componentes disponibles, consulta la [documentación de bloques de construcción](/manuals/building-blocks) y los artículos relacionados). El objeto de juego en la captura de pantalla siguiente consiste en un sprite y un script. El componente script se usa para controlar el comportamiento y el aspecto de los objetos de juego durante todo el ciclo de vida del objeto:

![script component](images/flash/script_component.png)

Aunque los movie clips pueden contener otros movie clips, los objetos de juego no pueden *contener* objetos de juego. Sin embargo, los objetos de juego pueden convertirse en *hijos* de otros objetos de juego, creando jerarquías que se pueden mover, escalar o rotar al unísono.

## Flash: crear movie clips manualmente

En Flash, se pueden agregar instancias de movie clips a la escena manualmente arrastrándolas desde la biblioteca hasta la línea de tiempo. Esto se ilustra en la captura de pantalla siguiente, donde cada logo de Flash es una instancia del movieclip "logo":

![manual movie clips](images/flash/manual_movie_clips.png)

## Defold: crear objetos de juego manualmente

Como se mencionó antes, Defold no tiene un concepto de línea de tiempo. En su lugar, los objetos de juego se organizan en colecciones. Las colecciones son contenedores (o prefabs) que contienen objetos de juego y otras colecciones. En el nivel más básico, un juego puede consistir solo en una colección. Con más frecuencia, los juegos de Defold usan varias colecciones, ya sea agregadas manualmente a la colección bootstrap "main" o cargadas dinámicamente mediante [proxies de colección](/manuals/collection-proxy). Este concepto de cargar "niveles" o "pantallas" no tiene un equivalente directo en Flash.

En el ejemplo siguiente, la colección "main" contiene tres instancias (listadas a la derecha, en la ventana *Outline*) del objeto de juego "logo" (visible a la izquierda, en la ventana del navegador *Assets*):

![manual game objects](images/flash/manual_game_objects.png)

## Flash: referenciar movie clips creados manualmente

Referenciar movie clips creados manualmente en Flash requiere usar un nombre de instancia definido manualmente:

![flash instance name](images/flash/flash_instance_name.png)

## Defold: id de objeto de juego

En Defold, todos los objetos de juego y componentes se referencian mediante una dirección. En la mayoría de los casos basta con un nombre simple o un atajo. Por ejemplo:

- `"."` direcciona el objeto de juego actual.
- `"#"` direcciona el componente actual (el script).
- `"logo"` direcciona el objeto de juego con el id "logo".
- `"#script"` direcciona el componente con id "script" en el objeto de juego actual.
- `"logo#script"` direcciona el componente con id "script" en el objeto de juego con id "logo".

La dirección de los objetos de juego colocados manualmente se determina mediante la propiedad *Id* asignada (consulta la parte inferior derecha de la captura de pantalla). El id debe ser único para el archivo de colección actual en el que estás trabajando. El editor define automáticamente un id por ti, pero puedes cambiarlo para cada instancia de objeto de juego que crees.

![game object id](images/flash/game_object_id.png)

::: sidenote
Puedes encontrar el id de un objeto de juego ejecutando el código siguiente en su componente script: `print(go.get_id())`. Esto imprimirá el id del objeto de juego actual en la consola.
:::

El modelo de direccionamiento y el paso de mensajes son conceptos clave en el desarrollo de juegos con Defold. El [manual de direccionamiento](/manuals/addressing) y el [manual de paso de mensajes](/manuals/message-passing) los explican con mucho detalle.

## Flash: crear movie clips dinámicamente

Para crear movie clips dinámicamente en Flash, primero hay que configurar ActionScript Linkage:

![actionscript linkage](images/flash/actionscript_linkage.png)

Esto crea una clase (Logo en este caso), que luego permite instanciar nuevas instancias de esta clase. Agregar una instancia de la clase Logo al Stage podría hacerse como se muestra a continuación:

```as
var logo:Logo = new Logo();
addChild(logo);
```

## Defold: crear objetos de juego usando factories

En Defold, la generación dinámica de objetos de juego se logra mediante el uso de *factories*. Las factories son componentes que se usan para generar copias de un objeto de juego específico. En este ejemplo, se ha creado una factory con el objeto de juego "logo" como prototipo:

![logo factory](images/flash/logo_factory.png)

Es importante tener en cuenta que las factories, como todos los componentes, deben agregarse a un objeto de juego antes de poder usarse. En este ejemplo, hemos creado un objeto de juego llamado "factories" para contener nuestro componente factory:

![factory component](images/flash/factory_component.png)

La función que se debe llamar para generar una instancia del objeto de juego logo es:

```lua
local logo_id = factory.create("factories#logo_factory")
```

La URL es un parámetro requerido de `factory.create()`. Además, puedes agregar parámetros opcionales para definir posición, rotación, propiedades y escala. Para más información sobre el componente factory, consulta el [manual de factory](/manuals/factory). Vale la pena señalar que llamar a `factory.create()` devuelve el id del objeto de juego creado. Este id se puede almacenar para referencia posterior en una tabla (que es el equivalente en Lua de un array).

## Flash: stage

En Flash, estamos familiarizados con la Timeline (sección superior de la captura de pantalla siguiente) y el Stage (visible debajo de la Timeline):

![timeline and stage](images/flash/stage.png)

Como se explicó en la sección de movie clips anterior, el Stage es esencialmente el contenedor de nivel superior de un juego Flash y se crea cada vez que se exporta un proyecto. El Stage tendrá por defecto un hijo, la *`MainTimeline`*. Cada movie clip generado en el proyecto tendrá su propia línea de tiempo y puede servir como contenedor para otros símbolos (incluidos movie clips).

## Defold: colecciones

El equivalente en Defold del Stage de Flash es una colección. Cuando el motor arranca, crea un nuevo mundo de juego basado en el contenido de un archivo de colección. Por defecto, este archivo se llama "main.collection", pero puedes cambiar qué colección se carga al inicio accediendo al archivo de configuración *game.project*, que está en la raíz de cada proyecto de Defold:

![game.project](images/flash/game_project.png)

Las colecciones son contenedores que se usan en el editor para organizar objetos de juego y otras colecciones. El contenido de una colección también se puede generar mediante script en el runtime usando una [factory de colección](/manuals/collection-factory/#spawning-a-collection), que funciona igual que una factory normal de objeto de juego. Esto es útil para generar grupos de enemigos o un patrón de monedas coleccionables, por ejemplo. En la captura de pantalla siguiente, hemos colocado manualmente dos instancias de la colección "logos" dentro de la colección "main".

![collection](images/flash/collection.png)

En algunos casos, quieres cargar un mundo de juego completamente nuevo. El componente [proxy de colección](/manuals/collection-proxy/) te permite crear un nuevo mundo de juego basado en el contenido de un archivo de colección. Esto sería útil para escenarios como cargar nuevos niveles de juego, minijuegos o cinemáticas.

## Flash: línea de tiempo

La línea de tiempo de Flash se usa principalmente para animación, mediante varias técnicas frame by frame o interpolaciones de forma/movimiento. La configuración general de FPS (frames por segundo) del proyecto define el tiempo durante el cual se muestra un frame. Los usuarios avanzados pueden modificar los FPS generales del juego, o incluso los de movie clips individuales.

Las interpolaciones de forma permiten la interpolación de gráficos vectoriales entre dos estados. En general solo son útiles para formas y aplicaciones simples, como demuestra el siguiente ejemplo de interpolación de forma de un cuadrado a un triángulo:

![timeline](images/flash/timeline.png)

Las interpolaciones de movimiento permiten animar varias propiedades de un objeto, incluidas tamaño, posición y rotación. En el ejemplo siguiente, se han modificado todas las propiedades listadas.

![motion tween](images/flash/tween.png)

## Defold: animación de propiedades

Defold trabaja con imágenes de pixeles en lugar de gráficos vectoriales, por lo que no tiene un equivalente para la interpolación de forma. Sin embargo, la interpolación de movimiento tiene un equivalente potente en la [animación de propiedades](/ref/go/#go.animate). Esto se consigue mediante script, usando la función `go.animate()`. La función `go.animate()` interpola una propiedad (como color, escala, rotación o posición) desde el valor inicial hasta el valor final deseado, usando una de las muchas funciones de easing disponibles (incluidas funciones personalizadas). Mientras que Flash requería que el usuario implementara las funciones de easing más avanzadas, Defold incluye [muchas funciones de easing](/manuals/property-animation/#easing) integradas en el motor.

Mientras Flash usa keyframes de gráficos en una línea de tiempo para la animación, uno de los principales métodos de animación gráfica en Defold es la animación flipbook de secuencias de imágenes importadas. Las animaciones se organizan en un componente de objeto de juego conocido como atlas. En este caso tenemos un atlas para un personaje de juego con una secuencia de animación llamada "run". Esta consiste en una serie de archivos png:

![flipbook](images/flash/flipbook.png)

## Flash: índice de profundidad

En Flash, la lista de visualización determina qué se muestra y en qué orden. El orden de los objetos en un contenedor (como el Stage) se maneja mediante un índice. Los objetos agregados a un contenedor usando el método `addChild()` ocuparán automáticamente la posición superior del índice, comenzando en 0 e incrementándose con cada objeto adicional. En la captura de pantalla siguiente, hemos generado tres instancias del movie clip "logo":

![depth index](images/flash/depth_index.png)

Las posiciones en la lista de visualización se indican con los números junto a cada instancia de logo. Ignorando cualquier código para manejar la posición x/y de los movie clips, lo anterior podría haberse generado así:

```as
var logo1:Logo = new Logo();
var logo2:Logo = new Logo();
var logo3:Logo = new Logo();

addChild(logo1);
addChild(logo2);
addChild(logo3);
```

Que un objeto se muestre por encima o por debajo de otro se determina por sus posiciones relativas en el índice de la lista de visualización. Esto se ilustra bien intercambiando las posiciones de índice de dos objetos, por ejemplo:

```as
swapChildren(logo2,logo3);
```

El resultado se vería como abajo (con la posición de índice actualizada):

![depth index](images/flash/depth_index_2.png)

## Defold: posición z

Las posiciones de los objetos de juego en Defold se representan con vectores que consisten en tres variables: x, y y z. La posición z determina la profundidad de un objeto de juego. En el [script de render](/manuals/render) predeterminado, las posiciones z disponibles van de -1 a 1.

::: sidenote
Los objetos de juego con una posición z fuera del rango de -1 a 1 no se renderizarán y, por lo tanto, no serán visibles. Este es un error común para desarrolladores nuevos en Defold, y vale la pena tenerlo en cuenta si un objeto de juego no es visible cuando esperas que lo sea.
:::

A diferencia de Flash, donde el editor solo implica el índice de profundidad (y permite modificarlo usando comandos como *Bring Forward* y *Send Backward*), Defold te permite definir la posición z de los objetos directamente en el editor. En la captura de pantalla siguiente, puedes ver que "logo3" se muestra encima y tiene una posición z de 0.2. Los otros objetos de juego tienen posiciones z de 0.0 y 0.1.

![z-order](images/flash/z_order.png)

Ten en cuenta que la posición z de un objeto de juego anidado en una o más colecciones se decide por su propia posición z junto con la de todos sus padres. Por ejemplo, imagina que los objetos de juego logo anteriores se colocaran en una colección "logos" que a su vez se colocara en "main" (consulta la captura de pantalla siguiente). Si la colección "logos" tuviera una posición z de 0.9, las posiciones z de los objetos de juego contenidos serían 0.9, 1.0 y 1.1. Por lo tanto, "logo3" no se renderizaría, ya que su posición z es mayor que 1.

![z-order](images/flash/z_order_outline.png)

Por supuesto, la posición z de un objeto de juego se puede cambiar usando script. Supón que lo siguiente está ubicado en el componente script de un objeto de juego:

```lua
local pos = go.get_position()
pos.z  = 0.5
go.set_position(pos)
```

## Detección de colisiones `hitTestObject` y `hitTestPoint` en Flash

La detección básica de colisiones en Flash se consigue usando el método `hitTestObject()`. En este ejemplo, tenemos dos movie clips: "bullet" y "bullseye". Se ilustran en la captura de pantalla siguiente. La caja delimitadora azul es visible al seleccionar los símbolos en el editor de Flash, y son estas cajas delimitadoras las que determinan el resultado del método `hitTestObject()`.

![hit test](images/flash/hittest.png)

La detección de colisiones usando `hitTestObject()` se hace de la siguiente manera:

```as
bullet.hitTestObject(bullseye);
```

Usar las cajas delimitadoras en este caso no sería apropiado, ya que se registraría un impacto en el escenario siguiente:

![hit test bounding box](images/flash/hitboundingbox.png)

Una alternativa a `hitTestObject()` es el método `hitTestPoint()`. Este método contiene un parámetro `shapeFlag`, que permite realizar pruebas de impacto contra los pixeles reales de un objeto en lugar de contra la caja delimitadora. La detección de colisiones usando `hitTestPoint()` podría hacerse como se muestra a continuación:

```as
bullseye.hitTestPoint(bullet.x, bullet.y, true);
```

Esta línea comprobaría la posición x e y de la bala (arriba a la izquierda en este escenario) contra la forma del objetivo. Como `hitTestPoint()` comprueba un punto contra una forma, decidir qué punto (¡o puntos!) comprobar es una consideración clave.

## Defold: objetos colisionadores

Defold incluye un motor de físicas que puede detectar colisiones y permitir que un script reaccione a ellas. La detección de colisiones en Defold comienza asignando componentes de objeto colisionador a objetos de juego. En la captura de pantalla siguiente, hemos agregado un objeto colisionador al objeto de juego "bullet". El objeto colisionador se indica como la caja roja transparente (que solo es visible en el editor):

![collision object](images/flash/collision_object.png)

Defold incluye una versión modificada del motor de físicas Box2D, que puede simular colisiones realistas automáticamente. Esta guía asume el uso de objetos colisionadores cinemáticos, ya que son los que más se parecen a la detección de colisiones en Flash. Lee más sobre los objetos colisionadores dinámicos en el [manual de físicas](/manuals/physics) de Defold.

El objeto colisionador incluye las siguientes propiedades:

![collision object properties](images/flash/collision_object_properties.png)

Se ha usado una forma de caja porque era la más apropiada para el gráfico de la bala. La otra forma usada para colisiones 2D, esfera, se usará para el objetivo. Definir el tipo como Kinematic significa que la resolución de colisiones la hace tu script en lugar del motor de físicas integrado (para más información sobre los otros tipos, consulta el [manual de físicas](/manuals/physics)). Las propiedades *Group* y *Mask* determinan a qué grupo de colisión pertenece el objeto y contra qué grupo de colisión debe comprobarse, respectivamente. La configuración actual significa que una "bullet" solo puede colisionar con un "target". Imagina que la configuración se cambiara a la siguiente:

![collision group/mask](images/flash/collision_groupmask.png)

Ahora, las balas pueden colisionar con objetivos y otras balas. Como referencia, hemos configurado un objeto colisionador para el objetivo que se ve así:

![collision object bullet](images/flash/collision_object_bullet.png)

Observa cómo la propiedad *Group* se define como "target" y *Mask* se define como "bullet".

En Flash, la detección de colisiones ocurre solo cuando el script la llama explícitamente. En Defold, la detección de colisiones ocurre continuamente en segundo plano mientras un objeto colisionador permanezca habilitado. Cuando ocurre una colisión, se envían mensajes a todos los componentes de un objeto de juego (de forma más relevante, a los componentes script). Estos son los mensajes [`collision_response` y `contact_point_response`](/manuals/physics-messages), que contienen toda la información necesaria para resolver la colisión como se desee.

La ventaja de la detección de colisiones de Defold es que es más avanzada que la de Flash, con la capacidad de detectar colisiones entre formas relativamente complejas con muy poco esfuerzo de configuración. La detección de colisiones es automática, lo que significa que no es necesario recorrer los distintos objetos de los diferentes grupos de colisión ni realizar pruebas de impacto explícitamente. La principal desventaja es que no hay equivalente al `shapeFlag` de Flash. Sin embargo, para la mayoría de usos bastan combinaciones de las formas básicas de caja y esfera. Para escenarios más complejos, [son posibles](//forum.defold.com/t/does-defold-support-only-three-shapes-for-collision-solved/1985) las formas personalizadas.

## Flash: manejo de eventos

Los objetos de evento y sus listeners asociados se usan para detectar diversos eventos (por ejemplo, clicks del mouse, pulsaciones de botones, clips que se cargan) y ejecutar acciones en respuesta. Hay una variedad de eventos con los que trabajar.

## Defold: funciones callback y mensajería

El equivalente en Defold del sistema de manejo de eventos de Flash consiste en varios aspectos. En primer lugar, cada componente script viene con un conjunto de funciones callback que detectan eventos específicos. Son:

init
:   Se llama cuando el componente script se inicializa. Equivale a la función constructora en Flash.

final
:   Se llama cuando el componente script se destruye (por ejemplo, cuando se elimina un objeto de juego generado).

update
:   Se llama en cada frame. Equivale a `enterFrame` en Flash.

on_message
:   Se llama cuando el componente script recibe un mensaje.

on_input
:   Se llama cuando la entrada del usuario (por ejemplo, mouse o teclado) se envía a un objeto de juego con [foco de input](/ref/go/#acquire_input_focus), lo que significa que el objeto recibe todo el input y puede reaccionar a él.

on_reload
:   Se llama cuando se recarga el componente script.

Todas las funciones callback listadas arriba son opcionales y se pueden eliminar si no se usan. Para detalles sobre cómo configurar el input, consulta el [manual de input](/manuals/input). Un error común ocurre al trabajar con proxies de colección; consulta [esta sección](/manuals/input/#input-dispatch-and-on_input) del manual de input para más información.

Como se explicó en la sección de detección de colisiones, los eventos de colisión se gestionan mediante el envío de mensajes a los objetos de juego involucrados. Sus componentes script respectivos reciben el mensaje en sus funciones callback `on_message`.

## Flash: símbolos de botón

Flash usa un tipo de símbolo dedicado para botones. Los botones usan métodos específicos de manejo de eventos (por ejemplo, `click` y `buttonDown`) para ejecutar acciones cuando se detecta interacción del usuario. La forma gráfica de un botón en la sección "Hit" del símbolo de botón determina el área de impacto del botón.

![button](images/flash/button.png)

## Defold: escenas GUI y scripts

Defold no incluye un componente de botón nativo, ni los clicks pueden detectarse fácilmente contra la forma de un objeto de juego dado del modo en que se manejan los botones en Flash. El uso de un componente [GUI](/manuals/gui) es la solución más común, en parte porque las posiciones de los componentes GUI de Defold no se ven afectadas por la cámara del juego (si se usa). La API de GUI también contiene funciones para detectar si entradas de usuario como clicks y eventos táctiles están dentro de los límites de un elemento GUI.

## Depuración

En Flash, el comando `trace()` es tu aliado al depurar. El equivalente de Defold es `print()`, y se usa de la misma forma que `trace()`:

```lua
print("Hello world!"")
```

Puedes imprimir varias variables usando una función `print()`:

```lua
print(score, health, ammo)
```

También hay una función `pprint()` (pretty print), que es útil al trabajar con tablas. Esta función imprime el contenido de las tablas, incluidas tablas anidadas. Considera el script siguiente:

```lua
factions = {"red", "green", "blue"}
world = {name = "Terra", teams = factions}
pprint(world)
```

Esto contiene una tabla (`factions`) anidada en una tabla (`world`). Usar el comando `print()` normal generaría el id único de la tabla, pero no el contenido real:

```
DEBUG:SCRIPT: table: 0x7ff95de63ce0
```

Usar la función `pprint()` como se ilustró arriba produce resultados más significativos:

```
DEBUG:SCRIPT:
{
  name = Terra,
  teams = {
    1 = red,
    2 = green,
    3 = blue,
  }
}
```

Si tu juego usa detección de colisiones, puedes activar o desactivar la depuración de físicas enviando el mensaje siguiente:

```lua
msg.post("@system:", "toggle_physics_debug")
```

La depuración de físicas también se puede habilitar en la configuración del proyecto. Antes de activar la depuración de físicas, nuestro proyecto se vería así:

![no debug](images/flash/no_debug.png)

Activar la depuración de físicas muestra los objetos colisionadores agregados a nuestros objetos de juego:

![with debug](images/flash/with_debug.png)

Cuando ocurren colisiones, los objetos colisionadores relevantes se iluminan. Además, se muestra el vector de colisión:

![collision](images/flash/collision.png)

Por último, consulta la [documentación del profiler](/ref/profiler/) para información sobre cómo monitorear el uso de CPU y memoria. Para más información sobre técnicas avanzadas de depuración, consulta la [sección de depuración](/manuals/debugging) en el manual de Defold.

## Dónde ir desde aquí

- [Ejemplos de Defold](/examples)
- [Tutoriales](/tutorials)
- [Manuales](/manuals)
- [Referencia](/ref/go)
- [FAQ](/faq/faq)

Si tienes preguntas o te atascas, los [foros de Defold](//forum.defold.com) son un gran lugar para pedir ayuda.
