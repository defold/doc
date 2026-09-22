---
title: Configuration d'un serveur de build local
brief: Ce manuel explique comment configurer et exécuter un serveur de build local.
---

# Configuration locale du serveur de build {#build-server-local-setup}

Il existe deux façons d'exécuter un serveur de build local (également appelé « Extender ») :
1. Exécuter un serveur de build local avec des artefacts préconfigurés.
2. Exécuter un serveur de build local avec des artefacts compilés localement.

## Exécuter Extender en local avec des artefacts préconfigurés {#how-to-run-local-extender-with-preconfigured-artifacts}

Avant de pouvoir exécuter un serveur de build cloud en local, vous devez installer les logiciels suivants :

* [Docker](https://www.docker.com/) - Docker est un ensemble de produits de type plateforme en tant que service qui utilisent la virtualisation au niveau du système d'exploitation pour distribuer des logiciels sous forme de paquets appelés conteneurs. Pour exécuter les serveurs de build cloud sur votre machine de développement locale, vous devez installer [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Google Cloud CLI - Google Cloud CLI est un ensemble d'outils permettant de créer et de gérer des ressources Google Cloud. Ces outils peuvent être [installés directement depuis Google](https://cloud.google.com/sdk/docs/install) ou depuis un gestionnaire de paquets tel que Brew, Chocolatey ou Snap.
* Vous avez également besoin d'un compte Google pour télécharger les conteneurs contenant les serveurs de build propres à chaque plateforme.

Une fois les logiciels mentionnés ci-dessus installés, suivez ces étapes pour installer et exécuter les serveurs de build cloud Defold :

**Remarque pour les utilisateurs de Windows** : utilisez le terminal git bash pour exécuter les commandes ci-dessous.

1. __Authentifiez-vous auprès de Google Cloud et créez des identifiants d'application par défaut__ - Vous devez disposer d'un compte Google pour télécharger les images de conteneurs Docker afin que nous puissions surveiller et garantir une utilisation équitable du registre public de conteneurs, et suspendre temporairement les comptes qui téléchargent un nombre excessif d'images.

   ```sh
   gcloud auth login
   ```
2. __Configurez Docker pour utiliser les registres d'artefacts__ - Docker doit être configuré pour utiliser `gcloud` comme assistant de gestion des identifiants lors du téléchargement d'images de conteneurs depuis le registre public de conteneurs situé à l'adresse `europe-west1-docker.pkg.dev`.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Vérifiez que Docker et Google Cloud sont correctement configurés__ - Vérifiez que Docker et Google Cloud sont correctement configurés en téléchargeant l'image de base utilisée par toutes les images de conteneurs des serveurs de build. Assurez-vous que Docker Desktop est en cours d'exécution avant d'exécuter la commande ci-dessous :
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Clonez le dépôt Extender__ - Maintenant que Docker et Google Cloud sont correctement configurés, nous sommes presque prêts à démarrer les serveurs. Avant de pouvoir démarrer le serveur, nous devons cloner le dépôt Git contenant le serveur de build :
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __Téléchargez les fichiers jar précompilés__ - L'étape suivante consiste à télécharger le serveur précompilé (`extender.jar`) et l'outil de fusion des manifestes (`manifestmergetool.jar`) :
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
6. __Démarrez le serveur__ - Nous pouvons maintenant démarrer le serveur en exécutant la commande principale docker compose :
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
où *profile* peut être :
* **all** - exécute les instances distantes pour toutes les plateformes
* **android** - exécute une instance frontale + les instances distantes pour compiler la version Android
* **web** - exécute une instance frontale + les instances distantes pour compiler la version Web
* **linux** - exécute une instance frontale + les instances distantes pour compiler la version Linux
* **windows** - exécute une instance frontale + les instances distantes pour compiler la version Windows
* **consoles** - exécute une instance frontale + les instances distantes pour compiler les versions Nintendo Switch/PS4/PS5
* **nintendo** - exécute une instance frontale + les instances distantes pour compiler la version Nintendo Switch
* **playstation** - exécute une instance frontale + les instances distantes pour compiler les versions PS4/PS5
* **metrics** - exécute VictoriaMetrics + Grafana comme serveur de métriques et outil de visualisation
Pour plus d'informations sur les arguments de `docker compose`, consultez https://docs.docker.com/reference/cli/docker/compose/.

Lorsque docker compose est en cours d'exécution, vous pouvez utiliser **http://localhost:9000** comme `Build server address` dans les préférences de l'éditeur, ou comme valeur de `--build-server` si vous utilisez Bob pour compiler le projet.

Plusieurs profils peuvent être passés en ligne de commande. Par exemple :
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
L'exemple ci-dessus exécute les instances frontale, Android, Web et Windows.

Pour arrêter les services - Appuyez sur Ctrl+C si docker compose est exécuté en mode non détaché, ou 
```sh
docker compose -p extender down
```
si docker compose a été exécuté en mode détaché (par exemple, si l'option '-d' a été passée à la commande `docker compose up`).

Si vous souhaitez télécharger les dernières versions des fichiers jar, vous pouvez utiliser la commande suivante pour déterminer la dernière version
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

### Qu'en est-il de macOS et iOS ? {#what-about-macos-and-ios}

Les builds macOS et iOS sont réalisés sur du matériel Apple physique à l'aide d'un serveur de build exécuté en mode autonome sans Docker. XCode, Java et les autres outils nécessaires sont alors installés directement sur la machine, et le serveur de build s'exécute comme un processus Java ordinaire. Vous pouvez découvrir comment configurer cela dans la [documentation du serveur de build sur GitHub](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos).


## Exécuter Extender en local avec des artefacts compilés localement {#how-to-run-local-extender-with-locally-built-artifacts}

Suivez les [instructions du dépôt Extender sur GitHub](https://github.com/defold/extender) pour compiler et exécuter manuellement un serveur de build local.
