---
title: Manual de factory de colección
brief: Este manual explica cómo usar componentes factory de colección para generar jerarquías de objetos de juego.
---

# Componentes factory de colección

El componente factory de colección se usa para generar grupos y jerarquías de objetos de juego almacenados en archivos de colección dentro de un juego en ejecución.

Las colecciones proporcionan un mecanismo potente para crear plantillas reutilizables, o "prefabs", en Defold. Para una visión general de las colecciones, consulta la [documentación de bloques de construcción](/manuals/building-blocks#collections). Las colecciones pueden colocarse en el editor, o pueden insertarse dinámicamente en tu juego.

Con un componente factory de colección puedes generar el contenido de un archivo de colección en un mundo de juego. Esto es análogo a generar todos los objetos de juego dentro de la colección con una factory y luego construir la jerarquía padre-hijo entre los objetos. Un caso de uso típico es generar enemigos compuestos por varios objetos de juego (enemigo + arma, por ejemplo).

## Generar una colección

Supongamos que queremos un objeto de juego de personaje y un objeto de juego de escudo separado como hijo del personaje. Construimos la jerarquía de objetos de juego en un archivo de colección y lo guardamos como "bean.collection".

::: sidenote
El componente *collection proxy* se usa para crear un mundo de juego nuevo, incluido un mundo de física separado, basado en una colección. Se accede al mundo nuevo a través de un socket nuevo. Todos los recursos contenidos en la colección se cargan a través del proxy cuando envías un mensaje al proxy para iniciar la carga. Esto los hace muy útiles para, por ejemplo, cambiar niveles en un juego. Sin embargo, los mundos de juego nuevos conllevan bastante sobrecarga, así que no los uses para la carga dinámica de elementos pequeños. Para obtener más información, consulta la [documentación de Collection proxy](/manuals/collection-proxy).
:::

![Colección que se va a generar](images/collection_factory/collection.png)

Luego añadimos un *Collection factory* a un objeto de juego que se encargará de la generación y definimos "bean.collection" como el *Prototype* del componente:

![Factory de colección](images/collection_factory/factory.png)

Generar un bean y un escudo ahora solo requiere llamar a la función `collectionfactory.create()`:

```lua
local bean_ids = collectionfactory.create("#bean_factory")
```

La función toma 5 parámetros:

`url`
: El id del componente factory de colección que debe generar el nuevo conjunto de objetos de juego.

`[position]`
: (opcional) La posición en el mundo de los objetos de juego generados. Debe ser un `vector3`. Si no especificas una posición, los objetos se generan en la posición del componente factory de colección.

`[rotation]`
: (opcional) La rotación en el mundo de los objetos de juego nuevos. Debe ser un `quat`.

`[properties]`
: (opcional) Una tabla Lua con pares `id`-`table` usados para iniciar los objetos de juego generados. Consulta abajo cómo construir esta tabla.

`[scale]`
: (opcional) La escala de los objetos de juego generados. La escala puede expresarse como un `number` (mayor que 0) que especifica una escala uniforme en todos los ejes. También puedes proporcionar un `vector3` donde cada componente especifica la escala en el eje correspondiente.

`collectionfactory.create()` devuelve los identificadores de los objetos de juego generados como una tabla. Las claves de la tabla asignan el hash del id local de cada objeto en la colección al id de runtime de cada objeto:

::: sidenote
La relación padre-hijo entre "bean" y "shield" *no* se refleja en la tabla devuelta. Esta relación solo existe en el gráfico de la escena en runtime, es decir, en cómo se transforman juntos los objetos. Cambiar el padre de un objeto nunca cambia su id.
:::

```lua
local bean_ids = collectionfactory.create("#bean_factory")
go.set_scale(0.5, bean_ids[hash("/bean")])
pprint(bean_ids)
-- DEBUG:SCRIPT:
-- {
--   hash: [/shield] = hash: [/collection0/shield], -- <1>
--   hash: [/bean] = hash: [/collection0/bean],
-- }
```
1. Se añade al id un prefijo `/collection[N]/`, donde `[N]` es un contador, para identificar cada instancia de forma única:

## Propiedades

Al generar una colección, puedes pasar parámetros de propiedades a cada objeto de juego construyendo una tabla donde las claves son ids de objetos y los valores son tablas con las propiedades de script que se deben definir.

```lua
local props = {}
props[hash("/bean")] = { shield = false }
local ids = collectionfactory.create("#bean_factory", nil, nil, props)
```

Supongamos que el objeto de juego "bean" en "bean.collection" define la propiedad "shield". El [manual de propiedades de script](/manuals/script-properties) contiene información sobre las propiedades de script.

```lua
-- bean/controller.script
go.property("shield", true)

function init(self)
    if not self.shield then
        go.delete("shield")
    end
end
```

## Carga dinámica de recursos de factory

Al marcar la casilla *Load Dynamically* en las propiedades de factory de colección, el motor pospone la carga de los recursos asociados con la factory.

![Cargar dinámicamente](images/collection_factory/load_dynamically.png)

Con la casilla desmarcada, el motor carga los recursos del prototipo cuando se carga el componente factory de colección, de modo que estén listos de inmediato para generar instancias.

Con la casilla marcada, tienes dos opciones de uso:

Carga síncrona
: Llama a [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create:url-[position]-[rotation]-[properties]-[scale]) cuando quieras generar objetos. Esto cargará los recursos de forma síncrona, lo que puede causar una pausa, y luego generará instancias nuevas.

  ```lua
  function init(self)
      -- No se cargan recursos de factory cuando se carga la
      -- colección padre de la factory de colección. Llamar create sin
      -- haber llamado load creará los recursos de forma síncrona.
      self.go_ids = collectionfactory.create("#collectionfactory")
  end

  function final(self)
      -- Elimina objetos de juego. Reducirá el contador de referencia
      -- de los recursos.
      -- En este caso los recursos se eliminan porque el componente
      -- factory de colección no mantiene ninguna referencia.
      go.delete(self.go_ids)

      -- Llamar unload no hará nada porque el factory
      -- no mantiene referencias.
      collectionfactory.unload("#factory")
  end
  ```

Carga asíncrona
: Llama a [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load:[url]-[complete_function]) para cargar explícitamente los recursos de forma asíncrona. Cuando los recursos estén listos para generar instancias, se recibe un callback.

  ```lua
  function load_complete(self, url, result)
      -- La carga terminó; los recursos están listos para generar instancias.
      self.go_ids = collectionfactory.create(url)
  end

  function init(self)
      -- No se cargan recursos de factory cuando se carga la
      -- colección padre de la factory de colección. Llamar load cargará
      -- los recursos.
      collectionfactory.load("#factory", load_complete)
  end

  function final(self)
      -- Elimina el objeto de juego. Reducirá el contador de referencia
      -- de los recursos.
      -- En este caso los recursos no se eliminan porque el componente
      -- factory de colección aún mantiene una referencia.
      go.delete(self.go_ids)

      -- Llamar unload reducirá el contador de referencia de los recursos
      -- que mantiene el componente factory, lo que causará la destrucción
      -- de los recursos.
      collectionfactory.unload("#factory")
  end
  ```


## Prototipo dinámico

Es posible cambiar qué *Prototype* puede crear una factory de colección marcando la casilla *Dynamic Prototype* en las propiedades de factory de colección.

![Prototipo dinámico](images/collection_factory/dynamic_prototype.png)

Cuando la opción *Dynamic Prototype* está marcada, el componente factory de colección puede cambiar de prototipo mediante la función `collectionfactory.set_prototype()`. Ejemplo:

```lua
collectionfactory.unload("#factory") -- descarga los recursos anteriores
collectionfactory.set_prototype("#factory", "/main/levels/level1.collectionc")
local ids = collectionfactory.create("#factory")
```

::: important
Cuando la opción *Dynamic Prototype* está definida, el recuento de componentes de colección no se puede optimizar, y la colección propietaria usará los recuentos de componentes predeterminados del archivo *game.project*.
:::
