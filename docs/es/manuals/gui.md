---
title: Escenas GUI en Defold
brief: Este manual explica el editor GUI de Defold, los distintos tipos de nodos GUI y el scripting de GUI.
---

# GUI

Defold te proporciona un editor GUI personalizado y potentes posibilidades de scripting diseñadas específicamente para la construcción e implementación de interfaces de usuario.

Una interfaz gráfica de usuario en Defold es un componente que construyes, adjuntas a un objeto de juego y colocas en una colección. Este componente tiene las siguientes propiedades:

* Tiene funcionalidades de layout simples, pero potentes, que permiten renderizar tu interfaz de usuario independientemente de la resolución y la relación de aspecto.
* Puede tener comportamiento lógico adjunto mediante un *GUI script*.
* De forma predeterminada se renderiza encima de otro contenido, independientemente de la vista de la cámara, por lo que incluso si tienes una cámara en movimiento, tus elementos GUI permanecerán fijos en la pantalla. El comportamiento de renderizado se puede cambiar.

Los componentes GUI se renderizan de forma independiente de la vista del juego. Por eso no se colocan en una ubicación concreta en el editor de colecciones ni tienen una representación visual en el editor de colecciones. Sin embargo, los componentes GUI deben residir en un objeto de juego que sí tiene una ubicación en una colección. Cambiar esa ubicación no tiene efecto en la GUI.

## Crear un componente GUI

Los componentes GUI se crean a partir de un archivo prototipo de escena GUI (también conocido como "prefabs" o "blueprints" en otros motores). Para crear un nuevo componente GUI, haz <kbd>click derecho</kbd> en una ubicación del navegador *Assets* y selecciona <kbd>New ▸ Gui</kbd>. Escribe un nombre para el nuevo archivo GUI y presiona <kbd>Ok</kbd>.

![Nuevo archivo GUI](images/gui/new_gui_file.png)

Defold ahora abre automáticamente el archivo en el editor de escenas GUI.

![Nueva GUI](images/gui/new_gui.png)

*Outline* lista todo el contenido de la GUI: su lista de nodos y cualquier dependencia (ver abajo).

El área central de edición muestra la GUI. La barra de herramientas en la esquina superior derecha del área de edición contiene las herramientas *Move*, *Rotate* y *Scale*, además de un selector de [layout](/manuals/gui-layouts).

![barra de herramientas](images/gui/toolbar.png)

Un rectángulo blanco muestra los límites del layout seleccionado actualmente, con el ancho y la altura de visualización predeterminados definidos en la configuración del proyecto.

## Propiedades de Gui

Al seleccionar el nodo raíz "Gui" en *Outline* se muestran las propiedades del componente GUI en *Properties*:

*Script*
: El GUI script vinculado a este componente GUI.

*Material*
: El material usado al renderizar esta GUI. Ten en cuenta que también es posible añadir varios materiales a una Gui desde el panel *Outline* y asignarlos a nodos individuales.

*Adjust Reference*
: Controla cómo debe calcularse el *Adjust Mode* de cada nodo:

  - `Per Node` ajusta cada nodo contra el tamaño ajustado del nodo padre o de la pantalla redimensionada.
  - `Disable` desactiva el modo de ajuste de nodos. Esto fuerza a todos los nodos a conservar el tamaño que tienen definido.

*Current Nodes*
: La cantidad de nodos que se usan actualmente en esta GUI.

*Max Nodes*
: La cantidad máxima de nodos para esta GUI.

*Max Dynamic Textures*
: La cantidad máxima de texturas dinámicas que controla este componente GUI; el valor predeterminado es `128`. Esto incluye las texturas creadas con [`gui.new_texture()`](/ref/stable/gui/#gui.new_texture:texture_id-width-height-type-buffer-flip) y las texturas externas asignadas a la GUI mediante `go.set(..., "textures", ...)` o `gui.set(msg.url(), "textures", ...)`. Los proyectos que sustituyan muchas texturas externas pueden necesitar aumentar este límite.


## Manipulación en tiempo de ejecución

Puedes manipular propiedades GUI en tiempo de ejecución desde un componente script usando `go.get()` y `go.set()`:

Fonts
: Obtener o definir una fuente usada en una GUI.

![get_set_font](images/gui/get_set_font.png)

```lua
go.property("mybigfont", resource.font("/assets/mybig.font"))

function init(self)
  -- obtener el archivo de fuente asignado actualmente a la fuente con id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /builtins/fonts/default.font

  -- asignar a la fuente con id 'default' el archivo de fuente asignado a la propiedad de recurso 'mybigfont'
  go.set("#gui", "fonts", self.mybigfont, { key = "default" })

  -- obtener el nuevo archivo de fuente asignado a la fuente con id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /assets/mybig.font
end
```

Materials
: Obtener o definir un material usado en una GUI.

![get_set_material](images/gui/get_set_material.png)

```lua
go.property("myeffect", resource.material("/assets/myeffect.material"))

function init(self)
  -- obtener el archivo de material asignado actualmente al material con id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /effect.material

  -- asignar al material con id 'effect' el archivo de material asignado a la propiedad de recurso 'myeffect'
  go.set("#gui", "materials", self.myeffect, { key = "effect" })

  -- obtener el nuevo archivo de material asignado al material con id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /assets/myeffect.material
end
```

Textures
: Obtener o definir una textura (atlas) usada en una GUI.

![get_set_texture](images/gui/get_set_texture.png)

```lua
go.property("mytheme", resource.atlas("/assets/mytheme.atlas"))

function init(self)
  -- obtener el archivo de textura asignado actualmente a la textura con id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /theme.atlas

  -- asignar a la textura con id 'theme' el archivo de textura asignado a la propiedad de recurso 'mytheme'
  go.set("#gui", "textures", self.mytheme, { key = "theme" })

  -- obtener el nuevo archivo de textura asignado a la textura con id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /assets/mytheme.atlas
end
```

## Dependencias

El árbol de recursos en un juego Defold es estático, así que cualquier dependencia que necesites para tus nodos GUI debe añadirse al componente. *Outline* agrupa todas las dependencias por tipo bajo "carpetas":

![dependencias](images/gui/dependencies.png)

Para añadir una nueva dependencia, arrástrala y suéltala desde el panel *Asset* a la vista del editor.

Como alternativa, haz <kbd>click derecho</kbd> en la raíz "Gui" en *Outline* y luego selecciona <kbd>Add ▸ [type]</kbd> en el menú contextual emergente.

También puedes hacer <kbd>click derecho</kbd> en el icono de carpeta del tipo que quieres añadir y seleccionar <kbd>Add ▸ [type]</kbd>.

## Tipos de nodo {#node-types}

Un componente GUI se construye a partir de un conjunto de nodos. Los nodos son elementos simples. Se pueden transformar (mover, escalar y rotar) y ordenar en jerarquías padre-hijo, ya sea en el editor o en tiempo de ejecución mediante scripting. Existen los siguientes tipos de nodo:

Nodo caja
: ![nodo caja](images/icons/gui-box-node.png){.left}
  Nodo rectangular con un solo color, una textura o una animación flip-book. Consulta la [documentación de nodo caja](/manuals/gui-box) para obtener detalles.

<div style="clear: both;"></div>

Nodo de texto
: ![nodo de texto](images/icons/gui-text-node.png){.left}
  Muestra texto. Consulta la [documentación de nodo de texto](/manuals/gui-text) para obtener detalles.

<div style="clear: both;"></div>

Nodo circular
: ![nodo circular](images/icons/gui-pie-node.png){.left}
  Un nodo circular o elipsoide que se puede rellenar parcialmente o invertir. Consulta la [documentación de nodo circular](/manuals/gui-pie) para obtener detalles.

<div style="clear: both;"></div>

Nodo template
: ![nodo template](images/icons/gui.png){.left}
  Los templates se usan para crear instancias basadas en otros archivos de escena GUI. Consulta la [documentación de nodo template](/manuals/gui-template) para obtener detalles.

<div style="clear: both;"></div>

Nodo ParticleFX
: ![nodo particlefx](images/icons/particlefx.png){.left}
  Reproduce un efecto de partículas. Consulta la [documentación de nodo ParticleFX](/manuals/gui-particlefx) para obtener detalles.

<div style="clear: both;"></div>

Añade nodos haciendo <kbd>click derecho</kbd> en la carpeta *Nodes* y seleccionando <kbd>Add ▸</kbd> y luego <kbd>Box</kbd>, <kbd>Text</kbd>, <kbd>Pie</kbd>, <kbd>Template</kbd> o <kbd>ParticleFx</kbd>.

![Añadir nodos](images/gui/add_node.png)

También puedes presionar <kbd>A</kbd> y seleccionar el tipo que quieres añadir a la GUI.

## Propiedades de nodo {#node-properties}

Cada nodo tiene un conjunto amplio de propiedades que controlan su apariencia:

Id
: La identidad del nodo. Este nombre debe ser único dentro de la escena GUI.

Position, Rotation and Scale
: Controla la ubicación, orientación y estiramiento del nodo. Puedes usar las herramientas *Move*, *Rotate* y *Scale* para cambiar estos valores. Los valores se pueden animar desde script ([más información](/manuals/property-animation)).

Size (nodos caja, de texto y circulares)
: El tamaño del nodo es automático de forma predeterminada, pero al definir *Size Mode* en `Manual` puedes alterar el valor. El tamaño define los límites del nodo y se usa al hacer selección por input. Este valor se puede animar desde script ([más información](/manuals/property-animation)).

Size Mode (nodos caja y circulares)
: Si se define en `Automatic`, el editor definirá un tamaño para el nodo. Si se define en `Manual`, puedes definir el tamaño tú mismo.

Enabled
: Si está desmarcado, el nodo no se renderiza, no se anima y no se puede seleccionar usando `gui.pick_node()`. Usa `gui.set_enabled()` y `gui.is_enabled()` para cambiar y comprobar esta propiedad mediante programación.

Visible
: Si está desmarcado, el nodo no se renderiza, pero todavía se puede animar y seleccionar usando `gui.pick_node()`. Usa `gui.set_visible()` y `gui.get_visible()` para cambiar y comprobar esta propiedad mediante programación.

Text (nodos de texto)
: El texto que se muestra en el nodo.

Line Break (nodos de texto)
: Se define para que el texto se ajuste según el ancho del nodo.

Font (nodos de texto)
: La fuente que se usa al renderizar el texto.

Texture (nodos caja y circulares)
: La textura que se dibuja en el nodo. Es una referencia a una imagen o animación en un atlas o tile source.

Material (nodos caja, circulares, de texto y ParticleFX)
: El material que se usa al dibujar el nodo. Puede ser un material añadido a la sección Materials de *Outline* o dejarse en blanco para usar el material predeterminado asignado al componente GUI.

Slice 9 (nodos caja)
: Se define para conservar el tamaño en píxeles de la textura del nodo alrededor de los bordes cuando se redimensiona el nodo. Consulta la [documentación de nodo caja](/manuals/gui-box) para obtener detalles.

Inner Radius (nodos circulares)
: El radio interior del nodo, expresado a lo largo del eje X. Consulta la [documentación de nodo circular](/manuals/gui-pie) para obtener detalles.

Outer Bounds (nodos circulares)
: Controla el comportamiento de los límites exteriores. Consulta la [documentación de nodo circular](/manuals/gui-pie) para obtener detalles.

Perimeter Vertices (nodos circulares)
: La cantidad de segmentos que se usarán para construir la forma. Consulta la [documentación de nodo circular](/manuals/gui-pie) para obtener detalles.

Pie Fill Angle (nodos circulares)
: Qué porción del nodo circular debe rellenarse. Consulta la [documentación de nodo circular](/manuals/gui-pie) para obtener detalles.

Template (nodos template)
: El archivo de escena GUI que se usa como template para el nodo. Consulta la [documentación de nodo template](/manuals/gui-template) para obtener detalles.

ParticleFX (nodos ParticleFX)
: El efecto de partículas que se usa en este nodo. Consulta la [documentación de nodo ParticleFX](/manuals/gui-particlefx) para obtener detalles.

Color
: El color del nodo. Si el nodo tiene textura, el color tiñe la textura. El color se puede animar desde script ([más información](/manuals/property-animation)).

Alpha
: La translucidez del nodo. El valor alpha se puede animar desde script ([más información](/manuals/property-animation)).

Inherit Alpha
: Marcar esta casilla hace que un nodo herede el valor alpha del nodo padre. El valor alpha del nodo se multiplica entonces por el valor alpha del padre.

Leading (nodos de texto)
: Un número de escala para el interlineado. Un valor de `0` no da interlineado. `1` (el valor predeterminado) es el interlineado normal.

Tracking (nodos de texto)
: Un número de escala para el espaciado entre letras. El valor predeterminado es 0.

Layer
: Asignar una capa al nodo anula el orden de dibujo normal y en su lugar sigue el orden de capas. Consulta abajo para obtener detalles.

Blend mode
: Controla cómo se mezclan los gráficos del nodo con los gráficos de fondo:
  - `Alpha` mezcla con alpha los valores de píxel del nodo con el fondo. Esto corresponde al modo de mezcla "Normal" en software gráfico.
  - `Add` suma los valores de píxel del nodo con el fondo. Esto corresponde a "Linear dodge" en algunos software gráficos.
  - `Multiply` multiplica los valores de píxel del nodo con el fondo.
  - `Screen` multiplica inversamente los valores de píxel del nodo con el fondo. Esto corresponde al modo de mezcla "Screen" en software gráfico.

Pivot
: Define el punto pivot del nodo. Esto se puede ver como el "punto central" del nodo. Cualquier rotación, escalado o cambio de tamaño ocurrirá alrededor de este punto.

  Los valores posibles son `Center`, `North`, `South`, `East`, `West`, `North West`, `North East`, `South West` o `South East`.

  ![punto pivot](images/gui/pivot.png)

  Si cambias el pivot de un nodo, el nodo se moverá para que el nuevo pivot quede en la posición del nodo. Los nodos de texto se alinean de modo que `Center` centra el texto, `West` alinea el texto a la izquierda y `East` alinea el texto a la derecha.

X Anchor, Y Anchor
: El anclaje controla cómo se altera la posición vertical y horizontal del nodo cuando los límites de la escena, o los límites del nodo padre, se estiran para ajustarse al tamaño físico de la pantalla.

  ![Anclaje sin ajustar](images/gui/anchoring_unadjusted.png)

  Están disponibles los siguientes modos de anclaje:

  - `None` (para *X Anchor* y *Y Anchor*) conserva la posición del nodo desde el centro del nodo padre o de la escena, relativa a su tamaño *ajustado*.
  - `Left` o `Right` (*X Anchor*) escala la posición horizontal del nodo para que mantenga la posición desde los bordes izquierdo y derecho del nodo padre o de la escena en el mismo porcentaje.
  - `Top` o `Bottom` (*Y Anchor*) escala la posición vertical del nodo para que mantenga la posición desde los bordes superior e inferior del nodo padre o de la escena en el mismo porcentaje.

  ![Anclaje](images/gui/anchoring.png)

Adjust Mode
: Define el modo de ajuste del nodo. La configuración del modo de ajuste controla qué le ocurre a un nodo cuando los límites de la escena, o los límites del nodo padre, se ajustan para encajar con el tamaño físico de la pantalla.

  Un nodo creado en una escena donde la resolución lógica es una resolución horizontal típica:

  ![Sin ajustar](images/gui/unadjusted.png)

  Ajustar la escena a una pantalla vertical hace que la escena se estire. La caja delimitadora de cada nodo se estira del mismo modo. Sin embargo, al definir el modo de ajuste, la relación de aspecto del contenido del nodo puede mantenerse intacta. Están disponibles los siguientes modos:

  - `Fit` escala el contenido del nodo para que sea igual al ancho o alto de la caja delimitadora estirada, el que sea menor. En otras palabras, el contenido encajará dentro de la caja delimitadora estirada del nodo.
  - `Zoom` escala el contenido del nodo para que sea igual al ancho o alto de la caja delimitadora estirada, el que sea mayor. En otras palabras, el contenido cubrirá por completo la caja delimitadora estirada del nodo.
  - `Stretch` estira el contenido del nodo para que rellene la caja delimitadora estirada del nodo.

  ![Modos de ajuste](images/gui/adjusted.png)

  Si la propiedad de escena GUI *Adjust Reference* se define en `Disabled`, esta configuración se ignorará.

Clipping Mode (nodos caja y circulares)
: Define el modo de clipping en el nodo:

  - `None` renderiza el nodo como de costumbre.
  - `Stencil` hace que los límites del nodo definan una máscara stencil que se usa para recortar los nodos hijos del nodo.

  Consulta el [manual de clipping de GUI](/manuals/gui-clipping) para obtener detalles.

Clipping Visible (nodos caja y circulares)
: Se define para renderizar el contenido del nodo en el área stencil. Consulta el [manual de clipping de GUI](/manuals/gui-clipping) para obtener detalles.

Clipping Inverted (nodos caja y circulares)
: Invierte la máscara stencil. Consulta el [manual de clipping de GUI](/manuals/gui-clipping) para obtener detalles.


## Pivot, Anchors y Adjust Mode

La combinación de las propiedades Pivot, Anchors y Adjust Mode permite un diseño de GUI muy flexible, pero puede ser algo difícil entender cómo funciona todo sin mirar un ejemplo concreto. Tomemos como ejemplo este mockup de GUI creado para una pantalla de 640x1136:

![](images/gui/adjustmode_example_original.png)

La interfaz se crea con X Anchor e Y Anchor definidos en None, y el Adjust Mode de cada nodo se deja en el valor predeterminado de Fit. El punto Pivot del panel superior es North, el pivot del panel inferior es South y el punto pivot de las barras del panel superior se define en West. El resto de los nodos tiene puntos pivot definidos en Center. Si redimensionamos la ventana para hacerla más ancha, esto es lo que ocurre:

![](images/gui/adjustmode_example_resized.png)

Ahora, ¿qué pasa si queremos que las barras superior e inferior siempre sean tan anchas como la pantalla? Podemos cambiar el Adjust Mode de los paneles de fondo grises de arriba y abajo a Stretch:

![](images/gui/adjustmode_example_resized_stretch.png)

Esto es mejor. Los paneles de fondo grises ahora siempre se estirarán al ancho de la ventana, pero las barras del panel superior, así como las dos cajas de la parte inferior, no están posicionadas correctamente. Si queremos mantener las barras de arriba posicionadas a la izquierda, necesitamos cambiar X Anchor de None a Left:

![](images/gui/adjustmode_example_top_anchor_left.png)

Eso es exactamente lo que queremos para el panel superior. Las barras del panel superior ya tenían sus puntos Pivot definidos en West, lo que significa que se posicionarán correctamente con el borde izquierdo/oeste de las barras (Pivot) anclado al borde izquierdo del panel padre (X Anchor).

Ahora, si definimos X Anchor en Left para la caja de la izquierda y X Anchor en Right para la caja de la derecha, obtenemos el siguiente resultado:

![](images/gui/adjustmode_example_bottom_anchor_left_right.png)

Este no es exactamente el resultado esperado. Las dos cajas deberían permanecer tan cerca de los bordes izquierdo y derecho como las dos barras del panel superior. La razón es que el punto Pivot es incorrecto:

![](images/gui/adjustmode_example_bottom_pivot_center.png)

Ambas cajas tienen un punto Pivot definido en Center. Esto significa que, cuando la pantalla se vuelve más ancha, el punto central (el punto pivot) de las cajas permanecerá a la misma distancia relativa de los bordes. En el caso de la caja izquierda, estaba a un 17% del borde izquierdo con la ventana original de 640x1136:

![](images/gui/adjustmode_example_original_ratio.png)

Cuando se redimensiona la pantalla, el punto central de la caja izquierda permanece a la misma distancia de 17% del borde izquierdo:

![](images/gui/adjustmode_example_resized_stretch_ratio.png)

Si cambiamos el punto Pivot de Center a West para la caja de la izquierda y a East para la caja de la derecha, y reposicionamos las cajas, obtenemos el resultado que buscamos incluso cuando se redimensiona la pantalla:

![](images/gui/adjustmode_example_bottom_pivot_west_east.png)


## Orden de dibujo

Todos los nodos se renderizan en el orden en que aparecen bajo la carpeta "Nodes". El nodo en la parte superior de la lista se dibuja primero y por lo tanto aparecerá detrás de todos los demás nodos. El último nodo de la lista se dibuja al final, lo que significa que aparecerá delante de todos los demás nodos. Alterar el valor Z de un nodo no controla su orden de dibujo; sin embargo, si defines el valor Z fuera del rango de renderizado de tu render script, el nodo ya no se renderizará en pantalla. Puedes anular el orden por índice de los nodos con capas (ver abajo).

![Orden de dibujo](images/gui/draw_order.png)

Selecciona un nodo y presiona <kbd>Alt + Up/Down</kbd> para mover un nodo hacia arriba o hacia abajo y cambiar su orden de índice.

El orden de dibujo se puede cambiar en script:

```lua
local bean_node = gui.get_node("bean")
local shield_node = gui.get_node("shield")

if gui.get_index(shield_node) < gui.get_index(bean_node) then
  gui.move_above(shield_node, bean_node)
end
```

## Jerarquías padre-hijo

Un nodo se convierte en hijo de otro nodo arrastrándolo sobre el nodo que quieres que sea el padre del hijo. Un nodo con un padre hereda la transformación (posición, rotación y escala) aplicada al padre y relativa al pivot del padre.

![Padre hijo](images/gui/parent_child.png)

Los padres se dibujan antes que sus hijos. Usa capas para cambiar el orden de dibujo de los nodos padre e hijo y para optimizar el renderizado de nodos (ver abajo).


## Capas y draw calls {#layers-and-draw-calls}

Las capas proporcionan control preciso sobre cómo se dibujan los nodos y se pueden usar para reducir la cantidad de draw calls que el motor debe crear para dibujar una escena GUI. Cuando el motor está a punto de dibujar los nodos de una escena GUI, agrupa los nodos en lotes de draw calls según las siguientes condiciones:

- Los nodos deben usar el mismo tipo.
- Los nodos deben usar el mismo atlas o tile source.
- Los nodos deben renderizarse con el mismo blend mode.
- Deben usar la misma fuente.

Si un nodo difiere del anterior en cualquiera de estos puntos, romperá el lote y creará otra draw call. Los nodos de clipping siempre rompen el lote y cada ámbito stencil también rompe el lote.

La capacidad de organizar nodos en jerarquías facilita agrupar nodos en unidades manejables. Pero las jerarquías pueden romper efectivamente el renderizado en lotes si mezclas distintos tipos de nodo:

![Jerarquía que rompe el lote](images/gui/break_batch.png)

Cuando el pipeline de renderizado recorre la lista de nodos, se ve forzado a preparar un lote separado para cada nodo independiente porque los tipos son diferentes. En total, estos tres botones requerirán seis draw calls.

Al asignar capas a los nodos, se pueden ordenar de forma diferente, lo que permite que el pipeline de renderizado agrupe los nodos en menos draw calls. Empieza añadiendo a la escena las capas que necesites. Haz <kbd>click derecho</kbd> en el icono de carpeta "Layers" en *Outline* y selecciona <kbd>Add ▸ Layer</kbd>. Selecciona la nueva capa y asígnale una propiedad *Name* en la vista *Properties*.

![Capas](images/gui/layers.png)

Luego define la propiedad *Layer* en cada nodo con la capa correspondiente. El orden de dibujo de capas tiene prioridad sobre el orden normal de nodos por índice, por lo que definir los nodos caja de gráficos de botón como "graphics" y los nodos de texto de botón como "text" dará como resultado el siguiente orden de dibujo:

* Primero todos los nodos en la capa "graphics", desde arriba:

  1. "button-1"
  2. "button-2"
  3. "button-3"

* Luego todos los nodos en la capa "text", desde arriba:

  4. "button-text-1"
  5. "button-text-2"
  6. "button-text-3"

Los nodos ahora se pueden agrupar en dos draw calls, en lugar de seis. Una mejora importante de rendimiento.

Ten en cuenta que un nodo hijo sin capa definida heredará implícitamente la configuración de capa de su nodo padre. No definir una capa en un nodo lo añade implícitamente a la capa "null", que se dibuja antes que cualquier otra capa.
