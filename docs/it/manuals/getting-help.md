---
title: Come ottenere assistenza
brief: Questo manuale descrive come ottenere assistenza se riscontri un problema durante l'uso di Defold.
---

# Ottenere assistenza {#getting-help}

Se riscontri un problema durante l'uso di Defold, faccelo sapere così potremo risolverlo e/o aiutarti ad aggirarlo! Ci sono diversi modi per discutere dei problemi e segnalarli. Scegli l'opzione più adatta a te:

## Segnalare un problema sul forum {#report-a-problem-on-the-forum}

Un buon modo per discutere di un problema e ricevere assistenza è pubblicare una domanda sul nostro [forum](https://forum.defold.com). Pubblicala nella categoria [Questions](https://forum.defold.com/c/questions) o [Bugs](https://forum.defold.com/c/bugs), a seconda del tipo di problema. Prima di fare una domanda, ricorda di [cercare](https://forum.defold.com/search) la tua domanda o il tuo problema, perché potrebbe già esserci una soluzione.

Se hai diverse domande, crea più post. Non porre domande su argomenti diversi nello stesso post.

### Informazioni necessarie {#required-information}
Non potremo fornire assistenza se non ci comunichi le informazioni necessarie:

**Titolo**
Assicurati di usare un titolo breve e descrittivo. Un buon titolo potrebbe essere "Come sposto un oggetto di gioco nella direzione in cui è ruotato?" oppure "Come faccio a far scomparire gradualmente uno sprite?". Un titolo poco utile sarebbe "Mi serve aiuto per usare Defold!" oppure "Il mio gioco non funziona!".

**Descrizione del bug (OBBLIGATORIA)**
Una descrizione chiara e concisa del bug.

**Procedura per riprodurlo (OBBLIGATORIA)**
Passaggi per riprodurre il comportamento:
1. Vai a '...'
2. Fai clic su '....'
3. Scorri verso il basso fino a '....'
4. Osserva l'errore

**Comportamento atteso (OBBLIGATORIO)**
Una descrizione chiara e concisa di ciò che ti aspettavi accadesse.

**Versione di Defold (OBBLIGATORIA):**
  - Versione [ad es. 1.2.155]

**Piattaforme (OBBLIGATORIE):**
 - Piattaforme: [ad es. iOS, Android, Windows, macOS, Linux, HTML5]
 - Sistema operativo: [ad es. iOS8.1, Windows 10, High Sierra]
 - Dispositivo: [ad es. iPhone6]

**Progetto minimo per riprodurre il problema (FACOLTATIVO):**
Allega un progetto minimo in cui si riproduca il bug. Sarà di grande aiuto a chi cercherà di analizzarlo e risolverlo.

**Log (FACOLTATIVI):**
Fornisci i log pertinenti del motore, dell'editor o del server di build. Scopri [qui](#log-files) dove vengono salvati i log.

**Soluzione temporanea (FACOLTATIVA):**
Se esiste una soluzione per aggirare il problema, descrivila qui.

**Schermate (FACOLTATIVE):**
Se utili, aggiungi delle schermate per illustrare il problema.

**Ulteriori informazioni (FACOLTATIVE):**
Aggiungi qui qualsiasi altra informazione utile sul problema.


### Condividere il codice {#sharing-code}
Quando condividi del codice, ti consigliamo di farlo come testo, anziché come schermate. Il testo permette di effettuare ricerche, evidenziare gli errori e suggerire o apportare modifiche facilmente. Condividi il codice racchiudendolo tra tre \`\`\` oppure indentandolo con 4 spazi.

Esempio:

\`\`\`
print("Hello code!")
\`\`\`

Risultato:

```
print("Hello code!")
```


## Segnalare un problema dall'editor {#report-a-problem-from-the-editor}

L'editor offre un modo pratico per segnalare i problemi. Seleziona la voce di menu <kbd>Help->Report Issue</kbd> nell'editor per segnalare un problema.

![](images/getting_help/report_issue.png)

Selezionando questa voce di menu si aprirà il sistema di tracciamento dei problemi su GitHub. Fornisci i [file di log](#log-files), informazioni sul sistema operativo, i passaggi per riprodurre il problema, eventuali soluzioni temporanee e così via.

::: sidenote
Per inviare una segnalazione di bug in questo modo è necessario un account GitHub.
:::


## Discutere di un problema su Discord {#discuss-a-problem-on-discord}

Se riscontri un problema durante l'uso di Defold, puoi provare a porre la domanda su [Discord](https://www.defold.com/discord/). Consigliamo comunque di pubblicare sul forum le domande complesse e le discussioni approfondite. Tieni inoltre presente che non accettiamo segnalazioni di bug inviate tramite Discord.


# File di log {#log-files}

Il motore, l'editor e il server di build generano informazioni di log che possono essere molto utili quando si chiede assistenza e si analizza un problema. Fornisci sempre i file di log quando segnali un problema:

* [Log del motore](/manuals/debugging-game-and-system-logs)
* [Log dell'editor](/manuals/editor#editor-logs)
* [Log del server di build](/manuals/extensions#build-server-logs)
