---
title: HTML5 platformu için Defold ile geliştirme
brief: Bu kılavuz, HTML5 oyunu oluşturma sürecini, bilinen sorunları ve kısıtlamaları açıklar.
---

# HTML5 için geliştirme

Defold, diğer platformlarda olduğu gibi HTML5 platformu için de standart paketleme (bundling) menüsü üzerinden oyun derlemeyi destekler. Ayrıca ortaya çıkan oyun, basit bir şablon sistemi aracılığıyla biçimlendirilebilen standart bir HTML sayfasına gömülür.

*game.project* dosyası HTML5'e özgü ayarları içerir:

![Proje ayarları](images/html5/html5_project_settings.png)

## Öbek boyutu {#heap-size}

Defold'un HTML5 desteği Emscripten ile sağlanır (bkz. http://en.wikipedia.org/wiki/Emscripten). Emscripten, uygulamanın çalıştığı öbek (heap) için yalıtılmış bir bellek alanı oluşturur. Motor varsayılan olarak oldukça büyük miktarda bellek (256 MB) ayırır. Bu miktarın tipik bir oyun için fazlasıyla yeterli olması beklenir. Optimizasyon sürecinizin bir parçası olarak daha küçük bir değer kullanmayı seçebilirsiniz. Bunu yapmak için şu adımları izleyin:

1. *heap_size* ayarını tercih ettiğiniz değere ayarlayın. Değer megabayt cinsinden belirtilmelidir.
2. HTML5 dağıtım paketinizi oluşturun (aşağıya bakın)

## HTML5 derlemesini test etme

HTML5 derlemesini test etmek için bir HTTP sunucusu gerekir. <kbd>Project ▸ Build HTML5</kbd> seçeneğini seçerseniz Defold sizin için bir sunucu oluşturur.

![HTML5 derleme](images/html5/html5_build_launch.png)

Dağıtım paketinizi test etmek için uzak HTTP sunucunuza yüklemeniz veya örneğin dağıtım paketi klasöründe Python kullanarak yerel bir sunucu oluşturmanız yeterlidir.
Python 2:

```sh
python -m SimpleHTTPServer
```

Python 3:

```sh
python -m http.server
```

veya

```sh
python3 -m http.server
```

::: important
HTML5 dağıtım paketini, `index.html` dosyasını tarayıcıda açarak test edemezsiniz. Bunun için bir HTTP sunucusu gerekir.
:::

::: important
Konsolda `"wasm streaming compile failed: TypeError: Failed to execute ‘compile’ on ‘WebAssembly’: Incorrect response MIME type. Expected ‘application/wasm’."` hatasını görürseniz sunucunuzun `.wasm` dosyaları için `application/wasm` MIME türünü kullandığından emin olmalısınız.
:::

## HTML5 dağıtım paketi oluşturma {#creating-html5-bundle}

Defold ile HTML5 içeriği oluşturmak basittir ve desteklenen diğer tüm platformlarla aynı yöntemi izler: menüden <kbd>Project ▸ Bundle... ▸ HTML5 Application...</kbd> seçeneğini seçin:

![HTML5 dağıtım paketi oluşturma](images/html5/html5_bundle.png)

HTML5 dağıtım paketleri iki WebAssembly mimarisini destekler:

* `wasm-web` - iş parçacıklarını (thread) kullanmayan standart WebAssembly motoru.
* `wasm_pthread-web` - iş parçacıklarını kullanabilen bir WebAssembly motoru.

Mimarilerden birini veya her ikisini de pakete ekleyebilirsiniz. Her ikisi de eklendiğinde yükleyici, tarayıcı ve barındırma ortamı destekliyorsa `wasm_pthread-web` mimarisini seçer; aksi durumda `wasm-web` mimarisine geçer. Standart hedef adları için [Bob kılavuzuna](/manuals/bob/#usage) bakın.

::: important
İş parçacıklarını kullanan motor, güvenli ve [kökenler arasında yalıtılmış (cross-origin-isolated)](https://developer.mozilla.org/en-US/docs/Web/API/Window/crossOriginIsolated) bir sayfada `SharedArrayBuffer` gerektirir. Dağıtım paketini HTTPS (veya localhost) üzerinden sunun ve sunucuyu uyumlu kökenler arası yalıtım üstbilgileriyle yapılandırın. Yaygın olarak kullanılan üstbilgiler şunlardır:

```txt
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Sayfanın farklı kökenlerden yüklediği kaynaklar da uyumlu CORS veya Cross-Origin-Resource-Policy üstbilgileri kullanmalıdır. Yalnızca `wasm_pthread-web` içeren bir dağıtım paketi, bu gereksinimler karşılanmadığında çalışamaz; oyun kökenler arası yalıtımı desteklemeyen bir sitede barındırılabilecekse yedek seçenek olarak `wasm-web` mimarisini de ekleyin.
:::

Defold HTML5 dağıtım paketleri, WebAssembly destekleyen modern bir tarayıcı gerektirir. Internet Explorer 11 desteklenmez.

<kbd>Create bundle</kbd> düğmesine tıkladığınızda uygulamanın oluşturulacağı klasörü seçmeniz istenir. Dışa aktarma işlemi tamamlandıktan sonra uygulamayı çalıştırmak için gereken tüm dosyaları bu klasörde bulabilirsiniz.

## WebGL bağlam sürümü

İstenen grafik bağlamını [`graphics.webgl_version_hint`](/manuals/project-settings/#webgl-version-hint) aracılığıyla seçin. Varsayılan değer WebGL 2'dir; her iki sürümü de destekleyen tarayıcılarda WebGL 1 bağlamını test etmek veya hedeflemek için WebGL 1'i isteyin.

## İndirme doğrulaması {#download-verification}

HTML5 yükleyicisi varsayılan olarak indirilen motor ve arşiv dosyalarının boyutlarını kontrol eder. Kontroller başarısız olursa yükleyici hata bildirmeden önce indirmeler yeniden denenir:

* Motorun JavaScript veya WebAssembly dosyasını indirirken oluşan ağ hataları, başarısız HTTP durumları ve boyut uyuşmazlıkları için `html5.retry_count` ayarındaki yeniden deneme sınırı kullanılır.
* Arşiv dosyası doğrulamasında boyut veya SHA-1 uyuşmazlıkları için ayrı bir yeniden deneme sınırı vardır. Her doğrulama yeniden denemesi, dosyanın parçalarını yeniden indirir ve her indirme için normal ağ yeniden denemeleri kullanılabilir.

`html5.retry_time` ayarı, her iki durumda da yeniden denemeler arasındaki gecikmeyi kontrol eder.

Sunucunuz, vekil sunucunuz veya CDN'niz sunulan dosyaları kasıtlı olarak yeniden yazıyor ve boyutlarını değiştiriyorsa *game.project* dosyasında boyut doğrulamasını devre dışı bırakın:

```ini
[html5]
verify_downloaded_file_size = 0
```

**Verify Downloaded File Size** seçeneğinin devre dışı bırakılması, dağıtım paketine dahil edilen tüm SHA-1 doğrulamalarını etkin bırakır. [HTML5 proje ayarlarına](/manuals/project-settings/#verify-downloaded-file-size) bakın.

## Bilinen sorunlar ve kısıtlamalar

* Çalışma sırasında yeniden yükleme (Hot Reload) - Çalışma sırasında yeniden yükleme HTML5 derlemelerinde çalışmaz. Defold uygulamalarının düzenleyiciden güncellemeleri alabilmek için kendi küçük web sunucularını çalıştırmaları gerekir; bu, bir HTML5 derlemesinde mümkün değildir.
* Chrome
  * Yavaş hata ayıklama derlemeleri - HTML5 hata ayıklama derlemelerinde hataları saptamak için tüm WebGL grafik çağrılarını doğrularız. Ne yazık ki Chrome'da test yaparken bu işlem çok yavaştır. *game.project* dosyasındaki *Engine Arguments* alanını `--verify-graphics-calls=false` olarak ayarlayarak bunu devre dışı bırakabilirsiniz.
* Oyun kumandası (gamepad) desteği - HTML5'te dikkate almanız gereken özel durumlar ve uygulamanız gerekebilecek adımlar için [oyun kumandası belgelerine bakın](/manuals/input-gamepads/#gamepads-in-html5).

## HTML5 dağıtım paketini özelleştirme

Oyununuzun HTML5 sürümünü oluştururken Defold varsayılan bir web sayfası sağlar. Bu sayfa, oyununuzun nasıl sunulacağını belirleyen stil ve betik kaynaklarına başvurur.

Uygulama her dışa aktarıldığında bu içerik yeniden oluşturulur. Bu öğelerden herhangi birini özelleştirmek istiyorsanız proje ayarlarınızda değişiklik yapmanız gerekir. Bunun için Defold düzenleyicisinde *game.project* dosyasını açın ve *html5* bölümüne kaydırın:

![HTML5 bölümü](images/html5/html5_section.png)

Her seçenek hakkında daha fazla bilgi [proje ayarları kılavuzunda](/manuals/project-settings/#html5) bulunur.

::: important
`builtins` klasöründeki varsayılan html/css şablonunun dosyalarını değiştiremezsiniz. Değişikliklerinizi uygulamak için gereken dosyayı `builtins` klasöründen kopyalayıp yapıştırın ve bu dosyayı *game.project* içinde ayarlayın.
:::

::: important
Tuvale (canvas) kenarlık veya iç boşluk uygulanmamalıdır. Uygularsanız fare girdisinin koordinatları yanlış olur.
:::

*game.project* dosyasında `Fullscreen` düğmesini ve `Made with Defold` bağlantısını kapatabilirsiniz.
Defold, `index.html` için koyu ve açık tema sağlar. Varsayılan olarak açık tema seçilidir ancak `Custom CSS` dosyasını değiştirerek temayı değiştirebilirsiniz. Ayrıca `Scale Mode` alanında seçebileceğiniz dört ön tanımlı ölçek modu vardır.

::: important
*game.project* dosyasında (`Display` bölümü) `High Dpi` seçeneğini açarsanız tüm ölçek modlarının hesaplamaları geçerli ekran DPI değerini de içerir
:::

### Downscale Fit ve Fit

`Fit` modunda tuvalin boyutu, oyun tuvalinin tamamını özgün oranlarıyla ekranda gösterecek şekilde değiştirilir. `Downscale Fit` modunun tek farkı, boyutu yalnızca web sayfasının iç boyutu oyunun özgün tuvalinden küçük olduğunda değiştirmesidir; web sayfası oyunun özgün tuvalinden büyük olduğunda tuvali büyütmez.

![HTML5 bölümü](images/html5/html5_fit.png)

### Stretch

`Stretch` modunda tuvalin boyutu, web sayfasının iç alanını tamamen dolduracak şekilde değiştirilir.

![HTML5 bölümü](images/html5/html5_stretch.png)

### No Scale
`No Scale` modunda tuvalin boyutu, *game.project* dosyasının `[display]` bölümünde önceden tanımladığınız boyutla tamamen aynıdır.

![HTML5 bölümü](images/html5/html5_no_scale.png)

## Şablon belirteçleri

`index.html` dosyasını oluşturmak için [Mustache şablon dilini](https://mustache.github.io/mustache.5.html) kullanırız. Projeyi derlerken veya paketlerken HTML ve CSS dosyaları, belirli belirteçleri (token) proje ayarlarınıza bağlı değerlerle değiştirebilen bir derleyiciden geçirilir. Bu belirteçler, karakter dizilerine kaçış uygulanıp uygulanmayacağına bağlı olarak her zaman çift veya üçlü süslü parantez içine alınır (`{{TOKEN}}` veya `{{{TOKEN}}}`). Proje ayarlarınızı sık sık değiştiriyorsanız veya içeriği başka projelerde yeniden kullanmayı planlıyorsanız bu özellik yararlı olabilir.

::: sidenote
Mustache şablon dili hakkında daha fazla bilgi [kılavuzda](https://mustache.github.io/mustache.5.html) bulunur.
:::

*game.project* dosyasındaki her değer bir belirteç olabilir. Örneğin, `Display` bölümündeki `Width` değerini kullanmak istiyorsanız:

![Display bölümü](images/html5/html5_display.png)

*game.project* dosyasını metin olarak açın ve `[section_name]` değerini ve kullanmak istediğiniz alanın adını kontrol edin. Ardından bunu bir belirteç olarak kullanabilirsiniz: `{{section_name.field}}` veya `{{{section_name.field}}}`.

![Display bölümü](images/html5/html5_game_project.png)

Örneğin, HTML şablonunda JavaScript içinde:

```javascript
function doSomething() {
    var x = {{display.width}};
    // ...
}
```

Ayrıca şu özel belirteçler de vardır:

DEFOLD_SPLASH_IMAGE
: Açılış görseli dosyasının adını veya *game.project* dosyasındaki `html5.splash_image` boşsa `false` yazar


```css
{{#DEFOLD_SPLASH_IMAGE}}
		background-image: url("{{DEFOLD_SPLASH_IMAGE}}");
{{/DEFOLD_SPLASH_IMAGE}}
```

exe-name
: Geçersiz simgeler çıkarılmış proje adı

DEFOLD_ARCHIVE_LOCATION_PREFIX
: `html5.archive_location_prefix` temel alınarak çözümlenen ve yükleyici tarafından kullanılan arşiv yolu öneki.

DEFOLD_ARCHIVE_LOCATION_SUFFIX
: `html5.archive_location_suffix` temel alınarak çözümlenen ve arşiv URL'lerine eklenen sonek.

DEFOLD_HAS_ARCHIVE_ORIGIN
: Arşiv öneki, `//cdn.example.com/archive` gibi protokole göreli bir URL dahil olmak üzere bir HTTP veya HTTPS kökeni belirtiyorsa `true` olur. Göreli arşiv önekleri için `false` olur. Defold 1.13.2'den itibaren kullanılabilir.

DEFOLD_ARCHIVE_ORIGIN
: Şema, ana makine ve isteğe bağlı bağlantı noktası dahil arşiv kökeni; köken belirtilmemişse boş bir dize. Protokole göreli bir önek, protokole göreli bir köken üretir. Ön bağlantı ipucu için kullanılır ve Defold 1.13.2'den itibaren kullanılabilir.

DEFOLD_HAS_WASM_ENGINE
: Dağıtım paketi, `wasm-web` veya `wasm_pthread-web` olmak üzere bir WebAssembly motoru içeriyorsa `true` olur.

DEFOLD_HAS_WASM_PTHREAD_ENGINE
: Dağıtım paketi `wasm_pthread-web` içeriyorsa `true` olur. Yükleyici mimariyi çalışma sırasında seçtiğinde yanlış motor çeşidinin önceden yüklenmesini önlemek için bunu kullanın.


DEFOLD_CUSTOM_CSS_INLINE
: *game.project* ayarlarınızda belirtilen CSS dosyasının içeriğinin satır içi olarak eklendiği yerdir.


```html
<style>
{{{DEFOLD_CUSTOM_CSS_INLINE}}}
</style>
```

::: important
Bu satır içi bloğun, ana uygulama betiği yüklenmeden önce yer alması önemlidir. HTML etiketleri içerdiği için bu makro, karakter dizilerine kaçış uygulanmasını önlemek üzere üçlü süslü parantez `{{{TOKEN}}}` içinde yer almalıdır.
:::

DEFOLD_SCALE_MODE_IS_DOWNSCALE_FIT
: `html5.scale_mode` değeri `Downscale Fit` ise bu belirteç `true` olur.

DEFOLD_SCALE_MODE_IS_FIT
: `html5.scale_mode` değeri `Fit` ise bu belirteç `true` olur.

DEFOLD_SCALE_MODE_IS_NO_SCALE
: `html5.scale_mode` değeri `No Scale` ise bu belirteç `true` olur.

DEFOLD_SCALE_MODE_IS_STRETCH
: `html5.scale_mode` değeri `Stretch` ise bu belirteç `true` olur.

DEFOLD_HEAP_SIZE
: *game.project* dosyasındaki `html5.heap_size` ayarında belirtilen öbek boyutunun bayta dönüştürülmüş değeri.

DEFOLD_ENGINE_ARGUMENTS
: *game.project* dosyasındaki `html5.engine_arguments` ayarında belirtilen, `,` simgesiyle ayrılmış motor bağımsız değişkenleri.

build-timestamp
: Geçerli derlemenin saniye cinsinden zaman damgası.


## Ek parametreler

Özel bir şablon oluşturursanız genel `CUSTOM_PARAMETERS` nesnesinde değer atamaları yaparak motor yükleyicisinin parametrelerini değiştirebilirsiniz. Yerleşik şablon, bu özelleştirmeler için bilerek boş bırakılmış bir `<script id="engine-setup">` bloğu sağlar.
::: important
`engine-setup` bloğunu, `dmloader.js` dosyasını yükleyen betikten sonra ve `EngineLoader.load()` işlevini çağıran `engine-start` bloğundan önce tutun.
:::
Örneğin:

```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.disable_context_menu = false;
        CUSTOM_PARAMETERS.unsupported_webgl_callback = function() {
            console.log("Oh-oh. WebGL not supported...");
        };
    </script>
```

`CUSTOM_PARAMETERS`, aşağıdakiler dahil çeşitli alanlar içerebilir:

```
'archive_location_filter':
    Filter function that will run for each archive path.

'unsupported_webgl_callback':
    Function that is called if WebGL is not supported.

'engine_arguments':
    List of arguments (strings) that will be passed to the engine.

'custom_heap_size':
    Number of bytes specifying the memory heap size.

'disable_context_menu':
    Disables the right-click context menu on the canvas element if true.

'retry_time':
    Pause in seconds before retry file loading after error.

'retry_count':
    How many attempts we do when trying to download a file.

'can_not_download_file_callback':
    Function that is called if you can't download file after 'retry_count' attempts.

'resize_window_callback':
    Function that is called when resize/orientationchanges/focus events happened

'start_success':
    Function that is called just before main is called upon successful load.

'update_progress':
    Function that is called as progress is updated. Parameter progress is updated 0-100.
```

## HTML5'te dosya işlemleri

HTML5 derlemeleri `sys.save()`, `sys.load()` ve `io.open()` gibi dosya işlemlerini destekler, ancak bu işlemlerin içeride nasıl ele alındığı diğer platformlardan farklıdır. JavaScript bir tarayıcıda çalıştırıldığında gerçek anlamda bir dosya sistemi kavramı yoktur ve güvenlik nedeniyle yerel dosya erişimi engellenir. Bunun yerine Emscripten (ve dolayısıyla Defold), tarayıcıda sanal bir dosya sistemi oluşturmak için verileri kalıcı olarak saklamakta kullanılan tarayıcı içi bir veritabanı olan [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB) kullanır. Diğer platformlardaki dosya sistemi erişiminden önemli farkı, bir dosyaya yazılması ile değişikliğin veritabanına gerçekten kaydedilmesi arasında küçük bir gecikme olabilmesidir. Tarayıcının geliştirici konsolu genellikle IndexedDB içeriğini incelemenize olanak tanır.


## HTML5 oyununa bağımsız değişken aktarma

Bazen bir oyuna başlatılmadan önce veya başlatılırken ek bağımsız değişkenler sağlamak gerekir. Bu, örneğin bir kullanıcı kimliği, oturum belirteci veya oyun başladığında hangi seviyenin yükleneceği olabilir. Bunu gerçekleştirmenin farklı yolları vardır; bunlardan bazıları burada açıklanmıştır.

### Motor bağımsız değişkenleri

Motor yapılandırılıp yüklenirken ek motor bağımsız değişkenleri belirtmek mümkündür. Bu ek motor bağımsız değişkenleri, çalışma sırasında `sys.get_config_string()` kullanılarak alınabilir. Bağımsız değişkenleri `index.html` dosyasının `engine-setup` bloğunda doğrudan `CUSTOM_PARAMETERS.engine_arguments` alanına atayın:


```html
    <script id="engine-setup" type="text/javascript">
        CUSTOM_PARAMETERS.engine_arguments = [
            "--config=example.foo1=bar1",
            "--config=example.foo2=bar2"
        ];
    </script>
```

Yeni bir dizi atamak, *game.project* dosyasında yapılandırılmış tüm motor bağımsız değişkenlerinin yerini alır. Bu bağımsız değişkenleri koruyup bir tane daha eklemek için bunun yerine `CUSTOM_PARAMETERS.engine_arguments.push("--config=example.foo3=bar3")` kullanın.

Ayrıca *game.project* dosyasının HTML5 bölümündeki *Engine Arguments* alanına `--config=example.foo1=bar1, --config=example.foo2=bar2` ekleyebilirsiniz. Virgülle ayrılmış değerler, oluşturulan `dmloader.js` dosyasındaki `CUSTOM_PARAMETERS.engine_arguments` alanına eklenir.

Çalışma sırasında değerleri şöyle alırsınız:

```lua
local foo1 = sys.get_config_string("example.foo1")
local foo2 = sys.get_config_string("example.foo2")
print(foo1) -- bar1
print(foo2) -- bar2
```


### URL'deki sorgu bağımsız değişkenleri

Bağımsız değişkenleri sayfa URL'sindeki sorgu parametrelerinin bir parçası olarak aktarabilir ve bunları çalışma sırasında okuyabilirsiniz:

```
https://www.mygame.com/index.html?foo1=bar1&foo2=bar2
```

```lua
local url = html5.run("window.location")
print(url)
```

Tüm sorgu parametrelerini bir Lua tablosu olarak alan eksiksiz bir yardımcı işlev:

```lua
local function get_query_parameters()
    local url = html5.run("window.location")
    -- get the query part of the url (the bit after ?)
    local query = url:match(".*?(.*)")
    if not query then
        return {}
    end

    local params = {}
    -- iterate over all key value pairs
    for kvp in query:gmatch("([^&]+)") do
        local key, value = kvp:match("(.+)=(.+)")
        params[key] = value
    end
    return params
end

function init(self)
    local params = get_query_parameters()
    print(params.foo1) -- bar1
end
```

## Optimizasyonlar
HTML5 oyunlarında, düşük donanımlı cihazlarda ve yavaş internet bağlantılarında oyunların hızlı yüklenmesini ve iyi çalışmasını sağlamak için ilk indirme boyutu, başlatma süresi ve bellek kullanımı konusunda genellikle sıkı gereksinimler vardır. Bir HTML5 oyununu optimize etmek için şu alanlara odaklanmanız önerilir:

* [Bellek kullanımı](/manuals/optimization-memory)
* [Motor boyutu](/manuals/optimization-size)
* [Oyun boyutu](/manuals/optimization-size)

## Sık sorulan sorular
:[HTML5 FAQ](../shared/html5-faq.md)
