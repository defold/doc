---
title: Wejście z myszy i dotyku w Defold
brief: Ta instrukcja wyjaśnia, jak działa wejście z myszy i dotyku.
---

::: sidenote
Zaleca się najpierw zapoznać z ogólnym sposobem działania wejścia w Defold, z tym, jak odbiera się wejście i w jakiej kolejności skrypty je otrzymują. Więcej informacji znajdziesz w [instrukcji ogólnej o wejściu](/manuals/input).
:::

# Wyzwalacze myszy
Wyzwalacze myszy pozwalają przypisać wejście z przycisków myszy i kółka przewijania do akcji gry.

![](images/input/mouse_bindings.png)

::: sidenote
Wejścia z przycisków myszy `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` i `MOUSE_BUTTON_MIDDLE` są równoważne `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` i `MOUSE_BUTTON_3`.
:::

::: important
Poniższe przykłady używają akcji pokazanych na obrazku powyżej. Jak w przypadku każdego wejścia, możesz nazwać swoje akcje wejściowe dowolnie.
:::

## Przyciski myszy
Przyciski myszy generują zdarzenia naciśnięcia, zwolnienia i powtórzenia. Poniższy przykład pokazuje, jak wykryć wejście z lewego przycisku myszy (zarówno przy naciśnięciu, jak i przy zwolnieniu):

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- lewy przycisk myszy naciśnięty
        elseif action.released then
            -- lewy przycisk myszy zwolniony
        end
    end
end
```

::: important
Akcje wejścia `MOUSE_BUTTON_LEFT` (lub `MOUSE_BUTTON_1`) są wysyłane także dla pojedynczego dotyku.
:::

## Kółko myszy
Wejścia z kółka myszy wykrywają przewijanie. Pole `action.value` ma wartość `1`, jeśli kółko zostało przewinięte, i `0` w przeciwnym razie. Zdarzenia przewijania są traktowane jak naciśnięcia przycisków. Obecnie Defold nie obsługuje precyzyjnego przewijania na gładzikach.

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- kółko myszy przewinięte w górę
        end
    end
end
```

## Ruch myszy
Ruch myszy jest obsługiwany osobno. Zdarzenia ruchu myszy nie są odbierane, jeśli nie skonfigurujesz przynajmniej jednego wyzwalacza myszy.

Ruch myszy nie jest powiązany w <kbd>input bindings</kbd>, ale `action_id` ma wartość `nil`, a tabela `action` zawiera położenie myszy oraz zmianę jej położenia.

```lua
function on_input(self, action_id, action)
    if action.x and action.y then
        -- pozwól obiektowi gry podążać za ruchem myszy/dotyku
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# Wyzwalacze dotyku
Wyzwalacze pojedynczego dotyku i wielodotyku są dostępne na urządzeniach iOS i Android w aplikacjach natywnych oraz w pakietach HTML5.

![](images/input/touch_bindings.png)

## Pojedynczy dotyk
Wyzwalacze pojedynczego dotyku nie są konfigurowane w sekcji <kbd>Touch Triggers</kbd> w <kbd>input bindings</kbd>. Zamiast tego są **automatycznie konfigurowane**, gdy masz ustawione wejście myszy dla `MOUSE_BUTTON_LEFT` lub `MOUSE_BUTTON_1`.

## Wielodotyk
Wyzwalacze wielodotyku wypełniają tabelę `touch` w tabeli akcji. Elementy w tabeli są indeksowane liczbami całkowitymi od `1` do `N`, gdzie `N` to liczba punktów dotyku. Każdy element zawiera pola z danymi wejściowymi:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- Twórz obiekt w każdym punkcie dotyku
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
Multi-touch nie może być przypisany do tej samej akcji co wejście myszy `MOUSE_BUTTON_LEFT` lub `MOUSE_BUTTON_1`. Przypisanie tej samej akcji w praktyce nadpisze pojedynczy dotyk i uniemożliwi otrzymywanie jakichkolwiek zdarzeń pojedynczego dotyku.
:::

::: sidenote
Biblioteka [Defold-Input asset](https://defold.com/assets/defoldinput/) może posłużyć do łatwego ustawienia wirtualnych elementów sterowania na ekranie, takich jak przyciski i analogowe gałki, z obsługą wielodotyku.
:::

## Wykrywanie kliknięć lub stuknięć na obiektach
Wykrywanie, kiedy użytkownik kliknął lub stuknął element wizualny, to bardzo częsta operacja potrzebna w wielu grach. Może dotyczyć interakcji z przyciskiem lub innym elementem interfejsu użytkownika albo interakcji z obiektem gry, takim jak jednostka kontrolowana przez gracza w grze strategicznej, skarb na poziomie w grze typu dungeon crawler albo zleceniodawca zadania w RPG. Sposób działania zależy od rodzaju elementu wizualnego.

### Wykrywanie interakcji z węzłami GUI
W przypadku elementów UI dostępna jest funkcja `gui.pick_node(node, x, y)`, która zwraca true albo false zależnie od tego, czy podana współrzędna mieści się w granicach węzła GUI. Zobacz [dokumentację API](/ref/gui/#gui.pick_node:node-x-y), [przykład wykrywania wskaźnika](/examples/gui/pointer_over/) lub [przykład przycisku](/examples/gui/button/) aby dowiedzieć się więcej.

### Wykrywanie interakcji z obiektami gry
W przypadku obiektów gry jest to bardziej złożone, ponieważ takie czynniki jak przesunięcie kamery i projekcja w skrypcie renderowania wpływają na wymagane obliczenia. Istnieją dwa ogólne podejścia do wykrywania interakcji z obiektami gry:

  1. Śledzić pozycję i rozmiar obiektów gry, z którymi użytkownik może wejść w interakcję, i sprawdzać, czy współrzędne myszy lub dotyku mieszczą się w granicach któregokolwiek z tych obiektów.
  2. Dołączyć obiekty kolizji do obiektów gry, z którymi użytkownik może wejść w interakcję, oraz jeden obiekt kolizji podążający za myszą lub palcem, a następnie sprawdzać kolizje między nimi.

::: sidenote
Gotowe rozwiązanie wykorzystujące obiekty kolizji do wykrywania wejścia użytkownika z obsługą przeciągania i kliknięć można znaleźć w [Defold-Input asset](https://defold.com/assets/defoldinput/).
:::

W obu przypadkach trzeba przeliczyć współrzędne ekranu dla zdarzenia myszy lub dotyku na współrzędne świata obiektów gry. Można to zrobić na kilka sposobów:

  * Ręcznie śledzić, jaki widok i jaka projekcja są używane przez skrypt renderowania, a następnie wykorzystać je do przeliczania między współrzędnymi świata i ekranu. Zobacz [instrukcję o kamerze](/manuals/camera/#converting-mouse-to-world-coordinates) jako przykład.
  * Użyć [rozwiązania kamery innej firmy](/manuals/camera/#third-party-camera-solutions) i skorzystać z dostarczonych funkcji konwersji z ekranu do świata.
