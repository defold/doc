---
title: Importazione dei modelli
brief: Questo manuale spiega come importare i modelli 3D utilizzati dal componente modello.
---

# Importazione di modelli 3D {#importing-3d-models}
Defold supporta modelli, scheletri e animazioni nel formato glTF 2.0 (GL Transmission Format). Usa file *.gltf* o *.glb* per i modelli 3D. glTF è un formato moderno progettato per trasferire e caricare dati 3D nei motori di gioco e nelle applicazioni in tempo reale.

Puoi usare strumenti come Maya, 3ds Max, SketchUp e Blender per creare modelli 3D o convertirli in glTF.

Blender è un programma potente e diffuso per la modellazione 3D, l'animazione e il rendering. Funziona su Windows, macOS e Linux ed è disponibile gratuitamente all'indirizzo [https://www.blender.org](https://www.blender.org).

![Modello in Blender](images/model/blender_gltf.png)

## Importazione in Defold {#importing-to-defold}
Per importare un modello, trascina e rilascia il file *.gltf* o *.glb* nel *pannello Assets* dell'editor Defold.

glTF può essere salvato in due modi comuni:

* *.glb* è un singolo file binario. Contiene i dati del modello e può contenere anche le immagini delle texture incorporate. È comodo quando vuoi spostare o archiviare un modello come un unico file.
* *.gltf* è un file JSON testuale. Di solito fa riferimento a un file *.bin* separato per i dati delle mesh e a immagini texture separate, come *.png*, *.jpg* o *.ktx2*. Quando usi questa variante, aggiungi tutti i file referenziati al progetto e mantieni intatti i percorsi relativi.

Le immagini incorporate possono essere usate direttamente da un file glTF o GLB senza estrarle in asset separati. I file esterni di immagini e buffer devono comunque essere importati con il modello, preservandone i percorsi relativi.

::: sidenote
Defold conserva le posizioni e le trasformazioni del file glTF importato e non ricentra automaticamente il modello durante l'importazione. L'anteprima dell'editor e il runtime usano in modo coerente le trasformazioni importate: le mesh con skinning o con un osso come genitore conservano le trasformazioni locali relative allo scheletro, mentre le mesh rigide mantengono il posizionamento nel mondo risultante dall'appiattimento della gerarchia.

Un [componente Model](/manuals/model/#model-properties) può selezionare una singola mesh denominata dalla scena importata. Lasciare vuoto il campo *Mesh* usa l'intera scena e conserva le trasformazioni descritte sopra. Selezionare una mesh ne usa la geometria locale senza le trasformazioni dei nodi glTF: posizionala quindi tramite la trasformazione del componente Model o dell'oggetto di gioco.

Se un modello creato con una versione precedente di Defold cambia posizione o orientamento dopo una nuova importazione, correggi la trasformazione in Blender o in un altro strumento di creazione ed esporta di nuovo il file *.gltf* o *.glb*.
:::

### Geometria compressa {#compressed-geometry}

Le sorgenti *.gltf* e *.glb* possono contenere geometria compressa con Draco o Meshopt. Le estensioni di compressione glTF supportate sono:

| Compressione | Estensione glTF |
| --- | --- |
| Draco | `KHR_draco_mesh_compression` |
| Meshopt | `EXT_meshopt_compression` e `KHR_meshopt_compression` |

Esporta o ottimizza l'asset glTF 2.0 usando una di queste estensioni, quindi importalo seguendo gli stessi passaggi di un modello non compresso. Includi tutti i buffer e le texture esterni, preservandone i percorsi relativi. Assegna il file importato alla proprietà *Scene* di un componente Model come di consueto.

Defold decodifica la geometria compressa durante l'importazione e la build. Il modello risultante usa la normale rappresentazione geometrica di Defold a runtime. Questo supporto non abilita la compressione Draco o Meshopt nel motore in esecuzione e un file sorgente più piccolo non garantisce un bundle del gioco più piccolo.

### Esplorazione della scena importata {#browsing-the-imported-scene}

Espandi un file *.gltf* o *.glb* nel pannello *Assets* per esplorarne mesh, materiali generati e immagini incorporate. Aprire la scena ne mostra un'anteprima con i materiali e le texture definiti. Puoi anche aprire una singola mesh per visualizzarne l'anteprima.

Le risorse esposte all'interno del file sono di sola lettura. Per creare una risorsa Model modificabile per una mesh, copia la mesh e incollala in una cartella del progetto. Il file *.model* risultante continua a fare riferimento al file glTF o GLB importato. Per modificare la geometria sorgente o le immagini incorporate, modifica l'asset nello strumento di creazione ed esportalo di nuovo.

Gli script dell'editor possono enumerare queste risorse con `editor.resource_children(path)`. Consulta [Attraversamento delle risorse del progetto](/manuals/editor-scripts/#traversing-project-resources) per un esempio che visita ricorsivamente le risorse contenute nelle cartelle e nei file glTF/GLB.

### Texture KTX2 {#ktx2-textures}

Le texture dei modelli possono usare sorgenti *.ktx2*, sia come file esterni sia come immagini incorporate in un file *.gltf* o *.glb*. Importa i file esterni insieme al modello. Le immagini KTX2 incorporate compaiono sotto la scena nel pannello *Assets* e possono essere assegnate direttamente ai campi texture dei materiali o tramite <kbd>Auto Fill</kbd>.

I [profili texture](/manuals/texture-profiles/#ktx2-source-textures) determinano se conservare il formato sorgente KTX2 o convertirlo nei formati di uscita configurati. **Keep KTX2 Format** preserva il formato di codifica sorgente quando la compressione delle texture è abilitata, ma l'elaborazione dell'immagine può comunque richiedere una nuova codifica. Controlla il supporto del formato sui dispositivi di destinazione e considera la possibile perdita aggiuntiva di qualità quando ricomprimi una texture già compressa. Consulta [Formati di ingresso e anteprime KTX2](/manuals/importing-graphics/#ktx2-textures).

## Utilizzo di un modello {#using-a-model}
Dopo aver importato il modello, usalo in un [componente modello](/manuals/model):

1. Crea un file Model dal pannello *Assets* con <kbd>New... ▸ Model</kbd>, oppure aggiungi un componente modello direttamente a un oggetto di gioco con <kbd>Add Component ▸ Model</kbd>.
2. Imposta la proprietà *Scene* sul file *.gltf* o *.glb* importato.
3. Quando compare la finestra *Auto Fill Model Fields?*, scegli <kbd>Auto Fill</kbd> per assegnare i materiali generati e le texture referenziate dalla scena. Ciò sostituisce le associazioni esistenti di materiali e texture. Scegli <kbd>Keep Current</kbd> per conservare le tue associazioni; la nuova selezione della scena viene comunque applicata.
4. Lascia *Mesh* vuoto per usare l'intera scena oppure seleziona una mesh denominata per usarne soltanto la geometria locale. Cambiare la selezione della mesh può mostrare la stessa finestra: selezionare una mesh propone i suoi materiali, mentre cancellare la selezione propone tutti i materiali della scena. <kbd>Keep Current</kbd> conserva le associazioni applicando la nuova selezione della mesh.
5. Per un modello animato, imposta la proprietà *Skeleton* sul file *.gltf* o *.glb* contenente lo scheletro. Spesso è lo stesso file usato per *Scene* quando mesh, scheletro e animazioni vengono esportati insieme.
6. Crea un file *Animation Set* per le animazioni e assegnalo alla proprietà *Animations*. Imposta *Default Animation* se vuoi che un'animazione parta automaticamente.

L'editor propone di compilare le associazioni quando la sorgente glTF o GLB selezionata espone dei materiali. Risolve sia le immagini incorporate sia i riferimenti a immagini esterne. I materiali generati usano gli shader glTF integrati; consulta il [manuale PBR](/manuals/physically-based-rendering/#built-in-pbr-materials) per l'illuminazione e gli effetti dei materiali supportati.

### Assegnazione manuale di materiali e texture {#assigning-materials-and-textures-manually}

Se scegli <kbd>Keep Current</kbd> o hai bisogno di uno shading personalizzato, imposta ogni proprietà *Material* su un materiale appropriato. I materiali `gltf` integrati forniscono lo shading PBR; sono disponibili anche i materiali `model` integrati e i tuoi materiali. Consulta il [manuale dei modelli](/manuals/model/#material) per le varianti statiche, con skinning e con istanze e per i relativi requisiti.

Assegna ogni texture al campo texture del materiale corrispondente. Puoi usare un'immagine incorporata esposta sotto il file glTF o GLB nel pannello *Assets* oppure un asset immagine separato nel progetto. Per i materiali con più sampler, associa ogni texture al sampler previsto; il [manuale PBR elenca i nomi dei sampler glTF integrati](/manuals/physically-based-rendering/#built-in-pbr-materials).


## Esportazione in glTF {#exporting-to-gltf}
Il file *.gltf* o *.glb* esportato contiene tutti i vertici, gli spigoli e le facce che compongono il modello, oltre alle _coordinate UV_ (quale parte dell'immagine della texture corrisponde a una determinata parte della mesh), se le hai definite, alle ossa dello scheletro e ai dati di animazione.

* Una descrizione dettagliata delle mesh poligonali è disponibile su http://en.wikipedia.org/wiki/Polygon_mesh.

* Le coordinate UV e la mappatura UV sono descritte su http://en.wikipedia.org/wiki/UV_mapping.

Defold impone alcune limitazioni ai dati di animazione esportati:

* Attualmente Defold supporta solo animazioni precalcolate (baked). Le animazioni devono avere matrici per ogni osso animato a ogni fotogramma chiave, anziché posizione, rotazione e scala come chiavi separate.

* Inoltre, le animazioni vengono interpolate linearmente. Se usi un'interpolazione delle curve più avanzata, le animazioni devono essere precalcolate dall'esportatore.

### Requisiti {#requirements}
Quando esporti un modello, ricorda che il supporto glTF può differire tra strumenti e motori. Usa glTF 2.0 e assicurati che il modello abbia coordinate UV corrette se usa texture. Le immagini possono essere incorporate nel file glTF o GLB oppure memorizzate in file separati referenziati dalla scena. Includi tutti i file esterni di immagini e buffer quando importi il modello in Defold.

Sebbene il nostro obiettivo sia supportare completamente il formato glTF, non ci siamo ancora arrivati.
Se manca una funzionalità, invia una richiesta per aggiungerla nel [nostro repository](https://github.com/defold/defold/issues)

### Esportazione di una texture {#exporting-a-texture}
Se vuoi creare manualmente un'immagine texture, puoi esportare il layout UV da Blender come modello. Inizia selezionando la mesh e tutti i suoi vertici:

![Selezione di tutti i vertici](images/model/blender_select_all_vertices.png)

Quando tutti i vertici sono selezionati, distendi la mesh per ottenere il layout UV:

![Distensione della mesh](images/model/blender_unwrap_mesh.png)

Puoi quindi esportare il layout UV in un'immagine da usare come texture:

![Esportazione del layout UV](images/model/blender_export_uv_layout.png)

![Risultato dell'esportazione del layout UV](images/model/blender_export_uv_layout_result.png)

### Esportazione con Blender {#exporting-using-blender}
Esporta il modello da Blender usando <kbd>File ▸ Export ▸ glTF 2.0 (.glb/.gltf)</kbd>.

![Esportazione con Blender](images/model/export_gltf.png)

Seleziona l'oggetto o gli oggetti prima di esportare e abilita *Selected Objects* se vuoi esportare solo la selezione.

Scegli una delle opzioni di *Format*:

* *glTF Binary (.glb)* crea un solo file. Usa questa opzione se vuoi che il modello sia facile da spostare o archiviare come un unico asset.
* *glTF Separate (.gltf + .bin + textures)* crea file separati per la descrizione del modello, i dati binari e le texture. Usa questa opzione se vuoi modificare le immagini delle texture o assegnarle separatamente in Defold.

Se il modello contiene animazioni, abilita l'esportazione delle animazioni e assicurati che siano precalcolate. Se il modello usa texture, assicurati che la mesh sia stata distesa per la mappatura UV e che le immagini delle texture vengano esportate in un formato che Defold può importare, come PNG o JPEG.

![Esportazione con Blender](images/model/export_settings.png)
