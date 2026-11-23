---
title: Использование Swift в нативных расширениях для iOS и macOS
brief: В этом руководстве описано, как писать код нативного расширения на Swift для сборок под iOS и macOS.
---

# Swift в нативных расширениях {#swift-in-native-extensions}

Многие API Apple, например StoreKit 2 и CryptoKit, доступны только из Swift. Нативное расширение может содержать собственные исходные файлы на Swift наряду с файлами Objective-C++. Сервер сборки компилирует их вместе с остальным кодом расширения и компонует результат с движком. Готовые зависимости подключаются отдельно, через [пакеты Swift](/manuals/extensions-spm) и [CocoaPods](/manuals/extensions-cocoapods).

Код на Swift компилируется для macOS (`arm64` и `x86_64`) и для iOS (устройства и симулятор). При сборке для других платформ файлы Swift игнорируются.


## Добавление исходных файлов Swift {#adding-swift-sources}

Поместите файлы `.swift` в папку `src` расширения рядом с файлами C++ и Objective-C++.

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Храните все файлы Swift в `src`. Если в папке `commonsrc` или `pluginsrc` обнаружится файл Swift, сборка для macOS или iOS завершится ошибкой.

Все файлы Swift одного расширения компилируются в один модуль Swift. Его имя берётся из поля `name` файла `ext.manifest`. Все символы, кроме букв, цифр и подчёркиваний, заменяются на `_` (например, `My-Extension` становится `My_Extension`). Компилятор работает в режиме языка Swift 5.

Имя модуля должно отличаться от имён модулей, которые импортирует его код. Например, в расширении с именем `StoreKit` нельзя написать `import StoreKit`, поскольку компилятор сочтёт это импортом самого модуля.


## Вызов Swift из Objective-C++ {#calling-swift-from-objective-c}

Точкой входа расширения по-прежнему служит функция C++, зарегистрированная с помощью `DM_DECLARE_EXTENSION`. Поэтому в расширении должен быть хотя бы один файл `.cpp` или `.mm`. Из этого файла можно вызывать код на Swift через сгенерированный заголовочный файл `<Module>-Swift.h`.

Из Objective-C видны только классы, протоколы и методы, помеченные атрибутом `@objc`. Объявляйте классы как `public` и наследуйте их от `NSObject`.

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

* Сгенерированный заголовок импортирует `Foundation`. Для типов из других фреймворков в нём есть только предварительные объявления. Перед вызовом методов, использующих такие типы, импортируйте в файл `.mm` заголовок соответствующего фреймворка, например `UIKit`.
* Функции с `throws` доступны как методы с параметром `NSError **`, а функции с `async` — как методы с обработчиком завершения.
* Из Objective-C недоступны специфичные для Swift конструкции, например обобщения, перечисления с ассоциированными значениями и структуры. Чтобы работать с ними из Objective-C, оберните их в класс с атрибутом `@objc`.
* Файлы `.mm` компилируются только для iOS и macOS. Если в расширении есть только файлы `.mm` и `.swift`, сборка для других платформ завершится ошибкой `Extension has no source!`. Чтобы расширение собиралось и для других платформ, поместите `DM_DECLARE_EXTENSION` в файл `.cpp`. В нём вызывайте код из файла `.mm` только внутри блока условной компиляции с проверкой `DM_PLATFORM_IOS` или `DM_PLATFORM_OSX`.


## Вызов Objective-C из Swift {#calling-objective-c-from-swift}

Чтобы использовать в Swift объявления из Objective-C или C, добавьте в папку `src` связующий заголовок (bridging header) с именем `<Module>-Bridging-Header.h`. Например, файл `src/MyExtension-Bridging-Header.h` может содержать такую строку:

```cpp
#import "mynative.h"
```

Если связующий заголовок существует, он автоматически импортируется в модуль Swift. Компилятор ищет подключаемые им заголовки в папке `include` расширения и в папках, перечисленных в `additionalSwiftIncludePaths` (см. ниже).

Фреймворки Apple, например `Foundation`, `UIKit` и `StoreKit`, импортируются в Swift обычной директивой `import`. Фреймворки, перечисленные в `frameworks` и `weakFrameworks` файла `ext.manifest`, подключаются при компоновке как обычно. Большинство системных фреймворков подключаются автоматически, если их импортирует код на Swift.


## Использование пакетов Swift в коде на Swift {#using-swift-packages-from-swift}

Код расширения на Swift может использовать продукты [пакетов Swift](/manuals/extensions-spm), объявленных в файле `SwiftPackages.json` этого расширения. Импортируйте нужный модуль в файле Swift.

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

Заголовки Objective-C из пакета можно импортировать в связующем заголовке так же, как в файле `.mm`.

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

Объявите пакет в файле `SwiftPackages.json` того расширения, которое его использует. Сервер сборки сначала собирает пакеты, а затем код расширения на Swift. Если пакету требуется версия ОС новее минимальной версии, которую поддерживает движок, укажите требуемую версию в поле `minVersion` файла `SwiftPackages.json`. Тогда код расширения на Swift также будет собран для этой версии. Использование зависимостей CocoaPods из Swift не поддерживается. Обращайтесь к ним из файла Objective-C++ и передавайте в код на Swift всё необходимое.


## Параметры компилятора {#compiler-options}

Параметры компилятора Swift задаются в файле `ext.manifest` в том же разделе `context`, что и параметры компилятора C++.

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

* `defines` — макросы, заданные для C++, передаются в Swift как имена для условной компиляции. Поэтому условие `#if MY_DEFINE` работает и в Swift. Если у макроса есть значение, как в `MY_DEFINE=1`, оно отбрасывается, поскольку Swift поддерживает только имена.
* `swiftFlags` — дополнительные флаги компилятора Swift. Указывайте каждый флаг и каждое значение отдельным элементом списка. Если флага нет в списке разрешённых, сборка завершается ошибкой `Invalid flag - 'swiftFlags'`. Ошибка `invalid 'swiftFlags' value` возникает, если значение содержит пробельный символ, обратную косую черту или шаблонное выражение либо указывает на файл аргументов компилятора (response file). Допускаются следующие флаги:
  * `-enable-upcoming-feature <Feature>` — включает возможность, запланированную для будущей версии языка, например `["-enable-upcoming-feature", "ExistentialAny"]`.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize` и `-Onone` — уровень оптимизации. По умолчанию используется `-O`.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` — папки, в которых компилятор Swift ищет заголовки и модули, помимо папки `include` самого расширения.
* `additionalFrameworkSearchPaths` — папки, в которых выполняется поиск фреймворков, помимо папки `lib/<platform>` расширения. Эти пути используются при компиляции исходных файлов расширения на Swift, C++ и Objective-C++, а также при компоновке.

Пути задаются относительно папки расширения, не могут выходить за её пределы и могут содержать только буквы, цифры и символы `._+-/`. На сервер сборки передаются только папки расширения `include`, `src`, `commonsrc`, `pluginsrc`, `lib/<platform>`, `manifests/<platform>` и `res/<platform>`, поэтому пути должны вести в одну из них. Файлы из других папок, например из папки `vendor` в корне расширения, недоступны при сборке.

Параметры Swift для платформы `ios` действуют и для устройств, и для симулятора. Если версия сервера сборки выпущена до появления поддержки Swift, сервер отклонит эти параметры с ошибкой `Manifest context variable unsupported`. Проект удастся собрать после обновления Defold и сервера сборки.


## Минимальные версии ОС {#minimum-os-versions}

Среда выполнения Swift входит в состав всех версий iOS и macOS, поддерживаемых Defold. Код на Swift компилируется для минимальной версии iOS или macOS, заданной для сборки, а приложение использует среду выполнения Swift из операционной системы. Перед обращением к API, появившимся позже этой минимальной версии, проверяйте их доступность с помощью `#available`.

Некоторые компоненты среды выполнения входят в состав ОС только начиная с более поздних версий. Например, тип `MutableSpan` и связанные с ним типы появились в iOS 26 и macOS 26. Если минимальная версия ОС ниже, а ваш код на Swift или динамический фреймворк из пакета использует подобную возможность, для запуска приложения на устройствах с более старой ОС может потребоваться дополнительная библиотека. Добавлять её вручную не нужно. Как и Xcode, сервер сборки определяет, какие библиотеки нужны движку и поставляемым вместе с ним динамическим библиотекам, и добавляет их в приложение. В iOS они помещаются в папку `Frameworks` приложения и подписываются вместе с остальным кодом.

Минимальная версия ОС для сборки определяется тем, какую версию поддерживает движок. Это зависит от версии Defold и сервера сборки. Параметр `minVersion` в файле `SwiftPackages.json` позволяет повысить минимальную версию для сборки пакетов, компиляции кода на Swift и компоновки движка, как описано в [руководстве по Swift Package Manager](/manuals/extensions-spm). Понизить минимальную версию нельзя.


## Ограничения {#limitations}

* Расширению по-прежнему нужен файл C++ или Objective-C++ с `DM_DECLARE_EXTENSION`. Зарегистрировать расширение из Swift нельзя. API C++ из комплекта Defold SDK (`dmsdk`) также недоступен из Swift, поэтому вызывайте его из файла Objective-C++. Совместимые с C заголовки `dmsdk`, например `dmsdk/dlib/hash.h`, можно подключать в связующем заголовке. Если в расширении есть только файлы `.swift`, компоновщик сообщит о неопределённом символе с именем расширения.
* Использование зависимостей CocoaPods из Swift не поддерживается. Обращайтесь к ним из файла Objective-C++ и передавайте в код на Swift всё необходимое.
* Поддерживается только режим языка Swift 5. Взаимодействие с C++ отключено.
* Поддержка исходных файлов Swift появилась в Defold 1.14.2. На сервере сборки с более ранней версией SDK сборка завершается ошибкой `Swift sources are not supported by this Defold SDK version`.
* При сборке артефакта `library` (`--build-artifacts library` в [Bob](/manuals/bob)) исходные файлы Swift не компилируются, поэтому файл Objective-C++, импортирующий `<Module>-Swift.h`, при такой сборке не скомпилируется.


## Устранение неполадок {#troubleshooting}

`no such module 'Name'`
: Ни один из продуктов пакетов, объявленных в `SwiftPackages.json`, не предоставляет этот модуль. Убедитесь, что в `products` указан продукт, предоставляющий модуль, как описано в [руководстве по Swift Package Manager](/manuals/extensions-spm).

`Swift sources are only supported in the 'src' folder`
: Переместите файлы `.swift` в папку `src` расширения.

`'MyExtension-Swift.h' file not found`
: Имя модуля формируется из поля `name` файла `ext.manifest`. Проверьте имя в строке `#import`.

`unknown type name 'MyExtensionGreeter'`
: Класс отсутствует в сгенерированном заголовке. Убедитесь, что класс помечен `public` и `@objc` и наследуется от `NSObject`, а в файле `.mm` используется имя, заданное в `@objc(...)`.

`cannot find 'AppStore' in scope` вместе с `file 'A.swift' is part of module 'StoreKit'; ignoring import`
: Имя расширения совпадает с именем одного из импортируемых им модулей. Переименуйте расширение в `ext.manifest`.

`Undefined symbols ... _MyExtension`
: В расширении отсутствует `DM_DECLARE_EXTENSION`. Добавьте файл `.mm`, который регистрирует расширение, как описано выше.

`Invalid flag - 'swiftFlags'`
: Флага нет в списке разрешённых. Удалите его или используйте один из перечисленных флагов.

`invalid 'swiftFlags' value`
: Значение содержит пробельный символ, обратную косую черту или шаблонное выражение либо указывает на файл аргументов компилятора. Запишите каждый флаг и каждое значение отдельным элементом списка.
