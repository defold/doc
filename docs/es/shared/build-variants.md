## Variantes de build

Cuando creas un bundle de un juego, debes elegir qué tipo de motor quieres usar. Tienes tres opciones básicas:

  * Debug
  * Release
  * Headless

Estas diferentes versiones también se denominan `Build variants`.

::: sidenote
Cuando eliges <kbd>Project ▸ Build</kbd>, siempre obtendrás la versión de depuración.
:::


### Debug

Este tipo de ejecutable se usa normalmente durante el desarrollo de un juego, ya que incluye varias funcionalidades útiles de depuración:

* Profiler - Se usa para recopilar contadores de rendimiento y uso. Aprende cómo usar el profiler en el [manual de profiling](/manuals/profiling/).
* Logging - El motor registrará información del sistema, advertencias y errores cuando el logging esté habilitado. El motor también generará logs desde la función Lua `print()` y desde el logging de extensiones nativas que use `dmLogInfo()`, `dmLogError()` y similares. Aprende cómo leer estos logs en el [manual de logs del juego y del sistema](https://defold.com/manuals/debugging-game-and-system-logs/).
* Hot reload - Hot-reload es una funcionalidad potente que permite a un desarrollador recargar recursos mientras el juego se está ejecutando. Aprende cómo usarla en el [manual de Hot-Reload](https://defold.com/manuals/hot-reload/).
* Servicios del motor - Es posible conectarse a una versión de depuración de un juego e interactuar con ella mediante varios puertos TCP abiertos y servicios. Los servicios incluyen la funcionalidad hot-reload, acceso remoto a logs y el profiler mencionado antes, además de otros servicios para interactuar de forma remota con el motor. Aprende más sobre los servicios del motor [en la documentación para desarrolladores](https://github.com/defold/defold/blob/dev/engine/docs/DEBUG_PORTS_AND_SERVICES.md).


### Release

Esta variante tiene las funcionalidades de depuración deshabilitadas. Esta opción debe elegirse cuando el juego esté listo para publicarse en la tienda de aplicaciones o compartirse con jugadores por otros medios. No se recomienda publicar un juego con las funcionalidades de depuración habilitadas por varias razones:

* Las funcionalidades de depuración ocupan un poco de espacio en el binario, y [es una buena práctica intentar mantener el tamaño del binario de un juego publicado lo más pequeño posible](https://defold.com/manuals/optimization/#optimize-application-size).
* Las funcionalidades de depuración también consumen un poco de tiempo de CPU. Esto puede afectar el rendimiento del juego si un usuario tiene hardware de gama baja. En teléfonos móviles, el aumento del uso de CPU también contribuirá al calentamiento y al consumo de batería.
* Las funcionalidades de depuración pueden exponer información sobre el juego que no está destinada a los jugadores, ya sea desde una perspectiva de seguridad, trampas o fraude.


### Headless

Este ejecutable se ejecuta sin gráficos ni sonido. Esto significa que puedes ejecutar las pruebas unitarias o de humo del juego en un servidor de CI, o incluso usarlo como servidor de juego en la nube.
