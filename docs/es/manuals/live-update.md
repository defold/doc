---
title: Contenido de Live update en Defold
brief: La funcionalidad Live update proporciona un mecanismo que permite al runtime obtener recursos y almacenarlos en el bundle de la aplicación cuando se dejaron intencionalmente fuera del bundle en el momento de la build. Este manual explica cómo funciona.
---

# Live update

Al crear el bundle de un juego, Defold empaqueta todos los recursos del juego en el paquete resultante específico de la plataforma. En la mayoría de los casos esto es lo preferible, ya que el motor en ejecución tiene acceso instantáneo a todos los recursos y puede cargarlos rápidamente desde el almacenamiento. Sin embargo, hay casos en los que quizá quieras posponer la carga de recursos para una etapa posterior. Por ejemplo:

- Tu juego incluye una serie de episodios y quieres incluir solo el primero para que los jugadores lo prueben antes de decidir si quieren continuar con el resto del juego.
- Tu juego está dirigido a HTML5. En el navegador, cargar una aplicación desde el almacenamiento significa que todo el paquete de la aplicación debe descargarse antes del arranque. En una plataforma así, quizá quieras enviar un paquete inicial mínimo y poner la app en marcha rápidamente antes de descargar el resto de los recursos del juego.
- Tu juego contiene recursos muy grandes (imágenes, videos, etc.) cuya descarga quieres posponer hasta que estén a punto de mostrarse en el juego. Esto sirve para mantener bajo el tamaño de instalación.

La funcionalidad Live update amplía el concepto del proxy de colección con un mecanismo que permite al runtime obtener recursos y almacenarlos en el bundle de la aplicación cuando se dejaron intencionalmente fuera del bundle en el momento de la build.

Te permite dividir tu contenido en varios archivos:

* _Archivo base_
* Archivos comunes de niveles
* Pack de niveles 1
* Pack de niveles 2
* ...

## Preparar contenido para Live update

Supongamos que estamos creando un juego que contiene recursos de imagen grandes y de alta resolución. El juego mantiene estas imágenes en colecciones con un objeto de juego y un sprite con la imagen:

![Colección Mona Lisa](images/live-update/mona-lisa.png)

Para que el motor cargue dinámicamente una colección de este tipo, simplemente podemos agregar un componente proxy de colección y apuntarlo a *`monalisa.collection`*. Ahora el juego puede elegir cuándo cargar el contenido de la colección desde el almacenamiento a la memoria enviando un mensaje `load` al proxy de colección. Sin embargo, queremos ir más allá y controlar nosotros mismos la carga de los recursos contenidos en la colección.

Esto se hace simplemente marcando la casilla *Exclude* en las propiedades del proxy de colección, lo que indica a Defold que deje fuera cualquier contenido de *`monalisa.collection`* al crear un bundle de aplicación.

::: important
Cualquier recurso referenciado por el paquete base del juego no se excluirá.
:::

![Proxy de colección excluido](images/live-update/proxy-excluded.png)

## Configuración de Live update

Cuando Defold crea un bundle de aplicación, necesita almacenar en algún lugar los recursos excluidos. La configuración del proyecto para Live update controla la ubicación de esos recursos. La configuración se encuentra en <kbd>Project ▸ Live update Settings...</kbd>. Esto creará un archivo de configuración si no existe ninguno. En *game.project*, selecciona qué archivo de configuración de live-update usar al crear el bundle. Esto permite usar distintas configuraciones de live-update para distintos entornos, por ejemplo live, QA, development, etc.

![Configuración de Live update](images/live-update/05-liveupdate-settings-zip.png)

Actualmente hay tres formas en que Defold puede almacenar los recursos. Elige el método en el desplegable *Mode* de la ventana de configuración:

`Zip`
: Esta opción indica a Defold que cree un archivo Zip con cualquier recurso excluido. El archivo se guarda en la ubicación especificada en *Export path* y puede montarse durante la ejecución con una URI `zip:` y `liveupdate.add_mount()`.

`Folder`
: Esta opción indica a Defold que cree una carpeta con todos los recursos excluidos. Resulta útil para posprocesar los archivos antes de subirlos o empaquetarlos. Una carpeta de archivos compilados individuales, organizados en las rutas de recursos esperadas, puede montarse durante la ejecución con una URI `file:`.

`Amazon`
: Esta opción indica a Defold que suba automáticamente los recursos excluidos a un bucket S3 de Amazon Web Service (AWS). Completa el nombre de tu *Credential profile* de AWS, selecciona el *Bucket* apropiado e indica un nombre de *Prefix*. Puedes leer más sobre cómo configurar una cuenta de AWS en esta [guía de AWS](/manuals/live-update-aws)

## Crear bundles con Live update

::: important
Crear y ejecutar desde el editor (<kbd>Project ▸ Build</kbd>) no es compatible con Live Update. Para probar Live Update necesitas crear el bundle del proyecto.
:::

Crear un bundle con Live update es sencillo. Selecciona <kbd>Project ▸ Bundle ▸ ...</kbd> y luego la plataforma para la que quieres crear un bundle de aplicación. Esto abre el diálogo de creación de bundle:

![Aplicación Live de bundle](images/live-update/bundle-app.png)

Al crear el bundle, cualquier recurso excluido se dejará fuera del bundle de la aplicación. Al marcar la casilla *Publish Live update content*, indicas a Defold que suba los recursos excluidos a Amazon o que cree un archivo Zip, según cómo hayas configurado Live update (ver arriba). El contenido de Live Update publicado aún incluye `liveupdate.game.dmanifest`, que contiene la lista completa de recursos necesaria para la entrega remota.

Al publicar contenido de Live Update, Defold elimina automáticamente las entradas exclusivas de Live Update del `game.dmanifest` incluido en el bundle, mientras que el `liveupdate.game.dmanifest` publicado conserva la lista completa de recursos. Esto reduce el tamaño del bundle y el uso de memoria en runtime. La configuración anterior `liveupdate.exclude_entries_from_main_manifest` se ha eliminado; cualquier entrada restante en el proyecto se ignora.

En el flujo de trabajo basado en archivos comprimidos, `collectionproxy.get_resources()` devuelve `{}` hasta que se haya montado el archivo correspondiente. Después de montarlo, devuelve los hashes de recursos de ese proxy.

Haz click en *Package* y selecciona una ubicación para el bundle de la aplicación. Ahora puedes iniciar la aplicación y comprobar que todo funciona como se espera.

## Los archivos .zip

Un archivo .zip de live update contiene archivos que se excluyeron del paquete base del juego.

Aunque nuestro pipeline actual solo permite crear un único archivo .zip, en realidad es posible dividir ese archivo zip en archivos .zip más pequeños. Esto permite descargas más pequeñas para un juego: packs de niveles, contenido de temporada, etc. Cada archivo .zip también contiene un archivo de manifiesto que describe los metadatos de cada recurso contenido dentro del archivo .zip.

## Dividir archivos .zip

A menudo es deseable dividir el contenido excluido en varios archivos más pequeños para tener un control más granular sobre el uso de recursos. Un ejemplo es dividir un juego basado en niveles en varios packs de niveles. Otro es colocar distintas decoraciones de interfaz con temática de festividades en archivos separados y cargar y montar solo el tema activo actualmente en el calendario.

El gráfico de recursos se almacena en `build/default/game.graph.json` y se genera automáticamente cada vez que se crea el bundle del proyecto. El archivo generado contiene una lista de todos los recursos del proyecto y las dependencias de cada recurso. Entrada de ejemplo:

```json
{
  "path" : "/game/player.goc",
  "hexDigest" : "caa342ec99794de45b63735b203e83ba60d7e5a1",
  "children" : [ "/game/ship.spritec", "/game/player.scriptc" ]
}
```

Cada entrada tiene un `path` que representa la ruta única del recurso dentro del proyecto. El `hexDigest` representa la huella criptográfica del recurso y será el nombre de archivo usado en el archivo .zip de liveupdate. Finalmente, el campo `children` es una lista de otras dependencias de las que depende este recurso. En el ejemplo anterior, `/game/player.goc` tiene una dependencia hacia un sprite y un componente script.

Puedes analizar el archivo `game.graph.json` y usar esta información para identificar grupos de entradas en el gráfico de recursos y almacenar sus recursos correspondientes en archivos separados junto con el archivo de manifiesto original (el archivo de manifiesto se recortará en runtime para que contenga solo los archivos del archivo).

## Live Update en Android

Es posible usar Play Asset Delivery para descargar y montar contenido de Live Update. Aprende más [en el manual oficial](https://defold.com/extension-pad/).

## Verificación de contenido

Una de las funcionalidades principales del sistema de live update es que ahora puedes usar muchos archivos de contenido, potencialmente de muchas versiones distintas de Defold.

El comportamiento por defecto de `liveupdate.add_mount()` es agregar una comprobación de versión del motor al adjuntar un montaje.
Esto significa que tanto el archivo base del juego como los archivos de live update deben crearse al mismo tiempo con la misma versión del motor, usando la opción de bundle. Esto invalidará cualquier archivo descargado previamente por el cliente, obligándolo a volver a descargar el contenido.

Este comportamiento puede desactivarse con un flag de opciones.
Cuando está desactivado, la responsabilidad de verificar el contenido recae completamente en el desarrollador, para garantizar que cada archivo de live update funcione con el motor en ejecución.

Recomendamos almacenar metadatos para cada montaje, de modo que la aplicación pueda decidir si el paquete debe permanecer montado. Valídalos después de agregar el montaje, también cuando la aplicación vuelva a agregar sus montajes durante el arranque.
Una forma de hacerlo es agregar un archivo `metadata.json` al Zip después de crear el bundle y recuperarlo con `sys.load_resource("/metadata.json")` tras montar el paquete. _Usa una ruta de recurso única para los datos de cada montaje o se devolverá el archivo del montaje con mayor prioridad._

Si no lo haces, puedes terminar en una situación en la que el contenido no sea compatible con el motor en absoluto, lo que obligará a cerrarlo.

## Montajes

El sistema de live update puede usar varios archivos de contenido al mismo tiempo.
Cada archivo se "monta" en el sistema de recursos del motor, con un nombre y una prioridad.

Si dos archivos tienen el mismo archivo `sprite.texturec`, el motor cargará el archivo desde el montaje con la prioridad más alta.

El motor no conserva una referencia a ningún recurso de un montaje. Una vez que un recurso se carga en memoria, el archivo puede desmontarse. El recurso permanecerá en memoria hasta que se descargue.

Los montajes solo están activos durante la sesión actual del motor. La aplicación debe volver a llamar a `liveupdate.add_mount()` para cada paquete que necesite después de reiniciar. Guarda la ubicación, el nombre y la prioridad del paquete en datos persistentes administrados por la aplicación si deben conservarse entre sesiones.

::: sidenote
Montar un archivo Zip o una carpeta no los copia ni los mueve. El contenido debe permanecer en la ubicación indicada mientras se use el montaje.
:::

## Scripting con Live Update

Para usar realmente el contenido de live update, necesitas descargar y montar los datos en tu juego.
Lee más sobre cómo [hacer scripting con live update aquí](/manuals/live-update-scripting).

## Consideraciones de desarrollo

Depuración
: Al ejecutar una versión con bundle de tu juego, no tienes acceso directo a una consola. Esto causa problemas para depurar. Sin embargo, puedes ejecutar la aplicación desde la línea de comando o haciendo doble click directamente en el ejecutable del bundle:

  ![Ejecutar una aplicación de bundle](images/live-update/run-bundle.png)

  Ahora el juego se inicia con una ventana de shell que mostrará cualquier sentencia `print()`:

  ![Salida de consola](images/live-update/run-bundle-console.png)

Forzar la descarga de recursos de nuevo
: El desarrollador puede descargar el contenido en cualquier archivo/carpeta que quiera, pero a menudo se ubica bajo la ruta de la aplicación. La ubicación de la carpeta de soporte depende del sistema operativo y puede encontrarse con `print(sys.get_save_file("", ""))`. Para forzar una descarga, elimina el paquete descargado y la entrada correspondiente del estado administrado por la aplicación. No existe una lista de montajes administrada por el motor; los montajes no persisten tras reiniciar.

  ![Almacenamiento local](images/live-update/local-storage.png)
