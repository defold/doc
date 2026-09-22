---
title: Ottimizzare le dimensioni di un gioco Defold
brief: Questo manuale descrive come ottimizzare le dimensioni di un gioco Defold.
---

# Ottimizzare le dimensioni del gioco {#optimizing-game-size}

Le dimensioni del gioco possono essere un fattore determinante per il successo su piattaforme come il web e i dispositivi mobili, mentre hanno meno importanza su desktop e console, dove lo spazio su disco è economico e spesso abbondante.

### iOS e Android {#ios-and-android}
Apple e Google hanno definito limiti alle dimensioni delle applicazioni scaricabili tramite reti mobili (rispetto al download tramite Wi-Fi). Per Android questo limite è di 200 MB per le app pubblicate con gli [app bundle](https://developer.android.com/guide/app-bundle#size_restrictions). Su iOS gli utenti ricevono un avviso se l'applicazione supera i 200 MB, ma possono comunque procedere al download.

::: sidenote
Uno studio del 2017 ha mostrato che "Per ogni aumento di 6 MB nelle dimensioni di un APK, si osserva una diminuzione dell'1% nel tasso di conversione in installazioni." ([fonte](https://medium.com/googleplaydev/shrinking-apks-growing-installs-5d3fcba23ce2))
:::

### HTML5
Poki e molte altre piattaforme di giochi web consigliano che il download iniziale non superi i 5 MB.

Facebook raccomanda che un Facebook Instant Game si avvii in meno di 5 secondi e preferibilmente in meno di 3 secondi. Non è definito con chiarezza che cosa significhi in termini di dimensioni effettive dell'applicazione, ma si parla di dimensioni fino a circa 20 MB.

Gli annunci giocabili hanno solitamente un limite compreso tra 2 e 5 MB, a seconda della rete pubblicitaria.

## Strategie per ottimizzare le dimensioni {#size-optimization-strategies}
Puoi ottimizzare le dimensioni dell'applicazione in due modi: riducendo le dimensioni del motore e/o quelle degli asset del gioco.

Per capire meglio che cosa contribuisce alle dimensioni dell'applicazione, puoi [generare un report di build](/manuals/bundling/#build-reports) durante la creazione del bundle. Molto spesso sono i suoni e la grafica a occupare la maggior parte dello spazio di un gioco.

::: important
Defold crea un albero delle dipendenze durante la build e la creazione del bundle dell'applicazione. Il sistema di build parte dalla collezione di bootstrap specificata nel file *game.project* ed esamina ogni collezione, oggetto di gioco e componente a cui viene fatto riferimento, per creare un elenco degli asset in uso. Solo questi asset vengono inclusi nel bundle finale dell'applicazione. Tutto ciò a cui non viene fatto riferimento direttamente viene escluso. Anche se è utile sapere che gli asset inutilizzati non verranno inclusi, come sviluppatore devi comunque valutare che cosa entra nell'applicazione finale, le dimensioni dei singoli asset e le dimensioni complessive del bundle dell'applicazione. 
:::

## Ottimizzare le dimensioni del motore {#optimize-engine-size}
Un modo rapido per ridurre le dimensioni del motore è rimuovere le funzionalità che non usi. Puoi farlo tramite il [file manifest dell'applicazione](https://defold.com/manuals/app-manifest/), che consente di rimuovere i componenti del motore di cui non hai bisogno. Esempi:

* Fisica - Se il gioco non usa la fisica di Box2D o Bullet3D, è fortemente consigliato rimuovere i motori fisici
* GUI, effetti particellari e tilemap - Puoi escludere separatamente questi componenti con le [opzioni dei componenti nell'App Manifest](/manuals/app-manifest/#exclude-gui). Rimuovi i riferimenti ai componenti e le chiamate API per ogni funzionalità che escludi. Escludere gli effetti particellari rimuove anche il supporto per i nodi particellari nelle scene GUI.
* Testo formattato - Disabilita [Use Rich Text](/manuals/app-manifest/#use-rich-text) se alle etichette e al testo GUI serve soltanto testo semplice. Questo rimuove l'analisi del testo formattato e gli effetti di stile, mantenendo il normale rendering del testo.
* LiveUpdate - Se il gioco non usa LiveUpdate, puoi rimuoverlo
* Caricamento delle immagini - Se il gioco non carica e decodifica manualmente le immagini usando `image.load()`
* BasisU - Se il gioco contiene poche texture, confronta le dimensioni di una build senza BasisU (rimosso tramite il manifest dell'applicazione) e senza compressione delle texture con quelle di una build con BasisU e texture compresse. Per i giochi con poche texture, può essere più vantaggioso ridurre le dimensioni del binario e rinunciare alla compressione delle texture. Inoltre, non usare il transcodificatore può ridurre la quantità di memoria necessaria per eseguire il gioco.

## Ottimizzare le dimensioni degli asset {#optimize-asset-size}
I maggiori vantaggi nell'ottimizzazione delle dimensioni degli asset si ottengono solitamente riducendo le dimensioni di suoni e texture.

### Ottimizzare i suoni {#optimize-sounds}
Defold supporta questi formati:
* .wav
* .ogg
* .opus

Defold supporta file Wave PCM a 8 e 16 bit. Ogg Vorbis e Ogg Opus usano i rispettivi formati compressi e non richiedono una profondità in bit PCM specifica. Il decodificatore Opus non è incluso per impostazione predefinita; abilita **Include Sound Decoder: Opus** nel [manifest dell'applicazione](/manuals/app-manifest/#sound) prima di usare risorse `.opus`.
I decodificatori audio di Defold aumentano o riducono la frequenza di campionamento dei suoni in base alle esigenze del dispositivo audio in uso.

I suoni più brevi, come gli effetti sonori, vengono spesso compressi maggiormente, mentre i file musicali subiscono una compressione minore.
Defold non esegue alcuna compressione, quindi devi occupartene in modo specifico per ogni formato audio.

Puoi modificare i suoni con un programma esterno di editing audio (o dalla riga di comando, usando ad esempio [ffmpeg](https://ffmpeg.org)) per ridurne la qualità o convertirli tra formati. Valuta anche la conversione dei suoni da stereo a mono per ridurre ulteriormente le dimensioni dei contenuti.

### Ottimizzare le texture {#optimize-textures}
Hai diverse opzioni per ottimizzare le texture usate dal gioco, ma la prima cosa da fare è controllare le dimensioni delle immagini aggiunte a un atlas o usate come sorgenti di tile. Non dovresti mai usare immagini più grandi di quanto sia effettivamente necessario nel gioco. Importare immagini grandi e ridimensionarle verso il basso fino alla dimensione appropriata è uno spreco di memoria per le texture e va evitato. Inizia adattando le immagini alle dimensioni effettivamente necessarie nel gioco con un programma esterno di editing delle immagini. Per elementi come le immagini di sfondo, può anche andare bene usare un'immagine piccola e ingrandirla fino alle dimensioni desiderate. Una volta portate le immagini alle dimensioni corrette e aggiunte agli atlas o usate nelle sorgenti di tile, devi considerare anche le dimensioni degli atlas stessi. La dimensione massima utilizzabile per un atlas varia in base alla piattaforma e all'hardware grafico.

::: sidenote
[Questo post del forum](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl) offre diversi suggerimenti per ridimensionare più immagini usando script o software di terze parti.
:::

* Dimensione massima delle texture su HTML5 segnalata al [progetto Web3D Survey](https://web3dsurvey.com/webgl/parameters/MAX_TEXTURE_SIZE)
* Dimensione massima delle texture su iOS:
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* La dimensione massima delle texture su Android varia molto, ma in generale tutti i dispositivi abbastanza recenti supportano almeno 4096x4096.

Se un atlas è troppo grande, devi dividerlo in più atlas più piccoli, usare atlas con più pagine oppure ridimensionare l'intero atlas tramite un profilo di texture. Il sistema dei profili di texture di Defold consente sia di ridimensionare interi atlas sia di applicare algoritmi di compressione per ridurre le dimensioni dell'atlas su disco. Puoi [approfondire i profili di texture nel manuale](/manuals/texture-profiles/). Se non sai che cosa usare, prova queste impostazioni come punto di partenza per ulteriori personalizzazioni:

* mipmaps: false
* premultiply_alpha: true
* format: TEXTURE_FORMAT_RGBA
* compression_level: NORMAL
* compression_type: COMPRESSION_TYPE_BASIS_UASTC

::: sidenote
Puoi approfondire come ottimizzare e gestire le texture in [questo post del forum](https://forum.defold.com/t/texture-management-in-defold/8921).
:::

### Ottimizzare i caratteri {#optimize-fonts}
I caratteri occuperanno meno spazio se specifichi quali simboli intendi usare e li imposti in [Characters](/manuals/font/#properties), invece di usare la casella di controllo All Chars.

### Escludere contenuti per scaricarli su richiesta {#exclude-content-for-download-on-demand}
Un altro modo per ridurre le dimensioni iniziali dell'applicazione è escludere parti dei contenuti del gioco dal bundle dell'applicazione e scaricarle su richiesta. Defold offre un sistema chiamato Live Update per escludere contenuti da scaricare su richiesta.

I contenuti esclusi possono comprendere interi livelli oppure personaggi, aspetti, armi o veicoli sbloccabili. Se il gioco contiene molti contenuti, organizza il processo di caricamento in modo che la collezione di bootstrap e quella del primo livello includano solo le risorse strettamente necessarie per quel livello. Puoi ottenere questo risultato usando proxy di collezione o fabbriche (factory) con la casella di controllo "Exclude" abilitata. Suddividi le risorse in base ai progressi del giocatore. Questo approccio garantisce un caricamento efficiente delle risorse e mantiene basso l'utilizzo iniziale della memoria. Per saperne di più, consulta il [manuale di Live Update](/manuals/live-update/).

## Ottimizzazioni delle dimensioni specifiche per Android {#android-specific-size-optimizations}
Le build Android devono supportare architetture CPU sia a 32 bit sia a 64 bit. Quando [crei un bundle per Android](/manuals/android), puoi specificare quali architetture CPU includere:

![Firma del bundle Android](images/android/sign_bundle.png)

Per impostazione predefinita, un bundle include le architetture `armv7-android` e `arm64-android`. È disponibile una terza architettura, `x86_64-android`, che non è inclusa per impostazione predefinita perché è utile soprattutto per gli emulatori Android, ChromeOS e Windows Subsystem for Android, più che per i dispositivi fisici. Lasciala deselezionata per contenere le dimensioni del bundle, a meno che tu non debba supportare specificamente uno di questi ambienti.

Google Play supporta [più APK](https://developer.android.com/google/play/publishing/multiple-apks) per ogni release di un gioco: puoi quindi ridurre le dimensioni dell'applicazione generando due APK, uno per ogni architettura CPU, e caricandoli entrambi su Google Play.

Puoi anche combinare i [file di espansione APK](https://developer.android.com/google/play/expansion-files) con i [contenuti Live Update](/manuals/live-update) grazie all'[estensione APKX nell'Asset Portal](https://defold.com/assets/apkx/).
