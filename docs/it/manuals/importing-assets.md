---
title: Importazione e modifica degli asset
brief: Questo manuale spiega come importare e modificare gli asset.
---

# Importazione e modifica degli asset {#importing-and-editing-assets}

Un progetto di gioco è solitamente composto da numerosi asset esterni, realizzati con vari programmi specializzati per la creazione di grafica, modelli 3D, file audio, animazioni e così via. Defold è progettato per un flusso di lavoro in cui usi i tuoi strumenti esterni e importi gli asset in Defold man mano che sono pronti.


## Importazione degli asset {#importing-assets}

Defold richiede che tutti gli asset usati nel progetto si trovino all'interno della gerarchia del progetto. Devi quindi importare tutti gli asset prima di poterli usare. Per importare gli asset, basta trascinare i file dal file system del computer e rilasciarli nella posizione appropriata nel *pannello Assets* dell'editor Defold.

![Importazione dei file](images/graphics/import.png)

::: sidenote
Defold supporta immagini nei formati PNG e JPEG. Le immagini PNG devono essere in formato RGBA a 32 bit. Gli altri formati di immagine devono essere convertiti prima di poter essere usati.
:::


## Uso degli asset {#using-assets}

Una volta importati in Defold, gli asset possono essere usati dai vari tipi di componenti supportati da Defold:

* Le immagini possono essere usate per creare molti tipi di componenti visivi di uso comune nei giochi 2D. Per saperne di più, consulta [come importare e usare la grafica 2D](/manuals/importing-graphics).
* I suoni possono essere usati dal [componente Sound](/manuals/sound) per riprodurre audio.
* I font vengono usati dal [componente Label](/manuals/label) e dai [nodi di testo](/manuals/gui-text) in una GUI.
* I modelli glTF (*.gltf* e *.glb*) possono essere usati dal [componente Model](/manuals/model) per mostrare modelli 3D con animazioni. Importa tutte le immagini delle texture usate dal modello come asset separati e assegnale nelle proprietà delle texture del materiale del componente Model. Per saperne di più, consulta [come importare e usare i modelli 3D](/manuals/importing-models).


## Modifica degli asset esterni {#editing-external-assets}

Defold non fornisce strumenti di modifica per immagini, file audio, modelli o animazioni. Questi asset devono essere creati al di fuori di Defold con strumenti specializzati e poi importati in Defold. Defold rileva automaticamente le modifiche apportate a qualsiasi asset tra i file del progetto e aggiorna di conseguenza la vista dell'editor.


## Modifica degli asset Defold {#editing-defold-assets}

L'editor salva tutti gli asset Defold in file di testo che facilitano l'unione delle modifiche. Sono anche facili da creare e modificare con semplici script. Consulta [questa discussione sul forum](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210) per ulteriori informazioni. Tieni presente, però, che non pubblichiamo i dettagli del nostro formato di file perché cambiano di tanto in tanto. Puoi anche usare gli [script dell'editor](/manuals/editor-scripts/) per intercettare determinati eventi del ciclo di vita dell'editor ed eseguire script che generano o modificano gli asset.

Presta particolare attenzione quando lavori sui file degli asset Defold con un editor di testo o uno strumento esterno. Eventuali errori introdotti possono impedire l'apertura del file nell'editor Defold.

Alcuni strumenti esterni, come [Tiled](/assets/tiled/) e [Tilesetter](https://www.tilesetter.org/beta), possono essere usati per generare automaticamente asset Defold.
