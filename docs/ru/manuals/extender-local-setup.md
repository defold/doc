---
title: Установка локального сервера сборки
brief: Руководство описывает как установить и запустить локальный сервер сборки
---

# Установка локального сервера сборки

Существует два варианта запуска локального сервера сборки (также известного как 'Extender'):
1. Запуск локального сервера сборки с заранее подготовленными артефактами.
2. Запуск локального сервера сборки с артефактами, собранными локально.

## Как запустить локальный Extender с заранее подготовленными артефактами

Прежде чем вы сможете запустить локальный облачный сборщик, необходимо установить следующее программное обеспечение:

* [Docker](https://www.docker.com/) — Docker — это набор платформенных сервисов, использующих виртуализацию на уровне операционной системы для доставки программного обеспечения в виде контейнеров. Чтобы запускать облачные сборщики на вашей локальной машине, необходимо установить [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Google Cloud CLI — Набор инструментов для создания и управления ресурсами Google Cloud. CLI можно [установить напрямую с сайта Google](https://cloud.google.com/sdk/docs/install) или с помощью пакетного менеджера, такого как Brew, Chocolatey или Snap.
* Также вам понадобится учетная запись Google для загрузки контейнеров с платформенными серверами сборки.

После установки указанного выше программного обеспечения выполните следующие шаги для установки и запуска облачных сборщиков Defold:

**Примечание для пользователей Windows**: используйте git bash для выполнения команд описанных ниже.

1. Авторизуемся в Google Cloud и создаем учетные данные приложения по умолчанию (Application default credentials/ADC)

   ```sh
   gcloud auth login
   ```
2. __Настройте Docker для использования реестра артефактов__ — необходимо настроить Docker для использования `gcloud` в качестве помощника по учетным данным при загрузке образов контейнеров из публичного реестра `europe-west1-docker.pkg.dev`.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Убедитесь, что Docker и Google Cloud настроены корректно__ — Проверьте, что Docker и Google Cloud настроены правильно, выполнив загрузку базового образа, используемого всеми контейнерами сервера сборки. Убедитесь, что Docker Desktop запущен перед выполнением следующей команды:
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Клонируйте репозиторий Extender__ — После корректной настройки Docker и Google Cloud мы почти готовы к запуску серверов. Прежде чем запустить сервер, необходимо клонировать Git-репозиторий, содержащий сервер сборки:
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. Скачиваем готовые jar файлы:
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
6. __Запуск сервера__ — Теперь мы можем запустить сервер, выполнив основную команду docker compose:
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

Когда docker compose запустить, то можно использовать адрес **http://localhost:9000** как адрес сервера сборки в настройках Редактора или как значение для аргумента `--build-server`, если Вы используете Bob для сборки проекта.

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

### Что насчёт macOS и iOS?

Сборки для macOS и iOS выполняются на реальном оборудовании Apple с использованием сервера сборки, работающего в автономном режиме без Docker. Вместо этого XCode, Java и другие необходимые инструменты устанавливаются напрямую на машину, и сервер сборки запускается как обычный Java-процесс. Вы можете узнать, как настроить это, в [документации по серверу сборки на GitHub](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos).


## Как запустить локальный Extender с локально собранными артефактами

Пожалуйста, следуйте [инструкции в репозитории Extender на GitHub](https://github.com/defold/extender), чтобы вручную собрать и запустить локальный сервер сборки.