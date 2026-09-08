---
title: Linee guida per il porting e la pubblicazione
brief: Questo manuale illustra alcuni aspetti da considerare quando adatti un gioco a una nuova piattaforma o lo pubblichi per la prima volta.
---

# Linee guida per il porting e la pubblicazione {#porting-and-release-guidelines}

Questa pagina contiene una guida e un elenco di controllo degli aspetti da considerare quando pubblichi un gioco o lo adatti a una nuova piattaforma.

Adattare un gioco Defold a una nuova piattaforma o pubblicarlo per la prima volta è in genere un processo semplice. In teoria basta assicurarsi che le sezioni pertinenti del file *game.project* siano configurate, ma per sfruttare al meglio ogni piattaforma è consigliabile adattare il gioco alle sue caratteristiche specifiche.


## Input
Assicurati di adattare il gioco ai metodi di input della piattaforma. Valuta l'aggiunta del supporto per i [gamepad](/manuals/input-gamepads) se la piattaforma li supporta! Assicurati inoltre che il gioco disponga di un menu di pausa: se un controller si disconnette all'improvviso, il gioco dovrebbe essere messo in pausa!

## Localizzazione {#localization}
Traduci tutti i testi del gioco. Per la pubblicazione in Europa e nelle Americhe, valuta una traduzione almeno nelle lingue EFIGS (inglese, francese, italiano, tedesco e spagnolo). Assicurati che sia possibile passare facilmente da una lingua all'altra all'interno del gioco (tramite il menu di pausa).

::: important
Solo iOS: assicurati di specificare [Localizations](/manuals/project-settings/#localizations) in `game.project`, poiché `sys.get_info()` non restituirà mai una lingua che non sia presente in questo elenco.
:::

Traduci i testi della pagina dello store: questo avrà un effetto positivo sulle vendite! Alcune piattaforme richiedono che i testi della pagina dello store siano tradotti nella lingua di ciascun paese in cui il gioco è disponibile.

## Materiali per lo store {#store-materials}

### Icona dell'app {#app-icon}
Assicurati che il tuo gioco si distingua dalla concorrenza. L'icona è spesso il primo punto di contatto con i potenziali giocatori. Dovrebbe essere facile da individuare in una pagina piena di icone di giochi.

### Banner e immagini dello store {#store-banners-and-images}
Assicurati di usare immagini d'impatto e coinvolgenti per il tuo gioco. Può valere la pena investire del denaro nella collaborazione con un artista per creare immagini che attirino i giocatori.


## Salvataggi del gioco {#save-games}

### Salvataggi su desktop, dispositivi mobili e web {#save-games-on-desktop-mobile-and-web}
I salvataggi del gioco e gli altri dati di stato possono essere memorizzati usando la funzione dell'API Defold `sys.save(filename, data)` e caricati usando `sys.load(filename)`. Puoi usare `sys.get_save_file(application_id, name)` per ottenere il percorso di una posizione specifica del sistema operativo in cui salvare i file, in genere nella cartella personale dell'utente che ha effettuato l'accesso.

### Salvataggi su console {#save-games-on-console}
L'uso di `sys.get_save_file()` e `sys.save()` funziona bene sulla maggior parte delle piattaforme, ma sulle console è consigliabile adottare un approccio diverso. Le piattaforme console associano in genere un utente a ciascun controller collegato; di conseguenza, i salvataggi del gioco, gli obiettivi e le altre funzionalità dovrebbero essere associati al rispettivo utente.

Gli eventi di input del gamepad contengono un ID utente che può essere usato per associare le azioni di un controller a un utente della console.

Le piattaforme console e le relative estensioni native espongono funzioni API specifiche della piattaforma per salvare e caricare i dati associati a un determinato utente. Usa queste API per salvare e caricare dati su console.

Le API delle piattaforme console per le operazioni sui file sono in genere asincrone. Quando sviluppi un gioco multipiattaforma destinato anche alle console, è consigliabile progettarlo in modo che tutte le operazioni sui file siano asincrone, indipendentemente dalla piattaforma. Esempio:

```lua
local function save_game(data, user_id, cb)
	if console then
		local filename = "savegame"
		consoleapi.save(user_id, filename, data, cb)
	else
		local filename = sys.get_save_file("mygame", "savegame" .. user_id)
		local success = sys.save(filename, data)
		cb(success)
	end
end
```


## Artefatti di build {#build-artifacts}

Assicurati di [generare i simboli di debug](/manuals/debugging-native-code/#symbolicate-a-callstack) per ogni versione pubblicata, in modo da poter analizzare i crash. Conservali insieme al bundle dell'applicazione.

## Ottimizzazione dell'applicazione {#application-optimizations}

Leggi il [manuale sull'ottimizzazione](/manuals/optimization) per sapere come ottimizzare l'applicazione in termini di prestazioni, dimensioni, uso della memoria e consumo della batteria.



## Prestazioni {#performance}
Esegui sempre i test sull'hardware di destinazione! Controlla le prestazioni del gioco e ottimizzalo se necessario. Usa il [profilatore](/manuals/profiling) per individuare i colli di bottiglia nel codice.


## Risoluzione dello schermo e frequenza di aggiornamento {#screen-resolution-and-refresh-rate}
Per le piattaforme con orientamento e risoluzione dello schermo fissi, verifica che il gioco funzioni con la risoluzione e il rapporto d'aspetto dello schermo della piattaforma di destinazione. Per le piattaforme con risoluzione dello schermo e rapporto d'aspetto variabili, verifica che il gioco funzioni con diverse risoluzioni e rapporti d'aspetto. Tieni conto del tipo di [proiezione della vista](/manuals/render/#default-view-projection) usato nello script di rendering e nella camera.

Per le piattaforme mobili, blocca l'orientamento dello schermo in *game.project* oppure assicurati che il gioco funzioni sia in modalità orizzontale sia in modalità verticale.

* **Dimensioni dello schermo** - Tutto viene visualizzato correttamente su uno schermo più grande o più piccolo rispetto alla larghezza e all'altezza predefinite impostate in *game.project*?
  * La proiezione usata nello script di rendering e i layout usati nella GUI influiscono su questo aspetto.
* **Rapporti d'aspetto** - Tutto viene visualizzato correttamente su uno schermo con un rapporto d'aspetto diverso da quello predefinito, ricavato dalla larghezza e dall'altezza impostate in *game.project*?
  * La proiezione usata nello script di rendering e i layout usati nella GUI influiscono su questo aspetto.
* **Frequenza di aggiornamento** - Il gioco funziona bene su uno schermo con una frequenza di aggiornamento superiore a 60 Hz?
  * La sincronizzazione verticale e l'intervallo di scambio nella sezione Display di *game.project* 


## Telefoni cellulari con notch o fotocamere in un foro nello schermo {#mobile-phones-and-notch-and-hole-punch-cameras}
È sempre più comune usare una piccola apertura nello schermo per ospitare la fotocamera anteriore e i sensori (nota anche come notch o foro per la fotocamera). Quando adatti un gioco ai dispositivi mobili, assicurati che le informazioni essenziali rimangano all'interno dell'area sicura della piattaforma.

Defold offre un supporto integrato per l'area sicura su Android e iOS. Imposta `gui.safe_area_mode` in *game.project* per controllare quali margini opposti dell'area sicura influiscono sull'adattamento della GUI. `none` è il valore predefinito e ignora i margini; `long` applica quelli sinistro e destro in modalità orizzontale e quelli superiore e inferiore in modalità verticale; `short` applica la coppia opposta; `both` applica tutti e quattro i margini. Uno script GUI può sovrascrivere la modalità del progetto per la propria scena con [`gui.set_safe_area_mode()`](/ref/gui/#gui.set_safe_area_mode). Per una logica personalizzata della GUI o del rendering, [`window.get_safe_area()`](/ref/window/#window.get_safe_area) restituisce il rettangolo dell'area sicura e i singoli margini dai bordi. Le piattaforme prive di margini integrati per l'area sicura restituiscono l'intera finestra e margini pari a zero.

L'[estensione Safe Area](/extension-safearea) rimane un'alternativa per i progetti meno recenti o per i flussi di lavoro che richiedono comportamenti aggiuntivi rispetto alle API integrate; non è necessaria per la gestione standard dell'area sicura su Android e iOS.


## Linee guida specifiche per piattaforma {#platform-specific-guidelines}

### Android
Assicurati di conservare il tuo [keystore](/manuals/android/#creating-a-keystore) in un luogo sicuro, così da poter aggiornare il gioco.


### Console {#consoles}
Conserva il bundle completo di ogni versione. Questi file ti serviranno se vorrai creare una patch per il gioco.


### Nintendo Switch
Integra il codice specifico della piattaforma: per Nintendo Switch è disponibile un'estensione separata con alcune funzionalità di supporto per la selezione dell'utente e altre operazioni.

Defold per Nintendo Switch usa Vulkan come backend grafico: assicurati di testare il gioco usando il [backend grafico Vulkan](https://github.com/defold/extension-vulkan).


### PlayStation®4
Integra il codice specifico della piattaforma: per PlayStation®4 è disponibile un'estensione separata con alcune funzionalità di supporto per la selezione dell'utente e altre operazioni.


### HTML5
Giocare a giochi web sui telefoni cellulari è sempre più diffuso: cerca di far funzionare bene il gioco anche in un browser mobile! È inoltre importante ricordare che ci si aspetta che i giochi web si carichino rapidamente! Assicurati di ottimizzare le dimensioni del gioco. Considera anche l'esperienza di caricamento nel suo complesso, per evitare di perdere giocatori inutilmente.

Nel 2018 i browser hanno introdotto una regola per la riproduzione automatica dei suoni che impedisce ai giochi e agli altri contenuti web di riprodurre audio finché non si verifica un evento di interazione dell'utente (tocco, pulsante, gamepad e così via). È importante tenerne conto quando adatti il gioco a HTML5 e avviare la riproduzione di suoni e musica solo alla prima interazione dell'utente. I tentativi di riprodurre suoni prima di qualsiasi interazione dell'utente vengono registrati come errori nella console per sviluppatori del browser, ma non influiscono sul gioco.

Assicurati inoltre di mettere in pausa tutti i suoni in riproduzione mentre il gioco mostra annunci pubblicitari.
