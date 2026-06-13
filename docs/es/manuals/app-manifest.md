---
title: Manifiesto de la aplicación
brief: Este manual describe cómo se puede usar el manifiesto de la aplicación para excluir funcionalidades del motor.
---

# Manifiesto de la aplicación

El manifiesto de la aplicación se usa para excluir o controlar qué funcionalidades se incluyen en el motor. Excluir funcionalidades del motor que no se usan es una práctica recomendada, ya que reduce el tamaño binario final del juego.
El manifiesto de la aplicación también contiene algunas opciones para controlar la compilación de código para la plataforma HTML5, como la versión mínima de navegador compatible y los ajustes de memoria, que también pueden afectar el tamaño del binario resultante.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# Aplicar el manifiesto

En `game.project`, asigna el manifiesto en `Native Extensions` -> `App Manifest`.

## Físicas (`Physics`)

Controla qué motor de físicas usar, o selecciona None para excluir completamente las físicas.

## Físicas 2D (`Physics 2d`)

Selecciona qué versión de Box2D usar.

## Rig + modelo (`Rig + Model`)

Controla la funcionalidad de rig y modelo, o selecciona None para excluir por completo modelo y rig. (Consulta la documentación de [`Model`](https://defold.com/manuals/model/#model-component)).


## Excluir grabación (`Exclude Record`)

Excluye la capacidad de grabación de video del motor (consulta la documentación del mensaje [`start_record`](https://defold.com/ref/stable/sys/#start_record)).


## Excluir profiler (`Exclude Profiler`)

Excluye el profiler del motor. El profiler se usa para recopilar contadores de rendimiento y uso. Aprende a usar el profiler en el [manual de profiling](/manuals/profiling/).


## Excluir sonido (`Exclude Sound`)

Excluye todas las capacidades de reproducción de sonido del motor.


## Excluir input (`Exclude Input`)

Excluye todo el manejo de input del motor.


## Excluir Live Update (`Exclude Live Update`)

Excluye la [funcionalidad Live Update](/manuals/live-update) del motor.


## Excluir módulo `image` (`Exclude Image`)

Excluye del motor el módulo de script `image` [enlace](https://defold.com/ref/stable/image/).


## Excluir módulo `types` (`Exclude Types`)

Excluye del motor el módulo de script `types` [enlace](https://defold.com/ref/stable/types/).


## Excluir Basis Universal (`Exclude Basis Universal`)

Excluye del motor la [biblioteca de compresión de texturas](/manuals/texture-profiles) Basis Universal.


## Usar Android Support Lib (`Use Android Support Lib`)

Usa la Android Support Library obsoleta en lugar de Android X. [Más información](https://defold.com/manuals/android/#using-androidx).


## Gráficos (`Graphics`)

Selecciona qué backend gráfico usar.

* OpenGL - Incluye solo OpenGL.
* Vulkan - Incluye solo Vulkan.
* OpenGL and Vulkan - Incluye tanto OpenGL como Vulkan. Vulkan será el backend predeterminado y recurrirá a OpenGL si Vulkan no está disponible.

## Usar el sistema completo de layout de texto (`Use full text layout system`)

Si está activado (`true`), permite usar la generación en runtime para fuentes de tipo SDF al usar True Type Fonts (`.ttf`) en el proyecto. Lee más detalles en el [manual de fuentes](https://defold.com/manuals/font/#enabling-runtime-fonts).


## Versión mínima de Safari (solo wasm-web)
Nombre del campo YAML: **`minSafariVersion`**
Valor predeterminado: **90000**

Versión mínima compatible de Safari. No puede ser menor que 90000. Para más información, consulta las opciones del compilador Emscripten [enlace](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-safari-version).

## Versión mínima de Firefox (solo wasm-web)
Nombre del campo YAML: **`minFirefoxVersion`**
Valor predeterminado: **34**

Versión mínima compatible de Firefox. No puede ser menor que 34. Para más información, consulta las opciones del compilador Emscripten [enlace](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-firefox-version).

## Versión mínima de Chrome (solo wasm-web)
Nombre del campo YAML: **`minChromeVersion`**
Valor predeterminado: **32**

Versión mínima compatible de Chrome. No puede ser menor que 32. Para más información, consulta las opciones del compilador Emscripten [enlace](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-chrome-version).

## Memoria inicial (solo wasm-web)
Nombre del campo YAML: **`initialMemory`**
Valor predeterminado: **33554432**

El tamaño de memoria asignado a la aplicación web. Si `ALLOW_MEMORY_GROWTH=0`, esta es la cantidad total de memoria que la aplicación web puede usar. Para más información, consulta [enlace](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#initial-memory). Valor en bytes. Ten en cuenta que el valor debe ser múltiplo del tamaño de página de WebAssembly (64KiB).
Esta opción se relaciona con `html5.heap_size` en *game.project* [enlace](https://defold.com/manuals/html5/#heap-size). La opción configurada mediante el manifiesto de la aplicación se establece durante la compilación y se usa como valor predeterminado para la opción `INITIAL_MEMORY`. El valor de *game.project* sobrescribe el valor del manifiesto de la aplicación y se usa en runtime.

## Tamaño del stack (solo wasm-web)
Nombre del campo YAML: **`stackSize`**
Valor predeterminado: **5242880**

El tamaño del stack de la aplicación. Para más información, consulta [enlace](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#stack-size). Valor en bytes.
