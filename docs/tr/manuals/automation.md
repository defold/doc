---
title: Defold'da otomasyon
brief: Bu kılavuz Defold'un otomasyon arayüzlerini tanıtır ve düzenleyici, çalışma zamanı, komut satırı, test ve ajanların yönettiği iş akışları arasında nasıl seçim yapılacağını açıklar.
---

# Defold'da otomasyon

Bu kılavuz, genel bir açıklama ve her konu için ayrı kılavuzlara bağlantılar sunar.

Defold, çeşitli düzeylerde otomasyonu destekler. Göreve uygun bir arayüz seçmek, etkili otomasyonun en önemli yönlerinden biridir. Aşağıdaki tablo, belirli bir işlem için en basit arayüzü seçmenize yardımcı olabilir:

| Katman | Amaç |
| --- | --- |
| [Düzenleyici betikleri (Editor Scripts)](/manuals/editor-scripts) | Test ve geliştirme süreçlerini hızlandıran özel komutlar ve düzenleyici iş akışları veya tümleştirmeleri; örneğin bölüm ve varlık (asset) oluşturma |
| [Düzenleyici UI betikleri](/manuals/editor-scripts-ui/) | Düzenleyici betiklerinden yararlanan özel görsel araçlar, açılır pencereler, yapılandırma araçları veya kullanıcı arayüzleri (UI) |
| [Düzenleyici HTTP API'si](/manuals/editor-http-api) | Özel işlemler, harici araçlar, IDE tümleştirmeleri ve test denetleyicileri için Defold düzenleyicisinde açık olan oyun projesini OpenAPI işlemleri, proje kaynakları (resource), derlemeler, düzenleyici komutları, önizlemeler, tercihler, konsol çıktısı veya düzenleyici betikleri aracılığıyla denetleme |
| [Bob CLI](/manuals/bob) | Komut satırından proje derleme, veri arşivleri veya bağımsız dağıtım paketleri oluşturma, raporlar, CI |
| [Yaşam döngüsü kancaları (lifecycle hooks)](/manuals/editor-http-api#lifecycle-hooks) | Düzenleyicide proje derleme veya paketleme işlemlerinden önce ve sonra geçerleme veya üretim |
| [Motor HTTP hizmeti](/manuals/engine-service) | Çalışan Defold oyun motorunu (`dmengine`) inceleme, geliştirme hizmetleri, profil çıkarma, çalışma zamanı iletileri veya uzantıların tanımladığı çalışma zamanı otomasyon API'leri, harici araçlarla sorgulama, çalışan bir hata ayıklama derlemesine komut gönderme |
| [Automation Bridge](https://github.com/defold/extension-automation-bridge) | motorun çalışma zamanı için ek otomasyon uç noktaları sağlayan resmî Defold uzantısı |
| [Otomatik testler](/manuals/automated-testing) | Oyun mantığını, iletileri, bileşenleri (component), girdiyi, fiziği ve motor davranışını test etme, sahne inceleme, örneğin [düzenleyici önizlemesi](/manuals/editor-http-api/#rendering-scene-previews) aracılığıyla görsel geri bildirim, program yoluyla sağlanan girdi, canlı uygulama durumu, [test koleksiyonlarını (collection) çalıştırma](/manuals/automated-testing/#tests-in-a-running-collection) |
| Kabuk betikleri veya görev çalıştırıcıları | Üretim, biçimlendirme, geçerleme ve tekrarlanabilir görevler, sıradan dosya işlemleri |
| Platforma özgü harici araçlar ve web tarayıcısı otomasyon araçları | Masaüstü test araçları, HTML5 etkileşim testleri, ekran görüntüleri, web tümleştirmeleri |
| Yapay zekâ kodlama ajanları ve çok modlu modeller | Belirlenimci (deterministic) bir yaklaşımı uygulamanın zor veya imkânsız olduğu görevler, sahnelerin, GUI yerleşimlerinin veya çalışma sırasında alınan ekran görüntülerinin anlamsal analizi |

En önemli ayrım, Defold düzenleyicisi ile çalışan bir oyun arasındadır. Bunlar, ayrı HTTP sunucularına sahip ayrı süreçlerdir.

## Belirlenimci otomasyon veya yapay zekâ ajanları

İşlem sırası zaten biliniyorsa, örneğin bir bölüm geçerleme aracında, biçimlendiricide, derleme görevinde veya gerileme testinde, belirlenimci bir çözümü tercih edin. Bunların normalde girdilerinin, çıktılarının, zaman aşımı sürelerinin ve çıkış kodlarının tutarlı olması önerilir. Bu yaklaşım, CI üzerinde güvenilir biçimde çalıştırılabilen otomatik kancalar ve testler için uygundur. Projelerinizde kaynakları prosedürel olarak oluşturmak için de belirlenimci bir çözüm tercih edilir; örneğin gltf nesnelerini belirli bir materyale sahip modellere dönüştüren veya bir bölüme ağaçlar gibi nesneler yerleştiren bir araç. Bu işlemler, düzenleyici betikleri ve UI ile her proje için kolayca oluşturulabilir. Bunlar hakkında daha fazla bilgi için [kılavuzu](/manuals/editor-scripts-ui) okuyun.

Bir görev araştırma veya çok modlu (örneğin görsel içeriği de kapsayan) analiz gerektiriyorsa ajan yararlı olabilir: ilgili kaynakları bulmak, bir uygulama biçimi seçmek, birkaç dosyayı değiştirmek, hataları yorumlamak ve tanımlanmış kabul ölçütlerine ulaşana kadar yinelemek gibi. Bununla birlikte ajanın yine de belirlenimci arayüzleri çağırması ve yerel bir betik veya CI çalıştırıcısıyla aynı kanıtları kullanması önerilir. [Defold ile yapay zekâ kodlama ajanlarını kullanma](/manuals/ai-agents) kılavuzuna bakın.

## Otomasyon döngüsü {#the-automation-loop}

Güvenilir bir otomasyon süreci kapalı bir döngü oluşturur:

1. İnceleyin - proje dosyalarını, güncel arayüz açıklamasını ve ilgili belgeleri okuyun.
2. Değiştirin - düzenleyici işlemlerini (editor transactions), düzenleyici betiklerini veya dosya ve kabuk araçlarını kullanın.
3. Doğrulayın - projeyi derleyin, belirli bir konuya odaklanan testleri çalıştırın ve günlükleri, raporları, durum bilgilerini veya görüntüleri toplayın.
4. Değerlendirin - kanıtları kabul ölçütleriyle karşılaştırın, ardından bitirin veya yeniden deneyin.

![İnceleme, değiştirme, doğrulama ve değerlendirmeden oluşan otomasyon döngüsü](images/automation/automation_loop.png)

Doğrulamanın gerçek ortamdan kanıt sağlaması önerilir. Uygun kanıtlar şunları içerir:

* başarılı bir proje derleme sonucu;
* tamamlandığı açıkça belirtilen bir test takımı;
* çalışan oyundaki beklenen durum;
* oluşturulmuş bir dağıtım paketi veya derleme raporu;
* belirlenimci bir görüntü karşılaştırması;
* tanımlanmış görsel ölçütleri karşılayan bir ekran görüntüsü.

Değişiklik yapmadan önce beklenen sonucu tanımlayın. Ayrıca bir zaman aşımı süresi ve en fazla kaç düzeltme denemesi yapılacağını belirleyin. Gözetimsiz bir sürecin, kabul ölçütlerini karşılayamadığında süresiz olarak devam etmesi önerilmez.

## Sonraki adımlar

Otomasyon iş akışlarıyla ilgili belirli konular hakkında daha ayrıntılı bilgi için aşağıdaki kılavuzlara bakın:

* [Defold düzenleyicisi görevlerini HTTP API ile otomatikleştirme](/manuals/editor-http-api)
* [Motor hizmeti ve çalışma zamanı HTTP API'si](/manuals/engine-service)
* [Otomatik test ve doğrulama](/manuals/automated-testing)
* [Defold ile yapay zekâ kodlama ajanlarını kullanma](/manuals/ai-agents)
