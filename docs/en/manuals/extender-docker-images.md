---
title: Available Docker images
brief: Document described available Docker images and Defold versions that used it
---

# Avaialble Docker images
Below is a list of all avaialble Docker images in public Registry. That images can be used to run Extender in environment with old SDK that isn't supported yet.

|SDK|Image tag|Platform name (in Extender's config)|Defold version that used image|
|---|---------|------------------------------------|------------------------------|
|Linux latest|europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest|linux-latest|All Defold versions|
|Android NDK25|europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest|android-ndk25|Since 1.4.3|
|Emscripten 2.0.11|europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest|emsdk-2011|Until 1.7.0|
|Emscripten 3.1.55|europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest|emsdk-3155|[1.8.0-1.9.3]|
|Emscripten 3.1.65|europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest|emsdk-3165|Since 1.9.4|
|Winsdk 2019|europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest|winsdk-2019|Until 1.6.1|
|Winsdk 2022|europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest|winsdk-2022|Since 1.6.2|

# How to use old Docker images
To use old environment you should go through following steps:
1. Modify `docker-compose.yml` from Extender's repository [link](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml). Need to add one more definition of service with necessary Docker image. For example, if we want to use Docker image that contains Emscripten 2.0.11 we need to add following service definition:
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
    Important fields are:
    * **profiles** - list of profiles that triggers service start. Profile names passed via `--profile <profile_name>` argument to `docker compose` command.
    * **networks** - list of networks that shoud used by Docker container. For running Extender used network with name `default`. Important to set service network aliases (it will be used in later Extender's configuration).
2. Add definition of remote builder in [application-local-dev-app.yml](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml) in `extender.remote-builder.platforms` section. In our example it will looks like:
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    Url should be in following format: `http://<service_network_alias>:9000`, where `service_network_alias` - network alias from step 1. 9000 - standard port for Extender (can be different if you are using custom Extender configuration).
3. Run local Extender as it described in [How to run local Extender with preconfigured artifacts](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts).