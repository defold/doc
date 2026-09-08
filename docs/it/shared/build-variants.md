## Varianti di build {#build-variants}

Quando crei il bundle di un gioco, devi scegliere quale tipo di motore usare. Hai tre opzioni di base:

  * Debug
  * Release
  * Headless

Queste diverse versioni sono anche indicate come `Build variants`

::: sidenote
Quando scegli <kbd>Project ▸ Build</kbd> ottieni sempre la versione di debug.
:::


### Debug

Questo tipo di eseguibile viene generalmente usato durante lo sviluppo di un gioco perché include diverse funzionalità utili per il debug:

* Profilatore - Serve a raccogliere contatori delle prestazioni e dell'utilizzo. Scopri come usare il profilatore nel [manuale sulla profilazione](/manuals/profiling/).
* Registrazione dei log - Quando la registrazione dei log è abilitata, il motore registra informazioni sul sistema, avvisi ed errori. Il motore produce anche i log generati dalla funzione Lua `print()` e dalle estensioni native che usano `dmLogInfo()`, `dmLogError()` e così via. Scopri come leggere questi log nel [manuale sui log del gioco e del sistema](https://defold.com/manuals/debugging-game-and-system-logs/).
* Hot reload - L'hot reload è una potente funzionalità che permette a uno sviluppatore di ricaricare le risorse mentre il gioco è in esecuzione. Scopri come usarla nel [manuale sull'hot reload](https://defold.com/manuals/hot-reload/).
* Servizi del motore - Puoi connetterti a una versione di debug di un gioco e interagire con essa attraverso diverse porte TCP aperte e vari servizi. Questi servizi comprendono la funzionalità di hot reload, l'accesso remoto ai log e il profilatore menzionati sopra, oltre ad altri servizi per interagire a distanza con il motore. Scopri di più sui servizi del motore [nella documentazione per gli sviluppatori](https://github.com/defold/defold/blob/dev/engine/docs/DEBUG_PORTS_AND_SERVICES.md).


### Release

In questa variante le funzionalità di debug sono disabilitate. Scegli questa opzione quando il gioco è pronto per essere pubblicato in uno store di applicazioni o distribuito ai giocatori in altri modi. È sconsigliato pubblicare un gioco con le funzionalità di debug abilitate per diversi motivi:

* Le funzionalità di debug occupano un po' di spazio nel file binario e [è buona pratica cercare di mantenere il più possibile ridotte le dimensioni del file binario di un gioco pubblicato](https://defold.com/manuals/optimization/#optimize-application-size).
* Le funzionalità di debug richiedono anche un po' di tempo della CPU. Questo può influire sulle prestazioni del gioco se un utente dispone di hardware di fascia bassa. Sui telefoni cellulari, il maggiore utilizzo della CPU contribuisce anche al riscaldamento e al consumo della batteria.
* Le funzionalità di debug possono rivelare informazioni sul gioco che non dovrebbero essere accessibili ai giocatori, per ragioni legate alla sicurezza o alla prevenzione di trucchi e frodi.


### Headless

Questo eseguibile funziona senza grafica né audio. Ciò significa che puoi eseguire i test unitari e gli smoke test del gioco su un server di integrazione continua (CI), o persino usarlo come server di gioco nel cloud.