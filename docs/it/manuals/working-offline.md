---
title: Lavorare offline
brief: Questo manuale descrive come lavorare offline su progetti che contengono dipendenze e, in particolare, estensioni native
---

# Lavorare offline {#working-offline}

Nella maggior parte dei casi, Defold non richiede una connessione a Internet per funzionare. Ci sono tuttavia alcune situazioni in cui è necessaria:

* Aggiornamenti automatici
* Segnalazione di problemi
* Recupero delle dipendenze
* Compilazione delle estensioni native


## Aggiornamenti automatici {#automatic-updates}

Defold controlla periodicamente se sono disponibili nuovi aggiornamenti. I controlli degli aggiornamenti di Defold vengono effettuati sul [sito ufficiale dei download](https://d.defold.com). Se viene rilevato un aggiornamento, questo viene scaricato automaticamente.

Se hai una connessione a Internet solo per periodi di tempo limitati e non vuoi attendere l'avvio dell'aggiornamento automatico, puoi scaricare manualmente le nuove versioni di Defold dal [sito ufficiale dei download](https://d.defold.com).


## Segnalazione di problemi {#reporting-issues}

Se viene rilevato un problema nell'editor, puoi scegliere di segnalarlo nel sistema di tracciamento dei problemi di Defold. Questo sistema è [ospitato su GitHub](https://www.github.com/defold/editor2-issues), quindi è necessaria una connessione a Internet per segnalare il problema.

Se riscontri un problema mentre sei offline, puoi segnalarlo manualmente in seguito usando l'[opzione Report Issue nel menu Help](/manuals/getting-help/#report-a-problem-from-the-editor) dell'editor.


## Recupero delle dipendenze {#fetching-dependencies}

Defold consente agli sviluppatori di condividere codice e asset tramite i cosiddetti [progetti libreria (Library Projects)](/manuals/libraries/). Le librerie sono file zip che possono essere ospitati ovunque online. In genere puoi trovare progetti libreria Defold su GitHub e in altri repository di codice sorgente online.

Puoi aggiungere una libreria a un progetto come [dipendenza nelle impostazioni del progetto](/manuals/project-settings/#dependencies). Le dipendenze vengono scaricate o aggiornate all'apertura del progetto oppure ogni volta che selezioni l'opzione *Fetch Libraries* dal menu *Project*.

Se devi lavorare offline su più progetti, puoi scaricare le dipendenze in anticipo e poi condividerle tramite un server locale. Le dipendenze su GitHub sono solitamente disponibili nella scheda Releases del repository del progetto:

![URL della libreria su GitHub](images/libraries/libraries_library_url_github.png)

Puoi usare Python per creare facilmente un server locale:

    python -m SimpleHTTPServer

Questo comando crea un server nella directory corrente che serve i file su `localhost:8000`. Se la directory corrente contiene le dipendenze scaricate, puoi aggiungerle al file *game.project*:

    http://localhost:8000/extension-fbinstant-4.1.1.zip


## Compilazione delle estensioni native {#building-native-extensions}

Defold consente agli sviluppatori di aggiungere codice nativo per ampliare le funzionalità del motore tramite un sistema chiamato [estensioni native (Native Extensions)](/manuals/extensions/). Defold permette di iniziare a usare le estensioni native senza alcuna configurazione, grazie a una soluzione di build basata sul cloud.

La prima volta che crei una build di un progetto che contiene un'estensione nativa, il codice nativo viene compilato sui server di build di Defold e incorporato in un motore di gioco Defold personalizzato, che viene poi inviato al tuo PC. Il motore personalizzato viene memorizzato nella cache del progetto e riutilizzato per le build successive, finché non aggiungi, rimuovi o modifichi un'estensione nativa e non aggiorni l'editor.

Se devi lavorare offline e il tuo progetto contiene estensioni native, assicurati di completare con successo almeno una build, in modo che il progetto contenga una copia del motore personalizzato nella cache.
