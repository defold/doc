---
title: Sviluppo con Defold per la piattaforma Android
brief: Questo manuale descrive come creare build ed eseguire applicazioni Defold sui dispositivi Android
---

# Sviluppo per Android {#android-development}

I dispositivi Android consentono di eseguire liberamente le proprie applicazioni. È molto semplice creare una build del gioco e copiarla su un dispositivo Android. Questo manuale illustra i passaggi necessari per creare un bundle del gioco per Android. Durante lo sviluppo, spesso è preferibile eseguire il gioco tramite l'[applicazione di sviluppo](/manuals/dev-app), poiché consente di ricaricare a caldo contenuti e codice direttamente sul dispositivo.

## Processo di firma per Android e Google Play {#android-and-google-play-signing-process}

Android richiede che tutti gli APK siano firmati digitalmente con un certificato prima di essere installati su un dispositivo o aggiornati. Se utilizzi gli Android App Bundle, devi firmare solo il bundle dell'applicazione prima di caricarlo nella Play Console; [Play App Signing](https://developer.android.com/studio/publish/app-signing#app-signing-google-play) si occupa del resto. Puoi comunque firmare manualmente l'applicazione per caricarla su Google Play, su altri store di applicazioni o per distribuirla al di fuori di qualsiasi store.

Quando crei un bundle di un'applicazione Android dall'editor Defold o dallo [strumento a riga di comando](/manuals/bob), puoi fornire un keystore (contenente il certificato e la chiave) e la relativa password, che verranno utilizzati per firmare l'applicazione. Se non li fornisci, Defold genera un keystore di debug e lo utilizza per firmare il bundle dell'applicazione.

::: important
Non caricare **mai** l'applicazione su Google Play se è stata firmata con un keystore di debug. Utilizza sempre un keystore dedicato che hai creato personalmente.
:::

## Creazione di un keystore {#creating-a-keystore}

::: sidenote
Defold utilizza un keystore per il processo di firma Android. [Ulteriori informazioni sono disponibili in questo post sul forum](https://forum.defold.com/t/upcoming-change-to-the-android-build-pipeline/66084).
:::

Puoi creare un keystore [utilizzando Android Studio](https://developer.android.com/studio/publish/app-signing#generate-key) oppure da un terminale/prompt dei comandi:

```bash
keytool -genkey -v -noprompt -dname "CN=John Smith, OU=Area 51, O=US Air Force, L=Unknown, ST=Nevada, C=US" -keystore mykeystore.keystore -storepass 5Up3r_53cR3t -alias myAlias -keyalg RSA -validity 9125
```

Questo comando crea un file keystore chiamato `mykeystore.keystore`, contenente una chiave e un certificato. L'accesso alla chiave e al certificato sarà protetto dalla password `5Up3r_53cR3t`. La chiave e il certificato saranno validi per 25 anni (9125 giorni). La chiave e il certificato generati saranno identificati dall'alias `myAlias`.

::: important
Assicurati di conservare il keystore e la relativa password in un luogo sicuro. Se firmi e carichi personalmente le applicazioni su Google Play e perdi il keystore o la sua password, non potrai più aggiornare l'applicazione su Google Play. Puoi evitare questo problema utilizzando Google Play App Signing e lasciando che sia Google a firmare le applicazioni per te.
:::


## Creazione di un bundle di un'applicazione Android {#creating-an-android-application-bundle}

L'editor consente di creare facilmente un bundle autonomo del gioco. Prima di creare il bundle, puoi specificare le icone da utilizzare per l'applicazione, impostare il codice di versione e altri parametri nel [file delle impostazioni del progetto](/manuals/project-settings/#android) *game.project*.

Per creare il bundle, seleziona <kbd>Project ▸ Bundle... ▸ Android Application...</kbd> dal menu.

Se vuoi che l'editor crei automaticamente certificati di debug casuali, lascia vuoti i campi *Keystore* e *Keystore password*:

![Firma del bundle Android](images/android/sign_bundle.png)

Se vuoi firmare il bundle con un keystore specifico, indica *Keystore* e *Keystore password*. Il file *Keystore* deve avere l'estensione `.keystore`, mentre la password deve essere salvata in un file di testo con estensione `.txt`. Puoi anche specificare una *Key password* se la chiave nel keystore utilizza una password diversa da quella del keystore stesso:

![Firma del bundle Android](images/android/sign_bundle2.png)

Defold supporta la creazione di file APK e AAB. Seleziona APK o AAB dal menu a discesa *Bundle Format*.

Premi <kbd>Create Bundle</kbd> dopo aver configurato le impostazioni del bundle dell'applicazione. Ti verrà quindi chiesto di specificare dove creare il bundle sul computer.

![File del pacchetto dell'applicazione Android](images/android/apk_file.png)

:[Build Variants](../shared/build-variants.md)

### Installazione di un bundle di un'applicazione Android {#installing-an-android-application-bundle}

#### Installazione di un APK {#installing-an-apk}

Un file *`.apk`* può essere copiato sul dispositivo con lo strumento `adb`, oppure caricato su Google Play tramite la [console per sviluppatori di Google Play](https://play.google.com/apps/publish/).

:[Android ADB](../shared/android-adb.md)

```
$ adb install Defold\ examples.apk
4826 KB/s (18774344 bytes in 3.798s)
  pkg: /data/local/tmp/my_app.apk
Success
```

#### Installazione di un APK dall'editor {#installing-an-apk-using-editor}

Puoi installare e avviare un file *`.apk`* utilizzando le caselle di controllo "Install on connected device" e "Launch installed app" dell'editor nella finestra di dialogo Bundle:

![Installazione e avvio dell'APK](images/android/install_and_launch.png)

Per utilizzare questa funzionalità, devi avere *ADB* installato e *USB debugging* abilitato sul dispositivo collegato. Se l'editor non riesce a rilevare il percorso di installazione dello strumento a riga di comando ADB, devi specificarlo in [Preferences](/manuals/editor-preferences/#tools).

#### Installazione di un AAB {#installing-an-aab}

Un file *.aab* può essere caricato su Google Play tramite la [console per sviluppatori di Google Play](https://play.google.com/apps/publish/). Puoi anche generare un file *`.apk`* da un file *.aab* per installarlo localmente utilizzando [Android bundletool](https://developer.android.com/studio/command-line/bundletool).

## Autorizzazioni {#permissions}

Il motore Defold richiede diverse autorizzazioni affinché tutte le sue funzionalità possano operare. Le autorizzazioni sono definite in `AndroidManifest.xml`, specificato nel [file delle impostazioni del progetto](/manuals/project-settings/#android) *game.project*. Puoi approfondire le autorizzazioni Android nella [documentazione ufficiale](https://developer.android.com/guide/topics/permissions/overview). Il manifest predefinito richiede le seguenti autorizzazioni:

### android.permission.INTERNET e android.permission.ACCESS_NETWORK_STATE (Livello di protezione: normal) {#androidpermissioninternet-and-androidpermissionaccess_network_state-protection-level-normal}
Consente alle applicazioni di aprire *socket di rete* e di accedere alle informazioni sulle reti. Queste autorizzazioni sono necessarie per l'accesso a Internet. ([Documentazione ufficiale di Android](https://developer.android.com/reference/android/Manifest.permission#INTERNET)) e ([Documentazione ufficiale di Android](https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE)).

### android.permission.WAKE_LOCK (Livello di protezione: normal) {#androidpermissionwake_lock-protection-level-normal}
Consente di utilizzare i WakeLock di PowerManager per impedire la sospensione del processore o l'oscuramento dello schermo. Questa autorizzazione è necessaria per impedire temporaneamente al dispositivo di entrare in sospensione durante la ricezione di una notifica push. ([Documentazione ufficiale di Android](https://developer.android.com/reference/android/Manifest.permission#WAKE_LOCK))


## Utilizzo di AndroidX {#using-androidx}
AndroidX rappresenta un importante miglioramento rispetto alla libreria Android Support Library originale, che non è più mantenuta. I pacchetti AndroidX sostituiscono completamente la Support Library, offrendo le stesse funzionalità e nuove librerie. La maggior parte delle estensioni Android nell'[Asset Portal](/assets) supporta AndroidX. Se non vuoi utilizzare AndroidX, puoi disabilitarlo esplicitamente a favore della vecchia Android Support Library selezionando `Use Android Support Lib` nel [manifest dell'applicazione](https://defold.com/manuals/app-manifest/).

![](images/android/enable_supportlibrary.png)

## FAQ
:[Android FAQ](../shared/android-faq.md)
