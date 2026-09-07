---
title: Debug con ZeroBrane Studio
brief: Questo manuale spiega come usare ZeroBrane Studio per eseguire il debug del codice Lua in Defold.
---

# Debug degli script Lua con ZeroBrane Studio {#debugging-lua-scripts-with-zerobrane-studio}

Defold include un debugger integrato, ma puoi anche usare l'IDE Lua gratuito e open source _ZeroBrane Studio_ come debugger esterno. Per usare le funzionalità di debug devi installare ZeroBrane Studio. Il programma è multipiattaforma e funziona sia su macOS sia su Windows.

Scarica "ZeroBrane Studio" da http://studio.zerobrane.com

## Configurazione di ZeroBrane {#zerobrane-configuration}

Affinché ZeroBrane trovi i file del tuo progetto, devi indicargli il percorso della directory del progetto Defold. Un modo pratico per trovarlo è usare l'opzione <kbd>Show in Desktop</kbd> su un file nella radice del progetto Defold.

1. Fai clic con il pulsante destro su *game.project*
2. Scegli <kbd>Show in Desktop</kbd>

![Visualizzazione nel Finder](images/zerobrane/show_in_desktop.png)

## Configurare ZeroBrane {#to-set-up-zerobrane}

Per configurare ZeroBrane, seleziona <kbd>Project ▸ Project Directory ▸ Choose...</kbd>:

![Configurazione](images/zerobrane/setup.png)

Una volta impostata la directory del progetto Defold corrente, dovresti poter vedere l'albero delle directory del progetto Defold in ZeroBrane, esplorarlo e aprire i file.

Più avanti nel documento trovi altre modifiche alla configurazione consigliate, ma non necessarie.

## Avvio del server di debug {#starting-the-debugging-server}

Prima di iniziare una sessione di debug, devi avviare il server di debug integrato di ZeroBrane. L'opzione per avviarlo si trova nel menu <kbd>Project</kbd>. Seleziona <kbd>Project ▸ Start Debugger Server</kbd>:

![Avvio del debugger](images/zerobrane/startdebug.png)

## Connessione dell'applicazione al debugger {#connecting-your-application-to-the-debugger}

Puoi iniziare il debug in qualsiasi momento del ciclo di vita dell'applicazione Defold, ma devi avviarlo esplicitamente da uno script Lua. Il codice Lua per avviare una sessione di debug è il seguente:

::: sidenote
Se il gioco si chiude quando viene chiamato `dbg.start()`, potrebbe essere perché ZeroBrane ha rilevato un problema e invia il comando di uscita al gioco. Per qualche motivo, ZeroBrane richiede un file aperto per avviare la sessione di debug; altrimenti mostra il messaggio:
"Can't start debugging without an opened file or with the current file not being saved 'untitled.lua')."
Per risolvere questo errore, apri in ZeroBrane il file in cui hai aggiunto `dbg.start()`.
:::

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start()
```

Inserendo il codice precedente nell'applicazione, questa si connetterà al server di debug di ZeroBrane (tramite "localhost", per impostazione predefinita) e si fermerà alla prossima istruzione da eseguire.

```txt
Debugger server started at localhost:8172.
Mapped remote request for '/' to '/Users/my_user/Documents/Projects/Defold_project/'.
Debugging session started in '/Users/my_user/Documents/Projects/Defold_project'.
```

Ora puoi usare le funzionalità di debug disponibili in ZeroBrane: eseguire il codice passo per passo, ispezionarlo, aggiungere e rimuovere punti di interruzione e così via.

::: sidenote
Il debug verrà abilitato soltanto per il contesto Lua da cui viene avviato. Abilitando "shared_state" in *game.project* puoi eseguire il debug dell'intera applicazione, indipendentemente da dove lo hai avviato.
:::

![Esecuzione passo per passo](images/zerobrane/code.png)

Se il tentativo di connessione fallisce (per esempio perché il server di debug non è in esecuzione), l'applicazione continuerà a funzionare normalmente al termine del tentativo.

## Debug remoto {#remote-debugging}

Poiché il debug avviene tramite normali connessioni di rete (TCP), puoi eseguirlo anche da remoto. Puoi quindi eseguire il debug dell'applicazione mentre è in esecuzione su un dispositivo mobile.

L'unica modifica necessaria riguarda il comando che avvia il debug. Per impostazione predefinita, `start()` tenta di connettersi a localhost, ma per il debug remoto devi specificare manualmente l'indirizzo del server di debug di ZeroBrane, in questo modo:

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start("192.168.5.101")
```

Devi quindi assicurarti che il dispositivo remoto disponga di una connessione di rete e che eventuali firewall o software simili consentano le connessioni TCP sulla porta 8172. In caso contrario, l'applicazione potrebbe bloccarsi all'avvio mentre tenta di connettersi al server di debug.

## Altra impostazione consigliata per ZeroBrane {#other-recommended-zerobrane-setting}

Puoi fare in modo che ZeroBrane apra automaticamente i file di script Lua durante il debug. Questo ti permette di entrare nelle funzioni di altri file sorgente durante l'esecuzione passo per passo, senza doverli aprire manualmente.

Il primo passo è accedere al file di configurazione dell'editor. Si consiglia di modificare la versione utente del file.

- Seleziona <kbd>Edit ▸ Preferences ▸ Settings: User</kbd>
- Aggiungi quanto segue al file di configurazione:

  ```txt
  - to automatically open files requested during debugging
  editor.autoactivate = true
  ```

- Riavvia ZeroBrane

![Altre impostazioni consigliate](images/zerobrane/otherrecommended.png)
