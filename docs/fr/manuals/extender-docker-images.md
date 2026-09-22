---
title: Images Docker disponibles
brief: Ce document décrit les images Docker disponibles et les versions de Defold qui les utilisent.
---

# Images Docker disponibles {#available-docker-images}
Vous trouverez ci-dessous la liste de toutes les images Docker disponibles dans le registre public. Ces images permettent d'exécuter Extender dans un environnement avec d'anciens SDK qui ne sont plus pris en charge.

|SDK               |Étiquette de l'image                                                                                      |Nom de la plateforme (dans la configuration d'Extender) |Versions de Defold utilisant l'image |
|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------|
|Linux (dernière version) |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`                       |Toutes les versions de Defold  |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`                      |Depuis la version 1.4.3        |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                         |Jusqu'à la version 1.7.0        |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                         |[1.8.0-1.9.3]                  |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                         |Depuis la version 1.9.4        |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                        |Jusqu'à la version 1.6.1        |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                        |Depuis la version 1.6.2        |

# Utiliser d'anciennes images Docker {#how-to-use-old-docker-images}
Pour utiliser un ancien environnement, suivez les étapes ci-dessous :
1. Modifiez `docker-compose.yml` dans le dépôt d'Extender ([lien](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml)). Vous devez ajouter une définition de service supplémentaire avec l'image Docker nécessaire. Par exemple, si nous voulons utiliser l'image Docker contenant Emscripten 2.0.11, nous devons ajouter la définition de service suivante :
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
    Les champs importants sont :
    * **profiles** - liste des profils qui déclenchent le démarrage du service. Les noms des profils sont transmis via l'argument `--profile <profile_name>` à la commande `docker compose`.
    * **networks** - liste des réseaux que le conteneur Docker doit utiliser. Pour exécuter Extender, le réseau nommé `default` est utilisé. Il est important de définir les alias réseau du service (ils seront utilisés plus loin dans la configuration d'Extender).
2. Ajoutez la définition d'un serveur de build distant dans [`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml), dans la section `extender.remote-builder.platforms`. Dans notre exemple, elle aura la forme suivante :
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    L'URL doit avoir le format suivant : `http://<service_network_alias>:9000`, où `service_network_alias` est l'alias réseau défini à l'étape 1. 9000 est le port standard d'Extender (il peut être différent si vous utilisez une configuration personnalisée d'Extender).
3. Exécutez Extender en local comme décrit dans [Exécuter Extender en local avec des artefacts préconfigurés](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts).
