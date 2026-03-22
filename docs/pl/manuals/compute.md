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
-- Do compute work here, call render.set_compute() to unbind
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
-- dispatch_compute also accepts an options table as the last argument
-- you can use this argument table to pass in render constants to the dispatch call
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### Zapisywanie danych z programów compute

Obecnie generowanie dowolnego rodzaju danych wyjściowych z programu compute jest możliwe tylko za pomocą `storage textures`. Tekstura storage jest podobna do „zwykłej tekstury”, ale oferuje więcej funkcji i opcji konfiguracji. Jak sugeruje nazwa, `storage textures` mogą służyć jako ogólny bufor, z którego program compute może odczytywać i do którego może zapisywać dane. Ten sam bufor możesz potem powiązać z innym programem shadera do odczytu.

Aby utworzyć teksturę storage w Defold, musisz zrobić to ze zwykłego pliku `.script`. Skrypty do renderowania nie mają tej funkcjonalności, ponieważ tekstury dynamiczne trzeba tworzyć przez API zasobów, które jest dostępne tylko w zwykłych plikach `.script`.

```lua
-- In a .script file:
function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = resource.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = resource.TEXTURE_FORMAT_RGBA32F,
        flags  = resource.TEXTURE_USAGE_FLAG_STORAGE + resource.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- get the texture handle from the resource
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- notify the renderer of the backing texture, so it can be bound with render.enable_texture
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## Kompletny przykład

### Program shadera

```glsl
// compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// specify the input resources
uniform vec4 color;
uniform sampler2D texture_in;

// specify the output image
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // This isn't a particularly interesting shader, but it demonstrates
    // how to read from a texture and constant buffer and write to a storage texture

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // Write the output value to the storage texture
    imageStore(texture_out, tex_coord, output_value);
}
```

### Komponent skryptu
```lua
-- In a .script file

-- Here we specify the input texture that we later will bind to the
-- compute program. We can assign this texture to a model component,
-- or enable it to the render context in the render script.
go.property("texture_in", resource.texture())

function init(self)
    -- Create a texture resource like usual, but add the "storage" flag
    -- so it can be used as the backing storage for compute programs
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

    -- notify the renderer of the input and output textures
    msg.post("@render:", "set_backing_texture", textures)
end
```

### Skrypt do renderowania
```lua
-- respond to the message "set_backing_texture"
-- to set the backing texture for the compute program
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- We can bind textures to specific named constants
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- Dispatch the compute program as many times as we have pixels.
    -- This constitutes our "working group". The shader will be invoked
    -- 128 x 128 x 1 times, or once per pixel.
    render.dispatch_compute(128, 128, 1)
    -- when we are done with the compute program, we need to unbind it
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
