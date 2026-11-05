---
title: Pautas para portar y lanzar juegos
brief: Este manual destaca algunos aspectos a tener en cuenta al portar un juego a una nueva plataforma o al lanzar tu juego por primera vez.
---

# Pautas para portar y lanzar juegos {#porting-and-release-guidelines}

Esta página contiene una guía útil y una lista de comprobación de aspectos a tener en cuenta al lanzar un juego o al portarlo a una nueva plataforma.

Portar un juego de Defold a una nueva plataforma o lanzarlo por primera vez suele ser un proceso sencillo. En teoría basta con asegurarse de que las secciones correspondientes estén configuradas en el archivo *game.project*, pero para aprovechar al máximo cada plataforma se recomienda adaptar el juego a las particularidades de cada una.


## Controles {#input}
Asegúrate de adaptar el juego a los métodos de entrada de la plataforma. Considera agregar soporte para [gamepads](/manuals/input-gamepads) si la plataforma los soporta. Asegúrate también de que el juego tenga un menú de pausa: si un controlador se desconecta de repente, el juego debe pausarse.

## Localización {#localization}
Traduce todo el texto del juego. Para lanzamientos en Europa y América, considera traducir al menos a EFIGS (inglés, francés, italiano, alemán y español). Asegúrate de que sea posible cambiar fácilmente entre distintos idiomas dentro del juego (mediante el menú de pausa).

::: important
Solo iOS: asegúrate de especificar [Localizations](/manuals/project-settings/#localizations) en `game.project`, ya que `sys.get_info()` nunca devolverá un idioma que no esté en esta lista.
:::

Traduce el texto de la página de la tienda, ya que esto tendrá un impacto positivo en las ventas. Algunas plataformas requieren que el texto de la página de la tienda se traduzca al idioma de cada país donde el juego esté disponible.

## Materiales de la tienda {#store-materials}

### Icono de la app {#app-icon}
Asegúrate de que tu juego destaque frente a la competencia. El icono suele ser tu primer punto de contacto con posibles jugadores. Debe ser fácil de encontrar en una página llena de iconos de juegos.

### Banners e imágenes de la tienda {#store-banners-and-images}
Asegúrate de usar arte impactante y emocionante para tu juego. Probablemente valga la pena invertir algo de dinero en trabajar con un artista para crear arte que atraiga jugadores.


## Partidas guardadas {#save-games}

### Partidas guardadas en escritorio, móvil y web {#save-games-on-desktop-mobile-and-web}
Las partidas guardadas y otros estados guardados se pueden almacenar con la función de la API de Defold `sys.save(filename, data)` y cargar con `sys.load(filename)`. Puedes usar `sys.get_save_file(application_id, name)` para obtener una ruta a una ubicación específica del sistema operativo donde se pueden guardar archivos, normalmente en la carpeta personal del usuario que ha iniciado sesión.

### Partidas guardadas en consola {#save-games-on-console}
Usar `sys.get_save_file()` y `sys.save()` funciona bien en la mayoría de las plataformas, pero en consolas se recomienda adoptar un enfoque diferente. Las plataformas de consola suelen asociar un usuario con cada controlador conectado y, por lo tanto, las partidas guardadas, los logros y otras funcionalidades deben asociarse con su usuario correspondiente.

Los eventos de input de gamepad contendrán un id de usuario que se puede usar para asociar las acciones de un controlador con un usuario en la consola.

Las plataformas de consola y sus extensiones nativas expondrán funciones de API específicas de la plataforma para guardar y cargar datos asociados con un usuario específico. Usa estas API al guardar y cargar en consola.

Las API de plataformas de consola para operaciones de archivos suelen ser asíncronas. Al desarrollar un juego multiplataforma dirigido a consola, se recomienda diseñar el juego de modo que todas las operaciones de archivos sean asíncronas, independientemente de la plataforma. Ejemplo:

```lua
local function save_game(data, user_id, cb)
	if console then
		local filename = "savegame"
		consoleapi.save(user_id, filename, data, cb)
	else
		local filename = sys.get_save_file("mygame", "savegame" .. user_id)
		local success = sys.save(filename, data)
		cb(success)
	end
end
```


## Artefactos de build {#build-artifacts}

Asegúrate de [generar símbolos de depuración](/manuals/debugging-native-code/#symbolicate-a-callstack) para cada versión publicada, de modo que puedas depurar fallos. Guárdalos junto con el bundle de la aplicación.

## Optimizaciones de la aplicación {#application-optimizations}

Lee el [manual de optimización](/manuals/optimization) para saber cómo optimizar tu aplicación en rendimiento, tamaño, memoria y uso de batería.



## Rendimiento {#performance}
Prueba siempre en el hardware objetivo. Revisa el rendimiento del juego y optimiza si es necesario. Usa el [profiler](/manuals/profiling) para encontrar cuellos de botella en el código.


## Resolución de pantalla y tasa de refresco {#screen-resolution-and-refresh-rate}
Para plataformas con orientación y resolución de pantalla fijas: comprueba que el juego funcione con la resolución de pantalla y la relación de aspecto de la plataforma objetivo. Para plataformas con resolución de pantalla y relación de aspecto variables: comprueba que el juego funcione con una variedad de resoluciones de pantalla y relaciones de aspecto. Ten en cuenta qué tipo de [proyección de vista](/manuals/render/#default-view-projection) se usa en el script de render y la cámara.

Para plataformas móviles, bloquea la orientación de pantalla en *game.project* o asegúrate de que el juego funcione tanto en modo horizontal como vertical.

* **Tamaños de pantalla** - ¿Todo se ve bien en una pantalla más grande o más pequeña que el ancho y alto predeterminados configurados en *game.project*?
  * La proyección usada en el script de render y los layouts usados en la GUI influyen aquí.
* **Relaciones de aspecto** - ¿Todo se ve bien en una pantalla con una relación de aspecto diferente a la relación de aspecto predeterminada del ancho y alto configurados en *game.project*?
  * La proyección usada en el script de render y los layouts usados en la GUI influyen aquí.
* **Tasa de refresco** - ¿El juego funciona bien en una pantalla con una tasa de refresco superior a 60 Hz?
  * El vsync y el intervalo de swap en la sección Display de *game.project*.


## Teléfonos móviles, notch y cámaras hole punch {#mobile-phones-and-notch-and-hole-punch-cameras}
Se ha vuelto cada vez más popular usar un pequeño recorte para la lente en la pantalla para alojar la cámara frontal y los sensores (también conocido como notch o cámara hole punch). Al portar un juego a móvil, asegúrate de que la información crítica se mantenga dentro del área segura de la plataforma.

Defold cuenta con soporte integrado para áreas seguras en Android e iOS. Define `gui.safe_area_mode` en *game.project* para controlar qué márgenes opuestos del área segura afectan al ajuste de la GUI. `none` es el valor predeterminado e ignora los márgenes; `long` aplica los márgenes izquierdo y derecho en orientación horizontal y superior e inferior en vertical; `short` aplica el par opuesto; y `both` aplica los cuatro bordes. Un script GUI puede sustituir el modo global del proyecto para su escena con [`gui.set_safe_area_mode()`](/ref/gui/#gui.set_safe_area_mode). Para lógica personalizada de GUI o renderizado, [`window.get_safe_area()`](/ref/window/#window.get_safe_area) devuelve el rectángulo seguro y los márgenes individuales de cada borde. Las plataformas sin márgenes de área segura integrados devuelven la ventana completa y márgenes de cero.

La [extensión Safe Area](/extension-safearea) sigue siendo una alternativa para proyectos heredados o flujos de trabajo que necesiten un comportamiento adicional al de las API integradas; no es necesaria para el manejo habitual de áreas seguras en Android e iOS.

### Áreas reservadas de la pantalla {#reserved-screen-areas}

[`window.get_reserved_areas()`](/ref/window/#window.get_reserved_areas) devuelve las regiones individuales que obstruyen la ventana del juego, como los recortes de cámara y la Dynamic Island. Usa estos rectángulos al colocar contenido alrededor de obstrucciones concretas. Usa `window.get_safe_area()` cuando necesites un único rectángulo seguro para el layout y sus márgenes.

El resultado es un array de tablas con los campos `x`, `y`, `width` y `height`. Cada rectángulo se recorta a la ventana del juego. El origen está en la esquina inferior izquierda: `x` es el borde izquierdo e `y` el inferior, en píxeles de ventana que corresponden a [`window.get_size()`](/ref/window/#window.get_size). Estas coordenadas son independientes del ajuste de la GUI y de la resolución lógica de *game.project*, así que ten en cuenta las transformaciones de tu GUI antes de usarlas como posiciones de nodos.

La compatibilidad por plataforma es:

- **iOS 27.1 y posteriores:** oclusiones activas notificadas por UIKit, incluidos sus márgenes de interacción.
- **Android 9 (nivel de API 28) y posteriores:** rectángulos de recortes de pantalla.

La función devuelve una tabla vacía en plataformas y versiones de sistema operativo no compatibles, o cuando no se notifican obstrucciones para la ventana. Una tabla vacía no significa que toda la ventana sea segura para contenido importante: los pliegues, barras del sistema, teclados y regiones de gestos quedan fuera de esta API. Usa `window.get_safe_area()` para el rectángulo seguro de la plataforma.

### Actualizar las áreas después de eventos de ventana {#refreshing-areas-after-window-events}

Consulta las áreas reservadas durante la inicialización y de nuevo en cada callback [`window.WINDOW_EVENT_RESIZED`](/ref/window/#window.WINDOW_EVENT_RESIZED). Después de la primera consulta, los cambios en la geometría de las áreas reservadas también activan este evento en las plataformas compatibles, aunque el tamaño de la ventana no cambie. Cada tabla devuelta es una instantánea; las tablas guardadas no se actualizan automáticamente.

En iOS, este evento también se envía después de transiciones de orientación y cambios de márgenes del área segura. Una rotación horizontal de 180° puede mover un recorte de cámara o la Dynamic Island al otro lado sin cambiar las dimensiones de la ventana ni los márgenes del área segura. Actualiza la geometría cuando ocurra el evento aunque `data.width` y `data.height` sean iguales a sus valores anteriores.

El siguiente script mantiene actualizados ambos conjuntos de geometría:

```lua
local function refresh_screen_areas(self)
    self.safe_area = window.get_safe_area()
    self.reserved_areas = window.get_reserved_areas()
    -- Actualiza la interfaz usando el nuevo rectángulo seguro y las áreas reservadas.
end

local function on_window_event(self, event, data)
    if event == window.WINDOW_EVENT_RESIZED then
        -- Actualiza incluso cuando el ancho y el alto no hayan cambiado.
        refresh_screen_areas(self)
    end
end

function init(self)
    refresh_screen_areas(self)
    window.set_listener(on_window_event)
end

function final(self)
    window.set_listener(nil)
end
```

Solo puede registrarse un listener de eventos de ventana a la vez. Si tu juego ya tiene uno, agrega esta lógica de actualización a ese listener. Reemplazar el array guardado en cada actualización también borra los rectángulos obsoletos cuando el resultado queda vacío.


## Pautas específicas de plataforma {#platform-specific-guidelines}

### Android
Asegúrate de guardar tu [keystore](/manuals/android/#creating-a-keystore) en un lugar seguro para poder actualizar tu juego.


### Consolas {#consoles}
Guarda el bundle completo de cada versión. Necesitarás estos archivos si quieres aplicar parches al juego.


### Nintendo Switch
Integra código específico de plataforma: para Nintendo Switch hay una extensión separada con algunas funcionalidades auxiliares para la selección de usuarios, etc.

Defold para Nintendo Switch usa Vulkan como backend de gráficos. Asegúrate de probar el juego usando el [backend de gráficos Vulkan](https://github.com/defold/extension-vulkan).


### PlayStation®4
Integra código específico de plataforma: para PlayStation®4 hay una extensión separada con algunas funcionalidades auxiliares para la selección de usuarios, etc.


### HTML5
Jugar juegos web en teléfonos móviles es cada vez más popular. Intenta que el juego también funcione bien en un navegador móvil. También es importante tener en cuenta que se espera que los juegos web carguen rápido. Asegúrate de optimizar el tamaño del juego. Considera también la experiencia de carga en general para no perder jugadores innecesariamente.

En 2018 los navegadores introdujeron una política de reproducción automática para sonidos que impide que los juegos y otros contenidos web reproduzcan sonidos hasta que haya ocurrido un evento de interacción del usuario (toque, botón, gamepad, etc.). Es importante tener esto en cuenta al portar a HTML5 y comenzar a reproducir sonidos y música solo después de la primera interacción del usuario. Los intentos de reproducir sonidos antes de cualquier interacción del usuario se registrarán como error en la consola de desarrollo del navegador, pero no afectarán al juego.

Asegúrate también de pausar cualquier sonido en reproducción si el juego muestra anuncios.
