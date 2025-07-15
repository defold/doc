---
title: Setup local build server
brief: Manual described how to setup and run local build server
---

# Build server local setup

There are two variants how to run local build server (aka 'Extender'):
1. Run local build server with preconfigured artifacts.
2. Run local build server with locally built artifacts.

## How to run local Extender with preconfigured artifacts

Before you can run a local cloud builder you need to install the following software:

* [Docker](https://www.docker.com/) - Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. To run the cloud builders on your local development machine you need to install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Google Cloud CLI - The Google Cloud CLI is a set of tools to create and manage Google Cloud resources. The tools can be [installed directly from Google](https://cloud.google.com/sdk/docs/install) or from a package manager such as Brew, Chocolatey or Snap.
* You also need a Google account to download the containers with the platform specific build servers.

Once you have the above mentioned software installed follow these steps to install and run the Defold cloud builders:

**Note for Windows users**: use git bash terminal for executing commands below.

1. __Authorize to Google Cloud and create Application default credentials__ - You need to have a Google account when downloading the Docker container images so that we can monitor and ensure fair use of the public container registry and temporarily suspend accounts which download images excessively.

   ```sh
   gcloud auth login
   ```
2. __Configure Docker to use Artifact registries__ - Docker needs to be configured to use `gcloud` as a credential helper when downloading container images from the public container registry at `europe-west1-docker.pkg.dev`.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Verify that Docker and Google Cloud are configured correctly__ - Verify that Docker and Google Cloud are set up successfully by pulling the base image used by all of the build server container images. Make sure that Docker Desktop is running before running the command below:
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Clone Extender repository__ - With Docker and Google Cloud correctly set up we are almost ready to start the servers. Before we can start the server we need to clone the Git repository containing the build server:
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __Download prebuilt jars__ - Next step is to download the prebuilt server (`extender.jar`) and manifest merge tool (`manifestmergetool.jar`):
   ```sh
    TMP_DIR=$(pwd)/server/_tmp
    APPLICATION_DIR=$(pwd)/server/app
    # set necessary version of Extender and Manifest merge tool
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
6. __Start the server__ - We can now start the server by running the docker compose main command:
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
For more information about `docker compose` arguments see https://docs.docker.com/reference/cli/docker/compose/.

When docker compose is up you can use **http://localhost:9000** as Build server address in Editor's preference or as `--build-server` value if you use Bob to build the project.

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

### What about macOS and iOS?

The macOS and iOS builds are done on real Apple hardware using a build server running in stand-alone mode without Docker. Instead XCode, Java and other required tools are installed directly on the machine and the build server is running as a normal Java process. You can learn how to set this up in the [build server documentation on GitHub](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos).


## How to run local Extender with locally built artifacts

Please follow the [instructions in the Extender repository on GitHub](https://github.com/defold/extender) to manually build and run a local build server.