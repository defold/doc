---
title: Animacja modeli 3D
brief: Ta instrukcja opisuje wsparcie dla animacji modeli 3D w silniku Defold.
---

# Animacja modeli 3D

Animacja szkieletowa trójwymiarowych modeli jest podobna do animacji typu Spine, z tym, że działa również w trójwymiarze. Animacja szkieletowa modeli 3D wykorzystuje "kości" (ang. bones) modelu do deformacji wierzchołków (ang. vertices) w modelu. Model 3D nie jest jednak podzielony na osobne części związane ze sobą w łańcuch kinematyczny, a w zamian tego, ruch "kości" deformuje siatkę wierzchołków reprezentującą obiekt 3D, a Ty masz kontrolę nad tym, w jaki sposób kości wpływają na taką deformację.

  Szczegóły dotyczące importowania danych 3D do komponentu typu "Model" dla animacji znajdziesz tutaj: [Instrukcja Modeli 3D](/manuals/model).

  ![Blender animation](images/animation/blender_animation.png){.inline srcset="images/animation/blender_animation@2x.png 2x"}
  ![Wiggle loop](images/animation/suzanne.gif){.inline}

## Odtwarzanie animacji

Modele są animowane za pomocą funkcji [`model.play_anim()`](/ref/model#model.play_anim):

```lua
function init(self)
    -- Rozpocznij animację "wiggle" w tę i z powrotem komponentu #model
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
W chwili obecnej Defold obsługuje tylko tzw. animacje wypieczone (baked animations). Animacje muszą zawierać macierze dla każdej animowanej kości na każdej klatce kluczowej, a nie pozycje, rotacje i skale jako osobne klucze.

Animacje są także interpolowane liniowo. Jeśli chcesz użyć bardziej zaawansowanej interpolacji krzywych, animacje muszą zostać wypieczone (prebaked) z poziomu eksportera.

Klipy animacji w Collada nie są obsługiwane. Aby użyć wielu animacji na jednym modelu, wyeksportuj je jako osobne pliki *.dae*, a następnie zgromadź te pliki w pliku *.animationset* w Defold.
:::

### Hierarchia kości

Kości (ang. bones) w szkielecie modelu są reprezentowane wewnętrznie jako obiekty gry (game objects).

Możesz uzyskać identyfikator (id) instancji obiektu gry kości w czasie rzeczywistym. Funkcja [`model.get_go()`](/ref/model#model.get_go) zwraca identyfikator obiektu gry dla określonej kości.

```lua
-- Weź środek kości 002 obiektu gry modelu wiggler
local bone_go = model.get_go("#wiggler", "Bone_002")

-- Zrób coś z obiektem gry
```

### Animacja kursora

Oprócz korzystania z `model.play_anim()` do animacji modelu, komponenty typu *Model* udostępniają specjalną właściwość "kursor" (ang. cursor), którą można manipulować za pomocą `go.animate()` (więcej na temat [animacji właściwości](/manuals/property-animation))). Przykład:

```lua
-- Ustaw animację komponentu #model ale jeszcze nie rozpoczynaj
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- Ustaw kursor animacji na początku (0)
go.set("#model", "cursor", 0)
-- Animuj wartość kursora animacji między 0 i 1 w tę i z powrotem
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## Funkcje po zakończeniu animacji

Animacje modelu (`model.play_anim()`) obsługują opcjonalną funkcję zwrotną Lua jako ostatni argument. Funkcja ta zostanie wywołana po zakończeniu animacji. Funkcja nigdy nie jest wywoływana dla animacji w pętli, więc takich, których tryby odtwarzania zaczynają się od: `PLAYBACK_LOOP_*`, ani w przypadku ręcznego anulowania animacji za pomocą `go.cancel_animations()`. Funkcję zwrotną można wykorzystać do wyzwalania zdarzeń po zakończeniu animacji (np. procesu zadania obrażeń po skończonej animacji ataku) lub do połączenia różnych animacji w serie, jedna za drugą. Przykłady: 

```lua
local function wiggle_done(self, message_id, message, sender)
    -- Animacja skończona
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## Tryby odtwarzania

Animacje można odtwarzać raz lub w pętli. Sposób odtwarzania animacji jest określany przez tryb odtwarzania (ang. Playback mode):

* go.PLAYBACK_NONE
* go.PLAYBACK_ONCE_FORWARD
* go.PLAYBACK_ONCE_BACKWARD
* go.PLAYBACK_ONCE_PINGPONG
* go.PLAYBACK_LOOP_FORWARD
* go.PLAYBACK_LOOP_BACKWARD
* go.PLAYBACK_LOOP_PINGPONG
