---
title: Desarrollo Defold para la plataforma macOS
brief: Este manual describe cómo crear y ejecutar aplicaciones Defold en macOS
---

# Desarrollo en macOS

Desarrollar aplicaciones Defold para la plataforma macOS es un proceso directo con muy pocas consideraciones a tener en cuenta.

## Configuración del proyecto

La configuración de aplicaciones específica de macOS se hace desde la [sección macOS](/manuals/project-settings/#macos) del archivo de configuración *game.project*.

## Icono de la aplicación

El icono de la aplicación usado para un juego de macOS debe estar en formato `.icns`. Puedes crear fácilmente un archivo `.icns` a partir de un conjunto de archivos `.png` reunidos como un `.iconset`. Sigue las [instrucciones oficiales para crear un archivo `.icns`](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html). Resumen breve de los pasos:

* Crea una carpeta para los iconos, por ejemplo `game.iconset`
* Copia los archivos de icono a la carpeta creada:

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* Convierte la carpeta `.iconset` a un archivo `.icns` usando la herramienta de línea de comando `iconutil`:

```
iconutil -c icns -o game.icns game.iconset
```

## Publicar tu aplicación
Puedes publicar tu aplicación en la Mac App Store, usando una tienda o portal de terceros como Steam o itch.io, o por tu cuenta a través de un sitio web. Antes de publicar tu aplicación, debes prepararla para el envío. Los siguientes pasos son necesarios independientemente de cómo pretendas distribuir la aplicación:

1. Asegúrate de que cualquiera pueda ejecutar tu juego agregando permisos de ejecución (el valor predeterminado es que solo el propietario del archivo tenga permisos de ejecución):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

2. Crea un archivo de entitlements que especifique los permisos requeridos por tu juego. Para la mayoría de los juegos, los siguientes permisos son suficientes:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - Indica si la app puede crear memoria escribible y ejecutable usando la bandera `MAP_JIT`
  * `com.apple.security.cs.allow-unsigned-executable-memory` - Indica si la app puede crear memoria escribible y ejecutable sin las restricciones impuestas por el uso de la bandera `MAP_JIT`
  * `com.apple.security.cs.allow-dyld-environment-variables` - Indica si la app puede verse afectada por variables de ambiente del enlazador dinámico, que puedes usar para inyectar código en el proceso de tu app

Algunas aplicaciones también pueden necesitar entitlements adicionales. La extensión Steamworks necesita este entitlement extra:

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

    * `com.apple.security.cs.disable-library-validation` - Indica si la app puede cargar plug-ins o frameworks arbitrarios, sin requerir firma de código.

Todos los entitlements que se pueden conceder a una aplicación se listan en la [documentación oficial para desarrolladores de Apple](https://developer.apple.com/documentation/bundleresources/entitlements).

3. Firma tu juego usando `codesign`:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Publicar fuera de la Mac App Store
Apple requiere que todo el software distribuido fuera de la Mac App Store sea notarizado por Apple para ejecutarse por defecto en macOS Catalina. Consulta la [documentación oficial](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow) para aprender cómo agregar notarización a un entorno de build con scripts fuera de Xcode. Resumen breve de los pasos:

1. Sigue los pasos anteriores para agregar permisos y firmar la aplicación.

2. Comprime y sube tu juego para notarización usando `altool`.

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

3. Comprueba el estado de tu envío usando el UUID de solicitud devuelto por la llamada a `altool --notarize-app`:

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

4. Espera hasta que el estado sea `success` y adjunta el ticket de notarización al juego:

```
$ xcrun stapler staple "Game.app"
```

5. Tu juego ya está listo para su distribución.

## Publicar en la Mac App Store
El proceso para publicar en la Mac App Store está bien documentado en la [documentación de Apple Developer](https://developer.apple.com/macos/submit/). Asegúrate de agregar permisos y firmar la aplicación como se describió arriba antes de enviarla.

Nota: El juego no necesita estar notarizado al publicarse en la Mac App Store.

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)
