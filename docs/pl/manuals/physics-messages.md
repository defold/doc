---
title: Wiadomości kolizji w silniku Defold
brief: Kiedy obiekty się zderzają, silnik Defold wysyła wiadomości do komponentów tych obiektów.
---

# Wiadomości kolizji

Kiedy dwa obiekty kolizji pozostają w kontakcie, silnik wysyła zdarzenia do ich komponentów. Na przykład, wiadomość może być dostarczona do funkcji zwrotnej obsługi zdarzeń (`physics.set_event_listener()`) albo trafić do domyślnego odbiorcy wiadomości za pomocą `on_message()`.

## Filtracja zdarzeń

Rodzaje generowanych zdarzeń kontrolujesz przez przełączniki dla każdego obiektu kolizji:

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

Wszystkie są domyślnie ustawione na `true`. Gdy dwa obiekty kolizji wchodzą w interakcję, sprawdzamy te przełączniki, żeby zdecydować, czy wysłać wiadomość do gry.

Przykład dla zaznaczonych opcji "Generate Contact Events":

Gdy korzystasz z `physics.set_event_listener()`:

| Komponent A | Komponent B | Wyślij wiadomość |
|-------------|-------------|------------------|
| ✅︎          | ✅︎          | Tak              |
| ❌          | ✅︎          | Tak              |
| ✅︎          | ❌          | Tak              |
| ❌          | ❌          | Nie              |

Podstawowy handler wiadomości zachowuje się trochę inaczej:

| Komponent A | Komponent B | Wyślij wiadomość(y)   |
|-------------|-------------|------------------------|
| ✅︎          | ✅︎          | Tak (A,B) + (B,A)      |
| ❌          | ✅︎          | Tak (B,A)             |
| ✅︎          | ❌          | Tak (A,B)             |
| ❌          | ❌          | Nie                   |

## Odpowiedź na kolizję

Wiadomość "collision_response" jest wysyłana, gdy przynajmniej jeden z kolidujących obiektów ma typ "dynamic", "kinematic" lub "static". Zawiera następujące pola:

`other_id`
: identyfikator instancji, z którą obiekt kolizji kolidował (`hash`).

`other_position`
: pozycja innej instancji w przestrzeni świata gry, z którą obiekt kolizji kolidował (`vector3`).

`other_group`
: grupa kolizyjna drugiego obiektu (`hash`).

`own_group`
: grupa kolizyjna obiektu, który otrzymał wiadomość (`hash`).

Wiadomość "collision_response" nadaje się do prostych detekcji kolizji, kiedy nie potrzebujesz szczegółów przecięcia, np. gdy chcesz sprawdzić, czy pocisk trafił wroga. W ciągu jednej klatki zostaje wysłana tylko jedna taka wiadomość dla każdej pary obiektów.

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("collision_response") then
        -- take action
        print("I collided with", message.other_id)
    end
end
```

## Odpowiedź punktu kontaktu

Wiadomość "contact_point_response" jest wysyłana wtedy, gdy jeden z kolidujących obiektów ma typ "dynamic" lub "kinematic", a drugi może być "dynamic", "kinematic" lub "static". Oto zestaw dostępnych pól:

`position`
: pozycja punktu kontaktu w przestrzeni świata gry (`vector3`).

`normal`
: normalna w przestrzeni świata wskazująca od drugiego obiektu w kierunku aktualnego obiektu (`vector3`).

`relative_velocity`
: prędkość względna obserwowana z punktu widzenia drugiego obiektu (`vector3`).

`distance`
: odległość penetracji między obiektami (nieujemna, `number`).

`applied_impulse`
: impuls powstały wskutek kontaktu (`number`).

`life_time`
: (*obecnie nieużywane!*) czas trwania kontaktu (`number`).

`mass`
: masa bieżącego obiektu kolizji w kilogramach (`number`).

`other_mass`
: masa drugiego obiektu kolizji (`number`).

`other_id`
: identyfikator instancji, z którą obiekt kolizji się styka (`hash`).

`other_position`
: pozycja drugiego obiektu kolizji w przestrzeni świata (`vector3`).

`other_group`
: grupa kolizyjna drugiego obiektu (`hash`).

`own_group`
: grupa kolizyjna obiektu, który otrzymał wiadomość (`hash`).

Dla zastosowań wymagających najwyższej precyzji wiadomość "contact_point_response" dostarcza wszystkie potrzebne dane. Zwróć uwagę, że dla jednej pary kolidujących obiektów możesz otrzymać kilka takich wiadomości w jednej klatce, zależnie od natury kolizji. Zobacz [Resolving collisions for more information](/manuals/physics-resolving-collisions).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("contact_point_response") then
        -- take action
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## Odpowiedź na wyzwalacz

Wiadomość "trigger_response" jest wysyłana, gdy jeden z kolidujących obiektów ma typ "trigger". Występuje raz na początku kolizji i raz po jej zakończeniu. Zawiera ona następujące pola:

`other_id`
: identyfikator instancji, z którą obiekt kolizji kolidował (`hash`).

`enter`
: `true`, jeśli wejście było wejściem do wyzwalacza, `false`, jeśli było wyjściem (`boolean`).

`other_group`
: grupa kolizyjna innego obiektu (`hash`).

`own_group`
: grupa kolizyjna obiektu, który otrzymał wiadomość (`hash`).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("trigger_response") then
        if message.enter then
            -- take action for entry
            print("I am now inside", message.other_id)
        else
            -- take action for exit
            print("I am now outside", message.other_id)
        end
    end
end
```
