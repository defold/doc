---
title: Tutorial sullo shader di correzione cromatica
brief: In questo tutorial creerai un effetto di post-elaborazione a schermo intero in Defold.
---

# Tutorial sulla correzione cromatica {#grading-tutorial}

In questo tutorial creeremo un effetto di post-elaborazione per la correzione cromatica (color grading) a schermo intero. Il metodo di rendering di base utilizzato si presta a molti tipi di effetti di post-elaborazione, come sfocature, scie, bagliori, regolazioni del colore e così via.

Si presuppone che tu sappia orientarti nell'editor Defold e che abbia una conoscenza di base degli shader GL e della pipeline di rendering di Defold. Se hai bisogno di approfondire questi argomenti, consulta [il nostro manuale sugli shader](/manuals/shader/) e il [manuale sul rendering](/manuals/render/).

## Destinazioni di rendering {#render-targets}

Con lo script di rendering predefinito, ogni componente visivo (sprite, tilemap, effetto particellare, GUI ecc.) viene renderizzato direttamente nel *frame buffer* della scheda grafica. L'hardware fa quindi apparire la grafica sullo schermo. Il disegno effettivo dei pixel di un componente viene eseguito da un *programma shader* GL. Defold include un programma shader predefinito per ogni tipo di componente, che disegna i dati dei pixel sullo schermo senza modificarli. Normalmente è il comportamento desiderato: le immagini devono apparire sullo schermo come sono state concepite in origine.

Puoi sostituire il programma shader di un componente con uno che modifichi i dati dei pixel o crei colori dei pixel completamente nuovi tramite codice. Il [tutorial su Shadertoy](/tutorials/shadertoy) ti insegna come fare.

Supponiamo ora che tu voglia renderizzare l'intero gioco in bianco e nero. Una possibile soluzione consiste nel modificare il programma shader di ogni tipo di componente, in modo che ciascuno shader desaturi i colori dei pixel. Attualmente Defold include 6 materiali integrati e 6 coppie di programmi vertex shader e fragment shader, quindi questo richiederà una discreta quantità di lavoro. Inoltre, ogni modifica successiva o aggiunta di effetti dovrà essere applicata a ciascun programma shader.

Un approccio molto più flessibile consiste nell'eseguire il rendering in due passaggi separati:

![Destinazione di rendering](images/grading/render_target.png)

1. Disegna tutti i componenti come di consueto, ma in un buffer fuori schermo anziché nel normale frame buffer. Per farlo, disegna in una cosiddetta *destinazione di rendering* (render target).
2. Disegna un poligono quadrato nel frame buffer e usa i dati dei pixel memorizzati nella destinazione di rendering come sorgente della texture del poligono. Assicurati inoltre che il poligono quadrato sia esteso fino a coprire l'intero schermo.

Con questo metodo possiamo leggere i dati visivi risultanti e modificarli prima che raggiungano lo schermo. Aggiungendo programmi shader al passaggio 2, possiamo ottenere facilmente effetti a schermo intero. Vediamo come configurare tutto questo in Defold.

## Configurare un renderer personalizzato {#setting-up-a-custom-renderer}

Dobbiamo modificare lo script di rendering integrato e aggiungere la nuova funzionalità di rendering. Lo script di rendering predefinito è un buon punto di partenza, quindi inizia copiandolo:

1. Copia */builtins/render/default.render_script*: nella vista *Asset*, fai clic con il pulsante destro su *default.render_script*, seleziona <kbd>Copy</kbd>, poi fai clic con il pulsante destro su *main* e seleziona <kbd>Paste</kbd>. Fai clic con il pulsante destro sulla copia, seleziona <kbd>Rename...</kbd> e assegnale un nome appropriato, come "grade.render_script".
2. Crea un nuovo file di rendering chiamato */main/grade.render* facendo clic con il pulsante destro su *main* nella vista *Asset* e selezionando <kbd>New ▸ Render</kbd>.
3. Apri *grade.render* e imposta la proprietà *Script* su "/main/grade.render_script".

   ![grade.render](images/grading/grade_render.png)

4. Apri *game.project* e imposta *Render* su "/main/grade.render".

   ![game.project](images/grading/game_project.png)

Ora il gioco è configurato per essere eseguito con una nuova pipeline di rendering che possiamo modificare. Per verificare che il motore utilizzi la nostra copia dello script di rendering, avvia il gioco, apporta allo script una modifica che produca un risultato visibile, quindi ricarica lo script. Per esempio, puoi disattivare il disegno di tile e sprite, poi premere <kbd>⌘ + R</kbd> per eseguire l'hot reload dello script di rendering "alterato" nel gioco in esecuzione:

```lua
...

render.set_projection(vmath.matrix4_orthographic(0, render.get_width(), 0, render.get_height(), -1, 1))

-- render.draw(self.tile_pred) -- <1>
render.draw(self.particle_pred)
render.draw_debug3d()

...
```
1. Commenta la riga che disegna il predicato "tile", che include tutti gli sprite e i tile. Questa riga di codice si trova intorno alla riga 33 del file dello script di rendering.

Se gli sprite e i tile scompaiono durante questo semplice test, hai la conferma che il gioco esegue il tuo script di rendering. Se tutto funziona come previsto, puoi annullare la modifica allo script.

## Disegnare in una destinazione fuori schermo {#drawing-to-an-off-screen-target}

Ora modifichiamo lo script di rendering in modo che disegni nella destinazione di rendering fuori schermo anziché nel frame buffer. Per prima cosa dobbiamo creare la destinazione di rendering:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})

    self.clear_color = vmath.vector4(0, 0, 0, 1)
    self.clear_color.x = sys.get_config_number("render.clear_color_red", 0)
    self.clear_color.y = sys.get_config_number("render.clear_color_green", 0)
    self.clear_color.z = sys.get_config_number("render.clear_color_blue", 0)
    self.clear_color.w = sys.get_config_number("render.clear_color_alpha", 1)

    self.view = vmath.matrix4()

    local color_params = { format = graphics.TEXTURE_FORMAT_RGBA,
                       width = render.get_width(),
                       height = render.get_height() } -- <1>
    local target_params = {[graphics.BUFFER_TYPE_COLOR0_BIT] = color_params }

    self.target = render.render_target("original", target_params) -- <2>
end
```
1. Imposta i parametri del buffer dei colori per la destinazione di rendering. Usiamo la risoluzione di destinazione del gioco.
2. Crea la destinazione di rendering con i parametri del buffer dei colori.

Ora dobbiamo soltanto racchiudere il codice di rendering originale tra chiamate a `render.set_render_target()`, in questo modo:

```lua
function update(self)
  render.set_render_target(self.target) -- <1>

  render.set_depth_mask(true)
  render.set_stencil_mask(0xff)
  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color, [graphics.BUFFER_TYPE_DEPTH_BIT] = 1, [graphics.BUFFER_TYPE_STENCIL_BIT] = 0})

  render.set_viewport(0, 0, render.get_width(), render.get_height()) -- <2>
  render.set_view(self.view)
  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT) -- <3>
end
```
1. Attiva la destinazione di rendering. Da questo momento, ogni chiamata a `render.draw()` disegnerà nei buffer della nostra destinazione di rendering fuori schermo.
2. Tutto il codice di disegno originale in `update()` rimane invariato, a parte il viewport, che viene impostato sulla risoluzione della destinazione di rendering.
3. A questo punto, tutta la grafica del gioco è stata disegnata nella destinazione di rendering. È quindi il momento di disattivarla, ripristinando la destinazione di rendering predefinita.

Non serve altro. Se esegui il gioco ora, disegnerà tutto nella destinazione di rendering. Ma poiché non disegniamo più nulla nel frame buffer, vedremo soltanto uno schermo nero.

## Qualcosa con cui riempire lo schermo {#something-to-fill-the-screen-with}

Per disegnare sullo schermo i pixel del buffer dei colori della destinazione di rendering, dobbiamo predisporre un elemento a cui applicare i dati dei pixel come texture. A questo scopo useremo un modello 3D piatto e quadrato.

1. Apri *`main.collection`* e crea un nuovo oggetto di gioco chiamato "`grade`".
2. Aggiungi un componente Model all'oggetto di gioco "`grade`".
3. Imposta la proprietà *Mesh* del componente modello sul file *`quad.gltf`* che si trova in `builtins/assets/meshes`.

Lascia l'oggetto di gioco all'origine, senza modificarne la scala. In seguito, quando renderizzeremo il quadrilatero, lo proietteremo in modo che riempia l'intero schermo. Prima, però, ci servono un materiale e dei programmi shader per il quadrilatero:

1. Crea un nuovo materiale e chiamalo *`grade.material`* facendo clic con il pulsante destro su *main* nella vista *Asset* e selezionando <kbd>New ▸ Material</kbd>.
2. Crea un programma vertex shader chiamato *`grade.vp`* e un programma fragment shader chiamato *`grade.fp`* facendo clic con il pulsante destro su *main* nella vista *Asset* e selezionando <kbd>New ▸ Vertex program</kbd> e <kbd>New ▸ Fragment program</kbd>.
3. Apri *grade.material* e imposta le proprietà *Vertex program* e *Fragment program* sui nuovi file dei programmi shader.
4. Aggiungi una *Vertex constant* chiamata "`view_proj`" di tipo `CONSTANT_TYPE_VIEWPROJ`. È la matrice di vista e proiezione utilizzata nel programma vertex shader per i vertici del quadrilatero.
5. Aggiungi un *Sampler* chiamato "`original`". Servirà a campionare i pixel dal buffer dei colori della destinazione di rendering fuori schermo.
6. Aggiungi un *Tag* chiamato "`grade`". Creeremo nello script di rendering un nuovo *predicato di rendering* che corrisponda a questo tag per disegnare il quadrilatero.

   ![grade.material](images/grading/grade_material.png)

7. Apri *`main.collection`*, seleziona il componente modello nell'oggetto di gioco "`grade`" e imposta la sua proprietà *Material* su "`/main/grade.material`".

   ![Proprietà del modello](images/grading/model_properties.png)

8. Puoi lasciare il programma vertex shader così come viene creato dal modello di base:

    ```glsl
    // grade.vp
    uniform mediump mat4 view_proj;

    // positions are in world space
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
      gl_Position = view_proj * vec4(position.xyz, 1.0);
      var_texcoord0 = texcoord0;
    }
    ```

9. Nel programma fragment shader, invece di impostare direttamente `gl_FragColor` sul valore del colore campionato, eseguiamo una semplice manipolazione del colore. Lo facciamo soprattutto per assicurarci che fin qui tutto funzioni come previsto:

    ```glsl
    // grade.fp
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;

    void main()
    {
      vec4 color = texture2D(original, var_texcoord0.xy);
      // Desaturate the color sampled from the original texture
      float grey = color.r * 0.3 + color.g * 0.59 + color.b * 0.11;
      gl_FragColor = vec4(grey, grey, grey, 1.0);
    }
    ```

Ora abbiamo predisposto il modello del quadrilatero con il suo materiale e i suoi shader. Non ci resta che disegnarlo nel frame buffer dello schermo.

## Applicare una texture usando il buffer fuori schermo {#texturing-with-the-off-screen-buffer}

Dobbiamo aggiungere un predicato di rendering allo script di rendering per poter disegnare il modello del quadrilatero. Apri *`grade.render_script`* e modifica la funzione `init()`:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})
    self.grade_pred = render.predicate({"grade"}) -- <1>

    ...
end
```
1. Aggiungi un nuovo predicato che corrisponda al tag "grade" impostato in *`grade.material`*.

Dopo aver riempito il buffer dei colori della destinazione di rendering in `update()`, impostiamo una vista e una proiezione che facciano riempire l'intero schermo al modello del quadrilatero. Usiamo quindi il buffer dei colori della destinazione di rendering come texture del quadrilatero:

```lua
function update(self)
  render.set_render_target(self.target)

  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT)

  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color}) -- <1>

  render.set_viewport(0, 0, render.get_window_width(), render.get_window_height()) -- <2>
  render.set_view(vmath.matrix4()) -- <3>
  render.set_projection(vmath.matrix4())

  render.enable_texture(0, self.target, graphics.BUFFER_TYPE_COLOR0_BIT) -- <4>
  render.draw(self.grade_pred) -- <5>
  render.disable_texture(0, self.target) -- <6>
end
```
1. Svuota il frame buffer. Nota che la precedente chiamata a `render.clear()` agisce sulla destinazione di rendering, non sul frame buffer dello schermo.
2. Imposta il viewport in modo che corrisponda alle dimensioni della finestra.
3. Imposta la vista sulla matrice identità. Questo significa che la camera si trova all'origine e guarda direttamente lungo l'asse Z. Imposta anche la proiezione sulla matrice identità, in modo che il quadrilatero venga proiettato piatto sull'intero schermo.
4. Imposta lo slot texture 0 sul buffer dei colori della destinazione di rendering. Nel nostro *`grade.material`*, il sampler "original" si trova nello slot 0, quindi il fragment shader campionerà dalla destinazione di rendering.
5. Disegna usando il predicato che abbiamo creato, che corrisponde a qualsiasi materiale con il tag "grade". Il modello del quadrilatero usa *`grade.material`*, che imposta quel tag: il quadrilatero verrà quindi disegnato.
6. Dopo il disegno, disattiva lo slot texture 0, poiché abbiamo finito di usarlo.

Ora eseguiamo il gioco e osserviamo il risultato:

![Gioco desaturato](images/grading/desaturated_game.png)

## Correzione cromatica {#color-grading}

I colori sono espressi da tre valori, ciascuno dei quali determina la quantità di rosso, verde o blu che compone un colore. L'intero spettro cromatico, dal nero al bianco passando per rosso, verde, blu, giallo e rosa, può essere racchiuso in un cubo:

![Cubo dei colori](images/grading/color_cube.png)

Qualsiasi colore visualizzabile sullo schermo si trova in questo cubo dei colori. L'idea alla base della correzione cromatica è usare un cubo di questo tipo, ma con colori modificati, come *tabella di ricerca* 3D.

Per ogni pixel:

1. Individua la posizione del suo colore nel cubo dei colori (in base ai valori di rosso, verde e blu).
2. *Leggi* il colore che il cubo corretto cromaticamente ha memorizzato in quella posizione.
3. Disegna il pixel con il colore letto anziché con il colore originale.

Possiamo farlo nel nostro fragment shader:

1. Campiona il valore del colore di ogni pixel nel buffer fuori schermo.
2. Individua la posizione del colore del pixel campionato in un cubo dei colori corretto cromaticamente.
3. Imposta il colore del frammento in uscita sul valore trovato.

![Correzione cromatica della destinazione di rendering](images/grading/render_target_grading.png)

## Rappresentare la tabella di ricerca {#representing-the-lookup-table}

Open GL ES 2.0 non supporta le texture 3D, quindi dobbiamo trovare un altro modo per rappresentare il cubo dei colori 3D. Un metodo comune consiste nel suddividere il cubo in sezioni lungo l'asse Z (blu) e disporre le sezioni una accanto all'altra in una griglia bidimensionale. Ciascuna delle 16 sezioni contiene una griglia di 16⨉16 pixel. Memorizziamo il tutto in una texture dalla quale possiamo leggere nel fragment shader tramite un sampler:

![Texture di ricerca](images/grading/lut.png)

La texture risultante contiene 16 celle (una per ogni intensità del blu) e, all'interno di ogni cella, 16 valori di rosso lungo l'asse X e 16 valori di verde lungo l'asse Y. La texture rappresenta l'intero spazio cromatico RGB di 16 milioni di colori con soli 4096 colori: appena 4 bit di profondità cromatica. È una precisione scarsa secondo la maggior parte dei criteri, ma grazie a una funzionalità dell'hardware grafico GL possiamo recuperare una precisione cromatica molto elevata. Vediamo come.

## Cercare i colori {#looking-up-colors}

Per cercare un colore basta controllare la componente blu e determinare da quale cella prendere i valori di rosso e verde. La formula per trovare la cella con l'insieme corretto di colori rosso-verdi è semplice:

```math
cell = \left \lfloor{B \times (N - 1)} \right \rfloor
```

Qui `B` è il valore della componente blu, compreso tra 0 e 1, e `N` è il numero totale di celle. Nel nostro caso il numero della cella sarà nell'intervallo `0`--`15`, dove la cella `0` contiene tutti i colori con la componente blu a `0` e la cella `15` tutti i colori con la componente blu a `1`.

Per esempio, il valore RGB `(0.63, 0.83, 0.4)` si trova nella cella che contiene tutti i colori con un valore di blu pari a `0.4`, ovvero la cella numero 6. Sapendolo, è semplice determinare le coordinate finali della texture in base ai valori di verde e rosso:

![Tabella di ricerca](images/grading/lut_lookup.png)

Nota che dobbiamo considerare i valori di rosso e verde `(0, 0)` come corrispondenti al *centro* del pixel in basso a sinistra e i valori `(1.0, 1.0)` come corrispondenti al *centro* del pixel in alto a destra.

::: sidenote
Leggiamo a partire dal centro del pixel in basso a sinistra fino al centro del pixel in alto a destra perché non vogliamo che i pixel esterni alla cella corrente influenzino il valore campionato. Vedi più avanti la spiegazione sul filtraggio.
:::

Campionando a queste coordinate specifiche della texture, vediamo che ci troviamo esattamente tra 4 pixel. Quale valore di colore ci restituirà GL per quel punto?

![Filtraggio della tabella di ricerca](images/grading/lut_filtering.png)

La risposta dipende da come abbiamo specificato il *filtraggio* del sampler nel materiale.

- Se il filtraggio del sampler è `NEAREST`, GL restituirà il valore del colore del pixel più vicino (con il valore della posizione arrotondato per difetto). Nel caso precedente, GL restituirà il valore del colore alla posizione `(0.60, 0.80)`. Per la nostra texture di ricerca a 4 bit, questo significa che quantizzeremo i valori dei colori in soli 4096 colori complessivi.

- Se il filtraggio del sampler è `LINEAR`, GL restituirà il valore del colore *interpolato*. GL mescolerà un colore in base alla distanza dai pixel che circondano la posizione di campionamento. Nel caso precedente, GL restituirà un colore composto per il 25% da ciascuno dei 4 pixel intorno al punto di campionamento.

Usando il filtraggio lineare eliminiamo quindi la quantizzazione dei colori e otteniamo un'ottima precisione cromatica da una tabella di ricerca piuttosto piccola.

## Implementare la ricerca {#implementing-the-lookup}

Implementiamo la ricerca nella texture all'interno del fragment shader:

1. Apri *`grade.material`*.
2. Aggiungi un secondo sampler chiamato "`lut`" (da lookup table, tabella di ricerca).
3. Imposta la proprietà *`Filter min`* su `FILTER_MODE_MIN_LINEAR` e la proprietà *`Filter mag`* su `FILTER_MODE_MAG_LINEAR`.

    ![Sampler della tabella di ricerca](images/grading/material_lut_sampler.png)

4. Scarica la seguente texture della tabella di ricerca (*`lut16.png`*) e aggiungila al tuo progetto.

    ![Tabella di ricerca a 16 colori](images/grading/lut16.png)

5. Apri *`main.collection`* e imposta la proprietà della texture *`lut`* sulla texture di ricerca scaricata.

    ![Tabella di ricerca del modello del quadrilatero](images/grading/quad_lut.png)

6. Infine, apri *`grade.fp`* per aggiungere il supporto alla ricerca dei colori:

    ```glsl
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;
    uniform lowp sampler2D lut; // <1>

    #define MAXCOLOR 15.0 // <2>
    #define COLORS 16.0
    #define WIDTH 256.0
    #define HEIGHT 16.0

    void main()
    {
        vec4 px = texture2D(original, var_texcoord0.xy); // <3>

        float cell = floor(px.b * MAXCOLOR); // <4>

        float half_px_x = 0.5 / WIDTH; // <5>
        float half_px_y = 0.5 / HEIGHT;

        float x_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
        float y_offset = half_px_y + px.g * (MAXCOLOR / COLORS); // <6>

        vec2 lut_pos = vec2(cell / COLORS + x_offset, y_offset); // <7>

        vec4 graded_color = texture2D(lut, lut_pos); // <8>

        gl_FragColor = graded_color; // <9>
    }
    ```
    1. Dichiara il sampler `lut`.
    2. Costanti per il valore massimo del colore (15, poiché partiamo da 0), il numero di colori per canale e la larghezza e l'altezza della texture di ricerca.
    3. Campiona il colore di un pixel (chiamato `px`) dalla texture originale (il buffer dei colori della destinazione di rendering fuori schermo).
    4. Calcola da quale cella leggere il colore in base al valore del canale blu di `px`.
    5. Calcola gli scostamenti di mezzo pixel, in modo da leggere dai centri dei pixel.
    6. Calcola gli scostamenti X e Y sulla texture in base ai valori di rosso e verde di `px`.
    7. Calcola la posizione di campionamento finale sulla texture di ricerca.
    8. Campiona il colore risultante dalla texture di ricerca.
    9. Imposta il colore sulla texture del quadrilatero sul colore risultante.

Al momento, la texture della tabella di ricerca restituisce gli stessi valori di colore che cerchiamo. Questo significa che il gioco dovrebbe essere renderizzato con i suoi colori originali:

![Aspetto originale del mondo](images/grading/world_original.png)

Fin qui sembra che abbiamo fatto tutto correttamente, ma c'è un problema nascosto. Guarda cosa succede quando aggiungiamo uno sprite con una texture di test contenente un gradiente:

![Bande nel blu](images/grading/blue_banding.png)

Il gradiente blu mostra delle bande davvero sgradevoli. Perché?

## Interpolare il canale blu {#interpolating-the-blue-channel}

Il problema delle bande nel canale blu è che GL non può eseguire alcuna interpolazione di questo canale quando legge il colore dalla texture. Selezioniamo in anticipo una specifica cella da cui leggere in base al valore del blu, e ci fermiamo lì. Per esempio, se il canale blu contiene un valore qualsiasi nell'intervallo `0.400`--`0.466`, il valore preciso non conta: campioneremo sempre il colore finale dalla cella numero 6, dove il canale blu è impostato a `0.400`.

Per ottenere una migliore risoluzione del canale blu, possiamo implementare noi stessi l'interpolazione. Se il valore del blu è compreso tra quelli di due celle adiacenti, possiamo campionare da entrambe le celle e poi mescolare i colori. Per esempio, se il valore del blu è `0.420`, dovremmo campionare dalla cella numero 6 *e* dalla cella numero 7, poi mescolare i colori.

Dobbiamo quindi leggere da due celle:

```math
cell_{low} = \left \lfloor{B \times (N - 1)} \right \rfloor
```

e:

```math
cell_{high} = \left \lceil{B \times (N - 1)} \right \rceil
```

Poi campioniamo i valori dei colori da ciascuna di queste celle e interpoliamo i colori linearmente, secondo la formula:

```math
color = color_{low} \times (1 - C_{frac}) + color_{high} \times C_{frac}
```

Qui `color`~low~ è il colore campionato dalla cella inferiore (più a sinistra) e `color`~high~ è il colore campionato dalla cella superiore (più a destra). La funzione GLSL `mix()` esegue questa interpolazione lineare per noi.

Il valore `C~frac~` nella formula precedente è la parte frazionaria del valore del canale blu, riscalato nell'intervallo di colori `0`--`15`:

```math
C_{frac} = B \times (N - 1) - \left \lfloor{B \times (N - 1)} \right \rfloor
```

Anche in questo caso esiste una funzione GLSL che restituisce la parte frazionaria di un valore. Si chiama `frac()`. L'implementazione finale nel fragment shader (*`grade.fp`*) è piuttosto semplice:

```glsl
varying mediump vec4 position;
varying mediump vec2 var_texcoord0;

uniform lowp sampler2D original;
uniform lowp sampler2D lut;

#define MAXCOLOR 15.0
#define COLORS 16.0
#define WIDTH 256.0
#define HEIGHT 16.0

void main()
{
  vec4 px = texture2D(original, var_texcoord0.xy);

    float cell = px.b * MAXCOLOR;

    float cell_l = floor(cell); // <1>
    float cell_h = ceil(cell);

    float half_px_x = 0.5 / WIDTH;
    float half_px_y = 0.5 / HEIGHT;
    float r_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
    float g_offset = half_px_y + px.g * (MAXCOLOR / COLORS);

    vec2 lut_pos_l = vec2(cell_l / COLORS + r_offset, g_offset); // <2>
    vec2 lut_pos_h = vec2(cell_h / COLORS + r_offset, g_offset);

    vec4 graded_color_l = texture2D(lut, lut_pos_l); // <3>
    vec4 graded_color_h = texture2D(lut, lut_pos_h);

    // <4>
    vec4 graded_color = mix(graded_color_l, graded_color_h, fract(cell));

    gl_FragColor = graded_color;
}
```

1. Calcola le due celle adiacenti da cui leggere.
2. Calcola due posizioni di ricerca separate, una per ogni cella.
3. Campiona i due colori dalle posizioni delle celle.
3. Mescola i colori linearmente in base alla parte frazionaria di `cell`, che è il valore del blu riscalato.

Eseguendo di nuovo il gioco con la texture di test, ora otteniamo risultati molto migliori. Le bande nel canale blu sono scomparse:

![Blu senza bande](images/grading/blue_no_banding.png)

## Correggere i colori della texture di ricerca {#grading-the-lookup-texture}

Bene, è stato un bel po' di lavoro per disegnare qualcosa che ha esattamente lo stesso aspetto del mondo di gioco originale. Ma questa configurazione ci permette di fare qualcosa di davvero interessante. Preparati!

1. Acquisisci una schermata del gioco senza modifiche ai colori.
2. Apri la schermata nel tuo programma di elaborazione delle immagini preferito.
3. Applica tutte le regolazioni del colore che desideri (luminosità, contrasto, curve dei colori, bilanciamento del bianco, esposizione ecc.).

![Mondo in Affinity](images/grading/world_graded_affinity.png)

4. Applica le stesse regolazioni del colore al file della texture della tabella di ricerca (*`lut16.png`*).
5. Salva il file della texture della tabella di ricerca con i colori regolati.
6. Sostituisci la texture *`lut16.png`* utilizzata nel tuo progetto Defold con quella dai colori regolati.
7. Esegui il gioco!

![Mondo con correzione cromatica](images/grading/world_graded.png)

Che soddisfazione!
