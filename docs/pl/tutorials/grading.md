---
title: Samouczek shadera grading
brief: W tym samouczku utworzysz pełnoekranowy efekt post-processingu w Defold.
---

# Samouczek gradingu

W tym samouczku utworzymy pełnoekranowy efekt post-processingu do color gradingu. Podstawowa metoda renderowania użyta tutaj ma szerokie zastosowanie w różnych typach efektów post-processingu, takich jak blur, trails, glow, korekty kolorów i podobne.

Zakładamy, że swobodnie poruszasz się po edytorze Defold oraz masz podstawową wiedzę o shaderach GL i pipeline renderowania Defold. Jeśli chcesz uzupełnić wiedzę na te tematy, zajrzyj do [instrukcji Shader](/manuals/shader/) oraz [instrukcji Render](/manuals/render/).

## Render targety

Przy domyślnym skrypcie do renderowania (ang. render script) każdy komponent wizualny (sprite, mapa kafelków, efekt cząsteczkowy, GUI itd.) jest renderowany bezpośrednio do *frame buffer* karty graficznej. Następnie sprzęt powoduje wyświetlenie grafiki na ekranie. Faktyczne rysowanie pikseli komponentu wykonuje program GL typu *shader program*. Defold dostarcza domyślny program shaderów dla każdego typu komponentu, który rysuje dane pikseli na ekranie bez zmian. Zwykle właśnie takiego zachowania oczekujesz: obrazy powinny pojawiać się na ekranie tak, jak zostały pierwotnie przygotowane.

Możesz zastąpić program shaderów komponentu innym, który modyfikuje dane pikseli albo programowo tworzy zupełnie nowe kolory pikseli. [Samouczek Shadertoy](/tutorials/shadertoy) pokazuje, jak to zrobić.

Załóżmy teraz, że chcesz renderować całą grę w czerni i bieli. Jednym z możliwych rozwiązań jest zmodyfikowanie poszczególnych programów shaderów dla każdego typu komponentu tak, aby każdy shader desaturował kolory pikseli. Obecnie Defold dostarcza 6 wbudowanych materiałów i 6 par programów shaderów vertex/fragment, więc wymagałoby to sporo pracy. Co więcej, każdą kolejną zmianę lub dodanie efektu trzeba byłoby wprowadzać w każdym programie shaderów osobno.

Bardziej elastycznym podejściem jest podzielenie renderowania na dwa osobne kroki:

![Cel renderowania](images/grading/render_target.png)

1. Narysuj wszystkie komponenty jak zwykle, ale do bufora poza ekranem zamiast do zwykłego frame buffer. Robi się to przez rysowanie do czegoś, co nazywa się *render target*.
2. Narysuj kwadratowy wielokąt do frame buffer i użyj danych pikseli zapisanych w render target jako źródła tekstury dla tego wielokąta. Upewnij się też, że kwadratowy wielokąt jest rozciągnięty tak, aby pokrywał cały ekran.

Dzięki tej metodzie możemy odczytać wynikowe dane wizualne i zmodyfikować je, zanim trafią na ekran. Dodając programy shaderów do kroku 2 powyżej, możemy łatwo uzyskać pełnoekranowe efekty. Zobaczmy, jak skonfigurować to w Defold.

## Konfigurowanie własnego renderera

Musimy zmodyfikować wbudowany skrypt do renderowania i dodać nową funkcjonalność renderowania. Domyślny skrypt do renderowania to dobry punkt wyjścia, więc zacznij od skopiowania go:

1. Skopiuj */builtins/render/default.render_script*: w widoku *Asset* kliknij prawym przyciskiem myszy *default.render_script*, wybierz <kbd>Copy</kbd>, następnie kliknij prawym przyciskiem *main* i wybierz <kbd>Paste</kbd>. Kliknij prawym przyciskiem kopię, wybierz <kbd>Rename...</kbd> i nadaj jej odpowiednią nazwę, na przykład "grade.render_script".
2. Utwórz nowy plik renderowania o nazwie */main/grade.render*, klikając prawym przyciskiem *main* w widoku *Asset* i wybierając <kbd>New ▸ Render</kbd>.
3. Otwórz *grade.render* i ustaw jego właściwość *Script* na "/main/grade.render_script".

   ![Plik grade.render](images/grading/grade_render.png)

4. Otwórz *game.project* i ustaw *Render* na "/main/grade.render".

   ![Plik game.project](images/grading/game_project.png)

Gra jest teraz skonfigurowana do działania z nowym pipeline renderowania, który możemy modyfikować. Aby sprawdzić, czy silnik używa kopii twojego skryptu renderowania, uruchom grę, wprowadź do skryptu do renderowania zmianę dającą widoczny efekt, a następnie przeładuj skrypt. Możesz na przykład wyłączyć rysowanie kafelków i sprite'ów, a potem nacisnąć <kbd>⌘ + R</kbd>, aby szybko przeładować "uszkodzony" skrypt do renderowania w działającej grze:

```lua
...

render.set_projection(vmath.matrix4_orthographic(0, render.get_width(), 0, render.get_height(), -1, 1))

-- render.draw(self.tile_pred) -- <1>
render.draw(self.particle_pred)
render.draw_debug3d()

...
```
1. Zakomentuj rysowanie predykatu "tile", który obejmuje wszystkie sprite'y i kafelki. Tę linię kodu znajdziesz mniej więcej w okolicy linii 33 pliku skryptu do renderowania.

Jeśli po tym prostym teście sprite'y i kafelki znikną, wiesz już, że gra korzysta z twojego skryptu do renderowania. Jeśli wszystko działa zgodnie z oczekiwaniami, możesz cofnąć tę zmianę.

## Rysowanie do celu poza ekranem

Teraz zmodyfikujemy skrypt do renderowania tak, aby rysował do celu renderowania poza ekranem zamiast do frame buffer. Najpierw musimy utworzyć render target:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})

    self.clear_color = vmath.vector4(0, 0, 0, 0)
    self.clear_color.x = sys.get_config("render.clear_color_red", 0)
    self.clear_color.y = sys.get_config("render.clear_color_green", 0)
    self.clear_color.z = sys.get_config("render.clear_color_blue", 0)
    self.clear_color.w = sys.get_config("render.clear_color_alpha", 0)

    self.view = vmath.matrix4()

    local color_params = { format = render.FORMAT_RGBA,
                       width = render.get_width(),
                       height = render.get_height() } -- <1>
    local target_params = {[render.BUFFER_COLOR_BIT] = color_params }

    self.target = render.render_target("original", target_params) -- <2>
end
```
1. Skonfiguruj parametry bufora kolorów dla render target. Używamy docelowej rozdzielczości gry.
2. Utwórz render target z parametrami bufora kolorów.

Teraz wystarczy opakować oryginalny kod renderowania wywołaniem `render.set_render_target()` w taki sposób:

```lua
function update(self)
  render.set_render_target(self.target) -- <1>

  render.set_depth_mask(true)
  render.set_stencil_mask(0xff)
  render.clear({[render.BUFFER_COLOR_BIT] = self.clear_color, [render.BUFFER_DEPTH_BIT] = 1, [render.BUFFER_STENCIL_BIT] = 0})

  render.set_viewport(0, 0, render.get_width(), render.get_height()) -- <2>
  render.set_view(self.view)
  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT) -- <3>
end
```
1. Włącz render target. Od tej chwili każde wywołanie `render.draw()` będzie rysować do buforów naszego render target poza ekranem.
2. Cały oryginalny kod rysowania w `update()` pozostaje bez zmian, poza viewportem, który ustawiamy na rozdzielczość render target.
3. W tym momencie cała grafika gry została narysowana do render target. Czas więc go wyłączyć, ustawiając domyślny render target.

To wszystko, co musimy zrobić. Jeśli teraz uruchomisz grę, wszystko zostanie narysowane do render target. Ponieważ jednak nic nie rysujemy już do frame-buffer, zobaczysz tylko czarny ekran.

## Czymś trzeba wypełnić ekran

Aby narysować na ekranie piksele z bufora kolorów render target, musimy przygotować coś, co będzie można oteksturzyć tymi danymi pikseli. W tym celu użyjemy płaskiego, kwadratowego modelu 3D.

1. Otwórz *`main.collection`* i utwórz nowy obiekt gry o nazwie "`grade`".
2. Dodaj komponent Model do obiektu gry "`grade`".
3. Ustaw właściwość *Mesh* komponentu modelu na plik *`quad.gltf`* znajdujący się w `builtins/assets/meshes`.

Pozostaw obiekt gry nieskalowany w punkcie początkowym. Później, podczas renderowania quada, wykonamy projekcję tak, aby wypełniał cały ekran. Najpierw jednak potrzebujemy materiału i programów shaderów dla quada:

1. Utwórz nowy materiał i nazwij go *`grade.material`*, klikając prawym przyciskiem *main* w widoku *Asset* i wybierając <kbd>New ▸ Material</kbd>.
2. Utwórz program shaderów vertex o nazwie *`grade.vp`* oraz program shaderów fragment o nazwie *`grade.fp`*, klikając prawym przyciskiem *main* w widoku *Asset* i wybierając <kbd>New ▸ Vertex program</kbd> oraz <kbd>New ▸ Fragment program</kbd>.
3. Otwórz *grade.material* i ustaw właściwości *Vertex program* oraz *Fragment program* na nowe pliki programów shaderów.
4. Dodaj *Vertex constant* o nazwie "`view_proj`" i typie `CONSTANT_TYPE_VIEWPROJ`. To macierz widoku i projekcji używana w programie shaderów vertex dla wierzchołków quada.
5. Dodaj *Sampler* o nazwie "`original`". Będzie używany do próbkowania pikseli z bufora kolorów render target poza ekranem.
6. Dodaj *Tag* o nazwie "`grade`". W skrypcie do renderowania utworzymy nowy *render predicate* pasujący do tego tagu, aby narysować quada.

    ![Plik grade.material](images/grading/grade_material.png)

7. Otwórz *`main.collection`*, zaznacz komponent modelu w obiekcie gry "`grade`" i ustaw jego właściwość *Material* na "`/main/grade.material`".

   ![Właściwości modelu](images/grading/model_properties.png)

8. Program shaderów vertex można pozostawić w postaci utworzonej z bazowego szablonu:

    ```glsl
    // plik: grade.vp
    uniform mediump mat4 view_proj;

    // pozycje są w przestrzeni świata
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
      gl_Position = view_proj * vec4(position.xyz, 1.0);
      var_texcoord0 = texcoord0;
    }
    ```

9. W programie shaderów fragment zamiast ustawiać `gl_FragColor` bezpośrednio na próbkowaną wartość koloru wykonajmy prostą manipulację kolorem. Robimy to głównie po to, żeby upewnić się, że wszystko do tej pory działa zgodnie z oczekiwaniami:

    ```glsl
    // plik: grade.fp
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;

    void main()
    {
      vec4 color = texture2D(original, var_texcoord0.xy);
      // Desaturuj kolor próbkowany z oryginalnej tekstury
      float grey = color.r * 0.3 + color.g * 0.59 + color.b * 0.11;
      gl_FragColor = vec4(grey, grey, grey, 1.0);
    }
    ```

Mamy już model quada wraz z materiałem i shaderami. Pozostaje tylko narysować go do frame buffer ekranu.

## Teksturowanie buforem poza ekranem

Musimy dodać do skryptu do renderowania render predicate, aby móc narysować model quada. Otwórz *`grade.render_script`* i edytuj funkcję `init()`:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})
    self.grade_pred = render.predicate({"grade"}) -- <1>

    ...
end
```
1. Dodaj nowy predykat pasujący do tagu "grade", który ustawiliśmy w *`grade.material`*.

Po wypełnieniu bufora kolorów render target w `update()` ustawimy widok i projekcję tak, aby model quada wypełnił cały ekran. Następnie użyjemy bufora kolorów render target jako tekstury quada:

```lua
function update(self)
  render.set_render_target(self.target)

  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT)

  render.clear({[render.BUFFER_COLOR_BIT] = self.clear_color}) -- <1>

  render.set_viewport(0, 0, render.get_window_width(), render.get_window_height()) -- <2>
  render.set_view(vmath.matrix4()) -- <3>
  render.set_projection(vmath.matrix4())

  render.enable_texture(0, self.target, render.BUFFER_COLOR_BIT) -- <4>
  render.draw(self.grade_pred) -- <5>
  render.disable_texture(0, self.target) -- <6>
end
```
1. Wyczyść frame buffer. Zauważ, że poprzednie wywołanie `render.clear()` dotyczy render target, a nie ekranowego frame buffer.
2. Ustaw viewport zgodnie z rozmiarem okna.
3. Ustaw widok na macierz jednostkową. Oznacza to, że kamera znajduje się w punkcie początkowym i patrzy prosto wzdłuż osi Z. Ustaw także projekcję na macierz jednostkową, dzięki czemu quad zostanie rzutowany płasko na cały ekran.
4. Ustaw slot tekstury 0 na bufor kolorów render target. W *`grade.material`* mamy sampler "original" w slocie 0, więc shader fragment będzie próbkował z render target.
5. Narysuj utworzony przez nas predykat, pasujący do każdego materiału z tagiem "grade". Model quada używa *`grade.material`*, które ustawia ten tag, więc quad zostanie narysowany.
6. Po narysowaniu wyłącz slot tekstury 0, ponieważ nie jest już potrzebny.

Uruchommy teraz grę i zobaczmy wynik:

![Gra po desaturacji](images/grading/desaturated_game.png)

## Korekcja kolorów

Kolory są wyrażane jako wartości trzech składowych, z których każda określa ilość czerwieni, zieleni lub błękitu, z jakiej składa się dany kolor. Całe spektrum barw, od czerni przez czerwień, zieleń, błękit, żółć i róż aż po biel, można zmieścić w sześcianie:

![Sześcian kolorów](images/grading/color_cube.png)

Każdy kolor, który można wyświetlić na ekranie, znajduje się w tym sześcianie kolorów. Podstawowa idea color gradingu polega na użyciu takiego sześcianu kolorów, ale z przekształconymi kolorami, jako trójwymiarowej *lookup table*.

Dla każdego piksela:

1. Odszukaj pozycję jego koloru w sześcianie kolorów na podstawie wartości czerwieni, zieleni i błękitu.
2. *Odczytaj*, jaki kolor ma zapisany przekształcony sześcian w tym miejscu.
3. Narysuj piksel odczytanym kolorem zamiast kolorem oryginalnym.

Możemy to zrobić w shaderze fragment:

1. Próbkuj wartość koloru każdego piksela w buforze poza ekranem.
2. Odszukaj pozycję koloru próbkowanego piksela w sześcianie kolorów z color gradingiem.
3. Ustaw wyjściowy kolor fragmentu na odszukaną wartość.

![Korekcja kolorów na render target](images/grading/render_target_grading.png)

## Reprezentacja lookup table

Open GL ES 2.0 nie obsługuje tekstur 3D, więc musimy znaleźć inny sposób reprezentacji trójwymiarowego sześcianu kolorów. Powszechną metodą jest pocięcie sześcianu wzdłuż osi Z (blue) i ułożenie każdego wycinka obok siebie w dwuwymiarowej siatce. Każdy z 16 wycinków zawiera siatkę 16⨉16 pikseli. Zapisujemy to w teksturze, z której możemy odczytywać dane w shaderze fragment przy użyciu samplera:

![Tekstura LUT](images/grading/lut.png)

Powstała tekstura zawiera 16 komórek, po jednej dla każdej intensywności koloru blue, a wewnątrz każdej komórki 16 poziomów czerwieni wzdłuż osi X i 16 poziomów zieleni wzdłuż osi Y. Tekstura reprezentuje całą 16-milionową przestrzeń kolorów RGB za pomocą zaledwie 4096 kolorów, czyli tylko 4 bitów głębi koloru. Według większości standardów to bardzo słaby wynik, ale dzięki pewnej właściwości sprzętu graficznego GL możemy odzyskać bardzo wysoką dokładność kolorów. Zobaczmy jak.

## Odszukiwanie kolorów

Odszukanie koloru polega na sprawdzeniu składowej blue i określeniu, z której komórki pobrać wartości red i green. Wzór na znalezienie komórki zawierającej właściwy zestaw kolorów red-green jest prosty:

```math
cell = \left \lfloor{B \times (N - 1)} \right \rfloor
```

Tutaj `B` to wartość składowej blue z zakresu od 0 do 1, a `N` to całkowita liczba komórek. W naszym przypadku numer komórki będzie mieścił się w zakresie `0`--`15`, gdzie komórka `0` zawiera wszystkie kolory ze składową blue równą `0`, a komórka `15` wszystkie kolory ze składową blue równą `1`.

Na przykład wartość RGB `(0.63, 0.83, 0.4)` znajduje się w komórce zawierającej wszystkie kolory o wartości blue równej `0.4`, czyli w komórce numer 6. Znając to, obliczenie końcowych współrzędnych tekstury na podstawie wartości green i red jest proste:

![Tabela LUT](images/grading/lut_lookup.png)

Zwróć uwagę, że wartości red i green `(0, 0)` musimy traktować jako położone w *środku* lewego dolnego piksela, a wartości `(1.0, 1.0)` jako położone w *środku* prawego górnego piksela.

::: sidenote
Powód, dla którego odczyt rozpoczynamy od środka lewego dolnego piksela i kończymy na środku prawego górnego, jest taki, że nie chcemy, aby na próbkowaną wartość wpływały piksele spoza bieżącej komórki. Więcej na temat filtrowania poniżej.
:::

Gdy próbkujemy teksturę w tych konkretnych współrzędnych, okazuje się, że trafiamy dokładnie między 4 piksele. Jaką wartość koloru zwróci GL dla tego punktu?

![Filtrowanie tabeli LUT](images/grading/lut_filtering.png)

Odpowiedź zależy od tego, jak ustawiliśmy *filtering* samplera w materiale.

- Jeśli filtrowanie samplera ma wartość `NEAREST`, GL zwróci wartość koloru najbliższego piksela (pozycja zostanie zaokrąglona w dół). W powyższym przypadku GL zwróci wartość koloru z pozycji `(0.60, 0.80)`. Dla naszej 4-bitowej tekstury lookup oznacza to kwantyzację kolorów do łącznie tylko 4096 kolorów.

- Jeśli filtrowanie samplera ma wartość `LINEAR`, GL zwróci *interpolowaną* wartość koloru. GL zmiesza kolor na podstawie odległości od pikseli otaczających pozycję próbkowania. W powyższym przypadku GL zwróci kolor będący w 25% każdym z 4 pikseli wokół punktu próbkowania.

Używając filtrowania liniowego, eliminujemy więc kwantyzację kolorów i uzyskujemy bardzo dobrą precyzję kolorów z dość małej lookup table.

## Implementacja lookup

Zaimplementujmy lookup tekstury w shaderze fragment:

1. Otwórz *`grade.material`*.
2. Dodaj drugi sampler o nazwie "`lut`" (od lookup table).
3. Ustaw właściwość *`Filter min`* na `FILTER_MODE_MIN_LINEAR`, a właściwość *`Filter mag`* na `FILTER_MODE_MAG_LINEAR`.

    ![Sampler tabeli LUT](images/grading/material_lut_sampler.png)

4. Pobierz poniższą teksturę lookup table (*`lut16.png`*) i dodaj ją do projektu.

    ![16-kolorowa tabela LUT](images/grading/lut16.png)

5. Otwórz *`main.collection`* i ustaw właściwość tekstury *`lut`* na pobraną teksturę lookup.

    ![Tabela LUT dla modelu quada](images/grading/quad_lut.png)

6. Na koniec otwórz *`grade.fp`*, aby dodać obsługę lookup kolorów:

    ```glsl
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;
    uniform lowp sampler2D lut; // <1>

    #define MAXCOLOR 15.0 // <2>
    #define COLORS 16.0
    #define WIDTH 256.0
    #define HEIGHT 16.0

    void main()
    {
        vec4 px = texture2D(original, var_texcoord0.xy); // <3>

        float cell = floor(px.b * MAXCOLOR); // <4>

        float half_px_x = 0.5 / WIDTH; // <5>
        float half_px_y = 0.5 / HEIGHT;

        float x_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
        float y_offset = half_px_y + px.g * (MAXCOLOR / COLORS); // <6>

        vec2 lut_pos = vec2(cell / COLORS + x_offset, y_offset); // <7>

        vec4 graded_color = texture2D(lut, lut_pos); // <8>

        gl_FragColor = graded_color; // <9>
    }
    ```
    1. Zadeklaruj sampler `lut`.
    2. Stałe określające maksymalną wartość koloru (15, ponieważ zaczynamy od 0), liczbę kolorów na kanał oraz szerokość i wysokość tekstury lookup.
    3. Próbkuj kolor piksela (nazwany `px`) z oryginalnej tekstury, czyli bufora kolorów render target poza ekranem.
    4. Oblicz, z której komórki odczytać kolor na podstawie wartości kanału blue w `px`.
    5. Oblicz przesunięcia o połowę piksela, aby odczytywać ze środków pikseli.
    6. Oblicz przesunięcia X i Y na teksturze na podstawie wartości red i green w `px`.
    7. Oblicz końcową pozycję próbkowania w teksturze lookup.
    8. Próbkuj wynikowy kolor z tekstury lookup.
    9. Ustaw kolor tekstury quada na wynikowy kolor.

Obecnie tekstura lookup table po prostu zwraca te same wartości kolorów, które odszukujemy. Oznacza to, że gra powinna renderować się z oryginalną kolorystyką:

![Świat w oryginalnej kolorystyce](images/grading/world_original.png)

Jak dotąd wygląda na to, że wszystko zrobiliśmy poprawnie, ale pod powierzchnią kryje się problem. Zobacz, co się stanie, gdy dodamy sprite z testową teksturą gradientu:

![Pasmowanie kanału niebieskiego](images/grading/blue_banding.png)

Gradient blue pokazuje bardzo brzydkie pasmowanie. Skąd się to bierze?

## Interpolacja kanału blue

Problem z pasmowaniem w kanale blue polega na tym, że GL nie potrafi wykonać interpolacji kanału blue podczas odczytu koloru z tekstury. Z góry wybieramy konkretną komórkę do odczytu na podstawie wartości koloru blue i na tym koniec. Na przykład jeśli kanał blue zawiera wartość z zakresu `0.400`--`0.466`, to dokładna wartość nie ma znaczenia: zawsze pobierzemy końcowy kolor z komórki numer 6, gdzie kanał blue ma wartość `0.400`.

Aby uzyskać lepszą rozdzielczość kanału blue, możemy zaimplementować interpolację samodzielnie. Jeśli wartość blue znajduje się między wartościami dwóch sąsiednich komórek, możemy próbkować z obu tych komórek, a następnie zmieszać kolory. Na przykład jeśli wartość blue wynosi `0.420`, powinniśmy próbkować z komórki numer 6 *oraz* z komórki numer 7, a potem zmieszać kolory.

Powinniśmy więc odczytać z dwóch komórek:

```math
cell_{low} = \left \lfloor{B \times (N - 1)} \right \rfloor
```

oraz:

```math
cell_{high} = \left \lceil{B \times (N - 1)} \right \rceil
```

Następnie próbkujemy wartości kolorów z każdej z tych komórek i interpolujemy kolory liniowo według wzoru:

```math
color = color_{low} \times (1 - C_{frac}) + color_{high} \times C_{frac}
```

Tutaj `color`~low~ to kolor próbkowany z niższej (bardziej lewej) komórki, a `color`~high~ to kolor próbkowany z wyższej (bardziej prawej) komórki. Funkcja GLSL `mix()` wykonuje za nas tę interpolację liniową.

Wartość `C~frac~` powyżej to część ułamkowa wartości kanału blue przeskalowanej do zakresu kolorów `0`--`15`:

```math
C_{frac} = B \times (N - 1) - \left \lfloor{B \times (N - 1)} \right \rfloor
```

Ponownie, istnieje funkcja GLSL, która zwraca część ułamkową wartości. Nazywa się `fract()`. Końcowa implementacja w shaderze fragment (*`grade.fp`*) jest całkiem prosta:

```glsl
varying mediump vec4 position;
varying mediump vec2 var_texcoord0;

uniform lowp sampler2D original;
uniform lowp sampler2D lut;

#define MAXCOLOR 15.0
#define COLORS 16.0
#define WIDTH 256.0
#define HEIGHT 16.0

void main()
{
  vec4 px = texture2D(original, var_texcoord0.xy);

    float cell = px.b * MAXCOLOR;

    float cell_l = floor(cell); // <1>
    float cell_h = ceil(cell);

    float half_px_x = 0.5 / WIDTH;
    float half_px_y = 0.5 / HEIGHT;
    float r_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
    float g_offset = half_px_y + px.g * (MAXCOLOR / COLORS);

    vec2 lut_pos_l = vec2(cell_l / COLORS + r_offset, g_offset); // <2>
    vec2 lut_pos_h = vec2(cell_h / COLORS + r_offset, g_offset);

    vec4 graded_color_l = texture2D(lut, lut_pos_l); // <3>
    vec4 graded_color_h = texture2D(lut, lut_pos_h);

    // <4>
    vec4 graded_color = mix(graded_color_l, graded_color_h, fract(cell));

    gl_FragColor = graded_color;
}
```

1. Oblicz dwie sąsiednie komórki, z których trzeba odczytać dane.
2. Oblicz dwie osobne pozycje lookup, po jednej dla każdej komórki.
3. Próbkuj dwa kolory z pozycji odpowiadających komórkom.
3. Zmieszaj kolory liniowo zgodnie z częścią ułamkową `cell`, czyli przeskalowanej wartości koloru blue.

Ponowne uruchomienie gry z teksturą testową daje teraz znacznie lepsze rezultaty. Pasmowanie w kanale blue zniknęło:

![Kanał niebieski bez pasmowania](images/grading/blue_no_banding.png)

## Nadawanie gradingu teksturze lookup

Dobrze, wykonaliśmy sporo pracy po to, aby narysować coś, co wygląda dokładnie tak jak oryginalny świat gry. Jednak ta konfiguracja pozwala nam zrobić coś naprawdę fajnego. Uwaga!

1. Zrób zrzut ekranu gry w jej niezmienionej postaci.
2. Otwórz zrzut ekranu w swoim ulubionym programie do edycji obrazów.
3. Zastosuj dowolną liczbę korekt kolorów: brightness, contrast, color curves, white balance, exposure itd.

![Świat w Affinity](images/grading/world_graded_affinity.png)

4. Zastosuj te same korekty kolorów do pliku tekstury lookup table (*`lut16.png`*).
5. Zapisz teksturę lookup table po korekcie kolorów.
6. Zastąp teksturę *`lut16.png`* używaną w projekcie Defold wersją po korekcie kolorów.
7. Uruchom grę!

![Świat po gradingu](images/grading/world_graded.png)

Pięknie!
