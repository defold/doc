---
title: Komunikaty kolizji w Defold
brief: Gdy dwa obiekty się zderzają, silnik wywołuje funkcję zwrotną zdarzeń albo rozsyła komunikaty do obu obiektów.
---

# Komunikaty kolizji

Gdy dwa obiekty się zderzają, silnik wyśle zdarzenie do funkcji zwrotnej zdarzeń albo rozgłosi komunikaty do obu obiektów.

## Filtrowanie zdarzeń

Typy generowanych zdarzeń można kontrolować za pomocą przełączników dla każdego obiektu:

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

Wszystkie są domyślnie ustawione na `true`.
Gdy dwa obiekty kolizji wchodzą w interakcję, sprawdzamy, czy na podstawie tych pól wyboru należy wysłać wiadomość do użytkownika.

Na przykład dla pola "Generate Contact Events":

Gdy używasz `physics.set_event_listener()`:

| Komponent A | Komponent B | Wyślij wiadomość |
|-------------|-------------|------------------|
| ✅︎          | ✅︎          | Tak              |
| ❌          | ✅︎          | Tak              |
| ✅︎          | ❌          | Tak              |
| ❌          | ❌          | Nie              |

Gdy używasz domyślnego handlera wiadomości:

| Komponent A | Komponent B | Wyślij wiadomości |
|-------------|-------------|-------------------|
| ✅︎          | ✅︎          | Tak (A,B) + (B,A) |
| ❌          | ✅︎          | Tak (B,A)         |
| ✅︎          | ❌          | Tak (A,B)         |
| ❌          | ❌          | Nie               |

## Odpowiedź na kolizję

Wiadomość `"collision_response"` jest wysyłana, gdy jeden z obiektów biorących udział w zderzeniu ma typ "dynamic", "kinematic" lub "static". Zawiera następujące pola:

`other_id`
: identyfikator instancji, z którą obiekt kolizji się zderzył (`hash`)

`other_position`
: pozycja w przestrzeni świata instancji, z którą obiekt kolizji się zderzył (`vector3`)

`other_group`
: grupa kolizyjna drugiego obiektu kolizji (`hash`)

`own_group`
: grupa kolizyjna obiektu kolizji (`hash`)

Wiadomość collision_response wystarcza do obsługi kolizji, jeśli nie potrzebujesz żadnych szczegółów dotyczących rzeczywistego przecięcia obiektów, na przykład gdy chcesz wykryć, czy pocisk trafił wroga. Dla każdej pary obiektów, które się zderzają, w jednej klatce wysyłana jest tylko jedna taka wiadomość.

```Lua
function on_message(self, message_id, message, sender)
    -- sprawdź wiadomość
    if message_id == hash("collision_response") then
        -- wykonaj działanie
        print("I collided with", message.other_id)
    end
end
```

## Odpowiedź punktu kontaktu

Wiadomość `"contact_point_response"` jest wysyłana, gdy jeden z obiektów biorących udział w zderzeniu ma typ "dynamic" lub "kinematic", a drugi ma typ "dynamic", "kinematic" lub "static". Zawiera następujące pola:

`position`
: pozycja punktu kontaktu w przestrzeni świata (`vector3`).

`normal`
: normalna w przestrzeni świata dla punktu kontaktu, skierowana od drugiego obiektu w stronę bieżącego obiektu (`vector3`).

`relative_velocity`
: prędkość względna obiektu kolizji obserwowana względem drugiego obiektu (`vector3`).

`distance`
: odległość penetracji między obiektami, nieujemna (`number`).

`applied_impulse`
: impuls wynikający z kontaktu (`number`).

`life_time`
: (*obecnie nieużywane!*) czas trwania kontaktu (`number`).

`mass`
: masa bieżącego obiektu kolizji w kg (`number`).

`other_mass`
: masa drugiego obiektu kolizji w kg (`number`).

`other_id`
: identyfikator instancji, z którą obiekt kolizji pozostaje w kontakcie (`hash`).

`other_position`
: pozycja drugiego obiektu kolizji w przestrzeni świata (`vector3`).

`other_group`
: grupa kolizyjna drugiego obiektu kolizji (`hash`).

`own_group`
: grupa kolizyjna obiektu kolizji (`hash`).

Jeśli tworzysz grę albo aplikację, w której obiekty muszą być rozdzielane z dużą dokładnością, wiadomość `"contact_point_response"` dostarcza wszystkich potrzebnych informacji. Zwróć jednak uwagę, że dla danej pary kolizji w jednej klatce możesz otrzymać kilka takich wiadomości `"contact_point_response"`, zależnie od charakteru zderzenia. Zobacz [Rozwiązywanie kolizji](/manuals/physics-resolving-collisions), aby poznać więcej szczegółów.

```Lua
function on_message(self, message_id, message, sender)
    -- sprawdź wiadomość
    if message_id == hash("contact_point_response") then
        -- wykonaj działanie
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## Odpowiedź na wyzwalacz

Wiadomość `"trigger_response"` jest wysyłana, gdy jeden z obiektów biorących udział w zderzeniu ma typ "trigger". Jest wysyłana raz, gdy kolizja zostanie wykryta po raz pierwszy, a potem jeszcze raz, gdy obiekty przestają ze sobą kolidować. Zawiera następujące pola:

`other_id`
: identyfikator instancji, z którą obiekt kolizji się zderzył (`hash`).

`enter`
: `true`, jeśli interakcja oznaczała wejście do wyzwalacza, `false`, jeśli oznaczała wyjście (`boolean`).

`other_group`
: grupa kolizyjna drugiego obiektu kolizji (`hash`).

`own_group`
: grupa kolizyjna obiektu kolizji (`hash`).

```Lua
function on_message(self, message_id, message, sender)
    -- sprawdź wiadomość
    if message_id == hash("trigger_response") then
        if message.enter then
            -- wykonaj działanie przy wejściu
            print("I am now inside", message.other_id)
        else
            -- wykonaj działanie przy wyjściu
            print("I am now outside", message.other_id)
        end
    end
end
```
