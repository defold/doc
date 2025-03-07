---
title: Importowanie i używanie grafiki 2D
brief: Ta instrukcja opisuje ze szczegółami jak importować i używać grafiki 2D.
---

# Importowanie grafiki 2D

Defold wspiera różnego rodzaju komponenty wizualne używane często w grach 2D. Możesz użyć Defolda do stworzenia statycznych i animowanych sprite'ów, komponentów interfejsu użytkownika (GUI), efektór cząsteczkowych (particle fx), map kafelków (tilemap) fontów bitmapowych i animacji Spine. Zanim możliwe będzie stworzenie tych wizualnych komponentów, musisz zaimportować pliki graficzne, których chcesz używać. Aby zaimportować pliki, przenieś je do katalogu projektu lub przeciągnij nad panel *Assets pane* w edytorze Defold.

![Importowanie plików](images/graphics/import.png)

::: sidenote
Defold wspiera pliki graficzne w formatach PNG i JPEG. Pliki PNG muszą być w formacie 32-bitowym RGBA. Inne pliki graficzne muszą być przekonwertowane do wspieranych, aby móc ich użyć.
:::


## Tworzenie zasobów Defolda

Kiedy pliki graficzne są już zaimportowane do projektu, mogą być wykorzystywane do stworzenia różnych specyficznych dla Defolda zasobów:

![atlas](images/icons/atlas.png){.icon} Atlas (galeria)
: Atlas (galeria obrazów) zawiera listę oddzielnych plików graficznych, które są automatycznie połączone w jedną, większą teksturę. Atlasy mogą zawierać statyczne, pojedyncze obrazy lub mogą zawierać grupy tworzące animację poklatkową używając opcji *Animation Groups*.

  ![atlas](images/graphics/atlas.png)

Więcej szczegółów na ten temat znajdziejsz w [tej instrukcji do atlasów](/manuals/atlas).

![tile source](images/icons/tilesource.png){.icon} Tile Source (źródło kafelków)
: Żródła kafelków zawierają referencje do plików graficznych, które są przygotowane w ten sposób, że mogą być podzielone na mniejsze kafelki (ang. tile) ułożone na kwadratowej, jednakowej siatce. Często obrazki takie nazywane są również _sprite sheet_. Źródła kafelków mogą również zawierać animacje poklatkowe zdefiniowane przez określenie pierwszego i ostatniego numeru kafelka, które są po kolei odtwarzane. Ponadto, korzystając ze źródła kafelków, można automatycznie określić kształt kolizji na podstawie obrazu na danym kafelku (transparentne tło jest "wycinane" z kształtu kolizji danego kafelka).

  ![tile source](images/graphics/tilesource.png)

Więcej szczegółów na ten temat znajdziejsz w [tej instrukcji do źródeł kafelków](/manuals/tilesource).

![bitmap font](images/icons/font.png){.icon} Fonty bitmapowe
: Fonty bitmapowe zawierają informacje o znakach (ang. glyph) w arkuszu fontowym PNG. Te typy fontów nie są lepsze od fontów TrueType czy OpenType pod kątem wydajności, ale mogą dodaktowo zawierać informację o kolorach, cieniach, obrysowaniach i grafice bezpośrednio w pliku.

Więcej szczegółów na ten temat znajdziejsz w [tej instrukcji do fontów](/manuals/font/#bitmap-bmfonts).

  ![BMfont](images/font/bm_font.png)


## Używanie zasobów Defolda

Kiedy już pliki graficzne są przekonwertowane w zasoby typu Atlas czy Tile Source, możesz używać ich do tworzenia wielu różnych rodzajów komponentów wizualnych:

![sprite](images/icons/sprite.png){.icon}
: Sprite (obraz) jest statycznym obrazem lub animacją poklatkową (ang. flipbook animation) wyświetlaną na ekranie.

  ![sprite](images/graphics/sprite.png)

Więcej szczegółów na ten temat znajdziejsz w [tej instrukcji do sprite'ów](/manuals/sprite).

![tile map](images/icons/tilemap.png){.icon} Tile map (mapy kafelków)
: Mapa kafelków (ang. tile map) składa w jedną całość (mapę) kafelki (zarówno obrazy jak i kształty kolizji) ze źródeł kafelków. Mapy kafelków nie mogą korzystać z atlasów jako źródła.

  ![tilemap](images/graphics/tilemap.png)

Więcej szczegółów na ten temat znajdziejsz w [tej instrukcji do map kafelków](/manuals/tilemap).

![particle effect](images/icons/particlefx.png){.icon} Particle fx (efekty cząsteczkowe)
: Efekty cząteczkowe są tworzone przy użyciu cząsteczek (ang. particles) rozpylanych z emiterów cząsteczek (ang. particle emitter). Cząstki te mogą składać się ze statycznych obrazów lub animacji poklatkowych zarówno z atlasów jak i źródeł kafelków.

  ![particles](images/graphics/particles.png)

Więcej szczegółów na ten temat znajdziejsz w [tej instrukcji do efektów cząsteczkowych](/manuals/particlefx).

![gui](images/icons/gui.png){.icon} GUI (graficzny interfejs użytkownika)
: Węzły prostokątne i kołowe GUI (ang. box nodes, pie nodes) mogą wykorzystywać statyczne obrazy lub animacje poklatkowe zarówno z atlasów jak i źródeł kafelków.

  ![gui](images/graphics/gui.png)

Więcej szczegółów na ten temat znajdziejsz w [tej instrukcji do interfejsów użytkownika GUI](/manuals/gui).

![spine](images/icons/spine-model.png){.icon} Model Spine
: Modele szkieletowe Spine przetwarzają dane ze scen Spine. Zawierają dwie składowe danych:

  1. Plik w formacie Spine JSON, który opisuje animację kości (ang. bone) czy też tzw. szkieletu.
  2. Atlas zawierający informacje o obrazach dołączanych do poszczególnych kości szkieletu. Modele Spine nie mogą korzystać ze źródeł kafelków.

  ![spine](images/graphics/spine.png)

Więcej szczegółów na ten temat znajdziejsz w [tej instrukcji do modeli Spine](/manuals/spinemodel).
