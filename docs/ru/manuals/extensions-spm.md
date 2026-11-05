---
title: Использование зависимостей Swift Package Manager в сборках для iOS и macOS
brief: В этом руководстве описано, как использовать Swift Package Manager для разрешения зависимостей в сборках для iOS и macOS.
---

# Swift Package Manager

[Swift Package Manager](https://www.swift.org/documentation/package-manager/) — менеджер зависимостей, встроенный в Swift и Xcode. Многие SDK для iOS и macOS распространяются в виде пакетов Swift, а некоторые из них больше не публикуются в CocoaPods. Defold не использует Xcode для сборки движка, однако сервер сборки использует Xcode для загрузки и сборки пакетов Swift, от которых зависит расширение. Полученный результат затем компонуется с движком так же, как [зависимости CocoaPods](/manuals/extensions-cocoapods).

CocoaPods и пакеты Swift можно использовать в одном проекте и даже в одном расширении.


## Объявление зависимостей {#declaring-dependencies}

Нативные расширения могут содержать файл `SwiftPackages.json` в папках `manifests/ios` и `manifests/osx`, чтобы задать пакеты Swift, от которых зависит расширение. Пример:

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

Это обычный JSON-файл. Вам не нужно писать `Package.swift` самостоятельно: сервер сборки создаёт его из файлов `SwiftPackages.json` всех расширений.

Файл содержит следующие поля:

* `platform` — обязательное. `"ios"` в `manifests/ios/SwiftPackages.json` и `"osx"` в `manifests/osx/SwiftPackages.json`.
* `minVersion` — необязательное. Минимальная версия iOS или macOS, для которой собираются пакеты, например `"15.0"`. При сборке пакетов и компоновке движка используется наибольшее из значений всех расширений и минимальной версии, поддерживаемой движком.
* `wrapperType` — необязательное. `"static"` (по умолчанию) или `"dynamic"`. См. раздел [Статическая и динамическая компоновка](#static-and-dynamic-linking) ниже.
* `packages` — обязательное. Список пакетов. У каждого пакета есть следующие поля:
  * `url` — URL git-репозитория пакета, начинающийся с `https://`. URL с учётными данными, нестандартным портом или строкой запроса, а также URL `ssh` не принимаются, поэтому репозиторий должен быть общедоступным.
  * `products` — продукты пакета, которые нужно скомпоновать с движком. Это библиотечные продукты, перечисленные в разделе `products` файла `Package.swift` пакета. Имя продукта не обязательно совпадает с именем пакета или импортируемого модуля.
  * Ровно одно требование к версии:
    * `version` — указанная точная версия, например `"12.16.0"`.
    * `from` — указанная версия или более поздняя версия с тем же основным номером. Например, `"9.0.0"` разрешается в последний выпуск `9.x.x`.
    * `branch` — последний коммит в ветке, например `"main"`.
    * `revision` — конкретный коммит, указанный полным хешем из 40 символов.

Сервер сборки собирает файлы `SwiftPackages.json` всех расширений и использует их для разрешения всех зависимостей, включая зависимости самих пакетов, и включает их при сборке нативного кода.


## Использование пакетов в коде расширения {#using-packages-from-extension-code}

Заголовочные файлы продуктов доступны исходному коду расширения. Используйте их в исходных файлах Objective-C++ (`.mm`). В этом примере [Sentry](https://github.com/getsentry/sentry-cocoa) SDK запускается при запуске приложения:

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

* Заголовки Objective-C импортируются как `#import <Module/Header.h>`, где `Module` — имя модуля, который их предоставляет.
* Классы, реализованные на Swift, объявлены в сгенерированном заголовке `<Module/Module-Swift.h>`. Он содержит только классы и методы, которые модуль предоставляет для Objective-C (помеченные `@objc` в Swift). Импортируйте `UIKit` (или `AppKit` на macOS) перед ним, поскольку сгенерированный заголовок использует их типы.


## Зависимости нескольких расширений {#dependencies-of-several-extensions}

Когда несколько расширений в проекте используют пакеты Swift, все их файлы `SwiftPackages.json` для платформы объединяются в единый граф пакетов:

* Пакеты с одинаковым URL объединяются вместе с запрошенными продуктами.
* Пакет, используемый несколькими расширениями, должен иметь одинаковое требование к версии во всех них. Различные требования, например `"version": "12.16.0"` в одном расширении и `"from": "12.0.0"` в другом, приводят к ошибке сборки `Conflicting requirements for Swift package`.
* Используется наибольшее значение `minVersion`.
* Все расширения, задающие `wrapperType`, должны указывать одно и то же значение.

В проекте также можно сочетать расширения, использующие CocoaPods, с расширениями, использующими пакеты Swift. Зависимости обоих типов разрешаются и компонуются с движком. Однако один SDK не должен поступать из обоих источников: если одно расширение получает Firebase из `Podfile`, а другое — из `SwiftPackages.json`, компоновка движка завершится ошибками дублирования символов. Расширения, использующие общий SDK, должны использовать один менеджер зависимостей.


## Фиксация версий пакетов {#locking-package-versions}

После успешной сборки сервер возвращает файл `Package.resolved` с точной версией и коммитом каждого пакета в графе, включая зависимости пакетов. Он размещается в папке сборки проекта, например `build/arm64-ios/Package.resolved`.

Скопируйте этот файл в расширение рядом с `SwiftPackages.json` (например, `manifests/ios/Package.resolved`), чтобы зафиксировать версии пакетов. Сервер сборки будет использовать зафиксированные версии, пока они соответствуют требованиям в `SwiftPackages.json`. Это также ускоряет сборку: без файла `Package.resolved` сервер последовательно определяет зависимости пакетов, что может занимать много времени для пакетов с большим числом зависимостей.

Если несколько расширений содержат файл `Package.resolved` для одной платформы, используется только один из них.


## Статическая и динамическая компоновка {#static-and-dynamic-linking}

По умолчанию все пакеты Swift объединяются в одну статическую библиотеку, которая компонуется с исполняемым файлом движка.

Некоторые SDK нельзя объединить в статическую библиотеку; в этом случае компоновка движка завершается ошибками дублирования символов. Установите `"wrapperType": "dynamic"` в `SwiftPackages.json`. Тогда пакеты будут собраны в динамический фреймворк, встраиваемый в бандл приложения.


## Ресурсы и манифесты конфиденциальности {#resources-and-privacy-manifests}

Бандлы ресурсов и манифесты конфиденциальности (`PrivacyInfo.xcprivacy`) пакетов включаются в бандл приложения так же, как для зависимостей CocoaPods.


## Переход с CocoaPods {#migrating-from-cocoapods}

Многие SDK публикуются и как pod, и как пакет Swift. Чтобы перевести расширение с `Podfile` на файл `SwiftPackages.json`:

1. Найдите git-репозиторий пакета Swift в документации SDK. Часто это тот же репозиторий, что и у pod.
2. Найдите имена продуктов в файле `Package.swift` пакета. Имена pod и продуктов часто различаются.
3. Замените `Podfile` файлом `SwiftPackages.json`. Версия `platform :ios` из `Podfile` становится `minVersion`.
4. Убедитесь, что строки `#import` расширения по-прежнему соответствуют именам модулей продуктов.

Например, этот `Podfile`:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

преобразуется в такой `SwiftPackages.json`:

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

В этом случае модули сохраняют свои имена, поэтому `#import <FBSDKCoreKit/FBSDKCoreKit.h>` работает с обоими вариантами.


## Ограничения {#limitations}

* Поддерживаются только репозитории пакетов, общедоступные по `https://`. Реестры пакетов Swift не поддерживаются.
* Файлы `Package.swift` и плагины пакетов выполняются на сервере сборки без доступа к сети. Сервер сам загружает пакеты и их бинарные фреймворки перед сборкой пакетов.
* Для сборки пакетов с каталогами ассетов (`.xcassets`) для iOS требуется сервер сборки с Xcode 27 или новее. При более ранней версии Xcode сборка завершается ошибкой с перечислением таких пакетов.
* Файлы `SwiftPackages.json` проекта могут объявлять не более 32 пакетов и 64 продуктов на платформу.


## Устранение неполадок {#troubleshooting}

`'Module/Header.h' file not found` или неопределённые символы
: Проверьте, что `products` в `SwiftPackages.json` содержит имена продуктов из `Package.swift` и что заголовок принадлежит одному из них. Сервер сборки без поддержки Swift Package Manager игнорирует `SwiftPackages.json`, что также приводит к ошибкам компиляции или компоновки расширения.

`The Swift package graph did not resolve within the ... time budget`
: У пакетов слишком много зависимостей, чтобы определить их без файла фиксации версий. Добавьте `Package.resolved` рядом с `SwiftPackages.json`, как описано в разделе [Фиксация версий пакетов](#locking-package-versions). Поскольку сборка не завершилась, создайте файл локально, например добавив те же пакеты в проект Xcode. Xcode сохраняет файл в `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`.


## Локальный сервер сборки {#local-build-server}

Пакеты Swift собираются сервером сборки на macOS. Для использования пакетов Swift на [локальном сервере сборки](/manuals/extender-local-setup) необходимы полная установка Xcode (одних Command Line Tools недостаточно), [XcodeGen](https://github.com/yonaskolb/XcodeGen) и поддержка Swift Package Manager, включённая настройкой `extender.spm.enabled`. Подробнее см. в [документации сервера сборки на GitHub](https://github.com/defold/extender).
