---
title: Skrypty edytora
brief: Ta instrukcja wyjaśnia, jak rozszerzać edytor Defold przy użyciu Lua.
---

# Skrypty edytora

Możesz tworzyć własne pozycje menu i hooki cyklu życia edytora przy użyciu plików Lua ze specjalnym rozszerzeniem `.editor_script`. Dzięki temu mechanizmowi da się dostosować edytor tak, aby usprawnić własny proces pracy.

## Środowisko uruchomieniowe skryptów edytora

Skrypty edytora działają wewnątrz edytora, w maszynie wirtualnej Lua emulowanej przez JVM. Wszystkie skrypty współdzielą jedno środowisko, więc mogą ze sobą współpracować. Możesz używać modułów Lua przez require, podobnie jak w plikach `.script`, ale wersja Lua uruchamiana w edytorze jest inna, dlatego współdzielony kod musi być z nią zgodny. Edytor używa Lua 5.2.x, a dokładniej środowiska [luaj](https://github.com/luaj/luaj), które obecnie jest jedynym sensownym sposobem uruchamiania Lua na JVM. Poza tym obowiązuje kilka ograniczeń:

- nie ma pakietu `debug`;
- nie ma `os.execute`, ale dostępna jest podobna funkcja `editor.execute()`;
- nie ma `os.tmpname` ani `io.tmpfile` — obecnie skrypty edytora mogą uzyskiwać dostęp tylko do plików wewnątrz katalogu projektu;
- obecnie nie ma `os.rename`, choć planujemy je dodać;
- nie ma `os.exit` ani `os.setlocale`;
- w kontekstach, w których edytor potrzebuje natychmiastowej odpowiedzi od skryptu, nie wolno używać niektórych długo działających funkcji; szczegóły znajdziesz w sekcji [Tryby wykonania](#tryby-wykonania).

Wszystkie rozszerzenia edytora zdefiniowane w skryptach edytora są ładowane podczas otwierania projektu. Gdy pobierasz biblioteki, rozszerzenia są przeładowywane, ponieważ w zależnościach mogą pojawić się nowe skrypty edytora. Podczas takiego przeładowania zmiany w twoich własnych skryptach nie są wykrywane, bo możesz być akurat w trakcie ich edycji. Aby przeładować także je, uruchom polecenie **Project → Reload Editor Scripts**.

## Anatomia pliku `.editor_script`

Każdy skrypt edytora powinien zwracać moduł, na przykład:

```lua
local M = {}

function M.get_commands()
  -- TODO - zdefiniuj polecenia edytora
end

function M.get_language_servers()
  -- TODO - zdefiniuj serwery językowe
end

function M.get_prefs_schema()
  -- TODO - zdefiniuj preferencje
end

return M
```

Edytor zbiera wszystkie skrypty edytora zdefiniowane w projekcie i bibliotekach, ładuje je do jednej maszyny Lua i wywołuje wtedy, gdy są potrzebne. Więcej informacji znajdziesz w sekcjach [Polecenia](#commands) i [Hooki cyklu życia](#lifecycle-hooks).

## API edytora

Z edytorem możesz komunikować się przez pakiet `editor`, który udostępnia następujące API:

- `editor.platform` — łańcuch znaków określający platformę: `"x86_64-win32"` dla Windows, `"x86_64-macos"` dla macOS albo `"x86_64-linux"` dla Linux;
- `editor.version` — łańcuch znaków z nazwą wersji Defold, na przykład `"1.4.8"`;
- `editor.engine_sha1` — łańcuch znaków z SHA1 silnika Defold;
- `editor.editor_sha1` — łańcuch znaków z SHA1 edytora Defold;
- `editor.get(node_id, property)` — odczytuje wartość wybranego węzła wewnątrz edytora. Węzły w edytorze to różne byty, na przykład pliki skryptów lub kolekcji, obiekty gry wewnątrz kolekcji, pliki JSON wczytane jako zasoby itd. `node_id` to wartość userdata przekazywana skryptowi przez edytor. Zamiast `node_id` możesz też podać ścieżkę zasobu, na przykład `"/main/game.script"`. `property` to łańcuch znaków. Obecnie obsługiwane są między innymi:
  - `"path"` — ścieżka zasobu względem katalogu projektu dla zasobów istniejących jako pliki lub katalogi. Przykładowa wartość: `"/main/game.script"`;
  - `"children"` — lista ścieżek zasobów potomnych dla zasobów będących katalogami;
  - `"text"` — tekstowa zawartość zasobu edytowalnego jako tekst, na przykład plików skryptów lub JSON. Przykładowa wartość: `"function init(self)\nend"`. To nie jest to samo co odczyt pliku przez `io.open()`, ponieważ plik może być zmieniony, ale jeszcze niezapisany, a takie zmiany są dostępne tylko przez właściwość `"text"`;
  - dla atlasów: `images` (lista węzłów obrazów atlasu) oraz `animations` (lista węzłów animacji);
  - dla animacji atlasu: `images`;
  - dla tilemap: `layers` (lista węzłów warstw tilemapy);
  - dla warstw tilemapy: `tiles` (nieograniczona dwuwymiarowa siatka kafelków), więcej w `tilemap.tiles.*`;
  - dla `particlefx`: `emitters` (lista węzłów emiterów) i `modifiers` (lista węzłów modyfikatorów);
  - dla emiterów `particlefx`: `modifiers`;
  - dla obiektów kolizji: `shapes` (lista węzłów kształtów kolizji);
  - dla plików GUI: `layers` (lista węzłów warstw);
  - część właściwości widocznych w panelu Properties, gdy w Outline coś jest zaznaczone. Obecnie obsługiwane są typy:
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    Niektóre z tych właściwości mogą być tylko do odczytu albo niedostępne w danym kontekście, dlatego przed odczytem użyj `editor.can_get`, a przed zapisem `editor.can_set`. Po najechaniu kursorem na nazwę właściwości w panelu Properties zobaczysz podpowiedź z nazwą używaną w skryptach edytora. Właściwości zasobów możesz ustawić na `nil`, przekazując `""`.
- `editor.can_get(node_id, property)` — sprawdza, czy odczyt danej właściwości przez `editor.get()` nie zakończy się błędem;
- `editor.can_set(node_id, property)` — sprawdza, czy krok transakcji `editor.tx.set()` dla tej właściwości nie zakończy się błędem;
- `editor.create_directory(resource_path)` — tworzy katalog, jeśli nie istnieje, wraz z brakującymi katalogami nadrzędnymi;
- `editor.create_resources(resources)` — tworzy co najmniej jeden zasób, z szablonów albo z własną zawartością;
- `editor.delete_directory(resource_path)` — usuwa katalog, jeśli istnieje, wraz z istniejącymi podkatalogami i plikami;
- `editor.execute(cmd, [...args], [options])` — uruchamia polecenie powłoki, opcjonalnie przechwytując jego wynik;
- `editor.save()` — zapisuje wszystkie niezapisane zmiany na dysk;
- `editor.transact(txs)` — modyfikuje stan edytora w pamięci przy użyciu jednego lub wielu kroków transakcji utworzonych przez `editor.tx.*`;
- `editor.ui.*` — funkcje związane z interfejsem; szczegóły w [instrukcji UI](/manuals/editor-scripts-ui);
- `editor.prefs.*` — funkcje do pracy z preferencjami edytora; szczegóły w sekcji [Preferencje](#preferences).

Pełne API edytora znajdziesz [tutaj](https://defold.com/ref/alpha/editor/).

## Polecenia

Jeśli moduł skryptu edytora definiuje funkcję `get_commands`, zostanie ona wywołana podczas przeładowywania rozszerzeń, a zwrócone polecenia będą dostępne w pasku menu edytora albo w menu kontekstowych paneli Assets i Outline. Przykład:

```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
      locations = {"Edit", "Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        local path = editor.get(opts.selection, "path")
        return ends_with(path, ".lua") or ends_with(path, ".script")
      end,
      run = function(opts)
        local text = editor.get(opts.selection, "text")
        editor.transact({
          editor.tx.set(opts.selection, "text", strip_comments(text))
        })
      end
    },
    {
      label = "Minify JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        editor.execute("./scripts/minify-json.sh", path:sub(2))
      end
    }
  }
end

return M
```

Edytor oczekuje, że `get_commands()` zwróci tablicę tabel, z których każda opisuje jedno polecenie. Opis polecenia składa się z:

- `label` (wymagane) — tekst pozycji menu widoczny dla użytkownika;
- `locations` (wymagane) — tablica zawierająca `"Edit"`, `"View"`, `"Project"`, `"Debug"`, `"Assets"`, `"Bundle"`, `"Scene"` albo `"Outline"`, określająca, gdzie polecenie ma być dostępne. `"Edit"`, `"View"`, `"Project"` i `"Debug"` oznaczają górny pasek menu, `"Assets"` oznacza menu kontekstowe panelu Assets, `"Outline"` oznacza menu kontekstowe panelu Outline, a `"Bundle"` oznacza podmenu **Project → Bundle**;
- `query` — sposób, w jaki polecenie prosi edytor o potrzebne dane i definiuje, na czym operuje. Dla każdego klucza w tabeli `query` pojawi się odpowiadający klucz w tabeli `opts`, przekazywanej do funkcji `active` i `run`. Obsługiwane klucze:
  - `selection` oznacza, że polecenie działa na aktualnym zaznaczeniu.
    - `type` określa typ zaznaczonych węzłów. Obecnie dozwolone są:
      - `"resource"` — w Assets i Outline oznacza zaznaczony element mający odpowiadający mu plik. W pasku menu (Edit lub View) oznacza aktualnie otwarty plik;
      - `"outline"` — coś, co może być pokazane w Outline. W Outline to zaznaczony element, w pasku menu — aktualnie otwarty plik;
      - `"scene"` — coś, co da się wyrenderować w Scene;
    - `cardinality` określa liczbę zaznaczonych elementów. Dla `"one"` callback otrzyma pojedynczy `node_id`, a dla `"many"` — tablicę co najmniej jednego `node_id`;
  - `argument` — argument polecenia. Obecnie tylko polecenia z lokalizacją `"Bundle"` otrzymują argument: `true`, gdy użytkownik jawnie wybrał bundlowanie, i `false` przy rebundle;
- `id` — identyfikator polecenia, używany na przykład do zapamiętywania ostatnio użytego polecenia bundlowania w `prefs`;
- `active` — callback sprawdzający, czy polecenie ma być aktywne. Powinien zwracać wartość logiczną. Jeśli `locations` zawiera `"Assets"`, `"Scene"` albo `"Outline"`, `active` zostanie wywołane przy otwieraniu menu kontekstowego. Jeśli `locations` zawiera `"Edit"` albo `"View"`, `active` będzie uruchamiane przy każdej interakcji użytkownika, na przykład podczas pisania na klawiaturze lub kliknięć myszą, więc musi działać stosunkowo szybko;
- `run` — callback wykonywany po wybraniu polecenia przez użytkownika.

### Używanie poleceń do zmiany stanu edytora w pamięci

Wewnątrz `run` możesz odczytywać i zmieniać stan edytora zapisany w pamięci. Odczyt odbywa się przez `editor.get()`, co pozwala pobierać aktualny stan plików i zaznaczenia (jeśli używasz `query = {selection = ...}`). Możesz pobrać właściwość `"text"` plików skryptów oraz wybrane właściwości widoczne w panelu Properties — najedź kursorem na nazwę właściwości, aby zobaczyć, jak nazywa się w skryptach edytora. Zmiany w stanie edytora wykonuje się przez `editor.transact()`, gdzie grupujesz jedną lub więcej modyfikacji w pojedynczy krok z możliwością cofnięcia. Na przykład polecenie resetujące transformację obiektu gry może wyglądać tak:

```lua
{
  label = "Reset transform",
  locations = {"Outline"},
  query = {selection = {type = "outline", cardinality = "one"}},
  active = function(opts)
    local node = opts.selection
    return editor.can_set(node, "position")
       and editor.can_set(node, "rotation")
       and editor.can_set(node, "scale")
  end,
  run = function(opts)
    local node = opts.selection
    editor.transact({
      editor.tx.set(node, "position", {0, 0, 0}),
      editor.tx.set(node, "rotation", {0, 0, 0}),
      editor.tx.set(node, "scale", {1, 1, 1})
    })
  end
}
```

#### Edycja atlasów

Poza odczytem i zapisem właściwości atlasu możesz też odczytywać i modyfikować obrazy oraz animacje atlasu. Atlas definiuje właściwości listowe `images` i `animations`, a animacje mają dodatkowo listową właściwość `images`. Z tymi właściwościami można używać kroków transakcji `editor.tx.add`, `editor.tx.remove` i `editor.tx.clear`.

Na przykład, aby dodać obraz do atlasu, uruchom w `run` takie polecenie:

```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```

Aby zbudować zbiór wszystkich obrazów w atlasie:

```lua
local all_images = {} ---@type table<string, true>
-- najpierw zbierz "gołe" obrazy
local image_nodes = editor.get("/main.atlas", "images")
for i = 1, #image_nodes do
    all_images[editor.get(image_nodes[i], "image")] = true
end
-- następnie zbierz obrazy używane w animacjach
local animation_nodes = editor.get("/main.atlas", "animations")
for i = 1, #animation_nodes do
    local animation_image_nodes = editor.get(animation_nodes[i], "images")
    for j = 1, #animation_image_nodes do
        all_images[editor.get(animation_image_nodes[j], "image")] = true
    end
end
pprint(all_images)
-- {
--     ["/assets/hero.png"] = true,
--     ["/assets/enemy.png"] = true,
-- }}
```

Aby zastąpić wszystkie animacje w atlasie:

```lua
editor.transact({
    editor.tx.clear("/main.atlas", "animations"),
    editor.tx.add("/main.atlas", "animations", {
        id = "hero_run",
        images = {
            {image = "/assets/hero_run_1.png"},
            {image = "/assets/hero_run_2.png"},
            {image = "/assets/hero_run_3.png"},
            {image = "/assets/hero_run_4.png"}
        }
    })
})
```

#### Edycja tilesource

Poza zwykłymi właściwościami z Outline, tilesource definiuje jeszcze:

- `animations` — listę węzłów animacji tilesource;
- `collision_groups` — listę węzłów grup kolizji tilesource;
- `tile_collision_groups` — tabelę przypisań grup kolizji do kafelków tilesource.

Przykładowa konfiguracja tilesource:

```lua
local tilesource = "/game/world.tilesource"
editor.transact({
    editor.tx.add(tilesource, "animations", {id = "idle", start_tile = 1, end_tile = 1}),
    editor.tx.add(tilesource, "animations", {id = "walk", start_tile = 2, end_tile = 6, fps = 10}),
    editor.tx.add(tilesource, "collision_groups", {id = "player"}),
    editor.tx.add(tilesource, "collision_groups", {id = "obstacle"}),
    editor.tx.set(tilesource, "tile_collision_groups", {
        [1] = "player",
        [7] = "obstacle",
        [8] = "obstacle"
    })
})
```

#### Edycja tilemap

Tilemapy definiują właściwość `layers`, która jest listą węzłów warstw. Każda warstwa ma z kolei właściwość `tiles`, przechowującą nieograniczoną dwuwymiarową siatkę kafelków. To zachowuje się inaczej niż w silniku: kafelki nie mają ograniczonych granic i można je dodawać w dowolnym miejscu, także na ujemnych współrzędnych. Do pracy z kafelkami API skryptów edytora udostępnia moduł `tilemap.tiles` z funkcjami:

- `tilemap.tiles.new()` — tworzy pustą strukturę danych dla nieograniczonej siatki kafelków;
- `tilemap.tiles.get_tile(tiles, x, y)` — zwraca indeks kafelka na podanych współrzędnych;
- `tilemap.tiles.get_info(tiles, x, y)` — zwraca pełne informacje o kafelku w danym punkcie (kształt danych jest zgodny z `tilemap.get_tile_info` w silniku);
- `tilemap.tiles.iterator(tiles)` — tworzy iterator po wszystkich kafelkach tilemapy;
- `tilemap.tiles.clear(tiles)` — usuwa wszystkie kafelki;
- `tilemap.tiles.set(tiles, x, y, tile_or_info)` — ustawia kafelek w podanym miejscu;
- `tilemap.tiles.remove(tiles, x, y)` — usuwa kafelek z podanych współrzędnych.

Przykład wypisania całej zawartości tilemapy:

```lua
local layers = editor.get("/level.tilemap", "layers")
for i = 1, #layers do
    local layer = layers[i]
    local id = editor.get(layer, "id")
    local tiles = editor.get(layer, "tiles")
    print("layer " .. id .. ": {")
    for x, y, tile in tilemap.tiles.iterator(tiles) do
        print("  [" .. x .. ", " .. y .. "] = " .. tile)
    end
    print("}")
end
```

Przykład dodania nowej warstwy z kafelkami:

```lua
local tiles = tilemap.tiles.new()
tilemap.tiles.set(tiles, 1, 1, 2)
editor.transact({
    editor.tx.add("/level.tilemap", "layers", {
        id = "new_layer",
        tiles = tiles
    })
})
```

#### Edycja particlefx

particlefx możesz edytować przez właściwości `modifiers` i `emitters`. Na przykład dodanie emitera kołowego z modyfikatorem przyspieszenia wygląda tak:

```lua
editor.transact({
    editor.tx.add("/fire.particlefx", "emitters", {
        type = "emitter-type-circle",
        modifiers = {
          {type = "modifier-type-acceleration"}
        }
    })
})
```

Wiele właściwości particlefx to krzywe albo krzywe ze spreadem (czyli krzywa plus losowy rozrzut). Krzywe są reprezentowane jako tabela z niepustą listą `points`, gdzie każdy punkt jest tabelą z właściwościami:

- `x` — współrzędna x punktu; powinna zaczynać się od 0 i kończyć na 1;
- `y` — wartość punktu;
- `tx` (0 do 1) i `ty` (-1 do 1) — tangensy punktu. Dla kąta 80 stopni `tx` powinno być równe `math.cos(math.rad(80))`, a `ty` — `math.sin(math.rad(80))`.

Krzywe ze spreadem mają dodatkowo właściwość liczbową `spread`.

Przykład ustawienia krzywej alpha czasu życia cząsteczki dla istniejącego emitera:

```lua
local emitter = editor.get("/fire.particlefx", "emitters")[1]
editor.transact({
    editor.tx.set(emitter, "particle_key_alpha", { points = {
        {x = 0,   y = 0, tx = 0.1, ty = 1}, -- startuj od 0 i szybko rośnij
        {x = 0.2, y = 1, tx = 1,   ty = 0}, -- osiągnij 1 po 20% czasu życia
        {x = 1,   y = 0, tx = 1,   ty = 0}  -- powoli opadaj do 0
    }})
})
```

Oczywiście można też użyć klucza `particle_key_alpha` bezpośrednio w tabeli podczas tworzenia emitera. Dodatkowo zamiast krzywej możesz podać pojedynczą liczbę reprezentującą krzywą statyczną.

#### Edycja obiektów kolizji

Poza domyślnymi właściwościami z Outline obiekty kolizji definiują listową właściwość `shapes`. Dodawanie nowych kształtów kolizji wygląda tak:

```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- albo "shape-type-sphere", "shape-type-capsule"
    })
})
```

Właściwość `type` kształtu jest wymagana podczas tworzenia i nie można jej zmienić po dodaniu kształtu. Dostępne są trzy typy:

- `shape-type-box` — kształt pudełkowy z właściwością `dimensions`;
- `shape-type-sphere` — kształt sferyczny z właściwością `diameter`;
- `shape-type-capsule` — kapsuła z właściwościami `diameter` i `height`.

#### Edycja plików GUI

Poza właściwościami z Outline pliki GUI definiują:

- `layers` — listę węzłów warstw GUI z możliwością zmiany kolejności;
- `materials` — listę węzłów materiałów.

Warstwy GUI można edytować przez właściwość `layers`, na przykład:

```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```

Można też zmieniać kolejność warstw:

```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```

Podobnie fonty, materiały, tekstury i particlefx są edytowane przez właściwości `fonts`, `materials`, `textures` i `particlefxs`:

```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.material"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```

Te właściwości nie obsługują zmiany kolejności.

Na końcu możesz też edytować węzły GUI przez listową właściwość `nodes`, na przykład:

```lua
editor.transact({
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-box",
        position = {20, 20, 20}
    }),
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-template",
        template = "/button.gui"
    }),
})
```

Wbudowane typy węzłów:

- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

Jeśli korzystasz z rozszerzenia Spine, możesz też używać typu `gui-node-type-spine`.

Jeżeli plik GUI definiuje layouty, możesz pobierać i ustawiać wartości z layoutów przez składnię `layout:property`, na przykład:

```lua
local node = editor.get("/main.gui", "nodes")[1]

-- ODCZYT:
local position = editor.get(node, "position")
pprint(position) -- {20, 20, 20}
local landscape_position = editor.get(node, "Landscape:position")
pprint(landscape_position) -- {20, 20, 20}

-- ZAPIS:
editor.transact({
    editor.tx.set(node, "Landscape:position", {30, 30, 30})
})
pprint(editor.get(node, "Landscape:position")) -- {30, 30, 30}
```

Właściwości layoutów, które zostały ustawione, można przywracać do wartości domyślnych przez `editor.tx.reset`:

```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```

Drzewa węzłów szablonu można odczytywać, ale nie można ich edytować — da się ustawiać tylko właściwości węzłów w drzewie szablonu:

```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (nadpisuje wartość z szablonu)
```

#### Edycja obiektów gry

Skrypty edytora potrafią edytować komponenty pliku obiektu gry. Komponenty występują w dwóch wariantach: referencyjne i osadzone. Komponenty referencyjne mają typ `component-reference` i działają jako odwołania do innych zasobów, pozwalając jedynie nadpisywać właściwości go zdefiniowane w skryptach. Komponenty osadzone mają typy takie jak `sprite`, `label` itd. i pozwalają edytować wszystkie właściwości właściwe dla danego typu komponentu, a także dodawać podkomponenty, na przykład kształty obiektów kolizji. Przykładowa konfiguracja obiektu gry:

```lua
editor.transact({
    editor.tx.add("/npc.go", "components", {
        type = "sprite",
        id = "view"
    }),
    editor.tx.add("/npc.go", "components", {
        type = "collisionobject",
        id = "collision",
        shapes = {
            {
                type = "shape-type-box",
                dimensions = {32, 32, 32}
            }
        }
    }),
    editor.tx.add("/npc.go", "components", {
        type = "component-reference",
        path = "/npc.script",
        id = "controller",
        __hp = 100 -- ustaw właściwość go zdefiniowaną w skrypcie
    })
})
```

#### Edycja kolekcji

Skrypty edytora potrafią też edytować kolekcje. Możesz dodawać obiekty gry (osadzone albo referencyjne) oraz kolekcje referencyjne. Na przykład:

```lua
local coll = "/char.collection"
editor.transact({
    editor.tx.add(coll, "children", {
        -- osadzony obiekt gry
        type = "go",
        id = "root",
        children = {
            {
                -- referencyjny obiekt gry
                type = "go-reference",
                path = "/char-view.go",
                id = "view"
            },
            {
                -- referencyjna kolekcja
                type = "collection-reference",
                path = "/body-attachments.collection",
                id = "attachments"
            }
        },
        -- osadzone obiekty gry mogą też zawierać komponenty
        components = {
            {
                type = "collisionobject",
                id = "collision",
                shapes = {
                    {type = "shape-type-box", dimensions = {2.5, 2.5, 2.5}}
                }
            },
            {
                type = "component-reference",
                id = "controller",
                path = "/char.script",
                __hp = 100 -- ustaw właściwość go zdefiniowaną w skrypcie
            }
        }
    })
})
```

Podobnie jak w edytorze, referencyjne kolekcje można dodawać tylko do korzenia edytowanej kolekcji, a obiekty gry można dodawać tylko do osadzonych albo referencyjnych obiektów gry, ale nie do referencyjnych kolekcji ani do obiektów gry wewnątrz takich kolekcji.

### Używanie poleceń powłoki

Wewnątrz `run` możesz zapisywać pliki przy użyciu modułu `io` i uruchamiać polecenia powłoki przez `editor.execute()`. Przy wykonywaniu poleceń możesz też przechwycić ich tekstowy wynik i użyć go dalej w kodzie. Jeśli na przykład chcesz dodać polecenie formatujące JSON przez globalnie zainstalowane [`jq`](https://jqlang.github.io/jq/), możesz napisać:

```lua
{
  label = "Format JSON",
  locations = {"Assets"},
  query = {selection = {type = "resource", cardinality = "one"}},
  action = function(opts)
    local path = editor.get(opts.selection, "path")
    return path:match(".json$") ~= nil
  end,
  run = function(opts)
    local text = editor.get(opts.selection, "text")
    local new_text = editor.execute("jq", "-n", "--argjson", "data", text, "$data", {
      reload_resources = false, -- nie przeładowuj zasobów, bo jq nie zapisuje nic na dysku
      out = "capture" -- zwróć tekstowy wynik zamiast braku wyniku
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```

Ponieważ to polecenie uruchamia program powłoki tylko do odczytu i informuje o tym edytor przez `reload_resources = false`, akcję nadal da się cofnąć.

::: sidenote
Jeśli chcesz dystrybuować skrypt edytora jako bibliotekę, możesz chcieć dołączyć binarny program dla platform edytora w ramach zależności. Więcej informacji znajdziesz w sekcji [Skrypty edytora w bibliotekach](#editor-scripts-in-libraries).
:::

## Hooki cyklu życia

Istnieje specjalnie traktowany plik skryptu edytora: `hooks.editor_script`, umieszczony w katalogu głównym projektu, obok pliku *game.project*. Tylko ten jeden skrypt edytora otrzymuje zdarzenia cyklu życia z edytora. Przykład:

```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```

Zdecydowaliśmy się ograniczyć hooki cyklu życia do jednego pliku skryptu edytora, ponieważ kolejność wykonywania kroków builda jest ważniejsza niż łatwość dodania kolejnego kroku. Polecenia są od siebie niezależne, więc kolejność wyświetlania ich w menu nie ma większego znaczenia — i tak użytkownik uruchamia konkretne wybrane polecenie. Gdyby hooki builda dało się definiować w wielu skryptach edytora, pojawiłby się problem: w jakiej kolejności miałyby działać? Prawdopodobnie chcesz wyliczać sumy kontrolne dopiero po skompresowaniu zawartości. Jeden plik, który jawnie ustala kolejność kroków builda przez wywoływanie odpowiednich funkcji, rozwiązuje ten problem.

Istniejące haki cyklu życia, które może zdefiniować `/hooks.editor_script`:

- `on_build_started(opts)` — wywoływany, gdy gra jest budowana do uruchomienia lokalnie albo na zdalnym urządzeniu przez Project Build lub Debug Start. Twoje zmiany pojawią się w zbudowanej grze. Wyrzucenie błędu z tego haka przerwie build. `opts` to tabela z kluczami:
  - `platform` — łańcuch w formacie `%arch%-%os%`, opisujący platformę docelową; obecnie zawsze taki sam jak `editor.platform`;
- `on_build_finished(opts)` — wywoływany po zakończeniu builda, niezależnie od wyniku. `opts` zawiera:
  - `platform` — to samo co w `on_build_started`;
  - `success` — `true` albo `false`, w zależności od tego, czy build zakończył się powodzeniem;
- `on_bundle_started(opts)` — wywoływany podczas tworzenia bundla albo budowania wersji HTML5. Podobnie jak `on_build_started`, zmiany wykonane przez ten hak trafią do bundla, a błędy przerwą proces. `opts` zawiera:
  - `output_directory` — ścieżkę do katalogu z wynikowym bundlem, na przykład `"/path/to/project/build/default/__htmlLaunchDir"`;
  - `platform` — platformę, dla której tworzony jest bundle. Listę możliwych wartości znajdziesz w [instrukcji Boba](/manuals/bob);
  - `variant` — wariant bundla: `"debug"`, `"release"` albo `"headless"`;
- `on_bundle_finished(opts)` — wywoływany po zakończeniu bundlowania, niezależnie od wyniku. `opts` zawiera te same dane co `on_bundle_started`, plus klucz `success`;
- `on_target_launched(opts)` — wywoływany, gdy użytkownik uruchomi grę i start zakończy się sukcesem. `opts` zawiera klucz `url` wskazujący uruchomioną usługę silnika, na przykład `"http://127.0.0.1:35405"`;
- `on_target_terminated(opts)` — wywoływany po zamknięciu uruchomionej gry; otrzymuje taki sam `opts` jak `on_target_launched`.

Pamiętaj, że hooki cyklu życia są obecnie funkcją dostępną wyłącznie w edytorze i nie są wykonywane przez Boba podczas bundlowania z wiersza poleceń.

## Serwery językowe

Edytor obsługuje podzbiór [Language Server Protocol](https://microsoft.github.io/language-server-protocol/). Docelowo chcemy rozszerzyć obsługę funkcji LSP, ale obecnie edytor potrafi tylko pokazywać diagnostykę (czyli linty) w edytowanych plikach oraz podpowiedzi.

Aby zdefiniować serwer językowy, edytuj funkcję `get_language_servers` w swoim skrypcie edytora na przykład tak:

```lua
function M.get_language_servers()
  local command = 'build/plugins/my-ext/plugins/bin/' .. editor.platform .. '/lua-lsp'
  if editor.platform == 'x86_64-win32' then
    command = command .. '.exe'
  end
  return {
    {
      languages = {'lua'},
      watched_files = {
        { pattern = '**/.luacheckrc' }
      },
      command = {command, '--stdio'}
    }
  }
end
```

Edytor uruchomi serwer językowy przy użyciu zdefiniowanego `command`, komunikując się z procesem przez standardowe wejście i wyjście.

Tabela definicji serwera językowego może zawierać:

- `languages` (wymagane) — listę języków, którymi serwer jest zainteresowany; identyfikatory są zdefiniowane [tutaj](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers), ale działają też rozszerzenia plików;
- `command` (wymagane) — tablicę z poleceniem i argumentami;
- `watched_files` — tablicę tabel z kluczami `pattern` (glob), które będą wyzwalały powiadomienie serwera o [zmianie obserwowanych plików](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles).

## Serwer HTTP

Każda uruchomiona instancja edytora ma aktywny serwer HTTP. Można go rozszerzać przy użyciu skryptów edytora. Aby dodać własne endpointy, zdefiniuj funkcję `get_http_server_routes`, która zwróci dodatkowe trasy:

```lua
print("My route: " .. http.server.url .. "/my-extension")

function M.get_http_server_routes()
  return {
    http.server.route("/my-extension", "GET", function(request)
      return http.server.response(200, "Hello world!")
    end)
  }
end
```

Po przeładowaniu skryptów edytora w konsoli zobaczysz komunikat podobny do `My route: http://0.0.0.0:12345/my-extension`. Po otwarciu tego linku w przeglądarce zobaczysz komunikat `"Hello world!"`.

Argument `request` jest prostą tabelą Lua z informacjami o żądaniu. Zawiera między innymi klucze `path` (segment ścieżki URL zaczynający się od `/`), `method` (na przykład `"GET"`), `headers` (tabela z nazwami nagłówków zapisanymi małymi literami), a opcjonalnie także `query` oraz `body`, jeśli dana trasa definiuje sposób interpretacji body. Na przykład endpoint przyjmujący body w formacie JSON definiuje się z konwerterem `"json"`:

```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```

Taki endpoint możesz przetestować w terminalu przez `curl` i `jq`:

```sh
curl 'http://0.0.0.0:12345/my-extension/echo-request?q=1' -X POST --data '{"input": "json"}' | jq
{
  "path": "/my-extension/echo-request",
  "method": "POST",
  "query": "q=1",
  "headers": {
    "host": "0.0.0.0:12345",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "user-agent": "curl/8.7.1",
    "content-length": "17"
  },
  "body": {
    "input": "json"
  }
}
```

Ścieżka trasy obsługuje wzorce, które można wyłuskać z request path i przekazać do handlera jako część obiektu request, na przykład:

```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```

Jeśli otworzysz adres taki jak `http://0.0.0.0:12345/my-extension/setting/project.title`, zobaczysz tytuł gry odczytany z pliku `/game.project`.

Poza wzorcami pojedynczego segmentu można też dopasowywać resztę ścieżki URL składnią `{*name}`. Na przykład prosty endpoint serwujący pliki z katalogu projektu może wyglądać tak:

```lua
http.server.route("/my-extension/files/{*file}", function(request)
  local attrs = editor.external_file_attributes(request.file)
  if attrs.is_file then
    return http.server.external_file_response(request.file)
  else
    return 404
  end
end)
```

Po otwarciu adresu takiego jak `http://0.0.0.0:12345/my-extension/files/main/main.collection` w przeglądarce zobaczysz zawartość pliku `main/main.collection`.

## Skrypty edytora w bibliotekach

Możesz publikować biblioteki zawierające polecenia dla innych użytkowników, a edytor wykryje je automatycznie. Haki nie mogą być jednak wykrywane automatycznie, bo muszą być zdefiniowane w pliku znajdującym się w katalogu głównym projektu, podczas gdy biblioteki udostępniają tylko podkatalogi. To celowe: użytkownik powinien mieć większą kontrolę nad procesem builda. Nadal możesz definiować haki cyklu życia jako zwykłe funkcje w plikach `.lua`, a użytkownicy biblioteki mogą je potem załadować i wykorzystać w swoim `/hooks.editor_script`.

Warto też pamiętać, że choć zależności są widoczne w Assets, nie istnieją jako zwykłe pliki — są wpisami w archiwum zip. Edytor potrafi jednak wypakować wybrane pliki z zależności do katalogu `build/plugins/`. W tym celu utwórz plik `ext.manifest` w katalogu biblioteki, a następnie katalog `plugins/bin/${platform}` w tym samym folderze, w którym znajduje się plik `ext.manifest`. Zawartość tego katalogu zostanie automatycznie wypakowana do `/build/plugins/${extension-path}/plugins/bin/${platform}`, dzięki czemu skrypty edytora będą mogły się do niej odwoływać.

## Preferencje

Skrypty edytora mogą definiować i używać preferencji, czyli trwałych, niezatwierdzonych danych przechowywanych na komputerze użytkownika. Preferencje mają trzy główne cechy:

- są typowane: każda preferencja ma definicję schematu zawierającą typ danych i dodatkowe metadane, takie jak wartość domyślna;
- mają zakres: preferencje są ograniczone albo do projektu, albo do użytkownika;
- są zagnieżdżone: każdy klucz preferencji jest łańcuchem rozdzielanym kropkami, gdzie pierwszy segment identyfikuje skrypt edytora, a kolejne opisują strukturę danej preferencji.

Wszystkie preferencje trzeba zarejestrować przez zdefiniowanie schematu:

```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```

Po przeładowaniu takiego skryptu edytor rejestruje schemat. Następnie skrypt może odczytywać i zapisywać preferencje, na przykład:

```lua
-- Pobierz konkretną preferencję
editor.prefs.get("my_json_formatter.indent.type")
-- Zwróci: "spaces"

-- Pobierz całą grupę preferencji
editor.prefs.get("my_json_formatter")
-- Zwróci:
-- {
--   jq_path = "",
--   indent = {
--     size = 2,
--     type = "spaces"
--   }
-- }

-- Ustaw wiele zagnieżdżonych preferencji naraz
editor.prefs.set("my_json_formatter.indent", {
    type = "tabs",
    size = 1
})
```

## Tryby wykonania

Środowisko uruchomieniowe skryptów edytora używa dwóch trybów wykonania, które w większości są przezroczyste dla samego skryptu: **immediate** i **long-running**.

Tryb **immediate** jest używany wtedy, gdy edytor potrzebuje odpowiedzi od skryptu możliwie natychmiast. Na przykład callbacki `active` poleceń menu są wykonywane w tym trybie, ponieważ sprawdzenia aktywności odbywają się w wątku UI edytora i muszą odświeżyć interfejs w tej samej klatce.

Tryb **long-running** jest używany wtedy, gdy odpowiedź nie musi być natychmiastowa. Na przykład callbacki `run` poleceń menu działają w trybie **long-running**, więc skrypt może poświęcić więcej czasu na wykonanie zadania.

Niektóre funkcje dostępne dla skryptów edytora mogą wykonywać się długo. Na przykład `editor.execute("git", "status", {reload_resources=false, out="capture"})` może w dużym projekcie działać nawet sekundę. Aby zachować responsywność i wydajność edytora, takich funkcji nie wolno używać w kontekstach wymagających natychmiastowej odpowiedzi. Próba użycia ich w takim kontekście zakończy się błędem: `Cannot use long-running editor function in immediate context`. Rozwiązaniem jest unikanie tych funkcji w trybie immediate.

Za długo działające uznawane są:

- `editor.create_directory()`, `editor.create_resources()`, `editor.delete_directory()`, `editor.save()`, `os.remove()` i `file:write()` — modyfikują pliki na dysku, przez co edytor musi zsynchronizować drzewo zasobów w pamięci ze stanem dysku, co w dużych projektach może trwać sekundy;
- `editor.execute()` — uruchamianie poleceń powłoki może zająć nieprzewidywalnie dużo czasu;
- `editor.transact()` — duże transakcje na szeroko referencjonowanych węzłach mogą trwać setki milisekund, co jest zbyt wolne dla responsywnego UI.

W trybie immediate działają:

- callbacki `active` poleceń menu — edytor potrzebuje odpowiedzi w tej samej klatce UI;
- kod wykonywany na najwyższym poziomie skryptów edytora — sam proces przeładowywania skryptów nie powinien powodować skutków ubocznych.

## Akcje

::: sidenote
Wcześniej edytor komunikował się z maszyną Lua w sposób blokujący, więc skrypty edytora nie mogły blokować działania edytora, bo część interakcji była wykonywana z wątku UI. Z tego powodu nie było na przykład `editor.execute()` ani `editor.transact()`. Uruchamianie skryptów i zmiany stanu edytora były wtedy inicjowane przez zwracanie tablicy "actions" z hooków i callbacków `run`.

Obecnie edytor komunikuje się z maszyną Lua w sposób nieblokujący, więc akcje nie są już potrzebne: korzystanie z funkcji takich jak `editor.execute()` jest wygodniejsze, krótsze i daje większe możliwości. Akcje są teraz **DEPRECATED**, choć nie planujemy ich usuwać.
:::

Skrypty edytora mogą zwracać tablicę akcji z funkcji `run` poleceń albo z hooków w `/hooks.editor_script`. Edytor wykona potem te akcje.

Action to tabela opisująca, co edytor ma zrobić. Każda akcja ma klucz `action`. Akcje występują w dwóch wariantach: z możliwością cofnięcia i bez możliwości cofnięcia.

### Akcje z możliwością cofnięcia

::: sidenote
Preferuj używanie `editor.transact()`.
:::

Akcję z możliwością cofnięcia można cofnąć po jej wykonaniu. Jeśli polecenie zwraca kilka akcji tego typu, zostaną wykonane i cofnięte razem. W miarę możliwości warto ich używać, choć są bardziej ograniczone.

Obecnie dostępne akcje z możliwością cofnięcia:

- `"set"` — ustawia właściwość węzła w edytorze na wybraną wartość. Przykład:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  Akcja `"set"` wymaga:
  - `node_id` — identyfikatora węzła jako userdata. Alternatywnie można podać ścieżkę zasobu, na przykład `"/main/game.script"`;
  - `property` — właściwości do ustawienia, na przykład `"text"`;
  - `value` — nowej wartości właściwości. Dla `"text"` powinna to być wartość typu string.

### Akcje bez możliwości cofnięcia

::: sidenote
Preferuj używanie `editor.execute()`.
:::

Akcja bez możliwości cofnięcia czyści historię cofania, więc jeśli chcesz ją odwrócić, musisz użyć innych metod, na przykład systemu kontroli wersji.

Obecnie dostępne akcje bez możliwości cofnięcia:

- `"shell"` — uruchamia skrypt powłoki. Przykład:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- usuń początkowy "/"
    }
  }
  ```
  Akcja `"shell"` wymaga klucza `command`, czyli tablicy z poleceniem i argumentami.

### Łączenie akcji i efektów ubocznych

Możesz mieszać akcje z możliwością cofnięcia i bez niej. Akcje są wykonywane sekwencyjnie, więc w zależności od kolejności możesz utracić możliwość cofnięcia części polecenia.

Zamiast zwracać akcje z funkcji, które ich oczekują, możesz też po prostu czytać i zapisywać pliki bezpośrednio przez `io.open()`. Spowoduje to przeładowanie zasobów, a to z kolei wyczyści historię cofania.
