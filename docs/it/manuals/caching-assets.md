---
title: Memorizzazione degli asset nella cache
brief: Questo manuale spiega come usare la cache degli asset per velocizzare le build.
---

# Memorizzazione degli asset nella cache {#caching-assets}

La build dei giochi creati con Defold richiede solitamente pochi secondi, ma man mano che un progetto cresce aumenta anche la quantità di asset. La compilazione dei font e la compressione delle texture possono richiedere molto tempo in un progetto di grandi dimensioni. La cache degli asset serve a velocizzare le build ricompilando soltanto gli asset modificati e utilizzando quelli già compilati nella cache per gli asset rimasti invariati.

Defold utilizza una cache a tre livelli:

1. Cache del progetto
2. Cache locale
3. Cache remota


## Cache del progetto {#project-cache}

Per impostazione predefinita, Defold memorizza gli asset compilati nella cache nella cartella `build/default` di un progetto Defold. La cache del progetto velocizza le build successive, poiché soltanto gli asset modificati devono essere ricompilati, mentre quelli rimasti invariati vengono recuperati dalla cache del progetto. Questa cache è sempre abilitata ed è utilizzata sia dall'editor sia dagli strumenti a riga di comando.

Puoi svuotare manualmente la cache del progetto eliminando i file in `build/default` oppure eseguendo il comando `clean` dello [strumento di build a riga di comando Bob](/manuals/bob).


## Cache locale {#local-cache}

La cache locale è una seconda cache facoltativa in cui gli asset compilati vengono memorizzati in un percorso esterno sullo stesso computer o su un'unità di rete. Grazie alla sua posizione esterna, il contenuto della cache viene conservato anche quando la cache del progetto viene svuotata. Può inoltre essere condivisa da più sviluppatori che lavorano allo stesso progetto. Attualmente questa cache è disponibile solo per le build create con gli strumenti a riga di comando. Si abilita tramite l'opzione `resource-cache-local`:

```sh
java -jar bob.jar --resource-cache-local /Users/john.doe/defold_local_cache
```

Gli asset compilati vengono recuperati dalla cache locale in base a una somma di controllo calcolata tenendo conto della versione del motore Defold, dei nomi e del contenuto degli asset sorgente, nonché delle opzioni di build del progetto. Questo garantisce che gli asset nella cache siano univoci e che la cache possa essere condivisa tra più versioni di Defold.

::: sidenote
I file nella cache locale vengono conservati a tempo indeterminato. Spetta allo sviluppatore rimuovere manualmente i file vecchi o inutilizzati.
:::


## Cache remota {#remote-cache}

La cache remota è una terza cache facoltativa in cui gli asset compilati vengono memorizzati su un server e recuperati tramite richieste HTTP. Attualmente questa cache è disponibile solo per le build create con gli strumenti a riga di comando. Si abilita tramite l'opzione `resource-cache-remote`:

```sh
java -jar bob.jar --resource-cache-remote http://192.168.0.100/
```

Come per la cache locale, tutti gli asset vengono recuperati dalla cache remota in base a una somma di controllo calcolata. Gli asset nella cache sono accessibili tramite i metodi di richiesta HTTP GET, PUT e HEAD. Defold non fornisce il server della cache remota. Spetta a ciascuno sviluppatore configurarlo. Puoi consultare qui un [esempio di un semplice server Python](https://github.com/britzl/httpserver-python).
