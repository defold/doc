---
title: 可用的Docker镜像
brief: 文档描述了可用的Docker镜像和使用它们的Defold版本
---

# 可用的Docker镜像
以下是公共注册表中所有可用的Docker镜像列表。这些镜像可用于在不再支持旧SDK的环境中运行Extender。

|SDK               |镜像标签                                                                                                 |平台名称（在Extender配置中） |使用该镜像的Defold版本 |
|------------------|---------------------------------------------------------------------------------------------------------|-----------------------------|-----------------------|
|Linux latest      |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`               |所有Defold版本          |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`              |从1.4.3开始             |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                 |直到1.7.0              |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                 |[1.8.0-1.9.3]          |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                 |从1.9.4开始             |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                |直到1.6.1              |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                |从1.6.2开始             |

# 如何使用旧的Docker镜像
要使用旧环境，您应该按照以下步骤操作：
1. 修改Extender存储库中的`docker-compose.yml`文件[链接](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml)。需要添加一个带有必要Docker镜像的服务定义。例如，如果我们想使用包含Emscripten 2.0.11的Docker镜像，我们需要添加以下服务定义：
    ```yml
    emscripten_2011-dev:
        image: europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest
        extends:
        file: common-services.yml
        service: remote_builder
        profiles:
        - all
        - web
        networks:
        default:
            aliases:
            - emsdk-2011
    ```
    重要字段包括：
    * **profiles** - 触发服务启动的配置文件列表。配置文件名称通过`--profile <profile_name>`参数传递给`docker compose`命令。
    * **networks** - Docker容器应使用的网络列表。运行Extender使用名为`default`的网络。重要的是设置服务网络别名（它将在后续的Extender配置中使用）。
2. 在[`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml)的`extender.remote-builder.platforms`部分添加远程构建器的定义。在我们的示例中，它将如下所示：
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    URL应采用以下格式：`http://<service_network_alias>:9000`，其中`service_network_alias` - 来自步骤1的网络别名。9000 - Extender的标准端口（如果您使用自定义Extender配置，可能会有所不同）。
3. 按照[如何使用预配置构件运行本地Extender](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts)中的描述运行本地Extender。