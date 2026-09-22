---
title: Immagini Docker disponibili
brief: Questo documento descrive le immagini Docker disponibili e le versioni di Defold che le hanno utilizzate
---

# Immagini Docker disponibili {#available-docker-images}
Di seguito trovi l'elenco di tutte le immagini Docker disponibili nel registro pubblico. Puoi utilizzare queste immagini per eseguire Extender in un ambiente con SDK precedenti che non sono più supportati.

|SDK               |Tag dell'immagine                                                                                        |Nome della piattaforma (nella configurazione di Extender) |Versioni di Defold che hanno utilizzato l'immagine |
|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------|
|Linux più recente |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`                       |Tutte le versioni di Defold    |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`                      |Dalla 1.4.3                    |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                         |Fino alla 1.7.0                |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                         |[1.8.0-1.9.3]                  |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                         |Dalla 1.9.4                    |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                        |Fino alla 1.6.1                |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                        |Dalla 1.6.2                    |

# Come utilizzare le immagini Docker precedenti {#how-to-use-old-docker-images}
Per utilizzare un ambiente precedente, segui questi passaggi:
1. Modifica `docker-compose.yml` nel repository di Extender, disponibile a [questo link](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml). Devi aggiungere un'altra definizione di servizio con l'immagine Docker necessaria. Ad esempio, per utilizzare l'immagine Docker che contiene Emscripten 2.0.11, aggiungi la seguente definizione di servizio:
    ```yml
    emscripten_2011-dev:
        image: europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest
        extends:
        file: common-services.yml
        service: remote_builder
        profiles:
        - all
        - web
        networks:
        default:
            aliases:
            - emsdk-2011
    ```
    I campi principali sono:
    * **profiles** - elenco dei profili che attivano l'avvio del servizio. I nomi dei profili vengono passati tramite l'argomento `--profile <profile_name>` al comando `docker compose`.
    * **networks** - elenco delle reti che il container Docker deve utilizzare. Per eseguire Extender si utilizza la rete denominata `default`. È importante impostare gli alias di rete del servizio, che verranno utilizzati in seguito nella configurazione di Extender.
2. Aggiungi la definizione del sistema di build remoto in [`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml), nella sezione `extender.remote-builder.platforms`. Nel nostro esempio sarà così:
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    L'URL deve avere il formato `http://<service_network_alias>:9000`, dove `service_network_alias` è l'alias di rete del passaggio 1. 9000 è la porta standard di Extender (può essere diversa se utilizzi una configurazione personalizzata di Extender).
3. Esegui Extender in locale come descritto in [Come eseguire Extender in locale con artefatti preconfigurati](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts).
