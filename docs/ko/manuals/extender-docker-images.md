---
title: 사용 가능한 Docker 이미지
brief: 사용 가능한 Docker 이미지와 이를 사용한 Defold 버전을 설명합니다
---

# 사용 가능한 Docker 이미지
아래는 public Registry에서 제공되는 모든 Docker 이미지 목록입니다. 이 이미지들은 더 이상 지원되지 않는 오래된 SDK가 포함된 환경에서 Extender를 실행하는 데 사용할 수 있습니다.

|SDK               |이미지 태그                                                                                              |플랫폼 이름(Extender config 기준)    |이미지를 사용한 Defold 버전     |
|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------|
|Linux latest      |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`                       |모든 Defold 버전               |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`                      |1.4.3부터                      |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                         |1.7.0까지                      |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                         |[1.8.0-1.9.3]                  |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                         |1.9.4부터                      |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                        |1.6.1까지                      |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                        |1.6.2부터                      |

# 오래된 Docker 이미지 사용 방법
오래된 환경을 사용하려면 다음 단계를 수행해야 합니다:
1. Extender 저장소의 `docker-compose.yml`을 수정합니다 [링크](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml). 필요한 Docker 이미지를 사용하는 서비스 정의를 하나 더 추가해야 합니다. 예를 들어 Emscripten 2.0.11이 포함된 Docker 이미지를 사용하려면 다음 서비스 정의를 추가해야 합니다:
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
    중요한 필드는 다음과 같습니다:
    * **profiles** - 서비스 시작을 트리거하는 profiles 목록입니다. Profile 이름은 `docker compose` 명령에 `--profile <profile_name>` 인자로 전달됩니다.
    * **networks** - Docker 컨테이너에서 사용해야 하는 networks 목록입니다. Extender를 실행할 때는 `default`라는 이름의 network를 사용합니다. 서비스 network aliases를 설정하는 것이 중요합니다(이후 Extender 설정에서 사용됩니다).
2. [`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml)의 `extender.remote-builder.platforms` 섹션에 원격 빌더(remote builder) 정의를 추가합니다. 이 예제에서는 다음과 같습니다:
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    URL은 다음 형식이어야 합니다: `http://<service_network_alias>:9000`. 여기서 `service_network_alias`는 1단계의 network alias입니다. 9000은 Extender의 표준 포트입니다(커스텀 Extender 설정을 사용하는 경우 다를 수 있습니다).
3. [사전 구성된 아티팩트로 로컬 Extender를 실행하는 방법](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts)에 설명된 대로 로컬 Extender를 실행합니다.
