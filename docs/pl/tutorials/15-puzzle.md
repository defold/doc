---
title: Tworzenie gry 15 puzzle w Defold
brief: Jeśli dopiero zaczynasz pracę z Defold, ten przewodnik pomoże ci poćwiczyć kilka podstawowych elementów składowych silnika i uruchamianie logiki skryptów.
---

# Klasyczne 15 puzzle

Ta dobrze znana łamigłówka zyskała popularność w Ameryce w latach 70. XIX wieku. Celem gry jest uporządkowanie kafelków na planszy przez przesuwanie ich w poziomie i pionie. Łamigłówka zaczyna się od układu, w którym kafelki są pomieszane.

Najczęściej spotykana wersja pokazuje na kafelkach liczby 1--15. Możesz jednak trochę zwiększyć poziom trudności, wykorzystując jako kafelki fragmenty obrazka. Zanim zaczniemy, spróbuj rozwiązać łamigłówkę. Kliknij kafelek sąsiadujący z pustym polem, aby przesunąć go na puste miejsce.

## Tworzenie projektu

1. Uruchom Defold.
2. Po lewej stronie wybierz *New Project*.
3. Wybierz kartę *From Template*.
4. Wybierz *Empty Project*
5. Wybierz lokalizację projektu na dysku.
6. Kliknij *Create New Project*.

Otwórz plik ustawień *game.project* i ustaw wymiary gry na 512⨉512. Będą one odpowiadać obrazowi, którego użyjesz.

![Ustawienia wyświetlania](images/15-puzzle/display_settings.png)

Następnym krokiem jest pobranie odpowiedniego obrazka do łamigłówki. Wybierz dowolny kwadratowy obraz, ale pamiętaj, aby przeskalować go do 512 na 512 pikseli. Jeśli nie chcesz samodzielnie szukać obrazka, możesz użyć tego:

![Mona Lisa](images/15-puzzle/monalisa.png)

Pobierz obraz, a następnie przeciągnij go do folderu *main* w projekcie.

## Reprezentacja siatki

Defold zawiera wbudowany komponent *Tilemap* (mapa kafelków), który świetnie nadaje się do wizualizacji planszy łamigłówki. Mapy kafelków pozwalają ustawiać i odczytywać pojedyncze kafelki, a to w tym projekcie w zupełności wystarczy.

Zanim jednak utworzysz mapę kafelków, potrzebujesz zasobu *Tilesource* (źródło kafelków), z którego mapa będzie pobierać obrazy kafelków.

<kbd>Kliknij prawym przyciskiem myszy</kbd> folder *main* i wybierz <kbd>New ▸ Tile Source</kbd>. Nazwij nowy plik `monalisa.tilesource`.

Ustaw właściwości *Width* i *Height* kafelka na 128. Dzięki temu obraz o wymiarach 512⨉512 pikseli zostanie podzielony na 16 kafelków. Kafelki otrzymają numery 1--16, gdy umieścisz je na mapie kafelków.

![Źródło kafelków](images/15-puzzle/tilesource.png)

Następnie <kbd>Kliknij prawym przyciskiem myszy</kbd> folder *main* i wybierz <kbd>New ▸ Tile Map</kbd>. Nazwij nowy plik "grid.tilemap".

Defold wymaga zainicjalizowania siatki. W tym celu zaznacz warstwę "layer1" i namaluj siatkę kafelków 4⨉4 tuż na prawo od początku układu współrzędnych. Nie ma większego znaczenia, jakie kafelki ustawisz. Za chwilę dodasz kod, który automatycznie ustawi ich zawartość.

![Mapa kafelków](images/15-puzzle/tilemap.png)

## Składanie całości

Otwórz *main.collection*. <kbd>Kliknij prawym przyciskiem myszy</kbd> węzeł główny w *Outline* i wybierz <kbd>Add Game Object</kbd>. Ustaw właściwość *Id* nowego obiektu gry na "game".

<kbd>Kliknij prawym przyciskiem myszy</kbd> obiekt gry i wybierz <kbd>Add Component File</kbd>. Wskaż plik *grid.tilemap*. Ustaw właściwość *Id* na "tilemap".

<kbd>Kliknij prawym przyciskiem myszy</kbd> obiekt gry i wybierz <kbd>Add Component ▸ Label</kbd>. Ustaw właściwość *Id* etykiety na "done", a jej właściwość *Text* na "Brawo". Przesuń etykietę na środek mapy kafelków.

Ustaw pozycję Z etykiety na 1, aby mieć pewność, że zostanie narysowana nad siatką.

![Główna kolekcja](images/15-puzzle/main_collection.png)

Następnie utwórz plik skryptu Lua dla logiki łamigłówki: <kbd>Kliknij prawym przyciskiem myszy</kbd> folder *main* i wybierz <kbd>New ▸ Script</kbd>. Nazwij nowy plik "game.script".

Potem <kbd>Kliknij prawym przyciskiem myszy</kbd> obiekt gry o nazwie "game" w *main.collection* i wybierz <kbd>Add Component File</kbd>. Wskaż plik *game.script*.

Uruchom grę. Powinieneś zobaczyć siatkę taką, jaką narysowałeś, oraz etykietę z komunikatem "Brawo" nad nią.

## Logika łamigłówki

Teraz masz już wszystkie elementy na miejscu, więc reszta tutoriala będzie poświęcona złożeniu logiki łamigłówki.

Skrypt będzie przechowywał własną reprezentację kafelków planszy, niezależną od mapy kafelków. Dzięki temu łatwiej będzie na niej operować. Zamiast przechowywać kafelki w tablicy dwuwymiarowej, będą one zapisane jako jednowymiarowa lista w tabeli Lua. Lista zawiera numery kafelków po kolei, zaczynając od lewego górnego rogu siatki aż do prawego dolnego:

```lua
-- Ukończona plansza wygląda tak:
self.board = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}
```

Kod, który bierze taką listę kafelków i rysuje ją na mapie kafelków, jest całkiem prosty, ale musi przeliczyć pozycję na liście na współrzędne x i y:

```lua
-- Narysuj listę kafelków z tabeli na mapie 4x4
local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4) -- <1>
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end
```
1. W mapach kafelków kafelek o wartości x równej 1 i y równej 1 znajduje się w lewym dolnym rogu. Dlatego pozycję y trzeba odwrócić.

Możesz sprawdzić, czy funkcja działa zgodnie z oczekiwaniami, tworząc testową funkcję `init()`:

```lua
function init(self)
    -- Odwrócona plansza do testów
    self.board = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    draw(self.board)
end
```

Gdy kafelki są zapisane jako lista w tabeli Lua, pomieszanie ich kolejności jest bardzo proste. Kod przechodzi po każdym elemencie listy i zamienia każdy kafelek z innym, losowo wybranym:

```lua
-- Zamień miejscami dwa elementy na liście w tabeli
local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

-- Wylosuj kolejność elementów na liście w tabeli
local function scramble(t)
    local n = #t
    for i = 1, n - 1 do
        t = swap(t, i, math.random(i, n))
    end
    return t
end
```

Zanim przejdziesz dalej, musisz uwzględnić jedną ważną rzecz dotyczącą 15 puzzle: jeśli losowo ustawisz kolejność kafelków tak jak powyżej, istnieje 50% szans, że łamigłówki *nie da się* rozwiązać.

To zła wiadomość, bo na pewno nie chcesz dawać graczowi układu, którego nie można ukończyć.

Na szczęście da się ustalić, czy dany układ jest rozwiązywalny. Oto jak:

## Rozwiązywalność

Aby sprawdzić, czy pozycja w łamigłówce 4⨉4 jest rozwiązywalna, potrzebne są dwie informacje:

1. Liczba "inwersji" w układzie. Inwersja występuje wtedy, gdy przed kafelkiem stoi inny kafelek z mniejszym numerem. Na przykład lista `{1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 0}` ma 3 inwersje:

    - liczba 12 ma za sobą 11 i 10, co daje 2 inwersje.
    - liczba 11 ma za sobą 10, co daje jeszcze 1 inwersję.

    (Zwróć uwagę, że rozwiązany stan łamigłówki ma zero inwersji)

2. Wiersz, w którym znajduje się puste pole (oznaczone na liście przez `0`).

Te dwie liczby można obliczyć za pomocą następujących funkcji:

```lua
-- Policz liczbę inwersji na liście kafelków
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then -- <1>
                inv = inv + 1
            end
        end
    end
    return inv
end
```
1. Zwróć uwagę, że puste pole się nie liczy.

```lua
-- Znajdź pozycję x i y wskazanego kafelka
local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4) -- <1>
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end
```
1. Pozycja Y liczona od dołu.

Mając te dwie liczby, można określić, czy stan łamigłówki jest rozwiązywalny. Stan planszy 4⨉4 jest *rozwiązywalny*, jeśli:

- jeśli puste pole znajduje się w *nieparzystym* wierszu (1 lub 3 licząc od dołu), a liczba inwersji jest *parzysta*.
- jeśli puste pole znajduje się w *parzystym* wierszu (2 lub 4 licząc od dołu), a liczba inwersji jest *nieparzysta*.

## Jak to działa?

Każdy dozwolony ruch przesuwa element przez zamianę jego miejsca z pustym polem, poziomo albo pionowo.

Przesunięcie elementu w poziomie nie zmienia liczby inwersji ani numeru wiersza, w którym znajduje się puste pole.

Przesunięcie elementu w pionie zmienia natomiast parzystość liczby inwersji (z nieparzystej na parzystą albo z parzystej na nieparzystą). Zmienia też parzystość wiersza pustego pola.

Na przykład:

![Przesuwanie elementu](images/15-puzzle/slide.png)

Ten ruch zmienia kolejność kafelków z:

`{ ... 0, 11, 2, 13, 6 ... }`

na

`{ ... 6, 11, 2, 13, 0 ... }`

Nowy stan dodaje 3 inwersje w następujący sposób:

- liczba 6 dodaje 1 inwersję (liczba 2 znajduje się teraz po 6)
- liczba 11 traci 1 inwersję (liczba 6 znajduje się teraz przed 11)
- liczba 13 traci 1 inwersję (liczba 6 znajduje się teraz przed 13)

Liczba inwersji po pionowym przesunięciu może zmienić się o ±1 albo ±3.

Numer wiersza pustego pola po pionowym przesunięciu może zmienić się o ±1.

W końcowym stanie łamigłówki puste pole znajduje się w prawym dolnym rogu (w *nieparzystym* wierszu 1), a liczba inwersji ma *parzystą* wartość 0. Każdy dozwolony ruch albo pozostawia te dwie wartości bez zmian (ruch poziomy), albo zmienia ich parzystość (ruch pionowy). Żaden dozwolony ruch nigdy nie sprawi, że parzystość liczby inwersji i wiersza pustego pola będzie *nieparzysta*, *nieparzysta* albo *parzysta*, *parzysta*.

Dlatego każdego stanu łamigłówki, w którym obie liczby są jednocześnie nieparzyste albo jednocześnie parzyste, nie da się rozwiązać.

Oto kod sprawdzający rozwiązywalność:

```lua
-- Sprawdź, czy podana lista kafelków 4x4 jest rozwiązywalna
local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end
```

## Dane wejściowe użytkownika

Pozostało już tylko sprawić, by łamigłówka była interaktywna.

Utwórz funkcję `init()`, która wykona całą konfigurację w czasie działania programu przy użyciu funkcji utworzonych wcześniej:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>
    math.randomseed(socket.gettime()) -- <2>
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}) -- <3>
    while not solvable(self.board) do -- <4>
        self.board = scramble(self.board)
    end
    draw(self.board) -- <5>
    self.done = false -- <6>
    msg.post("#done", "disable") -- <7>
end
```
1. Poinformuj silnik, że ten obiekt gry ma odbierać dane wejściowe.
2. Zainicjalizuj generator liczb losowych.
3. Utwórz początkowy losowy stan planszy.
4. Jeśli stan jest nierozwiązywalny, przetasuj planszę ponownie.
5. Narysuj planszę.
6. Ustaw flagę ukończenia do śledzenia stanu wygranej.
7. Wyłącz etykietę z komunikatem ukończenia.

Otwórz */input/game.input_bindings* i dodaj nowy *Mouse Trigger*. Ustaw nazwę akcji na "press":

![Wejście](images/15-puzzle/input.png)

Wróć do skryptu i utwórz funkcję `on_input()`.

```lua
-- Obsłuż wejście użytkownika
function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then -- <1>
        local x = math.ceil(action.x / 128) -- <2>
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0) -- <3>
        if math.abs(x - ex) + math.abs(y - ey) == 1 then -- <4>
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x) -- <5>
            draw(self.board) -- <6>
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then -- <7>
            self.done = true
            msg.post("#done", "enable")
        end
    end
end
```
1. Jeśli naciśnięto przycisk myszy i gra nadal trwa, wykonaj następujące czynności.
2. Oblicz współrzędne x i y pola, które kliknął użytkownik.
3. Znajdź bieżące położenie pustego pola (`0`).
4. Jeśli kliknięte pole znajduje się dokładnie nad pustym polem, pod nim, po jego lewej albo prawej stronie, wykonaj następujące czynności:
5. Zamień miejscami kafelek z klikniętego pola i puste pole.
6. Narysuj zaktualizowaną planszę ponownie.
7. Jeśli liczba inwersji na planszy wynosi 0, co oznacza, że wszystko jest we właściwej kolejności, a puste pole znajduje się w skrajnej prawej kolumnie (musi być wtedy w ostatnim wierszu, aby liczba inwersji wynosiła 0), łamigłówka jest rozwiązana, więc wykonaj następujące czynności:
8. Ustaw flagę ukończenia.
9. Włącz/pokaż komunikat o ukończeniu.

I to wszystko! Gotowe, gra z łamigłówką jest ukończona!

## Pełny skrypt

Poniżej znajduje się kompletny kod skryptu do wglądu:

```lua
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then
                inv = inv + 1
            end
        end
    end
    return inv
end

local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4)
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end

local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end

local function scramble(t)
    for i=1, #t do
        local tmp = t[i]
        local r = math.random(#t)
        t[i] = t[r]
        t[r] = tmp
    end
    return t
end

local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4)
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end

function init(self)
    msg.post(".", "acquire_input_focus")
    math.randomseed(socket.gettime())
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0})   
    while not solvable(self.board) do
        self.board = scramble(self.board)
    end
    draw(self.board)
    self.done = false
    msg.post("#done", "disable")
end

function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then
        local x = math.ceil(action.x / 128)
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0)
        if math.abs(x - ex) + math.abs(y - ey) == 1 then
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x)
            draw(self.board)
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then
            self.done = true
            msg.post("#done", "enable")
        end
    end
end

function on_reload(self)
    self.done = false
    msg.post("#done", "disable")
end
```

## Dalsze ćwiczenia

1. Zrób łamigłówkę 5⨉5, a potem 6⨉5. Upewnij się, że sprawdzanie rozwiązywalności działa poprawnie w ogólnym przypadku.
2. Dodaj animacje przesuwania. Kafelków nie da się przesuwać niezależnie od mapy kafelków, więc musisz wymyślić sposób na obejście tego ograniczenia. Być może osobna mapa kafelków zawierająca tylko przesuwany element okaże się dobrym rozwiązaniem?
