---
title: Automatyzacja w Defold
brief: Ta instrukcja przedstawia interfejsy automatyzacji Defold i wyjaśnia, jak wybierać między przepływami pracy obejmującymi edytor, środowisko uruchomieniowe, wiersz poleceń, testy i agentów.
---

# Automatyzacja w Defold {#automation-in-defold}

Ta instrukcja zawiera ogólny opis i odnośniki do osobnych instrukcji dotyczących poszczególnych tematów.

Defold obsługuje automatyzację na kilku poziomach. Wybór interfejsu odpowiedniego do zadania jest jednym z najważniejszych aspektów skutecznej automatyzacji. Poniższa tabela pomoże wybrać najprostszy interfejs dla danego działania:

| Warstwa | Zastosowanie |
| --- | --- |
| [Skrypty edytora](/manuals/editor-scripts) | Własne polecenia i przepływy pracy lub integracje edytora, które przyspieszają testowanie i tworzenie, np. poziomów i zasobów |
| [Skrypty interfejsu edytora](/manuals/editor-scripts-ui/) | Własne narzędzia wizualne, wyskakujące okna, konfiguratory lub interfejsy użytkownika korzystające ze skryptów edytora |
| [Editor HTTP API](/manuals/editor-http-api) | Sterowanie otwartym projektem gry w edytorze Defold za pomocą operacji OpenAPI, zasobów projektu, buildów, poleceń edytora, podglądów, preferencji, danych wyjściowych konsoli lub skryptów edytora udostępniających własne operacje narzędziom zewnętrznym, integracjom IDE i kontrolerom testów |
| [Bob CLI](/manuals/bob) | Budowanie projektu, tworzenie archiwów danych lub samodzielnych pakietów z wiersza poleceń, raporty, CI |
| [Haki cyklu życia](/manuals/editor-http-api#lifecycle-hooks) | Walidacja lub generowanie przed budowaniem i tworzeniem pakietów w edytorze oraz po ich zakończeniu |
| [Usługa HTTP silnika](/manuals/engine-service) | Sprawdzanie uruchomionego silnika gry Defold (`dmengine`), usługi programistyczne, profilowanie, wiadomości czasu działania lub interfejsy API automatyzacji w czasie działania zdefiniowane przez rozszerzenia, odpytywanie przez narzędzia zewnętrzne, wysyłanie poleceń do uruchomionej kompilacji w trybie debugowania |
| [Automation Bridge](https://github.com/defold/extension-automation-bridge) | oficjalne rozszerzenie Defold, które udostępnia dodatkowe punkty końcowe automatyzacji silnika w czasie działania |
| [Testy automatyczne](/manuals/automated-testing) | Testowanie logiki gry, wiadomości, komponentów, wejścia, fizyki i zachowania silnika, sprawdzanie scen, wizualne informacje zwrotne np. za pomocą [podglądu edytora](/manuals/editor-http-api/#rendering-scene-previews), wstrzykiwanie wejścia, bieżący stan aplikacji, [uruchamiane kolekcje testowe](/manuals/automated-testing/#tests-in-a-running-collection) |
| Skrypty powłoki lub narzędzia do uruchamiania zadań | Generowanie, formatowanie, walidacja i powtarzalne zadania, zwykłe operacje na plikach |
| Zewnętrzne narzędzia automatyzacji charakterystyczne dla platformy i przeglądarek internetowych | Narzędzia do testowania aplikacji komputerowych, testy interakcji HTML5, zrzuty ekranu, integracje internetowe |
| Agenci AI wspomagający programowanie i modele multimodalne | Zadania, dla których podejście deterministyczne jest trudne lub niemożliwe do zaimplementowania, analiza semantyczna scen, układów GUI lub zrzutów ekranu z uruchomionej aplikacji |

Najważniejszym rozróżnieniem jest podział na edytor Defold i uruchomioną grę. Są to osobne procesy z osobnymi serwerami HTTP.

## Automatyzacja deterministyczna czy agenci AI {#deterministic-automation-or-ai-agents}

Rozwiązanie deterministyczne jest preferowane, gdy sekwencja operacji jest już znana, na przykład w przypadku walidatora poziomów, programu formatującego, zadania budowania lub testu regresji. Takie rozwiązania powinny zwykle mieć stabilne dane wejściowe, dane wyjściowe, limity czasu i kody wyjścia. Dobrze sprawdzają się w automatycznych hakach i testach, które można niezawodnie uruchamiać w CI. Preferowane jest również deterministyczne rozwiązanie do proceduralnego tworzenia zasobów w projektach, np. narzędzie przekształcające obiekty gltf w modele z określonym materiałem albo wypełniające poziom drzewami. Takie procedury można łatwo tworzyć dla każdego projektu za pomocą skryptów edytora i interfejsu użytkownika. Więcej informacji znajduje się w [instrukcji](/manuals/editor-scripts-ui).

Agent może być przydatny, gdy zadanie wymaga analizy lub przetwarzania multimodalnego (np. obejmującego obrazy): znajdowania odpowiednich zasobów, wyboru implementacji, modyfikowania kilku plików, interpretowania błędów i iteracyjnego dążenia do zdefiniowanych kryteriów akceptacji. Agent powinien jednak nadal wywoływać interfejsy deterministyczne i korzystać z tych samych dowodów, co lokalny skrypt lub mechanizm wykonawczy CI. Zobacz instrukcję dotyczącą [korzystania z agentów AI wspomagających programowanie z Defold](/manuals/ai-agents).

## Pętla automatyzacji {#the-automation-loop}

Niezawodny proces automatyzacji tworzy zamkniętą pętlę:

1. Sprawdź — odczytaj pliki projektu, opis bieżącego interfejsu i odpowiednią dokumentację.
2. Zmień — użyj transakcji edytora, skryptów edytora albo narzędzi do plików i powłoki.
3. Zweryfikuj — zbuduj projekt, uruchom ukierunkowane testy i zbierz logi, raporty, stan lub obrazy.
4. Oceń — porównaj dowody z kryteriami akceptacji, a następnie zakończ lub ponów próbę.

![Pętla automatyzacji obejmująca sprawdzanie, zmianę, weryfikację i ocenę](images/automation/automation_loop.png)

Weryfikacja powinna dostarczać dowodów z rzeczywistego środowiska. Odpowiednie dowody obejmują:

* pomyślny wynik budowania;
* jednoznacznie ukończony zestaw testów;
* oczekiwany stan uruchomionej gry;
* wygenerowany pakiet lub raport z budowania;
* deterministyczne porównanie obrazów;
* zrzut ekranu spełniający zdefiniowane kryteria wizualne.

Oczekiwany wynik należy określić przed wprowadzeniem zmian. Należy także określić limit czasu i maksymalną liczbę prób naprawy. Proces nienadzorowany nie powinien trwać w nieskończoność, jeśli nie może spełnić kryteriów akceptacji.

## Następne kroki {#next-steps}

Więcej informacji na temat konkretnych przepływów pracy automatyzacji znajduje się w następujących instrukcjach:

* [Automatyzowanie zadań edytora Defold za pomocą HTTP API](/manuals/editor-http-api)
* [Usługa silnika i HTTP API czasu działania](/manuals/engine-service)
* [Testowanie automatyczne i weryfikacja](/manuals/automated-testing)
* [Korzystanie z agentów AI wspomagających programowanie z Defold](/manuals/ai-agents)
