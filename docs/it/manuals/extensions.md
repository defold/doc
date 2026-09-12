---
title: Scrivere estensioni native per Defold
brief: Questo manuale spiega come scrivere un'estensione nativa per il motore di gioco Defold e come compilarla tramite i servizi di build nel cloud, senza alcuna configurazione.
---

# Estensioni native {#native-extensions}

Se devi interagire in modo personalizzato con software o hardware esterni a basso livello e Lua non è sufficiente, l'SDK di Defold permette di scrivere estensioni del motore in C, C++, C#, Objective-C, Java o JavaScript, a seconda della piattaforma di destinazione. Alcuni casi d'uso tipici delle estensioni native sono:

- Interazione con hardware specifico, per esempio la fotocamera dei telefoni cellulari.
- Interazione con API esterne di basso livello, per esempio le API delle reti pubblicitarie che non consentono l'interazione tramite API di rete, per le quali si potrebbe usare Luasocket.
- Calcoli ed elaborazione dei dati ad alte prestazioni.

::: sidenote
Il supporto a C# è sperimentale ed è destinato alle estensioni native, non ai componenti script di Defold. Usa .NET 9 NativeAOT per produrre una libreria statica; aggiungi i file sorgente `.cs` alla cartella `src` di un'estensione e il servizio di build genererà il file di progetto. Le piattaforme di destinazione supportate dipendono dalle capacità attuali di NativeAOT e del servizio di build. Consulta l'[esempio ufficiale dei linguaggi per le estensioni native](https://github.com/defold/example-languages) per il flusso di lavoro attuale e la configurazione verificata.
:::

## Il server di build {#the-build-server}

Defold permette di iniziare a usare le estensioni native senza alcuna configurazione, grazie a una soluzione di build nel cloud. Ogni estensione nativa sviluppata e aggiunta a un progetto di gioco, direttamente o tramite un [progetto libreria](/manuals/libraries/), diventa parte del normale contenuto del progetto. Non occorre creare versioni speciali del motore e distribuirle ai membri del team: tutto questo viene gestito automaticamente. Ogni membro del team che crea una build ed esegue il progetto ottiene un eseguibile del motore specifico per quel progetto, con tutte le estensioni native integrate.

![Build nel cloud](images/extensions/cloud_build.png)

Defold mette a disposizione gratuitamente il server di build nel cloud, senza limitazioni d'uso. Il server è ospitato in Europa e l'URL a cui viene inviato il codice nativo si configura nella [finestra delle preferenze dell'editor](/manuals/editor-preferences/#extensions) oppure tramite l'opzione a riga di comando `--build-server` di [bob](/manuals/bob/#usage). Se desideri configurare un tuo server, [segui queste istruzioni](/manuals/extender-local-setup).

## Struttura del progetto {#project-layout}

Per creare una nuova estensione, crea una cartella nella radice del progetto. Questa cartella conterrà tutte le impostazioni, il codice sorgente, le librerie e le risorse associate all'estensione. Il servizio di build delle estensioni riconosce la struttura delle cartelle e raccoglie tutti i file sorgente e le librerie.

```
 myextension/
 │
 ├── ext.manifest
 │
 ├── src/
 │
 ├── include/
 │
 ├── lib/
 │   └──[platforms]
 │
 ├── manifests/
 │   └──[platforms]
 │
 └── res/
     └──[platforms]

```
*ext.manifest*
: La cartella dell'estensione _deve_ contenere un file *ext.manifest*. Si tratta di un file di configurazione con flag e definizioni usati durante la build di una singola estensione. La definizione del formato del file si trova nel [manuale del manifest delle estensioni](https://defold.com/manuals/extensions-ext-manifests/).

*src*
: Questa cartella deve contenere tutti i file di codice sorgente.

*include*
: Questa cartella facoltativa contiene gli eventuali file di inclusione.

*lib*
: Questa cartella facoltativa contiene le eventuali librerie compilate da cui dipende l'estensione. I file delle librerie vanno collocati in sottocartelle denominate secondo lo schema `platform` o `architecture-platform`, a seconda delle architetture supportate dalle librerie.

  :[platforms](../shared/platforms.md)

*manifests*
: Questa cartella facoltativa contiene file aggiuntivi usati nel processo di build o di creazione del bundle. Per i dettagli, vedi sotto.

*res*
: Questa cartella facoltativa contiene le eventuali risorse aggiuntive da cui dipende l'estensione. I file delle risorse vanno collocati in sottocartelle denominate secondo lo schema `platform` o `architecture-platform`, come per le sottocartelle di `lib`. È consentita anche una sottocartella `common`, contenente i file delle risorse comuni a tutte le piattaforme.

### File manifest {#manifest-files}

La cartella facoltativa *manifests* di un'estensione contiene file aggiuntivi usati nel processo di build e di creazione del bundle. I file vanno collocati in sottocartelle denominate secondo lo schema `platform`:

* `android` - Questa cartella accetta un frammento di file manifest da unire a quello dell'applicazione principale ([come descritto qui](/manuals/extensions-manifest-merge-tool)).
  * La cartella può contenere anche un file `build.gradle` con dipendenze da [risolvere tramite Gradle](/manuals/extensions-gradle).
  * Le estensioni con codice Java dovrebbero includere un [file di regole di conservazione R8](#r8-keep-rules-for-android) (`.keep`) per le classi necessarie a runtime.
* `ios` - Questa cartella accetta un frammento di file manifest da unire a quello dell'applicazione principale ([come descritto qui](/manuals/extensions-manifest-merge-tool)).
  * La cartella può contenere anche un file `Podfile` con dipendenze da [risolvere tramite Cocoapods](/manuals/extensions-cocoapods).
* `osx` - Questa cartella accetta un frammento di file manifest da unire a quello dell'applicazione principale ([come descritto qui](/manuals/extensions-manifest-merge-tool)).
* `web` - Questa cartella accetta un frammento di file manifest da unire a quello dell'applicazione principale ([come descritto qui](/manuals/extensions-manifest-merge-tool)).


### Regole di conservazione R8 per Android {#r8-keep-rules-for-android}

Aggiungi un file `.keep` alla directory `manifests/android` dell'estensione, accanto a `build.gradle`. Per esempio, `/myextension/manifests/android/myextension.keep` può conservare le classi Java dell'estensione con:

```proguard
-keep,allowoptimization class com.example.myextension.** { *; }
```

Sostituisci `com.example.myextension` con il package che contiene le classi Java della tua estensione. Questa regola conserva le classi e i loro membri, consentendo a R8 di ottimizzarne il codice. Aggiungi regole per le altre classi a cui accedi tramite Java Native Interface (JNI) o reflection, poiché R8 potrebbe non rilevare automaticamente questi utilizzi.

Se l'estensione dipende da annotazioni a runtime, includi anche:

```proguard
-keepattributes *Annotation*
```

Queste regole vengono combinate con il file di conservazione selezionato nel progetto quando [R8 è abilitato](/manuals/android/#enabling-r8).


## Risorse personalizzate {#custom-resources}

Un'estensione può includere dati nell'archivio del gioco dichiarando risorse personalizzate in un file `ext.properties` accanto al suo `ext.manifest`:

```ini
[project]
custom_resources.default = /myextension/data
```

Per esempio, inserisci un file JSON in `/myextension/data/settings.json`. Il percorso è relativo alla radice del progetto e include la cartella dell'estensione. Quando condividi l'estensione come libreria, includi `myextension` in [Include Dirs](/manuals/libraries/#setting-up-library-sharing) della libreria, affinché i progetti che la usano ricevano l'estensione e i suoi dati.

Questi percorsi vengono combinati con `project.custom_resources` di *game.project* e con quelli forniti dalle altre estensioni. Impostare le risorse personalizzate nel progetto non sostituisce quelle fornite dalle estensioni. Sia le build dell'editor sia gli archivi di Bob includono i file, che possono essere caricati a runtime:

```lua
local data, err = sys.load_resource("/myextension/data/settings.json")
if data then
    local settings = json.decode(data)
    pprint(settings)
else
    print(err)
end
```

Consulta [Accesso ai file](/manuals/file-access/#custom-resources) per le differenze tra risorse personalizzate e risorse del bundle.

## Condividere un'estensione {#sharing-an-extension}

Le estensioni vengono trattate come qualsiasi altro asset del progetto e possono essere condivise allo stesso modo. Se una cartella di estensione nativa viene aggiunta come cartella di libreria, può essere condivisa e usata da altri come dipendenza del progetto. Consulta il [manuale dei progetti libreria](/manuals/libraries/) per ulteriori informazioni.


## Un semplice esempio di estensione {#a-simple-example-extension}

Realizza un'estensione molto semplice. Per prima cosa, crea una nuova cartella *`myextension`* nella radice e aggiungi un file *`ext.manifest`* contenente il nome dell'estensione, "`MyExtension`". Il nome è un simbolo C++ e deve corrispondere al primo argomento di `DM_DECLARE_EXTENSION` (vedi sotto).

![File manifest](images/extensions/manifest.png)

```yaml
# C++ symbol in your extension
name: "MyExtension"
```

L'estensione è composta da un singolo file C++, *`myextension.cpp`*, creato nella cartella "`src`".

![File C++](images/extensions/cppfile.png)

Il file sorgente dell'estensione contiene il seguente codice:

```cpp
// myextension.cpp
// Extension lib defines
#define LIB_NAME "MyExtension"
#define MODULE_NAME "myextension"

// include the Defold SDK
#include <dmsdk/sdk.h>

static int Reverse(lua_State* L)
{
    // The number of expected items to be on the Lua stack
    // once this struct goes out of scope
    DM_LUA_STACK_CHECK(L, 1);

    // Check and get parameter string from stack
    char* str = (char*)luaL_checkstring(L, 1);

    // Reverse the string
    int len = strlen(str);
    for(int i = 0; i < len / 2; i++) {
        const char a = str[i];
        const char b = str[len - i - 1];
        str[i] = b;
        str[len - i - 1] = a;
    }

    // Put the reverse string on the stack
    lua_pushstring(L, str);

    // Return 1 item
    return 1;
}

// Functions exposed to Lua
static const luaL_reg Module_methods[] =
{
    {"reverse", Reverse},
    {0, 0}
};

static void LuaInit(lua_State* L)
{
    int top = lua_gettop(L);

    // Register lua names
    luaL_register(L, MODULE_NAME, Module_methods);

    lua_pop(L, 1);
    assert(top == lua_gettop(L));
}

dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result InitializeMyExtension(dmExtension::Params* params)
{
    // Init Lua
    LuaInit(params->m_L);
    printf("Registered %s Extension\n", MODULE_NAME);
    return dmExtension::RESULT_OK;
}

dmExtension::Result AppFinalizeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result FinalizeMyExtension(dmExtension::Params* params)
{
    return dmExtension::RESULT_OK;
}


// Defold SDK uses a macro for setting up extension entry points:
//
// DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)

// MyExtension is the C++ symbol that holds all relevant extension data.
// It must match the name field in the `ext.manifest`
DM_DECLARE_EXTENSION(MyExtension, LIB_NAME, AppInitializeMyExtension, AppFinalizeMyExtension, InitializeMyExtension, 0, 0, FinalizeMyExtension)
```

Osserva la macro `DM_DECLARE_EXTENSION`, usata per dichiarare i vari punti di ingresso nel codice dell'estensione. Il primo argomento, `symbol`, deve corrispondere al nome specificato in *ext.manifest*. In questo semplice esempio non servono punti di ingresso `update` o `on_event`, quindi in quelle posizioni viene passato `0` alla macro.

Ora basta creare una build del progetto (<kbd>Project ▸ Build</kbd>). L'estensione verrà caricata sul servizio di build delle estensioni, che produrrà un motore personalizzato con la nuova estensione inclusa. Se il servizio rileva errori, verrà mostrata una finestra di dialogo con gli errori di build.

Per provare l'estensione, crea un oggetto di gioco (game object) e aggiungi un componente script con del codice di test:

```lua
local s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
local reverse_s = myextension.reverse(s)
print(reverse_s) --> ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba
```

Ecco fatto! Hai creato un'estensione nativa completamente funzionante.


## Ciclo di vita dell'estensione {#extension-lifecycle}

Come visto sopra, la macro `DM_DECLARE_EXTENSION` serve a dichiarare i vari punti di ingresso nel codice dell'estensione:

`DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)`

I punti di ingresso permettono di eseguire codice in vari momenti del ciclo di vita di un'estensione:

* Avvio del motore
  * I sistemi del motore si avviano
  * `app_init` dell'estensione
  * `init` dell'estensione - Tutte le API di Defold sono state inizializzate. Questo è il momento consigliato nel ciclo di vita dell'estensione per creare i binding Lua al codice dell'estensione.
  * Inizializzazione degli script - Viene chiamata la funzione `init()` dei file script.
* Ciclo del motore
  * Aggiornamento del motore
    * `update` dell'estensione
    * Aggiornamento degli script - Viene chiamata la funzione `update()` dei file script.
  * Eventi del motore (riduzione a icona o ingrandimento della finestra, ecc.)
    * `on_event` dell'estensione
* Arresto (o riavvio) del motore
  * Finalizzazione degli script - Viene chiamata la funzione `final()` dei file script.
  * `final` dell'estensione
  * `app_final` dell'estensione

## Identificatori di piattaforma definiti {#defined-platform-identifiers}

Il servizio di build definisce i seguenti identificatori sulle rispettive piattaforme:

* `DM_PLATFORM_WINDOWS`
* `DM_PLATFORM_OSX`
* `DM_PLATFORM_IOS`
* `DM_PLATFORM_ANDROID`
* `DM_PLATFORM_LINUX`
* `DM_PLATFORM_HTML5`

## Log del server di build {#build-server-logs}

I log del server di build sono disponibili quando il progetto usa estensioni native. Il log del server di build (`log.txt`) viene scaricato insieme al motore personalizzato quando viene creata una build del progetto. Viene conservato nel file `.internal/%platform%/build.zip` ed estratto anche nella cartella di build del progetto.

## Estensioni di esempio {#example-extensions}

* [Esempio di estensione di base](https://github.com/defold/template-native-extension) (l'estensione di questo manuale)
* [Esempio di estensione per Android](https://github.com/defold/extension-android)
* [Esempio di estensione per HTML5](https://github.com/defold/extension-html5)
* [Estensione per la riproduzione video su macOS, iOS e Android](https://github.com/defold/extension-videoplayer)
* [Estensione per la fotocamera su macOS e iOS](https://github.com/defold/extension-camera)
* [Estensione per gli acquisti in-app su iOS e Android](https://github.com/defold/extension-iap)
* [Estensione Firebase Analytics per iOS e Android](https://github.com/defold/extension-firebase-analytics)

Anche l'[Asset Portal di Defold](https://www.defold.com/assets/) contiene diverse estensioni native.
