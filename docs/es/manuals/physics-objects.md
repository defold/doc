---
title: Objetos de colisión en Defold
brief: Un objeto de colisión es un componente que usas para dar comportamiento físico a un objeto de juego. Un objeto de colisión tiene propiedades físicas y una forma espacial.
---

# Objetos de colisión

Un objeto de colisión es un componente que usas para dar comportamiento físico a un objeto de juego. Un objeto de colisión tiene propiedades físicas como peso, restitución y fricción, y su extensión espacial está definida por una o más _formas_ que adjuntas al componente. Defold admite los siguientes tipos de objetos de colisión:

Objetos estáticos
: Los objetos estáticos nunca se mueven, pero un objeto dinámico que colisiona con un objeto estático reaccionará rebotando y/o deslizándose. Los objetos estáticos son muy útiles para construir geometría de niveles (es decir, suelo y paredes) que no se mueve. También son más baratos en rendimiento que los objetos dinámicos. No puedes mover ni cambiar de otro modo los objetos estáticos.

Objetos dinámicos
: Los objetos dinámicos son simulados por el motor de física. El motor resuelve todas las colisiones y aplica las fuerzas resultantes. Los objetos dinámicos son adecuados para objetos que deberían comportarse de forma realista. La forma más común de afectarlos es indirectamente, [aplicando fuerzas](/ref/physics/#apply_force) o cambiando el [damping](/ref/stable/physics/#angular_damping) y la [velocity](/ref/stable/physics/#linear_velocity) angulares, y el [damping](/ref/stable/physics/#linear_damping) y la [velocity](/ref/stable/physics/#angular_velocity) lineales. También es posible manipular directamente la posición y orientación de un objeto dinámico cuando la [opción Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) está habilitada en *game.project*.

Objetos cinemáticos
: Los objetos cinemáticos registran colisiones con otros objetos de física, pero el motor de física no realiza ninguna simulación automática. El trabajo de resolver las colisiones, o ignorarlas, queda a tu cargo ([más información](/manuals/physics-resolving-collisions)). Los objetos cinemáticos son muy adecuados para objetos controlados por el jugador o por scripts que requieren control detallado de las reacciones físicas, como un personaje jugador.

Triggers
: Los triggers son objetos que registran colisiones simples. Los triggers son objetos de colisión ligeros. Son similares a los [ray casts](/manuals/physics-ray-casts), ya que leen el mundo físico en lugar de interactuar con él. Son útiles para objetos que solo necesitan registrar un impacto (como una bala) o como parte de la lógica del juego cuando quieres activar ciertas acciones al llegar un objeto a un punto específico. Los triggers son computacionalmente más baratos que los objetos cinemáticos y deberían usarse en su lugar si es posible.


## Agregar un componente de objeto de colisión

Un componente de objeto de colisión tiene un conjunto de *Properties* que definen su tipo y sus propiedades físicas. También contiene una o más *Shapes* que definen la forma completa del objeto de física.

Para agregar un componente de objeto de colisión a un objeto de juego:

1. En la vista *Outline*, haz <kbd>click derecho</kbd> en el objeto de juego y selecciona <kbd>Add Component ▸ Collision Object</kbd> en el menú contextual. Esto crea un nuevo componente sin formas.
2. Haz <kbd>click derecho</kbd> en el nuevo componente y selecciona <kbd>Add Shape ▸ Box / Capsule / Sphere</kbd>. Esto agrega una nueva forma al componente de objeto de colisión. Puedes agregar cualquier número de formas al componente. También puedes usar un tilemap o un convex hull para definir la forma del objeto de física.
3. Usa las herramientas de mover, rotar y escalar para editar las formas.
4. Selecciona el componente en *Outline* y edita las *Properties* del objeto de colisión.

![Objeto de colisión de física](images/physics/collision_object.png)


## Agregar una forma de colisión

Un componente de colisión puede usar varias formas primitivas o una única forma compleja. Aprende más sobre las distintas formas y cómo agregarlas a un componente de colisión en el [manual de Collision Shapes](/manuals/physics-shapes).


## Propiedades del objeto de colisión

Id
: La identidad del componente.

Collision Shape
: Esta propiedad se usa para geometría de tile map o formas convexas que no usan formas primitivas. Consulta [Collision Shapes para obtener más información](/manuals/physics-shapes).

Type
: El tipo de objeto de colisión: `Dynamic`, `Kinematic`, `Static` o `Trigger`. Si defines el objeto como `Dynamic`, _debes_ definir la propiedad *Mass* con un valor distinto de cero. Para objetos `Dynamic` o `Static`, también deberías comprobar que los valores de *Friction* y *Restitution* sean adecuados para tu caso de uso.

Friction
: La fricción hace posible que los objetos se deslicen de forma realista unos contra otros. El valor de fricción suele definirse entre `0` (sin fricción en absoluto, un objeto muy resbaladizo) y `1` (fricción fuerte, un objeto abrasivo). Sin embargo, cualquier valor positivo es válido.

  La intensidad de la fricción es proporcional a la fuerza normal (esto se llama fricción de Coulomb). Cuando la fuerza de fricción se calcula entre dos formas (`A` y `B`), los valores de fricción de ambos objetos se combinan con la media geométrica:

```math
F = sqrt( F_A * F_B )
```

  Esto significa que si uno de los objetos tiene fricción cero, entonces el contacto entre ellos tendrá fricción cero.

Restitution
: El valor de restitución define el "rebote" del objeto. El valor suele estar entre 0 (colisión inelástica: el objeto no rebota en absoluto) y 1 (colisión perfectamente elástica: la velocidad del objeto se reflejará exactamente en el rebote).

  Los valores de restitución entre dos formas (`A` y `B`) se combinan usando la siguiente fórmula:

```math
R = max( R_A, R_B )
```

  Cuando una forma desarrolla múltiples contactos, la restitución se simula de forma aproximada porque Box2D usa un solver iterativo. Box2D también usa colisiones inelásticas cuando la velocidad de colisión es pequeña para evitar vibración por rebote.

Linear damping
: Linear damping reduce la velocidad lineal del cuerpo. Es diferente de la fricción, que solo ocurre durante el contacto, y puede usarse para dar a los objetos una apariencia flotante, como si se movieran a través de algo más denso que el aire. Los valores válidos están entre 0 y 1.

  Box2D aproxima el damping por estabilidad y rendimiento. Con valores pequeños, el efecto de damping es independiente del paso de tiempo, mientras que con valores de damping mayores, el efecto de damping varía con el paso de tiempo. Si ejecutas tu juego con un paso de tiempo fijo, esto nunca se convierte en un problema.

Angular damping
: Angular damping funciona como linear damping, pero reduce la velocidad angular del cuerpo. Los valores válidos están entre 0 y 1.

Locked rotation
: Al definir esta propiedad, se deshabilita totalmente la rotación en el objeto de colisión, sin importar qué fuerzas se le apliquen.

Bullet
: Al definir esta propiedad, se habilita la detección continua de colisiones (CCD) entre el objeto de colisión y otros objetos de colisión dinámicos. La propiedad *Bullet* se ignora si *Type* no está definido como `Dynamic`.

Group
: El nombre del grupo de colisión al que debería pertenecer el objeto. Puedes tener 16 grupos diferentes y nombrarlos como prefieras para tu juego. Por ejemplo, "players", "bullets", "enemies" y "world". Si *Collision Shape* está definido como un tile map, este campo no se usa, sino que los nombres de grupo se toman de la tile source. [Aprende más sobre los grupos de colisión](/manuals/physics-groups).

Mask
: Los otros _grupos_ con los que este objeto debería colisionar. Puedes nombrar un grupo o especificar varios grupos en una lista separada por comas. Si dejas el campo *Mask* vacío, el objeto no colisionará con nada. [Aprende más sobre los grupos de colisión](/manuals/physics-groups).

Generate Collision Events
: Si se habilita, permite que este objeto envíe eventos de colisión.

Generate Contact Events
: Si se habilita, permite que este objeto envíe eventos de contacto.

Generate Trigger Events
: Si se habilita, permite que este objeto envíe eventos de trigger.


## Propiedades en tiempo de ejecución

Un objeto de física tiene varias propiedades distintas que se pueden leer y cambiar usando `go.get()` y `go.set()`:

`angular_damping`
: El valor de angular damping para el componente de objeto de colisión (`number`). [Referencia de la API](/ref/physics/#angular_damping).

`angular_velocity`
: La velocidad angular actual del componente de objeto de colisión (`vector3`). [Referencia de la API](/ref/physics/#angular_velocity).

`linear_damping`
: El valor de linear damping para el objeto de colisión (`number`). [Referencia de la API](/ref/physics/#linear_damping).

`linear_velocity`
: La velocidad lineal actual del componente de objeto de colisión (`vector3`). [Referencia de la API](/ref/physics/#linear_velocity).

`mass`
: La masa física definida del componente de objeto de colisión. READ ONLY. (`number`). [Referencia de la API](/ref/physics/#mass).
