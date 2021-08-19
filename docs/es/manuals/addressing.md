---
title: Direccionamiento en Defold
brief: Este manual explica cómo Defold ha solucionado los problemas de direccionamiento

---

# Direccionamiento

En un juego, el código que creamos tiene que ser capaz de encontrar cada objeto y componente, con tal de mover, escalar, animar, eliminar y manipular aquello que el jugador percibe del juego. En Defold, el direccionamiento es el mecanismo que se encarga de que ello sea posible.

## Identificadores

Defold usa direcciones (o URL, cómo se mostrará más adelante) para referenciar objetos y componentes del juego. Estas direcciones se basan en identificadores, tal y como se muestra en los siguientes ejemplos.

'''lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
'''

Empecemos con un ejemplo muy simple. Suponiendo que tenemos un objeto simple con un sprite y un script como componentes, se vería de la siguiente forma:

![bean in editor](images/addressing/bean_editor.png)

Ahora vamos a deshabilitar el sprite cuando el juego inicia, para hacerlo aparecer cuando lo necesitemos. Esto se hace fácilmente con el siguiente fragmento de código en "controller.script":

'''lua
function init(self)
msg.post("#body", "disable") -- <1&gt;
end
'''
1. No te preocupes si no acabas de entender el '#'. Más tarde se explicará.

Esto hará que cuando el juego inicie, el script "direccione" el sprite por el identificador "body" y use esa dirección para mandarle un "mensaje" con "disable". Este mensaje hará que el componente sprite se esconda a la vista. La siguiente imagen ayuda a comprender su funcionamiento.

![bean](images/addressing/bean.png)

El identificador es un parámetro sobre el que nosotros decidimos el valor. En este caso, se le da al objeto el identificador de "bean", al igual que al script se le nombra "controller" y al sprite "body"

::: sidenote

Si no eliges un nombre, el editor creara de forma automática un ID único.

Los objetos obtienen un id llamado "go", seguido posteriormente de números("go2", "go3", ...).
Los componentes, de igual forma, reciben un nombre relativo a su tipo ("sprite", "sprite2", ...).

Puedes dejar estos nombres sin modificar, pero sería recomendable que no lo hicieras y crearas nombres más descriptivos.

:::

Ahora, añadamos un nuevo sprite y hagamos que la judía obtenga un escudo:

![bean](images/addressing/bean_shield_editor.png)

El nuevo componente debe tener un identificador único, para no crear ambiguedad a la hora de referirnos a él desde un script. Ahora, podemos mostrar y ocultar ambos sprites a voluntad

![bean](images/addressing/bean_shield.png)

::: sidenote

Si intentas crear dos identificadores iguales, el editor mostrara un mensaje de error.

![bean](images/addressing/name_collision.png)
:::

Ahora, veamos que ocurre si añadimos más objetos. Supongamos que queremos crear un par de judías y crear un pequeño equipo. Decidimos que una se llama "bean" y la otra "buddy", además de cuando "bean" esté cierto tiempo sin moverse "buddy" empiece a bailar. Eso se puede hacer enviando un mensaje llamado baila desde "bean" hasta "buddy", tal y como se muestra a continuación.

![bean](images/addressing/bean_buddy.png)

::: sidenote

Hay dos componentes separados llamados "controller", uno en cada objeto, sin que ello tenga porque dar problemas.
:::

Dado que el direccionamiento de los mensajes se encuentra fuera del objeto("bean), el código necesita especificar donde debería "controller" recibir el mensaje. Esto se especifica tanto en con el objeto objetivo como en el identificador del componente. Esto se traduce en: '"buddy#controller"'. Las dos partes que la forman son:

- Primero el identificador del objeto al que se dirige ("buddy").
- Un separador("#").
- Y segundo el identificador del componente objetivo ("controller").

Volviendo al ejemplo anterior, con un único objeto, vemos que al omitir la parte del identificador del objeto de la dirección objetivo, el código puede direccionar componentes en el "objeto en ejecución".

Por ejemplo, '"#body"' denota la dirección del componente "body" en el objeto de juego actual. Esto es muy útil porque puede funcionar en cualquier otro objeto, siempre que haya un componente de "body" presente.

## Colecciones

Las colecciones hacen posible crear grupos (o jerarquías) de objetos y reutilizarlos de una forma controlada. Usa las colecciones como base a la hora de llenar el juego de contenido

Suponiendo que quieres crear un gran número de equipos de "bean/buddy", una buena forma de hacerlo es crear un template en un nuevo documento de tipo colección (como "team.collection"), crear el conjunto de objetos en él y darle un nuevo nombre (como "team_1"):

![bean](images/addressing/team_editor.png)

Con esta estructura, el objeto de juego "bean" todavía puede referirse al componente "controller" en "buddy" por la dirección '"buddy#controller"'

![bean](images/addressing/collection_team.png)

Si se agrega una segunda instancia de "team.collection" ("team_2"), el código que se ejecuta dentro de los componentes del script "team_2" funcionará igual de bien. La instancia del objeto de juego "bean" de la colección "team_2" aún puede dirigirse al componente "controller" en "buddy" con la dirección '"buddy#controller "'.

![bean](images/addressing/teams_editor.png)

## Direccionamiento relativo


La dirección '"buddy#controller"' funciona para los objetos en ambas colecciones, por ser una dirección "relativa":

![relative id](images/addressing/relative_same.png)

Tanto en el primer como en el segundo equipo, se considera que "bean" y "buddy" son identificadores únicos.

El direccionamiento relativo busca el nombre que se encuentra más cerca de donde nos encontramos, siendo esto tremendamente útil para crear grupos de objetos con el mismo código y reutilizarlos de manera eficiente durante todo el juego.

### Atajos

Defold proporciona dos tipos de abreviaturas que pueden ser utilizadas para enviar mensajes sin especificar una URL completa:

:[Shorthands](../shared/url-shorthands.md)

## Rutas de objetos del juego

Para comprender correctamente el mecanismo de nomenclatura, veamos qué sucede cuando compila y ejecuta el proyecto:

1. El editor lee "main.collection" y todo su contenido (objetos del juego y otras colecciones).
2. Para cada objeto estático, el compilador crea un identificador. Estos se construyen como "rutas" comenzando en la raíz y bajando en la jerarquía. Se agrega '/' en cada nivel.

Para nuestro ejemplo anterior, el juego se ejecutará con los siguientes 4 objetos de juego:

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote

Los identificadores se almacenan como valores hash. En tiempo de ejecución también se almacena el estado del hash y se usa para extraer la id absoluta desde un valor relativo.

:::

En tiempo de ejecución, la agrupación de colecciones no existe. No hay forma de averiguar a qué colección pertenecía un objeto de juego específico antes de la compilación. Tampoco es posible manipular todos los objetos de una colección a la vez. Si necesitas realizar este tipo de operaciones, puedes realizar fácilmente el seguimiento en el código. El identificador de cada objeto es estático y se garantiza que permanecerá fijo durante toda la vida útil del objeto. Esto significa que se puede almacenar de forma segura la identidad de un objeto y ser utilizado más tarde.

## Direccionamiento absoluto

Es posible utilizar los identificadores completos descritos anteriormente al direccionar. En la mayoría de los casos, se prefiere el direccionamiento relativo, ya que permite la reutilización del contenido, pero hay casos en los que el direccionamiento absoluto se vuelve necesario.

Por ejemplo, supongamos que queremos un administrador de IA que rastree el estado de cada objeto bean. Queremos que los "beans" informen sobre su estado activo y sé dé órdenes en función de este, así que tendría mucho sentido, en este caso, crear un único objeto con un componente de script que de las órdenes y colocarlo junto con las colecciones del equipo en la colección "bootstrap".

![manager object](images/addressing/manager_editor.png)

Cada "bean" será responsable de enviar un mensaje de estado a "manager": "contact" si se encuentra un enemigo o "ouch!", si recibe daño de este. Para que funcione, el script que controla a "bean" usara una dirección absoluta para enviar el mensaje a "controller" en "manager".

Cualquier dirección que comience con una '/' se resolverá desde la raíz del juego. Esto corresponde a la raíz de la "bootstrap collection" que se carga al inicio del juego.

La raiz absoluta del script de manager es '"/manager#controller"' y siempre se interpretará de la misma forma sin importar desde donde se use.

![teams and manager](images/addressing/teams_manager.png)

![absolute addressing](images/addressing/absolute.png)

## Identificadores hash

El motor almacena todos los identificadores como valores hash. Todas las funciones que toman como argumento un componente o un objeto de juego aceptan una cadena, hash o un objeto URL, tal y como hemos visto en el direccionamiento de arriba.

Cuando obtenemos el identificador de un objeto, el motor siempre devolverá un hash con el identificador de ruta absoluto:

'''lua
local my_id = go.get_id()
print(my_id) --&gt; hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --&gt; hash: [/instance42]
'''

Puedes usar un identificador de este tipo en lugar de una identificación de cadena o construir de cero. Sin embargo, ten en cuenta que una identificación hash corresponde a la ruta al objeto, es decir, una dirección absoluta:

::: sidenote
La razón por la que la dirección relativa debe ser dada como string es porque se calculara el nuevo id del hash basandose en donde está la colección actual junto con el string que queremos añadir.
:::

'''lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- This will not work! Relative addresses must be given as strings.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
'''

## URLs

Para terminar, vamos a ver el formato completo de las direcciones de Defold. Las URL.

Una URL es un objeto, normalmente escrito como una string. Una URL genérica se compone de tres partes:

'[socket:][path][#fragment]'

socket
: Identifica el contexto del objetivo. Esto es importante cuando trabajamos con [Collection Proxies](/manuals/collection-proxy) y usado para identificar la "_dynamically loaded collection_".

path
: Esta parte de la URL contiene la identificación completa del objeto de destino.

fragment
: La identidad del componente objetivo dentro del objeto especificado.

Como hemos visto anteriormente, podemos omitir parte o la mayor parte de esta información en la mayoría de los casos. Casi nunca es necesario especificar el socket y, a menudo pero no siempre, se debe de especificar la ruta. En aquellos casos en los que necesitemos interactuar con otras partes del juego, debemos especificar la parte del socket de la URL. Por ejemplo, la cadena de URL completa para el script "controlador" en el objeto de juego "administrador" anterior es:

'"main:/manager#controller"'

y el controlador de "buddy" en team_2 es:

'"main:/team_2/buddy#controller"'

Podemos enviarles mensaje así:

'''lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
'''

## Construyendo objetos URL

Los objetos URL también se pueden construir mediante Lua:

'''lua
-- Construct URL object from a string:
local my_url = msg.url("main:/manager#controller")
print(my_url) --&gt; url: [main:/manager#controller]
print(my_url.socket) --&gt; 786443 (internal numeric value)
print(my_url.path) --&gt; hash: [/manager]
print(my_url.fragment) --&gt; hash: [controller]

-- Construct URL from parameters:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --&gt; url: [main:/manager#controller]

-- Build from empty URL object:
local my_url = msg.url()
my_url.socket = "main" -- specify by valid name
my_url.path = hash("/manager") -- specify as string or hash
my_url.fragment = "controller" -- specify as string or hash

-- Post to target specified by URL
msg.post(my_url, "hello_manager!")
'''
