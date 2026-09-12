---
title: "Editor-Skripte: Benutzeroberfläche"
brief: Dieses Handbuch erklärt, wie du mit Lua UI-Elemente im Editor erstellst
---

# Editor-Skripte und Benutzeroberflächen {#editor-scripts-and-ui}

Dieses Handbuch erklärt, wie du mit in Lua geschriebenen Editor-Skripten interaktive Dialogfelder erstellst und Ressourcen im Editor öffnest. Einen Einstieg in Editor-Skripte findest du im [Handbuch zu Editor-Skripten](/manuals/editor-scripts). Die vollständige API-Referenz des Editors findest du [hier](/ref/stable/editor-lua/).

## Hallo Welt {#hello-world}

Alle Funktionen für Benutzeroberflächen befinden sich im Modul `editor.ui`. Hier ist zum Einstieg das einfachste Beispiel für ein Editor-Skript mit einer benutzerdefinierten Benutzeroberfläche:
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

Dieser Codeausschnitt definiert einen Befehl **View → Do with confirmation**. Wenn du ihn ausführst, siehst du das folgende Dialogfeld:

![Hallo-Welt-Dialogfeld](images/editor_scripts/perform_action_dialog.png)

Nachdem du <kbd>Enter</kbd> drückst (oder auf die Schaltfläche `Perform` klickst), siehst du schließlich die folgende Zeile in der Editorkonsole:
```
Perform action:	true
```

## Ressourcen öffnen {#opening-resources}

Rufe `editor.ui.open_resource()` in der Funktion `run` eines Befehls auf, um eine Projektressource zu öffnen. Der Pfad beginnt mit `/`. Wenn du die Ansicht weglässt, wird die primäre Ansicht der Ressource ausgewählt:

```lua
editor.ui.open_resource("/main/main.script")
```

Die Ansichten `code` und `text` akzeptieren als drittes Argument eine Cursorposition oder eine Auswahl. Zeilen- und Spaltennummern beginnen bei `1`; eine fehlende Spaltenangabe hat den Standardwert `1`. Gib die Ansicht an, wenn du diese Argumente übergibst:

```lua
editor.ui.open_resource("/main/main.script", "code", { line = 10 })
editor.ui.open_resource("/main/main.script", "code", { line = 10, column = 5 })
```

Um einen Bereich auszuwählen, gib stattdessen die Cursorpositionen `from` und `to` an:

```lua
editor.ui.open_resource("/main/main.script", "code", {
    from = { line = 10, column = 1 },
    to = { line = 12, column = 1 }
})
```

Die konfigurierte Ressourcenansicht kann im Editor oder in einer externen Anwendung geöffnet werden. Die integrierten Ansichten Code und Text unterstützen die Argumente für Cursorposition und Auswahl. Die unterstützten Ansichtsnamen findest du unter [`editor.ui.open_resource()`](/ref/beta/editor/#editor.ui.open_resource:resource_path-view-args).

## Grundbegriffe {#basic-concepts}

### Komponenten {#components}

Der Editor bietet verschiedene UI-**Komponenten** (components), die du kombinieren kannst, um die gewünschte Benutzeroberfläche zu erstellen. Konventionsgemäß werden alle Komponenten mit einer einzigen Tabelle namens **props** konfiguriert. Die Komponenten selbst sind keine Tabellen, sondern **unveränderliche userdata-Werte**, die der Editor zum Erstellen der Benutzeroberfläche verwendet.

### Props

**Props** sind Tabellen, die Eingaben für Komponenten definieren. Props sollten als unveränderlich behandelt werden: Wenn du die Props-Tabelle direkt änderst, wird die Komponente nicht erneut gerendert. Verwendest du jedoch eine andere Tabelle, wird sie erneut gerendert. Die Benutzeroberfläche wird aktualisiert, wenn die Komponenteninstanz eine Props-Tabelle erhält, die bei einem flachen Vergleich mit der vorherigen Tabelle nicht übereinstimmt.

### Ausrichtung {#alignment}

Wenn der Komponente ein Bereich in der Benutzeroberfläche zugewiesen wird, nimmt sie den gesamten Platz ein. Das bedeutet jedoch nicht, dass der sichtbare Teil der Komponente gestreckt wird. Stattdessen nimmt der sichtbare Teil den benötigten Platz ein und wird dann innerhalb des zugewiesenen Bereichs ausgerichtet. Daher definieren die meisten integrierten Komponenten eine Eigenschaft `alignment`.

Betrachte beispielsweise diese Beschriftungskomponente:
```lua
editor.ui.label({
    text = "Hello",
    alignment = editor.ui.ALIGNMENT.RIGHT
})
```
Der sichtbare Teil ist der Text `Hello`, der innerhalb des zugewiesenen Komponentenbereichs ausgerichtet wird:

![Ausrichtung](images/editor_scripts/alignment.png)

## Integrierte Komponenten {#built-in-components}

Der Editor definiert verschiedene integrierte Komponenten, die du zum Erstellen der Benutzeroberfläche kombinieren kannst. Komponenten lassen sich grob in 3 Kategorien einteilen: Layout, Datendarstellung und Eingabe.

### Layoutkomponenten {#layout-components}

Layoutkomponenten dienen dazu, andere Komponenten nebeneinander anzuordnen. Die wichtigsten Layoutkomponenten sind **`horizontal`**, **`vertical`** und **`grid`**. Diese Komponenten definieren außerdem Eigenschaften wie **padding** und **spacing**. Dabei bezeichnet padding den leeren Raum vom Rand des zugewiesenen Bereichs bis zum Inhalt und spacing den leeren Raum zwischen untergeordneten Komponenten:

![Innenabstand und Abstand zwischen Komponenten](images/editor_scripts/padding_and_spacing.png)

Der Editor definiert die Konstanten `small`, `medium` und `large` für Innenabstände und Abstände zwischen Komponenten. Bei Abständen zwischen Komponenten ist `small` für den Abstand zwischen verschiedenen Unterelementen eines einzelnen UI-Elements vorgesehen, `medium` für den Abstand zwischen einzelnen UI-Elementen und `large` für den Abstand zwischen Elementgruppen. Der Standardabstand ist `medium`. Ein Innenabstand von `large` bezeichnet den Abstand vom Fensterrand zum Inhalt, `medium` den Abstand von den Rändern eines größeren UI-Elements und `small` den Abstand von den Rändern kleiner UI-Elemente wie Kontextmenüs und Tooltips (noch nicht implementiert).

Ein **`horizontal`**-Container ordnet seine untergeordneten Komponenten horizontal hintereinander an und passt die Höhe jeder Komponente immer so an, dass sie den verfügbaren Platz ausfüllt. Standardmäßig bleibt die Breite jeder untergeordneten Komponente minimal. Du kannst sie jedoch so viel Platz wie möglich einnehmen lassen, indem du ihre Eigenschaft `grow` auf `true` setzt.

Ein **`vertical`**-Container ähnelt einem horizontalen Container, allerdings mit vertauschten Achsen.

Schließlich ist **`grid`** eine Containerkomponente, die ihre untergeordneten Komponenten in einem 2D-Raster wie in einer Tabelle anordnet. Die Einstellung `grow` gilt in einem Raster für Zeilen oder Spalten und wird daher in der Konfigurationstabelle der Spalte statt an einer untergeordneten Komponente festgelegt. Außerdem kannst du untergeordnete Komponenten in einem Raster mit den Eigenschaften `row_span` und `column_span` so konfigurieren, dass sie sich über mehrere Zeilen oder Spalten erstrecken. Raster eignen sich zum Erstellen von Formularen mit mehreren Eingabefeldern:
```lua
editor.ui.grid({
    padding = editor.ui.PADDING.LARGE, -- add padding around dialog edges
    columns = {{}, {grow = true}}, -- make 2nd column grow
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
Der obige Code erzeugt das folgende Dialogformular:

![Dialogfeld für ein neues Level](images/editor_scripts/new_level_dialog.png)

### Komponenten zur Datendarstellung {#data-presentation-components}

Der Editor definiert die folgenden Komponenten zur Datendarstellung:

- **`label`** — eine Textbeschriftung, die für die Verwendung mit Formulareingaben vorgesehen ist.
- **`icon`** — ein Symbol; derzeit kann es nur eine kleine Auswahl vordefinierter Symbole darstellen, das Defold-Team plant aber, künftig weitere Symbole zuzulassen.
- **`image`** — ein Bild, das über einen mit `/` beginnenden Projektressourcenpfad oder über eine externe URL geladen wird. Die optionalen Eigenschaften `width` und `height` passen das Bild unter Beibehaltung seines Seitenverhältnisses in die angegebenen Abmessungen ein.
- **`heading`** — ein Textelement zur Darstellung einer Überschrift, beispielsweise in einem Formular oder Dialogfeld. Der Aufzählungstyp `editor.ui.HEADING_STYLE` definiert verschiedene Überschriftenstile, darunter die HTML-Überschriften `H1`-`H6` sowie die editorspezifischen Stile `DIALOG` und `FORM`.
- **`paragraph`** — ein Textelement zur Darstellung eines Textabsatzes. Der Hauptunterschied zu `label` besteht darin, dass ein Absatz den Zeilenumbruch unterstützt: Ist der zugewiesene Bereich horizontal zu klein, wird der Text umgebrochen und möglicherweise mit `"..."` gekürzt, wenn er nicht in die Ansicht passt.

Eine Benutzeroberfläche kann beispielsweise sowohl ein Projektbild als auch ein Bild aus dem Web anzeigen:

```lua
editor.ui.vertical({
    children = {
        editor.ui.image({
            image = "/builtins/assets/images/logo/logo_256.png",
            width = 64,
            height = 64
        }),
        editor.ui.image({
            image = "https://defold.com/images/assets/monarch-hero.jpg"
        })
    }
})
```

### Eingabekomponenten {#input-components}

Eingabekomponenten ermöglichen dir, mit der Benutzeroberfläche zu interagieren. Alle Eingabekomponenten unterstützen die Eigenschaft `enabled`, die steuert, ob die Interaktion aktiviert ist, und definieren verschiedene Callback-Eigenschaften, die das Editor-Skript bei einer Interaktion benachrichtigen.

Wenn du eine statische Benutzeroberfläche erstellst, genügt es, Callbacks zu definieren, die lediglich lokale Variablen ändern. Für dynamische Benutzeroberflächen und komplexere Interaktionen siehe [Reaktivität](#reactivity).

Du kannst beispielsweise folgendermaßen ein einfaches statisches Dialogfeld für eine neue Datei erstellen:
```lua
-- initial file name, will be replaced by the dialog
local file_name = ""
local create_file = editor.ui.show_dialog(editor.ui.dialog({
    title = "Create New File",
    content = editor.ui.horizontal({
        padding = editor.ui.PADDING.LARGE,
        spacing = editor.ui.SPACING.MEDIUM,
        children = {
            editor.ui.label({
                text = "New File Name",
                alignment = editor.ui.ALIGNMENT.CENTER
            }),
            editor.ui.string_field({
                grow = true,
                text = file_name,
                -- Typing callback:
                on_value_changed = function(new_text)
                    file_name = new_text
                end
            })
        }
    }),
    buttons = {
        editor.ui.dialog_button({ text = "Cancel", cancel = true, result = false }),
        editor.ui.dialog_button({ text = "Create File", default = true, result = true })
    }
}))
if create_file then
    print("create", file_name)
end
```
Hier ist eine Liste der integrierten Eingabekomponenten:
- **`string_field`**, **`integer_field`** und **`number_field`** sind Varianten eines einzeiligen Textfelds, mit denen du Zeichenfolgen, ganze Zahlen und Zahlen bearbeiten kannst.
- **`select_box`** dient dazu, über eine Auswahlliste eine Option aus einem vordefinierten Array von Optionen auszuwählen.
- **`check_box`** ist ein boolesches Eingabefeld mit einem Callback `on_value_changed`
- **`button`** mit einem Callback `on_press`, der beim Drücken der Schaltfläche aufgerufen wird.
- **`external_file_field`** ist eine Komponente zum Auswählen eines Dateipfads auf dem Computer. Sie besteht aus einem Textfeld und einer Schaltfläche, die ein Dialogfeld zur Dateiauswahl öffnet.
- **`resource_field`** ist eine Komponente zum Auswählen einer Ressource im Projekt.

Bei allen Komponenten außer Schaltflächen kannst du eine Eigenschaft `issue` festlegen, die ein Problem im Zusammenhang mit der Komponente anzeigt (entweder `editor.ui.ISSUE_SEVERITY.ERROR` oder `editor.ui.ISSUE_SEVERITY.WARNING`), zum Beispiel:
```lua
issue = {severity = editor.ui.ISSUE_SEVERITY.WARNING, message = "This value is deprecated"}
```
Wenn ein Problem angegeben ist, ändert sich das Erscheinungsbild der Eingabekomponente, und ein Tooltip mit der Problemmeldung wird hinzugefügt.

Hier siehst du eine Demonstration aller Eingaben mit ihren Varianten für Problemmeldungen:

![Eingaben](images/editor_scripts/inputs_demo.png)

### Komponenten für Dialogfelder {#dialog-related-components}

Um ein Dialogfeld anzuzeigen, musst du die Funktion `editor.ui.show_dialog` verwenden. Sie erwartet eine Komponente **`dialog`**, die die Grundstruktur von Defold-Dialogfeldern definiert: `title`, `header`, `content` und `buttons`. Die Dialogkomponente hat eine Besonderheit: Du kannst sie nicht als untergeordnete Komponente einer anderen Komponente verwenden, weil sie ein Fenster und kein UI-Element darstellt. `header` und `content` sind jedoch gewöhnliche Komponenten.

Dialogschaltflächen sind ebenfalls besonders: Sie werden mit der Komponente **`dialog_button`** erstellt. Anders als gewöhnliche Schaltflächen haben Dialogschaltflächen keinen Callback `on_pressed`. Stattdessen definieren sie eine Eigenschaft `result` mit einem Wert, den die Funktion `editor.ui.show_dialog` zurückgibt, wenn das Dialogfeld geschlossen wird. Dialogschaltflächen definieren außerdem die booleschen Eigenschaften `cancel` und `default`: Eine Schaltfläche mit der Eigenschaft `cancel` wird ausgelöst, wenn du <kbd>Escape</kbd> drückst oder das Dialogfeld mit der Schließen-Schaltfläche des Betriebssystems schließt. Die Schaltfläche `default` wird ausgelöst, wenn du <kbd>Enter</kbd> drückst. Bei einer Dialogschaltfläche können die Eigenschaften `cancel` und `default` gleichzeitig auf `true` gesetzt sein.

### Hilfskomponenten {#utility-components}

Zusätzlich definiert der Editor einige Hilfskomponenten: 
- **`separator`** ist eine dünne Linie zum Trennen von Inhaltsblöcken
- **`scroll`** ist eine Wrapper-Komponente, die Bildlaufleisten anzeigt, wenn die umschlossene Komponente nicht in den zugewiesenen Bereich passt

## Reaktivität {#reactivity}

Da Komponenten **unveränderliche userdata-Werte** sind, kannst du sie nach ihrer Erstellung nicht mehr ändern. Wie lässt sich die Benutzeroberfläche dann im Laufe der Zeit ändern? Die Antwort: **reaktive Komponenten**. 

::: sidenote
Die Benutzeroberflächen für Editor-Skripte orientieren sich an der Bibliothek [React](https://react.dev/). Daher sind Kenntnisse über reaktive Benutzeroberflächen und React-Hooks hilfreich. 
:::

Vereinfacht ausgedrückt ist eine reaktive Komponente eine Komponente mit einer Lua-Funktion, die Daten (Props) empfängt und eine Ansicht (eine andere Komponente) zurückgibt. Die Funktion einer reaktiven Komponente kann **Hooks** verwenden: spezielle Funktionen im Modul `editor.ui`, die deinen Komponenten reaktive Funktionen hinzufügen. Konventionsgemäß beginnen die Namen aller Hooks mit `use_`.

Verwende die Funktion `editor.ui.component()`, um eine reaktive Komponente zu erstellen. 

Sehen wir uns dieses Beispiel an: ein Dialogfeld für eine neue Datei, das die Erstellung einer Datei nur erlaubt, wenn der eingegebene Dateiname nicht leer ist:

```lua
-- 1. dialog is a reactive component
local dialog = editor.ui.component(function(props)
    -- 2. the component defines a local state (file name) that defaults to empty string
    local name, set_name = editor.ui.use_state("")

    return editor.ui.dialog({ 
        title = props.title,
        content = editor.ui.vertical({
            padding = editor.ui.PADDING.LARGE,
            children = { 
                editor.ui.string_field({ 
                    value = name,
                    -- 3. typing + Enter updates the local state
                    on_value_changed = set_name 
                }) 
            }
        }),
        buttons = {
            editor.ui.dialog_button({ 
                text = "Cancel", 
                cancel = true 
            }),
            editor.ui.dialog_button({ 
                text = "Create File",
                -- 4. creation is enabled when the name exists
                enabled = name ~= "",
                default = true,
                -- 5. result is the name
                result = name
            })
        }
    })
end)

-- 6. show_dialog will either return non-empty file name or nil on cancel
local file_name = editor.ui.show_dialog(dialog({ title = "New File Name" }))
if file_name then 
    print("create " .. file_name)
else
    print("cancelled")
end
```

Wenn du einen Menübefehl ausführst, der diesen Code ausführt, zeigt der Editor ein Dialogfeld mit der anfangs deaktivierten Schaltfläche `"Create File"` an. Wenn du jedoch einen Namen eingibst und <kbd>Enter</kbd> drückst, wird sie aktiviert:

![Dialogfeld für eine neue Datei](images/editor_scripts/reactive_new_file_dialog.png)

Wie funktioniert das? Beim allerersten Rendern erstellt der Hook `use_state` einen mit der Komponente verknüpften lokalen Zustand und gibt ihn zusammen mit einer Setter-Funktion für den Zustand zurück. Wenn die Setter-Funktion aufgerufen wird, plant sie ein erneutes Rendern der Komponente ein. Bei nachfolgenden Renderdurchläufen wird die Komponentenfunktion erneut aufgerufen, und `use_state` gibt den aktualisierten Zustand zurück. Die neue Ansichtskomponente, die die Komponentenfunktion zurückgibt, wird dann mit der alten verglichen, und die Benutzeroberfläche wird dort aktualisiert, wo Änderungen erkannt wurden.

Dieser reaktive Ansatz vereinfacht das Erstellen interaktiver Benutzeroberflächen und ihre Synchronisierung erheblich: Statt bei einer Benutzereingabe alle betroffenen UI-Komponenten ausdrücklich zu aktualisieren, definierst du die Ansicht als reine Funktion der Eingabe (Props und lokaler Zustand). Der Editor übernimmt alle Aktualisierungen selbst.

### Regeln für Reaktivität {#rules-of-reactivity}

Damit reaktive Funktionskomponenten funktionieren, erwartet der Editor, dass sie die folgenden Regeln einhalten:

1. Komponentenfunktionen müssen rein sein. Es gibt keine Garantie dafür, wann oder wie oft eine Komponentenfunktion aufgerufen wird. Alle Seiteneffekte sollten außerhalb des Renderns stattfinden, beispielsweise in Callbacks
2. Props und lokaler Zustand müssen unveränderlich sein. Verändere Props nicht. Wenn dein lokaler Zustand eine Tabelle ist, ändere sie nicht direkt, sondern erstelle eine neue Tabelle und übergib sie an die Setter-Funktion, wenn sich der Zustand ändern muss.
3. Komponentenfunktionen müssen bei jedem Aufruf dieselben Hooks in derselben Reihenfolge aufrufen. Rufe Hooks nicht innerhalb von Schleifen, in bedingten Blöcken, nach vorzeitigen Rückgaben usw. auf. Es hat sich bewährt, Hooks am Anfang der Komponentenfunktion vor jedem anderen Code aufzurufen.
4. Rufe Hooks nur aus Komponentenfunktionen heraus auf. Hooks arbeiten im Kontext einer reaktiven Komponente. Daher dürfen sie nur in der Komponentenfunktion aufgerufen werden (oder in einer anderen Funktion, die direkt von der Komponentenfunktion aufgerufen wird).

### Hooks

::: sidenote
Wenn du mit [React](https://react.dev/) vertraut bist, wirst du feststellen, dass Hooks im Editor hinsichtlich ihrer Abhängigkeiten eine etwas andere Semantik haben.
:::

Der Editor definiert 2 Hooks: **`use_memo`** und **`use_state`**.

### **`use_state`**

Du kannst lokalen Zustand auf 2 Arten erstellen: mit einem Standardwert oder mit einer Initialisierungsfunktion:
```lua
-- default value
local enabled, set_enabled = editor.ui.use_state(true)
-- initializer function + args
local id, set_id = editor.ui.use_state(string.lower, props.name)
```
Ebenso kannst du die Setter-Funktion mit einem neuen Wert oder mit einer Aktualisierungsfunktion aufrufen:
```lua
-- updater function
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

Schließlich kann der Zustand **zurückgesetzt** werden. Der Zustand wird zurückgesetzt, wenn sich eines der Argumente von `editor.ui.use_state()` ändert; dies wird mit `==` geprüft. Deshalb darfst du keine Tabellenliterale oder als Literal definierten Initialisierungsfunktionen als Argumente an den Hook `use_state` übergeben: Dadurch wird der Zustand bei jedem erneuten Rendern zurückgesetzt. Zur Veranschaulichung:
```lua
-- ❌ BAD: literal table initializer causes state reset on every re-render
local user, set_user = editor.ui.use_state({ first_name = props.first_name, last_name = props.last_name})

-- ✅ GOOD: use initializer function outside of component function to create table state
local function create_user(first_name, last_name) 
    return { first_name = first_name, last_name = last_name}
end
-- ...later, in component function:
local user, set_user = editor.ui.use_state(create_user, props.first_name, props.last_name)


-- ❌ BAD: literal initializer function causes state reset on every re-render
local id, set_id = editor.ui.use_state(function() return string.lower(props.name) end)

-- ✅ GOOD: use referenced initializer function to create the state
local id, set_id = editor.ui.use_state(string.lower, props.name)
```

### **`use_memo`**

Du kannst den Hook `use_memo` verwenden, um die Leistung zu verbessern. Häufig werden in den Renderfunktionen Berechnungen ausgeführt, beispielsweise um zu prüfen, ob die Benutzereingabe gültig ist. Der Hook `use_memo` eignet sich für Fälle, in denen die Prüfung, ob sich die Argumente der Berechnungsfunktion geändert haben, weniger Aufwand verursacht als der Aufruf der Berechnungsfunktion. Der Hook ruft die Berechnungsfunktion beim ersten Rendern auf und verwendet den berechneten Wert bei nachfolgenden Renderdurchläufen erneut, wenn alle Argumente von `use_memo` unverändert sind:
```lua
-- validation function outside of component function
local function validate_password(password)
    if #password < 8 then
        return false, "Password must be at least 8 characters long."
    elseif not password:match("%l") then
        return false, "Password must include at least one lowercase letter."
    elseif not password:match("%u") then
        return false, "Password must include at least one uppercase letter."
    elseif not password:match("%d") then
        return false, "Password must include at least one number."
    else
        return true, "Password is valid."
    end
end

-- ...later, in component function
local username, set_username = editor.ui.use_state('')
local password, set_password = editor.ui.use_state('')
local valid, message = editor.ui.use_memo(validate_password, password)
```
In diesem Beispiel wird die Kennwortvalidierung bei jeder Kennwortänderung ausgeführt (beispielsweise beim Tippen in ein Kennwortfeld), aber nicht, wenn der Benutzername geändert wird.

Ein weiterer Anwendungsfall für `use_memo` ist das Erstellen von Callbacks, die anschließend in Eingabekomponenten verwendet werden, oder die Verwendung einer lokal erstellten Funktion als Eigenschaftswert einer anderen Komponente. Dies verhindert unnötiges erneutes Rendern.
