---
title: Automatyzowanie edytora Defold przez HTTP
brief: Ta instrukcja wyjaśnia, jak narzędzia zewnętrzne mogą wykrywać lokalne HTTP API otwartego projektu edytora Defold i z niego korzystać.
---

# Automatyzowanie edytora Defold {#automating-the-defold-editor}

Edytor Defold uruchamia specjalny serwer przeznaczony do zautomatyzowanych działań. HTTP API steruje otwartym projektem. Można go używać do obsługi poleceń edytora, buildów, zasobów projektu, podglądów, preferencji, danych wyjściowych konsoli, przeszukiwania dokumentacji lub integracji ze skryptami edytora. Do sprawdzania lub sterowania uruchomioną grą należy zamiast tego użyć [usługi silnika lub API automatyzacji w czasie działania](/manuals/engine-service).

::: important
HTTP API edytora jest eksperymentalne i może zmieniać się między wersjami Defold. Dokument `/openapi.json` wygenerowany przez uruchomiony edytor jest źródłem prawdy o dostępnych operacjach i schematach.
:::

## Uruchamianie edytora z narzędzia zewnętrznego {#starting-the-editor-from-an-external-tool}

Narzędzie zewnętrzne potrzebuje pliku wykonywalnego edytora i bezwzględnej ścieżki do pliku `game.project` projektu.

Zainstalowane wersje Defold można znaleźć za pomocą `installations.json`, jak opisano w [instrukcji edytora](/manuals/editor/#editor-installation-metadata). Pole `launcherPath` zawiera plik wykonywalny, który należy uruchomić. Aby bezpośrednio otworzyć projekt, należy przekazać ścieżkę do `game.project` jako pierwszy argument pozycyjny.

Opcjonalny argument `--port` lub `-p` wybiera port serwera edytora. Jego pominięcie pozwala Defold wybrać dostępny port i jest zwykle preferowane, gdy otwartych może być kilka projektów.

```sh
# Linux
/path/to/Defold/Defold --port 8181 /absolute/path/to/project/game.project
```

```sh
# macOS
/path/to/Defold.app/Contents/MacOS/Defold --port 8181 /absolute/path/to/project/game.project
```

```powershell
# Windows
C:\path\to\Defold\Defold.exe --port 8181 C:\absolute\path\to\project\game.project
```

Edytor jest graficzną aplikacją komputerową. Należy go uruchamiać w interaktywnej sesji użytkownika z dostępem do ekranu. Gdy sesja graficzna jest niedostępna, np. w CI bez interfejsu graficznego, lub w przypadku automatyzacji obejmującej wyłącznie kompilowanie i tworzenie samodzielnych pakietów należy użyć [Bob](/manuals/bob).

Po uruchomieniu edytora należy poczekać na otwarcie projektu i pojawienie się pliku `.internal/editor.port`. Następnie należy odpytywać `/openapi.json`, dopóki nie zwróci prawidłowego dokumentu. Nie należy zakładać, że utworzenie procesu oznacza gotowość projektu.

## Lokalizowanie serwera edytora {#locating-the-editor-server}

Gdy projekt jest otwarty, edytor uruchamia lokalny serwer HTTP. Aby otworzyć jego stronę główną w domyślnej przeglądarce, wybierz <kbd>Help ▸ Open Editor Server</kbd>:

![Strona główna lokalnego serwera edytora](images/automation/editor_server.png)

Wybrany port jest zapisywany w projekcie w pliku:

```text
.internal/editor.port
```

Od tego miejsca przykłady i polecenia w tej instrukcji będą odwoływać się do następujących zmiennych powłoki:

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"
```

Plik portu należy do bieżącej sesji edytora. Po ponownym uruchomieniu edytora należy odczytać go ponownie.

::: important
Serwer edytora jest zaufanym lokalnym interfejsem sterowania. Nie należy udostępniać go przez adres publiczny, przekierowanie portu ani niezaufany tunel.
:::

## Wykrywanie operacji za pomocą OpenAPI {#discovering-operations-through-openapi}

Jedynymi informacjami startowymi charakterystycznymi dla Defold, których powinno potrzebować narzędzie zewnętrzne, są port edytora i dokument OpenAPI:

```sh
curl -sS "http://127.0.0.1:$(cat .internal/editor.port)/openapi.json"
```

Zwrócony dokument OpenAPI 3.0.3 opisuje operacje obsługiwane przez uruchomioną wersję edytora, w tym ścieżki, metody, parametry, nazwy poleceń, formaty żądań, odpowiedzi, kody stanu i wymagania dotyczące uwierzytelniania.

Wyświetlenie udokumentowanych ścieżek:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[]'
```

Wyświetlenie dostępnych poleceń edytora:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '
    .paths["/command/{command}"].post.parameters[]
    | select(.name == "command")
    | .schema.enum[]
  '
```

Integracja uwzględniająca wersję powinna sprawdzać każdą wymaganą operację i konfigurować żądania na podstawie zwróconego schematu. Odradzamy utrzymywanie rzekomo kompletnej kopii nazw punktów końcowych lub poleceń, ponieważ może się zdezaktualizować.

Trasy zdefiniowane przez projekt również pojawiają się w `/openapi.json`, gdy ich skrypty edytora udostępniają opis operacji OpenAPI.

## Wykonywanie poleceń edytora {#executing-editor-commands}

Polecenia edytora są wywoływane przez:

```text
POST /command/{command}
```

Na przykład bieżące polecenie `build` kompiluje i uruchamia projekt:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build" |
  jq
```

Pomyślna kompilacja zwraca ustrukturyzowany wynik:

```json
{
  "success": true,
  "issues": []
}
```

Nieudana kompilacja zwraca stan HTTP `422` z problemami takimi jak:

```json
{
  "success": false,
  "issues": [
    {
      "message": "Example compiler message",
      "severity": "error",
      "resource": "/main/player.script",
      "range": {
        "start": {
          "line": 12,
          "character": 4
        },
        "end": {
          "line": 12,
          "character": 17
        }
      }
    }
  ]
}
```

Dostępne pola zależą od błędu. Należy korzystać ze ścieżki zasobu i zakresu kodu źródłowego, gdy są dostępne, ale również obsługiwać problemy zawierające tylko wiadomość.

Często przydatne polecenia, jeśli są wymienione przez uruchomiony edytor, obejmują:

`build`
: Kompiluje i uruchamia projekt.

`clean-build`
: Czyści pamięć podręczną budowania, a następnie kompiluje i uruchamia projekt. Należy go używać tylko wtedy, gdy zwykłe budowanie zachowuje się niespójnie lub zdaje się pomijać zmiany.

`build-html5`
: Buduje projekt dla HTML5 i udostępnia wynik przez serwer edytora.

`fetch-libraries`
: Pobiera i ponownie wczytuje zależności projektu.

`hot-reload`
: Ponownie wczytuje zmodyfikowane zasoby do uruchomionej gry.

`reload-extensions`
: Ponownie wczytuje skrypty edytora.

`debugger-start`, `debugger-stop` i polecenia krokowe debuggera
: Sterują sesją debugowania i uruchomionym projektem.

Dokładne nazwy i dostępność zależą od wersji edytora i jego bieżącego stanu; należy wykrywać je za pomocą `/openapi.json`.

Polecenia wykonujące operacje na zasobach projektu synchronizują zewnętrzne zmiany plików przed wykonaniem.

### Odpowiedzi poleceń i praca asynchroniczna {#command-responses-and-asynchronous-work}

Operacja polecenia dokumentuje kody odpowiedzi w bieżącym schemacie OpenAPI.

| Stan | Znaczenie |
| --- | --- |
| `200` | Polecenie zostało ukończone i zwróciło wynik |
| `202` | Polecenie zostało przyjęte i jest nadal wykonywane asynchronicznie |
| `403` | Polecenie nie jest aktywne w bieżącym stanie edytora |
| `404` | Polecenie nie jest dostępne |
| `422` | Budowanie lub walidacja nie powiodły się |
| `500` | Wystąpił wewnętrzny błąd edytora |

Odpowiedź HTTP `202` nie dowodzi, że żądany wynik istnieje. Należy poczekać na odpowiednie dane wyjściowe, zasób, znacznik konsoli lub udostępniany adres URL oraz wymusić limit czasu.

### Budowanie HTML5 {#building-html5}

Jeśli bieżący dokument OpenAPI wymienia `build-html5`, należy wywołać to polecenie za pomocą operacji polecenia:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build-html5"
```

Polecenie działa asynchronicznie i zwykle zwraca stan HTTP `202`. Po ukończeniu budowania edytor udostępnia wynik pod adresem:

```text
http://127.0.0.1:<editor-port>/html5/
```

Przed rozpoczęciem testów przeglądarkowych należy poczekać, aż adres URL stanie się dostępny. Więcej informacji zawiera sekcja [Testy przeglądarkowe dla HTML5](/manuals/automated-testing/#browser-tests-for-html5).

## Przeszukiwanie dokumentacji API {#searching-api-documentation}

Gdy operacja `/ref` jest obecna w `/openapi.json`, przeszukuje dokumentację API dołączoną do uruchomionej wersji edytora. Udostępnia nazwy i sygnatury pasujące do tej wersji.

Na przykład aby wyszukać funkcję, użyj:

```sh
curl -sS \
  --get \
  --data-urlencode "q=go.animate" \
  "$BASE_URL/ref" |
  jq
```

Filtrowanie według środowiska i języka:

```sh
curl -sS \
  --get \
  --data-urlencode "environment=runtime" \
  --data-urlencode "language=Lua" \
  --data-urlencode "q=collision message|raycast" \
  "$BASE_URL/ref" |
  jq
```

Parametry wyszukiwania to:

`environment`
: `editor`, `runtime` lub wartości rozdzielone przecinkami.

`language`
: `Lua`, `C`, `C++` lub wartości rozdzielone przecinkami.

`q`
: Wyrażenie bez rozróżniania wielkości liter. Białe znaki oznaczają AND, a `|` oznacza OR.

Dostępne są też skrócone zasoby dokumentacji: [indeks dokumentacji dla modeli LLM](https://defold.com/llms.txt) zawiera odnośniki do oficjalnych instrukcji, przestrzeni nazw API i przykładów, a [pełna dokumentacja dla modeli LLM](https://defold.com/llms-full.txt) obejmuje kompletną dokumentację do wyszukiwania offline i lokalnego indeksowania.

Agenci AI powinni jednak preferować konkretne wyszukiwania zamiast pobierania całej dokumentacji, gdy potrzebne jest tylko jedno API lub jedna wiadomość. Pozwala to oszczędzać tokeny i przygotować lepszy, czysty kontekst dla danego zadania.

## Odczytywanie danych wyjściowych konsoli {#reading-console-output}

Konsolę edytora można odczytać jako JSON:

```sh
curl -sS "$BASE_URL/console" | jq
```

Odpowiedź zawiera tekst konsoli w `lines` i regiony semantyczne w `regions`, w tym błędy, wyniki oceny i odwołania do zasobów.

Aby stale śledzić dane wyjściowe konsoli, użyj:

```sh
curl -N "$BASE_URL/console/stream"
```

Strumień zawiera istniejące wiersze konsoli, a następnie pozostaje otwarty dla nowych danych wyjściowych. Należy go zamknąć po otrzymaniu znacznika zakończenia lub błędu, wykryciu zakończenia procesu albo osiągnięciu limitu czasu lub liczby wierszy.

Informacje o ramkowaniu wyników testów i klasyfikacji niepowodzeń zawiera sekcja [Testowanie automatyczne i weryfikacja](/manuals/automated-testing/#structured-test-results).

## Renderowanie podglądów scen {#rendering-scene-previews}

Edytor Defold (od wersji 1.13.1) może wyrenderować „zrzut ekranu” obsługiwanego zasobu sceny do formatu PNG za pomocą polecenia `/preview/{path}`:

```sh
mkdir -p build/automation

curl -sS \
  "$BASE_URL/preview/main/main.collection?width=1280&height=720" \
  --output build/automation/main-preview.png
```

Powoduje to wyrenderowanie głównej kolekcji otwartego projektu z szablonu Basic 3D w domyślnym widoku początkowym:

![Podgląd głównej kolekcji wyrenderowany przez edytor](images/automation/main-preview.png)

Renderowania można używać do uzyskiwania podglądów zasobów korzystających z wizualnego edytora scen. Na przykład w ten sam sposób można wyrenderować komponent modelu, co pozwala sprawdzić jego wygląd lub poprawność shadera:

```sh
curl -sS \
  "$BASE_URL/preview/assets/models/cube.model?width=1280&height=720" \
  --output build/automation/cube-preview.png
```

![Podgląd modelu sześcianu wyrenderowany przez edytor](images/automation/cube-preview.png)

Ścieżka po `/preview/` nie zawiera początkowego ukośnika. Opcjonalne wymiary domyślnie odpowiadają rozmiarowi wyświetlania projektu i muszą mieścić się w zakresie od `1` do `4096`.

| Stan | Znaczenie |
| --- | --- |
| `200` | Podgląd został wyrenderowany |
| `400` | Wymiary są nieprawidłowe |
| `404` | Nie znaleziono zasobu |
| `422` | Zasób nie jest wczytany lub nie obsługuje podglądów sceny |

Podglądy mogą być bardzo przydatne do analizy wizualnej projektu: sprawdzania układów poziomów i GUI, konfiguracji shaderów i oświetlenia, regresji wizualnych lub tworzenia miniatur dokumentacji.

::: important
Podgląd edytora nie jest zrzutem ekranu uruchomionej gry. Nie weryfikuje dynamicznie tworzonych obiektów, post-processingu w czasie działania ani renderowania charakterystycznego dla platformy. Gdy te elementy są potrzebne, należy użyć [zrzutu ekranu z uruchomionej aplikacji](/manuals/automated-testing/#editor-previews-and-runtime-screenshots).
:::

## Wykonywanie kodu Lua edytora {#executing-editor-lua}

Uwierzytelniona operacja `POST /eval` wykonuje kod Lua w środowisku rozszerzeń edytora. Token bearer przypisany do sesji jest przechowywany w pliku:

```text
.internal/editor.token
```

Odczyt tokenu i wykonanie kodu:

```sh
TOKEN="$(cat .internal/editor.token)"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary 'print(editor.version) return editor.platform' \
  "$BASE_URL/eval"
```

Wydrukowane dane wyjściowe i zwracane wartości są zwracane jako tekst. Typowe odpowiedzi to:

| Stan | Znaczenie |
| --- | --- |
| `200` | Kod został wykonany |
| `401` | Brakuje tokenu bearer lub jest on nieprawidłowy |
| `422` | Nie udało się przeanalizować lub wykonać kodu Lua |
| `503` | Środowisko rozszerzeń edytora nie jest gotowe |

Klient może ponowić próbę po `503`, ale powinien ograniczyć liczbę prób. Przed powtórzeniem żądania, które zwróciło `422`, należy poprawić kod.

Wykonywany kod może używać [Editor API](https://defold.com/ref/editor-lua/) i środowiska skryptów edytora. Nie może korzystać z interfejsów API czasu działania gry, takich jak `go.*`, aby manipulować uruchomioną grą. Do obsługi rozgrywki należy użyć testu czasu działania, debuggera, testu przeglądarkowego lub [API automatyzacji w czasie działania](/manuals/engine-service/#automation-bridge-extension).

### Modyfikowanie zasobów i plików {#modifying-resources-and-files}

Wiele zasobów źródłowych Defold korzysta z formatów tekstowych i może być edytowanych za pomocą dowolnego narzędzia do edycji tekstu. W przypadku modyfikowania ustrukturyzowanych zasobów projektu Defold należy preferować transakcje edytora.

| Zmiana | Preferowana metoda |
| --- | --- |
| Lua, shader, JSON lub inny znany format tekstowy | Bezpośrednia modyfikacja pliku |
| Niezapisany tekst w otwartej karcie edytora | `editor.get()` i `editor.transact()` |
| Kolekcja, obiekt gry, GUI, atlas lub inny ustrukturyzowany zasób | Transakcja edytora |
| Wielokrotnie generowana zawartość | Samodzielny generator |
| Powtarzalna operacja na projekcie | Polecenie edytora lub własny punkt końcowy HTTP |
| Transformacja tylko dla CI | Samodzielny skrypt uruchamiany przed Bob |

Przed zmianą zasobu należy go sprawdzić:

```sh
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary '
    local path = "/game.project"
    pprint(editor.properties(path))
    return editor.get(path, "path")
  ' \
  "$BASE_URL/eval"
```

Przed wykonaniem transakcji należy sprawdzić `editor.can_get()`, `editor.can_set()` i pozostałe funkcje `editor.can_*()`.

Do uruchomienia programu formatującego, walidatora lub generatora w kodzie Lua edytora użyj `editor.execute()`:

```lua
local output = editor.execute(
  "python3",
  "scripts/generate_levels.py",
  {
    out = "capture"
  }
)

print(output)
```

Jeśli polecenie nie modyfikuje zasobów projektu, należy ustawić `reload_resources = false`, aby uniknąć niepotrzebnego ponownego wczytania.

::: important
Nie należy modyfikować plików w `.internal/` ani wygenerowanej zawartości w `build/`.
:::

## Preferencje

Preferencje edytora można odczytywać i zapisywać za pośrednictwem ścieżki udokumentowanej w OpenAPI, obecnie `/prefs/{path}`.

Można na przykład odczytać skonfigurowany rozmiar fontu kodu:

```sh
curl -sS "$BASE_URL/prefs/code/font/size" | jq
```

Można też ustawić go na przykład na 16:

```sh
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  --data '16' \
  "$BASE_URL/prefs/code/font/size"
```

Edytor sprawdza wartość względem swojego schematu preferencji. Nieprawidłowa ścieżka lub wartość zwraca stan HTTP `400`.

Preferencje to trwałe ustawienia użytkownika lub użytkownika projektu, a nie konfiguracja projektu przechowywana w `game.project`. Jeśli automatyzacja musi tymczasowo zmienić preferencję, powinna zapisać poprzednią wartość, a następnie ją przywrócić.

## Trasy zdefiniowane przez projekt {#project-defined-routes}

Skrypty edytora mogą definiować dodatkowe trasy za pomocą [`get_http_server_routes()`](/manuals/editor-scripts/#http-server). Opcjonalna tabela operacji OpenAPI udostępnia trasę za pośrednictwem tego samego dokumentu `/openapi.json`, co operacje wbudowane.

Trasy zdefiniowane przez projekt mogą zapewniać generowanie zawartości, walidację, raporty, kontrole lokalizacji, analizę zasobów, testy charakterystyczne dla projektu lub węższy interfejs dla IDE albo zewnętrznego kontrolera.

Dobra trasa powinna wykonywać jedną jasno nazwaną operację, sprawdzać swoje dane wejściowe, zwracać ustrukturyzowany wynik, w miarę możliwości być idempotentna i ograniczać kosztowne operacje.

Trasy zdefiniowane przez projekt nie są automatycznie chronione tokenem `/eval`. Gdy trasa wykonuje operacje wrażliwe, należy dodać uwierzytelnianie i kontrole bezpieczeństwa charakterystyczne dla projektu.

## Haki cyklu życia {#lifecycle-hooks}

Haki to funkcje, które mogą być uruchamiane przed budowaniem i po nim, przed utworzeniem pakietu i po nim oraz przy uruchamianiu lub kończeniu procesu gry. Projekt może zawierać jeden plik `hooks.editor_script` w swoim katalogu głównym. Tylko główny plik haków otrzymuje te zdarzenia, co zapewnia projektowi jedno miejsce do definiowania ich kolejności.

```lua
local M = {}

local function validate_project()
  print(editor.execute(
    "python3",
    "scripts/validate_project.py",
    {
      out = "capture",
      reload_resources = false
    }
  ))
end

function M.on_build_started(opts)
  validate_project()
end

function M.on_build_finished(opts)
  print("Build successful:", opts.success)
end

return M
```

Błąd zgłoszony przez `on_build_started()` zatrzymuje budowanie w edytorze. Haki cyklu życia działają tylko w edytorze; współdzieloną logikę walidacji i generowania należy umieścić w samodzielnych skryptach, które można też wywołać z CI.

## Bezpieczeństwo i zgodność {#security-and-compatibility}

Cały serwer edytora należy traktować jako zaufany interfejs lokalny:

* Nie należy publicznie udostępniać dostępu do portu.
* Należy chronić `.internal/editor.token`; autoryzuje on `/eval` w bieżącej sesji.
* Nie należy udostępniać na zewnątrz nieograniczonego dostępu do `/eval`.
* Token należy przechowywać w lokalnej warstwie integracji, a nie w promptach, raportach lub logach.
* Należy pamiętać, że trasy zdefiniowane przez projekt nie dziedziczą uwierzytelniania `/eval`.
* Należy korzystać z aktualnego `/openapi.json`.
* Należy stosować ograniczone oczekiwanie na automatyczne polecenia asynchroniczne i uruchomienie edytora.

## Serwer silnika {#engine-server}

Serwer edytora należy do procesu edytora. Uruchomiona gra korzysta z innego portu i ma inne zadania, opisane w [instrukcji usługi silnika i HTTP API czasu działania](/manuals/engine-service).
