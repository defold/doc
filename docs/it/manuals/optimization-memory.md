---
title: Ottimizzare l'uso della memoria in un gioco Defold
brief: Questo manuale descrive come ottimizzare l'uso della memoria in un gioco Defold.
---

# Ottimizzare l'uso della memoria {#optimizing-memory-usage}

## Compressione delle texture {#texture-compression}
La compressione delle texture non solo riduce le dimensioni delle risorse nell'archivio del gioco, ma può anche ridurre la quantità di memoria GPU necessaria.

## Caricamento dinamico {#dynamic-loading}
La maggior parte dei giochi contiene almeno alcuni contenuti usati di rado. Dal punto di vista dell'uso della memoria, non ha senso tenerli sempre caricati: è preferibile caricarli quando servono e scaricarli quando non sono più necessari. Questo comporta ovviamente un compromesso tra avere contenuti subito disponibili, occupando memoria durante l'esecuzione, e caricarli al momento, impiegando del tempo per il caricamento.

Defold offre diversi modi per caricare contenuti dinamicamente:

* [Proxy di collezione](/manuals/collection-proxy/)
* [Fabbriche di collezioni dinamiche (collection factory)](/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [Fabbriche dinamiche (factory)](/manuals/factory/#dynamic-loading-of-factory-resources)
* [Live Update](/manuals/live-update/)

## Ottimizzare i contatori dei componenti {#optimize-component-counters}
Per ridurre la frammentazione della memoria, Defold alloca una sola volta la memoria per componenti e risorse quando viene creata una collezione. La quantità di memoria allocata dipende dalla configurazione dei vari contatori dei componenti in *game.project*. Usa il [profilatore](/manuals/profiling/) per misurare con precisione l'uso di componenti e risorse e configura il gioco con valori massimi più vicini al numero effettivo di componenti e risorse. In questo modo ridurrai la quantità di memoria usata dal gioco (consulta le informazioni sull'[ottimizzazione del numero massimo di componenti](/manuals/project-settings/#component-max-count-optimizations)).

## Ottimizzare il numero di nodi GUI {#optimize-gui-node-count}
Ottimizza il numero di nodi GUI impostando nel file GUI un numero massimo di nodi limitato a quelli necessari. Il campo `Current Nodes` nelle [proprietà del componente GUI](https://defold.com/manuals/gui/#gui-properties) mostra il numero di nodi usati dal componente GUI.

:[HTML5 Optimizations](../shared/optimization-memory-html5.md)

