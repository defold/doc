---
title: Düzenleyiciye genel bakış
brief: Bu kılavuz, Defold düzenleyicisinin görünümüne, işleyişine ve içinde nasıl gezinileceğine genel bir bakış sunar.
---

# Düzenleyiciye genel bakış

Düzenleyici, oyun projenizdeki tüm dosya ve klasörlere göz atmanızı ve bunlar üzerinde verimli bir şekilde işlem yapmanızı sağlar. Bir dosyayı düzenlemeye başladığınızda uygun düzenleyici açılır ve dosyayla ilgili tüm bilgiler ayrı görünümlerde gösterilir.

## Düzenleyiciyi başlatma

Defold düzenleyicisini çalıştırdığınızda proje seçme ve oluşturma ekranı açılır. Yapmak istediğiniz işlemi tıklayarak seçin:

MY PROJECTS
: Yakın zamanda açtığınız projeler, onlara hızlıca erişebilmeniz için burada bulunur. Bu, başlangıç ekranının varsayılan görünümüdür.

  Daha önce hiç proje açmadıysanız (veya tümünü kaldırdıysanız) iki düğme gösterilir. Sistem dosya tarayıcısıyla bir proje bulup açmak için `Open From Disk…` düğmesine tıklayabilir veya `Create New Project` düğmesine tıklayarak `TEMPLATES` sekmesine geçebilirsiniz.

  ![Projelerim](images/editor/start_no_projects.png)


  Daha önce proje açtıysanız aşağıdaki resimdeki gibi projelerinizin listesi gösterilir:

  ![Projelerim](images/editor/start_my_projects.png)

TEMPLATES
: Belirli platformlar için veya belirli eklentileri kullanarak yeni bir Defold projesine hızlıca başlamanız amacıyla hazırlanmış boş ya da neredeyse boş temel projeleri içerir.


TUTORIALS
: Bir öğreticiyi izlemek istiyorsanız öğrenebileceğiniz, oynayabileceğiniz ve değiştirebileceğiniz, adım adım yönlendiren öğreticiler içeren projeler sunar.


SAMPLES
: Belirli kullanım senaryolarını göstermek için hazırlanmış projeler içerir.

  ![Yeni proje](images/editor/start_templates.png)

Yeni bir proje oluşturduğunuzda proje yerel sürücünüzde saklanır ve yaptığınız tüm değişiklikler yerel olarak kaydedilir.

Farklı seçenekler hakkında daha fazla bilgiyi [Proje kurulumu kılavuzunda](https://www.defold.com/manuals/project-setup/) bulabilirsiniz.

## Düzenleyici dili

Başlangıç ekranının sol alt köşesinde dil seçimini görebilirsiniz. Mevcut yerelleştirmelerden birini seçin. Bu ayara düzenleyicide `File ▸ Preferences ▸ General ▸ Editor Language` yolundan da erişebilirsiniz.

![Diller](images/editor/languages.png)

## Düzenleyici bölmeleri {#the-editor-views}

Defold düzenleyicisi, belirli bilgileri gösteren bölmelerden veya görünümlerden oluşur.

![Düzenleyici 2](images/editor/editor_overview.png)

### 1. Assets bölmesi
Projenizdeki tüm dosya ve klasörleri, diskinizdeki yapıyla aynı olan bir ağaç yapısında listeler. Listede gezinmek için tıklayın ve kaydırın. Dosyalarla ilgili tüm işlemleri bu görünümde yapabilirsiniz:

   - Herhangi bir dosya veya klasörü seçmek için <kbd>sol tıklayın</kbd>; <kbd>⇧ Shift</kbd> tuşunu basılı tutarak seçimi genişletebilir veya <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> tuşunu basılı tutarak tıkladığınız öğeyi seçebilir ya da seçimden çıkarabilirsiniz.
   - Bir dosyayı, dosya türüne özgü düzenleyicide açmak için dosyaya <kbd>çift tıklayın</kbd>.
   - Diskinizdeki başka konumlardan projeye dosya eklemek veya dosya ve klasörleri proje içinde yeni konumlara taşımak için <kbd>sürükleyip bırakın</kbd>.
   - Yeni dosya veya klasör oluşturabileceğiniz, yeniden adlandırma, silme, dosya bağımlılıklarını izleme ve başka işlemler yapabileceğiniz _bağlam menüsünü_ açmak için <kbd>sağ tıklayın</kbd>.

*Assets* bölmesinden silinen dosya ve klasörler, platform destekliyorsa sistemin Trash veya Recycle Bin klasörüne taşınır. Bir öğeyi çöp kutusuna taşıma desteklenmiyorsa veya başarısız olursa düzenleyici öğeyi kalıcı olarak siler.

### 2. Scene Editor bölmesi {#the-scene-editor}

Bir koleksiyon (collection), oyun nesnesi (game object) veya görsel bileşen (component) dosyasına çift tıkladığınızda, sahne oluşturmak ve düzenlemek için kullanılan görsel düzenleyici olan *Scene Editor* açılır. Betik dosyaları ve görsel olmayan diğer kaynaklar (resource) ise kendilerine özgü düzenleyicilerde açılır.

![Scene Editor görünümü](images/editor/2d_scene.png)

Scene Editor tarafından sunulan temel özelliklerden bazıları:

- Ortografik ve perspektif kamera modlarıyla [2B ve 3B sahnelerde gezinme](/manuals/scene-editing/#2d-and-3d-scene-orientation)
- Nesneleri taşımak, döndürmek ve ölçeklemek için [dönüşüm araçları](/manuals/scene-editing/#manipulating-objects)
- Birinci şahıs bakış açısıyla 3B gezinme için [serbest kamera modu](/manuals/scene-editing/#free-camera-mode)
- Boyutu, düzlemi ve görünümü yapılandırılabilen [ızgara ayarları](/manuals/scene-editing/#grid-settings)
- Bileşen türlerinin ve kılavuzların görünürlüğünü değiştirmek için [görünürlük filtreleri](/manuals/scene-editing/#visibility-filters)

Daha fazla bilgiyi [Sahne düzenleyicisi kılavuzunda](/manuals/scene-editing/) bulabilirsiniz.

### 3. Outline bölmesi

Bu görünüm, düzenlemekte olduğunuz dosyanın içeriğini hiyerarşik bir ağaç yapısında gösterir. Outline, düzenleyici görünümünü yansıtır ve öğeleriniz üzerinde işlem yapmanızı sağlar:

   - Bir öğeyi seçmek için <kbd>sol tıklayın</kbd>; <kbd>⇧ Shift</kbd> tuşunu basılı tutarak seçimi genişletebilir veya <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> tuşunu basılı tutarak tıkladığınız öğeyi seçebilir ya da seçimden çıkarabilirsiniz.
   - Öğeleri taşımak için <kbd>sürükleyip bırakın</kbd>. Üst-alt nesne ilişkisi oluşturmak için bir koleksiyondaki oyun nesnesini başka bir oyun nesnesinin üzerine bırakın.
   - Öğe ekleyebileceğiniz, seçili öğeleri silebileceğiniz ve benzeri işlemler yapabileceğiniz _bağlam menüsünü_ açmak için <kbd>sağ tıklayın</kbd>.

Listedeki bir öğenin sağında bulunan küçük `👁` göz simgesine tıklayarak oyun nesnelerinin ve görsel bileşenlerin görünürlüğünü değiştirebilirsiniz.

![Outline bölmesi](images/editor/outline.png)

### 4. Properties bölmesi

Bu görünüm, seçili öğeyle ilişkili Id, URL, Position, Rotation, Scale gibi özellikleri ve/veya bileşene özgü diğer özellikleri, ayrıca betiklerin özel özelliklerini gösterir.

Sayısal bir özelliğin değerini, `↕` yukarı-aşağı okunu <kbd>sürükleyerek</kbd> ve fareyi hareket ettirerek de değiştirebilirsiniz.

![Properties bölmesi](images/editor/properties.png)

### 5. Tools bölmesi

Bu görünümde birkaç sekme bulunur.

*Console* sekmesi: oyununuz çalışırken motorun ürettiği hata, uyarı ve bilgi çıktılarını veya sizin özellikle yazdırdığınız çıktıları gösterir,

*Build Errors*: proje derleme sürecindeki hataları gösterir,

*Search Results*: `Keep Results` düğmesine tıklarsanız projenin tamamında yaptığınız aramanın (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>) sonuçlarını gösterir

*Curve Editor*: [Parçacık düzenleyicisinde](/manuals/particlefx/) eğrileri düzenlerken kullanılır.

Tools bölmesi, tümleşik hata ayıklayıcıyla etkileşim kurmak için de kullanılır. Daha fazla bilgiyi [Hata ayıklama kılavuzunda](/manuals/debugging/) bulabilirsiniz.

### 6. Changed Files bölmesi

Projenizde Git kullanılıyorsa bu görünüm, geçerli Git kaydına (commit) (`HEAD`) kıyasla yerel olarak değiştirilen, eklenen, yeniden adlandırılan veya silinen dosyaları listeler. Uzak bir depoyla eşitlemek için harici bir Git istemcisi veya komut satırını kullanın. Daha fazla bilgiyi [Sürüm kontrolü kılavuzunda](/manuals/version-control/) bulabilirsiniz. Dosyalarla ilgili bazı işlemleri bu görünümde yapabilirsiniz:

   - Bir dosyayı seçmek için <kbd>sol tıklayın</kbd>; <kbd>⇧ Shift</kbd> tuşunu basılı tutarak seçimi genişletebilir veya <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> tuşunu basılı tutarak tıkladığınız öğeyi seçebilir ya da seçimden çıkarabilirsiniz. Değiştirilmiş tek bir dosya seçiliyse farkları göstermek için `Diff` düğmesine tıklayabilirsiniz. Seçili tüm dosyalardaki değişiklikleri geri almak için `Revert` düğmesine tıklayabilirsiniz.
   - Bir dosyanın görünümünü açmak için dosyaya <kbd>sol tuşla çift tıklayın</kbd>. Düzenleyici, Assets görünümünde olduğu gibi dosyayı uygun düzenleyicide açar.
   - Fark görünümünü açabileceğiniz, dosyada yapılan tüm değişiklikleri geri alabileceğiniz, dosyayı dosya sisteminde bulabileceğiniz ve başka işlemler yapabileceğiniz açılır menüyü açmak için dosyaya <kbd>sağ tıklayın</kbd>.

### Menü çubuğu

Düzenleyici görünümünün üst kısmında veya Mac'te sistem çubuğunda, 6 menü içeren menü çubuğunu bulabilirsiniz: `File`, `Edit`, `View`, `Project`, `Debug`, `Help`. Bu menülerin işlevleri kılavuzlarda açıklanacaktır.

### Durum çubuğu

Düzenleyicinin alt çubuğunda, durumun gösterildiği dar bir alan bulunur. Örneğin:
- Yeni bir güncelleme mevcut olduğunda tıklanabilir `Update Available` düğmesi görünür. Bu kılavuzun aşağıdaki Düzenleyiciyi güncelleme bölümüne bakın.
- Proje derlenirken veya paketlenirken ilerleme burada gösterilir.

## Bölme boyutu ve görünürlüğü

Düzenleyicide bölmelerin boyutunu, yukarıda açıklanan 6 bölme arasındaki sınırları <kbd>sürükleyerek</kbd> ayarlayabilirsiniz.

Düzenleyicide bölmelerin görünürlüğünü `View` menüsündeki seçenekleri veya belirtilen kısayolları kullanarak değiştirebilirsiniz:
- `Toggle Assets Pane` (<kbd>F6</kbd>), Assets ve Changed Files bölmelerinin görünürlüğünü değiştirir
- `Toggle Changed Files`, yalnızca Changed Files bölmesinin görünürlüğünü değiştirir
- `Toggle Tools Pane` (<kbd>F7</kbd>), Tools bölmesinin görünürlüğünü değiştirir
- `Toggle Properties Pane` (<kbd>F8</kbd>), Outline ve Properties bölmelerinin görünürlüğünü değiştirir

![Bölme görünürlüğü](images/editor/editor_panes.png)

`View` menüsünden Grid, Guides veya Camera gibi görünürlükle ilgili diğer ayarları da açıp kapatabilir ya da değiştirebilir, görünümü seçime sığdırabilir (`Frame Selection` veya <kbd>F</kbd> tuşu) ve varsayılan 2B ve 3B görünümler arasında geçiş yapabilirsiniz (`Realign Camera` veya <kbd>.</kbd> tuşu). Bunların çoğuna araç çubuğundan veya kısayollarla da erişilebilir.

## Sekmeler

Birden fazla dosya açıksa düzenleyici görünümünün üst kısmında her dosya için ayrı bir sekme gösterilir. Aynı bölmedeki sekmelerin yerini değiştirebilirsiniz; sekme çubuğundaki konumlarını değiştirmek için <kbd>sürükleyip bırakın</kbd>. Ayrıca şunları yapabilirsiniz:

- Bir _bağlam menüsü_ açmak için sekmeye <kbd>sağ tıklayın</kbd>,
- Tek bir sekmeyi kapatmak için `Close` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>W</kbd>) seçeneğine tıklayın,
- Seçili sekme dışındaki tüm sekmeleri kapatmak için `Close Others` seçeneğine tıklayın,
- Etkin bölmedeki tüm sekmeleri kapatmak için `Close All` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd>+<kbd>W</kbd>) seçeneğine tıklayın,
- Varsayılan düzenleyici dışında bir düzenleyici veya `File ▸ Preferences ▸ Code ▸ Custom Editor` altında ayarlanmış ilişkili harici aracı kullanmak için `➝| Open As` seçeneğini seçin. Daha fazla bilgiyi [Tercihler kılavuzunda](/manuals/editor-preferences) bulabilirsiniz.

![Sekmeler](images/editor/tabs_custom.png)

## Yan yana düzenleme

2 düzenleyici görünümünü yan yana açabilirsiniz.

- Taşımak istediğiniz düzenleyicinin sekmesine <kbd>sağ tıklayın</kbd> ve `Move to Other Tab Pane` seçeneğini seçin.

![2 bölme](images/editor/2-panes.png)

Sekme menüsündeki `Swap with Other Tab Pane` seçeneğiyle bir sekmeyi bölmeler arasında taşıyabilir veya `Join Tab Panes` seçeneğiyle bölmeleri tek bir bölmede birleştirebilirsiniz.

## Yeni proje dosyaları oluşturma {#creating-new-project-files}

Yeni kaynak dosyaları oluşturmak için `File ▸ New…` seçeneğini seçip menüden dosya türünü belirleyin veya bağlam menüsünü kullanın:

`Assets` tarayıcısında hedef konuma <kbd>sağ tıklayın</kbd>, ardından `New… ▸ [file type]` seçeneğini seçin:

![Dosya oluşturma](images/editor/create_file.png)

Yeni dosya için *Name* alanına uygun bir ad yazın ve gerekirse *Location* alanındaki konumu değiştirin. Dosya türü uzantısı dahil tam dosya adı, iletişim kutusundaki *Preview* alanında gösterilir:

![Oluşturulacak dosyanın adı](images/editor/create_file_name.png)

## Şablonlar

Her proje için özel şablonlar belirleyebilirsiniz. Bunun için projenin kök dizininde `templates` adlı yeni bir klasör oluşturun ve `/templates/default.gui` veya `/templates/default.script` gibi istediğiniz uzantılara sahip, `default.*` biçiminde adlandırılmış yeni dosyalar ekleyin. Ayrıca bu dosyalarda `{{NAME}}` belirteci kullanılırsa yerine dosya oluşturma penceresinde belirtilen dosya adı konur.

Belirli bir dosya türü için şablon varsa bu türde yeni bir dosya oluşturulduğunda dosyanın başlangıç içeriği `templates` klasöründeki dosyadan alınır.


![Şablonlar](images/editor/templates.png)

## Dosyaları projenize içe aktarma

Projenize varlık (asset) dosyaları (görüntüler, sesler, modeller vb.) eklemek için dosyaları *Assets* tarayıcısında uygun konuma sürükleyip bırakmanız yeterlidir. Böylece proje dosya yapısında seçilen konumda dosyaların _kopyaları_ oluşturulur. Daha fazla bilgiyi [varlıkları içe aktarma kılavuzumuzda](/manuals/importing-assets/) bulabilirsiniz.

![Dosyaları içe aktarma](images/editor/import.png)

## Düzenleyiciyi güncelleme

Düzenleyici, internete bağlıyken güncellemeleri otomatik olarak denetler. Bir güncelleme algılandığında proje seçme ekranının sol alt köşesinde veya düzenleyici penceresinin sağ alt köşesinde, tıklanabilir mavi `Update Available` bağlantısı gösterilir.

![Proje seçim ekranından güncelleme](images/editor/update_start.png)
![Düzenleyiciden güncelleme](images/editor/update_available.png)

İndirmek ve güncellemek için tıklanabilir `Update Available` bağlantısına basın. Bilgi içeren bir onay penceresi açılır; devam etmek için `Download Update` düğmesine tıklayın.

![Düzenleyiciyi güncelleme penceresi](images/editor/update.png)

İndirme ilerlemesini alttaki durum çubuğunda görebilirsiniz:

![İndirme ilerlemesi](images/editor/download_status.png)

Güncelleme indirildikten sonra mavi bağlantı `Restart to Update` olarak değişir. Yeniden başlatmak ve güncellenmiş düzenleyiciyi açmak için bu bağlantıya tıklayın.

![Güncellemek için yeniden başlatma](images/editor/restart_to_update.png)

## Tercihler

Düzenleyicinin ayarlarını `Preferences` penceresinde değiştirebilirsiniz. Bu pencereyi açmak için `File ▸ Preferences…` seçeneğine tıklayın veya <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>,</kbd> kısayolunu kullanın

Daha fazla ayrıntıyı [Tercihler kılavuzunda](/manuals/editor-preferences) bulabilirsiniz

![Preferences penceresi](images/editor/preferences.png)

## Düzenleyici günlükleri {#editor-logs}
Düzenleyicide bir sorunla karşılaşıp bunu bildirmeniz gerektiğinde (`Help  ▸ Report Issue`), düzenleyicinin günlük dosyalarını da sağlamanız iyi olur. Günlüklerin konumunu sisteminizin dosya tarayıcısında açmak için `Help ▸ Show Logs` seçeneğine tıklayın.

Daha fazla bilgiyi [Yardım alma kılavuzunda](/manuals/getting-help/#getting-help) bulabilirsiniz.

![Show Logs seçeneği](images/editor/show_logs.png)

Düzenleyici günlük dosyalarını şu konumlarda bulabilirsiniz:

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` veya `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` veya `~/.local/state/Defold`

Düzenleyici bir terminalden/komut isteminden başlatıldıysa çalışırken de düzenleyici günlüklerine erişebilirsiniz. Düzenleyiciyi başlatmak için şu komutu kullanın:

```shell
# Linux:
$ ./path/to/Defold/Defold

# macOS:
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## Düzenleyici sunucusu

Düzenleyici bir proje açtığında rastgele bir bağlantı noktasında web sunucusu başlatır. Bu sunucu, diğer uygulamalardan düzenleyiciyle etkileşim kurmak için kullanılabilir. Bağlantı noktası `.internal/editor.port` dosyasına yazılır.

Sunucu, `http://localhost:$(cat .internal/editor.port)/openapi.json` adresinde bir OpenAPI belirtimi sunar. Bu, ajanların yürüttüğü iş akışları için yararlı ve temel bir başlangıç noktasıdır.

Ayrıca düzenleyicinin yürütülebilir dosyası, başlatma sırasında bağlantı noktası belirtmenizi sağlayan `--port` (veya `-p`) komut satırı seçeneğine sahiptir. Örneğin::
```shell
# Windows
.\path\to\Defold\Defold.exe --port 8181

# Linux:
./path/to/Defold/Defold --port 8181

# macOS:
./path/to/Defold/Defold.app/Contents/MacOS/Defold --port 8181
```

## Düzenleyici kurulum üst verileri {#editor-installation-metadata}

Düzenleyici başlatıldığında, başlatıcı ve kurulum yolları hakkındaki bilgileri bilinen bir konuma yazar. Üçüncü taraf IDE tümleştirmeleri ve diğer araçlar bu bilgileri kurulu Defold düzenleyicilerini bulmak için kullanabilir:

| İşletim sistemi | Konum |
|---------|----------|
| macOS   | `~/Library/Application Support/Defold/installations.json` |
| Linux   | `${XDG_STATE_HOME:-~/.local/state}/Defold/installations.json` |
| Windows | `%LOCALAPPDATA%\Defold\installations.json` |

Dosya, bilinen her kurulum için bir nesne içeren bir JSON dizisi içerir:

```json
[
  {
    "launcherPath": "/Applications/Defold.app/Contents/MacOS/Defold",
    "installPath": "/Applications/Defold.app",
    "lastLaunchedAt": "2026-07-06T12:34:56.789Z"
  }
]
```

## Düzenleyici biçimlendirmesi

Düzenleyicinin görünümü özel biçimlendirmeyle değiştirilebilir. Daha fazla bilgiyi [Düzenleyici biçimlendirme kılavuzunda](/manuals/editor-styling) bulabilirsiniz.

## Sık sorulan sorular
:[Editor FAQ](../shared/editor-faq.md)
