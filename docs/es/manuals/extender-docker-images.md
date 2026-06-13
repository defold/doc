---
title: Imágenes Docker disponibles
brief: Describe las imágenes Docker disponibles y las versiones de Defold que las usaron
---

# Imágenes Docker disponibles
A continuación se muestra la lista de todas las imágenes Docker disponibles en el registro público. Las imágenes se pueden usar para ejecutar Extender en un entorno con SDK antiguos que ya no son compatibles.

|SDK               |Etiqueta de imagen                                                                                       |Nombre de plataforma (en la configuración de Extender) |Versiones de Defold que usaron la imagen |
|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------------------------|------------------------------------|
|Linux latest      |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`                                         |Todas las versiones de Defold       |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`                                        |Desde 1.4.3                         |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                                           |Hasta 1.7.0                         |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                                           |[1.8.0-1.9.3]                       |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                                           |Desde 1.9.4                         |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                                          |Hasta 1.6.1                         |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                                          |Desde 1.6.2                         |

# Cómo usar imágenes Docker antiguas
Para usar un entorno antiguo debes seguir estos pasos:
1. Modifica `docker-compose.yml` del repositorio de Extender [enlace](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml). Debes agregar una definición más de servicio con la imagen Docker necesaria. Por ejemplo, si queremos usar la imagen Docker que contiene Emscripten 2.0.11, debemos agregar la siguiente definición de servicio:
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
    Los campos importantes son:
    * **profiles** - lista de perfiles que activan el inicio del servicio. Los nombres de perfil se pasan mediante el argumento `--profile <profile_name>` al comando `docker compose`.
    * **networks** - lista de redes que debe usar el contenedor Docker. Para ejecutar Extender se usa la red con el nombre `default`. Es importante configurar los alias de red del servicio (se usarán más adelante en la configuración de Extender).
2. Agrega la definición del builder remoto en [`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml), en la sección `extender.remote-builder.platforms`. En nuestro ejemplo se verá así:
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    La URL debe tener el siguiente formato: `http://<service_network_alias>:9000`, donde `service_network_alias` es el alias de red del paso 1. 9000 es el puerto estándar para Extender (puede ser diferente si usas una configuración personalizada de Extender).
3. Ejecuta Extender local como se describe en [Cómo ejecutar Extender local con artefactos preconfigurados](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts).
