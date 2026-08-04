---
title: Usługa silnika i interfejsy HTTP API czasu działania
brief: Ta instrukcja opisuje programistyczną usługę HTTP w uruchomionym silniku debugowania Defold i sposób jej wykorzystania przez rozszerzenia czasu działania lub narzędzia zewnętrzne.
---

# Usługa silnika i interfejsy HTTP API czasu działania {#the-engine-service-and-runtime-http-apis}

Uruchomienie projektu w trybie Debug tworzy proces konkretnej instancji silnika z grą oraz specjalną usługę silnika, która udostępnia infrastrukturę programistyczną i profilowania, logikę i wiadomości czasu działania, stan silnika oraz rozszerzenia.

Usługa silnika jest programistyczną usługą HTTP należącą do uruchomionego silnika debugowania (`dmengine`).

Jest oddzielona od [serwera edytora](/manuals/editor-http-api), który należy do edytora Defold i steruje otwartym projektem.

Obie usługi korzystają z różnych portów. Narzędzie połączone z portem edytora nie może wywoływać na nim tras rozszerzeń czasu działania i odwrotnie — narzędzie połączone z usługą silnika nie może wywoływać operacji edytora.

Usługa silnika stanowi część infrastruktury debugowania, tworzenia i profilowania. Instancje silnika w wersji wydaniowej nie tworzą tej usługi.

## Dostępność i wykrywanie portu {#availability-and-port-discovery}

Gdy edytor uruchamia silnik debugowania, żąda dynamicznie przypisanego portu usługi. Silnik zgłasza wybrany port w `Console` (`i w swoim logu, jeśli został uruchomiony z CLI):

![Informacja o porcie usługi silnika w buildzie debugowania Defold](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

Wiersz pojawia się w konsoli edytora, gdy gra została uruchomiona z edytora. Prosty kontroler lokalny może przeanalizować ten wiersz, ale integracja wielokrotnego użytku powinna pozwolić edytorowi lub narzędziu opakowującemu śledzić instancję silnika i zarejestrowany port. Pozwala to uniknąć pomylenia starego portu z nowo uruchomionym lub ponownie użytym procesem.

Silnik ogłasza też cele programistyczne za pomocą wykrywania usług na obsługiwanych platformach. Mechanizm ten jest używany przede wszystkim przez narzędzia Defold i nie należy zastępować go trwale zakodowanym portem.

Serwer jest dostępny na hoście lokalnym (`127.0.0.1`) pod określonym portem:

![Dostęp do serwera silnika](images/automation/engine-server.png)

## Wbudowane punkty końcowe {#built-in-endpoints}

Bieżący silnik debugowania rejestruje niewielki zestaw tras podstawowych.

| Punkt końcowy | Zastosowanie |
| --- | --- |
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

Trasa `/post` jest używana przez operacje programistyczne, takie jak szybkie przeładowanie, ponowne uruchamianie, zmiana rozmiaru i sterowanie procesem. Jej treść jest binarną wiadomością Protobuf typu podanego w trasie; nie jest to API wiadomości JSON.

Trasy te należą do infrastruktury programistycznej. Implementacja silnika zawiera też dodatkowe trasy profilera i sprawdzania zasobów.

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
Usługa silnika nie publikuje obecnie dokumentu OpenAPI. Integracje powinny ograniczać się do udokumentowanego zachowania lub wersjonowanego API rozszerzenia.
:::

Skrypty czasu działania, fizyka, wejście, dynamicznie tworzone obiekty i renderowanie charakterystyczne dla platformy wymagają uruchomionego silnika i powinny być weryfikowane przez [automatyczne testy czasu działania](/manuals/automated-testing).

* Nie należy udostępniać usługi przez router, interfejs publiczny ani niezaufany tunel.
* Nie należy zakładać, że trasy usługi silnika wymagają uwierzytelnienia.
* Trasy czasu działania mogą się różnić zależnie od wersji rozszerzenia, platformy, backendu graficznego i możliwości silnika.
* W przypadku aktualnych interfejsów API zdefiniowanych przez rozszerzenia należy uzgadniać wersję lub możliwości.
