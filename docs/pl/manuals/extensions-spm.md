---
title: Korzystanie z zależności Swift Package Manager w buildach iOS i macOS
brief: Ta instrukcja wyjaśnia, jak używać Swift Package Manager do rozwiązywania zależności w buildach iOS i macOS.
---

# Swift Package Manager

[Swift Package Manager](https://www.swift.org/documentation/package-manager/) to menedżer zależności wbudowany w Swift i Xcode. Wiele SDK dla iOS i macOS jest dystrybuowanych jako pakiety Swift, a część z nich nie jest już publikowana jako CocoaPods. Defold nie używa Xcode podczas budowania silnika, ale serwer budowania używa Xcode do pobierania i budowania pakietów Swift, od których zależy rozszerzenie. Wynik jest następnie linkowany do silnika tak samo jak [zależności CocoaPods](/manuals/extensions-cocoapods).

CocoaPods i pakietów Swift można używać w tym samym projekcie, a nawet w tym samym rozszerzeniu.

## Deklarowanie zależności {#declaring-dependencies}

Rozszerzenia natywne mogą zawierać plik `SwiftPackages.json` w folderach `manifests/ios` i `manifests/osx`, aby określić pakiety Swift, od których zależy rozszerzenie. Przykład:

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

Plik ma zwykły format JSON. Nie piszesz samodzielnie pliku `Package.swift`; serwer budowania generuje go z plików `SwiftPackages.json` wszystkich rozszerzeń.

Plik zawiera następujące pola:

* `platform` - Wymagane. `"ios"` w `manifests/ios/SwiftPackages.json` i `"osx"` w `manifests/osx/SwiftPackages.json`.
* `minVersion` - Opcjonalne. Minimalna wersja iOS lub macOS, dla której budowane są pakiety, na przykład `"15.0"`. Używana jest najwyższa wartość ze wszystkich rozszerzeń i minimalnej wersji obsługiwanej przez silnik, zarówno podczas budowania pakietów, jak i linkowania silnika.
* `wrapperType` - Opcjonalne. `"static"` (domyślne) lub `"dynamic"`. Zobacz [Linkowanie statyczne i dynamiczne](#static-and-dynamic-linking) poniżej.
* `packages` - Wymagane. Lista pakietów. Każdy pakiet ma następujące pola:
  * `url` - Adres `https://` repozytorium git pakietu. Adresy URL z danymi uwierzytelniającymi, niestandardowym portem lub ciągiem zapytania oraz adresy `ssh` nie są akceptowane, więc repozytorium musi być publicznie dostępne.
  * `products` - Produkty pakietu linkowane z silnikiem. Są to produkty biblioteczne wymienione w sekcji `products` pliku `Package.swift` pakietu. Nazwa produktu nie musi być taka sama jak nazwa pakietu lub importowanego modułu.
  * Dokładnie jedno wymaganie wersji:
    * `version` - Dokładnie ta wersja, na przykład `"12.16.0"`.
    * `from` - Ta wersja lub dowolna nowsza z tym samym numerem głównym. Na przykład `"9.0.0"` rozwiązuje się do najnowszego wydania `9.x.x`.
    * `branch` - Najnowszy commit na gałęzi, na przykład `"main"`.
    * `revision` - Konkretny commit podany jako pełny, 40-znakowy hasz commita.

Serwer budowania zbiera pliki `SwiftPackages.json` wszystkich rozszerzeń, rozwiązuje za ich pomocą wszystkie zależności, także zależności samych pakietów, i uwzględnia je podczas budowania kodu natywnego.

## Używanie pakietów w kodzie rozszerzenia {#using-packages-from-extension-code}

Nagłówki produktów są dostępne dla kodu źródłowego rozszerzenia. Używaj ich z plików źródłowych Objective-C++ (`.mm`). Ten przykład uruchamia SDK [Sentry](https://github.com/getsentry/sentry-cocoa) podczas startu aplikacji:

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

* Nagłówki Objective-C są importowane jako `#import <Module/Header.h>`, gdzie `Module` to nazwa modułu, który je udostępnia.
* Klasy zaimplementowane w Swift są deklarowane w generowanym nagłówku `<Module/Module-Swift.h>`. Zawiera on tylko klasy i metody udostępniane przez moduł dla Objective-C (oznaczone `@objc` w Swift). Zaimportuj przed nim `UIKit` (lub `AppKit` na macOS), ponieważ wygenerowany nagłówek używa ich typów.

## Zależności kilku rozszerzeń {#dependencies-of-several-extensions}

Gdy kilka rozszerzeń projektu używa pakietów Swift, wszystkie ich pliki `SwiftPackages.json` dla danej platformy są łączone w jeden graf pakietów:

* Pakiety z tym samym adresem URL są scalane, a żądane produkty łączone.
* Pakiet współdzielony przez kilka rozszerzeń musi mieć takie samo wymaganie wersji w każdym z nich. Różne wymagania, na przykład `"version": "12.16.0"` w jednym rozszerzeniu i `"from": "12.0.0"` w innym, powodują niepowodzenie budowania z błędem `Conflicting requirements for Swift package`.
* Używana jest najwyższa wartość `minVersion`.
* Wszystkie rozszerzenia ustawiające `wrapperType` muszą podawać tę samą wartość.

Projekt może też łączyć rozszerzenia korzystające z CocoaPods i pakietów Swift. Oba rodzaje zależności są rozwiązywane i linkowane z silnikiem. To samo SDK nie może jednak pochodzić z obu źródeł: jeśli jedno rozszerzenie pobiera Firebase z `Podfile`, a inne ze `SwiftPackages.json`, linkowanie silnika kończy się błędami powielonych symboli. Rozszerzenia współdzielące SDK powinny używać tego samego menedżera zależności.

## Blokowanie wersji pakietów {#locking-package-versions}

Po pomyślnym budowaniu serwer zwraca plik `Package.resolved` z dokładną wersją i commitem każdego pakietu w grafie, w tym zależności pakietów. Jest on umieszczany w folderze budowania projektu, na przykład `build/arm64-ios/Package.resolved`.

Skopiuj ten plik do rozszerzenia, obok `SwiftPackages.json` (na przykład `manifests/ios/Package.resolved`), aby zablokować wersje pakietów. Serwer używa wtedy zablokowanych wersji, o ile pasują do wymagań w `SwiftPackages.json`. Przyspiesza to też budowanie: bez `Package.resolved` serwer odkrywa zależności pakietów krok po kroku, co dla pakietów z wieloma zależnościami może trwać długo.

Jeśli kilka rozszerzeń dołącza `Package.resolved` dla tej samej platformy, używany jest tylko jeden z tych plików.

## Linkowanie statyczne i dynamiczne {#static-and-dynamic-linking}

Domyślnie wszystkie pakiety Swift są łączone w jedną bibliotekę statyczną, linkowaną do pliku wykonywalnego silnika.

Niektórych SDK nie można połączyć w bibliotekę statyczną, co powoduje błędy powielonych symboli podczas linkowania silnika. W takim przypadku ustaw `"wrapperType": "dynamic"` w `SwiftPackages.json`. Pakiety zostaną wtedy zbudowane jako framework dynamiczny osadzany w paczce aplikacji.

## Zasoby i manifesty prywatności {#resources-and-privacy-manifests}

Paczki zasobów i manifesty prywatności (`PrivacyInfo.xcprivacy`) pakietów są dołączane do paczki aplikacji tak samo jak w przypadku zależności CocoaPods.

## Migracja z CocoaPods {#migrating-from-cocoapods}

Wiele SDK jest publikowanych zarówno jako pod, jak i pakiet Swift. Aby przenieść rozszerzenie z `Podfile` do `SwiftPackages.json`:

1. Znajdź repozytorium git pakietu Swift w dokumentacji SDK. Często jest to to samo repozytorium co dla poda.
2. Znajdź nazwy produktów w pliku `Package.swift` pakietu. Nazwy podów i produktów często się różnią.
3. Zastąp `Podfile` plikiem `SwiftPackages.json`. Wersja `platform :ios` z `Podfile` staje się `minVersion`.
4. Upewnij się, że wiersze `#import` rozszerzenia nadal odpowiadają nazwom modułów produktów.

Na przykład ten `Podfile`:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

staje się takim `SwiftPackages.json`:

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

W tym przypadku moduły zachowują nazwy, więc `#import <FBSDKCoreKit/FBSDKCoreKit.h>` działa z obiema wersjami.

## Ograniczenia {#limitations}

* Obsługiwane są tylko repozytoria pakietów publicznie dostępne przez `https://`. Rejestry pakietów Swift nie są obsługiwane.
* Pliki `Package.swift` i wtyczki pakietów działają bez dostępu do sieci na serwerze budowania. Serwer sam pobiera pakiety i ich frameworki binarne przed zbudowaniem pakietów.
* Budowanie pakietów zawierających katalogi zasobów (`.xcassets`) dla iOS wymaga serwera budowania z Xcode 27 lub nowszym. Przy starszej wersji Xcode budowanie kończy się błędem wymieniającym te pakiety.
* Pliki `SwiftPackages.json` projektu mogą deklarować najwyżej 32 pakiety i 64 produkty na platformę.

## Rozwiązywanie problemów {#troubleshooting}

`'Module/Header.h' file not found` lub niezdefiniowane symbole
: Sprawdź, czy `products` w `SwiftPackages.json` to nazwy produktów z `Package.swift` i czy nagłówek należy do jednego z nich. Serwer budowania bez obsługi Swift Package Manager ignoruje `SwiftPackages.json`, a rozszerzenie kończy kompilację lub linkowanie takim samym błędem.

`The Swift package graph did not resolve within the ... time budget`
: Pakiety mają zbyt wiele zależności, aby odkryć je bez pliku blokady. Dodaj `Package.resolved` obok `SwiftPackages.json`, jak opisano w sekcji [Blokowanie wersji pakietów](#locking-package-versions). Ponieważ budowanie się nie zakończyło, utwórz plik lokalnie, na przykład dodając te same pakiety do projektu Xcode. Xcode zapisuje go w `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`.

## Lokalny serwer budowania {#local-build-server}

Pakiety Swift są budowane przez serwer budowania macOS. Aby korzystać z nich na [lokalnym serwerze budowania](/manuals/extender-local-setup), potrzebna jest pełna instalacja Xcode (same Command Line Tools nie wystarczą), [XcodeGen](https://github.com/yonaskolb/XcodeGen) i obsługa Swift Package Manager włączona ustawieniem `extender.spm.enabled`. Więcej informacji znajdziesz w [dokumentacji serwera budowania na GitHub](https://github.com/defold/extender).
