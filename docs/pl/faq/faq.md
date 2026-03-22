---
title: FAQ o silniku i edytorze Defold
brief: Najczęściej zadawane pytania o silnik gry Defold, edytor i platformę.
---

# Najczęściej zadawane pytania

## Pytania ogólne

#### P: Czy Defold naprawdę jest darmowy?

A: Tak, silnik i edytor Defold z pełną funkcjonalnością są całkowicie bezpłatne. Bez ukrytych kosztów, opłat ani tantiem. Po prostu za darmo.


#### P: Dlaczego Defold Foundation miałaby udostępniać Defold za darmo?

A: Jednym z celów [Defold Foundation](/foundation) jest zapewnienie, że oprogramowanie Defold będzie dostępne dla deweloperów na całym świecie, a kod źródłowy będzie dostępny bezpłatnie.


#### P: Jak długo będziecie wspierać Defold?

A: Jesteśmy mocno zaangażowani w Defold. [Defold Foundation](/foundation) została powołana tak, aby przez wiele kolejnych lat pozostawać odpowiedzialnym właścicielem silnika Defold. Nie zniknie.


#### P: Czy mogę zaufać Defold w profesjonalnej produkcji?

A: Oczywiście. Defold jest używany przez coraz większą liczbę profesjonalnych twórców gier i studiów. Zobacz [galerię gier](/showcase), aby znaleźć przykłady gier stworzonych w Defold.


#### P: Jakiego rodzaju śledzenie użytkowników prowadzicie?

A: Rejestrujemy anonimowe dane użycia z naszych stron internetowych i edytora Defold, aby ulepszać nasze usługi i produkt. W grach, które tworzysz, nie ma śledzenia użytkowników, chyba że sam dodasz usługę analityczną. Więcej informacji znajdziesz w naszej [Polityce prywatności](/privacy-policy).


#### P: Kto stworzył Defold?

A: Defold został stworzony przez Ragnara Svenssona i Christiana Murraya. Zaczęli pracować nad silnikiem, edytorem i serwerami w 2009 roku. W 2013 roku King nawiązało współpracę z Defold, a w 2014 roku przejęło Defold. Przeczytaj pełną historię [tutaj](/about).


## Pytania o tworzenie gier

#### P: Czy mogę tworzyć gry 3D w Defold?

A: Oczywiście! Silnik jest pełnoprawnym silnikiem 3D. Zestaw narzędzi jest jednak przygotowany głównie pod 2D, więc wiele rzeczy trzeba będzie zrobić samodzielnie. Lepsze wsparcie 3D jest planowane.


## Pytania o język programowania

#### P: W jakim języku programowania pracuje się w Defold?

A: Logika gry w projekcie Defold jest przede wszystkim pisana w języku Lua, konkretnie Lua 5.1/LuaJIT. Szczegóły znajdziesz w [podręczniku Lua](/manuals/lua). Lua to lekki, dynamiczny język, który jest szybki i bardzo wydajny. Od wersji 1.8.1 Defold obsługuje użycie transpilerów generujących kod Lua. Po zainstalowaniu rozszerzenia do transpilacji możesz używać alternatywnych języków, takich jak [Teal](https://github.com/defold/extension-teal), do pisania statycznie sprawdzanego Lua. Możesz też używać kodu natywnego (C/C++, Objective-C, Java i JavaScript w zależności od platformy), aby [rozszerzać silnik Defold o nową funkcjonalność](/manuals/extensions/). Przy tworzeniu [własnych materiałów](/manuals/material/) używany jest język shaderów OpenGL ES SL do pisania shaderów wierzchołków i fragmentów.


#### P: Czy mogę używać C++ do pisania logiki gry?

A: Obsługa C++ w Defold służy głównie do pisania rozszerzeń natywnych, które integrują się z SDK innych firm lub platformowymi API. [dmSDK](https://defold.com/ref/stable/dmGameObject/) (API C++ dla Defold używane w rozszerzeniach natywnych) będzie stopniowo rozbudowywane o kolejne funkcje, tak aby w przyszłości dało się pisać całą logikę gry w C++, jeśli deweloper będzie tego chciał. Lua pozostanie głównym językiem do logiki gry, ale dzięki rozbudowanemu API C++ będzie można pisać logikę gry także w C++. Prace nad rozbudową API C++ polegają głównie na przenoszeniu istniejących prywatnych plików nagłówkowych do sekcji publicznej i porządkowaniu API do publicznego użytku.


#### P: Czy mogę używać TypeScript z Defold?

A: TypeScript nie jest oficjalnie obsługiwany. Społeczność utrzymuje zestaw narzędzi [ts-defold](https://ts-defold.dev/) do pisania w TypeScript i transpilowania go do Lua bezpośrednio z VSCode.


#### P: Czy mogę używać Haxe z Defold?

A: Haxe nie jest oficjalnie obsługiwany. Społeczność utrzymuje [hxdefold](https://github.com/hxdefold/hxdefold) do pisania w Haxe i transpilowania go do Lua.


#### P: Czy mogę używać C# z Defold?

A: Defold Foundation doda obsługę C# i udostępni ją jako zależność biblioteczną. C# to szeroko stosowany język programowania i pomoże studiom oraz deweloperom mocno zainwestowanym w C# przejść na Defold.


#### P: Obawiam się, że dodanie obsługi C# negatywnie wpłynie na Defold. Czy powinienem się martwić?

A: Defold NIE odchodzi od Lua jako głównego języka skryptowego. Obsługa C# zostanie dodana jako nowy język dla rozszerzeń. Nie wpłynie na silnik, chyba że zdecydujesz się używać rozszerzeń C# w swoim projekcie.

Obsługa C# będzie miała swoją cenę, na przykład większy rozmiar pliku wykonywalnego czy wpływ na wydajność w czasie działania, ale to już decyzja konkretnego dewelopera lub studia.

Samo dodanie C# to stosunkowo niewielka zmiana, ponieważ system rozszerzeń już obsługuje wiele języków (C/C++, Java, Objective-C, Zig). Generowane wiązania C# pozwolą utrzymać SDK w synchronizacji. Dzięki temu te wiązania pozostaną aktualne przy minimalnym nakładzie pracy.

Defold Foundation wcześniej była przeciwna dodaniu obsługi C# w Defold, ale zmieniła zdanie z kilku powodów:

* Studia i deweloperzy nadal proszą o obsługę C#.
* Obsługa C# została ograniczona wyłącznie do rozszerzeń, czyli przy niskim nakładzie pracy.
* Główny silnik nie ulegnie zmianie.
* API C# można utrzymywać w synchronizacji przy minimalnym nakładzie pracy, jeśli jest generowane.
* Obsługa C# będzie oparta na DotNet 9 z NativeAOT, co wygeneruje biblioteki statyczne, do których istniejący potok budowania może linkować, tak jak do każdego innego rozszerzenia Defold.


## Pytania o platformy

#### P: Na jakich platformach działa Defold?

A: Następujące platformy są obsługiwane przez edytor i narzędzia oraz przez środowisko uruchomieniowe silnika:

  | System             | Wersja             | Architektury       | Obsługiwane        |
  | ------------------ | ------------------ | ------------------ | ------------------ |
  | macOS              | 11 Big Sur         | `x86-64`, `arm-64` | Edytor i silnik    |
  | Windows            | Vista              | `x86-32`, `x86-64` | Edytor i silnik    |
  | Ubuntu (1)         | 22.04 LTS          | `x86-64`           | Edytor             |
  | Linux (2)          | Dowolna            | `x86-64`, `arm-64` | Silnik             |
  | iOS                | 15.0               | `arm-64`  `x86_64` | Silnik             |
  | Android            | 5.0 (API level 21) | `arm-32`, `arm-64` | Silnik             |
  | HTML5              |                    | `asm.js`, `wasm`   | Silnik             |

  (1 Edytor jest budowany i testowany dla 64-bitowego Ubuntu. Powinien też działać na innych dystrybucjach, ale nie dajemy żadnych gwarancji.)

  (2 Środowisko uruchomieniowe silnika powinno działać na większości 64-bitowych dystrybucji Linuksa, o ile sterowniki graficzne są aktualne. Więcej informacji znajdziesz poniżej, w sekcji o API graficznych.)


#### P: Na jakie platformy docelowe mogę tworzyć gry z Defold?

A: Jednym kliknięciem możesz publikować na PS4™, PS5™, Nintendo Switch, iOS (64-bit), Android (32-bit i 64-bit) oraz HTML5, a także na macOS (x86-64 i arm64), Windows (32-bit i 64-bit) i Linux (x86-64 i arm64). To naprawdę jedna baza kodu i wiele obsługiwanych platform.


#### P: Jakiego API renderowania używa Defold?

A: Jako deweloper pracujesz tylko z jednym API renderowania, korzystając z [w pełni skryptowalnego potoku renderowania](/manuals/render/). API skryptu renderowania w Defold tłumaczy operacje renderowania na następujące API graficzne:

:[API graficzne](../shared/graphics-api.md)

#### P: Czy mogę sprawdzić, jaką wersję uruchamiam?

A: Tak, wybierz opcję <kbd>Help ▸ About</kbd> w menu <kbd>Help</kbd>. Okno wyraźnie pokazuje wersję beta Defold i, co ważniejsze, konkretny SHA1 wydania. Aby odczytać wersję środowiska uruchomieniowego, użyj [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info).

Najnowszą wersję beta dostępną do pobrania z http://d.defold.com/beta można sprawdzić, otwierając http://d.defold.com/beta/info.json. Ten sam plik istnieje także dla wersji stabilnych: http://d.defold.com/stable/info.json


#### P: Czy da się sprawdzić, na jakiej platformie działa gra w czasie uruchomienia?

A: Tak, zobacz [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info).


## Pytania o edytor
:[FAQ dotyczące edytora](../shared/editor-faq.md)


## Pytania o Linuksa
:[FAQ dotyczące Linuksa](../shared/linux-faq.md)


## Pytania o Androida
:[FAQ dotyczące Androida](../shared/android-faq.md)


## Pytania o HTML5
:[FAQ dotyczące HTML5](../shared/html5-faq.md)


## Pytania o iOS
:[FAQ dotyczące iOS](../shared/ios-faq.md)


## Pytania o Windows
:[FAQ dotyczące Windows](../shared/windows-faq.md)


## Pytania o konsole
:[FAQ dotyczące konsol](../shared/consoles-faq.md)


## Publikowanie gier

#### P: Próbuję opublikować moją grę w App Store. Jak powinienem odpowiedzieć na IDFA?

A: Podczas przesyłania aplikacji Apple pokazuje trzy pola wyboru dla trzech poprawnych przypadków użycia IDFA:

  1. Wyświetlanie reklam w aplikacji
  2. Atrybucja instalacji na podstawie reklam
  3. Atrybucja działań użytkownika na podstawie reklam

  Jeśli zaznaczysz opcję 1, recenzent aplikacji będzie szukał reklam w aplikacji. Jeśli twoja gra nie wyświetla reklam, może zostać odrzucona. Sam Defold nie używa identyfikatora reklamowego.


#### P: Jak mogę monetyzować swoją grę?

A: Defold obsługuje zakupy w aplikacji oraz różne rozwiązania reklamowe. Sprawdź kategorię [Monetization](https://defold.com/tags/stars/monetization/) w Asset Portal, aby zobaczyć aktualną listę dostępnych opcji monetyzacji.


## Błędy podczas korzystania z Defold

#### P: Nie mogę uruchomić gry i nie ma błędu budowania. Co jest nie tak?

A: Proces budowania może w rzadkich przypadkach nie przebudować plików, jeśli wcześniej wystąpiły błędy budowania, które już naprawiłeś. Wymuś pełną przebudowę, wybierając <kbd>Project ▸ Rebuild And Launch</kbd> z menu.



## Zawartość gry

#### P: Czy Defold obsługuje prefaby?

A: Tak. Nazywają się [kolekcje](/manuals/building-blocks/#collections). Pozwalają tworzyć złożone hierarchie obiektów gry i przechowywać je jako oddzielne elementy składowe, które można instancjonować w edytorze lub w czasie działania programu, przez tworzenie instancji kolekcji. Dla węzłów GUI dostępne są szablony GUI.


#### P: Dlaczego nie mogę dodać obiektu gry jako dziecka innego obiektu gry?

A: Najprawdopodobniej próbujesz dodać obiekt podrzędny w pliku obiektu gry, a to nie jest możliwe. Żeby zrozumieć dlaczego, trzeba pamiętać, że hierarchie rodzic-dziecko są wyłącznie hierarchią transformacji grafu sceny. Obiekt gry, który nie został umieszczony (lub utworzony dynamicznie) w scenie (kolekcji), nie należy do grafu sceny, więc nie może być częścią takiej hierarchii.


#### P: Dlaczego nie mogę rozsyłać wiadomości do wszystkich dzieci obiektu gry?

A: Relacje rodzic-dziecko wyrażają wyłącznie relacje transformacji w grafie sceny i nie należy ich mylić z agregatami obiektów w programowaniu obiektowym. Jeśli skupisz się na danych swojej gry i na tym, jak najlepiej je przekształcać, gdy gra zmienia stan, prawdopodobnie rzadziej będziesz musiał wysyłać wiadomości z danymi stanu do wielu obiektów jednocześnie. Tam, gdzie potrzebujesz hierarchii danych, można je łatwo tworzyć i obsługiwać w Lua.


#### P: Dlaczego widzę artefakty wizualne wokół krawędzi moich sprite'ów?

A: To artefakt wizualny nazywany `edge bleeding`, w którym piksele z krawędzi sąsiednich obrazów w atlasie przenikają do obrazu przypisanego do sprite'a. Rozwiązaniem jest dodanie dodatkowych wierszy i kolumn identycznych pikseli na obrzeżach obrazów atlasu. Na szczęście można to zrobić automatycznie w edytorze atlasu w Defold. Otwórz atlas i ustaw wartość <kbd>Extrude Borders</kbd> na `1`.


#### P: Czy mogę barwić sprite'y albo uczynić je przezroczystymi, czy muszę napisać do tego własny shader?

A: Wbudowany shader sprite'a, używany domyślnie dla wszystkich sprite'ów, ma zdefiniowaną stałą `tint`:

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### P: Jeśli ustawię współrzędną Z sprite'a na 100, to nie będzie renderowany. Dlaczego?

A: Pozycja Z obiektu gry kontroluje kolejność renderowania. Niższe wartości są rysowane przed wyższymi. W domyślnym skrypcie do renderowania rysowane są obiekty gry o głębokości od -1 do 1, a wszystko poza tym zakresem nie zostanie narysowane. Więcej o skrypcie do renderowania przeczytasz w oficjalnej [dokumentacji renderowania](/manuals/render). W przypadku węzłów GUI wartość Z jest ignorowana i w ogóle nie wpływa na kolejność renderowania. Zamiast tego węzły są renderowane w kolejności, w jakiej widnieją na liście, oraz zgodnie z hierarchią węzłów podrzędnych i warstwami. Więcej o renderowaniu GUI i optymalizacji wywołań rysowania z użyciem warstw przeczytasz w oficjalnej [dokumentacji GUI](/manuals/gui).


#### P: Czy zmiana zakresu Z projekcji widoku na zakres od -100 do 100 wpłynęłaby na wydajność?

A: Nie. Jedyny efekt dotyczy precyzji. Bufor Z jest logarytmiczny i ma bardzo wysoką rozdzielczość wartości Z blisko 0 oraz mniejszą rozdzielczość dalej od 0. Na przykład przy 24-bitowym buforze wartości 10.0 i 10.000005 można odróżnić, natomiast 10000 i 10005 już nie.


#### P: Dlaczego sposób reprezentacji kątów jest niespójny?

A: W rzeczywistości istnieje spójność. Kąty są wszędzie w edytorze i w API gry wyrażane w stopniach. Biblioteki matematyczne używają radianów. Obecnie wyjątek stanowi właściwość fizyki `angular_velocity`, która jest wyrażana w radianach/s. To ma się zmienić.


#### P: Gdy tworzę węzeł GUI typu box z samym kolorem, bez tekstury, jak będzie renderowany?

A: To po prostu kształt pokolorowany wierzchołkami. Trzeba jednak pamiętać, że nadal będzie to kosztować fill-rate.


#### P: Jeśli w locie zmienię zasoby, czy silnik automatycznie je zwolni?

A: Wszystkie zasoby są wewnętrznie objęte zliczaniem referencji. Gdy tylko licznik referencji spadnie do zera, zasób zostaje zwolniony.


#### P: Czy można odtwarzać dźwięk bez używania komponentu dźwięku dołączonego do obiektu gry?

A: W Defold wszystko jest oparte na komponentach. Można utworzyć pusty obiekt gry z wieloma dźwiękami i odtwarzać je, wysyłając wiadomości do obiektu sterującego dźwiękiem.


#### P: Czy można w czasie działania zmienić plik dźwiękowy powiązany z komponentem dźwięku?

A: Zasadniczo wszystkie zasoby są deklarowane statycznie, dzięki czemu zarządzanie nimi dostajesz za darmo. Możesz użyć [właściwości zasobów](/manuals/script-properties/#resource-properties), aby zmienić zasób przypisany do komponentu.


#### P: Czy istnieje sposób na dostęp do właściwości kształtu kolizji w fizyce?

A: Nie, obecnie nie jest to możliwe.


#### P: Czy istnieje jakiś szybki sposób na renderowanie obiektów kolizji w mojej scenie? (jak debug draw w Box2D)

A: Tak, ustaw flagę `physics.debug` w `game.project`. (Zobacz oficjalną [dokumentację ustawień projektu](/manuals/project-settings/#debug))


#### P: Jakie są koszty wydajnościowe wielu kontaktów i kolizji?

A: Defold uruchamia w tle zmodyfikowaną wersję Box2D, więc koszt wydajnościowy powinien być bardzo podobny. Zawsze możesz sprawdzić, ile czasu silnik spędza na fizyce, otwierając [profiler](/manuals/debugging). Powinieneś też wziąć pod uwagę, jakich obiektów kolizji używasz. Na przykład obiekty statyczne są tańsze wydajnościowo. Zobacz oficjalną [dokumentację fizyki](/manuals/physics) w Defold, aby uzyskać więcej szczegółów.


#### P: Jaki jest wpływ na wydajność wielu komponentów efektów cząsteczkowych?

A: To zależy od tego, czy są odtwarzane, czy nie. ParticleFX, który nie jest odtwarzany, nie ma żadnego kosztu wydajnościowego. Wpływ odtwarzanego ParticleFX trzeba ocenić za pomocą profilera, ponieważ zależy od jego konfiguracji. Jak w większości innych przypadków pamięć jest rezerwowana z góry dla liczby komponentów ParticleFX zdefiniowanej jako `max_count` w `game.project`.


#### P: Jak mogę odbierać wejście w obiekcie gry wewnątrz kolekcji załadowanej przez pełnomocnika kolekcji?

A: Każda kolekcja załadowana przez pełnomocnika kolekcji ma własny stos wejścia. Wejście jest kierowane ze stosu wejścia głównej kolekcji przez komponent pełnomocnika kolekcji do obiektów w kolekcji. Oznacza to, że nie wystarczy, aby obiekt gry w załadowanej kolekcji przejął skupienie wejścia. Obiekt gry, który _zawiera_ komponent pełnomocnika kolekcji, również musi przejąć skupienie wejścia. Zobacz [dokumentację wejścia](/manuals/input), aby uzyskać szczegóły.


#### P: Czy mogę używać właściwości skryptowych typu string?

A: Nie. Defold obsługuje właściwości typu [hash](/ref/builtins#hash). Można ich używać do oznaczania typów, identyfikatorów stanu lub dowolnych kluczy. Hashe można też wykorzystywać do przechowywania identyfikatorów obiektów gry (ścieżek), choć często lepsze są właściwości [url](/ref/msg#msg.url), ponieważ edytor automatycznie wypełnia listę rozwijaną odpowiednimi adresami URL. Zobacz [dokumentację właściwości skryptowych](/manuals/script-properties), aby uzyskać szczegóły.


#### P: Jak uzyskać dostęp do poszczególnych komórek macierzy (utworzonej za pomocą [`vmath.matrix4()`](/ref/vmath/#vmath.matrix4:m1) lub podobnej)?

A: Dostęp do komórek uzyskujesz przez `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` itd.


#### P: Dostaję komunikat `Not enough resources to clone the node` podczas używania [gui.clone()](/ref/gui/#gui.clone:node) lub [gui.clone_tree()](/ref/gui/#gui.clone_tree:node)

A: Zwiększ wartość `Max Nodes` komponentu GUI. Znajdziesz ją w panelu `Properties`, gdy zaznaczysz korzeń komponentu w `Outline`.


## Forum

#### P: Czy mogę założyć wątek, w którym reklamuję swoją pracę?

A: Oczywiście! Mamy do tego specjalną kategorię ["Work for hire"](https://forum.defold.com/c/work-for-hire). Zawsze wspieramy wszystko, co służy społeczności, a oferowanie swoich usług społeczności, za wynagrodzeniem lub bez, jest tego dobrym przykładem.


#### P: Założyłem wątek i dodałem swoją pracę. Czy mogę dodać więcej?

A: Aby ograniczyć podbijanie wątków z kategorii "Work for hire", nie możesz pisać w swoim własnym wątku częściej niż raz na 14 dni, chyba że jest to bezpośrednia odpowiedź na komentarz w wątku, wtedy możesz odpowiedzieć. Jeśli chcesz dodać dodatkową pracę do wątku w ciągu 14 dni, musisz edytować istniejące posty i dopisać do nich nową treść.


#### P: Czy mogę użyć kategorii „Work for hire” do publikowania ofert pracy?

A: Jasne, śmiało! Można jej używać zarówno do ofert, jak i do próśb o współpracę, na przykład: „Programista szuka grafika 2D specjalizującego się w pixel arcie. Mam pieniądze i dobrze zapłacę”.
