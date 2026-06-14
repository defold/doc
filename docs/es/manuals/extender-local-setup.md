---
title: Configurar un servidor de build local
brief: Manual que describe cómo configurar y ejecutar un servidor de build local
---

# Configuración local del servidor de build

Hay dos variantes para ejecutar un servidor de build local (también conocido como 'Extender'):
1. Ejecutar un servidor de build local con artefactos preconfigurados.
2. Ejecutar un servidor de build local con artefactos compilados localmente.

## Cómo ejecutar Extender local con artefactos preconfigurados {#how-to-run-local-extender-with-preconfigured-artifacts}

Antes de poder ejecutar un builder en la nube local, necesitas instalar el siguiente software:

* [Docker](https://www.docker.com/) - Docker es un conjunto de productos de plataforma como servicio que usan virtualización a nivel de sistema operativo para distribuir software en paquetes llamados contenedores. Para ejecutar los builders en la nube en tu máquina de desarrollo local, necesitas instalar [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Google Cloud CLI - Google Cloud CLI es un conjunto de herramientas para crear y gestionar recursos de Google Cloud. Las herramientas se pueden [instalar directamente desde Google](https://cloud.google.com/sdk/docs/install) o desde un gestor de paquetes como Brew, Chocolatey o Snap.
* También necesitas una cuenta de Google para descargar los contenedores con los servidores de build específicos de cada plataforma.

Cuando tengas instalado el software mencionado arriba, sigue estos pasos para instalar y ejecutar los builders en la nube de Defold:

**Nota para usuarios de Windows**: usa la terminal Git Bash para ejecutar los comandos siguientes.

1. __Autorizar en Google Cloud y crear Application Default Credentials__ - Necesitas tener una cuenta de Google al descargar las imágenes de contenedor de Docker para que podamos supervisar y garantizar un uso justo del registro público de contenedores y suspender temporalmente las cuentas que descarguen imágenes de forma excesiva.

   ```sh
   gcloud auth login
   ```
2. __Configurar Docker para usar Artifact Registry__ - Docker necesita estar configurado para usar `gcloud` como credential helper al descargar imágenes de contenedor del registro público de contenedores en `europe-west1-docker.pkg.dev`.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Verificar que Docker y Google Cloud están configurados correctamente__ - Verifica que Docker y Google Cloud estén configurados correctamente descargando la imagen base usada por todas las imágenes de contenedor del servidor de build. Asegúrate de que Docker Desktop esté ejecutándose antes de ejecutar el comando siguiente:
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Clonar el repositorio de Extender__ - Con Docker y Google Cloud configurados correctamente, ya casi podemos iniciar los servidores. Antes de poder iniciar el servidor, necesitamos clonar el repositorio Git que contiene el servidor de build:
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __Descargar jars precompilados__ - El siguiente paso es descargar el servidor precompilado (`extender.jar`) y la herramienta de fusión de manifiestos (`manifestmergetool.jar`):
   ```sh
    TMP_DIR=$(pwd)/server/_tmp
    APPLICATION_DIR=$(pwd)/server/app
    # establece la versión necesaria de Extender y de la herramienta de fusión de manifiestos
    # las versiones se pueden encontrar en la página de releases de GitHub https://github.com/defold/extender/releases
    # o puedes obtener la versión más reciente (consulta el ejemplo de código de abajo)
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
6. __Iniciar el servidor__ - Ahora podemos iniciar el servidor ejecutando el comando principal de docker compose:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
donde *profile* puede ser:
* **all** - ejecuta instancias remotas para todas las plataformas
* **android** - ejecuta la instancia frontend e instancias remotas para crear la versión de Android
* **web** - ejecuta la instancia frontend e instancias remotas para crear la versión Web
* **linux** - ejecuta la instancia frontend e instancias remotas para crear la versión de Linux
* **windows** - ejecuta la instancia frontend e instancias remotas para crear la versión de Windows
* **consoles** - ejecuta la instancia frontend e instancias remotas para crear versiones de Nintendo Switch/PS4/PS5
* **nintendo** - ejecuta la instancia frontend e instancias remotas para crear la versión de Nintendo Switch
* **playstation** - ejecuta la instancia frontend e instancias remotas para crear versiones de PS4/PS5
* **metrics** - ejecuta VictoriaMetrics + Grafana como backend de métricas y herramienta de visualización
Para más información sobre los argumentos de `docker compose`, consulta https://docs.docker.com/reference/cli/docker/compose/.

Cuando docker compose esté activo, puedes usar **http://localhost:9000** como valor de `Build server address` en las preferencias del editor o como valor de `--build-server` si usas Bob para crear la build del proyecto.

Se pueden pasar varios perfiles a la línea de comando. Por ejemplo:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
El ejemplo anterior ejecuta las instancias frontend, Android, Web y Windows.

Para detener los servicios, presiona Ctrl+C si docker compose se ejecuta en modo no detached, o
```sh
docker compose -p extender down
```
si docker compose se ejecutó en modo detached (por ejemplo, si se pasó el flag '-d' al comando `docker compose up`).

Si quieres descargar las versiones más recientes de los jars, puedes usar el comando siguiente para determinar la versión más reciente
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

### ¿Qué ocurre con macOS e iOS?

Las builds de macOS e iOS se hacen en hardware Apple real usando un servidor de build ejecutado en modo stand-alone sin Docker. En su lugar, Xcode, Java y otras herramientas necesarias se instalan directamente en la máquina, y el servidor de build se ejecuta como un proceso Java normal. Puedes aprender a configurarlo en la [documentación del servidor de build en GitHub](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos).


## Cómo ejecutar Extender local con artefactos compilados localmente

Sigue las [instrucciones del repositorio Extender en GitHub](https://github.com/defold/extender) para compilar y ejecutar manualmente un servidor de build local.
