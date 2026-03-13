---
title: Wyświetlanie obrazów 2D
brief: Ta instrukcja opisuje, jak wyświetlać obrazy 2D i animacje przy użyciu komponentu Sprite.
---

# Sprite

Komponent Sprite to prosty obraz lub animacja poklatkowa (flipbook), która jest wyświetlana na ekranie.

![sprite](images/graphics/sprite.png)

Komponent Sprite może korzystać jako źródła grafiki z [Atlasu](/manuals/atlas) albo [Tile source (Źródła kafelków)](/manuals/tilesource).

## Właściwości komponentu Sprite

Poza właściwościami *Id*, *Position* i *Rotation* komponent ma następujące właściwości specyficzne dla Sprite:

*Image*
: Jeśli shader ma pojedynczy sampler, to pole nosi nazwę `Image`. W przeciwnym razie każde pole jest nazwane zgodnie z samplerem tekstury w materiale. Każde pole określa zasób atlasu albo źródła kafelków używany przez sprite na danym samplerze tekstury.

*Default Animation*
: Animacja używana przez sprite. Informacje o animacji są pobierane z pierwszego atlasu albo źródła kafelków.

*Material*
: Materiał używany do renderowania sprite'a.

*Blend Mode*
: Tryb mieszania używany podczas renderowania sprite'a.

*Size Mode*
: Jeśli ustawisz `Automatic`, edytor sam ustawi rozmiar sprite'a. Jeśli ustawisz `Manual`, możesz ustawić rozmiar ręcznie.

*Slice 9*
: Ustaw tę opcję, aby zachować rozmiar pikseli tekstury przy krawędziach sprite'a podczas zmiany jego rozmiaru.

:[Slice-9](../shared/slice-9-texturing.md)

### Tryby mieszania
:[blend-modes](../shared/blend-modes.md)

## Manipulacja w czasie działania

Możesz modyfikować sprite'y w czasie działania za pomocą różnych funkcji i właściwości. Sposób użycia znajdziesz w [dokumentacji API](/ref/sprite/). Funkcje:

* `sprite.play_flipbook()` - Odtwarza animację na komponencie Sprite.
* `sprite.set_hflip()` i `sprite.set_vflip()` - Ustawiają poziome i pionowe odbicie animacji sprite'a.

Sprite ma też kilka właściwości, którymi można manipulować przy użyciu `go.get()` i `go.set()`:

`cursor`
: Znormalizowany kursor animacji (`number`).

`image`
: Obraz sprite'a (`hash`). Możesz go zmienić za pomocą właściwości zasobu wskazującej atlas albo źródło kafelków i funkcji `go.set()`. Przykład znajdziesz w [referencji API](/ref/sprite/#image).

`material`
: Materiał sprite'a (`hash`). Możesz go zmienić za pomocą właściwości zasobu materiału i funkcji `go.set()`. Przykład znajdziesz w [referencji API](/ref/sprite/#material).

`playback_rate`
: Tempo odtwarzania animacji (`number`).

`scale`
: Niejednorodna skala sprite'a (`vector3`).

`size`
: Rozmiar sprite'a (`vector3`). Tę właściwość można zmienić tylko wtedy, gdy tryb rozmiaru sprite'a jest ustawiony na ręczny.

## Stałe materiału

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: Odcień koloru sprite'a (`vector4`). `vector4` reprezentuje zabarwienie, gdzie składowe x, y, z i w odpowiadają kolejno kanałom czerwieni, zieleni, błękitu i alfa.

## Atrybuty materiału

Sprite może nadpisywać atrybuty wierzchołków z aktualnie przypisanego materiału. Zostaną one przekazane z komponentu do vertex shadera. Więcej informacji znajdziesz w [instrukcji do materiałów](/manuals/material/#attributes).

Atrybuty określone w materiale pojawią się w inspectorze jako zwykłe właściwości i można je ustawiać osobno dla każdego komponentu Sprite. Jeśli którykolwiek atrybut zostanie nadpisany, będzie widoczny jako nadpisana właściwość i zostanie zapisany w pliku sprite'a na dysku:

![sprite-attributes](../images/graphics/sprite-attributes.png)

## Konfiguracja projektu

Plik *game.project* zawiera kilka [ustawień projektu](/manuals/project-settings#sprite) związanych ze sprite'ami.

## Sprite'y z wieloma teksturami

Gdy sprite korzysta z wielu tekstur, warto pamiętać o kilku rzeczach.

### Animacje

Dane animacji, takie jak fps i nazwy klatek, są obecnie pobierane z pierwszej tekstury. Nazwijmy ją „animacją sterującą”.

Id obrazów z animacji sterującej są używane do wyszukiwania obrazów w kolejnej teksturze. Dlatego ważne jest, aby id klatek były zgodne pomiędzy teksturami.

Na przykład, jeśli `diffuse.atlas` ma animację `run` w takiej postaci:

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

to id klatek będą wyglądały tak: `run/hero_run_color_1`. Taki identyfikator prawdopodobnie nie zostanie znaleziony na przykład w `normal.atlas`:

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

Dlatego używamy `Rename patterns` w [instrukcji do atlasów](/manuals/atlas/), aby zmienić te nazwy. Ustaw `_color=` i `_normal=` w odpowiednich atlasach, a w obu atlasach otrzymasz nazwy klatek w tej postaci:

```
run/hero_run_1
run/hero_run_2
...
```

### UVs

Współrzędne UV są pobierane z pierwszej tekstury. Ponieważ istnieje tylko jeden zestaw wierzchołków, nie da się zagwarantować dobrego dopasowania, jeśli dodatkowe tekstury mają więcej współrzędnych UV albo inny kształt.

Warto o tym pamiętać i zadbać, aby obrazy miały wystarczająco podobne kształty, bo w przeciwnym razie może pojawić się bleeding tekstur.

Wymiary obrazów w poszczególnych teksturach mogą się różnić.
