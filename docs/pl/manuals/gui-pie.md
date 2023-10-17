---
title: Węzły pierścieniowe - pie w Defoldzie.
brief: Ta instrukcja wyjaśnia jak używać węzłów typu pie.
---

# Węzeł GUI typu pie

Węzły pierścieniowe - "pie" są używane do tworzenia obiektów okrągłych lub elipsoidalnych, począwszy od zwykłych okręgów po kształty przypominające placki lub kwadratowe pączki.

## Tworzenie węzła pie

Kliknij <kbd>prawym przyciskiem myszy</kbd> w sekcji *Nodes* w panelu *Outline* i wybierz <kbd>Add ▸ Pie</kbd>. Nowy węzeł pie zostaje zaznaczony, i możesz modyfikować jego właściwości.

![Create pie node](images/gui-pie/create.png){srcset="images/gui-pie/create@2x.png 2x"}

Następujące właściwości są unikalne dla węzłów pie:

Inner Radius
: Wewnętrzny promień węzła, wyrażony wzdłuż osi X.

Outer Bounds
: Kształt zewnętrznych granic węzła.

  - `Ellipse`  rozszerzy węzeł do zewnętrznego promienia.
  - `Rectangle`  rozszerzy węzeł do obwiedni węzła.

Perimeter Vertices
: Wierzchołki obwiedni - liczba segmentów, które zostaną użyte do zbudowania kształtu, wyrażona jako liczba wierzchołków wymaganych do pełnego obwiedni 360 stopni węzła.

Pie Fill Angle
: Kąt wypełnienia - określa, ile z placka ma zostać wypełnione. Wyrażane jako kąt przeciwny do ruchu wskazówek zegara, zaczynając od prawej strony.

![Properties](images/gui-pie/properties.png){srcset="images/gui-pie/properties@2x.png 2x"}

Jeśli ustawisz teksturę na węźle, obraz tekstury jest używany "płasko", tak aby rogi tekstury korelowały z rogami obwiedni węzła.

## Modyfikacja węzłów pie w czasie działania programu

Węzły pie reagują na ogólne funkcje manipulacji węzłami do ustawiania rozmiaru, punktu obrotu, koloru i innych. Istnieje kilka funkcji i właściwości dostępnych tylko dla węzłów pie:

```lua
local pienode = gui.get_node("my_pie_node")

-- pobierz zewnętrzne granice
local fill_angle = gui.get_fill_angle(pienode)

-- zwiększ liczbę wierzchołków obwiedni
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- zmień zewnętrzne granice
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- animuj wewnętrzny promień
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
