---
title: Contenuti Live Update in Defold
brief: La funzionalità Live Update offre un meccanismo che consente al runtime di recuperare e memorizzare nel bundle dell'applicazione risorse escluse intenzionalmente dal bundle durante la build. Questo manuale ne spiega il funzionamento.
---

# Live Update

Quando crea il bundle di un gioco, Defold inserisce tutte le risorse del gioco nel pacchetto risultante, specifico per la piattaforma. Nella maggior parte dei casi questa è la soluzione preferibile, perché il motore in esecuzione ha accesso immediato a tutte le risorse e può caricarle rapidamente dall'archiviazione. In alcuni casi, tuttavia, potresti voler rimandare il caricamento delle risorse a una fase successiva. Per esempio:

- Il tuo gioco è composto da una serie di episodi e vuoi includere soltanto il primo, affinché i giocatori possano provarlo prima di decidere se proseguire con il resto del gioco.
- Il tuo gioco è destinato a HTML5. Nel browser, caricare un'applicazione dall'archiviazione significa dover scaricare l'intero pacchetto dell'applicazione prima dell'avvio. Su una piattaforma di questo tipo potresti voler inviare un pacchetto iniziale minimo e avviare rapidamente l'applicazione prima di scaricare le altre risorse del gioco.
- Il tuo gioco contiene risorse molto grandi (immagini, video ecc.) di cui vuoi rimandare il download fino al momento in cui stanno per essere mostrate nel gioco. Questo permette di ridurre le dimensioni dell'installazione.

La funzionalità Live Update estende il concetto di proxy di collezione (collection proxy) con un meccanismo che consente al runtime di recuperare e memorizzare nel bundle dell'applicazione risorse escluse intenzionalmente dal bundle durante la build.

Consente di suddividere i contenuti in più archivi:

* _Archivio di base_
* File comuni ai livelli
* Pacchetto di livelli 1
* Pacchetto di livelli 2
* ...

## Preparare i contenuti per Live Update {#preparing-content-for-live-update}

Supponiamo di realizzare un gioco contenente risorse grafiche di grandi dimensioni e ad alta risoluzione. Il gioco conserva queste immagini in collezioni (collection) con un oggetto di gioco (game object) e uno sprite con l'immagine:

![Collezione della Gioconda](images/live-update/mona-lisa.png)

Per fare in modo che il motore carichi una collezione di questo tipo dinamicamente, possiamo semplicemente aggiungere un componente proxy di collezione e farlo puntare a *`monalisa.collection`*. Ora il gioco può scegliere quando caricare in memoria il contenuto della collezione dall'archiviazione, inviando un messaggio `load` al proxy di collezione. Vogliamo però andare oltre e controllare direttamente il caricamento delle risorse contenute nella collezione.

Per farlo basta selezionare la casella *Exclude* nelle proprietà del proxy di collezione, indicando a Defold di escludere tutti i contenuti di *`monalisa.collection`* durante la creazione del bundle dell'applicazione.

::: important
Le risorse a cui fa riferimento il pacchetto di base del gioco non verranno escluse.
:::

![Proxy di collezione escluso](images/live-update/proxy-excluded.png)

## Impostazioni di Live Update {#live-update-settings}

Quando Defold crea un bundle dell'applicazione, deve memorizzare da qualche parte le risorse escluse. Le impostazioni del progetto per Live Update determinano la posizione di queste risorse. Le impostazioni si trovano in <kbd>Project ▸ Live update Settings...</kbd>. Questa operazione crea un file di impostazioni se non ne esiste già uno. In *game.project*, seleziona il file di impostazioni di Live Update da usare durante la creazione del bundle. Puoi così usare impostazioni di Live Update diverse per ambienti diversi, per esempio produzione, QA, sviluppo ecc.

![Impostazioni di Live Update](images/live-update/05-liveupdate-settings-zip.png)

Attualmente Defold può memorizzare le risorse in tre modi. Scegli il metodo nel menu a discesa *Mode* della finestra delle impostazioni:

`Zip`
: Questa opzione indica a Defold di creare un archivio Zip con le risorse escluse. L'archivio viene salvato nella posizione specificata dall'impostazione *Export path* e può essere montato durante l'esecuzione usando un URI `zip:` e `liveupdate.add_mount()`.

`Folder`  
: Questa opzione indica a Defold di creare una cartella con tutte le risorse escluse. È utile quando devi elaborare ulteriormente i file prima di caricarli o inserirli in un pacchetto. Una cartella di singoli file compilati, disposti nei rispettivi percorsi di risorsa previsti, può essere montata durante l'esecuzione usando un URI `file:`.

`Amazon`
: Questa opzione indica a Defold di caricare automaticamente le risorse escluse in un bucket S3 di Amazon Web Service (AWS). Inserisci il nome del tuo *Credential profile* AWS, seleziona il *Bucket* appropriato e fornisci un nome per *Prefix*.  Puoi approfondire la configurazione di un account AWS in questa [guida ad AWS](/manuals/live-update-aws)

## Creare un bundle con Live Update {#bundling-with-live-update}

::: important
La creazione di una build e la sua esecuzione dall'editor (<kbd>Project ▸ Build</kbd>) non supportano Live Update. Per provare Live Update devi creare un bundle del progetto.
:::

Creare un bundle con Live Update è semplice. Seleziona <kbd>Project ▸ Bundle ▸ ...</kbd> e poi la piattaforma per cui vuoi creare un bundle dell'applicazione. Si apre la finestra di dialogo per la creazione del bundle:

![Creazione del bundle di un'applicazione con Live Update](images/live-update/bundle-app.png)

Durante la creazione del bundle, tutte le risorse escluse vengono omesse dal bundle dell'applicazione. Selezionando la casella *Publish Live update content*, indichi a Defold di caricare le risorse escluse su Amazon oppure di creare un archivio Zip, in base alla configurazione delle impostazioni di Live Update (vedi sopra). I contenuti Live Update pubblicati includono comunque `liveupdate.game.dmanifest`, che contiene l'elenco completo delle risorse necessarie per la distribuzione remota.

Quando pubblica contenuti Live Update, Defold rimuove automaticamente dal `game.dmanifest` incluso nel bundle le voci relative esclusivamente a Live Update, mentre il `liveupdate.game.dmanifest` pubblicato mantiene l'elenco completo delle risorse. Questo riduce le dimensioni del bundle e l'uso della memoria durante l'esecuzione. La precedente impostazione `liveupdate.exclude_entries_from_main_manifest` è stata rimossa; eventuali voci ancora presenti nel progetto vengono ignorate.

Nel flusso di lavoro basato sugli archivi, `collectionproxy.get_resources()` restituisce `{}` finché l'archivio pertinente non viene montato. Dopo il montaggio, restituisce gli hash delle risorse per quel proxy.

Fai clic su *Package* e seleziona una posizione per il bundle dell'applicazione. Ora puoi avviare l'applicazione e verificare che tutto funzioni come previsto.

## Gli archivi .zip {#the-zip-archives}

Un file .zip di Live Update contiene file esclusi dal pacchetto di base del gioco.

Sebbene la pipeline attuale supporti soltanto la creazione di un singolo file .zip, è possibile suddividerlo in file .zip più piccoli. Questo consente download più piccoli per un gioco: pacchetti di livelli, contenuti stagionali ecc. Ogni file .zip contiene anche un file manifest che descrive i metadati di ciascuna risorsa contenuta al suo interno.

## Suddividere gli archivi .zip {#splitting-zip-archives}

Spesso è utile suddividere i contenuti esclusi in diversi archivi più piccoli per controllare più nel dettaglio l'uso delle risorse. Un esempio è la suddivisione di un gioco basato su livelli in più pacchetti di livelli. Un altro è inserire in archivi separati le decorazioni dell'interfaccia a tema per diverse festività, caricando e montando soltanto il tema attivo in quel momento secondo il calendario.

Il grafo delle risorse viene memorizzato in `build/default/game.graph.json` e viene generato automaticamente ogni volta che si crea un bundle del progetto. Il file generato contiene un elenco di tutte le risorse del progetto e delle dipendenze di ciascuna risorsa. Esempio di voce:

```json
{
  "path" : "/game/player.goc",
  "hexDigest" : "caa342ec99794de45b63735b203e83ba60d7e5a1",
  "children" : [ "/game/ship.spritec", "/game/player.scriptc" ]
}
```

Ogni voce ha un `path` che rappresenta il percorso univoco della risorsa all'interno del progetto. Il `hexDigest` rappresenta l'impronta crittografica della risorsa e sarà il nome del file usato nell'archivio .zip di Live Update. Infine, il campo `children` è un elenco delle altre risorse da cui questa dipende. Nell'esempio precedente, `/game/player.goc` dipende da un componente sprite e da un componente script.

Puoi analizzare il file `game.graph.json` e usare queste informazioni per identificare gruppi di voci nel grafo delle risorse e memorizzare le risorse corrispondenti in archivi separati insieme al file manifest originale (il file manifest verrà ridotto durante l'esecuzione in modo da contenere soltanto i file presenti nell'archivio).

## Live Update su Android {#live-update-on-android}

Puoi usare Play Asset Delivery per scaricare e montare contenuti Live Update. Per saperne di più, consulta [il manuale ufficiale](https://defold.com/extension-pad/).

## Verifica dei contenuti {#content-verification}

Una delle funzionalità principali del sistema Live Update è la possibilità di usare numerosi archivi di contenuti, potenzialmente provenienti da molte versioni diverse di Defold.

Per impostazione predefinita, `liveupdate.add_mount()` verifica la versione del motore quando aggiunge un punto di montaggio.
Questo significa che sia l'archivio di base del gioco sia gli archivi di Live Update devono essere creati contemporaneamente con la stessa versione del motore, usando l'opzione per la creazione del bundle. Questo invaliderà gli archivi precedentemente scaricati dal client, costringendolo a scaricare nuovamente i contenuti.

Puoi disattivare questo comportamento tramite un flag nelle opzioni.
Quando è disattivato, la responsabilità di verificare i contenuti ricade interamente sullo sviluppatore, che deve garantire che ogni archivio di Live Update funzioni con il motore in esecuzione.

Consigliamo di memorizzare metadati per ogni punto di montaggio, così che l'applicazione possa decidere se il pacchetto debba rimanere montato. Esegui la verifica dopo aver aggiunto il punto di montaggio, anche quando l'applicazione aggiunge nuovamente all'avvio i punti di montaggio necessari.
Un modo per farlo è aggiungere un file supplementare all'archivio zip dopo aver creato il bundle del gioco. Per esempio, inserisci un `metadata.json` con le informazioni necessarie al gioco, poi recuperalo con `sys.load_resource("/metadata.json")` dopo il montaggio. _Usa un percorso di risorsa univoco per i dati personalizzati di ciascun punto di montaggio, altrimenti la ricerca delle risorse restituirà il file del punto di montaggio con la priorità più alta._

Se non lo fai, potresti ritrovarti con contenuti del tutto incompatibili con il motore, costringendolo a terminare.

## Punti di montaggio {#mounts}

Il sistema Live Update può usare più archivi di contenuti contemporaneamente.
Ogni archivio viene "montato" nel sistema delle risorse del motore, con un nome e una priorità.

Se due archivi contengono lo stesso file `sprite.texturec`, il motore caricherà il file dal punto di montaggio con la priorità più alta.

Il motore non conserva riferimenti alle risorse di un punto di montaggio. Una volta caricata una risorsa in memoria, l'archivio può essere smontato. La risorsa rimane in memoria finché non viene scaricata dalla memoria.

I punti di montaggio sono attivi soltanto per la sessione corrente del motore. Dopo un riavvio, l'applicazione deve chiamare nuovamente `liveupdate.add_mount()` per ogni pacchetto di cui ha bisogno. Memorizza la posizione del pacchetto, il nome del punto di montaggio e la priorità in dati persistenti gestiti dall'applicazione se queste scelte devono essere mantenute tra una sessione e l'altra.

::: sidenote
Montare un archivio Zip o una cartella non li copia né li sposta. I contenuti montati devono rimanere nella posizione specificata finché il punto di montaggio è in uso.
:::

## Usare Live Update negli script {#scripting-with-live-update}

Per usare effettivamente i contenuti di Live Update, devi scaricare e montare i dati nel gioco.
Per approfondire, consulta la guida su come [usare Live Update negli script](/manuals/live-update-scripting).

## Accorgimenti durante lo sviluppo {#development-caveats}

Debug
: Quando esegui una versione del gioco distribuita come bundle, non hai accesso diretto a una console. Questo crea problemi per il debug. Puoi però eseguire l'applicazione dalla riga di comando o facendo doppio clic direttamente sull'eseguibile nel bundle:

  ![Esecuzione di un'applicazione da un bundle](images/live-update/run-bundle.png)

  Ora il gioco si avvia con una finestra della shell che mostra l'output di tutte le istruzioni `print()`:

  ![Output della console](images/live-update/run-bundle-console.png)

Forzare un nuovo download delle risorse
: Lo sviluppatore può scaricare i contenuti in qualsiasi file o cartella desideri, ma spesso si trovano all'interno del percorso dell'applicazione. La posizione della cartella di supporto dell'applicazione dipende dal sistema operativo. Puoi trovarla con `print(sys.get_save_file("", ""))`. Per forzare un download, rimuovi il pacchetto scaricato e la voce corrispondente da qualsiasi stato gestito dall'applicazione. Non esiste un elenco dei punti di montaggio gestito dal motore da eliminare; i punti di montaggio non persistono dopo un riavvio.

  ![Archiviazione locale](images/live-update/local-storage.png)
