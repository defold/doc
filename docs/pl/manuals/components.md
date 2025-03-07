---
title: Komponenty obiektów gry
brief: Ta instrukcja prezentuje przegląd komponentów i jak ich używać.
---

#  Komponenty

:[components](../shared/components.md)

## Typy komponentów

Defold wspiera następujące typy komponentów:

* [Collection factory](/manuals/collection-factory) - Fabryki kolecji do ich tworzenia
* [Collection proxy](/manuals/collection-proxy) - Pełnomocnicy kolekcji do ich ładowania i zwalniania
* [Collision object](/manuals/physics) - Obiekty kolizji fizyki 2D i 3D
* [Camera](/manuals/camera) - Kamera, umożliwiająca zmianę projekcji i rzutni świata gry
* [Factory](/manuals/factory) - Fabryka do tworzenia obiektów gry
* [GUI](/manuals/gui) - Graficzny interfejs użytkownika
* [Label](/manuals/label) - Etykieta z tekstem
* [Mesh](/manuals/mesh) - Siatka trójwymiarowa (z tworzeniem i manipulacją w trakcie działania aplikacji)
* [Model](/manuals/model) - Model trójwymiarowy (z opcjonalnymi animacjami)
* [Particle FX](/manuals/particlefx) -  Efekty cząsteczkowe
* [Script](/manuals/script) - Skrypt, dodający logikę do gry
* [Sound](/manuals/sound) - Odtwarzanie dźwięku lub muzyki
* [Spine model](/manuals/spinemodel) - Model szkieletowy animacji
* [Sprite](/manuals/sprite) - Obraz dwuwymiarowy (z opcjonalną animacją poklatkową)
* [Tilemap](/manuals/tilemap) - Mapa kafelków

## Aktywowanie i dezaktywowanie komponentów

Komponenty obiektów gry są aktywne wraz z utworzeniem ich obiektu gry. Jeśli chcesz je dezaktywować możesz wysłać wiadomość [`disable`](/ref/go/#disable) do danego komponentu:

```lua
-- disable the component with id 'weapon' on the same game object as this script
msg.post("#weapon", "disable")

-- disable the component with id 'shield' on the 'enemy' game object
msg.post("enemy#shield", "disable")

-- disable all components on the current game object
msg.post(".", "disable")

-- disable all components on the 'enemy' game object
msg.post("enemy", "disable")
```

To enable a component again you can post an [`enable`](/ref/go/#enable) message to the component:

```lua
-- enable the component with id 'weapon'
msg.post("#weapon", "enable")
```

## Właściwości komponentów

Komponenty w Defoldzie mają różne właściwości. Panel [Właściwości](/manuals/editor/#the-editor-views) w edytorze pokazuje właściwości aktualnie wybranego w panelu [Outline](/manuals/editor/#the-editor-views) komponentu. Szukaj właściwości różnych komponentów w instrukcjach do nich.

## Pozycja, orientacja i skala komponentów

Komponenty wizualne mają pozycję, orientację i niektóre skalę. Właściwości te mogą być zmienione z poziomu Edytora Defold, ale w większości przypadków nie mogą już być zmienione w trakcie działania aplikacji (wyjątkiem jest skala sprite'ów i etykiet (label)).

Jeśli potrzebujesz zmienić pozycję, rotację czy skalę komponentu w czasie działania programu możesz zmienić właściwości obiektu gry, który posiada te komponenty. Skutkuje to jednak zmianą właściwości wszystkich komponentów danego obiektu gry. Jeśli chcesz manipulować pojedynczym komponentem, zalecamy, żeby przenieść dany komponent do innego obiektu gry, który będzie posiadał go osobno, a następnie dodanie takiego obiektu jako dziecko podstawowego obiektu, do którego komponent należał początkowo.

## Kolejność rysowania komponentów

Kolejność rysowania komponentów zależy od:

### Predykaty skryptu renderowania
Każdy komponent ma przypisany [materiał](/manuals/material/), a każdy materiał ma jeden lub więcej tagów. Skrypt renderowania z kolei określa liczbę predykatów, z których każdy odpowiada tagowi. [Predykaty są rysowane jeden nad poprzednim](/manuals/render/#render-predicates) w funkcji *update()*, a komponenty, których materiały mają tagi określone dla danego predykatu są wtedy rysowane. Domyślny skrypt renderowania wyrysuje najpierw sprite'y i mapy kafelków, następnie efekty cząsteczkowe osobno w przestrzeni świata gry, a na końcu komponenty GUI w przestrzeni ekranu.

### Wartość współrzędnej Z
Wszystkie obiekty gry i komponenty są umieszczone w przestrzeni 3D z pozycją jako wektor trzech współrzędnych. Kiedy oglądasz swoją grę w 2D, wspołrzędne X i Y pozycję elementu na ekranie wzdłuż szerokości i wysokości, a współrzędna Z określa głębokość. Umożliwia to więc określanie pozycji nachodzących się na siebie kształtów: sprite z wartością Z = 1 pojawi się przed sprite'm z pozycją Z = 0. Domyślnie, Defold umożliwia rysowanie obiektów na osi Z o wartościach z przedziału -1 i 1:

![model](images/graphics/z-order.png)

Komponenty, których materiały mają tagi określone dla danego [predykatu](/manuals/render/#render-predicates) są rysowane razem, a kolejność ich rysowania zależy od ostatecznej wartości współrzędnej Z. Ostateczna wartość Z jest sumą wartości Z komponentu, obiektu gry i każdego obiektu, do którego należy dany obiektu (rodzica).

::: sidenote
Kolejność, w której rysowane są komponenty GUI components **NIE** jest określona przez współrzędne Z komponentów GUI. Kolejność ta jest kontrolowana przez funkcję [gui.set_render_order()](/ref/gui/#gui.set_render_order:order).
:::

Przykład: Dwa obiekty gry A i B. Obiekt B jest dzieckiem obiektu A. Obiekt B ma komponent typu sprite.

| Id       | Z       |
|----------|---------|
| A        | 2       |
| B        | 1       |
| B#sprite | 0.5     |

![](images/graphics/component-hierarchy.png)

Przy powyższej hierarchi ostateczna wartość Z komponentu typu sprite to 2 + 1 + 0.5 = 3.5.

::: important
Jeśli dwa komponenty mają dokładnie taką samą wartość komponentu Z, to kolejność rysowania jest nieokreślona i obiekty mogą migać zmieniając nieustannie tę kolejność w zależności od platformy.

Domyślny skrypt renderowania określa najbliższą i najdalszą powierzchnię na osi Z (równoległą do płaszczyzny XY), która zostanie wyrysowana. Każdy komponent, który miałby być wyrysowany poza tymi wartościami nie będzie renderowany. Domyślny przedział wartości Z to -1 do 1, ale z łatwością [można go zmienić](/manuals/render/#default-view-projection). Precyzja numeryczna wartości Z pomiędzy wartościa -1 i 1 jest bardzo wysoka. Pracując z zasobami 3D, możesz chciceć zmienić limity najbliższej i najdalszej powierzchni w Twoim skrypie renderowania. Więcej szczegółów znajdziesz w [instrucji do renderowania](/manuals/render/).
:::
