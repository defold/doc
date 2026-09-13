---
title: Verfügbare Docker-Images
brief: Dieses Dokument beschreibt die verfügbaren Docker-Images und die Defold-Versionen, die sie verwendet haben.
---

# Verfügbare Docker-Images {#available-docker-images}
Die folgende Liste enthält alle Docker-Images, die in der öffentlichen Registry verfügbar sind. Mit diesen Images kannst du Extender in einer Umgebung mit alten SDKs ausführen, die nicht mehr unterstützt werden.

|SDK               |Image-Tag                                                                                                |Plattformname (in der Extender-Konfiguration) |Defold-Version, die das Image verwendet hat |
|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------|
|Linux latest      |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`                       |Alle Defold-Versionen          |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`                      |Seit 1.4.3                     |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                         |Bis 1.7.0                      |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                         |[1.8.0-1.9.3]                  |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                         |Seit 1.9.4                     |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                        |Bis 1.6.1                      |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                        |Seit 1.6.2                     |

# Alte Docker-Images verwenden {#how-to-use-old-docker-images}
Um eine alte Umgebung zu verwenden, solltest du die folgenden Schritte ausführen:
1. Ändere `docker-compose.yml` aus dem Extender-Repository [Link](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml). Du musst eine weitere Dienstdefinition mit dem benötigten Docker-Image hinzufügen. Wenn wir beispielsweise ein Docker-Image verwenden möchten, das Emscripten 2.0.11 enthält, müssen wir die folgende Dienstdefinition hinzufügen:
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
    Wichtige Felder sind:
    * **profiles** - Liste der Profile, die den Start des Dienstes auslösen. Die Profilnamen werden über das Argument `--profile <profile_name>` an den Befehl `docker compose` übergeben.
    * **networks** - Liste der Netzwerke, die der Docker-Container verwenden soll. Zum Ausführen von Extender wird das Netzwerk mit dem Namen `default` verwendet. Es ist wichtig, die Netzwerk-Aliase des Dienstes festzulegen (sie werden später in der Extender-Konfiguration verwendet).
2. Füge die Definition eines entfernten Build-Servers (remote builder) in [`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml) im Abschnitt `extender.remote-builder.platforms` hinzu. In unserem Beispiel sieht sie so aus:
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    Die URL sollte das folgende Format haben: `http://<service_network_alias>:9000`, wobei `service_network_alias` der Netzwerk-Alias aus Schritt 1 ist. 9000 ist der Standardport für Extender (er kann abweichen, wenn du eine benutzerdefinierte Extender-Konfiguration verwendest).
3. Starte den lokalen Extender wie unter [Einen lokalen Extender mit vorkonfigurierten Artefakten ausführen](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts) beschrieben.
