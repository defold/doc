---
title: Samouczek Shadertoy w silniku Defold
brief: W tym samouczku przekonwertujesz shader z Shadertoy i uruchomisz go w silniku Defold.
---

# Samouczek Shadertoy

[Shadertoy.com](https://www.shadertoy.com/) to serwis gromadzący shadery GL tworzone przez użytkowników. To świetne źródło kodu shaderów i inspiracji. W tym samouczku weźmiemy shader z Shadertoy i uruchomimy go w silniku Defold. Zakładamy podstawową znajomość shaderów. Jeśli chcesz odświeżyć wiedzę, [instrukcja Shader](/manuals/shader/) to dobre miejsce na początek.

Użyjemy shadera [Star Nest](https://www.shadertoy.com/view/XlfGRj) autorstwa Pablo Andrioliego (użytkownik "Kali" na Shadertoy). To czysto proceduralny, matematyczny shader fragmentu, działający jak czarna magia i renderujący naprawdę efektowne gwiezdne pole.

![Star Nest](../images/shadertoy/starnest.png)

Ten shader ma zaledwie 65 linii dość złożonego kodu GLSL, ale nie martw się. Potraktujemy go jak czarną skrzynkę, która wykonuje swoją pracę na podstawie kilku prostych danych wejściowych. Naszym zadaniem będzie zmodyfikowanie shadera tak, aby współpracował z Defold zamiast z Shadertoy.

## Potrzebujemy czegoś do oteksturowania

Shader Star Nest to czysty shader fragmentu, więc potrzebujemy tylko czegoś, co będzie teksturowane przez ten shader. Mamy kilka możliwości: sprite'a, mapę kafelków, GUI albo model. W tym samouczku użyjemy prostego modelu 3D. Powód jest prosty: dzięki temu łatwo zamienimy renderowanie modelu w pełnoekranowy efekt, co jest potrzebne na przykład do wizualnego post-processingu.

Możemy zacząć od pustego projektu.

1. Otwórz Defold i wybierz Create From *Templates*.
2. Wybierz *Empty Project*.
3. Ustaw *Title* i wybierz *Location* na dysku.
4. Kliknij <kbd>Create New Project</kbd>.

![start](../images/shadertoy/empty_project.png)

Możesz użyć wbudowanej siatki `quad.gltf` z `builtins/assets/meshes`.

Opcjonalnie możesz też utworzyć kwadratową siatkę płaszczyzny w Blenderze lub dowolnym innym programie do modelowania 3D --- dla wygody cztery współrzędne wierzchołków znajdują się na -1 i 1 na osi X oraz na -1 i 1 na osi Y. Blender domyślnie ma oś Z skierowaną do góry, więc trzeba obrócić siatkę o 90° wokół osi X. Upewnij się też, że siatka ma poprawnie wygenerowane współrzędne UV. W Blenderze, mając zaznaczoną siatkę, wejdź do *Edit Mode*, a następnie wybierz <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>.

<div class='sidenote' markdown='1'>
Blender to darmowy, otwartoźródłowy program 3D, który można pobrać z [blender.org](https://www.blender.org).
</div>

![Kwadratowa siatka w Blenderze](../images/shadertoy/quad_blender.png)

1. Otwórz plik "main.collection" w projekcie Defold i utwórz nowy obiekt gry "star-nest".
2. Dodaj komponent *Model* do obiektu gry "star-nest".
3. Ustaw właściwość *Mesh* na nasz `quad.gltf`.
4. Musimy ustawić materiał dla modelu, więc na razie wybierz wbudowany `model.material`.

Model powinien pojawić się w edytorze sceny, ale renderuje się całkowicie na czarno. Dzieje się tak, ponieważ nie ma jeszcze ustawionej tekstury:

![Kwadrat w Defold](../images/shadertoy/quad_default_material.png)

## Tworzenie materiału

1. Utwórz nowy plik materiału *`star-nest.material`*, klikając <kbd>Right Mouse Button</kbd> folder `main` w panelu `Assets`, wybierając <kbd>New</kbd>-><kbd>Material</kbd> i nadając mu nazwę `star-nest`.

 ![Materiał](../images/shadertoy/new_material.png)

2. W ten sam sposób utwórz vertex shader program `star-nest.vp` oraz fragment shader program `star-nest.fp`:
3. Otwórz *star-nest.material*.
4. Ustaw *Vertex Program* na `star-nest.vp`.
5. Ustaw *Fragment Program* na `star-nest.fp`.
6. Dodaj *Vertex Constant* i nadaj mu nazwę "`view_proj`" typu `Viewproj` (od "view projection").
8. Dodaj tag "tile" do *Tags*. Dzięki temu quad zostanie uwzględniony w przebiegu renderowania, gdy rysowane są sprites i tiles.

 ![Materiał](../images/shadertoy/material.png)

### Program wierzchołków

1. Otwórz plik vertex shader program `star-nest.vp`. Powinien zawierać poniższy kod:

    ```glsl
    #version 140

    // positions are in world space
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### Program fragmentów

1. Otwórz plik fragment shader program `star-nest.fp` i zmodyfikuj kod tak, aby kolor fragmentu był ustawiany na podstawie składowych X i Y współrzędnych UV (`var_texcoord0`). Robimy to, żeby upewnić się, że model jest poprawnie skonfigurowany:

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. Ustaw właściwość `Material` na nowo utworzony materiał `star-nest` w komponencie modelu obiektu gry `star-nest` w `main.collection`.

Teraz edytor powinien renderować model z nowym shaderem i możemy wyraźnie zobaczyć, czy współrzędne UV są poprawne. Lewy dolny róg powinien mieć kolor czarny (0, 0, 0), lewy górny zielony (0, 1, 0), prawy górny żółty (1, 1, 0), a prawy dolny czerwony (1, 0, 0):

![Kwadrat w Defold](../images/shadertoy/quad_material.png)

## Kamera

Możemy teraz uruchomić projekt (<kbd>Project</kbd>-><kbd>Build</kbd> albo skrótem <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>), ale zobaczymy czarny ekran (no, prawie, może poza jednym małym pikselem w lewym dolnym rogu). Dzieje się tak, ponieważ nie ma kamery, a domyślny skrypt renderowania używa prostego fallbacku, który pokazuje ogromną przestrzeń 2D, podczas gdy nasz model znajduje się w pozycji (0,0,0) i ma szerokość tylko 1.

Dodajmy obiekt gry z komponentem kamery, aby określić, co zobaczymy w grze.

1. Dodaj obiekt gry o nazwie `camera` z pozycją (0,0,1). (Ważne jest ustawienie współrzędnej Z na 1, aby ten obiekt gry znajdował się przed naszym modelem, ponieważ w domyślnej konfiguracji 2D oś Z jest teraz skierowana w naszą stronę).
2. Dodaj komponent `Camera`, a zobaczysz podgląd kamery z naszym quadem w środku. Przy domyślnych właściwościach mamy szczęście, że w takim ustawieniu nie trzeba nic zmieniać i powinniśmy już widzieć poprawny wynik, poza jedną rzeczą - nie potrzebujemy tak dużego view frustum kamery, więc możemy zmniejszyć `Far Z` do `2`.

![kamera](../images/shadertoy/camera.png)

Opcjonalnie możemy zmienić typ kamery, ustawiając `Orthographic Projection` na `true`, a następnie dostosować `Orthographic Zoom` do wartości około 600, ale w tym przypadku nie będziemy mieć automatycznych proporcji obrazu, więc model nie wypełni ekranu.

## Shader Star Nest

Teraz wszystko jest już gotowe, by zająć się właściwym kodem shadera. Najpierw spójrzmy na oryginalny kod. Składa się z kilku sekcji:

![Kod shadera Star Nest](../images/shadertoy/starnest_code.png)

Będziemy używać nowoczesnego pipeline z GLSL w wersji 140 - w tym celu zadeklarujemy wersję na początku pliku za pomocą `#version 140`.

1. Linie 5--18 definiują zestaw stałych. Możemy zostawić je bez zmian. Są to zwykłe stałe GLSL i nie zależą konkretnie od Shadertoy ani Defold.

2. Linie 21 i 63 zawierają wejściowe współrzędne tekstury fragmentu X i Y w przestrzeni ekranu (`in vec2 fragCoord`) oraz wyjściowy kolor fragmentu (`out vec4 fragColor`).

    Defold przekazuje współrzędne tekstury z shadera wierzchołków do shadera fragmentów przez interpolowaną zmienną jako współrzędne UV (w zakresie 0--1). W naszym shaderze wierzchołków jest ona zadeklarowana kwalifikatorem `out`:

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     W shaderze fragmentów ta sama wartość jest odbierana z kwalifikatorem `in`:

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    Następnie w GLSL 140 deklarujemy jawne wyjście fragmentu z kwalifikatorem `out`:

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    Tam więc, gdzie oryginalny kod Shadertoy zapisuje do `fragColor`, nasz shader Defold zapisuje do `out_fragColor`.

3. Linie 23--27 ustawiają wymiary tekstury, kierunek ruchu oraz przeskalowany czas. W Shadertoy shader otrzymuje pozycję piksela przez `fragCoord`, a rozdzielczość viewportu/tekstury jest przekazywana do shadera jako `uniform vec3 iResolution`. Shader oblicza współrzędne w stylu UV z poprawnymi proporcjami obrazu na podstawie współrzędnych fragmentu i rozdzielczości. Wykonywane jest też niewielkie przesunięcie, aby uzyskać przyjemniejsze kadrowanie.

    W Defold nie zaczynamy od współrzędnych pikseli. Zamiast tego otrzymujemy już znormalizowane współrzędne UV z shadera wierzchołków przez `var_texcoord0`. Te współrzędne mieszczą się w zakresie od `0.0` do `1.0` na całym renderowanym quadzie.

    Wersja dla Defold musi zmienić te obliczenia tak, aby korzystały ze współrzędnych UV z `var_texcoord0`.
    Typowa konwersja wygląda tak:

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    Dokładna wartość `aspect` zależy od konfiguracji przykładu. Jeśli efekt jest renderowany na pełnoekranowym quadzie o znanym rozmiarze wyświetlania, proporcje obrazu można zahardkodować na potrzeby samouczka. Jeśli efekt ma obsługiwać dowolne rozmiary okna, przekaż rozdzielczość jako fragment constant i umieść ją w uniform block GLSL 140.

    Tutaj ustawiany jest też czas. Jest on przekazywany do shadera jako `uniform float iGlobalTime`. Defold (od wersji 1.12.3) udostępnia czas shaderom przez specjalną stałą `Time`, której użyjemy.

    W nowoczesnym Defold uniformy non-opaque deklaruje się wewnątrz uniform blocks.
    W shaderze fragmentów deklarujemy ją tak:

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    Następnie w `star-nest.material` dodamy Fragment Constant o nazwie `time` i ustawimy jej typ na `Time`.

    Wartości można wtedy użyć tak:

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    gdzie `time.x` to czas od startu silnika, a `time.y` to delta time z poprzedniej klatki.

4. Linie 29--39 ustawiają obrót renderowania wolumetrycznego, a pozycja myszy wpływa na ten obrót. Współrzędne myszy są przekazywane do shadera jako `uniform vec4 iMouse`.

    W tym samouczku pominiemy wejście z myszy.

5. Linie 41--62 to główna część shadera. Ten kod możemy zostawić bez zmian.

## Zmodyfikowany shader Star Nest

Przejście przez powyższe sekcje i wprowadzenie niezbędnych zmian daje następujący kod shadera. Został on nieco uporządkowany, aby był czytelniejszy. Różnice między wersją dla Defold a wersją z Shadertoy są oznaczone poniżej:

```glsl
#version 140 // <1>

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

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// get coords and direction
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// volumetric rendering
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// tiling fold
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// the magic formula
			p = abs(p) / dot(p, p) - formuparam;

			// absolute sum of average change
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// dark matter
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// dark matter, don't render near
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// coloring based on distance
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// color adjust
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```
1. Deklarujemy #version 140 na początku pliku, aby używać nowoczesnego pipeline GLSL w Defold. Następnie zostawiamy defines bez zmian.
2. Shader wierzchołków przekazuje współrzędne UV do shadera fragmentów przez var_texcoord0. W GLSL 140 shader fragmentów odbiera tę interpolowaną wartość z kwalifikatorem in.
3. W GLSL 140 shader fragmentów powinien zadeklarować jawną zmienną wyjściową zamiast zapisywać do gl_FragColor. Tutaj używamy out vec4 out_fragColor.
4. Stała materiału Time z Defold jest udostępniana shaderowi przez uniform block. W star-nest.material dodaj Fragment Constant o nazwie time i ustaw jej typ na Time.
5. Shadertoy używa mainImage(out vec4 fragColor, in vec2 fragCoord). W Defold używamy zwykłego punktu wejścia void main(), odczytujemy interpolowane współrzędne UV z var_texcoord0 i zapisujemy finalny kolor do out_fragColor.
6. W tym samouczku definiujemy statyczną wartość resolution/aspect dla renderowania. Obecnie model jest kwadratowy, więc możemy użyć `vec2 res = vec2(1.0, 1.0);`. Dla prostokątnego modelu o rozmiarze 1280×720 moglibyśmy zamiast tego użyć `vec2 res = vec2(1.78, 1.0);` i pomnożyć przez to współrzędne UV, aby zachować poprawne proporcje obrazu.
7. Oryginalny shader Shadertoy używa iGlobalTime. W tej wersji dla Defold time.x zawiera czas od startu silnika, więc przypisujemy go do lokalnej zmiennej iGlobalTime i używamy do animowania ruchu kamery przez gwiezdne pole.
8. Uprościmy ten samouczek, usuwając całkowicie wartości iMouse. Sam obrót pozostaje, ponieważ zmniejsza symetrię wizualną w renderowaniu wolumetrycznym.
9. Na końcu shader zapisuje wynikowy kolor fragmentu do out_fragColor.

Zapisz program shadera fragmentów. Model powinien teraz być ładnie oteksturowany gwiezdnym polem w edytorze sceny i w czasie działania:

![Quad z efektem Star Nest](../images/shadertoy/quad_starnest.png)


## Animacja {#animation}

Ostatnim elementem układanki jest wprowadzenie czasu, aby gwiazdy zaczęły się poruszać. Defold (od wersji 1.12.3) udostępnia go automatycznie przez fragment constant typu `Time`.

1. Otwórz *star-nest.material*.
2. Dodaj *Fragment Constant* i nadaj mu nazwę "time".
3. Ustaw jego *Type* na `Time`.

![Stała time](../images/shadertoy/time_constant.png)

I to wszystko! Obsługujemy już ten `time` w shaderze fragmentów. Gotowe.

## Ćwiczenia

Ciekawym ćwiczeniem rozwijającym jest dodanie do shadera oryginalnego wejścia ruchu myszy. Musisz utworzyć nową Fragment Constant, tym razem typu `User`, i aktualizować ją w `on_input` w skrypcie wykrywającym ruch myszy za pomocą funkcji `go.set()` oraz ustawiającym współrzędne wejściowe w nowej stałej.

Miłego tworzenia w silniku Defold!
