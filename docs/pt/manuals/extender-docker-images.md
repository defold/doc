---
title: Imagens Docker disponíveis
brief: Este documento descreve as imagens Docker disponíveis e as versões do Defold que as usaram
---

# Imagens Docker disponíveis
Abaixo está a lista de todas as imagens Docker disponíveis no registro público. As imagens podem ser usadas para executar o Extender em um ambiente com SDKs antigos que não são mais suportados.

|SDK               |Tag da imagem                                                                                           |Nome da plataforma (na configuração do Extender) |Versão do Defold que usou a imagem |
|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------|
|Linux latest      |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`                       |Todas as versões do Defold     |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`                      |Desde 1.4.3                    |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                         |Até 1.7.0                      |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                         |[1.8.0-1.9.3]                  |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                         |Desde 1.9.4                    |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                        |Até 1.6.1                      |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                        |Desde 1.6.2                    |

# Como usar imagens Docker antigas
Para usar um ambiente antigo, siga estas etapas:
1. Modifique o `docker-compose.yml` do repositório do Extender [link](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml). É preciso adicionar mais uma definição de serviço com a imagem Docker necessária. Por exemplo, se quisermos usar a imagem Docker que contém o Emscripten 2.0.11, precisamos adicionar a seguinte definição de serviço:
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
    Campos importantes:
    * **profiles** - lista de profiles que acionam a inicialização do serviço. Os nomes dos profiles são passados pelo argumento `--profile <profile_name>` ao comando `docker compose`.
    * **networks** - lista de redes que devem ser usadas pelo container Docker. Para executar o Extender, é usada a rede chamada `default`. É importante definir aliases de rede do serviço (eles serão usados depois na configuração do Extender).
2. Adicione a definição do remote builder em [`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml) na seção `extender.remote-builder.platforms`. Em nosso exemplo, ela ficará assim:
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    A URL deve estar no seguinte formato: `http://<service_network_alias>:9000`, em que `service_network_alias` é o alias de rede da etapa 1. 9000 é a porta padrão do Extender (pode ser diferente se você estiver usando uma configuração personalizada do Extender).
3. Execute o Extender local conforme descrito em [Como executar o Extender local com artefatos pré-configurados](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts).
