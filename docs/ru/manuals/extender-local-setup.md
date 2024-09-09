---
title: Установка локального сервера сборки
brief: Руководство описывает как установить и запустить локальный сервер сборки
---

# Устновка локального сервера сборки
Существует два способа запуска локального сервера сборки (Extender):
1. Запуск локального сервера сборки с готовыми артефактами.
2. Сборка всех необходимых артефактов локально и использование этих артефактов для запуска локального сервера сборки.

## Как запустить локальный сервер сборки с готовыми артефактами

### Предустановки
* **Docker** - https://www.docker.com/products/docker-desktop/
* **gcloud cli** - https://cloud.google.com/sdk/docs/install
* **google account**

### Как использовать готовые образы Docker
1. Клонируем репозиторий `Extender`
   ```sh
   git clone https://github.com/defold/extender.git
   ```
2. Авторизуемся в Google Cloud и создаем учетные данные приложения по умолчанию (Application default credentials/ADC)
   ```sh
   gcloud auth application-default login
   ```
3. Конфигурируем Docker для использования реестра Артефактов
   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
4. Проверяем, что все сконфигурировано корректно путем скачивания базового образа. Запустите
   ```sh
   docker pull europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
5. Скачиваем готовые jar файлы:
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
6. Запускаем docker compose
главная команда
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
где *profile* может быть:
* **all** - запускает все сервисы, которые нужны для сборки на всех поддерживаемых платформах
* **android** - запускает frontend сервис + сервис для сборки Android версии
* **web** - запускает frontend сервис + сервис для сборки Web версии
* **linux** - запускает frontend сервис + сервис для сборки Linux версии
* **windows** - запускает frontend сервис + сервис для сборки Windows версии
* **consoles** - запускает frontend сервис + сервисы для сборки Nintendo Switch/PS4/PS5 версий
* **nintendo** - запускает frontend сервис + сервис для сборки Nintendo Switch версии
* **playstation** - запускает frontend сервис + сервисы для сборки PS4/PS5 версий
* **metrics** - запускает VictoriaMetrics + Grafana в качестве сервиса для сбора метрик и их визуализации
Для дополнительной информации о том, какие аргументы могут быть переданы команде `docker compose` смотрите https://docs.docker.com/reference/cli/docker/compose/.

Несколько профилей может быть одновременно передано в командную строку. Например:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
Пример выше запустит frontend сервис, а также сервисы для сборки Android, Web, Windows.

Для остановки всех сервисов - нажмите Ctrl+C если docker compose запущен в режиме без отсоединения, или
```sh
docker compose -p extender down
```
если docker compose был запущен в режиме отсоединения (т.е. флаг '-d' был передан при выполнении команды `docker compose up`).

Если вы хотите скачать последние версии jar файлов, то вы можете использовать следующие команды для определения последних доступных для скачивания версий
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