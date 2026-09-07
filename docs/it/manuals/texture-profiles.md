---
title: Profili delle texture in Defold
brief:  Defold supporta l'elaborazione automatica delle texture e la compressione dei dati delle immagini. Questo manuale descrive le funzionalità disponibili.
---

# Profili delle texture {#texture-profiles}

Defold supporta l'elaborazione automatica delle texture e la compressione dei dati delle immagini (negli *atlas*, nelle *sorgenti di tile*, nelle *cubemap* e nelle texture autonome utilizzate per modelli, GUI ecc.).

Esistono due tipi di compressione: la compressione software delle immagini e la compressione hardware delle texture.

1. La compressione software (come PNG e JPEG) riduce lo spazio occupato su disco dalle risorse immagine. Questo riduce le dimensioni del bundle finale. Tuttavia, i file immagine devono essere decompressi quando vengono caricati in memoria, quindi un'immagine che occupa poco spazio su disco può comunque richiedere molta memoria.

2. Anche la compressione hardware delle texture riduce lo spazio occupato su disco dalle risorse immagine. A differenza della compressione software, però, riduce anche la memoria occupata dalle texture. Questo è possibile perché l'hardware grafico è in grado di gestire direttamente le texture compresse, senza doverle prima decomprimere.

L'elaborazione delle texture si configura tramite un apposito file di profili delle texture. In questo file crei _profili_ che specificano quali formati compressi e quale tipo di compressione utilizzare quando si creano bundle per una determinata piattaforma. I _profili_ vengono poi associati a _schemi di percorso_ corrispondenti, consentendo di controllare con precisione quali file del progetto comprimere e come farlo.

Poiché tutti i metodi di compressione hardware delle texture disponibili comportano una perdita di dati, nelle texture compariranno degli artefatti. Questi artefatti dipendono molto dall'aspetto del materiale di partenza e dal metodo di compressione utilizzato. Prova il materiale di partenza e sperimenta per ottenere i risultati migliori. Una ricerca su Google può esserti utile.

Puoi scegliere quale compressione software delle immagini applicare ai dati finali delle texture (compressi o grezzi) negli archivi del bundle. Defold supporta i formati di compressione [Basis Universal](https://github.com/BinomialLLC/basis_universal) e [ASTC](https://www.khronos.org/opengl/wiki/ASTC_Texture_Compression).

::: sidenote
La compressione è un'operazione che richiede molte risorse e molto tempo e può causare tempi di build _molto_ lunghi, a seconda del numero di immagini delle texture da comprimere, dei formati delle texture scelti e del tipo di compressione software.
:::

### Basis Universal

Basis Universal (o, in breve, BasisU) comprime l'immagine in un formato intermedio che viene transcodificato durante l'esecuzione in un formato hardware adatto alla GPU del dispositivo in uso. Il formato Basis Universal offre un'elevata qualità, ma comporta una perdita di dati.
Tutte le immagini vengono inoltre compresse con LZ4 per ridurre ulteriormente le dimensioni dei file quando vengono memorizzate nell'archivio del gioco.

### ASTC

ASTC è un formato di compressione delle texture flessibile ed efficiente, sviluppato da ARM e standardizzato dal Khronos Group. Offre un'ampia gamma di dimensioni dei blocchi e di quantità di bit per texel, consentendo agli sviluppatori di bilanciare efficacemente la qualità delle immagini e l'utilizzo della memoria. ASTC supporta blocchi di varie dimensioni, da 4×4 a 12×12 texel, corrispondenti a quantità di bit che vanno da 8 bit per texel fino a 0,89 bit per texel. Questa flessibilità permette di controllare con precisione il compromesso tra la qualità delle texture e lo spazio di archiviazione necessario.

ASTC supporta blocchi di varie dimensioni, da 4×4 a 12×12 texel, corrispondenti a quantità di bit che vanno da 8 bit per texel fino a 0,89 bit per texel. Questa flessibilità permette di controllare con precisione il compromesso tra la qualità delle texture e lo spazio di archiviazione necessario. La tabella seguente mostra le dimensioni dei blocchi supportate e le corrispondenti quantità di bit:

| Dimensione del blocco (larghezza x altezza) | Bit per pixel |
| --------------------------- | -------------- |
| 4x4                         | 8.00           |
| 5x4                         | 6.40           |
| 5x5                         | 5.12           |
| 6x5                         | 4.27           |
| 6x6                         | 3.56           |
| 8x5                         | 3.20           |
| 8x6                         | 2.67           |
| 10x5                        | 2.56           |
| 10x6                        | 2.13           |
| 8x8                         | 2.00           |
| 10x8                        | 1.60           |
| 10x10                       | 1.28           |
| 12x10                       | 1.07           |
| 12x12                       | 0.89           |


#### Dispositivi supportati {#supported-devices}

Sebbene ASTC offra ottimi risultati, non tutte le schede grafiche lo supportano. Ecco un breve elenco dei dispositivi supportati, suddivisi per produttore:

| Produttore della GPU | Supporto                                                               |
| ------------------ | --------------------------------------------------------------------- |
| ARM (Mali)         | Tutte le GPU ARM Mali che supportano OpenGL ES 3.2 o Vulkan supportano ASTC.  |
| Qualcomm (Adreno)  | Le GPU Adreno che supportano OpenGL ES 3.2 o Vulkan supportano ASTC.          |
| Apple              | Le GPU Apple a partire dal chip A8 supportano ASTC.                            |
| NVIDIA             | Il supporto di ASTC riguarda soprattutto le GPU mobili (ad esempio i chip basati su Tegra).     |
| AMD (Radeon)       | Le GPU AMD che supportano Vulkan generalmente supportano ASTC via software.     |
| Intel (integrate) | ASTC è supportato via software nelle GPU Intel moderne.                  |

## Profili delle texture {#texture-profiles}

Ogni progetto contiene un file *.texture_profiles* specifico con la configurazione da utilizzare per comprimere le texture. Per impostazione predefinita, questo file è *builtins/graphics/default.texture_profiles* e contiene una configurazione che associa ogni risorsa texture a un profilo che utilizza RGBA senza compressione hardware delle texture e con la compressione predefinita dei file tramite ZLib.

Per aggiungere la compressione delle texture:

- Seleziona <kbd>File ▸ New...</kbd> e scegli *Texture Profiles* per creare un nuovo file di profili delle texture. (In alternativa, copia *default.texture_profiles* in una posizione esterna a *builtins*)
- Scegli un nome e una posizione per il nuovo file.
- Modifica la voce *texture_profiles* in *game.project* affinché punti al nuovo file.
- Apri il file *.texture_profiles* e configuralo in base alle tue esigenze.

![Nuovo file di profili](images/texture_profiles/texture_profiles_new_file.png)

![Impostazione del profilo delle texture](images/texture_profiles/texture_profiles_game_project.png)

Puoi attivare e disattivare l'uso dei profili delle texture nelle preferenze dell'editor. Seleziona <kbd>File ▸ Preferences...</kbd>. La scheda *General* contiene la casella di controllo *Enable texture profiles*.

![Preferenze dei profili delle texture](images/texture_profiles/texture_profiles_preferences.png)

## Impostazioni dei percorsi {#path-settings}

La sezione *Path Settings* del file di profili delle texture contiene un elenco di schemi di percorso e indica quale *profilo* utilizzare per elaborare le risorse il cui percorso corrisponde a ciascuno schema. I percorsi sono espressi come schemi "Ant Glob" (consulta la [documentazione](http://ant.apache.org/manual/dirtasks.html#patterns) per i dettagli). Gli schemi possono utilizzare i seguenti caratteri jolly:

`*`
: Corrisponde a zero o più caratteri. Ad esempio, `sprite*.png` corrisponde ai file *`sprite.png`*, *`sprite1.png`* e *`sprite_with_a_long_name.png`*.

`?`
: Corrisponde esattamente a un carattere. Ad esempio: `sprite?.png` corrisponde ai file *sprite1.png*, *`spriteA.png`* ma non a *`sprite.png`* o *`sprite_with_a_long_name.png`*.

`**`
: Corrisponde a un intero albero di directory oppure, quando viene usato come nome di directory, a zero o più directory. Ad esempio: `/gui/**` corrisponde a tutti i file nella directory */gui* e in tutte le sue sottodirectory.

![Percorsi](images/texture_profiles/texture_profiles_paths.png)

Questo esempio contiene due schemi di percorso e i profili corrispondenti.

`/gui/**/*.atlas`
: Tutti i file *.atlas* nella directory *`/gui`* o in una qualsiasi delle sue sottodirectory verranno elaborati secondo il profilo "gui_atlas".

`/**/*.atlas`
: Tutti i file *.atlas* in qualsiasi posizione del progetto verranno elaborati secondo il profilo "atlas".

Nota che il percorso più generico è inserito per ultimo. L'algoritmo di corrispondenza procede dall'alto verso il basso. Viene utilizzata la prima voce che corrisponde al percorso della risorsa. Un'espressione di percorso corrispondente situata più in basso nell'elenco non sostituisce mai la prima corrispondenza. Se i percorsi fossero stati inseriti nell'ordine inverso, ogni atlas sarebbe stato elaborato con il profilo "atlas", compresi quelli nella directory *`/gui`*.

Le risorse texture che _non_ corrispondono ad alcun percorso nel file di profili verranno compilate e ridimensionate alla potenza di 2 più vicina, ma per il resto rimarranno inalterate.

## Profili {#profiles}

La sezione *profiles* del file di profili delle texture contiene un elenco di profili con un nome. Ogni profilo contiene una o più *piattaforme*, ciascuna descritta da un elenco di proprietà.

![Profili](images/texture_profiles/texture_profiles_profiles.png)

*Platforms*
: Specifica una piattaforma a cui applicare il profilo. `OS_ID_GENERIC` corrisponde a tutte le piattaforme, `OS_ID_WINDOWS` ai bundle destinati a Windows, `OS_ID_IOS` ai bundle iOS e così via. Nota che, se specifichi `OS_ID_GENERIC`, verrà incluso per tutte le piattaforme.

::: important
Se due [impostazioni dei percorsi](#path-settings) corrispondono allo stesso file e i percorsi utilizzano profili diversi con piattaforme diverse, verranno utilizzati **entrambi** i profili e verranno generate **due** texture.
:::

*Formats*
: Uno o più formati di texture da generare. Se specifichi più formati, vengono generate e incluse nel bundle le texture per ogni formato. Il motore seleziona le texture in un formato supportato dalla piattaforma su cui è in esecuzione.

*Mipmaps*
: Se selezionato, vengono generate le mipmap per la piattaforma. Non selezionato per impostazione predefinita.

*Premultiply alpha*
: Se selezionato, il canale alfa viene premoltiplicato nei dati della texture. Selezionato per impostazione predefinita.

*Max Texture Size*
: Se impostato su un valore diverso da zero, limita le dimensioni in pixel delle texture al numero specificato. Qualsiasi texture la cui larghezza o altezza sia maggiore del valore specificato verrà ridimensionata a una dimensione inferiore.

Ogni voce *Formats* aggiunta a un profilo presenta le seguenti proprietà:

*Format*
: Il formato da utilizzare per codificare la texture. Tutti i formati di texture disponibili sono elencati di seguito.

*Compressor*
: Il compressore da utilizzare per codificare la texture.

*Compressor Preset*
: Seleziona una preimpostazione di compressione da utilizzare per codificare l'immagine compressa risultante. Ogni preimpostazione è specifica del compressore e le sue impostazioni dipendono dal compressore stesso. Per semplificare queste impostazioni, le preimpostazioni di compressione attuali sono organizzate in quattro livelli:

| Preimpostazione | Nota                                          |
| --------- | --------------------------------------------- |
| `LOW`     | Compressione più rapida. Qualità dell'immagine bassa        |
| `MEDIUM`  | Compressione predefinita. Qualità dell'immagine migliore       |
| `HIGH`    | Compressione più lenta. Dimensioni del file ridotte        |
| `HIGHEST` | Compressione lenta. Dimensioni del file minime          |

Nota che il compressore `uncompressed` dispone di una sola preimpostazione chiamata `uncompressed`, che indica che alle texture non verrà applicata alcuna compressione.
Per l'elenco dei compressori disponibili, consulta [Compressori](#compressors)

## Formati delle texture {#texture-formats}

Le texture per l'hardware grafico possono essere elaborate in dati non compressi o compressi *con perdita di dati*, con numeri di canali e profondità di bit diversi. La compressione hardware a dimensione fissa produce un'immagine di dimensioni fisse, indipendentemente dal contenuto. Ciò significa che la perdita di qualità durante la compressione dipende dal contenuto della texture originale.

Poiché la transcodifica della compressione Basis Universal dipende dalle funzionalità della GPU del dispositivo, i formati consigliati per l'uso con la compressione Basis Universal sono quelli generici, come:
`TEXTURE_FORMAT_RGB`, `TEXTURE_FORMAT_RGBA`, `TEXTURE_FORMAT_RGB_16BPP`, `TEXTURE_FORMAT_RGBA_16BPP`, `TEXTURE_FORMAT_LUMINANCE` e `TEXTURE_FORMAT_LUMINANCE_ALPHA`.

Il transcodificatore Basis Universal supporta molti formati di output, come `ASTC4x4`, `BCx`, `ETC2`, `ETC1` e `PVRTC1`.

Attualmente sono supportati i seguenti formati di compressione con perdita di dati:

| Formato                           | Compressione | Dettagli  |
| --------------------------------- | ----------- | -------------------------------- |
| `TEXTURE_FORMAT_RGB`              | nessuna        | Colore a 3 canali. Il canale alfa viene scartato |
| `TEXTURE_FORMAT_RGBA`             | nessuna        | Colore a 3 canali e canale alfa completo.    |
| `TEXTURE_FORMAT_RGB_16BPP`        | nessuna        | Colore a 3 canali. 5+6+5 bit. |
| `TEXTURE_FORMAT_RGBA_16BPP`       | nessuna        | Colore a 3 canali e canale alfa completo. 4+4+4+4 bit. |
| `TEXTURE_FORMAT_LUMINANCE`        | nessuna        | Scala di grigi a 1 canale, senza alfa. I canali RGB vengono moltiplicati per ottenere un unico canale. Il canale alfa viene scartato. |
| `TEXTURE_FORMAT_LUMINANCE_ALPHA`  | nessuna        | Scala di grigi a 1 canale e canale alfa completo. I canali RGB vengono moltiplicati per ottenere un unico canale. |

Per ASTC, il numero di canali è sempre 4 (RGB + alfa) e il formato stesso definisce le dimensioni del blocco di compressione.
Nota che questi formati sono compatibili soltanto con un compressore ASTC: qualsiasi altra combinazione produrrà un errore di build.

`TEXTURE_FORMAT_RGBA_ASTC_4X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X5`
`TEXTURE_FORMAT_RGBA_ASTC_8X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X5`
`TEXTURE_FORMAT_RGBA_ASTC_10X6`
`TEXTURE_FORMAT_RGBA_ASTC_10X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X12`


## Compressori {#compressors}

I seguenti compressori di texture sono supportati per impostazione predefinita. I dati vengono decompressi quando il file della texture viene caricato in memoria.

| Nome                              | Formati                   | Nota                                                                                          |
| --------------------------------- | ------------------------- | --------------------------------------------------------------------------------------------- |
| `Uncompressed`                    | Tutti i formati               | Non viene applicata alcuna compressione. Impostazione predefinita.                                                      |
| `BasisU`                          | Tutti i formati RGB/RGBA      | Compressione Basis Universal di alta qualità, con perdita di dati. Un livello di qualità inferiore produce dimensioni minori. |
| `ASTC`                            | Tutti i formati ASTC          | Compressione ASTC con perdita di dati. Un livello di qualità inferiore produce dimensioni minori.                          |

::: sidenote
Defold supporta compressori installabili nella pipeline di compressione delle texture. Ciò consente di implementare in un'estensione un algoritmo di compressione delle texture, come WEBP o un algoritmo completamente personalizzato.
:::

## Immagine di esempio {#example-image}

Per comprendere meglio il risultato, ecco un esempio.
Nota che la qualità dell'immagine, il tempo di compressione e le dimensioni dopo la compressione dipendono sempre dall'immagine di partenza e possono variare.

Immagine di partenza (1024x512):
![Nuovo file di profili](images/texture_profiles/kodim03_pow2.png)

### Tempi di compressione {#compression-times}

| Preimpostazione | Tempo di compressione | Tempo relativo |
| --------- | ---------------- | ------------- |
| `LOW`     | 0m0.143s         | 0.5x            |
| `MEDIUM`  | 0m0.294s         | 1.0x            |
| `HIGH`    | 0m1.764s         | 6.0x            |
| `HIGHEST` | 0m1.109s         | 3.8x            |

### Perdita di segnale {#signal-loss}

Il confronto viene eseguito con lo strumento `basisu` (misurando il PSNR)
100 dB significa che non c'è alcuna perdita di segnale (cioè l'immagine è identica all'originale).

| Preimpostazione | Segnale                                           |
| --------- | ------------------------------------------------ |
| `LOW`     | Max:  34 Mean: 0.470 RMS: 1.088 PSNR: 47.399 dB |
| `MEDIUM`  | Max:  35 Mean: 0.439 RMS: 1.061 PSNR: 47.620 dB |
| `HIGH`    | Max:  37 Mean: 0.898 RMS: 1.606 PSNR: 44.018 dB |
| `HIGHEST` | Max:  51 Mean: 1.298 RMS: 2.478 PSNR: 40.249 dB |

### Dimensioni dei file compressi {#compression-file-sizes}

Le dimensioni del file originale sono 1572882 byte.

| Preimpostazione | Dimensioni dei file | Rapporto |
| --------- | ---------- | ------- |
| `LOW`     | 357225     | 22.71 %  |
| `MEDIUM`  | 365548     | 23.24 %  |
| `HIGH`    | 277186     | 17.62 %  |
| `HIGHEST` | 254380     | 16.17 %  |


### Qualità delle immagini {#image-quality}

Ecco le immagini risultanti (ottenute dalla codifica ASTC tramite lo strumento `basisu`)

`LOW`
![preimpostazione di compressione bassa](images/texture_profiles/kodim03_pow2.fast.png)

`MEDIUM`
![preimpostazione di compressione media](images/texture_profiles/kodim03_pow2.normal.png)

`HIGH`
![preimpostazione di compressione alta](images/texture_profiles/kodim03_pow2.high.png)

`HIGHEST`
![preimpostazione di compressione migliore](images/texture_profiles/kodim03_pow2.best.png)
