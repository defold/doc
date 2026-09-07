---
title: Filtraggio delle texture
brief: Questo manuale descrive le opzioni disponibili per il filtraggio delle texture durante il rendering della grafica.
---

# Filtraggio e campionamento delle texture {#texture-filtering-and-sampling}

Il filtraggio delle texture determina il risultato visivo quando un _texel_ (un pixel di una texture) non è perfettamente allineato con un pixel dello schermo. Questo accade quando sposti un elemento grafico che contiene la texture di una distanza inferiore a un pixel. Sono disponibili i seguenti metodi di filtraggio:

Texel più vicino (Nearest)
: Per colorare il pixel dello schermo viene scelto il texel più vicino. Scegli questo metodo di campionamento se vuoi una corrispondenza perfetta, pixel per pixel, tra le texture e ciò che vedi sullo schermo. Con il filtraggio del texel più vicino, durante il movimento tutto passa a scatti da un pixel all'altro. Questo può produrre un movimento poco fluido se lo sprite si muove lentamente.

Lineare (Linear)
: Prima di colorare il pixel dello schermo, viene calcolata la media del texel con quelli vicini. Questo produce un aspetto fluido nei movimenti lenti e continui, poiché il colore dello sprite si diffonde nei pixel prima di colorarli completamente: è quindi possibile spostare uno sprite di una distanza inferiore a un pixel intero.

Il filtraggio da utilizzare è specificato nel file delle [impostazioni del progetto](/manuals/project-settings/#graphics). Sono presenti due impostazioni:

default_texture_min_filter
: Il filtraggio in riduzione si applica quando il texel è più piccolo del pixel dello schermo.

default_texture_mag_filter
: Il filtraggio in ingrandimento si applica quando il texel è più grande del pixel dello schermo.

Entrambe le impostazioni accettano i valori `linear`, `nearest`, `nearest_mipmap_nearest`, `nearest_mipmap_linear`, `linear_mipmap_nearest` o `linear_mipmap_linear`. Per esempio:

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

Se non specifichi alcun valore, entrambe sono impostate su `linear` per impostazione predefinita.

L'impostazione in *game.project* viene utilizzata dai campionatori predefiniti. Se specifichi dei campionatori in un materiale personalizzato, puoi impostare il metodo di filtraggio per ciascun campionatore. Consulta il [manuale dei materiali](/manuals/material/) per maggiori dettagli.
