---
title: Dostępne obrazy Docker
brief: Ten dokument opisuje dostępne obrazy Docker oraz wersje Defold, które z nich korzystały.
---

# Dostępne obrazy Docker
Poniżej znajduje się lista wszystkich dostępnych obrazów Docker w publicznym rejestrze. Można ich używać do uruchamiania usługi Extender w środowisku ze starszymi SDK, które nie są już wspierane.

|SDK               |Tag obrazu                                                                                                |Nazwa platformy (w konfiguracji usługi Extender) |Wersja Defold, która korzystała z obrazu |
|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------------------|-----------------------------------------|
|Linux latest      |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`                                   |Wszystkie wersje Defold                  |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`                                  |Od 1.4.3                                 |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                                     |Do 1.7.0                                 |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                                     |[1.8.0-1.9.3]                            |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                                     |Od 1.9.4                                 |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                                    |Do 1.6.1                                 |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                                    |Od 1.6.2                                 |

# Jak używać starszych obrazów Docker
Aby użyć starszego środowiska, wykonaj poniższe kroki:
1. Zmodyfikuj `docker-compose.yml` z repozytorium Extender [odnośnik](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml). Trzeba dodać jeszcze jedną definicję usługi z potrzebnym obrazem Docker. Na przykład jeśli chcesz użyć obrazu Docker zawierającego Emscripten 2.0.11, dodaj poniższą definicję usługi:
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
    Najważniejsze pola:
    * **profiles** - lista profili uruchamiających usługę. Nazwy profili przekazuje się do polecenia `docker compose` za pomocą argumentu `--profile <profile_name>`.
    * **networks** - lista sieci, z których powinien korzystać kontener Docker. Do uruchomienia usługi Extender używana jest sieć o nazwie `default`. Ważne jest ustawienie aliasów sieciowych usługi, ponieważ będą używane w późniejszej konfiguracji Extender.
2. Dodaj definicję zdalnego buildera w [`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml) w sekcji `extender.remote-builder.platforms`. W tym przykładzie będzie ona wyglądać tak:
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    Adres URL powinien mieć postać `http://<service_network_alias>:9000`, gdzie `service_network_alias` to alias sieciowy ze kroku 1. 9000 to standardowy port usługi Extender (może być inny, jeśli korzystasz z niestandardowej konfiguracji Extender).
3. Uruchom lokalny Extender zgodnie z opisem w sekcji [Jak uruchomić lokalny Extender z prekonfigurowanymi artefaktami](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts).
