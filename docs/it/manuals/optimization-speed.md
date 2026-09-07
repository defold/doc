---
title: Ottimizzare le prestazioni di un gioco Defold durante l'esecuzione
brief: Questo manuale descrive come ottimizzare un gioco Defold per ottenere una frequenza dei fotogrammi elevata e stabile.
---

# Ottimizzare la velocità di esecuzione {#optimizing-runtime-speed}
Prima di provare a ottimizzare un gioco per ottenere una frequenza dei fotogrammi elevata e stabile, devi sapere dove si trovano i colli di bottiglia. Quale operazione richiede effettivamente più tempo in un fotogramma del tuo gioco? Il rendering? La logica di gioco? Il grafo della scena? Per scoprirlo, è consigliabile usare gli strumenti di profilazione integrati. Usa il [profilatore a schermo o web](/manuals/profiling/) per campionare le prestazioni del gioco e poi decidere se ottimizzare qualcosa e su cosa intervenire. Quando avrai capito meglio quali operazioni richiedono tempo, potrai iniziare ad affrontare i problemi.

## Riduci il tempo di esecuzione degli script {#reduce-script-execution-time}
Devi ridurre il tempo di esecuzione degli script se il profilatore mostra valori elevati nell'ambito `Script`. Come regola generale, cerca naturalmente di eseguire meno codice possibile a ogni fotogramma. Eseguire molto codice in `update()` e `on_input()` a ogni fotogramma può incidere sulle prestazioni del gioco, soprattutto sui dispositivi di fascia bassa. Ecco alcune indicazioni:

### Usa schemi di programmazione reattiva {#use-reactive-code-patterns}
Non controllare continuamente se ci sono modifiche quando puoi ricevere una callback. Non animare manualmente un elemento e non eseguire un'attività che puoi affidare al motore (ad esempio, usa `go.animate)()` invece di animare manualmente un elemento).

### Riduci gli interventi del garbage collector {#reduce-garbage-collection}
Se a ogni fotogramma crei molti oggetti di breve durata, come le tabelle Lua, prima o poi attiverai il garbage collector di Lua. Quando questo accade, può manifestarsi con piccoli scatti o picchi nel tempo di elaborazione dei fotogrammi. Riutilizza le tabelle dove puoi e cerca il più possibile di evitare la creazione di tabelle Lua all'interno di cicli e costrutti simili.

### Precalcola gli hash degli ID di messaggi e azioni {#prehash-message-and-action-ids}
Se gestisci molti messaggi o devi elaborare numerosi eventi di input, è consigliabile precalcolare gli hash delle stringhe. Considera questo codice:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

Nell'esempio precedente, l'hash della stringa viene ricreato ogni volta che si riceve un messaggio. Puoi migliorare questo comportamento creando gli hash delle stringhe una sola volta e usando le versioni già calcolate durante la gestione dei messaggi:

```lua
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

### Preferisci gli URL e memorizzali nella cache {#prefer-and-cache-urls}
Puoi inviare messaggi o indirizzare in altro modo un oggetto di gioco o un componente fornendo un ID come stringa o hash oppure un URL. Se usi una stringa o un hash, internamente verrà convertito in un URL. Per ottenere le migliori prestazioni possibili dal sistema, è quindi consigliabile memorizzare nella cache gli URL usati spesso. Considera il codice seguente:

```lua
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- do something with pos
```

In tutti e tre i casi viene recuperata la posizione dell'oggetto di gioco con ID `enemy`. Nel primo e nel secondo caso, l'ID (stringa o hash) viene convertito in un URL prima di essere usato. Questo dimostra che, per ottenere le migliori prestazioni possibili, conviene memorizzare gli URL nella cache e usare la versione memorizzata:

```lua
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- do something with pos
    end
```

## Riduci il tempo necessario per il rendering di un fotogramma {#reduce-time-it-takes-to-render-a-frame}
Devi ridurre il tempo necessario per il rendering di un fotogramma se il profilatore mostra valori elevati negli ambiti `Render` e `Render Script`. Ci sono diversi aspetti da considerare quando cerchi di ridurre il tempo necessario per il rendering di un fotogramma:

* Riduci le chiamate di disegno - Per saperne di più su come ridurre le chiamate di disegno, leggi [questo post sul forum](https://forum.defold.com/t/draw-calls-and-defold/4674)
* Riduci il disegno ripetuto degli stessi pixel (overdraw)
* Riduci la complessità degli shader - Approfondisci le ottimizzazioni GLSL in [questo articolo di Khronos](https://www.khronos.org/opengl/wiki/GLSL_Optimizations). Puoi anche modificare gli shader predefiniti usati da Defold (disponibili in `builtins/materials`) e scegliere una precisione inferiore dove lo shader non richiede `highp`. Gli shader GLSL ES generati dalla compilazione incrociata usano per impostazione predefinita `mediump` per i valori in virgola mobile e `highp` per gli interi; puoi modificare questi valori predefiniti nella sezione Shader delle impostazioni del progetto. I qualificatori espliciti delle singole variabili hanno la precedenza. Consulta la [documentazione sulla precisione degli shader](/manuals/shader/#precision).

## Riduci la complessità del grafo della scena {#reduce-scene-graph-complexity}
Devi ridurre la complessità del grafo della scena se il profilatore mostra valori elevati nell'ambito `GameObject` e, più precisamente, nel campione `UpdateTransform`. Ecco alcuni interventi possibili:

* Esclusione degli oggetti non visibili - Disabilita gli oggetti di gioco (e i relativi componenti) se non sono attualmente visibili. Il modo in cui lo determini dipende molto dal tipo di gioco. Per un gioco 2D può essere sufficiente disabilitare sempre gli oggetti di gioco che si trovano al di fuori di un'area rettangolare. Puoi rilevarli con un trigger fisico oppure suddividendo gli oggetti in gruppi. Una volta individuati gli oggetti da disabilitare o abilitare, invia un messaggio `disable` o `enable` a ciascun oggetto di gioco.

## Esclusione degli elementi fuori dal frustum {#frustum-culling}
Lo script di rendering può ignorare automaticamente il rendering dei componenti degli oggetti di gioco che si trovano al di fuori di un volume di delimitazione definito (frustum). Per approfondire l'esclusione degli elementi fuori dal frustum, consulta il [manuale della pipeline di rendering](/manuals/render/#frustum-culling).

# Ottimizzazioni specifiche per piattaforma {#platform-specific-optimizations}

## Android Device Performance Framework
Android Dynamic Performance Framework è un insieme di API che consentono ai giochi di interagire più direttamente con i sistemi di gestione dell'energia e della temperatura dei dispositivi Android. Puoi monitorare il comportamento dinamico dei sistemi Android e ottimizzare le prestazioni del gioco a un livello sostenibile che non surriscaldi i dispositivi. Usa l'[estensione Android Dynamic Performance Framework](https://defold.com/extension-adpf/) per monitorare e ottimizzare le prestazioni del tuo gioco Defold sui dispositivi Android.
