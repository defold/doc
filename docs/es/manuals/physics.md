---
title: Física en Defold
brief: Defold incluye motores de física para 2D y 3D. Permiten simular interacciones de física newtoniana entre diferentes tipos de objetos de colisión.
---

# Física

Defold incluye una versión modificada del motor de física [Box2D](http://www.box2d.org) (versión 2.2.1) para simulaciones de física 2D y el motor de física Bullet (versión 2.77) para física 3D. Permite simular interacciones de física newtoniana entre diferentes tipos de _objetos de colisión_. Este manual explica cómo funciona.

Los conceptos principales de los motores de física usados en Defold son:

* **Objetos de colisión** - Un objeto de colisión es un componente que usas para dar comportamiento físico a un objeto de juego. Un objeto de colisión tiene propiedades físicas como peso, fricción y forma. [Aprende cómo crear un objeto de colisión](/manuals/physics-objects).
* **Formas de colisión** - Un objeto de colisión puede usar varias formas primitivas o una sola forma compleja para definir su extensión espacial. [Aprende cómo agregar formas a un objeto de colisión](/manuals/physics-shapes).
* **Grupos de colisión** - Todos los objetos de colisión deben pertenecer a un grupo predefinido, y cada objeto de colisión puede especificar una lista de otros grupos con los que puede colisionar. [Aprende cómo usar grupos de colisión](/manuals/physics-groups).
* **Mensajes de colisión** - Cuando dos objetos de colisión colisionan, el motor de física envía mensajes a los objetos de juego a los que pertenecen los componentes. [Aprende más sobre los mensajes de colisión](/manuals/physics-messages)

Además de los propios objetos de colisión, también puedes definir **constraints** de objetos de colisión, conocidos más comúnmente como **joints**, para conectar dos objetos de colisión y limitar o aplicar fuerza de otras maneras, así como influir en cómo se comportan en la simulación de física. [Aprende más sobre joints](/manuals/physics-joints).

También puedes sondear y leer el mundo de física a lo largo de un rayo lineal conocido como **ray cast**. [Aprende más sobre ray casts](/manuals/physics-ray-casts).


## Unidades usadas por la simulación del motor de física

El motor de física simula física newtoniana y está diseñado para funcionar bien con unidades de metros, kilogramos y segundos (MKS). Además, el motor de física está ajustado para funcionar bien con objetos en movimiento de un tamaño en el rango de 0.1 a 10 metros (los objetos estáticos pueden ser más grandes) y, por defecto, el motor trata 1 unidad (píxel) como 1 metro. Esta conversión entre píxeles y metros es conveniente a nivel de simulación, pero desde la perspectiva de creación de juegos no es muy útil. Con la configuración por defecto, una forma de colisión con un tamaño de 200 píxeles se trataría como si tuviera un tamaño de 200 metros, lo cual está muy fuera del rango recomendado, al menos para un objeto en movimiento.

En general, es necesario escalar la simulación de física para que funcione bien con el tamaño típico de los objetos en un juego. La escala de la simulación de física se puede cambiar en *game.project* mediante la [configuración de escala de física](/manuals/project-settings/#physics). Establecer este valor, por ejemplo, en 0.02 significaría que 200 píxeles se tratarían como 4 metros. Ten en cuenta que la gravedad (que también se cambia en *game.project*) debe aumentarse para adaptarse al cambio de escala.


## Actualizaciones de física {#physics-updates}

Se recomienda actualizar el motor de física a intervalos regulares para asegurar una simulación estable (en lugar de actualizarlo a intervalos posiblemente irregulares y dependientes de la tasa de fotogramas). Puedes usar una actualización fija para física marcando la [configuración Use Fixed Timestep](/manuals/project-settings/#physics) de la sección Physics en el archivo *game.project*. La frecuencia de actualización se controla mediante la [configuración Fixed Update Frequency](/manuals/project-settings/#engine) de la sección Engine en el archivo *game.project*. Al usar un timestep fijo para física, también se recomienda usar la función de ciclo de vida `fixed_update(self, dt)` para interactuar con los objetos de colisión de tu juego, por ejemplo al aplicarles fuerzas.


## Advertencias y problemas comunes

Proxies de colección
: A través de proxies de colección es posible cargar más de una colección de nivel superior, o *mundo de juego*, en el motor. Al hacerlo, es importante saber que cada colección de nivel superior es un mundo físico separado. Las interacciones de física ([colisiones, triggers](/manuals/physics-messages) y [ray-casts](/manuals/physics-ray-casts)) solo ocurren entre objetos que pertenecen al mismo mundo. Por lo tanto, aunque los objetos de colisión de dos mundos visualmente estén justo uno encima del otro, no puede haber ninguna interacción de física entre ellos.

Colisiones no detectadas
: Si tienes problemas con colisiones que no se manejan o detectan correctamente, asegúrate de leer sobre la [depuración de física en el manual de depuración](/manuals/debugging-game-logic/#debugging-problems-with-physics).
