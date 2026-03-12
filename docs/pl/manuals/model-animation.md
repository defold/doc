---
title: Animacja modeli 3D w silniku Defold
brief: Ta instrukcja opisuje, jak używać animacji modeli 3D w silniku Defold.
---

# Animacja szkieletowa 3D

Animacja szkieletowa modeli 3D wykorzystuje kości (ang. bones) modelu do deformowania wierzchołków (ang. vertices) w siatce, która tworzy obiekt 3D.

Szczegóły dotyczące importowania danych 3D do komponentu *Model* dla potrzeb animacji znajdziesz w [instrukcji modeli 3D](/manuals/model).

![Blender animation](images/animation/blender_animation.png)
![Wiggle loop](images/animation/suzanne.gif)

## Odtwarzanie animacji

Modele animuje się za pomocą funkcji [`model.play_anim()`](/ref/model#model.play_anim):

```lua
function init(self)
    -- Uruchom animację "wiggle" w tę i z powrotem na komponencie #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Silnik Defold aktualnie obsługuje tylko animacje wypieczone (baked animations). Animacje muszą zawierać macierze dla każdej animowanej kości na każdej klatce kluczowej, zamiast osobnych kluczy pozycji, rotacji i skali.

Animacje są interpolowane liniowo. Jeśli chcesz zrobić bardziej zaawansowaną interpolację krzywych, musisz wcześniej wypiec (prebaked) animację w eksporcie.
:::

### Hierarchia kości

Kości (ang. bones) w szkielecie modelu są reprezentowane wewnętrznie jako obiekty gry (game objects).

W czasie działania gry możesz pobrać identyfikator obiektu gry odpowiadającego konkretnej kości za pomocą funkcji [`model.get_go()`](/ref/model#model.get_go).

```lua
-- Pobierz obiekt gry dla środkowej kości modelu wiggler
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Wykonaj z nim dowolną operację...
```

### Animacja kursora

Oprócz wywoływania `model.play_anim()` do sterowania animacją, komponenty *Model* wystawiają właściwość "cursor", którą można animować za pomocą `go.animate()` (więcej w sekcji [animacje właściwości](/manuals/property-animation)).

```lua
-- Ustaw animację na komponencie #model, ale jej nie uruchamiaj
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Ustaw kursor na początku animacji
go.set("#model", "cursor", 0)
-- Pomiędzy 0 a 1 animuj kursor w tę i z powrotem z easingiem in-out quad
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Callbacki zakończenia

Funkcja `model.play_anim()` obsługuje opcjonalny callback Lua podany jako ostatni argument. Zostaje on wywołany po zakończeniu animacji. Nie jest uruchamiany dla animacji zapętlonych (z `PLAYBACK_LOOP_*`) ani gdy animację anulujesz ręcznie przez `go.cancel_animations()`. Callback umożliwia uruchamianie zdarzeń po zakończeniu animacji lub łączenie animacji w sekwencję.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Animacja zakończona
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Tryby odtwarzania

Animacje można odtwarzać raz lub w pętli, a sposób ich grania zależy od wybranego trybu odtwarzania (ang. playback mode):

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
