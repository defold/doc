---
title: Yerel derleme sunucusu kurulumu
brief: Bu kılavuz, yerel bir derleme sunucusunun nasıl kurulup çalıştırılacağını açıklar.
---

# Derleme sunucusunun yerel kurulumu

Yerel derleme sunucusunu (build server, diğer adıyla 'Extender') çalıştırmanın iki yolu vardır:
1. Yerel derleme sunucusunu önceden yapılandırılmış çıktı dosyalarıyla (artifact) çalıştırmak.
2. Yerel derleme sunucusunu yerel olarak derlenmiş çıktı dosyalarıyla çalıştırmak.

## Yerel Extender'ı önceden yapılandırılmış çıktı dosyalarıyla çalıştırma {#how-to-run-local-extender-with-preconfigured-artifacts}

Bir bulut derleyicisini yerel olarak çalıştırabilmeniz için aşağıdaki yazılımları kurmanız gerekir:

* [Docker](https://www.docker.com/) - Docker, yazılımı konteyner (container) adı verilen paketler içinde sunmak için işletim sistemi düzeyinde sanallaştırma kullanan bir hizmet olarak platform ürünleri kümesidir. Bulut derleyicilerini yerel geliştirme makinenizde çalıştırmak için [Docker Desktop](https://www.docker.com/products/docker-desktop/) kurmanız gerekir.
* Google Cloud CLI - Google Cloud CLI, Google Cloud kaynaklarını oluşturmak ve yönetmek için kullanılan bir araç kümesidir. Araçlar [doğrudan Google'dan](https://cloud.google.com/sdk/docs/install) veya Brew, Chocolatey ya da Snap gibi bir paket yöneticisinden kurulabilir.
* Platforma özgü derleme sunucularını içeren konteynerleri indirmek için bir Google hesabına da ihtiyacınız vardır.

Yukarıda belirtilen yazılımları kurduktan sonra Defold bulut derleyicilerini kurmak ve çalıştırmak için şu adımları izleyin:

**Windows kullanıcıları için not**: aşağıdaki komutları çalıştırmak için git bash terminalini kullanın.

1. __Google Cloud'da yetkilendirme yapın ve uygulamanın varsayılan kimlik bilgilerini (Application default credentials) oluşturun__ - Herkese açık konteyner kayıt deposunun adil kullanımını izleyip sağlayabilmemiz ve aşırı sayıda imaj indiren hesapları geçici olarak askıya alabilmemiz için Docker konteyner imajlarını indirirken bir Google hesabınızın olması gerekir.

   ```sh
   gcloud auth login
   ```
2. __Docker'ı çıktı dosyası kayıt depolarını (Artifact registries) kullanacak şekilde yapılandırın__ - Docker'ın kimlik bilgisi yardımcısı olarak `gcloud` kullanacak şekilde yapılandırılması gerekir; bu yardımcı, `europe-west1-docker.pkg.dev` adresindeki herkese açık konteyner kayıt deposundan konteyner imajları indirilirken kullanılır.

   ```sh
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   ```
3. __Docker ve Google Cloud'un doğru yapılandırıldığını doğrulayın__ - Tüm derleme sunucusu konteyner imajlarının kullandığı temel imajı indirerek Docker ve Google Cloud'un başarıyla kurulduğunu doğrulayın. Aşağıdaki komutu çalıştırmadan önce Docker Desktop'ın çalıştığından emin olun:
   ```sh
   docker pull --platform linux/amd64 europe-west1-docker.pkg.dev/extender-426409/extender-public-registry/extender-base-env:latest
   ```
4. __Extender deposunu klonlayın__ - Docker ve Google Cloud doğru şekilde kurulduktan sonra sunucuları başlatmaya neredeyse hazırız. Sunucuyu başlatmadan önce derleme sunucusunu içeren Git deposunu klonlamamız gerekir:
   ```sh
   git clone https://github.com/defold/extender.git
   cd extender
   ```
5. __Önceden derlenmiş jar dosyalarını indirin__ - Sonraki adım, önceden derlenmiş sunucuyu (`extender.jar`) ve bildirim birleştirme aracını (`manifestmergetool.jar`) indirmektir:
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
6. __Sunucuyu başlatın__ - Artık ana docker compose komutunu çalıştırarak sunucuyu başlatabiliriz:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile <profile> up
```
Burada *profile* şu değerlerden biri olabilir:
* **all** - her platform için uzak örnekleri (instance) çalıştırır
* **android** - Android sürümünü derlemek için ön uç örneğini + uzak örnekleri çalıştırır
* **web** - Web sürümünü derlemek için ön uç örneğini + uzak örnekleri çalıştırır
* **linux** - Linux sürümünü derlemek için ön uç örneğini + uzak örnekleri çalıştırır
* **windows** - Windows sürümünü derlemek için ön uç örneğini + uzak örnekleri çalıştırır
* **consoles** - Nintendo Switch/PS4/PS5 sürümlerini derlemek için ön uç örneğini + uzak örnekleri çalıştırır
* **nintendo** - Nintendo Switch sürümünü derlemek için ön uç örneğini + uzak örnekleri çalıştırır
* **playstation** - PS4/PS5 sürümlerini derlemek için ön uç örneğini + uzak örnekleri çalıştırır
* **metrics** - ölçüm verileri için arka uç ve görselleştirme aracı olarak VictoriaMetrics + Grafana'yı çalıştırır
`docker compose` bağımsız değişkenleri hakkında daha fazla bilgi için https://docs.docker.com/reference/cli/docker/compose/ adresine bakın.

docker compose çalışmaya başladığında **http://localhost:9000** adresini düzenleyici tercihlerinde `Build server address` olarak veya projeyi derlemek için Bob kullanıyorsanız `--build-server` değeri olarak kullanabilirsiniz.

Komut satırına birden fazla profil verilebilir. Örneğin:
```sh
docker compose -p extender -f server/docker/docker-compose.yml --profile android --profile web --profile windows up
```
Yukarıdaki örnek ön uç, Android, Web ve Windows örneklerini çalıştırır.

Hizmetleri durdurmak için docker compose terminale bağlı modda çalışıyorsa Ctrl+C tuşlarına basın veya 
```sh
docker compose -p extender down
```
docker compose arka planda çalıştırıldıysa (örneğin `docker compose up` komutuna '-d' seçeneği verildiyse) yukarıdaki komutu çalıştırın.

jar dosyalarının en son sürümlerini indirmek istiyorsanız en son sürümü belirlemek için aşağıdaki komutu kullanabilirsiniz
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

### Peki ya macOS ve iOS?

macOS ve iOS derlemeleri, Docker olmadan bağımsız modda çalışan bir derleme sunucusu kullanılarak gerçek Apple donanımında yapılır. XCode, Java ve diğer gerekli araçlar doğrudan makineye kurulur ve derleme sunucusu normal bir Java süreci olarak çalışır. Bunun nasıl kurulacağını [GitHub'daki derleme sunucusu belgelerinden](https://github.com/defold/extender?tab=readme-ov-file#running-as-a-stand-alone-server-on-macos) öğrenebilirsiniz.


## Yerel Extender'ı yerel olarak derlenmiş çıktı dosyalarıyla çalıştırma

Yerel bir derleme sunucusunu elle derlemek ve çalıştırmak için [GitHub'daki Extender deposunda yer alan yönergeleri](https://github.com/defold/extender) izleyin.
