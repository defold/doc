---
title: Escribir código
brief: Este manual cubre brevemente cómo trabajar con código en Defold.
---

# Escribir código

Aunque Defold te permite crear gran parte del contenido de tu juego usando herramientas visuales como los editores de tilemap y efectos de partículas, sigues creando la lógica del juego con un editor de código. La lógica del juego se escribe usando el [lenguaje de programación Lua](https://www.lua.org/), mientras que las extensiones del propio motor se escriben usando los lenguajes nativos de la plataforma objetivo.

## Escribir código Lua

Defold usa Lua 5.1 y LuaJIT (dependiendo de la plataforma objetivo), y debes seguir la especificación del lenguaje para esas versiones concretas de Lua al escribir la lógica de tu juego. Para más detalles sobre cómo trabajar con Lua en Defold, consulta nuestro [manual de Lua en Defold](/manuals/lua).

## Usar otros lenguajes que transpilan a Lua

Defold soporta el uso de transpiladores que emiten código Lua. Con una extensión de transpilador instalada, puedes usar lenguajes alternativos, como [Teal](https://github.com/defold/extension-teal), para escribir Lua con comprobación estática. Es una funcionalidad preliminar que tiene limitaciones: el soporte actual para transpiladores no expone la información sobre los módulos y funciones definidos en el runtime Lua de Defold. Esto significa que usar APIs de Defold como `go.animate` requerirá que escribas tú mismo las definiciones externas.

## Escribir código nativo

Defold te permite extender el motor de videojuegos con código nativo para acceder a funcionalidad específica de la plataforma que no proporciona el propio motor. También puedes usar código nativo cuando el rendimiento de Lua no sea suficiente (cálculos intensivos en recursos, procesamiento de imágenes, etc.). Consulta nuestros [manuales sobre extensiones nativas (Native Extensions)](/manuals/extensions/) para aprender más.

## Usar el editor de código integrado

Defold tiene un editor de código integrado que te permite abrir y editar archivos Lua (.lua), archivos script de Defold (.script, .gui_script y .render_script), así como cualquier otro archivo con una extensión que el editor no maneje de forma nativa. Además, el editor proporciona resaltado de sintaxis para archivos Lua y script.

![](/images/editor/code-editor.png)


### Autocompletado de código

El editor de código integrado mostrará autocompletado de funciones mientras escribes código:

![](/images/editor/codecompletion.png)

Presionar <kbd>CTRL</kbd> + <kbd>Space</kbd> mostrará información adicional sobre funciones, argumentos y valores de retorno:

![](/images/editor/apireference.png)

### Configuración de linting {#linting-configuration}

El editor de código integrado realiza linting de código usando [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) y [Lua language server](https://luals.github.io/wiki/diagnostics/). Para configurar Luacheck, crea un archivo `.luacheckrc` en la raíz del proyecto. Puedes leer la [página de configuración de Luacheck](https://luacheck.readthedocs.io/en/stable/config.html) para ver la lista de opciones disponibles. Defold usa los siguientes valores predeterminados para la configuración de Luacheck:

```lua
unused_args = false      -- no advertir sobre argumentos sin usar (común en archivos .script)
max_line_length = false  -- no advertir sobre líneas largas
ignore = {
    "611",               -- la línea contiene solo espacios en blanco
    "612",               -- la línea contiene espacios en blanco al final
    "614"                -- espacios en blanco al final en un comentario
},
```

## Usar un editor de código externo

El editor de código de Defold proporciona la funcionalidad básica que necesitas para escribir código, pero para casos de uso más avanzados o para usuarios avanzados con un editor de código favorito, es posible hacer que Defold abra los archivos usando un editor externo. En la [ventana Preferences, en la pestaña Code](/manuals/editor-preferences/#code), es posible definir un editor externo que se debe usar al editar código.

### Visual Studio Code - Defold Kit

Defold Kit es un plugin de Visual Studio Code con las siguientes funcionalidades:

* Instalar extensiones recomendadas
* Resaltado, autocompletado y linting de Lua
* Aplicar configuraciones relevantes al workspace
* Anotaciones Lua para la API de Defold
* Anotaciones Lua para dependencias
* Crear y lanzar builds
* Depurar con breakpoints
* Crear bundles para todas las plataformas
* Desplegar en dispositivos móviles conectados

Aprende más e instala Defold Kit desde el [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).


## Software de documentación

Hay paquetes de referencia de API creados por la comunidad disponibles para [Dash and Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
