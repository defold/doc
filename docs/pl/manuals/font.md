---
title: Fonty w silniku Defold
brief: Ta instrukcja opisuje, jak silnik Defold obsługuje fonty i jak wyświetlać tekst w grach.
---

# Pliki fontów

Fonty służą do renderowania tekstu w komponentach Label (Etykieta) oraz węzłach tekstowych GUI. Defold obsługuje kilka formatów plików fontów:

- TrueType
- OpenType
- BMFont

Fonty dodane do projektu są automatycznie konwertowane do formatu tekstury, który Defold potrafi renderować. Dostępne są dwie techniki renderowania fontów, a każda ma własne zalety i ograniczenia:

- Bitmap
- Distance field

## Fonty offline i runtime fonts

Domyślnie konwersja do zrasteryzowanych obrazów glifów odbywa się podczas budowania projektu, czyli offline. Wadą tego podejścia jest to, że każdy font musi wyrasteryzować wszystkie możliwe glify już na etapie buildu, co może prowadzić do powstawania bardzo dużych tekstur zużywających pamięć i zwiększających rozmiar bundla.

Jeśli używasz runtime fonts, pliki `.ttf` są dołączane do bundla bez zmian, a rasteryzacja odbywa się na żądanie podczas działania aplikacji. Dzięki temu zmniejsza się zarówno zużycie pamięci w runtime, jak i rozmiar bundla.

## Obsługa układu tekstu, na przykład right-to-left

Runtime fonts mają też tę zaletę, że obsługują pełny układ tekstu, na przykład right-to-left.
Obecnie wykorzystywane są biblioteki [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak) oraz [SkriBidi](https://github.com/memononen/Skribidi).

Zobacz [włączanie runtime fonts](/manuals/font#enabling-runtime-fonts).

## Kolekcja fontów

Format pliku `.fontc` jest też nazywany font collection (kolekcją fontów). W trybie offline powiązany jest z nim tylko jeden font.
Przy użyciu runtime fonts z kolekcją fontów możesz powiązać więcej niż jeden plik fontu `.ttf`.

Dzięki temu możesz używać kolekcji fontów podczas renderowania wielu tekstów w różnych językach i jednocześnie utrzymywać niskie zużycie pamięci.
Przykładowo możesz załadować kolekcję z japońskim fontem, skojarzyć ten font z bieżącym głównym fontem, a następnie zwolnić japońską kolekcję fontów.

## Tworzenie fontu

Aby utworzyć font do użycia w Defold, wybierz z menu <kbd>File ▸ New...</kbd>, a następnie <kbd>Font</kbd>. Możesz też <kbd>kliknąć prawym przyciskiem myszy</kbd> w wybranym miejscu panelu *Assets* i wybrać <kbd>New... ▸ Font</kbd>.

![New font name](images/font/new_font_name.png)

Nadaj nowemu plikowi nazwę i kliknij <kbd>Ok</kbd>. Nowy plik otworzy się teraz w edytorze.

![New font](images/font/new_font.png)

Przeciągnij font, którego chcesz użyć, do panelu *Assets* i upuść go w odpowiednim miejscu.

Ustaw właściwość *Font* na plik fontu i dostosuj pozostałe właściwości według potrzeb.

## Właściwości

*Font*
: Plik TTF, OTF albo *`.fnt`* używany do wygenerowania danych fontu.

*Material*
: Materiał używany do renderowania tego fontu. Pamiętaj, aby zmienić go dla Distance field i BMFonts. Szczegóły znajdziesz poniżej.

*Output Format*
: Typ generowanych danych fontu.

  - `TYPE_BITMAP` konwertuje zaimportowany plik OTF albo TTF na teksturę atlasu fontu, w której dane bitmapowe służą do renderowania tekstu. Kanały kolorów służą do kodowania kształtu znaku, obrysu i cienia. Dla plików *`.fnt`* źródłowa tekstura bitmapowa jest używana bez zmian.
  - `TYPE_DISTANCE_FIELD` konwertuje zaimportowany font do tekstury atlasu fontu, w której dane pikseli reprezentują nie piksele ekranu, lecz odległości od krawędzi glifu. Szczegóły znajdziesz poniżej.

*Render Mode*
: Tryb renderowania używany do renderowania glifów.

  - `MODE_SINGLE_LAYER` tworzy pojedynczy quad dla każdego znaku.
  - `MODE_MULTI_LAYER` tworzy osobne quady odpowiednio dla kształtu glifu, obrysu i cienia. Warstwy są renderowane od tyłu do przodu, co zapobiega zasłanianiu wcześniej wyrenderowanych znaków, jeśli obrys jest szerszy niż odstęp między glifami. Ten tryb renderowania umożliwia też poprawne przesuwanie cienia zgodnie z właściwościami Shadow X/Y w zasobie fontu.

*Size*
: Docelowy rozmiar glifów w pikselach.

*Antialias*
: Określa, czy font ma być wygładzany podczas wypalania na docelowej bitmapie. Ustaw 0, jeśli chcesz uzyskać pikselowo idealne renderowanie.

*Alpha*
: Przezroczystość glifu. Zakres 0.0-1.0, gdzie 0.0 oznacza pełną przezroczystość, a 1.0 pełną nieprzezroczystość.

*Outline Alpha*
: Przezroczystość wygenerowanego obrysu. Zakres 0.0-1.0.

*Outline Width*
: Szerokość wygenerowanego obrysu w pikselach. Ustaw 0, jeśli obrys nie jest potrzebny.

*Shadow Alpha*
: Przezroczystość wygenerowanego cienia. Zakres 0.0-1.0.

::: sidenote
Obsługa cienia jest włączona we wbudowanych shaderach materiałów fontów i działa zarówno w trybie renderowania jedno-, jak i wielowarstwowego. Jeśli nie potrzebujesz warstwowego renderowania fontów ani obsługi cienia, najlepiej użyć prostszego shadera, takiego jak *`builtins/font-singlelayer.fp`*.
:::

*Shadow Blur*
: Dla fontów bitmapowych to ustawienie określa, ile razy ma zostać zastosowane małe jądro rozmycia do każdego glifu. Dla Distance field ta wartość odpowiada rzeczywistej szerokości rozmycia w pikselach.

*Shadow X/Y*
: Poziome i pionowe przesunięcie wygenerowanego cienia w pikselach. To ustawienie wpływa na cień glifu tylko wtedy, gdy *Render Mode* ma wartość `MODE_MULTI_LAYER`.

*Characters*
: Określa, które znaki mają zostać uwzględnione w foncie. Domyślnie pole to zawiera drukowalne znaki ASCII o kodach 32-126. Możesz dodawać lub usuwać znaki, aby uwzględnić ich więcej albo mniej.

  Dla runtime fonts ten tekst działa też jako wstępne podgrzewanie pamięci podręcznej właściwymi glifami. Dzieje się to podczas ładowania. Zobacz `font.prewarm_text()`.

::: sidenote
Drukowalne znaki ASCII to:
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Po zaznaczeniu tej właściwości wszystkie glify dostępne w pliku źródłowym zostaną uwzględnione w wyniku.

*Cache Width/Height*
: Ogranicza rozmiar bitmapy pamięci podręcznej glifów. Gdy silnik renderuje tekst, wyszukuje glif w bitmapie cache. Jeśli go tam nie ma, glif zostaje dodany do cache przed renderowaniem. Jeśli bitmapa cache jest zbyt mała, aby pomieścić wszystkie glify, które silnik ma wyrenderować, zostanie zgłoszony błąd (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Jeśli ustawisz tę właściwość na 0, rozmiar cache jest dobierany automatycznie i może urosnąć maksymalnie do 2048x4096.

## Fonty typu Distance field

Fonty typu Distance field przechowują w teksturze odległość do krawędzi glifu zamiast danych bitmapowych. Gdy silnik renderuje taki font, potrzebny jest specjalny shader interpretujący dane odległości i wykorzystujący je do rysowania glifu. Fonty typu Distance field są bardziej zasobożerne niż fonty bitmapowe, ale zapewniają większą elastyczność skalowania.

![Distance field font](images/font/df_font.png)

Pamiętaj, aby przy tworzeniu fontu zmienić właściwość *Material* na *`builtins/fonts/font-df.material`* lub inny materiał obsługujący dane Distance field. W przeciwnym razie font nie będzie używał poprawnego shadera podczas renderowania na ekranie.

## Bitmap BMFonts

Oprócz generowanych bitmap Defold obsługuje także wstępnie przygotowane fonty bitmapowe w formacie BMFont. Taki font składa się z arkusza fontu PNG zawierającego wszystkie glify. Dodatkowo plik *`.fnt`* zawiera informacje o położeniu każdego glifu na arkuszu, a także o jego rozmiarze i kerningu. Pamiętaj, że Defold nie obsługuje wersji XML formatu *`.fnt`*, używanej przez Phaser i niektóre inne narzędzia.

Takie fonty nie przynoszą poprawy wydajności względem fontów bitmapowych generowanych z plików TrueType albo OpenType, ale mogą zawierać dowolną grafikę, kolorowanie i cienie bezpośrednio w obrazie.

Dodaj wygenerowane pliki *`.fnt`* i *`.png`* do projektu Defold. Pliki te muszą znajdować się w tym samym katalogu. Utwórz nowy plik fontu i ustaw właściwość *Font* na plik *`.fnt`*. Upewnij się, że *Output Format* ma wartość `TYPE_BITMAP`. Defold nie wygeneruje wtedy bitmapy, tylko użyje tej dostarczonej w PNG.

::: sidenote
Aby utworzyć BMFont, potrzebujesz narzędzia generującego odpowiednie pliki. Możesz użyć między innymi:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), narzędzia tylko dla Windows od AngelCode.
* [Shoebox](http://renderhjs.net/shoebox/), darmowej aplikacji opartej na Adobe Air dla Windows i macOS.
* [Hiero](https://libgdx.com/wiki/tools/hiero), narzędzia open source opartego na Java.
* [Glyph Designer](https://71squared.com/glyphdesigner), komercyjnego narzędzia dla macOS od 71 Squared.
* [bmGlyph](https://www.bmglyph.com), komercyjnego narzędzia dla macOS od Sovapps.
:::

![BMfont](images/font/bm_font.png)

Aby font renderował się poprawnie, pamiętaj o ustawieniu właściwości materiału na *`builtins/fonts/font-fnt.material`* podczas tworzenia fontu.

## Artefakty i najlepsze praktyki

Ogólnie fonty bitmapowe sprawdzają się najlepiej wtedy, gdy są renderowane bez skalowania. Są też szybsze w renderowaniu na ekranie niż fonty typu Distance field.

Fonty typu Distance field bardzo dobrze znoszą powiększanie. Fonty bitmapowe natomiast są po prostu obrazami pikselowymi, więc przy zwiększaniu rozmiaru piksele rosną razem z fontem, powodując widoczne blokowe artefakty. Poniżej znajduje się przykład fontu o rozmiarze 48 pikseli, powiększonego 4 razy.

![Fonts scaled up](images/font/scale_up.png)

Przy zmniejszaniu rozmiaru tekstury bitmapowe mogą być skutecznie i estetycznie skalowane w dół oraz wygładzane przez GPU. Font bitmapowy zachowuje też kolor lepiej niż font typu Distance field. Poniżej znajdziesz powiększenie tego samego przykładowego fontu o rozmiarze 48 pikseli, zmniejszonego do 1/5 oryginalnego rozmiaru:

![Fonts scaled down](images/font/scale_down.png)

Fonty typu Distance field muszą być renderowane do rozmiaru docelowego wystarczająco dużego, aby pomieścić informacje o odległości opisujące krzywizny glifów. Poniżej użyto tego samego fontu co wyżej, ale w rozmiarze 18 pikseli i powiększono go 10 razy. Wyraźnie widać, że ten rozmiar jest zbyt mały, by poprawnie zakodować kształty tego kroju pisma:

![Distance field artifacts](images/font/df_artifacts.png)

Jeśli nie potrzebujesz cienia ani obrysu, ustaw ich wartości alfa na zero. W przeciwnym razie dane cienia i obrysu nadal będą generowane, zajmując niepotrzebnie pamięć.

## Pamięć podręczna fontu

Zasób fontu w Defold daje w runtime dwie rzeczy: teksturę i dane fontu.

* Dane fontu składają się z listy wpisów glifów, z których każdy zawiera podstawowe informacje o kerningu oraz dane bitmapowe tego glifu.
* Tekstura jest wewnętrznie nazywana glyph cache texture (teksturą pamięci podręcznej glifów) i jest używana podczas renderowania tekstu dla konkretnego fontu.

Podczas renderowania tekstu w runtime silnik najpierw przechodzi po glifach, które mają zostać wyrenderowane, i sprawdza, które z nich są dostępne w pamięci podręcznej tekstury. Każdy brakujący glif powoduje przesłanie do tekstury danych bitmapowych przechowywanych w danych fontu.

Każdy glif jest wewnętrznie umieszczany w cache zgodnie z linią bazową fontu, co umożliwia obliczanie lokalnych współrzędnych tekstury glifu w odpowiadającej mu komórce cache bezpośrednio w shaderze. Dzięki temu można uzyskać dynamiczne efekty tekstowe, takie jak gradienty albo nakładki tekstur. Silnik udostępnia shaderowi metryki cache przez specjalną stałą shadera `texture_size_recip`, która zawiera następujące informacje w komponentach wektora:

* `texture_size_recip.x` to odwrotność szerokości cache
* `texture_size_recip.y` to odwrotność wysokości cache
* `texture_size_recip.z` to stosunek szerokości komórki cache do szerokości całego cache
* `texture_size_recip.w` to stosunek wysokości komórki cache do wysokości całego cache

Na przykład, aby wygenerować gradient w shaderze fragmentu, wystarczy zapisać:

`float horizontal_gradient = fract(var_texcoord0.y / texture_size_recip.w);`

Więcej informacji o uniformach shaderów znajdziesz w [instrukcji do shaderów](/manuals/shader).

## Włączanie runtime fonts

Można używać generowania w runtime dla fontów typu SDF, gdy korzystasz z fontów TrueType (`.ttf`).
Takie podejście może znacząco zmniejszyć rozmiar pobieranych danych i zużycie pamięci w runtime w grze Defold.
Niewielką wadą jest asynchroniczny charakter generowania każdego glifu.

* Włącz tę funkcję, ustawiając `font.runtime_generation` w `game.project`.

* Dodaj [App Manifest](/manuals/app-manifest) i włącz opcję `Use full text layout system`.
  Spowoduje to zbudowanie niestandardowego silnika z włączoną obsługą tej funkcji.

::: sidenote
Ta funkcja jest obecnie eksperymentalna, ale docelowo ma stać się domyślnym sposobem pracy.
:::

::: important
Ustawienie `font.runtime_generation` wpływa na wszystkie fonty `.ttf` w projekcie.
:::

### Skryptowanie fontów

#### Wstępne podgrzewanie cache glifów

Aby ułatwić pracę z runtime fonts, obsługują one wstępne podgrzewanie cache glifów.
Oznacza to, że font wygeneruje glify wypisane w polu *Characters*.

::: sidenote
Jeśli zaznaczone jest `All Chars`, podgrzewanie wstępne nie zostanie wykonane, ponieważ niweczyłoby to korzyść z niewymuszania generowania wszystkich glifów naraz.
:::

Jeśli pole `Characters` w pliku `.fontc` jest ustawione, jego zawartość służy jako tekst do ustalenia, które glify trzeba dodać do cache.

Możesz też ręcznie zaktualizować cache glifów, wywołując `font.prewarm_text(font_collection, text, callback)`. Funkcja przyjmuje callback informujący, że wszystkie brakujące glify zostały dodane do cache i można bezpiecznie wyświetlić tekst na ekranie.

### Dodawanie i usuwanie fontów z kolekcji fontów

Dla runtime fonts można dodawać lub usuwać fonty (`.ttf`) z font collection.
Jest to przydatne, gdy duży font został podzielony na kilka plików dla różnych zestawów znaków, na przykład CJK.

::: important
Dodanie fontu do font collection nie powoduje automatycznego załadowania ani wyrenderowania wszystkich glifów.
:::

```lua
-- pobierz główny font
local font_collection = go.get("#label", "font")
font.add_font(font_collection, self.language_ttf_hash)

-- pobierz font wybranego języka
local font_collection_language = go.get("localization_japanese#label", "font")
local font_info = font.get_info(font_collection_language)
self.language_ttf_hash = font_info.fonts[1].path_hash -- pobierz pierwszy font (ten wskazany w edytorze)
font.add_font(self.font_collection, self.language_ttf_hash) -- zwiększa licznik referencji fontu
```

```lua
-- usuń referencję do fontu
font.add_font(self.font_collection, self.language_ttf_hash)
```

### Wstępne podgrzewanie glifów

Aby poprawnie wyświetlić tekst przy użyciu runtime font, glify muszą zostać rozwiązane. `font.prewarm_text()` robi to za ciebie.
Jest to operacja asynchroniczna. Gdy się zakończy i otrzymasz callback, możesz bezpiecznie przejść do wyświetlenia dowolnej wiadomości zawierającej te glify.

::: important
Jeśli cache glifów się zapełni, najstarszy glif zostanie z niego usunięty.
:::

```lua
font.prewarm_text(self.font_collection, info.text, function (self, request_id, result, err)
    if result then
      print("PREWARMING OK!")
      label.set_text(self.label, info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
