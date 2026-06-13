---
title: Depuración con ZeroBrane Studio
brief: Este manual explica cómo usar ZeroBrane Studio para depurar código Lua en Defold.
---

# Depuración de scripts Lua con ZeroBrane Studio

Defold contiene un depurador integrado, pero también es posible ejecutar el IDE de Lua gratuito y de código abierto _ZeroBrane Studio_ como depurador externo. ZeroBrane Studio debe estar instalado para poder usar las funcionalidades de depuración. El programa es multiplataforma y se ejecuta tanto en macOS como en Windows.

Descarga "ZeroBrane Studio" desde http://studio.zerobrane.com

## Configuración de ZeroBrane

Para que ZeroBrane encuentre los archivos de tu proyecto, necesitas apuntarlo a la ubicación del directorio de tu proyecto Defold. Una forma cómoda de encontrarla es usar la opción <kbd>Show in Desktop</kbd> en un archivo en la raíz de tu proyecto Defold.

1. Haz click derecho en *game.project*
2. Elige <kbd>Show in Desktop</kbd>

![Mostrar en Finder](images/zerobrane/show_in_desktop.png)

## Configurar ZeroBrane

Para configurar ZeroBrane, selecciona <kbd>Project ▸ Project Directory ▸ Choose...</kbd>:

![Configurar](images/zerobrane/setup.png)

Una vez configurado para que coincida con el directorio actual del proyecto Defold, deberías poder ver el árbol de directorios del proyecto Defold en ZeroBrane, y navegar por los archivos y abrirlos.

Otros cambios de configuración recomendados, pero no necesarios, se encuentran más adelante en este documento.

## Iniciar el servidor de depuración

Antes de iniciar una sesión de depuración, debes iniciar el servidor de depuración integrado de ZeroBrane. La opción de menú para iniciarlo se encuentra en el menú <kbd>Project</kbd>. Selecciona <kbd>Project ▸ Start Debugger Server</kbd>:

![Iniciar depurador](images/zerobrane/startdebug.png)

## Conectar tu aplicación al depurador

La depuración se puede iniciar en cualquier momento durante la vida útil de la aplicación Defold, pero debe iniciarse activamente desde un script Lua. El código Lua para iniciar una sesión de depuración tiene este aspecto:

::: sidenote
Si tu juego se cierra cuando se llama a `dbg.start()`, podría deberse a que ZeroBrane detectó un problema y envía el comando de salida al juego. Por algún motivo, ZeroBrane necesita tener un archivo abierto para iniciar la sesión de depuración; de lo contrario, mostrará:
"Can't start debugging without an opened file or with the current file not being saved 'untitled.lua')."
En ZeroBrane, abre el archivo al que agregaste `dbg.start()` para corregir este error.
:::

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start()
```

Al insertar el código anterior en la aplicación, esta se conectará al servidor de depuración de ZeroBrane (a través de "localhost", por defecto) y se detendrá en la siguiente sentencia que se vaya a ejecutar.

```txt
Debugger server started at localhost:8172.
Mapped remote request for '/' to '/Users/my_user/Documents/Projects/Defold_project/'.
Debugging session started in '/Users/my_user/Documents/Projects/Defold_project'.
```

Ahora es posible usar las funcionalidades de depuración disponibles en ZeroBrane; puedes avanzar paso a paso, inspeccionar, agregar y eliminar breakpoints, etc.

::: sidenote
La depuración solo estará habilitada para el contexto Lua desde el que se inició. Habilitar "shared_state" en *game.project* significa que puedes depurar toda tu aplicación sin importar dónde la hayas iniciado.
:::

![Paso a paso](images/zerobrane/code.png)

Si el intento de conexión falla (posiblemente porque el servidor de depuración no se está ejecutando), tu aplicación seguirá ejecutándose con normalidad después de que se haya realizado el intento de conexión.

## Depuración remota

Como la depuración se realiza sobre conexiones de red normales (TCP), esto permite depurar de forma remota. Esto significa que es posible depurar tu aplicación mientras se ejecuta en un dispositivo móvil.

El único cambio necesario es en el comando que inicia la depuración. Por defecto, `start()` intentará conectarse a localhost, pero para la depuración remota necesitamos especificar manualmente la dirección del servidor de depuración de ZeroBrane, así:

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start("192.168.5.101")
```

Esto también significa que es importante asegurarse de tener conectividad de red desde el dispositivo remoto, y de que cualquier firewall o software similar permita conexiones TCP por el puerto 8172. De lo contrario, la aplicación podría quedarse bloqueada al iniciar cuando intente conectarse a tu servidor de depuración.

## Otra configuración recomendada de ZeroBrane

Es posible hacer que ZeroBrane abra automáticamente archivos script Lua durante la depuración. Esto permite entrar paso a paso en funciones de otros archivos fuente sin tener que abrirlos manualmente.

El primer paso es acceder al archivo de configuración del editor. Se recomienda cambiar la versión de usuario del archivo.

- Selecciona <kbd>Edit ▸ Preferences ▸ Settings: User</kbd>
- Agrega lo siguiente al archivo de configuración:

  ```txt
  - to automatically open files requested during debugging
  editor.autoactivate = true
  ```

- Reinicia ZeroBrane

![Other recommended settings](images/zerobrane/otherrecommended.png)
