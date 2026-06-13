---
title: Ejemplo de mapa RPG
brief: En este proyecto de ejemplo, aprenderás un método para crear mapas RPG muy grandes.
---
# Mapa RPG - proyecto de ejemplo

En este proyecto de ejemplo, que puedes [abrir desde el editor](/manuals/project-setup/) o [descargar desde GitHub](https://github.com/defold/sample-rpgmap), mostramos un método para crear mapas RPG muy grandes en Defold. El diseño se basa en las siguientes suposiciones:

1. El mundo se presenta una pantalla a la vez. Esto permite que el juego contenga de forma natural enemigos y personajes NPC dentro de los límites de una sola pantalla. El diseñador de niveles tiene control total sobre cómo se presenta el mundo en la pantalla del jugador.
2. El personaje del jugador debería poder viajar arbitrariamente lejos sin que el juego muestre problemas de precisión de punto flotante. Normalmente estos hacen que los objetos tiemblen de forma extraña cuando se mueven lejos del origen.
3. El movimiento del jugador está restringido por obstáculos en el mapa, para que el diseñador de niveles pueda guiar al jugador entre pantallas usando árboles, rocas, agua y otros obstáculos.
4. Debería ser posible mezclar tilemaps, sprites y otro contenido visual.

Primero, ejecuta el ejemplo y camina por el gran mundo de pantallas 3x3 para familiarizarte con la configuración del ejemplo. Controlas el personaje con las teclas de flecha.

## La colección principal

Abre "/main/main.collection" para ver la colección bootstrap de este ejemplo.

![](images/rpgmap/main_collection.png)

La colección principal contiene el objeto de juego del personaje del jugador, controlado en 8 direcciones con los botones de flecha, y un segundo objeto de juego llamado "game" que controla el flujo del juego. El objeto "game" consta de un script y una collection factory para cada pantalla del juego. Las factories se nombran según el esquema de nombres de la cuadrícula de pantallas.

El script "/main/game.script" rastrea en qué pantalla se encuentra actualmente el jugador. El script también reacciona a un mensaje personalizado llamado "load_screen". Este mensaje carga una nueva pantalla y la intercambia con la pantalla actual en la dirección en que se mueve el héroe. Inicialmente, una pantalla se carga en el centro de la pantalla y no hay otra pantalla con la que intercambiar lugar.

## Cambiar pantallas

El héroe está controlado por el script "/main/hero.script". El script comprueba si el objeto de juego del héroe se mueve más allá de una línea superior, inferior, izquierda o derecha cerca del borde de la pantalla:

![](images/rpgmap/change_screen.png)

1. Si el héroe se mueve lo suficientemente cerca de un borde de la pantalla, se envía un mensaje al script del objeto "game" para cargar la siguiente pantalla.
2. La siguiente colección de pantalla se genera llamando a `factory.create()` en el componente collectionfactory correcto. El contenido de la colección se posiciona fuera de la pantalla.
3. La siguiente pantalla se desplaza al centro de la vista y la pantalla actual se desplaza hacia afuera en la dirección opuesta. El personaje del jugador también se desplaza la misma distancia y con la misma velocidad.
4. La vieja pantalla actual, que ahora está fuera de pantalla, se elimina y la siguiente pantalla se promueve para ser la nueva pantalla actual.
5. El héroe se anima para entrar en la vista en la nueva pantalla y el jugador recupera el control.

Todo esto ocurre dentro de un segundo, así que la transición es suave y no disruptiva.

## Pantallas

Cada pantalla en el mundo del juego se construye dentro de una colección separada que contiene el tilemap, el objeto colisionador y otros objetos de juego que son únicos de la pantalla. Para facilitar la gestión y carga de las pantallas, las colecciones de pantalla se nombran según un esquema sencillo:

![](images/rpgmap/screens.png)

Cada colección de pantalla se nombra según su posición en la cuadrícula del mundo. El primer número es la posición X de la cuadrícula y el segundo es la posición Y de la cuadrícula.

En la vista *Assets*, navega hasta la colección "/main/screens/0-0.collection" y ábrela; describe la pantalla en la esquina inferior izquierda del mapa:

![](images/rpgmap/screen_collection.png)

Observa que hay un objeto de juego llamado "root" que es el padre de todo el contenido de la pantalla. Esta es otra convención usada en el ejemplo y sirve para un propósito muy importante: cuando una pantalla se trae a la vista, solo hay que mover el objeto de juego "root". Todos los objetos hijos se mueven automáticamente junto con el padre raíz. Si hay objetos de juego especiales en una pantalla, también pueden animarse libremente, ya que su movimiento es relativo al padre raíz. Cuando la pantalla se desplaza hacia dentro o hacia fuera, estos hijos se mueven con la pantalla. Solo se necesita código especial si un objeto debe moverse entre pantallas.

Las abejas en la pantalla 0-1 son demostraciones simples de esta idea:

![](images/rpgmap/bees.png)

## Editar pantallas en el contexto del mundo

Cada pantalla tiene su propio tilemap que se puede editar en el editor de tilemap integrado. Sin embargo, el principal inconveniente de editar cada pantalla de forma aislada es que no es posible ver fácilmente cómo se conecta con sus pantallas adyacentes, que es un aspecto importante para crear continuidad a través del mundo del juego.

Por esta razón, se creó una colección especial. Abre "/main/map/test_layout.collection" para ver esta colección de layout de prueba del mundo:

![](images/rpgmap/test_layout.png)

El único propósito de esta colección es usarse como herramienta de edición durante el desarrollo. Editar una pantalla específica lado a lado con la colección de layout de prueba te da contexto para la pantalla en la que estás trabajando actualmente y hace que el proceso de edición sea mucho más agradable:

![](images/rpgmap/side_by_side.png)

Cualquier edición en el tilemap de la pantalla (aquí en el panel derecho) se refleja inmediatamente en la colección de prueba (en el panel izquierdo). Ten en cuenta también que la colección de layout de prueba no se agrega a la jerarquía estática, por lo que se excluye automáticamente de todas las builds.

## Resumen

Como has visto, este ejemplo está construido según restricciones específicas respecto al mundo del juego y cómo el héroe del juego lo atraviesa. Si tu juego tiene requisitos diferentes, probablemente necesites encontrar una solución distinta. Por ejemplo, si tu juego exige que la cámara se mueva de forma continua sobre el mapa del mundo, necesitas una manera diferente de dividir tu contenido, un mecanismo de carga diferente y también herramientas diferentes que te ayuden a crear tu mundo de juego.

Esto concluye el recorrido del ejemplo de mapa RPG. Como siempre, eres libre de usar el contenido del ejemplo de cualquier forma que consideres adecuada. Para aprender más sobre Defold, revisa nuestras [páginas de documentación](https://defold.com/learn) para más ejemplos, tutoriales, manuales y documentación de la API.

Si tienes problemas o preguntas, [visita nuestro foro](https://forum.defold.com/).

¡Feliz Defolding!
