---
title: Zdarzenia kolizji w Defold
brief: Obsługę zdarzeń kolizji można scentralizować za pomocą `physics.set_event_listener()`, aby kierować wszystkie wiadomości o kolizjach i interakcjach do jednej wskazanej funkcji.
---

# Obsługa zdarzeń fizyki w silniku Defold

Wcześniej interakcje fizyczne w silniku Defold obsługiwano przez rozgłaszanie wiadomości do wszystkich komponentów obiektów, które się zderzały. Począwszy od wersji 1.6.4 Defold oferuje bardziej scentralizowane podejście za pośrednictwem funkcji `physics.set_event_listener()`. Funkcja ta pozwala ustawić własny słuchacz, który obsłuży wszystkie zdarzenia interakcji fizycznych w jednym miejscu, co upraszcza kod i poprawia wydajność.

## Ustawianie słuchacza świata fizycznego

W Defold każdy collection proxy (pełnomocnik kolekcji) tworzy własny, oddzielny świat fizyczny. Dlatego podczas pracy z wieloma collection proxy trzeba zarządzać osobnymi światami fizycznymi powiązanymi z każdym z nich. Aby zdarzenia fizyki były obsługiwane poprawnie w każdym świecie, musisz ustawić słuchacza świata fizycznego osobno dla świata każdego collection proxy.

Taka konfiguracja oznacza, że słuchacz zdarzeń fizyki musi zostać ustawiony z poziomu tej kolekcji, którą reprezentuje proxy. W ten sposób wiążesz słuchacz bezpośrednio z odpowiednim światem fizycznym, dzięki czemu może on precyzyjnie przetwarzać zdarzenia fizyki.

Oto przykład ustawienia słuchacza świata fizycznego w collection proxy:

```lua
function init(self)
    -- Assuming this script is attached to a game object within the collection loaded by the proxy
    -- Set the physics world listener for the physics world of this collection proxy
    physics.set_event_listener(physics_world_listener)
end
```

Dzięki takiemu podejściu zapewniasz, że każdy świat fizyczny utworzony przez collection proxy ma własny, dedykowany słuchacz. Ma to kluczowe znaczenie dla skutecznej obsługi zdarzeń fizyki w projektach korzystających z wielu collection proxy.

::: important
Jeśli słuchacz zostanie ustawiony, [wiadomości fizyki](/manuals/physics-messages) nie będą już wysyłane dla świata fizycznego, w którym ten słuchacz jest aktywny.
:::

## Struktura danych zdarzeń

Każde zdarzenie fizyki udostępnia tabelę `data` zawierającą konkretne informacje istotne dla danego zdarzenia.

1. **Zdarzenie punktu kontaktu (`contact_point_event`):**
To zdarzenie raportuje punkt kontaktu między dwoma obiektami kolizji. Jest przydatne przy szczegółowej obsłudze kolizji, na przykład do obliczania sił uderzenia albo własnych reakcji na kolizję.

   - `applied_impulse`: Impuls wynikający z kontaktu.
   - `distance`: Odległość penetracji między obiektami.
   - `a` i `b`: Obiekty reprezentujące zderzające się encje, z których każdy zawiera:
     - `position`: Pozycja punktu kontaktu w przestrzeni świata (vector3).
     - `instance_position`: Pozycja instancji obiektu gry w przestrzeni świata (vector3).
     - `id`: Identyfikator instancji (hash).
     - `group`: Grupa kolizyjna (hash).
     - `relative_velocity`: Prędkość względna względem drugiego obiektu (vector3).
     - `mass`: Masa w kilogramach (number).
     - `normal`: Normalna kontaktu wskazująca od drugiego obiektu (vector3).

2. **Zdarzenie kolizji (`collision_event`):**
To zdarzenie wskazuje, że doszło do kolizji między dwoma obiektami. Jest bardziej ogólne niż zdarzenie punktu kontaktu i nadaje się do wykrywania kolizji bez potrzeby uzyskiwania szczegółowych informacji o punktach kontaktu.

   - `a` i `b`: Obiekty reprezentujące zderzające się encje, z których każdy zawiera:
     - `position`: Pozycja w przestrzeni świata (vector3).
     - `id`: Identyfikator instancji (hash).
     - `group`: Grupa kolizyjna (hash).

3. **Zdarzenie wyzwalacza (`trigger_event`):**
To zdarzenie jest wysyłane, gdy obiekt wchodzi w interakcję z obiektem typu trigger. Przydaje się do tworzenia w grze obszarów, które wywołują określone działanie, gdy obiekt wchodzi do środka lub z nich wychodzi.

   - `enter`: Wskazuje, czy interakcja była wejściem (true), czy wyjściem (false).
   - `a` i `b`: Obiekty biorące udział w zdarzeniu wyzwalacza, z których każdy zawiera:
     - `id`: Identyfikator instancji (hash).
     - `group`: Grupa kolizyjna (hash).

4. **Odpowiedź rzutowania promienia (`ray_cast_response`):**
To zdarzenie jest wysyłane w odpowiedzi na rzut promienia i zawiera informacje o obiekcie trafionym przez promień.

   - `group`: Grupa kolizyjna trafionego obiektu (hash).
   - `request_id`: Identyfikator żądania rzutowania promienia (number).
   - `position`: Pozycja trafienia (vector3).
   - `fraction`: Ułamek długości promienia, w którym nastąpiło trafienie (number).
   - `normal`: Normalna w punkcie trafienia (vector3).
   - `id`: Identyfikator instancji trafionego obiektu (hash).

5. **Nietrafiony rzut promienia (`ray_cast_missed`):**
To zdarzenie jest wysyłane, gdy rzut promienia nie trafi w żaden obiekt.

   - `request_id`: Identyfikator żądania rzutowania promienia, które nie trafiło (number).

## Przykład użycia

```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            -- Handle detailed contact point data
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- Handle general collision data
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- Handle trigger interaction data
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- Handle raycast hit data
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- Handle raycast miss data
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## Ograniczenia

Słuchacz wywołuje się synchronicznie w momencie, w którym wystąpi zdarzenie. Dzieje się to w środku kroku czasowego, co oznacza, że świat fizyki jest zablokowany. W praktyce uniemożliwia to użycie funkcji, które mogą wpływać na symulację świata fizyki, na przykład `physics.create_joint()`.

Oto prosty przykład, jak obejść te ograniczenia:
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- fill the message in the same way arguments should be passed to `physics.create_joint()`
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- send message to the object itself
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- unpack message with function arguments
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```
