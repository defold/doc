---
title: Profile tekstur w Defold
brief: Defold obsługuje automatyczne przetwarzanie tekstur i kompresję danych obrazów. Ta instrukcja opisuje dostępne funkcje.
---

# Profile tekstur

Defold obsługuje automatyczne przetwarzanie tekstur i kompresję danych obrazów w zasobach typu *Atlas*, *Tile source*, *Cubemap* oraz w samodzielnych teksturach używanych przez modele, GUI i inne elementy.

Istnieją dwa typy kompresji: programowa kompresja obrazów oraz sprzętowa kompresja tekstur.

1. Kompresja programowa, taka jak PNG i JPEG, zmniejsza rozmiar zasobów obrazów na dysku. Dzięki temu końcowy bundle jest mniejszy. Jednak pliki obrazów muszą zostać rozpakowane podczas wczytywania do pamięci, więc mimo niewielkiego rozmiaru na dysku mogą zajmować dużo pamięci RAM.

2. Sprzętowa kompresja tekstur również zmniejsza rozmiar zasobów obrazów, ale w przeciwieństwie do kompresji programowej obniża także zużycie pamięci przez tekstury po załadowaniu. Dzieje się tak dlatego, że układ graficzny potrafi bezpośrednio pracować na skompresowanych teksturach, bez wcześniejszego rozpakowywania.

Przetwarzanie tekstur konfiguruje się za pomocą konkretnego profilu tekstur. W tym pliku tworzysz *profiles*, które określają, jakich skompresowanych formatów i jakiego typu kompresji należy użyć podczas tworzenia bundli dla konkretnej platformy. Następnie profile łączy się z pasującymi *path patterns*, co daje precyzyjną kontrolę nad tym, które pliki projektu mają zostać skompresowane i w jaki sposób.

Ponieważ wszystkie dostępne sprzętowe metody kompresji tekstur są stratne, w danych tekstury pojawią się artefakty. To, jak będą wyglądały, mocno zależy od materiału źródłowego i użytej metody kompresji. Warto testować własne zasoby i eksperymentować, aby uzyskać najlepszy rezultat.

Możesz wybrać, jaka programowa kompresja obrazu zostanie zastosowana do końcowych danych tekstury w archiwach bundla, zarówno dla danych już skompresowanych, jak i surowych. Defold obsługuje formaty kompresji [Basis Universal](https://github.com/BinomialLLC/basis_universal) oraz [ASTC](https://www.khronos.org/opengl/wiki/ASTC_Texture_Compression).

::: sidenote
Kompresja jest operacją kosztowną obliczeniowo i czasowo. W zależności od liczby kompresowanych tekstur, wybranych formatów i rodzaju kompresji programowej może bardzo wydłużyć czas builda.
:::

### Basis Universal

Basis Universal, w skrócie BasisU, kompresuje obraz do formatu pośredniego, który podczas działania jest transkodowany do sprzętowego formatu odpowiedniego dla GPU bieżącego urządzenia. Format Basis Universal zapewnia wysoką jakość, ale jest stratny. Wszystkie obrazy są dodatkowo kompresowane przy użyciu LZ4, aby jeszcze bardziej zmniejszyć rozmiar plików przechowywanych w archiwum gry.

### ASTC

ASTC to elastyczny i wydajny format kompresji tekstur opracowany przez ARM i ustandaryzowany przez Khronos Group. Oferuje szeroki zakres rozmiarów bloków i przepływności bitowej, dzięki czemu można skutecznie wyważyć jakość obrazu i zużycie pamięci. ASTC obsługuje rozmiary bloków od 4×4 do 12×12 texeli, co odpowiada przepływności od 8 bitów na texel do 0,89 bita na texel. Taka elastyczność pozwala bardzo precyzyjnie sterować kompromisem między jakością a wymaganiami pamięciowymi.

Poniższa tabela pokazuje obsługiwane rozmiary bloków i odpowiadające im przepływności bitowe:

| Rozmiar bloku (szerokość x wysokość) | Bity na piksel |
| ------------------------------------ | -------------- |
| 4x4                                  | 8.00           |
| 5x4                                  | 6.40           |
| 5x5                                  | 5.12           |
| 6x5                                  | 4.27           |
| 6x6                                  | 3.56           |
| 8x5                                  | 3.20           |
| 8x6                                  | 2.67           |
| 10x5                                 | 2.56           |
| 10x6                                 | 2.13           |
| 8x8                                  | 2.00           |
| 10x8                                 | 1.60           |
| 10x10                                | 1.28           |
| 12x10                                | 1.07           |
| 12x12                                | 0.89           |

#### Obsługiwane urządzenia

Choć ASTC daje bardzo dobre rezultaty, nie jest wspierane przez wszystkie karty graficzne. Oto skrócona lista wsparcia według producenta GPU:

| Producent GPU       | Wsparcie                                                                 |
| ------------------- | ------------------------------------------------------------------------ |
| ARM (Mali)          | Wszystkie układy ARM Mali obsługujące OpenGL ES 3.2 lub Vulkan wspierają ASTC. |
| Qualcomm (Adreno)   | Układy Adreno obsługujące OpenGL ES 3.2 lub Vulkan wspierają ASTC.      |
| Apple               | GPU Apple od układu A8 obsługują ASTC.                                  |
| NVIDIA              | Wsparcie ASTC dotyczy głównie mobilnych GPU, np. układów Tegra.         |
| AMD (Radeon)        | GPU AMD obsługujące Vulkan zwykle wspierają ASTC programowo.            |
| Intel (Integrated)  | Nowoczesne GPU Intela wspierają ASTC programowo.                        |

## Profile tekstur

Każdy projekt zawiera plik `*.texture_profiles`, który przechowuje konfigurację używaną podczas kompresji tekstur. Domyślnie jest to `builtins/graphics/default.texture_profiles`, a jego konfiguracja przypisuje każdy zasób tekstury do profilu używającego formatu RGBA, bez sprzętowej kompresji tekstur i z domyślną kompresją plików ZLib.

Aby dodać kompresję tekstur:

- Wybierz <kbd>File ▸ New...</kbd> i utwórz nowy plik *Texture Profiles*. Alternatywnie skopiuj `default.texture_profiles` poza katalog `builtins`.
- Wybierz nazwę i lokalizację nowego pliku.
- Zmień wpis `texture_profiles` w `game.project`, aby wskazywał na nowy plik.
- Otwórz plik `*.texture_profiles` i skonfiguruj go zgodnie z potrzebami projektu.

![New profiles file](images/texture_profiles/texture_profiles_new_file.png)

![Setting the texture profile](images/texture_profiles/texture_profiles_game_project.png)

Możesz włączać i wyłączać użycie profili tekstur w preferencjach edytora. Wybierz <kbd>File ▸ Preferences...</kbd>. W zakładce *General* znajduje się pole wyboru *Enable texture profiles*.

![Texture profiles preferences](images/texture_profiles/texture_profiles_preferences.png)

## Ustawienia ścieżek

Sekcja *Path Settings* w pliku profili tekstur zawiera listę wzorców ścieżek oraz informację, który *profile* należy zastosować do zasobów pasujących do danej ścieżki. Ścieżki zapisuje się jako wzorce "Ant Glob" - szczegóły znajdziesz w [dokumentacji](http://ant.apache.org/manual/dirtasks.html#patterns). Można używać następujących wildcardów:

`*`
: Dopasowuje zero lub więcej znaków. Na przykład `sprite*.png` pasuje do plików `sprite.png`, `sprite1.png` i `sprite_with_a_long_name.png`.

`?`
: Dopasowuje dokładnie jeden znak. Na przykład `sprite?.png` pasuje do plików `sprite1.png` i `spriteA.png`, ale nie do `sprite.png` ani `sprite_with_a_long_name.png`.

`**`
: Dopasowuje całe drzewo katalogów albo, gdy jest użyte jako nazwa katalogu, zero lub więcej katalogów. Na przykład `/gui/**` pasuje do wszystkich plików w katalogu `/gui` i jego podkatalogach.

![Paths](images/texture_profiles/texture_profiles_paths.png)

Ten przykład zawiera dwa wzorce ścieżek i odpowiadające im profile.

`/gui/**/*.atlas`
: Wszystkie pliki `*.atlas` w katalogu `/gui` i jego podkatalogach będą przetwarzane zgodnie z profilem `gui_atlas`.

`/**/*.atlas`
: Wszystkie pliki `*.atlas` w dowolnym miejscu projektu będą przetwarzane zgodnie z profilem `atlas`.

Zwróć uwagę, że bardziej ogólny wzorzec umieszczono na końcu. Algorytm dopasowania działa od góry do dołu. Zostanie użyte pierwsze wystąpienie pasujące do ścieżki zasobu. Dopasowanie niżej na liście nigdy nie nadpisuje pierwszego trafienia. Gdyby kolejność była odwrotna, każdy atlas zostałby przetworzony profilem `atlas`, również te z katalogu `/gui`.

Zasoby tekstur, które *nie* pasują do żadnej ścieżki z pliku profili, zostaną skompilowane i przeskalowane do najbliższej potęgi dwójki, ale poza tym pozostaną bez zmian.

## Profile

Sekcja *profiles* w pliku profili tekstur zawiera listę nazwanych profili. Każdy profil zawiera jedną lub więcej pozycji *platforms*, a każda platforma jest opisana zestawem właściwości.

![Profiles](images/texture_profiles/texture_profiles_profiles.png)

*Platforms*
: Określa pasującą platformę. `OS_ID_GENERIC` pasuje do wszystkich platform, `OS_ID_WINDOWS` do bundli Windows, `OS_ID_IOS` do bundli iOS itd. Jeśli podasz `OS_ID_GENERIC`, zostanie on uwzględniony dla wszystkich platform.

::: important
Jeśli dwa [ustawienia ścieżek](#ustawienia-ścieżek) pasują do tego samego pliku, a dana ścieżka używa różnych profili z różnymi platformami, zostaną użyte **oba** profile i wygenerowane zostaną **dwie** tekstury.
:::

*Formats*
: Jeden lub więcej formatów tekstur do wygenerowania. Jeśli podasz kilka formatów, do bundla trafią tekstury w każdym z nich. Silnik wybierze podczas działania format obsługiwany przez bieżącą platformę.

*Mipmaps*
: Jeśli opcja jest zaznaczona, dla tej platformy zostaną wygenerowane mipmapy. Domyślnie jest wyłączona.

*Premultiply alpha*
: Jeśli opcja jest zaznaczona, kanał alfa zostanie przemnożony z danymi tekstury. Domyślnie jest włączona.

*Max Texture Size*
: Jeśli ustawisz wartość inną niż zero, rozmiar tekstur w pikselach zostanie ograniczony do tej wartości. Każda tekstura szersza lub wyższa od tej granicy zostanie przeskalowana w dół.

Każdy wpis *Formats* dodany do profilu ma następujące właściwości:

*Format*
: Format używany podczas kodowania tekstury. Listę dostępnych formatów znajdziesz poniżej.

*Compressor*
: Kompresor używany do kodowania tekstury.

*Compressor Preset*
: Ustawia preset kompresji używany podczas kodowania wynikowego obrazu. Każdy preset zależy od danego kompresora i jego wewnętrznych ustawień. Dla uproszczenia dostępne presety mają obecnie cztery poziomy:

| Preset      | Informacja                                  |
| ----------- | ------------------------------------------- |
| `LOW`       | Najszybsza kompresja. Niska jakość obrazu   |
| `MEDIUM`    | Domyślna kompresja. Najlepsza jakość obrazu |
| `HIGH`      | Najwolniejsza kompresja. Mniejszy plik      |
| `HIGHEST`   | Wolna kompresja. Najmniejszy plik           |

Pamiętaj, że kompresor `uncompressed` ma tylko jeden preset o nazwie `uncompressed`, co oznacza brak kompresji tekstur.
Listę dostępnych kompresorów znajdziesz w sekcji [Kompresory](#compressors).

## Formaty tekstur

Tekstury sprzętowe mogą być przetwarzane do danych nieskompresowanych albo *stratnie* skompresowanych, z różną liczbą kanałów i różną głębią bitową. W przypadku stałorozmiarowej kompresji sprzętowej wynikowy obraz ma zawsze z góry określony rozmiar, niezależnie od treści. Oznacza to, że utrata jakości zależy od zawartości oryginalnej tekstury.

Ponieważ transkodowanie Basis Universal zależy od możliwości GPU urządzenia, zalecane formaty do stosowania z kompresją Basis Universal to formaty ogólne:
`TEXTURE_FORMAT_RGB`, `TEXTURE_FORMAT_RGBA`, `TEXTURE_FORMAT_RGB_16BPP`, `TEXTURE_FORMAT_RGBA_16BPP`, `TEXTURE_FORMAT_LUMINANCE` oraz `TEXTURE_FORMAT_LUMINANCE_ALPHA`.

Transkoder Basis Universal obsługuje wiele formatów wyjściowych, między innymi `ASTC4x4`, `BCx`, `ETC2`, `ETC1` i `PVRTC1`.

Obecnie obsługiwane są następujące formaty stratnej kompresji:

| Format                           | Kompresja | Szczegóły |
| -------------------------------- | --------- | --------- |
| `TEXTURE_FORMAT_RGB`             | brak      | Kolor 3-kanałowy. Kanał alfa jest odrzucany. |
| `TEXTURE_FORMAT_RGBA`            | brak      | Kolor 3-kanałowy i pełny kanał alfa. |
| `TEXTURE_FORMAT_RGB_16BPP`       | brak      | Kolor 3-kanałowy. 5+6+5 bitów. |
| `TEXTURE_FORMAT_RGBA_16BPP`      | brak      | Kolor 3-kanałowy i pełny kanał alfa. 4+4+4+4 bity. |
| `TEXTURE_FORMAT_LUMINANCE`       | brak      | 1-kanałowa skala szarości, bez alfy. Kanały RGB są zredukowane do jednego. Alfa jest odrzucana. |
| `TEXTURE_FORMAT_LUMINANCE_ALPHA` | brak      | 1-kanałowa skala szarości i pełny kanał alfa. Kanały RGB są zredukowane do jednego. |

W przypadku ASTC liczba kanałów zawsze wynosi 4 (RGB + alfa), a sam format określa rozmiar kompresji blokowej.
Te formaty są zgodne wyłącznie z kompresorem ASTC. Każda inna kombinacja spowoduje błąd builda.

`TEXTURE_FORMAT_RGBA_ASTC_4X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X5`
`TEXTURE_FORMAT_RGBA_ASTC_8X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X5`
`TEXTURE_FORMAT_RGBA_ASTC_10X6`
`TEXTURE_FORMAT_RGBA_ASTC_10X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X12`

## Kompresory

Domyślnie obsługiwane są następujące kompresory tekstur. Dane zostaną rozpakowane po załadowaniu pliku tekstury do pamięci.

| Nazwa          | Formaty              | Informacja |
| -------------- | -------------------- | ---------- |
| `Uncompressed` | Wszystkie formaty    | Brak kompresji. Ustawienie domyślne. |
| `BasisU`       | Wszystkie formaty RGB/RGBA | Wysokiej jakości, stratna kompresja Basis Universal. Niższa jakość daje mniejszy rozmiar. |
| `ASTC`         | Wszystkie formaty ASTC | Stratna kompresja ASTC. Niższa jakość daje mniejszy rozmiar. |

::: sidenote
W Defold 1.9.7 przebudowano pipeline kompresji tekstur tak, aby obsługiwał instalowalne kompresory. To pierwszy krok do umożliwienia implementowania algorytmów kompresji tekstur w rozszerzeniach, na przykład WEBP albo własnych rozwiązań.
:::

## Przykładowy obraz

Aby lepiej pokazać wynik działania kompresji, poniżej znajduje się przykład. Pamiętaj, że jakość obrazu, czas kompresji i rozmiar skompresowanych danych zawsze zależą od obrazu wejściowego i mogą się różnić.

Obraz bazowy (1024x512):
![New profiles file](images/texture_profiles/kodim03_pow2.png)

### Czas kompresji

| Preset      | Czas kompresji | Czas względny |
| ----------- | -------------- | ------------- |
| `LOW`       | 0m0.143s       | 0.5x          |
| `MEDIUM`    | 0m0.294s       | 1.0x          |
| `HIGH`      | 0m1.764s       | 6.0x          |
| `HIGHEST`   | 0m1.109s       | 3.8x          |

### Utrata sygnału

Porównanie wykonano narzędziem `basisu`, mierząc PSNR.
100 dB oznacza brak utraty sygnału, czyli identyczny obraz jak oryginał.

| Preset      | Sygnał |
| ----------- | ------ |
| `LOW`       | Max:  34 Mean: 0.470 RMS: 1.088 PSNR: 47.399 dB |
| `MEDIUM`    | Max:  35 Mean: 0.439 RMS: 1.061 PSNR: 47.620 dB |
| `HIGH`      | Max:  37 Mean: 0.898 RMS: 1.606 PSNR: 44.018 dB |
| `HIGHEST`   | Max:  51 Mean: 1.298 RMS: 2.478 PSNR: 40.249 dB |

### Rozmiary skompresowanych plików

Oryginalny plik ma rozmiar 1572882 bajtów.

| Preset      | Rozmiar pliku | Udział |
| ----------- | ------------- | ------ |
| `LOW`       | 357225        | 22.71 % |
| `MEDIUM`    | 365548        | 23.24 % |
| `HIGH`      | 277186        | 17.62 % |
| `HIGHEST`   | 254380        | 16.17 % |

### Jakość obrazu

Poniżej znajdują się obrazy wynikowe uzyskane z kodowania ASTC przy użyciu narzędzia `basisu`.

`LOW`
![low compression preset](images/texture_profiles/kodim03_pow2.fast.png)

`MEDIUM`
![medium compression preset](images/texture_profiles/kodim03_pow2.normal.png)

`HIGH`
![high compression preset](images/texture_profiles/kodim03_pow2.high.png)

`HIGHEST`
![best compression preset](images/texture_profiles/kodim03_pow2.best.png)
