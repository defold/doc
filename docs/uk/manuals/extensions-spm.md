---
title: Використання залежностей Swift Package Manager у збірках iOS і macOS
brief: Цей посібник пояснює, як використовувати Swift Package Manager для розв’язання залежностей у збірках iOS і macOS.
---

# Swift Package Manager {#swift-package-manager}

[Swift Package Manager](https://www.swift.org/documentation/package-manager/) — менеджер залежностей, вбудований у Swift і Xcode. Багато SDK для iOS і macOS поширюються як пакети Swift, а деякі вже не публікуються як CocoaPods. Defold не використовує Xcode для збирання рушія, але сервер збирання використовує Xcode, щоб завантажити й зібрати пакети Swift, від яких залежить розширення. Результат потім компонується з рушієм так само, як [залежності CocoaPods](/manuals/extensions-cocoapods).

CocoaPods і пакети Swift можна використовувати в одному проєкті й навіть в одному розширенні.

## Оголошення залежностей {#declaring-dependencies}

Нативні розширення можуть містити файл `SwiftPackages.json` у папках `manifests/ios` і `manifests/osx`, щоб указати пакети Swift, від яких залежить розширення. Приклад:

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

Це звичайний файл JSON. Вам не потрібно самостійно писати `Package.swift`: сервер збирання генерує його з файлів `SwiftPackages.json` усіх розширень.

Файл містить такі поля:

* `platform` — обов’язкове. `"ios"` у `manifests/ios/SwiftPackages.json` і `"osx"` у `manifests/osx/SwiftPackages.json`.
* `minVersion` — необов’язкове. Мінімальна версія iOS або macOS, для якої збираються пакети, наприклад `"15.0"`. Як для збирання пакетів, так і для компонування рушія використовується найбільше значення серед усіх розширень і мінімальної версії, яку підтримує рушій.
* `wrapperType` — необов’язкове. `"static"` (за замовчуванням) або `"dynamic"`. Див. [Статичне й динамічне компонування](#static-and-dynamic-linking) нижче.
* `packages` — обов’язкове. Список пакетів. Кожен пакет має такі поля:
  * `url` — URL `https://` Git-репозиторію пакета. URL з обліковими даними, нестандартним портом або рядком запиту, а також URL `ssh` не приймаються, тому репозиторій має бути загальнодоступним.
  * `products` — продукти пакета, які потрібно скомпонувати з рушієм. Це бібліотечні продукти, перелічені в розділі `products` файлу `Package.swift` пакета. Назва продукту не обов’язково збігається з назвою пакета або модуля, який ви імпортуєте.
  * Рівно одна вимога до версії:
    * `version` — саме ця версія, наприклад `"12.16.0"`.
    * `from` — ця або пізніша версія з тим самим основним номером. Наприклад, `"9.0.0"` вибирає останній випуск `9.x.x`.
    * `branch` — останній коміт гілки, наприклад `"main"`.
    * `revision` — певний коміт, заданий повним 40-символьним хешем коміту.

Сервер збирання збирає файли `SwiftPackages.json` усіх розширень, розв’язує всі залежності, зокрема залежності самих пакетів, і включає їх під час збирання нативного коду.

## Використання пакетів у коді розширення {#using-packages-from-extension-code}

Заголовки продуктів доступні вихідному коду розширення. Використовуйте їх із вихідних файлів Objective-C++ (`.mm`). Цей приклад запускає SDK [Sentry](https://github.com/getsentry/sentry-cocoa) під час запуску застосунку:

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

* Заголовки Objective-C імпортуються як `#import <Module/Header.h>`, де `Module` — назва модуля, який їх надає.
* Класи, реалізовані у Swift, оголошуються в згенерованому заголовку `<Module/Module-Swift.h>`. Він містить лише класи й методи, які модуль надає Objective-C (позначені `@objc` у Swift). Імпортуйте `UIKit` (або `AppKit` на macOS) перед ним, оскільки згенерований заголовок використовує їхні типи.

## Залежності кількох розширень {#dependencies-of-several-extensions}

Коли кілька розширень проєкту використовують пакети Swift, усі їхні файли `SwiftPackages.json` для платформи об’єднуються в один граф пакетів:

* Пакети з однаковим URL об’єднуються разом із запитаними продуктами.
* Пакет, спільний для кількох розширень, повинен мати однакову вимогу до версії в усіх них. Різні вимоги, наприклад `"version": "12.16.0"` в одному розширенні й `"from": "12.0.0"` в іншому, спричиняють помилку збирання `Conflicting requirements for Swift package`.
* Використовується найбільше значення `minVersion`.
* Усі розширення, що задають `wrapperType`, повинні задавати однакове значення.

Проєкт також може поєднувати розширення з CocoaPods і розширення з пакетами Swift. Обидва типи залежностей розв’язуються й компонуються з рушієм. Проте той самий SDK не має надходити з обох джерел: якщо одне розширення отримує Firebase з `Podfile`, а інше — зі `SwiftPackages.json`, компонування рушія завершується помилками дублювання символів. Розширення зі спільним SDK мають використовувати той самий менеджер залежностей.

## Фіксація версій пакетів {#locking-package-versions}

Після успішного збирання сервер повертає файл `Package.resolved` із точними версією й комітом кожного пакета в графі, зокрема залежностей пакетів. Він розміщується в папці збирання проєкту, наприклад `build/arm64-ios/Package.resolved`.

Скопіюйте цей файл до розширення поруч зі `SwiftPackages.json` (наприклад, `manifests/ios/Package.resolved`), щоб зафіксувати версії пакетів. Сервер збирання використовуватиме зафіксовані версії, доки вони відповідають вимогам `SwiftPackages.json`. Це також пришвидшує збирання: без `Package.resolved` сервер поступово виявляє залежності пакетів, що може тривати довго для пакетів із багатьма залежностями.

Якщо кілька розширень містять `Package.resolved` для тієї самої платформи, використовується лише один із них.

## Статичне й динамічне компонування {#static-and-dynamic-linking}

За замовчуванням усі пакети Swift об’єднуються в одну статичну бібліотеку, яка компонується з виконуваним файлом рушія.

Деякі SDK неможливо об’єднати в статичну бібліотеку, і тоді компонування рушія завершується помилками дублювання символів. У цьому випадку задайте `"wrapperType": "dynamic"` у `SwiftPackages.json`. Пакети будуть зібрані в динамічний фреймворк, вбудований у пакет застосунку.

## Ресурси й маніфести конфіденційності {#resources-and-privacy-manifests}

Пакети ресурсів і маніфести конфіденційності (`PrivacyInfo.xcprivacy`) пакетів включаються до пакета застосунку так само, як для залежностей CocoaPods.

## Перехід із CocoaPods {#migrating-from-cocoapods}

Багато SDK публікуються і як pod, і як пакет Swift. Щоб перевести розширення з `Podfile` на `SwiftPackages.json`:

1. Знайдіть Git-репозиторій пакета Swift у документації SDK. Часто це той самий репозиторій, що й для pod.
2. Знайдіть назви продуктів у файлі `Package.swift` пакета. Назви pod і продуктів часто відрізняються.
3. Замініть `Podfile` файлом `SwiftPackages.json`. Версія `platform :ios` із `Podfile` стає `minVersion`.
4. Переконайтеся, що рядки `#import` розширення й далі відповідають назвам модулів продуктів.

Наприклад, такий `Podfile`:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

перетворюється на такий `SwiftPackages.json`:

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

У цьому випадку модулі зберігають свої назви, тож `#import <FBSDKCoreKit/FBSDKCoreKit.h>` працює в обох варіантах.

## Обмеження {#limitations}

* Підтримуються лише репозиторії пакетів, загальнодоступні через `https://`. Реєстри пакетів Swift не підтримуються.
* Файли `Package.swift` і плагіни пакетів виконуються на сервері збирання без доступу до мережі. Сервер сам завантажує пакети й їхні двійкові фреймворки перед збиранням пакетів.
* Збирання пакетів, що містять каталоги ресурсів (`.xcassets`) для iOS, потребує сервера збирання з Xcode 27 або новішим. Зі старішою версією Xcode збирання завершується помилкою, яка називає ці пакети.
* Файли `SwiftPackages.json` проєкту можуть оголошувати щонайбільше 32 пакети й 64 продукти на платформу.

## Усунення несправностей {#troubleshooting}

`'Module/Header.h' file not found` або невизначені символи
: Перевірте, чи `products` у `SwiftPackages.json` містить назви продуктів із `Package.swift` і чи заголовок належить одному з них. Сервер збирання без підтримки Swift Package Manager ігнорує `SwiftPackages.json`, і тоді розширення так само не компілюється або не компонується.

`The Swift package graph did not resolve within the ... time budget`
: Пакети мають забагато залежностей для виявлення без файлу фіксації. Додайте `Package.resolved` поруч зі `SwiftPackages.json`, як описано в розділі [Фіксація версій пакетів](#locking-package-versions). Оскільки збирання не завершилося, створіть файл локально, наприклад додавши ті самі пакети до проєкту Xcode. Xcode зберігає файл у `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`.

## Локальний сервер збирання {#local-build-server}

Пакети Swift збирає сервер збирання macOS. Щоб використовувати пакети Swift з [локальним сервером збирання](/manuals/extender-local-setup), потрібні повна інсталяція Xcode (самих Command Line Tools недостатньо), [XcodeGen](https://github.com/yonaskolb/XcodeGen) і підтримка Swift Package Manager, увімкнена налаштуванням `extender.spm.enabled`. Докладніше див. [документацію сервера збирання на GitHub](https://github.com/defold/extender).
