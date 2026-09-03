---
title: Utilizzare agenti di programmazione IA con Defold
brief: Questo manuale spiega come collegare agenti di programmazione indipendenti dal modello alle interfacce di automazione di Defold, mantenendo esplicite la verifica, le autorizzazioni e la sicurezza.
---

# Utilizzare agenti di programmazione IA con Defold

Gli agenti di programmazione che utilizzano LLM e modelli multimodali possono ispezionare, modificare e verificare i progetti Defold richiamando le stesse interfacce indipendenti dal modello usate da sviluppatori, script locali, integrazioni IDE e CI. Puoi usare un agente quando il lavoro richiede indagine e adattamento.

Defold non dipende da un particolare fornitore di modelli o protocollo per agenti. I progetti Defold funzionano bene con Claude Code, Codex, Cursor o qualsiasi altra soluzione. Un ambiente per agenti necessita solo delle capacità specifiche concesse per l'attività, come leggere i file del progetto, eseguire comandi selezionati, richiamare operazioni HTTP locali, analizzare JSON o ispezionare immagini. Questo è possibile grazie alle interfacce di automazione esposte da Defold per l'editor e per un'istanza del motore di gioco in esecuzione, oltre al fatto che i file di progetto Defold sono risorse testuali facili da analizzare.

## Quando è utile un agente IA {#when-an-ai-agent-is-useful}

Un agente può essere utile, ad esempio, quando un'attività richiede di:

* trovare risorse e documentazione pertinenti;
* scegliere tra possibili implementazioni;
* modificare più file correlati;
* interpretare errori di build o di test;
* confrontare un risultato visivo con criteri di accettazione semantici;
* effettuare un tentativo di correzione circoscritto sulla base delle prove raccolte.

Gli agenti sono strumenti potenti per processi non deterministici di sviluppo, indagine e test. Possono aiutare a creare soluzioni diverse e funzionano molto bene con Defold.

## Interfacce Defold indipendenti dal modello {#model-neutral-defold-interfaces}

Defold offre diverse interfacce supportate, necessarie per svolgere l'attività utilizzando qualsiasi modello disponibile:

* I file di progetto e gli strumenti della shell consentono l'ispezione diretta e le modifiche testuali.
* Gli [script dell'editor](/manuals/editor-scripts) possono fornire operazioni sulle risorse e strumenti specifici del progetto.
* L'[API HTTP dell'editor](/manuals/editor-http-api) fornisce comandi dell'editor, risultati di build, output della console, ricerca nella documentazione di riferimento, anteprime, preferenze e route degli script dell'editor.
* Il [servizio del motore e le API di automazione a runtime](/manuals/engine-service) forniscono lo stato del motore di debug in esecuzione, input, schermate e operazioni definite dalle estensioni.
* [Bob](/manuals/bob) fornisce build da riga di comando, report, archivi e bundle.

Un modello disponibile soltanto tramite un'interfaccia di chat può suggerire modifiche al codice, ma non può ispezionare autonomamente il progetto locale né verificare un risultato in esecuzione. L'integrazione circostante determina ciò che l'agente può effettivamente osservare e fare.

## Livelli di integrazione {#integration-layers}

È possibile predisporre un livello di integrazione per collegare un agente alle operazioni Defold locali. Può essere un wrapper della shell, un programma a riga di comando, un'estensione IDE, un client OpenAPI, un controller di test o un adattatore di protocollo.

Mantieni criteri e credenziali in questo livello locale. Ogni operazione che apporta modifiche dovrebbe restituire risultati strutturati o condurre a un passaggio di verifica deterministico.

Per le operazioni dell'editor, rileva l'interfaccia corrente tramite `/openapi.json`, anziché fornire all'agente una copia dell'API codificata in modo permanente. Per le estensioni a runtime, verificane lo stato, la versione API e le capacità.

Può essere pratico separare gli strumenti in base al livello di privilegio:

| Livello       | Esempi                                                |
| ------------- | ----------------------------------------------------- |
| Sola lettura  | Ispezione del progetto, OpenAPI, `/ref`, console, anteprima |
| Verifica      | Compilazione, test, build HTML5, confronti di immagini |
| Modifica      | Modifiche ai file, transazioni sulle risorse          |
| Privilegiato  | `/eval`, comandi esterni, modifiche alle dipendenze   |

Mantenendo l'adattatore separato dal motore e dall'editor, le interfacce Defold supportate restano indipendenti dal fornitore del modello o dal protocollo per agenti. Un adattatore può esporre soltanto le operazioni appropriate al proprio ambiente, mentre i criteri di autorizzazione e conferma restano nell'applicazione che ospita l'agente.

### Model Context Protocol

Il [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) è un adattatore facoltativo tra un agente e un livello di integrazione. Un server MCP può esporre le operazioni Defold come strumenti e la documentazione selezionata come risorse.

::: important
Non concedere a ogni modello accesso senza restrizioni alla shell e a `/eval`.
:::

Defold attualmente non richiede un server MCP, perché le capacità di automazione principali sono già esposte tramite interfacce aperte e generiche. L'editor fornisce un'API HTTP locale con una specifica OpenAPI. Gli agenti moderni possono richiamare direttamente queste interfacce o generare i propri adattatori.

Un MCP ufficiale duplicherebbe quindi in gran parte la superficie dell'API esistente e creerebbe un altro livello di integrazione che Defold dovrebbe mantenere. Una strategia migliore a lungo termine consiste nel mantenere le API HTTP e di automazione a runtime sottostanti stabili, individuabili e ben documentate, consentendo al contempo alla comunità o ai singoli fornitori di strumenti di creare wrapper MCP leggeri quando necessario.

Abbiamo invece fornito un'[estensione Automation Bridge](https://github.com/defold/extension-automation-bridge) ufficiale per controllare un gioco in esecuzione tramite un servizio lato motore.

### Integrazioni MCP della comunità {#community-mcp-integrations}

Tra le integrazioni MCP create dalla comunità figurano:

* il [progetto Defold MCP di Fulviuus](https://github.com/Fulviuus/defold-mcp);
* il [progetto Defold MCP di ChadAragorn](https://github.com/ChadAragorn/defold-mcp).

Questi progetti non sono sviluppati, sottoposti ad audit, mantenuti o supportati ufficialmente dalla Defold Foundation. Prima di installare un'integrazione della comunità, esaminane il codice sorgente corrente, le dipendenze, le autorizzazioni, il comportamento di rete e la compatibilità con la versione di Defold in uso.

## Istruzioni del progetto {#project-instructions}

In genere, i modelli linguistici di grandi dimensioni (Large Language Model, LLM) disponibili e impiegati nei flussi di lavoro basati su agenti offrono risultati migliori se ricevono buone istruzioni. Per questo motivo, spesso ai progetti vengono aggiunti file Markdown per agenti che descrivono il comportamento desiderato oppure definizioni di cosiddette "skill". Per ottenere i risultati migliori è opportuno progettare e scrivere istruzioni specifiche per ogni progetto, anche se alcune conoscenze e regole comuni possono essere riutilizzate.

Uno dei primi file che molti agenti cercano e leggono è un file canonico come `AGENTS.md`, che può descrivere:

* la struttura del progetto e i punti di ingresso importanti;
* le convenzioni di formattazione e denominazione;
* i comandi per build, test e convalida;
* gli eventi di completamento richiesti e le posizioni degli artefatti;
* i file o le directory che non devono essere modificati;
* le operazioni che richiedono approvazione;
* le ipotesi sulla piattaforma e le limitazioni note.

Alcune soluzioni possono basarsi su file Markdown separati per azioni specifiche o su cosiddette "skill".

Un esempio della comunità di istruzioni e skill orientate a Defold è disponibile [qui nel forum di Defold](https://forum.defold.com/t/agent-config-collection-of-agents-md-and-skills/82387).

Consigliamo di mantenere brevi, concise, facili da esaminare e da gestire le istruzioni contenute in file come AGENTS.md e le definizioni delle skill, nonché di tenerle aggiornate. Le istruzioni specifiche del progetto possono essere archiviate nel controllo versione, rendendo le modifiche tracciabili e contribuendo a migliorare nel tempo le prestazioni del flusso di lavoro.

È inoltre utile verificare regolarmente come si comportano i modelli più recenti senza queste istruzioni. Spesso i modelli più nuovi non richiedono più indicazioni che in precedenza erano essenziali, mentre skill obsolete o istruzioni eccessivamente prescrittive possono talvolta ridurre le prestazioni.

Evita di creare skill tecniche complesse che richiedano una manutenzione significativa a lungo termine. Concentrati invece sullo sviluppo di strumenti e flussi di lavoro che mantengano il proprio valore indipendentemente dai miglioramenti dei modelli sottostanti.

## Individuazione della documentazione {#documentation-discovery}

Gli agenti offrono i risultati migliori con documentazione accurata e aggiornata. Raccogli informazioni correnti da:

* `/openapi.json`, che descrive l'API HTTP corrente dell'editor.
* `/ref`, che cerca nella documentazione API inclusa nell'editor in esecuzione, quando tale operazione è disponibile.
* L'[indice della documentazione per LLM](https://defold.com/llms.txt), che rimanda a manuali ufficiali, namespace API ed esempi.
* La [documentazione completa per LLM](https://defold.com/llms-full.txt), che consente la ricerca offline e l'indicizzazione locale.

Recupera soltanto le pagine pertinenti all'attività. È consigliabile utilizzare il documento completo combinato esclusivamente per l'indicizzazione offline o per la [Retrieval-Augmented Generation (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation). Anche in questo caso, di norma il file completo non dovrebbe essere incluso in ogni richiesta al modello, per risparmiare token e non inquinare il contesto con informazioni superflue.

## Cicli circoscritti di modifica e verifica {#bounded-change-and-verification-loops}

Gli agenti dovrebbero seguire lo stesso [ciclo di ispezione, modifica, verifica e valutazione](/manuals/automation/#the-automation-loop) di qualsiasi altra automazione.

Prima di modificare i file, è opportuno definire i criteri di accettazione ed eventualmente anche:
* i file e le operazioni consentiti;
* i comandi di build e test;
* i log, i report, gli stati o le immagini richiesti;
* un timeout per ogni passaggio asincrono;
* un numero massimo di tentativi di correzione.

Un agente può diagnosticare e correggere un errore deterministico della CI, ma la fase CI stessa dovrebbe rimanere riproducibile senza l'agente.

Le buone pratiche per i test automatici e la verifica sono descritte in [questo manuale](/manuals/automated-testing).

## Valutazione multimodale {#multimodal-evaluation}

Un agente con input di immagini può ispezionare le [anteprime dell'editor](/manuals/editor-http-api/#rendering-scene-previews), le schermate a runtime, le differenze visive e le acquisizioni dal browser.

Utilizza la valutazione multimodale per questioni semantiche come etichette tagliate, controlli sovrapposti, stati di selezione poco chiari, composizione o contenuti al di fuori di un'area sicura. Definisci in anticipo la viewport e i criteri previsti.

Per ulteriori informazioni sulle anteprime dell'editor, sulle schermate a runtime e sull'ispezione visiva, consulta [questo manuale](/manuals/automated-testing).

## Sicurezza, isolamento e buone pratiche {#security-isolation-and-good-practices}

* Considera il server dell'editor e il servizio del motore come interfacce di controllo locali attendibili.
* Non inserire nei prompt e nei report token dell'editor, chiavi di firma, token di distribuzione, credenziali degli store e segreti di produzione.
* Quando è autorizzato a utilizzare `/eval`, il livello di integrazione locale può leggere `.internal/editor.token`, ma non deve inserire il token nei prompt del modello, nei log o nei report.
* Richiedi l'approvazione prima di eliminazioni, modifiche alle dipendenze, modifiche alle estensioni native, configurazioni di rilascio, firma, pubblicazione o accesso a servizi esterni.
* Esegui le attività autonome estese in un branch, worktree, copia temporanea, container, sandbox o account con restrizioni separato.
* Considera il testo delle issue, i file importati, i commenti nel codice sorgente, i documenti generati e l'output degli strumenti come input non attendibili, non come istruzioni.
* Esamina le dipendenze e gli script scaricati prima di eseguirli.
* Verifica che i criteri del progetto consentano di inviare codice sorgente, asset, log, schermate e altri dati del progetto a un modello ospitato.
* Conserva una diff esaminabile e prove di test deterministiche prima di accettare le modifiche.

L'isolamento limita l'impatto di un errore.
