---
title: Direccionamiento en Defold
brief: Este manual explica cómo Defold ha resuelto el problema del direccionamiento.
---

# Direccionamiento

El código que controla un juego mientras se ejecuta debería poder alcanzar a todos los objetos yu componentes para poder moverlos, escalarlos, animarlos, eliminarlos y manipularlos lo que el jugador ve y oye. El mecanismo de direccionamiento de Defold hace esto posible.

## Identificadores

Defold utiliza direcciones (o URLs, pero vamos a ignorarlo por ahora) para referenciar a un objecto de juego ( gameobject) and componentes. Estas direcciones consisten en identificadores. Lo siguiente son ejemplos de cómo Defold utiliza estas direcciones. A través de este manual vamos a examinar en detalle how trabajan:

```lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```
Vamos a comenar con un ejemplo sencillo. Supongamos que tienes un game object solamente con un componente sprite. También tienes un componente script para controlar el game object. La configuración en el editor podría ser algo como esto: 

![bean in editor](images/addressing/bean_editor.png)

Ahora quieres deshabilitar el sprite cuando comience el juego, para que puedas hacerlo aparecer después. Esto se hace fácil colocando el siguinete código en "controller.script":

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. No te preocupes si estás perplejo por el uso de '#'. Llegaremos a eso pronto.

Esto funcionará como se espera. Cuando el juego comience, el componente script *direccionará* un *mensaje* de "disable" (inabilitado) al componente sprite que se encuentra identificado por "body". El efecto de este mensaje especial del motor es que el componente sprite ocultará las gráficas del sprite. Esquemáticamente, la configuración es algo cómo esto:

![bean](images/addressing/bean.png)

Los identificadores en la configuración son arbitrarios. Aquí hemos escogido darle el identificador de "bean" al game object, su componente sprite ha sido nombrado "body", y el componente script que controlar el personaje se llama "controller".

::: sidenote
Si le colcas un nombre, el editor lo hará. No importa si crear un nuevo objecto  de juego o un componente en el editor, un *Id* único se colocará automáticamente.

- Un objecto de juego automáticamente obtiene un id llamando "go" con un enumerador ("go2", "go3", etc).
- Los componente obtienen su id correspondiente según el tipo de componente ("sprite", "sprite2", etc).

Puedes utilizar estos nombres asignados automáticamente si quieres, pero te recomendamos que los cambies por nombres más descriptivos.
:::

Ahora, vamos a agregar otro componente sprite y dar al frijol un escudo:

![bean](images/addressing/bean_shield_editor.png)

El nuevo componente debería ser identificado de forma única con el objecto de juego. Si le dieras el nombre de "body" el código script será ambiguo sobre cuál de sprite debería enviar el mensaje "disable". Por lo tanto nosotros escogemos un único (y descriptivo) identificador "shield". Ahora podemos habilitar y deshabilitar los sprites "body" y "shield" a voluntad.

![bean](images/addressing/bean_shield.png)

::: sidenote
Si intentas utilizar un identificador más de una vez, el editor mostrará una señal de error así que esto nunca es un problema en la práctica:

![bean](images/addressing/name_collision.png)
:::

Ahora, vamos a ver que pasa si agregamos más objectos de juego. Supongamos que quieres agrupar dos "beans" en un pequeño equipo. Decides llamar a uno de ellos como "bean" y el otro "buddy". Además, cuando "bean" esta quieto por un tiempo, debería decirle a "buddy" que comience a bailar. Esto se hace al enviar un mensaje personalizado llamado "dance" desde el script "controller" en "bean" al script "controller" de "buddy":

![bean](images/addressing/bean_buddy.png)

::: sidenote
Existen dos componentes separados que se llaman "controller", uno en cada uno de los objetos de juego pero esto es perfectamente legal porque cada objecto de juego crea su propio contexto de nombre.
:::

Debido a que el destinatario del mensaje esta por fuera del object que está enviando el mensaje ("bean"), el código necesita especificar cual "controller" debería recibir el mensaje. Debe ser especificado ambos, tanto el id del objeto de juego cómo el id del componente. La dirección completa del componente sería `"buddy#controller"` y está dirección consiste en dos partes separadas.

- Primero viene el identificador del objecto que recibirá el mensaje ("buddy"),
- luego le sigue el caracter separador de objetos de juego y componente ("#"),
- y finalmente se escribe el identificar del componente objetivo ("controller").

Volviendo al ejemplo anterior con un solo objecto de juego vimos que que si no colocamos el identificar del objeto de juego como parte de la dirección, el código puede direccionar componentes dentro del *objecto de juego actual*

Por ejemplo, `"#body"` denota la dirección al componente "body" en el mismo objecto de juego. Esto puede ser muy útil porque el código trabajará en *cualquier* objeto de juego, mientras haya un componente "body" presente en él.

## Collections

Las colecciones hacen posible la creaci´no de grupos, o jerarquías, de objectos del juego y re utilizarlos en una forma controlada. Puedes utilizas colecciones de archivos como plantillas (o "prototipos" o "prefabricados") ("prototypes" or "prefab") en el editor cuando llenes tu juego de contenido

Supongamos que quieres crear un gran número de equipos bean/buddy. Una buena manera de hacer esto es crear una plantilla en una nuevo *archivo de colección* (nombrarlo "colección.equipo"). Construir los objectos del juego en un archivo de colección y guárdalo. Luego coloca una instancia de ese archivo de colección en la colección principal y asigna un identificador a la instancia (nómbralo "team_1"):

![bean](images/addressing/team_editor.png)

Con esta estructura, el objeto del juego "bean" puede seguir refiriendo al componente "controller" en "buddy" por la dirección `"buddy#controller"`.

![bean](images/addressing/collection_team.png)

Y si agregar una segunda instancia de "team.collecion" (nómbralo "team_2"), el códio que se ejecuta dentro de los componentes script de "team_2" funcinoarán muy bien. El objecto del juego "bean" de la colección "team_2" todavía puede direccionar al componente "controller" en "buddy" por la dirección `"buddy#controller"`.

![bean](images/addressing/teams_editor.png)

## Direcciones relativas (Relative addressing)

La dirección `"buddy#controller"` funciona para el objecto de juego en las dos colecciones por que es un dirección *relativa*. Cada colección de "team_1" y "team_2" crea un nuevo contexto de nombres, or también "namespace". Defold evita coleisiones de nombres tomando el contexto de los nombres de las colecciones creadas en condieración para el direccionamiento:

![relative id](images/addressing/relative_same.png)

- Con el contexto de nombre "team_1", los objetos del juego "bean" y "buddy" son identificados de forma única.
- De igual manera, con el contexto de nombre de "team_2", los objetos del juego "bean" y "buddy" son también identificados de forma única.

Direccionamiento relativo trabjar automáticamente anteponiendo el nombre del contexto actual cuando resuelve las direcciones objetivo. Esto es inmensamente útil y poderoso porque puedes crear grupos de objectos del juego con código y reusarlo efectivamente a través del juego.

### Shorthands

Defold provee de dos abreviaturas que puede sutilizar para enviar mensajes sin especificar la URL completa:

:[Shorthands](../shared/url-shorthands.md)

## Rutas de los objetos del juego

Para entender correctamente el mecanismo de nombramiento, vamos a mirar lo que sucede cuando compilamos y ejecutamos el proyecto:

1. El editor lee la colección principal ("main.collecion") y todo lo que contiene (objetos del juego y otras colecciones).
2. Por cada objecto estático del juego, el compilador crea un identificador. Esto es compilado como "rutas" comenzando por la raíz, siguiendo la jerarquía de colecciones hacia abajo hasta el objecto. A caracter '/' es agregado por cada nivel.

Para nuestro ejemplo de arriba, el juego se ejecutará con los siguientes 4 objectos del juego: 

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
Los identificadores son almacenados como valores hash. El entorno de ejecución también almacena el estado del hash por cada identificación de colección los cuales son usados para continuar la cadena relativa hash en un id absoluto.
:::

En el tiempo de ejecución, los grupos de colecciones no existe. No hay forma de saber qué colección pertenece un objecto de juego antes de la complicación. Tampoco es posible manipular todos los objetos en una colección al mismo tiempo. Si necesitas hacer estas operaciones, puedes fácilmente hacer el seguimiento de tu código. Cada identificador de objeto es estático, es garantizado que se quede fijo a través de tiempo de vida del objeto. Esto significa que puedes de forma segura almacenar la identidad de un objecto y usarlo después.

## Direcciones absolutas (absolute addressing)

Es posible utilizar el identificadores completos descritos arriba. En la mayoría de los casos las direcciones relativas son preferidas debido a que te permite el reuso, pero hay casos donde el direccionamiento absoluto se vuelve necesario.

Por ejemplo, supongamos que quieres un administrador de IA que hace el seguimiento del estado de cada uno de los objetos frijoles. Los frijoles deberían reportar sus estados activos al administrador, y así el administrador podrá crear decisiones estratégicas and dar órdenes a los frijoles basándose en sus estados. Aquí tendría mucho sentido crear un solo objecto del juego que haga de administrador con un componente script y colocarlo al mismo nivel que las colecciones de equipo en la colección principal.

![manager object](images/addressing/manager_editor.png)

Cada frijol es responsable de envidar mensajes con su estado al administrador: "contract" si mira a un enemigo o "ouch!" si es golpeado y obtiene un daño. Para que esto funcione, los scripts controladores del frijol utilizan direccionamiento absoluto para enviar mensajes al componente "controller" en el administrador "manager".

Cualquier dirección que comience con un '/' será resuvleta como la raíz del mundo del juego. Esto corresponde a la raíz de *bootstrap collection* que es cargada al comienzo del juego.

La ruta absoluta del script del administrador es `"/manager#controller"` y esta ruta absoluta será direccionada al componente correcto sin importar desde donde se utilice.

![teams and manager](images/addressing/teams_manager.png)

![absolute addressing](images/addressing/absolute.png)

## Indentificadores hashes (Hashed identifiers)

El motoro almacena todos los identificadores en sus valores hash. Todas las funciones que tienen como argumento un componente o un objecto del juego aceptan una cadena, hash o una URL del objeto. Hemos visto cómo usar estas cadenas para el direccionamiento anteriormente.

Cuando obtienes el identificador de un objecto del juego, el motor siempre regresará el identificador de la ruta absoluta que está hasheado:

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

Puedes utilizar este identificador como un id de cadena, o uno propio. Mira que ese id hashed corresponde a la ruta del objeto, p.e. una ruta absoluta:

::: sidenote
La razón de que las direcciones relativas deben ser entregadas como cadenas es debido a que el motor compuará un nuevo id hash basado en el estado del hash del contexto de nombre actual (colección) con la cadena dada agregada al hash.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- This will not work! Relative addresses must be given as strings.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URLs

Para completar, vamos a ver el formato completo de las direcciones de Defold: la URL.

Una URL es un objecto, usualmente escrito como cadenas especialmente formateadas. Una URL genérica consiste de tres partes:

`[socket:][path][#fragment]`

socket
: Identifica el mundo de juego objetivo. Esto es importante cuando trabjas con [Collection Proxies](/manuals/collection-proxy) y es utilizado para identificar _colección cargada dinámicamente_.

path (ruta)
: Esta parte de la URL contiene el id completo del objeto de juego objetivo.

fragment (fragmento)
: La identidad del componente objetivo con su objecto de juego especificado.

Cómo se puede ver arriba, puedes no escribir algunos, o la mayoría d esta información una gran cantidad de casos. Podrías casi nunca necesitas especificar un socket, y usualmente, pero no siempre, tener que especificar la ruta. En esos casos cuando necesites direcciones cosas en otro mundo de juego necesitas especificar el socket como parte de la URL. Por ejemplo, la cadena URL completa para el script "controller" en el "manager" (administrador) del ejemplo anterior sería:

`"main:/manager#controller"`

y el controlador (controller) de "buddy" en team_2 es:

`"main:/team_2/buddy#controller"`

Podemos enviar mensajes a ellos:

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## Construyendo objectos URL

Objectos URL pueden ser construidos programáticamente en código Lua:

```lua
-- Construct URL object from a string:
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (internal numeric value)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- Construct URL from parameters:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- Build from empty URL object:
local my_url = msg.url()
my_url.socket = "main" -- specify by valid name
my_url.path = hash("/manager") -- specify as string or hash
my_url.fragment = "controller" -- specify as string or hash

-- Post to target specified by URL
msg.post(my_url, "hello_manager!")
```
