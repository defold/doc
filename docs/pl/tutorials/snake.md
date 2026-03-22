---
title: Budowanie gry Snake w Defold
brief: Jeśli dopiero zaczynasz pracę z Defold, ten przewodnik pomoże ci wejść w logikę skryptów i poznać kilka podstawowych elementów Defold.
---

# Snake

Ten samouczek przeprowadzi cię przez proces tworzenia jednej z najpopularniejszych klasycznych gier, którą możesz spróbować odtworzyć. Istnieje wiele wariantów tej gry, a ta wersja zawiera węża, który zjada „jedzenie” i rośnie tylko wtedy, gdy coś zje. Wąż pełza też po planszy gry, na której znajdują się przeszkody.

## Tworzenie projektu

1. Uruchom Defold.
2. Po lewej stronie wybierz *New Project*.
3. Wybierz kartę *From Template*.
4. Wybierz *Empty Project*.
5. Wybierz lokalizację projektu na lokalnym dysku.
6. Kliknij <kbd>Create New Project</kbd>.

Otwórz plik ustawień *game.project* i ustaw wymiary gry na 768⨉768 albo na inną wielokrotność 16. Warto to zrobić, ponieważ gra będzie rysowana na siatce, na której każdy segment ma rozmiar 16x16 pikseli, a dzięki temu ekran gry nie odetnie żadnych częściowych segmentów.

## Dodawanie grafiki do gry

Do warstwy wizualnej potrzeba naprawdę niewiele. Jeden segment 16x16 dla węża, jeden dla przeszkód i jeden dla jedzenia. Ten obrazek to jedyny zasób, którego potrzebujesz. <kbd>Right click</kbd> obrazek, zapisz go na lokalnym dysku i przeciągnij do lokalizacji w folderze projektu.

![sprite'y węża](images/snake/snake.png)

Defold ma wbudowany komponent *Tilemap* (mapa kafelków), którego użyjesz do utworzenia planszy gry. Mapa kafelków pozwala ustawiać i odczytywać pojedyncze kafelki, więc ten projekt pasuje do niej idealnie. Ponieważ mapa kafelków pobiera grafiki z *Tilesource* (źródła kafelków), musisz takie źródło utworzyć:

<kbd>Right click</kbd> folder *main* i wybierz <kbd>New ▸ Tile Source</kbd>. Nazwij nowy plik "snake" (edytor zapisze plik jako "snake.tilesource").

Ustaw właściwość *Image* na plik grafiki, który właśnie zaimportowałeś.

Właściwości *Width* i *Height* powinny pozostać ustawione na 16. To podzieli obraz 32⨉32 piksele na 4 kafelki ponumerowane od 1 do 4.

![źródło kafelków](images/snake/tilesource.png)

Zwróć uwagę, że właściwość *Extrude Borders* ma ustawioną wartość 1 piksela. Ma to zapobiec artefaktom wizualnym wokół kafelków, których grafika dochodzi aż do krawędzi.

## Tworzenie mapy kafelków planszy

Teraz masz już gotowe źródło kafelków, więc czas utworzyć komponent mapy kafelków planszy:

<kbd>Right click</kbd> folder *main* i wybierz <kbd>New ▸ Tile Map</kbd>. Nazwij nowy plik "grid" (edytor zapisze plik jako "grid.tilemap").

![Set tilesource](images/snake/set_tilesource.png)

Ustaw właściwość *Tile Source* nowej mapy kafelków na "snake.tilesource".

Defold przechowuje tylko ten obszar mapy kafelków, który jest rzeczywiście używany, więc musisz dodać wystarczająco dużo kafelków, aby wypełnić granice ekranu.

Zaznacz warstwę "layer1".

Wybierz opcję menu <kbd>Edit ▸ Select Tile...</kbd>, aby wyświetlić paletę kafelków, a następnie kliknij kafelek, którego chcesz użyć do malowania.

Namaluj obramowanie wokół krawędzi ekranu i kilka przeszkód.

![tilemap](images/snake/tilemap.png)

Zapisz mapę kafelków, gdy skończysz.

## Dodawanie mapy kafelków i skryptu do gry

Teraz otwórz *main.collection*. To główna kolekcja bootstrapowa ładowana przy starcie silnika. <kbd>Right click</kbd> korzeń w *Outline* i wybierz <kbd>Add Game Object</kbd>, aby utworzyć nowy obiekt gry w kolekcji ładowanej wraz ze startem gry.

![add game object](images/snake/add_game_object.png)

Następnie <kbd>Right click</kbd> nowy obiekt gry i wybierz <kbd>Add Component File</kbd>. Wskaż plik "grid.tilemap", który właśnie utworzyłeś.

![add component](images/snake/add_component_file.png)

<kbd>Right click</kbd> folder *main* w przeglądarce *Assets* i wybierz <kbd>New ▸ Script</kbd>. Nazwij nowy plik skryptu "snake" (zostanie zapisany jako "snake.script"). Ten plik będzie przechowywał całą logikę gry.

Wróć do *main.collection* i <kbd>Right click</kbd> obiekt gry zawierający mapę kafelków. Wybierz <kbd>Add Component File</kbd> i wskaż plik "snake.script".

Teraz masz już na miejscu komponent mapy kafelków i skrypt. Jeśli uruchomisz grę, powinieneś zobaczyć planszę taką, jaką narysowałeś na mapie kafelków.

![main collection](images/snake/main_collection_no_gui.png)

## Skrypt gry - inicjalizacja

Skrypt, który napiszesz, będzie sterował całą grą. Pomysł na to, jak ma to działać, jest następujący:

1. Skrypt przechowuje listę pozycji kafelków, które obecnie zajmuje wąż.
2. Jeśli gracz naciśnie klawisz kierunku, zapisz kierunek, w którym wąż powinien się poruszać.
3. W regularnych odstępach czasu przesuwaj węża o jeden krok w bieżącym kierunku ruchu.

Otwórz *snake.script* i znajdź funkcję `init()`. Ta funkcja jest wywoływana przez silnik, gdy skrypt zostaje zainicjalizowany przy starcie gry. Zmień kod na następujący:

```lua
function init(self)
    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24} } -- <1>
    self.dir = {x = 1, y = 0} -- <2>
    self.speed = 7.0 -- <3>

    self.t = 0 -- <4>
end
```
1. Zapisz segmenty węża jako tabelę Lua zawierającą listę tabel, z których każda przechowuje pozycję X i Y jednego segmentu.
2. Zapisz bieżący kierunek jako tabelę przechowującą kierunek X i Y.
3. Zapisz bieżącą prędkość ruchu wyrażoną w kafelkach na sekundę.
4. Zapisz wartość timera, który będzie służył do śledzenia prędkości ruchu.

Powyższy kod skryptu jest zapisany w języku Lua. Warto zwrócić uwagę na kilka rzeczy:

- Defold rezerwuje zestaw wbudowanych funkcji zwrotnych, które są wywoływane w czasie życia komponentu skryptowego. To *nie są* metody, tylko zwykłe funkcje. W czasie działania silnik przekazuje odwołanie do bieżącej instancji komponentu skryptowego przez parametr `self`. To odwołanie `self` służy do przechowywania danych instancji.
- Literały tabel Lua zapisuje się w nawiasach klamrowych. Elementy tabeli mogą być parami klucz/wartość (`{x = 10, y = 20}`), zagnieżdżonymi tabelami Lua (`{ {a = 1}, {b = 2} a}`) albo innymi typami danych.
- Referencję `self` można traktować jak tabelę Lua, w której możesz przechowywać dane. Wystarczy używać notacji kropkowej tak samo jak przy każdej innej tabeli: `self.data = "value"`. Ta referencja jest ważna przez cały czas życia skryptu, w tym przypadku od startu gry aż do jej zamknięcia.

Jeśli nie zrozumiałeś wszystkiego powyżej, nie martw się. Po prostu idź dalej, eksperymentuj i daj sobie czas - w końcu to załapiesz.

## Skrypt gry - aktualizacja

Funkcja `init()` jest wywoływana dokładnie raz, gdy komponent skryptowy zostaje utworzony w działającej grze. Natomiast funkcja `update()` jest wywoływana raz na klatkę, 60 razy na sekundę. To sprawia, że idealnie nadaje się do logiki gry działającej w czasie rzeczywistym.

Pomysł na aktualizację jest taki:

1. W określonym odstępie czasu wykonaj następujące kroki:
2. Spójrz na głowę węża, a potem utwórz nową głowę przesuniętą względem bieżącej głowy o bieżący kierunek ruchu. Jeśli więc wąż porusza się z X=-1 i Y=0, a bieżąca głowa znajduje się w X=32 i Y=10, nowa głowa powinna mieć X=31 i Y=10.
3. Dodaj nową głowę do listy segmentów, z których składa się wąż.
4. Usuń ogon z tabeli segmentów.
5. Wyczyść kafelek ogona.
6. Narysuj segmenty węża.

Znajdź funkcję `update()` w *snake.script* i zmień kod na następujący:

```lua
function update(self, dt)
    self.t = self.t + dt -- <1>
    if self.t >= 1.0 / self.speed then -- <2>
        local head = self.segments[#self.segments] -- <3>
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y} -- <4>

        table.insert(self.segments, newhead) -- <5>

        local tail = table.remove(self.segments, 1) -- <6>
        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0) -- <7>

        for i, s in ipairs(self.segments) do -- <8>
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2) -- <9>
        end

        self.t = 0 -- <10>
    end
end
```
1. Zwiększ timer o różnicę czasu (w sekundach) od ostatniego wywołania `update()`.
2. Jeśli timer odmierzył już wystarczająco dużo czasu.
3. Pobierz bieżący segment głowy. `#` to operator służący do pobierania długości tabeli użytej jako tablica, a tak właśnie jest tutaj - wszystkie segmenty są wartościami tabeli bez określonych kluczy.
4. Utwórz nowy segment głowy na podstawie bieżącej pozycji głowy i kierunku ruchu (`self.dir`).
5. Dodaj nową głowę na końcu tabeli segmentów.
6. Usuń ogon z początku tabeli segmentów.
7. Wyczyść kafelek w pozycji usuniętego ogona.
8. Przejdź przez elementy tabeli segmentów. Przy każdej iteracji `i` będzie ustawione na pozycję w tabeli (zaczynając od 1), a `s` na bieżący segment.
9. Ustaw kafelek w pozycji segmentu na wartość 2, która odpowiada zielonemu kafelkowi węża.
10. Gdy skończysz, zresetuj timer do zera.

Jeśli teraz uruchomisz grę, powinieneś zobaczyć węża o długości 4 segmentów pełzającego z lewej do prawej po planszy.

![uruchom grę](images/snake/run_1.png)

## Wejście gracza

Zanim dodasz kod reagujący na wejście gracza, musisz skonfigurować wiązania wejść. Znajdź plik *input/game.input_binding* w przeglądarce *Assets* i <kbd>double click</kbd>, aby go otworzyć. Dodaj zestaw wiązań *Key Trigger* dla ruchu w górę, w dół, w lewo i w prawo.

![wejście](images/snake/input.png)

Plik wiązań wejść mapuje rzeczywiste wejście użytkownika (klawisze, ruchy myszy itd.) na *nazwy* akcji, które trafiają do skryptów proszących o przechwycenie wejścia. Gdy wiązania są już gotowe, otwórz *snake.script* i dodaj następujący kod:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24} }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0

    self.t = 0
end
```
1. Wyślij wiadomość do bieżącego obiektu gry ("." to skrót oznaczający bieżący obiekt gry), nakazując mu rozpoczęcie odbierania wejścia od silnika.

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
1. Jeśli zostanie odebrana akcja wejścia "up", skonfigurowana we wiązaniach wejść, i tabela `action` ma pole `pressed` ustawione na `true` (gracz nacisnął klawisz), wtedy:
2. Ustaw kierunek ruchu.

Uruchom grę ponownie i sprawdź, czy możesz sterować wężem.

Zwróć teraz uwagę, że jeśli naciśniesz dwa klawisze jednocześnie, spowoduje to dwa wywołania `on_input()`, po jednym dla każdego naciśnięcia. W kodzie zapisanym powyżej tylko wywołanie, które nastąpi jako ostatnie, wpłynie na kierunek węża, ponieważ kolejne wywołania `on_input()` nadpiszą wartości w `self.dir`.

Zwróć też uwagę, że jeśli wąż porusza się w lewo i naciśniesz klawisz <kbd>right</kbd>, wąż skręci w samego siebie. *Pozornie* oczywistym rozwiązaniem tego problemu jest dodanie dodatkowego warunku do klauzul `if` w `on_input()`:

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

Jeśli jednak wąż porusza się w lewo, a gracz *szybko* naciśnie najpierw <kbd>up</kbd>, a potem <kbd>right</kbd> przed kolejnym ruchem, wpływ będzie miał tylko nacisk <kbd>right</kbd> i wąż skręci w samego siebie. Po dodaniu powyższych warunków do klauzul `if` wejście zostanie zignorowane. *Niedobrze!*

Prawidłowym rozwiązaniem tego problemu jest zapisanie wejścia w kolejce i pobieranie z niej wpisów, gdy wąż się porusza:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24} }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {} -- <1>
    self.speed = 7.0

    self.t = 0
end

function update(self, dt)
    self.t = self.t + dt
    if self.t >= 1.0 / self.speed then
        local newdir = table.remove(self.dirqueue, 1) -- <2>
        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y -- <3>
            if not opposite then
                self.dir = newdir -- <4>
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

        self.t = 0
    end
end

function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1}) -- <5>
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```
1. Zainicjalizuj pustą tabelę, która będzie przechowywać kolejkę kierunków wejścia.
2. Pobierz pierwszy element z kolejki kierunków.
3. Jeśli istnieje element (`newdir` nie jest `nil`), sprawdź, czy `newdir` wskazuje w kierunku przeciwnym do `self.dir`.
4. Ustaw nowy kierunek tylko wtedy, gdy nie wskazuje on w przeciwną stronę.
5. Dodawaj kierunek wejścia do kolejki kierunków zamiast ustawiać `self.dir` bezpośrednio.

Uruchom grę i sprawdź, czy działa zgodnie z oczekiwaniami.

## Jedzenie i kolizje z przeszkodami

Wąż potrzebuje jedzenia na mapie, żeby mógł rosnąć i poruszać się szybciej. Dodajmy to!

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end

function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24} }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.t = 0

    math.randomseed(socket.gettime()) -- <4>
    put_food(self) -- <5>
end
```
1. Zdefiniuj nową funkcję `put_food()`, która umieszcza na mapie porcję jedzenia.
2. Zapisz losową pozycję X i Y w zmiennej `self.food`.
3. Ustaw kafelek w pozycji X i Y na wartość 3, która odpowiada grafice kafelka jedzenia.
4. Zanim zaczniesz pobierać losowe wartości za pomocą `math.random()`, ustaw ziarno generatora losowego, bo w przeciwnym razie będzie generowana ta sama sekwencja losowych wartości. To ziarno powinno być ustawione tylko raz.
5. Wywołaj funkcję `put_food()` na starcie gry, aby gracz zaczynał z jedzeniem na mapie.

Teraz wykrywanie, czy wąż zderzył się z czymkolwiek, sprowadza się do sprawdzenia, co znajduje się na mapie kafelków w miejscu, w które wąż zmierza, i odpowiedniej reakcji. Dodaj zmienną śledzącą, czy wąż żyje:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24} }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.alive = true -- <1>
    self.t = 0

    math.randomseed(socket.gettime())
    put_food(self)
end
```
1. Flaga informująca, czy wąż żyje.

Następnie dodaj logikę sprawdzającą kolizję ze ścianą/przeszkodą i z jedzeniem:

```lua
function update(self, dt)
    self.t = self.t + dt
    if self.t >= 1.0 / self.speed and self.alive then -- <1>
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

        self.t = 0
    end
end
```
1. Przesuwaj węża tylko wtedy, gdy żyje.
2. Zanim narysujesz coś na mapie kafelków, odczytaj to, co znajduje się w miejscu, w które trafi nowa głowa węża.
3. Jeśli kafelek jest przeszkodą albo inną częścią węża, gra się kończy!
4. Jeśli kafelek jest jedzeniem, zwiększ prędkość, a następnie umieść nowe jedzenie.
5. Zwróć uwagę, że usunięcie ogona następuje tylko wtedy, gdy nie dochodzi do kolizji. Oznacza to, że jeśli gracz zje jedzenie, wąż urośnie o jeden segment, ponieważ w tym ruchu ogon nie zostanie usunięty.

Teraz spróbuj uruchomić grę i upewnij się, że działa dobrze!

Na tym kończy się samouczek, ale zachęcamy do dalszych eksperymentów z grą i wykonania kilku ćwiczeń poniżej!

## Pełny skrypt

Oto pełny kod skryptu do wykorzystania jako punkt odniesienia:

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
        {x = 10, y = 24} }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.alive = true
    self.t = 0

    math.randomseed(socket.gettime())
    put_food(self)
end

function update(self, dt)
    self.t = self.t + dt
    if self.t >= 1.0 / self.speed and self.alive then
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

        self.t = 0
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

Wersja gry, którą możesz zagrać na początku tego samouczka, zawiera kilka dodatkowych usprawnień. Dobrym ćwiczeniem będzie spróbowanie zaimplementowania tych ulepszeń:

1. Dodaj punktację i licznik punktów.
2. Funkcja `put_food()` nie uwzględnia pozycji węża ani tego, gdzie znajdują się przeszkody. Napraw to.
3. Jeśli gra się kończy, pokaż komunikat "game over", a potem pozwól graczowi spróbować ponownie.
4. Dodatkowe punkty: dodaj węża dla gracza 2.
