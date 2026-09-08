---
title: Preferenze dell'editor
brief: Puoi modificare le impostazioni dell'editor dalla finestra Preferences.
---

# Preferenze dell'editor {#editor-preferences}

Puoi modificare le impostazioni dell'editor dalla finestra Preferences. Per aprire la finestra delle preferenze, seleziona <kbd>File -> Preferences</kbd> dal menu.

## Impostazioni generali {#general}

![](images/editor/preferences_general.png)

Load External Changes on App Focus
: Attiva la ricerca di modifiche esterne quando l'editor riceve il focus.

Open Bundle Target Folder
: Attiva l'apertura della cartella di destinazione del bundle al termine del processo di creazione del bundle.

Enable Texture Compression
: Attiva la [compressione delle texture](/manuals/texture-profiles) per tutte le build create dall'editor.

Escape Quits Game
: Consente di chiudere una build del gioco in esecuzione con il tasto <kbd>Esc</kbd>.

Track Active Tab in Asset Browser
: Il file modificato nella scheda selezionata del pannello *Editor* viene selezionato nell'Asset Browser (noto anche come pannello *Asset*).

Lint Code on Build
: Attiva l'[analisi statica del codice](/manuals/writing-code/#linting-configuration) durante la build del progetto. Questa opzione è attiva per impostazione predefinita, ma può essere disattivata se l'analisi statica richiede troppo tempo in un progetto di grandi dimensioni.

Engine Arguments
: Argomenti da passare all'eseguibile dmengine quando l'editor crea una build e la esegue.
 Usa un argomento per riga. Ad esempio:
 ```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```


## Codice {#code}

![](images/editor/preferences_code.png)

Custom Editor
: Percorso assoluto di un editor esterno. Su macOS deve essere il percorso dell'eseguibile all'interno del file .app (ad esempio `/Applications/Atom.app/Contents/MacOS/Atom`).

Open File
: Il modello usato dall'editor personalizzato per specificare il file da aprire. Il segnaposto `{file}` viene sostituito con il nome del file da aprire.

Open File at Line
: Il modello usato dall'editor personalizzato per specificare il file da aprire e il numero di riga. Il segnaposto `{file}` viene sostituito con il nome del file da aprire e `{line}` con il numero di riga.

Code editor font
: Nome di un carattere installato nel sistema da usare nell'editor di codice.

Zoom on Scroll
: Indica se modificare la dimensione del carattere quando scorri nell'editor di codice tenendo premuto il tasto Cmd/Ctrl.

Auto-insert closing parens
: Inserisce automaticamente i caratteri di chiusura corrispondenti durante la modifica del codice. Questa opzione è attiva per impostazione predefinita.


### Aprire i file di script in Visual Studio Code {#open-script-files-in-visual-studio-code}

![](images/editor/preferences_vscode.png)

Per aprire i file di script dall'editor Defold direttamente in Visual Studio Code, devi configurare le seguenti impostazioni specificando il percorso dell'eseguibile:

- macOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

 Imposta questi parametri per aprire file e righe specifici:

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

Il carattere `.` è necessario per aprire l'intera area di lavoro anziché un singolo file.


## Estensioni {#extensions}

![](images/editor/preferences_extensions.png)

Build Server
: URL del server di build usato per creare la build di un progetto contenente [estensioni native](/manuals/extensions). Puoi aggiungere un nome utente e un token di accesso all'URL per accedere al server di build con autenticazione. Usa la seguente notazione per specificare il nome utente e il token di accesso: `username:token@build.defold.com`. L'accesso autenticato è richiesto per le build per Nintendo Switch e quando esegui una tua istanza del server di build con l'autenticazione attivata ([consulta la documentazione del server di build](https://github.com/defold/extender/blob/dev/README_SECURITY.md) per maggiori informazioni). Puoi anche impostare il nome utente e la password tramite le variabili d'ambiente di sistema `DM_EXTENDER_USERNAME` e `DM_EXTENDER_PASSWORD`.

Build Server Username
: Nome utente per l'autenticazione.

Build Server Password
: Password per l'autenticazione, memorizzata in forma cifrata nel file delle preferenze.

Build Server Headers
: Intestazioni aggiuntive da inviare al server di build durante la creazione di build di estensioni native. Sono importanti per usare il servizio CloudFlare o servizi simili con extender.

## Strumenti {#tools}

![](images/editor/preferences_tools.png)

ADB path
: Percorso dello strumento a riga di comando [ADB](https://developer.android.com/tools/adb) installato su questo sistema. Se ADB è installato nel sistema, l'editor Defold lo usa per installare ed eseguire gli APK Android prodotti con la creazione di bundle su un dispositivo Android collegato. Per impostazione predefinita, l'editor verifica se ADB è installato nelle posizioni più comuni, quindi devi specificare il percorso solo se ADB è installato in una posizione personalizzata.

ios-deploy path
: Percorso degli strumenti a riga di comando [ios-deploy](https://github.com/ios-control/ios-deploy) installati su questo sistema (rilevante solo per macOS). Come per il percorso di ADB, l'editor Defold usa questo strumento per installare ed eseguire le applicazioni iOS prodotte con la creazione di bundle su un iPhone collegato. Per impostazione predefinita, l'editor verifica se ios-deploy è installato nelle posizioni più comuni, quindi devi specificare il percorso solo se usi un'installazione personalizzata di ios-deploy.

## Mappatura dei comandi {#keymap}

![](images/editor/preferences_keymap.png)

Puoi configurare le scorciatoie da tastiera e i controlli del mouse dell'editor nella scheda Keymap. Per modificare un comando, fai doppio clic su di esso, premi <kbd>Enter</kbd> o <kbd>Space</kbd>, oppure usa il menu contestuale della riga.

Le scorciatoie da tastiera appaiono come combinazioni di tasti nella colonna *Shortcuts*. I controlli del mouse appaiono nello stesso elenco, contrassegnati da un'etichetta:

- <kbd>MB</kbd> indica un'associazione a un pulsante del mouse, eventualmente combinato con <kbd>Shift</kbd>, <kbd>Ctrl</kbd>/<kbd>Control</kbd> o <kbd>Alt</kbd>.
- <kbd>MM</kbd> indica un tasto modificatore usato da un'azione del mouse.

Alcuni controlli del mouse riutilizzano le associazioni della Scene 2D Camera predefinita, quindi una riga può mostrare un'associazione prima che tu la personalizzi. Queste associazioni sono generalmente mostrate con un colore più scuro. Se imposti un'associazione personalizzata per quella riga, Defold usa la tua associazione. Usa *Reset to Defaults* per rimuovere la modifica e ripristinare il comportamento integrato o ereditato.

Gli avvisi sono mostrati in arancione. Passa il puntatore su un avviso per visualizzarne i dettagli. Gli avvisi in genere indicano che:
- la scorciatoia può inserire testo e interferire con i campi di testo.
- la stessa scorciatoia o associazione del mouse è già usata da un altro comando.
