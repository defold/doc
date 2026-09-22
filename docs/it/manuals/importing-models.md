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
* *.gltf* è un file JSON testuale. Di solito fa riferimento a un file *.bin* separato per i dati della mesh e a immagini delle texture separate, come *.png* o *.jpg*. Quando usi questa variante, aggiungi al progetto tutti i file a cui fa riferimento e mantieni intatti i loro percorsi relativi.

Se il modello deve usare una texture in Defold, importa l'immagine della texture come asset separato. Anche quando il file glTF/GLB sorgente contiene immagini incorporate, le texture devono essere assegnate al componente modello attraverso le proprietà delle texture del materiale del componente.

![Asset del modello importati](images/model/assets_gltf.png)

::: sidenote
A partire da Defold 1.13.0, Defold conserva le posizioni e le trasformazioni del file glTF importato e non ricentra automaticamente il modello durante l'importazione. L'anteprima dell'editor e il runtime usano le trasformazioni importate in modo coerente: le mesh deformate tramite skinning o con un osso come genitore conservano le proprie trasformazioni locali relative allo scheletro, mentre le mesh rigide mantengono la collocazione nello spazio globale risultante dall'appiattimento della gerarchia.

Da Defold 1.13.2, un [componente modello](/manuals/model/#model-properties) può selezionare una singola mesh con nome dalla scena importata. Lasciando vuoto il campo *Mesh*, viene usata l'intera scena e vengono conservate le trasformazioni descritte sopra. Selezionando una mesh, viene usata la sua geometria locale senza le trasformazioni dei nodi glTF: posizionala quindi tramite la trasformazione del componente modello o dell'oggetto di gioco.

Se un modello creato con una versione precedente di Defold cambia posizione o orientamento dopo una nuova importazione, correggi la trasformazione in Blender o in un altro strumento di creazione ed esporta di nuovo il file *.gltf* o *.glb*.
:::

## Utilizzo di un modello {#using-a-model}
Dopo aver importato il modello, usalo in un [componente modello](/manuals/model):

1. Crea un file Model dal pannello *Assets* con <kbd>New... ▸ Model</kbd>, oppure aggiungi un componente modello direttamente a un oggetto di gioco con <kbd>Add Component ▸ Model</kbd>.
2. Imposta la proprietà *Scene* sul file *.gltf* o *.glb* importato. Lascia vuoto *Mesh* per usare l'intera scena oppure seleziona una mesh con nome per usarne soltanto la geometria locale.
3. Per un modello animato, imposta la proprietà *Skeleton* sul file *.gltf* o *.glb* che contiene lo scheletro. Spesso è lo stesso file usato per *Scene* quando mesh, scheletro e animazioni vengono esportati insieme.
4. Crea un file *Animation Set* per le animazioni e assegnalo alla proprietà *Animations*. Imposta *Default Animation* se vuoi che un'animazione si avvii automaticamente.
5. Imposta la proprietà *Material* su un materiale adatto al modello. I file integrati *model.material*, *model_instanced.material*, *model_skinned.material* e *model_skinned_instanced.material* sono utili punti di partenza. I materiali per lo skinning usano lo spazio locale dei vertici affinché lo skinning possa essere eseguito sulla GPU; anche i materiali personalizzati per i modelli con skinning sulla GPU o per i modelli istanziati devono usare lo spazio locale dei vertici. Consulta il [manuale dei modelli](/manuals/model/#material) per il requisito relativo all'adattatore grafico.
6. Imposta le proprietà delle texture del materiale, come *Texture*, sui file delle immagini delle texture importate. Se il materiale usa più texture, assegna ciascuna texture al campo corrispondente delle texture del materiale.


## Esportazione in glTF {#exporting-to-gltf}
Il file *.gltf* o *.glb* esportato contiene tutti i vertici, gli spigoli e le facce che compongono il modello, oltre alle _coordinate UV_ (quale parte dell'immagine della texture corrisponde a una determinata parte della mesh), se le hai definite, alle ossa dello scheletro e ai dati di animazione.

* Una descrizione dettagliata delle mesh poligonali è disponibile su http://en.wikipedia.org/wiki/Polygon_mesh.

* Le coordinate UV e la mappatura UV sono descritte su http://en.wikipedia.org/wiki/UV_mapping.

Defold impone alcune limitazioni ai dati di animazione esportati:

* Attualmente Defold supporta solo animazioni precalcolate (baked). Le animazioni devono avere matrici per ogni osso animato a ogni fotogramma chiave, anziché posizione, rotazione e scala come chiavi separate.

* Inoltre, le animazioni vengono interpolate linearmente. Se usi un'interpolazione delle curve più avanzata, le animazioni devono essere precalcolate dall'esportatore.

### Requisiti {#requirements}
Quando esporti un modello, tieni presente che il supporto a glTF può variare tra strumenti e motori. Usa glTF 2.0, assicurati che il modello abbia coordinate UV corrette se usa texture e importa separatamente le immagini delle texture quando devono essere assegnate a un componente modello.

Sebbene il nostro obiettivo sia supportare completamente il formato glTF, non ci siamo ancora arrivati.
Se manca una funzionalità, invia una richiesta per aggiungerla nel [nostro repository](https://github.com/defold/defold/issues)

### Esportazione di una texture {#exporting-a-texture}
Se non hai già una texture per il modello, puoi usare Blender per generarne una. Dovresti farlo prima di rimuovere i materiali aggiuntivi dal modello. Inizia selezionando la mesh e tutti i suoi vertici:

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
