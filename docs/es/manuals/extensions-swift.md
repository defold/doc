---
title: Usar Swift en extensiones nativas para iOS y macOS
brief: Este manual explica cómo escribir en Swift el código de una extensión nativa para builds de iOS y macOS.
---

# Swift en extensiones nativas {#swift-in-native-extensions}

Muchas API de Apple, como StoreKit 2 o CryptoKit, solo se pueden usar desde Swift. En una extensión nativa (native extension) puedes incluir tus propios archivos fuente Swift junto a los de Objective-C++. El servidor de build los compila con el resto de la extensión y enlaza el resultado con el motor. Este mecanismo es independiente de los [paquetes Swift](/manuals/extensions-spm) y de [CocoaPods](/manuals/extensions-cocoapods), que proporcionan dependencias listas para usar.

El código Swift se compila para macOS (`arm64` y `x86_64`) y para iOS (dispositivos y simulador). Al crear builds para otras plataformas se ignoran los archivos Swift.


## Agregar archivos fuente Swift {#adding-swift-sources}

Coloca los archivos `.swift` en la carpeta `src` de la extensión, junto a los archivos C++ y Objective-C++.

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Guarda todos los archivos Swift en `src`. La build de macOS o iOS falla si encuentra un archivo Swift en `commonsrc` o `pluginsrc`.

Todos los archivos Swift de una extensión se compilan juntos y forman un único módulo Swift. Su nombre se toma del campo `name` de `ext.manifest`. Cada carácter que no sea una letra, un dígito o un guion bajo se sustituye por `_` (por ejemplo, `My-Extension` se convierte en `My_Extension`). El compilador usa el modo de lenguaje Swift 5.

El módulo debe tener un nombre distinto al de cualquiera de los módulos que importa el código. Una extensión llamada `StoreKit` no puede usar `import StoreKit` porque el compilador interpreta que el módulo se importa a sí mismo.


## Llamar a Swift desde Objective-C++ {#calling-swift-from-objective-c}

El punto de entrada de una extensión sigue siendo una función C++ registrada con `DM_DECLARE_EXTENSION`, por lo que necesitas al menos un archivo `.cpp` o `.mm`. Desde ese archivo puedes llamar al código Swift mediante la cabecera generada `<Module>-Swift.h`.

Desde Objective-C solo son visibles las clases, los protocolos y los métodos marcados con `@objc`. Declara las clases como `public` y haz que hereden de `NSObject`.

`src/Greeter.swift`:

```swift
import Foundation

@objc(MyExtensionGreeter)
public class Greeter: NSObject {
    @objc public func message() -> String {
        return "Hello from Swift"
    }
}
```

`src/myextension.mm`:

```cpp
#include <dmsdk/sdk.h>
#import <Foundation/Foundation.h>
#import "MyExtension-Swift.h"

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    MyExtensionGreeter* greeter = [[MyExtensionGreeter alloc] init];
    dmLogInfo("%s", [[greeter message] UTF8String]);
    return dmExtension::RESULT_OK;
}

DM_DECLARE_EXTENSION(MyExtension, "MyExtension", AppInitializeMyExtension, 0, 0, 0, 0, 0)
```

* La cabecera generada importa `Foundation`. Para los tipos de otros frameworks solo contiene declaraciones adelantadas. Importa la cabecera del framework correspondiente (por ejemplo, `UIKit`) en el archivo `.mm` antes de llamar a métodos que usen esos tipos.
* Las funciones `throws` se exponen como métodos con un parámetro `NSError **`, y las funciones `async`, como métodos que reciben un bloque que se ejecuta al finalizar la operación.
* Algunas características exclusivas de Swift, como los genéricos, las enumeraciones con valores asociados y las estructuras, no son visibles desde Objective-C. Envuélvelas en una clase `@objc`.
* Los archivos `.mm` solo se compilan para iOS y macOS. Si la extensión contiene únicamente archivos `.mm` y `.swift`, la build falla en otras plataformas con el error `Extension has no source!`. Para que la extensión se compile también en otras plataformas, coloca `DM_DECLARE_EXTENSION` en un archivo `.cpp`. Desde ese archivo, llama al código del archivo `.mm` dentro de un bloque de compilación condicional que compruebe `DM_PLATFORM_IOS` o `DM_PLATFORM_OSX`.


## Llamar a Objective-C desde Swift {#calling-objective-c-from-swift}

Para usar declaraciones de Objective-C o C desde Swift, agrega a la carpeta `src` una cabecera puente (bridging header) llamada `<Module>-Bridging-Header.h`, por ejemplo `src/MyExtension-Bridging-Header.h`.

```cpp
#import "mynative.h"
```

Si existe esa cabecera, se importa automáticamente en el módulo Swift. Las cabeceras que incluya se buscan en la carpeta `include` de la extensión y en las carpetas indicadas en `additionalSwiftIncludePaths` (consulta las opciones del compilador más abajo).

Para usar frameworks de Apple como `Foundation`, `UIKit` o `StoreKit` desde Swift, impórtalos con una instrucción `import` normal. Los frameworks enumerados en `frameworks` y `weakFrameworks` del archivo `ext.manifest` se enlazan como de costumbre. La mayoría de los frameworks del sistema se enlazan automáticamente cuando el código Swift los importa.


## Usar paquetes Swift desde Swift {#using-swift-packages-from-swift}

El código Swift de la extensión puede usar los productos de los [paquetes Swift](/manuals/extensions-spm) declarados en `SwiftPackages.json`. Importa el módulo en un archivo Swift.

```swift
import Foundation
import Sentry

@objc(MyExtensionCrashReporter)
public class CrashReporter: NSObject {
    @objc public func start(dsn: String) {
        SentrySDK.start { options in
            options.dsn = dsn
        }
    }
}
```

Puedes importar las cabeceras Objective-C de un paquete en la cabecera puente igual que en un archivo `.mm`.

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

Declara el paquete en el archivo `SwiftPackages.json` de la extensión que lo usa. El servidor de build compila primero los paquetes y después el código Swift de la extensión. Si un paquete requiere una versión del sistema operativo posterior a la mínima que admite el motor, indica la versión que necesita en el campo `minVersion` de `SwiftPackages.json`. El código Swift de la extensión también se compilará para esa versión. En una extensión de Defold, el código Swift no puede usar dependencias de CocoaPods directamente. Úsalas desde el archivo Objective-C++ y pasa al código Swift lo que necesite.


## Opciones del compilador {#compiler-options}

Configura las opciones del compilador Swift en el archivo `ext.manifest`, dentro del mismo `context` que las opciones del compilador C++.

```yaml
name: MyExtension

platforms:
    ios:
        context:
            defines: ["MY_DEFINE"]
            swiftFlags: ["-strict-concurrency=complete"]
            additionalSwiftIncludePaths: ["include/vendor/headers"]
            additionalFrameworkSearchPaths: ["lib/ios/vendor/frameworks"]
    osx:
        context:
            defines: ["MY_DEFINE"]
```

* `defines` - Las definiciones del preprocesador de C++ se pasan a Swift como nombres de condiciones de compilación. Así puedes usar `#if MY_DEFINE` en Swift. Si una definición tiene un valor, como en `MY_DEFINE=1`, ese valor se descarta porque Swift solo admite nombres.
* `swiftFlags` - Flags adicionales para el compilador Swift. Escribe cada flag y cada valor en un elemento separado de la lista. Si usas un flag que no está en la lista de permitidos, la build falla con el error `Invalid flag - 'swiftFlags'`. Si un valor contiene espacios en blanco, una barra inversa o sintaxis de plantilla, o si hace referencia a un archivo de respuesta, la build falla con el error `invalid 'swiftFlags' value`. Se admiten los siguientes flags.
  * `-enable-upcoming-feature <Feature>` - Activa una característica prevista para una versión futura del lenguaje, por ejemplo `["-enable-upcoming-feature", "ExistentialAny"]`.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize` y `-Onone` - Establecen el nivel de optimización. El valor predeterminado es `-O`.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - Carpetas en las que el compilador Swift busca cabeceras y módulos, además de la carpeta `include` de la extensión.
* `additionalFrameworkSearchPaths` - Carpetas en las que se buscan frameworks, además de la carpeta `lib/<platform>` de la extensión. Estas rutas se usan al compilar los archivos fuente de la extensión con Swift, C++ u Objective-C++. El enlazador también las usa.

Las rutas son relativas a la carpeta de la extensión, deben permanecer dentro de ella y solo pueden contener letras, dígitos y los caracteres `._+-/`. De la extensión solo se envían al servidor de build las carpetas `include`, `src`, `commonsrc`, `pluginsrc`, `lib/<platform>`, `manifests/<platform>` y `res/<platform>`. Las rutas deben apuntar al interior de alguna de ellas. Los archivos de otras carpetas, como una carpeta `vendor` en la raíz de la extensión, no están disponibles durante la build.

Las claves de Swift de la plataforma `ios` se aplican tanto a los dispositivos como al simulador. Un servidor de build anterior a la incorporación de Swift rechaza esas claves con el error `Manifest context variable unsupported`. La build del proyecto seguirá fallando hasta que actualices tanto la versión de Defold como el servidor de build.


## Versiones mínimas del sistema operativo {#minimum-os-versions}

El entorno de ejecución de Swift (runtime) forma parte de todas las versiones de iOS y macOS que admite Defold. El código Swift se compila para la versión mínima de iOS o macOS de la build y la aplicación usa el entorno de ejecución de Swift que proporciona el sistema operativo. Antes de llamar a una API introducida después de esa versión mínima, comprueba su disponibilidad con `#available`.

Algunos componentes del entorno de ejecución solo se incluyen en versiones más recientes del sistema operativo. Por ejemplo, `MutableSpan` y los tipos relacionados están disponibles en el sistema a partir de iOS 26 y macOS 26. Si la versión mínima es anterior y tu código Swift o un framework dinámico de un paquete usa una de estas características, la aplicación puede necesitar una biblioteca adicional para ejecutarse en dispositivos con el sistema anterior. El servidor de build se encarga de ello automáticamente. Al igual que Xcode, detecta de qué bibliotecas dependen el motor y las bibliotecas dinámicas incluidas con él, y agrega esas dependencias a la aplicación. En iOS las coloca en la carpeta `Frameworks` de la aplicación y las firma junto con el resto del código.

La versión mínima del sistema operativo para una build es la que admite el motor y depende de la versión de Defold y del servidor de build. Con `minVersion` en `SwiftPackages.json` puedes elevar ese mínimo para los paquetes, el código Swift y el enlazado del motor, como se describe en el [manual de Swift Package Manager](/manuals/extensions-spm). No puedes reducirlo.


## Limitaciones {#limitations}

* La extensión sigue necesitando un archivo C++ u Objective-C++ con `DM_DECLARE_EXTENSION`. El código Swift no puede registrar la extensión ni acceder a la API C++ del SDK de Defold (`dmsdk`). Usa esa API desde el archivo Objective-C++. En la cabecera puente puedes incluir las cabeceras de `dmsdk` compatibles con C, como `dmsdk/dlib/hash.h`. Si la extensión contiene únicamente archivos `.swift`, el enlazado falla con un error de símbolo no definido que indica el nombre de la extensión.
* El código Swift no puede usar dependencias de CocoaPods directamente. Úsalas desde el archivo Objective-C++ y pasa al código Swift lo que necesite.
* Solo se admite el modo de lenguaje Swift 5. La interoperabilidad con C++ está desactivada.
* Los archivos fuente Swift se admiten a partir de Defold 1.14.2. Si el servidor de build usa un SDK anterior, la build falla con el error `Swift sources are not supported by this Defold SDK version`.
* Al generar el artefacto `library` (`--build-artifacts library` en [Bob](/manuals/bob)) no se compilan los archivos fuente Swift. Por eso, si un archivo Objective-C++ importa `<Module>-Swift.h`, su compilación falla al generar ese artefacto.


## Resolución de problemas {#troubleshooting}

`no such module 'Name'`
: El módulo no es un producto de un paquete declarado en `SwiftPackages.json`. Comprueba que `products` incluya un producto que proporcione el módulo, como se describe en el [manual de Swift Package Manager](/manuals/extensions-spm).

`Swift sources are only supported in the 'src' folder`
: Mueve los archivos `.swift` a la carpeta `src` de la extensión.

`'MyExtension-Swift.h' file not found`
: El nombre del módulo se genera a partir de `name` en `ext.manifest`. Comprueba el nombre en la línea `#import`.

`unknown type name 'MyExtensionGreeter'`
: La clase no aparece en la cabecera generada. Comprueba que esté marcada con `public` y `@objc`, que herede de `NSObject` y que el archivo `.mm` use el nombre indicado en `@objc(...)`.

`cannot find 'AppStore' in scope` junto con `file 'A.swift' is part of module 'StoreKit'; ignoring import`
: La extensión tiene el mismo nombre que uno de los módulos que importa. Cambia el nombre de la extensión en `ext.manifest`.

`Undefined symbols ... _MyExtension`
: Falta `DM_DECLARE_EXTENSION` en la extensión. Agrega un archivo `.mm` que registre la extensión como se describe más arriba.

`Invalid flag - 'swiftFlags'`
: El flag no está en la lista de permitidos. Elimínalo o usa uno de los flags de la lista.

`invalid 'swiftFlags' value`
: El valor contiene espacios en blanco, una barra inversa o sintaxis de plantilla, o hace referencia a un archivo de respuesta. Escribe cada flag y cada valor en un elemento separado de la lista.
