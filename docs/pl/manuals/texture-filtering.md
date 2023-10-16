---
title: Filtrowanie i próbkowanie tekstur
brief: Ta instrukcja opisuje możliwe opcje filtrowania i próbkowania tekstur podczas renderowania grafiki.
---

# Filtrowanie i próbkowanie tekstur

Filtrowanie tekstury decyduje o wyniku wizualnym w przypadkach, gdy _texel_ (pojedynczy piksel w teksturze) nie jest idealnie wyrównany z rzeczywistym pikselem na ekranie. Dzieje się tak, gdy przesuniesz element graficzny zawierający teksturę o mniej niż jeden piksel. Dostępne są następujące metody filtrowania:

Nearest
: Najbliższy texel zostanie wybrany do pokolorowania piksela na ekranie. Ta metoda próbkowania powinna być wybrana, jeśli chcesz uzyskać idealne mapowanie jeden do jednego od pikseli na teksturze do tego, co widzisz na ekranie. Dzięki filtrowaniu "Nearest" wszystko będzie przeskakiwać z piksela na piksel podczas przesuwania. Może to wyglądać "nerwowo", jeśli Sprite porusza się wolno, za to może się sprawdzać przy grafice pixelart.

Linear
: Liniowe filtrowanie - kolor texelu zostanie uśredniony z kolorami sąsiadujących texeli przed pokolorowaniem piksela na ekranie. Ta metoda sprawia, że powolne, płynne ruchy wyglądają gładko, ponieważ Sprite stopniowo przechodzi w piksele, zanim zostaną one w pełni pokolorowane - dzięki czemu możliwe jest przesuwanie Sprite'a o mniej niż jeden pełny piksel.

Ustawienie, której metody filtrowania używać, znajduje się w Ustawieniach Projektu - [Project Settings](/manuals/project-settings/#graphics). Istnieją dwa takie ustawienia:

default_texture_min_filter
: Filtrowanie przy pomniejszaniu jest stosowane, gdy texel jest mniejszy niż piksel na ekranie.

default_texture_mag_filter
: Filtrowanie przy powiększaniu jest stosowane, gdy texel jest większy niż piksel na ekranie.	

Oba ustawienia mogą przyjmować wartości `linear` lub `nearest`. Na przykład:

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

Jeśli nie określisz niczego, oba są domyślnie ustawione na `linear`.

Zauważ, że ustawienie w *game.project* jest używane w domyślnych narzędziach do próbkowania (samplers). Jeśli określisz samplery we własnym, niestandardowym materiale, możesz ustawić metodę filtrowania dla każdego samplera osobno. Zobacz szczegóły w [instrukcji do materiałów](/manuals/material/).
