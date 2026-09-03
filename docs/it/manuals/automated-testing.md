---
title: Test automatici e verifica
brief: Questo manuale spiega come progettare, eseguire e documentare test Defold deterministici in locale, in un gioco in esecuzione, nei browser e nell'integrazione continua.
---

# Test automatici e verifica

I test automatici verificano il codice e i contenuti Defold tramite prove esplicite e leggibili dalle macchine. Usa questo manuale per progettare test che funzionino allo stesso modo con script locali, runner di CI (integrazione continua) e agenti di programmazione. Il manuale tratta test di modulo, collezioni in esecuzione, test nel browser, automazione a runtime, controlli visivi e build headless, oltre a fornire buone pratiche utili.

## Livelli di verifica {#verification-levels}

I buoni livelli di test automatico seguono il modello della piramide dei test, che suddivide i test in tre livelli principali: test unitari, test di integrazione e test end-to-end (E2E). In Defold puoi separare i test in collezioni specifiche caricabili al bootstrap. In genere è opportuno iniziare dal controllo più circoscritto e veloce in grado di rilevare il problema, aggiungendo poi test a runtime o specifici della piattaforma quando necessario.

| Livello | Prove adatte |
| --- | --- |
| Convalida statica | Parser, formatter, validatore di risorse o confronto di file generati |
| Test di modulo | Risultati delle asserzioni per la logica Lua riutilizzabile con dipendenze minime dal motore |
| Collezione in esecuzione | Messaggi, componenti, input, fisica, ciclo di vita e comportamento del motore |
| Automazione a runtime | Stato della scena in esecuzione, input iniettato, stato dell'applicazione e schermate a runtime |
| Test HTML5 nel browser | Input nel canvas, integrazione con il browser, comportamento della viewport e output web |
| Test di piattaforma | Comportamento e rendering dalla piattaforma di destinazione effettiva |
| Build e bundle | Stato di uscita di Bob, report di build, archivio e artefatti del bundle |

Una compilazione riuscita dimostra che il progetto viene compilato, ma non garantisce il corretto comportamento del gameplay. Una schermata non dimostra transizioni, animazioni, interazioni o flussi di gioco complessi, ma può essere utilizzata dalle moderne soluzioni multimodali per esaminare l'aspetto di un singolo fotogramma e verificare la correttezza degli shader e del layout visivo. Per i test automatici, tuttavia, prediligi asserzioni deterministiche ogni volta che la condizione può essere espressa direttamente.

## Codice Lua riutilizzabile e verificabile {#reusable-and-testable-lua-code}

Mantieni la logica riutilizzabile in moduli Lua con dipendenze minime dal motore. In questo modo, trasformazioni di dati pure, regole, macchine a stati e calcoli possono essere verificati senza creare un mondo di gioco completo.

Separa il codice che interagisce con il motore dalla logica che richiama. Uno script può tradurre messaggi e stato dei componenti in chiamate a un modulo, mentre i test richiamano direttamente il modulo con input controllati.

Per ulteriori dettagli, consulta il [manuale Scrivere codice](/manuals/writing-code).

## Test in una collezione in esecuzione {#tests-in-a-running-collection}

Utilizza una collezione di test dedicata quando il comportamento dipende da oggetti di gioco, componenti, messaggi, input, fisica o altri sistemi del motore.

Ogni test dovrebbe:

1. stabilire uno stato noto;
2. eseguire un comportamento;
3. verificare e valutare il risultato atteso;
4. rimuovere le risorse create;
5. emettere una descrizione strutturata del risultato.

Prediligi collezioni di test isolate. Un progetto può selezionare una collezione di bootstrap per i test tramite un'impostazione temporanea del progetto in `game.project`:

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

Non lasciare un bootstrap di test temporaneo nella configurazione normale del progetto. Nella CI, prediligi un file di impostazioni dedicato passato a Bob. La CI non può modificare lo stato del repository; dovrebbe apportare soltanto modifiche temporanee quando necessario.

Per i giochi complessi, puoi creare piccole collezioni usate come "stanze di sviluppo", con scenari predefiniti e semplici volumi provvisori. Rendono le meccaniche riproducibili e agevolano lo sviluppo e i test senza dover attraversare sezioni e stati di gioco non pertinenti.

### Framework di test {#test-frameworks}

I progetti possono implementare un piccolo runner o utilizzare una [libreria di test della comunità](https://defold.com/assets/?tag=testing).

Ad esempio, [DefTest](https://defold.com/assets/deftest/) è una libreria di test unitari basata su Telescope. Supporta suite, funzioni di setup e teardown, asserzioni, filtri per nome, mock per determinate API Defold e la copertura facoltativa LuaCov. I test possono essere eseguiti da una collezione di bootstrap dedicata, anche in un bundle headless creato con Bob.

## Risultati dei test strutturati {#structured-test-results}

Il riepilogo della console o del log di un framework può essere utile agli sviluppatori, ma un controller automatico non presidiato necessita comunque di un risultato di completamento esplicito. Se necessario, aggiungi un piccolo adattatore intorno al callback o al riepilogo del framework, in modo che il controller possa elaborare facilmente i risultati dei test.

Una semplice descrizione dei risultati può utilizzare un prefisso univoco seguito da un oggetto JSON su ogni riga fisica della console:

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

Un raccoglitore dovrebbe elaborare ogni riga in modo indipendente, trovare il prefisso `TEST`, analizzare il JSON che segue e ignorare l'output del motore non pertinente.

Includi un identificatore di esecuzione univoco, affinché l'output di un processo precedente o simultaneo non possa completare l'esecuzione corrente. Ogni suite dovrebbe emettere un solo evento finale non ambiguo (come `Pass`, `Failure`, `Crash`, `Timeout` ecc.).

### Raccolta dell'output della console {#collecting-console-output}

Quando un gioco viene eseguito dall'editor, sono disponibili sia la cronologia corrente della console sia un flusso continuo. Chiudi il flusso dopo un evento di completamento della suite corrispondente, la terminazione del processo, un errore o il raggiungimento del timeout o del limite di righe configurato.

Per ulteriori informazioni, consulta il [manuale dell'API HTTP dell'editor](/manuals/editor-http-api/#reading-console-output).

### Log persistenti {#persisted-logs}

Defold può anche salvare il log del gioco abilitando `Write Log File` in `game.project`. Consulta [Log di gioco e di sistema](/manuals/debugging-game-and-system-logs/). La registrazione su file è utile per le applicazioni distribuite in pacchetti e per testare dispositivi di destinazione sui quali la console dell'editor non è disponibile.

Il progetto può utilizzare le funzioni integrate `print()` e `pprint()` oppure, ad esempio, qualsiasi altra [libreria di logging](https://defold.com/assets/?tag=logging) disponibile nel nostro Asset Portal.

## Testare un gioco in esecuzione tramite un'API di runtime {#testing-a-running-game-through-a-runtime-api}

Un'API di automazione a runtime può ispezionare e controllare un motore di debug in esecuzione. Può essere utilizzata quando i test devono trovare oggetti a runtime, iniettare input, attendere uno stato visibile o acquisire il risultato renderizzato.

Per ulteriori dettagli, consulta il [manuale del servizio del motore](/manuals/engine-service/#automation-bridge-extension).

L'esempio seguente utilizza la struttura dell'helper Python di [Automation Bridge](https://github.com/defold/extension-automation-bridge). Il progetto deve includere una versione compatibile dell'estensione di debug, esporre un elemento con l'ID di automazione specificato e pubblicare lo stato dell'applicazione `screen`:

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()

try:
    play = game.element(automation_id="play_button")
    game.click(play)
    game.wait_for_state("screen", "gameplay", timeout=5.0)
    screenshot = game.screenshot()
    print(screenshot.path)
finally:
    game.close_engine()
```

Gli stati definiti dall'applicazione e gli ID di automazione utilizzano l'API Lua facoltativa di Automation Bridge, disponibile soltanto in modalità debug. Il progetto deve abilitare l'API ed esporre esplicitamente tali dati. Un'attesa fissa è sensibile alla velocità del computer e alla temporizzazione dei fotogrammi; un polling circoscritto di uno stato definito è più affidabile.

Automation Bridge è un'estensione, non fa parte del motore principale. Consulta il relativo [riferimento API Python](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) per selettori, attese, stato, eventi, schermate e diagnostica della versione installata.

## Test nel browser per HTML5 {#browser-tests-for-html5}

L'editor può creare e servire una build HTML5 tramite il comando corrente `build-html5`, come descritto nel [manuale dell'API HTTP dell'editor](/manuals/editor-http-api/#building-html5). Bob può inoltre creare un bundle HTML5 senza l'editor.

Strumenti esterni di automazione del browser come Playwright, Puppeteer, Selenium, WebdriverIO o Cypress possono:

* attendere il canvas Defold e che l'applicazione sia pronta;
* inviare input da tastiera, mouse e tocco emulato;
* ridimensionare la viewport;
* raccogliere l'output della console del browser e gli errori JavaScript;
* acquisire schermate e confrontare gli artefatti.

L'input indirizzato al canvas viene elaborato tramite i normali binding di input del progetto e i callback `on_input()`. Verifica sia la risposta del gioco sia i punti di integrazione specifici del browser.

L'approccio più affidabile consiste nell'esporre un bridge di test JavaScript esplicito nell'`index.html` personalizzato. Sul lato Defold, le build HTML5 possono eseguire JavaScript tramite `html5.run()`, rendendo possibile la comunicazione con un simile bridge lato browser. Per i comandi che passano da JavaScript a Defold, utilizza un bridge dedicato tra JavaScript e il motore.

Mantieni circoscritti i test nel browser. Nel report finale, distingui tra errore di caricamento della pagina, canvas mancante, errore JavaScript, timeout del test e asserzione del gioco non riuscita.

## Anteprime dell'editor e schermate a runtime per l'ispezione visiva {#editor-previews-and-runtime-screenshots}

È possibile acquisire una schermata di una risorsa nella vista predefinita della scena dell'editor aperto oppure di un gioco a runtime.

| Metodo | Scopo |
| --- | --- |
| [Anteprima dell'editor](/manuals/editor-http-api/#rendering-scene-previews) | Layout delle risorse caricate, ad esempio un livello o una GUI, composizione dell'atlas, ispezione della tilemap, composizione statica della scena, correttezza del rendering e degli shader dell'editor oppure creazione di miniature per la documentazione |
| [Schermata a runtime](/manuals/engine-service) | Stato renderizzato di una build in esecuzione in uno scenario controllato |

Puoi utilizzare il confronto di immagini, ad esempio, per i test di regressione. Quando un controllo fallisce, conserva l'immagine delle differenze e le metriche di confronto.

Un modello multimodale può valutare durante l'ispezione visiva condizioni semantiche difficili da esprimere diversamente, come testo tagliato, controlli sovrapposti, stati di selezione poco chiari o contenuti al di fuori di un'area sicura. È consigliabile considerare tale valutazione come un segnale aggiuntivo con criteri espliciti, ma non come sostituto di controlli logici deterministici o del confronto di immagini.

## Test headless e CI {#headless-tests-and-ci}

Utilizza Bob, lo strumento di build a riga di comando, per una CI indipendente dall'editor.

Puoi utilizzarlo per risolvere le dipendenze, creare una build del gioco, un archivio o un bundle autonomo e generare un report JSON:

```sh
mkdir -p build/reports

java -jar bob.jar \
  --root . \
  --archive \
  --build-report-json build/reports/build-report.json \
  resolve build
```

Crea un bundle di test headless con impostazioni dedicate:

```sh
java -jar bob.jar \
  --root . \
  --settings test/test.settings \
  --platform x86_64-linux \
  --variant headless \
  --archive \
  --bundle-output build/test-bundle \
  resolve build bundle
```

Esegui l'eseguibile risultante con un controller di processo adatto alla piattaforma. Acquisiscine lo stato di uscita e i log, imponi un timeout e richiedi l'evento strutturato di completamento della suite.

Il [manuale di Bob](/manuals/bob) descrive piattaforme, file di impostazioni, bundle, cache, estensioni native e report di build.

## Report degli errori e artefatti {#failure-reports-and-artifacts}

I buoni risultati dei test dovrebbero conservare prove sufficienti per riprodurre e diagnosticare un errore:

* nome del test, identificatore di esecuzione e dettagli dell'asserzione;
* tempo trascorso ed esito classificato;
* log completo della console o del processo;
* versione di Defold, piattaforma di destinazione e configurazione pertinente;
* report di build di Bob e stato di uscita del processo;
* stato a runtime o istantanea della scena, quando disponibile;
* schermate, differenze rispetto alla baseline, registrazioni o tracce del browser;
* percorsi o link a tutti gli artefatti generati.

Lo stesso formato dovrebbe poter essere utilizzato da uno sviluppatore, uno script locale, un servizio CI o un [agente di programmazione IA](/manuals/ai-agents). In questo modo, la verifica resta deterministica anche quando la diagnosi o la correzione viene delegata.
