---
title: Eseguire l'app di sviluppo sul dispositivo
brief: Questo manuale spiega come installare l'app di sviluppo sul dispositivo per lo sviluppo iterativo direttamente sul dispositivo.
---

# L'app di sviluppo per dispositivi mobili {#the-mobile-development-app}

L'app di sviluppo ti permette di inviarle contenuti tramite Wi-Fi. Questo riduce notevolmente il tempo necessario per ogni iterazione, perché non devi creare e installare un bundle ogni volta che vuoi provare le tue modifiche. Installa l'app di sviluppo sui tuoi dispositivi, avviala e poi seleziona il dispositivo come destinazione della build nell'editor.

## Installare un'app di sviluppo {#installing-a-development-app}

Qualsiasi applicazione iOS o Android per cui è stato creato un bundle in modalità Debug può funzionare come app di sviluppo. Questa è, infatti, la soluzione consigliata, perché l'app di sviluppo avrà le impostazioni del progetto corrette e userà le stesse [estensioni native](/manuals/extensions/) del progetto su cui stai lavorando. 

È possibile creare un bundle della variante Debug del progetto senza alcun contenuto. Usa questa opzione per creare una versione dell'applicazione con le estensioni native, adatta allo sviluppo iterativo descritto in questo manuale.

![Bundle senza contenuti](images/dev-app/contentless-bundle.png)

### Installare su iOS {#installing-on-ios}

Segui le [istruzioni nel manuale di iOS](/manuals/ios/#creating-an-ios-application-bundle) per creare un bundle per iOS. Assicurati di selezionare Debug come variante!

### Installare su Android {#installing-on-android}

Segui le [istruzioni nel manuale di Android](https://defold.com/manuals/android/#creating-an-android-application-bundle) per creare un bundle per Android.

## Avviare il gioco {#launching-your-game}

Per avviare il gioco sul dispositivo, l'app di sviluppo e l'editor devono potersi connettere tramite la stessa rete Wi-Fi o tramite USB (vedi sotto).

1. Assicurati che l'editor sia avviato e in esecuzione.
2. Avvia l'app di sviluppo sul dispositivo.
3. Seleziona il dispositivo in <kbd>Project ▸ Targets</kbd> nell'editor.
4. Seleziona <kbd>Project ▸ Build</kbd> per eseguire il gioco. L'avvio potrebbe richiedere un po' di tempo, perché il contenuto del gioco viene trasmesso al dispositivo tramite la rete.
5. Mentre il gioco è in esecuzione, puoi usare l'[hot reload](/manuals/hot-reload/) come al solito.

### Connettersi a un dispositivo iOS tramite USB su Windows {#connecting-to-an-ios-device-using-usb-on-windows}

Per connetterti tramite USB su Windows a un'app di sviluppo in esecuzione su un dispositivo iOS, devi prima [installare iTunes](https://www.apple.com/lae/itunes/download/). Dopo aver installato iTunes, devi anche [attivare Personal Hotspot](https://support.apple.com/en-us/HT204023) sul dispositivo iOS dal menu Settings. Se compare l'avviso "Trust This Computer?", tocca Trust. Il dispositivo dovrebbe ora comparire in <kbd>Project ▸ Targets</kbd> quando l'app di sviluppo è in esecuzione.

### Connettersi a un dispositivo iOS tramite USB su Linux {#connecting-to-an-ios-device-using-usb-on-linux}

Su Linux, quando il dispositivo è connesso tramite USB, devi attivare Personal Hotspot sul dispositivo dal menu Settings. Se compare l'avviso "Trust This Computer?", tocca Trust. Il dispositivo dovrebbe ora comparire in <kbd>Project ▸ Targets</kbd> quando l'app di sviluppo è in esecuzione.

### Connettersi a un dispositivo iOS tramite USB su macOS {#connecting-to-an-ios-device-using-usb-on-macos}

Nelle versioni più recenti di iOS, quando il dispositivo è connesso tramite USB su macOS, viene aperta automaticamente una nuova interfaccia Ethernet tra il dispositivo e il computer. Il dispositivo dovrebbe comparire in <kbd>Project ▸ Targets</kbd> quando l'app di sviluppo è in esecuzione.

Nelle versioni meno recenti di iOS, quando il dispositivo è connesso tramite USB su macOS, devi attivare Personal Hotspot sul dispositivo dal menu Settings. Se compare l'avviso "Trust This Computer?", tocca Trust. Il dispositivo dovrebbe ora comparire in <kbd>Project ▸ Targets</kbd> quando l'app di sviluppo è in esecuzione.

### Connettersi a un dispositivo Android tramite USB su macOS {#connecting-to-an-android-device-using-usb-on-macos}

Su macOS è possibile connettersi tramite USB a un'app di sviluppo in esecuzione su un dispositivo Android quando il dispositivo è impostato su USB Tethering Mode. Su macOS devi installare un driver di terze parti come [HoRNDIS](https://joshuawise.com/horndis#available_versions). Dopo aver installato HoRNDIS, devi anche consentirne l'esecuzione nelle impostazioni Security & Privacy. Una volta attivato USB Tethering, il dispositivo comparirà in <kbd>Project ▸ Targets</kbd> quando l'app di sviluppo è in esecuzione.

### Connettersi a un dispositivo Android tramite USB su Windows o Linux {#connecting-to-an-android-device-using-usb-on-windows-or-linux}

Su Windows e Linux è possibile connettersi tramite USB a un'app di sviluppo in esecuzione su un dispositivo Android quando il dispositivo è impostato su USB Tethering Mode. Una volta attivato USB Tethering, il dispositivo comparirà in <kbd>Project ▸ Targets</kbd> quando l'app di sviluppo è in esecuzione.

## Risoluzione dei problemi {#troubleshooting}

Impossibile scaricare l'applicazione
: Assicurati che l'UDID del dispositivo sia incluso nel profilo di provisioning usato per firmare l'app.

Il dispositivo non compare nel menu Targets
: Assicurati che il dispositivo sia connesso alla stessa rete Wi-Fi del computer. Assicurati che la build dell'app di sviluppo sia stata creata in modalità Debug.

Il gioco non si avvia e compare un messaggio che segnala una mancata corrispondenza tra le versioni
: Questo accade quando hai aggiornato l'editor alla versione più recente. Devi creare una build e installare una nuova versione.
