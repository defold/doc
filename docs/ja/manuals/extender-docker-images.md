---
title: 利用可能な Docker イメージ
brief: 利用可能な Docker イメージと、それらを使用していた Defold のバージョンを説明します。
---

# 利用可能な Docker イメージ {#available-docker-images}
以下は、公開レジストリで利用可能なすべての Docker イメージの一覧です。これらのイメージを使うと、サポートが終了した古い SDK を含む環境で Extender を実行できます。

|SDK               |イメージタグ                                                                                                |プラットフォーム名（Extender の設定内） |このイメージを使用していた Defold のバージョン |
|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------|
|Linux 最新版      |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`                       |Defold のすべてのバージョン            |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`                      |1.4.3 以降                    |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                         |1.7.0 まで                    |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                         |[1.8.0-1.9.3]                  |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                         |1.9.4 以降                    |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                        |1.6.1 まで                    |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                        |1.6.2 以降                    |

# 古い Docker イメージの使用方法 {#how-to-use-old-docker-images}
古い環境を使用するには、次の手順に従います。
1. Extender のリポジトリにある `docker-compose.yml`（[リンク](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml)）を変更します。必要な Docker イメージを使用するサービスの定義をもう1つ追加する必要があります。たとえば、Emscripten 2.0.11 を含む Docker イメージを使用する場合は、次のサービス定義を追加する必要があります。
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
    重要なフィールドは次のとおりです。
    * **profiles** - サービスの起動を引き起こすプロファイルの一覧です。プロファイル名は、`docker compose` コマンドの `--profile <profile_name>` 引数で渡します。
    * **networks** - Docker コンテナーが使用するネットワークの一覧です。Extender の実行には、`default` という名前のネットワークを使用します。サービスのネットワークエイリアスを設定することが重要です（後で Extender を設定するときに使用します）。
2. [`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml) の `extender.remote-builder.platforms` セクションに、リモートビルダー（remote builder）の定義を追加します。この例では、次のようになります。
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    URL は `http://<service_network_alias>:9000` の形式にする必要があります。`service_network_alias` は手順1のネットワークエイリアスです。9000 は Extender の標準ポートです（Extender の設定をカスタマイズしている場合は、異なることがあります）。
3. [設定済みのアーティファクトを使ってローカルの Extender を実行する方法](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts)の説明に従って、ローカルの Extender を実行します。
