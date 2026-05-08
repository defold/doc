---
title: Podręcznik cyklu życia aplikacji Defold
brief: Ten podręcznik opisuje cykl życia gier i aplikacji w Defold.
---

# Cykl życia aplikacji

Cykl życia aplikacji lub gry w Defold jest w dużej skali prosty. Silnik przechodzi przez trzy etapy działania: inicjalizację, pętlę aktualizacji, w której aplikacja spędza większość czasu, oraz finalizację.

::: sidenote
Podręcznik dotyczy wersji Defold od 1.12.0. W wersji 1.12.0 wprowadzono zmiany związane z cyklem życia oraz nową funkcję `late_update()`.
:::

![Przegląd cyklu życia](images/application_lifecycle/application_lifecycle.png)

W wielu przypadkach wystarcza podstawowe rozumienie wewnętrznego działania Defold. Czasem jednak można trafić na sytuacje brzegowe, w których kluczowa staje się dokładna kolejność wykonywania zadań przez silnik. Ten dokument opisuje, jak silnik uruchamia aplikację od startu do zakończenia.

Aplikacja zaczyna od zainicjalizowania wszystkiego, co jest potrzebne do uruchomienia silnika. Ładuje główną kolekcję i wywołuje [`init()`](/ref/go#init) na wszystkich załadowanych komponentach, które mają funkcję `init()` w Lua, czyli na komponentach skryptowych i komponentach GUI ze skryptami GUI. Dzięki temu można wykonać własną inicjalizację.

Następnie aplikacja przechodzi do pętli aktualizacji, w której spędza większość swojego czasu. W każdej klatce aktualizowane są obiekty gry i zawarte w nich komponenty. Wywoływane są funkcje [`update()`](/ref/go#update) w skryptach i skryptach GUI. W trakcie pętli aktualizacji wiadomości są rozsyłane do odbiorców, odtwarzane są dźwięki, a cała grafika jest renderowana.

W pewnym momencie cykl życia aplikacji dobiega końca. Zanim aplikacja zostanie zamknięta, silnik wychodzi z pętli aktualizacji i wchodzi w etap finalizacji. Przygotowuje wszystkie załadowane obiekty gry do usunięcia. Wywoływane są funkcje [`final()`](/ref/go#final) wszystkich komponentów obiektów, co pozwala na własne sprzątanie. Potem obiekty są usuwane, a główna kolekcja zostaje zwolniona.

Kroki wykonywane w przejściu ["rozsyłanie wiadomości"](#dispatching-messages) są dla przejrzystości pokazane na osobnym diagramie na końcu tego podręcznika i oznaczone na diagramach małą ikoną koperty ze strzałką 📩.

## Inicjalizacja

To tutaj zaczyna się gra i jest to pierwszy krok działania uruchomionej aplikacji. Można go podzielić na 3 fazy:

![Inicjalizacja](images/application_lifecycle/initialization.png)

### Preinicjalizacja

W fazie preinicjalizacji (`Preinitialization`) silnik wykonuje wiele kroków, zanim zostanie załadowana główna kolekcja bootstrapowa. Konfigurowane są profiler pamięci, gniazda, grafika, HID (urządzenia wejściowe), dźwięk, fizyka i wiele innych elementów. Ładowana i konfigurowana jest też konfiguracja aplikacji (*game.project*).

![Preinicjalizacja](images/application_lifecycle/pre_init.png)

Pierwszym punktem wejścia, nad którym użytkownik ma kontrolę pod koniec inicjalizacji silnika, jest wywołanie funkcji `init()` bieżącego skryptu renderującego.

Następnie ładowana i inicjalizowana jest główna kolekcja.

### Inicjalizacja kolekcji

W fazie inicjalizacji kolekcji (`Collection Init`) wszystkie obiekty gry w kolekcji przekazują swoje transformacje, czyli przesunięcie, obrót i skalę, swoim dzieciom. Potem wywoływane są funkcje `init()` wszystkich istniejących komponentów.

![Inicjalizacja kolekcji](images/application_lifecycle/collection_init.png)

::: sidenote
Kolejność wywoływania funkcji `init()` komponentów obiektów gry nie jest określona. Nie należy zakładać, że silnik inicjalizuje obiekty należące do tej samej kolekcji w jakiejkolwiek konkretnej kolejności.
:::

### Końcowa aktualizacja w inicjalizacji

Silnik wykonuje wtedy pełne przejście końcowej aktualizacji (`Post Update`) - dokładnie to samo, które później następuje po każdym kroku pętli aktualizacji (`Update Loop`). Jest ono wykonywane na końcu inicjalizacji, ponieważ kod w `init()` może wysyłać nowe wiadomości, polecać fabrykom tworzenie nowych obiektów, oznaczać obiekty do usunięcia i wykonywać inne działania.

![Końcowa aktualizacja](images/application_lifecycle/post_init.png)

To przejście obsługuje dostarczanie wiadomości, faktyczne tworzenie obiektów przez fabryki oraz usuwanie obiektów. Zwróć uwagę, że przejście `Post Update` obejmuje sekwencję „rozsyłania wiadomości” (`dispatch messages`), która nie tylko dostarcza zakolejkowane wiadomości, ale także przetwarza wiadomości wysyłane do pełnomocników kolekcji. Wszystkie kolejne aktualizacje proxy, takie jak `enable`, `disable`, `init`, `final`, `loading` i `mark for unloading`, są wykonywane w tych krokach.

Możliwe jest załadowanie [pełnomocnika kolekcji (Collection Proxy)](/manuals/collection-proxy) w trakcie `init()`, upewnienie się, że wszystkie zawarte w nim obiekty zostały zainicjalizowane, a następnie wyładowanie kolekcji przez proxy - i wszystko to przed wywołaniem pierwszego `update()` komponentu, czyli zanim silnik opuści etap inicjalizacji i wejdzie do pętli aktualizacji:

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- Kolekcja proxy jest wyładowana, zanim ten kod zostanie wykonany.
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- Funkcje init() i final() obiektów w kolekcji proxy
        -- są wywoływane, zanim dotrzemy do update() tego obiektu
    end
end
```

## Pętla aktualizacji

Pętla aktualizacji przebiega w każdej klatce według określonej sekwencji. Można ją podzielić na 5 głównych faz:

![Pętla aktualizacji](images/application_lifecycle/update_loop.png)

1. Wejście (przetwarzanie i obsługa)
2. Aktualizacja (w tym aktualizacje Fixed, Regular, Late oraz komponentów silnika)
3. Aktualizacja renderowania
4. Końcowa aktualizacja (wyładowywanie pełnomocników kolekcji, tworzenie i usuwanie obiektów gry)
5. Renderowanie klatki (końcowe renderowanie grafiki)

### Faza wejścia

Wejście jest odczytywane z dostępnych urządzeń, mapowane zgodnie z [powiązaniami wejść](/manuals/input), a następnie rozsyłane. Każdy obiekt gry, który przechwycił fokus wejścia, otrzymuje wejście we wszystkich swoich komponentach przez funkcje `on_input()`. Obiekt gry ze skryptem komponentu i komponentem GUI ze skryptem GUI otrzyma wejście w obu funkcjach `on_input()`, o ile są zdefiniowane i o ile obiekt przechwycił fokus wejścia.

![Faza wejścia](images/application_lifecycle/input_phase.png)

Każdy obiekt gry, który przechwycił fokus wejścia i zawiera komponenty pełnomocnika kolekcji, przekazuje wejście do komponentów wewnątrz kolekcji obsługiwanej przez tego pełnomocnika. Proces ten jest następnie wykonywany rekurencyjnie w kolejnych włączonych pełnomocnikach kolekcji.

### Faza aktualizacji

Faza aktualizacji (`Update`) jest częścią pętli aktualizacji. Zaczyna się raz dla głównej kolekcji, a następnie działa rekurencyjnie dla każdego włączonego pełnomocnika kolekcji.

W obrębie kolekcji Defold przetwarza callbacki według typu komponentu: iteruje po wszystkich instancjach typu komponentu, który implementuje daną fazę, wywołuje callback Lua dla każdej instancji, opróżnia wiadomości, a potem przechodzi do następnego typu komponentu.

Ogólna kolejność faz callbacków Lua dla komponentów *script* jest następująca:

1. `fixed_update()` - wywoływane 0..N razy na klatkę (jeśli używany jest stały krok czasowy)
2. `update()` - wywoływane 1 raz na klatkę
3. `late_update()` - wywoływane 1 raz na klatkę

![Faza aktualizacji](images/application_lifecycle/update_phase.png)

Każdy komponent obiektu gry w głównej kolekcji jest odwiedzany. Jeśli którykolwiek z tych komponentów ma skrypt z funkcją `fixed_update()`/`update()`/`late_update()`, to zostanie ona wywołana. Jeśli komponentem jest pełnomocnik kolekcji, każdy komponent w jego kolekcji jest aktualizowany rekurencyjnie we wszystkich krokach fazy `Update`.

::: sidenote
Kolejność wywoływania funkcji `update()` komponentów obiektów gry nie jest określona. Nie należy zakładać, że silnik aktualizuje obiekty należące do tej samej kolekcji w jakiejkolwiek konkretnej kolejności. To samo dotyczy `fixed_update()` i `late_update()` (od 1.12.0).
:::

#### Fizyka

Dla komponentów obiektów kolizji wiadomości fizyki, takich jak kolizje, wyzwalacze, odpowiedzi ray cast itd., są rozsyłane przez obejmujący je obiekt gry do wszystkich komponentów, które zawierają skrypt z funkcją `on_message()`.

Jeśli do symulacji fizyki używany jest [stały krok czasowy](/manuals/physics/#physics-updates), może też dojść do wywołania funkcji `fixed_update()` we wszystkich komponentach skryptowych. Ta funkcja jest przydatna w grach opartych na fizyce, gdy chcesz manipulować obiektami fizycznymi w regularnych odstępach czasu, aby uzyskać stabilną symulację.

#### Transformacje

Przed **każdą** aktualizacją typu komponentu, wielokrotnie w trakcie pętli aktualizacji (`Update Loop`), jeśli jest to potrzebne, aktualizowane są transformacje, czyli zastosowanie ruchu, obrotu i skali obiektów gry do każdego komponentu obiektu gry i do wszystkich potomnych komponentów obiektów gry.

Na końcu pętli aktualizacji (`Update Loop`) wykonywana jest jeszcze jedna końcowa aktualizacja transformacji, jeśli jest to potrzebne.

#### Faza aktualizacji silnika bez fixed updates

Poniższe tabele opisują przejścia aktualizacji na poziomie silnika. Celowo pomijają dokładną wewnętrzną kolejność priorytetów komponentów, ponieważ jest to szczegół implementacyjny silnika, ale pokazują gwarancje istotne dla skryptów:

- `fixed_update()` działa przed `update()`
- `late_update()` działa po `update()`
- wiadomości są opróżniane między aktualizacjami typów komponentów oraz między etapami callbacków skryptowych

Gdy `Use Fixed Timestep` ma wartość `false` i/lub Fixed Update Frequency ma wartość `0`, na początku fazy przygotowywane jest `dt`, a potem przebieg wygląda tak, jak w tabeli poniżej:

:::sidenote
Zwróć uwagę, że po **każdej** aktualizacji typu komponentu wszystkie wiadomości są rozsyłane - nie zaznaczono tego w tabeli poniżej, żeby zachować jej czytelność.
:::

| Krok | Faza silnika | Callback Lua | Komentarz |
|-|-|-|-|
| 1 | **Update** | `update()` | Wywoływane raz na klatkę dla każdego typu komponentu, który implementuje Update, zgodnie z wewnętrzną kolejnością priorytetów. Dodatkowo animacje właściwości GO uruchomione przez `go.animate()` są tu aktualizowane jako oddzielny typ komponentu. Aktualizowane są tu również komponenty **Physics**. Dla każdego włączonego Collection Proxy cała faza `Update` jest wywoływana rekurencyjnie od kroku 1. |
| 2 | **Late Update** | `late_update()` | Wywoływane raz na klatkę dla każdego typu komponentu, który implementuje Late Update, zgodnie z wewnętrzną kolejnością priorytetów. |
| 3 | **Transformacje** | | Na końcu wykonywana jest jeszcze jedna końcowa aktualizacja transformacji dla każdego komponentu, jeśli jest to potrzebne. |

#### Faza aktualizacji silnika ze stałym krokiem czasowym

Gdy `Use Fixed Timestep` ma wartość `true`, a Fixed Update Frequency jest różne od zera, na początku fazy przygotowywane są `dt` (delta time), `fixed_dt` i `num_fixed_steps` (`0..N`) - czyli liczba wywołań fixed update, wyznaczona na podstawie czasu od ostatniej aktualizacji, aby zachować stałą liczbę aktualizacji.

:::sidenote
Zwróć uwagę, że po **każdej** aktualizacji typu komponentu wszystkie wiadomości są rozsyłane - nie zaznaczono tego w tabeli poniżej, żeby zachować jej czytelność.
:::

Potem faza działa w pętli:

| Krok | Faza silnika | Callback Lua | Komentarz |
|-|-|-|-|
| 1 | **Fixed Update** | `fixed_update()` | Wywoływane `0..N` razy na klatkę, zależnie od czasu, dla każdego typu komponentu, który implementuje Fixed Update, zgodnie z wewnętrzną kolejnością priorytetów. Obejmuje to etapy Fixed Update komponentów *Physics*. |
| 2 | **Update** | `update()` | Wywoływane raz na klatkę dla każdego typu komponentu, który implementuje Update, zgodnie z wewnętrzną kolejnością priorytetów. Dodatkowo animacje właściwości GO uruchomione przez `go.animate()` są tu aktualizowane jako oddzielny typ komponentu. Dla każdego włączonego Collection Proxy faza `Update` jest wywoływana rekurencyjnie od kroku 1. |
| 3 | **Late Update** | `late_update()` | Wywoływane raz na klatkę dla każdego typu komponentu, który implementuje Late Update, zgodnie z wewnętrzną kolejnością priorytetów. |
| 4 | **Transformacje** | | Na końcu wykonywana jest jeszcze jedna końcowa aktualizacja transformacji dla każdego komponentu, jeśli jest to potrzebne. |

Jeśli chcesz poznać więcej szczegółów o wewnętrznym działaniu Defold w fazie Update, warto przeczytać sam kod [`gameobject.cpp`](https://github.com/defold/defold/blob/dev/engine/gameobject/src/gameobject/gameobject.cpp).

### Faza aktualizacji renderowania

Blok aktualizacji renderowania najpierw rozsyła wszystkie wiadomości wysłane do gniazda `@render` (na przykład wiadomości `set_view_projection`, `set_clear_color` itd.). Następnie wywoływana jest funkcja `update()` skryptu renderującego.

![Faza aktualizacji renderowania](images/application_lifecycle/render_update_phase.png)

### Faza post update

Po aktualizacjach uruchamiana jest sekwencja końcowej aktualizacji. Wyładowuje ona z pamięci pełnomocniki kolekcji oznaczone do wyładowania (dzieje się to podczas sekwencji „rozsyłania wiadomości” - `dispatch messages`). Każdy obiekt gry oznaczony do usunięcia wywołuje wszystkie funkcje `final()` swoich komponentów, jeśli takie istnieją. Kod w funkcjach `final()` często wysyła nowe wiadomości do kolejki, więc po tym uruchamiane jest ponownie przejście `dispatch messages`.

![Faza post update](images/application_lifecycle/post_update_phase.png)

Każdy komponent fabryki, który dostał polecenie utworzenia obiektu gry, zrobi to w następnym kroku. Na końcu obiekty gry oznaczone do usunięcia są faktycznie usuwane.

### Faza renderowania

Ostatni krok pętli aktualizacji obejmuje rozsyłanie wiadomości `@system` (`exit`, `reboot`, przełączanie profilera, uruchamianie i zatrzymywanie przechwytywania wideo itd.).

![Faza renderowania](images/application_lifecycle/render_phase.png)

Potem grafika jest renderowana, podobnie jak wizualizacja profilera (zobacz [dokumentację debugowania](/manuals/debugging)). Po renderowaniu grafiki wykonywane jest przechwytywanie wideo.

#### Liczba klatek i krok czasowy kolekcji

Liczbę aktualizacji klatki na sekundę, czyli liczbę przebiegów pętli aktualizacji na sekundę, można ustawić w ustawieniach projektu albo programowo, wysyłając wiadomość `set_update_frequency` do gniazda `@system`. Można też osobno ustawić krok czasowy (_time step_) dla pełnomocników kolekcji, wysyłając do proxy wiadomość `set_time_step`. Zmiana kroku czasowego kolekcji nie wpływa na liczbę klatek. Wpływa natomiast na krok czasowy aktualizacji fizyki oraz na wartość `dt` przekazywaną do `update()`. Pamiętaj też, że zmiana kroku czasowego nie zmienia liczby wywołań `update()` w każdej klatce - zawsze jest ono wywoływane dokładnie raz.

(Szczegóły znajdziesz w [podręczniku pełnomocnika kolekcji](/manuals/collection-proxy) oraz przy [`set_time_step`](/ref/collectionproxy#set-time-step))

#### Ograniczanie pracy silnika

W Defold 1.12.0 wprowadzono API ograniczania pracy silnika, które może całkowicie pominąć aktualizacje silnika i renderowanie, a mimo to nadal wykrywać wejście. Każde wejście wybudza silnik, a po czasie wyciszenia silnik może ponownie wejść w tryb ograniczania.

Szczegóły i przykłady użycia znajdziesz w API `sys.set_engine_throttle()`.

## Finalizacja

Gdy aplikacja się zamyka, najpierw kończy ostatnią sekwencję pętli aktualizacji, która wyładuje pełnomocniki kolekcji: finalizując i usuwając wszystkie obiekty gry w każdej obsługiwanej przez nie kolekcji.

Gdy to się skończy, silnik wchodzi w sekwencję finalizacji obsługującą główną kolekcję i jej obiekty:

![Finalizacja](images/application_lifecycle/finalization.png)

Najpierw wywoływane są funkcje `final()` komponentów. Potem następuje kolejne przejście rozsyłania wiadomości. Na końcu wszystkie obiekty gry są usuwane, a główna kolekcja zostaje zwolniona.

Silnik przechodzi potem do zamykania podsystemów działających w tle: usuwa konfigurację projektu, wyłącza profiler pamięci i tak dalej.

Aplikacja jest teraz całkowicie zamknięta.

## Rozsyłanie wiadomości

**Rozsyłanie wiadomości** to specjalne przejście wykonywane po **każdej** aktualizacji typu komponentu, na przykład po aktualizacji sprite'ów, skryptów i każdej innej operacji, która może wysyłać wiadomości. W trakcie wykonywania wszystkie zakolejkowane wiadomości są rozsyłane. Na diagramach są oznaczone małymi ikonami koperty ze strzałką 📩.

![Rozsyłanie wiadomości](images/application_lifecycle/dispatch_messages.png)

Po rozesłaniu wszystkich **wiadomości użytkownika** przez wywołanie `on_message()` dla każdego komponentu Defold obsługuje specjalne wiadomości w następującej kolejności, dla każdego pełnomocnika kolekcji:

1. wiadomości `load` - ładują pełnomocniki kolekcji oznaczone do wczytania i odsyłają wiadomość `proxy_loaded`.
2. wiadomości `unload` - wyładowują pełnomocniki kolekcji oznaczone do wyładowania i odsyłają wiadomość `proxy_unloaded`.
3. wiadomości `init` - uruchamiają fazę inicjalizacji kolekcji (`Collection Init`) dla wszystkich pełnomocników kolekcji, które mają zostać zainicjalizowane.
4. wiadomości `final` - wywołują `final()` na wszystkich komponentach proxy oznaczonych do finalizacji.
5. wiadomości `enable` - włączają pełnomocnika kolekcji, więc w następnej klatce zostanie dla niego wykonana pętla aktualizacji (`Update Loop`); to niejawnie uruchamia `init()` dla każdego komponentu w tej kolekcji.
6. wiadomości `disable` - wyłączają pełnomocnika kolekcji, więc w następnej klatce nie zostanie dla niego wykonana pętla aktualizacji (`Update Loop`); całkowicie zatrzymuje to działanie pętli aktualizacji dla tego proxy.

Ponieważ kod komponentów odbierających wiadomości w `on_message()` może wysyłać kolejne wiadomości, dispatcher będzie dalej rozsyłał wiadomości rekurencyjnie, aż kolejka będzie pusta. Istnieje jednak limit liczby przejść przez kolejkę wiadomości. Szczegóły znajdziesz w [łańcuchach wiadomości (Message Chains)](/manuals/message-passing).
