---
title: Ejecutar la app de desarrollo en un dispositivo
brief: Este manual explica cómo instalar la app de desarrollo en tu dispositivo para el desarrollo iterativo en dispositivo.
---

# La app de desarrollo móvil

La app de desarrollo te permite enviarle contenido por wifi. Esto reduce mucho el tiempo de iteración, ya que no necesitas crear un bundle e instalarlo cada vez que quieres probar tus cambios. Instala la app de desarrollo en tus dispositivos, inicia la app y luego selecciona el dispositivo como objetivo de build desde el editor.

## Instalar una app de desarrollo

Cualquier aplicación iOS o Android creada como bundle en modo Debug podrá actuar como app de desarrollo. De hecho, esta es la solución recomendada, ya que la app de desarrollo tendrá la configuración correcta del proyecto y usa las mismas [extensiones nativas](/manuals/extensions/) que el proyecto en el que estás trabajando.

Es posible crear un bundle de una variante Debug de tu proyecto sin contenido. Usa esta opción para crear una versión de tu aplicación con extensiones nativas, apta para el desarrollo iterativo como se describe en este manual.

![bundle sin contenido](images/dev-app/contentless-bundle.png)

### Instalar en iOS

Sigue las [instrucciones en el manual de iOS](/manuals/ios/#creating-an-ios-application-bundle) para crear un bundle para iOS. Asegúrate de seleccionar Debug como variante.

### Instalar en Android

Sigue las [instrucciones en el manual de Android](https://defold.com/manuals/android/#creating-an-android-application-bundle) para crear un bundle para Android.

## Iniciar tu juego

Para iniciar tu juego en tu dispositivo, la app de desarrollo y el editor deben poder conectarse a través de la misma red wifi o mediante USB (ver más abajo).

1. Asegúrate de que el editor esté iniciado y en ejecución.
2. Inicia la app de desarrollo en el dispositivo.
3. Selecciona tu dispositivo en <kbd>Project ▸ Targets</kbd> en el editor.
4. Selecciona <kbd>Project ▸ Build</kbd> para ejecutar el juego. Puede que el juego tarde un poco en iniciarse, ya que el contenido del juego se transmite al dispositivo a través de la red.
5. Mientras el juego se ejecuta, puedes usar [hot reloading](/manuals/hot-reload/) como de costumbre.

### Conectarse a un dispositivo iOS mediante USB en Windows

Al conectarte por USB en Windows a una app de desarrollo que se ejecuta en un dispositivo iOS, primero debes [instalar iTunes](https://www.apple.com/lae/itunes/download/). Cuando iTunes esté instalado, también debes [activar Personal Hotspot](https://support.apple.com/en-us/HT204023) en tu dispositivo iOS desde el menú Settings. Si ves una alerta que dice "Trust This Computer?", toca Trust. El dispositivo debería aparecer en <kbd>Project ▸ Targets</kbd> cuando la app de desarrollo esté en ejecución.

### Conectarse a un dispositivo iOS mediante USB en Linux

En Linux debes activar Personal Hotspot en tu dispositivo desde el menú Settings cuando esté conectado mediante USB. Si ves una alerta que dice "Trust This Computer?", toca Trust. El dispositivo debería aparecer en <kbd>Project ▸ Targets</kbd> cuando la app de desarrollo esté en ejecución.

### Conectarse a un dispositivo iOS mediante USB en macOS

En versiones más nuevas de iOS, el dispositivo abrirá automáticamente una nueva interfaz ethernet entre el dispositivo y la computadora cuando se conecte mediante USB en macOS. El dispositivo debería aparecer en <kbd>Project ▸ Targets</kbd> cuando la app de desarrollo esté en ejecución.

En versiones anteriores de iOS debes activar Personal Hotspot en tu dispositivo desde el menú Settings cuando esté conectado mediante USB en macOS. Si ves una alerta que dice "Trust This Computer?", toca Trust. El dispositivo debería aparecer en <kbd>Project ▸ Targets</kbd> cuando la app de desarrollo esté en ejecución.

### Conectarse a un dispositivo Android mediante USB en macOS

En macOS es posible conectarse por USB a una app de desarrollo en ejecución en un dispositivo Android cuando el dispositivo está en USB Tethering Mode. En macOS debes instalar un driver de terceros como [HoRNDIS](https://joshuawise.com/horndis#available_versions). Cuando HoRNDIS esté instalado, también debes permitir su ejecución desde la configuración de Security & Privacy. Una vez activado USB Tethering, el dispositivo aparecerá en <kbd>Project ▸ Targets</kbd> cuando la app de desarrollo esté en ejecución.

### Conectarse a un dispositivo Android mediante USB en Windows o Linux

En Windows y Linux es posible conectarse por USB a una app de desarrollo en ejecución en un dispositivo Android cuando el dispositivo está en USB Tethering Mode. Una vez activado USB Tethering, el dispositivo aparecerá en <kbd>Project ▸ Targets</kbd> cuando la app de desarrollo esté en ejecución.

## Solución de problemas

No se puede descargar la aplicación
: Asegúrate de que el UDID de tu dispositivo esté incluido en el mobile provisioning que se usó para firmar la app.

Tu dispositivo no aparece en el menú Targets
: Asegúrate de que tu dispositivo esté conectado a la misma red wifi que tu computadora. Asegúrate de que la app de desarrollo esté creada en modo Debug.

El juego no se inicia y muestra un mensaje sobre versiones incompatibles
: Esto ocurre cuando has actualizado el editor a la última versión. Debes crear e instalar una versión nueva.
