---
title: Rozszerzenia natywne - dobre praktyki
brief: Ta instrukcja opisuje dobre praktyki przy tworzeniu rozszerzeń natywnych.
---

# Dobre praktyki

Pisanie kodu wieloplatformowego może być trudne, ale istnieją sposoby, aby ułatwić zarówno jego tworzenie, jak i utrzymanie.


## Struktura projektu

Podczas tworzenia rozszerzenia warto zadbać o kilka rzeczy, które pomagają zarówno przy jego rozwijaniu, jak i późniejszym utrzymaniu.

### API Lua

Powinno istnieć tylko jedno API Lua i jedna jego implementacja. Dzięki temu znacznie łatwiej zachować takie samo działanie na wszystkich platformach.

Jeśli dana platforma nie powinna obsługiwać rozszerzenia, zaleca się po prostu nie rejestrować modułu Lua. Dzięki temu możesz wykryć obsługę, sprawdzając `nil`:

```lua
    if myextension ~= nil then
        myextension.do_something()
    end
```

### Struktura folderów

Poniższa struktura folderów jest często używana w rozszerzeniach:

```
    /root
        /input
        /main                            -- All the files for the actual example project
            /...
        /myextension                     -- The actual root folder of the extension
            ext.manifest
            /include                     -- External includes, used by other extensions
            /libs
                /<platform>              -- External libraries for all supported platforms
            /src
                myextension.cpp          -- The extension Lua api and the extension life cycle functions
                                            Also contains generic implementations of your Lua api functions.
                myextension_private.h    -- Your internal api that each platform will implement (I.e. `myextension_Init` etc)
                myextension.mm           -- If native calls are needed for iOS/macOS. Implements `myextension_Init` etc for iOS/macOS
                myextension_android.cpp  -- If JNI calls are needed for Android. Implements `myextension_Init` etc for Android
                /java
                    /<platform>          -- Any java files needed for Android
            /res                         -- Any resources needed for a platform
            /external
                README.md                -- Notes/scripts on how to build or package any external libraries
        /bundleres                       -- Resources that should be bundles for (see game.project and the [bundle_resources setting]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Any extra app configuration info
```

Pamiętaj, że `myextension.mm` i `myextension_android.cpp` są potrzebne tylko wtedy, gdy wykonujesz natywne wywołania specyficzne dla danej platformy.

#### Foldery platform

W niektórych miejscach architektura platformy jest używana jako nazwa folderu, aby określić, których plików użyć podczas kompilacji/dołączania aplikacji do bundla. Mają one postać:

    <architecture>-<platform>

Aktualna lista to:

    arm64-ios, armv7-ios, x86_64-ios, arm64-android, armv7-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

Na przykład biblioteki specyficzne dla platformy umieszczaj w:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## Pisanie kodu natywnego

W kodzie źródłowym Defold C++ jest używany bardzo oszczędnie i większość kodu ma charakter zbliżony do C. Szablony praktycznie nie występują, z wyjątkiem kilku klas kontenerów, ponieważ szablony zwiększają zarówno czas kompilacji, jak i rozmiar pliku wykonywalnego.

### Wersja C++

Kod źródłowy Defold jest budowany z użyciem domyślnej wersji C++ dla każdego kompilatora. Sam kod źródłowy Defold nie używa wersji C++ wyższej niż C++98. Chociaż można użyć nowszej wersji do zbudowania rozszerzenia, może się to wiązać ze zmianami ABI. Może to uniemożliwić używanie jednego rozszerzenia razem z rozszerzeniami w silniku lub z [asset portal](/assets).

Kod źródłowy Defold unika korzystania z najnowszych funkcji i wersji C++. Głównie dlatego, że przy tworzeniu silnika gier nowe funkcje nie są konieczne, ale też dlatego, że śledzenie najnowszych możliwości C++ jest czasochłonne, a ich pełne opanowanie wymaga dużo cennego czasu.

Daje to również dodatkową korzyść twórcom rozszerzeń, ponieważ Defold utrzymuje stabilne ABI. Warto też podkreślić, że używanie najnowszych funkcji C++ może uniemożliwić kompilację kodu na różnych platformach z powodu różnic w poziomie wsparcia.

### Bez wyjątków C++

Defold nie używa wyjątków w silniku. Wyjątków z reguły unika się w silnikach gier, ponieważ dane są w większości znane z góry, już na etapie tworzenia. Wyłączenie obsługi wyjątków C++ zmniejsza rozmiar pliku wykonywalnego i poprawia wydajność działania.

### Standard Template Libraries - STL

Ponieważ silnik Defold nie używa kodu STL, poza niektórymi algorytmami i matematyką (`std::sort`, `std::upper_bound` itd.), użycie STL w twoim rozszerzeniu może być dla ciebie dopuszczalne.

Pamiętaj jednak, że niezgodności ABI mogą utrudnić używanie twojego rozszerzenia razem z innymi rozszerzeniami lub bibliotekami firm trzecich.

Unikanie bibliotek STL (silnie opartych na szablonach) poprawia także czasy budowania, a co ważniejsze, zmniejsza rozmiar pliku wykonywalnego.

#### Ciągi znaków

W silniku Defold używa się `const char*` zamiast `std::string`. Używanie `std::string` jest częstą pułapką przy mieszaniu różnych wersji C++ lub kompilatorów, ponieważ może prowadzić do niedopasowania ABI. Użycie `const char*` i kilku funkcji pomocniczych pozwala tego uniknąć.

### Ukrywaj funkcje

Jeśli to możliwe, używaj słowa kluczowego `static` dla funkcji lokalnych dla danej jednostki kompilacji. Pozwala to kompilatorowi wykonać pewne optymalizacje, co może zarówno poprawić wydajność, jak i zmniejszyć rozmiar pliku wykonywalnego.

## Biblioteki firm trzecich

Wybierając bibliotekę firmy trzeciej do użycia (niezależnie od języka), rozważ następujące kwestie:

* Funkcjonalność - Czy rozwiązuje konkretny problem, który masz?
* Wydajność - Czy powoduje narzut wydajnościowy podczas działania?
* Rozmiar biblioteki - O ile większy będzie końcowy plik wykonywalny? Czy to akceptowalne?
* Zależności - Czy wymaga dodatkowych bibliotek?
* Wsparcie - W jakim stanie jest biblioteka? Czy ma wiele otwartych zgłoszeń? Czy jest nadal utrzymywana?
* Licencja - Czy można jej użyć w tym projekcie?


## Zależności open source

Zawsze upewnij się, że masz dostęp do swoich zależności. Na przykład jeśli zależysz od czegoś w GitHub, nic nie stoi na przeszkodzie, aby dane repozytorium zostało usunięte albo nagle zmieniło kierunek rozwoju lub właściciela. Możesz ograniczyć to ryzyko, tworząc fork repozytorium i używając własnego forka zamiast projektu upstream.

Pamiętaj, że kod z biblioteki zostanie wstrzyknięty do twojej gry, więc upewnij się, że biblioteka robi to, co powinna, i nic więcej!
