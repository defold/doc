---
title: Usar dependencias de Swift Package Manager en builds de iOS y macOS
brief: Este manual explica cómo usar Swift Package Manager para resolver dependencias en builds de iOS y macOS.
---

# Swift Package Manager

[Swift Package Manager](https://www.swift.org/documentation/package-manager/) es el gestor de dependencias integrado en Swift y Xcode. Muchos SDK de iOS y macOS se distribuyen como paquetes Swift, y algunos ya no se publican como CocoaPods. Defold no usa Xcode para crear la build del motor, pero el servidor de build lo usa para descargar y compilar los paquetes Swift de los que depende una extensión. El resultado se enlaza con el motor de la misma forma que las [dependencias de CocoaPods](/manuals/extensions-cocoapods).

CocoaPods y los paquetes Swift pueden usarse en el mismo proyecto e incluso en la misma extensión.


## Declarar dependencias {#declaring-dependencies}

Las extensiones nativas pueden incluir un archivo `SwiftPackages.json` en las carpetas `manifests/ios` y `manifests/osx` para especificar los paquetes Swift de los que dependen. Ejemplo:

```json
{
  "platform": "ios",
  "minVersion": "15.0",
  "packages": [
    {
      "url": "https://github.com/firebase/firebase-ios-sdk.git",
      "version": "12.16.0",
      "products": ["FirebaseCore", "FirebaseInstallations"]
    }
  ]
}
```

El archivo usa JSON normal. No tienes que escribir un archivo `Package.swift`: el servidor de build lo genera a partir de los archivos `SwiftPackages.json` de todas las extensiones.

El archivo contiene los siguientes campos:

* `platform` - Obligatorio. `"ios"` en `manifests/ios/SwiftPackages.json` y `"osx"` en `manifests/osx/SwiftPackages.json`.
* `minVersion` - Opcional. La versión mínima de iOS o macOS para la que se compilan los paquetes, por ejemplo `"15.0"`. Se usa el valor más alto entre todas las extensiones y la versión mínima admitida por el motor, tanto al compilar los paquetes como al enlazar el motor.
* `wrapperType` - Opcional. `"static"` (predeterminado) o `"dynamic"`. Consulta [Enlazado estático y dinámico](#static-and-dynamic-linking) más abajo.
* `packages` - Obligatorio. Una lista de paquetes. Cada paquete tiene los siguientes campos:
  * `url` - La URL `https://` del repositorio git del paquete. No se aceptan URL con credenciales, un puerto personalizado o parámetros de consulta, ni URL `ssh`, por lo que el repositorio debe ser de acceso público.
  * `products` - Los productos del paquete que se enlazarán con el motor. Son los productos de biblioteca enumerados en la sección `products` del archivo `Package.swift` del paquete. El nombre de un producto no tiene por qué coincidir con el nombre del paquete ni con el del módulo que importas.
  * Exactamente un requisito de versión:
    * `version` - Esta versión exacta, por ejemplo `"12.16.0"`.
    * `from` - Esta versión o una posterior con la misma versión mayor. Por ejemplo, `"9.0.0"` resuelve a la versión `9.x.x` más reciente.
    * `branch` - El commit más reciente de una rama, por ejemplo `"main"`.
    * `revision` - Un commit concreto, indicado mediante su hash completo de 40 caracteres.

El servidor de build recopila los archivos `SwiftPackages.json` de todas las extensiones y los usa para resolver todas las dependencias, incluidas las de los propios paquetes, e incluirlas al compilar el código nativo.


## Usar paquetes desde el código de una extensión {#using-packages-from-extension-code}

Las cabeceras de los productos están disponibles para el código fuente de la extensión. Úsalas desde archivos fuente Objective-C++ (`.mm`). Este ejemplo inicia el SDK de [Sentry](https://github.com/getsentry/sentry-cocoa) al arrancar la aplicación:

`manifests/ios/SwiftPackages.json`:

```json
{
  "platform": "ios",
  "minVersion": "15.0",
  "packages": [
    {
      "url": "https://github.com/getsentry/sentry-cocoa.git",
      "from": "9.0.0",
      "products": ["Sentry"]
    }
  ]
}
```

`src/myextension.mm`:

```cpp
#include <dmsdk/sdk.h>

#if defined(DM_PLATFORM_IOS)
#import <UIKit/UIKit.h>
#import <Sentry/Sentry.h>
#import <Sentry/Sentry-Swift.h>
#endif

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
#if defined(DM_PLATFORM_IOS)
    [SentrySDK startWithConfigureOptions:^(SentryOptions* options) {
        options.dsn = @"https://examplePublicKey@o0.ingest.sentry.io/0";
    }];
#endif
    return dmExtension::RESULT_OK;
}
```

* Las cabeceras Objective-C se importan como `#import <Module/Header.h>`, donde `Module` es el nombre del módulo que las proporciona.
* Las clases implementadas en Swift se declaran en la cabecera generada `<Module/Module-Swift.h>`. Solo contiene las clases y los métodos que el módulo expone a Objective-C (marcados con `@objc` en Swift). Importa `UIKit` (o `AppKit` en macOS) antes de ella, ya que la cabecera generada usa sus tipos.


## Dependencias de varias extensiones {#dependencies-of-several-extensions}

Cuando varias extensiones de un proyecto usan paquetes Swift, todos sus archivos `SwiftPackages.json` de la plataforma se combinan en un único grafo de paquetes:

* Los paquetes con la misma URL se fusionan, y sus productos solicitados se combinan.
* Un paquete compartido por varias extensiones debe tener el mismo requisito de versión en todas ellas. Los requisitos diferentes, por ejemplo `"version": "12.16.0"` en una extensión y `"from": "12.0.0"` en otra, hacen fallar la build con un error `Conflicting requirements for Swift package`.
* Se usa el valor `minVersion` más alto.
* Todas las extensiones que definan `wrapperType` deben usar el mismo valor.

Un proyecto también puede combinar extensiones que usan CocoaPods con extensiones que usan paquetes Swift. Ambas se resuelven y enlazan con el motor. Sin embargo, un mismo SDK no debe proceder de ambos: si una extensión obtiene Firebase desde un `Podfile` y otra desde un `SwiftPackages.json`, el enlazado del motor falla con errores de símbolos duplicados. Las extensiones que comparten un SDK deben usar el mismo gestor de dependencias.


## Fijar las versiones de los paquetes {#locking-package-versions}

Cuando la build termina correctamente, el servidor devuelve un archivo `Package.resolved` que enumera la versión y el commit exactos de cada paquete del grafo, incluidas sus dependencias. Se coloca en la carpeta de build del proyecto, por ejemplo `build/arm64-ios/Package.resolved`.

Copia este archivo en la extensión, junto a `SwiftPackages.json` (por ejemplo `manifests/ios/Package.resolved`), para fijar las versiones de los paquetes. El servidor de build usa entonces esas versiones mientras cumplan los requisitos de `SwiftPackages.json`. Esto también acelera la build: sin un archivo `Package.resolved`, el servidor descubre las dependencias de los paquetes paso a paso, lo que puede llevar mucho tiempo para paquetes con muchas dependencias.

Si varias extensiones incluyen un archivo `Package.resolved` para la misma plataforma, solo se usa uno de ellos.


## Enlazado estático y dinámico {#static-and-dynamic-linking}

De forma predeterminada, todos los paquetes Swift se combinan en una única biblioteca estática que se enlaza con el ejecutable del motor.

Algunos SDK no pueden combinarse en una biblioteca estática, y el enlazado del motor falla con errores de símbolos duplicados. En ese caso, establece `"wrapperType": "dynamic"` en `SwiftPackages.json`. Los paquetes se compilan entonces como un framework dinámico que se incorpora al bundle de la aplicación.


## Recursos y manifiestos de privacidad {#resources-and-privacy-manifests}

Los bundles de recursos y los manifiestos de privacidad (`PrivacyInfo.xcprivacy`) de los paquetes se incluyen en el bundle de la aplicación de la misma forma que con las dependencias de CocoaPods.


## Migrar desde CocoaPods {#migrating-from-cocoapods}

Muchos SDK se publican tanto como pods como paquetes Swift. Para cambiar una extensión de un archivo `Podfile` a un archivo `SwiftPackages.json`:

1. Busca el repositorio git del paquete Swift en la documentación del SDK. A menudo es el mismo repositorio que el del pod.
2. Busca los nombres de los productos en el archivo `Package.swift` del paquete. Los nombres de los pods y de los productos suelen ser diferentes.
3. Sustituye el `Podfile` por un archivo `SwiftPackages.json`. La versión de `platform :ios` del `Podfile` pasa a ser `minVersion`.
4. Comprueba que las líneas `#import` de la extensión siguen correspondiendo a los nombres de los módulos de los productos.

Por ejemplo, este `Podfile`:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

se convierte en este `SwiftPackages.json`:

```json
{
  "platform": "ios",
  "minVersion": "12.0",
  "packages": [
    {
      "url": "https://github.com/facebook/facebook-ios-sdk.git",
      "version": "17.0.0",
      "products": ["FacebookCore", "FacebookLogin", "FacebookShare", "FacebookGamingServices"]
    }
  ]
}
```

En este caso, los módulos conservan sus nombres, por lo que `#import <FBSDKCoreKit/FBSDKCoreKit.h>` funciona con ambos.


## Limitaciones {#limitations}

* Solo se admiten repositorios de paquetes de acceso público mediante `https://`. No se admiten registros de paquetes Swift.
* Los archivos `Package.swift` y los plugins de los paquetes se ejecutan sin acceso a la red en el servidor de build. El propio servidor descarga los paquetes y sus frameworks binarios antes de compilar los paquetes.
* Compilar paquetes que contienen catálogos de assets (`.xcassets`) para iOS requiere un servidor de build con Xcode 27 o posterior. Con una versión anterior de Xcode, la build falla con un error que identifica esos paquetes.
* Los archivos `SwiftPackages.json` de un proyecto pueden declarar como máximo 32 paquetes y 64 productos por plataforma.


## Resolución de problemas {#troubleshooting}

`'Module/Header.h' file not found` o símbolos no definidos
: Comprueba que los `products` de `SwiftPackages.json` sean nombres de productos de `Package.swift` y que la cabecera pertenezca a uno de ellos. Un servidor de build que no admita Swift Package Manager ignora `SwiftPackages.json`, y la compilación o el enlazado de la extensión falla de la misma forma.

`The Swift package graph did not resolve within the ... time budget`
: Los paquetes tienen demasiadas dependencias para descubrirlas sin un archivo de bloqueo. Agrega un archivo `Package.resolved` junto a `SwiftPackages.json`, como se describe en [Fijar las versiones de los paquetes](#locking-package-versions). Como la build no terminó, crea el archivo localmente, por ejemplo agregando los mismos paquetes a un proyecto de Xcode. Xcode lo guarda en `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`.


## Servidor de build local {#local-build-server}

El servidor de build de macOS compila los paquetes Swift. Para usarlos con un [servidor de build local](/manuals/extender-local-setup), este necesita una instalación completa de Xcode (las Command Line Tools por sí solas no bastan), [XcodeGen](https://github.com/yonaskolb/XcodeGen) y la compatibilidad con Swift Package Manager activada mediante el ajuste `extender.spm.enabled`. Consulta la [documentación del servidor de build en GitHub](https://github.com/defold/extender) para más información.
