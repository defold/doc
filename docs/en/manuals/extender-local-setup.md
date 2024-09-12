---
title: Setup local build server
brief: Manual described how to setup and run local build server
---

# Build server local setup

There are two variants how to run local build server (aka 'Extender'):
1. Run local build server with preconfigured artifacts.
2. Build all necessary artifacts locally and use it to run local build server.

## How to run local Extender with preconfigured artifacts

### Prerequisites
* **Docker** - https://www.docker.com/products/docker-desktop/
* **gcloud cli** - https://cloud.google.com/sdk/docs/install
* **google account**

### How to use ready-to-use Docker images
1. Authorize to Google Cloud and create Application default credentials
   ```sh
   gcloud auth application-default login
   ```
2. Configure Docker to use Artifact registries
   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. Check that Docker is running.
4. Check that everything set up correctly by pulling base image. Run
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
5. Clone `Extender` repository and switch to cloned repository root folder
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
6. Download prebuilt jars:
   ```sh
    TMP_DIR=$(pwd)/server/_tmp
    APPLICATION_DIR=$(pwd)/server/app
    # set nesessary version of Extender and Manifest merge tool
    # versions can be found at Github release page https://github.com/defold/extender/releases
    # or you can pull latest version (see code sample below)
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
7. Run docker compose:
main command
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
where *profile* can be:
* **all** - runs remote instances for every platform
* **android** - runs frontend instance + remote instances to build Android version
* **web** - runs frontend instance + remote instances to build Web version
* **linux** - runs frontend instance + remote instances to build Linux version
* **windows** - runs frontend instance + remote instances to build Windows version
* **consoles** - runs frontend instance + remote instances to build Nintendo Switch/PS4/PS5 versions
* **nintendo** - runs frontend instance + remote instances to build Nintendo Switch version
* **playstation** - runs frontend instance + remote instances to build PS4/PS5 versions
* **metrics** - runs VictoriaMetrics + Grafana as metrics backend and tool for visualization
For more information about `docker compose` argumets see https://docs.docker.com/reference/cli/docker/compose/.

When docker compose is up you can use **http://localhost:9000** as Build server address in Editor's prefence or as `--build-server` value if you use Bob to build the project.

Several profiles can be passed to command line. For example:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
Example above runs frontend, Android, Web, Windows instances.

To stop services - Press Ctrl+C if docker compose runs in non-detached mode, or 
```sh
docker compose -p extender down
```
if docker compose was run in detached mode (e.g. '-d' flag was passed to `docker compose up` command).

If you want to pull latest versions of jars you can use following command to determine latest version
```sh
    EXTENDER_VERSION=$(gcloud artifacts versions list \
        --location=europe-west1 \
        --repository=extender-maven \
        --package="com.defold.extender:server" \
        --sort-by="~createTime" \
        --limit=1 \
        --format="get(name)" | awk -F'/' '{print $NF}')

    MANIFESTMERGETOOL_VERSION=$(gcloud artifacts versions list \
        --location=europe-west1 \
        --repository=extender-maven \
        --package="com.defold.extender:manifestmergetool" \
        --sort-by="~createTime" \
        --limit=1 \
        --format="get(name)" | awk -F'/' '{print $NF}')
```