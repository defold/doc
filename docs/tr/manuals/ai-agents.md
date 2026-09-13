---
title: Defold ile yapay zekâ kodlama ajanlarını kullanma
brief: Bu kılavuz, doğrulama, izinler ve güvenlik konularını açıkça ele alarak belirli bir modele bağlı olmayan kodlama ajanlarının Defold otomasyon arayüzlerine nasıl bağlanacağını açıklar.
---

# Defold ile yapay zekâ kodlama ajanlarını kullanma

Büyük dil modellerini (LLM) ve çok modlu modelleri kullanan kodlama ajanları (coding agents), geliştiricilerin, yerel betiklerin, IDE tümleştirmelerinin ve sürekli tümleştirmenin (CI) kullandığı, belirli bir modele bağlı olmayan arayüzleri çağırarak Defold projelerini inceleyebilir, değiştirebilir ve doğrulayabilir. İşin araştırma ve uyarlama gerektirdiği durumlarda bir ajan kullanabilirsiniz.

Defold, belirli bir model sağlayıcısına veya ajan protokolüne bağlı değildir. Defold projeleri Claude Code, Codex, Cursor veya başka herhangi bir çözümle iyi çalışır. Bir ajan ortamı yalnızca görev için tanınan belirli yeteneklere ihtiyaç duyar; örneğin proje dosyalarını okuma, seçili komutları yürütme, yerel HTTP işlemlerini çağırma, JSON verilerini ayrıştırma veya görüntüleri inceleme. Bu, Defold'un düzenleyici ve çalışan bir oyun motoru örneği (engine instance) için sunduğu otomasyon arayüzleri ve Defold proje dosyalarının kolay ayrıştırılabilen metin tabanlı kaynak (resource) dosyaları olması sayesinde mümkündür.

## Yapay zekâ ajanı ne zaman yararlıdır?

Bir görev örneğin şunları gerektirdiğinde ajan yararlı olabilir:

* ilgili kaynakları ve belgeleri bulmak;
* olası uygulamalar arasından seçim yapmak;
* birbiriyle ilişkili birden çok dosyayı değiştirmek;
* derleme veya test başarısızlıklarını yorumlamak;
* görsel bir sonucu anlamsal kabul ölçütleriyle karşılaştırmak;
* toplanan kanıtlara dayanarak sınırları belirlenmiş bir düzeltme girişiminde bulunmak.

Ajanlar, belirlenimci olmayan geliştirme, araştırma ve test süreçlerinde güçlü araçlardır. Farklı çözümler oluşturmaya yardımcı olabilirler ve Defold ile çok iyi çalışırlar.

## Belirli bir modele bağlı olmayan Defold arayüzleri

Defold, görevin mevcut herhangi bir model kullanılarak gerçekleştirilmesi için gereken, desteklenen çeşitli arayüzler sunar:

* Proje dosyaları ve kabuk araçları doğrudan inceleme ve metin değişiklikleri yapma olanağı sağlar.
* [Düzenleyici betikleri](/manuals/editor-scripts), projeye özgü kaynak işlemleri ve araçlar sağlayabilir.
* [Düzenleyici HTTP API'si](/manuals/editor-http-api), düzenleyici komutları, derleme sonuçları, konsol çıktısı, başvuru araması, önizlemeler, tercihler ve düzenleyici betiği rotaları sağlar.
* [Motor hizmeti ve çalışma zamanı otomasyon API'leri](/manuals/engine-service), hata ayıklama motorunun canlı durumunu, girdileri, ekran görüntülerini ve eklentilerin tanımladığı işlemleri sağlar.
* [Bob](/manuals/bob), komut satırından proje derleme olanağı, raporlar, arşivler ve dağıtım paketleri sağlar.

Yalnızca sohbet arayüzü üzerinden erişilebilen bir model kod değişiklikleri önerebilir, ancak yerel projeyi bağımsız olarak inceleyemez veya çalışan bir sonucu doğrulayamaz. Ajanın gerçekte neyi gözlemleyip yapabileceğini, onu çevreleyen ek tümleştirme belirler.

## Tümleştirme katmanları

Bir ajanı yerel Defold işlemlerine bağlamak için tümleştirme katmanı (integration layer) kurulabilir. Bu katman bir kabuk sarmalayıcısı, komut satırı programı, IDE eklentisi, OpenAPI istemcisi, test denetleyicisi veya protokol bağdaştırıcısı olabilir.

Politikaları ve kimlik bilgilerini bu yerel katmanda tutun. Değişiklik yapan her işlemin yapılandırılmış sonuçlar döndürmesi veya belirlenimci bir doğrulama adımına yol açması önerilir.

Düzenleyici işlemleri için ajana API'nin kalıcı olarak kod içine sabitlenmiş bir kopyasını vermek yerine, geçerli arayüzü `/openapi.json` üzerinden keşfedin. Çalışma zamanı eklentileri için bunların sağlık durumunu, API sürümünü ve yeteneklerini kontrol edin.

Araçları yetki düzeyine göre ayırmak pratik olabilir:

| Düzey        | Örnekler                                              |
| ------------ | ----------------------------------------------------- |
| Salt okunur  | Proje inceleme, OpenAPI, `/ref`, konsol, önizleme       |
| Doğrulama    | Kod derleme, testler, HTML5 derlemeleri, görüntü karşılaştırmaları |
| Değişiklik   | Dosya değişiklikleri, kaynak işlemleri                 |
| Ayrıcalıklı  | `/eval`, harici komutlar, bağımlılık değişiklikleri     |

Bağdaştırıcıyı motordan ve düzenleyiciden ayrı tutmak, desteklenen Defold arayüzlerinin model sağlayıcısından veya ajan protokolünden bağımsız kalmasını sağlar. Bir bağdaştırıcı yalnızca kendi ortamına uygun işlemleri sunabilir; izin ve onay politikaları ise ajanı barındıran uygulamada kalır.

### Model Context Protocol

[Model Context Protocol](https://modelcontextprotocol.io/) (MCP), ajan ile tümleştirme katmanı arasında kullanılabilecek isteğe bağlı bir bağdaştırıcıdır. Bir MCP sunucusu, Defold işlemlerini araç olarak ve seçili belgeleri kaynak olarak sunabilir. 

::: important
Her modele sınırsız kabuk ve `/eval` erişimi vermeyin.
:::

Defold şu anda bir MCP sunucusu gerektirmez; çünkü temel otomasyon yetenekleri zaten açık, genel amaçlı arayüzler üzerinden sunulmaktadır. Düzenleyici, OpenAPI belirtimi olan yerel bir HTTP API'si sağlar. Modern ajanlar bu arayüzleri doğrudan çağırabilir veya kendi bağdaştırıcılarını oluşturabilir. 

Bu nedenle resmî bir MCP, büyük ölçüde mevcut API'nin sunduğu işlemleri tekrarlayacak ve Defold'un bakımını yapması gereken bir tümleştirme katmanı daha oluşturacaktır. Uzun vadede daha iyi bir strateji, temel HTTP ve çalışma zamanı otomasyon API'lerini kararlı, keşfedilebilir ve iyi belgelenmiş tutarken topluluğun veya araç sağlayıcılarının gerektiğinde hafif MCP sarmalayıcıları oluşturmasına olanak tanımaktır.

Bunun yerine, çalışan bir oyunun motor tarafındaki bir hizmet üzerinden kontrol edilmesini sağlayan resmî bir [Automation Bridge eklentisi](https://github.com/defold/extension-automation-bridge) sunduk.

### Topluluk MCP tümleştirmeleri

Topluluğun oluşturduğu MCP tümleştirmeleri arasında şunlar bulunur:

* [Fulviuus Defold MCP projesi](https://github.com/Fulviuus/defold-mcp);
* [ChadAragorn Defold MCP projesi](https://github.com/ChadAragorn/defold-mcp).

Bu projeler Defold Foundation tarafından geliştirilmez, denetlenmez, bakımı yapılmaz veya resmî olarak desteklenmez. Herhangi bir topluluk tümleştirmesini kurmadan önce güncel kaynak kodunu, bağımlılıklarını, izinlerini, ağ davranışını ve kullanılan Defold sürümüyle uyumluluğunu inceleyin.

## Proje talimatları

Ajan tabanlı iş akışlarında kullanılan mevcut büyük dil modelleri genellikle iyi talimatlarla daha iyi performans gösterir. Bu nedenle projelere sıklıkla ajanlardan beklenen davranışı açıklayan Markdown dosyaları veya skill adı verilen talimat paketleri eklenir. En iyi sonuçları elde etmek için her projeye özel talimatlar tasarlayıp yazmak yararlıdır; ancak bazı ortak bilgiler ve kurallar yeniden kullanılabilir.

Birçok ajanın arayıp okuduğu ilk dosya, aşağıdakileri açıklayabilen `AGENTS.md` gibi standart bir dosyadır:

* proje yapısı ve önemli giriş noktaları;
* biçimlendirme ve adlandırma kuralları;
* derleme, test ve geçerleme komutları;
* gerekli tamamlanma olayları ve çıktı dosyalarının konumları;
* değiştirilmemesi gereken dosyalar veya dizinler;
* onay gerektiren işlemler;
* platforma ilişkin varsayımlar ve bilinen sınırlamalar.

Bazı çözümler belirli eylemler için ayrı Markdown dosyalarına veya "skill" adı verilen talimat paketlerine dayanabilir.

Defold'a yönelik talimatların ve skill paketlerinin topluluk tarafından hazırlanmış bir örneğine [Defold forumundaki bu gönderiden](https://forum.defold.com/t/agent-config-collection-of-agents-md-and-skills/82387) ulaşabilirsiniz.

AGENTS.md gibi dosyalardaki talimatlarınızı ve skill tanımlarınızı kısa, öz, incelemesi ve bakımı kolay tutmanızı ve güncel tutmanızı öneririz. Projeye özgü talimatlar sürüm kontrolünde saklanabilir; bu, değişiklikleri izlenebilir kılar ve iş akışı performansının zamanla iyileştirilmesine yardımcı olur.

En yeni modellerin bu talimatlar olmadan nasıl performans gösterdiğini düzenli olarak test etmek de yararlıdır. Daha yeni modeller, önceden gerekli olan yönlendirmelere çoğu zaman artık ihtiyaç duymaz; güncelliğini yitirmiş skill paketleri veya aşırı kuralcı talimatlar bazen performansı düşürebilir.

Uzun vadede önemli miktarda bakım gerektiren karmaşık teknik skill paketleri oluşturmaktan kaçının. Bunun yerine, kullanılan modeller ne kadar gelişirse gelişsin değerini koruyan araçlar ve iş akışları geliştirmeye odaklanın.

## Belgeleri keşfetme

Ajanlar, doğru ve güncel belgelerle en iyi performansı gösterir. Güncel bilgileri şu kaynaklardan toplayın:

* `/openapi.json`, geçerli düzenleyici HTTP API'sini açıklar.
* `/ref`, bu işlem kullanılabilir olduğunda, çalışan düzenleyiciyle birlikte gelen API belgelerinde arama yapar.
* [LLM belge dizini](https://defold.com/llms.txt), resmî kılavuzlara, API ad alanlarına ve örneklere bağlantılar içerir.
* [Tam LLM belgeleri](https://defold.com/llms-full.txt), çevrimdışı aramayı ve yerel dizinlemeyi destekler.

Yalnızca görevle ilgili sayfaları alın. Birleştirilmiş belgenin tamamının yalnızca çevrimdışı dizinleme veya [bilgi getirmeyle desteklenen üretim (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) için kullanılması önerilir. Yine, token kullanımından tasarruf etmek ve bağlamı gereksiz bilgilerle doldurmamak için dosyanın tamamının normalde her model isteğine eklenmemesi önerilir.

## Sınırları belirlenmiş değişiklik ve doğrulama döngüleri

Ajanların diğer tüm otomasyonlarla aynı [incele, değiştir, doğrula, değerlendir döngüsünü](/manuals/automation/#the-automation-loop) izlemesi önerilir.

Dosyaları değiştirmeden önce kabul ölçütlerini ve isteğe bağlı olarak aşağıdakileri de tanımlamak yararlıdır:
* izin verilen dosyalar ve işlemler;
* derleme ve test komutları;
* gerekli günlükler, raporlar, durum veya görüntüler;
* her eşzamansız adım için bir zaman aşımı;
* en fazla kaç düzeltme girişiminde bulunulacağı.

Bir ajan, belirlenimci bir CI başarısızlığını tanılayıp düzeltebilir; ancak CI aşamasının kendisinin ajan olmadan da yeniden üretilebilir kalması önerilir.

Otomatik test ve doğrulamaya ilişkin iyi uygulamalar [bu kılavuzda](/manuals/automated-testing) açıklanır.

## Çok modlu değerlendirme

Görüntü girdisi alabilen bir ajan, [düzenleyici önizlemelerini](/manuals/editor-http-api/#rendering-scene-previews), çalışma sırasında alınan ekran görüntülerini, görsel farkları ve tarayıcı görüntülerini inceleyebilir.

Kırpılmış etiketler, üst üste binen denetimler, belirsiz seçim durumları, kompozisyon veya güvenli alanın dışındaki içerik gibi anlamsal konular için çok modlu değerlendirme kullanın. Beklenen görüntü alanını ve ölçütleri önceden tanımlayın.

Düzenleyici önizlemeleri, çalışma sırasında alınan ekran görüntüleri ve görsel inceleme hakkında daha fazla bilgi için [bu kılavuzu](/manuals/automated-testing) okuyun.

## Güvenlik, yalıtım ve iyi uygulamalar

* Düzenleyici sunucusunu ve motor hizmetini güvenilen yerel kontrol arayüzleri olarak değerlendirin.
* Düzenleyici erişim belirteçlerini, imzalama anahtarlarını, dağıtıma alma belirteçlerini, mağaza kimlik bilgilerini ve üretim ortamındaki gizli bilgileri istemlerin ve raporların dışında tutun.
* Yerel tümleştirme katmanı, `/eval` kullanmak için yetkilendirildiğinde `.internal/editor.token` dosyasını okuyabilir; ancak belirteci model istemlerine, günlüklere veya raporlara koyması önerilmez.
* Silme, bağımlılık değişiklikleri, yerel kod eklentisi değişiklikleri, yayımlanacak sürümün yapılandırılması, imzalama, yayımlama veya harici hizmetlere erişim öncesinde onay alın.
* Kapsamlı otonom çalışmaları ayrı bir dalda, çalışma ağacında, geçici kopyada, konteynerde, yalıtılmış çalışma ortamında veya kısıtlı hesapta yürütün.
* Sorun kaydı metinlerini, içe aktarılan dosyaları, kaynak kod yorumlarını, oluşturulan belgeleri ve araç çıktılarını talimat olarak değil, güvenilmeyen girdi olarak değerlendirin.
* İndirilen bağımlılıkları ve betikleri yürütmeden önce inceleyin.
* Proje politikasının kaynak kodun, varlıkların, günlüklerin, ekran görüntülerinin ve diğer proje verilerinin barındırılan bir modele gönderilmesine izin verdiğini doğrulayın.
* Değişiklikleri kabul etmeden önce incelenebilir bir değişiklik dökümünü ve belirlenimci test kanıtlarını saklayın.

Yalıtım, bir hatanın etkisini sınırlar.
