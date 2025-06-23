---
title: Доступные образы Docker
brief: Документ описывает доступные образы Docker и версии Defold, которые их используют
---

# Доступные образы Docker
Ниже представлен список всех доступных Docker-образов в публичном реестре. Эти образы можно использовать для запуска Extender в среде с устаревшими SDK, которые больше не поддерживаются.

| SDK               | Тег образа                                                                                                   | Название платформы (в конфигурации Extender)| Версия Defold, использовавшая образ |
|-------------------|--------------------------------------------------------------------------------------------------------------|---------------------------------------------|-------------------------------------|
| Linux latest      | europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest               | linux-latest                                | Все версии Defold                   |
| Android NDK25     | europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest       | android-ndk25                               | Начиная с 1.4.3                     |
| Emscripten 2.0.11 | europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest          | emsdk-2011                                  | До 1.7.0                            |
| Emscripten 3.1.55 | europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest          | emsdk-3155                                  | [1.8.0-1.9.3]                       |
| Emscripten 3.1.65 | europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest          | emsdk-3165                                  | Начиная с 1.9.4                     |
| Winsdk 2019       | europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest         | winsdk-2019                                 | До 1.6.1                            |
| Winsdk 2022       | europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest         | winsdk-2022                                 | Начиная с 1.6.2                     |

# Как использовать старые образы Docker
Для использования старой среды выполните следующие шаги:
1. Измените `docker-compose.yml` из репозитория Extender [ссылка](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml). Необходимо добавить ещё одно определение сервиса с нужным образом Docker. Например, если мы хотим использовать Docker-образ, содержащий Emscripten 2.0.11, нужно добавить следующее определение сервиса:
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
    Важные поля:
    - **profiles** — список профилей, при которых запускается сервис. Названия профилей передаются через аргумент `--profile <profile_name>` команде `docker compose`.
    - **networks** — список сетей, которые должны использоваться контейнером Docker. Для работы Extender используется сеть с именем `default`. Важно задать сетевые алиасы сервиса (они будут использоваться позже в конфигурации Extender).
2. Добавьте определение удаленного билдера в [application-local-dev-app.yml](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml) в секции `extender.remote-builder.platforms`. В нашем примере это будет выглядеть так:
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    URL должен быть в формате `http://<service_network_alias>:9000`, где `service_network_alias` — это сетевой алиас из шага 1. Порт 9000 является стандартным для Extender (может отличаться, если вы используете пользовательскую конфигурацию Extender).
3. Запустите локальный Extender, как описано в [Как запустить локальный Extender с предварительно настроенными артефактами](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts).