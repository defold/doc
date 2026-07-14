---
title: Vista general del editor
brief: Este manual ofrece una vista general de cómo se ve y funciona el editor Defold, y de cómo navegar por él.
---

# Vista general del editor

El editor te permite explorar y manipular todos los archivos y carpetas de tu proyecto de juego de forma eficiente. Al editar archivos se abre un editor adecuado y se muestra toda la información relevante sobre el archivo en vistas separadas.

## Iniciar el editor

Cuando ejecutas el Defold Editor, se muestra una pantalla de selección y creación de proyectos. Haz click para seleccionar lo que quieres hacer:

MY PROJECTS
: Aquí están tus proyectos abiertos recientemente para que puedas acceder a ellos con rapidez. Esta es la vista predeterminada de la pantalla de inicio.

  Si no abriste ningún proyecto antes (o los eliminaste todos), mostrará dos botones: puedes hacer click en `Open From Disk…` para buscar y abrir uno usando el navegador de archivos del sistema, o hacer click en el botón `Create New Project`, lo que cambiará a la pestaña `TEMPLATES`.

  ![my projects](images/editor/start_no_projects.png)


  Si ya abriste proyectos antes, mostrará una lista de tus proyectos, como en la imagen siguiente:

  ![my projects](images/editor/start_my_projects.png)

TEMPLATES
: Contiene proyectos básicos vacíos o casi vacíos, creados para iniciar rápidamente un nuevo proyecto Defold para ciertas plataformas o usando ciertas extensiones.


TUTORIALS
: Contiene proyectos con tutoriales guiados para aprender, jugar y modificar, si quieres seguir un tutorial.


SAMPLES
: Contiene proyectos preparados para mostrar ciertos casos de uso.

  ![New project](images/editor/start_templates.png)

Cuando creas un nuevo proyecto, se almacena en tu unidad local y cualquier edición que hagas se guarda localmente.

Puedes aprender más sobre las distintas opciones en el [manual de configuración de proyecto](https://www.defold.com/manuals/project-setup/).

## Idioma del editor

En la esquina inferior izquierda de la pantalla de inicio puedes ver una selección de idioma: selecciona una de las localizaciones disponibles actualmente. Esto también está disponible en el editor en `File ▸ Preferences ▸ General ▸ Editor Language`.

![Languages](images/editor/languages.png)

## Paneles del editor {#the-editor-views}

El Defold Editor está separado en un conjunto de paneles, o vistas, que muestran información específica.

![Editor 2](images/editor/editor_overview.png)

### 1. Panel Assets
Lista todos los archivos y carpetas que forman parte de tu proyecto en una estructura de árbol, correspondiente a la misma estructura en tu disco. Haz click y desplázate para navegar por la lista. Todas las operaciones orientadas a archivos pueden realizarse en esta vista:

   - <kbd>Click izquierdo</kbd> para seleccionar cualquier archivo o carpeta; mientras mantienes <kbd>⇧ Shift</kbd> puedes ampliar la selección, o mientras mantienes <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> puedes seleccionar o deseleccionar el elemento en el que hiciste click.
   - <kbd>Doble click</kbd> en un archivo para abrirlo en un editor específico para ese tipo de archivo.
   - <kbd>Arrastrar y soltar</kbd> para añadir archivos desde otro lugar de tu disco al proyecto o mover archivos y carpetas a nuevas ubicaciones dentro del proyecto.
   - <kbd>Click derecho</kbd> para abrir un _menú contextual_ desde donde puedes crear nuevos archivos o carpetas, renombrar, eliminar, rastrear dependencias de archivos y más.

Los archivos y carpetas eliminados mediante el panel *Assets* se mueven a la Papelera del sistema cuando la plataforma lo permite. Si no se admite mover un elemento a la Papelera o la operación falla, el editor lo elimina permanentemente.

### 2. Panel Scene Editor {#the-scene-editor}

Al hacer doble click en una colección, un objeto de juego o un archivo de componente visual, se abre el *Scene Editor*: el editor visual para construir y editar escenas. Los archivos script y otros recursos no visuales se abren en sus propios editores dedicados.

![Scene Editor](images/editor/2d_scene.png)

Algunas de las funcionalidades principales que ofrece el Scene Editor:

- [Navegación de escenas 2D y 3D](/manuals/scene-editing/#2d-and-3d-scene-orientation) con modos de cámara ortográfica y de perspectiva
- [Herramientas de transformación](/manuals/scene-editing/#manipulating-objects) para mover, rotar y escalar objetos
- [Free Camera Mode](/manuals/scene-editing/#free-camera-mode) para navegación 3D en primera persona
- [Configuración de Grid](/manuals/scene-editing/#grid-settings) con tamaño, plano y apariencia configurables
- [Filtros de visibilidad](/manuals/scene-editing/#visibility-filters) para alternar tipos de componentes y guías

Lee más en el [manual del Scene Editor](/manuals/scene-editing/).

### 3. Panel Outline

Esta vista muestra el contenido del archivo que se está editando actualmente, pero en una estructura de árbol jerárquica. Outline refleja la vista del editor y te permite realizar operaciones sobre tus elementos:

   - <kbd>Click izquierdo</kbd> para seleccionar un elemento; mientras mantienes <kbd>⇧ Shift</kbd> puedes ampliar la selección, o mientras mantienes <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> puedes seleccionar o deseleccionar el elemento en el que hiciste click.
   - <kbd>Arrastrar y soltar</kbd> para mover elementos. Suelta un objeto de juego sobre otro objeto de juego en una colección para crear una relación padre-hijo.
   - <kbd>Click derecho</kbd> para abrir un _menú contextual_ desde donde puedes añadir elementos, eliminar elementos seleccionados, etc.

Es posible alternar la visibilidad de objetos de juego y componentes visuales haciendo click en el pequeño icono de ojo `👁` a la derecha de un elemento en la lista.

![Outline](images/editor/outline.png)

### 4. Panel Properties

Esta vista muestra propiedades asociadas con el elemento seleccionado actualmente, como Id, URL, Position, Rotation, Scale u otras propiedades específicas de componentes, y también propiedades personalizadas para scripts.

También puedes <kbd>Arrastrar</kbd> la flecha arriba-abajo `↕` y mover el mouse para cambiar el valor de la propiedad numérica dada.

![Properties](images/editor/properties.png)

### 5. Panel Tools

Esta vista tiene varias pestañas.

Pestaña *Console* : muestra cualquier salida de error, advertencia e información del motor, o impresiones intencionales que hagas mientras tu juego se está ejecutando,

*Build Errors* : muestra errores del proceso de build,

*Search Results* : muestra los resultados de buscar (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>) en todo el proyecto, si haces click en `Keep Results`,

*Curve Editor* : se usa al editar curvas en el [Particle Editor](/manuals/particlefx/).

El panel Tools también se usa para interactuar con el depurador integrado. Lee más sobre esto en el [manual de depuración](/manuals/debugging/).

### 6. Panel Changed Files

Si tu proyecto usa el sistema distribuido de control de versiones Git, esta vista lista cualquier archivo que se haya cambiado, añadido o eliminado en tu proyecto. Al sincronizar el proyecto regularmente puedes mantener tu copia local sincronizada con lo que está almacenado en el repositorio Git del proyecto; de esa manera puedes colaborar dentro de un equipo y no perderás tu trabajo si ocurre un desastre. Puedes aprender más sobre Git en nuestro [manual de control de versiones](/manuals/version-control/). Algunas operaciones orientadas a archivos pueden realizarse en esta vista:

   - <kbd>Click izquierdo</kbd> - para seleccionar un archivo dado; mientras mantienes <kbd>⇧ Shift</kbd> puedes ampliar la selección, o mientras mantienes <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> puedes seleccionar o deseleccionar el elemento en el que hiciste click. Si se selecciona un solo archivo cambiado, puedes hacer click en `Diff` para mostrar las diferencias. Puedes hacer click en `Revert` para deshacer los cambios en todos los archivos seleccionados.
   - <kbd>Doble click izquierdo</kbd> en un archivo para abrir una vista del archivo. El editor abre el archivo en un editor adecuado, igual que en la vista Assets.
   - <kbd>Click derecho</kbd> en un archivo para abrir un menú popup desde donde puedes abrir una vista de diff, revertir todos los cambios hechos al archivo, encontrar el archivo en el sistema de archivos y más.

### Barra de menú

En la parte superior de la vista del editor, o en la barra del sistema en Mac, puedes encontrar la barra de menú con 6 menús: `File`, `Edit`, `View`, `Project`, `Debug`, `Help`. Sus funciones se explican en los manuales.

### Barra de estado

En la barra inferior del editor puedes encontrar un espacio estrecho donde se muestra el estado, por ejemplo:
- cuando hay una nueva actualización disponible, será visible el botón clicable `Update Available`; revisa la sección Actualizar el editor más abajo en este manual.
- al crear una build o un bundle, se mostrará allí su progreso.

## Tamaño y visibilidad de los paneles

El tamaño de los paneles se puede ajustar dentro del editor con la acción <kbd>Arrastrar</kbd> sobre los bordes de sección entre los 6 paneles descritos arriba.

La visibilidad de los paneles se puede alternar en el editor usando opciones del menú `View` o usando los atajos indicados:
- `Toggle Assets Pane` (<kbd>F6</kbd>) para alternar la visibilidad de los paneles Assets y Changed Files
- `Toggle Changed Files` para alternar solo la visibilidad del panel Changed Files
- `Toggle Tools Pane` (<kbd>F7</kbd>) para alternar la visibilidad del panel Tools
- `Toggle Properties Pane` (<kbd>F8</kbd>) para alternar la visibilidad de los paneles Outline y Properties

![Panes Visibility](images/editor/editor_panes.png)

En el menú `View` también puedes alternar o cambiar otros ajustes relacionados con visibilidad, como Grid, Guides, Camera, ajustar la vista a la selección (`Frame Selection` o la tecla <kbd>F</kbd>) y alternar entre la vista 2D y 3D predeterminada (`Realign Camera` o la tecla <kbd>.</kbd>); muchos de ellos también son accesibles desde la barra de herramientas o mediante atajos.

## Pestañas

Si tienes varios archivos abiertos, se muestra una pestaña separada para cada archivo en la parte superior de la vista del editor. Las pestañas en un solo panel pueden moverse: haz <kbd>Arrastrar y soltar</kbd> para intercambiar sus posiciones dentro de la barra de pestañas. También puedes:

- hacer <kbd>Click derecho</kbd> en una pestaña para abrir un _menú contextual_,
- hacer click en `Close` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>W</kbd>) para cerrar una sola pestaña,
- hacer click en `Close Others` para cerrar todas las pestañas excepto la seleccionada,
- hacer click en `Close All` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd>+<kbd>W</kbd>) para cerrar todas las pestañas del panel activo,
- seleccionar `➝| Open As` para usar un editor distinto al predeterminado o la herramienta externa asociada configurada en `File ▸ Preferences ▸ Code ▸ Custom Editor`. Consulta más en el [manual de preferencias](/manuals/editor-preferences).

![Tabs](images/editor/tabs_custom.png)

## Edición lado a lado

Es posible abrir 2 vistas de editor una al lado de la otra.

- Haz <kbd>Click derecho</kbd> en la pestaña del editor que quieres mover y selecciona `Move to Other Tab Pane`.

![2 panes](images/editor/2-panes.png)

También puedes usar el menú de pestaña para `Swap with Other Tab Pane` y mover una pestaña dada entre paneles, o `Join Tab Panes` para volver a un solo panel.

## Crear nuevos archivos de proyecto {#creating-new-project-files}

Para crear nuevos archivos de recurso, selecciona `File ▸ New…` y luego elige el tipo de archivo en el menú, o usa el menú contextual:

Haz <kbd>Click derecho</kbd> en la ubicación objetivo en el navegador `Assets`, luego selecciona `New… ▸ [file type]`:

![create file](images/editor/create_file.png)

Escribe un *Name* adecuado para el nuevo archivo y, si es necesario, cambia *Location*. El nombre completo del archivo, incluido el sufijo de tipo de archivo, se muestra bajo *Preview* en el diálogo:

![create file name](images/editor/create_file_name.png)

## Plantillas

Es posible especificar plantillas personalizadas para cada proyecto. Para hacerlo, crea una nueva carpeta llamada `templates` en el directorio raíz del proyecto y añade nuevos archivos llamados `default.*` con las extensiones deseadas, como `/templates/default.gui` o `/templates/default.script`. Además, si se usa el token `{{NAME}}` en estos archivos, se reemplazará por el nombre de archivo especificado en la ventana de creación de archivos.

Si hay una plantilla disponible para un tipo de archivo dado, cada vez que se cree un nuevo archivo de este tipo, se inicializará con el contenido del archivo de `templates`.


![Templates](images/editor/templates.png)

## Importar archivos a tu proyecto

Para añadir archivos de assets (imágenes, sonidos, modelos, etc.) a tu proyecto, simplemente arrástralos y suéltalos en la posición correcta en el navegador *Assets*. Esto hará _copias_ de los archivos en la ubicación seleccionada dentro de la estructura de archivos del proyecto. Lee más sobre [cómo importar assets en nuestro manual](/manuals/importing-assets/).

![Import files](images/editor/import.png)

## Actualizar el editor

El editor buscará actualizaciones automáticamente cuando esté conectado a internet. Cuando se detecte una actualización, se mostrará un enlace azul clicable `Update Available` en la esquina inferior izquierda de la pantalla de selección de proyecto o en la esquina inferior derecha de la ventana del editor.

![Update from project selection](images/editor/update_start.png)
![Update from Editor](images/editor/update_available.png)

Presiona el enlace clicable `Update Available` para descargar y actualizar. Aparecerá una ventana de confirmación con información; haz click en `Download Update` para continuar.

![Update Editor popup](images/editor/update.png)

Verás el progreso de la descarga en la barra de estado inferior:

![Download progress](images/editor/download_status.png)

Después de que se descargue la actualización, el enlace azul cambiará a `Restart to Update`. Haz click en él para reiniciar y abrir el editor actualizado.

![Restart to update](images/editor/restart_to_update.png)

## Preferencias

Puedes modificar la configuración del editor en la ventana `Preferences`. Para abrirla, haz click en `File ▸ Preferences…` o usa el atajo <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>,</kbd>

Lee más detalles en el [manual de preferencias](/manuals/editor-preferences)

![Preferences](images/editor/preferences.png)

## Logs del editor {#editor-logs}
Si encuentras un problema con el editor y necesitas reportar un issue (`Help  ▸ Report Issue`), es buena idea proporcionar archivos de log del editor mismo. Para abrir la ubicación de los logs en el navegador de archivos del sistema, haz click en `Help ▸ Show Logs`.

Lee más en el [manual para obtener ayuda](/manuals/getting-help/#getting-help).

![Show Logs](images/editor/show_logs.png)

Los archivos de logs del editor pueden encontrarse aquí:

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` o `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` o `~/.local/state/Defold`

También puedes acceder a los logs del editor mientras el editor se está ejecutando si se inicia desde una terminal o línea de comandos. Para iniciar el editor usa el comando:

```shell
# Linux:
$ ./path/to/Defold/Defold

# macOS:
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## Servidor del editor

Cuando el editor abre un proyecto, iniciará un servidor web en un puerto aleatorio. El servidor puede usarse para interactuar con el editor desde otras aplicaciones. El puerto se escribe en el archivo `.internal/editor.port`.

El servidor proporciona una especificación OpenAPI en `http://localhost:$(cat .internal/editor.port)/openapi.json`. Es un punto de partida mínimo útil para flujos de trabajo con agentes.

Además, el ejecutable del editor tiene una opción de línea de comando `--port` (o `-p`), que permite especificar el puerto durante el inicio, por ejemplo::
```shell
# Windows
.\path\to\Defold\Defold.exe --port 8181

# Linux:
./path/to/Defold/Defold --port 8181

# macOS:
./path/to/Defold/Defold.app/Contents/MacOS/Defold --port 8181
```

## Metadatos de instalación del editor

Cuando el editor se inicia, escribe información sobre el lanzador y las rutas de instalación en una ubicación conocida. Las integraciones con IDE de terceros y otras herramientas pueden usar esto para encontrar editores Defold instalados:

| SO      | Ubicación |
|---------|-----------|
| macOS   | `~/Library/Application Support/Defold/installations.json` |
| Linux   | `${XDG_STATE_HOME:-~/.local/state}/Defold/installations.json` |
| Windows | `%LOCALAPPDATA%\Defold\installations.json` |

El archivo contiene un array JSON con un objeto por cada instalación conocida:

```json
[
  {
    "launcherPath": "/Applications/Defold.app/Contents/MacOS/Defold",
    "installPath": "/Applications/Defold.app",
    "lastLaunchedAt": "2026-07-06T12:34:56.789Z"
  }
]
```

## Estilo del editor

La apariencia del editor puede cambiarse con estilos personalizados. Lee más en el [manual de estilo del editor](/manuals/editor-styling).

## FAQ
:[Editor FAQ](../shared/editor-faq.md)
