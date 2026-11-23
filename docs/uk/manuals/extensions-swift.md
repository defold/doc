---
title: Використання Swift у нативних розширеннях для iOS і macOS
brief: У цьому посібнику описано, як писати код нативного розширення мовою Swift для збірок iOS і macOS.
---

# Swift у нативних розширеннях {#swift-in-native-extensions}

Багато API Apple, зокрема StoreKit 2 і CryptoKit, доступні лише зі Swift. Нативне розширення (native extension) може містити власні файли вихідного коду Swift поряд із файлами Objective-C++. Сервер збирання компілює їх разом із рештою коду розширення й компонує результат із рушієм. Готові залежності можна підключати окремо за допомогою [пакетів Swift](/manuals/extensions-spm) і [CocoaPods](/manuals/extensions-cocoapods).

Код Swift компілюється для macOS (`arm64` і `x86_64`) та iOS (для пристроїв і симулятора). Під час збирання для інших платформ сервер ігнорує файли Swift.


## Додавання файлів вихідного коду Swift {#adding-swift-sources}

Помістіть файли `.swift` у папку `src` розширення поряд із файлами C++ та Objective-C++.

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Зберігайте всі файли Swift у `src`. Якщо в `commonsrc` або `pluginsrc` є файл Swift, збирання для macOS або iOS завершиться помилкою.

Усі файли Swift одного розширення компілюються разом в один модуль Swift. Назва модуля береться з поля `name` у `ext.manifest`. Кожен символ, окрім літер, цифр і знака підкреслення, замінюється на `_` (наприклад, `My-Extension` стає `My_Extension`). Компілятор працює в режимі мови Swift 5.

Назва модуля має відрізнятися від назв модулів, які імпортує код. У розширенні з назвою `StoreKit` не можна написати `import StoreKit`, оскільки компілятор сприйме це як спробу імпортувати поточний модуль.


## Виклик коду Swift з Objective-C++ {#calling-swift-from-objective-c}

Точкою входу розширення, як і раніше, є функція C++, зареєстрована за допомогою `DM_DECLARE_EXTENSION`. Тому розширенню потрібен хоча б один файл `.cpp` або `.mm`. Із цього файлу можна викликати код Swift через згенерований заголовок `<Module>-Swift.h`.

В Objective-C доступні лише класи, протоколи й методи з атрибутом `@objc`. Позначте класи як `public` і зробіть їх нащадками `NSObject`.

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

* Згенерований заголовок імпортує `Foundation`. Для типів з інших фреймворків він містить лише попередні оголошення. Імпортуйте заголовок відповідного фреймворку (наприклад, `UIKit`) у файл `.mm`, перш ніж викликати методи, що використовують ці типи.
* Функції `throws` доступні як методи з параметром `NSError **`, а функції `async` — як методи з обробником завершення.
* В Objective-C недоступні можливості, властиві лише Swift, зокрема узагальнення, переліки з асоційованими значеннями та структури. Для доступу до них створіть клас-обгортку з атрибутом `@objc`.
* Файли `.mm` компілюються лише для iOS і macOS. Тому збирання розширення, яке містить тільки файли `.mm` і `.swift`, для інших платформ завершується помилкою `Extension has no source!`. Щоб збирати розширення й для інших платформ, помістіть `DM_DECLARE_EXTENSION` у файл `.cpp`. З нього викликайте код із файлу `.mm` у блоці умовної компіляції з перевіркою `DM_PLATFORM_IOS` або `DM_PLATFORM_OSX`.


## Виклик коду Objective-C зі Swift {#calling-objective-c-from-swift}

Щоб використовувати оголошення Objective-C або C у Swift, додайте до папки `src` сполучний заголовок (bridging header) із назвою `<Module>-Bridging-Header.h`, наприклад `src/MyExtension-Bridging-Header.h`.

```cpp
#import "mynative.h"
```

Якщо такий заголовок існує, він автоматично імпортується в модуль Swift. Заголовки, які він включає, компілятор шукає в папці `include` розширення та в папках, зазначених у `additionalSwiftIncludePaths` (див. нижче).

Для імпорту фреймворків Apple, як-от `Foundation`, `UIKit` або `StoreKit`, у Swift використовуйте звичайну інструкцію `import`. Фреймворки, перелічені в `frameworks` і `weakFrameworks` у файлі `ext.manifest`, компонуються як зазвичай. Більшість системних фреймворків компонуються автоматично, коли їх імпортує код Swift.


## Використання пакетів Swift у коді Swift {#using-swift-packages-from-swift}

У коді Swift розширення доступні продукти [пакетів Swift](/manuals/extensions-spm), які це розширення оголошує у `SwiftPackages.json`. Імпортуйте модуль у файлі Swift.

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

Заголовки Objective-C з пакета можна імпортувати в сполучному заголовку так само, як у файлі `.mm`.

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

Оголосіть пакет у файлі `SwiftPackages.json` того розширення, яке його використовує. Сервер збирання спочатку збирає пакети, а потім код Swift розширення. Якщо пакету потрібна новіша версія ОС, ніж мінімальна версія, яку підтримує рушій, задайте її в полі `minVersion` файлу `SwiftPackages.json`. Тоді код Swift розширення також збиратиметься для цієї версії. Використання залежностей CocoaPods безпосередньо в коді Swift не підтримується. Працюйте з ними у файлі Objective-C++ і передавайте в код Swift потрібні дані.


## Параметри компілятора {#compiler-options}

Параметри компілятора Swift задаються у файлі `ext.manifest` у тому самому розділі `context`, що й параметри компілятора C++.

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

* `defines` — визначення препроцесора C++ передаються у Swift як імена для умовної компіляції, тож у Swift працює `#if MY_DEFINE`. Якщо визначення має значення, як у `MY_DEFINE=1`, це значення відкидається, оскільки Swift підтримує лише імена.
* `swiftFlags` — додаткові прапорці компілятора Swift. Записуйте кожен прапорець і кожне значення окремим елементом списку. Сервер приймає лише дозволені прапорці. З будь-яким іншим прапорцем збирання завершується помилкою `Invalid flag - 'swiftFlags'`. Якщо значення містить пробільний символ, зворотну скісну риску чи синтаксис шаблону або вказує на файл аргументів (response file), з’явиться помилка `invalid 'swiftFlags' value`. Дозволено такі прапорці.
  * `-enable-upcoming-feature <Feature>` — вмикає можливість із майбутньої версії мови, наприклад `["-enable-upcoming-feature", "ExistentialAny"]`.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize` і `-Onone` — рівень оптимізації. За замовчуванням використовується `-O`.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` — папки, у яких компілятор Swift шукає заголовки й модулі, окрім папки `include` розширення.
* `additionalFrameworkSearchPaths` — папки, у яких виконується пошук фреймворків, окрім папки `lib/<platform>` розширення. Ці шляхи використовують компілятор Swift, компілятор C++ та Objective-C++ під час компіляції вихідного коду розширення, а також компонувальник.

Вказуйте шляхи відносно папки розширення. Вони мають залишатися в її межах і можуть містити лише літери, цифри та символи `._+-/`. На сервер збирання надсилаються лише папки розширення `include`, `src`, `commonsrc`, `pluginsrc`, `lib/<platform>`, `manifests/<platform>` і `res/<platform>`, тому шляхи мають вести до однієї з них або до її підпапки. Файли з інших папок, наприклад із папки `vendor` у корені розширення, під час збирання недоступні.

Ключі Swift для платформи `ios` застосовуються і до пристроїв, і до симулятора. Старіший сервер збирання без підтримки Swift відхилить їх із помилкою `Manifest context variable unsupported`. Щоб знову зібрати проєкт, оновіть і версію Defold, і сервер збирання.


## Мінімальні версії ОС {#minimum-os-versions}

Середовище виконання Swift входить до складу всіх версій iOS і macOS, які підтримує Defold. Код Swift збирається для мінімальної версії iOS або macOS, заданої для збірки, а застосунок використовує середовище виконання Swift зі складу операційної системи. Перш ніж викликати API, що з’явився в новішій версії ОС, виконайте перевірку `#available`.

Деякі частини середовища виконання входять до складу ОС лише з певної версії. Наприклад, `MutableSpan` і пов’язані типи з’явилися в iOS 26 і macOS 26. Якщо мінімальна версія старіша, а ваш код Swift або динамічний фреймворк пакета використовує таку можливість, для запуску застосунку на пристроях зі старішою ОС може знадобитися додаткова бібліотека. Сервер збирання, як і Xcode, автоматично знаходить бібліотеки, які використовують рушій та вбудовані разом із ним динамічні бібліотеки, і додає їх до застосунку. На iOS він поміщає їх у папку `Frameworks` застосунку й підписує разом із рештою його коду.

Мінімальна версія ОС для збірки — це найстаріша версія, яку підтримує рушій. Її визначають версія Defold і сервер збирання. Значення `minVersion` у файлі `SwiftPackages.json` може підвищити її для пакетів, коду Swift і компонування рушія, як описано в [посібнику зі Swift Package Manager](/manuals/extensions-spm). Знизити її не можна.


## Обмеження {#limitations}

* Розширенню й надалі потрібен файл C++ або Objective-C++ із `DM_DECLARE_EXTENSION`. Зареєструвати розширення з коду Swift неможливо. API C++ із Defold SDK (`dmsdk`) також недоступний у Swift, тому викликайте його з файлу Objective-C++. У сполучний заголовок можна включати сумісні з C заголовки `dmsdk`, наприклад `dmsdk/dlib/hash.h`. Якщо розширення містить лише файли `.swift`, під час компонування виникає помилка про невизначений символ із назвою розширення.
* Використання залежностей CocoaPods безпосередньо в коді Swift не підтримується. Працюйте з ними у файлі Objective-C++ і передавайте в код Swift потрібні дані.
* Підтримується лише режим мови Swift 5. Взаємодію з C++ не ввімкнено.
* Файли вихідного коду Swift підтримуються починаючи з Defold 1.14.2. На сервері збирання зі старішим SDK збирання завершується помилкою `Swift sources are not supported by this Defold SDK version`.
* Під час збирання артефакту `library` (`--build-artifacts library` у [Bob](/manuals/bob)) вихідний код Swift не компілюється. Тому файл Objective-C++, який імпортує `<Module>-Swift.h`, у такій збірці не скомпілюється.


## Усунення несправностей {#troubleshooting}

`no such module 'Name'`
: Модуль не входить до продуктів пакета, оголошеного у `SwiftPackages.json`. Переконайтеся, що `products` містить продукт, який надає потрібний модуль, як описано в [посібнику зі Swift Package Manager](/manuals/extensions-spm).

`Swift sources are only supported in the 'src' folder`
: Перемістіть файли `.swift` у папку `src` розширення.

`'MyExtension-Swift.h' file not found`
: Назва модуля утворюється зі значення `name` у `ext.manifest`. Перевірте назву в рядку `#import`.

`unknown type name 'MyExtensionGreeter'`
: Клас відсутній у згенерованому заголовку. Перевірте, чи позначено його як `public` і `@objc`, чи успадковує він `NSObject` і чи використано у файлі `.mm` назву з `@objc(...)`.

`cannot find 'AppStore' in scope` разом із `file 'A.swift' is part of module 'StoreKit'; ignoring import`
: Назва розширення збігається з назвою модуля, який воно імпортує. Перейменуйте розширення у `ext.manifest`.

`Undefined symbols ... _MyExtension`
: У розширенні немає `DM_DECLARE_EXTENSION`. Додайте файл `.mm`, який реєструє розширення, як описано вище.

`Invalid flag - 'swiftFlags'`
: Прапорця немає в списку дозволених. Вилучіть його або використайте один із прапорців зі списку.

`invalid 'swiftFlags' value`
: Значення містить пробільний символ, зворотну скісну риску чи синтаксис шаблону або вказує на файл аргументів. Запишіть кожен прапорець і кожне значення окремим елементом списку.
