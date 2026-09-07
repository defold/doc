---
title: Sviluppo con Defold per la piattaforma macOS
brief: Questo manuale descrive come creare build ed eseguire applicazioni Defold su macOS
---

# Sviluppo per macOS {#macos-development}

Sviluppare applicazioni Defold per la piattaforma macOS è un processo semplice, con pochissimi aspetti da tenere in considerazione.

## Impostazioni del progetto {#project-settings}

La configurazione dell'applicazione specifica per macOS si effettua nella [sezione macOS](/manuals/project-settings/#macos) del file delle impostazioni *game.project*.

## Icona dell'applicazione {#application-icon}

L'icona dell'applicazione usata per un gioco macOS deve essere nel formato .`icns`. Puoi creare facilmente un file `.icns` a partire da un insieme di file `.png` raccolti in un `.iconset`. Segui le [istruzioni ufficiali per creare un file `.icns`](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html). Ecco una breve sintesi dei passaggi:

* Crea una cartella per le icone, ad esempio `game.iconset`
* Copia i file delle icone nella cartella creata:

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* Converti la cartella `.iconset` in un file `.icns` usando lo strumento a riga di comando `iconutil`:

```
iconutil -c icns -o game.icns game.iconset
```

## Pubblicazione dell'applicazione {#publishing-your-application}
Puoi pubblicare la tua applicazione sul Mac App Store, tramite uno store o un portale di terze parti come Steam o itch.io, oppure autonomamente attraverso un sito web. Prima di pubblicare l'applicazione, devi prepararla per l'invio. I passaggi seguenti sono necessari indipendentemente da come intendi distribuire l'applicazione:

1. Assicurati che chiunque possa eseguire il tuo gioco aggiungendo i permessi di esecuzione (per impostazione predefinita, solo il proprietario del file dispone dei permessi di esecuzione):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

2. Crea un file delle autorizzazioni (entitlements) che specifichi le autorizzazioni richieste dal tuo gioco. Per la maggior parte dei giochi sono sufficienti le seguenti autorizzazioni:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - Indica se l'app può creare memoria scrivibile ed eseguibile usando il flag MAP_JIT
  * `com.apple.security.cs.allow-unsigned-executable-memory` - Indica se l'app può creare memoria scrivibile ed eseguibile senza le restrizioni imposte dall'uso del flag MAP_JIT
  * `com.apple.security.cs.allow-dyld-environment-variables` - Indica se l'app può essere influenzata dalle variabili d'ambiente del linker dinamico, che puoi usare per iniettare codice nel processo dell'app

Alcune applicazioni potrebbero richiedere anche autorizzazioni aggiuntive. L'estensione Steamworks richiede questa autorizzazione aggiuntiva:

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

  * `com.apple.security.cs.disable-library-validation` - Indica se l'app può caricare plug-in o framework arbitrari, senza richiedere la firma del codice.

Tutte le autorizzazioni che possono essere concesse a un'applicazione sono elencate nella [documentazione ufficiale per sviluppatori Apple](https://developer.apple.com/documentation/bundleresources/entitlements).

3. Firma il tuo gioco usando `codesign`:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Pubblicazione al di fuori del Mac App Store {#publishing-outside-the-mac-app-store}
Apple richiede che tutto il software distribuito al di fuori del Mac App Store sia autenticato da Apple per poter essere eseguito con le impostazioni predefinite di macOS Catalina. Consulta la [documentazione ufficiale](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow) per scoprire come aggiungere l'autenticazione a un ambiente di build gestito da script al di fuori di Xcode. Ecco una breve sintesi dei passaggi:

1. Segui i passaggi precedenti per aggiungere i permessi e firmare l'applicazione.

2. Comprimi il gioco in un archivio ZIP e caricalo per l'autenticazione usando `altool`.

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

3. Controlla lo stato dell'invio usando l'UUID della richiesta restituito dalla chiamata a `altool --notarize-app`:

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

4. Attendi che lo stato diventi `success` e allega il ticket di autenticazione al gioco:

```
$ xcrun stapler staple "Game.app"
```

5. Il gioco è ora pronto per la distribuzione.

## Pubblicazione sul Mac App Store {#publishing-to-the-mac-app-store}
La procedura di pubblicazione sul Mac App Store è ben documentata nella [documentazione per sviluppatori Apple](https://developer.apple.com/macos/submit/). Assicurati di aggiungere i permessi e firmare l'applicazione con `codesign` come descritto sopra prima di inviarla.

Nota: non è necessario autenticare il gioco quando lo pubblichi sul Mac App Store.

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)
