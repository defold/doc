---
title: Manuale dei font in Defold
brief: Questo manuale descrive come Defold gestisce i font e come visualizzarli sullo schermo nei tuoi giochi.
---

# File dei font {#font-files}

I font vengono usati per visualizzare il testo nei componenti Label e nei nodi di testo GUI. Defold supporta diversi formati di file di font:

- TrueType
- OpenType
- BMFont

Sia il motore di layout del testo precedente sia quello completo supportano i contorni TrueType e i contorni OpenType CFF1/CFF2, compresa la generazione a runtime da risorse `.ttf` e `.otf`.

Per informazioni su come applicare stili a singole porzioni di testo e usare link e sprite in linea, consulta il [manuale del markup del testo formattato](/manuals/font-richtext).

Per i font TrueType e OpenType, la proprietà *Mode* seleziona il modo in cui vengono renderizzati i glifi:

- **Bitmap** usa immagini rasterizzate dei glifi.
- **SDF** (campo di distanza con segno) memorizza in una texture le distanze dai bordi dei glifi, consentendo un ridimensionamento più flessibile rispetto a Bitmap.
- **Vector** renderizza le forme dei glifi a partire dai dati delle curve, mantenendole nitide quando vengono ridimensionate. Gli effetti di contorno e ombra continuano a usare dati bitmap.

Le nuove risorse font usano la modalità **Vector** e la generazione dei glifi **Dynamic**. Le risorse font esistenti conservano la modalità Bitmap o SDF. Le sorgenti BMFont usano sempre la bitmap fornita.

La modalità Vector richiede il supporto grafico per le texture `RGBA16F` e `R32UI` e non è supportata su OpenGL ES 2 o WebGL 1. Per gli adattatori grafici non supportati, usa font Bitmap o SDF e i materiali corrispondenti; non esiste un ripiego automatico da Vector a SDF. Consulta [Font vettoriali](#vector-fonts) per la configurazione.

## Font offline o a runtime {#offline-or-runtime-fonts}

La proprietà *Glyph Generation* seleziona quando vengono generati i dati dei glifi di ogni font:

- **Static** genera i glifi selezionati durante la build (offline). *Characters* e *All Chars* controllano quali glifi vengono inclusi. Il file sorgente `.ttf` o `.otf` non viene incluso nel bundle per la generazione a runtime.
- **Dynamic** include nel bundle il file sorgente `.ttf` o `.otf` e genera i glifi su richiesta a runtime. *Prewarm Text* prepara i glifi quando il font viene caricato. Altri glifi possono essere generati in seguito quando necessario.

I font SDF e Vector supportano entrambe le opzioni. I font Bitmap e le sorgenti BMFont usano la generazione Static. Ogni risorsa font viene configurata indipendentemente, quindi un progetto può combinare font Static e Dynamic.

La generazione Dynamic può ridurre le dimensioni del bundle e l'uso di memoria a runtime, soprattutto per i font con insiemi di caratteri estesi. Richiede il sistema completo di layout del testo nel motore; consulta [Abilitazione dei font a runtime](#enabling-runtime-fonts).

## Supporto per il layout del testo (ad esempio da destra a sinistra) {#text-layout-support-eg-right-to-left}

I font a runtime hanno anche il vantaggio di supportare il layout completo del testo, ad esempio da destra a sinistra.
Attualmente usiamo le librerie [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak) e [SkriBidi](https://github.com/memononen/Skribidi).

Consulta [Abilitare i font a runtime](/manuals/font#enabling-runtime-fonts)

L'editor usa il renderer dei font del motore per le anteprime dei font e del testo nelle scene. La composizione dei glifi e il layout da destra a sinistra richiedono i [font a runtime](#enabling-runtime-fonts) e l'opzione **Use full text layout system** nell'App Manifest. Per i font offline, l'anteprima rispetta le impostazioni **Characters** e **All Chars** del font.

## Collezione di font {#font-collection}

Il formato di file `.fontc` è noto anche come collezione di font. In modalità offline, a esso è associato un solo font.
Quando usi i font a runtime, puoi associare più file di font (`.ttf` o `.otf`) alla collezione di font.

Questo consente di usare una collezione di font per visualizzare più testi in lingue diverse, mantenendo al contempo un basso consumo di memoria.
Ad esempio, puoi caricare una collezione con il font giapponese, associare quel font al font principale attuale e infine scaricare dalla memoria la collezione di font giapponese.

## Creare un font {#creating-a-font}

Per creare un font da usare in Defold, crea un nuovo file Font selezionando <kbd>File ▸ New...</kbd> dal menu, quindi seleziona <kbd>Font</kbd>. Puoi anche <kbd>fare clic con il pulsante destro</kbd> su una posizione nel browser *Assets* e selezionare <kbd>New... ▸ Font</kbd>.

![Nome del nuovo font](images/font/new_font_name.png)

Assegna un nome al nuovo file del font e fai clic su <kbd>Ok</kbd>. Il nuovo file del font si apre nell'editor.

Trascina il font che vuoi usare nel browser *Assets* e rilascialo in una posizione adatta.

Imposta la proprietà *Font* sul file del font. Per una sorgente `.ttf` o `.otf`, seleziona *Mode* e *Glyph Generation*, quindi configura le altre proprietà secondo necessità. Per la generazione Dynamic, completa anche la [configurazione dei font a runtime](#enabling-runtime-fonts).

![Proprietà del font con modalità Vector e generazione dei glifi Dynamic](images/font/font_properties.png)

Per i font Vector, usa *Font Size* su un componente Label o un nodo di testo GUI per cambiare le dimensioni del testo visualizzato. *Outline/Shadow Bitmap Size* controlla la risoluzione delle bitmap degli effetti indipendentemente dalle dimensioni del testo visualizzato.

Per i font Bitmap e SDF, imposta *Size* nella risorsa font per scegliere le dimensioni dei glifi generati. Le dimensioni dei BMFont provengono dal file sorgente `.fnt`. Per cambiare le dimensioni visualizzate di questi font, ridimensiona il componente Label o il nodo di testo GUI.

## Proprietà {#properties}

*Font*
: Il file TTF, OTF o *`.fnt`* da usare per generare i dati del font.

*Material*
: Il materiale da usare per renderizzare questo font. Deve corrispondere alla modalità del font; consulta [Materiali dei font](#font-materials).

*Mode*
: La tecnica di rendering per una sorgente `.ttf` o `.otf`: **Bitmap**, **SDF** o **Vector**. Sostituisce la precedente proprietà *Output Format*. La proprietà non viene mostrata per le sorgenti BMFont.

*Glyph Generation*
: **Static** genera i dati dei glifi durante la build. **Dynamic** li genera a runtime e richiede il [sistema completo di layout del testo](#enabling-runtime-fonts). Questa proprietà è disponibile per i font SDF e Vector. In modalità Bitmap è fissata a Static e non viene mostrata per le sorgenti BMFont.

*Render Mode*
: La disposizione dei livelli per i font Bitmap generati. Questa proprietà viene mostrata soltanto in modalità Bitmap per le sorgenti `.ttf` e `.otf`. Per le sorgenti SDF, Vector e BMFont, Defold seleziona automaticamente la disposizione dei livelli.

  - **Single Layer** produce un singolo quadrilatero per ogni carattere.
  - **Multi Layer** produce quadrilateri separati per la forma del glifo, il contorno e l'ombra. I livelli vengono renderizzati da dietro in avanti, evitando che un carattere copra quelli già renderizzati quando il contorno è più largo della distanza tra i glifi. Ciò abilita anche gli spostamenti dell'ombra tramite le proprietà *Shadow X/Y*.

*Size*
: Le dimensioni dei glifi in pixel usate per generare i dati dei font Bitmap o SDF. Per le sorgenti BMFont, le dimensioni vengono lette dal file `.fnt` e non possono essere modificate qui.

*Outline/Shadow Bitmap Size*
: In modalità Vector sostituisce *Size*. Controlla la risoluzione bitmap degli effetti di contorno e ombra abilitati, sia per la generazione Static sia per quella Dynamic. È disabilitata quando nessuno dei due effetti è abilitato, perché le forme dei glifi usano dati di curve. Modificare *Font Size* di un componente Label o di un nodo di testo GUI non cambia questa risoluzione bitmap condivisa.

*Antialias*
: Indica se applicare l'antialiasing ai glifi durante la generazione dei dati del font Bitmap. Disabilitalo per un rendering pixel perfect. Questa proprietà viene mostrata soltanto in modalità Bitmap per le sorgenti `.ttf` e `.otf`.

*Alpha*
: La trasparenza del glifo. 0.0--1.0, dove 0.0 significa trasparente e 1.0 opaco.

*Outline Alpha*
: La trasparenza del contorno generato. 0.0--1.0.

*Outline Width*
: La larghezza del contorno generato in pixel. Imposta il valore su 0 per non avere un contorno.

*Shadow Alpha*
: La trasparenza dell'ombra generata. 0.0--1.0.

::: sidenote
Lo shader integrato dei font Bitmap supporta le ombre sia nella modalità di rendering *Single Layer* sia in *Multi Layer*. Per i font Bitmap generati che usano il rendering *Single Layer* e non richiedono ombre, un materiale personalizzato può usare `/builtins/fonts/font-singlelayer.fp`. I font SDF e Vector richiedono shader corrispondenti alla propria modalità; consulta [Materiali dei font](#font-materials).
:::

*Shadow Blur*
: La quantità di sfocatura applicata all'ombra generata. Imposta a 0 per un'ombra nitida.

*Shadow X/Y*
: Lo spostamento orizzontale e verticale in pixel dell'ombra generata. Per i font Bitmap generati, usa la modalità di rendering *Multi Layer* per applicare questi spostamenti. Defold seleziona automaticamente i livelli appropriati per i font SDF e Vector.

*Characters*
: Per la generazione Static, i caratteri da includere nel font compilato. Per impostazione predefinita questo campo contiene i caratteri ASCII stampabili (codici carattere 32-126). Aggiungi o rimuovi caratteri per controllare quali glifi sono disponibili a runtime.

*Prewarm Text*
: Per la generazione Dynamic sostituisce *Characters*. Il testo viene usato per generare i glifi e preriscaldare la cache quando il font viene caricato. Non limita i caratteri che possono essere generati in seguito. Puoi anche preriscaldare il testo da uno script con [`font.prewarm_text()`](/ref/font/#font.prewarm_text).

::: sidenote
I caratteri ASCII stampabili sono:
spazio ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Per la generazione Static, include ogni glifo disponibile nella sorgente invece di limitare il font a *Characters*. Questa proprietà è nascosta per i font Dynamic.

*Cache Width/Height*
: Limita le dimensioni della bitmap della cache dei glifi usata dai font Bitmap e SDF e dagli effetti di contorno e ombra Vector. Quando il motore renderizza il testo, cerca il glifo nella bitmap della cache. Se non è presente, viene aggiunto alla cache prima del rendering. Se la bitmap è troppo piccola per contenere tutti i glifi che il motore deve renderizzare, viene segnalato un errore (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Se il valore è impostato su 0, le dimensioni della cache vengono impostate automaticamente e possono crescere fino a un massimo di 2048x4096.

## Materiali dei font {#font-materials}

Usa un materiale corrispondente alla modalità del font. La proprietà *Material* della risorsa font viene usata dai nodi di testo GUI. I componenti Label hanno una proprietà *Material* separata che deve anch'essa corrispondere al font:

| Modalità o sorgente del font | Materiale del font per il testo GUI | Materiale del componente Label |
| --- | --- | --- |
| Bitmap | `/builtins/fonts/font.material` | `/builtins/fonts/label.material` |
| SDF | `/builtins/fonts/font-df.material` | `/builtins/fonts/label-df.material` |
| Vector | `/builtins/fonts/font-vector.material` | `/builtins/fonts/label-vector.material` |
| BMFont (`.fnt`) | `/builtins/fonts/font-fnt.material` | `/builtins/fonts/label-fnt.material` |

Cambiare *Mode* nell'editor dei font seleziona il materiale integrato Bitmap, SDF o Vector corrispondente quando uno di questi materiali è già assegnato al font. I materiali personalizzati non vengono sostituiti automaticamente. Controlla anche la proprietà *Material* dei componenti Label che usano il font.

## Font vettoriali {#vector-fonts}

I font vettoriali renderizzano le forme dei glifi a partire dalle curve, mantenendole nitide al variare delle dimensioni del testo visualizzato. Per configurare un font che genera i propri glifi a runtime:

1. Crea una risorsa `.font`, per esempio `/fonts/ui.font`, e seleziona una sorgente TrueType o OpenType nella proprietà *Font*. Il font integrato `/builtins/fonts/vera_mo_bd.ttf` può essere usato per il testo ordinario.
2. Imposta *Mode* su **Vector**, *Glyph Generation* su **Dynamic** e *Material* su `/builtins/fonts/font-vector.material`. Sono i valori predefiniti delle nuove risorse font.
3. Abilita **Use full text layout system** in un App Manifest assegnato al progetto. Segui [Abilitazione dei font a runtime](#enabling-runtime-fonts) per configurare il motore personalizzato.
4. Abilita [Shader ▸ Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) in *game.project*.
5. Assegna il font a un componente [Label](/manuals/label/) oppure aggiungilo a *Fonts* di una scena GUI e selezionalo su un [nodo di testo](/manuals/gui-text/). Per un Label, imposta anche *Material* del componente su `/builtins/fonts/label-vector.material`. Imposta *Font Size* del componente o nodo sulle dimensioni di visualizzazione desiderate.

Le forme dei glifi Vector usano texture di curve, ma i contorni e le ombre abilitati continuano a generare dati bitmap SDF e consumano memoria delle texture della cache dei glifi. *Outline/Shadow Bitmap Size* imposta tale risoluzione bitmap indipendentemente da *Font Size* del Label o del nodo di testo GUI. Imposta *Outline Alpha* e *Shadow Alpha* a `0` quando questi effetti non servono, per evitarne la generazione dei dati bitmap.

### Emoji a colori {#color-emoji}

I font vettoriali possono renderizzare emoji a colori COLRv1, compresi i colori della palette e i gradienti lineari e radiali. Le modalità Bitmap e SDF non renderizzano i colori COLRv1. Usa la configurazione Dynamic Vector precedente, quindi aggiungi un font emoji COLRv1 come ripiego alla collezione di font. Il testo ordinario continua a usare il font originale.

Per esempio, copia il [font Noto Color Emoji](https://github.com/google/fonts/blob/main/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf) COLRv1 nel progetto come `/fonts/NotoColorEmoji-Regular.ttf`. Scegli la versione COLRv1: altri font emoji potrebbero usare un formato colore diverso anche se il nome del file termina con `.ttf`.

Aggiungi `/fonts/NotoColorEmoji-Regular.ttf` a **Project ▸ Custom Resources** in *game.project*. Se non ci sono altre risorse personalizzate, l'impostazione è:

```ini
[project]
custom_resources = /fonts/NotoColorEmoji-Regular.ttf
```

Scrivere il percorso di un font in Lua non include il file del font nel bundle. [Custom Resources](/manuals/project-settings/#custom-resources) rende questo font sorgente disponibile a [`font.add_font()`](/ref/font/#font.add_font), che lo carica tramite il sistema delle risorse. Passa il percorso stringa del font sorgente quando lo carichi dal bundle.

Aggiungi il font di ripiego una sola volta per ogni risorsa font condivisa. La modifica interessa tutti i Label e i nodi di testo GUI che usano quel font e aggiungere due volte lo stesso ripiego genera un errore. Se usi sia l'[esempio Label](/manuals/label/#vector-fonts-and-color-emoji) sia l'[esempio GUI](/manuals/gui-text/#vector-fonts-and-color-emoji) con lo stesso `.font`, coordina l'inizializzazione in modo da aggiungere il ripiego una sola volta, prima che uno dei due esempi preriscaldi o visualizzi il testo. Gli esempi preriscaldano il testo completo dopo aver aggiunto il ripiego e lo mostrano quando il callback riesce.

## Font a campo di distanza {#distance-field-fonts}

I font a campo di distanza memorizzano nella texture la distanza dal bordo del glifo invece dei dati bitmap. Quando il motore renderizza il font, è necessario uno shader speciale per interpretare i dati delle distanze e usarli per disegnare il glifo. I font a campo di distanza richiedono più risorse dei font bitmap, ma offrono una maggiore flessibilità nel ridimensionamento.

![Font a campo di distanza](images/font/df_font.png)

Seleziona **SDF** in *Mode* e scegli **Static** o **Dynamic** in *Glyph Generation*. Usa *`/builtins/fonts/font-df.material`* per il font e *`/builtins/fonts/label-df.material`* per i componenti Label oppure materiali personalizzati che gestiscano i dati dei campi di distanza.

## Font bitmap BMFont {#bitmap-bmfonts}

Oltre alle bitmap generate, Defold supporta i font bitmap prerasterizzati nel formato "BMFont". Questi font sono costituiti da un'immagine PNG contenente tutti i glifi. Inoltre, un file *`.fnt`* contiene informazioni sulla posizione di ciascun glifo nell'immagine, sulle dimensioni e sulla crenatura. (Tieni presente che Defold non supporta la versione XML del formato *`.fnt`* usata da Phaser e da altri strumenti)

Questi tipi di font non offrono miglioramenti delle prestazioni rispetto ai font bitmap generati da file di font TrueType o OpenType, ma possono includere grafica arbitraria, colori e ombre direttamente nell'immagine.

Aggiungi al progetto Defold i file *`.fnt`* e *`.png`* generati. Questi file devono risiedere nella stessa cartella. Crea un nuovo file font e imposta la proprietà *Font* sul file *`.fnt`*. Defold usa la bitmap fornita e ne legge le dimensioni dal file `.fnt`. *Mode* e *Glyph Generation* non vengono mostrati per le sorgenti BMFont.

::: sidenote
Per creare un BMFont, devi usare uno strumento in grado di generare i file appropriati. Sono disponibili diverse opzioni:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), uno strumento fornito da AngelCode e disponibile solo per Windows.
* [Shoebox](http://renderhjs.net/shoebox/), un'applicazione gratuita basata su Adobe Air per Windows e macOS.
* [Hiero](https://libgdx.com/wiki/tools/hiero), uno strumento open source basato su Java.
* [Glyph Designer](https://71squared.com/glyphdesigner), uno strumento commerciale per macOS di 71 Squared.
* [bmGlyph](https://www.bmglyph.com), uno strumento commerciale per macOS di Sovapps.
:::

![BMfont](images/font/bm_font.png)

Imposta *Material* del font su *`/builtins/fonts/font-fnt.material`*. Per i componenti Label, usa *`/builtins/fonts/label-fnt.material`*.

## Artefatti e buone pratiche {#artifacts-and-best-practices}

In generale, i font bitmap sono la scelta migliore quando il font viene visualizzato senza ridimensionamento. Il loro rendering sullo schermo è più veloce rispetto a quello dei font a campo di distanza.

I font a campo di distanza si prestano molto bene all'ingrandimento. I font bitmap, invece, essendo semplici immagini composte da pixel, aumentano di dimensioni ingrandendo anche i pixel, con conseguenti artefatti a blocchi. L'esempio seguente mostra un font di 48 pixel ingrandito di 4 volte.

![Font ingranditi](images/font/scale_up.png)

Quando si riducono le dimensioni, la GPU può ridimensionare le texture bitmap e applicare l'antialiasing in modo efficiente e con buoni risultati. Un font bitmap mantiene il colore meglio di un font a campo di distanza. Ecco un dettaglio ingrandito dello stesso font di esempio di 48 pixel, ridotto a 1/5 delle dimensioni:

![Font ridotti](images/font/scale_down.png)

I font a campo di distanza devono essere renderizzati a una dimensione di destinazione abbastanza grande da contenere informazioni sulle distanze in grado di rappresentare le curve dei glifi. Questo è lo stesso font mostrato sopra, ma con una dimensione di 18 pixel e ingrandito di 10 volte. È evidente che questa dimensione è troppo piccola per codificare le forme di questo carattere tipografico:

![Artefatti del campo di distanza](images/font/df_artifacts.png)

Se non vuoi il supporto per ombre o contorni, imposta a zero i rispettivi valori alpha. Altrimenti i dati di ombre e contorni verranno comunque generati, occupando memoria inutilmente. In modalità Vector, disabilitare entrambi gli effetti ne evita la generazione dei dati bitmap; le forme dei glifi continuano a usare dati di curve.

## Cache del font {#font-cache}
Le risorse font Bitmap e SDF usano a runtime una texture della cache dei glifi e dati dei font. I font Vector memorizzano le forme dei glifi come dati di curve e usano una cache bitmap per gli effetti di contorno e ombra abilitati. La disposizione della texture descritta di seguito si applica ai font Bitmap e SDF.

* I dati del font consistono in un elenco di voci relative ai glifi, ciascuna delle quali contiene alcune informazioni di base sulla crenatura e i dati bitmap del glifo.
* La texture viene chiamata internamente "texture della cache dei glifi" e viene usata per visualizzare il testo con un determinato font.

Durante l'esecuzione, quando visualizza il testo, il motore esamina prima i glifi da renderizzare per verificare quali sono disponibili nella cache della texture. Ogni glifo assente dalla cache della texture dei glifi attiva un caricamento nella texture a partire dai dati bitmap memorizzati nei dati del font.

Ogni glifo viene posizionato internamente nella cache in base alla linea di base del font, consentendo di calcolare in uno shader le coordinate locali della texture del glifo all'interno della cella corrispondente della cache. Questo significa che puoi ottenere dinamicamente alcuni effetti sul testo, come sfumature o sovrapposizioni di texture. Il motore espone allo shader le metriche della cache tramite una costante speciale dello shader chiamata `texture_size_recip`, che contiene le seguenti informazioni nei componenti del vettore:

* `texture_size_recip.x` è l'inverso della larghezza della cache
* `texture_size_recip.y` è l'inverso dell'altezza della cache
* `texture_size_recip.z` è il rapporto tra la larghezza della cella della cache e la larghezza della cache
* `texture_size_recip.w` è il rapporto tra l'altezza della cella della cache e l'altezza della cache

Ad esempio, per generare una sfumatura in un fragment shader, basta scrivere:

`float horizontal_gradient = fract(var_texcoord0.y / texture_size_recip.w);`

Per ulteriori informazioni sulle variabili uniform degli shader, consulta il [manuale degli shader](/manuals/shader).

## Abilitare i font a runtime {#enabling-runtime-fonts}

La generazione a runtime viene configurata per ogni risorsa font:

1. Apri la risorsa `.font` e seleziona una sorgente TrueType (`.ttf`) o OpenType (`.otf`).
2. Imposta *Mode* su **SDF** o **Vector** e *Glyph Generation* su **Dynamic**.
3. Scegli i [materiali corrispondenti per font e Label](#font-materials).
4. Aggiungi un [App Manifest](/manuals/app-manifest), assegnalo a *Native Extensions ▸ App Manifest* in *game.project* e abilita **Use full text layout system**. In questo modo viene creato un motore personalizzato con supporto per la generazione dei font a runtime e il layout completo del testo.
5. Imposta *Prewarm Text* sul testo da visualizzare poco dopo il caricamento del font. Per il testo necessario in seguito, usa [`font.prewarm_text()`](/ref/font/#font.prewarm_text) e attendi il suo callback prima di visualizzarlo.

Le nuove risorse font usano già la modalità Vector e la generazione Dynamic, ma richiedono comunque la configurazione dell'App Manifest descritta sopra.

### Usare i font negli script {#font-scripting}

#### Precaricare la cache dei glifi {#prewarming-glyph-cache}

I font Dynamic generano i glifi necessari a *Prewarm Text* quando il font viene caricato. Il campo viene interpretato come testo da impaginare, quindi la cache viene preparata per i glifi necessari al testo. *All Chars* non è disponibile per i font Dynamic.

Puoi anche chiamare `font.prewarm_text(font_collection, text, callback)` per un font Dynamic. Il callback indica quando tutti i glifi mancanti sono stati aggiunti alla cache ed è possibile visualizzare il testo. Questa funzione non può essere usata con i font Static.

### Aggiungere e rimuovere font da una collezione di font {#addingremoving-fonts-to-a-font-collection}

Per i font Dynamic è possibile aggiungere o rimuovere font sorgente (`.ttf` o `.otf`) da una collezione di font.
Questo è utile quando un font di grandi dimensioni è stato suddiviso in più file per diversi set di caratteri (ad esempio CJK)

::: important
Aggiungere un font a una collezione di font non carica né renderizza automaticamente tutti i glifi.
:::

```lua
function init(self)
    -- Get the target font collection.
    self.font_collection = go.get("#label", "font")

    -- Get the first font assigned to the selected language collection.
    local language_collection = go.get("localization_japanese#label", "font")
    local font_info = font.get_info(language_collection)
    self.language_ttf_hash = font_info.fonts[1].path_hash

    -- Associate it with the target collection and increase its reference count.
    font.add_font(self.font_collection, self.language_ttf_hash)
end
```

```lua
function final(self)
    -- Remove the association and release the font reference.
    font.remove_font(self.font_collection, self.language_ttf_hash)
end
```

### Precaricare i glifi {#prewarming-glyphs}

Per visualizzare correttamente un testo con un font a runtime, è necessario determinare i glifi da usare. `font.prewarm_text()` lo fa per te.
Si tratta di un'operazione asincrona e, una volta completata e ricevuta la callback, è possibile procedere a visualizzare qualsiasi messaggio contenente quei glifi.

::: important
Se la cache dei glifi si riempie, il glifo più vecchio presente nella cache viene rimosso.
:::

```lua
font.prewarm_text(self.font_collection, info.text, function (self, request_id, result, err)
    if result then
      print("PREWARMING OK!")
      go.set(self.label, "text", info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
