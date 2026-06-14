---
title: 로컬 빌드 서버 설정
brief: 로컬 빌드 서버를 설정하고 실행하는 방법을 설명하는 매뉴얼입니다
---

# 빌드 서버 로컬 설정 {#build-server-local-setup}

로컬 빌드 서버(일명 'Extender')를 실행하는 방법은 두 가지입니다:
1. 사전 구성된 아티팩트로 로컬 빌드 서버를 실행합니다.
2. 로컬에서 빌드한 아티팩트로 로컬 빌드 서버를 실행합니다.

## 사전 구성된 아티팩트로 로컬 Extender를 실행하는 방법 {#how-to-run-local-extender-with-preconfigured-artifacts}

로컬 클라우드 빌더를 실행하려면 먼저 다음 소프트웨어를 설치해야 합니다:

* [Docker](https://www.docker.com/) - Docker는 OS 수준 가상화를 사용해 컨테이너라는 패키지로 소프트웨어를 제공하는 PaaS 제품군입니다. 로컬 개발 머신에서 클라우드 빌더를 실행하려면 [Docker Desktop](https://www.docker.com/products/docker-desktop/)을 설치해야 합니다.
* Google Cloud CLI - Google Cloud CLI는 Google Cloud 리소스를 생성하고 관리하는 도구 모음입니다. 이 도구는 [Google에서 직접 설치](https://cloud.google.com/sdk/docs/install)하거나 Brew, Chocolatey, Snap 같은 패키지 매니저에서 설치할 수 있습니다.
* 플랫폼별 빌드 서버가 포함된 컨테이너를 다운로드하려면 Google 계정도 필요합니다.

위 소프트웨어를 설치한 뒤 다음 단계에 따라 Defold 클라우드 빌더를 설치하고 실행합니다:

**Windows 사용자를 위한 참고**: 아래 명령을 실행할 때는 git bash 터미널을 사용하세요.

1. __Google Cloud에 인증하고 Application default credentials 생성하기__ - Docker 컨테이너 이미지를 다운로드하려면 Google 계정이 필요합니다. 이는 public container registry의 공정한 사용을 모니터링하고 보장하며, 이미지를 과도하게 다운로드하는 계정을 일시적으로 정지할 수 있게 하기 위한 것입니다.

   ```sh
   gcloud auth login
   ```
2. __Artifact registries를 사용하도록 Docker 구성하기__ - `europe-west1-docker.pkg.dev`의 public container registry에서 컨테이너 이미지를 다운로드할 때 Docker가 `gcloud`를 credential helper로 사용하도록 구성해야 합니다.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Docker와 Google Cloud가 올바르게 구성되었는지 확인하기__ - 모든 빌드 서버 컨테이너 이미지에서 사용하는 기본 이미지를 가져와 Docker와 Google Cloud가 성공적으로 설정되었는지 확인합니다. 아래 명령을 실행하기 전에 Docker Desktop이 실행 중인지 확인하세요:
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Extender 저장소 클론하기__ - Docker와 Google Cloud가 올바르게 설정되면 서버를 시작할 준비가 거의 끝납니다. 서버를 시작하기 전에 빌드 서버가 들어 있는 Git 저장소를 클론해야 합니다:
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __사전 빌드된 jar 다운로드하기__ - 다음 단계는 사전 빌드된 서버(`extender.jar`)와 메니페스트 병합 도구(`manifestmergetool.jar`)를 다운로드하는 것입니다:
   ```sh
    TMP_DIR=$(pwd)/server/_tmp
    APPLICATION_DIR=$(pwd)/server/app
    # 필요한 Extender와 메니페스트 병합 도구 버전을 설정합니다
    # 버전은 GitHub 릴리스 페이지(https://github.com/defold/extender/releases)에서 확인할 수 있습니다
    # 또는 최신 버전을 가져올 수 있습니다(아래 코드 샘플 참조)
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
6. __서버 시작하기__ - 이제 docker compose 메인 명령을 실행해 서버를 시작할 수 있습니다:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
여기서 *profile*은 다음 중 하나일 수 있습니다:
* **all** - 모든 플랫폼의 원격 인스턴스를 실행합니다
* **android** - Android 버전을 빌드하기 위한 프론트엔드 인스턴스와 원격 인스턴스를 실행합니다
* **web** - Web 버전을 빌드하기 위한 프론트엔드 인스턴스와 원격 인스턴스를 실행합니다
* **linux** - Linux 버전을 빌드하기 위한 프론트엔드 인스턴스와 원격 인스턴스를 실행합니다
* **windows** - Windows 버전을 빌드하기 위한 프론트엔드 인스턴스와 원격 인스턴스를 실행합니다
* **consoles** - Nintendo Switch/PS4/PS5 버전을 빌드하기 위한 프론트엔드 인스턴스와 원격 인스턴스를 실행합니다
* **nintendo** - Nintendo Switch 버전을 빌드하기 위한 프론트엔드 인스턴스와 원격 인스턴스를 실행합니다
* **playstation** - PS4/PS5 버전을 빌드하기 위한 프론트엔드 인스턴스와 원격 인스턴스를 실행합니다
* **metrics** - 메트릭 백엔드 및 시각화 도구로 VictoriaMetrics와 Grafana를 실행합니다
`docker compose` 인자에 대한 자세한 내용은 https://docs.docker.com/reference/cli/docker/compose/ 를 참조하세요.

docker compose가 실행 중이면 Editor Preferences 창에서 **http://localhost:9000**을 `Build server address`로 사용하거나, Bob으로 프로젝트를 빌드하는 경우 `--build-server` 값으로 사용할 수 있습니다.

커맨드 라인에 여러 profile을 전달할 수 있습니다. 예:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
위 예제는 프론트엔드, Android, Web, Windows 인스턴스를 실행합니다.

서비스를 중지하려면 docker compose가 non-detached mode로 실행 중인 경우 Ctrl+C를 누르거나,
```sh
docker compose -p extender down
```
docker compose가 detached mode로 실행된 경우(예: `docker compose up` 명령에 '-d' 플래그를 전달한 경우) 위 명령을 실행합니다.

최신 jar 버전을 가져오려면 다음 명령을 사용해 최신 버전을 확인할 수 있습니다
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

### macOS와 iOS는 어떻게 하나요? {#what-about-macos-and-ios}

macOS와 iOS 빌드는 Docker 없이 독립 실행(stand-alone) 모드로 실행되는 빌드 서버를 사용해 실제 Apple 하드웨어에서 수행됩니다. 대신 XCode, Java 및 기타 필요한 도구를 머신에 직접 설치하고, 빌드 서버는 일반 Java 프로세스로 실행됩니다. 설정 방법은 GitHub의 [빌드 서버 문서](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos)에서 확인할 수 있습니다.


## 로컬에서 빌드한 아티팩트로 로컬 Extender를 실행하는 방법 {#how-to-run-local-extender-with-locally-built-artifacts}

로컬 빌드 서버를 직접 빌드하고 실행하려면 GitHub의 [Extender 저장소 지침](https://github.com/defold/extender)을 따르세요.
