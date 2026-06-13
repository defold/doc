---
title: Preferencias del editor
brief: Puedes modificar la configuración del editor desde la ventana Preferences.
---

# Preferencias del editor {#editor-preferences}

Puedes modificar la configuración del editor desde la ventana Preferences. La ventana de preferencias se abre desde el menú <kbd>File -> Preferences</kbd>.

## General {#general}

![](images/editor/preferences_general.png)

Load External Changes on App Focus
: Activa el escaneo de cambios externos cuando el editor recibe el foco.

Open Bundle Target Folder
: Activa la apertura de la carpeta de destino del bundle cuando termina el proceso de bundling.

Enable Texture Compression
: Activa la [compresión de texturas](/manuals/texture-profiles) para todas las builds creadas desde el editor.

Escape Quits Game
: Cierra una build en ejecución de tu juego usando la tecla <kbd>Esc</kbd>.

Track Active Tab in Asset Browser
: El archivo editado en la pestaña seleccionada del panel *Editor* se seleccionará en el Asset Browser (también conocido como el panel *Asset*).

Lint Code on Build
: Activa el [linting de código](/manuals/writing-code/#linting-configuration) cuando se crea la build del proyecto. Esta opción está activada por defecto, pero se puede desactivar si el linting de un proyecto grande tarda demasiado.

Engine Arguments
: Argumentos que se pasarán al ejecutable dmengine cuando el editor cree y ejecute la build.
 Usa un argumento por línea. Por ejemplo:
 ```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```


## Código {#code}

![](images/editor/preferences_code.png)

Custom Editor
: Ruta absoluta a un editor externo. En macOS debería ser la ruta al ejecutable dentro de la .app (por ejemplo, `/Applications/Atom.app/Contents/MacOS/Atom`).

Open File
: El patrón usado por el editor personalizado para especificar qué archivo abrir. El patrón `{file}` se reemplazará por el nombre del archivo que se debe abrir.

Open File at Line
: El patrón usado por el editor personalizado para especificar qué archivo abrir y en qué número de línea. El patrón `{file}` se reemplazará por el nombre del archivo que se debe abrir y `{line}` por el número de línea.

Code editor font
: Nombre de una fuente instalada en el sistema para usar en el editor de código.

Zoom on Scroll
: Indica si se debe cambiar el tamaño de la fuente al desplazarse en el editor de código mientras se mantiene presionada la tecla Cmd/Ctrl.


### Abrir archivos script en Visual Studio Code {#open-script-files-in-visual-studio-code}

![](images/editor/preferences_vscode.png)

Para abrir archivos script desde el editor Defold directamente en Visual Studio Code, debes configurar los siguientes ajustes especificando la ruta al archivo ejecutable:

- macOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

 Define estos parámetros para abrir archivos y líneas específicos:

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

El carácter `.` aquí es obligatorio para abrir todo el workspace, no un archivo individual.


## Extensiones {#extensions}

![](images/editor/preferences_extensions.png)

Build Server
: URL al build server usado al crear un proyecto que contiene [extensiones nativas](/manuals/extensions). Es posible agregar un nombre de usuario y un token de acceso a la URL para acceso autenticado al build server. Usa la siguiente notación para especificar el nombre de usuario y el token de acceso: `username:token@build.defold.com`. El acceso autenticado es obligatorio para builds de Nintendo Switch y cuando ejecutas tu propia instancia de build server con autenticación activada ([consulta la documentación del build server](https://github.com/defold/extender/blob/dev/README_SECURITY.md) para más información). El nombre de usuario y la contraseña también se pueden definir como las variables de ambiente del sistema `DM_EXTENDER_USERNAME` y `DM_EXTENDER_PASSWORD`.

Build Server Username
: nombre de usuario para autenticación.

Build Server Password
: contraseña para autenticación; se almacenará cifrada en el archivo de preferencias.

Build Server Headers
: headers adicionales para el build server al crear extensiones nativas. Es importante para usar el servicio CloudFlare o servicios similares con extender.

## Herramientas {#tools}

![](images/editor/preferences_tools.png)

ADB path
: Ruta a la herramienta de línea de comando [ADB](https://developer.android.com/tools/adb) instalada en este sistema. Si tienes ADB instalado en tu sistema, el editor Defold lo usará para instalar y ejecutar archivos APK de Android empaquetados en un dispositivo Android conectado. Por defecto, el editor comprueba si ADB está instalado en ubicaciones conocidas, así que solo necesitas especificar la ruta si tienes ADB instalado en una ubicación personalizada.

ios-deploy path
: Ruta a las herramientas de línea de comando [ios-deploy](https://github.com/ios-control/ios-deploy) instaladas en este sistema (solo relevante para macOS). De forma similar a la ruta de ADB, el editor Defold usará esta herramienta para instalar y ejecutar aplicaciones iOS empaquetadas en un iPhone conectado. Por defecto, el editor comprueba si ios-deploy está instalado en ubicaciones conocidas, así que solo necesitas especificar la ruta si usas una instalación personalizada de ios-deploy.

## Mapa de teclas {#keymap}

![](images/editor/preferences_keymap.png)

Puedes configurar los atajos del editor, tanto agregar atajos personalizados como eliminar los integrados. Usa el menú contextual en comandos individuales de la tabla de atajos para editar los atajos, o haz doble click/presiona <kbd>Enter</kbd> para abrir un popup para un nuevo atajo.

Algunos atajos pueden tener advertencias: se muestran en color naranja. Pasa el cursor sobre el atajo para ver la advertencia. Las advertencias típicas son:
- atajos que se pueden escribir: el atajo seleccionado se puede introducir en entradas de texto. Asegúrate de que el comando esté desactivado en los contextos de edición de código / entrada de texto.
- conflictos: el mismo atajo está asignado a varios comandos diferentes. Asegúrate de que como máximo un comando esté activado cuando se invoca el atajo; de lo contrario, el editor ejecutará uno de los comandos asignados sin un comportamiento definido.
