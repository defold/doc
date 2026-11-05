---
title: Defold'da profil çıkarma
brief: Bu kılavuz, Defold'da bulunan profil çıkarma olanaklarını açıklar.
---

# Profil çıkarma {#profiling}

Defold, motorla ve proje derleme hattıyla bütünleşik profil çıkarma (profiling) araçları içerir. Bunlar performans, bellek ve kaynak (resource) kullanımı sorunlarını bulmaya yardımcı olur. Çalışma zamanına ait profil çıkarma verileri çeşitli araçlar tarafından kullanılabilir:

* Temel profil çıkarıcı (profiler) ve oyun içi görsel profil çıkarıcı tüm platformlarda kullanılabilir.
* [Remotery profil çıkarıcı](https://github.com/Celtoys/Remotery) ve etkileşimli web tabanlı kare (frame) profil çıkarıcısı masaüstü ve mobil platformlarda kullanılabilir.
* Metal kullanan macOS hata ayıklama derlemeleri, Xcode'da incelemek üzere [GPU izlerini](#metal-gpu-trace-capture) kaydedebilir.
* HTML5 derlemeleri, Defold kapsamlarını (scope) tarayıcının Web Performance API'sine yayımlayabilir.

[App Manifest](/manuals/app-manifest/#profiler) içindeki **Profiler** ayarı, profil çıkarıcı kodunun bir derlemeye bağlanıp bağlanmayacağını denetler. Varsayılan değer **Debug Only** seçeneğidir; **None** kodu dışarıda bırakır, **Always** ise hem hata ayıklama derlemelerine hem de yayıma yönelik derlemelere dahil eder. *game.project* dosyasındaki `profiler` ayarları çalışma zamanı davranışını denetler ancak dışarıda bırakılmış profil çıkarıcı kodunu yeniden derlemeye bağlamaz. Özellikle **Track CPU**, CPU kullanımı örneklemesini denetler; App Manifest seçiminden ayrıdır.

## Çalışma zamanı görsel profil çıkarıcısı {#the-runtime-visual-profiler}

Profil çıkarıcı desteği içeren derlemelerde, canlı bilgileri çalışan uygulamanın üzerinde gösteren bir çalışma zamanı görsel profil çıkarıcısı bulunur:

```lua
function on_reload(self)
    -- Toggle the visual profiler on hot reload.
    profiler.enable_ui(true)
end
```

![Görsel profil çıkarıcı](images/profiling/visual_profiler.png)

Görsel profil çıkarıcı, verilerini sunma biçimini değiştirmek için kullanılabilecek çeşitli işlevler sağlar:

```lua

profiler.set_ui_mode()
profiler.set_ui_view_mode()
profiler.view_recorded_frame()
```

Profil çıkarıcı işlevleri hakkında daha fazla bilgi için [profil çıkarıcı API başvuru belgelerine](/ref/profiler/) bakın.

## Web profil çıkarıcısı {#the-web-profiler}
Profil çıkarıcı desteği içeren bir masaüstü veya mobil derlemeyi çalıştırırken, etkileşimli kare ve kaynak profil çıkarıcılarına bir tarayıcı üzerinden erişebilirsiniz.

### Remotery kare profil çıkarıcısı {#remotery-frame-profiler}
Kare profil çıkarıcısı, oyununuz çalışırken örnekler almanızı ve tek tek kareleri ayrıntılı olarak analiz etmenizi sağlar. Profil çıkarıcıya erişmek için:

1. Oyununuzu hedef cihazda başlatın.
2. <kbd> Debug ▸ Open Web Profiler</kbd> menüsünü seçin.

Kare profil çıkarıcısı, çalışan oyunu farklı açılardan gösteren çeşitli bölümlere ayrılmıştır. Profil çıkarıcının görünümleri güncellemesini geçici olarak durdurmak için sağ üst köşedeki Pause düğmesine basın.

![Web profil çıkarıcısı](images/profiling/webprofiler_page.png)

::: sidenote
Birden fazla hedefi aynı anda kullandığınızda, sayfanın üst kısmındaki Connection Address alanını, hedef başlatıldığında konsolda gösterilen Remotery profil çıkarıcı URL adresiyle eşleşecek şekilde değiştirerek hedefler arasında elle geçiş yapabilirsiniz:

```
INFO:ENGINE: Defold Engine 1.3.4 (80b1b73)
INFO:DLIB: Initialized Remotery (ws://127.0.0.1:17815/rmt)
INFO:ENGINE: Loading data from: build/default
```
:::

Sample Timeline
: Sample Timeline, motorda yakalanan kare verilerini her iş parçacığı (thread) için bir yatay zaman çizelgesinde gösterir. Main, tüm oyun mantığının ve motor kodunun büyük bölümünün çalıştığı ana iş parçacığıdır. Remotery, profil çıkarıcının kendisi içindir; Sound ise ses karıştırma ve çalma iş parçacığıdır. Yakınlaştırıp uzaklaştırabilir (fare tekerleğini kullanarak) ve bir karenin ayrıntılarını Frame Data görünümünde görmek için tek tek kareleri seçebilirsiniz.

  ![Sample Timeline](images/profiling/webprofiler_sample_timeline.png)


Frame Data
: Frame Data görünümü, seçili kareye ait tüm verilerin ayrıntılı olarak dökümünü içeren bir tablodur. Motorun her kapsamında kaç milisaniye harcandığını görebilirsiniz.

  ![Kare verileri](images/profiling/webprofiler_frame_data.png)


Global Properties
: Global Properties görünümü bir sayaç tablosu gösterir. Bu sayaçlar, örneğin çizim çağrılarının sayısını veya belirli bir türdeki bileşenlerin (component) sayısını izlemeyi kolaylaştırır.

  ![Global Properties](images/profiling/webprofiler_global_properties.png)

::: sidenote
LuaMem değeri, Lua çöp toplayıcısının bildirdiği üzere Lua VM tarafından kullanılan belleğin kilobayt cinsinden miktarıdır. Memory, motorun kullandığı belleğin kilobayt cinsinden miktarıdır.
:::

::: important
[Max Sample Count ayarı](/manuals/project-settings/#max-sample-count), her karede iş parçacığı başına kaydedilen profil çıkarıcı örneklerinin sayısını sınırlar. Profil çıkarıcı sınırın aşıldığını bildirirse önce yerel kod eklentilerindeki (native extension) profil çıkarma kodunda eşleşmeyen bir kapsam başlangıç/bitiş çifti olup olmadığını kontrol edin. Üst sınırı yalnızca geçerli bir kare, yapılandırılmış sınırdan daha fazla kapsam içeriyorsa yükseltin.
:::

### Kaynak profil çıkarıcısı {#resource-profiler}
Kaynak profil çıkarıcısı, oyununuzu çalışırken incelemenizi ve kaynak kullanımını ayrıntılı olarak analiz etmenizi sağlar. Profil çıkarıcıya erişmek için:

1. Oyununuzun hata ayıklama derlemesini hedef cihazınızda başlatın.
2. Bir tarayıcıda [motor hizmeti adresini](/manuals/engine-service/#availability-and-port-discovery) açın: `http://<address>:<port>/`. Çalışan motorun konsolda bildirdiği adresi ve bağlantı noktasını kullanın.

Kaynak profil çıkarıcısı 2 bölüme ayrılmıştır: biri oyununuzda o anda örnekleri oluşturulmuş koleksiyonların (collection), oyun nesnelerinin (game object) ve bileşenlerin hiyerarşik görünümünü, diğeri ise o anda yüklü olan tüm kaynakları gösterir.

![Kaynak profil çıkarıcısı](images/profiling/webprofiler_resources_page.png)

Koleksiyon görünümü
: Koleksiyon görünümü, oyunda o anda örnekleri oluşturulmuş tüm oyun nesnelerinin ve bileşenlerin hiyerarşik listesini ve hangi koleksiyondan geldiklerini gösterir. Belirli bir anda oyununuzda nelerin örneklerini oluşturduğunuzu ve nesnelerin nereden geldiğini ayrıntılı olarak inceleyip anlamanız gerektiğinde bu araç çok yararlıdır.

Kaynaklar görünümü
: Kaynaklar görünümü, o anda belleğe yüklenmiş tüm kaynakları, bunların boyutlarını ve her kaynağa yapılan başvuru sayısını gösterir. Bu, uygulamanızdaki bellek kullanımını optimize ederken belirli bir anda belleğe nelerin yüklendiğini anlamanız gerektiğinde yararlıdır.

#### Kaynak yükleme süreleri {#resource-loading-times}

Tek tek kaynakların ne kadar sürede yüklendiğini de inceleyebilirsiniz. Oyunu başlatmadan önce *game.project* dosyasında [Resource → Profile](/manuals/project-settings/#profile) ayarını etkinleştirin. Metin görünümünde bu ayar şöyledir:

```ini
[resource]
profile = 1
```

Ayar varsayılan olarak devre dışıdır. Başlangıç yüklemelerini ölçmek için etkinleştirdikten sonra oyunu yeniden başlatın. Tamamlanan veya başarısız olan her yükleme; kaynak yolu, toplam süre ve ön yükleme, okuma, oluşturma, oluşturma sonrası, kuyruk ve bekleme aşamalarının sürelerini içeren INFO düzeyinde bir günlük kaydı yazar. Önbellek isabetleri yeni yükleme kayıtları üretmez.

Kaynak profil çıkarıcısında süre sütunlarını göstermek için önce **Capture**, ardından **Show load times** düğmesine tıklayın. **Capture**, saklanan ölçümlerin görünümünü yeniler; profil çıkarmayı etkinleştirmez veya önceki yüklemeleri geriye dönük ölçmez.

| Sütun | Anlam |
| --- | --- |
| **Load (ms)** | Bağımlılıklar, oluşturma sonrası işler, kuyrukta bekleme ve diğer beklemeler dahil ilk yüklemede geçen toplam süre. |
| **Preload (ms)** | Kaynağın ön yükleme geri çağırımında hazırlanması için harcanan süre. |
| **Read (ms)** | Kaynak verilerini okumak için harcanan süre. |
| **Create (ms)** | Kaynağın oluşturma geri çağırımında çalışma zamanı kaynağını oluşturmak için harcanan süre. |

Yükleme sürelerini göstermek, tabloyu en yavaş kaynaklar ilk sırada olacak şekilde toplam yükleme süresine göre sıralar. Bir aşamaya göre sıralamak için ilgili süre sütununun başlığına tıklayın; sırayı tersine çevirmek için yeniden tıklayın. **Load** sütunundaki çubuklar, her toplamı görünen en yavaş kaynağa göre gösterir. Sütunları yeniden gizlemek için **Hide load times** düğmesine tıklayın.

Yükleme ve geri çağırım süreleri, iç içe bağımlılık işlerini içerir. Aynı iş birden çok kaynağın ölçümünde görünebileceği için başlangıç süresini hesaplamak üzere kaynakların toplamlarını toplamayın. **Preload**, **Read** ve **Create** sütunları da toplam yükleme süresinin tamamını kapsamaz; günlük ek aşamaları sağlar.

Uzun çizgi (`—`), örneğin profil çıkarma devre dışı olduğu veya ilk yükleme bitmediği için tamamlanmış ölçüm bulunmadığını belirtir. Ölçülen sıfır değeri `0.000` olarak gösterilir. Ölçümler ilk yüklemeyi açıklar: önbellek isabetleri ve çalışma sırasında yeniden yükleme bunları değiştirmez; kaynağı bellekten kaldırmak saklanan ölçümünü de kaldırır.

## Metal GPU izi yakalama {#metal-gpu-trace-capture}

[Motorun HTTP hizmeti](/manuals/engine-service/#metal-gpu-trace-endpoint), macOS'ta Metal GPU komutlarını bir *.gputrace* belgesine yakalayabilir. Yakalanan kareleri incelemek için tamamlanmış izi Xcode'da açın. Bu özellik hata ayıklama motorunda yerleşiktir.

### Başlatma ve desteği kontrol etme {#launch-and-check-support}

Yerel Metal grafik arka ucu dahil edilmiş bir macOS [Debug paketi](/manuals/bundling/#release-vs-debug) oluşturun. App Manifest kullanıyorsanız Metal içeren bir **Graphics (macOS)** seçeneği seçin; [grafik arka uçları](/manuals/app-manifest/#graphics) bölümüne bakın.

Paketin yürütülebilir dosyasını bir terminalden `METAL_CAPTURE_ENABLED=1` ile başlatın ve Metal bağdaştırıcısını seçin. Bu örnekte paket yolunu ve yürütülebilir dosya adını değiştirin:

```sh
METAL_CAPTURE_ENABLED=1 \
    "/absolute/path/MyGame.app/Contents/MacOS/MyGame" --graphics-adapter=metal
```

Ortam değişkeni motor başlarken ayarlanmış olmalıdır. Bunu yalnızca HTTP istekleri için kullanılan terminalde ayarlamak, zaten çalışan motorda yakalamayı etkinleştirmez.

İkinci bir terminalde [günlükte yazdırılan motor hizmeti bağlantı noktasını](/manuals/engine-service/#availability-and-port-discovery) kullanın. Aşağıdaki örnekler `curl` ve `jq` kullanır:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq '.paths["/profiler/gputrace"]'
curl -sS -i "$ENGINE_URL/profiler/gputrace"
```

Rota yalnızca macOS'ta kaydedilir. OpenAPI belgesindeki `null` girdisi, motorun bu rotayı sunmadığını gösterir. Rota mevcut olsa bile yakalama desteği grafik bağdaştırıcısına ve başlatma ortamına bağlıdır. Metal yakalama kullanılamıyorsa `GET /profiler/gputrace`, `error.code: "gputrace_unsupported"` ile HTTP 501 döndürür. Devam etmeden önce motorun Metal kullandığını ve `METAL_CAPTURE_ENABLED=1` ile başlatıldığını kontrol edin. Desteklenen istek, yakalama durumuyla HTTP 200 döndürür.

### Kareleri yakalama ve inceleme {#capture-and-inspect-frames}

Üst dizini mevcut olan ve yolunda henüz bir iz bulunmayan, `.gputrace` ile biten yazılabilir mutlak bir çıktı yolu seçin. Yol, motoru çalıştıran bilgisayardadır. Yerel bir motor için bu örnek yeni bir geçici dizin oluşturur ve bir kare ister:

```sh
GPU_TRACE_DIR=$(mktemp -d /tmp/defold-gputrace.XXXXXX)
GPU_TRACE_PATH="$GPU_TRACE_DIR/frame.gputrace"
GPU_TRACE_REQUEST=$(jq -n --arg path "$GPU_TRACE_PATH" '{path: $path, frames: 1}')
curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    --data "$GPU_TRACE_REQUEST" \
    "$ENGINE_URL/profiler/gputrace" | jq
```

`frames` isteğe bağlıdır, varsayılanı `1` değeridir ve `1` ile `10000` arasındaki tamsayıları kabul eder. Yakalama, bir sonraki işlenen kareden önce başlar ve istenen sayıda tam kare gönderildikten sonra durur. Beklerken oyunun kare işlemeye devam etmesini sağlayın. Yalnızca bir yakalama beklemede veya etkin olabilir; başka bir başlatma isteği `error.code: "gputrace_active"` ile HTTP 409 döndürür.

Yakalama zamanlandığında `POST`, `ok: true` ve `data.state: "pending"` ile HTTP 200 döndürür. Yakalamanın tamamlanması sonraki durum istekleriyle bildirilir. `data.state` değeri `complete`, `canceled` veya `failed` olana kadar durum isteğini yineleyin:

```sh
curl -fsS "$ENGINE_URL/profiler/gputrace" | jq
```

| `data.state` | Anlam |
| --- | --- |
| `idle` | Hiçbir yakalama zamanlanmamıştır. |
| `pending` | Yakalama, işlemenin başlamasını bekliyor. |
| `capturing` | Yakalama etkindir; `data.frames_captured` tamamlanan kareleri bildirir. |
| `complete` | Yakalama bitmiştir ve iz açılabilir. |
| `canceled` | Bekleyen yakalama, başlamadan iptal edilmiştir. |
| `failed` | Yakalama başlatılamamıştır; yerel hata için `data.error` alanını inceleyin. |

`GET`, geçerli veya en son yakalamayı açıklar. `data.path` değerinin istediğiniz yolla eşleştiğini kontrol edin. Başarısız yakalama yine `ok: true` ile HTTP 200 döndürür; sonucu belirlemek için `data.state` ve `data.error` alanlarını inceleyin. Otomatik istemcide gecikme ve zaman aşımı kullanarak sorgulayın.

Durum `complete` olduktan sonra izi motorun çalıştığı Mac'te Xcode ile açın:

```sh
open -a Xcode "$GPU_TRACE_PATH"
```

HTTP uç noktası durum döndürür; iz, motorun çalıştığı makinedeki `data.path` yoluna kaydedilir. Uzak motor için tamamlanmış belgeyi yerel olarak açmadan önce o makineden alın.

### Yakalamayı iptal etme veya durdurma {#cancel-or-stop-a-capture}

Bekleyen yakalamayı iptal etmek veya etkin yakalamayı erken bitirmek için:

```sh
curl -fsS -X DELETE "$ENGINE_URL/profiler/gputrace" | jq
```

Bekleyen yakalama `canceled` durumuna geçer. Etkin yakalamada `data.stop_requested` değeri `true` olur ve yakalama, işlenen geçerli kare gönderildikten sonra biter. Son duruma ulaşana kadar `GET` ile sorgulamaya devam edin. `DELETE`, diske zaten yazılmış izleri bırakır. Bekleyen veya etkin yakalama yoksa `error.code: "gputrace_inactive"` ile HTTP 409 döndürür.


## HTML5 tarayıcı performans zaman çizelgesi {#html5-browser-performance-timeline}

HTML5, tarayıcı zaman çizelgesi için Remotery yerine Web Performance API'sini kullanır. Defold kapsamlarını kaydetmek için:

1. Seçili App Manifest profil çıkarıcı modunun, çalıştırdığınız derleme çeşidine profil çıkarıcı desteğini dahil ettiğinden emin olun.
2. *game.project* dosyasında **Performance Timeline Enabled** (`profiler.performance_timeline_enabled`) ayarını etkinleştirin.
3. HTML5 derlemesini başlatın ve tarayıcının geliştirici araçlarını açın.
4. Tarayıcının **Performance** panelinde bir oturum kaydedin ve oluşan zaman çizelgesindeki Defold kapsamlarını inceleyin.

Bu tarayıcı zaman çizelgesi, hem oyun içi görsel profil çıkarıcıdan hem de etkileşimli Remotery web profil çıkarıcısından ayrıdır.


## Derleme raporları {#build-reports}
Oyununuzu paketlerken bir derleme raporu oluşturma seçeneği vardır. Bu, oyun dağıtım paketinizin parçası olan tüm varlıkların (asset) boyutunu anlamak için çok yararlıdır. Oyunu paketlerken *Generate build report* onay kutusunu işaretlemeniz yeterlidir.

![Derleme raporu](images/profiling/build_report.png)

Derleme aracı, oyun dağıtım paketinin yanında `report.html` adlı bir dosya oluşturur. Raporu incelemek için dosyayı bir web tarayıcısında açın:

![Derleme raporu](images/profiling/build_report_html.png)

*Overview*, proje boyutunun kaynak türüne göre genel görsel dökümünü sunar.

*Resources*, boyuta, sıkıştırma oranına, şifrelemeye, türe ve dizin adına göre sıralayabileceğiniz ayrıntılı bir kaynak listesi gösterir. Gösterilen kaynak girdilerini filtrelemek için "search" alanını kullanın.

*Structure* bölümü, kaynakların proje dosya yapısında nasıl düzenlendiğine göre boyutları gösterir. Girdiler, dosyanın ve dizin içeriğinin göreli boyutuna göre yeşilden (hafif) maviye (ağır) doğru renklerle kodlanır.


## Harici araçlar {#external-tools}
Yerleşik araçlara ek olarak, ücretsiz ve yüksek kaliteli çok çeşitli izleme ve profil çıkarma araçları mevcuttur. Bunlardan bazıları şunlardır:

ProFi (Lua)
: Yerleşik bir Lua profil çıkarıcısı sunmuyoruz, ancak kullanımı yeterince kolay harici kütüphaneler vardır. Betiklerinizin nerede zaman harcadığını bulmak için kodunuza kendiniz süre ölçümleri ekleyin veya [ProFi](https://github.com/jgrahamc/ProFi) gibi bir Lua profil çıkarma kütüphanesi kullanın.

  Yalnızca Lua ile yazılmış profil çıkarıcıların, kurdukları her kancayla (hook) oldukça fazla ek yük oluşturduğunu unutmayın. Bu nedenle böyle bir araçtan aldığınız zamanlama profillerine biraz temkinli yaklaşmanız önerilir. Bununla birlikte, sayım profilleri yeterince doğrudur.

Instruments (macOS ve iOS)
: Xcode'un parçası olan bir performans analiz ve görselleştirme aracıdır. Bir veya daha fazla uygulamanın ya da sürecin davranışını izlemenizi ve incelemenizi, cihaza özgü özellikleri (Wi-Fi ve Bluetooth gibi) incelemenizi ve çok daha fazlasını yapmanızı sağlar.

  ![Instruments](images/profiling/instruments.png)

OpenGL profiler (macOS)
: Apple'dan indirebileceğiniz "Additional Tools for Xcode" paketinin bir parçasıdır (Xcode menüsünde <kbd>Xcode ▸ Open Developer Tool ▸ More Developer Tools...</kbd> seçeneğini seçin).

  Bu araç, çalışan bir Defold uygulamasını incelemenizi ve OpenGL'i nasıl kullandığını görmenizi sağlar. OpenGL işlev çağrılarını izlemenizi, OpenGL işlevlerine kesme noktaları koymanızı, uygulama kaynaklarını (dokular, programlar, gölgelendiriciler vb.) incelemenizi, arabellek içeriklerine bakmanızı ve OpenGL durumunun diğer yönlerini kontrol etmenizi sağlar.

  ![OpenGL profil çıkarıcısı](images/profiling/opengl.png)

Android Profiler (Android)
: https://developer.android.com/studio/profile/android-profiler.html

  Oyununuzun CPU, bellek ve ağ etkinliğine ait gerçek zamanlı verileri yakalayan bir profil çıkarma araçları kümesidir. Kod yürütülürken örneklemeye dayalı yöntem izleme gerçekleştirebilir, öbek dökümleri alabilir, bellek ayırma işlemlerini görüntüleyebilir ve ağ üzerinden iletilen dosyaların ayrıntılarını inceleyebilirsiniz. Aracı kullanmak için `AndroidManifest.xml` dosyasında `android:debuggable="true"` ayarını yapmanız gerekir.

  ![Android Profiler](images/profiling/android_profiler.png)

  Not: Android Studio 4.1'den itibaren [Android Studio'yu başlatmadan profil çıkarma araçlarını çalıştırmak](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers) da mümkündür.

Graphics API Debugger (Android)
: https://github.com/google/gapid

  Bir uygulamadan grafik sürücüsüne yapılan çağrıları incelemenizi, değiştirmenizi ve yeniden yürütmenizi sağlayan bir araç kümesidir. Aracı kullanmak için `AndroidManifest.xml` dosyasında `android:debuggable="true"` ayarını yapmanız gerekir.

  ![Graphics API Debugger](images/profiling/gapid.png)
