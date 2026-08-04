---
title: Automazione in Defold
brief: Questo manuale introduce le interfacce di automazione di Defold e spiega come scegliere tra flussi di lavoro basati sull'editor, sul runtime, sulla riga di comando, sui test e sugli agenti.
---

# Automazione in Defold

Questo manuale offre una descrizione generale e i link ai manuali separati dedicati a ciascun argomento.

Defold supporta l'automazione a diversi livelli. Scegliere un'interfaccia adatta all'attività è uno degli aspetti più importanti per un'automazione efficace. La tabella seguente può aiutarti a scegliere l'interfaccia più semplice per una determinata azione:

| Livello | Scopo |
| --- | --- |
| [Script dell'editor](/manuals/editor-scripts) | Comandi personalizzati e flussi di lavoro o integrazioni dell'editor per velocizzare test e sviluppo, ad esempio la creazione di livelli e asset |
| [Script per l'interfaccia dell'editor](/manuals/editor-scripts-ui/) | Strumenti visivi, finestre a comparsa, configuratori o interfacce utente personalizzati che utilizzano gli script dell'editor |
| [API HTTP dell'editor](/manuals/editor-http-api) | Controllo del progetto di gioco aperto nell'editor Defold tramite operazioni OpenAPI, risorse del progetto, build, comandi dell'editor, anteprime, preferenze, output della console o script dell'editor per operazioni personalizzate, strumenti esterni, integrazioni IDE e controller di test |
| [Bob CLI](/manuals/bob) | Build di un progetto, creazione di archivi di dati o bundle autonomi dalla riga di comando, report, CI |
| [Hook del ciclo di vita](/manuals/editor-http-api#lifecycle-hooks) | Convalida o generazione prima e dopo le build dell'editor o la creazione dei bundle |
| [Servizio HTTP del motore](/manuals/engine-service) | Ispezione del motore di gioco Defold (`dmengine`) in esecuzione, servizi di sviluppo, profilazione, messaggi a runtime o API di automazione a runtime definite da estensioni, interrogazioni da strumenti esterni e invio di comandi a una build di debug in esecuzione |
| [Automation Bridge](https://github.com/defold/extension-automation-bridge) | Estensione ufficiale Defold che fornisce ulteriori endpoint per l'automazione del motore a runtime |
| [Test automatici](/manuals/automated-testing) | Test di logica di gioco, messaggi, componenti, input, fisica e comportamento del motore, ispezione delle scene, feedback visivo, ad esempio tramite [anteprima dell'editor](/manuals/editor-http-api/#rendering-scene-previews), input iniettato, stato dell'applicazione in esecuzione, [collection di test in esecuzione](/manuals/automated-testing/#tests-in-a-running-collection) |
| Script di shell o task runner | Generazione, formattazione, convalida e attività ripetibili, normali operazioni sui file |
| Strumenti esterni di automazione specifici della piattaforma e del browser web | Strumenti di test desktop, test di interazione HTML5, schermate, integrazioni web |
| Agenti di programmazione IA e modelli multimodali | Attività per le quali un approccio deterministico è difficile o impossibile da implementare, analisi semantica di scene, layout GUI o schermate a runtime |

La distinzione più importante è quella tra l'editor Defold e un gioco in esecuzione. Sono processi separati con server HTTP separati.

## Automazione deterministica o agenti IA {#deterministic-automation-or-ai-agents}

Prediligi una soluzione deterministica quando la sequenza di operazioni è già nota, ad esempio in un validatore di livelli, un formatter, un processo di build o un test di regressione. Queste soluzioni dovrebbero normalmente avere input, output, timeout e codici di uscita stabili. Sono adatte a hook e test automatici eseguibili in modo affidabile nella CI. È preferibile una soluzione deterministica anche per la creazione procedurale di risorse nei progetti, ad esempio uno strumento che converta oggetti glTF in modelli con un determinato materiale o popoli un livello con alberi. Queste procedure possono essere create facilmente per ogni progetto con gli script e l'interfaccia dell'editor. Per ulteriori informazioni, consulta [il manuale](/manuals/editor-scripts-ui).

Un agente può essere utile quando un'attività richiede indagine o analisi multimodale, ad esempio visiva: individuare risorse pertinenti, scegliere un'implementazione, modificare più file, interpretare errori e iterare verso criteri di accettazione definiti. L'agente dovrebbe comunque richiamare interfacce deterministiche e utilizzare le stesse prove di uno script locale o di un runner CI. Consulta il manuale sull'[utilizzo degli agenti di programmazione IA con Defold](/manuals/ai-agents).

## Il ciclo di automazione {#the-automation-loop}

Un processo di automazione affidabile forma un ciclo chiuso:

1. Ispeziona: leggi i file del progetto, la descrizione corrente dell'interfaccia e la documentazione pertinente.
2. Modifica: utilizza transazioni dell'editor, script dell'editor o strumenti per file e shell.
3. Verifica: crea una build, esegui test mirati e raccogli log, report, stati o immagini.
4. Valuta: confronta le prove con i criteri di accettazione, quindi termina o riprova.

![Il ciclo di automazione di ispezione, modifica, verifica e valutazione](images/automation/automation_loop.png)

La verifica dovrebbe fornire prove provenienti dall'ambiente effettivo. Tra le prove adatte figurano:

* il risultato positivo di una build;
* una suite di test completata esplicitamente;
* lo stato previsto del gioco in esecuzione;
* un bundle o un report di build generato;
* un confronto deterministico di immagini;
* una schermata che soddisfa criteri visivi definiti.

Definisci il risultato previsto prima di apportare modifiche. Definisci inoltre un timeout e un numero massimo di tentativi di correzione. Un processo non presidiato non dovrebbe proseguire indefinitamente quando non riesce a soddisfare i criteri di accettazione.

## Passaggi successivi {#next-steps}

Trova maggiori dettagli su argomenti specifici relativi ai flussi di lavoro di automazione nei manuali indicati:

* [Automatizzare le attività dell'editor Defold con l'API HTTP](/manuals/editor-http-api)
* [Il servizio del motore e l'API HTTP a runtime](/manuals/engine-service)
* [Test automatici e verifica](/manuals/automated-testing)
* [Utilizzare agenti di programmazione IA con Defold](/manuals/ai-agents)
