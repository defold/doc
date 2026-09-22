## Dimensione dell'heap (HTML5) {#heap-size-html5}
Puoi configurare la dimensione dell'heap di un gioco HTML5 realizzato con Defold tramite il [campo `heap_size`](/manuals/project-settings/#heap-size) in *game.project*. Assicurati di ottimizzare l'utilizzo della memoria del gioco e di impostare la dimensione dell'heap al minimo necessario.

Per i giochi piccoli, un heap di 32 MB è un obiettivo raggiungibile. Per i giochi più grandi, punta a 64–128 MB. Se, per esempio, sei a 58 MB e non sono possibili ulteriori ottimizzazioni, puoi scegliere 64 MB senza pensarci troppo. Non esiste una dimensione obiettivo rigida: dipende dal gioco. Cerca semplicemente di ridurre le dimensioni, scegliendo idealmente valori che siano potenze di due. 

Per controllare l'utilizzo attuale dell'heap, puoi avviare il gioco e giocare nel livello o nella sezione che richiede più risorse, monitorando l'utilizzo della memoria:

```lua
if html5 then
    local mem = tonumber(html5.run("HEAP8.length") / 1024 / 1024)
    print(mem)
end
```

Puoi anche aprire gli strumenti per sviluppatori del browser e scrivere quanto segue nella console:

```js
HEAP8.length / 1024 / 1024
```

Se l'utilizzo della memoria rimane a 32 MB, ottimo! Altrimenti, segui i passaggi per [ottimizzare le dimensioni del motore stesso e degli asset di grandi dimensioni, come suoni e texture](/manuals/optimization-size).
