---
brief: In questo tutorial convertirai uno shader da shadertoy.com per usarlo in Defold.
layout: tutorial
locale: it
title: Tutorial da Shadertoy a Defold
---

# Tutorial Shadertoy {#shadertoy-tutorial}

[Shadertoy.com](https://www.shadertoy.com/) è un sito che raccoglie shader GL creati dagli utenti. È un'ottima risorsa per trovare codice di shader e ispirazione. In questo tutorial prenderemo uno shader da Shadertoy e lo faremo funzionare in Defold. Si presuppone una conoscenza di base degli shader. Se hai bisogno di approfondire, [il manuale degli shader](/manuals/shader/) è un buon punto di partenza.

Lo shader che useremo è [Star Nest](https://www.shadertoy.com/view/XlfGRj) di Pablo Andrioli (l'utente "Kali" su Shadertoy). È un fragment shader interamente procedurale che, con una sorta di magia nera matematica, produce un bellissimo effetto di campo stellare.

![Star Nest](../images/shadertoy/starnest.png)

Lo shader è composto da appena 65 righe di codice GLSL piuttosto complicato, ma non preoccuparti. Lo tratteremo come una scatola nera che svolge il proprio compito in base a pochi semplici input. Il nostro compito è modificare lo shader affinché si interfacci con Defold invece che con Shadertoy.

## Una superficie a cui applicare la texture {#something-to-texture}

Lo shader Star Nest è un puro fragment shader, quindi ci serve soltanto una superficie a cui possa applicare la texture. Ci sono diverse opzioni: uno sprite, una mappa di tile, una GUI o un modello. Per questo tutorial useremo un semplice modello 3D. Il motivo è che possiamo facilmente trasformare il rendering del modello in un effetto a schermo intero---un'operazione necessaria, per esempio, se vogliamo applicare una post-elaborazione visiva.

Possiamo partire da un progetto vuoto.

1. Apri Defold e seleziona Create From *Templates*.
2. Seleziona *Empty Project*.
3. Imposta *Title* e seleziona *Location* sul disco.
4. Fai clic su <kbd>Create New Project</kbd>.

![Avvio](../images/shadertoy/empty_project.png)

Puoi usare la mesh integrata `quad.gltf` in `builtins/assets/meshes`.

Se preferisci, puoi anche creare una mesh piana quadrata in Blender o in qualsiasi altro programma di modellazione 3D --- per comodità, le coordinate dei 4 vertici sono -1 e 1 sull'asse X e -1 e 1 sull'asse Y. Per impostazione predefinita, in Blender l'asse Z è rivolto verso l'alto, quindi devi ruotare la mesh di 90° attorno all'asse X. Assicurati anche di generare coordinate UV corrette per la mesh. In Blender, entra in *Edit Mode* con la mesh selezionata, quindi seleziona <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>.

<div class='sidenote' markdown='1'>
Blender è un software 3D gratuito e open source che puoi scaricare da [blender.org](https://www.blender.org).
</div>

![Quadrilatero in Blender](../images/shadertoy/quad_blender.png)

1. Apri il file "main.collection" in Defold e crea un nuovo oggetto di gioco (game object) "star-nest".
2. Aggiungi un componente *Model* all'oggetto di gioco "star-nest".
3. Imposta la proprietà *Mesh* sul nostro `quad.gltf`.
4. Dobbiamo impostare il materiale del modello, quindi per ora seleziona il materiale integrato `model.material`.

Il modello dovrebbe apparire nell'editor della scena, ma viene disegnato completamente nero. Questo accade perché non ha ancora una texture impostata:

![Quadrilatero in Defold](../images/shadertoy/quad_default_material.png)

## Creazione del materiale {#creating-the-material}

1. Crea un nuovo file di materiale *`star-nest.material`* facendo clic con il <kbd>tasto destro del mouse</kbd> sulla cartella `main` nel pannello `Assets`, selezionando <kbd>New</kbd>-><kbd>Material</kbd> e assegnandogli il nome `star-nest`.

 ![Materiale](../images/shadertoy/new_material.png)

2. Allo stesso modo, crea un programma vertex shader `star-nest.vp` e un programma fragment shader `star-nest.fp`:
3. Apri *star-nest.material*.
4. Imposta *Vertex Program* su `star-nest.vp`.
5. Imposta *Fragment Program* su `star-nest.fp`.
6. Aggiungi una *Vertex Constant*, chiamala "`view_proj`" e assegnale il tipo `Viewproj` (per "proiezione della vista").
8. Aggiungi un tag "tile" a *Tags*. In questo modo il quadrilatero viene incluso nel passaggio di rendering in cui vengono disegnati sprite e tile.

 ![Materiale](../images/shadertoy/material.png)

### Programma vertex shader {#vertex-program}

1. Apri il file del programma vertex shader `star-nest.vp`. Dovrebbe contenere il seguente codice:

    ```glsl
    #version 140

    // positions are in world space
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### Programma fragment shader {#fragment-program}

1. Apri il file del programma fragment shader `star-nest.fp` e modifica il codice in modo che il colore del frammento venga impostato in base alle componenti X e Y delle coordinate UV (`var_texcoord0`). Lo facciamo per assicurarci di aver configurato correttamente il modello:

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. Imposta la proprietà `Material` sul materiale `star-nest` appena creato, nel componente modello dell'oggetto di gioco `star-nest` in `main.collection`.

Ora l'editor dovrebbe disegnare il modello con il nuovo shader e possiamo vedere chiaramente se le coordinate UV sono corrette; l'angolo in basso a sinistra dovrebbe essere nero (0, 0, 0), quello in alto a sinistra verde (0, 1, 0), quello in alto a destra giallo (1, 1, 0) e quello in basso a destra rosso (1, 0, 0):

![Quadrilatero in Defold](../images/shadertoy/quad_material.png)

## Telecamera {#camera}

Ora possiamo eseguire il progetto (<kbd>Project</kbd>-><kbd>Build</kbd> oppure la scorciatoia <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>), ma vedremo uno schermo nero (quasi, a parte forse un minuscolo pixel nell'angolo in basso a sinistra). Questo accade perché non c'è una telecamera e lo script di rendering predefinito usa una semplice soluzione di ripiego che mostra un enorme spazio 2D, mentre il nostro modello si trova nella posizione (0,0,0) e ha una larghezza di appena 1.

Aggiungiamo un oggetto di gioco con un componente telecamera per definire ciò che vedremo nel gioco.

1. Aggiungi un oggetto di gioco chiamato `camera` nella posizione (0,0,1). (È importante impostare la coordinata Z su 1, in modo che questo oggetto di gioco si trovi davanti al nostro modello, poiché nella configurazione 2D predefinita l'asse Z è rivolto verso di noi).
2. Aggiungi un componente `Camera` e vedrai un'anteprima della telecamera con il nostro quadrilatero al suo interno. In questa configurazione siamo fortunati: le proprietà predefinite vanno già bene e dovremmo vedere il risultato corretto, con una sola eccezione - non ci serve un volume di vista così ampio, quindi possiamo ridurre `Far Z` a `2`.

![Telecamera](../images/shadertoy/camera.png)

Se preferisci, puoi cambiare il tipo di telecamera impostando `Orthographic Projection` su `true` e regolando anche `Orthographic Zoom` su un valore come 600, ma in questo caso il rapporto d'aspetto non verrà adattato automaticamente e il modello non riempirà lo schermo.

## Lo shader Star Nest {#the-star-nest-shader}

Ora che tutto è pronto, iniziamo a lavorare sul codice dello shader vero e proprio. Diamo prima un'occhiata al codice originale. È composto da alcune sezioni:

![Codice dello shader Star Nest](../images/shadertoy/starnest_code.png)

Useremo una pipeline moderna con GLSL versione 140 - per farlo, dichiareremo la versione all'inizio del file con `#version 140`.

1. Le righe 5--18 definiscono una serie di costanti. Possiamo lasciarle così come sono. Sono normali costanti GLSL e non dipendono specificamente da Shadertoy o da Defold.

2. Le righe 21 e 63 contengono le coordinate X e Y della texture nello spazio dello schermo per il frammento in ingresso (`in vec2 fragCoord`) e il colore del frammento in uscita (`out vec4 fragColor`).

    Defold passa le coordinate della texture dal vertex shader al fragment shader attraverso una variabile interpolata sotto forma di coordinate UV (nell'intervallo 0--1). Nel nostro vertex shader questa viene dichiarata con un qualificatore `out`:

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     Nel fragment shader lo stesso valore viene ricevuto con un qualificatore `in`:

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    Poi, in GLSL 140, dichiariamo esplicitamente un'uscita per il frammento con il qualificatore `out`:

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    Quindi, dove il codice originale di Shadertoy scrive in `fragColor`, il nostro shader Defold scrive in `out_fragColor`.

3. Le righe 23--27 impostano le dimensioni della texture, la direzione del movimento e il tempo scalato. In Shadertoy lo shader riceve la posizione del pixel attraverso `fragCoord` e la risoluzione del viewport o della texture viene passata allo shader come `uniform vec3 iResolution`. Lo shader calcola coordinate di tipo UV con il rapporto d'aspetto corretto a partire dalle coordinate del frammento e dalla risoluzione. Applica anche alcuni scostamenti in base alla risoluzione per ottenere un'inquadratura migliore.

    In Defold non partiamo dalle coordinate dei pixel. Riceviamo invece dal vertex shader coordinate UV già normalizzate attraverso `var_texcoord0`. Queste coordinate variano da `0.0` a `1.0` lungo il quadrilatero disegnato.

    Nella versione Defold dobbiamo modificare questi calcoli per usare le coordinate UV di `var_texcoord0`.
    Una conversione tipica è la seguente:

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    Il valore esatto di `aspect` dipende da come è configurato l'esempio. Se l'effetto viene disegnato su un quadrilatero a schermo intero con dimensioni dello schermo note, per il tutorial possiamo scrivere il rapporto d'aspetto direttamente nel codice. Se l'effetto deve supportare finestre di dimensioni arbitrarie, passa la risoluzione come costante del fragment shader e inseriscila in un blocco uniform GLSL 140.

    Qui viene impostato anche il tempo, che viene passato allo shader come `uniform float iGlobalTime`. Defold (dalla versione 1.12.3) fornisce il tempo agli shader tramite una speciale costante `Time` che useremo.

    Nelle versioni moderne di Defold, le variabili uniform di tipo non opaco vengono dichiarate all'interno di blocchi uniform.
    Nel fragment shader lo dichiariamo così:

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    Poi, in `star-nest.material`, aggiungeremo una Fragment Constant chiamata `time` e imposteremo il suo tipo su `Time`.

    Il valore può quindi essere usato così:

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    dove `time.x` è il tempo trascorso dall'avvio del motore e `time.y` è il tempo trascorso dal fotogramma precedente.

4. Le righe 29--39 impostano la rotazione del rendering volumetrico, influenzata dalla posizione del mouse. Le coordinate del mouse vengono passate allo shader come `uniform vec4 iMouse`.

    Per questo tutorial tralasceremo l'input del mouse.

5. Le righe 41--62 costituiscono il nucleo dello shader. Possiamo lasciare questo codice così com'è.

## Lo shader Star Nest modificato {#the-modified-star-nest-shader}

Esaminando le sezioni precedenti e apportando le modifiche necessarie otteniamo il seguente codice dello shader. È stato riordinato un po' per renderlo più leggibile. Sono indicate le differenze tra le versioni Defold e Shadertoy:

```glsl
#version 140 // <1>

// Star Nest by Pablo Román Andrioli
// This content is under the MIT License.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// get coords and direction
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// volumetric rendering
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// tiling fold
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// the magic formula
			p = abs(p) / dot(p, p) - formuparam;

			// absolute sum of average change
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// dark matter
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// dark matter, don't render near
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// coloring based on distance
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// color adjust
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```

1. Dichiariamo #version 140 all'inizio del file per usare la pipeline GLSL moderna di Defold. Lasciamo poi invariate le direttive define.
2. Il vertex shader passa le coordinate UV al fragment shader attraverso var_texcoord0. In GLSL 140, il fragment shader riceve questo valore interpolato con il qualificatore in.
3. In GLSL 140, il fragment shader deve dichiarare una variabile di uscita esplicita anziché scrivere in gl_FragColor. Qui usiamo out vec4 out_fragColor.
4. La costante di materiale Time di Defold viene resa disponibile allo shader attraverso un blocco uniform. In star-nest.material, aggiungi una Fragment Constant chiamata time e imposta il suo tipo su Time.
5. Shadertoy usa mainImage(out vec4 fragColor, in vec2 fragCoord). In Defold usiamo il normale punto di ingresso void main(), leggiamo le coordinate UV interpolate da var_texcoord0 e scriviamo il colore finale in out_fragColor.
6. Per questo tutorial definiamo un valore statico di risoluzione e rapporto d'aspetto per il rendering. Attualmente il modello è quadrato, quindi possiamo usare vec2 res = vec2(1.0, 1.0);. Con un modello rettangolare di dimensioni 1280×720, potremmo invece usare vec2 res = vec2(1.78, 1.0); e moltiplicare le coordinate UV per questo valore per mantenere il rapporto d'aspetto corretto.
7. Lo shader Shadertoy originale usa iGlobalTime. In questa versione Defold, time.x contiene il tempo trascorso dall'avvio del motore, quindi lo assegniamo a una variabile locale iGlobalTime e lo usiamo per animare il movimento della telecamera attraverso il campo stellare.
8. Manteniamo semplice questo tutorial rimuovendo del tutto i valori iMouse. La rotazione viene comunque mantenuta, perché riduce la simmetria visiva nel rendering volumetrico.
9. Infine, lo shader scrive il colore risultante del frammento in out_fragColor.

Salva il programma fragment shader. Il modello dovrebbe ora mostrare una bella texture con un campo stellare nell'editor della scena e durante l'esecuzione:

![Quadrilatero con Star Nest](../images/shadertoy/quad_starnest.png)


## Animazione {#animation}

L'ultimo pezzo del puzzle è introdurre il tempo per far muovere le stelle. Defold (dalla versione 1.12.3) lo fornisce automaticamente attraverso una costante del fragment shader di tipo `Time`.

1. Apri *star-nest.material*.
2. Aggiungi una *Fragment Constant* e chiamala "time".
3. Imposta il suo *Type* su `Time`.

![Costante del tempo](../images/shadertoy/time_constant.png)

E questo è tutto! Gestiamo già questo `time` nel fragment shader. Abbiamo finito!

## Esercizi {#exercises}

Un esercizio divertente per proseguire è aggiungere allo shader l'input originale del movimento del mouse. Dovrai creare una nuova Fragment Constant, questa volta di tipo `User`, e aggiornarla in `on_input` in uno script che rileva il movimento del mouse, usando la funzione `go.set()` per assegnare le coordinate di input alla nuova costante.

Buon divertimento con Defold!
