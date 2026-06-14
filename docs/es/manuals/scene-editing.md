---
title: El editor de escenas de Defold
brief: El Scene Editor es donde editas colecciones, objetos de juego, GUIs, efectos de partículas y otros assets visuales. Este manual explica la selección, las herramientas y cómo navegar por la vista de escena en 2D y 3D, incluido Free Camera Mode y la configuración de cámara.
---

# El editor de escenas de Defold {#the-defold-scene-editor}

El **Scene Editor** es el editor visual que se usa para construir y editar escenas como colecciones, objetos de juego y otros assets visuales.

De forma predeterminada, muchas escenas visuales se abren con una vista **2D ortográfica**. Para trabajar en 3D puedes cambiar a una disposición orientada a 3D, activar un plano de Grid 3D y usar una cámara de **perspectiva**.

## Abrir el Scene Editor {#opening-the-scene-editor}

Abre el Scene Editor haciendo doble click en un recurso visual en el panel *Assets*, como:

- **Estructura de escena** — colecciones (`.collection`), objetos de juego (`.go`)
- **Assets 2D** — atlas (`.atlas`), tilemaps (`.tilemap`), sprites (`.sprite`), tile sources (`.tilesource`)
- **Assets 3D** — modelos (`.model`, `.glb`, `.gltf`)
- **UI** — escenas GUI (`.gui`)
- **Efectos** — efectos de partículas (`.particlefx`)
- Y otros

## Navegación de la vista de escena (controles de cámara) {#scene-view-navigation-camera-controls}

La cámara del Scene Editor puede controlarse con mouse y teclado. Los controles disponibles dependen de si usas la navegación estándar de cámara o **Free Camera Mode**.

### Navegación estándar (todos los editores visuales) {#standard-navigation-all-visual-editors}

Estos controles están disponibles en los editores visuales:

- **Desplazar**
  - <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Botón izquierdo del mouse</kbd>
- **Zoom**
  - <kbd>Rueda del mouse</kbd>, o
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Botón izquierdo del mouse</kbd>
- **Rotar/orbitar (3D) alrededor de la selección**
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Botón izquierdo del mouse</kbd>

También puedes usar **Frame Selection** (<kbd>F</kbd>) para enfocar la cámara en la selección actual.

## Orientación de escena 2D y 3D {#2d-and-3d-scene-orientation}

La vista de escena puede usarse en flujos de trabajo 2D y 3D:

- En **2D**, normalmente trabajas en una vista ortográfica con un Grid orientado a 2D.
- En **3D**, normalmente:
  - Reorientas la vista a una orientación 3D,
  - Usas una cámara de **perspectiva**,
  - Eliges un plano de Grid adecuado (a menudo **Y** para “suelo”).

Puedes acceder a estas funciones desde la barra de herramientas y el menú **View**.

![Scene Editor 3D](images/editor/3d_scene.png)

## Vista general de la barra de herramientas {#toolbar-overview}

En la esquina superior derecha de la vista de escena hay una barra de herramientas con herramientas y opciones de vista usadas con frecuencia (de izquierda a derecha):

- **Move Tool** (<kbd>W</kbd>)
- **Rotate Tool** (<kbd>E</kbd>)
- **Scale Tool** (<kbd>R</kbd>)
- **Grid Settings** (`▦`)
- **Align/Realign Camera 2D/3D** (`2D`) — alterna entre orientación 2D y 3D (atajo <kbd>.</kbd>)
- **Camera Perspective/Orthographic**
- **Visibility Filters** (`👁`)

![Barra de herramientas](images/editor/toolbar.png)

## Seleccionar y manipular objetos {#manipulating-objects}

### Seleccionar objetos {#selecting-objects}

Haz <kbd>Click izquierdo</kbd> en los objetos de la ventana principal para seleccionarlos. El rectángulo (o cuboide) que rodea al objeto en la vista del editor se resaltará en cian para indicar qué elemento está seleccionado. El objeto seleccionado también se resalta en la vista `Outline`, como en la imagen anterior.

  También puedes seleccionar objetos así:

- Haz <kbd>Click izquierdo</kbd> y <kbd>Arrastrar</kbd> para seleccionar todos los objetos dentro de la región de selección.
- Haz <kbd>Click izquierdo</kbd> en objetos en `Outline`; mientras mantienes <kbd>⇧ Shift</kbd> puedes ampliar la selección, o mientras mantienes <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> puedes seleccionar o deseleccionar el elemento en el que hiciste click.

#### Herramienta Move Tool {#move-tool}

![Move Tool](images/editor/icon_move.png){.left}

Para mover objetos, usa *Move Tool*. Puedes encontrarla en la barra de herramientas en la esquina superior derecha del editor de escenas, o presionando la tecla <kbd>W</kbd>.

![Mover objeto](images/editor/move.png){.inline}![Mover objeto 3D](images/editor/move_3d.png){.inline}

El gizmo cambia y muestra un conjunto de manipuladores, cuadrados y flechas (el manipulador seleccionado se vuelve naranja), que puedes <kbd>Arrastrar</kbd> para mover:

- un controlador cuadrado central cian para mover el objeto solo en el espacio de pantalla,
- 3 flechas, roja, verde y azul, a lo largo de cada eje para mover el objeto solo sobre el eje X, Y o Z indicado.
- 3 controladores cuadrados rojos, verdes y azules (con contorno y relleno transparente) para mover el objeto solo sobre el plano indicado, por ejemplo el plano X-Y (azul) y, si rotas la cámara en 3D, los planos X-Z (verde) y Y-Z (rojo).

#### Herramienta Rotate Tool {#rotate-tool}

![Rotate Tool](images/editor/icon_rotate.png){.left}

Para rotar objetos, usa *Rotate Tool* seleccionándola en la barra de herramientas, o presionando la tecla <kbd>E</kbd>.

![Rotar objeto](images/editor/rotate.png){.inline}![Rotar objeto 3D](images/editor/rotate_3d.png){.inline}

Esta herramienta consta de cuatro manipuladores circulares (el manipulador seleccionado se vuelve naranja) que puedes <kbd>Arrastrar</kbd> para rotar:

- un manipulador cian (el círculo exterior, el más grande) que rota el objeto en el espacio de pantalla
- 3 manipuladores circulares más pequeños, uno rojo, uno verde y uno azul, que permiten rotar alrededor de cada uno de los ejes X, Y y Z por separado. En la vista ortográfica 2D, dos de ellos son perpendiculares a los ejes X e Y, así que los círculos solo aparecen como dos líneas que cruzan el objeto.

#### Herramienta Scale Tool {#scale-tool}

![Scale Tool](images/editor/icon_scale.png){.left}

Para escalar objetos, usa *Scale Tool* seleccionándola en la barra de herramientas, o presionando la tecla <kbd>R</kbd>.

![Escalar objeto](images/editor/scale.png){.inline}![Escalar objeto 3D](images/editor/scale_3d.png){.inline}

Esta herramienta consta de un conjunto de manipuladores cuadrados/cúbicos (el manipulador seleccionado se vuelve naranja) que puedes <kbd>Arrastrar</kbd> para escalar:

- un cubo cian en el centro escala el objeto uniformemente en todos los ejes (incluido Z).
- 3 manipuladores cúbicos rojos, azules y verdes escalan el objeto a lo largo de cada uno de los ejes X, Y y Z por separado.
- 3 manipuladores cuadrados rojos, verdes y azules (con contorno y relleno transparente) escalan el objeto sobre los planos X-Y, X-Z o Y-Z por separado.

### Filtros de visibilidad {#visibility-filters}

Haz click en el icono de ojo de **Visibility Filters** (`👁`) en la barra de herramientas para alternar la visibilidad de varios tipos de componentes, así como de cajas delimitadoras y líneas guía (`Component Guides` o el atajo <kbd>Ctrl</kbd> + <kbd>H</kbd> (Win/Linux) o <kbd>^ Ctrl</kbd> + <kbd>⌘ Cmd</kbd> + <kbd>H</kbd> (Mac)).

![Filtros de visibilidad](images/editor/visibilityfilters.png)

## Configuración de Grid {#grid-settings}

La cuadrícula se puede personalizar para adaptarse a tu flujo de trabajo (especialmente útil en 3D). Haz click en el botón **Grid Settings** (`▦`) para abrir el popup de configuración de Grid.

![Grid Settings](images/editor/grid_popup.png)

La configuración incluye:

- **Grid size (X/Y/Z)**
  Define la separación entre líneas de la cuadrícula a lo largo de cada eje. Usa valores menores para colocar objetos pequeños con precisión, o valores mayores para una vista general más amplia.
- **Active plane (X/Y/Z)**
  Selecciona en qué plano se dibuja la cuadrícula. En flujos de trabajo 2D normalmente es **Z** (el plano X-Y predeterminado). En flujos de trabajo 3D, **Y** es común para representar un plano de suelo/piso.
- **Grid color**
  Define el color de las líneas de la cuadrícula. Es útil para obtener contraste sobre distintos fondos de escena.
- **Grid opacity**
  Controla cuán transparentes son las líneas de la cuadrícula. Los valores más bajos hacen que la cuadrícula sea menos intrusiva sin dejar de proporcionar una referencia.
- Un botón **Reset to Defaults**
  Restaura toda la configuración de Grid a sus valores originales.

## Tipo de cámara: Perspective frente a Orthographic {#camera-type-perspective-vs-orthographic}

El Scene Editor admite ambas:

- Cámara **Orthographic** (común en flujos de trabajo 2D)
- Cámara **Perspective** (común en flujos de trabajo 3D)

Usa el conmutador de cámara en la barra de herramientas para cambiar. En escenas 3D, la navegación en perspectiva suele sentirse más natural.

## Free Camera Mode {#free-camera-mode}

Para una navegación 3D rápida, el Scene Editor ofrece **Free Camera Mode**, una cámara en primera persona / de estilo “FPS”.

### Activar Free Camera Mode {#activating-free-camera-mode}

- Mantén presionado <kbd>Botón derecho del mouse</kbd> — Free Camera Mode está activo mientras mantengas presionado el botón
- <kbd>Shift</kbd> + <kbd>`</kbd> (backtick) — alterna Free Camera Mode, manteniéndolo activo después de soltar las teclas

::: sidenote
En algunas distribuciones de teclado (por ejemplo, sueca), la tecla backtick es una tecla muerta y puede no activar el atajo como se espera. Puedes reasignar este atajo en `File ▸ Preferences ▸ Keys` e introducir un atajo para `Scene -> Free Camera -> Activate`
:::

Cuando Free Camera Mode está activo, la vista de escena se resalta con una línea alrededor de los bordes.

### Salir de Free Camera Mode {#exiting-free-camera-mode}

- Suelta <kbd>Botón derecho del mouse</kbd> (cuando se activó manteniéndolo presionado), o
- <kbd>Botón izquierdo del mouse</kbd>, <kbd>Botón derecho del mouse</kbd> (presionar y soltar), o presiona <kbd>Esc</kbd> cuando Free Camera Mode se activó como alternancia.

### Mirar alrededor (mouse look) {#looking-around-mouse-look}

Mientras Free Camera Mode está activo, estas teclas controlan el movimiento de la cámara (en lugar de las herramientas del editor):

- Mueve el mouse para controlar **yaw** (izquierda/derecha) y **pitch** (arriba/abajo)
- **Pitch** está limitado para evitar que la cámara se voltee

También puedes invertir opcionalmente el eje Y (consulta la **configuración de Free Camera** más abajo).

### Moverse {#moving}

Mientras Free Camera Mode está activo:

- <kbd>W</kbd> — adelante
- <kbd>S</kbd> — atrás
- <kbd>A</kbd> — izquierda
- <kbd>D</kbd> — derecha
- <kbd>E</kbd> — arriba
- <kbd>Q</kbd> — abajo

::: sidenote
Todas las teclas de movimiento pueden reasignarse en `File ▸ Preferences ▸ Keys`. Luego busca `Scene -> Free Camera`
:::

Modificadores de velocidad:

- Mantén presionado <kbd>Shift</kbd> — moverse más rápido
- Mantén presionado <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> — moverse más lento / con más precisión

### Walking Mode (opcional) {#walking-mode-optional}

Free Camera Mode admite **Walking Mode**.

Cuando está activado:
- El movimiento arriba/abajo queda restringido para comportarse más como caminar en primera persona sobre un plano de suelo.
- Esto es útil al explorar un nivel y querer un movimiento “sobre el suelo” consistente.

## Popup de configuración de cámara {#camera-settings-popup}

El botón de cámara de perspectiva en la barra de herramientas tiene un popup de configuración para preferencias relacionadas con la cámara.

![Perspective Camera Settings](images/editor/camera_popup.png)

El popup contiene:

- **Move Speed**
  Ajusta la velocidad de movimiento de Free Camera.

- **Look Sensitivity**
  Ajusta qué tan rápido rota la cámara en respuesta al movimiento del mouse.

- **Invert Y**
  Invierte la mirada vertical del mouse.

- **Walking Mode**
  Restringe el movimiento para una navegación similar a estar sobre el suelo.

- **Reset to Defaults**
  Restaura la configuración de cámara predeterminada.
