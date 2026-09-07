---
title: Configurazione di un server di build locale
brief: Questo manuale descrive come configurare ed eseguire un server di build locale.
---

# Configurazione locale del server di build {#build-server-local-setup}

Puoi eseguire un server di build locale (noto anche come 'Extender') in due modi:
1. Eseguire un server di build locale con artefatti preconfigurati.
2. Eseguire un server di build locale con artefatti compilati localmente.

## Come eseguire Extender in locale con artefatti preconfigurati {#how-to-run-local-extender-with-preconfigured-artifacts}

Prima di poter eseguire in locale un server di build cloud, devi installare il seguente software:

* [Docker](https://www.docker.com/) - Docker è un insieme di prodotti di piattaforma come servizio che utilizzano la virtualizzazione a livello di sistema operativo per distribuire software in pacchetti chiamati container. Per eseguire i server di build cloud sulla tua macchina di sviluppo locale devi installare [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Google Cloud CLI - Google Cloud CLI è un insieme di strumenti per creare e gestire le risorse di Google Cloud. Gli strumenti possono essere [installati direttamente da Google](https://cloud.google.com/sdk/docs/install) oppure tramite un gestore di pacchetti come Brew, Chocolatey o Snap.
* Ti serve anche un account Google per scaricare i container con i server di build specifici per ciascuna piattaforma.

Una volta installato il software indicato sopra, segui questi passaggi per installare ed eseguire i server di build cloud di Defold:

**Nota per gli utenti Windows**: usa il terminale Git Bash per eseguire i comandi riportati di seguito.

1. __Autenticati su Google Cloud e crea le credenziali predefinite dell'applicazione__ - Per scaricare le immagini dei container Docker devi avere un account Google, in modo da consentirci di monitorare e garantire un uso equo del registro pubblico dei container e di sospendere temporaneamente gli account che scaricano immagini in quantità eccessive.

   ```sh
   gcloud auth login
   ```
2. __Configura Docker per usare i registri di artefatti__ - Docker deve essere configurato per usare `gcloud` come strumento di gestione delle credenziali quando scarica le immagini dei container dal registro pubblico dei container all'indirizzo `europe-west1-docker.pkg.dev`.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Verifica che Docker e Google Cloud siano configurati correttamente__ - Verifica che Docker e Google Cloud siano configurati correttamente scaricando l'immagine di base utilizzata da tutte le immagini dei container dei server di build. Assicurati che Docker Desktop sia in esecuzione prima di eseguire il comando seguente:
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Clona il repository di Extender__ - Con Docker e Google Cloud configurati correttamente, siamo quasi pronti ad avviare i server. Prima di avviare il server, devi clonare il repository Git che contiene il server di build:
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __Scarica i JAR precompilati__ - Il passaggio successivo consiste nello scaricare il server precompilato (`extender.jar`) e lo strumento per l'unione dei manifest (`manifestmergetool.jar`):
   ```sh
    TMP_DIR=$(pwd)/server/_tmp
    APPLICATION_DIR=$(pwd)/server/app
    # set necessary version of Extender and Manifest merge tool
    # versions can be found at Github release page https://github.com/defold/extender/releases
    # or you can pull latest version (see code sample below)
    EXTENDER_VERSION=2.6.5
    MANIFESTMERGETOOL_VERSION=1.3.0
    echo "Download prebuild jars to ${APPLICATION_DIR}"
    rm -rf ${TMP_DIR}
    mkdir -p ${TMP_DIR}
    rm -rf ${APPLICATION_DIR}
    mkdir -p ${APPLICATION_DIR}

    gcloud artifacts files download \
    --project=extender-426409 \
    --location=europe-west1 \
    --repository=extender-maven \
    --destination=${TMP_DIR} \
    com/defold/extender/server/${EXTENDER_VERSION}/server-${EXTENDER_VERSION}.jar

    gcloud artifacts files download \
    --project=extender-426409 \
    --location=europe-west1 \
    --repository=extender-maven \
    --destination=${TMP_DIR} \
    com/defold/extender/manifestmergetool/${MANIFESTMERGETOOL_VERSION}/manifestmergetool-${MANIFESTMERGETOOL_VERSION}.jar

    cp ${TMP_DIR}/$(ls ${TMP_DIR} | grep server-${EXTENDER_VERSION}.jar) ${APPLICATION_DIR}/extender.jar
    cp ${TMP_DIR}/$(ls ${TMP_DIR} | grep manifestmergetool-${MANIFESTMERGETOOL_VERSION}.jar) ${APPLICATION_DIR}/manifestmergetool.jar
   ```
6. __Avvia il server__ - Ora puoi avviare il server eseguendo il comando principale di docker compose:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
dove *profile* può essere:
* **all** - avvia le istanze remote per tutte le piattaforme
* **android** - avvia l'istanza frontend + le istanze remote per creare la build della versione Android
* **web** - avvia l'istanza frontend + le istanze remote per creare la build della versione Web
* **linux** - avvia l'istanza frontend + le istanze remote per creare la build della versione Linux
* **windows** - avvia l'istanza frontend + le istanze remote per creare la build della versione Windows
* **consoles** - avvia l'istanza frontend + le istanze remote per creare le build delle versioni Nintendo Switch/PS4/PS5
* **nintendo** - avvia l'istanza frontend + le istanze remote per creare la build della versione Nintendo Switch
* **playstation** - avvia l'istanza frontend + le istanze remote per creare le build delle versioni PS4/PS5
* **metrics** - avvia VictoriaMetrics + Grafana come backend per le metriche e strumento di visualizzazione
Per ulteriori informazioni sugli argomenti di `docker compose`, consulta https://docs.docker.com/reference/cli/docker/compose/.

Quando docker compose è in esecuzione, puoi usare **http://localhost:9000** come `Build server address` nelle preferenze dell'editor oppure come valore di `--build-server` se usi Bob per creare la build del progetto.

Puoi specificare più profili sulla riga di comando. Per esempio:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
L'esempio precedente avvia le istanze frontend, Android, Web e Windows.

Per arrestare i servizi, premi Ctrl+C se docker compose è in esecuzione in primo piano, oppure esegui 
```sh
docker compose -p extender down
```
se docker compose è stato avviato in background (per esempio, passando l'opzione '-d' al comando `docker compose up`).

Se vuoi scaricare le versioni più recenti dei JAR, puoi usare il comando seguente per determinare l'ultima versione
```sh
    EXTENDER_VERSION=$(gcloud artifacts versions list \
        --project=extender-426409 \
        --location=europe-west1 \
        --repository=extender-maven \
        --package="com.defold.extender:server" \
        --sort-by="~createTime" \
        --limit=1 \
        --format="value(name)")

    MANIFESTMERGETOOL_VERSION=$(gcloud artifacts versions list \
        --project=extender-426409 \
        --location=europe-west1 \
        --repository=extender-maven \
        --package="com.defold.extender:manifestmergetool" \
        --sort-by="~createTime" \
        --limit=1 \
        --format="value(name)")
```

### E per macOS e iOS? {#what-about-macos-and-ios}

Le build per macOS e iOS vengono create su hardware Apple reale utilizzando un server di build eseguito in modalità autonoma senza Docker. Xcode, Java e gli altri strumenti necessari vengono invece installati direttamente sulla macchina e il server di build viene eseguito come un normale processo Java. Puoi scoprire come configurarlo nella [documentazione del server di build su GitHub](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos).


## Come eseguire Extender in locale con artefatti compilati localmente {#how-to-run-local-extender-with-locally-built-artifacts}

Segui le [istruzioni nel repository di Extender su GitHub](https://github.com/defold/extender) per compilare ed eseguire manualmente un server di build locale.
