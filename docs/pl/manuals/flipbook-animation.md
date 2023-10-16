---
title: Animacja poklatkowa - Flip-book
brief: Ta instrukcja opisuje wsparcie dla animacji poklatkowych w silniku Defold.
---

# Animacja poklatkowa - flip-book

Animacja poklatkowa (ang. flip-book animation) składa się z serii obrazów (klatek animacji), które są pokazywane jeden za drugim, więc patrząc na nie sprawiają wrażenie ruchu. Technika ta jest bardzo podobna do tradycyjnej animacji używanej w kinematografii [https://pl.wikipedia.org/wiki/Animacja](https://pl.wikipedia.org/wiki/Animacja) i oferuje nieograniczoną kontrolę, ponieważ każda klatka może być modyfikowana indywidualnie. Jednakże pamięć zajmowana przez wszystkie obrazy składające się na taką animację może być duża w zależności od ilości klatek i ich wielkości. Płynność animacji zależy od liczby klatek pokazywanych w każdej sekundzie (FPS z ang. frames per second), co wymaga oczywiście większej ilości pracy. Animacje typu flip-book w Defoldzie są przechowywane albo jako indywidualne obrazy umieszczone w galerii zwanej [Atlas](/manuals/atlas), albo jako obrazy umieszczone w bezpośrednim sąsiedztwie, w poziomej sekwencji jak kafelki w tzw. Źródle Kafelków - [Tile Source](/manuals/tilesource).

  ![Animation sheet](images/animation/animsheet.png){.inline}
  ![Run loop](images/animation/runloop.gif){.inline}

## Odtwarzanie animacji flip-book

Sprite'y i węzły GUI mogą odtwarzać animacje poklatkowe i masz nad tym całkowitą kontrolę w trakcie działania programu.

Sprite'y
: Aby odtworzyć animację w trakcie działania programu używa się funkcji [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]). Poniżej przykład.

Węzły GUI
: Aby odtworzyć animację w trakcie działania programu używa się funkcji [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]). Poniżej przykład.

::: sidenote
Tryb odtwarzania (playback mode) "once ping-pong" odtworzy animację klatka po klatce do samego końca, a następnie odtworzy ją jeszcze raz w odwrotnej kolejności, od tyłu, ale do **drugiej** klatki animacji, a nie do pierwszej. Jest to zabieg służący łatwemu wiązaniu animacji w serie.
:::

### Przykład animacji ze spritem

Załóżmy, że Twoja gra posiada możliwość "uniku", która pozwala graczom nacisnąć klawisz, aby wykonać unik. Masz przygotowane 4 animacje, żeby w pełni pokazać unik:

"idle"
: Zapętlona animacja stojącej postaci będącej w bezczynności.

"dodge_idle"
: Zapętlona animacja postaci pochylonej, będącej w trakcie trwania uniku.

"start_dodge"
: Jednokrtotnie odtwarzana animacja postaci w momencie przejścia animacji z pozycji stojącej do pochylonej w celu wykonania uniku.

"stop_dodge"
: Jednokrtotnie odtwarzana animacja postaci w momencie przejścia animacji z pozycji uniku z powrotem do pozycji stojącej.

Skrypt poniżej przedstawia potrzebną logikę:

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" to nasza akcja zbindowana z inputem
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- zapamiętaj, że wykonujemy unik
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- zapamiętaj, że skończyliśmy unik
            self.dodge = false
        end
    end
end
```

### Przykład animacji z węzłem GUI

Przy wyborze obrazu i animacji dla węzła graficznego interfejsu użytkownika (ang. GUI), np. "box" albo "pie" tak naprawdę właśnie przypisujesz źródło obrazów (atlas lub tile source) i domyślną animację, tak samo jak w przypadku sprite'ów. Takie źródło grafiki jest statycznie przypisane do węzła, ale animacja może być zmieniona w trakcie trwania programu. Nieruchome obrazki są traktowane jako jednoklatkowa animacja, więc zamiana obrazu jest jednoznaczna z odtworzeniem innej animacji poklatkowej na węźle:

```lua
function init(self)
    local character_node = gui.get_node("character")
    -- To wymaga, żeby węzły miały domyślne animacje w tym samym atlasie lub źródłe kafelków
    -- co nowa animacja, którą odtwarzamy
    gui.play_flipbook(character_node, "jump_left")
end
```

## Funkcje po zakończeniu animacji

Funckje `sprite.play_flipbook()` i `gui.play_flipbook()` przyjmują jako ostatni argument opcjonalną funkcję, która jest wywoływana w momencie zakończenia animacji, tzw. callback. Będzie ona wywołana po skończeniu animacji, więc tylko dla takich, które nie są zapętlone, czyli w trybach odtwarzania: `PLAYBACK_ONCE_*` i nie będzie wywołana w przypadku ręcznego anulowania animacji za pomocą `go.cancel_animations()`. Można użyć takiej funkcjonalności w celu wywołania specjalnych wydarzeń po skończonej animacji (np. procesu zadania obrażeń po skończonej animacji ataku) lub do połączenia różnych animacji w serie, jedna za drugą. Przykłady:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    sprite.play_flipbook("#character", "jump_left", flipbook_done)
end
```

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    gui.play_flipbook(gui.get_node("character"), "jump_left", flipbook_done)
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
