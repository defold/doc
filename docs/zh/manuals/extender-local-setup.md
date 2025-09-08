---
title: 设置本地构建服务器
brief: 本手册描述如何设置和运行本地构建服务器
---

# 构建服务器本地设置

运行本地构建服务器（也称为'Extender'）有两种方式：
1. 使用预配置构件运行本地构建服务器。
2. 使用本地构建的构件运行本地构建服务器。

## 如何使用预配置构件运行本地Extender

在运行本地云构建器之前，您需要安装以下软件：

* [Docker](https://www.docker.com/) - Docker是一组平台即服务产品，使用操作系统级虚拟化来交付称为容器的软件包。要在本地开发机器上运行云构建器，您需要安装[Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Google Cloud CLI - Google Cloud CLI是一组用于创建和管理Google Cloud资源的工具。这些工具可以[直接从Google安装](https://cloud.google.com/sdk/docs/install)或从包管理器（如Brew、Chocolatey或Snap）安装。
* 您还需要一个Google账户来下载包含平台特定构建服务器的容器。

安装上述软件后，请按照以下步骤安装和运行Defold云构建器：

**Windows用户注意**：使用git bash终端执行以下命令。

1. __授权Google Cloud并创建应用程序默认凭据__ - 下载Docker容器镜像时，您需要拥有Google账户，以便我们可以监控并确保公共容器注册表的公平使用，并暂时暂停过度下载镜像的账户。

   ```sh
   gcloud auth login
   ```
2. __配置Docker使用工件注册表__ - 需要将Docker配置为使用`gcloud`作为凭据助手，以便从`europe-west1-docker.pkg.dev`的公共容器注册表下载容器镜像。

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __验证Docker和Google Cloud是否配置正确__ - 通过拉取所有构建服务器容器镜像使用的基础镜像，验证Docker和Google Cloud是否设置成功。在运行以下命令之前，请确保Docker Desktop正在运行：
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __克隆Extender仓库__ - 正确设置Docker和Google Cloud后，我们几乎可以启动服务器了。在启动服务器之前，我们需要克隆包含构建服务器的Git仓库：
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __下载预构建的jar文件__ - 下一步是下载预构建的服务器（`extender.jar`）和清单合并工具（`manifestmergetool.jar`）：
   ```sh
    TMP_DIR=$(pwd)/server/_tmp
    APPLICATION_DIR=$(pwd)/server/app
    # 设置必要的Extender和清单合并工具版本
    # 版本可以在Github发布页面找到 https://github.com/defold/extender/releases
    # 或者您可以拉取最新版本（见下面的代码示例）
    EXTENDER_VERSION=2.6.5
    MANIFESTMERGETOOL_VERSION=1.3.0
    echo "将预构建的jar文件下载到 ${APPLICATION_DIR}"
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
6. __启动服务器__ - 现在我们可以通过运行docker compose主命令来启动服务器：
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
其中*profile*可以是：
* **all** - 为每个平台运行远程实例
* **android** - 运行前端实例 + 用于构建Android版本的远程实例
* **web** - 运行前端实例 + 用于构建Web版本的远程实例
* **linux** - 运行前端实例 + 用于构建Linux版本的远程实例
* **windows** - 运行前端实例 + 用于构建Windows版本的远程实例
* **consoles** - 运行前端实例 + 用于构建Nintendo Switch/PS4/PS5版本的远程实例
* **nintendo** - 运行前端实例 + 用于构建Nintendo Switch版本的远程实例
* **playstation** - 运行前端实例 + 用于构建PS4/PS5版本的远程实例
* **metrics** - 运行VictoriaMetrics + Grafana作为指标后端和可视化工具
有关`docker compose`参数的更多信息，请参见 https://docs.docker.com/reference/cli/docker/compose/。

当docker compose启动后，您可以在编辑器的首选项中使用**http://localhost:9000**作为构建服务器地址，或者如果您使用Bob构建项目，则作为`--build-server`值。

可以将多个配置文件传递给命令行。例如：
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
上面的示例运行前端、Android、Web、Windows实例。

要停止服务 - 如果docker compose以非分离模式运行，请按Ctrl+C，或者
```sh
docker compose -p extender down
```
如果docker compose是以分离模式运行的（例如，向`docker compose up`命令传递了'-d'标志）。

如果您想拉取最新版本的jar文件，可以使用以下命令确定最新版本
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

### 那么macOS和iOS呢？

macOS和iOS的构建是在真实的Apple硬件上完成的，使用在独立模式下运行的构建服务器，而不使用Docker。而是在机器上直接安装XCode、Java和其他必需的工具，构建服务器作为普通的Java进程运行。您可以在[GitHub上的构建服务器文档](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos)中了解如何设置它。


## 如何使用本地构建的构件运行本地Extender

请遵循[GitHub上Extender仓库中的说明](https://github.com/defold/extender)来手动构建和运行本地构建服务器。