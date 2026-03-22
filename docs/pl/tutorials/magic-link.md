---
title: Samouczek Magic Link
brief: W tym samouczku zbudujesz kompletną, niewielką grę logiczną z ekranem startowym, mechaniką rozgrywki i prostym postępem poziomów w formie rosnącego poziomu trudności.
---

# Samouczek Magic Link

Ta gra jest odmianą klasycznej gry w dopasowywanie w stylu _Bejeweled_ i _Candy Crush_. Gracz przeciąga i łączy bloki tego samego koloru, aby je usuwać, ale celem gry nie jest usuwanie długich sekwencji bloków w tym samym kolorze, czyszczenie planszy ani zdobywanie punktów, tylko połączenie zestawu specjalnych „magicznych bloków” rozrzuconych po planszy.

Ten samouczek został napisany jako przewodnik krok po kroku, w którym budujemy grę na podstawie kompletnego projektu. W praktyce znalezienie projektu, który działa, wymaga dużo czasu i wysiłku. Możesz zacząć od rdzennej idei, a potem znaleźć sposób, by ją prototypować i lepiej zrozumieć, co ta idea może wnieść do gry. Nawet tak prosta gra jak „Magic Link” wymaga całkiem sporo pracy projektowej. Ta gra przeszła kilka iteracji i trochę eksperymentów, zanim osiągnęła swoją ostateczną postać i zestaw zasad, który nadal jest daleki od ideału. Na potrzeby tego samouczka pominiemy jednak ten proces i zaczniemy od budowania finalnego projektu.

## Pierwsze kroki

Najpierw musisz utworzyć nowy projekt i zaimportować pakiet zasobów:

* Utwórz [nowy projekt](/manuals/project-setup/#creating-a-new-project) z szablonu <kbd>Empty Project</kbd>
* Pobierz kompletny projekt „Magic Link” jako odniesienie: [magic-link.zip](https://github.com/defold/defold-examples/releases/latest). Kompletny projekt zawiera wszystkie zasoby, jeśli chcesz utworzyć projekt od zera.

## Zasady gry

![Schemat zasad gry](images/magic-link/linker_rules.png)

Plansza jest losowo wypełniana kolorowymi blokami oraz zestawem magicznych bloków w każdej rundzie. Kolorowe bloki podlegają następującym zasadom:

* Znikają, jeśli gracz połączy je z blokami tego samego koloru, przeciągając po nich.
* Gdy bloki znikają, zostawiają po sobie puste miejsca poniżej. Kolorowe bloki po prostu spadają pionowo w dół do pustych miejsc, które pojawiły się pod nimi.
* Dół ekranu zatrzymuje wszystkie bloki przed dalszym spadaniem.

Magiczne bloki zachowują się inaczej, zgodnie z tymi zasadami:

* Magiczne bloki przesuwają się _na boki_, jeśli po którejś stronie pojawi się wolne miejsce.
* Jeśli pojawi się pod nimi dziura, spadają tak jak zwykłe kolorowe bloki.

Gracz wchodzi w interakcję z grą zgodnie z następującymi zasadami:

* Gracz może przeciągać i łączyć kolorowe bloki, które sąsiadują poziomo, pionowo i po skosie.
* Połączone bloki znikają, gdy tylko gracz puści dotykowe wejście, czyli uniesie palec.
* Magiczne bloki nie reagują na przeciąganie i nie można ich ręcznie łączyć.
* Magiczne bloki reagują jednak na połączenie poziome lub pionowe. Innymi słowy, w takich sytuacjach łączą się automatycznie.
* Poziom zostaje ukończony, jeśli gracz zdoła automatycznie połączyć wszystkie magiczne bloki na planszy.

Poziom trudności określa liczbę magicznych bloków umieszczonych na planszy.

## Omówienie

Jak w przypadku każdego projektu, musimy najpierw opracować plan, jak podejść do implementacji w ogólnych zarysach. Taka gra może być zbudowana na wiele sposobów. Technicznie moglibyśmy zaimplementować całą grę w systemie GUI, gdybyśmy chcieli. Jednak budowanie gry z użyciem obiektów gry i sprite'ów oraz korzystanie z interfejsów API GUI do elementów na ekranie i HUD-u to najczęściej naturalny sposób tworzenia gry, więc pójdziemy właśnie tą drogą.

Ponieważ liczba plików powinna pozostać stosunkowo niewielka, utrzymamy strukturę folderów projektu bardzo prostą:

![Struktura folderów](images/magic-link/linker_folders.png)

*main*
: Ten folder będzie zawierał całą logikę gry. Wszystkie skrypty, pliki obiektów gry, pliki kolekcji, pliki GUI i tak dalej będą znajdować się w tym folderze. Jeśli chcesz podzielić go na kilka folderów albo zachować podfoldery, to też jest całkowicie w porządku.

*images*
: Wszystkie zasoby graficzne będą przechowywane w tym folderze.

*fonts*
: Czcionki używane do renderowania tekstu trafiają tutaj.

*input*
: Wiązania wejść są przechowywane w tym folderze.

## Konfiguracja projektu

Plik *game.project* pozostaje w większości ustawiony według wartości domyślnych, ale trzeba zdecydować o kilku parametrach. Przede wszystkim musimy wybrać rozdzielczość gry. Później dość łatwo ją zmienić, a w finalnej grze trzeba będzie jeszcze trochę popracować, aby wyglądała dobrze niezależnie od rozdzielczości lub proporcji ekranu urządzenia docelowego.

Wybraliśmy rozdzielczość 640x960 pikseli, czyli natywną rozdzielczość iPhone'a 4. To także rozdzielczość, która pasuje do wielu monitorów, więc testowanie na komputerze przebiega wygodnie. Jeśli chcesz pracować w innej rozdzielczości, wystarczy, że odpowiednio dostosujesz kilka wartości.

![Ustawienia projektu](images/magic-link/linker_project_settings.png)

Musimy też zwiększyć maksymalną liczbę renderowanych sprite'ów. Jeśli chcesz, możesz od razu przejść do następnej sekcji i wrócić tutaj, gdy w konsoli pojawi się informacja, że osiągnięto limit sprite'ów.

![Układ skalowania gry](images/magic-link/linker_layout.png)

Możemy obliczyć maksymalną potrzebną liczbę sprite'ów:

* Plansza gry będzie zawierała 7x9 bloków. Potrzeba też pewnego marginesu wokół krawędzi oraz miejsca u góry na elementy GUI. Oznacza to, że bloki będą miały w przybliżeniu rozmiar 90x90 pikseli. Mniejsze byłyby zbyt małe, by wygodnie wchodzić z nimi w interakcję na ekranie małego telefonu.
* Każdy blok to jeden sprite. Użyjemy animacji jednoklatkowych, aby ustawiać kolor bloku.
* Część bloków będzie magiczna, a do efektów specjalnych na każdym z nich użyjemy 4 sprite'ów.
* Grafika łączenia będzie wymagała jednego sprite'a na element. W najgorszym przypadku oznacza to dodatkowe 61 sprite'ów, jeśli gracz w jakiś sposób połączy całą planszę (minus 2 magiczne bloki, których nie można łączyć przez przeciąganie).

Załóżmy więc, że maksymalnie mamy 30 magicznych bloków. Plansza ma 63 bloki (sprite'y). Z nich 30 magicznych bloków dodaje po 4 sprite'y efektów specjalnych. To kolejne 120 sprite'ów. Z grafiką łączenia, której maksymalnie może być 33, musimy więc wyrenderować co najmniej 120 + 33 = 153 sprite'y w każdej klatce. Najbliższa potęga dwójki to 256.

Jednak ustawienie limitu na 256 nie wystarczy. Za każdym razem, gdy czyścimy i resetujemy planszę, usuwamy wszystkie bieżące obiekty gry i tworzymy nowe. Liczba sprite'ów musi uwzględniać wszystkie obiekty, które żyją w danej klatce. Dotyczy to również usuwanych obiektów, ponieważ są one usuwane dopiero na końcu klatki. Ustawienie maksymalnej liczby sprite'ów na 512 będzie więc wystarczające.

![Maksymalna liczba sprite'ów](images/magic-link/linker_sprite_max_count.png)

## Dodawanie zasobów graficznych

Wszystkie potrzebne zasoby gry zostały przygotowane wcześniej. Dodajemy je jako obrazy 512x512 pikseli i pozwalamy silnikowi przeskalować je do docelowego rozmiaru.

::: sidenote
Włączenie opcji *hidpi* w ustawieniach projektu oznacza, że backbuffer będzie miał wysoką rozdzielczość. Dzięki temu, że rysujemy duże obrazy i skalujemy je w dół, będą one wyglądały bardzo ostro na ekranach Retina.
:::

![Dodawanie obrazów](images/magic-link/linker_add_images.png)

Oprócz bloków dołączony jest obraz „connector” oraz sprite'y efektów. Mamy też dwa obrazy tła. Jeden będzie używany jako tło planszy, a drugi jako tło głównego menu. Dodaj wszystkie obrazy do folderu *images*, a następnie utwórz plik atlasu *sprites.atlas*. Otwórz atlas i dodaj do niego wszystkie obrazy.

![Dodawanie obrazów do atlasu](images/magic-link/linker_add_to_atlas.png)

Istnieje też zestaw obrazów GUI używanych do tworzenia elementów interfejsu, takich jak przyciski i wyskakujące okna. Są one dodawane do osobnego atlasu o nazwie *gui.atlas*.

## Generowanie planszy

Pierwszym krokiem jest zbudowanie logiki planszy. Plansza będzie znajdować się we własnej kolekcji, która będzie zawierała wszystko, co ma być widoczne na ekranie podczas rozgrywki. Na razie jedyną potrzebną rzeczą są komponent fabryki *blockfactory* i skrypt. Później dodamy fabrykę połączeń, komponenty GUI głównego menu oraz mechanikę ładowania rozpoczynającą grę z poziomu menu głównego i sposób wyjścia z powrotem do menu.

1. Utwórz *`board.collection`* w folderze *`main`*. Upewnij się, że jej nazwa to `board`, aby można było się do niej później odwołać. Jeśli dodasz komponent sprite'a tła, ustaw jego pozycję Z na `-1`, bo inaczej nie będzie renderowany za wszystkimi blokami, które utworzymy później.
2. Tymczasowo ustaw <kbd>Main Collection</kbd> (w sekcji <kbd>Bootstrap</kbd>) w *game.project* na `/main/board.collection`, aby łatwo można było testować.

![Kolekcja planszy](images/magic-link/linker_board_collection.png)

![Bootstrap kolekcji planszy](images/magic-link/linker_bootstrap_board.png)

Plik skryptu *board.script* będzie zawierał całą logikę samej planszy oraz bloków na planszy. Zacznij od utworzenia funkcji budującej planszę i wywołaj ją (tymczasowo) z `init()`. Dodajemy też dwie funkcje, których teraz nie będziemy używać, ale później bardzo się przydadzą:

`filter()`
: Ta funkcja pozwoli nam filtrować listy elementów (bloków).

`build_blocklist()`
: Tworzy listę wszystkich bloków na planszy ułożoną jako płaską listę, co pozwala ją łatwo filtrować.

Po zbudowaniu planszy będziemy używać dwóch różnych zbiorów danych zawierających wszystkie bloki: `self.blocks` i `self.board`:

```lua
-- board.script
go.property("timer", 0)     -- Use to time events
local blocksize = 80        -- Distance between block centers
local edge = 40             -- Left and right edge.
local bottom_edge = 50      -- Bottom edge.
local boardwidth = 7        -- Number of columns
local boardheight = 9       -- Number of rows
local centeroff = vmath.vector3(8, -8, 0) -- Center offset for connector gfx since there's shadow below in the block img
local dropamount = 3        -- The number of blocks dropped on a "drop"
local colors = { hash("orange"), hash("pink"), hash("blue"), hash("yellow"), hash("green") }

--
-- filter(function, table)
-- e.g: filter(is_even, {1,2,3,4}) -> {2,4}
--
local function filter(func, tbl)
    local new = {}
    for i, v in pairs(tbl) do
        if func(v) then
            new[i] = v
        end
    end
    return new
end

--
-- Build a list of blocks in 1 dimension for easy filtering
--
local function build_blocklist(self)
    self.blocks = {}
    for x, l in pairs(self.board) do
        for y, b in pairs(self.board[x]) do
            table.insert(self.blocks, { id = b.id, color = b.color, x = b.x, y = b.y })
        end
    end
end

--
-- INIT
--
function init(self)
    self.board = {}             -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.
    self.chain = {}             -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3          -- Number of magic blocks on the board
    self.drops = 1              -- Number of drops you have available
    self.magic_blocks = {}      -- Magic blocks that are lined up
    self.dragging = false       -- Drag touch input
    msg.post(".", "acquire_input_focus")
    msg.post("#", "start_level")
end

local function build_board(self)
    math.randomseed(os.time())
    local pos = vmath.vector3()
    local c
    local x = 0
    local y = 0
    for x = 0,boardwidth-1 do
        pos.x = edge + blocksize / 2 + blocksize * x
        self.board[x] = {}
        for y = 0,boardheight-1 do
            pos.y = bottom_edge + blocksize / 2 + blocksize * y
            -- Calc z
            pos.z = x * -0.1 + y * 0.01 -- <1>
            c = colors[math.random(#colors)]    -- Pick a random color
            local id = factory.create("#blockfactory", pos, null, { color = c })
            self.board[x][y] = { id = id, color = c,  x = x, y = y }
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        build_board(self)
    end
end
```
1. Zwróć uwagę, że ponieważ grafika bloków nachodzi na siebie, musimy rysować je we właściwej kolejności. Robimy to, ustawiając współrzędną z dla każdego bloku. Wartość pozostanie wyraźnie powyżej `-1`, gdzie mamy sprite tła.

Logika planszy tworzy obiekty gry „block” za pomocą komponentu fabryki „blockfactory”. Aby to działało, musimy zbudować obiekt gry block. Ma on skrypt i sprite. Ustawiamy domyślną animację sprite'a na jedną z kolorowych bloków w *`sprites.atlas`*, a następnie dodajemy kod do *`block.script`*, aby blok przyjmował właściwy kolor po utworzeniu:

![Obiekt gry block](images/magic-link/linker_block.png)

```lua
-- block.script
go.property("color", hash("none"))

function init(self)
    go.set_scale(0.18)        -- render scaled down
```

## Oznaczanie połączeń

Teraz potrzebujemy zasobów dla znacznika, który będzie wskazywał, kiedy bloki są połączone przez gracza. Pomysł polega po prostu na nałożeniu grafiki na każdy blok, aby pokazać, że jest połączony.

Musimy utworzyć obiekt gry „connector”, który zawiera obraz sprite'a connector oraz komponent fabryki „connector factory” w obiekcie gry „board”:

![Obiekt gry connector](images/magic-link/linker_connector.png)

![Fabryka connector](images/magic-link/linker_connector_factory.png)

Skrypt dla tego obiektu gry jest minimalny, potrzebuje tylko przeskalować grafikę, aby pasowała do reszty gry, i ustawić poprawnie kolejność Z.

```lua
-- connector.script
function init(self)
    go.set_scale(0.18)              -- Set the scale of this game object.
    go.set(".", "position.z", 1)    -- Put on top.
end
```

Funkcja `same_color_neighbors()` zwraca listę bloków sąsiadujących z danym blokiem (na pozycji x, y) i mających ten sam kolor. Funkcja ta korzysta z funkcji `filter()`, która jest stosowana do pełnej płaskiej listy bloków w `self.blocks`.

```lua
-- board.script
--
-- Returns a list of neighbor blocks of the same color as the
-- block on x, y
--
local function same_color_neighbors(self, x, y)
    local f = function (v)
        return (v.id ~= self.board[x][y].id) and
               (v.x == x or v.x == x - 1 or v.x == x + 1) and
               (v.y == y or v.y == y - 1 or v.y == y + 1) and
               (v.color == self.board[x][y].color)
    end
    return filter(f, self.blocks)
end
```

Funkcja pomocnicza `in_blocklist()` sprawdza, czy blok istnieje na liście bloków:

```lua
-- board.script
--
-- Does the block exist in the list of blocks?
--
local function in_blocklist(blocks, block)
    for i, b in pairs(blocks) do
        if b.id == block then
            return true
        end
    end
    return false
end
```

Używamy tych funkcji podczas obsługi dotyku i przeciągania w `on_input()`, aby budować łańcuch dotkniętych bloków. Na razie testujemy i ignorujemy tu magiczne bloki, choć jeszcze ich nie ma:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    -- If trying to manipulate magic blocks, ignore.
    if self.board[x][y].color == hash("magic") then
        return
    end

    if action.pressed then
        -- List of neighbors of the same color as touched block
        self.neighbors = same_color_neighbors(self, x, y)
        self.chain = {}
        table.insert(self.chain, self.board[x][y])

        -- Mark block.
        p = go.get_position(self.board[x][y].id)
        local id = factory.create("#connectorfactory", p + centeroff)
        table.insert(self.connectors, id)

        self.dragging = true
    elseif self.dragging then
        -- then drag
        if in_blocklist(self.neighbors, self.board[x][y].id) and not in_blocklist(self.chain, self.board[x][y].id) then
            -- dragging over a same-colored neighbor
            table.insert(self.chain, self.board[x][y])
            self.neighbors = same_color_neighbors(self, x, y)

            -- Mark block.
            p = go.get_position(self.board[x][y].id)
            local id = factory.create("#connectorfactory", p + centeroff)
            table.insert(self.connectors, id)
        end
    end
```

Na koniec, po zwolnieniu dotyku, usuwamy wizualnie wszystkie łączniki.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
end
```

![Łączniki w grze](images/magic-link/linker_connector_screen.png)

## Usuwanie połączonych bloków

Mamy już logikę, która pozwala łączyć bloki o tych samych kolorach, więc samo usuwanie połączonych bloków jest proste. Powodem, dla którego ustawiamy pozycję na planszy na `hash("removing")` zamiast po prostu na `nil`, jest to, że później, gdy dodamy logikę magicznych bloków, musimy dopilnować, aby magiczne bloki przesuwały się tylko do nowo usuniętych pól. Jeśli ustawimy tutaj pozycję na `nil`, nie będziemy mieli sposobu odróżnienia nowo usuniętych bloków od bloków usuniętych wcześniej.

```lua
-- board.script
-- Remove the currently selected block-chain
--
local function remove_chain(self)
    -- Delete all chained blocks
    for i, c in ipairs(self.chain) do
        self.board[c.x][c.y] = hash("removing")
        go.delete(c.id)
    end
    self.chain = {}
end
```

Będziemy też potrzebować funkcji, która faktycznie usuwa, czyli ustawia na `nil`, pozycje na planszy oznaczone jako `hash("removing")`:

```lua
-- board.script
--
-- Set removed blocks to nil
--
local function nilremoved(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] == hash("removing") then
                self.board[x][y] = nil
            end
        end
    end
end
```

Tworzymy też funkcję, która przesuwa pozostałe bloki w dół, gdy bloki pod nimi zostaną usunięte (ustawione na `nil`). Iterujemy po planszy kolumna po kolumnie od lewej do prawej i przechodzimy przez każdą kolumnę od dołu do góry. Jeśli napotkamy puste (`nil`) miejsce, przesuwamy wszystkie bloki powyżej tego miejsca w dół.

```lua
-- board.script
--
-- Apply shift-down logic to all blocks.
--
local function slide_board(self)
    -- Slide all remaining blocks down into blank spots.
    -- Going column by column makes this easy.
    local dy = 0
    local pos = vmath.vector3()
    for x = 0,boardwidth - 1 do
        dy = 0
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil then
                if dy > 0 then
                    -- Move down dy steps
                    self.board[x][y - dy] = self.board[x][y]
                    self.board[x][y] = nil
                    -- Calc new position
                    self.board[x][y - dy].y = self.board[x][y - dy].y - dy
                    go.animate(self.board[x][y-dy].id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * (y - dy), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y-dy].id, "position.z", x * -0.1 + (y-dy) * 0.01)
                end
            else
                dy = dy + 1
            end
        end
    end
    -- blocklist needs updating
    build_blocklist(self)
end
```

![Przesuwanie bloków w dół](images/magic-link/linker_blocks_slide.png)

Teraz możemy po prostu dodać wywołania tych funkcji w `on_input()`, gdy dotyk zostanie zwolniony i w `self.chain` znajdują się bloki.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and slide the remaining blocks down.
            remove_chain(self)
            nilremoved(self)
            slide_board(self)
        end

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

## Logika magicznych bloków

Teraz czas dodać do gry magiczne bloki. Najpierw dodajmy możliwość, aby blok mógł stać się magicznym blokiem. Dzięki temu możemy po prostu przejść osobną ścieżką po wypełnionej planszy i zamienić wybrane bloki w magiczne. Żeby nieco urozmaicić magiczne bloki, utwórzmy najpierw animowany efekt magiczny w postaci obiektu gry *`magic_fx.go`*, który będziemy mogli tworzyć z poziomu magicznego bloku.

![Magic_fx.go](images/magic-link/linker_magic_fx.png)

Ten obiekt gry zawiera dwa sprite'y. Jeden to kolor „magic” (sprite używający obrazu *`magic-sphere_layer2.png`*), a drugi to efekt „light” (sprite używający obrazu *`magic-sphere_layer3.png`*). Obiekt obraca się po utworzeniu, zależnie od wartości właściwości `direction`. Sprawiamy też, że obiekt reaguje na dwie wiadomości: `lights_on` i `lights_off`, które sterują sprite'em efektu świetlnego.

Utwórz nowy skrypt i dodaj go jako komponent skryptu do *`magic_fx.go`*:

```lua
-- magic_fx.script
go.property("direction", hash("left"))

function init(self)
    msg.post("#", "lights_off")
    if self.direction == hash("left") then
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, 360,  go.EASING_LINEAR, 3 + math.random())
    else
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, -360,  go.EASING_LINEAR, 2 + math.random())
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("lights_on") then
        msg.post("#light", "enable")
    elseif message_id == hash("lights_off") then
        msg.post("#light", "disable")
    end
end
```

Teraz magiczny blok będzie tworzył dwa obiekty gry `magic_fx` po otrzymaniu wiadomości `make_magic`. Każdy z nich będzie obracał się w przeciwną stronę, tworząc ładny, kolorowy taniec wewnątrz bloków. Dodajemy też dodatkowy sprite do *`block.go`* z obrazem *`magic-sphere_layer4.png`*. Ten obraz jest umieszczony na wyższym Z niż utworzony efekt i rysuje skorupę albo „pokrywę” magicznej kuli.

![Sprite pokrywy](images/magic-link/linker_cover.png)

Zwróć uwagę, że do obiektu gry block musimy dodać komponent *Factory* i ustawić go tak, aby używał naszego obiektu gry *`magic_fx.go`* jako *Prototype*. Skrypt bloku musi też reagować na wiadomości `lights_on` i `lights_off` i przekazywać je do utworzonych obiektów. Zwróć uwagę, że utworzone obiekty trzeba usunąć, gdy blok zostanie usunięty. Zajmuje się tym funkcja `final()` w skrypcie bloku. Wszystko to dzieje się w *`block.script`*.

```lua
-- block.script
function init(self)
    go.set_scale(0.18) -- render scaled down

    self.fx1 = nil
    self.fx2 = nil

    msg.post("#cover", "disable")

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end

function final(self)
    if self.fx1 ~= nil then
        go.delete(self.fx1)
    end

    if self.fx2 ~= nil then
        go.delete(self.fx2)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("make_magic") then
        self.color = hash("magic")
        msg.post("#cover", "enable")
        msg.post("#sprite", "enable")
        sprite.play_flipbook("#sprite", hash("magic-sphere_layer1"))

        self.fx1 = factory.create("#fxfactory", p, nil, { direction = hash("left") })
        self.fx2 = factory.create("#fxfactory", p, nil, { direction = hash("right") })

        go.set_parent(self.fx1, go.get_id())
        go.set_parent(self.fx2, go.get_id())

        go.set(self.fx1, "position.z", 0.01)
        go.set(self.fx1, "scale", 1)
        go.set(self.fx2, "position.z", 0.02)
        go.set(self.fx2, "scale", 1)
    elseif message_id == hash("lights_on") or message_id == hash("lights_off") then
        msg.post(self.fx1, message_id)
        msg.post(self.fx2, message_id)
    end
end
```

Teraz możemy tworzyć magiczne bloki, a także je podświetlać. Użyjemy tego efektu, aby wskazać, że magiczny blok stoi obok innego magicznego bloku.

![Magic block bez światła i ze światłem](images/magic-link/linker_magic_blocks.png)

Kod, który wypełnia planszę blokami, trzeba teraz zmodyfikować tak, aby pojawiały się na niej także magiczne bloki:

```lua
-- board.script
local function build_board(self)

    ...

    -- Distribute magic blocks.
    local rand_x = 0
    local rand_y
    for y = 0, boardheight - 1, boardheight / self.num_magic do
        local set = false
        while not set do
            rand_y = math.random(math.floor(y), math.min(boardheight - 1, math.floor(y + boardheight / self.num_magic)))
            rand_x = math.random(0, boardwidth - 1)
            if self.board[rand_x][rand_y].color ~= hash("magic") then
                msg.post(self.board[rand_x][rand_y].id, "make_magic")
                self.board[rand_x][rand_y].color = hash("magic")
                set = true
            end
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end
```

Główną mechaniką magicznych bloków jest ich zdolność przesuwania się na boki, gdy obok nich znika inny blok. Wszystkie szczegóły tej mechaniki odzwierciedla funkcja `slide_magic_blocks()` w *board.script*. Algorytm jest prosty:

1. Dla każdego wiersza na planszy twórz listę `M` magicznych bloków.
2. Iteruj po każdym magicznym bloku z listy `M`, aż lista przestanie się kurczyć. W każdej iteracji:
    1. Jeśli magiczny blok ma poniżej pozycję bloku `hash("removing")`, po prostu usuń go z listy `M`.
    2. Jeśli magiczny blok ma po boku dziurę oznaczoną `hash("removing")`, przesuń go tam, ustaw jego starą pozycję na `hash("removing")`, a potem usuń go z listy `M`.

```lua
-- board.script
-- Apply the shifting logic to magic blocks. Only slide to positions
-- marked for removal with hash("removing")
--
local function slide_magic_blocks(self)
    -- Slide all magic blocks to the side that should slide first.
    -- This works best going row by row!
    local row_m
    for y = 0,boardheight - 1 do
        row_m = {}
        -- Build list of magic blocks on this row.
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil and self.board[x][y] ~= hash("removing") and self.board[x][y].color == hash("magic") then
                table.insert(row_m, self.board[x][y])
            end
        end

        local mc = #row_m + 1
        -- Go through list, slide and remove if possible. Reiterate until the list does not shrink.
        while #row_m < mc do
            mc = #row_m
            for i, m in pairs(row_m) do
                local x = m.x
                if y > 0 and self.board[x][y-1] == hash("removing") then
                    -- Hole below, do nothing.
                    row_m[i] = nil
                elseif x > 0 and self.board[x-1][y] == hash("removing") then
                    -- Hole to the left! Slide magic block there
                    self.board[x-1][y] = self.board[x][y]
                    self.board[x-1][y].x = x - 1
                    go.animate(self.board[x][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x - 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y].id, "position.z", (x - 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                elseif x < boardwidth - 1 and self.board[x + 1][y] == hash("removing") then
                    -- Hole to the right. Slide magic block there
                    self.board[x+1][y] = self.board[x][y]
                    self.board[x+1][y].x = x + 1
                    go.animate(self.board[x+1][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x + 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x+1][y].id, "position.z", (x + 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                end
            end
        end
    end
end
```

Możemy przetestować tę mechanikę, dodając wywołanie funkcji w `on_input()`:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Teraz wyraźnie widać, dlaczego użyliśmy pośredniego znacznika `hash("removing")` dla pozycji, które usuwamy. Bez niego magiczne bloki przesuwałyby się tam i z powrotem do każdej pustej pozycji po bokach. Może to byłaby interesująca mechanika, ale nie taka, jakiej chcemy w tej małej grze.

Teraz potrzebujemy logiki wykrywającej, czy magiczne bloki są połączone (stoją obok siebie po lewej, prawej, nad albo pod sobą) oraz czy wszystkie magiczne bloki na planszy są ze sobą połączone. Użyty algorytm jest dość prosty:

1. Utwórz listę `M` wszystkich magicznych bloków na planszy.
2. Dla każdego bloku z listy `M`:
    1. Jeśli blok nie ma ustawionego `region`, przypisz mu numer regionu `R` (początkowo `1`).
    2. Oznacz wszystkich nieoznaczonych sąsiadów bloku tym samym numerem regionu `R` i przejdź do ich sąsiadów, sąsiadów sąsiadów i tak dalej.
    3. Zwiększ numer regionu `R` o `1`.

![Oznaczanie regionów](images/magic-link/linker_regions.png)

Oto implementacja tego algorytmu:

```lua
-- board.script
--
-- Build list of all current magic blocks.
--
local function magic_blocks(self)
    local magic = {}
    for x = 0,boardwidth - 1 do
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil and self.board[x][y].color == hash("magic") then
                table.insert(magic, self.board[x][y])
            end
        end
    end
    return magic
end

--
-- Filter out adjacent magic blocks
--
local function adjacent_magic_blocks(blocks, block)
    return filter(function (e)
        return (block.x == e.x and math.abs(block.y - e.y) == 1) or
               (block.y == e.y and math.abs(block.x - e.x) == 1)
    end, blocks)
end

--
-- Spread region to neighbors
--
local function mark_neighbors(blocks, block, region)
    local neighbors = adjacent_magic_blocks(blocks, block)
    for i, m in pairs(neighbors) do
        if m.region == nil then
            m.region = region
            mark_neighbors(blocks, m, region)
        end
    end
end

--
-- Mark all magic block regions
--
local function mark_magic_regions(self)
    local m_blocks = magic_blocks(self)
    -- 1. Clear all region marks and count neighbors
    for i, m in pairs(m_blocks) do
        m.region = nil
        local n = 0
        for _ in pairs(adjacent_magic_blocks(m_blocks, m)) do n = n + 1 end
        m.neighbors = n
    end

    -- 2. Assign regions and spread them
    local region = 1
    for i, m in pairs(m_blocks) do
        if m.region == nil then
            m.region = region
            mark_neighbors(m_blocks, m, region)
            region = region + 1
        end
    end
    return m_blocks
end
```

Tworzymy też funkcje, które pozwalają policzyć liczbę regionów wśród magicznych bloków. Jeśli liczba regionów wynosi 1, wiemy, że wszystkie magiczne bloki są połączone. Dodatkowo dodajemy funkcję, która wyłącza światła we wszystkich magicznych blokach, oraz funkcję, która włącza efekty świetlne w tych magicznych blokach, które mają sąsiednie magiczne bloki:

```lua
-- board.script
--
-- Count the number of connected regions among the magic blocks.
--
local function count_magic_regions(blocks)
    local maxr = 0
    for i, m in pairs(blocks) do
        if m.region > maxr then
            maxr = m.region
        end
    end
    return maxr
end

--
-- Shut off lights on all listed magic blocks
--
local function shutdown_lined_up_magic(self)
    for i, m in ipairs(self.lined_up_magic) do
        msg.post(m.id, "lights_off")
    end
end

--
-- Set highlight for all magic blocks
--
local function highlight_magic(blocks)
    for i, m in pairs(blocks) do
        if m.neighbors > 0 then
            msg.post(m.id, "lights_on")
        else
            msg.post(m.id, "lights_off")
        end
    end
end
```

Teraz możemy włączyć te fragmenty logiki do ogólnego przepływu. Po pierwsze, ponieważ generowanie planszy jest losowe, istnieje niewielka szansa, że zacznie się ona już w stanie wygranej. Jeśli tak się stanie, po prostu odrzucamy planszę i budujemy ją ponownie:

```lua
-- board.script
--
-- Clear the board
--
local function clear_board(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil then
                go.delete(self.board[x][y].id)
                self.board[x][y] = nil
            end
        end
    end
end

local function build_board(self)

    ...

    -- Build 1d list that we can easily filter.
    build_blocklist(self)

    local magic_blocks = mark_magic_regions(self)
    if count_magic_regions(magic_blocks) == 1 then
        -- "Win" from start. Make new board.
        clear_board(self)
        build_board(self)
    end
    highlight_magic(magic_blocks)
end
```

Reszta logiki mieści się w `on_input()`. Nadal nie ma kodu obsługującego wiadomość `level_completed`, ale na razie to nie problem:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and refill board.
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)

            local magic_blocks = mark_magic_regions(self)
            -- Highlight adjacent magic blocks.
            if count_magic_regions(magic_blocks) == 1 then
                -- Win!
                msg.post("#", "level_completed")
            end
            highlight_magic(magic_blocks)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Teraz można już zagrać i osiągnąć stan zwycięstwa, mimo że na razie nic się nie dzieje, gdy połączysz wszystkie magiczne bloki.

![Pierwsze zwycięstwo](images/magic-link/linker_first_win.png)

## Zrzuty

Pomysł z „dropem” polega na dodaniu prostej mechaniki postępu. Gracz może wykonać ograniczoną liczbę „dropów”, które po prostu zrzucają kilka nowych losowych elementów na planszę po naciśnięciu przycisku <kbd>DROP</kbd>. Gracz zaczyna z jednym dropem, a za każdym razem, gdy poziom zostanie ukończony, otrzymuje dodatkowy drop. Kod mechaniki dropów mieści się w dwóch funkcjach. Jedna zwraca listę możliwych miejsc, w których mogą wylądować dropy, a druga wykonuje sam drop wraz z animacją i całym resztą.

```lua
-- board.script
--
-- Find spots for a drop.
--
local function dropspots(self)
    local spots = {}
    for x = 0, boardwidth - 1 do
        for y = 0, boardheight - 1 do
            if self.board[x][y] == nil then
                table.insert(spots, { x = x, y = y })
                break
            end
        end
    end
    -- If more than dropamount, randomly remove a slot until dropamount
    for c = 1, #spots - dropamount do
        table.remove(spots, math.random(#spots))
    end
    return spots
end

--
-- Perform the drop
--
local function drop(self, spots)
    for i, s in pairs(spots) do
        local pos = vmath.vector3()
        pos.x = edge + blocksize / 2 + blocksize * s.x
        pos.y = 1000
        c = colors[math.random(#colors)]    -- Pick a random color
        local id = factory.create("#blockfactory", pos, null, { color = c })
        go.animate(id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * s.y, go.EASING_OUTBOUNCE, 0.5)
        -- Calc new z
        go.set(id, "position.z", s.x * -0.1 + s.y * 0.01)

        self.board[s.x][s.y] = { id = id, color = c,  x = s.x, y = s.y }
    end

    -- Rebuild blocklist
    build_blocklist(self)
end
```

Możemy przetestować dropy, uruchamiając na przykład następujący kod w `on_reload()` albo podpinając go tymczasowo pod akcję wejścia:

```lua
s = dropspots(self)
if #s > 0 then
    -- Do the drop
    drop(self, s)
end
```

![Drop](images/magic-link/linker_drop.png)

## Główne menu

Teraz czas złożyć wszystko w całość. Najpierw utwórzmy ekran startowy i oddzielmy go od planszy. Krok 1 to utworzenie *main_menu.gui* i skonfigurowanie go z przyciskiem <kbd>Start</kbd> (węzeł tekstowy i węzeł prostokątny z teksturą), węzłem tekstowym tytułu oraz kilkoma dekoracyjnymi blokami (węzłami prostokątnymi z teksturą). Skrypt *main_menu.gui_script*, który dołączamy do GUI, animuje dekoracyjne bloki w `init()`. Zawiera też `on_input()`, które wysyła wiadomość `start_game` do głównego skryptu. Za chwilę stworzymy ten skrypt.

![GUI głównego menu](images/magic-link/linker_main_menu.png)

```lua
-- main_menu.gui_script
function init(self)
    msg.post(".", "acquire_input_focus")

    local bs = { "brick1", "brick2", "brick3", "brick4", "brick5", "brick6" }
    for i, b in ipairs(bs) do
        local n = gui.get_node(b)
        local rt = (math.random() * 3) + 1
        local a = math.random(-45, 45)
        gui.set_color(n, vmath.vector4(1, 1, 1, 0))

        gui.animate(n, "position.y", -100 - math.random(0, 50), gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "color.w", 1, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "rotation.z", a, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
    end

    gui.animate(gui.get_node("start"), "color.x", 1, gui.EASING_INOUTSINE, 1, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local start = gui.get_node("start")

        if gui.pick_node(start, action.x, action.y) then
            msg.post("/main#script", "start_game")
        end
    end
end
```

Ponieważ uruchamianiem gry ma się wkrótce zająć skrypt głównego menu, usuń tymczasowe wywołanie konfigurujące planszę z `init()` w *board.script*:

```lua
-- board.script
--
-- INIT
--
function init(self)
    self.board = {}                -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.

    self.chain = {}                -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3          -- Number of magic blocks on the board

    self.drops = 1              -- Number of drops you have available

    self.magic_blocks = {}        -- Magic blocks that are lined up

    self.dragging = false       -- Drag touch input
end
```

Główny skrypt będzie przechowywał ogólny stan gry i uruchamiał grę na żądanie. Chcemy tu sprawić, aby *main.collection* zawierała tylko minimalną liczbę zasobów potrzebnych do wyświetlenia ekranu startowego. Robimy to, umieszczając w *main.collection* obiekt gry „main”, który zawiera GUI głównego menu, komponent skryptu oraz, co najważniejsze, komponent pełnomocnika kolekcji (<kbd>Collection Proxy</kbd>).

Pełnomocnik kolekcji pozwala dynamicznie ładować i odłączać kolekcje w uruchomionej grze. Działa on w imieniu wskazanego pliku kolekcji, a dynamiczną kolekcję ładujemy, inicjalizujemy, włączamy, wyłączamy i odłączamy, wysyłając wiadomości do proxy. Pełny opis użycia znajdziesz w [dokumentacji Collection Proxy](/manuals/collection-proxy).

W naszym przypadku ustawiamy właściwość <kbd>Collection</kbd> komponentu <kbd>Collection Proxy</kbd> na *board.collection*, która zawiera „level”.

![Główna kolekcja](images/magic-link/linker_main_collection.png)

Powinniśmy teraz otworzyć *game.project* i zmienić bootstrap *main_collection* na `/main/main.collectionc`.

![Bootstrap głównej kolekcji](images/magic-link/linker_bootstrap_main.png)

Od tej pory uruchomienie gry oznacza wysłanie wiadomości do naszego <kbd>Collection Proxy</kbd>, aby załadował, zainicjalizował i włączył planszę, a następnie wyłączył główne menu, żeby nie było widoczne. Powrót do głównego menu działa odwrotnie, o ile proxy załadował już kolekcję.

```lua
-- main.script
function init(self)
    msg.post("#", "to_main_menu")
    self.state = "MAIN_MENU"
end

function on_message(self, message_id, message, sender)
    if message_id == hash("to_main_menu") then
        if self.state ~= "MAIN_MENU" then
            msg.post("#boardproxy", "unload")
        end
        msg.post("main:/main#menu", "enable") -- <1>
        self.state = "MAIN_MENU"
    elseif message_id == hash("start_game") then
        msg.post("#boardproxy", "load")
        msg.post("#menu", "disable")
    elseif message_id == hash("proxy_loaded") then
        -- Board collection has loaded...
        msg.post(sender, "init")
        msg.post("board:/board#script", "start_level", { difficulty = 1 }) -- <2>
        msg.post(sender, "enable")
        self.state = "GAME_RUNNING"
    end
end
```
1. Zwróć uwagę, że używamy gniazda o nazwie `main`, więc musimy upewnić się, że taka nazwa została ustawiona w *main.collection*. Zaznacz węzeł główny i sprawdź, czy właściwość *Name* ma wartość `main`.
2. Podobnie wysyłamy wiadomości do załadowanej kolekcji przez jej gniazdo, którego nazwę ustala właściwość *Name* w kolekcji.

## GUI w grze

Zanim dodamy ostatni fragment logiki do skryptu planszy, powinniśmy dodać zestaw elementów GUI do planszy. Najpierw, nad planszą, dodajemy przycisk <kbd>RESTART</kbd> i przycisk <kbd>DROP</kbd>.

![GUI planszy](images/magic-link/linker_board_gui.png)

Skrypt GUI planszy wysyła wiadomości do elementu dialogu restartu po kliknięciu oraz do samego skryptu planszy po kliknięciu <kbd>DROP</kbd>:

```lua
-- board.gui_script
function init(self)
    msg.post("#", "show")
    msg.post("/restart#gui", "hide")
    msg.post("/level_complete#gui", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
    elseif message_id == hash("set_drop_counter") then
        local n = gui.get_node("drop_counter")
        gui.set_text(n, message.drops .. " x")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local restart = gui.get_node("restart")
        local drop = gui.get_node("drop")

        if gui.pick_node(restart, action.x, action.y) then
            -- Show the restart dialog box.
            msg.post("/restart#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(drop, action.x, action.y) then
            msg.post("/board#script", "drop")
```

Dialog <kbd>RESTART</kbd> jest prosty. Budujemy go jako *restart.gui* i dołączamy prosty skrypt, który nie robi nic, jeśli gracz kliknie <kbd>NO</kbd>, wysyła wiadomość `restart_level` do skryptu planszy, jeśli gracz kliknie <kbd>YES</kbd>, oraz wiadomość `to_main_menu` do skryptu głównego, jeśli gracz kliknie <kbd>Quit to main menu</kbd>:

![GUI restartu](images/magic-link/linker_restart_gui.png)

```lua
-- restart.gui_script
function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local yes = gui.get_node("yes")
        local no = gui.get_node("no")
        local quit = gui.get_node("quit")

        if gui.pick_node(no, action.x, action.y) then
            msg.post("#", "hide")
            msg.post("/board#gui", "show")
        elseif gui.pick_node(yes, action.x, action.y) then
            msg.post("board:/board#script", "restart_level")
            msg.post("/board#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(quit, action.x, action.y) then
            msg.post("main:/main#script", "to_main_menu")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Tworzymy też prosty dialog GUI informujący o ukończeniu poziomu w *level_complete.gui* z prostym skryptem, który wysyła wiadomość `next_level` do skryptu planszy, gdy gracz kliknie <kbd>CONTINUE</kbd>:

![Dialog ukończenia poziomu](images/magic-link/linker_level_complete_gui.png)

```lua
-- level_complete.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local continue = gui.get_node("continue")

        if gui.pick_node(continue, action.x, action.y) then
            msg.post("board#script", "next_level")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Dialog używany do prezentacji bieżącego poziomu, ze skryptem, który tylko ukrywa i pokazuje dialog. Po pokazaniu wiadomość dialogu jest ustawiana na wiadomość zawierającą aktualny poziom trudności:

![GUI prezentacji poziomu](images/magic-link/linker_present_level_gui.png)

```lua
-- present_level.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        local n = gui.get_node("message")
        gui.set_text(n, "Level " .. message.level)
        msg.post("#", "enable")
    end
end
```

Dodajemy też dialog, który pojawia się, jeśli gracz próbuje wykonać drop, ale nie ma już na niego miejsca.

![GUI braku miejsca na drop](images/magic-link/linker_no_drop_room_gui.png)

```lua
-- no_drop_room.gui_script
function init(self)
    msg.post("#", "hide")
    self.t = 0
end

function update(self, dt)
    if self.t < 0 then
        msg.post("#", "hide")
    else
        self.t = self.t - dt
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        self.t = 1
        msg.post("#", "enable")
    end
end
```

Na koniec dodajemy te komponenty GUI do *board.collection* i dopisujemy potrzebny kod do *board.script*:

![Finalna kolekcja planszy](images/magic-link/linker_board_collection_final.png)

Potrzebujemy kodu dla wszystkich wiadomości wysyłanych do i z planszy w `on_message()`.

`start_level`
: Ustaw liczbę magicznych bloków zgodnie z parametrem trudności, zbuduj planszę, a następnie pokaż dialog GUI `present_level` na 2 sekundy przed rozpoczęciem gry, po czym usuń dialog i przechwyć wejście. Zwróć uwagę, że używamy `go.animate()` jako timera, animując wartość `timer`, która nie jest używana do niczego innego.

`restart_level`
: To dzieje się, gdy gracz naciska i potwierdza przycisk GUI <kbd>RESTART</kbd>. Wyczyść i przebuduj planszę oraz zresetuj licznik dropów.

`level_completed`
: Wysyłana natychmiast po wejściu planszy w stan zwycięstwa. Wyłącz wejście, animuj magiczne bloki i pokaż dialog GUI `level_complete`. Dialog odeśle wiadomość `next_level`, gdy gracz kliknie przycisk <kbd>CONTINUE</kbd>.

`next_level`
: Gdy ta wiadomość zostanie odebrana, wyczyść planszę, zwiększ licznik dropów i wyślij `start_level` z ustawionym kolejnym poziomem trudności.

`drop`
: Sprawdź, gdzie można wykonać drop. Jeśli nie ma żadnych możliwych miejsc, pokaż dialog GUI `no_drop_room`, w przeciwnym razie wykonaj drop, jeśli gracz ma jeszcze dostępne dropy, zmniejsz licznik dropów i zaktualizuj wizualną reprezentację licznika.

```lua
-- board.script
function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        self.num_magic = message.difficulty + 1
        build_board(self)

        msg.post("#gui", "set_drop_counter", { drops = self.drops } )

        msg.post("present_level#gui", "show", { level = message.difficulty } )
        -- Wait some...
        go.animate("#", "timer", go.PLAYBACK_ONCE_FORWARD, 1, go.EASING_LINEAR, 2, 0, function ()
            msg.post("present_level#gui", "hide")
            msg.post(".", "acquire_input_focus")
        end)
    elseif message_id == hash("restart_level") then
        clear_board(self)
        build_board(self)
        self.drops = 1
        msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        msg.post(".", "acquire_input_focus")
    elseif message_id == hash("level_completed") then
        -- turn off input
        msg.post(".", "release_input_focus")

        -- Animate the magic!
        for i, m in ipairs(magic_blocks(self)) do
            go.set_scale(0.17, m.id)
            go.animate(m.id, "scale", go.PLAYBACK_LOOP_PINGPONG, 0.19, go.EASING_INSINE, 0.5, 0)
        end

        -- Show completion screen
        msg.post("level_complete#gui", "show")
    elseif message_id == hash("next_level") then
        clear_board(self)
        self.drops = self.drops + 1
        -- Difficulty level is number of magic blocks - 1
        msg.post("#", "start_level", { difficulty = self.num_magic })
    elseif message_id == hash("drop") then
        s = dropspots(self)
        if #s == 0 then
            -- Can't perform drop
            msg.post("no_drop_room#gui", "show")
        elseif self.drops > 0 then
            -- Do the drop
            drop(self, s)
            self.drops = self.drops - 1
            msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        end
    end
end
```
