Komponenty są używane, żeby nadać obiektom gry konkretne właściwości i funkcjonalności, takie jak reprezentacja graficzna, dźwiękowa czy logika gry. Komponenty muszą należeć do obiektu gry i są afektowane przez zmiany jego pozycji, orientacji i skali:

![Components](../shared/images/components.png){srcset="../shared/images/components@2x.png 2x"}

Wiele komponentów ma specyficzne właściwości, które mogą być modyfikowane. Istnieją trzy specyficzne funkcje do interakcji z nimi w trakcie działania programu:

```lua
-- disable the can "body" sprite
msg.post("can#body", "disable")

-- play "hoohoo" sound on "bean" in 1 second
sound.play("bean#hoohoo", { delay = 1, gain = 0.5 } )
```

Komponenty są dodawane do obiektów gry z poziomu Edytora jako ich nowe komponenty lub referencje do istniejących plików komponentów:

<kbd>Naciśnij prawym przyciskiem myszki</kbd> na obiekcie gry w panelu *Outline* i wybierz <kbd>Add Component</kbd> (nowy komponent) lub <kbd>Add Component File</kbd> (jako referencja do pliku).

W większości przypadków sens ma tworzenie nowych komponentów specyficznych dla danego obiektu, ale często możesz też wykorzystywać wspólne komponenty dla wielu obiektów, a niektóre z nich nie mogą być utworzone inaczej niż przez stworzenie wcześniej pliku:

* Skrypty
* komponenty GUI
* Efekty cząsteczkowe (Particle FX)
* Mapy kafelków (Tile maps)
