---
title: Natywne rozszerzenia - manifesty rozszerzeń
brief: Ta instrukcja opisuje manifest rozszerzenia i to, jak łączy się on z manifestem aplikacji oraz manifestem silnika.
---

# Pliki manifestów rozszerzenia, aplikacji i silnika

Manifest rozszerzenia to plik konfiguracyjny z flagami i definicjami używanymi podczas budowania pojedynczego rozszerzenia. Tę konfigurację łączy się z konfiguracją na poziomie aplikacji oraz z konfiguracją bazową samego silnika Defold.

## Manifest aplikacji

Manifest aplikacji (plik `.appmanifest`) to konfiguracja na poziomie aplikacji określająca sposób budowania gry na serwerach buildów. Manifest aplikacji pozwala usuwać z silnika części, których nie używasz. Jeśli nie potrzebujesz silnika fizyki, możesz usunąć go z pliku wykonywalnego, aby zmniejszyć jego rozmiar. Dowiedz się, jak wykluczać nieużywane funkcje [w instrukcji manifestu aplikacji](/manuals/app-manifest).

## Manifest silnika

Silnik Defold ma manifest budowania (`build.yml`), który jest dołączany do każdej wersji silnika i Defold SDK. Manifest kontroluje, których wersji SDK używać, jakich kompilatorów, linkerów i innych narzędzi używać oraz jakie domyślne flagi kompilacji i linkowania przekazywać tym narzędziom. Manifest można znaleźć w pliku share/extender/build_input.yml [na GitHubie](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml).

## Manifest rozszerzenia

Manifest rozszerzenia (`ext.manifest`) z kolei jest plikiem konfiguracyjnym przeznaczonym konkretnie dla rozszerzenia. Kontroluje sposób kompilacji i linkowania kodu źródłowego rozszerzenia oraz to, jakie dodatkowe biblioteki mają zostać dołączone.

Wszystkie trzy pliki manifestów używają tej samej składni, dzięki czemu można je łączyć i w pełni kontrolować sposób budowania rozszerzeń oraz gry.

Dla każdego budowanego rozszerzenia manifesty są łączone w następujący sposób:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

Dzięki temu użytkownik może nadpisać domyślne zachowanie silnika, a także zachowanie każdego rozszerzenia. Na potrzeby końcowego etapu linkowania łączymy manifest aplikacji z manifestem build.yml:

	manifest = merge(game.appmanifest, build.yml)


### Plik ext.manifest

Poza nazwą rozszerzenia plik manifestu może zawierać flagi kompilacji zależne od platformy, flagi linkowania, biblioteki i frameworki. Jeśli plik *ext.manifest* nie zawiera sekcji "platforms" albo którejś platformy brakuje na liście, platforma, dla której tworzysz pakiet, nadal się zbuduje, ale bez dodatkowych ustawionych flag.

Oto przykład:

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    armv7-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### Dozwolone klucze

Dozwolone klucze dla flag kompilacji zależnych od platformy to:

* `frameworks` - frameworki Apple do dołączenia podczas budowania (iOS i macOS)
* `weakFrameworks` - frameworki Apple do opcjonalnego dołączenia podczas budowania (iOS i macOS)
* `flags` - flagi przekazywane do kompilatora
* `linkFlags` - flagi przekazywane do linkera
* `libs` - dodatkowe biblioteki do dołączenia podczas linkowania
* `defines` - definicje ustawiane podczas budowania
* `aaptExtraPackages` - dodatkowa nazwa pakietu, która ma zostać wygenerowana (Android)
* `aaptExcludePackages` - wyrażenie regularne (lub dokładne nazwy) pakietów do wykluczenia (Android)
* `aaptExcludeResourceDirs` - wyrażenie regularne (lub dokładne nazwy) katalogów zasobów do wykluczenia (Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` - te flagi służą do usuwania elementów wcześniej zdefiniowanych w kontekście platformy.

Dla wszystkich słów kluczowych stosujemy filtr białej listy, aby uniknąć nieprawidłowej obsługi ścieżek i dostępu do plików spoza folderu przesyłania builda.
