---
title: Komponent Light w Defold
brief: Ta instrukcja wyjaśnia, jak używać światła otoczenia, kierunkowego, punktowego i reflektorowego oraz jak uzyskiwać dostęp do danych świateł w shaderach.
---

# Komponent Light

Komponent Light reprezentuje źródło światła w kolekcji. Silnik Defold obsługuje obecnie cztery typy zasobów świateł:

- Światło otoczenia (`.ambient_light`)
- Światło kierunkowe (`.directional_light`)
- Światło punktowe (`.point_light`)
- Światło reflektorowe (`.spot_light`)

Zasoby świateł dodaje się do obiektów gry tak samo jak inne zasoby komponentów. Komponenty Light można tworzyć bezpośrednio w obiekcie gry albo utworzyć zasób światła w przeglądarce *Assets*, a następnie dodać go jako komponent do obiektu gry w widoku *Outline*.

Silnik Defold nie stosuje oświetlenia automatycznie do każdego materiału. Silnik zbiera światła i udostępnia je shaderom przez wbudowany bufor świateł. To shader materiału decyduje, jak wykorzystać dane świateł.

Poniższe przykłady używają tej samej sceny, aby pokazać wpływ różnych typów świateł na wynik końcowy:

![Scena bez świateł](images/light/no_light.png)

## Właściwości świateł

Wszystkie kolory świateł są wartościami RGB. Kanał alfa nie jest używany przez zasoby świateł.

### Światło otoczenia

Światła otoczenia dodają do sceny stałe oświetlenie. Nie wpływa na nie pozycja, obrót ani skala obiektu gry. Można ich używać na przykład jako ogólnego oświetlenia tła albo do nadania obiektom wyglądu bez cieniowania.

Komponent światła otoczenia jest przedstawiany w edytorze ikoną ze strzałkami skierowanymi ku środkowi. Kolor ikony jest taki sam jak wartość właściwości `color`.

![Światło otoczenia o mniejszej intensywności](images/light/ambient_light_less_intensity.png)

Właściwości:

`color`
: Kolor RGB światła otoczenia.

`intensity`
: Mnoży kolor światła otoczenia.

![Światło otoczenia o większej intensywności](images/light/ambient_light_full_intensity.png)

Światła otoczenia są sumowane w buforze świateł shadera do pojedynczego koloru otoczenia `light_info.xyz`. Nie zajmują pozycji w tablicy `lights[]`. Wiele komponentów światła otoczenia w scenie daje tylko jeden kolor wynikowy, będący połączeniem kolorów wszystkich tych komponentów.

### Światło kierunkowe

Światła kierunkowe reprezentują światło padające z jednego kierunku, na przykład światło słoneczne. Nie wykorzystują pozycji ani skali obiektu gry, ale kierunek światła jest wyznaczany na podstawie obrotu obiektu gry w przestrzeni świata, zastosowanego do lokalnego kierunku do przodu `(0, 0, -1)`.

Komponent światła kierunkowego jest przedstawiany w edytorze kolorową ikoną słońca z trójwymiarową strzałką wskazującą jego kierunek.

![Światło kierunkowe](images/light/directional_light.png)

Właściwości:

`color`
: Kolor RGB światła kierunkowego.

`intensity`
: Mnoży kolor światła kierunkowego.


Światła kierunkowe często łączy się ze światłem otoczenia, aby powierzchnie odwrócone od światła kierunkowego nie stawały się całkowicie ciemne.

![Światło kierunkowe i światło otoczenia](images/light/directional_and_ambient_light.png)

### Światło punktowe

Światła punktowe emitują światło na zewnątrz z pozycji obiektu gry w przestrzeni świata. Pozycja światła punktowego pochodzi z pozycji obiektu gry w przestrzeni świata.

Komponent światła punktowego jest przedstawiany w edytorze punktem z rozchodzącymi się wokół niego promieniami. Jego kolor odpowiada właściwości `color`, a okrąg przedstawia `range`.

![Światło punktowe](images/light/point_light.png)

Właściwości:

`color`
: Kolor RGB światła punktowego.

`intensity`
: Mnoży kolor światła punktowego.

`range`
: Promień światła w jednostkach świata.

Efektywny zasięg jest mnożony przez najmniejszą z wartości bezwzględnych składowych skali obiektu gry w przestrzeni świata.

![Zasięg światła punktowego](images/light/point_light_range.png)

Zmiana koloru światła zabarwia udział światła punktowego w oświetleniu, natomiast zasięg określa, jak daleko od źródła dociera światło.

![Zasięg zielonego światła punktowego](images/light/point_ight_range_green_color.png)

### Światło reflektorowe

Światła reflektorowe emitują światło w stożku z pozycji obiektu gry w przestrzeni świata. Kierunek jest wyznaczany na podstawie obrotu obiektu gry w przestrzeni świata, zastosowanego do `(0, 0, -1)`.

Komponent światła reflektorowego jest przedstawiany w edytorze kolorową ikoną lampy oraz liniami pomocniczymi pokazującymi stożek zewnętrzny i wewnętrzny.

![Światło reflektorowe](images/light/spot_light.png)

Właściwości:

`color`
: Kolor RGB światła reflektorowego.

`intensity`
: Mnoży kolor światła reflektorowego.

`range`
: Promień światła w jednostkach świata.

`inner_cone_angle`
: Kąt wewnętrznego stożka, podawany w edytorze w stopniach. Piksele wewnątrz tego stożka otrzymują pełny udział światła reflektorowego.

`outer_cone_angle`
: Kąt zewnętrznego stożka, podawany w edytorze w stopniach. Światło zanika pomiędzy stożkiem wewnętrznym i zewnętrznym.

Efektywny zasięg jest mnożony przez najmniejszą z wartości bezwzględnych składowych skali obiektu gry w przestrzeni świata. Kąty stożków edytuje się w stopniach, a w skompilowanym zasobie światła są przeliczane na radiany.

![Linie pomocnicze światła reflektorowego](images/light/spot_light_gizmos.png)

## Walidacja

Proces budowania sprawdza i normalizuje dane zasobów świateł:

- `color` musi zawierać dokładnie trzy liczby.
- `intensity` jest ograniczane od dołu do `0`.
- `range` jest ograniczane od dołu do `0` dla świateł punktowych i reflektorowych.
- Kąty stożków światła reflektorowego są ograniczane do `0..180` stopni.
- `inner_cone_angle` jest ograniczany tak, aby nigdy nie przekraczał `outer_cone_angle`.

## Limit projektu

Maksymalną liczbą komponentów Light steruje ustawienie projektu `light.max_count`. Jego domyślna wartość to `64`.

Światła otoczenia nie zajmują pozycji w tablicy `lights[]` shadera, ale nadal są komponentami Light i wliczają się do `light.max_count`. Aktywne światła kierunkowe, punktowe i reflektorowe zajmują pozycje w `lights[]`.

Jeśli liczba komponentów Light przekroczy `light.max_count`, silnik zgłosi błąd przepełnienia bufora komponentów.

## Bufor świateł w shaderach

Shader może uzyskać dostęp do aktywnych świateł, deklarując blok uniformów o nazwie `LightBuffer` z wbudowanym układem. Silnik wykrywa ten blok i automatycznie wiąże dane świateł z materiałami i programami obliczeniowymi, które go używają.

![Bufor świateł w shaderze](images/light/light-buffer-shader.png)

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

struct Light
{
    vec4 position;        // xyz: pozycja w przestrzeni świata, w: nieużywane
    vec4 color;           // rgb: kolor, a: nieużywane
    vec4 direction_range; // xyz: znormalizowany kierunek w przestrzeni świata, w: zasięg
    vec4 params;          // x: typ, y: intensywność, z: stożek wewnętrzny, w: stożek zewnętrzny
};

uniform LightBuffer
{
    // xyz: zsumowany kolor otoczenia, w: liczba aktywnych świateł innych niż światła otoczenia
    vec4 light_info;
    Light lights[MAX_LIGHT_COUNT];
};
```

Typ światła jest zapisany w `lights[i].params.x`:

| Typ | Wartość |
|------|-------|
| Kierunkowe | `0` |
| Punktowe | `1` |
| Reflektorowe | `2` |

Shader może zadeklarować tablicę `lights[]` mniejszą niż `light.max_count`, ale nie większą. Pętle przetwarzające światła należy zawsze ograniczać do zadeklarowanego rozmiaru tablicy:

```glsl
vec3 apply_lights(vec3 normal)
{
    vec3 result = light_info.xyz;
    int active_light_count = int(light_info.w);

    for (int i = 0; i < MAX_LIGHT_COUNT; ++i)
    {
        if (i >= active_light_count)
        {
            break;
        }

        int type = int(lights[i].params.x);
        vec3 light_color = lights[i].color.rgb * lights[i].params.y;

        if (type == 0) // Kierunkowe
        {
            vec3 light_dir = normalize(-lights[i].direction_range.xyz);
            result += light_color * max(dot(normal, light_dir), 0.0);
        }
        else if (type == 1) // Punktowe
        {
            result += light_color;
        }
        else if (type == 2) // Reflektorowe
        {
            result += light_color;
        }
    }

    return result;
}
```

Powyższy przykład pokazuje sposób uzyskiwania dostępu do bufora. Rzeczywisty shader światła punktowego lub reflektorowego powinien również obliczać wektor od cieniowanego punktu do `lights[i].position.xyz`, stosować tłumienie wraz z odległością przy użyciu `lights[i].direction_range.w`, a dla świateł reflektorowych używać `lights[i].params.z` oraz `lights[i].params.w` jako kątów stożka w radianach.

## Wbudowane funkcje pomocnicze oświetlenia

Silnik Defold zawiera plik z funkcjami pomocniczymi shadera w `/builtins/materials/lighting.glsl`. Zdefiniuj `MAX_LIGHT_COUNT`, udostępnij oczekiwane przez te funkcje zmienne varying, a następnie dołącz plik w shaderze fragmentów:

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

in vec3 var_normal;
in vec4 var_position;
in mat4 var_view;

out vec4 color_out;

#include "/builtins/materials/lighting.glsl"

void main()
{
    vec3 normal = normalize(var_normal);
    vec3 ambient = ambient_light();
    vec3 diffuse = diffuse_lambert(normal, var_position.xyz);
    color_out = vec4(ambient + diffuse, 1.0);
}
```

Plik pomocniczy definiuje stałe `LIGHT_DIRECTIONAL`, `LIGHT_POINT` i `LIGHT_SPOT`, udostępnia funkcję `ambient_light()` oraz zawiera funkcje rozproszonego oświetlenia Lamberta dla świateł w buforze.

## Zobacz także

- [Instrukcja shaderów](/manuals/shader)
- [Instrukcja materiałów](/manuals/material)
- [Instrukcja renderowania](/manuals/render)
