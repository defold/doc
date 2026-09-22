## Applicazione di texture con slice-9 {#slice-9-texturing}

I nodi GUI di tipo box e i componenti sprite a volte includono elementi le cui dimensioni dipendono dal contesto: pannelli e finestre di dialogo da ridimensionare per adattarli al contenuto, oppure una barra della salute da ridimensionare per mostrare la salute rimanente di un nemico. L'applicazione di texture al nodo o allo sprite ridimensionato può causare problemi visivi.

Normalmente, il motore ridimensiona la texture per adattarla ai limiti rettangolari, ma definendo le aree dei bordi con slice-9 è possibile limitare le parti della texture da ridimensionare:

![Ridimensionamento della GUI](../shared/images/gui_slice9_scaling.png)

La proprietà *Slice9* del nodo box è composta da 4 numeri che specificano il numero di pixel dei margini sinistro, superiore, destro e inferiore da escludere dal normale ridimensionamento:

![Proprietà di slice-9](../shared/images/gui_slice9_properties.png)

I margini vengono impostati in senso orario, a partire dal bordo sinistro:

![Sezioni di slice-9](../shared/images/gui_slice9.png)

- I segmenti agli angoli non vengono mai ridimensionati.
- I segmenti dei bordi vengono ridimensionati lungo un solo asse. I segmenti dei bordi sinistro e destro vengono ridimensionati verticalmente. I segmenti dei bordi superiore e inferiore vengono ridimensionati orizzontalmente.
- L'area centrale della texture viene ridimensionata orizzontalmente e verticalmente secondo necessità.

Il ridimensionamento della texture con *Slice9* descritto sopra viene applicato solo quando modifichi le dimensioni del nodo box o dello sprite:

![Dimensioni del nodo GUI di tipo box](../shared/images/gui_slice9_size.png)

![Dimensioni dello sprite](../shared/images/sprite_slice9_size.png)

::: important
Se modifichi il parametro di scala del nodo box o dello sprite (oppure dell'oggetto di gioco), il nodo o lo sprite e la texture vengono ridimensionati senza applicare i parametri *Slice9*.
:::

::: important
Quando applichi texture con slice-9 agli sprite, la [proprietà Sprite Trim Mode dell'immagine](https://defold.com/manuals/atlas/#image-properties) deve essere impostata su Off.
:::


### Mipmap e slice-9 {#mipmaps-and-slice-9}
Per il modo in cui il mipmapping funziona nel renderer, il ridimensionamento dei segmenti della texture può talvolta produrre artefatti. Questo accade quando _riduci_ i segmenti al di sotto delle dimensioni originali della texture. Il renderer seleziona quindi una mipmap a risoluzione inferiore per il segmento, causando artefatti visivi.

![Mipmapping con slice-9](../shared/images/gui_slice9_mipmap.png)

Per evitare questo problema, assicurati che i segmenti della texture da ridimensionare siano abbastanza piccoli da dover essere soltanto ingranditi, mai ridotti.
