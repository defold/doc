---
title: Samouczek Shadertoy w silniku Defold
brief: W tym samouczku przekonwertujesz shader z Shadertoy i uruchomisz go w silniku Defold.
---

# Samouczek Shadertoy

[Shadertoy.com](https://www.shadertoy.com/) to serwis gromadzący shadery GL tworzone przez użytkowników. To świetne źródło kodu shaderów i inspiracji. W tym samouczku weźmiemy shader z Shadertoy i uruchomimy go w silniku Defold. Zakładamy podstawową znajomość shaderów. Jeśli chcesz odświeżyć wiedzę, [instrukcja Shader](/manuals/shader/) to dobre miejsce na początek.

Użyjemy shadera [Star Nest](https://www.shadertoy.com/view/XlfGRj) autorstwa Pablo Andrioliego (użytkownik "Kali" na Shadertoy). To czysto proceduralny, matematyczny shader fragmentu, działający jak czarna magia i renderujący naprawdę efektowne gwiezdne pole.

![Star Nest](images/shadertoy/starnest.png)

Ten shader ma zaledwie 65 linii dość złożonego kodu GLSL, ale nie martw się. Potraktujemy go jak czarną skrzynkę, która wykonuje swoją pracę na podstawie kilku prostych danych wejściowych. Naszym zadaniem będzie zmodyfikowanie shadera tak, aby współpracował z Defold zamiast z Shadertoy.

## Potrzebujemy czegoś do oteksturowania

Shader Star Nest to czysty shader fragmentu, więc potrzebujemy tylko czegoś, co będzie teksturowane przez ten shader. Mamy kilka możliwości: sprite'a, mapę kafelków, GUI albo model. W tym samouczku użyjemy prostego modelu 3D. Powód jest prosty: dzięki temu łatwo zamienimy renderowanie modelu w pełnoekranowy efekt, co jest potrzebne na przykład do wizualnego post-processingu.

Zaczynamy od utworzenia kwadratowej siatki płaszczyzny w Blenderze (lub w dowolnym innym programie do modelowania 3D). Dla wygody cztery współrzędne wierzchołków znajdują się na -1 i 1 na osi X oraz na -1 i 1 na osi Y. Blender domyślnie ma oś Z skierowaną do góry, więc trzeba obrócić siatkę o 90° wokół osi X. Upewnij się też, że siatka ma poprawnie wygenerowane współrzędne UV. W Blenderze, mając zaznaczoną siatkę, wejdź do *Edit Mode*, a następnie wybierz <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>.


[Pobierz quad.dae](https://github.com/defold/template-basic-3d/blob/master/assets/meshes/quad.dae)


::: sidenote
Blender to darmowy, otwartoźródłowy program 3D, który można pobrać z [blender.org](https://www.blender.org).
:::

![quad w Blenderze](images/shadertoy/quad_blender.png)

1. Otwórz plik "main.collection" w projekcie Defold i utwórz nowy obiekt gry "star-nest".
2. Dodaj komponent *Model* do obiektu gry "star-nest".
3. Ustaw właściwość *Mesh* na plik *`quad.gltf`* znajdujący się w `builtins/assets/meshes`.
4. Model jest mały (2⨉2 jednostki), więc musimy przeskalować obiekt gry "star-nest" do sensownego rozmiaru. 600⨉600 to całkiem duży rozmiar, więc ustaw skalę X i Y na 300.

Model powinien pojawić się w edytorze sceny, ale renderuje się całkowicie na czarno. Dzieje się tak, ponieważ nie przypisano mu jeszcze materiału:

![quad w Defold](images/shadertoy/quad_no_material.png)

## Tworzenie materiału

Utwórz nowy plik materiału *`star-nest.material`*, program shadera wierzchołków *`star-nest.vp`* oraz program shadera fragmentu *`star-nest.fp`*:

1. Otwórz *star-nest.material*.
2. Ustaw właściwość *Vertex Program* na `star-nest.vp`.
3. Ustaw właściwość *Fragment Program* na `star-nest.fp`.
4. Dodaj *Vertex Constant* i nadaj mu nazwę "`view_proj`" (od "view projection").
5. Ustaw jego *Type* na `CONSTANT_TYPE_VIEWPROJ`.
6. Dodaj tag "`tile`" do *Tags*. Dzięki temu quad zostanie uwzględniony w przebiegu renderowania, gdy rysowane są sprite'y i kafelki.

    ![material](images/shadertoy/material.png)

7. Otwórz plik programu shadera wierzchołków *`star-nest.vp`*. Powinien zawierać poniższy kod. Zostaw go bez zmian.

    ```glsl
    // star-nest.vp
    uniform mediump mat4 view_proj;

    // positions are in world space
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

8. Otwórz plik programu shadera fragmentu *`star-nest.fp`* i zmodyfikuj kod tak, aby kolor fragmentu był ustawiany na podstawie składowych X i Y współrzędnych UV (`var_texcoord0`). Robimy to, żeby upewnić się, że model jest poprawnie skonfigurowany:

    ```glsl
    // star-nest.fp
    varying mediump vec2 var_texcoord0;

    void main()
    {
        gl_FragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

9. Ustaw materiał na komponencie modelu w obiekcie gry "star-nest".

Teraz edytor powinien renderować model z nowym shaderem i możemy wyraźnie zobaczyć, czy współrzędne UV są poprawne. Lewy dolny róg powinien mieć kolor czarny (0, 0, 0), lewy górny zielony (0, 1, 0), prawy górny żółty (1, 1, 0), a prawy dolny czerwony (1, 0, 0):

![quad w Defold](images/shadertoy/quad_material.png)

## Shader Star Nest

Teraz wszystko jest już gotowe, by zająć się właściwym kodem shadera. Najpierw spójrzmy na oryginalny kod. Składa się z kilku sekcji:

![Kod shadera Star Nest](images/shadertoy/starnest_code.png)

1. Linie 5--18 definiują zestaw stałych. Możemy zostawić je bez zmian.

2. Linie 21 i 63 zawierają wejściowe współrzędne tekstury fragmentu X i Y w przestrzeni ekranu (`in vec2 fragCoord`) oraz wyjściowy kolor fragmentu (`out vec4 fragColor`).

    W Defold wejściowe współrzędne tekstury są przekazywane z shadera wierzchołków jako współrzędne UV (w zakresie 0--1) przez zmienną varying `var_texcoord0`. Wyjściowy kolor fragmentu trafia do wbudowanej zmiennej `gl_FragColor`.

3. Linie 23--27 ustawiają wymiary tekstury, kierunek ruchu oraz przeskalowany czas. Rozdzielczość viewportu/tekstury jest przekazywana do shadera jako `uniform vec3 iResolution`. Shader oblicza współrzędne w stylu UV z poprawnymi proporcjami obrazu na podstawie współrzędnych fragmentu i rozdzielczości. Wykonywane jest też niewielkie przesunięcie, aby uzyskać przyjemniejsze kadrowanie.

    Wersja dla Defold musi zmienić te obliczenia tak, aby korzystały ze współrzędnych UV z `var_texcoord0`.

    Tutaj ustawiany jest też czas. Jest on przekazywany do shadera jako `uniform float iGlobalTime`. Defold obecnie nie obsługuje uniformów typu `float`, więc musimy przekazać czas przez `vec4`.

4. Linie 29--39 ustawiają obrót renderowania wolumetrycznego, a pozycja myszy wpływa na ten obrót. Współrzędne myszy są przekazywane do shadera jako `uniform vec4 iMouse`.

    W tym samouczku pominiemy wejście z myszy.

5. Linie 41--62 to główna część shadera. Ten kod możemy zostawić bez zmian.

## Zmodyfikowany shader Star Nest

Przejście przez powyższe sekcje i wprowadzenie niezbędnych zmian daje następujący kod shadera. Został on nieco uporządkowany, aby był czytelniejszy. Różnice między wersją dla Defold a wersją z Shadertoy są oznaczone poniżej:

```glsl
// Star Nest by Pablo Román Andrioli
// This content is under the MIT License.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

varying mediump vec2 var_texcoord0; // <1>

void main() // <2>
{
    // get coords and direction
    vec2 res = vec2(1.0, 1.0); // <3>
    vec2 uv = var_texcoord0.xy * res.xy - 0.5;
    vec3 dir = vec3(uv * zoom, 1.0);
    float time = 0.0; // <4>

    float a1=0.5; // <5>
    float a2=0.8;
    mat2 rot1=mat2(cos(a1),sin(a1),-sin(a1),cos(a1));
    mat2 rot2=mat2(cos(a2),sin(a2),-sin(a2),cos(a2));
    dir.xz*=rot1;
    dir.xy*=rot2;
    vec3 from = vec3(1.0, 0.5, 0.5);
    from += vec3(time * 2.0, time, -2.0);
    from.xz *= rot1;
    from.xy *= rot2;

    //volumetric rendering
    float s = 0.1, fade = 1.0;
    vec3 v = vec3(0.0);
    for(int r = 0; r < volsteps; r++) {
        vec3 p = from + s * dir * 0.5;
        // tiling fold
        p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));
        float pa, a = pa = 0.0;
        for (int i=0; i < iterations; i++) {
            // the magic formula
            p = abs(p) / dot(p, p) - formuparam;
            // absolute sum of average change
            a += abs(length(p) - pa);
            pa = length(p);
        }
        //dark matter
        float dm = max(0.0, darkmatter - a * a * 0.001);
        a *= a * a;
        // dark matter, don't render near
        if(r > 6) fade *= 1.0 - dm;
        v += fade;
        // coloring based on distance
        v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;
        fade *= distfading;
        s += stepsize;
    }
    // color adjust
    v = mix(vec3(length(v)), v, saturation);
    gl_FragColor = vec4(v * 0.01, 1.0); // <6>
}
```
1. Shader wierzchołków ustawia zmienną varying `var_texcoord0` z współrzędnymi UV. Musimy ją zadeklarować.
2. Shadertoy ma punkt wejścia `void mainImage(out vec4 fragColor, in vec2 fragCoord)`. W Defold funkcja `main()` nie przyjmuje żadnych parametrów. Zamiast tego odczytujemy zmienną varying `var_texcoord0` i zapisujemy wynik do `gl_FragColor`.
3. W tym samouczku przyjmujemy stałą rozdzielczość renderowania. Ponieważ model jest kwadratowy, możemy użyć `vec2 res = vec2(1.0, 1.0);`. Dla prostokątnego modelu o rozmiarze 1280⨉720 ustawilibyśmy `vec2 res = vec2(1.78, 1.0);` i pomnożyli współrzędne UV przez ten wektor, aby uzyskać poprawne proporcje obrazu.
4. Na razie `time` ma wartość zero. Dodamy czas w następnym kroku.
5. Uprościmy ten samouczek, usuwając całkowicie wartości `iMouse`. Zwróć uwagę, że nadal używamy obliczeń obrotu, aby zmniejszyć symetrię wizualną w renderowaniu wolumetrycznym.
6. Na końcu ustaw wynikowy kolor fragmentu.

Zapisz program shadera fragmentu. Model powinien teraz być ładnie oteksturowany gwiezdnym polem w edytorze sceny:

![quad with starnest](images/shadertoy/quad_starnest.png)


## Animacja

Ostatnim elementem układanki jest dodanie czasu, aby gwiazdy zaczęły się poruszać. Aby przekazać do shadera wartość czasu, musimy użyć stałej shadera, czyli uniformu. Aby skonfigurować nową stałą:

1. Otwórz *star-nest.material*.
2. Dodaj *Fragment Constant* i nadaj mu nazwę "time".
3. Ustaw jego *Type* na `CONSTANT_TYPE_USER`. Składowe x, y, z i w pozostaw na 0.

![time constant](images/shadertoy/time_constant.png)

Teraz musimy zmodyfikować kod shadera, aby zadeklarować nową stałą i z niej skorzystać:

```glsl
...
varying mediump vec2 var_texcoord0;
uniform lowp vec4 time; // <1>

void main()
{
    //get coords and direction
    vec2 res = vec2(2.0, 1.0);
    vec2 uv = var_texcoord0.xy * res.xy - 0.5;
    vec3 dir = vec3(uv * zoom, 1.0);
    float time = time.x * speed + 0.25; // <2>
    ...
```
1. Zadeklaruj nowy uniform typu `vec4` o nazwie "time". Wystarczy pozostawić go jako `lowp` (Low precision).
2. Odczytaj składową `x` uniformu czasu i użyj jej do obliczenia wartości czasu.

Ostatnim krokiem jest przekazanie wartości czasu do shadera:

1. Utwórz nowy plik skryptu *`star-nest.script`*.
2. Wpisz następujący kod:

```lua
function init(self)
    self.t = 0 -- <1>
end

function update(self, dt)
    self.t = self.t + dt -- <2>
    go.set("#model", "time", vmath.vector4(self.t, 0, 0, 0)) -- <3>
end
```
1. Przechowuj w komponencie skryptowym (`self`) wartość `t` i zainicjalizuj ją na 0.
2. W każdej klatce zwiększaj `self.t` o liczbę sekund, która upłynęła od poprzedniej klatki. Ta wartość jest dostępna w parametrze `dt` (delta time) i wynosi 1/60 (`update()` jest wywoływane 60 razy na sekundę).
3. Ustaw stałą "time" na komponencie modelu. Stała ma typ `vector4`, więc dla wartości czasu używamy składowej `x`.
4. Na koniec dodaj *star-nest.script* jako komponent skryptowy do obiektu gry "star-nest":

    ![script component](images/shadertoy/script_component.png)

I to wszystko! Gotowe.

Ciekawym ćwiczeniem rozwijającym byłoby dodanie do shadera oryginalnego ruchu myszy. Powinno być to dość proste, jeśli wiesz, jak obsługiwać wejście.

Miłego tworzenia w silniku Defold!
