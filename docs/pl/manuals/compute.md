---
title: Programy compute w Defold
brief: Ta instrukcja wyjaśnia, jak pracować z programami compute, stałymi shaderów i samplerami.
---

# Programy compute

::: sidenote
Obsługa shaderów obliczeniowych (ang. compute shaders) w Defold jest obecnie w fazie *technical preview*.
Oznacza to, że części funkcji jeszcze brakuje, a API może w przyszłości ulec zmianie.
:::

Shadery obliczeniowe (ang. compute shaders) są potężnym narzędziem do wykonywania obliczeń ogólnego przeznaczenia na GPU. Pozwalają wykorzystać moc przetwarzania równoległego GPU do zadań takich jak symulacje fizyki, przetwarzanie obrazów i wiele innych. Shader obliczeniowy działa na danych przechowywanych w buforach lub teksturach, wykonując operacje równolegle w wielu wątkach GPU. To właśnie ta równoległość sprawia, że shadery obliczeniowe są tak skuteczne przy wymagających obliczeniach.

* Więcej informacji o potoku renderowania znajdziesz w [dokumentacji renderowania](/manuals/render).
* Szczegółowe wyjaśnienie programów shaderowych znajdziesz w [dokumentacji shaderów](/manuals/shader).

## Co można zrobić za pomocą shaderów obliczeniowych?

Ponieważ shadery obliczeniowe są przeznaczone do ogólnych obliczeń, praktycznie nie ma ograniczeń co do tego, do czego możesz ich użyć. Oto kilka przykładów typowych zastosowań shaderów obliczeniowych:

Przetwarzanie obrazów
  - Filtrowanie obrazów: stosowanie rozmycia, wykrywania krawędzi, wyostrzania i podobnych efektów.
  - Korekcja barwna: dostosowywanie przestrzeni kolorów obrazu.

Fizyka
  - Systemy cząsteczek: symulacja dużej liczby cząsteczek dla efektów takich jak dym, ogień czy dynamika płynów.
  - Fizyka ciał miękkich: symulacja odkształcalnych obiektów, takich jak tkanina czy galaretka.
  - Odrzucanie: `occlusion culling`, `frustum culling`

Generowanie proceduralne
  - Generowanie terenu: tworzenie szczegółowego terenu przy użyciu funkcji szumu.
  - Roślinność i zarośla: tworzenie proceduralnie generowanych roślin i drzew.

Efekty renderowania
  - Oświetlenie globalne (`global illumination`): symulowanie realistycznego oświetlenia przez przybliżenie sposobu, w jaki światło odbija się w scenie.
  - Wokselizacja (`voxelization`): tworzenie trójwymiarowej siatki wokseli z danych siatki.

## Jak działają shadery obliczeniowe?

Na wysokim poziomie shadery obliczeniowe działają przez podział zadania na wiele mniejszych zadań, które mogą zostać wykonane jednocześnie. Odbywa się to dzięki pojęciom `work groups` i `invocations`:

Grupy robocze (Work Groups)
: Shader obliczeniowy działa na siatce `work groups`. Każda grupa robocza zawiera stałą liczbę wywołań (`invocations`, czyli wątków). Rozmiar grup roboczych i liczba wywołań są definiowane w kodzie shadera.

Wywołania (Invocations)
: Każde wywołanie (`invocation`, czyli wątek) wykonuje program shadera obliczeniowego. Wywołania w obrębie jednej grupy roboczej mogą współdzielić dane przez pamięć współdzieloną, co pozwala na wydajną komunikację i synchronizację między nimi.

GPU wykonuje shader obliczeniowy, uruchamiając równolegle wiele wywołań w wielu grupach roboczych, co zapewnia znaczną moc obliczeniową dla odpowiednich zadań.

## Tworzenie programu compute

Aby utworzyć program compute, <kbd>kliknij prawym przyciskiem myszy</kbd> docelowy folder w widoku *Assets* i wybierz <kbd>New... ▸ Compute</kbd>. (Możesz też wybrać z menu <kbd>File ▸ New...</kbd>, a następnie <kbd>Compute</kbd>). Nadaj nazwę nowemu plikowi compute i naciśnij <kbd>Ok</kbd>.

![Plik compute](images/compute/compute_file.png)

Nowy plik compute otworzy się w edytorze *Compute Editor*.

![Edytor compute](images/compute/compute.png)

Plik compute zawiera następujące informacje:

Compute Program
: Plik programu shadera compute (*`.cp`*), którego należy użyć. Shader działa na „abstrakcyjnych elementach roboczych”, co oznacza, że nie istnieje stała definicja typów danych wejściowych i wyjściowych. To programista definiuje, co shader obliczeniowy ma wygenerować.

Constants
: Uniformy, które zostaną przekazane do programu shadera compute. Poniżej znajdziesz listę dostępnych stałych.

Samplers
: W pliku materiału możesz opcjonalnie skonfigurować konkretne samplery. Dodaj sampler, nazwij go zgodnie z nazwą używaną w programie shadera i ustaw parametry wrap oraz filter według potrzeb.


## Używanie programu compute w Defold

W odróżnieniu od materiałów programy compute nie są przypisywane do żadnych komponentów i nie są częścią normalnego przebiegu renderowania. Aby wykonały jakąkolwiek pracę, trzeba je wywołać (`dispatch`) w skrypcie do renderowania. Zanim jednak to zrobisz, musisz upewnić się, że skrypt do renderowania ma odniesienie do programu compute. Obecnie jedynym sposobem, aby skrypt do renderowania wiedział o programie compute, jest dodanie go do pliku `.render`, który przechowuje odniesienie do twojego skryptu do renderowania:

![Plik render z compute](images/compute/compute_render_file.png)

Aby użyć programu compute, trzeba go najpierw powiązać z kontekstem renderowania. Robi się to tak samo jak w przypadku materiałów:

```lua
render.set_compute("my_compute")
-- Tutaj wykonuj obliczenia compute; wywołaj render.set_compute(), aby odwiązać program
render.set_compute()
```

Choć stałe compute zostaną automatycznie zastosowane podczas wywołania programu, z poziomu edytora nie da się powiązać z programem compute żadnych zasobów wejściowych ani wyjściowych (tekstur, buforów itd.). Zamiast tego trzeba to zrobić w skryptach do renderowania:

```lua
render.enable_texture("blur_render_target", "tex_blur")
render.enable_texture(self.storage_texture, "tex_storage")
```

Aby uruchomić program w ustalonej przez siebie przestrzeni roboczej, musisz go wywołać:

```lua
render.dispatch_compute(128, 128, 1)
-- dispatch_compute przyjmuje też tabelę opcji jako ostatni argument
-- tej tabeli możesz użyć do przekazania stałych renderowania do wywołania dispatch
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### Zapisywanie danych z programów compute

Obecnie generowanie dowolnego rodzaju danych wyjściowych z programu compute jest możliwe tylko za pomocą `storage textures`. Tekstura storage jest podobna do „zwykłej tekstury”, ale oferuje więcej funkcji i opcji konfiguracji. Jak sugeruje nazwa, `storage textures` mogą służyć jako ogólny bufor, z którego program compute może odczytywać i do którego może zapisywać dane. Ten sam bufor możesz potem powiązać z innym programem shadera do odczytu.

Aby utworzyć teksturę storage w Defold, musisz zrobić to ze zwykłego pliku `.script`. Skrypty do renderowania nie mają tej funkcjonalności, ponieważ tekstury dynamiczne trzeba tworzyć przez API zasobów, które jest dostępne tylko w zwykłych plikach `.script`.

```lua
-- W pliku .script:
function init(self)
    -- Utwórz zasób tekstury jak zwykle, ale dodaj flagę "storage",
    -- aby można go było użyć jako tekstury bazowej dla programów compute
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = resource.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = resource.TEXTURE_FORMAT_RGBA32F,
        flags  = resource.TEXTURE_USAGE_FLAG_STORAGE + resource.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- pobierz uchwyt tekstury z zasobu
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- powiadom renderer o teksturze bazowej, aby można było ją powiązać przez render.enable_texture
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## Kompletny przykład

### Program shadera

```glsl
// plik: compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// określ zasoby wejściowe
uniform vec4 color;
uniform sampler2D texture_in;

// określ obraz wyjściowy
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // To nie jest szczególnie ciekawy shader, ale pokazuje,
    // jak czytać z tekstury i bufora stałych oraz zapisywać do tekstury storage

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // Zapisz wartość wyjściową do tekstury storage
    imageStore(texture_out, tex_coord, output_value);
}
```

### Komponent skryptu
```lua
-- W pliku .script:

-- Tutaj określamy teksturę wejściową, którą później powiążemy
-- z programem compute. Możemy przypisać tę teksturę do komponentu modelu
-- albo włączyć ją w kontekście renderowania w skrypcie renderowania.
go.property("texture_in", resource.texture())

function init(self)
    -- Utwórz zasób tekstury jak zwykle, ale dodaj flagę "storage",
    -- aby można go było użyć jako tekstury bazowej dla programów compute
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = resource.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = resource.TEXTURE_FORMAT_RGBA32F,
        flags  = resource.TEXTURE_USAGE_FLAG_STORAGE + resource.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    local textures = {
        texture_in = resource.get_texture_info(self.texture_in).handle,
        texture_out = resource.get_texture_info(t_backing).handle
    }

    -- powiadom renderer o teksturach wejściowej i wyjściowej
    msg.post("@render:", "set_backing_texture", textures)
end
```

### Skrypt do renderowania
```lua
-- reaguj na wiadomość "set_backing_texture",
-- aby ustawić teksturę bazową dla programu compute
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- Możemy powiązać tekstury z konkretnymi nazwanymi stałymi
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- Uruchom program compute tyle razy, ile mamy pikseli.
    -- To stanowi naszą "grupę roboczą". Shader zostanie wywołany
    -- 128 x 128 x 1 times, or once per pixel.
    render.dispatch_compute(128, 128, 1)
    -- gdy skończymy pracę z programem compute, musimy go odwiązać
    render.set_compute()
end
```

## Zgodność

Defold obsługuje obecnie shadery obliczeniowe na następujących adapterach graficznych:

- Vulkan
- Metal (przez MoltenVK)
- OpenGL 4.3+
- OpenGL ES 3.1+

::: sidenote
Obecnie nie ma sposobu, aby sprawdzić, czy uruchomiony klient obsługuje shadery obliczeniowe.
Oznacza to, że jeśli adapter graficzny jest oparty na OpenGL lub OpenGL ES, nie ma gwarancji, że klient obsłuży uruchamianie shaderów obliczeniowych.
Vulkan i Metal obsługują shadery obliczeniowe od wersji 1.0. Aby użyć backendu Vulkan, musisz utworzyć własny manifest i wybrać ten backend.
:::
