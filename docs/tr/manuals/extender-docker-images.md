---
title: Kullanılabilir Docker imajları
brief: Bu belge, kullanılabilir Docker imajlarını ve bu imajları kullanan Defold sürümlerini açıklar.
---

# Kullanılabilir Docker imajları
Aşağıda, herkese açık kayıt deposunda (registry) bulunan tüm Docker imajlarının (Docker images) listesi yer alır. Bu imajlar, artık desteklenmeyen eski yazılım geliştirme kitlerinin (SDK) bulunduğu bir ortamda Extender'ı çalıştırmak için kullanılabilir.

|SDK               |İmaj etiketi                                                                                             |Platform adı (Extender yapılandırmasında) |İmajı kullanan Defold sürümü |
|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------|
|Linux son sürüm   |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-linux-env:latest`         |`linux-latest`                       |Tüm Defold sürümleri           |
|Android NDK25     |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-android-ndk25-env:latest` |`android-ndk25`                      |1.4.3'ten itibaren             |
|Emscripten 2.0.11 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-2011-env:latest`    |`emsdk-2011`                         |1.7.0'a kadar                  |
|Emscripten 3.1.55 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3155-env:latest`    |`emsdk-3155`                         |[1.8.0-1.9.3]                  |
|Emscripten 3.1.65 |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-emsdk-3165-env:latest`    |`emsdk-3165`                         |1.9.4'ten itibaren             |
|Winsdk 2019       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2019-env:latest`   |`winsdk-2019`                        |1.6.1'e kadar                  |
|Winsdk 2022       |`europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-winsdk-2022-env:latest`   |`winsdk-2022`                        |1.6.2'den itibaren             |

# Eski Docker imajlarını kullanma
Eski ortamı kullanmak için aşağıdaki adımları izleyin:
1. Extender deposundaki `docker-compose.yml` dosyasını değiştirin: [bağlantı](https://github.com/defold/extender/blob/dev/server/docker/docker-compose.yml). Gerekli Docker imajını içeren bir hizmet tanımı daha eklemeniz gerekir. Örneğin, Emscripten 2.0.11 içeren Docker imajını kullanmak istiyorsak aşağıdaki hizmet tanımını eklememiz gerekir:
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
    Önemli alanlar şunlardır:
    * **profiles** - hizmetin başlatılmasını tetikleyen profillerin listesi. Profil adları, `--profile <profile_name>` bağımsız değişkeni aracılığıyla `docker compose` komutuna iletilir.
    * **networks** - Docker konteynerinin kullanması gereken ağların listesi. Extender'ı çalıştırmak için `default` adlı ağ kullanılır. Hizmetin ağ takma adlarını ayarlamak önemlidir (bunlar daha sonra Extender yapılandırmasında kullanılacaktır).
2. [`application-local-dev-app.yml`](https://github.com/defold/extender/blob/dev/server/configs/application-local-dev-app.yml) dosyasının `extender.remote-builder.platforms` bölümüne uzak derleme sunucusu (remote builder) tanımını ekleyin. Örneğimizde tanım şöyle görünür:
    ```yml
        emsdk-2011:
            url: http://emsdk-2011:9000
            instanceId: emsdk-2011
    ```
    URL şu biçimde olmalıdır: `http://<service_network_alias>:9000`; burada `service_network_alias`, 1. adımdaki ağ takma adıdır. 9000, Extender'ın standart bağlantı noktasıdır (özel bir Extender yapılandırması kullanıyorsanız farklı olabilir).
3. Yerel Extender'ı [Önceden yapılandırılmış çıktı dosyalarıyla yerel Extender'ı çalıştırma](/manuals/extender-local-setup#how-to-run-local-extender-with-preconfigured-artifacts) bölümünde açıklandığı gibi çalıştırın.