---
title: Manuale sulla sicurezza delle applicazioni
brief: Questo manuale tratta diversi ambiti legati alle pratiche di sviluppo sicuro.
---

# Sicurezza delle applicazioni {#application-security}

La sicurezza delle applicazioni è un argomento ampio, che comprende tutto ciò che va dalle pratiche di sviluppo sicuro alla protezione dei contenuti del gioco dopo la pubblicazione. Questo manuale tratta diversi ambiti, inquadrandoli nel contesto della sicurezza delle applicazioni quando si utilizzano il motore, gli strumenti e i servizi Defold:

* Protezione della proprietà intellettuale
* Soluzioni contro i trucchi nei giochi
* Comunicazioni di rete sicure
* Uso di software di terze parti
* Uso dei server di build nel cloud
* Contenuti scaricabili


## Proteggere la tua proprietà intellettuale dal furto {#securing-your-intellectual-property-from-theft}
Una preoccupazione comune tra gli sviluppatori è come proteggere le proprie creazioni dal furto. Dal punto di vista giuridico, il diritto d'autore, i brevetti e i marchi possono essere utilizzati per tutelare i diversi aspetti della proprietà intellettuale dei videogiochi. Il diritto d'autore conferisce al titolare il diritto esclusivo di distribuire l'opera creativa, i brevetti proteggono le invenzioni e i marchi tutelano nomi, simboli e loghi.

Può essere opportuno anche adottare precauzioni tecniche per proteggere il lavoro creativo di un gioco. È tuttavia importante tenere presente che, una volta che il gioco è nelle mani del giocatore, è possibile trovare modi per estrarne gli asset. Ciò può avvenire attraverso l'ingegneria inversa dell'applicazione e dei file del gioco, ma anche usando strumenti per estrarre texture e modelli mentre vengono inviati alla GPU o quando altri asset vengono caricati in memoria.

Per questo motivo, la nostra posizione generale è che, se gli utenti sono determinati a estrarre gli asset di un gioco, riusciranno a farlo.

Gli sviluppatori possono aggiungere protezioni personalizzate per rendere più difficile, __ma non impossibile__, l'estrazione degli asset. In genere si tratta di diversi metodi di crittografia e offuscamento per proteggere e nascondere gli asset del gioco.

### Offuscamento del codice sorgente {#source-code-obfuscation}
L'offuscamento del codice sorgente è un processo automatico che rende deliberatamente difficile la comprensione del codice da parte delle persone, senza influire sull'output del programma. Lo scopo è solitamente proteggerlo dal furto, ma anche rendere più difficile barare.

In Defold è possibile applicare l'offuscamento del codice sorgente come passaggio preliminare alla build oppure come parte integrante del processo di build di Defold. Con l'offuscamento preliminare, il codice sorgente viene offuscato usando uno strumento apposito prima di avviare il processo di build di Defold.

L'offuscamento durante la build, invece, viene integrato nel processo di build mediante un plugin del builder Lua. Un plugin del builder Lua riceve in input il codice sorgente originale e restituisce in output una versione offuscata. Un esempio di offuscamento durante la build è mostrato nell'[estensione Prometheus](https://github.com/defold/extension-prometheus), basata sull'offuscatore Lua Prometheus disponibile su GitHub. Di seguito trovi un esempio di utilizzo di Prometheus per offuscare in modo aggressivo un frammento di codice (tieni presente che questo tipo di offuscamento pesante incide sulle prestazioni del codice Lua durante l'esecuzione):

Esempio:

```
function init(self)
 print("hello")
 test.greet("Bob")
end
```

Output offuscato:

```
local v={"+qdW","ZK0tEKf=";"XP/IX3+="}for o,J in ipairs({{1;3};{1,1},{2,3}})do while J[1]<J[2]do v[J[1]],v[J[2]],J[1],J[2]=v[J[2]],v[J[1]],J[1]+1,J[2]-1 end end local function J(o)return v[o+45816]end do local o={["/"]=9;["8"]=48;["9"]=1;q=38,o=62;V=33;y=43,d=61,B=50,L=54;v=2;["0"]=21,n=31;p=63;R=5;N=3;i=10;e=35;C=7;l=56;a=47,J=58;m=59;["2"]=36;z=11;M=12;Z=26;O=18;["5"]=20;s=8,["4"]=30,P=55;w=4;U=29;Q=28;r=24,h=41;G=45;c=19;W=34,k=57;T=14,t=44,S=0;f=60;F=42,E=27;u=40;X=25,j=17;["3"]=23,b=13;["1"]=53;Y=32,A=22,K=6,["+"]=16,["6"]=46;["7"]=51;I=37;D=52;H=15,x=49,g=39}local J=type local x=string.sub local d=v local l=string.len local W=string.char local L=table.insert local w=table.concat local h=math.floor for v=1,#d,1 do local X=d[v]if J(X)=="string"then local J=l(X)local H={}local S=1 local k=0 local K=0 while S<=J do local v=x(X,S,S)local d=o[v]if d then k=k+d*64^(3-K)K=K+1 if K==4 then K=0 local o=h(k/65536)local v=h((k%65536)/256)local J=k%256 L(H,W(o,v,J))k=0 end elseif v=="="then L(H,W(h(k/65536)))if S>=J or x(X,S+1,S+1)~="="then L(H,W(h((k%65536)/256)))end break end S=S+1 end d[v]=w(H)end end end local function o(o)test[J(-45815)](o)end function init(v)print(J(-45813))o(J(-45814))end
```

### Crittografia delle risorse {#resource-encryption}
Durante il processo di build di Defold, le risorse del gioco vengono elaborate e trasformate in formati adatti all'uso da parte del motore Defold durante l'esecuzione. Le texture vengono compilate nel formato Basis Universal, le collezioni, gli oggetti di gioco e i componenti vengono convertiti da una rappresentazione testuale leggibile a equivalenti binari e il codice sorgente Lua viene elaborato e compilato in bytecode. Altri asset, come i file audio, vengono utilizzati così come sono.

Al termine di questo processo, gli asset vengono aggiunti all'archivio del gioco uno alla volta. L'archivio del gioco è un grande file binario e la posizione di ciascuna risorsa al suo interno viene memorizzata in un file indice dell'archivio. Il formato è documentato [qui](https://github.com/defold/defold/blob/dev/engine/docs/ARCHIVE_FORMAT.md).

Prima di essere aggiunti all'archivio, i file sorgente Lua possono anche essere crittografati. La crittografia predefinita fornita da Defold è un semplice cifrario a blocchi usato per impedire che le stringhe nel codice siano immediatamente visibili quando si ispeziona l'archivio del gioco con uno strumento di visualizzazione di file binari. Non va considerata sicura dal punto di vista crittografico, poiché il codice sorgente di Defold è disponibile su GitHub e la chiave del cifrario è visibile al suo interno.

È possibile aggiungere una crittografia personalizzata ai file sorgente Lua implementando un plugin di crittografia delle risorse. Un plugin di crittografia delle risorse comprende una parte che crittografa le risorse durante il processo di build e una parte che le decrittografa a runtime quando vengono lette dall'archivio del gioco. Un plugin di base per la crittografia delle risorse, utilizzabile come punto di partenza per una soluzione personalizzata, è [disponibile su GitHub](https://github.com/defold/extension-resource-encryption).


### Codificare i valori di configurazione del progetto {#encoding-project-configuration-values}
Il file *game.project* viene incluso così com'è nel bundle dell'applicazione. A volte potresti voler memorizzare chiavi di accesso ad API pubbliche o valori simili, di natura sensibile ma non necessariamente privata. Per rafforzarne la sicurezza, questi valori possono essere inclusi nel binario dell'applicazione invece di essere memorizzati in *game.project*, restando comunque accessibili alle funzioni dell'API Defold, come `sys.get_config_string()` e funzioni analoghe. Per farlo, puoi aggiungere un'estensione nativa nel tuo *game.project* e usare la macro `DM_DECLARE_CONFIGFILE_EXTENSION` per personalizzare il recupero dei valori di configurazione tramite le funzioni dell'API Defold. Un progetto di esempio utilizzabile come punto di partenza è [disponibile su GitHub](https://github.com/defold/example-configfile-extension/tree/master).


## Proteggere il tuo gioco da chi bara {#securing-your-game-against-cheaters}
I trucchi nei videogiochi esistono da quando esiste l'industria dei giochi. Un tempo i codici dei trucchi venivano condivisi nelle riviste di videogiochi più diffuse e per i primi computer domestici venivano vendute apposite cartucce. Con l'evoluzione dell'industria e dei giochi, si sono evoluti anche i giocatori che barano e i loro metodi. Alcuni dei meccanismi più diffusi per barare nei giochi sono:

* Ricreazione dei pacchetti dei contenuti del gioco per inserirvi logica personalizzata
* Alterazioni della velocità per far eseguire un gioco più velocemente o più lentamente del normale
* Automazione e analisi visiva per la mira automatica e i bot
* Iniezione di codice e modifiche alla memoria per alterare punteggi, vite, munizioni e così via

Proteggersi da chi bara è difficile, quasi impossibile. Anche il gioco nel cloud, in cui i giochi vengono eseguiti su server remoti e trasmessi in streaming direttamente al dispositivo dell'utente, non è completamente immune dai trucchi.

Defold non fornisce soluzioni contro i trucchi nel motore o negli strumenti e rimanda questo tipo di intervento a una delle numerose aziende specializzate in soluzioni contro i trucchi nei giochi.


## Proteggere le tue comunicazioni di rete {#securing-your-network-communication}
Le comunicazioni tramite socket e HTTP di Defold supportano connessioni socket sicure. Si consiglia di utilizzare connessioni sicure per qualsiasi comunicazione con un server, per autenticarlo e proteggere la riservatezza e l'integrità dei dati scambiati durante il transito dal client al server e viceversa. Defold utilizza [Mbed TLS](https://github.com/Mbed-TLS/mbedtls), una nota e ampiamente adottata implementazione open source dei protocolli TLS e SSL. Mbed TLS è sviluppata da ARM e dai suoi partner tecnologici.

### Validazione dei certificati SSL {#ssl-certificate-validation}
Per prevenire gli attacchi di tipo man-in-the-middle alle tue comunicazioni di rete, è possibile validare la catena dei certificati durante l'handshake SSL, quando si negozia una connessione con un server. Per farlo, puoi fornire un elenco di chiavi pubbliche al client di rete in Defold. Per ulteriori informazioni sulla protezione delle comunicazioni di rete, consulta la sezione sulla verifica SSL nel [manuale di rete](https://defold.com/manuals/networking/#secure-connections).


## Usare software di terze parti in modo sicuro {#securing-your-use-of-third-party-software}
Sebbene non sia necessario utilizzare librerie di terze parti o estensioni native per creare un gioco, tra gli sviluppatori è ormai molto comune usare asset dell'[Asset Portal](https://defold.com/assets/) ufficiale per accelerare lo sviluppo. L'Asset Portal contiene un'ampia selezione di asset, dalle integrazioni con SDK di terze parti ai gestori di schermate, alle librerie per l'interfaccia utente, alle telecamere e molto altro.

Nessuno degli asset presenti nell'Asset Portal è stato esaminato dalla Defold Foundation e non ci assumiamo alcuna responsabilità per eventuali danni al tuo computer o ad altri dispositivi, né per la perdita di dati derivante dall'uso di asset ottenuti tramite l'Asset Portal. Puoi leggere i dettagli nei nostri [Termini e condizioni](https://defold.com/terms-and-conditions/#3-no-warranties).

Ti consigliamo di esaminare ogni asset prima di usarlo e, dopo averlo ritenuto adatto al tuo progetto, di crearne un fork o una copia per assicurarti che non cambi senza che tu te ne accorga.


## Usare i server di build nel cloud in modo sicuro {#securing-your-use-of-cloud-build-servers}
I server di build nel cloud di Defold (chiamati anche server extender) sono stati creati per aiutare gli sviluppatori ad aggiungere nuove funzionalità al motore Defold senza dover ricostruire il motore stesso. Quando si crea per la prima volta una build di un progetto Defold contenente codice nativo, il codice nativo e le risorse associate vengono inviati ai server di build nel cloud, dove viene creata una versione personalizzata del motore Defold che viene poi restituita allo sviluppatore. Lo stesso processo si applica quando si crea la build di un progetto usando un manifesto dell'applicazione personalizzato per rimuovere dal motore i componenti inutilizzati.

I server di build nel cloud sono ospitati su AWS e configurati secondo le migliori pratiche di sicurezza. La Defold Foundation, tuttavia, non garantisce che i server di build nel cloud soddisfino i tuoi requisiti, siano privi di difetti o virus, siano sicuri o privi di errori, né che il loro utilizzo sia ininterrotto o sicuro. Puoi leggere i dettagli nei nostri [Termini e condizioni](https://defold.com/terms-and-conditions/#3-no-warranties).

Se la sicurezza e la disponibilità dei server di build ti preoccupano, ti consigliamo di configurare server di build privati. Puoi trovare le istruzioni per configurare un tuo server nel [file readme principale](https://github.com/defold/extender) del repository extender su GitHub.


## Proteggere i tuoi contenuti scaricabili {#securing-your-downloadable-content}
Il sistema Live Update di Defold consente agli sviluppatori di escludere contenuti dal bundle principale del gioco per scaricarli e utilizzarli in un secondo momento. Un caso d'uso tipico è scaricare livelli, mappe o mondi aggiuntivi man mano che il giocatore avanza nel gioco.

Quando un contenuto escluso viene scaricato e preparato per l'uso in un gioco, il motore lo verifica prima di utilizzarlo. La verifica comprende una serie di controlli:

* Il formato binario è corretto?
* Il contenuto scaricato è supportato dalla versione del motore attualmente in esecuzione?
* Il contenuto scaricato è completo e non manca alcun file?

Puoi leggere ulteriori dettagli su questo processo nel [manuale di Live Update](https://defold.com/manuals/live-update/#content-verification).
