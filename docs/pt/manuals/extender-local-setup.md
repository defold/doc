---
title: Configurar servidor de build local
brief: Este manual descreve como configurar e executar um servidor de build local
---

# Configuração local do servidor de build

Há duas variantes para executar o servidor de build local (também conhecido como 'Extender'):
1. Executar o servidor de build local com artefatos pré-configurados.
2. Executar o servidor de build local com artefatos compilados localmente.

## Como executar o Extender local com artefatos pré-configurados

Antes de executar um cloud builder local, você precisa instalar o seguinte software:

* [Docker](https://www.docker.com/) - Docker é um conjunto de produtos de plataforma como serviço que usam virtualização em nível de sistema operacional para entregar software em pacotes chamados containers. Para executar os cloud builders na sua máquina de desenvolvimento local, você precisa instalar o [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Google Cloud CLI - O Google Cloud CLI é um conjunto de ferramentas para criar e gerenciar recursos do Google Cloud. As ferramentas podem ser [instaladas diretamente pelo Google](https://cloud.google.com/sdk/docs/install) ou por um gerenciador de pacotes como Brew, Chocolatey ou Snap.
* Você também precisa de uma conta Google para baixar os containers com os servidores de build específicos de plataforma.

Depois de instalar o software mencionado acima, siga estas etapas para instalar e executar os cloud builders do Defold:

**Observação para usuários Windows**: use o terminal git bash para executar os comandos abaixo.

1. __Autorize no Google Cloud e crie credenciais Application Default__ - Você precisa ter uma conta Google ao baixar as imagens de container Docker para que possamos monitorar e garantir uso justo do registro público de containers e suspender temporariamente contas que baixem imagens excessivamente.

   ```sh
   gcloud auth login
   ```
2. __Configure o Docker para usar Artifact Registry__ - O Docker precisa ser configurado para usar `gcloud` como helper de credenciais ao baixar imagens de container do registro público de containers em `europe-west1-docker.pkg.dev`.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Verifique se Docker e Google Cloud estão configurados corretamente__ - Verifique se Docker e Google Cloud foram configurados com sucesso baixando a imagem base usada por todas as imagens de container do servidor de build. Certifique-se de que o Docker Desktop esteja em execução antes de rodar o comando abaixo:
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Clone o repositório Extender__ - Com Docker e Google Cloud configurados corretamente, estamos quase prontos para iniciar os servidores. Antes de iniciar o servidor, precisamos clonar o repositório Git que contém o servidor de build:
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __Baixe os jars pré-compilados__ - A próxima etapa é baixar o servidor pré-compilado (`extender.jar`) e a ferramenta de merge de manifesto (`manifestmergetool.jar`):
   ```sh
    TMP_DIR=$(pwd)/server/_tmp
    APPLICATION_DIR=$(pwd)/server/app
    # defina a versão necessária do Extender e da ferramenta Manifest merge
    # as versões podem ser encontradas na página de releases do GitHub https://github.com/defold/extender/releases
    # ou você pode baixar a versão mais recente (veja o exemplo de código abaixo)
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
6. __Inicie o servidor__ - Agora podemos iniciar o servidor executando o comando principal do docker compose:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
em que *profile* pode ser:
* **all** - executa instâncias remotas para todas as plataformas
* **android** - executa a instância frontend + instâncias remotas para compilar a versão Android
* **web** - executa a instância frontend + instâncias remotas para compilar a versão Web
* **linux** - executa a instância frontend + instâncias remotas para compilar a versão Linux
* **windows** - executa a instância frontend + instâncias remotas para compilar a versão Windows
* **consoles** - executa a instância frontend + instâncias remotas para compilar versões Nintendo Switch/PS4/PS5
* **nintendo** - executa a instância frontend + instâncias remotas para compilar a versão Nintendo Switch
* **playstation** - executa a instância frontend + instâncias remotas para compilar versões PS4/PS5
* **metrics** - executa VictoriaMetrics + Grafana como backend de métricas e ferramenta de visualização
Para mais informações sobre argumentos de `docker compose`, veja https://docs.docker.com/reference/cli/docker/compose/.

Quando o docker compose estiver ativo, você pode usar **http://localhost:9000** como endereço do Build server nas preferências do editor ou como valor de `--build-server` se usar Bob para compilar o projeto.

Vários profiles podem ser passados na linha de comando. Por exemplo:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
O exemplo acima executa as instâncias frontend, Android, Web e Windows.

Para interromper os serviços, pressione Ctrl+C se o docker compose estiver rodando em modo não detached, ou
```sh
docker compose -p extender down
```
se o docker compose foi executado em modo detached (por exemplo, se a flag '-d' foi passada ao comando `docker compose up`).

Se quiser baixar as versões mais recentes dos JARs, você pode usar o seguinte comando para determinar a versão mais recente:
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

### E macOS e iOS?

Os builds macOS e iOS são feitos em hardware Apple real usando um servidor de build executado em modo stand-alone, sem Docker. Em vez disso, Xcode, Java e outras ferramentas necessárias são instaladas diretamente na máquina, e o servidor de build roda como um processo Java normal. Você pode aprender como configurar isso na [documentação do servidor de build no GitHub](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos).


## Como executar o Extender local com artefatos compilados localmente

Siga as [instruções no repositório Extender no GitHub](https://github.com/defold/extender) para compilar e executar manualmente um servidor de build local.
