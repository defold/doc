---
title: Lokalen Build-Server einrichten
brief: Dieses Handbuch beschreibt, wie du einen lokalen Build-Server einrichtest und betreibst.
---

# Lokalen Build-Server einrichten {#build-server-local-setup}

Es gibt zwei Möglichkeiten, einen lokalen Build-Server (auch „Extender“ genannt) zu betreiben:
1. Lokalen Build-Server mit vorkonfigurierten Artefakten betreiben.
2. Lokalen Build-Server mit lokal erstellten Artefakten betreiben.

## Lokalen Extender mit vorkonfigurierten Artefakten betreiben {#how-to-run-local-extender-with-preconfigured-artifacts}

Bevor du einen lokalen Cloud-Build-Server betreiben kannst, musst du die folgende Software installieren:

* [Docker](https://www.docker.com/) - Docker ist eine Reihe von Platform-as-a-Service-Produkten, die Virtualisierung auf Betriebssystemebene nutzen, um Software in Paketen bereitzustellen, die Container genannt werden. Um die Cloud-Build-Server auf deinem lokalen Entwicklungsrechner zu betreiben, musst du [Docker Desktop](https://www.docker.com/products/docker-desktop/) installieren.
* Google Cloud CLI - Die Google Cloud CLI ist eine Sammlung von Werkzeugen zum Erstellen und Verwalten von Google-Cloud-Ressourcen. Du kannst die Werkzeuge [direkt von Google installieren](https://cloud.google.com/sdk/docs/install) oder einen Paketmanager wie Brew, Chocolatey oder Snap verwenden.
* Du benötigst außerdem ein Google-Konto, um die Container mit den plattformspezifischen Build-Servern herunterzuladen.

Sobald du die oben genannte Software installiert hast, führe die folgenden Schritte aus, um die Cloud-Build-Server von Defold zu installieren und zu betreiben:

**Hinweis für Windows-Nutzer**: Verwende das Git-Bash-Terminal, um die folgenden Befehle auszuführen.

1. __Autorisierung bei Google Cloud und Erstellung von Standardanmeldedaten für Anwendungen__ - Du benötigst ein Google-Konto, um die Docker-Container-Images herunterzuladen. Dadurch kann das Defold-Team die faire Nutzung der öffentlichen Container-Registry überwachen und sicherstellen sowie Konten vorübergehend sperren, die übermäßig viele Images herunterladen.

   ```sh
   gcloud auth login
   ```
2. __Docker für die Nutzung von Artefakt-Registrys konfigurieren__ - Docker muss so konfiguriert werden, dass es `gcloud` als Hilfsprogramm für Zugangsdaten verwendet, wenn Container-Images aus der öffentlichen Container-Registry unter `europe-west1-docker.pkg.dev` heruntergeladen werden.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Überprüfen, ob Docker und Google Cloud richtig konfiguriert sind__ - Überprüfe, ob Docker und Google Cloud erfolgreich eingerichtet sind, indem du das Basis-Image herunterlädst, das alle Container-Images der Build-Server verwenden. Stelle sicher, dass Docker Desktop läuft, bevor du den folgenden Befehl ausführst:
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Extender-Repository klonen__ - Wenn Docker und Google Cloud richtig eingerichtet sind, sind wir fast bereit, die Server zu starten. Bevor wir den Server starten können, müssen wir das Git-Repository klonen, das den Build-Server enthält:
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __Vorgefertigte JAR-Dateien herunterladen__ - Als Nächstes lädst du den vorgefertigten Server (`extender.jar`) und das Werkzeug zum Zusammenführen von Manifesten (`manifestmergetool.jar`) herunter:
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
6. __Server starten__ - Wir können den Server jetzt starten, indem wir den Hauptbefehl von docker compose ausführen:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
Dabei kann *profile* einen der folgenden Werte haben:
* **all** - startet Remote-Instanzen für jede Plattform
* **android** - startet die Frontend-Instanz + Remote-Instanzen zum Erstellen der Android-Version
* **web** - startet die Frontend-Instanz + Remote-Instanzen zum Erstellen der Webversion
* **linux** - startet die Frontend-Instanz + Remote-Instanzen zum Erstellen der Linux-Version
* **windows** - startet die Frontend-Instanz + Remote-Instanzen zum Erstellen der Windows-Version
* **consoles** - startet die Frontend-Instanz + Remote-Instanzen zum Erstellen der Versionen für Nintendo Switch/PS4/PS5
* **nintendo** - startet die Frontend-Instanz + Remote-Instanzen zum Erstellen der Nintendo-Switch-Version
* **playstation** - startet die Frontend-Instanz + Remote-Instanzen zum Erstellen der PS4/PS5-Versionen
* **metrics** - startet VictoriaMetrics + Grafana als Backend für Metriken und als Werkzeug zur Visualisierung
Weitere Informationen zu den Argumenten von `docker compose` findest du unter https://docs.docker.com/reference/cli/docker/compose/.

Sobald docker compose läuft, kannst du **http://localhost:9000** als `Build server address` in den Editoreinstellungen verwenden oder als Wert für `--build-server`, wenn du das Projekt mit Bob erstellst.

Du kannst mehrere Profile auf der Kommandozeile übergeben. Zum Beispiel:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
Das obige Beispiel startet Instanzen für das Frontend, Android, Web und Windows.

Um die Dienste zu stoppen, drücke Ctrl+C, wenn docker compose im Vordergrund läuft, oder führe folgenden Befehl aus, 
```sh
docker compose -p extender down
```
wenn docker compose im Hintergrund gestartet wurde (z. B. wenn die Option '-d' an den Befehl `docker compose up` übergeben wurde).

Wenn du die neuesten Versionen der JAR-Dateien herunterladen möchtest, kannst du mit dem folgenden Befehl die jeweils neueste Version ermitteln:
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

### Wie sieht es mit macOS und iOS aus? {#what-about-macos-and-ios}

Die Builds für macOS und iOS werden auf echter Apple-Hardware mit einem Build-Server erstellt, der eigenständig ohne Docker läuft. Stattdessen werden XCode, Java und andere erforderliche Werkzeuge direkt auf dem Rechner installiert, und der Build-Server läuft als normaler Java-Prozess. Wie du das einrichtest, erfährst du in der [Dokumentation zum Build-Server auf GitHub](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos).


## Lokalen Extender mit lokal erstellten Artefakten betreiben {#how-to-run-local-extender-with-locally-built-artifacts}

Befolge die [Anweisungen im Extender-Repository auf GitHub](https://github.com/defold/extender), um einen lokalen Build-Server manuell zu erstellen und zu betreiben.
