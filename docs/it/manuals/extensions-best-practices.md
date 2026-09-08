---
title: Estensioni native - Buone pratiche
brief: Questo manuale descrive le buone pratiche per lo sviluppo di estensioni native.
---

# Buone pratiche {#best-practices}

Scrivere codice multipiattaforma può essere difficile, ma esistono alcuni accorgimenti che ne facilitano sia lo sviluppo sia la manutenzione.


## Struttura del progetto {#project-structure}

Quando crei un'estensione, alcuni accorgimenti ne facilitano sia lo sviluppo sia la manutenzione.

### API Lua {#lua-api}

Dovrebbe esserci una sola API Lua, con una sola implementazione. Questo rende molto più semplice ottenere lo stesso comportamento su tutte le piattaforme.

Se una piattaforma non deve supportare l'estensione, si consiglia semplicemente di non registrare alcun modulo Lua. In questo modo puoi verificare se l'estensione è supportata controllando la presenza di `nil`:

```lua
    if myextension ~= nil then
        myextension.do_something()
    end
```

### Struttura delle cartelle {#folder-structure}

Per le estensioni viene spesso usata la seguente struttura delle cartelle:

```
    /root
        /input
        /main                            -- All the files for the actual example project
            /...
        /myextension                     -- The actual root folder of the extension
            ext.manifest
            /include                     -- External includes, used by other extensions
            /libs
                /<platform>              -- External libraries for all supported platforms
            /src
                myextension.cpp          -- The extension Lua api and the extension life cycle functions
                                            Also contains generic implementations of your Lua api functions.
                myextension_private.h    -- Your internal api that each platform will implement (I.e. `myextension_Init` etc)
                myextension.mm           -- If native calls are needed for iOS/macOS. Implements `myextension_Init` etc for iOS/macOS
                myextension_android.cpp  -- If JNI calls are needed for Android. Implements `myextension_Init` etc for Android
                /java
                    /<platform>          -- Any java files needed for Android
            /res                         -- Any resources needed for a platform
            /external
                README.md                -- Notes/scripts on how to build or package any external libraries
        /bundleres                       -- Resources that should be bundles for (see game.project and the [bundle_resources setting]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Any extra app configuration info
```

Tieni presente che `myextension.mm` e `myextension_android.cpp` sono necessari solo se effettui chiamate native specifiche per la rispettiva piattaforma.

#### Cartelle delle piattaforme {#platform-folders}

In alcuni percorsi, l'architettura della piattaforma viene usata come nome della cartella per determinare quali file usare durante la compilazione o la creazione del bundle dell'applicazione. Questi nomi hanno la forma:

    <architecture>-<platform>

L'elenco attuale è:

    arm64-ios, arm64_sim-ios, arm64-android, armv7-android, x86_64-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

Per esempio, colloca le librerie specifiche di una piattaforma in:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## Scrivere codice nativo {#writing-native-code}

Nel codice sorgente di Defold, C++ viene usato con molta parsimonia e la maggior parte del codice segue uno stile molto simile al C. I template sono quasi del tutto assenti, a eccezione di alcune classi contenitore, poiché incidono sui tempi di compilazione e sulle dimensioni dell'eseguibile.

### Versione di C++ {#c-version}

Per compilare il nucleo del motore usiamo C++11, mentre su Windows usiamo C++14. Le build per console ora richiedono generalmente C++14 o versioni successive.

Per le estensioni native non fissiamo una versione di C++, ma ci affidiamo alla versione predefinita della toolchain della piattaforma.

Il codice sorgente di Defold evita di usare le funzionalità o le versioni più recenti di C++. Questo avviene soprattutto perché non servono nuove funzionalità per sviluppare un motore di gioco, ma anche perché tenersi aggiornati sulle ultime funzionalità di C++ richiede tempo, e padroneggiarle davvero richiede molto tempo prezioso.

Per chi sviluppa estensioni, questo offre anche il vantaggio di mantenere stabile l'ABI di Defold. Inoltre, l'uso delle funzionalità più recenti di C++ può impedire la compilazione del codice su altre piattaforme, a causa delle differenze nel supporto disponibile.

### Nessuna eccezione C++ {#no-c-exceptions}

Defold non usa eccezioni nel motore. In genere i motori di gioco evitano le eccezioni, poiché i dati sono perlopiù noti in anticipo, durante lo sviluppo. Eliminare il supporto alle eccezioni C++ riduce le dimensioni dell'eseguibile e migliora le prestazioni durante l'esecuzione.

### Librerie di template standard - STL {#standard-template-libraries-stl}

Poiché il motore Defold non usa codice STL, a eccezione di alcuni algoritmi e funzioni matematiche (`std::sort`, `std::upper_bound` ecc.), potresti riuscire a usare STL nella tua estensione.

Anche in questo caso, tieni presente che le incompatibilità ABI possono creare problemi quando usi la tua estensione insieme ad altre estensioni o a librerie di terze parti.

Evitare le librerie STL, che fanno ampio uso di template, riduce anche i tempi di build e, soprattutto, le dimensioni dell'eseguibile.

#### Stringhe {#strings}

Nel motore Defold si usa `const char*` al posto di `std::string`. L'uso di `std::string` è una fonte comune di problemi quando si combinano versioni diverse di C++ o del compilatore, poiché può causare un'incompatibilità ABI. L'uso di `const char*` e di alcune funzioni di supporto evita questo problema.

### Limita la visibilità delle funzioni {#make-functions-hidden}

Se possibile, usa la parola chiave `static` per le funzioni locali alla tua unità di compilazione. Questo consente al compilatore di effettuare alcune ottimizzazioni e può sia migliorare le prestazioni sia ridurre le dimensioni dell'eseguibile.

## Librerie di terze parti {#3rd-party-libraries}

Quando scegli una libreria di terze parti da usare, indipendentemente dal linguaggio, considera i seguenti aspetti:

* Funzionalità - Risolve il tuo problema specifico?
* Prestazioni - Comporta un costo in termini di prestazioni durante l'esecuzione?
* Dimensioni della libreria - Quanto aumenteranno le dimensioni dell'eseguibile finale? È accettabile?
* Dipendenze - Richiede altre librerie?
* Supporto - In che stato si trova la libreria? Ha molte segnalazioni aperte? Viene ancora mantenuta?
* Licenza - Consente l'uso della libreria in questo progetto?


## Dipendenze open source {#open-source-dependencies}

Assicurati sempre di avere accesso alle tue dipendenze. Per esempio, se dipendi da un progetto su GitHub, nulla impedisce che il suo repository venga rimosso o che cambi improvvisamente direzione o proprietario. Puoi ridurre questo rischio creando un fork del repository e usando il tuo fork al posto del progetto originale.

Ricorda che il codice della libreria verrà incorporato nel tuo gioco, quindi assicurati che la libreria faccia ciò che deve fare, e niente di più!
