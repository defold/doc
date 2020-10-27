---
title: Sprite - reprezentacja graficzna 2D
brief: Instrukcja ta opisuje jak pokazywać dwuwymiarowe grafiki używając komponentu typu Sprite.
---

#  Sprite

Komponent typu Sprite (z ang. dosłownie: chochlik/duszek/krasnoludek - popularna w gamedevie od lat nazwa obrazków 2D w grach - przyp.tłum.) to dwuwymiarowa reprezentacja wizualna w grafice komputerowej wyświetlana jako pojedynczy obrazek lub animacja poklatkowa (flipbook animation).

![sprite](images/graphics/sprite.png){srcset="images/graphics/sprite@2x.png 2x"}

Komponent typu Sprite może wykorzystywać jako teksturę [Galerię - Atlas](/manuals/atlas) lub [Źródło kafelków - Tile Source](/manuals/tilesource).

## Właściwości Sprite'ów

Poza właściwościami takimi jak *Id*, *Position* i *Rotation* komponenty te posiadają swoje specyficzne właściwości:

*Image*
: Obraz/tekstura dwuwymiarowa - może nią być Galeria - `Atlas` lub Źródło kafelków - `Tile Source`.

*DefaultAnimation*
: Domyślna animacja używana przy wyświetlaniu obrazu.

*Material*
: Materiał służący do renderowania.

*Blend Mode*
: Tryb "mieszania"/blendowania używany również przy renderowaniu. Więcej szczegółów poniżej.

### Blend modes - tryby blendowania
:[blend-modes](../shared/blend-modes.md)

## Manipulacja w trakcie działania programu

Możesz manipulować właściwościami Sprite'ów w trakcie działania programu dzięki wielu funkcjom i zmiennym właściwościom (szukaj przykładów użycia w [API](/ref/sprite/)). Funkcje:

* `sprite.play_flipbook()` - Odtwarzaj animację sprite'a.
* `sprite.set_hflip()` and `sprite.set_vflip()` - Odwróć w pionie lub poziomie animację/obraz sprite'a.

Sprite posiada również różne właściwości, którymi można manipulować przy użyciu funkcji `go.get()` i `go.set()`:

`cursor`
: Znormalizowany (czyli w przedziale 0-1) kursor animacji, czyli wskaźnik na klatki danej animacji poklatkowej (liczba - `number`).

`image`
: Obraz sprite'a (`hash`). Możesz użyć tej właściwości do podmiany tekstury sprite'a na inną galerią lub źródło kafelków, które mogą być właściwościami zasobu (resource property) i ustawić używając `go.set()`. Sprawdź szczegóły i przykłady w [API](/ref/sprite/#image).

`material`
: Materiał sprite'a (`hash`). Możesz podmienić materiał korzystając z właściwości zasobu (resource property) i ustawić używając `go.set()`. Sprawdź szczegóły i przykłady w [API](/ref/sprite/#material).

`playback_rate`
: Wskaźnik odtwarzania animacji, czyli prędkość z jaką odtwarzana jest animacja (`number`).

`scale`
: Skala obrazka (wektor - `vector3`).

`size`
: Rozmiar obrazka (`vector3`) (Wartość tylko do odczytu - pokazuje rozmiar tekstury).

## Stałe materiału

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: Kolor zabarwienia/odcienia obrazka (`vector4`). Wektor czterech komponentów reprezentuje zabarwienie, gdzie komponenty x, y, z, w odpowiadają składowym: czerwony, zielony, niebieski i przezroczystość (red, green, blue, alpha).

## Konfiguracja projektu

Plik *game.project* zawiera [te ustawienia](/manuals/project-settings#sprite) dotyczące sprite'ów.
