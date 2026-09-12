---
title: Defold'da Live Update içeriği
brief: Live Update özelliği, derleme sırasında bilinçli olarak paket dışında bırakılan kaynakların çalışma zamanı ortamı tarafından getirilip uygulamanın dağıtım paketinde saklanmasını sağlayan bir mekanizma sunar. Bu kılavuz, bu mekanizmanın nasıl çalıştığını açıklar.
---

# Live Update

Bir oyunun dağıtım paketi (bundle) oluşturulurken Defold, oyunun tüm kaynaklarını (resource) hedef platforma özgü pakete ekler. Çalışan motor tüm kaynaklara anında erişebildiği ve bunları depolama alanından hızla yükleyebildiği için çoğu durumda bu tercih edilir. Ancak bazı durumlarda kaynakların yüklenmesini daha sonraki bir aşamaya ertelemek isteyebilirsiniz. Örneğin:

- Oyununuz bir dizi bölümden oluşuyor ve oyuncuların oyunun geri kalanına devam edip etmeyeceklerine karar vermeden önce denemeleri için pakete yalnızca ilk bölümü eklemek istiyorsunuz.
- Oyununuz HTML5 platformunu hedefliyor. Tarayıcıda bir uygulamayı depolama alanından yüklemek, uygulama başlatılmadan önce uygulama paketinin tamamının indirilmesini gerektirir. Böyle bir platformda, oyun kaynaklarının geri kalanını indirmeden önce asgari boyutta bir başlangıç paketi gönderip uygulamayı hızla çalışır duruma getirmek isteyebilirsiniz.
- Oyununuz, indirilmelerini oyunda görüntülenmelerinden hemen öncesine kadar ertelemek istediğiniz çok büyük kaynaklar (görüntüler, videolar vb.) içeriyor. Bunun amacı kurulum boyutunu düşük tutmaktır.

Live Update özelliği, koleksiyon vekili (collection proxy) kavramını genişletir; derleme sırasında bilinçli olarak paket dışında bırakılan kaynakların çalışma zamanı ortamı tarafından getirilip uygulamanın dağıtım paketinde saklanmasını sağlayan bir mekanizma ekler.

Bu sayede içeriğinizi birden fazla arşive ayırabilirsiniz:

* _Temel arşiv_
* Seviyelerin ortak dosyaları
* Seviye paketi 1
* Seviye paketi 2
* ...

## İçeriği Live Update için hazırlama

Büyük ve yüksek çözünürlüklü görüntü kaynakları içeren bir oyun yaptığımızı varsayalım. Oyun, bu görüntüleri bir oyun nesnesi (game object) ve görüntüyü içeren bir sprite bileşeni (sprite component) bulunan koleksiyonlarda (collection) tutar:

![Mona Lisa koleksiyonu](images/live-update/mona-lisa.png)

Motorun böyle bir koleksiyonu dinamik olarak yüklemesi için bir koleksiyon vekili bileşeni (component) ekleyip onu *`monalisa.collection`* dosyasına yönlendirmemiz yeterlidir. Artık oyun, koleksiyon vekiline bir `load` iletisi göndererek koleksiyondaki içeriğin depolama alanından belleğe ne zaman yükleneceğini seçebilir. Ancak biz daha ileri gidip koleksiyonda bulunan kaynakların yüklenmesini kendimiz kontrol etmek istiyoruz.

Bunun için koleksiyon vekilinin özelliklerindeki *Exclude* onay kutusunu işaretlemek yeterlidir. Bu, Defold'a uygulamanın dağıtım paketini oluştururken *`monalisa.collection`* içindeki tüm içeriği paket dışında bırakmasını söyler.

::: important
Temel oyun paketinin başvurduğu hiçbir kaynak paket dışında bırakılmaz.
:::

![Paket dışında bırakılan koleksiyon vekili](images/live-update/proxy-excluded.png)

## Live Update ayarları

Defold, uygulamanın dağıtım paketini oluştururken paket dışında bırakılan kaynakları bir yerde saklamalıdır. Live Update için proje ayarları bu kaynakların konumunu belirler. Ayarlara <kbd>Project ▸ Live update Settings...</kbd> seçeneğinden erişilir. Henüz bir ayar dosyası yoksa bu işlem bir tane oluşturur. *game.project* içinde, paketleme sırasında hangi Live Update ayar dosyasının kullanılacağını seçin. Böylece canlı ortam, kalite güvencesi (QA), geliştirme gibi farklı ortamlar için farklı Live Update ayarları kullanabilirsiniz.

![Live Update ayarları](images/live-update/05-liveupdate-settings-zip.png)

Defold şu anda kaynakları üç farklı yöntemle saklayabilir. Ayarlar penceresindeki *Mode* açılır listesinden yöntemi seçin:

`Zip`
: Bu seçenek, Defold'a paket dışında bırakılan kaynakları içeren bir Zip arşiv dosyası oluşturmasını söyler. Arşiv, *Export path* ayarında belirtilen konuma kaydedilir ve çalışma sırasında bir `zip:` URI'si ve `liveupdate.add_mount()` kullanılarak bağlanabilir (mount).

`Folder`  
: Bu seçenek, Defold'a paket dışında bırakılan tüm kaynakları içeren bir klasör oluşturmasını söyler. Dosyaları yüklemeden veya paketlemeden önce üzerlerinde sonradan işlem yapmanız gerektiğinde yararlıdır. Tek tek derlenmiş dosyaların beklenen kaynak yollarına yerleştirildiği bir klasör, çalışma sırasında bir `file:` URI'si kullanılarak bağlanabilir.

`Amazon`
: Bu seçenek, Defold'a paket dışında bırakılan kaynakları otomatik olarak bir Amazon Web Service (AWS) S3 kovasına yüklemesini söyler. AWS *Credential profile* adınızı girin, uygun *Bucket* seçeneğini seçin ve bir *Prefix* adı belirtin. AWS hesabının nasıl kurulacağı hakkında daha fazla bilgiyi bu [AWS kılavuzunda](/manuals/live-update-aws) bulabilirsiniz

## Live Update ile paketleme

::: important
Düzenleyiciden derleyip çalıştırma (<kbd>Project ▸ Build</kbd>) Live Update özelliğini desteklemez. Live Update özelliğini test etmek için projenin dağıtım paketini oluşturmanız gerekir.
:::

Live Update ile dağıtım paketi oluşturmak kolaydır. <kbd>Project ▸ Bundle ▸ ...</kbd> seçeneğini, ardından uygulamanın dağıtım paketini oluşturmak istediğiniz platformu seçin. Bu, paketleme iletişim kutusunu açar:

![Live Update uygulamasının dağıtım paketini oluşturma](images/live-update/bundle-app.png)

Paketleme sırasında, hariç tutulan tüm kaynaklar uygulamanın dağıtım paketinin dışında bırakılır. *Publish Live update content* onay kutusunu işaretlediğinizde, Defold'a Live Update ayarlarınızın yapılandırmasına göre (yukarıya bakın) paket dışında bırakılan kaynakları Amazon'a yüklemesini veya bir Zip arşivi oluşturmasını söylersiniz. Yayımlanan Live Update içeriği, uzaktan dağıtım için gereken tam kaynak listesini içeren `liveupdate.game.dmanifest` dosyasını içermeye devam eder.

Live Update içeriği yayımlanırken Defold, dağıtım paketindeki `game.dmanifest` dosyasından yalnızca Live Update için kullanılan kayıtları otomatik olarak kaldırır; yayımlanan `liveupdate.game.dmanifest` dosyası ise kaynak listesinin tamamını korur. Bu, dağıtım paketinin boyutunu ve çalışma sırasındaki bellek kullanımını azaltır. Eski `liveupdate.exclude_entries_from_main_manifest` ayarı kaldırılmıştır; projede bu ayara ait bir kayıt kaldıysa yok sayılır.

Arşiv tabanlı iş akışında `collectionproxy.get_resources()`, ilgili arşiv bağlanana kadar `{}` döndürür. Bağlama işleminden sonra, söz konusu vekilin kaynak karma değerlerini döndürür.

*Package* seçeneğine tıklayın ve uygulamanın dağıtım paketi için bir konum seçin. Artık uygulamayı başlatıp her şeyin beklendiği gibi çalıştığını kontrol edebilirsiniz.

## .zip arşivleri

Bir Live Update .zip dosyası, temel oyun paketinin dışında bırakılan dosyaları içerir.

Mevcut işlem hattımız yalnızca tek bir .zip dosyası oluşturmayı desteklese de bu zip dosyasını daha küçük .zip dosyalarına bölmek mümkündür. Böylece seviye paketleri, sezonluk içerikler vb. oyun içerikleri daha küçük parçalar halinde indirilebilir. Her .zip dosyası, içindeki her kaynağın üst verilerini (metadata) açıklayan bir bildirim dosyası (manifest) da içerir.

## .zip arşivlerini bölme

Kaynak kullanımı üzerinde daha ayrıntılı kontrol sağlamak için paket dışında bırakılan içeriği birkaç küçük arşive bölmek çoğu zaman tercih edilir. Seviyelerden oluşan bir oyunu birden fazla seviye paketine bölmek buna bir örnektir. Bir başka örnek de farklı bayram ve tatil temalı arayüz süslemelerini ayrı arşivlere koyup yalnızca takvimde o anda geçerli olan temayı yüklemek ve bağlamaktır.

Kaynak grafı (resource graph), `build/default/game.graph.json` dosyasında saklanır ve projenin dağıtım paketi her oluşturulduğunda otomatik olarak üretilir. Oluşturulan dosya, projedeki tüm kaynakların listesini ve her kaynağın bağımlılıklarını içerir. Örnek kayıt:

```json
{
  "path" : "/game/player.goc",
  "hexDigest" : "caa342ec99794de45b63735b203e83ba60d7e5a1",
  "children" : [ "/game/ship.spritec", "/game/player.scriptc" ]
}
```

Her kaydın, kaynağın proje içindeki benzersiz yolunu temsil eden bir `path` alanı vardır. `hexDigest`, kaynağın kriptografik parmak izini temsil eder ve Live Update .zip arşivinde kullanılan dosya adı olur. Son olarak `children` alanı, bu kaynağın bağlı olduğu diğer bağımlılıkların listesidir. Yukarıdaki örnekte `/game/player.goc`, bir sprite bileşenine ve bir betik bileşenine bağımlıdır.

`game.graph.json` dosyasını ayrıştırıp bu bilgileri kullanarak kaynak grafındaki kayıt gruplarını belirleyebilir ve bunlara karşılık gelen kaynakları özgün bildirim dosyasıyla birlikte ayrı arşivlerde saklayabilirsiniz (bildirim dosyası, çalışma sırasında yalnızca arşivdeki dosyaları içerecek şekilde budanır).

## Android'de Live Update

Live Update içeriğini indirmek ve bağlamak için Play Asset Delivery kullanabilirsiniz. Daha fazla bilgiyi [resmî kılavuzda](https://defold.com/extension-pad/) bulabilirsiniz.

## İçerik doğrulama

Live Update sisteminin başlıca özelliklerinden biri, artık birçok farklı Defold sürümünden gelebilen çok sayıda içerik arşivini kullanabilmenizdir.

`liveupdate.add_mount()` işlevinin varsayılan davranışı, bir bağlama eklerken motor sürümünü kontrol etmektir.
Bu, hem oyunun temel arşivinin hem de Live Update arşivlerinin paketleme seçeneği kullanılarak aynı anda, aynı motor sürümüyle oluşturulması gerektiği anlamına gelir. Bu işlem, istemcinin daha önce indirdiği tüm arşivleri geçersiz kılar ve istemcinin içeriği yeniden indirmesini gerektirir.

Bu davranış bir seçenek bayrağıyla kapatılabilir.
Kapatıldığında, her Live Update arşivinin kullanılmakta olan motorla çalışacağını garanti etmek için içeriği doğrulama sorumluluğu tamamen geliştiriciye aittir.

Uygulamanın paketin bağlı kalıp kalmayacağına karar verebilmesi için her bağlamaya ait üst verileri saklamanızı öneririz. Uygulamanın başlangıç sırasında gereken bağlamaları yeniden eklediği durumlar da dahil olmak üzere, bağlamayı ekledikten sonra bu verileri doğrulayın.
Bunu yapmanın bir yolu, oyunun dağıtım paketi oluşturulduktan sonra zip arşivine ek bir dosya koymaktır. Örneğin, oyunun ihtiyaç duyduğu bilgileri içeren bir `metadata.json` dosyası ekleyin ve ardından bağlama işleminden sonra `sys.load_resource("/metadata.json")` ile bu dosyayı alın. _Her bağlamanın özel verileri için benzersiz bir kaynak yolu kullanın; aksi takdirde kaynak araması en yüksek önceliğe sahip bağlamadaki dosyayı döndürür._

Bunu yapmazsanız içeriğin motorla hiç uyumlu olmadığı ve motorun kapanmak zorunda kaldığı bir durumla karşılaşabilirsiniz.

## Bağlamalar

Live Update sistemi aynı anda birden fazla içerik arşivini kullanabilir.
Her arşiv, bir ad ve öncelik değeriyle motorun kaynak sistemine "bağlanır".

İki arşivde de aynı `sprite.texturec` dosyası varsa motor, dosyayı en yüksek önceliğe sahip bağlamadan yükler.

Motor, bir bağlamadaki herhangi bir kaynağa başvuru tutmaz. Bir kaynak belleğe yüklendikten sonra arşivin bağlaması kaldırılabilir. Kaynak, bellekten kaldırılana kadar bellekte kalır.

Bağlamalar yalnızca geçerli motor oturumu boyunca etkindir. Uygulama, yeniden başlatıldıktan sonra ihtiyaç duyduğu her paket için `liveupdate.add_mount()` işlevini yeniden çağırmalıdır. Bu seçimlerin oturumlar arasında korunması gerekiyorsa paket konumunu, bağlama adını ve önceliğini uygulamanın yönettiği kalıcı verilerde saklayın.

::: sidenote
Bir Zip arşivini veya klasörü bağlamak onu kopyalamaz ya da taşımaz. Bağlanan içerik, bağlama kullanımda olduğu sürece belirtilen konumda kalmalıdır.
:::

## Live Update ile betik yazma

Live Update içeriğini kullanabilmek için verileri indirip oyununuza bağlamanız gerekir.
[Live Update ile nasıl betik yazılacağı hakkında daha fazla bilgiyi burada bulabilirsiniz](/manuals/live-update-scripting).

## Geliştirme sırasında dikkat edilmesi gerekenler

Hata ayıklama
: Oyununuzun dağıtım paketi oluşturulmuş bir sürümünü çalıştırırken bir konsola doğrudan erişiminiz olmaz. Bu durum, hata ayıklamada sorunlara yol açar. Ancak uygulamayı komut satırından veya dağıtım paketindeki yürütülebilir dosyaya doğrudan çift tıklayarak çalıştırabilirsiniz:

  ![Dağıtım paketindeki uygulamayı çalıştırma](images/live-update/run-bundle.png)

  Artık oyun, tüm `print()` ifadelerinin çıktısını gösterecek bir kabuk penceresiyle başlar:

  ![Konsol çıktısı](images/live-update/run-bundle-console.png)

Kaynakların yeniden indirilmesini zorunlu kılma
: Geliştirici, içeriği istediği dosyaya veya klasöre indirebilir; ancak içerik genellikle uygulama yolunun altında bulunur. Uygulama destek klasörünün konumu işletim sistemine bağlıdır. Bu konum `print(sys.get_save_file("", ""))` ile bulunabilir. Yeniden indirmeyi zorunlu kılmak için indirilen paketi ve uygulamanın yönettiği durum verilerindeki ilgili kaydı kaldırın. Silinecek, motor tarafından yönetilen bir bağlama listesi yoktur; bağlamalar yeniden başlatmalar arasında korunmaz.

  ![Yerel depolama](images/live-update/local-storage.png)
