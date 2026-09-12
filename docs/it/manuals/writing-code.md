---
title: Scrivere codice
brief: Questo manuale descrive brevemente come lavorare con il codice in Defold.
---

# Scrivere codice {#writing-code}

Defold ti permette di creare gran parte dei contenuti del gioco con strumenti visivi, come gli editor di mappe di tile ed effetti particellari, ma per la logica di gioco devi comunque usare un editor di codice. La logica di gioco si scrive con il [linguaggio di programmazione Lua](https://www.lua.org/), mentre le estensioni del motore stesso si scrivono con i linguaggi nativi della piattaforma di destinazione.

## Scrivere codice Lua {#writing-lua-code}

Defold usa Lua 5.1 e LuaJIT (a seconda della piattaforma di destinazione) e, quando scrivi la logica di gioco, devi seguire le specifiche del linguaggio per queste versioni di Lua. Per maggiori dettagli su come lavorare con Lua in Defold, consulta il [manuale Lua in Defold](/manuals/lua).

## Usare altri linguaggi che si transcompilano in Lua {#using-other-languages-that-transpile-to-lua}

Defold supporta l'uso di transcompilatori che generano codice Lua. Con un'estensione di transcompilazione installata, puoi usare linguaggi alternativi — come [Teal](https://github.com/defold/extension-teal) — per scrivere codice Lua verificato staticamente. È una funzionalità in anteprima che presenta alcune limitazioni: il supporto attuale per i transcompilatori non espone le informazioni sui moduli e sulle funzioni definiti nel runtime Lua di Defold. Questo significa che, per usare API di Defold come `go.animate`, dovrai scrivere tu le definizioni esterne.

## Scrivere codice nativo {#writing-native-code}

Defold ti permette di estendere il motore di gioco con codice nativo per accedere a funzionalità specifiche della piattaforma che il motore stesso non fornisce. Puoi usare il codice nativo anche quando le prestazioni di Lua non sono sufficienti (calcoli che richiedono molte risorse, elaborazione di immagini, ecc.). Consulta i [manuali sulle estensioni native](/manuals/extensions/) per saperne di più.

## Usare l'editor di codice integrato {#using-the-built-in-code-editor}

Defold dispone di un editor di codice integrato che ti permette di aprire e modificare file Lua (.lua), file di script Defold (.script, .gui_script e .render_script) e qualsiasi altro file la cui estensione non sia gestita nativamente dall'editor. Inoltre, l'editor offre l'evidenziazione della sintassi per i file Lua e gli script.

![](/images/editor/code-editor.png)

### Completamento del codice {#code-completion}

L'editor di codice integrato mostra suggerimenti per completare i nomi delle funzioni mentre scrivi il codice:

![](/images/editor/codecompletion.png)

Premendo <kbd>CTRL</kbd> + <kbd>Space</kbd> vengono mostrate ulteriori informazioni su funzioni, argomenti e valori restituiti:

![](/images/editor/apireference.png)

Il server di linguaggio Lua incluso contiene annotazioni dei tipi per le API Defold. Il completamento, le informazioni al passaggio del puntatore e la diagnostica comprendono i tipi Defold, come hash, URL, vettori e quaternioni, oltre agli argomenti e ai valori restituiti dalle funzioni. L'editor fornisce annotazioni per gli script di gioco e per le API `editor.*` usate nei file `.editor_script`. Quando usi l'editor di codice Defold, non serve una libreria di annotazioni separata per le API integrate.

Le API delle estensioni di terze parti possono richiedere annotazioni proprie.

### Formattare il codice {#formatting-code}

Seleziona <kbd>Edit ▸ Format Document/Selection</kbd> oppure premi <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd> per eseguire il formatter del server di linguaggio. Se è presente una selezione, l'editor formatta le righe selezionate; altrimenti formatta il documento. La formattazione richiede un server di linguaggio che supporti la relativa operazione.

Per formattare al salvataggio i file aperti e modificati, abilita **Format on save** in <kbd>Preferences ▸ Code</kbd>. Questa preferenza è disabilitata per impostazione predefinita e richiede un server di linguaggio che supporti la formattazione dei documenti. Consulta [Preferenze del codice](/manuals/editor-preferences/#code).

### Passare a un simbolo {#jump-to-symbol}

L'editor di codice integrato può mostrare un elenco ricercabile dei simboli presenti nel file di codice corrente, come funzioni, oggetti e variabili. Seleziona <kbd>View ▸ Jump to Symbol…</kbd>, oppure premi <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd> su Windows e Linux, o <kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd> su macOS.

Inizia a digitare per cercare i simboli anche con corrispondenze approssimative, usa i tasti freccia per spostarti tra i risultati e visualizzare in anteprima le rispettive posizioni nell'editor, poi premi <kbd>Enter</kbd> per passare al simbolo selezionato. Premi <kbd>Esc</kbd> per chiudere la finestra di dialogo e ripristinare la posizione precedente del cursore e dello scorrimento.

![](/images/editor/jump-to-symbol.png)

### Configurazione dell'analisi statica {#linting-configuration}

L'editor di codice integrato esegue l'analisi statica del codice usando [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) e [Lua language server](https://luals.github.io/wiki/diagnostics/). Per configurare Luacheck, crea un file `.luacheckrc` nella radice del progetto. Puoi consultare la [pagina di configurazione di Luacheck](https://luacheck.readthedocs.io/en/stable/config.html) per conoscere le opzioni disponibili. Defold usa i seguenti valori predefiniti per la configurazione di Luacheck:

```lua
unused_args = false      -- don't warn on unused arguments (common for .script files)
max_line_length = false  -- don't warn on long lines
ignore = {
    "611",               -- line contains only whitespace
    "612",               -- line contains trailing whitespace
    "614"                -- trailing whitespace in a comment
},
```

## Usare un editor di codice esterno {#using-an-external-code-editor}

L'editor di codice di Defold offre le funzionalità di base necessarie per scrivere codice, ma per esigenze più avanzate o per gli utenti esperti che hanno un editor preferito, puoi fare in modo che Defold apra i file con un editor esterno. Nella [finestra Preferences, nella scheda Code](/manuals/editor-preferences/#code), puoi definire un editor esterno da usare per modificare il codice.

### Visual Studio Code - Defold Kit

Defold Kit è un plugin di Visual Studio Code con le seguenti funzionalità:

* Installazione delle estensioni consigliate
* Evidenziazione della sintassi, completamento automatico e analisi statica di Lua
* Applicazione delle impostazioni pertinenti all'area di lavoro
* Annotazioni Lua per l'API di Defold
* Annotazioni Lua per le dipendenze
* Creazione della build e avvio
* Debug con punti di interruzione
* Creazione di bundle per tutte le piattaforme
* Distribuzione sui dispositivi mobili collegati

Scopri di più e installa Defold Kit da [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold).


## Software per la documentazione {#documentation-software}

Sono disponibili pacchetti di riferimento API creati dalla comunità per [Dash e Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417).
