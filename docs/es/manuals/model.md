---
title: Modelos 3D en Defold
brief: Este manual describe cómo llevar modelos 3D, esqueletos y animaciones a tu juego.
---

# Componente Model

Defold es, en esencia, un motor 3D. Incluso cuando trabajas solo con material 2D, todo el renderizado se realiza en 3D, pero se proyecta ortográficamente en la pantalla. Defold te permite usar contenido 3D completo al incluir assets 3D, o _modelos_, en tus colecciones. Puedes crear juegos estrictamente en 3D solo con assets 3D, o puedes mezclar contenido 3D y 2D como prefieras.

## Crear un componente Model

Los componentes Model se crean igual que cualquier otro componente de objeto de juego. Puedes hacerlo de dos formas:

- Crea un *archivo Model* con <kbd>click derecho</kbd> en una ubicación del explorador *Assets* y selecciona <kbd>New... ▸ Model</kbd>.
- Crea el componente incrustado directamente en un objeto de juego con <kbd>click derecho</kbd> en un objeto de juego en la vista *Outline* y selecciona <kbd>Add Component ▸ Model</kbd>.

![Model en objeto de juego](images/model/model_gltf.png)

Una vez creado el modelo, debes especificar varias propiedades:

### Propiedades de Model

Aparte de las propiedades *Id*, *Position* y *Rotation*, existen las siguientes propiedades específicas del componente:

*Mesh*
: Esta propiedad debe hacer referencia al archivo glTF *.gltf* o *.glb* que contiene la malla que se va a usar. Si el archivo contiene morph targets, se importan junto con la malla. Si el archivo contiene varias mallas, solo se lee la primera.

*Create GO Bones*
: Activa esto para crear un objeto de juego por cada hueso del modelo. Puedes usar los objetos de juego para adjuntar otros objetos de juego, como armas, a los huesos de las manos y casos similares.

*Skeleton*
: Esta propiedad debe hacer referencia al archivo glTF *.gltf* o *.glb* que contiene el esqueleto que se va a usar para la animación. Ten en cuenta que Defold requiere un único hueso raíz en la jerarquía.

*Animations*
: Define esta propiedad con el *Animation Set File* que contiene las animaciones que quieres usar en el modelo.

*Default Animation*
: Esta es la animación (del animation set) que se reproducirá automáticamente en el modelo.

Además de las propiedades anteriores, también habrá un campo para asignar un material por cada malla del modelo:

*Material*
: Define esta propiedad con un material que hayas creado y que sea adecuado para un objeto 3D con textura. Hay varios materiales integrados que puedes usar como punto de partida:

  * Usa *model.material* para modelos estáticos no instanciados
  * Usa *model_instances.material* para modelos estáticos instanciados
  * Usa *model_skinned.material* para modelos con skin (animados) no instanciados
  * Usa *model_skinned_instances.material* para modelos con skin (animados) instanciados

Según el material, habrá una o más propiedades de textura:

*Texture*
: Esta propiedad debe apuntar al archivo de imagen de textura que quieres aplicar al objeto.


## Manipulación en el editor

Con el componente Model en su lugar, puedes editar y manipular libremente el componente y/o el objeto de juego que lo encapsula con las herramientas habituales de *Scene Editor* para mover, rotar y escalar el modelo a tu gusto.

## Manipulación en runtime

Puedes manipular modelos en runtime mediante varias funciones y propiedades diferentes (consulta la [documentación de la API para su uso](/ref/model/)).

![Wiggler en el juego](images/model/runtime.png)

### Animación en runtime

Defold proporciona soporte potente para controlar la animación en runtime. Más información en el [manual de animación de modelos](/manuals/model-animation):

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

El cursor de reproducción de animación se puede animar a mano o mediante el sistema de animación de propiedades:

```lua
-- define la animación run
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- anima el cursor
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

Los modelos también pueden usar animaciones de morph targets de glTF. Los pesos de los morph targets se animan con `model.play_anim()` igual que otras animaciones de modelos, y se pueden leer o sobrescribir en runtime con [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) y [`model.set_blend_weights()`](/ref/model#model.set_blend_weights). Consulta la [sección de morph targets](/manuals/model-animation#morph-targets) en el manual de animación de modelos para más detalles.

### Cambiar propiedades

Un modelo también tiene varias propiedades diferentes que pueden manipularse con `go.get()` y `go.set()`:

`animation`
: La animación actual del modelo (`hash`) (solo lectura). Cambias la animación usando `model.play_anim()` (ver arriba).

`cursor`
: El cursor de animación normalizado (`number`).

`material`
: El material del modelo (`hash`). Puedes cambiarlo usando una propiedad de recurso de material y `go.set()`. Consulta la [referencia de la API para ver un ejemplo](/ref/model/#material).

`playback_rate`
: La tasa de reproducción de la animación (`number`).

`textureN`
: Las texturas del modelo donde N es 0-7 (`hash`). Puedes cambiarlas usando una propiedad de recurso de textura y `go.set()`. Consulta la [referencia de la API para ver un ejemplo](/ref/model/#textureN).


## Material

El software 3D suele permitirte definir propiedades en los vértices del objeto, como color y texturas. Esta información se guarda en el archivo glTF *.gltf* o *.glb* que exportas desde tu software 3D. Según los requisitos de tu juego, tendrás que seleccionar y/o crear materiales adecuados y _eficientes_ para tus objetos. Un material combina _programas de shader_ con un conjunto de parámetros para renderizar el objeto.

Hay varios materiales integrados que puedes usar como punto de partida:

  * Usa *model.material* para modelos estáticos no instanciados
  * Usa *model_instances.material* para modelos estáticos instanciados
  * Usa *model_skinned.material* para modelos con skin (animados) no instanciados
  * Usa *model_skinned_instances.material* para modelos con skin (animados) instanciados

Si necesitas crear materiales personalizados para tus modelos, consulta la [documentación de Material](/manuals/material) para más información. El [manual de Shader](/manuals/shader) contiene información sobre cómo funcionan los programas de shader.


### Constantes del material

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: El tinte de color del modelo (`vector4`). El vector4 se usa para representar el tinte con x, y, z y w correspondientes al tinte rojo, verde, azul y alfa.


## Renderizado

El script de render predeterminado está hecho a medida para juegos 2D y no funciona con modelos 3D. Pero puedes habilitar el renderizado de tus modelos copiando el script de render predeterminado y agregando unas pocas líneas de código al script de render. Por ejemplo:

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- ortográfica
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

Consulta la [documentación de Render](/manuals/render) para más detalles sobre cómo funcionan los scripts de render.
