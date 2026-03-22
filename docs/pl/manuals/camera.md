---
title: Instrukcja komponentu Camera
brief: Ta instrukcja opisuje działanie komponentu Camera w silniku Defold.
---

# Kamery

Kamera (ang. camera) w silniku Defold jest komponentem, który zmienia obszar widoczny i projekcję świata gry. Komponent Camera definiuje podstawową kamerę perspektywiczną albo ortograficzną i przekazuje do skryptu renderującego macierz widoku oraz macierz projekcji.

Kamera perspektywiczna jest zwykle używana w grach 3D, gdzie widok kamery oraz rozmiar i perspektywa obiektów zależą od bryły widoku (frustum), odległości od kamery i kąta patrzenia na obiekty w grze.

W grach 2D często pożądane jest renderowanie sceny z użyciem projekcji ortograficznej. Oznacza to, że widok kamery nie jest już wyznaczany przez bryłę widoku, lecz przez prostokątny obszar. Projekcja ortograficzna jest niefotorealistyczna, ponieważ nie zmienia rozmiaru obiektów zależnie od ich odległości. Obiekt oddalony o 1000 jednostek zostanie narysowany w takim samym rozmiarze jak obiekt znajdujący się tuż przed kamerą.

![projections](images/camera/projections.png)


## Tworzenie kamery

Aby utworzyć kamerę, <kbd>right click</kbd> obiekt gry i wybierz <kbd>Add Component ▸ Camera</kbd>. Możesz też utworzyć plik komponentu w hierarchii projektu i dodać ten plik komponentu do obiektu gry.

![create camera component](images/camera/create.png)

Komponent Camera ma następujące właściwości definiujące jego *frustum*:

![camera settings](images/camera/settings.png)

Id
: Id komponentu.

Aspect Ratio
: (**Tylko dla kamery perspektywicznej**) Stosunek szerokości bryły widoku do jej wysokości. 1.0 oznacza widok kwadratowy. 1.33 dobrze pasuje do widoku 4:3, takiego jak 1024x768. 1.78 dobrze pasuje do widoku 16:9. To ustawienie jest ignorowane, jeśli włączone jest *Auto Aspect Ratio*.

Fov
: (**Tylko dla kamery perspektywicznej**) *Pionowe* pole widzenia kamery wyrażone w radianach. Im szersze pole widzenia, tym większy obszar zobaczy kamera.

Near Z
: Wartość Z bliskiej płaszczyzny odcięcia.

Far Z
: Wartość Z dalekiej płaszczyzny odcięcia.

Auto Aspect Ratio
: (**Tylko dla kamery perspektywicznej**) Włącz tę opcję, aby kamera automatycznie obliczała współczynnik proporcji.

Orthographic Projection
: Włącz tę opcję, aby przełączyć kamerę na projekcję ortograficzną.

Orthographic Zoom
: (**Tylko dla kamery ortograficznej**) Powiększenie używane w projekcji ortograficznej (> 1 = przybliżenie, < 1 = oddalenie).

Orthographic Mode
: (**Tylko dla kamery ortograficznej**) Określa, jak kamera ortograficzna wyznacza zoom względem rozmiaru okna i rozdzielczości projektowej, czyli wartości `game.project` → `display.width/height`.
  - `Fixed` (stały zoom): używa bieżącej wartości `Orthographic Zoom` bez zmian.
  - `Auto Fit` (contain): automatycznie dopasowuje zoom tak, aby cały obszar projektowy mieścił się w oknie. Może pokazać dodatkową zawartość po bokach albo u góry i na dole.
  - `Auto Cover` (cover): automatycznie dopasowuje zoom tak, aby obszar projektowy wypełniał całe okno. Może przycinać zawartość po bokach albo u góry i na dole.
  Ta opcja jest dostępna tylko wtedy, gdy włączone jest `Orthographic Projection`.


## Używanie kamery

Wszystkie kamery są automatycznie włączane i aktualizowane w każdej klatce, a moduł Lua `camera` jest dostępny we wszystkich kontekstach skryptowych. Od Defold 1.8.1 nie trzeba już jawnie włączać kamery przez wysłanie do komponentu wiadomości `acquire_camera_focus`. Stare wiadomości acquire i release nadal istnieją, ale zaleca się używanie wiadomości enable i disable, tak samo jak w przypadku innych komponentów, które chcesz włączać i wyłączać:

```lua
msg.post("#camera", "disable")
msg.post("#camera", "enable")
```

Aby wyświetlić listę wszystkich obecnie dostępnych kamer, możesz użyć camera.get_cameras():

```lua
-- Uwaga: wywołania render są dostępne tylko w skrypcie renderującym.
--        Funkcji camera.get_cameras() można używać wszędzie,
--        ale render.set_camera tylko w skrypcie renderującym.

for k,v in pairs(camera.get_cameras()) do
    -- tabela kamer zawiera URL-e wszystkich kamer
    render.set_camera(v)
    -- tutaj wykonaj renderowanie; wszystko, co zostanie tu narysowane
    -- z użyciem materiałów korzystających z macierzy widoku i projekcji,
    -- będzie używać macierzy z tej kamery.
end
-- aby wyłączyć kamerę, przekaż nil (albo nie podawaj argumentów) do render.set_camera.
-- po tym wywołaniu wszystkie operacje renderowania będą używać macierzy widoku i projekcji
-- ustawionych bezpośrednio w kontekście renderowania (render.set_view i render.set_projection)
render.set_camera()
```

Moduł skryptowy `camera` udostępnia wiele funkcji do manipulowania kamerą. Poniżej kilka przykładów; pełną listę znajdziesz w [dokumentacji API](/ref/camera/).

```lua
camera.get_aspect_ratio(camera) -- pobierz współczynnik proporcji
camera.get_far_z(camera) -- pobierz far z
camera.get_fov(camera) -- pobierz pole widzenia
camera.get_orthographic_mode(camera) -- pobierz tryb ortograficzny (jedna z wartości camera.ORTHO_MODE_*)
camera.set_aspect_ratio(camera, ratio) -- ustaw współczynnik proporcji
camera.set_far_z(camera, far_z) -- ustaw far z
camera.set_near_z(camera, near_z) -- ustaw near z
camera.set_orthographic_mode(camera, camera.ORTHO_MODE_AUTO_FIT) -- ustaw tryb ortograficzny
... I tak dalej
```

Kamera jest identyfikowana przez URL, czyli pełną ścieżkę komponentu w scenie, obejmującą kolekcję, obiekt gry, do którego należy, oraz id komponentu. W tym przykładzie do identyfikacji komponentu kamery z tej samej kolekcji użyjesz URL `/go#camera`, a przy dostępie do kamery z innej kolekcji albo ze skryptu renderującego użyjesz `main:/go#camera`.

![create camera component](images/camera/create.png)

```lua
-- Dostęp do kamery ze skryptu w tej samej kolekcji:
camera.get_fov("/go#camera")

-- Dostęp do kamery ze skryptu w innej kolekcji:
camera.get_fov("main:/go#camera")

-- Dostęp do kamery ze skryptu renderującego:
render.set_camera("main:/go#camera")
```

W każdej klatce komponent kamery, który ma aktualnie fokus kamery, wysyła wiadomość `set_view_projection` do gniazda "@render":

```lua
-- builtins/render/default.render_script
--
function on_message(self, message_id, message)
    if message_id == hash("set_view_projection") then
        self.view = message.view                    -- [1]
        self.projection = message.projection
    end
end
```
1. Wiadomość wysyłana z komponentu kamery zawiera macierz widoku i macierz projekcji.

Komponent Camera dostarcza skryptowi renderującemu macierz projekcji perspektywicznej albo ortograficznej, zależnie od właściwości *Orthographic Projection*. Macierz projekcji uwzględnia też ustawione bliską i daleką płaszczyznę odcięcia, pole widzenia oraz współczynnik proporcji kamery.

Macierz widoku dostarczana przez kamerę definiuje położenie i orientację kamery. Kamera z włączonym *Orthographic Projection* centruje widok na pozycji obiektu gry, do którego jest podłączona, natomiast kamera z *Perspective Projection* będzie miała lewy dolny róg widoku ustawiony w pozycji obiektu gry, do którego jest podłączona.


### Skrypt do renderowania

Podczas używania domyślnego skryptu do renderowania Defold automatycznie ustawia ostatnią włączoną kamerę, która ma być używana do renderowania. Wcześniej skrypt w projekcie musiał jawnie wysyłać do renderera wiadomość `use_camera_projection`, aby poinformować go, że ma korzystać z widoku i projekcji z komponentów kamery. Nie jest to już konieczne, ale nadal można tak robić dla zachowania zgodności wstecznej.

Alternatywnie możesz ustawić w skrypcie do renderowania konkretną kamerę, której należy użyć do renderowania. Przydaje się to wtedy, gdy chcesz dokładniej kontrolować, która kamera jest używana, na przykład w grze wieloosobowej.

```lua
-- render.set_camera będzie automatycznie używać macierzy widoku i projekcji
-- przy każdym renderowaniu aż do wywołania render.set_camera().
render.set_camera("main:/my_go#camera")
```

Aby sprawdzić, czy kamera jest aktywna, możesz użyć funkcji `get_enabled` z [Camera API](https://defold.com/ref/alpha/camera/#camera.get_enabled:camera):

```lua
if camera.get_enabled("main:/my_go#camera") then
    -- kamera jest włączona, użyj jej do renderowania!
    render.set_camera("main:/my_go#camera")
end
```

::: sidenote
Aby używać funkcji `set_camera` razem z odrzucaniem poza bryłą widoku (frustum culling), musisz przekazać do niej taką opcję:
`render.set_camera("main:/my_go#camera", {use_frustum = true})`
:::

### Poruszanie kamerą

Kamerę przesuwa się po świecie gry przez przesuwanie obiektu gry, do którego przypisany jest komponent Camera. Komponent automatycznie wyśle zaktualizowaną macierz widoku na podstawie bieżącej pozycji kamery na osiach X i Y.

### Zoomowanie kamery

Przy użyciu kamery perspektywicznej możesz przybliżać i oddalać widok, przesuwając obiekt gry, do którego przypisana jest kamera, wzdłuż osi Z. Komponent Camera automatycznie wyśle zaktualizowaną macierz widoku na podstawie bieżącej pozycji kamery na osi Z.

W przypadku kamery ortograficznej możesz przybliżać i oddalać widok przez zmianę właściwości *Orthographic Zoom*:

```lua
go.set("#camera", "orthographic_zoom", 2)
```

Przy użyciu kamery ortograficznej możesz też przełączać sposób wyznaczania zoomu za pomocą ustawienia `Orthographic Mode` albo z poziomu skryptu:

```lua
-- pobierz bieżący tryb (jedna z wartości camera.ORTHO_MODE_FIXED, _AUTO_FIT, _AUTO_COVER)
local mode = camera.get_orthographic_mode("#camera")

-- przełącz na auto-fit (contain), aby cały obszar projektowy zawsze pozostawał widoczny
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)

-- przełącz na auto-cover, aby obszar projektowy zawsze wypełniał okno
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_COVER)

-- wróć do trybu fixed, aby ręcznie sterować zoomem przez orthographic_zoom
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_FIXED)
```

### Adaptacyjny zoom

Idea adaptacyjnego zoomu polega na dostosowywaniu wartości zoomu kamery, gdy rozdzielczość wyświetlacza zmienia się względem początkowej rozdzielczości ustawionej w *game.project*.

Dwa częste podejścia do adaptacyjnego zoomu to:

1. Maksymalny zoom: oblicz taką wartość zoomu, aby obszar zawartości odpowiadający początkowej rozdzielczości z *game.project* wypełniał ekran i wykraczał poza jego krawędzie, co może ukryć część zawartości po bokach albo u góry i na dole.
2. Minimalny zoom: oblicz taką wartość zoomu, aby obszar zawartości odpowiadający początkowej rozdzielczości z *game.project* w całości mieścił się w granicach ekranu, co może pokazać dodatkową zawartość po bokach albo u góry i na dole.

Przykład:

```lua
local DISPLAY_WIDTH = sys.get_config_int("display.width")
local DISPLAY_HEIGHT = sys.get_config_int("display.height")

function init(self)
    local initial_zoom = go.get("#camera", "orthographic_zoom")
    local display_scale = window.get_display_scale()
    window.set_listener(function(self, event, data)
        if event == window.WINDOW_EVENT_RESIZED then
            local window_width = data.width
            local window_height = data.height
            local design_width = DISPLAY_WIDTH / initial_zoom
            local design_height = DISPLAY_HEIGHT / initial_zoom

            -- maksymalny zoom: upewnij się, że początkowe wymiary projektu
            -- wypełnią ekran i wyjdą poza jego granice
            local zoom = math.max(window_width / design_width, window_height / design_height) / display_scale

            -- minimalny zoom: upewnij się, że początkowe wymiary projektu
            -- zmieszczą się w granicach ekranu
            --local zoom = math.min(window_width / design_width, window_height / design_height) / display_scale
            
            go.set("#camera", "orthographic_zoom", zoom)
        end
    end)
end
```

Pełny przykład adaptacyjnego zoomu znajdziesz w [tym projekcie przykładowym](https://github.com/defold/sample-adaptive-zoom).

Uwaga: przy użyciu kamery ortograficznej możesz teraz uzyskać zachowanie contain/cover bez własnego kodu, ustawiając `Orthographic Mode` na `Auto Fit` (contain) albo `Auto Cover` (cover). W tych trybach efektywny zoom jest obliczany automatycznie na podstawie rozmiaru okna i rozdzielczości projektowej.


### Śledzenie obiektu gry

Możesz sprawić, aby kamera śledziła obiekt gry, ustawiając obiekt gry, do którego przypisany jest komponent Camera, jako dziecko śledzonego obiektu:

![follow game object](images/camera/follow.png)

Innym sposobem jest aktualizowanie co klatkę pozycji obiektu gry, do którego przypisany jest komponent Camera, zgodnie z ruchem śledzonego obiektu.

### Konwersja współrzędnych myszy na współrzędne świata

Gdy kamera została przesunięta, przybliżona lub korzysta z innej projekcji niż domyślna rozciągnięta projekcja ortograficzna, współrzędne myszy dostarczane do funkcji cyklu życia `on_input()` przestają odpowiadać współrzędnym świata obiektów gry. Trzeba wtedy ręcznie uwzględnić zmianę widoku albo projekcji. Kod konwertujący współrzędne myszy i ekranu na współrzędne świata wygląda tak:

```Lua
--- Konwertuje współrzędne ekranu na współrzędne świata,
-- biorąc pod uwagę widok i projekcję konkretnej kamery
-- @param camera URL kamery używanej do konwersji
-- @param screen_x Współrzędna x na ekranie do przeliczenia
-- @param screen_y Współrzędna y na ekranie do przeliczenia
-- @param z opcjonalna współrzędna z przekazywana przez konwersję, domyślnie 0
-- @return world_x Wynikowa współrzędna x w świecie
-- @return world_y Wynikowa współrzędna y w świecie
-- @return world_z Wynikowa współrzędna z w świecie
function M.screen_to_world(camera, screen_x, screen_y, z)
    local projection = go.get(camera, "projection")
    local view = go.get(camera, "view")
    local w, h = window.get_size()

    -- https://defold.com/manuals/camera/#converting-mouse-to-world-coordinates
    local inv = vmath.inv(projection * view)
    local x = (2 * screen_x / w) - 1
    local y = (2 * screen_y / h) - 1
    local x1 = x * inv.m00 + y * inv.m01 + z * inv.m02 + inv.m03
    local y1 = x * inv.m10 + y * inv.m11 + z * inv.m12 + inv.m13
    return x1, y1, z or 0
end
```

Pamiętaj, że jako argumentów tej funkcji należy używać wartości `action.screen_x` i `action.screen_y` z `on_input()`. Zobacz [stronę Examples](https://defold.com/examples/render/screen_to_world/), aby sprawdzić konwersję współrzędnych ekranu na współrzędne świata w praktyce. Dostępny jest też [projekt przykładowy](https://github.com/defold/sample-screen-to-world-coordinates/) pokazujący, jak wykonać taką konwersję.

::: sidenote
[Rozwiązania kamer od społeczności wymienione w tym podręczniku](/manuals/camera/#third-party-camera-solutions) zawierają funkcje konwersji do współrzędnych ekranu i z powrotem.
:::

## Manipulacja w czasie działania

Kamerami można manipulować w czasie działania za pomocą różnych wiadomości i właściwości. Sposób użycia znajdziesz w [dokumentacji API](/ref/camera/).

Kamera ma kilka właściwości, którymi można sterować przy użyciu `go.get()` i `go.set()`:

`fov`
: Pole widzenia kamery (`number`).

`near_z`
: Bliska wartość Z kamery (`number`).

`far_z`
: Daleka wartość Z kamery (`number`).

`orthographic_zoom`
: Zoom kamery ortograficznej (`number`).

`aspect_ratio`
: Stosunek szerokości bryły widoku do jej wysokości. Używany przy obliczaniu projekcji kamery perspektywicznej (`number`).

`view`
: Obliczona macierz widoku kamery. Tylko do odczytu (`matrix4`).

`projection`
: Obliczona macierz projekcji kamery. Tylko do odczytu (`matrix4`).


## Rozwiązania kamer od społeczności

Społeczność stworzyła rozwiązania kamerowe implementujące typowe funkcje, takie jak trzęsienie ekranu, śledzenie obiektów gry, konwersję współrzędnych ekranu na współrzędne świata i wiele innych. Można je pobrać z portalu zasobów Defold:

- [Orthographic camera](https://defold.com/assets/orthographic/) (tylko 2D) autorstwa Björna Ritzla.
- [Defold Rendy](https://defold.com/assets/defold-rendy/) (2D i 3D) autorstwa Klaytona Kowalskiego.
