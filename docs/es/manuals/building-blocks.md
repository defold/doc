---
title: Los bloques de construcción de Defold
brief: Este manual se adentra en los detalles de cómo los objetos, componentes y colecciones del juego funcionan.
---

#  Bloques de construcción

En el núcleo del diseño de Defold hay unos conceptos que pueden llevar tiempo dominarlos. Este manual explica en qué consisten los bloques de construcción de Defold. Después de leer este manual, sigue al [addressing manual](/manuals/addressing) y al [message passing manual](/manuals/message-passing). También hay una serie de [tutoriales](/tutorials/getting-started) disponibles desde el editor para tenerte listo rápidamente.

![Bloques de construcción](images/building_blocks/building_blocks.png){srcset="images/building_blocks/building_blocks@2x.png 2x"}

Hay tres tipos básicos de bloques de construcción que puedes usar para construir un juego de Defold:

Colección (Collection)
: Una colección es un archivo usado para estructurar tu juego. En las colecciones puedes construir jerarquías de los objetos del juego y otras colecciones. Son típicamente utilizadas para estructurar niveles, grupos de enemigos o personajes creados a partir de diversos objetos.

Objeto del juego (Game object)
: Un objeto del juego es un contenedor con un identificador (id), posición, rotación y escala. Es utilizado para contener componentes. Son típicamente utilizados para crear personajes jugadores, balas, el sistema de reglas del juego o un sistema de carga/descarga de nivel.

Componente (Component)
: Los componentes son entidades que son puestas en el objeto del juego para darles representación visual, auditiva o lógica en el videojuego. Son típicamente utilizados para crear sprites de personajes, archivos script, añadir efectos de sonido o añadir efectos de partículas.

## Colecciones

Las colecciones son estructuras de arbol que contienen objetos y otras colecciones. Una colección siempre estará guardada en archivo.

Cuando el motor Defold inicia, carga una _colección bootstrap_ especificado en el archivo de configuración *game.project*.La colección bootstrap es normalmente llamada "main.collection" pero eres libre de elegir cualquier nombre que prefieras.

Una colección puede contener objetos y otras colecciones (por referencia al archivo de subcolecciones), anidados abritrariamente profundos. Aquí hay un archivo ejemplo llamado "main.collection". Contiene un objeto (con la id "can") y una sub-colección (con la id "bean"). La sub-colección, en turno, contiene dos objetos: "bean" y "shield".

![Colección](images/building_blocks/collection.png){srcset="images/building_blocks/collection@2x.png 2x"}

Fíjate que la sub-colección con la id "bean" está guardada en su propio arcivo, llamado "/main/bean.collection" y es únicamente referenciado en "main.collection":

![Colección Bean](images/building_blocks/bean_collection.png){srcset="images/building_blocks/bean_collection@2x.png 2x"}

No puedes dirigir colecciones por sí mismas ya que no hay objetos runtime correspondiendo a las colecciones "main" y "bean". Sin embargo, a veces puedes usar la identidad de una colección como parte de una ruta(en inglés _path_) a un objeto (ver el [addressing manual](/manuals/addressing) para más detalles):

```lua
-- file: can.script
-- get position of the "bean" game object in the "bean" collection
local pos = go.get_position("bean/bean")
```

Una colección siempre es añadida a otra colección como referencia a un archivo de colección:

<kbd>Click derecho</kbd> a la colección en la *Outline* view y selecciona <kbd>Add Collection File</kbd>.

## Objetos del juego

Los objetos del juego son objetos simples con un tiempo de vida separado cada uno durante la ejecución de tu juego. Los objetos del juego tienen una posición, rotación y escala que cada uno puede ser manipulado y animado en la ejecución.

```lua
-- animate X position of "can" game object
go.animate("can", "position.x", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 1.0)
```

Los objetos del juego pueden usarse vacíos (como marcadores de posición, por instancia) pero son equipados usualmente con varios componentes, como sprites, sonidos, scripts, modelos, fábricas y más. Son creados ya sea en el editor, puestos en archivos de colección, o aparecidos dinámicamente en la ejecución a través de componentes _factory_.

Los objetos del juego son ya sea añadidos en una colección, o añadidos en una colección como referencia a un archivo de objeto de juego:

<kbd>Click derecho</kbd> a la colección en la *Outline* view y selecciona <kbd>Add Game Object</kbd> (añadir en el lugar) o <kbd>Add Game Object File</kbd> (añadir como referencia de archivo).


## Componentes

:[componentes](../shared/components.md)

Refiere al [component overview](/manuals/components/) para una lista de todos los tipos de componentes..

## Objetos añadidos en el lugar o por referencia

Cuando creas una colección, objeto de juego o componente _file_, tu creas un plano (blueprint), o prototipo. Esto solo añade un archivo al proyecto a la estructura de archivos, nada es añadido a tu juego en ejecución. Para añadir una instancia de una colección, objeto de juego o componente basado en un archivo blueprint, añades una instancia de ello en uno de tus archivos de colección.

Puedes ver cual instancia de objeto está basado de cual archivo en outline view. El archivo "main.collection" contiene tres instancias que son basadas en archivos:

1. La sub-colección "bean".
2. El componente script "bean" en el objeto de juego "bean" en la sub-colección "bean".
3. El script "can" en el objeto de juego "can".

![Instancia](images/building_blocks/instance.png){srcset="images/building_blocks/instance@2x.png 2x"}

El beneficio de crear archivos blueprint se vuelve aparente cuando tienes múltiples instancias de un objeto de juego o colección y deseas cambiar todos:

![GO instances](images/building_blocks/go_instance.png){srcset="images/building_blocks/go_instance@2x.png 2x"}

Al cambiar el archivo file, cualquier instancia que usa ese archivo será actualizado inmediatamente.

![GO instances updated](images/building_blocks/go_instance2.png){srcset="images/building_blocks/go_instance2@2x.png 2x"}

## Emparentando objetos de juego

En un archivo de colección, puedes crear jerarquías de objetos de juego de tal forma que uno o más objetos sean hijos (children) de un objeto de juego padre (parent). Simplemente <kbd>arrastrando</kbd> un objeto de juego y <kbd>soltarlo</kbd> en otro el objeto de juego arrastrado se vuelve el hijo bajo el objeto seleccionado:

![Emparentando objetos de juego](images/building_blocks/childing.png){srcset="images/building_blocks/childing@2x.png 2x"}

Las jerarquías padre-hijo de objetos es una relación dinámica que afecta cómo los objetos reaccionan a las transformaciones. Cualquier transformación (movimiento, rotación o escalado) aplicado a un objeto será aplicado al hijo del objeto en turno, ambos en el editor y en la ejecución:

![Transformación de hijos](images/building_blocks/child_transform.png){srcset="images/building_blocks/child_transform@2x.png 2x"}

De manera conversa, la traslación de un hijo será hecha en el espacio local del padre. En el editor, puedes elegir el editar un objeto de juego hijo en el espacio local o el mundo (world space) seleccionando <kbd>Edit ▸ World Space</kbd> (por defecto) o <kbd>Edit ▸ Local Space</kbd>.

También es posible alterar el padre de un objeto en la ejecución enviando un mensaje `set_parent` al objeto.

```lua
local parent = go.get_id("bean")
msg.post("child_bean", "set_parent", { parent_id = parent })
```

::: importante
Un malentendido común es que el lugar de un objeto de juego en la jerarquía de la colección cambia cuando se vuelve parte de una jerarquía padre-hijo. Sin embargo, estos son dos cosas diferentes. Las jerarquías padre-hijo alteran gráficamente la escena que permite que objetos estén visualmente unidos entre sí. La única cosa que dicta la dirección de un objeto de juego es su lugar en la colección. La dirección es estática a través de la vida del objeto.
:::
