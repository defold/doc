---
title: Налаштування локального сервера збирання
brief: У цьому посібнику описано, як налаштувати й запустити локальний сервер збирання.
---

# Локальне налаштування сервера збирання {#build-server-local-setup}

Є два способи запуску локального сервера збирання (також відомого як «Extender»):
1. Запустити локальний сервер збирання з попередньо налаштованими артефактами.
2. Запустити локальний сервер збирання з локально зібраними артефактами.

## Як запустити локальний Extender із попередньо налаштованими артефактами {#how-to-run-local-extender-with-preconfigured-artifacts}

Перш ніж запускати хмарний сервер збирання локально, потрібно встановити таке програмне забезпечення:

* [Docker](https://www.docker.com/) — Docker — це набір продуктів типу «платформа як сервіс», які використовують віртуалізацію на рівні ОС для постачання програмного забезпечення в пакетах, що називаються контейнерами. Щоб запускати хмарні сервери збирання на локальному комп’ютері для розробки, потрібно встановити [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Google Cloud CLI — Google Cloud CLI — це набір інструментів для створення ресурсів Google Cloud і керування ними. Інструменти можна [встановити безпосередньо від Google](https://cloud.google.com/sdk/docs/install) або за допомогою менеджера пакетів, наприклад Brew, Chocolatey чи Snap.
* Також вам потрібен обліковий запис Google, щоб завантажити контейнери із серверами збирання для конкретних платформ.

Після встановлення зазначеного вище програмного забезпечення виконайте такі кроки, щоб встановити й запустити хмарні сервери збирання Defold:

**Примітка для користувачів Windows**: виконуйте наведені нижче команди в терміналі git bash.

1. __Авторизуйтеся в Google Cloud і створіть стандартні облікові дані застосунку__ — Для завантаження образів контейнерів Docker потрібен обліковий запис Google, щоб ми могли відстежувати й забезпечувати справедливе використання публічного реєстру контейнерів і тимчасово блокувати облікові записи, які завантажують надмірну кількість образів.

   ```sh
   gcloud auth login
   ```
2. __Налаштуйте Docker для використання реєстрів артефактів__ — Docker потрібно налаштувати на використання `gcloud` як допоміжного засобу для роботи з обліковими даними під час завантаження образів контейнерів із публічного реєстру контейнерів за адресою `europe-west1-docker.pkg.dev`.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Перевірте, чи правильно налаштовано Docker і Google Cloud__ — Переконайтеся, що Docker і Google Cloud налаштовано успішно, завантаживши базовий образ, який використовують усі образи контейнерів серверів збирання. Перш ніж виконувати наведену нижче команду, переконайтеся, що Docker Desktop запущено:
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Клонуйте репозиторій Extender__ — Коли Docker і Google Cloud налаштовано правильно, ми майже готові запустити сервери. Перед запуском сервера потрібно клонувати репозиторій Git, що містить сервер збирання:
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __Завантажте попередньо зібрані файли jar__ — Наступний крок — завантажити попередньо зібраний сервер (`extender.jar`) та інструмент злиття маніфестів (`manifestmergetool.jar`):
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
6. __Запустіть сервер__ — Тепер можна запустити сервер, виконавши основну команду docker compose:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
де *profile* може бути:
* **all** — запускає віддалені екземпляри для кожної платформи
* **android** — запускає екземпляр фронтенду та віддалені екземпляри для збирання версії для Android
* **web** — запускає екземпляр фронтенду та віддалені екземпляри для збирання вебверсії
* **linux** — запускає екземпляр фронтенду та віддалені екземпляри для збирання версії для Linux
* **windows** — запускає екземпляр фронтенду та віддалені екземпляри для збирання версії для Windows
* **consoles** — запускає екземпляр фронтенду та віддалені екземпляри для збирання версій для Nintendo Switch/PS4/PS5
* **nintendo** — запускає екземпляр фронтенду та віддалені екземпляри для збирання версії для Nintendo Switch
* **playstation** — запускає екземпляр фронтенду та віддалені екземпляри для збирання версій для PS4/PS5
* **metrics** — запускає VictoriaMetrics і Grafana як серверну частину для метрик та інструмент візуалізації
Докладніше про аргументи `docker compose` див. на https://docs.docker.com/reference/cli/docker/compose/.

Коли docker compose запущено, можна використовувати **http://localhost:9000** як `Build server address` у налаштуваннях редактора або як значення `--build-server`, якщо ви використовуєте Bob для збирання проєкту.

У командному рядку можна передати кілька профілів. Наприклад:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
Наведений вище приклад запускає екземпляри фронтенду, Android, Web і Windows.

Щоб зупинити сервіси, натисніть Ctrl+C, якщо docker compose працює не у фоновому режимі, або виконайте
```sh
docker compose -p extender down
```
якщо docker compose було запущено у фоновому режимі (наприклад, команді `docker compose up` передано прапорець '-d').

Якщо ви хочете завантажити найновіші версії файлів jar, можете скористатися наведеною нижче командою, щоб визначити найновішу версію
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

### А як щодо macOS та iOS? {#what-about-macos-and-ios}

Збірки для macOS та iOS створюють на фізичному обладнанні Apple за допомогою сервера збирання, який працює автономно без Docker. Натомість XCode, Java та інші потрібні інструменти встановлюють безпосередньо на комп’ютер, а сервер збирання працює як звичайний процес Java. Дізнатися, як це налаштувати, можна в [документації сервера збирання на GitHub](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos).


## Як запустити локальний Extender із локально зібраними артефактами {#how-to-run-local-extender-with-locally-built-artifacts}

Дотримуйтеся [інструкцій у репозиторії Extender на GitHub](https://github.com/defold/extender), щоб вручну зібрати й запустити локальний сервер збирання.
