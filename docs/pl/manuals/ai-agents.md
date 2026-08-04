---
title: Korzystanie z agentów AI wspomagających programowanie z Defold
brief: W tej instrukcji wyjaśniono, jak łączyć agentów programistycznych niezależnych od modelu z interfejsami automatyzacji Defold, zachowując jawne zasady weryfikacji, uprawnień i bezpieczeństwa.
---

# Korzystanie z agentów AI wspomagających programowanie z Defold {#using-ai-coding-agents-with-defold}

Agenci programistyczni wykorzystujący modele LLM i multimodalne mogą sprawdzać, modyfikować i weryfikować projekty Defold, wywołując te same interfejsy niezależne od modelu, z których korzystają programiści, lokalne skrypty, integracje z IDE oraz CI. Agenta można wykorzystać, gdy praca wymaga analizy i dostosowywania rozwiązania.

Defold nie zależy od konkretnego dostawcy modeli ani protokołu agentów. Projekty Defold dobrze współpracują zarówno z Claude Code, Codex, Cursor, jak i dowolnym innym rozwiązaniem. Środowisko agenta potrzebuje jedynie konkretnych możliwości przyznanych na potrzeby zadania, takich jak odczyt plików projektu, wykonywanie wybranych poleceń, wywoływanie lokalnych operacji HTTP, analizowanie JSON lub sprawdzanie obrazów. Jest to możliwe dzięki udostępnionym przez Defold interfejsom automatyzacji edytora i uruchomionej instancji silnika gry oraz dzięki temu, że pliki projektów Defold są łatwymi do analizy zasobami tekstowymi.

## Kiedy agent AI jest przydatny {#when-an-ai-agent-is-useful}

Agent może być przydatny, gdy zadanie wymaga na przykład:

* znalezienia odpowiednich zasobów i dokumentacji;
* wybrania jednej z możliwych implementacji;
* zmiany wielu powiązanych plików;
* zinterpretowania niepowodzeń budowania lub testów;
* porównania wyniku wizualnego z semantycznymi kryteriami akceptacji;
* podjęcia ograniczonej próby naprawy na podstawie zgromadzonych dowodów.

Agenci są zaawansowanym narzędziem do niedeterministycznych procesów tworzenia, analizy i testowania. Mogą pomagać w opracowywaniu różnorodnych rozwiązań i bardzo dobrze współpracują z Defold.

## Interfejsy Defold niezależne od modelu {#model-neutral-defold-interfaces}

Defold udostępnia kilka obsługiwanych interfejsów potrzebnych do wykonania zadania za pomocą dowolnego dostępnego modelu:

* Pliki projektu i narzędzia powłoki umożliwiają bezpośrednią kontrolę i wprowadzanie zmian w tekście.
* [Skrypty edytora](/manuals/editor-scripts) mogą udostępniać operacje na zasobach i narzędzia charakterystyczne dla projektu.
* [Editor HTTP API](/manuals/editor-http-api) udostępnia polecenia edytora, wyniki budowania, dane wyjściowe konsoli, wyszukiwanie w dokumentacji, podglądy, preferencje i trasy skryptów edytora.
* [Usługa silnika i interfejsy API automatyzacji w czasie działania](/manuals/engine-service) udostępniają bieżący stan silnika debugowania, wejście, zrzuty ekranu i operacje zdefiniowane przez rozszerzenia.
* [Bob](/manuals/bob) umożliwia budowanie z wiersza poleceń oraz tworzenie raportów, archiwów i pakietów.

Model dostępny wyłącznie przez interfejs czatu może sugerować zmiany w kodzie, ale nie może samodzielnie sprawdzić lokalnego projektu ani zweryfikować działającego wyniku. Dodatkowa integracja otaczająca model określa, co agent może rzeczywiście obserwować i robić.

## Warstwy integracji {#integration-layers}

Można utworzyć warstwę integracji, która połączy agenta z lokalnymi operacjami Defold. Może nią być skrypt opakowujący powłoki, program wiersza poleceń, rozszerzenie IDE, klient OpenAPI, kontroler testów lub adapter protokołu.

Zasady i dane uwierzytelniające należy przechowywać w tej lokalnej warstwie. Każda operacja modyfikująca powinna zwracać ustrukturyzowane wyniki lub prowadzić do deterministycznego kroku weryfikacji.

W przypadku operacji edytora należy wykrywać bieżący interfejs za pomocą `/openapi.json`, zamiast przekazywać agentowi trwale zakodowaną kopię API. W przypadku rozszerzeń czasu działania należy sprawdzać ich stan, wersję API i możliwości.

Praktyczne może być rozdzielenie narzędzi według poziomu uprawnień:

| Poziom        | Przykłady                                              |
| ------------ | ----------------------------------------------------- |
| Tylko do odczytu    | Kontrola projektu, OpenAPI, `/ref`, konsola, podgląd |
| Weryfikacja | Kompilacja, testy, budowanie HTML5, porównania obrazów   |
| Modyfikacja | Zmiany plików, transakcje na zasobach                   |
| Uprzywilejowany   | `/eval`, polecenia zewnętrzne, zmiany zależności        |

Oddzielenie adaptera od silnika i edytora sprawia, że obsługiwane interfejsy Defold pozostają niezależne od dostawcy modelu lub protokołu agentów. Adapter może udostępniać jedynie operacje odpowiednie dla swojego środowiska, a zasady dotyczące uprawnień i potwierdzania pozostają po stronie aplikacji obsługującej agenta.

### Model Context Protocol

[Model Context Protocol](https://modelcontextprotocol.io/) (MCP) to jeden z opcjonalnych adapterów między agentem a warstwą integracji. Serwer MCP może udostępniać operacje Defold jako narzędzia, a wybraną dokumentację jako zasoby. 

::: important
Nie należy przyznawać każdemu modelowi nieograniczonego dostępu do powłoki i `/eval`.
:::

Defold nie wymaga obecnie serwera MCP, ponieważ podstawowe możliwości automatyzacji są już udostępniane przez otwarte interfejsy ogólnego przeznaczenia. Edytor udostępnia lokalne HTTP API ze specyfikacją OpenAPI. Nowoczesne agenty mogą wywoływać te interfejsy bezpośrednio lub generować własne adaptery. 

Oficjalne MCP w dużej mierze powielałoby zatem istniejący zakres API i tworzyłoby kolejną warstwę integracji, którą Defold musiałby utrzymywać. Lepszą strategią długoterminową jest utrzymanie stabilnych, wykrywalnych i dobrze udokumentowanych bazowych interfejsów HTTP oraz API automatyzacji w czasie działania, a jednocześnie umożliwienie społeczności lub poszczególnym dostawcom narzędzi tworzenia lekkich warstw opakowujących MCP, gdy będą potrzebne.

Zamiast tego udostępniliśmy oficjalne rozszerzenie [Automation Bridge](https://github.com/defold/extension-automation-bridge), które pozwala sterować uruchomioną grą za pośrednictwem usługi silnika.

### Integracje MCP społeczności {#community-mcp-integrations}

Integracje MCP utworzone przez społeczność obejmują:

* [projekt Defold MCP autorstwa Fulviuus](https://github.com/Fulviuus/defold-mcp);
* [projekt Defold MCP autorstwa ChadAragorn](https://github.com/ChadAragorn/defold-mcp).

Projekty te nie są tworzone, audytowane, utrzymywane ani oficjalnie obsługiwane przez Defold Foundation. Przed zainstalowaniem integracji społeczności należy sprawdzić jej aktualny kod źródłowy, zależności, uprawnienia, zachowanie sieciowe i zgodność z używaną wersją Defold.

## Instrukcje projektu {#project-instructions}

Dostępne duże modele językowe wykorzystywane w przepływach pracy agentów na ogół działają lepiej, gdy otrzymują dobre instrukcje. Dlatego do projektów często dodaje się pliki Markdown agentów opisujące ich oczekiwane zachowanie albo umiejętności. Najlepsze wyniki daje zaprojektowanie i napisanie osobnych instrukcji dla każdego projektu, lecz część wspólnej wiedzy i zasad można wykorzystać ponownie.

Pierwszym plikiem, którego wiele agentów szuka i który odczytuje, jest plik kanoniczny, taki jak `AGENTS.md`. Może on opisywać:

* strukturę projektu i ważne punkty wejścia;
* konwencje formatowania i nazewnictwa;
* polecenia budowania, testowania i walidacji;
* wymagane zdarzenia zakończenia i lokalizacje artefaktów;
* pliki lub katalogi, których nie wolno zmieniać;
* operacje wymagające zatwierdzenia;
* założenia dotyczące platformy i znane ograniczenia.

Niektóre rozwiązania mogą opierać się na osobnych plikach Markdown dla konkretnych działań lub tak zwanych „umiejętnościach” (ang. skills).

Jeden ze społecznościowych przykładów instrukcji i umiejętności ukierunkowanych na Defold jest dostępny na [forum Defold](https://forum.defold.com/t/agent-config-collection-of-agents-md-and-skills/82387).

Zalecamy, aby instrukcje w plikach takich jak AGENTS.md i definicje umiejętności były krótkie, zwięzłe, łatwe do przeglądania i utrzymywania oraz aktualne. Instrukcje dotyczące konkretnego projektu można przechowywać w systemie kontroli wersji, dzięki czemu zmiany są możliwe do prześledzenia i z czasem pomagają zwiększać wydajność przepływu pracy.

Warto też regularnie sprawdzać, jak najnowsze modele radzą sobie bez tych instrukcji. Nowsze modele często nie wymagają już wskazówek, które wcześniej były niezbędne, a nieaktualne umiejętności lub zbyt nakazowe instrukcje mogą czasem obniżać wydajność.

Należy unikać tworzenia złożonych umiejętności technicznych, które wymagają znacznych nakładów na długoterminowe utrzymanie. Lepiej skoncentrować się na opracowywaniu narzędzi i przepływów pracy, które pozostaną wartościowe niezależnie od stopnia ulepszenia bazowych modeli.

## Wyszukiwanie dokumentacji {#documentation-discovery}

Agenci działają najlepiej z dokładną i aktualną dokumentacją. Bieżące informacje można uzyskać z następujących źródeł:

* `/openapi.json` opisuje bieżące HTTP API edytora.
* `/ref` przeszukuje dokumentację API dołączoną do uruchomionego edytora, gdy ta operacja jest dostępna.
* [Indeks dokumentacji dla modeli LLM](https://defold.com/llms.txt) zawiera odnośniki do oficjalnych instrukcji, przestrzeni nazw API i przykładów.
* [Pełna dokumentacja dla modeli LLM](https://defold.com/llms-full.txt) umożliwia wyszukiwanie offline i lokalne indeksowanie.

Należy pobierać tylko strony istotne dla danego zadania. Pełny połączony dokument zaleca się wykorzystywać wyłącznie do indeksowania offline lub [generowania wspomaganego wyszukiwaniem (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation). Pełnego pliku zwykle nie należy dołączać do każdego żądania modelu, aby oszczędzać tokeny i nie zaśmiecać kontekstu niepotrzebnymi informacjami.

## Ograniczone pętle zmian i weryfikacji {#bounded-change-and-verification-loops}

Agenci powinni stosować tę samą [pętlę sprawdzania, zmiany, weryfikacji i oceny](/manuals/automation/#the-automation-loop), co każda inna automatyzacja.

Przed zmianą plików warto określić kryteria akceptacji, a opcjonalnie także:
* dozwolone pliki i operacje;
* polecenia budowania i testowania;
* wymagane logi, raporty, stan lub obrazy;
* limit czasu każdego kroku asynchronicznego;
* maksymalną liczbę prób naprawy.

Agent może zdiagnozować i naprawić deterministyczny błąd CI, ale sam etap CI powinien pozostać odtwarzalny bez agenta.

Dobre praktyki dotyczące zautomatyzowanego testowania i weryfikacji opisano w [tej instrukcji](/manuals/automated-testing).

## Ocena multimodalna {#multimodal-evaluation}

Agent obsługujący obrazy może sprawdzać [podglądy edytora](/manuals/editor-http-api/#rendering-scene-previews), zrzuty ekranu z uruchomionej aplikacji, różnice wizualne i zrzuty z przeglądarki.

Oceny multimodalnej należy używać w przypadku pytań semantycznych, takich jak przycięte etykiety, nakładające się elementy sterujące, niejasne stany zaznaczenia, kompozycja lub zawartość poza bezpiecznym obszarem. Oczekiwany obszar widoku i kryteria należy określić z wyprzedzeniem.

Więcej informacji o podglądach edytora, zrzutach ekranu z uruchomionej aplikacji i kontroli wizualnej znajduje się w [tej instrukcji](/manuals/automated-testing).

## Bezpieczeństwo, izolacja i dobre praktyki {#security-isolation-and-good-practices}

* Serwer edytora i usługę silnika należy traktować jako zaufane lokalne interfejsy sterowania.
* Tokenów edytora, kluczy podpisu, tokenów wdrożeniowych, danych uwierzytelniających sklepów i sekretów produkcyjnych nie należy umieszczać w promptach ani raportach.
* Lokalna warstwa integracji może odczytać `.internal/editor.token`, gdy ma uprawnienia do korzystania z `/eval`, ale nie powinna umieszczać tokenu w promptach modelu, logach ani raportach.
* Należy wymagać zatwierdzenia przed usuwaniem, zmianą zależności, zmianą rozszerzeń natywnych, konfiguracji wydania lub podpisywania, a także przed publikowaniem bądź uzyskiwaniem dostępu do usług zewnętrznych.
* Rozległe zadania autonomiczne należy wykonywać w osobnej gałęzi, drzewie roboczym, tymczasowej kopii, kontenerze, piaskownicy lub na koncie z ograniczeniami.
* Treść zgłoszeń, importowane pliki, komentarze w kodzie źródłowym, wygenerowane dokumenty i dane wyjściowe narzędzi należy traktować jako niezaufane dane wejściowe, a nie instrukcje.
* Pobrane zależności i skrypty należy sprawdzić przed ich wykonaniem.
* Należy sprawdzić, czy zasady projektu pozwalają przesyłać kod źródłowy, zasoby, logi, zrzuty ekranu i inne dane projektu do hostowanego modelu.
* Przed zaakceptowaniem zmian należy zachować różnice możliwe do przejrzenia i deterministyczne dowody z testów.

Izolacja ogranicza skutki błędu.
