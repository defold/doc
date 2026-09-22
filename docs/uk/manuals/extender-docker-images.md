---
title: Доступні образи Docker
brief: У документі описано доступні образи Docker і версії Defold, які їх використовували
---

# Доступні образи Docker {#available-docker-images}
Нижче наведено список усіх доступних образів Docker у публічному реєстрі. Ці образи можна використовувати для запуску Extender у середовищі зі старими SDK, які більше не підтримуються.

|SDK               |Тег образу                                                                                                |Назва платформи (у конфігурації Extender) |Версія Defold, яка використовувала образ |
|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------|
|Linux, найновіша версія |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`                       |Усі версії Defold              |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`                      |Починаючи з 1.4.3              |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                         |До 1.7.0                       |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                         |[1.8.0-1.9.3]                  |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                         |Починаючи з 1.9.4              |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                        |До 1.6.1                       |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                        |Починаючи з 1.6.2              |

# Як використовувати старі образи Docker {#how-to-use-old-docker-images}
Щоб використовувати старе середовище, виконайте такі кроки:
1. Змініть `docker-compose.yml` із репозиторію Extender за цим [посиланням](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml). Додайте ще одне визначення сервісу з потрібним образом Docker. Наприклад, щоб використовувати образ Docker, який містить Emscripten 2.0.11, додайте таке визначення сервісу:
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
    Важливі поля:
    * **profiles** — список профілів, які запускають сервіс. Назви профілів передаються через аргумент `--profile <profile_name>` команді `docker compose`.
    * **networks** — список мереж, які має використовувати контейнер Docker. Для запуску Extender використовується мережа з назвою `default`. Важливо задати мережеві псевдоніми сервісу (їх буде використано пізніше в конфігурації Extender).
2. Додайте визначення віддаленого засобу збирання у файлі [`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml) у розділі `extender.remote-builder.platforms`. У нашому прикладі воно матиме такий вигляд:
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    URL має бути в такому форматі: `http://<service_network_alias>:9000`, де `service_network_alias` — мережевий псевдонім із кроку 1. 9000 — стандартний порт для Extender (він може відрізнятися, якщо ви використовуєте власну конфігурацію Extender).
3. Запустіть локальний Extender, як описано в розділі [Як запустити локальний Extender із попередньо налаштованими артефактами](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts).
