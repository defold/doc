---
title: Input da tastiera e di testo in Defold
brief: Questo manuale spiega come funziona l'input da tastiera e di testo.
---

::: sidenote
Ti consigliamo di familiarizzare con il funzionamento generale dell'input in Defold, con il modo in cui riceverlo e con l'ordine in cui viene ricevuto nei file di script. Per saperne di più sul sistema di input, consulta il [manuale di panoramica sull'input](/manuals/input).
:::

# Trigger dei tasti {#key-triggers}
I trigger dei tasti consentono di associare l'input di singoli tasti della tastiera ad azioni di gioco. Ogni tasto è associato separatamente a un'azione corrispondente. I trigger dei tasti servono a collegare tasti specifici a funzioni specifiche, come il movimento del personaggio con i tasti freccia o WASD. Se devi leggere un input da tastiera arbitrario, usa i trigger di testo (vedi sotto).

![](images/input/key_bindings.png)

```lua
function on_input(self, action_id, action)
    if action_id == hash("left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

# Trigger di testo {#text-triggers}
I trigger di testo servono a leggere un input di testo arbitrario. Esistono due tipi di trigger di testo: `text` e `marked-text`.

![](images/input/text_bindings.png)

## Testo {#text}
Il trigger `text` acquisisce il normale input di testo. Imposta il campo `text` della tabella dell'azione su una stringa contenente il carattere digitato. L'azione viene generata solo alla pressione del tasto; non viene inviata alcuna azione `release` o `repeated`.

```lua
function on_input(self, action_id, action)
    if action_id == hash("text") then
        -- Concatenate the typed character to the "user" node...
        local node = gui.get_node("user")
        local name = gui.get_text(node)
        name = name .. action.text
        gui.set_text(node, name)
    end
end
```

## Testo in composizione {#marked-text}
Il trigger `marked-text` viene usato principalmente per le tastiere asiatiche, in cui più pressioni di tasti possono corrispondere a un singolo input. Ad esempio, con la tastiera "Japanese-Kana" di iOS, l'utente può digitare combinazioni e la parte superiore della tastiera mostrerà i simboli o le sequenze di simboli disponibili per l'inserimento.

![Input di testo in composizione](images/input/marked_text.png)

- Ogni pressione di un tasto genera un'azione distinta e imposta il campo `text` dell'azione sulla sequenza di simboli attualmente inserita (il "testo in composizione").
- Quando l'utente seleziona un simbolo o una combinazione di simboli, viene inviata un'azione distinta del trigger di tipo `text` (purché ne sia stato configurato uno nell'elenco dei binding di input). Questa azione imposta il campo `text` dell'azione sulla sequenza di simboli definitiva.
