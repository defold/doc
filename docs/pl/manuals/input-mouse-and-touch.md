---
title: Wejścia myszki i dotykowe w silniku Defold
brief: Ta instrukcja wyjaśnia, jak działa wejście za pomocą myszki i dotyku na urządzeniach dotykowych w silniku Defold.
---

::: sidenote
Zalecamy zapoznanie się z ogólnym sposobem działania wejścia w Defoldzie, jak przechwytuje się wejście, jak wiążę z akcjami oraz w jakiej kolejności skrypty odbierają dane wejściowe. Dowiedz się więcej na temat systemu wejść w [ogólnej instrukcji na temat Wejść](/manuals/input).
:::

# Obsługa myszki

Wyzwalacze myszy pozwalają na przypisanie akcji gry do klawiszy myszy i kółka przewijania.

![](images/input/mouse_bindings.png)

::: sidenote
Przyciski myszy `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` i `MOUSE_BUTTON_MIDDLE` są równoznaczne z `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` i `MOUSE_BUTTON_3`.
:::

::: important
Poniższe przykłady korzystają z akcji pokazanych na powyższym obrazku. Możesz dowolnie nazywać akcje wejściowe - użyj takich, jakie są dla Ciebie najlepsze.
:::

## Przyciski myszki

Klawisze myszy generują zdarzenia wciśnięcia, zwolnienia i powtarzania. Przykład pokazuje, jak wykrywać wejście z lewego klawisza myszy (czy wciśnięty lub zwolniony):

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- wciśnięto lewy przycisk myszy
        elseif action.released then
            -- wciśnięto prawy przycisk myszy
        end
    end
end
```

::: important
Akcje wejścia `MOUSE_BUTTON_LEFT` (lub `MOUSE_BUTTON_1`) są również wysyłane dla pojedynczego dotyku na urządzeniach dotykowych.
:::

## Kółko myszki

Wejścia kółka myszy wykrywają akcje przewijania. Pole `action.value` wynosi `1`, jeśli kółko zostało przewinięte, a w przeciwnym przypadku `0` (akcje przewijania traktowane są tak, jak gdyby były to naciśnięcia klawiszy). Aktualnie Defold nie obsługuje dokładnego przewijania palcem na urządzeniach dotykowych.

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- przewinięcie kółka myszy w górę
        end
    end
end
```

## Ruch myszki

Ruch myszy jest obsługiwany osobno. Zdarzenia ruchu myszy nie są normalnie odbierane, chyba że w twoich przypisaniach wejścia jest ustawiony przynajmniej jeden wyzwalacz myszy.

Ruch myszy nie jest opisywany w ustawieniach *input bindings*, dlatego `action_id` jest ustawiane na `nil`, a tabela `action` jest wypełniana pozycją i zmianą pozycji myszy, kiedy mysz jest poruszona.

```lua
function on_input(self, action_id, action)
    if action.x and action.y then
        -- pozwól obiektowi gry śledzić ruch myszy/dotyku
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# Obsługa urządzeń dotykowych

Wyzwalacze dotyku (pojedynczego i wielodotykowego (ang. multitouch)) są dostępne na urządzeniach iOS i Android w aplikacjach natywnych oraz w grach przeglądarkowych HTML5.

![](images/input/touch_bindings.png)

## Pojedyncze dotknięcie

Wyzwalacze pojedynczego dotyku nie są konfigurowane z poziomu sekcji *Touch Triggers* w przypisaniach wejścia (input bindings). Zamiast tego, wyzwalacze pojedynczego dotyku są **automatycznie konfigurowane**, gdy masz skonfigurowane wejście z klawiszem myszy `MOUSE_BUTTON_LEFT` lub `MOUSE_BUTTON_1`.

## Multi-touch

Wyzwalacze dotyku wielokrotnego wypełniają tabelę w tabeli akcji o nazwie `touch`. Elementy w tabeli są indeksowane liczbami całkowitymi od `1` do `N`, gdzie `N` to liczba punktów dotyku. Każdy element tabeli zawiera pola z danymi wejściowymi:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- Twórz w każdym punkcie dotyku
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
Multi-touch nie może być przypisany do tej samej akcji co wejście klawisza myszy `MOUSE_BUTTON_LEFT` lub `MOUSE_BUTTON_1`. Przypisanie tej samej akcji efektywnie nadpisze wyzwalacze pojedynczego dotyku i uniemożliwi otrzymanie jakichkolwiek zdarzeń pojedyncze dotknięcie.
:::

::: sidenote
Gotowe rozwiązania do używania elementów sterowania na ekranie dotykowym (on-screen controls) czy ogólnie do obsługi przycisków i gałek analgowych z obsługą przeciągania i kliknięcia można znaleźć w bibliotece [Defold-Input](https://defold.com/assets/defoldinput/).
:::


## Detekcja kliknięć i dotknięć na obiekcie

Wykrywanie kliknięć lub dotknięć na komponentach wizualnych to bardzo częsta operacja, którą można znaleźć w wielu grach. Może to być interakcja użytkownika z przyciskiem lub innym elementem interfejsu użytkownika, a także interakcja z obiektem gry, takim jak jednostka kontrolowana przez gracza w grze strategicznej, skarb na poziomie w grze typu dungeon crawler czy postać oferująca zadanie w grze RPG. Sposób użycia różni się w zależności od rodzaju komponentu wizualnego.

### Wykrywanie interakcji z węzłami GUI

Dla elementów interfejsu użytkownika istnieje funkcja `gui.pick_node(node, x, y)`, która zwraca wartość `true` lub `false`, w zależności od tego, czy określona współrzędna mieści się w granicach węzła GUI. Aby dowiedzieć się więcej, zajrzyj do [dokumentacji API](/ref/gui/#gui.pick_node:node-x-y), [przykładu nawigacji wskaźnikiem myszy](/examples/gui/pointer_over/) lub [przykładu z przyciskiem](/examples/gui/button/.

### Wykrywanie interakcji z obiektami gry

W przypadku obiektów gry (game objects) jest bardziej skomplikowane wykrywanie interakcji, ponieważ takie rzeczy jak przekształcenia kamery i projekcje renderowania mogą wpłynąć na wymagane obliczenia. Istnieją dwa ogólne podejścia do wykrywania interakcji z obiektami gry:

  1. Śledzenie pozycji i rozmiaru obiektów gry, z którymi użytkownik może współdziałać, i sprawdzanie, czy współrzędne myszy lub dotyku mieszczą się w granicach któregoś z tych obiektów.
  2. Dołączanie obiektów kolizji do obiektów gry, z którymi użytkownik może współdziałać, oraz jednego obiektu kolizji, który podąża za myszą lub palcem i sprawdzanie kolizji między nimi.

::: sidenote
Gotowe rozwiązanie do używania obiektów kolizji do wykrywania wejścia użytkownika z obsługą przeciągania i kliknięcia można znaleźć w elemencie [Defold-Input](https://defold.com/assets/defoldinput/).
:::

W obu przypadkach konieczne jest przeliczenie współrzędnych przestrzeni ekranu myszy lub dotyku na współrzędne przestrzeni gry. Można to zrobić na kilka różnych sposobów:

  * Ręczne śledzenie, który widok i projekcja są używane przez skrypt renderujący i wykorzystaj to do przeliczenia współrzędnych na współrzędne przestrzeni gry. Zobacz [instrukcję kamery](/manuals/camera/#converting-mouse-to-world-coordinates).
  * Użyj [bibliotek dla kamery](/manuals/camera/#third-party-camera-solutions) i skorzystaj z dostarczonych funkcji konwersji z ekranu na świat.
