---
brief: Jeśli dopiero zaczynasz pracę z Defold, ten przewodnik pomoże ci rozpocząć pisanie logiki skryptów oraz poznać kilka podstawowych elementów Defold podczas budowania od zera klona gry Snake.
layout: tutorial
title: Budowanie gry Snake w Defold
difficulty: Beginner
---

# Snake

Ten samouczek przeprowadzi cię przez proces tworzenia jednej z najczęściej odtwarzanych klasycznych gier. Istnieje wiele wariantów tej gry; w tej wersji wąż zjada "jedzenie" i rośnie tylko wtedy, gdy je zje. Wąż porusza się też po planszy zawierającej przeszkody.

![thumbnail](images/snake/thumbnail.png)

### Czego się tutaj nauczysz?

W tym samouczku nauczysz się:
- tworzyć grę od zera w Defold
- konfigurować i obsługiwać wejście
- tworzyć mapy kafelków i modyfikować je w czasie działania
- pisać skrypty w Lua

### Uwaga dla początkujących

Ten samouczek jest przeznaczony dla początkujących, ale jeśli jesteś zupełnie nowy w Defold i tworzeniu gier, zalecamy najpierw przeczytać kilka wprowadzających instrukcji, szczególnie o [blokach budulcowych Defold](/manuals/building-blocks/) oraz [słowniczku](/manuals/glossary/). Jeśli nie masz jeszcze pobranego Defold, sprawdź [instrukcję instalacji](/manuals/install/). Warto też zajrzeć do [przeglądu edytora](/manuals/editor/), aby szybko poznać sam edytor, ale w tym samouczku pokazujemy również zrzuty ekranu dla każdego kroku.

## Tworzenie projektu

Uruchom Defold i:

1. Wybierz *Create From* ▸ *Templates* po lewej stronie.
2. Wybierz *Empty Project*.
3. Wpisz nazwę projektu w polu *Title*.
4. Wybierz *Location* dla projektu.
5. Kliknij *Create New Project*.

![start](images/snake/1.png)

<input type="checkbox"/> Gotowe!

## Ustawienia projektu

Zaczniemy od zdefiniowania rozdzielczości gry.

1. Po otwarciu edytora znajdź plik `game.project` po lewej stronie, w panelu *Assets*. Kliknij go dwukrotnie, aby go otworzyć.
2. Przejdź do sekcji *Display* w pliku `game.project`.
3. Ustaw wymiary gry (`Width` i `Height`) na 768⨉768 lub inną wielokrotność 16.

![display](images/snake/2.png)

Powodem jest to, że gra będzie rysowana na siatce, w której każdy segment ma 16x16 pikseli, więc ekran gry nie utnie żadnych częściowych segmentów. Plik `game.project` zawiera wszystkie ważne ustawienia projektu - więcej przeczytasz o nich w [instrukcji ustawień projektu](/manuals/project-settings/).

<input type="checkbox"/> Gotowe!

## Tworzenie nowych folderów w panelu Assets

Do minimalistycznego klona Snake potrzeba bardzo niewiele grafiki. Jeden zielony segment 16⨉16 dla węża, jeden biały blok dla przeszkód i jeden mniejszy czerwony blok reprezentujący jedzenie.

Najpierw utwórz katalog na zasoby w edytorze Defold:

1. <kbd>Kliknij prawym przyciskiem</kbd> folder `main`
2. Wybierz `New Folder`.
3. Pojawi się okno z pytaniem o nazwę - wpisz `assets` i kliknij `Create Folder`.

![new_folder](images/snake/3.png)

<input type="checkbox"/>`Gotowe!`

## Dodawanie grafiki do gry

Poniższy obraz jest jedynym zasobem, którego potrzebujesz:

![snake_sprites](images/snake/snake.png)

1. <kbd>Kliknij prawym przyciskiem</kbd> obraz powyżej i zapisz go na dysku lokalnym. Następnie przeciągnij i upuść (albo skopiuj i wklej) pobrany obraz do nowej lokalizacji w folderze projektu, którą właśnie utworzyłeś.

![new_folder](images/snake/4.png)

Więcej szczegółów możesz też przeczytać w instrukcji o [importowaniu zasobów graficznych](/manuals/importing-graphics/).

<input type="checkbox"/>`Gotowe!`

## Dodawanie Tile Source

Defold udostępnia wbudowany komponent [Tilemap](/manuals/tilemap/), którego użyjesz do utworzenia planszy złożonej z *kafelków* wyrównanych do siatki. Mapa kafelków pozwala ustawiać i odczytywać pojedyncze kafelki, co idealnie pasuje do tej gry. Ponieważ mapy kafelków pobierają grafikę z [Tilesource](/manuals/tilesource/), musisz utworzyć taki zasób:

1. <kbd>Kliknij prawym przyciskiem</kbd> folder `assets`.
2. Wybierz `New` ▸ `Tile Source` w sekcji "Resources".
3. Nazwij nowy plik "snake" (edytor zapisze go jako `snake.tilesource`).

![new_tilesource](images/snake/5.png)

Tilesource otworzy się w dedykowanym edytorze Tilesource dla tego typu pliku i pojawi się prośba o wskazanie obrazu, który jest wymagany. Po prawej stronie znajdziesz panel `Properties`:

4. Ustaw właściwość `Image` na właśnie zaimportowany plik graficzny.
![tilesource](images/snake/6.png)

5. Właściwości `Width` i `Height` powinny pozostać ustawione na 16 (wartość domyślna). Podzieli to obraz 32⨉32 piksele na 4 kafelki, ponumerowane 1-4.

![tilesource_properties](images/snake/7.png)

Zwróć uwagę, że właściwość *Extrude Borders* jest ustawiona na 2 piksele. Zapobiega to artefaktom wizualnym wokół kafelków, których grafika dochodzi aż do krawędzi.

Jeśli dokonasz zmian w pliku, przy jego nazwie na karcie pojawi się znak gwiazdki `*`. Wybierz `File` ▸ `Save All` lub użyj skrótu `<kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>⌘Cmd</kbd> + <kbd>S</kbd> na Macu), aby zapisać wszystkie pliki.

<input type="checkbox"/> Gotowe!

## Tworzenie mapy kafelków planszy

Masz już gotowe źródło kafelków, więc pora utworzyć komponent mapy kafelków dla planszy:

1. <kbd>Kliknij prawym przyciskiem</kbd> folder `main` i wybierz <kbd>New</kbd> ▸ <kbd>Tile Map</kbd> w sekcji "Components". Nazwij nowy plik "grid" (edytor zapisze go jako "grid.tilemap").
![add_tilemap](images/snake/8.png)

2. Plik otworzy się w edytorze Tilemap i zaznaczy, że potrzebuje **Tile Source**, więc ustaw właściwość *Tile Source* na wcześniej utworzony plik "snake.tilesource".
![set_tilesource](images/snake/9.png)

<input type="checkbox"/> Gotowe!

## Rysowanie kafelków w mapie kafelków

Defold przechowuje tylko ten obszar mapy kafelków, który jest rzeczywiście używany, dlatego musisz dodać wystarczająco dużo kafelków, aby wypełnić granice ekranu.

1. Wybierz warstwę `layer1` w panelu `Outline` po prawej stronie.
2. Wybierz opcję menu `Edit` ▸ `Select Tile...` albo skrót <kbd>Space</kbd>, aby wyświetlić paletę kafelków, a następnie kliknij kafelek, którego chcesz używać podczas malowania.
![tilemap](images/snake/10.png)

3. Namaluj obramowanie wokół krawędzi ekranu oraz kilka przeszkód.
![tilemap_final](images/snake/11.png)

Będziesz potrzebować mapy kafelków o rozmiarze 48x48 kafelków (ponieważ nasz ekran ma 768 pikseli, a kafelki mają 16px, więc 768/16 = 48), aby wypełnić ekran gry.

Zapisz mapę kafelków po zakończeniu.

<input type="checkbox"/> Gotowe!

## Dodawanie mapy kafelków do gry

Teraz musimy dodać mapę kafelków do gry. Jeśli znasz bloki budulcowe Defold, komponenty są częścią obiektów gry, a obiekty gry mogą być definiowane w kolekcjach.

1. Otwórz `main.collection`, klikając go dwukrotnie w panelu `Assets`. W szablonie Empty Project jest to domyślna kolekcja startowa ładowana przy uruchomieniu silnika.

2. <kbd>Kliknij prawym przyciskiem</kbd> korzeń w panelu `Outline` i wybierz `Add Game Object`, co utworzy nowy obiekt gry w kolekcji ładowanej przy starcie gry.
![add_game_object](images/snake/12.png)

3. <kbd>Kliknij prawym przyciskiem</kbd> nowy obiekt gry i wybierz `Add Component File`. Wybierz utworzony przed chwilą plik "grid.tilemap".
![add_component](images/snake/13.png)

W tej chwili mamy mapę kafelków w kolekcji gry. Powinna być widoczna po uruchomieniu gry z edytora.

1. Wybierz `Project` ▸ `Build` albo skrót <kbd>Ctrl</kbd> + <kbd>B</kbd> (<kbd>⌘Cmd</kbd> + <kbd>B</kbd> na Macu).

![run_game](images/snake/14.png)

<input type="checkbox"/> Gotowe!

## Dodawanie skryptu do gry

1. <kbd>Kliknij prawym przyciskiem</kbd> folder `main` w przeglądarce `Assets` i wybierz `New` ▸ `Script` w sekcji Scripts. Nazwij nowy plik skryptu "snake" (zostanie zapisany jako "snake.script"). Ten plik będzie zawierał całą logikę gry.
![add_script](images/snake/15.png)

2. Wróć do *main.collection* i <kbd>kliknij prawym przyciskiem</kbd> obiekt gry zawierający mapę kafelków. Wybierz <kbd>Add&nbsp;Component&nbsp;File</kbd> i wskaż plik "snake.script".

![main _ollection](images/snake/16.png)

Teraz komponent mapy kafelków i skrypt są już na miejscu.

<input type="checkbox"/> Gotowe!

## Skrypt gry

Skrypt, który napiszesz, będzie sterował całą grą. Będziemy dodawać funkcje jedna po drugiej.

### Prosty algorytm ruchu

Pomysł na działanie jest następujący:

1. Skrypt przechowuje listę pozycji kafelków, które aktualnie zajmuje wąż.
2. Jeśli gracz naciśnie klawisz kierunku, zapisz kierunek, w którym wąż ma się poruszać.
3. W regularnym odstępie przesuwaj węża o jeden krok w aktualnym kierunku ruchu.

### Inicjalizacja

Otwórz *snake.script* i znajdź funkcję `init()`. Ta funkcja jest wywoływana przez silnik podczas inicjalizacji skryptu przy starcie gry. Zmień kod na następujący:

```lua
function init(self)
    self.segments = { -- <1>
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0} -- <2>
    self.speed = 7.0 -- <3>
    self.time = 0 -- <4>
end
```

W tym kodzie:

1. Przechowujemy segmenty węża jako tablicę Lua o nazwie `self.segments`, zawierającą listę tabel, z których każda trzyma pozycję X i Y segmentu.
2. Przechowujemy aktualny kierunek jako tabelę o nazwie `self.dir`, zawierającą kierunek X i Y.
3. Przechowujemy aktualną prędkość ruchu w `self.speed`, wyrażoną w kafelkach na sekundę.
4. Przechowujemy wartość timera w `self.time`, która będzie używana do śledzenia prędkości ruchu.

Powyższy kod skryptu jest napisany w języku Lua. Warto zwrócić uwagę na kilka rzeczy w tym kodzie, ale jeśli jeszcze nie rozumiesz któregoś z poniższych punktów, nie martw się. Idź dalej, eksperymentuj i daj sobie czas --- w końcu to zrozumiesz. Na razie możesz zapamiętać, że w `init()` po prostu zainicjalizowaliśmy zmienne, których będziemy używać.

- Defold rezerwuje zestaw wbudowanych *funkcji* wywołań zwrotnych, które są wywoływane podczas życia komponentu skryptu. To *nie* są metody, tylko zwykłe funkcje.
- Środowisko uruchomieniowe przekazuje referencję do bieżącej instancji komponentu skryptu przez parametr `self`. Referencja `self` służy do przechowywania danych instancji.
- Referencji `self` można używać jak tabeli Lua, w której przechowujesz dane. Używaj notacji kropkowej tak jak w każdej innej tabeli: `self.data = "value"`. Referencja jest ważna przez cały czas życia skryptu, w tym przypadku od startu gry aż do jej zamknięcia.
- Literały tabel Lua zapisuje się w nawiasach klamrowych `{}`.
- Wpisy tabeli mogą być parami klucz/wartość (`{x = 10, y = 20}`), zagnieżdżonymi tabelami Lua (`{ {a = 1}, {b = 2} }`) albo innymi typami danych.

<input type="checkbox"/> Gotowe!

### Aktualizacja

Funkcja `init()` jest wywoływana dokładnie raz, gdy komponent skryptu zostaje utworzony w działającej grze. Funkcja `update()` jest natomiast wywoływana raz **w każdej klatce**, domyślnie 60 razy na sekundę. Dzięki temu idealnie nadaje się do logiki gry działającej w czasie rzeczywistym.

Pomysł na aktualizację jest taki: w ustalonym odstępie wykonuj następujące kroki:

1. Znajdź pozycję głowy węża, a następnie utwórz nową głowę w pozycji obok niej, przesuniętą o aktualny kierunek ruchu. Jeśli więc wąż porusza się o X=1 i Y=0, a aktualna głowa jest w miejscu X=0 i Y=0, nowa głowa powinna znaleźć się w X=1 i Y=0.
2. Zapisz nową pozycję głowy na liście segmentów tworzących węża.
3. Pobierz pozycję ogona z tabeli segmentów.
4. Wyczyść kafelek ogona w tej pozycji.
5. Narysuj wszystkie segmenty węża (kafelki) w pozycjach z tabeli.

![algorithm](images/snake/17.png)

:::sidenote
Pamiętaj, że głowa węża znajduje się na końcu tabeli, a ogon na początku.
:::

1. Znajdź funkcję `update()` w *snake.script* i zmień kod na następujący:

```lua
function update(self, dt)
    self.time = self.time + dt -- <1>
    if self.time >= 1.0 / self.speed then -- <2>
        local head = self.segments[#self.segments] -- <3>
        local newhead = {
            x = head.x + self.dir.x,
            y = head.y + self.dir.y
        } -- <4>

        table.insert(self.segments, newhead) -- <5>

        local tail = table.remove(self.segments, 1) -- <6>

        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0) -- <7>

        for i, s in ipairs(self.segments) do -- <8>
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2) -- <9>
        end

        self.time = 0 -- <10>
    end
end
```

W tym kodzie:

1. Zwiększamy timer o różnicę czasu (w sekundach) od ostatniego wywołania `update()` --- tak zwany "delta time", czyli `dt`.
2. Jeśli timer przesunął się wystarczająco:
3. Pobieramy pozycję bieżącej głowy. `#` to operator używany do pobrania długości tabeli, gdy jest ona używana jako tablica, co ma miejsce w naszym przypadku --- wszystkie segmenty są wartościami tabeli bez określonego klucza.
4. Tworzymy nowy segment głowy na podstawie aktualnej pozycji głowy i kierunku ruchu (`self.dir`).
5. Dodajemy nową głowę na koniec tabeli segmentów.
6. Usuwamy ogon z początku tabeli segmentów.
7. Czyścimy kafelek w pozycji usuniętego ogona. Nasza mapa kafelków `#grid` ma tylko 1 warstwę o nazwie `layer1`.
8. Iterujemy po elementach w tabeli segmentów. W każdej iteracji `i` będzie ustawione na pozycję w tabeli (zaczynając od 1), a `s` na aktualny segment.
9. Ustawiamy kafelek w pozycji segmentu na wartość 2 (czyli kafelek z zielonym kolorem węża).
10. Po zakończeniu resetujemy timer do zera.

Jeśli teraz uruchomisz grę, powinieneś zobaczyć węża o długości 4 segmentów pełznącego od lewej do prawej po planszy.

![run the game](images/snake/snake_run_1.png)

<input type="checkbox"/> Gotowe!

## Wejście gracza

Zanim dodasz kod reagujący na wejście gracza, musisz skonfigurować połączenia wejścia.

### Powiązania wejścia

1. Znajdź w folderze `input` plik `game.input_binding` i <kbd>kliknij go dwukrotnie</kbd>, aby go otworzyć.
2. Dodaj zestaw powiązań *Key Trigger* dla ruchu w górę, w dół, w lewo i w prawo. W kolumnie *Input* wybierz klawisze klawiatury, a w kolumnach *Action* wpisz nazwy akcji.

![input](images/snake/18.png)

Plik powiązań wejścia mapuje rzeczywiste wejście użytkownika (klawisze, ruchy myszy itd.) na *nazwy* akcji, które trafiają do skryptów proszących o wejście.

<input type="checkbox"/> Gotowe!

### Przejmowanie fokusu wejścia

Mając powiązania, otwórz *snake.script* i dodaj następujący wiersz na początku funkcji `init()`:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0
end
```

Dodany wiersz:
1. Wysyła wiadomość do bieżącego obiektu gry ("." to skrót oznaczający bieżący obiekt gry), informując go, że ma zacząć odbierać wejście z silnika.

Następnie znajdź funkcję `on_input` i wpisz następujący kod:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then -- <1>
        self.dir.x = 0 -- <2>
        self.dir.y = 1
    elseif action_id == hash("down") and action.pressed then
        self.dir.x = 0
        self.dir.y = -1
    elseif action_id == hash("left") and action.pressed then
        self.dir.x = -1
        self.dir.y = 0
    elseif action_id == hash("right") and action.pressed then
        self.dir.x = 1
        self.dir.y = 0
    end
end
```

Te gałęzie `if...elseif...` robią następujące rzeczy:
1. Jeśli odebrano akcję wejścia "up", skonfigurowaną w powiązaniach wejścia, a tabela `action` ma pole `pressed` ustawione na `true` (gracz nacisnął klawisz), wtedy:
2. Ustawiany jest kierunek ruchu.

Uruchom grę ponownie i sprawdź, czy możesz sterować wężem.

<input type="checkbox"/> Gotowe!

### Ulepszanie obsługi wejścia

Zauważ teraz, że jeśli naciśniesz dwa klawisze jednocześnie, spowoduje to dwa wywołania `on_input()`, po jednym dla każdego naciśnięcia. Przy kodzie zapisanym powyżej tylko wywołanie, które nastąpi jako ostatnie, wpłynie na kierunek węża, ponieważ kolejne wywołania `on_input()` nadpisują wartości w `self.dir`.

Zwróć też uwagę, że jeśli wąż porusza się w lewo, a ty naciśniesz klawisz <kbd>right</kbd>, wąż skręci w samego siebie. *Pozornie* oczywistą poprawką tego problemu jest dodanie dodatkowego warunku do instrukcji `if` w `on_input()`:

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

Jeśli jednak wąż porusza się w lewo, a gracz *szybko* naciśnie najpierw <kbd>up</kbd>, a potem <kbd>right</kbd> przed następnym krokiem ruchu, efekt będzie miało tylko naciśnięcie <kbd>right</kbd> i wąż wejdzie w samego siebie. Po dodaniu warunków do instrukcji `if` pokazanych powyżej takie wejście zostanie zignorowane. *Niedobrze!*

Właściwym rozwiązaniem tego problemu jest zapisanie wejścia w kolejce i pobieranie wpisów z tej kolejki podczas ruchu węża:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0

    self.dirqueue = {} -- <1>
end
```

Tym razem:
1. Dodaliśmy zmienną `self.dirqueue`, która jest inicjalizowana jako pusta tabela.

W funkcji `update()` dodaj:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed then
        local newdir = table.remove(self.dirqueue, 1) -- <1>
        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y -- <2>
            if not opposite then
                self.dir = newdir -- <3>
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tail = table.remove(self.segments, 1)
        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0)

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end
```

1. Pobierz pierwszy element z kolejki kierunków.
2. Jeśli istnieje element (`newdir` nie jest wartością null), sprawdź, czy `newdir` wskazuje kierunek przeciwny do `self.dir`.
3. Ustaw nowy kierunek tylko wtedy, gdy nie wskazuje kierunku przeciwnego.

I zmodyfikuj `on_input`, aby zamiast tego zapisywać bieżące wejście w kolejce:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1}) -- <1>
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

1. Dodaj kierunek wejścia do kolejki kierunków zamiast ustawiać bezpośrednio `self.dir`.

Uruchom grę i sprawdź, czy działa zgodnie z oczekiwaniami.

<input type="checkbox"/> Gotowe!

## Jedzenie i kolizja z przeszkodami

Wąż potrzebuje jedzenia na mapie, aby mógł rosnąć i przyspieszać. Dodajmy je!

### Tworzenie jedzenia

Nad funkcją `init()` dodaj nową funkcję:

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end
```

W tej funkcji:
1. Deklarujemy nową funkcję o nazwie `put_food()`, która umieszcza porcję jedzenia na mapie.
2. Zapisujemy losową pozycję X i Y w zmiennej o nazwie `self.food`.
3. Ustawiamy kafelek w pozycji X i Y na wartość 3, czyli grafikę kafelka jedzenia.

Następnie wywołaj ją na końcu funkcji `init()`:
```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    math.randomseed(socket.gettime()) -- <1>
    put_food(self) -- <2>
end
```

1. Zanim zaczniesz pobierać losowe wartości za pomocą `math.random()`, ustaw ziarno losowości, w przeciwnym razie wygenerowana zostanie ta sama seria losowych wartości. To ziarno powinno być ustawione tylko raz.
2. Wywołaj funkcję `put_food()` przy starcie gry, aby gracz zaczynał z elementem jedzenia na mapie.

<input type="checkbox"/> Gotowe!

### Zjadanie jedzenia

Teraz wykrywanie, czy wąż z czymś się zderzył, sprowadza się do sprawdzenia, co znajduje się na mapie kafelków w miejscu, do którego zmierza wąż, i zareagowania.

Dodaj zmienną śledzącą, czy wąż żyje:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true -- <1>

    math.randomseed(socket.gettime())
    put_food(self)
end
```

1. Flaga informująca, czy wąż żyje.

Następnie dodaj logikę sprawdzającą kolizję ze ścianą/przeszkodą oraz jedzeniem:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then -- <1>
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y) -- <2>

        if tile == 2 or tile == 4 then
            self.alive = false -- <3>
        elseif tile == 3 then
            self.speed = self.speed + 1 -- <4>
            put_food(self)
        else
            local tail = table.remove(self.segments, 1) -- <5>
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end
```

1. Przesuwaj węża tylko wtedy, gdy żyje.
2. Przed rysowaniem do mapy kafelków odczytaj, co znajduje się w pozycji, w której pojawi się nowa głowa węża.
3. Jeśli kafelek jest przeszkodą albo inną częścią węża, koniec gry!
4. Jeśli kafelek jest jedzeniem, zwiększ prędkość, a następnie umieść nowy element jedzenia.
5. Zauważ, że usunięcie ogona następuje tylko wtedy, gdy nie ma kolizji. Oznacza to, że jeśli gracz zje jedzenie, wąż urośnie o jeden segment, ponieważ w tym ruchu ogon nie zostanie usunięty.

Teraz wypróbuj grę i upewnij się, że działa dobrze!

To kończy samouczek, ale zachęcamy do dalszego eksperymentowania z grą i wykonania kilku poniższych ćwiczeń!

<input type="checkbox"/> Gotowe!

## Pełny skrypt

Oto kompletny kod skryptu dla odniesienia:

```lua
local function put_food(self)
    self.food = {x = math.random(2, 47), y = math.random(2, 47)}
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3)
end

function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true

    math.randomseed(socket.gettime())
    put_food(self)
end

function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y)

        if tile == 2 or tile == 4 then
            self.alive = false
        elseif tile == 3 then
            self.speed = self.speed + 1
            put_food(self)
        else
            local tail = table.remove(self.segments, 1)
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end

function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1})
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

## Ćwiczenia

Dobrym ćwiczeniem jest spróbowanie wdrożenia tych ulepszeń:

1. Dodaj obsługę klawisza do ponownego uruchomienia gry po jej zakończeniu.
2. Dodaj punktację i licznik punktów, używając samego komponentu etykiety (łatwiej) albo całego gui.
3. Funkcja put_food() nie uwzględnia pozycji węża ani żadnych przeszkód. Napraw ją tak, aby jedzenie pojawiało się tylko na wolnych polach.
4. Po zakończeniu gry pokaż komunikat “Game Over” i pozwól graczowi spróbować ponownie.
5. Dodatkowe zadanie: dodaj drugiego węża sterowanego przez gracza.
