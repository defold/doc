---
title: Rozszerzenia natywne - dobre praktyki
brief: Ta instrukcja opisuje dobre praktyki przy tworzeniu rozszerzeń natywnych.
---

# Dobre praktyki

Pisanie kodu wieloplatformowego bywa trudne, ale istnieją sposoby, aby ułatwić zarówno jego tworzenie, jak i utrzymanie.


## Struktura projektu

Przy tworzeniu rozszerzenia warto zadbać o kilka rzeczy, które pomagają zarówno w jego rozwijaniu, jak i późniejszym utrzymaniu.

### API Lua

Powinno istnieć tylko jedno API Lua i jedna jego implementacja. Dzięki temu znacznie łatwiej zapewnić takie samo działanie na wszystkich platformach.

Jeśli dana platforma nie powinna obsługiwać rozszerzenia, zaleca się po prostu nie rejestrować modułu Lua. Dzięki temu można wykryć obsługę, sprawdzając `nil`:

```lua
    if myextension ~= nil then
        myextension.do_something()
    end
```

### Struktura folderów

W rozszerzeniach często stosuje się następującą strukturę folderów:

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

Zwróć uwagę, że `myextension.mm` i `myextension_android.cpp` są potrzebne tylko wtedy, gdy wykonujesz konkretne natywne wywołania dla danej platformy.

#### Foldery platform

W niektórych miejscach architektura platformy jest używana jako nazwa folderu, aby określić, których plików użyć podczas kompilacji lub bundlowania aplikacji. Mają one postać:

    <architecture>-<platform>

Aktualna lista to:

    arm64-ios, arm64_sim-ios, arm64-android, armv7-android, x86_64-android, x86_64-linux, x86_64-osx, x86_64-win32

Na przykład biblioteki specyficzne dla platformy umieszczaj w:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## Pisanie kodu natywnego

W kodzie źródłowym Defold C++ jest używany bardzo oszczędnie, a większość kodu ma bardzo C-podobny charakter. Szablonów prawie się tam nie stosuje, z wyjątkiem kilku klas kontenerów, ponieważ szablony zwiększają zarówno czas kompilacji, jak i rozmiar pliku wykonywalnego.

### Wersja C++

Podczas budowania głównego silnika używamy C++11, ale w systemie Windows używamy C++14. Kompilacje na konsole zazwyczaj wymagają obecnie C++14 lub nowszego.

W przypadku natywnych rozszerzeń nie używamy ustalonej wersji C++, lecz polegamy na domyślnej wersji toolchaina danej platformy.

Kod źródłowy Defold unika korzystania z najnowszych funkcji i wersji C++. Głównie dlatego, że przy tworzeniu silnika gier nie ma potrzeby wprowadzania nowych funkcji, ale też dlatego, że śledzenie najnowszych możliwości C++ jest czasochłonne, a ich naprawdę dobre opanowanie wymagałoby dużo cennego czasu.

Ma to też dodatkową korzyść dla twórców rozszerzeń: Defold utrzymuje stabilne ABI. Warto również podkreślić, że używanie najnowszych funkcji C++ może uniemożliwić kompilację kodu na różnych platformach z powodu różnego poziomu wsparcia.

### Bez wyjątków C++

Defold nie korzysta z wyjątków w silniku. Wyjątków z reguły unika się w silnikach gier, ponieważ dane są w większości znane wcześniej, na etapie tworzenia. Wyłączenie obsługi wyjątków C++ zmniejsza rozmiar pliku wykonywalnego i poprawia wydajność działania.

### Standard Template Libraries - STL

Ponieważ silnik Defold nie używa kodu STL, poza niektórymi algorytmami i matematyką (`std::sort`, `std::upper_bound` itd.), użycie STL w twoim rozszerzeniu może się sprawdzić.

Pamiętaj jednak, że niezgodności ABI mogą utrudnić używanie twojego rozszerzenia razem z innymi rozszerzeniami lub bibliotekami firm trzecich.

Unikanie bibliotek STL, które w dużym stopniu opierają się na szablonach, poprawia też czas budowania, a co ważniejsze, zmniejsza rozmiar pliku wykonywalnego.

#### Ciągi znaków

W silniku Defold zamiast `std::string` używa się `const char*`. Używanie `std::string` jest częstą pułapką przy mieszaniu różnych wersji C++ lub wersji kompilatorów, ponieważ może prowadzić do niedopasowania ABI. Użycie `const char*` i kilku funkcji pomocniczych pozwala tego uniknąć.

### Ukrywaj funkcje

Jeśli to możliwe, używaj słowa kluczowego `static` dla funkcji lokalnych względem danej jednostki kompilacji. Pozwala to kompilatorowi na pewne optymalizacje, co może zarówno poprawić wydajność, jak i zmniejszyć rozmiar pliku wykonywalnego.

## Biblioteki firm trzecich

Wybierając bibliotekę firm trzecich do użycia, niezależnie od języka, rozważ następujące kwestie:

* Funkcjonalność - Czy rozwiązuje konkretny problem, który masz?
* Wydajność - Czy powoduje narzut wydajnościowy podczas działania?
* Rozmiar biblioteki - O ile większy będzie końcowy plik wykonywalny? Czy to akceptowalne?
* Zależności - Czy wymaga dodatkowych bibliotek?
* Wsparcie - W jakim stanie jest biblioteka? Czy ma wiele otwartych zgłoszeń? Czy jest nadal utrzymywana?
* Licencja - Czy można jej użyć w tym projekcie?


## Zależności open source

Zawsze upewnij się, że masz dostęp do swoich zależności. Na przykład jeśli zależysz od czegoś na GitHubie, nic nie stoi na przeszkodzie, aby to repozytorium zostało usunięte albo nagle zmieniło kierunek rozwoju lub właściciela. Możesz ograniczyć to ryzyko, tworząc fork repozytorium i używając własnego forka zamiast projektu upstream.

Pamiętaj, że kod z biblioteki zostanie wstrzyknięty do twojej gry, więc upewnij się, że biblioteka robi to, co powinna, i nic więcej!
