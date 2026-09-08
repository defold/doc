---
title: Sviluppo con Defold per la piattaforma iOS
brief: Questo manuale spiega come creare build ed eseguire giochi e applicazioni sui dispositivi iOS con Defold.
---

# Sviluppo per iOS {#ios-development}

::: sidenote
La creazione di bundle di giochi per iOS è disponibile solo nella versione per Mac dell'editor Defold.
:::

iOS richiede che _qualsiasi_ applicazione di cui crei una build e che vuoi eseguire sul tuo telefono o tablet _debba_ essere firmata con un certificato e un profilo di provisioning rilasciati da Apple. Questo manuale spiega i passaggi necessari per creare un bundle del tuo gioco per iOS. Durante lo sviluppo, spesso è preferibile eseguire il gioco tramite l'[applicazione di sviluppo](/manuals/dev-app), perché consente di ricaricare a caldo contenuti e codice direttamente sul dispositivo.

## Il processo di firma del codice di Apple {#apples-code-signing-process}

La sicurezza delle applicazioni iOS si basa su diversi componenti. Puoi accedere agli strumenti necessari iscrivendoti al [programma iOS Developer Program di Apple](https://developer.apple.com/programs/). Una volta iscritto, accedi al [Developer Member Center di Apple](https://developer.apple.com/membercenter/index.action).

![Apple Member Center](images/ios/apple_member_center.png)

La sezione *Certificates, Identifiers & Profiles* contiene tutti gli strumenti necessari. Da qui puoi creare, eliminare e modificare:

Certificates
: Certificati crittografici rilasciati da Apple che ti identificano come sviluppatore. Puoi creare certificati di sviluppo o di produzione. I certificati di sviluppo consentono di testare determinate funzionalità, come il meccanismo degli acquisti in-app, in un ambiente di test sandbox. I certificati di produzione vengono usati per firmare l'applicazione finale da caricare sull'App Store. Ti serve un certificato per firmare le applicazioni prima di poterle installare sul dispositivo per i test.

Identifiers
: Identificatori per vari usi. Puoi registrare identificatori con caratteri jolly (ad esempio `some.prefix.*`) utilizzabili con più applicazioni. Gli App ID possono contenere informazioni sui servizi dell'applicazione, ad esempio se l'applicazione abilita l'integrazione con Passbook, Game Center e così via. Questi App ID non possono essere identificatori con caratteri jolly. Perché i servizi dell'applicazione funzionino, l'*identificatore del bundle* della tua applicazione deve corrispondere all'App ID.

Devices
: Ogni dispositivo di sviluppo deve essere registrato con il proprio UDID (Unique Device IDentifier, vedi sotto).

Provisioning Profiles
: I profili di provisioning associano i certificati agli App ID e a un elenco di dispositivi. Stabiliscono quale applicazione di quale sviluppatore può essere installata su quali dispositivi.

Per firmare i tuoi giochi e le tue applicazioni in Defold, servono un certificato valido e un profilo di provisioning valido.

::: sidenote
Alcune operazioni disponibili nella pagina iniziale del Member Center possono essere eseguite anche dall'ambiente di sviluppo Xcode, se lo hai installato.
:::

Identificatore del dispositivo (UDID)
: Puoi trovare l'UDID di un dispositivo iOS collegandolo a un computer tramite Wi-Fi o cavo. Apri Xcode e seleziona <kbd>Window ▸ Devices and Simulators</kbd>. Quando selezioni il dispositivo, vengono visualizzati il numero di serie e l'identificatore.

  ![Dispositivi in Xcode](images/ios/xcode_devices.png)

  Se non hai installato Xcode, puoi trovare l'identificatore in iTunes. Fai clic sull'icona dei dispositivi e seleziona il tuo dispositivo.

  ![Dispositivi in iTunes](images/ios/itunes_devices.png)

  1. Nella pagina *Summary*, individua *Serial Number*.
  2. Fai clic una volta su *Serial Number* per cambiare il campo in *UDID*. Facendo clic più volte, verranno visualizzate diverse informazioni sul dispositivo. Continua a fare clic finché non compare *UDID*.
  3. Fai clic con il pulsante destro sulla lunga stringa UDID e seleziona <kbd>Copy</kbd> per copiare l'identificatore negli appunti, così potrai incollarlo facilmente nel campo UDID quando registri il dispositivo nel Developer Member Center di Apple.

## Sviluppare con un account sviluppatore Apple gratuito {#developing-using-a-free-apple-developer-account}

A partire da Xcode 7, chiunque può installare Xcode e sviluppare gratuitamente sul dispositivo. Non è necessario iscriversi all'iOS Developer Program. Xcode rilascerà automaticamente un certificato che ti identifica come sviluppatore (valido per 1 anno) e un profilo di provisioning per la tua applicazione (valido per una settimana) sul tuo specifico dispositivo.

1. Collega il dispositivo.
2. Installa Xcode.
3. Aggiungi un nuovo account a Xcode e accedi con il tuo Apple ID.
4. Crea un nuovo progetto. Va bene anche una semplice `Single View App`.
5. Seleziona il tuo `Team` (creato automaticamente per te) e assegna un identificatore del bundle all'applicazione.

::: important
Annota l'identificatore del bundle, perché dovrai usare lo stesso identificatore nel tuo progetto Defold.
:::

6. Assicurati che Xcode abbia creato un *Provisioning Profile* e un *Signing Certificate* per l'applicazione.

   ![](images/ios/xcode_certificates.png)

7. Crea la build dell'applicazione sul dispositivo. La prima volta, Xcode ti chiederà di abilitare la modalità sviluppatore e preparerà il dispositivo con il supporto per il debugger. Potrebbe volerci un po' di tempo.
8. Dopo aver verificato che l'applicazione funzioni, trovala sul disco. Puoi vedere il percorso della build nel report di build in `Report Navigator`.

   ![](images/ios/app_location.png)

9. Individua l'applicazione, fai clic con il pulsante destro e seleziona <kbd>Show Package Contents</kbd>.

   ![](images/ios/app_contents.png)

10. Copia il file `embedded.mobileprovision` in una posizione sul disco dove potrai ritrovarlo.

   ![](images/ios/free_provisioning.png)

Questo file di provisioning può essere usato insieme alla tua identità di firma del codice per firmare applicazioni in Defold per una settimana.

Quando il profilo di provisioning scade, devi creare nuovamente la build dell'applicazione in Xcode e ottenere un nuovo file di provisioning temporaneo come descritto sopra.

## Creare un bundle di applicazione iOS {#creating-an-ios-application-bundle}

Quando hai l'identità di firma del codice e il profilo di provisioning, puoi creare dall'editor un bundle di applicazione autonomo per il tuo gioco. Basta selezionare <kbd>Project ▸ Bundle... ▸ iOS Application...</kbd> dal menu.

![Firma del bundle iOS](images/ios/sign_bundle.png)

Seleziona la tua identità di firma del codice, individua il file di provisioning mobile e scegli la variante (Debug o Release). Puoi deselezionare la casella `Sign application` per saltare il processo di firma e firmare manualmente in un secondo momento. Seleziona `Simulator` per creare un bundle `arm64_sim-ios` per il simulatore iOS anziché un bundle per dispositivo.

::: important
I bundle per simulatore funzionano solo nel simulatore iOS sui Mac con Apple Silicon. Non usano un'identità di firma né un profilo di provisioning, quindi le opzioni di firma, installazione e avvio vengono disabilitate quando `Simulator` è selezionato. Installa il bundle con `xcrun simctl` come descritto sotto.
:::

Premi *Create Bundle*: ti verrà chiesto di specificare dove creare il bundle sul computer.

![Bundle di applicazione iOS ipa](images/ios/ipa_file.png){.left}

Specifica l'icona da usare per l'applicazione, lo storyboard della schermata di avvio e altre opzioni nel file delle impostazioni del progetto *game.project*, nella [sezione iOS](/manuals/project-settings/#ios).

### Info.plist personalizzato e rilevamento delle destinazioni locali {#custom-infoplist-and-local-target-discovery}

Il file `Info.plist` integrato per iOS contiene il servizio Bonjour e la descrizione dell'uso della rete locale necessari per il rilevamento automatico delle destinazioni da parte dell'editor nelle build che non sono di release. Un file `Info.plist` personalizzato sostituisce questo manifesto di base integrato. Se usi un manifesto personalizzato per una build di debug e hai bisogno del rilevamento delle destinazioni, della profilazione, dell'hot reload o dello streaming dei log sulla rete locale, includi queste voci:

```xml
{{^variant_release}}
<key>NSBonjourServices</key>
<array>
    <string>_defold._tcp</string>
</array>
<key>NSLocalNetworkUsageDescription</key>
<string>Discover Defold targets on the local network.</string>
{{/variant_release}}
```

La condizione Mustache esclude le voci per il rilevamento dai bundle di release. La stringa che descrive l'utilizzo viene mostrata all'utente da iOS e può essere modificata o localizzata. Rimuovi la condizione solo se l'applicazione di release stessa usa lo stesso servizio Bonjour e le stesse funzionalità di rete locale.

:[Build Variants](../shared/build-variants.md)

## Installare e avviare un bundle su un iPhone collegato {#installing-and-launching-bundle-on-a-connected-iphone}

Puoi installare e avviare il bundle creato usando le caselle `Install on connected device` e `Launch installed app` dell'editor nella finestra di dialogo Bundle:

![Installazione e avvio del bundle iOS](images/ios/install_and_launch.png)

Per usare questa funzionalità, devi avere installato lo strumento a riga di comando [ios-deploy](https://github.com/ios-control/ios-deploy). Il modo più semplice per installarlo è usare Homebrew:
```
$ brew install ios-deploy
```

Se l'editor non riesce a rilevare il percorso di installazione dello strumento ios-deploy, dovrai specificarlo in [Preferences](/manuals/editor-preferences/#tools). 

### Creare uno storyboard {#creating-a-storyboard}

Puoi creare un file storyboard usando Xcode. Avvia Xcode e crea un nuovo progetto. Seleziona iOS e Single View App:

![Creazione del progetto](images/ios/xcode_create_project.png)

Fai clic su Next e procedi alla configurazione del progetto. Inserisci un Product Name:

![Impostazioni del progetto](images/ios/xcode_storyboard_create_project_settings.png)

Fai clic su Create per completare il processo. Il progetto è stato creato e puoi procedere alla creazione dello storyboard:

![Vista del progetto](images/ios/xcode_storyboard_project_view.png)

Trascina e rilascia un'immagine per importarla nel progetto. Poi seleziona `Assets.xcassets` e rilascia l'immagine in `Assets.xcassets`:

![Aggiunta di un'immagine](images/ios/xcode_storyboard_add_image.png)

Apri `LaunchScreen.storyboard` e fai clic sul pulsante più (<kbd>+</kbd>). Digita `imageview` nella finestra di dialogo per trovare il componente ImageView.

![Aggiunta di una vista immagine](images/ios/xcode_storyboard_add_imageview.png)

Trascina il componente Image View sullo storyboard:

![Aggiunta allo storyboard](images/ios/xcode_storyboard_add_imageview_to_storyboard.png)

Seleziona l'immagine che hai aggiunto in precedenza ad `Assets.xcassets` dal menu a discesa Image:

![](images/ios/xcode_storyboard_select_image.png)

Posiziona l'immagine e apporta le altre modifiche necessarie, magari aggiungendo una Label o un altro elemento dell'interfaccia. Quando hai finito, imposta lo schema attivo su **Any iOS Device (arm64)** (o **Generic iOS Device**) e seleziona **Product ▸ Build**. Defold supporta iOS 15.0 e versioni successive sui dispositivi a 64 bit, quindi mantieni la versione minima di destinazione a 15.0 o successiva. Attendi il completamento del processo di build.

Se usi immagini nello storyboard, non verranno incluse automaticamente in `LaunchScreen.storyboardc`. Usa il campo `Bundle Resources` in *game.project* per includere le risorse.
Ad esempio, crea la cartella `LaunchScreen` nel progetto Defold e una cartella `ios` al suo interno (la cartella `ios` serve a includere questi file solo nei bundle per iOS), quindi inserisci i file in `LaunchScreen/ios/`. Aggiungi questo percorso in `Bundle Resources`.

![](images/ios/bundle_res.png)

L'ultimo passaggio consiste nel copiare il file compilato `LaunchScreen.storyboardc` nel progetto Defold. Apri Finder nel percorso seguente e copia il file `LaunchScreen.storyboardc` nel tuo progetto Defold:

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Intermediates.noindex/YOUR-PRODUCT-NAME.build/Debug-iphonesimulator/YOUR-PRODUCT-NAME.build/Base.lproj/LaunchScreen.storyboardc

::: sidenote
L'utente del forum Sergey Lerg ha realizzato [un tutorial video che illustra il processo](https://www.youtube.com/watch?v=6jU8wGp3OwA&feature=emb_logo).
:::

Una volta ottenuto il file storyboard, puoi farvi riferimento da *game.project*.


### Creare un catalogo di asset per le icone {#creating-an-icon-asset-catalog}

Il catalogo di asset è il metodo consigliato da Apple per gestire le icone della tua applicazione. È infatti l'unico modo per fornire l'icona usata nella scheda dell'App Store. Puoi creare un catalogo di asset nello stesso modo di uno storyboard, usando Xcode. Avvia Xcode e crea un nuovo progetto. Seleziona iOS e Single View App:

![Creazione del progetto](images/ios/xcode_create_project.png)

Fai clic su Next e procedi alla configurazione del progetto. Inserisci un Product Name:

![Impostazioni del progetto](images/ios/xcode_icons_create_project_settings.png)

Fai clic su Create per completare il processo. Il progetto è stato creato e puoi procedere alla creazione del catalogo di asset:

![Vista del progetto](images/ios/xcode_icons_project_view.png)

Trascina e rilascia le immagini nei riquadri vuoti che rappresentano le diverse dimensioni di icona supportate:

![Aggiunta delle icone](images/ios/xcode_icons_add_icons.png)

::: sidenote
Non aggiungere icone per Notifications, Settings o Spotlight.
:::

Quando hai finito, imposta lo schema attivo su `Build -> Any iOS Device (arm64)`(o `Generic iOS Device`) e seleziona <kbd>Product</kbd> -> <kbd>Build</kbd>. Attendi il completamento del processo di build.

::: sidenote
Assicurati di creare la build per `Any iOS Device (arm64)` o `Generic iOS Device`, altrimenti riceverai l'errore `ERROR ITMS-90704` quando caricherai la build.
:::

![Build del progetto](images/ios/xcode_icons_build.png)

L'ultimo passaggio consiste nel copiare il file compilato `Assets.car` nel progetto Defold. Apri Finder nel percorso seguente e copia il file `Assets.car` nel tuo progetto Defold:

    /Library/Developer/Xcode/DerivedData/YOUR-PRODUCT-NAME-cbqnwzfisotwygbybxohrhambkjy/Build/Products/Debug-iphoneos/Icons.app/Assets.car

Una volta ottenuto il file del catalogo di asset, puoi farvi riferimento insieme alle icone da *game.project*:

![Aggiunta dell'icona e del catalogo di asset a game.project](images/ios/defold_icons_game_project.png)

::: sidenote
Non è necessario fare riferimento all'icona dell'App Store da *game.project*. Viene estratta automaticamente dal file `Assets.car` durante il caricamento su iTunes Connect.
:::


## Installare un bundle di applicazione iOS {#installing-an-ios-application-bundle}

L'editor scrive un file *.ipa*, che è un bundle di applicazione iOS. Per installare il file sul dispositivo, puoi usare uno dei seguenti strumenti:

* Xcode tramite la finestra `Devices and Simulators`
* Lo strumento a riga di comando [`ios-deploy`](https://github.com/ios-control/ios-deploy)
* [`Apple Configurator 2`](https://apps.apple.com/us/app/apple-configurator-2/) dall'App Store di macOS
* iTunes

Puoi anche usare lo strumento a riga di comando `xcrun simctl` per lavorare con i simulatori iOS disponibili tramite Xcode:

```
# show a list of available devices
xcrun simctl list

# boot an iPhone X simulator
xcrun simctl boot "iPhone X"

# install your.app to a booted simulator
xcrun simctl install booted your.app

# launch the simulator
open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
```

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)


## Informazioni sulla conformità alle norme di esportazione {#export-compliance-information}

Quando invii il tuo gioco all'App Store, ti verrà chiesto di fornire informazioni sulla conformità alle norme di esportazione relative all'uso della crittografia nel gioco. [Apple spiega perché sono necessarie](https://developer.apple.com/documentation/security/complying_with_encryption_export_regulations):

"Quando invii la tua applicazione a TestFlight o all'App Store, la carichi su un server negli Stati Uniti. Se distribuisci la tua applicazione al di fuori degli Stati Uniti o del Canada, l'applicazione è soggetta alle leggi statunitensi sull'esportazione, indipendentemente da dove ha sede la tua entità giuridica. Se la tua applicazione usa, accede a, contiene, implementa o incorpora la crittografia, ciò è considerato un'esportazione di software crittografico. Questo significa che la tua applicazione è soggetta ai requisiti statunitensi di conformità alle norme di esportazione, oltre che ai requisiti di conformità alle norme di importazione dei paesi in cui distribuisci l'applicazione."

Il motore di gioco Defold usa la crittografia per i seguenti scopi:

* Effettuare chiamate su canali sicuri (ad esempio HTTPS e SSL)
* Proteggere il copyright del codice Lua (per impedirne la duplicazione)

Questi usi della crittografia nel motore Defold sono esenti dall'obbligo di presentare documentazione di conformità alle norme di esportazione secondo la legislazione degli Stati Uniti e dell'Unione europea. La maggior parte dei progetti Defold mantiene questa esenzione, ma l'aggiunta di altri metodi crittografici potrebbe modificarne lo stato. È tua responsabilità assicurarti che il progetto soddisfi i requisiti di queste leggi e le regole dell'App Store. Per ulteriori informazioni, consulta la [panoramica sulla conformità alle norme di esportazione](https://help.apple.com/app-store-connect/#/dev88f5c7bf9) di Apple.

Se ritieni che il tuo progetto sia esente, imposta la chiave [`ITSAppUsesNonExemptEncryption`](https://developer.apple.com/documentation/bundleresources/information-property-list/itsappusesnonexemptencryption) su `False` nel file `Info.plist` del progetto; consulta [Manifesti delle applicazioni](/manuals/extensions-manifest-merge-tool) per ulteriori dettagli.

## FAQ
:[iOS FAQ](../shared/ios-faq.md)
