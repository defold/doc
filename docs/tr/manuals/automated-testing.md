---
title: Otomatik test ve doğrulama
brief: Bu kılavuz, belirlenimci Defold testlerinin yerel ortamda, çalışan bir oyunda, tarayıcılarda ve sürekli tümleştirme ortamında nasıl tasarlanacağını, çalıştırılacağını ve raporlanacağını açıklar.
---

# Otomatik test ve doğrulama

Otomatik test (automated testing), Defold kodunu ve içeriğini açık, makine tarafından okunabilir kanıtlarla doğrular. Yerel betiklerle, sürekli tümleştirme (Continuous Integration, CI) çalıştırıcılarıyla ve kodlama ajanlarıyla kullanılabilen testler tasarlamak için bu kılavuzu kullanın. Kılavuz; modül testlerini, çalışan koleksiyonları, tarayıcı testlerini, çalışma zamanı otomasyonunu, görsel kontrolleri, grafik arayüzü olmadan çalışan (headless) derlemeleri ele alır ve yararlı uygulama önerileri sunar.

## Doğrulama düzeyleri

İyi bir otomatik test yapısı, testleri üç ana katmana ayıran test piramidi yaklaşımını izler: birim testleri (unit test), tümleştirme testleri (integration test) ve uçtan uca testler (end-to-end, E2E). Defold'da testleri başlangıçta yüklenebilen belirli koleksiyonlara (collection) ayırabilirsiniz. Genellikle sorunu saptayabilecek en dar kapsamlı ve en hızlı kontrolle başlayıp gerektiğinde çalışma zamanı veya platform testleri eklemek iyi bir yaklaşımdır.

| Düzey | Uygun kanıt |
| --- | --- |
| Statik geçerleme | Ayrıştırıcı, biçimlendirici, kaynak geçerleyicisi veya oluşturulan dosyaların karşılaştırması |
| Modül testi | Motor bağımlılıkları en az düzeyde olan, yeniden kullanılabilir Lua mantığı için doğrulama koşullarının sonuçları |
| Çalışan koleksiyon | İletiler, bileşenler (component), girdi, fizik, yaşam döngüsü ve motor davranışı |
| Çalışma zamanı otomasyonu | Canlı sahne durumu, program yoluyla sağlanan girdi, uygulama durumu ve çalışma sırasında alınan ekran görüntüleri |
| HTML5 tarayıcı testi | Tuval girdisi, tarayıcı tümleştirmesi, görüntü alanının davranışı ve web çıktısı |
| Platform testi | Asıl hedef platformdaki davranış ve işleme (rendering, görüntü oluşturma) |
| Derleme ve paketleme | Bob çıkış durumu, derleme raporu, arşiv ve dağıtım paketi çıktı dosyaları |

Başarılı bir kod derleme işlemi, projenin derlenebildiğini kanıtlar; ancak oynanış davranışının doğru olduğunu kanıtlamaz. Bir ekran görüntüsü karmaşık geçişleri, animasyonları, etkileşimleri veya oynanış akışını kanıtlamaz; ancak modern çok modlu çözümler, bir karenin nasıl göründüğünü ve gölgelendiriciler ile görsel yerleşimin doğru olup olmadığını incelemek için ekran görüntüsünü kullanabilir. Bununla birlikte, otomatik testlerde koşulun doğrudan ifade edilebildiği her durumda belirlenimci (deterministic) doğrulama koşullarını tercih edin.

## Yeniden kullanılabilir ve test edilebilir Lua kodu

Yeniden kullanılabilir mantığı, motor bağımlılıkları en az düzeyde olan Lua modüllerinde tutun. Böylece yan etkisiz veri dönüşümleri, kurallar, durum makineleri ve hesaplamalar, eksiksiz bir oyun dünyası oluşturmadan sınanabilir.

Motorla etkileşen kodu, çağırdığı mantıktan ayırın. Bir betik, iletileri ve bileşen durumunu bir modüle yapılan çağrılara dönüştürebilir; testler ise modülü kontrollü girdilerle doğrudan çağırır.

Daha fazla ayrıntı için [Kod yazma kılavuzuna](/manuals/writing-code) bakın.

## Çalışan bir koleksiyonda testler {#tests-in-a-running-collection}

Davranış oyun nesnelerine (game object), bileşenlere, iletilere, girdiye, fiziğe veya diğer motor sistemlerine bağlıysa özel bir test koleksiyonu kullanın.

Her testin şu adımları izlemesi önerilir:

1. bilinen bir durum oluşturmak;
2. tek bir davranışı yürütmek;
3. beklenen sonucu doğrulamak ve değerlendirmek;
4. oluşturulan kaynakları temizlemek;
5. yapılandırılmış bir sonuç açıklaması üretmek.

Testler için yalıtılmış test koleksiyonlarını tercih edin. Bir proje, `game.project` dosyasındaki geçici bir proje ayarıyla test amaçlı bir başlangıç koleksiyonu (bootstrap collection) seçebilir:

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

Geçici test başlangıç koleksiyonunu projenin normal yapılandırmasında bırakmayın. CI ortamında, Bob'a iletilen özel bir ayar dosyasını tercih edin. CI deponun durumunu değiştiremez; yalnızca gerektiğinde geçici değişiklikler yapmalıdır.

Karmaşık oyunlar için önceden tanımlanmış senaryolar ve basit kaba bölüm taslakları içeren küçük "geliştirme odası" koleksiyonları oluşturabilirsiniz. Bunlar mekaniklerin yeniden üretilebilmesini sağlar ve oyunun ilgisiz durumlarında ve bölümlerinde gezinmeden test yapmayı mümkün kılarak geliştirmeyi kolaylaştırır.

### Test çatıları

Projeler küçük bir test çalıştırıcısı uygulayabilir veya [topluluk tarafından sunulan bir test kütüphanesi](https://defold.com/assets/?tag=testing) kullanabilir.

Örneğin [DefTest](https://defold.com/assets/deftest/), Telescope tabanlı bir birim testi kütüphanesidir. Test takımlarını, hazırlık ve test sonrası temizleme işlevlerini, doğrulama koşullarını, ada göre filtrelemeyi, seçili Defold API'leri için mock yapılarını ve isteğe bağlı LuaCov kod kapsamı ölçümünü destekler. Testler özel bir başlangıç koleksiyonundan çalıştırılabilir; buna Bob ile oluşturulmuş grafik arayüzü olmadan çalışan bir dağıtım paketinde çalıştırma da dahildir.

## Yapılandırılmış test sonuçları {#structured-test-results}

Bir test çatısının konsol/günlük özeti geliştiriciler için yararlı olabilir; ancak gözetimsiz çalışan bir otomatik denetleyicinin yine de açık bir tamamlanma sonucuna ihtiyacı vardır. Denetleyicinin test sonuçlarını kolayca işleyebilmesi için gerekirse çatının geri çağırımını veya özetini sarmalayan küçük bir bağdaştırıcı ekleyin.

Basit bir sonuç açıklaması, her fiziksel konsol satırında benzersiz bir önekin ardından tek bir JSON nesnesi kullanabilir:

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

Bir toplayıcının her satırı bağımsız olarak işlemesi, `TEST` önekini bulması, ardından gelen JSON verisini ayrıştırması ve ilgisiz motor çıktısını yok sayması önerilir.

Eski veya eşzamanlı bir sürecin çıktısının geçerli çalıştırmayı tamamlayamaması için benzersiz bir çalıştırma tanımlayıcısı ekleyin. Her test takımının, tek ve anlamı açık bir son olay üretmesi önerilir (`Pass`, `Failure`, `Crash`, `Timeout` vb.).

### Konsol çıktısını toplama

Bir oyun düzenleyiciden çalıştırıldığında hem mevcut konsol geçmişi hem de sürekli bir akış sunulur. Akışı, eşleşen bir test takımı tamamlanma olayından, sürecin sonlanmasından, bir hatadan veya yapılandırılan zaman aşımı ve satır sınırına ulaşılmasından sonra kapatın.

[Düzenleyici HTTP API'si kılavuzunda](/manuals/editor-http-api/#reading-console-output) daha fazla bilgi bulabilirsiniz.

### Kalıcı günlükler

Defold, `Write Log File` seçeneğini `game.project` dosyasında etkinleştirerek oyun günlüğünü kalıcı olarak da kaydedebilir. [Oyun ve sistem günlüklerine](/manuals/debugging-game-and-system-logs/) bakın. Günlüğün dosyaya kaydedilmesi, paketlenmiş uygulamalar için ve düzenleyici konsolunun kullanılamadığı hedef cihazları test ederken yararlıdır.

Proje, yerleşik `print()` ve `pprint()` işlevlerini veya örneğin Asset Portal'ımızdaki diğer [günlük kütüphanelerinden](https://defold.com/assets/?tag=logging) herhangi birini kullanabilir.

## Çalışan bir oyunu çalışma zamanı API'si üzerinden test etme

Bir çalışma zamanı otomasyonu API'si, çalışan bir hata ayıklama motorunu inceleyebilir ve kontrol edebilir. Testlerin çalışma zamanı nesnelerini bulması, program yoluyla girdi sağlaması, görünür bir durumu beklemesi veya işlenmiş görüntüyü alması gerektiğinde kullanılabilir.

Daha fazla ayrıntı için [motor hizmeti kılavuzunu](/manuals/engine-service/#automation-bridge-extension) okuyun.

Aşağıdaki örnek, [Automation Bridge](https://github.com/defold/extension-automation-bridge) Python yardımcı yapısını kullanır. Projenin hata ayıklama eklentisinin uyumlu bir sürümünü içermesi, belirtilen otomasyon tanımlayıcısına sahip bir öğeyi erişime açması ve `screen` uygulama durumunu yayımlaması gerekir:

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()

try:
    play = game.element(automation_id="play_button")
    game.click(play)
    game.wait_for_state("screen", "gameplay", timeout=5.0)
    screenshot = game.screenshot()
    print(screenshot.path)
finally:
    game.close_engine()
```

Uygulamanın tanımladığı durumlar ve otomasyon tanımlayıcıları, Automation Bridge'in isteğe bağlı, yalnızca hata ayıklamaya özel Lua API'sini kullanır; projenin bu API'yi etkinleştirmesi ve yayımlaması gerekir. Sabit süreli bir bekleme, makine hızından ve kare zamanlamasından etkilenir; tanımlanmış bir durumu sınırları belirlenmiş şekilde düzenli aralıklarla sorgulamak daha güvenilirdir.

Automation Bridge bir eklentidir; çekirdek motorun parçası değildir. Kurulu sürüme ait seçiciler, beklemeler, durum, olaylar, ekran görüntüleri ve tanılama hakkında bilgi için [Python API başvuru belgelerine](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) bakın.

## HTML5 için tarayıcı testleri {#browser-tests-for-html5}

Düzenleyici, [düzenleyici HTTP API'si kılavuzunda](/manuals/editor-http-api/#building-html5) açıklandığı gibi, mevcut `build-html5` komutuyla bir HTML5 derlemesi oluşturup sunabilir. Bob da düzenleyici olmadan bir HTML5 dağıtım paketi oluşturabilir.

Playwright, Puppeteer, Selenium, WebdriverIO veya Cypress gibi harici tarayıcı otomasyon araçları şunları yapabilir:

* Defold tuvalinin ve uygulamanın hazır olmasını beklemek;
* klavye, fare ve öykünülmüş dokunma girdisi göndermek;
* görüntü alanını yeniden boyutlandırmak;
* tarayıcı konsol çıktısını ve JavaScript hatalarını toplamak;
* ekran görüntüleri almak ve çıktı dosyalarını karşılaştırmak.

Tuvale yönlendirilen girdi, projenin normal girdi eşlemeleri (input binding) ve `on_input()` geri çağırımları aracılığıyla işlenir. Hem oyunun tepkisini hem de tarayıcıya özgü tümleştirme noktalarını test edin.

En güvenilir yaklaşım, özel `index.html` dosyasında açık bir JavaScript test köprüsü sunmaktır. Defold tarafında HTML5 derlemeleri, `html5.run()` kullanarak JavaScript yürütebilir; bu da tarayıcı tarafındaki böyle bir köprüyle iletişimi mümkün kılar. JavaScript'ten Defold'a geri gönderilen komutlar için JavaScript'ten motora iletişim sağlayan özel bir köprü kullanın.

Tarayıcı testlerinin sınırlarını belirleyin. Son raporda sayfanın yüklenememesini, tuvalin eksik olmasını, JavaScript hatasını, test zaman aşımını ve başarısız oyun doğrulama koşulunu birbirinden ayırın.

## Görsel inceleme için düzenleyici önizlemeleri ve çalışma sırasında alınan ekran görüntüleri {#editor-previews-and-runtime-screenshots}

Açık düzenleyicinin varsayılan sahne görünümünde kaynak dosyalarının veya çalışma sırasında oyunun ekran görüntüsünü alabilirsiniz.

| Yöntem | Amaç |
| --- | --- |
| [Düzenleyici önizlemesi](/manuals/editor-http-api/#rendering-scene-previews) | Yüklenmiş kaynakların yerleşimi (ör. bölüm veya GUI), atlas düzeni, karo haritası incelemesi, statik sahne düzeni, düzenleyicide işleme ve gölgelendiricilerin doğruluğu veya belgeler için küçük resimler oluşturma |
| [Çalışma sırasında alınan ekran görüntüsü](/manuals/engine-service) | Kontrollü bir senaryoda çalışan bir derlemenin işlenmiş durumu |

Görüntü karşılaştırmasını örneğin gerileme testleri için kullanabilirsiniz. Bir kontrol başarısız olduğunda fark görüntüsünü ve karşılaştırma ölçümlerini saklayın.

Çok modlu bir model; kırpılmış metin, üst üste binen denetimler, belirsiz seçim durumları veya güvenli alanın dışındaki içerik gibi başka türlü ifade edilmesi zor anlamsal koşulları görsel inceleme sırasında değerlendirebilir. Bu değerlendirmeyi, açık ölçütlere dayanan ek bir gösterge olarak ele almanız; belirlenimci mantık kontrollerinin veya görüntü karşılaştırmasının yerine kullanmamanız önerilir.

## Grafik arayüzü olmadan çalışan testler ve CI

Düzenleyiciden bağımsız CI için Bob derleme komut satırı aracını kullanın.

Bu araçla bağımlılıkları çözümleyebilir, bir oyun, arşiv veya bağımsız dağıtım paketi oluşturabilir ve bir JSON raporu üretebilirsiniz:

```sh
mkdir -p build/reports

java -jar bob.jar \
  --root . \
  --archive \
  --build-report-json build/reports/build-report.json \
  resolve build
```

Özel ayarlarla, grafik arayüzü olmadan çalışan bir test dağıtım paketi oluşturun:

```sh
java -jar bob.jar \
  --root . \
  --settings test/test.settings \
  --platform x86_64-linux \
  --variant headless \
  --archive \
  --bundle-output build/test-bundle \
  resolve build bundle
```

Oluşan yürütülebilir dosyayı platforma uygun bir süreç denetleyicisiyle çalıştırın. Çıkış durumunu ve günlüklerini kaydedin, bir zaman aşımı uygulayın ve yapılandırılmış test takımı tamamlanma olayını zorunlu tutun.

[Bob kılavuzu](/manuals/bob); platformları, ayar dosyalarını, dağıtım paketlerini, önbellekleri, yerel kod eklentilerini ve derleme raporlarını açıklar.

## Başarısızlık raporları ve çıktı dosyaları

İyi test sonuçlarının, bir başarısızlığı yeniden üretmek ve nedenini saptamak için yeterli kanıtı saklaması önerilir:

* test adı, çalıştırma tanımlayıcısı ve doğrulama koşulunun ayrıntıları;
* geçen süre ve sınıflandırılmış sonuç;
* konsolun veya sürecin tam günlüğü;
* Defold sürümü, hedef platform ve ilgili yapılandırma;
* Bob derleme raporu ve süreç çıkış durumu;
* varsa çalışma zamanı durumu veya sahnenin anlık görüntüsü;
* ekran görüntüleri, referans görüntüye göre farklar, kayıtlar veya tarayıcı izleri;
* oluşturulan tüm çıktı dosyalarına ait yollar veya bağlantılar.

Aynı biçimin bir geliştirici, yerel betik, CI hizmeti veya [yapay zekâ kodlama ajanı](/manuals/ai-agents) tarafından kullanılabilir olması önerilir. Böylece tanılama veya onarım başka birine devredildiğinde bile doğrulama belirlenimci kalır.
