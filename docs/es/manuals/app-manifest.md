---
title: Manifiesto de la aplicación
brief: Este manual describe cómo se puede usar el manifiesto de la aplicación para excluir funcionalidades del motor.
---

# Manifiesto de la aplicación

El manifiesto de la aplicación controla qué funcionalidades y backends se enlazan con el motor. Se recomienda excluir las funcionalidades que no se usan porque reduce el tamaño binario final del juego. El manifiesto de la aplicación también contiene opciones de compilación, como las versiones mínimas de navegador compatibles con HTML5 y los ajustes de memoria de WebAssembly.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# Aplicar el manifiesto

En `game.project`, asigna el manifiesto en `Native Extensions` -> `App Manifest`.

## Físicas 2D (`Physics 2D`) {#physics-2d}

Selecciona qué implementación de Box2D incluir:

* **Box2D Version 3** - Incluye Box2D 3. Es opcional y puede producir resultados de simulación diferentes a los de la implementación heredada, por lo que los proyectos existentes podrían necesitar reajustar sus opciones de físicas.
* **Box2D (Legacy Defold version)** - Incluye la implementación heredada de Box2D de Defold. Es la predeterminada.
* **None** - Excluye las físicas 2D.

Los ajustes del solver de Box2D son específicos de cada versión. Consulta las [opciones de proyecto de Box2D](/manuals/project-settings/#box2d) para más detalles.

## Físicas 3D (`Physics 3D`)

Incluye la implementación de físicas Bullet 3D. Se incluye de forma predeterminada; desactiva este ajuste para excluir las físicas 3D.

## Rig + modelo (`Rig + Model`)

Controla la funcionalidad de rig y modelo, o selecciona None para excluir por completo modelo y rig. (Consulta la documentación de [`Model`](https://defold.com/manuals/model/#model-component)).


## Excluir grabación (`Exclude Record`)

Excluye la capacidad de grabación de video del motor (consulta la documentación del mensaje [`start_record`](https://defold.com/ref/stable/sys/#start_record)).


## Profiler {#profiler}

Controla cuándo se enlaza la funcionalidad del profiler con el motor:

* **Debug Only** - Incluye el profiler solo en builds debug. Es el valor predeterminado.
* **None** - Excluye la funcionalidad del profiler de todas las variantes de build.
* **Always** - Incluye el profiler tanto en builds debug como release.

El ajuste del manifiesto de la aplicación controla si el código del profiler se enlaza con una build. Los ajustes de `profiler` en *game.project* controlan su comportamiento en runtime. Aprende a usar las funciones disponibles en el [manual de profiling](/manuals/profiling/).


## Sonido {#sound}

Los controles de sonido determinan qué sistema de sonido y decodificadores se enlazan con el motor.

### Excluir sonido (`Exclude Sound`)

Excluye todas las capacidades de reproducción de sonido del motor.

### Excluir decodificador de sonido: WAV (`Exclude Sound Decoder: WAV`)

Excluye el soporte para recursos de sonido WAV.

### Excluir decodificador de sonido: OGG (`Exclude Sound Decoder: OGG`)

Excluye el soporte para recursos de sonido Ogg Vorbis.

### Incluir decodificador de sonido: Opus (`Include Sound Decoder: Opus`)

Incluye soporte para recursos de sonido Ogg Opus. El decodificador Opus se excluye de forma predeterminada, por lo que esta opción debe activarse antes de poder reproducir recursos `.opus`. Consulta el [manual de sonido](/manuals/sound/) para conocer los formatos compatibles.


## Excluir input (`Exclude Input`)

Excluye todo el manejo de input del motor.


## Excluir Live Update (`Exclude Live Update`)

Excluye la [funcionalidad Live Update](/manuals/live-update) del motor.


## Excluir módulo `image` (`Exclude Image`)

Excluye del motor el módulo de script `image` [enlace](https://defold.com/ref/stable/image/).


## Excluir módulo `types` (`Exclude Types`)

Excluye del motor el módulo de script `types` [enlace](https://defold.com/ref/stable/types/).


## Excluir transcodificador Basis (`Exclude Basis Transcoder`)

Excluye del motor la [biblioteca de compresión de texturas](/manuals/texture-profiles) Basis Universal.


## Usar Android Support Lib (`Use Android Support Lib`)

Usa la Android Support Library obsoleta en lugar de Android X. [Más información](https://defold.com/manuals/android/#using-androidx).


## Gráficos (`Graphics`)

Selecciona qué backends gráficos incluir para cada plataforma. Una opción combinada incluye ambos backends para que el preferido pueda recurrir al otro cuando no esté disponible.

| Campo | Plataformas | Opciones | Predeterminado |
|---|---|---|---|
| **Graphics** | Windows y Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

En Linux ARM64, la opción **OpenGL** usa el backend OpenGL ES. En Android, la opción combinada predeterminada prefiere Vulkan cuando está disponible y recurre a OpenGL ES en caso contrario.

## Usar el sistema completo de layout de texto (`Use full text layout system`)

Si está activado (`true`), permite usar la generación en runtime para fuentes de tipo SDF al usar True Type Fonts (`.ttf`) en el proyecto. Lee más detalles en el [manual de fuentes](https://defold.com/manuals/font/#enabling-runtime-fonts).


## Versiones mínimas del navegador

Los campos YAML **`minSafariVersion`**, **`minFirefoxVersion`** y **`minChromeVersion`** especifican las versiones mínimas de navegador para las que compila Emscripten. Los valores predeterminados actuales y las versiones mínimas compatibles difieren entre los targets sin threads y con threads:

| Target | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Especifica los valores personalizados en el contexto del target correspondiente. El target con threads también tiene [requisitos de alojamiento](/manuals/html5/#creating-html5-bundle) adicionales. Consulta la referencia de ajustes de Emscripten para [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) y [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version).

## Memoria inicial (HTML5)
Nombre del campo YAML: **`initialMemory`**
Valor predeterminado: **33554432**

La cantidad inicial de memoria asignada a la aplicación web, en bytes. El valor debe ser múltiplo del tamaño de página de WebAssembly (64 KiB). Consulta el ajuste [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory) de Emscripten.

Esta opción proporciona el valor predeterminado en tiempo de compilación. El valor [`html5.heap_size`](/manuals/html5/#heap-size) de *game.project* lo sobrescribe en runtime.

## Tamaño del stack (HTML5)
Nombre del campo YAML: **`stackSize`**
Valor predeterminado: **5242880**

El tamaño del stack de la aplicación, en bytes. Consulta el ajuste [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size) de Emscripten.
