---
title: Skrypty Edytora
brief: Ta instrukcja wyjaśnia, jak rozszerzać Edytor za pomocą Lua.
---

# Skrypty Edytora

Możesz tworzyć niestandardowe pozycje menu oraz rozszerzać cyklu życia Edytora, używając plików Lua o specjalnym rozszerzeniu: `.editor_script`. Dzięki temu systemowi możesz dostosować dowolnie Edytor, aby zwiększyć swoją wydajność w procesie tworzenia gier.

## Uruchamianie skryptów Edytora

Skrypty Edytora (editor scripts) działają wewnątrz Edytora, w maszynie wirtualnej Lua emulowanej przez maszynę wirtualną Java. Wszystkie skrypty współdzielą to samo środowisko, co oznacza, że mogą ze sobą współdziałać. Możesz wymagać (require) modułów Lua, tak samo jak w przypadku plików `.script`, ale wersja Lua uruchamiana wewnątrz Edytora jest inna, więc upewnij się, że twój współdzielony kod jest zgodny. Edytor używa wersji Lua 5.2.x, a dokładniej [silnika luaj](https://github.com/luaj/luaj), który jest obecnie jedynym dostępnym rozwiązaniem do uruchamiania Lua w JVM. Oprócz tego istnieją pewne ograniczenia:
- brak pakietów `debug` i `coroutine`;
- brak funkcji `os.execute` — zapewniamy bardziej przyjazny i bezpieczny sposób wykonywania skryptów powłoki (shell scripts) w sekcji "akcje" - [actions](#actions);
- brak funkcji `os.tmpname` i `io.tmpfile` — obecnie skrypty Edytora mają dostęp tylko do plików wewnątrz katalogu projektu;
- obecnie brak funkcji `os.rename`, choć zamierzamy ją dodać;
- brak funkcji `os.exit` i `os.setlocale`.

Wszystkie rozszerzenia Edytora zdefiniowane w skryptach Edytora są ładowane podczas otwierania projektu. Podczas pobierania bibliotek rozszerzenia są ponownie ładowane, ponieważ w bibliotekach, od których zależysz, mogą znajdować się nowe skrypty Edytora. Podczas tego ponownego ładowania nie są wykrywane żadne zmiany w twoich własnych skryptach Edytora, ponieważ mogłeś być w trakcie ich zmian. Aby również je ponownie załadować, musisz uruchomić komendę Project → Reload Editor Scripts (Przeładuj skrypty Edytora).

## Anatomia skryptu `.editor_script`

Każdy skrypt Edytora powinien zwracać moduł, na przykład:
```lua
local M = {}

function M.get_commands()
  -- TODO - define editor commands
end

function M.get_language_servers()
  -- TODO - define language servers
end

return M
```

Edytor zbiera wszystkie skrypty Edytora zdefiniowane w projekcie i bibliotekach, ładuje je do pojedynczej maszyny Lua i wywołuje je w odpowiednich momentach (więcej na ten temat w sekcjach "komendy": [commands](#commands) i "haki cyklu życia": [lifecycle hooks](#lifecycle-hooks)).

## Edytor API

Możesz komunikować się z Edytorem za pomocą pakietu `editor`, który definiuje to API:

- `editor.platform` — string oznaczający platformę: `"x86_64-win32"` dla systemu Windows, `"x86_64-macos"` dla macOS lub `"x86_64-linux"` dla systemu Linux.
- `editor.version` — string - nazwa wersji Defold, na przykład `"1.4.8"`.
- `editor.engine_sha1` — string - SHA1 silnika Defold.
- `editor.editor_sha1` — string - SHA1 Edytora Defold.
- `editor.get(node_id, property)` — pobierz wartość węzła (node) w Edytorze. Węzły w kontekście Edytora Defold to różne elementy, takie jak pliki skryptów, pliki kolekcji, obiekty gry w kolekcjach, pliki JSON wczytywane jako zasoby itp. `"node_id"` to userdata przekazywane do Skryptu Edytora przez sam Edytor. Możesz również podać ścieżkę zasobu zamiast identyfikatora węzła, na przykład `"/main/game.script"`. `"property"` to string. Obecnie obsługiwane są tylko te właściwości:
  - `"path"` — ścieżka pliku od katalogu projektu dla zasobów — elementów, które istnieją jako pliki. Przykład zwracanej wartości: `"/main/game.script"`
  - `"text"` — treść tekstowa zasobu edytowalna jako tekst (na przykład pliki skryptów lub pliki JSON). Przykład zwracanej wartości: `"function init(self)\nend"`. Należy zauważyć, że to nie jest to samo co odczytywanie pliku za pomocą `io.open()`, ponieważ możesz edytować plik bez zapisywania go, a te edycje są dostępne tylko podczas dostępu do właściwości `"text"`.
  - niektóre właściwości wyświetlane w widoku Properties (Właściwości), gdy coś jest zaznaczone w panelu Outline. Obsługiwane są następujące typy właściwości:
    - string - ciągi znaków
    - boolean - zmienne logiczne
    - number - liczby
    - vec2/vec3/vec4 - wektory
    - resource - zasoby
    
Należy zauważyć, że niektóre z tych właściwości mogą być tylko do odczytu (read-only), a niektóre mogą być niedostępne w różnych kontekstach, więc przed ich odczytaniem powinieneś użyć `editor.can_get`, a przed ich zmianą - `editor.can_set`, które zwrócą informację, czy daną właściwość można odczytać i czy można zmienić i zapisać. Najedź wskaźnikiem myszki na właściwość w panelu Properties (właściwości), żeby zobaczyć tooltop z informacją o jej nazwie w skryptach Edytora. Możesz ustawić właściwości zasobów jako `nil` używając pustej wartości `""`.
- `editor.can_get(node_id, property)` — sprawdź czy można odczytać daną właściwość w danym kontekście. Jeśli tak (true), to `editor.get()` nie zwróci błędu.
- `editor.can_set(node_id, property)` — sprawdź czy można zmienić i zapisać daną właściwość w danym kontekście. Jeśli tak (true), to akcja `"set"` na tej właściwości nie zwróci błędu.

## Komendy

Jeśli Skrypt Edytora definiuje funckję `get_commands`, to będzie one wywołana podczas przeładowania rozszerzenia i zwróci komendy możliwe do użycia w Edytorze w pasku menu lub w kontekstowym menu w panelach Assets i Outline. Przykład:

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
        return {
          {
            action = "set",
            node_id = opts.selection,
            property = "text",
            value = strip_comments(text)
          }
        }
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
        return {
          {
            action = "shell",
            command = {"./scripts/minify-json.sh", path:sub(2)}
          }
        }
      end
    }
  }
end

return M
```

Edytor oczekuje, że funkcja `get_commands()` zwróci tablicę tablic, z których każda opisuje osobne polecenie. Opis polecenia składa się z:

- `label` (wymagane) — tekst, który zostanie wyświetlony użytkownikowi jako pozycja w menu.
- `locations` (wymagane) — tablica zawierająca jedno z poniższych: `"Edit"`, `"View"`, `"Assets"` lub `"Outline"` - określa, w jakim miejscu Edytora menu powinno być dostępne. `"Edit"` i `"View"` oznaczają pasek menu na górze, `"Assets"` oznacza menu kontekstowe w panelu `"Assets"`, a `"Outline"` oznacza menu kontekstowe w panelu `"Outline"`.
- `query` — sposób, w jaki polecenie pyta Edytor o odpowiednie informacje i definiuje, na jakich danych operuje. Dla każdego klucza w tabeli `query` istnieje odpowiadający klucz w tabeli `opts`, który jest przekazywany jako argument do funkcji `active` i `run`. Obsługiwane klucze to:
  - `selection` — oznacza, że polecenie jest ważne, gdy coś w Edytorze jest zaznaczone, i działa na tym zaznaczeniu.
    - `type` — określa typ zaznaczonych węzłów, na które polecenie jest zainteresowane. Obecnie dozwolone są następujące rodzaje:
      - `"resource"` — w panelach `"Assets"` i `"Outline"` oznacza zaznaczony element, który ma odpowiadający plik. W pasku menu (`Edit` lub `View`), `"resource"` to aktualnie otwarty plik;
      - `"outline"` — coś, co może być wyświetlane w `"Outline"`. W `"Outline"` to zaznaczony element, w pasku menu to aktualnie otwarty plik;
    - `cardinality` — określa, ile zaznaczonych elementów powinno być. Jeśli jest to `"one"`, zaznaczenie przekazywane do funkcji obsługującej polecenie będzie zawierać tylko jeden identyfikator węzła. Jeśli jest to `"many"`, przekazywana tablica będzie zawierać jeden lub więcej identyfikatorów węzła.
- `active` - funkcja wywoływana w celu sprawdzenia, czy polecenie jest aktywne, powinna zwracać wartość logiczną. Jeśli w locations zawarte są `"Assets"` lub `"Outline"`, funkcja `active` zostanie wywołana podczas wyświetlania menu kontekstowego. Jeśli w `locations` zawarte są `"Edit"` lub `"View"`, funkcja `active` zostanie wywołana przy każdej interakcji użytkownika, takiej jak pisanie na klawiaturze lub klikanie myszą, dlatego upewnij się, że funkcja `active` działa stosunkowo szybko.
- `run` - funkcja wywoływana, gdy użytkownik wybierze pozycję z menu, i powinna zwrócić tablicę akcji - [actions](#actions).

## Actions

Action (akcja) to tabela opisująca, co Edytor powinien zrobić. Każda akcja zawiera klucz `action`. Akcje dzielą się na dwa rodzaje: możliwe do cofnięcia (undoable) i niemożliwe do cofnięcia (non-undoable).

### Akcje możliwe do cofnięcia

Undoable action - możliwa do cofnięcia akcja może zostać cofnięta po jej wykonaniu (Undo or Ctrl + Z). Jeśli polecenie zwraca wiele akcji możliwych do cofnięcia, są one wykonywane razem i cofane razem. Należy używać akcji możliwych do cofnięcia, jeśli to możliwe. Ich wadą są większe ograniczenia.

Istniejące działania możliwe do cofnięcia to:

- `"set"` — ustawienie właściwości węzła w Edytorze na określoną wartość. Przykład:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
Akcja `"set"` wymaga podania tych parametrów:
  - `node_id` — identyfikator węzła jako userdata. Alternatywnie, można użyć ścieżki zasobu zamiast identyfikatora węzła otrzymanego od Edytora, na przykład `"/main/game.script"`;
  - `property` — właściwość węzła do ustawienia, obecnie obsługiwane jes tylko `"text"`;
  - `value` — nowa wartość właściwości. Dla właściwości `"text"` powinno to być łańcuchem znaków (string).

### Akcje niemożliwe do cofnięcia

Akcje możliwe do cofnięcia czyszczą historię cofnięć (undo), więc z poziomu Edytora nie można ich cofnąć i jeśli użytkownik chce to zrobić, musi użyć innych środków, np. systemów kontroli wersji.

Istniejące działania niemożliwe do cofnięcia to:
- `"shell"` — wykonanie skryptu powłoki. Przykład:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- trim leading "/"
    }
  }
  ```
Działanie `"shell"` wymaga parametru `command`, który jest tablicą polecenia, oraz jego argumentów. Główna różnica w porównaniu do `os.execute` polega na tym, że jest to potencjalnie niebezpieczna operacja, dlatego Edytor wyświetli okno dialogowe z pytaniem do użytkownika czy na pewno chce wywołać daną komendę. Edytor zapamięta, jeśli użytkownik już wyraził zgodę na wykonanie takiej komendy.

### Łączenie akcji i efekty uboczne

Możesz łączyć akcje możliwe do cofnięcia (undoable) i akcje niemożliwe do cofnięcia (non-undoable). Akcje są wykonywane sekwencyjnie, dlatego w zależności od kolejności działań możesz stracić możliwość cofania części tego polecenia.

Zamiast zwracać akcje z funkcji, które ich oczekują, możesz po prostu czytać i zapisywać dane bezpośrednio do plików, korzystając z funkcji `io.open()`. Spowoduje to ponowne załadowanie zasobów, co wyczyści historię cofania (undo history).

## Haki cyklu życia (Lifecycle Hooks)

Istnieje jeden, specjalnie traktowany plik Skryptu Edytora: `hooks.editor_script`, znajdujący się w głównym katalogu twojego projektu, w tym samym katalogu co `game.project`. Tylko ten plik Skryptu Edytora otrzyma zdarzenia cyklu życia od Edytora. Oto przykład takiego pliku:

```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write("{\"build_time\": \"".. os.date() .."\"}")
  file:close()
end

return M
```

Zdecydowaliśmy się ograniczyć haki cyklu życia do jednego pliku Skryptu Edytora, ponieważ kolejność wykonywania haków budowania (build hooks) jest ważniejsza niż łatwość dodawania kolejnego kroku buildu. Polecenia są niezależne od siebie, więc nie ma znaczenia, w jakiej kolejności są wyświetlane w menu. W końcu to użytkownik wykonuje konkretne polecenie, które wybrał. Gdyby można było określać haki cyklu życia w różnych plikach Skryptu Edytora, stworzyłoby to problem: w jakiej kolejności mają się wykonywać haki? Chcesz prawdopodobnie utworzyć sumy kontrolne zawartości po jej skompresowaniu... Dlatego posiadanie jednego pliku, który ustala kolejność kroków buildu, wywołując każdą funkcję kroku, jest sposobem na rozwiązanie tego problemu.

Każdy hak cyklu życia może zwracać akcje lub zapisywać pliki w katalogu projektu.

Istniejące haki cyklu życia, które plik `hooks.editor_script` może określić:
- `on_build_started(opts)` — wykonywane, gdy gra jest budowana w celu uruchomienia jej lokalnie lub na zdalnym, docelowym urządzeniu, używając opcji `"Project Build"` lub `"Debug Start"`. Twoje zmiany, czy to zwracane akcje czy zaktualizowane zawartości pliku, pojawią się w zbudowanej grze. Wyrzucenie błędu z tego haka spowoduje przerwanie budowy. `opts` to tabela zawierająca obecnie następujący klucz:
  - `platform` — łańcuch w formacie `%arch%-%os%`, opisujący platformę, dla której budowana jest gra, zawsze taki sam jak `editor.platform`.
- `on_build_finished(opts)` — wykonywane, gdy budowa zostanie zakończona, niezależnie od tego, czy zakończyła się sukcesem czy nie. `opts` w tym przypadku to tabela zawierająca następujące klucze:
  - `platform` — to samo, co w `on_build_started`.
  - `success` — czy budowa zakończyła się sukcesem, true lub false.
- `on_bundle_started(opts)` — wykonywane, gdy tworzysz paczkę z grą lub budujesz wersję HTML5 gry. Podobnie jak `on_build_started`, zmiany wywołane przez ten hak pojawią się w paczce, a błędy spowodują przerwanie procesu pakowania (bundle). `opts` zawiera tutaj następujące klucze:
  - `output_directory — ścieżka do katalogu wyjściowego paczki, na przykład `"/path/to/project/build/default/__htmlLaunchDir"`
  - `platform` — platforma, dla której paczka jest tworzona. Zobacz listę możliwych wartości platform w podręczniku Boba (narzędzia do budowania i pakowania).
  - `variant` — wariant paczki, `"debug"`, `"release"` lub `"headless"`.  
- `on_bundle_finished(opts)` — wykonywane, gdy budowanie paczki (bundle) zostanie ukończone, niezależnie od tego, czy zakończyło się sukcesem. `opts` w tym przypadku to tabela zawierająca te same dane co `opts` w `on_bundle_started`, oraz dodatkowo klucz `success`, który wskazuje, czy budowa zakończyła się sukcesem.
  - `on_target_launched(opts)` — wykonywane, gdy użytkownik uruchomił grę i uruchomienie zakończyło się sukcesem. `opts` zawiera klucz `url` wskazujący na uruchomioną usługę silnika, na przykład `"http://127.0.0.1:35405"`.
  - `on_target_terminated(opts)` — wykonywane, gdy uruchomiona gra zostaje zamknięta. `opts` ma te same klucze co `on_target_launched`.

Należy zauważyć, że haki cyklu życia są obecnie funkcją dostępną tylko w Edytorze i nie są wykonywane przez Boba podczas pakowania z wiersza poleceń.

## Skrypty Edytora w bibliotekach

Możesz publikować biblioteki dla użytku przez inne osoby, które zawierają polecenia, i zostaną one automatycznie wykryte przez Edytor. Haki cyklu życia nie mogą być jednak automatycznie wykrywane, ponieważ muszą być zdefiniowane w pliku znajdującym się w głównym katalogu projektu, a biblioteki wystawiają tylko podkatalogi. Ma to na celu umożliwienie większej kontroli nad procesem budowy: nadal możesz tworzyć haki cyklu życia jako proste funkcje w plikach `.lua`, więc użytkownicy twojej biblioteki mogą je zaimportować i używać w swoim pliku `hooks.editor_script`.

Należy również zauważyć, że chociaż zależności są wyświetlane w widoku `"Assets"`, to nie istnieją one jako pliki (są wpisami w archiwum zip), więc obecnie nie ma łatwego sposobu na wykonanie skryptu powłoki dostarczonego jako zależności (biblioteki). Jeśli jest to absolutnie konieczne, będziesz musiał wydobyć dostarczone skrypty, pobierając ich tekst za pomocą `editor.get()` i zapisując go gdzieś za pomocą `file:write()`, na przykład w katalogu `build/editor-scripts/your-extension-name`.

Prostszym sposobem na wydobycie niezbędnych plików jest wykorzystanie systemu wtyczek rozszerzeń natywnych (native extensions). Aby to zrobić, musisz utworzyć plik `ext.manifest` w katalogu twojej biblioteki, a następnie utworzyć katalog `plugins/bin/${platform}` w tym samym katalogu, w którym znajduje się plik `ext.manifest`. Pliki w tym katalogu zostaną automatycznie wydobyte do katalogu `/build/plugins/${extension-path}/plugins/bin/${platform}`, dzięki czemu twoje Skrypty Edytora mogą się do nich odnosić.

## Serwery językowy (language servers)

Edytor obsługuje niewielki podzbiór protokołu [Language Server Protocol](https://microsoft.github.io/language-server-protocol/). Chociaż zamierzamy rozwijać obsługę Edytora dla funkcji LSP w przyszłości, obecnie obsługuje on tylko wykrywanie diagnoz (lints) w edytowanych plikach.

Aby zdefiniować serwer językowy, musisz edytować funkcję `get_language_servers` w swoim Skrypcie Edytora, jak w poniższym przykładzie:


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

Edytor uruchomi serwer językowy, korzystając z określonej komendy, używając standardowego wejścia i wyjścia procesu serwera do komunikacji.

Tabela definicji serwera językowego może określać:

- `languages` (wymagane) — listę języków, których serwer dotyczy, zdefiniowanych [tutaj](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers)  (rozszerzenia plików także działają);
- `command` (wymagane) - tablicę komendy i jej argumentów
- `watched_files` - tablicę tablic z kluczami `pattern` (glob), które będą powiadomiać serwer o zmianie plików, zgodnie z powiadomieniami o [zmianie plików śledzonych](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles).
