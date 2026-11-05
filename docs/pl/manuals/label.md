---
title: Komponenty tekstowe Label w Defold
brief: Ta instrukcja wyjaśnia, jak używać komponentów Label do wyświetlania tekstu na obiektach gry w świecie gry.
---

# Label

Komponent *Label* renderuje fragment tekstu na ekranie, w przestrzeni gry. Domyślnie jest sortowany i rysowany razem ze wszystkimi grafikami sprite i tile. Komponent ma zestaw właściwości, które określają sposób renderowania tekstu. GUI w Defold obsługuje tekst, ale umieszczanie elementów GUI w świecie gry może być trudne. Label ułatwia to zadanie.

## Tworzenie Label

Aby utworzyć komponent Label, <kbd>kliknij prawym przyciskiem myszy</kbd> obiekt gry i wybierz <kbd>Add Component ▸ Label</kbd>.

![Dodawanie Label](images/label/add_label.png)

(Jeśli chcesz utworzyć kilka Label z tego samego szablonu, możesz też utworzyć nowy plik komponentu Label: <kbd>kliknij prawym przyciskiem myszy</kbd> folder w przeglądarce *Assets* i wybierz <kbd>New... ▸ Label</kbd>, a następnie dodaj ten plik jako komponent do dowolnych obiektów gry.)

![Nowy Label](images/label/label.png)

Ustaw właściwość *Font* na font, którego chcesz użyć, i upewnij się, że właściwość *Material* wskazuje materiał zgodny z typem fontu:

![Font i material](images/label/font_material.png)

## Fonty wektorowe i kolorowe emoji {#vector-fonts-and-color-emoji}

Aby używać fontu Vector, wykonaj kroki [konfiguracji fontów wektorowych](/manuals/font/#vector-fonts), przypisz zasób `.font` do właściwości *Font* etykiety i ustaw jej *Material* na `/builtins/fonts/label-vector.material`. Rozmiar wyświetlanego tekstu określa *Font Size*.

Aby wyświetlać kolorowe emoji, wykonaj też [konfigurację fontu zapasowego COLRv1 i zasobów paczki](/manuals/font/#color-emoji). Poniższy przykład zakłada etykietę o identyfikatorze `label` i skrypt na tym samym obiekcie gry. Pozostaw *Text* etykiety puste, aby powitanie pojawiło się dopiero po przygotowaniu jego glifów:

```lua
function init(self)
    local text = "Hello 😀 🍎 🚀"
    local font_resource = go.get("#label", "font")
    -- Dodaj font zastępczy raz dla tego współdzielonego zasobu fontu.
    font.add_font(font_resource, "/fonts/NotoColorEmoji-Regular.ttf")
    font.prewarm_text(font_resource, text, function(self, request_id, result, err)
        if result then
            go.set("#label", "text", text)
        else
            print("Could not prepare label text:", err)
        end
    end)
end
```

Zwykłe litery korzystają z oryginalnego fontu, a emoji z dodanego fontu kolorowego. Jeśli inne etykiety lub węzły tekstowe GUI współdzielą ten zasób fontu, zainicjalizuj font zapasowy w jednym miejscu i używaj go ponownie.

## Właściwości Label

Oprócz właściwości *Id*, *Position*, *Rotation* i *Scale* istnieją też następujące właściwości specyficzne dla komponentu:

*Text*
: Treść tekstu Label.

*Size*
: Rozmiar ramki ograniczającej tekst. Jeśli ustawiono *Line Break*, szerokość określa miejsce, w którym tekst zostanie zawinięty.

*Color*
: Kolor tekstu.

*Outline*
: Kolor obrysu.

*Shadow*
: Kolor cienia.

::: sidenote
Należy pamiętać, że domyślny materiał ma renderowanie cienia wyłączone ze względów wydajnościowych.
:::

*Leading*
: Skalowany współczynnik odstępu między wierszami. Wartość 0 oznacza brak odstępu między wierszami. Domyślnie wynosi 1.

*Tracking*
: Skalowany współczynnik odstępu między literami. Domyślnie wynosi 0.

*Pivot*
: Punkt zaczepienia tekstu. Użyj go, aby zmienić wyrównanie tekstu (patrz niżej).

*Blend Mode*
: Tryb mieszania używany podczas renderowania Label.

*Line Break*
: Wyrównanie tekstu zależy od ustawienia pivot, a włączenie tej właściwości pozwala tekstowi płynąć w kilku wierszach. Szerokość komponentu określa miejsce zawijania tekstu. Pamiętaj, że w tekście musi być spacja, aby mogło dojść do złamania.

*Font*
: Zasób fontu używany przez ten Label.

*Material*
: Materiał używany do renderowania etykiety. Wybierz materiał pasujący do trybu lub źródła fontu (Bitmap, SDF, Vector lub BMFont). Pasujące wbudowane materiały etykiet opisano w sekcji [Materiały fontów](/manuals/font/#font-materials).

### Tryby mieszania
:[blend-modes](../shared/blend-modes.md)

### Pivot i wyrównanie

Ustawiając właściwość *Pivot*, możesz zmienić sposób wyrównania tekstu.

*Center*
: Jeśli pivot jest ustawiony na `Center`, `North` lub `South`, tekst jest wyrównany do środka.

*Left*
: Jeśli pivot jest ustawiony na dowolny z trybów `West`, tekst jest wyrównany do lewej.

*Right*
: Jeśli pivot jest ustawiony na dowolny z trybów `East`, tekst jest wyrównany do prawej.

![Wyrównanie tekstu](images/label/align.png)

## Modyfikowanie w czasie działania

Możesz modyfikować Label w czasie działania, odczytując i ustawiając tekst Label oraz inne właściwości.

`text`
: Treść etykiety (`string`). Dostępna przez `go.get()` i `go.set()`.

`color`
: Kolor Label (`vector4`)

`outline`
: Kolor obrysu Label (`vector4`)

`shadow`
: Kolor cienia Label (`vector4`)

`scale`
: Skala Label, jako `number` dla jednolitego skalowania albo `vector3` dla osobnego skalowania wzdłuż każdej osi.

`size`
: Rozmiar Label (`vector3`)

```lua
function init(self)
    -- Ustaw tekst komponentu "my_label" w tym samym obiekcie gry
    -- co ten skrypt.
    go.set("#my_label", "text", "New text")
    local text = go.get("#my_label", "text")
    print(text) -- New text
end
```

::: sidenote
Funkcje `label.set_text()` i `label.get_text()` są przestarzałe i zaleca się używanie właściwości `text`. Stare funkcje pozostają dostępne dla zgodności. Stara funkcja ustawiająca tekst umieszcza wiadomość w kolejce, natomiast `go.set()` aktualizuje tekst natychmiast.
:::

```lua
function init(self)
    -- Ustaw kolor komponentu "my_label" w tym samym obiekcie gry.
    -- Kolor to wartość RGBA przechowywana w vector4.
    local grey = vmath.vector4(0.5, 0.5, 0.5, 1.0)
    go.set("#my_label", "color", grey)

    -- ...i usuń obrys, ustawiając jego alfę na 0...
    go.set("#my_label", "outline.w", 0)

    -- ...i przeskaluj go 2x wzdłuż osi x.
    local scale_x = go.get("#my_label", "scale.x")
    go.set("#my_label", "scale.x", scale_x * 2)
end
```

## Konfiguracja projektu

Plik *game.project* ma kilka [ustawień projektu](/manuals/project-settings#label) związanych z Label.
