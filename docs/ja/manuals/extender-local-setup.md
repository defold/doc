---
title: ローカルビルドサーバーのセットアップ
brief: ローカルビルドサーバーのセットアップと実行方法を説明するマニュアルです
---

# ビルドサーバーのローカルセットアップ {#build-server-local-setup}

ローカルのビルドサーバー（build server、別名「Extender」）を実行する方法には、次の2つがあります：
1. 設定済みの成果物を使用してローカルビルドサーバーを実行します。
2. ローカルでビルドした成果物を使用してローカルビルドサーバーを実行します。

## 設定済みの成果物を使用してローカルで Extender を実行する方法 {#how-to-run-local-extender-with-preconfigured-artifacts}

ローカルでクラウドビルダーを実行するには、あらかじめ次のソフトウェアをインストールする必要があります：

* [Docker](https://www.docker.com/) - Docker は、OS レベルの仮想化を使用して、コンテナーと呼ばれるパッケージでソフトウェアを提供する PaaS 製品群です。ローカルの開発マシンでクラウドビルダーを実行するには、[Docker Desktop](https://www.docker.com/products/docker-desktop/) をインストールする必要があります。
* Google Cloud CLI - Google Cloud CLI は、Google Cloud リソースを作成および管理するためのツール群です。これらのツールは、[Google から直接インストールする](https://cloud.google.com/sdk/docs/install)か、Brew、Chocolatey、Snap などのパッケージマネージャーからインストールできます。
* プラットフォームごとのビルドサーバーを含むコンテナーをダウンロードするには、Google アカウントも必要です。

上記のソフトウェアをインストールしたら、次の手順に従って Defold のクラウドビルダーをインストールして実行します：

**Windows ユーザーへの注意**：以下のコマンドの実行には git bash ターミナルを使用してください。

1. __Google Cloud へのアクセスを認可し、アプリケーションのデフォルト認証情報を作成します__ - Docker コンテナーイメージのダウンロードには Google アカウントが必要です。これにより、Defold 側で公開コンテナーレジストリの利用を監視して公平な利用を確保し、イメージを過剰にダウンロードするアカウントを一時的に停止できます。

   ```sh
   gcloud auth login
   ```
2. __Artifact Registry を使用するように Docker を設定します__ - `europe-west1-docker.pkg.dev` の公開コンテナーレジストリからコンテナーイメージをダウンロードする際に、認証情報ヘルパーとして `gcloud` を使用するように Docker を設定する必要があります。

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Docker と Google Cloud が正しく設定されていることを確認します__ - すべてのビルドサーバーのコンテナーイメージが使用するベースイメージをプルして、Docker と Google Cloud が正しく設定されていることを確認します。以下のコマンドを実行する前に、Docker Desktop が実行中であることを確認してください：
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Extender リポジトリをクローンします__ - Docker と Google Cloud が正しく設定されれば、サーバーを起動する準備はほぼ完了です。サーバーを起動する前に、ビルドサーバーを含む Git リポジトリをクローンする必要があります：
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __ビルド済みの jar をダウンロードします__ - 次に、ビルド済みのサーバー（`extender.jar`）とマニフェストマージツール（`manifestmergetool.jar`）をダウンロードします：
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
6. __サーバーを起動します__ - 次の docker compose のメインコマンドを実行して、サーバーを起動できます：
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
*profile* には、次の値を指定できます：
* **all** - すべてのプラットフォーム用のリモートインスタンスを実行します。
* **android** - Android 版をビルドするためのフロントエンドインスタンス + リモートインスタンスを実行します。
* **web** - Web 版をビルドするためのフロントエンドインスタンス + リモートインスタンスを実行します。
* **linux** - Linux 版をビルドするためのフロントエンドインスタンス + リモートインスタンスを実行します。
* **windows** - Windows 版をビルドするためのフロントエンドインスタンス + リモートインスタンスを実行します。
* **consoles** - Nintendo Switch/PS4/PS5 版をビルドするためのフロントエンドインスタンス + リモートインスタンスを実行します。
* **nintendo** - Nintendo Switch 版をビルドするためのフロントエンドインスタンス + リモートインスタンスを実行します。
* **playstation** - PS4/PS5 版をビルドするためのフロントエンドインスタンス + リモートインスタンスを実行します。
* **metrics** - メトリクスのバックエンドと可視化ツールとして VictoriaMetrics + Grafana を実行します。
`docker compose` の引数について詳しくは、https://docs.docker.com/reference/cli/docker/compose/ を参照してください。

docker compose が起動したら、エディターの環境設定の `Build server address` に **http://localhost:9000** を指定できます。Bob を使用してプロジェクトをビルドする場合は、`--build-server` の値に指定できます。

コマンドラインには複数のプロファイルを渡せます。たとえば：
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
上記の例では、フロントエンド、Android、Web、Windows のインスタンスを実行します。

サービスを停止するには、docker compose が非デタッチモードで実行されている場合は Ctrl+C を押します。デタッチモードで実行されている場合は、次のコマンドを実行します： 
```sh
docker compose -p extender down
```
デタッチモードでの実行とは、たとえば `docker compose up` コマンドに '-d' フラグを渡した場合です。

最新バージョンの jar をプルしたい場合は、次のコマンドを使用して最新バージョンを確認できます。
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

### macOS と iOS の場合は？ {#what-about-macos-and-ios}

macOS と iOS のビルドは、実際の Apple ハードウェア上で、Docker を使わずにスタンドアロンモードで動作するビルドサーバーを使用して行います。この場合、XCode、Java、その他の必要なツールをマシンに直接インストールし、ビルドサーバーを通常の Java プロセスとして実行します。セットアップ方法については、[GitHub のビルドサーバードキュメント](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos)を参照してください。


## ローカルでビルドした成果物を使用してローカルで Extender を実行する方法 {#how-to-run-local-extender-with-locally-built-artifacts}

ローカルビルドサーバーを手動でビルドして実行するには、[GitHub の Extender リポジトリにある手順](https://github.com/defold/extender)に従ってください。
