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

## Absolute addressing

It is possible to use the full identifiers described above when addressing. In most cases relative addressing is preferred since it allows for content reuse, but there are cases where absolutely addressing becomes necessary.

For example, suppose that you want an AI manager that tracks the state of each bean object. You want beans to report to their active status to the manager, and the manager makes tactical decisions and gives orders to the beans based on their status. It would make perfect sense in this case to create a single manager game object with a script component and place that alongside the team collections in the bootstrap collection.

![manager object](images/addressing/manager_editor.png)

Each bean is then responsible for sending status messages to the manager: "contact" if it spots an enemy or "ouch!" if it is hit and takes damage. For this to work, the bean controller scrips use absolute addressing to send messages to the component "controller" in "manager".

Any address that starts with a '/' will be resolved from the root of the game world. This corresponds to the root of the *bootstrap collection* that is loaded on game start.

The absolute address of the manager script is `"/manager#controller"` and this absolute address will resolve to the right component no matter where it is used.

![teams and manager](images/addressing/teams_manager.png)

![absolute addressing](images/addressing/absolute.png)

## Hashed identifiers

The engine stores all identifiers as hashed values. All functions that take as argument a component or a game object accepts a string, hash or an URL object. We have seen how to use strings for addressing above.

When you get the identifier of a game object, the engine will always return an absolute path identifier that is hashed:

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

You can use such an identifier in place of a string id, or construct one yourself. Note though that a hashed id corresponds to the path to the object, i.e. an absolute address:

::: sidenote
The reason relative addresses must be given as strings is because the engine will compute a new hash id based on the hash state of the current naming context (collection) with the given string added to the hash.
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

To complete the picture, let's look at the full format of Defold addresses: the URL.

An URL is an object, usually written as specially formatted strings. A generic URL consists of three parts:

`[socket:][path][#fragment]`

socket
: Identifies the game world of the target. This is important when working with [Collection Proxies](/manuals/collection-proxy) and is then used to identify the _dynamically loaded collection_.

path
: This part of the URL contains the full id of the target game object.

fragment
: The identity of the target component within the specified game object.

As we have seen above, you can leave out some, or most of this information in the majority of cases. You almost never need to specify the socket, and you often, but not always, have to specify the path. In those cases when you do need to address things in another game world then you need to specify the socket part of the URL. For instance, the full URL string for the "controller" script in the "manager" game object above is:

`"main:/manager#controller"`

and the buddy controller in team_2 is:

`"main:/team_2/buddy#controller"`

We can send messages to them:

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## Constructing URL objects

URL objects can also be constructed programmatically in Lua code:

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
