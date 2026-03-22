---
title: Shader przewijania tekstury
brief: W tym samouczku nauczysz się używać shadera do przewijania powtarzającej się tekstury.
---

Autorstwo: Ten samouczek został przygotowany przez użytkownika forum MasterMind ([oryginalny wpis na forum](https://forum.defold.com/t/texture-scrolling-shader-tutorial-example/71553)).

# Samouczek o shaderze przewijania tekstury

Przewijanie tekstur za pomocą shadera to podstawowy element wielu efektów shaderowych. Zróbmy własny! Skorzystaj z [przykładowego projektu](https://github.com/FlexYourBrain/Texture_Scrolling_Example), aby przejść przez kolejne kroki i wypróbować go samodzielnie. Zastosowana metoda to przesuwanie współrzędnych UV przy użyciu stałej w shaderze.

Dostępne jest też [demo przykładowego projektu na itch.io](https://flexyourbrain.itch.io/texture-scrolling-in-defold) dla tych, którzy chcą zobaczyć efekt tego krótkiego samouczka/przewodnika:


## Konfiguracja

Projekt jest skonfigurowany w następujący sposób:

* Jedna podzielona na segmenty płaszczyzna 3D (.dae), która będzie służyć do wyświetlania przewijanej tekstury.
* Jeden komponent modelu z przypisanym plikiem płaszczyzny 3D (.dae).
* Dwa obrazy tekstur 64x64 (`water_bg.png` i `water_wave.png`), utworzone tak, aby łączyły się bez szwów, przypisane we właściwościach pliku .model.
* Jeden shader (Material + Vertex Program + Fragment Program) przypisany do modelu płaszczyzny.
* Jedna stała ustawiona w materiałach i shaderze.
* Jeden komponent skryptowy dołączony do obiektu gry modelu, aby uruchomić pętlę animacji.

![](images/texture-scrolling/model_setup.png)

_Uwaga: `water_bg` jest przypisany do slotu `tex0`, a `water_wave` do slotu `tex1`. Dwa sloty samplerów przypisano we właściwościach samplera materiału pokazanych poniżej._

![](images/texture-scrolling/material_setup.png)

_Obecnie `tex1` będzie teksturą przewijaną, więc `Wrap U` i `Wrap V` ustawiono na `Repeat`._

To podstawowa konfiguracja, a teraz możemy przejść do programów `water_scroll.vp` (vertex) i `water_scroll.fp` (fragment). Jak widać na obrazie powyżej, są one przypisane do materiału.


## Kod shadera

Dobrą praktyką jest unikanie wykonywania zbyt wielu obliczeń w programie fragmentów, jeśli można tego uniknąć, więc obliczamy przesunięcie UV w programie wierzchołków, zanim współrzędne zostaną przekazane do programu fragmentów. Tworzymy też stałą `animation_time` typu user w właściwościach stałej wierzchołkowej ustawionych w materiale (jak widać wyżej). Stała jest wektorem 4, ale używamy tylko pierwszej wartości. Jeśli oznaczymy ten wektor 4 jako `vector4(x,y,z,w)`, w shaderze użyjemy tylko wartości `x`, jak pokazano poniżej.


```glsl
// water_scroll.vp

// UV / Texture Scroll
attribute highp vec4 position;
attribute mediump vec2 texcoord0;

uniform mediump mat4 mtx_worldview;
uniform mediump mat4 mtx_proj;
uniform mediump vec4 animation_time; // vertex constant set up in material as type user.

varying mediump vec2 var_texcoord0; // setup var texcoord 0
varying mediump vec2 var_texcoord1; // setup var texcoord 1

void main()
{
    vec4 p = mtx_worldview * vec4(position.xyz, 1.0);
    var_texcoord0 = texcoord0;
    var_texcoord1 = vec2(texcoord0.x - animation_time.x, texcoord0.y); // Calculate var texcoord 1 uv offset on U(x) axis to fragment program 
    gl_Position = mtx_proj * p;
}
```

Model dostarcza atrybut `texcoord0`, czyli nasze współrzędne UV tekstury. Deklarujemy uniform `vec4` o nazwie `animation_time`, a także dwa varying `vec2`, `var_texcoord0` i `var_texcoord1`, które przekazujemy do programu fragmentów po przypisaniu im współrzędnych UV z atrybutu `texcoord0` w `void main()`. Jak widać, `var_texcoord1` jest inny, ponieważ przesuwamy go jeszcze przed wysłaniem do programu fragmentów. Używamy `vec2`, aby w razie potrzeby można było niezależnie operować na składowych x i y. W tym przypadku bierzemy tylko `texcoord0.x` i odejmujemy od niego naszą stałą `animation_time.x`, co po animacji spowoduje przesunięcie w ujemnym kierunku osi U (w lewo). `texcoord0.y` pozostawiamy bez zmian, aby zachować pozycję atrybutu.


```glsl
// water_scroll.fp

varying mediump vec2 var_texcoord0; // var texcoord 0 used with water_bg sampler
varying mediump vec2 var_texcoord1; // var texcoord 1 used with water_waves sampler, UV animation calulation done in vertex program

uniform lowp sampler2D tex0; // Material sampler slot 0 = water background / set in plane.model
uniform lowp sampler2D tex1; // Material sampler slot 1 = water waves / set in plane.model

void main()
{
    vec4 water_bg = texture2D(tex0, var_texcoord0.xy);
    vec4 water_waves = texture2D(tex1, var_texcoord1.xy);
    
    gl_FragColor = vec4(water_bg.rgb + water_waves.rgb ,1.0); // add texture waves to bg using addition(+), alpha set to 1.0 as there is no transparency being used0
}
```

Przechodząc do programu fragmentów, mamy prostą konfigurację. Dwa varying `vec2`, które przekazaliśmy z programu wierzchołków, to `var_textcoord0` i `var_texcoord1`, a następnie definiujemy uniformy dla tekstur samplera ustawionych w modelu i materiale, nazwane `tex0` i `tex1`. W `void main()` tworzymy wartości `vec4` dla próbkowanych tekstur przy użyciu `texture2d()`. Obrazy są w formacie kanałów RGBA (red, green, blue, alpha). Najpierw podajemy nazwę samplera, a potem współrzędne tekstury, których ma użyć. Jak widać na powyższym obrazie, `water_waves` ma przypisany `var_texcoord1`. To tekstura, którą animujemy/przewijamy, natomiast `var_texcoord0` przypisany do `water_bg` pozostawiamy bez zmian. Dla globalnej zastrzeżonej zmiennej `gl_FragColor` to tutaj przypisuje się kolory pikseli, w tym samym formacie `vec4(r,g,b,a)`. Chcemy połączyć dwie tekstury, więc używamy dodawania, aby zsumować składowe rgb każdej z nich. Nie używamy też kanału alpha tekstur, więc przypisujemy wartość typu float `1.0`, która oznacza pełną nieprzezroczystość.


## Skrypt animacji shadera

```lua
-- animate_shader.script
local animate = 1.0
-- local float will be used to set animation_time constant in scroll material , only x constant value is used in the shader 
-- so there is no need to create a vector 4

function init(self)
	go.animate("/scroll#plane", "animation_time.x", go.PLAYBACK_LOOP_FORWARD, animate, go.EASING_LINEAR, 4.0)
end
```

Istnieje więcej niż jeden sposób animowania wartości stałych. Możesz obliczać kroki delta time i aktualizować stałą tymi wartościami w skrypcie renderowania albo zwykłym skrypcie. W tym przypadku animujemy tylko jeden shader, więc jeśli chciałbyś mieć krok czasowy w kilku shaderach, obliczanie tego w `update()` mogłoby być lepsze. Użyjemy jednak `go.animate()`, ponieważ daje nam do dyspozycji wiele możliwości. Dzięki `go.animate()` możemy animować tylko wartość x naszej stałej, używając `animation_time.x`. Możemy też skorzystać z czasu trwania, opóźnienia i easing, jeśli chcemy. Możemy również ustawić odtwarzanie w pętli albo jednorazowe odtworzenie i anulować animację, jeśli zajdzie taka potrzeba. To wszystko bardzo przydaje się podczas animowania shaderów.

Lokalna zmienna `animate` typu float o wartości `1.0` jest wartością docelową, do której animujemy `animation_time.x`. W shaderach zazwyczaj pracujemy na znormalizowanych wartościach float od `0.0` do `1.0`. Zauważ, że domyślne wartości stałej `animation_time` w materiale to `(0,0,0,0)`, więc animujemy pierwszy zero od `0.0` do `1.0`. Oznacza to, że nasze przesunięte współrzędne UV będą animować się do krawędzi, a potem zapętlać w kółko, dokładnie tak jak chcemy!


## Następne kroki

Jako ćwiczenie możesz spróbować animować współrzędne tekstury `water_bg` w przeciwnym kierunku, tak jak w przykładowym demie!

Mam nadzieję, że to pomoże. Jeśli stworzysz coś, co się przewija, podziel się tym!

/ MasterMind
