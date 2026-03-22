---
title: Samouczek gry z niekończącym się biegiem
brief: W tym samouczku zaczniesz od pustego projektu i zbudujesz kompletną grę z niekończącym się biegiem, z animowaną postacią, kolizjami fizycznymi, przedmiotami do zbierania i punktacją.
---

# Samouczek gry z niekończącym się biegiem

W tym samouczku zaczniemy od pustego projektu i zbudujemy kompletną grę z niekończącym się biegiem, z animowaną postacią, kolizjami fizycznymi, przedmiotami do zbierania i punktacją.

W trakcie nauki nowego silnika gier trzeba przyswoić sporo rzeczy, dlatego przygotowaliśmy ten samouczek, aby ułatwić ci start. To dość kompletny przewodnik pokazujący, jak działa silnik i edytor. Zakładamy, że masz już pewną znajomość programowania.

Jeśli potrzebujesz wprowadzenia do programowania w Lua, zajrzyj do naszego [podręcznika Lua w Defold](/manuals/lua).

Jeśli czujesz, że ten samouczek to na początek zbyt dużo, zajrzyj na naszą [stronę z samouczkami](//www.defold.com/tutorials), gdzie znajdziesz zestaw materiałów o różnym poziomie trudności.

Jeśli wolisz oglądać samouczki wideo, zajrzyj do [wersji wideo na YouTube](https://www.youtube.com/playlist?list=PLXsXu5srjNlxtYPQ_YJQSxJG2AN9OVS5b).

Korzystamy z zasobów gry z dwóch innych samouczków, wprowadzając przy tym kilka drobnych zmian. Samouczek jest podzielony na kilka kroków, a każdy z nich prowadzi nas znacząco bliżej końcowej gry.

Efektem końcowym będzie gra, w której sterujesz bohaterem biegnącym przez otoczenie, zbierającym monety i omijającym przeszkody. Bohater porusza się ze stałą prędkością, a gracz kontroluje wyłącznie skok bohatera, naciskając jeden przycisk (albo dotykając ekranu na urządzeniu mobilnym). Poziom składa się z nieskończonego ciągu platform, po których można skakać, oraz monet do zebrania.

Jeśli na dowolnym etapie utkniesz w tym samouczku albo podczas tworzenia własnej gry, nie wahaj się poprosić nas o pomoc na [Forum Defold](//forum.defold.com). Na forum możesz rozmawiać o Defold, prosić zespół Defold o pomoc, zobaczyć, jak inni twórcy gier rozwiązali swoje problemy, i znaleźć nowe inspiracje. Zacznij już teraz.

::: sidenote
W całym samouczku szczegółowe opisy pojęć i sposobów wykonania niektórych kroków są oznaczone właśnie w ten sposób. Jeśli uznasz, że te sekcje wchodzą w zbyt duży szczegół, po prostu je pomiń.
:::

Zacznijmy więc. Mamy nadzieję, że przejście przez ten samouczek sprawi ci dużo radości i pomoże ci ruszyć z Defold.

> Pobierz zasoby do tego samouczka [tutaj](https://github.com/defold/sample-runner/tree/main/def-runner).

## KROK 1 - Instalacja i konfiguracja

Pierwszym krokiem jest [pobranie następujących plików](https://github.com/defold/sample-runner/tree/main/def-runner).

Jeśli jeszcze nie pobrałeś i nie zainstalowałeś edytora Defold, to czas to zrobić:

:[install](../shared/install.md)

Gdy edytor jest już zainstalowany i uruchomiony, pora utworzyć nowy projekt i przygotować go do pracy. Utwórz [nowy projekt](/manuals/project-setup/#creating-a-new-project) z szablonu "Empty Project".

::: sidenote
Ten samouczek korzysta z funkcji Spine, które od wersji Defold 1.2.188 zostały przeniesione do własnego rozszerzenia. Jeśli używasz nowszej wersji, dodaj [Spine Extension](https://github.com/defold/extension-spine) do sekcji zależności w *game.project*.
:::

## Edytor

Gdy uruchamiasz edytor po raz pierwszy, startuje on pusty, bez otwartego projektu, więc wybierz z menu <kbd>Open Project</kbd> i wskaż nowo utworzony projekt. Zostaniesz też poproszony o utworzenie dla projektu "branch".

W panelu *Assets pane* zobaczysz wszystkie pliki należące do projektu. Jeśli dwukrotnie klikniesz plik "main/main.collection", otworzy się on w centralnym widoku edytora:

![Widok edytora](images/runner/1/editor2_overview.png)

Edytor składa się z następujących głównych obszarów:

Assets pane
: To widok wszystkich plików w twoim projekcie. Różne typy plików mają różne ikony. Kliknij plik dwukrotnie, aby otworzyć go w odpowiednim edytorze dla tego typu. Specjalny, tylko do odczytu folder *builtins* jest wspólny dla wszystkich projektów i zawiera przydatne elementy, takie jak domyślny skrypt do renderowania, font, materiały do renderowania różnych komponentów i inne rzeczy.

Główny widok edytora
: W zależności od typu edytowanego pliku ten widok pokazuje edytor dla danego typu. Najczęściej używany jest tu edytor sceny, który widzisz na ilustracji. Każdy otwarty plik jest pokazany w osobnej karcie.

Zmienione pliki
: Zawiera listę wszystkich zmian, które wprowadziłeś w swojej gałęzi od ostatniej synchronizacji. Jeśli więc widzisz coś w tym panelu, oznacza to, że masz zmiany, których jeszcze nie ma na serwerze. Możesz otworzyć różnicę wyświetlaną tylko jako tekst i wycofać zmiany przez ten widok.

Outline
: Hierarchiczny widok zawartości aktualnie edytowanego pliku. Możesz przez ten widok dodawać, usuwać, modyfikować i zaznaczać obiekty oraz komponenty.

Properties
: Właściwości ustawione na aktualnie zaznaczonym obiekcie lub komponencie.

Konsola
: Podczas uruchamiania gry ten widok przechwytuje dane wyjściowe z silnika gry, takie jak logi, błędy i informacje diagnostyczne, a także wszystkie własne komunikaty debugowania `print()` i `pprint()` pochodzące ze skryptów. Jeśli aplikacja lub gra nie chce się uruchomić, konsola jest pierwszym miejscem, które warto sprawdzić. Za konsolą znajduje się zestaw kart pokazujących informacje o błędach, a także edytor krzywych używany podczas tworzenia efektów cząsteczkowych.

## Uruchamianie gry

Szablon projektu "Empty" jest w rzeczywistości całkowicie pusty. Mimo to wybierz <kbd>Project ▸ Build</kbd>, aby zbudować projekt i uruchomić grę.

![Budowanie](images/runner/1/build_and_launch.png)

Czarny ekran może nie wyglądać zbyt ekscytująco, ale to działająca aplikacja gry w Defold i możemy łatwo zmodyfikować ją w coś ciekawszego. Zróbmy więc to.

::: sidenote
Edytor Defold pracuje na plikach. Dwukrotne kliknięcie pliku w *Assets pane* otwiera go w odpowiednim edytorze. Następnie możesz pracować z zawartością tego pliku.

Gdy skończysz edycję pliku, musisz go zapisać. Wybierz <kbd>File ▸ Save</kbd> z głównego menu. Edytor daje podpowiedź, dodając gwiazdkę `'*'` do nazwy pliku na karcie każdego pliku, który zawiera niezapisane zmiany.

![Plik z niezapisanymi zmianami](images/runner/1/file_changed.png)
:::

## Konfiguracja projektu

Zanim zaczniemy, ustawmy kilka parametrów naszego projektu. Otwórz zasób *game.project* z panelu *Assets pane* i przewiń do sekcji Display. Ustaw `width` i `height` projektu odpowiednio na `1280` i `720`.

Musisz też dodać do projektu rozszerzenie Spine, abyśmy mogli animować postać bohatera. Dodaj wersję rozszerzenia Spine zgodną z wersją edytora Defold, którą masz zainstalowaną. Dostępne wersje Spine możesz zobaczyć tutaj:

[https://github.com/defold/extension-spine/releases](https://github.com/defold/extension-spine/releases)

Kliknij prawym przyciskiem myszy link do pliku zip z wydaniem, którego chcesz użyć:

![Kliknij prawym przyciskiem i skopiuj link do wydania](images/runner/extension-spine-releases.png)

Dodaj link do wydania do listy [zależności game.project](/manuals/libraries/#setting-up-library-dependencies). Gdy rozszerzenie Spine zostanie dodane, musisz też zrestartować edytor, aby aktywować integrację edytora dołączoną do Spine Extension.


## KROK 2 - Tworzenie podłoża

Zróbmy pierwsze małe kroki i stwórzmy arenę dla naszej postaci, a właściwie fragment przewijanego podłoża. Zrobimy to w kilku etapach.

1. Zaimportuj zasoby graficzne do projektu, przeciągając pliki obrazów "ground01.png" i "ground02.png" (z podfolderu "level-images" w paczce zasobów) do odpowiedniego miejsca w projekcie, na przykład do folderu "images" wewnątrz folderu "main".
2. Utwórz nowy plik *Atlas*, który będzie przechowywał tekstury podłoża (kliknij prawym przyciskiem odpowiedni folder, na przykład folder *main*, w *Assets pane* i wybierz <kbd>New ▸ Atlas File</kbd>). Nazwij plik atlasu *level.atlas*.

  ::: sidenote
  *Atlas* to plik, który łączy zestaw oddzielnych obrazów w jeden większy plik graficzny. Robi się tak, aby oszczędzić miejsce i poprawić wydajność. Więcej o atlasach i innych funkcjach grafiki 2D przeczytasz w [dokumentacji grafiki 2D](/manuals/2dgraphics).
  :::

3. Dodaj obrazy podłoża do nowego atlasu, klikając prawym przyciskiem korzeń atlasu w *Outline* i wybierając <kbd>Add Images</kbd>. Wybierz zaimportowane obrazy i kliknij *OK*. Każdy obraz w atlasie jest teraz dostępny jako jednoramkowa animacja (obraz statyczny), której można używać w sprite'ach, efektach cząsteczkowych i innych elementach wizualnych. Zapisz plik.

  ![Utwórz nowy atlas](images/runner/1/new_atlas.png)

  ![Dodaj obrazy do atlasu](images/runner/1/add_images_to_atlas.png)

  ::: sidenote
  *Dlaczego to nie działa!?* Częsty problem osób zaczynających pracę z Defold polega na tym, że zapominają zapisać plik! Po dodaniu obrazów do atlasu musisz zapisać plik, zanim będziesz mógł uzyskać do tych obrazów dostęp.
  :::

4. Utwórz plik kolekcji *ground.collection* dla podłoża i dodaj do niego 7 obiektów gry (kliknij prawym przyciskiem korzeń kolekcji w widoku *Outline* i wybierz <kbd>Add Game Object</kbd>). Nazwij obiekty "ground0", "ground1", "ground2" itd., zmieniając właściwość *Id* w widoku *Properties*. Zwróć uwagę, że Defold automatycznie przypisuje nowym obiektom gry unikalne id.

5. Do każdego obiektu dodaj komponent sprite (kliknij prawym przyciskiem obiekt gry w widoku *Outline* i wybierz <kbd>Add Component</kbd>, następnie wybierz *Sprite* i kliknij *OK*), ustaw właściwość *Image* komponentu sprite na właśnie utworzony atlas i ustaw domyślną animację sprite'a na jeden z dwóch obrazów podłoża. Ustaw pozycję X _komponentu sprite_ (nie obiektu gry) na 190, a pozycję Y na 40. Ponieważ szerokość obrazu wynosi 380 pikseli i przesuwamy go w bok o połowę tej wartości, punkt zakotwiczenia obiektu gry znajdzie się na lewej krawędzi obrazu sprite'a.

  ![Utwórz kolekcję podłoża](images/runner/1/ground_collection.png)

6. Grafika, której używamy, jest trochę za duża, więc przeskaluj każdy obiekt gry do 60% (skalowanie 0.6 w X i Y, co daje fragmenty podłoża o szerokości 228 pikseli).

  ![Skalowanie podłoża](images/runner/1/scale_ground.png)

7. Ustaw wszystkie _obiekty gry_ w jednej linii. Ustaw pozycje X _obiektów gry_ (nie komponentów sprite) na 0, 228, 456, 684, 912, 1140 i 1368 (wielokrotności szerokości 228 pikseli).

  ::: sidenote
  Najłatwiej będzie najpierw utworzyć jeden kompletny, przeskalowany obiekt gry z komponentem sprite, a potem go skopiować. Zaznacz go w widoku *Outline*, a następnie wybierz <kbd>Edit ▸ Copy</kbd> i potem <kbd>Edit ▸ Paste</kbd>.

  Warto zauważyć, że jeśli chcesz większych lub mniejszych kafli, wystarczy zmienić skalowanie. Będzie to jednak wymagało również zmiany pozycji X wszystkich obiektów gry podłoża na wielokrotności nowej szerokości.
  :::

8. Zapisz plik, a następnie dodaj *ground.collection* do pliku *main.collection*: najpierw dwukrotnie kliknij plik *main.collection*, potem kliknij prawym przyciskiem korzeń obiektu w widoku *Outline* i wybierz <kbd>Add Collection From File</kbd>. W oknie dialogowym wybierz *ground.collection* i kliknij *OK*. Upewnij się, że umieszczasz *ground.collection* w pozycji 0, 0, 0, bo inaczej będzie wizualnie przesunięta. Zapisz ją.

9. Uruchom grę (<kbd>Project ▸ Build</kbd>), aby sprawdzić, że wszystko jest na miejscu.

  ![Nieruchome podłoże](images/runner/1/still_ground.png)

Na tym etapie możesz być już nieco zdezorientowany i zastanawiać się, czym właściwie są wszystkie rzeczy, które tworzymy, więc zatrzymajmy się na chwilę i przyjrzyjmy się najbardziej podstawowym elementom każdego projektu Defold:

Obiekty gry (Game objects)
: To rzeczy, które istnieją w uruchomionej grze. Każdy obiekt gry ma pozycję w przestrzeni 3D, obrót i skalowanie. Nie musi być wcale widoczny. Obiekt gry może zawierać dowolną liczbę _komponentów_, które dodają możliwości takie jak grafika (sprite'y, tilemapy, modele, modele Spine i efekty cząsteczkowe), dźwięki, fizykę, fabryki (do tworzenia nowych obiektów) i wiele innych. Można też dodawać komponenty _skryptów Lua_, aby nadać obiektowi gry zachowanie. Każdy obiekt gry, który istnieje w twoich grach, ma *id*, którego potrzebujesz, aby komunikować się z nim za pomocą przekazywania wiadomości.

Kolekcje (Collections)
: Kolekcje nie istnieją same z siebie w uruchomionej grze, ale służą do umożliwienia statycznego nazywania obiektów gry i jednocześnie do tworzenia wielu instancji tego samego obiektu gry. W praktyce kolekcje działają jako kontenery dla obiektów gry i innych kolekcji. Możesz używać kolekcji podobnie jak prototypów (w innych silnikach znanych też jako "prefaby" albo "blueprints") złożonych hierarchii obiektów gry i kolekcji. Przy starcie silnik wczytuje główną kolekcję i ożywia wszystko, co się w niej znajduje. Domyślnie jest to plik *main.collection* w folderze *main* projektu, ale możesz to zmienić w ustawieniach projektu.

Na razie te opisy prawdopodobnie wystarczą. Znacznie pełniejsze omówienie tych kwestii znajdziesz jednak w [podręczniku o blokach budujących](/manuals/building-blocks). Warto zajrzeć do niego później, aby lepiej zrozumieć, jak rzeczy działają w Defold.

## KROK 3 - Wprawianie podłoża w ruch

Teraz, gdy wszystkie fragmenty podłoża są już na miejscu, ich poruszanie jest dość proste. Chodzi o to: przesuwać elementy z prawej do lewej, a gdy któryś z nich dotrze do lewego skraju poza ekranem, przenieść go na prawy skraj. Aby poruszać wszystkimi tymi obiektami gry, potrzebujemy skryptu Lua, więc utwórzmy go:

1. Kliknij prawym przyciskiem folder *main* w *Assets pane* i wybierz <kbd>New ▸ Script File</kbd>. Nazwij nowy plik *ground.script*.
2. Kliknij dwukrotnie nowy plik, aby otworzyć edytor skryptu Lua.
3. Usuń domyślną zawartość pliku i wklej do niego poniższy kod Lua, a następnie zapisz plik.

```lua
-- plik: ground.script
local pieces = { "ground0", "ground1", "ground2", "ground3",
                    "ground4", "ground5", "ground6" } -- <1>

function init(self) -- <2>
    self.speed = 360  -- Prędkość w pikselach/s
end

function update(self, dt) -- <3>
    for i, p in ipairs(pieces) do -- <4>
        local pos = go.get_position(p)
        if pos.x <= -228 then -- <5>
            pos.x = 1368 + (pos.x + 228)
        end
        pos.x = pos.x - self.speed * dt -- <6>
        go.set_position(pos, p) -- <7>
    end
end
```
1. Zapisz id obiektów gry podłoża w tabeli Lua, abyśmy mogli po nich iterować.
2. Funkcja `init()` jest wywoływana, gdy obiekt gry "ożywa" w grze. Inicjalizujemy lokalną zmienną członka obiektu, która przechowuje prędkość podłoża.
3. `update()` jest wywoływana raz na klatkę, zwykle 60 razy na sekundę. `dt` zawiera liczbę sekund od poprzedniego wywołania.
4. Przejdź po wszystkich obiektach gry podłoża.
5. Zapisz bieżącą pozycję w lokalnej zmiennej, a potem jeśli bieżący obiekt znajduje się na lewym skraju, przenieś go na prawy skraj.
6. Zmniejsz bieżącą pozycję X o ustawioną prędkość. Pomnóż przez `dt`, aby uzyskać prędkość niezależną od liczby klatek, wyrażoną w pikselach/s.
7. Zaktualizuj pozycję obiektu nową wartością.

::: sidenote
Defold to szybki rdzeń silnika, który zarządza danymi i obiektami gry. Całą logikę lub zachowanie potrzebne w grze tworzysz w języku Lua. Lua to szybki i lekki język programowania, świetny do pisania logiki gier. Dostępnych jest wiele świetnych źródeł do nauki języka, na przykład książka [Programming in Lua](http://www.lua.org/pil/) oraz oficjalny [Lua reference manual](http://www.lua.org/manual/5.3/).

Defold dodaje do Lua zestaw API, a także system _przekazywania wiadomości_, który pozwala programować komunikację między obiektami gry. Szczegóły działania znajdziesz w [podręczniku o przekazywaniu wiadomości](/manuals/message-passing).
:::

::: sidenote
Możesz przełączać widoczność sekcji Assets Pane, Console i Outline w edytorze za pomocą klawiszy <kbd>F6</kbd>, <kbd>F7</kbd> i <kbd>F8</kbd> odpowiednio.
:::

Teraz, gdy mamy plik skryptu, powinniśmy dodać do niego referencję w komponencie obiektu gry. Dzięki temu skrypt będzie wykonywany jako część cyklu życia obiektu gry. Zrobimy to, tworząc nowy obiekt gry w *ground.collection* i dodając do niego komponent *Script*, który odwołuje się do właśnie utworzonego pliku skryptu Lua:

1. Kliknij prawym przyciskiem korzeń kolekcji i wybierz <kbd>Add Game Object</kbd>. Ustaw *id* obiektu na "controller".
2. Kliknij prawym przyciskiem obiekt "controller" i wybierz <kbd>Add Component from file</kbd>, a następnie wskaż plik *ground.script*.

![Kontroler podłoża](images/runner/1/ground_controller.png)

Teraz, gdy uruchomisz grę, obiekt gry "controller" uruchomi skrypt w swoim komponencie *Script*, przez co podłoże będzie płynnie przewijać się przez ekran.

## KROK 4 - Tworzenie postaci bohatera

Postać bohatera będzie obiektem gry złożonym z następujących komponentów:

*Spine Model*
: Daje nam małą postać w stylu papierowej lalki, której części ciała można płynnie i tanio animować.

*Collision Object*
: Będzie wykrywać kolizje między bohaterem a rzeczami w poziomie, po których może biegać, które są niebezpieczne albo które można podnieść.

*Script*
: Pobiera dane wejściowe użytkownika i reaguje na nie, sprawia, że bohater skacze, animuje się i obsługuje kolizje.

Zacznij od zaimportowania obrazów części ciała, a następnie dodaj je do nowego atlasu, który nazwiemy *hero.atlas*:

1. Utwórz nowy folder, klikając prawym przyciskiem w *Assets pane* i wybierając <kbd>New ▸ Folder</kbd>. Upewnij się, że nie wybierzesz wcześniej żadnego folderu, bo nowy folder zostanie utworzony wewnątrz zaznaczonego. Nazwij folder "hero".
2. Utwórz nowy plik atlasu, klikając prawym przyciskiem folder *hero* i wybierając <kbd>New ▸ Atlas File</kbd>. Nazwij plik *hero.atlas*.
3. Utwórz nowy podfolder *images* w folderze *hero*. Kliknij prawym przyciskiem folder *hero* i wybierz <kbd>New ▸ Folder</kbd>.
4. Przeciągnij obrazy części ciała z folderu *hero-images* w paczce zasobów do folderu *images*, który właśnie utworzyłeś w *Assets pane*.
5. Otwórz *hero.atlas*, kliknij prawym przyciskiem korzeń w *Outline* i wybierz <kbd>Add Images</kbd>. Zaznacz wszystkie obrazy części ciała i kliknij *OK*.
6. Zapisz plik atlasu.

![Atlas bohatera](images/runner/2/hero_atlas.png)

Musimy też zaimportować dane animacji Spine i skonfigurować dla nich *Spine Scene*:

1. Przeciągnij plik *hero.spinejson* (jest dołączony do paczki zasobów) do folderu *hero* w *Assets pane*.
2. Utwórz plik *Spine Scene*. Kliknij prawym przyciskiem folder *hero* i wybierz <kbd>New ▸ Spine Scene File</kbd>. Nazwij plik *hero.spinescene*.
3. Kliknij dwukrotnie nowy plik, aby go otworzyć i edytować *Spine Scene*.
4. Ustaw właściwość *spine_json* na zaimportowany plik JSON *hero.spinejson*. Kliknij właściwość, a potem przycisk wyboru pliku *...*, aby otworzyć przeglądarkę zasobów.
5. Ustaw właściwość *atlas*, aby wskazywała plik *hero.atlas*.
6. Zapisz plik.

![Scena Spine bohatera](images/runner/2/hero_spinescene.png)

::: sidenote
Plik *hero.spinejson* został wyeksportowany w formacie Spine JSON. Do tworzenia takich plików potrzebujesz oprogramowania Spine do animacji. Jeśli chcesz używać innego programu do animacji, możesz wyeksportować animacje jako sprite-sheety i używać ich jako animacji flip-book z zasobów *Tile Source* albo *Atlas*. Więcej informacji znajdziesz w podręczniku [Animacja](/manuals/animation).
:::

### Budowanie obiektu gry

Teraz możemy zacząć budować obiekt gry bohatera:

1. Utwórz nowy plik *hero.go* (kliknij prawym przyciskiem folder *hero* i wybierz <kbd>New ▸ Game Object File</kbd>).
2. Otwórz plik obiektu gry.
3. Dodaj do niego komponent *Spine Model*. (Kliknij prawym przyciskiem korzeń w *Outline* i wybierz <kbd>Add Component</kbd>, a następnie wybierz "Spine Model".)
4. Ustaw właściwość *Spine Scene* komponentu na plik *hero.spinescene*, który właśnie utworzyłeś, i wybierz "run_right" jako domyślną animację (poprawimy później prawidłowe sterowanie animacją).
5. Zapisz plik.

![Właściwości Spine Model](images/runner/2/spinemodel_properties.png)

Teraz czas dodać fizykę, aby kolizje działały:

1. Dodaj komponent *Collision Object* do obiektu gry bohatera. (Kliknij prawym przyciskiem korzeń w *Outline* i wybierz <kbd>Add Component</kbd>, a następnie wybierz "Collision Object")
2. Kliknij prawym przyciskiem nowy komponent i wybierz <kbd>Add Shape</kbd>. Dodaj dwa kształty, aby pokryć ciało postaci. Wystarczy kula i prostopadłościan.
3. Kliknij kształty i użyj *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>), aby ustawić je w odpowiednich miejscach.
4. Zaznacz komponent *Collision Object* i ustaw właściwość *Type* na "Kinematic".

::: sidenote
Kolizja "Kinematic" oznacza, że chcemy rejestrować zderzenia, ale silnik fizyki nie będzie automatycznie rozwiązywał kolizji ani symulował obiektów. Silnik fizyki obsługuje kilka różnych typów obiektów kolizji. Więcej o nich przeczytasz w [dokumentacji fizyki](/manuals/physics).
:::

Ważne jest, aby określić, z czym obiekt kolizji ma wchodzić w interakcję:

1. Ustaw właściwość *Group* na nową grupę kolizji o nazwie "hero".
2. Ustaw właściwość *Mask* na inną grupę, "geometry", z którą ten obiekt kolizji ma rejestrować zderzenia. Zwróć uwagę, że grupa "geometry" jeszcze nie istnieje, ale wkrótce dodamy do niej obiekty kolizji.

Na koniec utwórz nowy plik *hero.script* i dodaj go do obiektu gry.

1. Kliknij prawym przyciskiem folder *hero* w *Assets pane* i wybierz <kbd>New ▸ Script File</kbd>. Nazwij nowy plik *hero.script*.
2. Otwórz nowy plik, a następnie skopiuj i wklej do niego poniższy kod skryptu i zapisz plik. (Kod jest dość prosty, poza rozwiązaniem, które oddziela kształt kolizji bohatera od obiektu, z którym się on zderza. Odpowiada za to funkcja `handle_geometry_contact()`.)

![Obiekt gry bohatera](images/runner/2/hero_game_object.png)

::: sidenote
Powód, dla którego obsługujemy kolizję samodzielnie, jest taki, że gdybyśmy zamiast tego ustawili typ obiektu kolizji postaci na dynamiczny, silnik wykonałby newtonowską symulację zaangażowanych ciał. W grze takiej jak ta taka symulacja jest daleka od optymalnej, więc zamiast walczyć z silnikiem fizyki przy użyciu różnych sił, przejmujemy pełną kontrolę.

Aby to zrobić i poprawnie obsługiwać kolizje, potrzeba trochę matematyki wektorowej. Szczegółowe wyjaśnienie, jak rozwiązywać kolizje kinematyczne, znajdziesz w [dokumentacji fizyki](/manuals/physics#resolving-kinematic-collisions).
:::

```lua
-- grawitacja ściągająca gracza w dół, w pikselach/sˆ2
local gravity = -20

-- prędkość wybicia przy skoku, w pikselach/s
local jump_takeoff_speed = 900

function init(self)
    -- to mówi silnikowi, aby wysyłał wejście do on_input() w tym skrypcie
    msg.post(".", "acquire_input_focus")

    -- zapisz pozycję początkową
    self.position = go.get_position()

    -- śledź wektor ruchu i to, czy postać ma kontakt z podłożem
    self.velocity = vmath.vector3(0, 0, 0)
    self.ground_contact = false
end

function final(self)
    -- oddaj fokus wejścia, gdy obiekt zostanie usunięty
    msg.post(".", "release_input_focus")
end

function update(self, dt)
    local gravity = vmath.vector3(0, gravity, 0)

    if not self.ground_contact then
        -- zastosuj grawitację, jeśli nie ma kontaktu z podłożem
        self.velocity = self.velocity + gravity
    end

    -- zastosuj prędkość do postaci gracza
    go.set_position(go.get_position() + self.velocity * dt)

    -- zresetuj stan chwilowy
    self.correction = vmath.vector3()
    self.ground_contact = false
end

local function handle_geometry_contact(self, normal, distance)
    -- rzutuj wektor korekcji na normalną kontaktu
    -- (wektor korekcji jest wektorem zerowym dla pierwszego punktu kontaktu)
    local proj = vmath.dot(self.correction, normal)
    -- oblicz kompensację potrzebną dla tego punktu kontaktu
    local comp = (distance - proj) * normal
    -- dodaj ją do wektora korekcji
    self.correction = self.correction + comp
    -- zastosuj kompensację do postaci gracza
    go.set_position(go.get_position() + comp)
    -- sprawdź, czy normalna jest skierowana dostatecznie w górę, aby uznać, że gracz stoi na ziemi
    -- (0.7 odpowiada mniej więcej odchyleniu o 45 stopni od pionu)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- rzutuj prędkość na normalną
    proj = vmath.dot(self.velocity, normal)
    -- jeśli rzut jest ujemny, oznacza to, że część prędkości jest skierowana w stronę punktu kontaktu
    if proj < 0 then
        -- w takim przypadku usuń tę składową
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("contact_point_response") then
        -- sprawdź, czy otrzymaliśmy wiadomość o punkcie kontaktu; jedna wiadomość przypada na każdy punkt kontaktu
        if message.group == hash("geometry") then
            handle_geometry_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- pozwól skakać tylko z podłoża
    if self.ground_contact then
        -- ustaw prędkość wybicia
        self.velocity.y = jump_takeoff_speed
    end
end

local function abort_jump(self)
    -- skróć skok, jeśli nadal poruszamy się w górę
    if self.velocity.y > 0 then
        -- zmniejsz prędkość skierowaną w górę
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == hash("jump") or action_id == hash("touch") then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    end
end
```

1. Dodaj ten skrypt jako komponent *Script* do obiektu bohatera (kliknij prawym przyciskiem korzeń *hero.go* w widoku *Outline* i wybierz <kbd>Add Component from File</kbd>, a następnie wybierz plik *hero.script*).

Jeśli chcesz, możesz teraz tymczasowo dodać postać bohatera do głównej kolekcji i uruchomić grę, aby zobaczyć, jak spada przez świat.

Ostatnią rzeczą, której potrzebujemy, aby bohater działał poprawnie, jest wejście użytkownika. Powyższy skrypt zawiera już funkcję `on_input()`, która reaguje na akcje "jump" i "touch" (dla ekranów dotykowych). Dodajmy wiązania wejść dla tych akcji.

1. Otwórz "input/game.input_bindings"
2. Dodaj wyzwalacz klawisza dla "KEY_SPACE" i nazwij akcję "jump"
3. Dodaj wyzwalacz dotyku dla "TOUCH_MULTI" i nazwij akcję "touch". (Nazwy akcji są dowolne, ale muszą zgadzać się z nazwami w twoim skrypcie. Zwróć uwagę, że nie możesz mieć tej samej nazwy akcji na wielu wyzwalaczach)
4. Zapisz plik.

![Wiązania wejść](images/runner/2/input_bindings.png)

## KROK 5 - Refaktoryzacja poziomu

Teraz, gdy mamy już skonfigurowanego bohatera z kolizjami i wszystkim innym, musimy dodać kolizje także do podłoża, aby bohater miał z czym się zderzać (albo po czym biec). Zrobimy to za chwilę, ale najpierw wykonamy trochę refaktoryzacji i przeniesiemy wszystkie elementy poziomu do osobnej kolekcji oraz nieco uporządkujemy strukturę plików:

1. Utwórz nowy plik *level.collection* (kliknij prawym przyciskiem *main* w *Assets pane* i wybierz <kbd>New ▸ Collection File</kbd>).
2. Otwórz nowy plik, kliknij prawym przyciskiem korzeń w *Outline* i wybierz <kbd>Add Collection from File</kbd>, a następnie wskaż *ground.collection*.
3. W *level.collection* kliknij prawym przyciskiem korzeń w *Outline* i wybierz <kbd>Add Game Object File</kbd>, a następnie wskaż *hero.go*.
4. Teraz utwórz nowy folder o nazwie *level* w katalogu głównym projektu (kliknij prawym przyciskiem białą przestrzeń pod *game.project* i wybierz <kbd>New ▸ Folder</kbd>), a następnie przenieś do niego utworzone dotąd zasoby poziomu: pliki *level.collection*, *level.atlas*, folder "images" zawierający obrazy atlasu poziomu oraz pliki *ground.collection* i *ground.script*.
5. Otwórz *main.collection*, usuń *ground.collection*, a zamiast tego dodaj *level.collection* (kliknij prawym przyciskiem i wybierz <kbd>Add Collection from File</kbd>), która teraz zawiera *ground.collection*. Upewnij się, że umieszczasz kolekcję w pozycji 0, 0, 0.

::: sidenote
Jak mogłeś już zauważyć, hierarchia plików widoczna w *Assets pane* jest odłączona od struktury zawartości, którą budujesz w swoich kolekcjach. Pojedyncze pliki są odwołaniami z plików kolekcji i obiektów gry, ale ich położenie jest całkowicie dowolne.

Jeśli chcesz przenieść plik w nowe miejsce, Defold pomaga automatycznie aktualizując odwołania do pliku (refaktoryzacja). Podczas tworzenia złożonego oprogramowania, takiego jak gra, możliwość zmieniania struktury projektu wraz z jego wzrostem i zmianami jest niezwykle pomocna. Defold zachęca do tego i sprawia, że proces przebiega płynnie, więc nie bój się przestawiać plików!
:::

Powinniśmy też dodać obiekt gry `controller` z komponentem skryptu do kolekcji poziomu:

1. Utwórz nowy plik skryptu. Kliknij prawym przyciskiem folder *level* w *Assets pane* i wybierz <kbd>New ▸ Script File</kbd>. Nazwij plik *controller.script*.
2. Otwórz plik skryptu, skopiuj do niego poniższy kod i zapisz plik:

    ```lua
    -- controller.script
    go.property("speed", 360) -- <1>

    function init(self)
        msg.post("ground/controller#ground", "set_speed", { speed = self.speed })
    end
    ```
    1. To jest właściwość skryptu. Ustawiamy jej wartość domyślną, ale każda umieszczona instancja skryptu może tę wartość nadpisać bezpośrednio w widoku właściwości w edytorze.

3. Otwórz plik *level.collection*.
4. Kliknij prawym przyciskiem korzeń w *Outline* i wybierz <kbd>Add Game Object</kbd>.
5. Ustaw *Id* na "controller".
6. Kliknij prawym przyciskiem obiekt gry "controller" w *Outline* i wybierz <kbd>Add Component from File</kbd>, a następnie wskaż plik *controller.script* z folderu *level*.
7. Zapisz plik.

![Właściwość skryptu](images/runner/2/script_property.png)

::: sidenote
Obiekt gry "controller" nie istnieje w pliku, lecz jest tworzony bezpośrednio w kolekcji poziomu. Oznacza to, że instancja obiektu gry jest tworzona z danych zapisanych bezpośrednio w miejscu umieszczenia. To jest w porządku w przypadku obiektów gry o jednym przeznaczeniu, takich jak ten. Jeśli potrzebujesz wielu instancji jakiegoś obiektu gry i chcesz móc modyfikować prototyp/szablon używany do tworzenia każdej instancji, po prostu utwórz plik obiektu gry i dodaj obiekt gry z pliku do kolekcji. W ten sposób powstaje obiekt gry z odwołaniem do pliku jako prototypu/szablonu.

Celem tego obiektu gry "controller" jest sterowanie wszystkim, co dotyczy uruchomionego poziomu. Wkrótce ten skrypt będzie odpowiadać za tworzenie platform i monet, z którymi będzie wchodzić w interakcję bohater, ale na razie będzie ustawiać tylko prędkość poziomu.
:::

W funkcji `init()` skryptu kontrolera poziomu wysyłana jest wiadomość do komponentu skryptu obiektu kontrolera podłoża, adresowana przez jego id:

```lua
msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
```

Id obiektu gry kontrolera jest ustawione na `"ground/controller"`, ponieważ znajduje się on w kolekcji "ground". Następnie dodajemy id komponentu `"controller"` po znaku hash `"#"`, który oddziela id obiektu od id komponentu. Zwróć uwagę, że skrypt podłoża nie ma jeszcze kodu reagującego na wiadomość `set_speed`, więc musimy dodać do *ground.script* funkcję `on_message()` i logikę dla niej.

1. Otwórz *ground.script*.
2. Dodaj poniższy kod i zapisz plik:

```lua
-- ground.script
function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then -- <1>
        self.speed = message.speed -- <2>
    end
end
```
1. Wszystkie wiadomości są wewnętrznie haszowane w momencie wysłania i muszą być porównywane z wartością haszowaną.
2. Dane wiadomości to tabela Lua zawierająca dane wysłane wraz z wiadomością.

![Dodaj kod podłoża](images/runner/insert_ground_code.png)

## KROK 6 - Fizyka podłoża i platformy

Na tym etapie powinniśmy dodać kolizje fizyczne do podłoża:

1. Otwórz plik *ground.collection*.
2. Dodaj nowy komponent *Collision Object* do odpowiedniego obiektu gry. Ponieważ skrypt podłoża nie reaguje na kolizje (cała ta logika znajduje się w skrypcie bohatera), możemy umieścić go w dowolnym _nieruchomym_ obiekcie gry (obiekty-kafle podłoża nie są nieruchome, więc ich unikaj). Dobrym kandydatem jest obiekt gry "controller", ale możesz też utworzyć dla tego osobny obiekt. Kliknij prawym przyciskiem obiekt gry i wybierz <kbd>Add Component</kbd>, a potem *Collision Object*.
3. Dodaj kształt box, klikając prawym przyciskiem komponent *Collision Object* i wybierając <kbd>Add Shape</kbd>, a następnie *Box*.
4. Użyj *Move Tool* i *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> i <kbd>Scene ▸ Scale Tool</kbd>), aby box obejmował wszystkie kafle podłoża.
5. Ustaw właściwość *Type* obiektu kolizji na "Static", ponieważ fizyka podłoża nie będzie się poruszać.
6. Ustaw właściwość *Group* obiektu kolizji na "geometry", a *Mask* na "hero". Teraz obiekt kolizji bohatera i ten obiekt będą rejestrować między sobą kolizje.
7. Zapisz plik.

![Kolizja podłoża](images/runner/2/ground_collision.png)

Teraz powinieneś móc uruchomić grę (<kbd>Project ▸ Build</kbd>). Bohater powinien biec po podłożu i powinno być możliwe skakanie przyciskiem <kbd>Space</kbd>. Jeśli uruchomisz grę na urządzeniu mobilnym, możesz skakać, stukając w ekran.

Aby trochę urozmaicić życie w naszym świecie gry, powinniśmy dodać platformy, po których można skakać.

1. Przeciągnij plik obrazu *rock_planks.png* z paczki zasobów do podfolderu *level/images*.
2. Otwórz *level.atlas* i dodaj nowy obraz do atlasu (kliknij prawym przyciskiem korzeń w *Outline* i wybierz <kbd>Add Images</kbd>).
3. Zapisz plik.
4. Utwórz nowy plik *Game Object* o nazwie *platform.go* w folderze *level*. (Kliknij prawym przyciskiem *level* w *Assets pane*, a następnie wybierz <kbd>New ▸ Game Object File</kbd>)
5. Dodaj komponent *Sprite* do obiektu gry (kliknij prawym przyciskiem korzeń w widoku *Outline* i wybierz <kbd>Add Component</kbd>, a następnie *Sprite*).
6. Ustaw właściwość *Image* tak, aby wskazywała plik *level.atlas*, i ustaw *Default Animation* na "rock_planks". Dla wygody trzymaj obiekty poziomu w podfolderze "level/objects".
7. Dodaj komponent *Collision Object* do obiektu gry platformy (kliknij prawym przyciskiem korzeń w widoku *Outline* i wybierz <kbd>Add Component</kbd>).
8. Upewnij się, że ustawiasz *Type* komponentu na "Kinematic", a *Group* i *Mask* odpowiednio na "geometry" i "hero".
9. Dodaj *Box Shape* do komponentu *Collision Object*. (Kliknij prawym przyciskiem komponent w *Outline* i wybierz <kbd>Add Shape</kbd>, a następnie wybierz *Box*).
10. Użyj *Move Tool* i *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> i <kbd>Scene ▸ Scale Tool</kbd>), aby kształt w komponencie *Collision Object* obejmował platformę.
11. Utwórz plik *Script* o nazwie *platform.script* (kliknij prawym przyciskiem w *Assets pane* i wybierz <kbd>New ▸ Script File</kbd>) i wstaw do pliku poniższy kod, a następnie zapisz go:

    ```lua
    -- plik: platform.script
    function init(self)
        self.speed = 540      -- Domyślna prędkość w pikselach/s
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            go.delete() -- <1>
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        end
    end
    ```
    1. Po prostu usuń platformę, gdy zostanie przesunięta poza prawą krawędź ekranu.

12. Otwórz *platform.go* i dodaj nowy skrypt jako komponent (kliknij prawym przyciskiem korzeń w widoku *Outline* i wybierz <kbd>Add Component From File</kbd>, a następnie wskaż *platform.script*).
13. Skopiuj *platform.go* do nowego pliku (kliknij prawym przyciskiem plik w *Assets pane* i wybierz <kbd>Copy</kbd>, potem kliknij prawym przyciskiem ponownie i wybierz <kbd>Paste</kbd>) i nazwij nowy plik *platform_long.go*.
14. Otwórz *platform_long.go* i dodaj drugi komponent *Sprite* (kliknij prawym przyciskiem korzeń w widoku *Outline* i wybierz <kbd>Add Component</kbd>). Alternatywnie możesz skopiować istniejący *Sprite*.
15. Użyj *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>), aby ustawić komponenty *Sprite* obok siebie.
16. Użyj *Move Tool* i *Scale Tool*, aby kształt w komponencie *Collision Object* obejmował obie platformy.

![Platforma](images/runner/2/platform_long.png)

::: sidenote
Zwróć uwagę, że zarówno *platform.go*, jak i *platform_long.go* mają komponenty *Script*, które odwołują się do tego samego pliku skryptu. To dobrze, bo każda zmiana w tym pliku skryptu wpłynie na zachowanie zarówno zwykłych, jak i długich platform.
:::

## Tworzenie platform

Pomysł na tę grę jest taki, że ma to być prosta gra z niekończącym się biegiem. Oznacza to, że obiektów gry platform nie można umieszczać w kolekcji w edytorze. Zamiast tego musimy tworzyć je dynamicznie:

1. Otwórz *level.collection*.
2. Dodaj dwa komponenty *Factory* do obiektu gry "controller" (kliknij prawym przyciskiem i wybierz <kbd>Add Component</kbd>, a następnie *Factory*).
3. Ustaw właściwości *Id* komponentów na "platform_factory" i "platform_long_factory".
4. Ustaw właściwość *Prototype* dla "platform_factory" na plik */level/objects/platform.go*.
5. Ustaw właściwość *Prototype* dla "platform_long_factory" na plik */level/objects/platform_long.go*.
6. Zapisz plik.
7. Otwórz plik *controller.script*, który zarządza poziomem.
8. Zmodyfikuj skrypt tak, aby zawierał poniższy kod, a następnie zapisz plik:

```lua
-- plik: controller.script
go.property("speed", 360)

local grid = 460
local platform_heights = { 100, 200, 350 } -- <1>

function init(self)
    msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
    self.gridw = 0
end

function update(self, dt) -- <2>
    self.gridw = self.gridw + self.speed * dt

    if self.gridw >= grid then
        self.gridw = 0

        -- Być może utwórz platformę na losowej wysokości
        if math.random() > 0.2 then
            local h = platform_heights[math.random(#platform_heights)]
            local f = "#platform_factory"
            if math.random() > 0.5 then
                f = "#platform_long_factory"
            end

            local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, 0.6)
            msg.post(p, "set_speed", { speed = self.speed })
        end
    end
end
```
1. Wstępnie zdefiniowane wartości położenia Y, na których będą tworzone platformy.
2. Funkcja `update()` jest wywoływana raz na klatkę i używamy jej do decydowania, czy utworzyć zwykłą czy długą platformę w określonych odstępach czasu i na określonych wysokościach, aby uniknąć nakładania się obiektów. Łatwo można eksperymentować z różnymi algorytmami tworzenia, aby uzyskać różne sposoby rozgrywki.

Teraz uruchom grę (<kbd>Project ▸ Build</kbd>).

Wow, to zaczyna już przypominać coś, co można (prawie) zagrać...

![Uruchomiona gra](images/runner/2/run_game.png)

## KROK 7 - Animacja i śmierć

Pierwszą rzeczą, którą zrobimy, jest tchnienie życia w bohatera. W tej chwili biedak utknął w pętli biegu i nie reaguje dobrze na skoki ani na nic innego. Plik Spine, który dodaliśmy z paczki zasobów, zawiera właśnie zestaw animacji do tego celu.

1. Otwórz plik *hero.script* i dodaj poniższe funkcje _przed_ istniejącą funkcją `update()`:

```lua
    -- plik: hero.script
    local function play_animation(self, anim)
        -- odtwarzaj tylko animacje, które nie są już odtwarzane
        if self.anim ~= anim then
            -- poleć modelowi Spine odtworzyć animację
            local anim_props = { blend_duration = 0.15 }
            spine.play_anim("#spinemodel", anim, go.PLAYBACK_LOOP_FORWARD, anim_props)
            -- zapamiętaj, która animacja jest odtwarzana
            self.anim = anim
        end
    end

    local function update_animation(self)
        -- upewnij się, że odtwarzana jest właściwa animacja
        if self.ground_contact then
            play_animation(self, hash("run"))
        else
            play_animation(self, hash("jump"))

        end
    end
```

2. Znajdź funkcję `update()` i dodaj wywołanie `update_animation`:

```lua
    ...
    -- zastosuj to do postaci gracza
    go.set_position(go.get_position() + self.velocity * dt)

    update_animation(self)
    ...
  ```

![Wstaw kod bohatera](images/runner/insert_hero_code.png)

::: sidenote
Lua ma dla zmiennych lokalnych "zakres leksykalny" i jest wrażliwa na kolejność, w jakiej umieszczasz lokalne funkcje. Funkcja `update()` wywołuje lokalne funkcje `update_animation()` i `play_animation()`, co oznacza, że runtime musi już znać te lokalne funkcje, aby móc je wywołać. Dlatego musimy umieścić je przed `update()`. Jeśli zmienisz kolejność funkcji, otrzymasz błąd. Zwróć uwagę, że dotyczy to tylko zmiennych `local`. Więcej o regułach zakresu w Lua i lokalnych funkcjach przeczytasz na http://www.lua.org/pil/6.2.html
:::

To wszystko, czego potrzeba, aby dodać do bohatera animacje skoku i upadku. Jeśli uruchomisz grę, zauważysz, że gra się od razu przyjemniej. Możesz też zauważyć, że platformy niestety potrafią zepchnąć bohatera poza ekran. To efekt uboczny obsługi kolizji, ale rozwiązanie jest proste: dodajmy trochę przemocy i sprawmy, by krawędzie platform były niebezpieczne!

1. Przeciągnij *spikes.png* z paczki zasobów do folderu "level/images" w *Assets pane*.
2. Otwórz *level.atlas* i dodaj obraz (kliknij prawym przyciskiem i wybierz <kbd>Add Images</kbd>).
3. Otwórz *platform.go* i dodaj kilka komponentów *Sprite*. Ustaw *Image* na *level.atlas* i *Default Animation* na "spikes".
4. Użyj *Move Tool* i *Rotate Tool*, aby ustawić kolce wzdłuż krawędzi platformy.
5. Aby kolce renderowały się za platformą, ustaw pozycję *Z* sprite'ów kolców na -0.1.
6. Dodaj nowy komponent *Collision Object* do platform (kliknij prawym przyciskiem korzeń w *Outline* i wybierz <kbd>Add Component</kbd>). Ustaw właściwość *Group* na "danger". Ustaw też *Mask* na "hero".
7. Dodaj box shape do *Collision Object* (kliknij prawym przyciskiem i wybierz <kbd>Add Shape</kbd>) i użyj *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) oraz *Scale Tool*, aby ustawić kształt tak, by bohater zderzał się z obiektem "danger", gdy uderza w platformę z boku albo od spodu.
8. Zapisz plik.

    ![Kolce platformy](images/runner/3/danger_edges.png)

9. Otwórz *hero.go*, zaznacz *Collision Object* i dodaj nazwę "danger" do właściwości *Mask*. Następnie zapisz plik.

    ![Kolizja bohatera](images/runner/3/hero_collision.png)

10. Otwórz *hero.script* i zmień funkcję `on_message()` tak, aby bohater reagował na kolizję z krawędzią "danger":

    ```lua
    -- plik: hero.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            self.velocity = vmath.vector3(0, 0, 0)
            self.correction = vmath.vector3()
            self.ground_contact = false
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- sprawdź, czy otrzymaliśmy wiadomość o punkcie kontaktu
            if message.group == hash("danger") then
                -- Zgiń i uruchom ponownie
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("#", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end
    ```
    1. Dodaj rotację i ruch upadku do bohatera w chwili śmierci. To można znacznie ulepszyć!

11. Zmień funkcję `init()`, aby wysyłała wiadomość "reset" inicjalizującą obiekt, a następnie zapisz plik:

    ```lua
    -- plik: hero.script
    function init(self)
        -- to pozwala nam obsługiwać wejście w tym skrypcie
        msg.post(".", "acquire_input_focus")
        -- zapisz pozycję
        self.position = go.get_position()
        msg.post("#", "reset")
    end
    ```

## KROK 8 - Resetowanie poziomu

Jeśli teraz spróbujesz uruchomić grę, szybko stanie się jasne, że mechanizm resetu nie działa. Reset bohatera jest w porządku, ale łatwo możesz zresetować się do sytuacji, w której natychmiast spadniesz na krawędź platformy i zginiesz ponownie. Chcemy więc poprawnie resetować cały poziom po śmierci. Ponieważ poziom to po prostu seria tworzonych platform, wystarczy śledzić wszystkie utworzone platformy i usuwać je przy resecie:

1. Otwórz plik *controller.script* i zmodyfikuj kod tak, aby przechowywał id wszystkich tworzonych platform:

    ```lua
    -- plik: controller.script
    go.property("speed", 360)

    local grid = 460
    local platform_heights = { 100, 200, 350 }

    function init(self)
        msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
        self.gridw = 0
        self.spawns = {} -- <1>
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= grid then
            self.gridw = 0

            -- Być może utwórz platformę na losowej wysokości
            if math.random() > 0.2 then
                local h = platform_heights[math.random(#platform_heights)]
                local f = "#platform_factory"
                if math.random() > 0.5 then
                    f = "#platform_long_factory"
                end

                local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, 0.6)
                msg.post(p, "set_speed", { speed = self.speed })
                table.insert(self.spawns, p) -- <1>
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then -- <2>
            -- Poleć bohaterowi się zresetować.
            msg.post("hero#hero", "reset")
            -- Usuń wszystkie platformy
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then -- <3>
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```
    1. Używamy tabeli do przechowywania wszystkich utworzonych platform.
    2. Wiadomość "reset" usuwa wszystkie platformy zapisane w tabeli.
    3. Wiadomość "delete_spawn" usuwa konkretną platformę i usuwa ją z tabeli.

2. Zapisz plik.
3. Otwórz *platform.script* i zmodyfikuj go tak, aby zamiast po prostu usuwać platformę, która dotarła do lewego skraju, wysyłał do kontrolera poziomu wiadomość z prośbą o usunięcie platformy:

    ```lua
    -- plik: platform.script
    ...
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    ...
    ```

    ![Wstaw kod platformy](images/runner/insert_platform_code.png)

4. Zapisz plik.
5. Otwórz *hero.script*. Teraz ostatnią rzeczą, którą musimy zrobić, jest poinformowanie poziomu, aby wykonał reset. Przenieśliśmy wiadomość proszącą bohatera o reset do skryptu kontrolera poziomu. Ma sens scentralizować w ten sposób sterowanie resetowaniem, ponieważ pozwala to na przykład znacznie łatwiej wprowadzić dłuższą, opóźnioną sekwencję śmierci:

```lua
-- plik: hero.script
...
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
    function()
        msg.post("controller#controller", "reset")
    end)
...
```

![Wstaw kod bohatera 2](images/runner/insert_hero_code_2.png)

I w ten sposób mamy już podstawową pętlę restartu i śmierci!

Następny krok - coś, dla czego warto żyć: monety!

## KROK 9 - Monety do zebrania

Pomysł jest taki, aby umieszczać w poziomie monety do zebrania przez gracza. Pierwsze pytanie brzmi: jak w ogóle wstawiać je do poziomu. Można na przykład opracować schemat tworzenia, który będzie w jakiś sposób zsynchronizowany z algorytmem tworzenia platform. Ostatecznie wybraliśmy jednak znacznie prostsze podejście i pozwoliliśmy, aby same platformy tworzyły monety:

1. Przeciągnij obraz *coin.png* z paczki zasobów do "level/images" w *Assets pane*.
2. Otwórz *level.atlas* i dodaj obraz (kliknij prawym przyciskiem i wybierz <kbd>Add Images</kbd>).
3. Utwórz plik *Game Object* o nazwie *coin.go* w folderze *level* (kliknij prawym przyciskiem *level* w *Assets pane* i wybierz <kbd>New ▸ Game Object File</kbd>).
4. Otwórz *coin.go* i dodaj komponent *Sprite* (kliknij prawym przyciskiem i wybierz <kbd>Add Component</kbd> w *Outline*). Ustaw *Image* na *level.atlas* i *Default Animation* na "coin".
5. Dodaj *Collision Object* (kliknij prawym przyciskiem w *Outline* i wybierz <kbd>Add Component</kbd>) i dodaj *Sphere* shape obejmujący obraz (kliknij prawym przyciskiem komponent i wybierz <kbd>Add Shape</kbd>).
6. Użyj *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) i *Scale Tool*, aby kula obejmowała obraz monety.
7. Ustaw *Type* obiektu kolizji na "Kinematic", *Group* na "pickup", a *Mask* na "hero".
8. Otwórz *hero.go* i dodaj "pickup" do właściwości *Mask* komponentu *Collision Object*, a następnie zapisz plik.
9. Utwórz nowy plik skryptu *coin.script* (kliknij prawym przyciskiem *level* w *Assets pane* i wybierz <kbd>New ▸ Script File</kbd>). Zastąp kod szablonu poniższym:

    ```lua
    -- plik: coin.script
    function init(self)
        self.collected = false
    end

    function on_message(self, message_id, message, sender)
        if self.collected == false and message_id == hash("collision_response") then
            self.collected = true
            msg.post("#sprite", "disable")
        elseif message_id == hash("start_animation") then
            pos = go.get_position()
            go.animate(go.get_id(), "position.y", go.PLAYBACK_LOOP_PINGPONG, pos.y + 24, go.EASING_INOUTSINE, 0.75, message.delay)
        end
    end
    ```

10. Dodaj plik skryptu jako komponent *Script* do obiektu monety (kliknij prawym przyciskiem korzeń w *Outline* i wybierz <kbd>Add Component from File</kbd>).

    ![Obiekt gry monety](images/runner/3/coin.png)

Plan jest taki, aby monety były tworzone przez obiekty platform, więc dodajmy fabryki monet do *platform.go* i *platform_long.go*.

1. Otwórz *platform.go* i dodaj komponent *Factory* (kliknij prawym przyciskiem w *Outline* i wybierz <kbd>Add Component</kbd>).
2. Ustaw *Id* komponentu *Factory* na "coin_factory" i ustaw jego *Prototype* na plik *coin.go*.
3. Teraz otwórz *platform_long.go* i utwórz identyczny komponent *Factory*.
4. Zapisz oba pliki.

![Fabryka monet](images/runner/3/coin_factory.png)

Teraz musimy zmodyfikować *platform.script*, aby tworzył i usuwał monety:

```lua
-- plik: platform.script
function init(self)
    self.speed = 540     -- Domyślna prędkość w pikselach/s
    self.coins = {}
end

function final(self)
    for i,p in ipairs(self.coins) do
        go.delete(p)
    end
end

function update(self, dt)
    local pos = go.get_position()
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    pos.x = pos.x - self.speed * dt
    go.set_position(pos)
end

function create_coins(self, params)
    local spacing = 56
    local pos = go.get_position()
    local x = pos.x - params.coins * (spacing*0.5) - 24
    for i = 1, params.coins do
        local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
        msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
        msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
        table.insert(self.coins, coin)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then
        self.speed = message.speed
    elseif message_id == hash("create_coins") then
        create_coins(self, message)
    end
end
```
1. Ustawiając rodzica utworzonej monety na platformę, będzie ona poruszać się razem z platformą.
2. Animacja sprawia, że monety poruszają się w górę i w dół względem platformy, która jest teraz ich rodzicem.

::: sidenote
Relacje rodzic-dziecko są ściśle modyfikacją _grafu sceny_. Dziecko będzie transformowane razem ze swoim rodzicem, czyli przesuwane, skalowane lub obracane. Jeśli potrzebujesz dodatkowych relacji "własności" między obiektami gry, musisz śledzić je osobno w kodzie.
:::

Ostatnim krokiem w tym samouczku jest dodanie kilku linii do *controller.script*:

```lua
-- plik: controller.script
...
local platform_heights = { 100, 200, 350 }
local coins = 3 -- <1>
...
```
1. Liczba monet tworzonych na zwykłej platformie.

```lua
-- controller.script
...
local coins = coins
if math.random() > 0.5 then
    f = "#platform_long_factory"
    coins = coins * 2 -- Dwa razy więcej monet na długich platformach
end
...
```

```lua
-- controller.script
...
msg.post(p, "set_speed", { speed = self.speed })
msg.post(p, "create_coins", { coins = coins })
table.insert(self.spawns, p)
...
```

![Wstaw kod kontrolera](images/runner/insert_controller_code.png)

A teraz mamy prostą, ale działającą grę! Jeśli dotarłeś aż tutaj, możesz chcieć kontynuować samodzielnie i dodać następujące elementy:

1. Licznik punktów i licznik żyć
2. Efekty cząsteczkowe dla przedmiotów do zebrania i śmierci
3. Ładną grafikę tła

> Pobierz ukończoną wersję projektu [tutaj](images/runner/sample-runner.zip)

Na tym kończy się ten samouczek wprowadzający. Teraz śmiało zanurz się w Defold. Przygotowaliśmy wiele [podręczników i samouczków](//www.defold.com/learn), które poprowadzą cię dalej, a jeśli utkniesz, zapraszamy na [forum](//forum.defold.com).

Miłego tworzenia w silniku Defold!
