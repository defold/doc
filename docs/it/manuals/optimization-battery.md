---
title: Ottimizzazione del consumo della batteria di un gioco Defold
brief: Questo manuale descrive come ottimizzare il consumo della batteria di un gioco Defold.
---

# Ottimizzare il consumo della batteria {#optimize-battery-usage}
Il consumo della batteria è un aspetto da considerare soprattutto se il gioco è destinato a dispositivi mobili o portatili. Un utilizzo elevato della CPU o della GPU scarica rapidamente la batteria e surriscalda il dispositivo.

Consulta i manuali su come [ottimizzare le prestazioni durante l'esecuzione](/manuals/optimization-speed) di un gioco per scoprire come ridurre l'utilizzo della CPU e della GPU.

## Disattivare l'accelerometro {#disable-accelerometer}
Se stai creando un gioco per dispositivi mobili che non utilizza l'accelerometro del dispositivo, ti consigliamo di [disattivarlo in *game.project*](/manuals/project-settings/#use-accelerometer) per ridurre il numero di eventi di input generati.

# Ottimizzazioni specifiche per piattaforma {#platform-specific-optimizations}

## Android Device Performance Framework

Android Dynamic Performance Framework è un insieme di API che consentono ai giochi di interagire più direttamente con i sistemi di gestione energetica e termica dei dispositivi Android. Puoi monitorare il comportamento dinamico dei sistemi Android e ottimizzare le prestazioni del gioco mantenendole a un livello sostenibile, che non surriscaldi i dispositivi. Usa l'[estensione Android Dynamic Performance Framework](https://defold.com/extension-adpf/) per monitorare e ottimizzare le prestazioni del tuo gioco Defold sui dispositivi Android.
