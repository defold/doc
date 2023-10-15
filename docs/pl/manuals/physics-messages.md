---
title: Wiadomości kolizji w Defoldzie
brief: Kiedy obiekty się zderzają, silnik Defold wysyła wiadomości do komponentów tych obiektów.
---

# Wiadomości kolizji

Kiedy dwa obiekty kolizji kolidują ze sobą, silnik wysyła wiadomości do wszystkich komponentów w obu tych obiektach:

## Odpowiedź na kolizję

Odpowiedź na kolizję `"collision_response"` to wiadomość wysyłana do wszystkich obiektów w przypadku ich kolizji. Zawiera ona następujące pola:

`other_id`
: identyfikator innej instancji, z którą obiekt kolizji kolidował (typ `hash`).

`other_position`
: pozycja innej instancji w przestrzeni świata gry (world position), z którą obiekt kolizji kolidował (typ `vector3`).

`other_group`
: grupa kolizyjna innego obiektu kolizji, z którą obiekt kolizji kolidował (typ `hash`).

Wiadomość `"collision_response"` jest odpowiednia do rozwiązywania kolizji, gdzie nie potrzebujesz szczegółów dotyczących rzeczywistego przecięcia (intersection) obiektów, na przykład, jeśli chcesz wykryć tylko czy pocisk trafia wroga. W ciągu jednej klatki jest wysyłana tylko jedna z tych wiadomości dla każdej pary obiektów kolidujących ze sobą.

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

Odpowiedź punktu kontaktu `"contact_point_response"` to wiadomość wysyłana, gdy jeden z kolidujących obiektów jest dynamiczny lub kinematyczny. Zawiera ona następujące pola:

`position`
: pozycja punktu kontaktu/styku w przestrzeni świata gry (world position) (typ `vector3`)

`normal`
: wektor normalny w przestrzeni świata do punktu kontaktu/styku, który wskazuje od innego obiektu kolizji w kierunku bieżącego obiektu, czyli tego, który otrzymał tę wiadomość (typ `vector3`).

`relative_velocity`
: prędkość względna obiektu kolizji obserwowana z punktu widzenia innego obiektu kolizji, z którym obiekt, który otrzymał tę wiadomość kolidował (typ `vector3`).

`distance`
: odległość penetracji między obiektami kolizji - nieujemna (typ `number`).

`applied_impulse`
: impuls, czyli siła która wynikała z kontaktu (typ `number`).

`life_time`
: (*obecnie nieużywane!*) czas trwania kontaktu (typ `number`).

`mass`
: masa bieżącego obiektu kolizji w kilogramach (typ `number`).

`other_mass`
: masa innego obiektu kolizji, z którym kolidował obiekt, który otrzymał tę wiadomość, w kilogramach (typ `number`).

`other_id`
: identyfikator instancji, z którą obiekt kolizji znajduje się w kontakcie (typ `hash`).

`other_position`
: pozycja w przestrzeni świata gry (world position) innego obiektu kolizji, z którym kolidował obiekt, który otrzymał tę wiadomość (typ `vector3`).

`group`
: grupa kolizyjna innego obiektu kolizji, z którym kolidował obiekt, który otrzymał tę wiadomość (typ `hash`).

Dla gry lub aplikacji, w których potrzebujesz idealnie rozdzielać obiekty, wiadomość `"contact_point_response"` dostarcza wszystkie informacje, których potrzebujesz. Należy jednak zauważyć, że w przypadku danej pary kolizji, w zależności od charakteru kolizji, można otrzymać wiele wiadomości `"contact_point_response"` w jednej klatce. Zobacz szczegóły w [instrukcji do rozwiązywania kolizji](/manuals/physics-resolving-collisions).

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

Odpowiedź na wyzwalacz `"trigger_response"` to wiadomość wysyłana, gdy obiekt kolidujący ma typ `"trigger"` (wyzwalacz).

W kolizji typu "trigger" są wysyłane wiadomości `"collision_response"`. Dodatkowo, wyzwalacze wysyłają również specjalną wiadomość `"trigger_response"` na początku i na końcu kolizji. Wiadomość ta zawiera następujące pola:

`other_id`
: identyfikator instancji, z którą obiekt kolizji kolidował (typ `hash`).

`enter`
: wejście - `true` jeśli interakcja była wejściem do wyzwalacza, `false`, jeśli była wyjściem (typ `boolean`).

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
