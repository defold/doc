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

Jeśli dana platforma nie powinna obsługiwać rozszerzenia, zaleca się po prostu nie rejestrować modułu Lua. Dzięki temu można wykryć obsługę, sprawdzając nil:

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
        /main                            -- Wszystkie pliki właściwego projektu przykładowego
            /...
        /myextension                     -- Rzeczywisty katalog główny rozszerzenia
            ext.manifest
            /include                     -- Zewnętrzne pliki include używane przez inne rozszerzenia
            /libs
                /<platform>              -- Zewnętrzne biblioteki dla wszystkich obsługiwanych platform
            /src
                myextension.cpp          -- API Lua rozszerzenia i funkcje cyklu życia rozszerzenia
                                            Zawiera też ogólne implementacje funkcji API Lua.
                myextension_private.h    -- Twoje wewnętrzne API, które zaimplementuje każda platforma (np. `myextension_Init` itd.)
                myextension.mm           -- Potrzebny, jeśli dla iOS/macOS są wymagane natywne wywołania. Implementuje `myextension_Init` itd. dla iOS/macOS
                myextension_android.cpp  -- Potrzebny, jeśli dla Androida są wymagane wywołania JNI. Implementuje `myextension_Init` itd. dla Androida
                /java
                    /<platform>          -- Dowolne pliki Java potrzebne dla Androida
            /res                         -- Dowolne zasoby potrzebne dla danej platformy
            /external
                README.md                -- Notatki/skrypty dotyczące tego, jak budować lub pakować zewnętrzne biblioteki
        /bundleres                       -- Zasoby, które powinny zostać dołączone do bundla (zob. game.project oraz [bundle_resources setting]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Dodatkowe informacje o konfiguracji aplikacji
```

Zwróć uwagę, że `myextension.mm` i `myextension_android.cpp` są potrzebne tylko wtedy, gdy wykonujesz konkretne natywne wywołania dla danej platformy.

#### Foldery platform

W niektórych miejscach architektura platformy jest używana jako nazwa folderu, aby określić, których plików użyć podczas kompilacji lub bundlowania aplikacji. Mają one postać:

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

W kodzie źródłowym Defold C++ jest używany bardzo oszczędnie, a większość kodu ma bardzo C-podobny charakter. Szablonów prawie się tam nie stosuje, z wyjątkiem kilku klas kontenerów, ponieważ szablony zwiększają zarówno czas kompilacji, jak i rozmiar pliku wykonywalnego.

### Wersja C++

Kod źródłowy Defold jest budowany z użyciem domyślnej wersji C++ każdego kompilatora. Sam kod źródłowy Defold nie używa wersji C++ wyższej niż C++98. Chociaż do zbudowania rozszerzenia można użyć nowszej wersji, może ona wiązać się ze zmianami ABI. To może uniemożliwić używanie jednego rozszerzenia razem z innymi rozszerzeniami w silniku lub z [asset portal](/assets).

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
