---
title: Animacja modeli 3D w instrukcji Defold
brief: Ta instrukcja opisuje, jak używać animacji modeli 3D w Defold.
---

# Animacja szkieletowa 3D

Animacja szkieletowa modeli 3D wykorzystuje kości modelu do deformowania wierzchołków w siatce modelu.

Szczegóły dotyczące importowania danych 3D do komponentu Model na potrzeby animacji znajdziesz w [dokumentacji Model](/manuals/model).

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
Defold obecnie obsługuje tylko animacje wypieczone (baked animations). Animacje muszą zawierać macierze dla każdej animowanej kości na każdej klatce kluczowej, a nie osobne klucze pozycji, rotacji i skali.

Animacje są też interpolowane liniowo. Jeśli potrzebujesz bardziej zaawansowanej interpolacji krzywych, musisz wypiec animację wcześniej, w eksporcie.
:::

### Hierarchia kości

Kości w szkielecie modelu są wewnętrznie reprezentowane jako obiekty gry (game objects).

W czasie działania gry możesz pobrać identyfikator obiektu gry odpowiadającego danej kości za pomocą funkcji [`model.get_go()`](/ref/model#model.get_go).

```lua
-- Pobierz obiekt gry dla środkowej kości modelu wiggler
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Potem wykonaj na nim potrzebną operację...
```

### Animacja kursora

Oprócz używania `model.play_anim()` do sterowania animacją komponenty *Model* udostępniają właściwość "cursor", którą można animować za pomocą `go.animate()` (więcej w sekcji [animacje właściwości](/manuals/property-animation)).

```lua
-- Ustaw animację na komponencie #model, ale jej nie uruchamiaj
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Ustaw kursor na początku animacji
go.set("#model", "cursor", 0)
-- Animuj kursor między 0 a 1 w trybie pingpong z easingiem in-out quad
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Wywołania zwrotne po zakończeniu

Funkcja `model.play_anim()` obsługuje opcjonalny callback Lua jako ostatni argument. Zostaje on wywołany, gdy animacja dobiegnie końca. Nie jest wywoływany dla animacji zapętlonych ani wtedy, gdy anulujesz animację ręcznie przez `go.cancel_animations()`. Callback możesz wykorzystać do uruchamiania zdarzeń po zakończeniu animacji albo do łączenia kilku animacji w sekwencję.

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Zakończono animację
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Tryby odtwarzania

Animacje można odtwarzać raz albo w pętli. Sposób ich odtwarzania zależy od wybranego trybu:

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
