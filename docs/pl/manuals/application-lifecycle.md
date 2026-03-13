---
title: Cykl życia aplikacji w silniku Defold
brief: Przewodnik wyjaśnia cykl życia aplikacji zbudowanej w silniku Defold od uruchomienia do zamknięcia.
---

# Cykl życia aplikacji

Cykl życia aplikacji lub gry w silniku Defold jest zasadniczo prosty. Silnik przechodzi przez trzy główne fazy: inicjalizację, pętlę aktualizacyjną (gdzie aplikacja spędza większość czasu) oraz finalizację.

::: sidenote
Instrukcja odnosi się do wersji Defold 1.12.0. W tej wersji wprowadzono zmiany w procesie cyklu życia oraz nową funkcję `late_update()`.
:::

![Lifecycle overview](images/application_lifecycle/application_lifecycle.png)

W wielu przypadkach wystarczy ogólna wiedza o tym, jak działa silnik Defold. Jednak czasem trzeba poznać dokładną kolejność wykonywanych operacji. Ten dokument opisuje przebieg działania silnika od startu do zakończenia aplikacji.

Aplikacja zaczyna się od przygotowania wszystkiego, co jest potrzebne do działania silnika. Główna kolekcja zostaje załadowana, a silnik Defold wywołuje [`init()`](/ref/go#init) dla wszystkich załadowanych komponentów, które posiadają tę funkcję (zarówno w skryptach obiektów, jak i skryptach GUI). Dzięki temu można przeprowadzić własną inicjalizację.

Następnie aplikacja wchodzi w pętlę aktualizacyjną, w której spędza większość swojego czasu. Każda klatka aktualizuje obiekty gry i komponenty. Wywoływane są funkcje [`update()`](/ref/go#update) zarówno w skryptach, jak i w skryptach GUI. Podczas tej fazy wiadomości są rozsyłane do odbiorców, odtwarzane są dźwięki, a wszystkie elementy graficzne są renderowane.

W pewnym momencie cykl życia dobiega końca. Zanim aplikacja się zakończy, silnik wychodzi z pętli aktualizacyjnej i przechodzi do fazy finalizacyjnej. Przygotowuje wszystkie obiekty gry do usunięcia. Funkcje [`final()`](/ref/go#final) każdego komponentu są uruchamiane, co pozwala na własne procedury sprzątania. Potem obiekty są usuwane, a główna kolekcja zostaje zwolniona.

Wszystkie kroki zawarte w przejściu „dispatch messages” są pokazane osobno na końcu tego podręcznika, a na diagramach oznaczone ikoną koperty ze strzałką 📩.

## Faza inicjalizacyjna

To tutaj zaczyna się gra, i jest to pierwszy etap uruchomienia. Można go podzielić na trzy podfazy:

![Initizalization](images/application_lifecycle/initialization.png)

### Przedinicjalizacja (Preinitialization)

W fazie `Preinitialization` silnik wykonuje wiele działań zanim załaduje główną (bootstrapową) kolekcję. Konfigurowany jest profiler pamięci, gniazda, grafika, wejścia (HID), dźwięk, fizyka i wiele innych subsystemów. Wczytywany jest także plik konfiguracyjny (*game.project*).

![Preinitialization](images/application_lifecycle/pre_init.png)

Pierwszym punktem, w którym użytkownik kontroluje przepływ, jest wywołanie `init()` aktualnego render scriptu.

Główna kolekcja zostaje wtedy załadowana i zainicjalizowana.

### Inicjalizacja kolekcji (Collection Init)

Podczas fazy `Collection Init` wszystkie obiekty gry w kolekcji przypisują transformacje – przesunięcie, obrót i skalowanie – swoim dzieciom. Następnie wywoływane są funkcje `init()` wszystkich komponentów, które ją udostępniają.

![Collection Init](images/application_lifecycle/collection_init.png)

::: sidenote
Kolejność wywołań funkcji `init()` komponentów obiektów gry nie jest określona. Nie należy zakładać konkretnej kolejności inicjalizacji w obrębie tej samej kolekcji.
:::

### Post Update podczas inicjalizacji

Po inicjalizacji silnik wykonuje pełne przejście `Post Update` – to samo, które odbywa się po każdym kroku pętli `Update Loop`. Szczególnie ważne jest to, że w tej fazie można zainicjalizować nowo tworzone obiekty, wysłać wiadomości, oznaczyć obiekty do usunięcia itd.

![Post Update](images/application_lifecycle/post_init.png)

Ten etap zajmuje się dostarczeniem wiadomości, tworzeniem nowych obiektów przez fabryki oraz usuwaniem obiektów. Przejście `Post Update` zawiera sekwencję „dispatch messages”, która nie tylko rozsyła zakolejkowane wiadomości, ale także obsługuje wiadomości skierowane do pełnomocników kolekcji (collection proxies). W kolejnych krokach aktualizowane są stany proxy (enable, disable, init, final, loading, mark for unloading).

Możliwe jest załadowanie [collection proxy](/manuals/collection-proxy) w trakcie `init()`, zainicjalizowanie jego obiektów, a następnie zwolnienie kolekcji – i to wszystko jeszcze zanim zostanie wywołana pierwsza funkcja `update()` komponentu, czyli zanim silnik opuści fazę inicjalizacji i wejdzie w pętlę aktualizacyjną:

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- The proxy collection is unloaded before this code is reached.
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- The proxy collection objects’ init() and final() functions
        -- are called before we reach this object’s update()
    end
end
```

## Pętla aktualizacyjna (Update Loop)

Pętla aktualizacyjna przebiega według określonej sekwencji w każdej klatce. Jej przebieg podzielony jest na pięć głównych faz:

![Update Loop](images/application_lifecycle/update_loop.png)

1. Input (odczyt i obsługa)
2. Update (obejmuje Fixed, Regular, Late oraz aktualizacje komponentów silnika)
3. Render Update
4. Post Update (zwalnianie kolekcji, tworzenie i usuwanie obiektów)
5. Frame Render (ostatnie renderowanie grafiki)

### Faza wejść (Input Phase)

Wejścia są odczytywane z dostępnych urządzeń, mapowane zgodnie z [input bindings](/manuals/input) i rozsyłane dalej. Każdy obiekt gry, który zdobył `acquire_input_focus`, otrzymuje wejścia w funkcje `on_input()` wszystkich swoich komponentów. Jeżeli obiekt posiada zarówno skrypt komponentu, jak i komponent GUI, oba dostaną wejścia, pod warunkiem że oba mają przechwytywanie wejścia.

![Input Phase](images/application_lifecycle/input_phase.png)

Jeżeli obiekt gry, który ma fokus wejścia, zawiera pełnomocników kolekcji, wejścia są przekazywane do komponentów wewnątrz tych proxy. Proces ten rekurencyjnie działa dla wszystkich włączonych proxy w obrębie włączonych proxy.

### Faza aktualizacji (Update Phase)

Faza `Update` zaczyna się dla głównej kolekcji, a następnie jest wywoływana rekurencyjnie dla każdego włączonego collection proxy.

W obrębie kolekcji silnik Defold przetwarza callbacki według typu komponentu: dla każdego typu iteruje po wszystkich instancjach, które implementują daną fazę, wywołuje funkcję Lua, opróżnia wiadomości, a potem przechodzi do następnego typu.

Wysoki poziom kolejności callbacków Lua w komponentach typu *script* wygląda następująco:

1. `fixed_update()` – wywoływane `0..N` razy na klatkę (gdy używany jest stały krok czasu)
2. `update()` – wywoływane raz na klatkę
3. `late_update()` – wywoływane raz na klatkę

![Update Phase](images/application_lifecycle/update_phase.png)

Każdy komponent obiektu gry w głównej kolekcji jest odwiedzany. Jeśli którykolwiek komponent posiada `fixed_update()`/`update()`/`late_update()`, to są one uruchamiane. Jeżeli komponent jest collection proxy, wszystkie komponenty tej kolekcji proxy są aktualizowane rekurencyjnie we wszystkich krokach fazy `Update`.

::: sidenote
Kolejność wywołań funkcji `update()` komponentów nie jest określona. Nie należy zakładać konkretnego porządku aktualizacji obiektów należących do tej samej kolekcji. To samo dotyczy `fixed_update()` i `late_update()` (od wersji 1.12.0).
:::

#### Fizyka

Dla komponentów collision object wiadomości fizyki (kolizje, wyzwalacze, odpowiedzi ray cast itd.) są rozsyłane do wszystkich komponentów, które implementują `on_message()` w obrębie danego obiektu gry.

Jeżeli do symulacji fizyki używany jest [fixed timestep](/manuals/physics/#physics-updates), to funkcje `fixed_update()` są wywoływane we wszystkich komponentach skryptowych. Ta funkcja jest przydatna do stabilnego sterowania obiektami fizycznymi.

#### Transformaty

Przed każdą aktualizacją typu komponentu, wielokrotnie w trakcie `Update Loop`, jeśli jest to potrzebne, aktualizowane są transformaty – przesunięcie, obrót i skala obiektów, ich komponentów i obiektów potomnych.

Na końcu `Update Loop` wykonywana jest jeszcze jedna finalna aktualizacja transformacji, jeśli jest to wymagane.

#### Faza silnika bez fixed update

Poniższe tabele opisują aktualizacje na poziomie silnika. Pomijają dokładną kolejność priorytetów komponentów (to szczegół implementacji), ale oddają gwarancje ważne dla skryptów:

- `fixed_update()` działa przed `update()`
- `late_update()` działa po `update()`
- wiadomości są rozsyłane między aktualizacjami typu komponentu oraz między etapami callbacków skryptowych

Gdy `Use Fixed Timestep` jest ustawione na `false` i/lub `Fixed Update Frequency` wynosi `0`, na początku faza przygotowuje `dt`, a następnie przebieg jest następujący:

::: sidenote
Po każdej aktualizacji typu komponentu wszystkie wiadomości są rozsyłane – w tabelach nie pokazano tego dla przejrzystości.
:::

| Krok | Faza silnika | Callback Lua | Komentarz |
|-|-|-|-|
| 1 | **Update** | `update()` | Wywoływane raz na klatkę dla każdego typu komponentu implementującego Update według wewnętrznego priorytetu. Animacje właściwości GO zaczęte przez `go.animate()` działają tu jako oddzielny typ komponentu. Aktualizowane są również komponenty fizyki. Dla każdego włączonego collection proxy cała faza `Update` jest wykonywana rekurencyjnie od kroku 1. |
| 2 | **Late Update** | `late_update()` | Wywoływane raz na klatkę dla każdego typu komponentu implementującego Late Update zgodnie z priorytetem. |
| 3 | **Transforms** |  | Na końcu przeprowadzana jest dodatkowa aktualizacja transformacji dla każdego komponentu, jeśli jest to potrzebne. |

#### Faza silnika z fixed timestep

Gdy `Use Fixed Timestep` ma wartość `true`, a `Fixed Update Frequency` jest różna od zera, na początku faza przygotowuje `dt`, `fixed_dt` oraz `num_fixed_steps` (`0..N`) – czyli ile razy zostanie wywołana funkcja fixed update, określone przez czas od ostatniej aktualizacji, aby zachować stałą liczbę kroków.

::: sidenote
Po każdej aktualizacji typu komponentu wszystkie wiadomości są rozsyłane – tabelki tego nie pokazują dla przejrzystości.
:::

Potem faza przebiega w pętli:

| Krok | Faza silnika | Callback Lua | Komentarz |
|-|-|-|-|
| 1 | **Fixed Update** | `fixed_update()` | Wywoływana `0..N` razy na klatkę dla każdego typu komponentu implementującego Fixed Update według priorytetu. Zawiera również Fixed Update komponentów fizyki. |
| 2 | **Update** | `update()` | Wywoływana raz na klatkę dla każdego typu komponentu implementującego Update według priorytetu. Animacje właściwości GO uruchomione przez `go.animate()` działają tu jako oddzielny typ komponentu. Dla każdego włączonego collection proxy faza `Update` jest wykonywana rekurencyjnie, zaczynając od kroku 1. |
| 3 | **Late Update** | `late_update()` | Wywoływana raz na klatkę dla każdego typu komponentu implementującego Late Update według priorytetu. |
| 4 | **Transforms** |  | Na końcu przeprowadzana jest dodatkowa aktualizacja transformacji dla każdego komponentu, jeśli jest to potrzebne. |

W razie potrzeby więcej informacji o wewnętrznym działaniu fazy Update można znaleźć w kodzie [`gameobject.cpp`](https://github.com/defold/defold/blob/dev/engine/gameobject/src/gameobject/gameobject.cpp).

### Faza renderowania (Render Update Phase)

W bloku `Render Update` najpierw przetwarzane są wszystkie wiadomości wysłane na gniazdo `@render` (np. wiadomości `set_view_projection`, `set_clear_color` itd.). Następnie wywoływana jest funkcja `update()` skryptu renderującego.

![Render Update Phase](images/application_lifecycle/render_update_phase.png)

### Faza post-aktualizacji (Post update Phase)

Po aktualizacjach uruchamiana jest sekwencja post-aktualizacji. Z pamięci są zwalniani collection proxy oznaczeni do wyładowania (co następuje podczas sekwencji `dispatch messages`). Wszystkie obiekty oznaczone do usunięcia wywołują `final()` we wszystkich komponentach je posiadających. Kod w tych funkcjach może wysyłać kolejne wiadomości, stąd po `final()` ponownie uruchamiana jest sekwencja rozsyłania wiadomości.

![Post Update Phase](images/application_lifecycle/post_update_phase.png)

Następnie komponenty fabryki, które miały zostać uruchomione, tworzą obiekty. Na końcu obiekty oznaczone do usunięcia są faktycznie usuwane.

### Faza renderowania (Render Phase)

Ostatnim krokiem pętli aktualizacyjnej jest obsłużenie wiadomości wysyłanych do gniazda `@system` (`exit`, `reboot`, przełączanie profilera, uruchamianie i zatrzymywanie nagrywania wideo itd.).

![Render Phase](images/application_lifecycle/render_phase.png)

Następnie grafika jest renderowana, w tym wizualizacja profilera (zobacz [dokumentację debugowania](/manuals/debugging)). Zaraz po renderowaniu następuje przechwytywanie wideo.

#### Liczba klatek i krok czasowy kolekcji

Liczba klatek na sekundę (odpowiednio liczba przebiegów pętli aktualizacyjnej) jest ustawiana w ustawieniach projektu albo dynamicznie przez wysłanie wiadomości `set_update_frequency` do gniazda `@system`. Można też ustawić _time step_ dla każdego collection proxy przez `set_time_step`. Zmiana kroku kolekcji nie wpływa na liczbę klatek (czyli ilość wywołań `update()` w każdej klatce), ale zmienia czas kroków fizyki oraz wartość `dt` przekazywaną do `update()`.

(Zobacz [Instrukcję pełnomocników kolekcji](/manuals/collection-proxy) i [`set_time_step`](/ref/collectionproxy#set-time-step) po więcej szczegółów)

#### Ograniczanie pracy silnika

W Defold 1.12.0 dodano API ograniczające pracę silnika, które może pominąć aktualizacje i renderowanie, jednocześnie wykrywając wejście. Każde wejście budzi silnik i po okresie chłodzenia można ponownie wejść w ograniczoną pracę.

Zobacz `sys.set_engine_throttle()` dla szczegółów i przykładów użycia.

## Faza finalizacyjna

Gdy aplikacja kończy pracę, najpierw dokańcza ostatnią sekwencję pętli aktualizacyjnej, która zwalnia collection proxy – finalizując i usuwając obiekty wewnątrz nich.

Po tym silnik przechodzi do samej finalizacji, która dotyczy głównej kolekcji i jej obiektów:

![Finalization](images/application_lifecycle/finalization.png)

Na początku wywoływane są funkcje `final()` wszystkich komponentów. Później uruchamiana jest sekwencja rozsyłania wiadomości. Na końcu wszystkie obiekty są usuwane, a główna kolekcja zostaje zwolniona.

Silnik dalej kończy pracę wewnętrznych subsystemów, np. usuwa konfigurację projektu, zatrzymuje profiler pamięci itd.

Aplikacja jest wtedy całkowicie zamknięta.

## Rozsyłanie wiadomości (Dispatching Messages)

`Dispatching Messages` to specjalne przejście wykonywane po **każdej** aktualizacji typu komponentu (np. aktualizacji sprite’a, skryptów itp.). W tym kroku wszystkie zgromadzone wiadomości są rozsyłane. Diagram oznacza te działania ikoną koperty ze strzałką 📩.

![Dispatch Messages](images/application_lifecycle/dispatch_messages.png)

Po tym, jak wszystkie **wiadomości użytkownika** zostaną dostarczone przez wywołanie `on_message()`, silnik obsługuje specjalne wiadomości Defold w następującej kolejności (przy każdym collection proxy):

1. `load` – ładuje pełnomocniki oznaczone do wczytania, wysyła z powrotem `proxy_loaded`.
2. `unload` – zwalnia pełnomocniki oznaczone do zwolnienia, wysyła `proxy_unloaded`.
3. `init` – wywołuje fazę `Collection Init` dla proxy zaznaczonych do inicjalizacji.
4. `final` – wywołuje `final()` dla wszystkich komponentów proxy oznaczonych do zamknięcia.
5. `enable` – aktywuje collection proxy, żeby w następnej klatce wykonać dla niego `Update Loop`; to też uruchamia `init()` dla składników proxy.
6. `disable` – dezaktywuje collection proxy, więc pętla aktualizacyjna nie będzie dla niego wykonywana.

Ponieważ kod odbiorców `on_message()` może publikować kolejne wiadomości, dispatcher kontynuuje przetwarzanie kolejki aż do jej opróżnienia. Jednak dispatcher ma limit liczby przejść przez kolejkę. Więcej informacji znaleźć można w rozdziale [Message Chains](/manuals/message-passing).
