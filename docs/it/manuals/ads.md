---
title: Mostrare annunci pubblicitari in Defold
brief: Mostrare annunci pubblicitari di vario tipo è un modo comune per monetizzare i giochi web e per dispositivi mobili. Questo manuale illustra diversi modi per monetizzare il tuo gioco con gli annunci pubblicitari.
---

# Annunci pubblicitari {#ads}

Gli annunci pubblicitari sono diventati un modo molto comune per monetizzare i giochi web e per dispositivi mobili, dando origine a un settore da miliardi di dollari. Come sviluppatore, vieni pagato in base al numero di persone che guardano gli annunci mostrati nel tuo gioco. Di solito il principio è semplice: più visualizzazioni equivalgono a maggiori guadagni, ma anche altri fattori influiscono su quanto ricevi:

* La qualità degli annunci - gli annunci pertinenti hanno maggiori probabilità di stimolare l'interazione e attirare l'attenzione dei tuoi giocatori.
* Il formato degli annunci - i banner di solito rendono meno, mentre gli annunci a schermo intero guardati dall'inizio alla fine rendono di più.
* La rete pubblicitaria - l'importo che ricevi varia da una rete pubblicitaria all'altra.

::: sidenote
CPM = Costo per mille. L'importo che un inserzionista paga per mille visualizzazioni. Il CPM varia a seconda della rete pubblicitaria e del formato degli annunci.
:::

## Formati {#formats}

Nei giochi si possono utilizzare molti formati pubblicitari diversi. Tra i più comuni ci sono i banner, gli annunci interstitial e gli annunci con ricompensa:

### Annunci banner {#banner-ads}

Gli annunci banner si basano su testo, immagini o video e occupano una parte relativamente piccola dello schermo, di solito in alto o in basso. Sono molto facili da implementare e si adattano molto bene ai giochi casual con una singola schermata, in cui è facile riservare un'area dello schermo alla pubblicità. I banner massimizzano l'esposizione degli annunci mentre gli utenti giocano senza interruzioni.

### Annunci interstitial {#interstitial-ads}

Gli annunci interstitial sono contenuti di grandi dimensioni a schermo intero con animazioni e, talvolta, anche contenuti *multimediali avanzati* interattivi. In genere vengono mostrati tra un livello e l'altro o tra una sessione di gioco e l'altra, poiché questi sono momenti di pausa naturali nell'esperienza di gioco. Di solito gli annunci interstitial generano meno visualizzazioni dei banner, ma il costo (CPM) è molto più alto, con ricavi pubblicitari complessivi significativi.

### Annunci con ricompensa {#rewarded-ads}

Gli annunci con ricompensa (noti anche come annunci incentivati) sono facoltativi e quindi meno invasivi di molte altre forme di pubblicità. Di solito sono contenuti a schermo intero, come gli annunci interstitial. L'utente può scegliere una ricompensa in cambio della visualizzazione dell'annuncio, per esempio *bottino*, monete, vite, tempo o un'altra valuta o vantaggio all'interno del gioco. Gli annunci con ricompensa hanno generalmente il costo (CPM) più alto, ma il numero di visualizzazioni dipende direttamente dalla percentuale di utenti che scelgono di guardarli. Questi annunci danno ottimi risultati solo se le ricompense hanno un valore sufficiente e vengono offerte al momento giusto.


## Reti pubblicitarie {#ad-networks}

Il [Defold Asset Portal](/tags/stars/ads/) contiene diversi asset che si integrano con i fornitori di annunci pubblicitari:

* [AdMob](https://defold.com/assets/admob-defold/) - Mostra annunci utilizzando la rete Google AdMob.
* [AppLovin MAX](https://defold.com/extension-applovin/) - Mostra annunci utilizzando la mediazione pubblicitaria di AppLovin MAX.
* [Facebook Instant Games](https://defold.com/assets/facebookinstantgames/) - Mostra annunci nel tuo Facebook Instant Game.
* [LevelPlay](https://defold.com/extension-levelplay/) - Mostra annunci utilizzando la mediazione pubblicitaria di Unity LevelPlay.
* [Unity Ads](https://defold.com/assets/defvideoads/) - Mostra annunci utilizzando la rete Unity Ads.


# Come integrare gli annunci nel tuo gioco {#how-to-integrate-ads-in-your-game}

Una volta scelta la rete pubblicitaria da integrare nel tuo gioco, devi seguire le istruzioni di installazione e utilizzo dello specifico *asset*. Di solito il primo passo consiste nell'aggiungere l'estensione come [dipendenza del progetto](/manuals/libraries/#setting-up-library-dependencies). Dopo aver aggiunto l'asset al progetto, puoi procedere con l'integrazione e chiamare le funzioni specifiche dell'asset per caricare e mostrare gli annunci.


# Combinare annunci e acquisti in-app {#combining-ads-and-in-app-purchases}

Nei giochi per dispositivi mobili è piuttosto comune offrire un [acquisto in-app](/manuals/iap) per eliminare definitivamente gli annunci.


## Per saperne di più {#learn-more}

Esistono molte risorse online per imparare a ottimizzare i ricavi pubblicitari:

* Google AdMob [Monetizzare i giochi per dispositivi mobili con gli annunci](https://admob.google.com/home/resources/monetize-mobile-game-with-ads/)
* Game Analytics [Formati pubblicitari più diffusi e come utilizzarli](https://gameanalytics.com/blog/popular-mobile-game-ad-formats.html)
* deltaDNA [Pubblicare annunci nei giochi: 10 consigli degli esperti](https://deltadna.com/blog/ad-serving-in-games-10-tips/)
