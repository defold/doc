---
title: Konfiguracja lokalnego serwera budowania
brief: Instrukcja opisuje, jak skonfigurować i uruchomić lokalny serwer budowania
---

# Konfiguracja lokalnego serwera budowania

Lokalny serwer budowania (ang. build server, znany też jako Extender) można uruchomić na dwa sposoby:
1. Uruchomić lokalny serwer budowania ze wstępnie skonfigurowanymi artefaktami.
2. Uruchomić lokalny serwer budowania z artefaktami zbudowanymi lokalnie.

## Jak uruchomić lokalny Extender ze wstępnie skonfigurowanymi artefaktami

Zanim uruchomisz lokalny serwer budowania, musisz zainstalować następujące oprogramowanie:

* [Docker](https://www.docker.com/) - Docker to zestaw produktów typu platform as a service, które wykorzystują wirtualizację na poziomie systemu operacyjnego do dostarczania oprogramowania w pakietach zwanych kontenerami. Aby uruchamiać chmurowe serwery budowania na lokalnej maszynie deweloperskiej, musisz zainstalować [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Google Cloud CLI - Google Cloud CLI to zestaw narzędzi do tworzenia zasobów Google Cloud i zarządzania nimi. Narzędzia można [zainstalować bezpośrednio od Google](https://cloud.google.com/sdk/docs/install) albo z menedżera pakietów, takiego jak Brew, Chocolatey lub Snap.
* Potrzebujesz też konta Google, aby pobierać kontenery z serwerami budowania dla poszczególnych platform.

Gdy zainstalujesz powyższe oprogramowanie, wykonaj poniższe kroki, aby zainstalować i uruchomić chmurowe serwery budowania Defold:

**Uwaga dla użytkowników Windows**: do wykonania poniższych poleceń użyj terminala Git Bash.

1. __Autoryzuj się w Google Cloud i utwórz Application default credentials__ - Podczas pobierania obrazów kontenerów Docker musisz mieć konto Google, abyśmy mogli monitorować korzystanie z publicznego rejestru kontenerów, dbać o uczciwe użytkowanie i tymczasowo zawieszać konta, które pobierają obrazy w nadmiernej liczbie.

   ```sh
   gcloud auth login
   ```
2. __Skonfiguruj Docker do używania rejestrów Artifact Registry__ - Docker musi być skonfigurowany tak, aby podczas pobierania obrazów kontenerów z publicznego rejestru kontenerów pod adresem `europe-west1-docker.pkg.dev` używał `gcloud` jako pomocnika poświadczeń.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Sprawdź, czy Docker i Google Cloud są poprawnie skonfigurowane__ - Potwierdź, że Docker i Google Cloud zostały poprawnie skonfigurowane, pobierając obraz bazowy używany przez wszystkie obrazy kontenerów serwera budowania. Zanim uruchomisz poniższe polecenie, upewnij się, że Docker Desktop działa:
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Sklonuj repozytorium Extender__ - Gdy Docker i Google Cloud są już poprawnie skonfigurowane, prawie wszystko jest gotowe do uruchomienia serwera. Zanim go uruchomimy, musimy sklonować repozytorium Git zawierające serwer budowania:
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __Pobierz gotowe pliki JAR__ - Następnym krokiem jest pobranie gotowego serwera (`extender.jar`) i narzędzia do scalania manifestów (`manifestmergetool.jar`):
   ```sh
    TMP_DIR=$(pwd)/server/_tmp
    APPLICATION_DIR=$(pwd)/server/app
    # ustaw wymaganą wersję Extender i narzędzia Manifest merge tool
    # wersje znajdziesz na stronie wydań GitHub: https://github.com/defold/extender/releases
    # albo możesz pobrać najnowszą wersję (zobacz przykład kodu poniżej)
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
6. __Uruchom serwer__ - Możemy teraz uruchomić serwer, wykonując główne polecenie `docker compose`:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
gdzie *profile* może mieć jedną z następujących wartości:
* **all** - uruchamia zdalne instancje dla każdej platformy
* **android** - uruchamia instancję frontendu + zdalne instancje do budowania wersji na Androida
* **web** - uruchamia instancję frontendu + zdalne instancje do budowania wersji Web
* **linux** - uruchamia instancję frontendu + zdalne instancje do budowania wersji Linux
* **windows** - uruchamia instancję frontendu + zdalne instancje do budowania wersji Windows
* **consoles** - uruchamia instancję frontendu + zdalne instancje do budowania wersji na Nintendo Switch/PS4/PS5
* **nintendo** - uruchamia instancję frontendu + zdalne instancje do budowania wersji na Nintendo Switch
* **playstation** - uruchamia instancję frontendu + zdalne instancje do budowania wersji na PS4/PS5
* **metrics** - uruchamia VictoriaMetrics + Grafana jako backend metryk i narzędzie do wizualizacji
Więcej informacji o argumentach `docker compose` znajdziesz pod adresem https://docs.docker.com/reference/cli/docker/compose/.

Gdy `docker compose` działa, możesz użyć **http://localhost:9000** jako adresu w ustawieniu `Build Server` w preferencjach edytora albo jako wartości `--build-server`, jeśli do budowania projektu używasz narzędzia Bob.

W wierszu poleceń można przekazać kilka profili. Na przykład:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
Powyższy przykład uruchamia instancję frontendu oraz instancje Android, Web i Windows.

Aby zatrzymać usługi, naciśnij Ctrl+C, jeśli `docker compose` działa bez odłączenia od terminala, albo
```sh
docker compose -p extender down
```
jeśli `docker compose` uruchomiono w trybie odłączonym (na przykład przekazano flagę `-d` do polecenia `docker compose up`).

Jeśli chcesz pobrać najnowsze wersje plików JAR, możesz użyć poniższego polecenia, aby ustalić najnowsze wersje:
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

### A co z macOS i iOS?

Kompilacje dla macOS i iOS są wykonywane na rzeczywistym sprzęcie Apple przy użyciu serwera budowania działającego w trybie stand-alone, bez Dockera. Zamiast tego Xcode, Java i inne wymagane narzędzia są instalowane bezpośrednio na maszynie, a serwer budowania działa jako zwykły proces Java. Jak to skonfigurować, dowiesz się z [dokumentacji serwera budowania na GitHub](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos).


## Jak uruchomić lokalny Extender z artefaktami zbudowanymi lokalnie

Aby ręcznie zbudować i uruchomić lokalny serwer budowania, postępuj zgodnie z [instrukcjami w repozytorium Extender na GitHub](https://github.com/defold/extender).
