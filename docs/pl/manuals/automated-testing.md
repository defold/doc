---
title: Testowanie automatyczne i weryfikacja
brief: Ta instrukcja wyjaśnia, jak projektować, uruchamiać i raportować deterministyczne testy Defold lokalnie, w uruchomionej grze, w przeglądarkach i w ramach ciągłej integracji.
---

# Testowanie automatyczne i weryfikacja {#automated-testing-and-verification}

Testowanie automatyczne weryfikuje kod i zawartość Defold za pomocą jednoznacznych dowodów w formacie czytelnym dla maszyn. Ta instrukcja pomaga projektować testy, które działają zarówno z lokalnymi skryptami, mechanizmami wykonawczymi CI (Continuous Integration), jak i agentami programistycznymi. Obejmuje testy modułów, uruchamiane kolekcje, testy przeglądarkowe, automatyzację w czasie działania, kontrole wizualne i kompilacje bez interfejsu graficznego, a także przedstawia przydatne dobre praktyki.

## Poziomy weryfikacji {#verification-levels}

Dobre poziomy testowania automatycznego odpowiadają strukturze piramidy testów, która dzieli testy na trzy główne warstwy: testy jednostkowe, integracyjne i kompleksowe (end-to-end, E2E). W Defold testy można rozdzielić na określone kolekcje, które mogą być ładowane jako kolekcja startowa. Zwykle najlepiej rozpocząć od najbardziej zawężonej i najszybszej kontroli, która może wykryć problem, a następnie w razie potrzeby dodać testy czasu działania lub testy platformowe.

| Poziom | Odpowiednie dowody |
| --- | --- |
| Walidacja statyczna | Parser, program formatujący, walidator zasobów lub porównanie wygenerowanych plików |
| Test modułu | Wyniki asercji dla logiki Lua wielokrotnego użytku z minimalnymi zależnościami od silnika |
| Uruchomiona kolekcja | Wiadomości, komponenty, wejście, fizyka, cykl życia i zachowanie silnika |
| Automatyzacja w czasie działania | Bieżący stan sceny, wstrzyknięte wejście, stan aplikacji i zrzuty ekranu z uruchomionej aplikacji |
| Test przeglądarkowy HTML5 | Wejście obszaru canvas, integracja z przeglądarką, zachowanie obszaru widoku i dane wyjściowe WWW |
| Test platformowy | Zachowanie i renderowanie na rzeczywistej platformie docelowej |
| Budowanie i tworzenie pakietu | Stan wyjścia Bob, raport z budowania, archiwum i artefakty pakietu |

Pomyślna kompilacja dowodzi, że projekt się buduje, ale nie dowodzi prawidłowego zachowania rozgrywki. Zrzut ekranu nie potwierdza złożonych przejść, animacji, interakcji ani przebiegu rozgrywki, lecz nowoczesne rozwiązania multimodalne mogą go wykorzystać do sprawdzenia wyglądu pojedynczej klatki oraz poprawności shaderów i układu wizualnego. W testach automatycznych należy jednak preferować deterministyczne asercje zawsze wtedy, gdy warunek można wyrazić bezpośrednio.

## Kod Lua wielokrotnego użytku i łatwy do testowania {#reusable-and-testable-lua-code}

Logikę wielokrotnego użytku należy przechowywać w modułach Lua z minimalnymi zależnościami od silnika. Dzięki temu czyste transformacje danych, reguły, maszyny stanów i obliczenia można sprawdzać bez tworzenia kompletnego świata gry.

Kod zależny od silnika należy oddzielić od wywoływanej przez niego logiki. Skrypt może przekładać wiadomości i stan komponentów na wywołania modułu, natomiast testy mogą wywoływać moduł bezpośrednio z kontrolowanymi danymi wejściowymi.

Więcej informacji zawiera [instrukcja pisania kodu](/manuals/writing-code).

## Testy w uruchomionej kolekcji {#tests-in-a-running-collection}

Gdy zachowanie zależy od obiektów gry, komponentów, wiadomości, wejścia, fizyki lub innych systemów silnika, należy użyć specjalnej kolekcji testowej.

Każdy test powinien:

1. ustanowić znany stan;
2. wykonać jedno zachowanie;
3. sprawdzić i ocenić oczekiwany wynik;
4. uprzątnąć utworzone zasoby;
5. wysłać ustrukturyzowany opis wyniku.

W testach najlepiej używać izolowanych kolekcji testowych. Projekt może wybrać kolekcję testową jako tymczasową kolekcję startową za pomocą ustawienia w `game.project`:

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

Nie należy pozostawiać tymczasowej testowej kolekcji startowej w zwykłej konfiguracji projektu. W CI najlepiej użyć osobnego pliku ustawień przekazanego do Bob. CI nie może zmieniać stanu repozytorium; w razie potrzeby powinien wprowadzać wyłącznie zmiany tymczasowe.

W przypadku złożonych gier można tworzyć małe kolekcje „pomieszczeń programistycznych” ze wstępnie zdefiniowanymi scenariuszami i prostymi makietami. Zapewniają one odtwarzalność mechanik i ułatwiają testowanie podczas tworzenia bez konieczności przechodzenia przez niepowiązane stany i sekcje gry.

### Frameworki testowe {#test-frameworks}

W projekcie można zaimplementować niewielki mechanizm wykonawczy albo skorzystać ze [społecznościowej biblioteki testowej](https://defold.com/assets/?tag=testing).

Na przykład [DefTest](https://defold.com/assets/deftest/) to biblioteka testów jednostkowych oparta na Telescope. Obsługuje zestawy testów, funkcje konfiguracji i sprzątania, asercje, filtrowanie według nazw, atrapy wybranych interfejsów API Defold oraz opcjonalne pokrycie LuaCov. Testy można uruchamiać ze specjalnej kolekcji startowej, również w pakiecie bez interfejsu graficznego utworzonym za pomocą Bob.

## Ustrukturyzowane wyniki testów {#structured-test-results}

Podsumowanie frameworka w konsoli lub logu może być przydatne dla programistów, ale nienadzorowany automatyczny kontroler nadal potrzebuje jednoznacznego wyniku zakończenia. W razie potrzeby należy dodać mały adapter otaczający funkcję zwrotną lub podsumowanie frameworka, aby kontroler mógł łatwo przetworzyć wyniki testów.

Prosty opis wyników może używać unikalnego prefiksu, po którym w każdym fizycznym wierszu konsoli występuje jeden obiekt JSON:

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

Kolektor powinien przetwarzać każdy wiersz niezależnie, znajdować prefiks `TEST`, analizować następujący po nim JSON i ignorować niepowiązane dane wyjściowe silnika.

Należy dołączyć unikalny identyfikator uruchomienia, aby dane wyjściowe starego lub równoległego procesu nie mogły zakończyć bieżącego uruchomienia. Każdy zestaw powinien wysłać jedno jednoznaczne zdarzenie końcowe (np. `Pass`, `Failure`, `Crash`, `Timeout` itd.).

### Zbieranie danych wyjściowych konsoli {#collecting-console-output}

Gdy gra jest uruchamiana z edytora, udostępnia zarówno bieżącą historię konsoli, jak i ciągły strumień. Strumień należy zamknąć po znalezieniu pasującego zdarzenia zakończenia zestawu, zakończeniu procesu, wystąpieniu błędu albo osiągnięciu skonfigurowanego limitu czasu lub liczby wierszy.

Więcej informacji znajduje się w [instrukcji Editor HTTP API](/manuals/editor-http-api/#reading-console-output).

### Utrwalone logi {#persisted-logs}

Defold może też zapisywać log gry po włączeniu `Write Log File` w `game.project`. Zobacz [Logi gry i systemu](/manuals/debugging-game-and-system-logs/). Rejestrowanie do pliku jest przydatne w przypadku spakowanych aplikacji i testowania urządzeń docelowych, na których konsola edytora jest niedostępna.

Projekt może korzystać z wbudowanych funkcji `print()` i `pprint()` albo na przykład z dowolnej innej [biblioteki do logowania](https://defold.com/assets/?tag=logging) z Asset Portal.

## Testowanie uruchomionej gry za pomocą API czasu działania {#testing-a-running-game-through-a-runtime-api}

API automatyzacji w czasie działania może sprawdzać i kontrolować działający silnik debugowania. Można go użyć, gdy testy muszą znajdować obiekty czasu działania, wstrzykiwać wejście, czekać na widoczny stan lub przechwytywać wyrenderowany wynik.

Więcej informacji zawiera [instrukcja usługi silnika](/manuals/engine-service/#automation-bridge-extension).

Poniższy przykład korzysta ze struktury pomocniczego narzędzia Python rozszerzenia [Automation Bridge](https://github.com/defold/extension-automation-bridge). Projekt musi zawierać zgodną wersję rozszerzenia debugowania, udostępniać element o podanym identyfikatorze automatyzacji i publikować stan aplikacji `screen`:

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()

try:
    play = game.element(automation_id="play_button")
    game.click(play)
    game.wait_for_state("screen", "gameplay", timeout=5.0)
    screenshot = game.screenshot()
    print(screenshot.path)
finally:
    game.close_engine()
```

Stany zdefiniowane przez aplikację i identyfikatory automatyzacji korzystają z opcjonalnego API Lua rozszerzenia Automation Bridge, dostępnego wyłącznie w trybie debugowania, które projekt musi włączyć i w którym musi opublikować te dane. Stałe opóźnienie jest podatne na różnice w szybkości komputera i czasie klatek; ograniczone odpytywanie o określony stan jest bardziej niezawodne.

Automation Bridge jest rozszerzeniem, a nie częścią podstawowego silnika. Informacje o selektorach, oczekiwaniu, stanie, zdarzeniach, zrzutach ekranu i diagnostyce dla zainstalowanej wersji zawiera [dokumentacja Python API](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python).

## Testy przeglądarkowe dla HTML5 {#browser-tests-for-html5}

Edytor może utworzyć i udostępnić kompilację HTML5 za pomocą bieżącego polecenia `build-html5`, jak opisano w [instrukcji Editor HTTP API](/manuals/editor-http-api/#building-html5). Bob również może utworzyć pakiet HTML5 bez edytora.

Zewnętrzne narzędzia automatyzacji przeglądarki, takie jak Playwright, Puppeteer, Selenium, WebdriverIO lub Cypress, mogą:

* czekać na gotowość obszaru canvas Defold i aplikacji;
* wysyłać wejście z klawiatury, myszy i emulowanego dotyku;
* zmieniać rozmiar obszaru widoku;
* zbierać dane wyjściowe konsoli przeglądarki i błędy JavaScript;
* wykonywać zrzuty ekranu i porównywać artefakty.

Wejście skierowane do obszaru canvas jest przetwarzane za pomocą zwykłych wiązań wejścia projektu i funkcji zwrotnych `on_input()`. Należy testować zarówno reakcję gry, jak i punkty integracji charakterystyczne dla przeglądarki.

Najbardziej niezawodnym podejściem jest udostępnienie jednoznacznego mostu testowego JavaScript we własnym pliku `index.html`. Po stronie Defold kompilacje HTML5 mogą wykonywać JavaScript za pomocą `html5.run()`, co umożliwia komunikację z takim mostem po stronie przeglądarki. Do przesyłania poleceń z JavaScript z powrotem do Defold należy użyć osobnego mostu między JavaScript a silnikiem.

Testy przeglądarkowe powinny mieć określone ograniczenia. W raporcie końcowym należy rozróżnić błąd wczytywania strony, brak obszaru canvas, błąd JavaScript, przekroczenie limitu czasu testu i nieudaną asercję gry.

## Podglądy edytora i zrzuty ekranu z uruchomionej aplikacji do kontroli wizualnej {#editor-previews-and-runtime-screenshots}

Można utworzyć zrzut ekranu plików zasobów w domyślnym widoku sceny otwartego edytora albo gry w czasie działania.

| Metoda | Zastosowanie |
| --- | --- |
| [Podgląd edytora](/manuals/editor-http-api/#rendering-scene-previews) | Układ wczytanego zasobu, np. poziomu lub GUI, kompozycja atlasu, sprawdzanie mapy kafelków, kompozycja statycznej sceny, poprawność renderowania i shaderów edytora albo tworzenie miniatur dokumentacji |
| [Zrzut ekranu z uruchomionej aplikacji](/manuals/engine-service) | Wyrenderowany stan uruchomionej kompilacji w kontrolowanym scenariuszu |

Porównywania obrazów można użyć na przykład w testach regresji. Gdy kontrola się nie powiedzie, należy zapisać obraz różnicowy i metryki porównania.

Model multimodalny może oceniać podczas kontroli wizualnej warunki semantyczne, które trudno wyrazić w inny sposób, takie jak przycięty tekst, nakładające się elementy sterujące, niejasne stany zaznaczenia lub zawartość poza bezpiecznym obszarem. Zaleca się traktowanie tej oceny jako dodatkowego sygnału z jednoznacznymi kryteriami, a nie jako zamiennika deterministycznych kontroli logiki lub porównywania obrazów.

## Testy bez interfejsu graficznego i CI {#headless-tests-and-ci}

W CI niezależnym od edytora należy używać narzędzia CLI Bob the builder.

Można go użyć do rozwiązywania zależności, budowania gry, archiwum lub samodzielnego pakietu oraz generowania raportu JSON:

```sh
mkdir -p build/reports

java -jar bob.jar \
  --root . \
  --archive \
  --build-report-json build/reports/build-report.json \
  resolve build
```

Pakiet testowy bez interfejsu graficznego można zbudować z osobnymi ustawieniami:

```sh
java -jar bob.jar \
  --root . \
  --settings test/test.settings \
  --platform x86_64-linux \
  --variant headless \
  --archive \
  --bundle-output build/test-bundle \
  resolve build bundle
```

Utworzony plik wykonywalny należy uruchomić za pomocą kontrolera procesu odpowiedniego dla platformy. Należy przechwycić jego stan wyjścia i logi, wymusić limit czasu oraz wymagać ustrukturyzowanego zdarzenia zakończenia zestawu.

[Instrukcja Bob](/manuals/bob) opisuje platformy, pliki ustawień, pakiety, pamięci podręczne, rozszerzenia natywne i raporty z budowania.

## Raporty o błędach i artefakty {#failure-reports-and-artifacts}

Dobre wyniki testów powinny zachowywać wystarczająco dużo dowodów, aby odtworzyć i zdiagnozować błąd:

* nazwę testu, identyfikator uruchomienia i szczegóły asercji;
* czas trwania i sklasyfikowany wynik;
* kompletny log konsoli lub procesu;
* wersję Defold, platformę docelową i odpowiednią konfigurację;
* raport z budowania Bob i stan wyjścia procesu;
* stan czasu działania lub migawkę sceny, jeśli są dostępne;
* zrzuty ekranu, różnice względem obrazu bazowego, nagrania lub ślady przeglądarki;
* ścieżki lub odnośniki do wszystkich wygenerowanych artefaktów.

Ten sam format powinien być przydatny dla programisty, lokalnego skryptu, usługi CI lub [agenta AI wspomagającego programowanie](/manuals/ai-agents). Dzięki temu weryfikacja pozostaje deterministyczna nawet wtedy, gdy diagnozowanie lub naprawa zostaną oddelegowane.
