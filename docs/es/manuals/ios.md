---
title: Desarrollo de Defold para la plataforma iOS
brief: Este manual explica cómo crear y ejecutar juegos y apps en dispositivos iOS en Defold.
---

# Desarrollo en iOS

::: sidenote
Crear un bundle de un juego para iOS solo está disponible en la versión para Mac del editor Defold.
:::

iOS requiere que _cualquier_ app que crees y quieras ejecutar en tu teléfono o tablet _deba_ estar firmada con un certificado emitido por Apple y un perfil provisional. Este manual explica los pasos necesarios para crear un bundle de tu juego para iOS. Durante el desarrollo, suele ser preferible ejecutar tu juego mediante la [app de desarrollo](/manuals/dev-app), ya que te permite recargar contenido y código en caliente directamente en tu dispositivo.

## Proceso de firmado de código de Apple

La seguridad asociada con las apps iOS consta de varios componentes. Puedes acceder a las herramientas necesarias registrándote en el [iOS Developer Program de Apple](https://developer.apple.com/programs/). Cuando te hayas inscrito, ve al [Developer Member Center de Apple](https://developer.apple.com/membercenter/index.action).

![Apple Member Center](images/ios/apple_member_center.png)

La sección *Certificates, Identifiers & Profiles* contiene todas las herramientas que necesitas. Desde aquí puedes crear, eliminar y editar:

Certificates
: Certificados criptográficos emitidos por Apple que te identifican como desarrollador. Puedes crear certificados de desarrollo o de producción. Los certificados de desarrollo te permiten probar ciertas funcionalidades, como el mecanismo de compras dentro de la app, en un entorno de pruebas sandbox. Los certificados de producción se usan para firmar la app final que se subirá a la App Store. Necesitas un certificado para firmar apps antes de poder instalarlas en tu dispositivo para probarlas.

Identifiers
: Identificadores para varios usos. Es posible registrar identificadores wildcard (por ejemplo, `some.prefix.*`) que pueden usarse con varias apps. Los App IDs pueden contener información de Application Services, por ejemplo si la app activa la integración con Passbook, Game Center, etc. Esos App IDs no pueden ser identificadores wildcard. Para que los Application Services funcionen, el *identificador de bundle* de tu aplicación debe coincidir con el identificador del App ID.

Devices
: Cada dispositivo de desarrollo debe registrarse con su UDID (Unique Device IDentifier, consulta más abajo).

Provisioning Profiles
: Los perfiles provisionales asocian certificados con App IDs y una lista de dispositivos. Indican qué app, de qué desarrollador, puede estar en qué dispositivos.

Al firmar tus juegos y apps en Defold, necesitas un certificado válido y un perfil provisional válido.

::: sidenote
Algunas de las cosas que puedes hacer en la página de inicio de Member Center también puedes realizarlas desde el entorno de desarrollo Xcode, si lo tienes instalado.
:::

Identificador de dispositivo (UDID)
: El UDID de un dispositivo iOS puede encontrarse conectando el dispositivo a una computadora por wifi o cable. Abre Xcode y selecciona <kbd>Window ▸ Devices and Simulators</kbd>. El número de serie y el identificador se muestran cuando seleccionas tu dispositivo.

  ![dispositivos xcode](images/ios/xcode_devices.png)

  Si no tienes Xcode instalado, puedes encontrar el identificador en iTunes. Haz click en el símbolo de dispositivos y selecciona tu dispositivo.

  ![dispositivos itunes](images/ios/itunes_devices.png)

  1. En la página *Summary*, localiza el *Serial Number*.
  2. Haz click una vez en *Serial Number* para que el campo cambie a *UDID*. Si haces click varias veces, aparecerán varios datos del dispositivo. Sigue haciendo click hasta que se muestre *UDID*.
  3. Haz click derecho en la cadena larga del UDID y selecciona <kbd>Copy</kbd> para copiar el identificador al portapapeles, de modo que puedas pegarlo fácilmente en el campo UDID al registrar el dispositivo en Developer Member Center de Apple.

## Desarrollar con una cuenta gratuita de desarrollador de Apple

Desde Xcode 7, cualquiera puede instalar Xcode y desarrollar en dispositivo de forma gratuita. No tienes que registrarte en el iOS Developer Program. En su lugar, Xcode emitirá automáticamente un certificado para ti como desarrollador (válido durante 1 año) y un perfil provisional para tu app (válido durante una semana) en tu dispositivo específico.

1. Conecta tu dispositivo.
2. Instala Xcode.
3. Agrega una cuenta nueva a Xcode e inicia sesión con tu Apple ID.
4. Crea un proyecto nuevo. La opción más simple, "Single View App", funciona bien.
5. Selecciona tu "Team" (creado automáticamente para ti) y dale a la app un identificador de bundle.

::: important
Anota el identificador de bundle, ya que debes usar el mismo identificador de bundle en tu proyecto Defold.
:::

6. Asegúrate de que Xcode haya creado un *Provisioning Profile* y un *Signing Certificate* para la app.

   ![](images/ios/xcode_certificates.png)

7. Crea la build de la app en tu dispositivo. La primera vez, Xcode te pedirá activar Developer mode y preparará el dispositivo con soporte para depurador. Esto puede tardar un poco.
8. Cuando hayas verificado que la app funciona, búscala en tu disco. Puedes ver la ubicación de la build en el Build report del "Report Navigator".

   ![](images/ios/app_location.png)

9. Localiza la app, haz click derecho sobre ella y selecciona <kbd>Show Package Contents</kbd>.

   ![](images/ios/app_contents.png)

10. Copia el archivo "embedded.mobileprovision" a algún lugar de tu unidad donde puedas encontrarlo.

   ![](images/ios/free_provisioning.png)

Este archivo de perfil provisional puede usarse junto con tu identidad de firmado de código para firmar apps en Defold durante una semana.

Cuando el perfil provisional expire, debes crear la build de la app otra vez en Xcode y obtener un nuevo archivo de perfil provisional temporal como se describió arriba.

## Crear un bundle de aplicación iOS {#creating-an-ios-application-bundle}

Cuando tengas la identidad de firmado de código y el perfil provisional, estarás listo para crear desde el editor un bundle de aplicación independiente para tu juego. Simplemente selecciona <kbd>Project ▸ Bundle... ▸ iOS Application...</kbd> en el menú.

![Firmar bundle iOS](images/ios/sign_bundle.png)

Selecciona tu identidad de firmado de código y busca tu archivo de mobile provisioning. Selecciona la arquitectura de dispositivo `arm64-ios` y, cuando sea necesario, la arquitectura de simulador `x86_64-ios`, así como la variante (Debug o Release). Opcionalmente puedes desmarcar la casilla `Sign application` para omitir el proceso de firmado y firmar manualmente en una etapa posterior.

::: important
**Debes** desmarcar la casilla `Sign application` al probar tu juego en el simulador de iOS. Podrás instalar la aplicación, pero no arrancará.
:::

Pulsa *Create Bundle* y se te pedirá que especifiques en qué lugar de tu computadora se creará el bundle.

![bundle de aplicación ipa iOS](images/ios/ipa_file.png){.left}

Puedes especificar qué icono usar para la app, el storyboard de pantalla de lanzamiento, etc. en el archivo de configuración del proyecto *game.project*, en la [sección iOS](/manuals/project-settings/#ios).

### Info.plist personalizado y descubrimiento de targets locales

El `Info.plist` integrado de iOS contiene el servicio Bonjour y la descripción de uso de la red local necesarios para el descubrimiento automático de targets del editor en builds que no son release. Un `Info.plist` personalizado sustituye ese manifiesto base integrado. Si se usa un manifiesto personalizado para una build debug y necesitas descubrimiento de targets, profiling, hot reload o streaming de logs por la red local, incluye estas entradas:

```xml
{{^variant_release}}
<key>NSBonjourServices</key>
<array>
    <string>_defold._tcp</string>
</array>
<key>NSLocalNetworkUsageDescription</key>
<string>Discover Defold targets on the local network.</string>
{{/variant_release}}
```

La condición Mustache excluye las entradas de descubrimiento de los bundles release. iOS muestra al usuario el texto de descripción de uso, que puede modificarse o localizarse. Elimina la condición solo si la propia aplicación release usa el mismo servicio Bonjour y la funcionalidad de red local.

:[Build Variants](../shared/build-variants.md)

## Instalar y ejecutar un bundle en un iPhone conectado

Puedes instalar y ejecutar el bundle creado usando las casillas "Install on connected device" y "Launch installed app" del editor en el diálogo Bundle:

![Instalar y ejecutar bundle iOS](images/ios/install_and_launch.png)

Para que esta funcionalidad funcione, necesitas tener instalada la herramienta de línea de comando [ios-deploy](https://github.com/ios-control/ios-deploy). La forma más simple de instalarla es usando Homebrew:
```
$ brew install ios-deploy
```

Si el editor no puede detectar la ubicación de instalación de la herramienta ios-deploy, tendrás que especificarla en [Preferences](/manuals/editor-preferences/#tools).

### Crear un storyboard {#creating-a-storyboard}

Creas un archivo storyboard usando Xcode. Inicia Xcode y crea un proyecto nuevo. Selecciona iOS y Single View App:

![Crear proyecto](images/ios/xcode_create_project.png)

Haz click en Next y continúa para configurar tu proyecto. Ingresa un Product Name:

![Configuración del proyecto](images/ios/xcode_storyboard_create_project_settings.png)

Haz click en Create para finalizar el proceso. Tu proyecto ya está creado y podemos continuar para crear el storyboard:

![La vista del proyecto](images/ios/xcode_storyboard_project_view.png)

Arrastra y suelta una imagen para importarla al proyecto. Luego selecciona `Assets.xcassets` y suelta la imagen en `Assets.xcassets`:

![Agregar imagen](images/ios/xcode_storyboard_add_image.png)

Abre `LaunchScreen.storyboard` y haz click en el botón de suma (<kbd>+</kbd>). Escribe "imageview" en el diálogo para encontrar el componente ImageView.

![Agregar vista de imagen](images/ios/xcode_storyboard_add_imageview.png)

Arrastra el componente Image View al storyboard:

![Agregar al storyboard](images/ios/xcode_storyboard_add_imageview_to_storyboard.png)

Selecciona la imagen que agregaste previamente a `Assets.xcassets` desde el desplegable Image:

![](images/ios/xcode_storyboard_select_image.png)

Posiciona la imagen y realiza cualquier otro ajuste que necesites, quizá agregando un Label u otro elemento de interfaz. Cuando termines, establece el esquema activo en **Any iOS Device (arm64)** (o **Generic iOS Device**) y selecciona **Product ▸ Build**. Defold admite iOS 15.0 y versiones posteriores en dispositivos de 64 bits, así que mantén el deployment target en 15.0 o posterior. Espera a que finalice el proceso de build.

Si usas imágenes en el storyboard, no se incluirán automáticamente en tu `LaunchScreen.storyboardc`. Usa el campo `Bundle Resources` en *game.project* para incluir recursos.
Por ejemplo, crea la carpeta `LaunchScreen` en el proyecto Defold y una carpeta `ios` dentro (la carpeta `ios` es necesaria para incluir estos archivos solo en bundles de iOS), luego coloca tus archivos en `LaunchScreen/ios/`. Agrega esta ruta en `Bundle Resources`.

![](images/ios/bundle_res.png)

El último paso es copiar el archivo compilado `LaunchScreen.storyboardc` a tu proyecto Defold. Abre Finder en la siguiente ubicación y copia el archivo `LaunchScreen.storyboardc` a tu proyecto Defold:

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Intermediates.noindex/YOUR-PRODUCT-NAME.build/Debug-iphonesimulator/YOUR-PRODUCT-NAME.build/Base.lproj/LaunchScreen.storyboardc

::: sidenote
El usuario del foro Sergey Lerg preparó [un video tutorial que muestra el proceso](https://www.youtube.com/watch?v=6jU8wGp3OwA&feature=emb_logo).
:::

Una vez que tengas el archivo storyboard, puedes referenciarlo desde *game.project*.


### Crear un asset catalog de iconos

Usar un asset catalog es la forma preferida por Apple de gestionar los iconos de tu aplicación. De hecho, es la única forma de proporcionar el icono usado en la ficha de la App Store. Creas un asset catalog de la misma manera que un storyboard, usando Xcode. Inicia Xcode y crea un proyecto nuevo. Selecciona iOS y Single View App:

![Crear proyecto](images/ios/xcode_create_project.png)

Haz click en Next y continúa para configurar tu proyecto. Ingresa un Product Name:

![Configuración del proyecto](images/ios/xcode_icons_create_project_settings.png)

Haz click en Create para finalizar el proceso. Tu proyecto ya está creado y podemos continuar para crear el asset catalog:

![La vista del proyecto](images/ios/xcode_icons_project_view.png)

Arrastra y suelta imágenes en las casillas vacías que representan los distintos tamaños de icono admitidos:

![Agregar iconos](images/ios/xcode_icons_add_icons.png)

::: sidenote
No agregues iconos para Notifications, Settings ni Spotlight.
:::

Cuando termines, establece el esquema activo en "Build -> Any iOS Device (arm64)" (o "Generic iOS Device") y selecciona <kbd>Product</kbd> -> <kbd>Build</kbd>. Espera a que finalice el proceso de build.

::: sidenote
Asegúrate de crear la build para "Any iOS Device (arm64)" o "Generic iOS Device"; de lo contrario, obtendrás el error `ERROR ITMS-90704` al subir tu build.
:::

![Crear build del proyecto](images/ios/xcode_icons_build.png)

El último paso es copiar el archivo compilado `Assets.car` a tu proyecto Defold. Abre Finder en la siguiente ubicación y copia el archivo `Assets.car` a tu proyecto Defold:

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Products/Debug-iphoneos/Icons.app/Assets.car

Una vez que tengas el archivo asset catalog, puedes referenciarlo a él y a los iconos desde *game.project*:

![Agregar icono y asset catalog a game.project](images/ios/defold_icons_game_project.png)

::: sidenote
No es necesario referenciar el icono de la App Store desde *game.project*. Se extrae automáticamente del archivo `Assets.car` al subir a iTunes Connect.
:::


## Instalar un bundle de aplicación iOS

El editor escribe un archivo *.ipa*, que es un bundle de aplicación iOS. Para instalar el archivo en tu dispositivo, puedes usar una de las siguientes herramientas:

* Xcode mediante la ventana "Devices and Simulators"
* La herramienta de línea de comando [`ios-deploy`](https://github.com/ios-control/ios-deploy)
* [`Apple Configurator 2`](https://apps.apple.com/us/app/apple-configurator-2/) desde el macOS App Store
* iTunes

También puedes usar la herramienta de línea de comando `xcrun simctl` para trabajar con los simuladores de iOS disponibles mediante Xcode:

```
# mostrar una lista de dispositivos disponibles
xcrun simctl list

# arrancar un simulador de iPhone X
xcrun simctl boot "iPhone X"

# instalar your.app en un simulador arrancado
xcrun simctl install booted your.app

# iniciar el simulador
open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
```

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)


## Información de cumplimiento de exportación

Cuando envíes tu juego a la App Store, se te pedirá que proporciones información de cumplimiento de exportación con respecto al uso de cifrado en tu juego. [Apple explica por qué esto es necesario](https://developer.apple.com/documentation/security/complying_with_encryption_export_regulations):

"Cuando envías tu app a TestFlight o a la App Store, subes tu app a un servidor en Estados Unidos. Si distribuyes tu app fuera de EE. UU. o Canadá, tu app está sujeta a las leyes de exportación de EE. UU., sin importar dónde tenga sede tu entidad legal. Si tu app usa, accede, contiene, implementa o incorpora cifrado, esto se considera una exportación de software de cifrado, lo que significa que tu app está sujeta a los requisitos de cumplimiento de exportación de EE. UU., así como a los requisitos de cumplimiento de importación de los países donde distribuyes tu app."

El motor de videojuegos Defold usa cifrado para los siguientes propósitos:

* Realizar llamadas a través de canales seguros (por ejemplo, HTTPS y SSL)
* Protección contra copia del código Lua (para evitar duplicación)

Estos usos de cifrado en el motor Defold están exentos de los requisitos de documentación de cumplimiento de exportación según las leyes de Estados Unidos y de la Unión Europea. La mayoría de los proyectos Defold seguirán exentos, pero agregar otros métodos criptográficos puede cambiar este estado. Es tu responsabilidad asegurarte de que tu proyecto cumpla con los requisitos de estas leyes y las reglas de la App Store. Consulta el [Export Compliance Overview](https://help.apple.com/app-store-connect/#/dev88f5c7bf9) de Apple para obtener más información.

Si crees que tu proyecto está exento, define la clave [`ITSAppUsesNonExemptEncryption`](https://developer.apple.com/documentation/bundleresources/information-property-list/itsappusesnonexemptencryption) como `False` en el `Info.plist` del proyecto. Consulta [Manifiestos de aplicación](/manuals/extensions-manifest-merge-tool) para obtener más detalles.

## FAQ
:[iOS FAQ](../shared/ios-faq.md)
