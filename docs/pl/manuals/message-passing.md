---
title: Przekazywanie wiadomości w Defold
brief: Przekazywanie wiadomości to mechanizm używany przez Defold do umożliwiania komunikacji luźno powiązanych obiektów. Ten podręcznik szczegółowo opisuje ten mechanizm.
---

# Przekazywanie wiadomości

Przekazywanie wiadomości to mechanizm, dzięki któremu obiekty gry w Defold mogą komunikować się ze sobą. Ten podręcznik zakłada, że znasz podstawy [mechanizmu adresowania](/manuals/addressing) i [podstawowych elementów budujących grę](/manuals/building-blocks).

Defold nie realizuje programowania obiektowego w tym sensie, że definiujesz aplikację przez budowanie hierarchii klas z dziedziczeniem i metodami składowymi w obiektach, jak w Javie, C++ czy C#. Zamiast tego Defold rozszerza Luę o prosty i skuteczny model zorientowany obiektowo, w którym stan obiektu jest przechowywany wewnętrznie w komponentach skryptowych i dostępny przez referencję `self`. Obiekty można też całkowicie odseparować, a do komunikacji między nimi używać asynchronicznego przekazywania wiadomości.

## Przykłady użycia

Najpierw przyjrzyjmy się kilku prostym przykładom użycia. Załóżmy, że tworzysz grę składającą się z:

1. Głównej kolekcji bootstrapowej zawierającej obiekt gry z komponentem GUI. GUI składa się z minimapy i licznika punktów. Znajduje się tam również kolekcja o identyfikatorze `"level"`.
2. Kolekcji o nazwie `"level"`, która zawiera dwa obiekty gry: bohatera i przeciwnika.

![Message passing structure](images/message_passing/message_passing_structure.png)

::: sidenote
Treść tego przykładu znajduje się w dwóch oddzielnych plikach. Jeden plik odpowiada głównej kolekcji bootstrapowej, a drugi kolekcji o identyfikatorze "level". W Defold nazwy plików _nie mają znaczenia_. Liczy się tożsamość, jaką nadajesz instancjom.
:::

W grze występuje kilka prostych mechanik wymagających komunikacji między obiektami:

![Message passing](images/message_passing/message_passing.png)

① Bohater uderza przeciwnika
: W ramach tej mechaniki wiadomość `"punch"` jest wysyłana ze skryptu bohatera do skryptu przeciwnika. Ponieważ oba obiekty znajdują się w tej samej gałęzi hierarchii kolekcji, preferowane jest adresowanie względne:

  ```lua
  -- Wysyłaj "punch" ze skryptu "hero" do skryptu "enemy"
  msg.post("enemy#controller", "punch")
  ```

  W grze jest tylko jeden wariant mocnego ciosu, więc wiadomość nie musi zawierać żadnych dodatkowych informacji poza nazwą "punch".

  W komponencie skryptowym przeciwnika tworzysz funkcję odbierającą wiadomość:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  W tym przypadku kod sprawdza tylko nazwę wiadomości, przekazywaną jako hashowany ciąg w parametrze `message_id`. Nie interesują go dane wiadomości ani nadawca - *każdy*, kto wyśle wiadomość "punch", zada obrażenia biednemu przeciwnikowi.

② Bohater zdobywa punkty
: Gdy gracz pokonuje przeciwnika, jego wynik wzrasta. Wiadomość `"update_score"` jest również wysyłana ze skryptu obiektu gry "hero" do komponentu GUI w obiekcie gry "interface".

  ```lua
  -- Przeciwnik pokonany. Zwiększ licznik punktów o 100.
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  W tym przypadku nie da się zapisać adresu względnego, ponieważ "interface" znajduje się w korzeniu hierarchii nazw, a "hero" nie. Wiadomość trafia do komponentu GUI z dołączonym skryptem, dzięki czemu może on odpowiednio zareagować. Wiadomości można swobodnie wysyłać między skryptami, skryptami GUI i skryptami do renderowania.

  Wiadomość `"update_score"` jest powiązana z danymi o wyniku. Dane przekazywane są jako tabela Lua w parametrze `message`:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- Ustaw licznik punktów na nowy wynik
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    end
  end
  ```

③ Pozycja przeciwnika na minimapie
: Gracz ma na ekranie minimapę, która pomaga lokalizować i śledzić przeciwników. Każdy przeciwnik odpowiada za sygnalizowanie swojej pozycji przez wysyłanie wiadomości `update_minimap` do komponentu GUI w obiekcie gry "interface":

  ```lua
  -- Wyślij bieżącą pozycję, aby zaktualizować minimapę interfejsu
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  Kod skryptu GUI musi śledzić pozycje każdego przeciwnika, a jeśli ten sam przeciwnik wyśle nową pozycję, poprzednia powinna zostać zastąpiona. Nadawca wiadomości, przekazany w parametrze `sender`, może służyć jako klucz tabeli Lua przechowującej pozycje:

  ```lua
  function init(self)
    self.minimap_positions = {}
  end

  local function update_minimap(self)
    for url, pos in pairs(self.minimap_positions) do
      -- Zaktualizuj pozycję na mapie
      ...
    end
  end

  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- Ustaw licznik punktów na nowy wynik
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    elseif message_id == hash("update_minimap") then
      -- Zaktualizuj minimapę o nowe pozycje
      self.minimap_positions[sender] = message.position
      update_minimap(self)
    end
  end
  ```

## Wysyłanie wiadomości

Mechanizm wysyłania wiadomości jest, jak już widzieliśmy, bardzo prosty. Wywołujesz funkcję `msg.post()`, która umieszcza wiadomość w kolejce wiadomości. Następnie silnik w każdej klatce przechodzi przez kolejkę i dostarcza każdą wiadomość do jej docelowego adresu. W przypadku niektórych wiadomości systemowych, takich jak `"enable"`, `"disable"` czy `"set_parent"`, wiadomość obsługuje kod silnika. Silnik generuje też własne wiadomości systemowe, takie jak `"collision_response"` przy kolizjach fizycznych, które są dostarczane do twoich obiektów. W przypadku wiadomości użytkownika wysyłanych do komponentów skryptowych silnik po prostu wywołuje specjalną funkcję Lua o nazwie `on_message()`.

Możesz wysyłać dowolne wiadomości do dowolnego istniejącego obiektu lub komponentu, a to kod po stronie odbiorcy decyduje, jak na nie zareagować. Jeśli wyślesz wiadomość do komponentu skryptowego, który ją zignoruje, nic się nie stanie. Odpowiedzialność za obsługę wiadomości spoczywa całkowicie na odbiorcy.

Silnik sprawdza adres docelowy wiadomości. Jeśli spróbujesz wysłać wiadomość do nieznanego odbiorcy, Defold zgłosi błąd w konsoli:

```lua
-- Try to post to a non existing object
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

Pełna sygnatura wywołania `msg.post()` to:

`msg.post(receiver, message_id, [message])`

receiver
: Identyfikator docelowego komponentu lub obiektu gry. Zwróć uwagę, że gdy adresatem jest obiekt gry, wiadomość zostanie rozesłana do wszystkich komponentów w tym obiekcie.

message_id
: Ciąg znaków lub hashowany ciąg z nazwą wiadomości.

[message]
: Opcjonalna tabela Lua zawierająca pary klucz-wartość z danymi wiadomości. W tabeli można umieścić niemal każdy typ danych. Możesz przekazać liczby, ciągi znaków, wartości logiczne, URL-e, hashe i zagnieżdżone tabele. Nie możesz przekazać funkcji.

  ```lua
  -- Send table data containing a nested table
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
Istnieje twardy limit rozmiaru tabeli przekazywanej w parametrze `message`. Limit ten wynosi 2 kilobajty. Obecnie nie ma prostego sposobu, aby ustalić dokładny rozmiar pamięci zajmowany przez tabelę, ale możesz użyć `collectgarbage("count")` przed i po wstawieniu tabeli, aby monitorować zużycie pamięci.
:::

### Skróty

Defold udostępnia dwa wygodne skróty, których możesz użyć do wysyłania wiadomości bez podawania pełnego URL-a:

:[Skróty](../shared/url-shorthands.md)

## Odbieranie wiadomości

Odbieranie wiadomości sprowadza się do upewnienia się, że docelowy komponent skryptowy zawiera funkcję o nazwie `on_message()`. Funkcja przyjmuje cztery parametry:

`function on_message(self, message_id, message, sender)`

`self`
: Referencja do samego komponentu skryptowego.

`message_id`
: Zawiera nazwę wiadomości. Nazwa jest _hashowana_.

`message`
: Zawiera dane wiadomości. To tabela Lua. Jeśli nie ma danych, tabela jest pusta.

`sender`
: Zawiera pełny URL nadawcy.

```lua
function on_message(self, message_id, message, sender)
    print(message_id) --> hash: [my_message_name]

    pprint(message) --> {
                    -->   score = 100,
                    -->   value = "some string"
                    --> }

    print(sender) --> url: [main:/my_object#script]
end
```

## Wiadomości między światami gry

Jeśli używasz komponentu pełnomocnika kolekcji, aby załadować nowy świat gry do runtime, będziesz chciał wymieniać wiadomości między światami gry. Załóżmy, że załadowałeś kolekcję przez pełnomocnika, a właściwość *Name* tej kolekcji ma wartość "level":

![Collection name](images/message_passing/collection_name.png)

Gdy tylko kolekcja zostanie załadowana, zainicjalizowana i włączona, możesz wysyłać wiadomości do dowolnego komponentu lub obiektu w nowym świecie gry, podając nazwę świata gry w polu socket adresata:

```lua
-- Wyślij wiadomość do gracza w nowym świecie gry
msg.post("level:/player#controller", "wake_up")
```
Bardziej szczegółowy opis działania pełnomocników kolekcji znajdziesz w dokumentacji [Collection Proxies](/manuals/collection-proxy).

## Łańcuchy wiadomości

Gdy wysłana wiadomość zostanie ostatecznie dostarczona, wywoływana jest funkcja `on_message()` odbiorcy. Dość często kod reakcji wysyła kolejne wiadomości, które trafiają do kolejki wiadomości.

Gdy silnik zaczyna rozsyłanie wiadomości, przechodzi przez kolejkę i wywołuje funkcję `on_message()` każdego odbiorcy, aż kolejka zostanie opróżniona. Jeśli podczas tego przebiegu do kolejki zostaną dodane nowe wiadomości, silnik wykona kolejny przebieg. Istnieje jednak twardy limit tego, ile razy silnik próbuje opróżnić kolejkę, co w praktyce ogranicza długość łańcuchów wiadomości, które można oczekiwać, że zostaną w pełni rozesłane w ramach jednej klatki. Możesz łatwo sprawdzić, ile przebiegów rozsyłania wykonuje silnik między kolejnymi wywołaniami `update()`, używając poniższego skryptu:

```lua
function init(self)
    -- Zaczynamy długi łańcuch wiadomości podczas inicjalizacji obiektu
    -- i utrzymujemy go przez kilka kroków update().
    print("INIT")
    msg.post("#", "msg")
    self.updates = 0
    self.count = 0
end

function update(self, dt)
    if self.updates < 5 then
        self.updates = self.updates + 1
        print("UPDATE " .. self.updates)
        print(self.count .. " dispatch passes before this update.")
        self.count = 0
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("msg") then
        self.count = self.count + 1
        msg.post("#", "msg")
    end
end
```

Uruchomienie tego skryptu wypisze coś w rodzaju:

```txt
DEBUG:SCRIPT: INIT
INFO:ENGINE: Defold Engine 1.2.36 (5b5af21)
DEBUG:SCRIPT: UPDATE 1
DEBUG:SCRIPT: 10 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 2
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 3
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 4
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 5
DEBUG:SCRIPT: 75 dispatch passes before this update.
```

Widzimy, że ta konkretna wersja silnika Defold wykonuje 10 przebiegów rozsyłania wiadomości między `init()` a pierwszym wywołaniem `update()`. Następnie wykonuje 75 przebiegów podczas każdej kolejnej pętli aktualizacji.
