---
title: Gestión de recursos de Defold
brief: Este manual explica cómo Defold gestiona automáticamente los recursos y cómo puedes gestionar manualmente la carga de recursos para respetar las restricciones de uso de memoria y tamaño de bundle.
---

# Gestión de recursos

Si haces un juego muy pequeño, es posible que las limitaciones de la plataforma objetivo (uso de memoria, tamaño de bundle, potencia de cómputo y consumo de batería) nunca supongan un problema. Sin embargo, al crear juegos más grandes, y especialmente en dispositivos portátiles, el consumo de memoria probablemente será una de las mayores restricciones. Un equipo con experiencia elaborará cuidadosamente presupuestos de recursos en función de las restricciones de la plataforma. Defold proporciona varias funcionalidades para ayudar a gestionar la memoria y el tamaño de bundle. Este manual ofrece una visión general de estas funcionalidades.

## El árbol estático de recursos

Cuando creas un juego en Defold, declaras estáticamente el árbol de recursos. Todas las partes del juego se enlazan en el árbol, empezando por la colección bootstrap (normalmente llamada "main.collection"). El árbol de recursos sigue todas las referencias e incluye todos los recursos asociados con esas referencias:

- Datos de objetos de juego y componentes (atlas, sonidos, etc.).
- Prototipos de componentes factory (objetos de juego y colecciones).
- Referencias de componentes proxy de colección (colecciones).
- [Recursos personalizados](/manuals/project-settings/#custom-resources) declarados en *game.project*.

![Árbol de recursos](images/resource/resource_tree.png)

::: sidenote
Defold también tiene el concepto de [recursos de bundle](/manuals/project-settings/#bundle-resources). Los recursos de bundle se incluyen con el bundle de la aplicación, pero no forman parte del árbol de recursos. Los recursos de bundle pueden ser cualquier cosa, desde archivos de soporte específicos de plataforma hasta archivos externos [cargados desde el sistema de archivos](/manuals/file-access/#how-to-access-files-bundled-with-the-application) y usados por tu juego (por ejemplo, bancos de sonido FMOD).
:::

Cuando se crea el *bundle* del juego, solo se incluirá lo que está en el árbol de recursos. Todo lo que no esté referenciado en el árbol queda fuera. No hay necesidad de seleccionar manualmente qué incluir o excluir del bundle.

Cuando el juego se *ejecuta*, el motor empieza en la raíz bootstrap del árbol y carga recursos en memoria:

- Cualquier colección referenciada y su contenido.
- Objetos de juego y datos de componentes.
- Prototipos de componentes factory (objetos de juego y colecciones).

Sin embargo, el motor no cargará automáticamente los siguientes tipos de recursos referenciados en runtime:

- Colecciones de mundos de juego referenciadas mediante proxies de colección. Los mundos de juego son relativamente grandes, por lo que deberás activar manualmente su carga y descarga mediante código. Consulta el [manual de proxy de colección](/manuals/collection-proxy) para obtener más detalles.
- Archivos agregados mediante la configuración *Custom Resources* en *game.project*. Estos archivos se cargan manualmente con la función [`sys.load_resource()`](/ref/sys/#sys.load_resource).

La forma predeterminada en que Defold crea bundles y carga recursos puede modificarse para dar un control detallado sobre cómo y cuándo los recursos entran en memoria.

![Carga de recursos](images/resource/loading.png)

## Carga dinámica de recursos de factory

Los recursos referenciados por componentes factory normalmente se cargan en memoria cuando se carga el componente. Luego los recursos quedan listos para generar instancias en el juego en cuanto la factory existe en el runtime. Para cambiar el comportamiento predeterminado y posponer la carga de recursos de factory, simplemente puedes marcar una factory con la casilla *Load Dynamically*.

![Cargar dinámicamente](images/resource/load_dynamically.png)

Con esta casilla marcada, el motor seguirá incluyendo los recursos referenciados en el bundle del juego, pero no cargará automáticamente los recursos de factory. En su lugar, tienes dos opciones:

1. Llama a [`factory.create()`](/ref/factory/#factory.create) o [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create) cuando quieras generar objetos. Esto cargará los recursos de forma síncrona y luego generará nuevas instancias.
2. Llama a [`factory.load()`](/ref/factory/#factory.load) o [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load) para cargar los recursos de forma asíncrona. Cuando los recursos estén listos para generar instancias, se recibe un callback.

Consulta el [manual de Factory](/manuals/factory) y el [manual de factory de colección](/manuals/collection-factory) para obtener más detalles sobre cómo funciona.

## Descarga de recursos cargados dinámicamente

Defold mantiene contadores de referencia para todos los recursos. Si el contador de un recurso llega a cero, significa que ya nada hace referencia a él. Entonces el recurso se descarga automáticamente de la memoria. Por ejemplo, si eliminas todos los objetos generados por una factory y también eliminas el objeto que contiene el componente factory, los recursos a los que antes hacía referencia la factory se descargan de la memoria.

Para las factories marcadas con *Load Dynamically*, puedes llamar a la función [`factory.unload()`](/ref/factory/#factory.unload) o [`collectionfactory.unload()`](/ref/collectionfactory/#collectionfactory.unload). Esta llamada elimina la referencia del componente factory al recurso. Si nada más hace referencia al recurso (por ejemplo, si se eliminaron todos los objetos generados), el recurso se descargará de la memoria.

## Excluir recursos del bundle

Con proxies de colección, es posible dejar fuera del proceso de creación del bundle todos los recursos a los que hace referencia el componente. Esto es útil si necesitas mantener el tamaño del bundle al mínimo. Por ejemplo, al ejecutar juegos en la web como HTML5, el navegador descargará todo el bundle antes de ejecutar el juego.

![Excluir](images/resource/exclude.png)

Al marcar un proxy de colección como *Exclude*, el recurso referenciado quedará fuera del bundle del juego. En su lugar, puedes almacenar las colecciones excluidas en un servicio de almacenamiento en la nube seleccionado. El [manual de Live update](/manuals/live-update/) explica cómo funciona esta funcionalidad.
