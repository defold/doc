---
title: Właściwości w Defoldzie
brief: Ta instrukcja opisuje typy właściwości, jak je używać i animować.
---

# Właściwości

Defold udostępnia właściwości (ang. properties) dla obiektów gry, komponentów oraz węzłów GUI, które można odczytywać, ustawiać i animować. Istnieje kilka rodzajów właściwości:

* Systemowo zdefiniowane transformacje obiektów gry (pozycja, rotacja i skala) oraz specyficzne dla komponentów właściwości (na przykład rozmiar pikseli sprite'a lub masa obiektu kolizyjnego).
* Właściwości zdefiniowane przez użytkownika w komponentach skryptów Lua (zobacz [dokumentację właściwości skryptów](/manuals/script-properties)).
* Właściwości węzłów GUI.
* Stałe shaderów zdefiniowane w shaderach i plikach materiałów (zobacz [dokumentację materiałów](/manuals/material)).

W zależności od miejsca, w którym znajduje się właściwość, dostęp do niej uzyskuje się za pomocą funkcji ogólnej lub funkcji przeznaczonej do właściwości. Wiele z tych właściwości można automatycznie animować. Zaleca się animowanie właściwości za pomocą wbudowanego systemu, zarówno z powodów wydajnościowych, jak i wygody, zamiast manipulować nimi samodzielnie (wewnątrz funkcji `update()`).

Złożone właściwości typu `vector3`, `vector4` lub `quaternion` eksponują również swoje składowe (`x`, `y`, `z` i `w`). Możesz adresować składowe indywidualnie, dodając do nazwy właściwości kropkę (`.`) i nazwę składowej. Na przykład, aby ustawić składową x pozycji obiektu gry:

```lua
-- Ustaw x pozycji "game_object" na 10.
go.set("game_object", "position.x", 10)
```

Funkcje `go.get()`, `go.set()` i `go.animate()` przyjmują jako pierwszy parametr odniesienie oraz identyfikator właściwości jako drugi. Odniesienie identyfikuje obiekt gry (ang. game object) lub komponent (ang. component) i może być ciągiem znaków, haszem lub adresem URL. Adresy URL są szczegółowo omówione w [instrukcji dotyczącej adresowania](/manuals/addressing). Identyfikator właściwości to ciąg znaków lub hash, który określa właściwość.

```lua
-- Ustaw skalę x komponentu sprite
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

Dla węzłów GUI, identyfikator węzła jest podawany jako pierwszy parametr do funkcji przeznaczonej do właściwości:

```lua
-- Pobierz kolor przycisku
local node = gui.get_node("button")
local color = gui.get_color(node)
```

## Właściwości obiektów gry i komponentów

Wszystkie obiekty gry i niektóre typy komponentów mają właściwości, które można odczytywać i modyfikować w czasie rzeczywistym. Wartości te można odczytać za pomocą [`go.get()`](/ref/go#go.get) i zaktualizować za pomocą [`go.set()`](/ref/go#go.set). W zależności od typu wartości właściwości, można animować je za pomocą [`go.animate()`](/ref/go#go.animate). Kilka wybranych właściwości jest przeznaczonych tylko do odczytu.

`get`{.mark}
: Można je odczytywać za pomocą [`go.get()`](/ref/go#go.get).

`get+set`{.mark}
: Można je odczytywać za pomocą [`go.get()`](/ref/go#go.get) i aktualizować za pomocą [`go.set()`](/ref/go#go.set). Wartości numeryczne można animować za pomocą [`go.animate()`](/ref/go#go.animate).

*WŁAŚCIWOŚCI OBIEKTÓW GRY*

| Właściwość | Opis                                   | Typ             |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | Lokalna pozycja obiektu gry.           | `vector3`       | `get+set`{.mark} |
| *rotation* | Lokalna rotacja obiektu gry wyrażona jako kwaternion.    | `quaternion` | `get+set`{.mark} |
| *euler*    | Lokalna rotacja obiektu gry wyrażona jako kąty Eulera.   | `vector3`    | `get+set`{.mark} |
| *scale*    | Lokalna nieliniowa skala obiektu gry, wyrażona jako wektor, w którym każdy składnik zawiera mnożnik wzdłuż każdej osi. Przykładowo, aby podwoić rozmiar w osiach x i y, użyj vmath.vector3(2.0, 2.0, 0). | `vector3` | `get+set`{.mark} |

::: sidenote
Istnieją także konkretne funkcje do pracy z transformacją obiektu gry, takie jak `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`, `go.get_scale()` i `go.set_scale()`.
:::

*WŁAŚCIWOŚCI KOMPONENTÓW SPRITE*

| Właściwość | Opis                                   | Typ             |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | Rozmiar sprite'a nieprzeskalowany - jego rozmiar pobierany z atlasu źródłowego. | `vector3` | `get`{.mark} |
| *image*    | Skrót hasza ścieżki tekstury sprite'a. | `hash`    | `get`{.mark}|
| *scale*    | Nieliniowa skala sprite'a.             | `vector3` | `get+set`{.mark}|
| *material* | Materiał używany przez sprite'a.       | `hash`    | `get+set`{.mark}|
| *cursor*   | Pozycja (między 0 a 1) wskaźnika odtwarzania.   | `number`  | `get+set`{.mark}|
| *playback_rate* | Ilość klatek na sekundę animacji flipbook. | `number`  | `get+set`{.mark}|

*WŁAŚCIWOŚCI KOMPONENTÓW OBIEKTÓW KOLIZJI*

| Właściwość | Opis                                   | Typ             |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | Masa obiektu kolizyji.                 | `number`        | `get`{.mark} |
| *linear_velocity* | Aktualna prędkość liniowa obiektu kolizyji. | `vector3` | `get`{.mark} |
| *angular_velocity* | Aktualna prędkość kątowa obiektu kolizyji. | `vector3` | `get`{.mark} |
| *linear_damping* | Dławienie liniowe obiektu kolizyji. | `vector3`    | `get+set`{.mark} |
| *angular_damping* | Dławienie kątowe obiektu kolizyji. | `vector3`    | `get+set`{.mark} |

*WŁAŚCIWOŚCI KOMPONENTÓW MODELU 3D*

| Właściwość | Opis                                   | Typ             |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | Aktualna animacja.                    | `hash`          | `get`{.mark}     |
| *texture0*  | Skrót hasza ścieżki tekstury modelu.  | `hash` | `get`{.mark}|
| *cursor*    | Pozycja (między 0 a 1) wskaźnika odtwarzania. | `number`   | `get+set`{.mark} |
| *playback_rate* | Prędkość odtwarzania animacji. Mnożnik prędkości odtwarzania animacji. | `number` | `get+set`{.mark} |
| *material* | Materiał używany przez model. | `hash` | `get+set`{.mark}|

*WŁAŚCIWOŚCI KOMPONENTÓW ETYKIETY*

| Właściwość | Opis                                   | Typ             |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *scale*    | Skala etykiety.                        | `vector3`       | `get+set`{.mark} |
| *color*    | Kolor etykiety.                        | `vector4`       | `get+set`{.mark} |
| *outline*  | Kolor konturu etykiety.                | `vector4`       | `get+set`{.mark} |
| *shadow*   | Kolor cienia etykiety.                 | `vector4`       | `get+set`{.mark} |
| *size*     | Rozmiar etykiety. Rozmiar ogranicza tekst, jeśli jest włączona linia przerwy. | `vector3` | `get+set`{.mark} |
| *material* | Materiał używany przez etykietę.       | `hash`          | `get+set`{.mark}|
| *font*     | Czcionka używana przez etykietę.       | `hash`          | `get+set`{.mark}|

## Właściwości węzłów GUI

Węzły GUI również posiadają właściwości, ale są odczytywane i zapisywane za pomocą specjalnych funkcji getterów i setterów z API `gui`. Dla każdej właściwości istnieje funkcja gettera i settera. Istnieje także zestaw stałych zdefiniowanych do użycia jako odniesienie do właściwości podczas animacji. Jeśli potrzebujesz odnosić się do oddzielnych składowych właściwości, musisz używać nazwy ciągu znaków właściwości lub hasza nazwy ciągu znaków.

GUI nodes also contain properties, but they are read and written through special getter and setter functions. For each property there exists one get- and one set- function. There is also a set of constants defined to use as reference to the properties when animating them. If you need to refer to separate property components you have to use the string name of the property, or a hash of the string name.

* `position` (lub `gui.PROP_POSITION`)
* `rotation` (lub `gui.PROP_ROTATION`)
* `scale` (lub `gui.PROP_SCALE`)
* `color` (lub `gui.PROP_COLOR`)
* `outline` (lub `gui.PROP_OUTLINE`)
* `shadow` (lub `gui.PROP_SHADOW`)
* `size` (lub `gui.PROP_SIZE`)
* `fill_angle` (lub `gui.PROP_FILL_ANGLE`)
* `inner_radius` (lub `gui.PROP_INNER_RADIUS`)
* `slice9` (lub `gui.PROP_SLICE9`)

Zauważ, że wszystkie wartości koloru są zakodowane w vector4, gdzie składniki odpowiadają wartościom RGBA:

`x`
: Składnik koloru czerwonego

`y`
: Składnik koloru zielonego

`z`
: Składnik koloru niebieskiego

`w`
: Składnik alfa

*GUI NODE PROPERTIES*

| Właściwość | Opis                                   | Typ             |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*    | Kolor przedniej strony węzła.          | `vector4`       | `gui.get_color()` `gui.set_color()` |
| *outline*  | Kolor konturu węzła.                   | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | Pozycja węzła.                         | `vector3`       | `gui.get_position()` `gui.set_position()` |
| *rotation* | Obrót węzła wyrażony w kątach Eulera - stopnie obrócone wokół każdej osi. | `vector3` | `gui.get_rotation()` `gui.set_rotation()` |
| *scale*    | Skala węzła wyrażona jako mnożnik wzdłuż każdej osi.     | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow*   | Kolor cienia węzła.                    | `vector4`       | `gui.get_shadow()` `gui.set_shadow()` |
| *size*     | Rozmiar węzła niezeskalowany.          | `vector3`       | `gui.get_size()` `gui.set_size()` |
| *fill_angle*   | Kąt wypełnienia węzła typu pie wyrażony w stopniach przeciwnie do ruchu wskazówek zegara. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | Wewnętrzny promień węzła typu pie. | `number`        | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *slice9*   | Odległości brzegowe węzła typu slice9. | `vector4`       | `gui.get_slice9()` `gui.set_slice9()` |
