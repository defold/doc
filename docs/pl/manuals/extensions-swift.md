---
title: Używanie języka Swift w rozszerzeniach natywnych dla iOS i macOS
brief: Ta instrukcja wyjaśnia, jak pisać w języku Swift kod rozszerzenia natywnego dla iOS i macOS.
---

# Swift w rozszerzeniach natywnych {#swift-in-native-extensions}

Wiele interfejsów API firmy Apple, takich jak StoreKit 2 i CryptoKit, jest dostępnych tylko z poziomu języka Swift. Rozszerzenie natywne (ang. native extension) może zawierać własne pliki źródłowe Swift obok plików Objective-C++. Serwer budowania kompiluje je razem z pozostałym kodem rozszerzenia i linkuje wynik z silnikiem. Niezależnie od tego [pakiety Swift](/manuals/extensions-spm) i [CocoaPods](/manuals/extensions-cocoapods) dostarczają gotowe zależności.

Kod Swift jest kompilowany dla macOS (`arm64` i `x86_64`) oraz iOS (dla urządzeń i symulatora). Podczas budowania na inne platformy pliki Swift są pomijane.


## Dodawanie plików źródłowych Swift {#adding-swift-sources}

Umieść pliki `.swift` w folderze `src` rozszerzenia, obok plików C++ i Objective-C++.

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Wszystkie pliki Swift przechowuj w folderze `src`. Jeśli serwer budowania znajdzie plik Swift w folderze `commonsrc` lub `pluginsrc`, budowanie dla macOS lub iOS zakończy się błędem.

Wszystkie pliki Swift danego rozszerzenia są kompilowane razem jako jeden moduł Swift. Jego nazwa pochodzi z pola `name` w pliku `ext.manifest`. Każdy znak poza literami, cyframi i znakiem podkreślenia jest zastępowany przez `_` (np. `My-Extension` staje się `My_Extension`). Kompilator pracuje w trybie języka Swift 5.

Nazwa modułu musi się różnić od nazw modułów importowanych w jego kodzie. W rozszerzeniu o nazwie `StoreKit` nie można użyć `import StoreKit`, ponieważ kompilator potraktuje to jako próbę zaimportowania bieżącego modułu.


## Wywoływanie kodu Swift z Objective-C++ {#calling-swift-from-objective-c}

Punktem wejścia rozszerzenia nadal jest funkcja C++ zarejestrowana za pomocą `DM_DECLARE_EXTENSION`, dlatego rozszerzenie wymaga co najmniej jednego pliku `.cpp` lub `.mm`. W tym pliku możesz wywoływać kod Swift za pośrednictwem wygenerowanego nagłówka `<Module>-Swift.h`.

W Objective-C widoczne są tylko klasy, protokoły i metody oznaczone atrybutem `@objc`. Zadeklaruj klasy jako `public` i dopilnuj, by dziedziczyły po `NSObject`.

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

* Wygenerowany nagłówek importuje `Foundation`. Dla typów z innych frameworków zawiera jedynie deklaracje zapowiadające. Przed wywołaniem metod korzystających z tych typów zaimportuj w pliku `.mm` nagłówek odpowiedniego frameworka (np. `UIKit`).
* Funkcje oznaczone `throws` są dostępne jako metody z parametrem `NSError **`, a funkcje oznaczone `async` jako metody przyjmujące blok wywoływany po zakończeniu operacji.
* Mechanizmy specyficzne dla języka Swift, takie jak typy i funkcje generyczne, typy wyliczeniowe z wartościami powiązanymi i struktury, nie są widoczne w Objective-C. Udostępnij je za pośrednictwem klasy oznaczonej `@objc`.
* Pliki `.mm` są kompilowane tylko dla iOS i macOS, więc budowanie rozszerzenia złożonego wyłącznie z plików `.mm` i `.swift` na inne platformy kończy się błędem `Extension has no source!`. Aby budować rozszerzenie również na inne platformy, umieść `DM_DECLARE_EXTENSION` w pliku `.cpp`, a wywołanie kodu z pliku `.mm` obejmij w nim warunkiem kompilacji sprawdzającym `DM_PLATFORM_IOS` lub `DM_PLATFORM_OSX`.


## Wywoływanie kodu Objective-C z języka Swift {#calling-objective-c-from-swift}

Aby w kodzie Swift korzystać z deklaracji Objective-C lub C, dodaj do folderu `src` nagłówek pomostowy (ang. bridging header) o nazwie `<Module>-Bridging-Header.h`, na przykład `src/MyExtension-Bridging-Header.h`.

```cpp
#import "mynative.h"
```

Jeśli nagłówek istnieje, jest automatycznie importowany do modułu Swift. Kompilator szuka dołączanych przez niego nagłówków w folderze `include` rozszerzenia oraz w folderach wymienionych w `additionalSwiftIncludePaths` (zobacz niżej).

Frameworki Apple, takie jak `Foundation`, `UIKit` i `StoreKit`, importuje się w kodzie Swift zwykłą instrukcją `import`. Frameworki wymienione w polach `frameworks` i `weakFrameworks` pliku `ext.manifest` są linkowane jak zwykle. Większość frameworków systemowych jest linkowana automatycznie po zaimportowaniu ich w kodzie Swift.


## Korzystanie z pakietów Swift w kodzie Swift {#using-swift-packages-from-swift}

Kod Swift rozszerzenia ma dostęp do produktów [pakietów Swift](/manuals/extensions-spm) zadeklarowanych przez to rozszerzenie w pliku `SwiftPackages.json`. Zaimportuj moduł w pliku Swift.

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

Nagłówki Objective-C z pakietu możesz importować w nagłówku pomostowym tak samo jak w pliku `.mm`.

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

Zadeklaruj pakiet w pliku `SwiftPackages.json` rozszerzenia, które go używa. Serwer budowania najpierw buduje pakiety, a potem kod Swift rozszerzenia. Jeśli pakiet wymaga wersji systemu nowszej niż minimalna wersja obsługiwana przez silnik, podaj wymaganą wersję w polu `minVersion` w pliku `SwiftPackages.json`. Kod Swift rozszerzenia również zostanie zbudowany dla tej wersji. W kodzie Swift rozszerzenia nie można bezpośrednio korzystać z zależności CocoaPods. Używaj ich w pliku Objective-C++ i przekazuj z niego potrzebne dane do kodu Swift.


## Opcje kompilatora {#compiler-options}

Opcje kompilatora Swift ustaw w pliku `ext.manifest`, w tej samej sekcji `context` co opcje kompilatora C++.

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

* `defines` - Definicje z C++ są przekazywane do kompilatora Swift jako nazwy używane w kompilacji warunkowej, dzięki czemu w kodzie Swift działa `#if MY_DEFINE`. Swift obsługuje wyłącznie nazwy, więc wartość definicji jest pomijana (np. w przypadku `MY_DEFINE=1`).
* `swiftFlags` - Dodatkowe flagi kompilatora Swift. Każdą flagę i każdą wartość wpisz jako osobny element listy. Podanie flagi spoza listy dozwolonych powoduje błąd budowania `Invalid flag - 'swiftFlags'`. Jeśli wartość zawiera biały znak, ukośnik odwrotny lub składnię szablonu albo wskazuje plik odpowiedzi, pojawia się błąd `invalid 'swiftFlags' value`. Serwer akceptuje następujące flagi.
  * `-enable-upcoming-feature <Feature>` - Włącza funkcję przewidzianą na przyszłą wersję języka, np. `["-enable-upcoming-feature", "ExistentialAny"]`.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize` i `-Onone` - Poziom optymalizacji. Domyślna flaga to `-O`.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - Dodatkowe foldery wyszukiwania nagłówków i modułów. Kompilator Swift przeszukuje je oprócz folderu `include` rozszerzenia.
* `additionalFrameworkSearchPaths` - Dodatkowe foldery wyszukiwania frameworków, przeszukiwane oprócz folderu `lib/<platform>` rozszerzenia. Korzystają z nich linker, kompilator Swift oraz kompilator C++ i Objective-C++ przy kompilacji plików źródłowych rozszerzenia.

Ścieżki są względne wobec folderu rozszerzenia, muszą pozostawać w jego obrębie i mogą zawierać tylko litery, cyfry oraz znaki `._+-/`. Na serwer budowania wysyłane są wyłącznie foldery `include`, `src`, `commonsrc`, `pluginsrc`, `lib/<platform>`, `manifests/<platform>` i `res/<platform>` rozszerzenia, więc każda ścieżka musi wskazywać na jeden z tych folderów lub jego zawartość. Pliki z innych folderów, na przykład z folderu `vendor` w głównym katalogu rozszerzenia, są niedostępne podczas budowania.

Klucze Swift dla platformy `ios` dotyczą zarówno urządzeń, jak i symulatora. Serwer budowania w wersji sprzed wprowadzenia obsługi Swift odrzuca te klucze i zgłasza błąd `Manifest context variable unsupported`. Aby znów zbudować projekt, zaktualizuj zarówno silnik Defold, jak i serwer budowania.


## Minimalne wersje systemu operacyjnego {#minimum-os-versions}

Środowisko uruchomieniowe Swift jest częścią każdej wersji iOS i macOS obsługiwanej przez silnik Defold. Kod Swift jest kompilowany dla minimalnej wersji iOS lub macOS określonej dla danej kompilacji, a aplikacja korzysta ze środowiska uruchomieniowego Swift dostarczanego przez system. Przed wywołaniem API wprowadzonego w wersji nowszej niż minimalna sprawdź jego dostępność za pomocą `#available`.

Niektóre elementy środowiska uruchomieniowego są dołączane do systemu dopiero od określonej wersji. Na przykład `MutableSpan` i pokrewne typy są dostępne od iOS 26 i macOS 26. Jeśli minimalna wersja systemu jest starsza, a twój kod Swift lub dynamiczny framework z pakietu korzysta z takiej funkcji, aplikacja może potrzebować dodatkowej biblioteki do działania na urządzeniach ze starszym systemem. Serwer budowania automatycznie wykrywa biblioteki używane przez silnik i dołączone do niego biblioteki dynamiczne, podobnie jak robi to Xcode, po czym dodaje je do aplikacji. W systemie iOS trafiają one do folderu `Frameworks` aplikacji i są podpisywane wraz z resztą jej kodu.

Minimalna wersja systemu dla danej kompilacji odpowiada minimalnej wersji obsługiwanej przez silnik i zależy od wersji Defold oraz serwera budowania. Ustawienie `minVersion` w pliku `SwiftPackages.json` podnosi to minimum dla pakietów, kodu Swift i etapu linkowania silnika, zgodnie z opisem w [instrukcji Swift Package Manager](/manuals/extensions-spm). Tego minimum nie można obniżyć.


## Ograniczenia {#limitations}

* Rozszerzenie nadal wymaga pliku C++ lub Objective-C++ z makrem `DM_DECLARE_EXTENSION`. Kod Swift nie może zarejestrować rozszerzenia ani korzystać z API C++ pakietu Defold SDK (`dmsdk`). Wywołuj to API z pliku Objective-C++. Nagłówki `dmsdk` zgodne z C, np. `dmsdk/dlib/hash.h`, możesz dołączyć w nagłówku pomostowym. Budowanie rozszerzenia zawierającego wyłącznie pliki `.swift` kończy się podczas linkowania błędem niezdefiniowanego symbolu, którego nazwa pochodzi od nazwy rozszerzenia.
* W kodzie Swift rozszerzenia nie można bezpośrednio korzystać z zależności CocoaPods. Używaj ich w pliku Objective-C++ i przekazuj z niego potrzebne dane do kodu Swift.
* Obsługiwany jest wyłącznie tryb języka Swift 5. Współpraca z C++ na poziomie języka jest wyłączona.
* Pliki źródłowe Swift są obsługiwane od wersji 1.14.2 silnika Defold. Serwer budowania ze starszym SDK zgłasza błąd `Swift sources are not supported by this Defold SDK version`.
* Podczas budowania artefaktu `library` (`--build-artifacts library` w narzędziu [Bob](/manuals/bob)) pliki źródłowe Swift nie są kompilowane, więc kompilacja pliku Objective-C++ importującego `<Module>-Swift.h` kończy się błędem.


## Rozwiązywanie problemów {#troubleshooting}

`no such module 'Name'`
: Moduł nie jest produktem pakietu zadeklarowanego w pliku `SwiftPackages.json`. Sprawdź, czy lista `products` zawiera produkt udostępniający moduł, zgodnie z opisem w [instrukcji Swift Package Manager](/manuals/extensions-spm).

`Swift sources are only supported in the 'src' folder`
: Przenieś pliki `.swift` do folderu `src` rozszerzenia.

`'MyExtension-Swift.h' file not found`
: Nazwa modułu pochodzi z pola `name` w pliku `ext.manifest`. Sprawdź nazwę w wierszu `#import`.

`unknown type name 'MyExtensionGreeter'`
: W wygenerowanym nagłówku brakuje klasy. Sprawdź, czy klasa jest oznaczona jako `public` i `@objc`, czy dziedziczy po `NSObject` i czy w pliku `.mm` używasz nazwy podanej w `@objc(...)`.

`cannot find 'AppStore' in scope` wraz z `file 'A.swift' is part of module 'StoreKit'; ignoring import`
: Rozszerzenie ma taką samą nazwę jak jeden z importowanych modułów. Zmień nazwę rozszerzenia w pliku `ext.manifest`.

`Undefined symbols ... _MyExtension`
: W rozszerzeniu brakuje `DM_DECLARE_EXTENSION`. Dodaj plik `.mm`, który rejestruje rozszerzenie w sposób opisany powyżej.

`Invalid flag - 'swiftFlags'`
: Flaga nie znajduje się na liście dozwolonych flag. Usuń ją lub użyj jednej z wymienionych flag.

`invalid 'swiftFlags' value`
: Wartość zawiera biały znak, ukośnik odwrotny lub składnię szablonu albo wskazuje plik odpowiedzi. Umieść każdą flagę i każdą wartość w osobnym elemencie listy.
