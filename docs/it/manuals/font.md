---
title: Manuale dei font in Defold
brief: Questo manuale descrive come Defold gestisce i font e come visualizzarli sullo schermo nei tuoi giochi.
---

# File dei font {#font-files}

I font vengono usati per visualizzare il testo nei componenti Label e nei nodi di testo GUI. Defold supporta diversi formati di file di font:

- TrueType
- OpenType
- BMFont

Da Defold 1.13.2, sia il motore di layout del testo precedente sia quello completo supportano i contorni TrueType e OpenType CFF1/CFF2, inclusa la generazione a runtime da risorse `.ttf` e `.otf`.

Per informazioni su come applicare stili a singole porzioni di testo e usare link e sprite in linea, consulta il [manuale del markup del testo formattato](/manuals/font-richtext).

I font aggiunti al progetto vengono convertiti automaticamente in un formato di texture che Defold può renderizzare. Sono disponibili due tecniche di rendering dei font, ciascuna con vantaggi e svantaggi specifici:

- Bitmap
- Campo di distanza

## Font offline o a runtime {#offline-or-runtime-fonts}

Per impostazione predefinita, la conversione in immagini rasterizzate dei glifi avviene durante la build (offline). Lo svantaggio è che ogni font deve rasterizzare tutti i possibili glifi in fase di build, producendo texture potenzialmente molto grandi che consumano memoria e aumentano anche le dimensioni del bundle.

Usando i "font a runtime", i font `.ttf` e `.otf` vengono inclusi nel bundle così come sono e la rasterizzazione avviene su richiesta durante l'esecuzione. Questo riduce al minimo sia l'utilizzo della memoria a runtime sia le dimensioni del bundle.

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

![Nuovo font](images/font/new_font.png)

Trascina il font che vuoi usare nel browser *Assets* e rilascialo in una posizione adatta.

Imposta la proprietà *Font* sul file del font e configura le proprietà del font secondo le tue esigenze.

## Proprietà {#properties}

*Font*
: Il file TTF, OTF o *`.fnt`* da usare per generare i dati del font.

*Material*
: Il materiale da usare per il rendering di questo font. Assicurati di cambiarlo per i font a campo di distanza e i BMFont (vedi sotto per i dettagli).

*Output Format*
: Il tipo di dati del font da generare.

  - `TYPE_BITMAP` converte il file OTF o TTF importato in una texture contenente i glifi del font, i cui dati bitmap vengono usati per visualizzare i nodi di testo. I canali di colore vengono usati per codificare la forma del carattere, il contorno e l'ombra esterna. Per i file *`.fnt`*, la bitmap della texture sorgente viene usata così com'è.
  - `TYPE_DISTANCE_FIELD` Il font importato viene convertito in una texture contenente i glifi del font, in cui i dati dei pixel rappresentano le distanze dal bordo del font anziché i pixel dello schermo. Vedi sotto per i dettagli.

*Render Mode*
: La modalità di rendering da usare per i glifi.

  - `MODE_SINGLE_LAYER` produce un singolo quadrilatero per ogni carattere.
  - `MODE_MULTI_LAYER` produce quadrilateri separati rispettivamente per la forma del glifo, il contorno e le ombre. I livelli vengono renderizzati dal più lontano al più vicino, impedendo a un carattere di coprire quelli già renderizzati se il contorno è più largo della distanza tra i glifi. Questa modalità di rendering consente anche di spostare correttamente l'ombra esterna, come specificato dalle proprietà Shadow X/Y nella risorsa del font.

*Size*
: La dimensione di destinazione dei glifi in pixel.

*Antialias*
: Indica se applicare l'antialiasing al font quando viene rasterizzato nella bitmap di destinazione. Imposta il valore su 0 se vuoi un rendering del font preciso al pixel.

*Alpha*
: La trasparenza del glifo. 0.0--1.0, dove 0.0 significa trasparente e 1.0 opaco.

*Outline Alpha*
: La trasparenza del contorno generato. 0.0--1.0.

*Outline Width*
: La larghezza del contorno generato in pixel. Imposta il valore su 0 per non avere un contorno.

*Shadow Alpha*
: La trasparenza dell'ombra generata. 0.0--1.0.

::: sidenote
Il supporto per le ombre è abilitato dagli shader dei materiali dei font integrati e gestisce le modalità di rendering sia a un livello sia a più livelli. Se non ti servono il rendering dei font a livelli o il supporto per le ombre, è preferibile usare uno shader più semplice, come *`builtins/font-singlelayer.fp`*.
:::

*Shadow Blur*
: Per i font bitmap, questa impostazione indica quante volte viene applicato un piccolo kernel di sfocatura a ogni glifo del font. Per i font a campo di distanza, questa impostazione equivale alla larghezza effettiva della sfocatura in pixel.

*Shadow X/Y*
: Lo scostamento orizzontale e verticale in pixel dell'ombra generata. Questa impostazione influisce sull'ombra del glifo solo quando Render Mode è impostato su `MODE_MULTI_LAYER`.

*Characters*
: I caratteri da includere nel font. Per impostazione predefinita, questo campo include i caratteri ASCII stampabili (codici dei caratteri 32-126). Puoi aggiungere o rimuovere caratteri da questo campo per includerne di più o di meno nel font.

Per i font a runtime, questo testo serve a precaricare nella cache i glifi corretti. Questo avviene durante il caricamento. Consulta `font.prewarm_text()`.

::: sidenote
I caratteri ASCII stampabili sono:
spazio ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Se selezioni questa proprietà, tutti i glifi disponibili nel file sorgente vengono inclusi nell'output.

*Cache Width/Height*
: Limita le dimensioni della bitmap della cache dei glifi. Quando il motore visualizza il testo, cerca il glifo nella bitmap della cache. Se non è presente, viene aggiunto alla cache prima del rendering. Se la bitmap della cache è troppo piccola per contenere tutti i glifi che il motore deve visualizzare, viene segnalato un errore (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Se il valore è impostato su 0, le dimensioni della cache vengono impostate automaticamente e possono crescere fino a un massimo di 2048x4096.

## Font a campo di distanza {#distance-field-fonts}

I font a campo di distanza memorizzano nella texture la distanza dal bordo del glifo invece dei dati bitmap. Quando il motore renderizza il font, è necessario uno shader speciale per interpretare i dati delle distanze e usarli per disegnare il glifo. I font a campo di distanza richiedono più risorse dei font bitmap, ma offrono una maggiore flessibilità nel ridimensionamento.

![Font a campo di distanza](images/font/df_font.png)

Quando crei il font, assicurati di impostare la proprietà *Material* su *`builtins/fonts/font-df.material`* (o su un altro materiale in grado di gestire i dati del campo di distanza)---altrimenti il font non userà lo shader corretto quando verrà visualizzato sullo schermo.

## Font bitmap BMFont {#bitmap-bmfonts}

Oltre alle bitmap generate, Defold supporta i font bitmap prerasterizzati nel formato "BMFont". Questi font sono costituiti da un'immagine PNG contenente tutti i glifi. Inoltre, un file *`.fnt`* contiene informazioni sulla posizione di ciascun glifo nell'immagine, sulle dimensioni e sulla crenatura. (Tieni presente che Defold non supporta la versione XML del formato *`.fnt`* usata da Phaser e da altri strumenti)

Questi tipi di font non offrono miglioramenti delle prestazioni rispetto ai font bitmap generati da file di font TrueType o OpenType, ma possono includere grafica arbitraria, colori e ombre direttamente nell'immagine.

Aggiungi i file *`.fnt`* e *`.png`* generati al tuo progetto Defold. Questi file devono trovarsi nella stessa cartella. Crea un nuovo file del font e imposta la proprietà *font* sul file *`.fnt`*. Assicurati che *output_format* sia impostato su `TYPE_BITMAP`. Defold non genererà una bitmap, ma userà quella fornita nel PNG.

::: sidenote
Per creare un BMFont, devi usare uno strumento in grado di generare i file appropriati. Sono disponibili diverse opzioni:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), uno strumento fornito da AngelCode e disponibile solo per Windows.
* [Shoebox](http://renderhjs.net/shoebox/), un'applicazione gratuita basata su Adobe Air per Windows e macOS.
* [Hiero](https://libgdx.com/wiki/tools/hiero), uno strumento open source basato su Java.
* [Glyph Designer](https://71squared.com/glyphdesigner), uno strumento commerciale per macOS di 71 Squared.
* [bmGlyph](https://www.bmglyph.com), uno strumento commerciale per macOS di Sovapps.
:::

![BMfont](images/font/bm_font.png)

Per visualizzare correttamente il font, ricorda di impostare la proprietà del materiale su *`builtins/fonts/font-fnt.material`* quando crei il font.

## Artefatti e buone pratiche {#artifacts-and-best-practices}

In generale, i font bitmap sono la scelta migliore quando il font viene visualizzato senza ridimensionamento. Il loro rendering sullo schermo è più veloce rispetto a quello dei font a campo di distanza.

I font a campo di distanza si prestano molto bene all'ingrandimento. I font bitmap, invece, essendo semplici immagini composte da pixel, aumentano di dimensioni ingrandendo anche i pixel, con conseguenti artefatti a blocchi. L'esempio seguente mostra un font di 48 pixel ingrandito di 4 volte.

![Font ingranditi](images/font/scale_up.png)

Quando si riducono le dimensioni, la GPU può ridimensionare le texture bitmap e applicare l'antialiasing in modo efficiente e con buoni risultati. Un font bitmap mantiene il colore meglio di un font a campo di distanza. Ecco un dettaglio ingrandito dello stesso font di esempio di 48 pixel, ridotto a 1/5 delle dimensioni:

![Font ridotti](images/font/scale_down.png)

I font a campo di distanza devono essere renderizzati a una dimensione di destinazione abbastanza grande da contenere informazioni sulle distanze in grado di rappresentare le curve dei glifi. Questo è lo stesso font mostrato sopra, ma con una dimensione di 18 pixel e ingrandito di 10 volte. È evidente che questa dimensione è troppo piccola per codificare le forme di questo carattere tipografico:

![Artefatti del campo di distanza](images/font/df_artifacts.png)

Se non ti serve il supporto per ombre o contorni, imposta a zero i rispettivi valori alfa. Altrimenti, i dati delle ombre e dei contorni verranno comunque generati, occupando memoria inutilmente.

## Cache del font {#font-cache}
Una risorsa font in Defold produce due elementi durante l'esecuzione: una texture e i dati del font.

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

È possibile usare la generazione a runtime per i font di tipo SDF quando si usano font TrueType (`.ttf`) o OpenType (`.otf`). La generazione a runtime da risorse `.otf` è supportata da Defold 1.13.2.
Questo approccio può ridurre notevolmente le dimensioni del download e il consumo di memoria a runtime di un gioco Defold.
Il piccolo svantaggio è la natura asincrona della generazione di ciascun glifo.

* Abilita la funzionalità impostando `font.runtime_generation` in game.project.

* Aggiungi un [manifesto dell'applicazione](/manuals/app-manifest) e abilita l'opzione `Use full text layout system`.
Questo genera un motore personalizzato con questa funzionalità abilitata.

::: sidenote
Questa funzionalità è attualmente sperimentale, ma l'intenzione è di usarla come flusso di lavoro predefinito in futuro.
:::

::: important
L'impostazione `font.runtime_generation` influisce su tutti i font `.ttf` e `.otf` del progetto.
:::


### Usare i font negli script {#font-scripting}

#### Precaricare la cache dei glifi {#prewarming-glyph-cache}

Per semplificare l'uso dei font a runtime, è supportato il precaricamento della cache dei glifi.
Questo significa che il font genera i glifi elencati nella sua proprietà *Characters*.

::: sidenote
Se `All Chars` è selezionato, non viene eseguito alcun precaricamento, perché questo vanificherebbe lo scopo di non dover generare tutti i glifi contemporaneamente.
:::

Se il campo `Characters` del file `.fontc` è impostato, viene usato come testo per determinare quali glifi devono essere aggiornati nella cache dei glifi.

È anche possibile aggiornare manualmente la cache dei glifi chiamando `font.prewarm_text(font_collection, text, callback)`. La funzione fornisce una callback che ti avvisa quando tutti i glifi mancanti sono stati aggiunti alla cache dei glifi ed è possibile visualizzare il testo sullo schermo.

### Aggiungere e rimuovere font da una collezione di font {#addingremoving-fonts-to-a-font-collection}

Per i font a runtime, è possibile aggiungere font (`.ttf`) a una collezione di font o rimuoverli.
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
