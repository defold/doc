---
title: "Skrypty edytora: UI"
brief: Ta instrukcja wyjaśnia, jak tworzyć elementy UI w edytorze przy użyciu Lua
---

# Skrypty edytora i UI

Ta instrukcja wyjaśnia, jak tworzyć interaktywne elementy UI w edytorze przy użyciu skryptów edytora napisanych w Lua. Aby zacząć pracę ze skryptami edytora, zobacz [instrukcję skryptów edytora](/manuals/editor-scripts). Pełne API edytora znajdziesz [tutaj](/ref/stable/editor-lua/). Obecnie można tworzyć tylko interaktywne okna dialogowe, chociaż w przyszłości chcemy rozszerzyć obsługę skryptowego UI na resztę edytora.

## Witaj świecie

Cała funkcjonalność związana z UI znajduje się w module `editor.ui`. Oto najprostszy przykład skryptu edytora z własnym UI na start:
```lua
local M = {}

function M.get_commands()
    return {
        {
            label = "Do with confirmation",
            locations = {"View"},
            run = function()
                local result = editor.ui.show_dialog(editor.ui.dialog({
                    title = "Perform action?",
                    buttons = {
                        editor.ui.dialog_button({
                            text = "Cancel",
                            cancel = true,
                            result = false
                        }),
                        editor.ui.dialog_button({
                            text = "Perform",
                            default = true,
                            result = true
                        })
                    }
                }))
                print('Perform action:', result)
            end
        }
    }
end

return M

```

Ten fragment kodu definiuje polecenie **<kbd>View → Do with confirmation</kbd>**. Gdy je uruchomisz, zobaczysz następujące okno dialogowe:

![Okno dialogowe przykładu „Witaj świecie”](images/editor_scripts/perform_action_dialog.png)

Na końcu, po naciśnięciu <kbd>Enter</kbd> (albo kliknięciu przycisku `Perform`), w konsoli edytora zobaczysz następujący wiersz:
```
Perform action:	true
```

## Podstawowe pojęcia

### Komponenty

Edytor udostępnia różne **komponenty** UI, które można składać, aby uzyskać pożądany interfejs. Zgodnie z konwencją wszystkie komponenty są konfigurowane pojedynczą tabelą o nazwie **props**. Same komponenty nie są tabelami, lecz **niezmiennymi userdata** używanymi przez edytor do tworzenia UI.

### Props

**Props** to tabele definiujące wejścia komponentów. Należy traktować je jako niezmienne: modyfikowanie tabeli props in-place nie spowoduje ponownego renderowania komponentu, ale użycie innej tabeli już tak. UI jest aktualizowane wtedy, gdy instancja komponentu otrzyma tabelę props, która w płytkim porównaniu nie jest równa poprzedniej.

### Wyrównanie

Gdy komponent otrzyma jakiś obszar w UI, zajmie całą dostępną przestrzeń, ale nie oznacza to, że widoczna część komponentu się rozciągnie. Zamiast tego widoczna część zajmie tyle miejsca, ile potrzebuje, a następnie zostanie wyrównana w obrębie przydzielonego obszaru. Dlatego większość wbudowanych komponentów definiuje pole `alignment`.

Na przykład rozważ ten komponent etykiety:
```lua
editor.ui.label({
    text = "Hello",
    alignment = editor.ui.ALIGNMENT.RIGHT
})
```
Widoczna część to tekst `Hello`, a w obrębie przydzielonego obszaru komponentu jest on wyrównany tak:

![Wyrównanie](images/editor_scripts/alignment.png)

## Wbudowane komponenty

Edytor definiuje różne wbudowane komponenty, których można używać razem do budowania UI. Komponenty można z grubsza podzielić na 3 kategorie: układ, prezentacja danych i wejście.

### Komponenty układu

Komponenty układu służą do umieszczania innych komponentów obok siebie. Główne komponenty układu to **`horizontal`**, **`vertical`** i **`grid`**. Komponenty te definiują też pola takie jak **padding** i **spacing**, gdzie padding oznacza pustą przestrzeń od krawędzi przydzielonego obszaru do zawartości, a spacing pustą przestrzeń między elementami potomnymi:

![Padding i Spacing](images/editor_scripts/padding_and_spacing.png)

Edytor definiuje `small`, `medium` i `large` stałe dla paddingu i spacingu. W przypadku spacingu wartość `small` jest przeznaczona do odstępów między różnymi podelementami pojedynczego elementu UI, `medium` do odstępów między poszczególnymi elementami UI, a `large` do odstępów między grupami elementów. Domyślny spacing to `medium`. Dla paddingu wartość `large` oznacza odstęp od krawędzi okna do zawartości, `medium` odstęp od krawędzi istotnego elementu UI, a `small` odstęp od krawędzi małych elementów UI, takich jak menu kontekstowe i podpowiedzi, które nie są jeszcze zaimplementowane.

Kontener **`horizontal`** umieszcza swoje elementy potomne jeden po drugim w poziomie, zawsze rozciągając wysokość każdego elementu potomnego tak, aby wypełniała dostępną przestrzeń. Domyślnie szerokość każdego elementu potomnego jest utrzymywana na minimalnym poziomie, ale można sprawić, by zajmował tyle miejsca, ile się da, ustawiając w nim pole `grow` na `true`.

Kontener **`vertical`** jest podobny do horizontal, ale z zamienionymi osiami.

Na koniec, **`grid`** to komponent kontenera, który układa elementy potomne w dwuwymiarowej siatce, podobnie jak tabela. Ustawienie `grow` w siatce dotyczy wierszy albo kolumn, dlatego ustawia się je nie na elemencie potomnym, ale w tabeli konfiguracji kolumny. Dodatkowo elementy potomne w siatce można skonfigurować tak, aby zajmowały wiele wierszy lub kolumn za pomocą pól `row_span` i `column_span`. Siatki są przydatne przy tworzeniu formularzy z wieloma polami wejściowymi:
```lua
editor.ui.grid({
    padding = editor.ui.PADDING.LARGE, -- dodaj padding wokół krawędzi dialogu
    columns = {{}, {grow = true}}, -- spraw, by druga kolumna się rozciągała
    children = {
        {
            editor.ui.label({ 
                text = "Level Name",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        },
        {
            editor.ui.label({ 
                text = "Author",
                alignment = editor.ui.ALIGNMENT.RIGHT
            }),
            editor.ui.string_field({})
        }
    }
})
```
Powyższy kod utworzy następujący formularz w oknie dialogowym:

![Formularz nowego poziomu](images/editor_scripts/new_level_dialog.png)

### Komponenty prezentacji danych

Edytor definiuje 4 komponenty prezentacji danych:
- **`label`** — etykieta tekstowa przeznaczona do używania z polami formularzy.
- **`icon`** — ikona; obecnie można jej używać tylko do prezentowania niewielkiego zestawu predefiniowanych ikon, ale w przyszłości chcemy dopuścić więcej ikon.
- **`heading`** — element tekstowy przeznaczony do wyświetlania wiersza nagłówka, na przykład w formularzu lub oknie dialogowym. Enum `editor.ui.HEADING_STYLE` definiuje różne style nagłówków, w tym nagłówki `H1`-`H6` z HTML-a, a także specyficzne dla edytora `DIALOG` i `FORM`.
- **`paragraph`** — element tekstowy przeznaczony do wyświetlania akapitu tekstu. Główna różnica względem `label` polega na tym, że paragraph obsługuje zawijanie wierszy: jeśli przydzielony obszar jest zbyt wąski, tekst zostanie zawinięty, a jeśli nadal nie zmieści się w widoku, zostanie ewentualnie skrócony do `"..."`.

### Komponenty wejściowe

Komponenty wejściowe służą do interakcji użytkownika z UI. Wszystkie komponenty wejściowe obsługują pole `enabled`, które kontroluje, czy interakcja jest włączona, oraz definiują różne callbacki powiadamiające skrypt edytora o interakcji.

Jeśli tworzysz statyczne UI, wystarczy zdefiniować callbacki, które po prostu modyfikują zmienne lokalne. W przypadku dynamicznych interfejsów i bardziej zaawansowanych interakcji zobacz sekcję [reaktywność](#reactivity).

Na przykład można tak utworzyć proste, statyczne okno dialogowe tworzenia nowego pliku:
```lua
-- początkowa nazwa pliku, zostanie zastąpiona przez dialog
local file_name = ""
local create_file = editor.ui.show_dialog(editor.ui.dialog({
    title = "Utwórz nowy plik",
    content = editor.ui.horizontal({
        padding = editor.ui.PADDING.LARGE,
        spacing = editor.ui.SPACING.MEDIUM,
        children = {
            editor.ui.label({
                text = "Nazwa nowego pliku",
                alignment = editor.ui.ALIGNMENT.CENTER
            }),
            editor.ui.string_field({
                grow = true,
                text = file_name,
                -- Callback wywoływany podczas wpisywania:
                on_value_changed = function(new_text)
                    file_name = new_text
                end
            })
        }
    }),
    buttons = {
        editor.ui.dialog_button({ text = "Anuluj", cancel = true, result = false }),
        editor.ui.dialog_button({ text = "Utwórz plik", default = true, result = true })
    }
}))
if create_file then
    print("create", file_name)
end
```
Oto lista wbudowanych komponentów wejściowych:
- **`string_field`**, **`integer_field`** i **`number_field`** to warianty jednoliniowego pola tekstowego, które pozwalają edytować odpowiednio łańcuchy znaków, liczby całkowite i liczby.
- **`select_box`** służy do wybierania opcji z predefiniowanej tablicy za pomocą listy rozwijanej.
- **`check_box`** to logiczne pole wejściowe z callbackiem `on_value_changed`.
- **`button`** z callbackiem `on_press`, który jest wywoływany po naciśnięciu przycisku.
- **`external_file_field`** to komponent przeznaczony do wybierania ścieżki do pliku na komputerze. Składa się z pola tekstowego i przycisku otwierającego okno wyboru pliku.
- **`resource_field`** to komponent przeznaczony do wybierania zasobu w projekcie.

Wszystkie komponenty poza przyciskami pozwalają ustawić pole `issue`, które wyświetla problem powiązany z komponentem, czyli `editor.ui.ISSUE_SEVERITY.ERROR` albo `editor.ui.ISSUE_SEVERITY.WARNING`, na przykład:
```lua
issue = {severity = editor.ui.ISSUE_SEVERITY.WARNING, message = "Ta wartość jest przestarzała"}
```
Gdy issue jest określone, zmienia wygląd komponentu wejściowego i dodaje podpowiedź z komunikatem problemu.

Oto demonstracja wszystkich pól wejściowych wraz z ich wariantami issue:

![Pola wejściowe](images/editor_scripts/inputs_demo.png)

### Komponenty związane z dialogami

Aby wyświetlić okno dialogowe, musisz użyć funkcji `editor.ui.show_dialog`. Oczekuje ona komponentu **`dialog`**, który definiuje główną strukturę dialogów Defold: `title`, `header`, `content` i `buttons`. Komponent dialog jest trochę wyjątkowy: nie można użyć go jako elementu potomnego innego komponentu, ponieważ reprezentuje okno, a nie element UI. `header` i `content` są jednak zwykłymi komponentami.

Przyciski dialogowe też są szczególne: tworzy się je za pomocą komponentu **`dialog_button`**. W odróżnieniu od zwykłych przycisków przyciski dialogowe nie mają callbacku `on_pressed`. Zamiast tego definiują pole `result` z wartością, którą funkcja `editor.ui.show_dialog` zwróci po zamknięciu dialogu. Przyciski dialogowe definiują też logiczne pola `cancel` i `default`: przycisk z polem `cancel` jest uruchamiany, gdy użytkownik naciśnie <kbd>Escape</kbd> albo zamknie dialog przyciskiem zamykania systemu operacyjnego, a przycisk `default` jest uruchamiany, gdy użytkownik naciśnie <kbd>Enter</kbd>. Przycisk dialogowy może mieć jednocześnie ustawione `cancel` i `default` na `true`.

### Komponenty pomocnicze

Dodatkowo edytor definiuje kilka komponentów pomocniczych:
- **`separator`** to cienka linia używana do oddzielania bloków zawartości
- **`scroll`** to komponent opakowujący, który pokazuje paski przewijania, gdy opakowany komponent nie mieści się w przydzielonej przestrzeni

## Reaktywność

Ponieważ komponenty są **niezmiennymi userdata**, po ich utworzeniu nie da się ich zmieniać. Jak więc sprawić, żeby UI zmieniało się w czasie? Odpowiedź: **komponenty reaktywne**.

::: sidenote
UI skryptów edytora czerpie inspirację z biblioteki [React](https://react.dev/), więc wiedza o reaktywnym UI i hookach Reacta będzie pomocna.
:::

Najprościej mówiąc, komponent reaktywny to komponent z funkcją Lua, która otrzymuje dane (props) i zwraca widok, czyli inny komponent. Funkcja komponentu reaktywnego może używać **hooków**: specjalnych funkcji w module `editor.ui`, które dodają komponentom cechy reaktywne. Zgodnie z konwencją wszystkie hooki mają nazwy zaczynające się od `use_`.

Aby utworzyć komponent reaktywny, użyj funkcji `editor.ui.component()`.

Spójrzmy na przykład: okno dialogowe tworzenia nowego pliku, które pozwala utworzyć plik tylko wtedy, gdy wpisana nazwa pliku nie jest pusta:

```lua
-- 1. dialog jest komponentem reaktywnym
local dialog = editor.ui.component(function(props)
    -- 2. komponent definiuje lokalny stan, czyli nazwę pliku, która domyślnie jest pustym ciągiem
    local name, set_name = editor.ui.use_state("")

    return editor.ui.dialog({ 
        title = props.title,
        content = editor.ui.vertical({
            padding = editor.ui.PADDING.LARGE,
            children = { 
                editor.ui.string_field({ 
                    value = name,
                    -- 3. wpisywanie i Enter aktualizują lokalny stan
                    on_value_changed = set_name 
                }) 
            }
        }),
        buttons = {
            editor.ui.dialog_button({ 
                text = "Anuluj", 
                cancel = true 
            }),
            editor.ui.dialog_button({ 
                text = "Utwórz plik",
                -- 4. tworzenie jest włączone, gdy nazwa nie jest pusta
                enabled = name ~= "",
                default = true,
                -- 5. wynikiem jest nazwa
                result = name
            })
        }
    })
end)

-- 6. show_dialog zwróci albo niepustą nazwę pliku, albo nil po anulowaniu
local file_name = editor.ui.show_dialog(dialog({ title = "Nazwa nowego pliku" }))
if file_name then 
    print("create " .. file_name)
else
    print("cancelled")
end
```

Gdy uruchomisz polecenie menu wykonujące ten kod, edytor pokaże na początku dialog z wyłączonym przyciskiem `<kbd>Create File</kbd>`, ale gdy wpiszesz nazwę i naciśniesz <kbd>Enter</kbd>, przycisk stanie się aktywny:

![Okno dialogowe tworzenia nowego pliku](images/editor_scripts/reactive_new_file_dialog.png)

Jak to działa? Przy pierwszym renderowaniu hook `use_state` tworzy lokalny stan powiązany z komponentem i zwraca go wraz z setterem tego stanu. Gdy funkcja settera zostanie wywołana, planuje ponowne renderowanie komponentu. Podczas kolejnych renderowań funkcja komponentu jest wywoływana ponownie, a `use_state` zwraca zaktualizowany stan. Nowy komponent widoku zwrócony przez funkcję komponentu jest następnie porównywany z poprzednim, a UI jest aktualizowane tam, gdzie wykryto zmiany.

Takie reaktywne podejście bardzo upraszcza budowanie interaktywnych interfejsów i utrzymywanie ich w synchronizacji: zamiast jawnie aktualizować wszystkie dotknięte komponenty UI po danych wejściowych użytkownika, definiujesz widok jako czystą funkcję danych wejściowych (props i stanu lokalnego), a edytor sam obsługuje wszystkie aktualizacje.

### Zasady reaktywności

Edytor oczekuje, że reaktywne komponenty funkcyjne będą zachowywać się poprawnie, żeby to działało:

1. Funkcje komponentów muszą być czyste. Nie ma gwarancji, kiedy ani jak często funkcja komponentu zostanie wywołana. Wszystkie efekty uboczne powinny znajdować się poza renderowaniem, na przykład w callbackach.
2. Props i stan lokalny muszą być niezmienne. Nie mutuj props. Jeśli stan lokalny jest tabelą, nie modyfikuj jej in-place, tylko utwórz nową i przekaż ją do settera, gdy stan ma się zmienić.
3. Funkcje komponentów muszą wywoływać te same hooki w tej samej kolejności przy każdym wywołaniu. Nie wywołuj hooków wewnątrz pętli, w blokach warunkowych, po wcześniejszych return itd. Dobrą praktyką jest wywoływanie hooków na początku funkcji komponentu, przed jakimkolwiek innym kodem.
4. Wywołuj hooki tylko z funkcji komponentów. Hooki działają w kontekście komponentu reaktywnego, dlatego wolno je wywoływać wyłącznie w funkcji komponentu albo w innej funkcji wywoływanej bezpośrednio przez funkcję komponentu.

### Hooki

::: sidenote
Jeśli znasz [React](https://react.dev/), zauważysz, że hooki w edytorze mają nieco inną semantykę, jeśli chodzi o zależności hooków.
:::

Edytor definiuje 2 hooki: **`use_memo`** i **`use_state`**.

### **`use_state`**

Lokalny stan można utworzyć na 2 sposoby: z wartością domyślną albo z funkcją inicjalizującą:
```lua
-- wartość domyślna
local enabled, set_enabled = editor.ui.use_state(true)
-- funkcja inicjalizująca + argumenty
local id, set_id = editor.ui.use_state(string.lower, props.name)
```
Podobnie setter można wywołać z nową wartością albo funkcją aktualizującą:
```lua
-- funkcja aktualizująca
local function increment_by(n, by)
    return n + by
end

local counter = editor.ui.component(function(props)
    local count, set_count = editor.ui.use_state(0)
    
    return editor.ui.horizontal({
        spacing = editor.ui.SPACING.SMALL,
        children = {
            editor.ui.label({
                text = tostring(count),
                alignment = editor.ui.ALIGNMENT.LEFT,
                grow = true
            }),
            editor.ui.text_button({
                text = "+1",
                on_pressed = function() set_count(increment_by, 1) end
            }),
            editor.ui.text_button({
                text = "+5",
                on_pressed = function() set_count(increment_by, 5) end
            })
        }
    })
end)
```

Na koniec stan może zostać **zresetowany**. Dochodzi do tego, gdy zmieni się którykolwiek z argumentów przekazywanych do `editor.ui.use_state()`, sprawdzanych przez `==`. Z tego powodu nie wolno używać literałów tabel ani literałowych funkcji inicjalizujących jako argumentów haka `use_state`, bo spowoduje to reset stanu przy każdym ponownym renderowaniu. Dla zobrazowania:
```lua
-- ❌ ŹLE: literał tabeli w inicjalizatorze powoduje reset stanu przy każdym ponownym renderowaniu
local user, set_user = editor.ui.use_state({ first_name = props.first_name, last_name = props.last_name})

-- ✅ DOBRZE: użyj funkcji inicjalizującej poza funkcją komponentu, aby utworzyć stan tabeli
local function create_user(first_name, last_name) 
    return { first_name = first_name, last_name = last_name}
end
-- ...później, wewnątrz funkcji komponentu:
local user, set_user = editor.ui.use_state(create_user, props.first_name, props.last_name)


-- ❌ ŹLE: literał funkcji inicjalizującej powoduje reset stanu przy każdym ponownym renderowaniu
local id, set_id = editor.ui.use_state(function() return string.lower(props.name) end)

-- ✅ DOBRZE: użyj referencji do funkcji inicjalizującej, aby utworzyć stan
local id, set_id = editor.ui.use_state(string.lower, props.name)
```

### **`use_memo`**

Możesz użyć haka `use_memo`, aby poprawić wydajność. W funkcjach renderujących często wykonuje się pewne obliczenia, na przykład sprawdzanie poprawności danych wejściowych użytkownika. Haka `use_memo` można użyć wtedy, gdy sprawdzenie, czy argumenty funkcji obliczeniowej się zmieniły, jest tańsze niż samo wywołanie tej funkcji. Hak wywoła funkcję obliczeniową przy pierwszym renderowaniu i ponownie wykorzysta obliczoną wartość podczas kolejnych renderowań, jeśli wszystkie argumenty `use_memo` pozostaną bez zmian:
```lua
-- funkcja walidująca poza funkcją komponentu
local function validate_password(password)
    if #password < 8 then
        return false, "Hasło musi mieć co najmniej 8 znaków."
    elseif not password:match("%l") then
        return false, "Hasło musi zawierać co najmniej jedną małą literę."
    elseif not password:match("%u") then
        return false, "Hasło musi zawierać co najmniej jedną wielką literę."
    elseif not password:match("%d") then
        return false, "Hasło musi zawierać co najmniej jedną cyfrę."
    else
        return true, "Hasło jest poprawne."
    end
end

-- ...później, wewnątrz funkcji komponentu
local username, set_username = editor.ui.use_state('')
local password, set_password = editor.ui.use_state('')
local valid, message = editor.ui.use_memo(validate_password, password)
```
W tym przykładzie walidacja hasła wykona się przy każdej zmianie hasła, na przykład podczas wpisywania w polu hasła, ale nie wtedy, gdy zmieni się nazwa użytkownika.

Innym zastosowaniem haka `use_memo` jest tworzenie callbacków, które są potem używane w komponentach wejściowych, albo sytuacje, gdy lokalnie utworzona funkcja jest używana jako wartość props innego komponentu. To zapobiega niepotrzebnym ponownym renderowaniom.
