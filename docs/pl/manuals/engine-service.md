---
title: Usługa silnika i interfejsy HTTP API czasu działania
brief: Ta instrukcja opisuje programistyczną usługę HTTP w uruchomionym silniku debugowania Defold i sposób jej wykorzystania przez rozszerzenia czasu działania lub narzędzia zewnętrzne.
---

# Usługa silnika i interfejsy HTTP API czasu działania {#the-engine-service-and-runtime-http-apis}

Uruchomienie projektu w trybie Debug tworzy proces konkretnej instancji silnika z grą oraz specjalną usługę silnika, która udostępnia infrastrukturę programistyczną i profilowania, logikę i wiadomości czasu działania, stan silnika oraz rozszerzenia.

Usługa silnika jest programistyczną usługą HTTP należącą do uruchomionego silnika debug lub headless (`dmengine` lub `dmengine_headless`).

Jest oddzielona od [serwera edytora](/manuals/editor-http-api), który należy do edytora Defold i steruje otwartym projektem.

Obie usługi korzystają z różnych portów. Narzędzie połączone z portem edytora nie może wywoływać na nim tras rozszerzeń czasu działania i odwrotnie — narzędzie połączone z usługą silnika nie może wywoływać operacji edytora.

Usługa silnika stanowi część infrastruktury debugowania, tworzenia i profilowania. Instancje silnika w wersji wydaniowej nie tworzą tej usługi.

## Dostępność i wykrywanie portu {#availability-and-port-discovery}

Gdy edytor uruchamia silnik debug, żąda dynamicznie przypisanego portu usługi. Silnik zgłasza wybrany port w *Console* oraz w swoim logu, gdy jest uruchamiany z CLI:

![Informacja o porcie usługi silnika w buildzie debugowania Defold](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

Silnik zapisuje również pełny adres URL dokumentu OpenAPI, używając rzeczywistego adresu i przypisanego portu:

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

Te wiersze pojawiają się w konsoli edytora, gdy gra została uruchomiona z edytora. Prosty kontroler lokalny może je przeanalizować, ale integracja wielokrotnego użytku powinna pozwolić edytorowi lub narzędziu opakowującemu śledzić instancję silnika i zarejestrowany port. Pozwala to uniknąć pomylenia starego portu z nowo uruchomionym lub ponownie użytym procesem.

Silnik ogłasza też cele programistyczne za pomocą wykrywania usług na obsługiwanych platformach. Mechanizm ten jest używany przede wszystkim przez narzędzia Defold i nie należy zastępować go trwale zakodowanym portem.

Serwer jest dostępny na hoście lokalnym (`127.0.0.1`) pod określonym portem:

![Dostęp do serwera silnika](images/automation/engine-server.png)

## Wykrywanie operacji przez OpenAPI {#discovering-operations-through-openapi}

`GET /openapi.json` zwraca dokument OpenAPI 3.0.3 opisujący API HTTP środowiska uruchomieniowego. Użyj portu usługi silnika z logu. Dla silnika lokalnego zastąp `<port>` poniżej tym portem:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

Dokument opisuje ścieżki, metody, parametry, treści żądań i odpowiedzi dostarczane przez aktualnie zarejestrowane procedury obsługi, w tym natywne rozszerzenia udostępniające metadane OpenAPI. Jego obiekt `paths` zmienia się przy dodawaniu lub usuwaniu procedur obsługi. Trasy profilera i rozszerzeń zależą od platformy, konfiguracji i zarejestrowanych rozszerzeń działającego silnika, dlatego pobieraj dokument z używanej instancji.

Procedury obsługi zarejestrowane bez metadanych OpenAPI nadal można wywoływać, ale nie pojawiają się w dokumencie. Udokumentowana trasa może też zgłaszać niedostępną funkcję; przed użyciem operacji zależnych od platformy sprawdź opisy odpowiedzi i ewentualny punkt końcowy dostępnych możliwości.

Edytor ma własny [dokument OpenAPI](/manuals/editor-http-api/#discovering-operations-through-openapi) na porcie edytora. Do operacji podczas działania gry używaj dokumentu silnika.

## Wbudowane punkty końcowe {#built-in-endpoints}

Bieżący silnik debugowania rejestruje niewielki zestaw tras podstawowych.

| Punkt końcowy | Zastosowanie |
| --- | --- |
| `GET /openapi.json` | Wykrywanie aktualnie zarejestrowanych operacji HTTP środowiska uruchomieniowego udostępniających metadane OpenAPI |
| `GET /ping` | Sprawdzenie, czy usługa silnika odpowiada |
| `GET /info` | Odczyt wersji silnika, platformy, identyfikatora kompilacji i informacji o usłudze logowania |
| `GET /state` | Odczyt stanu połączenia programistycznego używanego przez narzędzia Defold |
| `POST /post/<socket>/<message-type>` | Wysłanie wiadomości Defold zakodowanej w Protobuf do nazwanego socketu silnika |

Na przykład:

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

Trasa `/post` jest używana przez operacje programistyczne, takie jak szybkie przeładowanie, ponowne uruchamianie, zmiana rozmiaru i sterowanie procesem. Jej treść jest binarną wiadomością Protobuf typu podanego w trasie; nie jest to API wiadomości JSON. Zserializowana wiadomość Protobuf nie może być większa niż 1024 bajty; w przeciwnym razie zostanie zwrócona odpowiedź `400 Too large message`.

Trasy te należą do infrastruktury programistycznej. Implementacja silnika zawiera też dodatkowe trasy profilera i sprawdzania zasobów.

## Punkty końcowe nagrywania {#recording-endpoints}

Desktopowe silniki debug udostępniają również natywne nagrywanie MP4 przez poniższe trasy. Są one pomijane w buildach release, headless, mobilnych i webowych oraz po włączeniu **Exclude Record** w [manifeście aplikacji](/manuals/app-manifest/#exclude-record).

| Punkt końcowy | Zastosowanie |
| --- | --- |
| `GET /recording/capabilities` | Sprawdzenie obsługi wideo/dźwięku, wymagań backendu i `instance_id` usługi nagrywania |
| `GET /recording/status` | Odczyt bieżącej operacji, postępu asynchronicznego i informacji o sfinalizowanym pliku |
| `POST /recording/start` | Żądanie nagrywania i otrzymanie jego `operation_id` |
| `POST /recording/stop` | Żądanie zatrzymania i finalizacji wskazanej operacji |
| `GET /recording/files/{id}` | Pobranie sfinalizowanego MP4 |
| `DELETE /recording/files/{id}` | Usunięcie ukończonego pliku przechowywanego przez usługę |

Wykryj te trasy przez `/openapi.json`, a następnie sprawdź `/recording/capabilities`, aby ustalić obsługę na bieżącej platformie. Operacje zmieniające stan nagrywania wymagają nagłówka `X-Recording-Instance`, a zatrzymanie dodatkowo przyjętego `operation_id`. Start i zatrzymanie są asynchroniczne; przed pobraniem pliku zaczekaj na finalizację. Pełny przebieg opisano w [podręczniku nagrywania](/manuals/recording/#recording-through-http).

Usługa HTTP współdzieli rejestrator z Lua. Nagrania uruchamiane przez HTTP domyślnie włączają dźwięk aplikacji, jeśli jest obsługiwany; nagrania Lua domyślnie obejmują tylko wideo. Tylko nagrania uruchomione przez HTTP otrzymują opis pliku `file` umożliwiający pobranie. Przed pobraniem poczekaj na `pending: false`, `finalized: true` i `file.state: "complete"`, a następnie [zweryfikuj rozmiar pliku i SHA-256](/manuals/recording/#download-and-release-the-file). Przy łączeniu klientów Lua i HTTP zobacz [współdzielenie rejestratora](/manuals/recording/#sharing-the-recorder-with-http-clients).

## Punkt końcowy śladu GPU Metal {#metal-gpu-trace-endpoint}

W systemie macOS silniki debug udostępniają `/profiler/gputrace` do przechwytywania śladów GPU Metal. Trasa pojawia się w `/openapi.json` tylko w macOS. Przechwytywanie wymaga natywnego adaptera Metal i `METAL_CAPTURE_ENABLED=1` w środowisku uruchamiania silnika. Jeśli przechwytywanie jest niedostępne, żądanie zwraca HTTP 501 z `error.code: "gputrace_unsupported"`.

| Punkt końcowy | Zastosowanie |
| --- | --- |
| `POST /profiler/gputrace` | Zaplanowanie przechwytywania do zapisywalnej ścieżki bezwzględnej `.gputrace`; `frames` ma domyślną wartość `1` i może wynosić `1`–`10000`. |
| `GET /profiler/gputrace` | Odczyt stanu, ścieżki i liczników klatek bieżącego lub ostatniego przechwytywania. |
| `DELETE /profiler/gputrace` | Anulowanie oczekującego przechwytywania albo zakończenie aktywnego po bieżącej wyrenderowanej klatce; ślad pozostaje na dysku. |

Przyjęte żądania zwracają HTTP 200 z `ok: true` i obiektem `data`. Przechwytywanie postępuje asynchronicznie: odpytuj `GET`, aż `data.state` przyjmie `complete`, `canceled` lub `failed`. Błędy natywnego uruchomienia są zgłaszane w `data.error`. Ślad jest zapisywany na hoście silnika. [Przewodnik przechwytywania śladów GPU Metal](/manuals/profiling/#metal-gpu-trace-capture) zawiera polecenia uruchomienia, wykrywanie obsługi, przykłady przechwytywania i otwieranie wyniku w Xcode.

## Trasy czasu działania zdefiniowane przez rozszerzenia {#extension-defined-runtime-routes}

W wersjach debugowania SDK rozszerzeń natywnych może udostępniać serwer WWW silnika. Rozszerzenie może zarejestrować prefiks trasy na tym serwerze i udostępnić operacje zależne od danych czasu działania.

Jest to przydatne w przypadku narzędzi programistycznych, ponieważ rozszerzenie może współdzielić istniejącą usługę silnika, zamiast otwierać kolejny serwer HTTP.

API automatyzacji w czasie działania zdefiniowane przez rozszerzenie powinno:

* używać odrębnego, wersjonowanego prefiksu trasy;
* udostępniać obsługiwane możliwości;
* zwracać ustrukturyzowane błędy;
* jawnie obsługiwać niedostępne funkcje platformy lub silnika;
* ograniczać operacje do tworzenia i testowania;
* dokumentować, czy jest pomijane w wersjach wydaniowych.

### Publikowanie operacji rozszerzenia w OpenAPI {#publishing-extension-operations-in-openapi}

W wywołaniu zwrotnym inicjalizacji aplikacji rozszerzenia natywnego pobierz serwer przez `dmEngine::GetWebServer(app_params)` i rejestruj procedury obsługi tylko wtedy, gdy zwrócony uchwyt nie jest pusty. Konfigurację wywołania zwrotnego opisuje [cykl życia rozszerzenia](/manuals/extensions/#extension-lifecycle).

Czteroargumentowe przeciążenie `dmWebServer::AddHandler()` przyjmuje obiekt Paths Object OpenAPI 3.0.3 jako ciąg JSON. Kluczami najwyższego poziomu obiektu są ścieżki tras. Każda ścieżka musi zaczynać się od zarejestrowanego prefiksu i nie może być już udokumentowana przez inną procedurę obsługi. Używaj schematów zapisanych bezpośrednio lub odwołań do ścieżek w wynikowym dokumencie.

Na przykład ta funkcja pomocnicza rejestruje wywołanie zwrotne i opis jego punktu końcowego stanu:

```cpp
#include <dmsdk/dlib/webserver.h>

static const char STATUS_OPENAPI[] = R"json(
{
  "/example/v1/status": {
    "get": {
      "summary": "Get extension status",
      "responses": {
        "200": {
          "description": "Current extension status",
          "content": {
            "text/plain": {
              "schema": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
)json";

dmWebServer::Result RegisterStatusHandler(dmWebServer::HServer server,
                                        dmWebServer::Handler callback,
                                        void* context)
{
    dmWebServer::HandlerParams params;
    params.m_Handler = callback;
    params.m_Userdata = context;
    return dmWebServer::AddHandler(
        server, "/example/v1", &params, STATUS_OPENAPI);
}
```

Przekaż wywołanie zwrotne implementujące `GET /example/v1/status` i zwracające udokumentowaną odpowiedź `text/plain`. Wywołanie zwrotne nadal odpowiada za sprawdzanie ścieżek i metod żądań oraz tworzenie odpowiedzi. Sprawdzaj wynik rejestracji: nieprawidłowe lub sprzeczne metadane zwracają `dmWebServer::RESULT_ERROR_INVAL`.

Serwer zachowuje wskaźnik JSON bez kopiowania ciągu. Jego pamięć musi pozostać niezmieniona i ważna do usunięcia procedury obsługi przez `dmWebServer::RemoveHandler()` lub zniszczenia serwera. Tablica `static const char` w przykładzie spełnia ten wymóg. Usunięcie procedury obsługi usuwa też jej ścieżki z kolejnych odpowiedzi `/openapi.json`.

Trzyargumentowe przeciążenie `dmWebServer::AddHandler(server, prefix, &params)` nadal jest obsługiwane. Odpowiada przekazaniu `0` jako czwartego argumentu: procedura jest rejestrowana bez metadanych OpenAPI i pomijana podczas wykrywania.

## Rozszerzenie Automation Bridge {#automation-bridge-extension}

Oficjalne rozszerzenie Defold [Automation Bridge](https://github.com/defold/extension-automation-bridge) jest rozszerzeniem natywnym dostępnym wyłącznie w trybie debugowania i zbudowanym na usłudze silnika. Rejestruje ono wersjonowane API automatyzacji w czasie działania pod adresem:

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

Jego API czasu działania udostępnia między innymi sprawdzanie scen i węzłów, wejście, informacje o ekranie, zrzuty ekranu, nagrywanie, informacje o cyklu życia i opcjonalną synchronizację zdefiniowaną przez aplikację. Niektóre operacje to:

| Operacja | Działanie |
| --- | --- |
| `GET  /automation-bridge/v1/health` | raport o stanie, możliwości API i zgodność |
| `POST /automation-bridge/v1/input/click` | interakcje z wejściem w czasie działania |
| `GET  /automation-bridge/v1/screenshot` | zrzuty ekranu z uruchomionej aplikacji |

Należy korzystać z [dokumentacji natywnego API](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge) rozszerzenia i [dokumentacji pomocniczych narzędzi Python](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) dla wersji zainstalowanej w projekcie.

Automation Bridge nie udostępnia ani swojego HTTP API, ani modułu Lua w wersjach wydaniowych.

### Klienty edytora i środowiska uruchomieniowego {#editor-and-runtime-clients}

Pomocnicze narzędzia Python rozszerzenia Automation Bridge ilustrują architekturę dwóch klientów. Funkcja `editor.open_project()` zwraca klienta projektu edytora, a `project.build_and_run()` — osobnego klienta silnika.

| Klient | Zastosowanie |
| --- | --- |
| Project | HTTP API edytora, polecenia, debugger, konsola, preferencje, dokumentacja, podglądy, budowanie i wykrywanie portu |
| Game - engine service | Scena, wejście, zrzuty ekranu, stan w czasie działania i synchronizacja |

Podział na `project` i `game` uwidacznia granicę między procesami. Operacje edytora pozostają na serwerze edytora, a obserwacje i działania dotyczące uruchomionej gry — w usłudze silnika.

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## Ograniczenia i bezpieczeństwo {#limitations-and-security}

Usługa silnika i trasy zdefiniowane przez rozszerzenia są narzędziami programistycznymi i należy je w ten sposób traktować.

::: important
W wersji Defold 1.14.1 i nowszych używaj dokumentu `/openapi.json` działającego silnika do wykrywania operacji. Starsze silniki nie udostępniają tego punktu końcowego. Dla procedur obsługi zarejestrowanych bez metadanych OpenAPI korzystaj z wersjonowanej dokumentacji API rozszerzenia.
:::

Skrypty czasu działania, fizyka, wejście, dynamicznie tworzone obiekty i renderowanie charakterystyczne dla platformy wymagają uruchomionego silnika i powinny być weryfikowane przez [automatyczne testy czasu działania](/manuals/automated-testing).

* Nie należy udostępniać usługi przez router, interfejs publiczny ani niezaufany tunel.
* Nie należy zakładać, że trasy usługi silnika wymagają uwierzytelnienia.
* Trasy czasu działania mogą się różnić zależnie od wersji rozszerzenia, platformy, backendu graficznego i możliwości silnika.
* W przypadku aktualnych interfejsów API zdefiniowanych przez rozszerzenia należy uzgadniać wersję lub możliwości.
