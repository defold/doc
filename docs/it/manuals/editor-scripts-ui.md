---
title: "Script dell'editor: interfaccia utente"
brief: Questo manuale spiega come creare elementi dell'interfaccia utente nell'editor usando Lua
---

# Script dell'editor e interfaccia utente {#editor-scripts-and-ui}

Questo manuale spiega come creare elementi interattivi dell'interfaccia utente nell'editor usando script dell'editor scritti in Lua. Per iniziare a usare gli script dell'editor, consulta il [manuale degli script dell'editor](/manuals/editor-scripts). La documentazione di riferimento completa dell'API dell'editor è disponibile [qui](/ref/stable/editor-lua/). Al momento è possibile creare soltanto finestre di dialogo interattive, ma in futuro vogliamo estendere il supporto agli script per l'interfaccia al resto dell'editor.

## Ciao mondo {#hello-world}

Tutte le funzionalità relative all'interfaccia utente si trovano nel modulo `editor.ui`. Per iniziare, ecco l'esempio più semplice di uno script dell'editor con un'interfaccia personalizzata:
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

Questo frammento di codice definisce un comando **View → Do with confirmation**. Quando lo esegui, vedrai la seguente finestra di dialogo:

![Finestra di dialogo Ciao mondo](images/editor_scripts/perform_action_dialog.png)

Infine, dopo aver premuto <kbd>Enter</kbd> (o fatto clic sul pulsante `Perform`), vedrai la seguente riga nella console dell'editor:
```
Perform action:	true
```

## Concetti di base {#basic-concepts}

### Componenti {#components}

L'editor fornisce vari **componenti** dell'interfaccia utente che puoi combinare per creare l'interfaccia desiderata. Per convenzione, tutti i componenti vengono configurati usando un'unica tabella chiamata **props**. I componenti stessi non sono tabelle, ma **userdata immutabili** che l'editor usa per creare l'interfaccia.

### Proprietà {#props}

Le **proprietà** (props) sono tabelle che definiscono i dati in ingresso dei componenti. Le proprietà devono essere trattate come immutabili: modificare direttamente la tabella delle proprietà non provoca un nuovo rendering del componente, mentre usare una tabella diversa sì. L'interfaccia viene aggiornata quando l'istanza del componente riceve una tabella delle proprietà che, confrontando i valori dei suoi campi senza esaminare le tabelle annidate, risulta diversa dalla precedente.

### Allineamento {#alignment}

Quando a un componente viene assegnata un'area nell'interfaccia, il componente occupa tutto lo spazio, ma ciò non significa che la sua parte visibile si estenda per riempirlo. La parte visibile occupa invece lo spazio necessario, poi viene allineata all'interno dell'area assegnata. Per questo motivo, la maggior parte dei componenti integrati definisce una proprietà `alignment`.

Per esempio, considera questo componente etichetta:
```lua
editor.ui.label({
    text = "Hello",
    alignment = editor.ui.ALIGNMENT.RIGHT
})
```
La parte visibile è il testo `Hello`, allineato all'interno dell'area assegnata al componente:

![Allineamento](images/editor_scripts/alignment.png)

## Componenti integrati {#built-in-components}

L'editor definisce vari componenti integrati che puoi usare insieme per costruire l'interfaccia utente. I componenti si possono suddividere a grandi linee in 3 categorie: layout, presentazione dei dati e input.

### Componenti di layout {#layout-components}

I componenti di layout servono a posizionare altri componenti uno accanto all'altro. I principali componenti di layout sono **`horizontal`**, **`vertical`** e **`grid`**. Questi componenti definiscono anche proprietà come **padding** e **spacing**: il padding è lo spazio vuoto tra il bordo dell'area assegnata e il contenuto, mentre lo spacing è lo spazio vuoto tra i figli:

![Spaziatura interna e tra i figli](images/editor_scripts/padding_and_spacing.png)

L'editor definisce le costanti `small`, `medium` e `large` per il padding e lo spacing. Per lo spacing, `small` indica la spaziatura tra i diversi sottoelementi di un singolo elemento dell'interfaccia, `medium` quella tra i singoli elementi dell'interfaccia e `large` quella tra gruppi di elementi. Lo spacing predefinito è `medium`. Un valore di padding `large` indica lo spazio tra i bordi della finestra e il contenuto, `medium` lo spazio dai bordi di un elemento significativo dell'interfaccia e `small` lo spazio dai bordi di elementi piccoli dell'interfaccia, come menu contestuali e suggerimenti (non ancora implementati).

Un contenitore **`horizontal`** dispone i figli uno dopo l'altro in orizzontale, facendo sempre in modo che l'altezza di ciascun figlio occupi tutto lo spazio disponibile. Per impostazione predefinita, la larghezza di ogni figlio viene mantenuta al minimo, ma puoi fargli occupare più spazio possibile impostando la sua proprietà `grow` su `true`.

Un contenitore **`vertical`** è simile a quello orizzontale, ma con gli assi invertiti.

Infine, **`grid`** è un componente contenitore che dispone i figli in una griglia 2D, come una tabella. In una griglia, l'impostazione `grow` si applica alle righe o alle colonne, quindi non viene impostata su un figlio, ma sulla tabella di configurazione della colonna. Inoltre, puoi configurare i figli di una griglia in modo che occupino più righe o colonne usando le proprietà `row_span` e `column_span`. Le griglie sono utili per creare moduli con più campi di input:
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
Il codice precedente produce il seguente modulo nella finestra di dialogo:

![Finestra di dialogo per un nuovo livello](images/editor_scripts/new_level_dialog.png)

### Componenti di presentazione dei dati {#data-presentation-components}

L'editor definisce i seguenti componenti di presentazione dei dati:

- **`label`** — etichetta di testo, pensata per essere usata con i campi di input dei moduli.
- **`icon`** — un'icona; al momento permette di visualizzare soltanto un piccolo insieme di icone predefinite, ma in futuro intendiamo consentire l'uso di altre icone.
- **`image`** — un'immagine caricata da un percorso di risorsa del progetto che inizia con `/` oppure da un URL esterno. Le proprietà facoltative `width` e `height` adattano l'immagine alle dimensioni specificate, mantenendone le proporzioni.
- **`heading`** — elemento di testo pensato per visualizzare una riga di intestazione, per esempio in un modulo o in una finestra di dialogo. L'enumerazione `editor.ui.HEADING_STYLE` definisce vari stili di intestazione, tra cui quelli HTML da `H1` a `H6`, oltre a `DIALOG` e `FORM`, specifici dell'editor.
- **`paragraph`** — elemento di testo pensato per visualizzare un paragrafo. La differenza principale rispetto a `label` è il supporto del ritorno a capo automatico: se l'area assegnata è troppo stretta, il testo va a capo e può essere abbreviato con `"..."` se non entra nella vista.

Per esempio, un'interfaccia può visualizzare sia un'immagine del progetto sia un'immagine dal web:

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

### Componenti di input {#input-components}

I componenti di input permettono all'utente di interagire con l'interfaccia. Tutti i componenti di input supportano la proprietà `enabled` per controllare se l'interazione è abilitata e definiscono varie proprietà di callback che notificano allo script dell'editor le interazioni.

Se crei un'interfaccia statica, è sufficiente definire callback che si limitano a modificare variabili locali. Per interfacce dinamiche e interazioni più avanzate, consulta la sezione sulla [reattività](#reactivity).

Per esempio, puoi creare una semplice finestra di dialogo statica per un nuovo file in questo modo:
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
Ecco un elenco dei componenti di input integrati:
- **`string_field`**, **`integer_field`** e **`number_field`** sono varianti di un campo di testo a riga singola che permettono di modificare stringhe, numeri interi e numeri.
- **`select_box`** permette di selezionare un'opzione da un array predefinito di opzioni tramite un elenco a discesa.
- **`check_box`** è un campo di input booleano con una callback `on_value_changed`
- **`button`** ha una callback `on_press` che viene invocata quando si preme il pulsante.
- **`external_file_field`** è un componente pensato per selezionare il percorso di un file sul computer. È composto da un campo di testo e da un pulsante che apre una finestra di dialogo per la selezione di un file.
- **`resource_field`** è un componente pensato per selezionare una risorsa nel progetto.

Tutti i componenti, tranne i pulsanti, permettono di impostare una proprietà `issue` che visualizza un problema relativo al componente (`editor.ui.ISSUE_SEVERITY.ERROR` oppure `editor.ui.ISSUE_SEVERITY.WARNING`), per esempio:
```lua
issue = {severity = editor.ui.ISSUE_SEVERITY.WARNING, message = "This value is deprecated"}
```
Quando viene specificato un problema, l'aspetto del componente di input cambia e viene aggiunto un suggerimento con il messaggio relativo al problema.

Ecco una dimostrazione di tutti i campi di input con le rispettive varianti che segnalano un problema:

![Campi di input](images/editor_scripts/inputs_demo.png)

### Componenti per le finestre di dialogo {#dialog-related-components}

Per mostrare una finestra di dialogo, devi usare la funzione `editor.ui.show_dialog`. Questa richiede un componente **`dialog`** che definisce la struttura principale delle finestre di dialogo di Defold: `title`, `header`, `content` e `buttons`. Il componente della finestra di dialogo ha una particolarità: non puoi usarlo come figlio di un altro componente, perché rappresenta una finestra e non un elemento dell'interfaccia. `header` e `content` sono invece componenti normali.

Anche i pulsanti delle finestre di dialogo sono particolari: vengono creati usando il componente **`dialog_button`**. A differenza dei pulsanti normali, non hanno una callback `on_pressed`. Definiscono invece una proprietà `result` il cui valore viene restituito dalla funzione `editor.ui.show_dialog` alla chiusura della finestra di dialogo. I pulsanti delle finestre di dialogo definiscono anche le proprietà booleane `cancel` e `default`: un pulsante con la proprietà `cancel` viene attivato quando l'utente preme <kbd>Escape</kbd> o chiude la finestra di dialogo usando il pulsante di chiusura del sistema operativo; il pulsante `default` viene attivato quando l'utente preme <kbd>Enter</kbd>. Un pulsante della finestra di dialogo può avere entrambe le proprietà `cancel` e `default` impostate su `true` contemporaneamente.

### Componenti di utilità {#utility-components}

Inoltre, l'editor definisce alcuni componenti di utilità: 
- **`separator`** è una linea sottile usata per delimitare blocchi di contenuto
- **`scroll`** è un componente wrapper che mostra le barre di scorrimento quando il componente racchiuso non entra nello spazio assegnato

## Reattività {#reactivity}

Poiché i componenti sono **userdata immutabili**, è impossibile modificarli dopo averli creati. Come puoi allora fare in modo che l'interfaccia cambi nel tempo? La risposta è usare **componenti reattivi**. 

::: sidenote
L'interfaccia per gli script dell'editor si ispira alla libreria [React](https://react.dev/), quindi conoscere le interfacce reattive e gli hook di React è utile. 
:::

In termini semplici, un componente reattivo è un componente con una funzione Lua che riceve dati (proprietà) e restituisce una vista (un altro componente). La funzione di un componente reattivo può usare gli **hook**: funzioni speciali del modulo `editor.ui` che aggiungono funzionalità reattive ai componenti. Per convenzione, tutti gli hook hanno un nome che inizia con `use_`.

Per creare un componente reattivo, usa la funzione `editor.ui.component()`. 

Esaminiamo questo esempio: una finestra di dialogo per un nuovo file che ne permette la creazione soltanto se il nome inserito non è vuoto:

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

Quando esegui un comando di menu che avvia questo codice, l'editor mostra una finestra di dialogo con il pulsante `"Create File"` inizialmente disabilitato; quando digiti un nome e premi <kbd>Enter</kbd>, il pulsante viene abilitato:

![Finestra di dialogo per un nuovo file](images/editor_scripts/reactive_new_file_dialog.png)

Come funziona? Al primo rendering, l'hook `use_state` crea uno stato locale associato al componente e lo restituisce insieme a una funzione che permette di impostarlo. Quando questa funzione viene invocata, pianifica un nuovo rendering del componente. Nei rendering successivi, la funzione del componente viene invocata di nuovo e `use_state` restituisce lo stato aggiornato. Il nuovo componente della vista restituito dalla funzione del componente viene quindi confrontato con quello precedente e l'interfaccia viene aggiornata nei punti in cui vengono rilevate modifiche.

Questo approccio reattivo semplifica notevolmente la creazione di interfacce interattive e il loro mantenimento in sincronia: invece di aggiornare esplicitamente tutti i componenti dell'interfaccia interessati dall'input dell'utente, la vista viene definita come una funzione pura dei dati in ingresso (proprietà e stato locale) e l'editor gestisce autonomamente tutti gli aggiornamenti.

### Regole della reattività {#rules-of-reactivity}

Per funzionare, i componenti reattivi definiti da funzioni devono rispettare le regole previste dall'editor:

1. Le funzioni dei componenti devono essere pure. Non è garantito quando o con quale frequenza verrà invocata la funzione di un componente. Tutti gli effetti collaterali devono avvenire al di fuori del rendering, per esempio nelle callback
2. Le proprietà e lo stato locale devono essere immutabili. Non modificare le proprietà. Se lo stato locale è una tabella, non modificarla direttamente: creane una nuova e passala alla funzione che imposta lo stato quando questo deve cambiare.
3. Le funzioni dei componenti devono chiamare gli stessi hook nello stesso ordine a ogni invocazione. Non chiamare gli hook all'interno di cicli, blocchi condizionali, dopo uscite anticipate dalla funzione e così via. È buona norma chiamare gli hook all'inizio della funzione del componente, prima di qualsiasi altro codice.
4. Chiama gli hook soltanto dalle funzioni dei componenti. Gli hook funzionano nel contesto di un componente reattivo, quindi possono essere chiamati soltanto nella funzione del componente (o in un'altra funzione chiamata direttamente da questa).

### Hook {#hooks}

::: sidenote
Se hai familiarità con [React](https://react.dev/), noterai che gli hook dell'editor hanno una semantica leggermente diversa per quanto riguarda le dipendenze degli hook.
:::

L'editor definisce 2 hook: **`use_memo`** e **`use_state`**.

### **`use_state`**

Puoi creare lo stato locale in 2 modi: con un valore predefinito o con una funzione di inizializzazione:
```lua
-- default value
local enabled, set_enabled = editor.ui.use_state(true)
-- initializer function + args
local id, set_id = editor.ui.use_state(string.lower, props.name)
```
Analogamente, puoi invocare la funzione che imposta lo stato con un nuovo valore o con una funzione di aggiornamento:
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

Infine, lo stato può essere **reimpostato**. Lo stato viene reimpostato quando cambia uno qualsiasi degli argomenti di `editor.ui.use_state()`, verificati con `==`. Per questo motivo, non devi usare tabelle letterali o funzioni di inizializzazione letterali come argomenti dell'hook `use_state`: ciò causerebbe la reimpostazione dello stato a ogni nuovo rendering. Per esempio:
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

Puoi usare l'hook `use_memo` per migliorare le prestazioni. È comune eseguire alcuni calcoli nelle funzioni di rendering, per esempio per verificare che l'input dell'utente sia valido. Puoi usare l'hook `use_memo` nei casi in cui verificare se gli argomenti della funzione di calcolo sono cambiati costa meno che invocare la funzione stessa. L'hook chiama la funzione di calcolo al primo rendering e riutilizza il valore calcolato nei rendering successivi se tutti gli argomenti di `use_memo` sono rimasti invariati:
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
In questo esempio, la validazione della password viene eseguita a ogni modifica della password (per esempio quando si digita nel relativo campo), ma non quando viene modificato il nome utente.

Un altro caso d'uso di `use_memo` è la creazione di callback da usare nei componenti di input oppure l'uso di una funzione creata localmente come valore di una proprietà di un altro componente: questo evita rendering aggiuntivi non necessari.
