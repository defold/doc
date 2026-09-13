---
title: RPG haritası örneği
brief: Bu örnek projede, çok büyük RPG haritaları oluşturmanın bir yöntemini öğreneceksiniz.
---
# RPG haritası - örnek proje

[Düzenleyiciden açabileceğiniz](/manuals/project-setup/) veya [GitHub'dan indirebileceğiniz](https://github.com/defold/sample-rpgmap) bu örnek projede, Defold'da çok büyük RPG haritaları oluşturmanın bir yöntemini gösteriyoruz. Tasarım şu varsayımlara dayanır:

1. Dünya, her seferinde tek bir ekran gösterilerek sunulur. Bu, oyunun düşmanları ve NPC karakterlerini doğal olarak tek bir ekranın sınırları içinde tutmasını sağlar. Bölüm tasarımcısı, dünyanın oyuncunun ekranında nasıl sunulacağı üzerinde tam kontrole sahiptir.
2. Oyuncu karakteri, oyunda kayan noktalı sayıların hassasiyetiyle ilgili sorunlar oluşmadan istediği kadar uzağa gidebilmelidir. Bu sorunlar genellikle nesnelerin başlangıç noktasından uzaklaştıklarında tuhaf bir şekilde titreşmelerine neden olur.
3. Oyuncunun hareketi haritadaki engellerle sınırlandırılır; böylece bölüm tasarımcısı ağaçları, kayaları, suyu ve diğer engelleri kullanarak oyuncuyu ekranlar arasında yönlendirebilir.
4. Karo haritalarını (tilemap), sprite bileşenlerini (sprite component) ve diğer görsel içerikleri farklı birleşimler halinde bir arada kullanmak mümkün olmalıdır.

Önce örneği çalıştırın ve nasıl yapılandırıldığını anlamak için 3x3 ekran büyüklüğündeki dünyada dolaşın. Karakteri ok tuşlarıyla kontrol edersiniz.

## Ana koleksiyon

Bu örneğin başlangıç koleksiyonunu (bootstrap collection) görmek için "/main/main.collection" dosyasını açın.

![](images/rpgmap/main_collection.png)

Ana koleksiyon, ok tuşlarıyla 8 yönde kontrol edilen oyuncu karakterinin oyun nesnesini (game object) ve oyunun akışını kontrol eden "game" adlı ikinci bir oyun nesnesini içerir. "game" nesnesi, bir betikten ve oyundaki her ekran için bir koleksiyon fabrikasından (collection factory) oluşur. Fabrikalar, ekran ızgarasının adlandırma şemasına göre adlandırılır.

"/main/game.script" betiği, oyuncunun o anda hangi ekranda olduğunu takip eder. Betik ayrıca "load_screen" adlı özel bir iletiye tepki verir. Bu ileti yeni bir ekran yükler ve kahramanın hareket ettiği yönde bu ekranı geçerli ekranla değiştirir. Başlangıçta bir ekran, görüntünün merkezine yüklenir ve yer değiştirecek başka bir ekran yoktur.

## Ekran değiştirme

Kahraman, "/main/hero.script" betiğiyle kontrol edilir. Betik, kahramanın oyun nesnesinin ekranın üst, alt, sol veya sağ kenarına yakın bir çizgiyi geçip geçmediğini kontrol eder:

![](images/rpgmap/change_screen.png)

1. Kahraman bir ekran kenarına yeterince yaklaşırsa, sonraki ekranı yüklemek için "game" nesnesinin betiğine bir ileti gönderilir.
2. Sonraki ekranın koleksiyonu, doğru collectionfactory bileşeninde `factory.create()` çağrılarak oluşturulur. Koleksiyonun içeriği ekranın dışına yerleştirilir.
3. Sonraki ekran, görüntünün merkezine kaydırılır ve geçerli ekran ters yönde dışarı kaydırılır. Oyuncu karakteri de aynı mesafe boyunca ve aynı hızla kaydırılır.
4. Artık ekran dışında kalan eski geçerli ekran silinir ve sonraki ekran, yeni geçerli ekran olur.
5. Kahraman, bir animasyonla yeni ekranda görünür hâle gelir ve oyuncu kontrolü geri kazanır.

Bütün bunlar bir saniye içinde gerçekleştiğinden geçiş akıcıdır ve oynanışı kesintiye uğratmaz.

## Ekranlar

Oyun dünyasındaki her ekran, o ekrana özgü karo haritasını, çarpışma nesnesini (collision object) ve diğer oyun nesnelerini içeren ayrı bir koleksiyonun içinde oluşturulur. Ekranların yönetimini ve yüklenmesini kolaylaştırmak için ekran koleksiyonları basit bir şemaya göre adlandırılır:

![](images/rpgmap/screens.png)

Her ekran koleksiyonu, dünya ızgarasındaki konumuna göre adlandırılır. İlk sayı ızgaradaki X konumunu, ikinci sayı ise Y konumunu belirtir.

*Assets* görünümünde, haritanın sol alt köşesindeki ekranı tanımlayan "/main/screens/0-0.collection" koleksiyonunu bulun ve açın:

![](images/rpgmap/screen_collection.png)

Ekranın tüm içeriğinin üst nesnesi olan "root" adlı bir oyun nesnesi bulunduğuna dikkat edin. Bu, örnekte kullanılan başka bir düzenleme kuralıdır ve çok önemli bir amaca hizmet eder: bir ekran görüntüye getirildiğinde yalnızca "root" oyun nesnesinin taşınması gerekir. Tüm alt nesneler otomatik olarak kök üst nesneyle birlikte taşınır. Bir ekranda özel oyun nesneleri varsa bunların hareketi kök üst nesneye göre tanımlandığından bu nesnelere serbestçe animasyon da uygulanabilir. Ekran içeri veya dışarı kaydırıldığında bu alt nesneler ekranla birlikte hareket eder. Yalnızca bir nesnenin ekranlar arasında hareket etmesi gerekiyorsa özel kod gerekir.

0-1 ekranındaki arılar bu fikri gösteren basit örneklerdir:

![](images/rpgmap/bees.png)

## Ekranları dünya bağlamında düzenleme

Her ekranın, yerleşik karo haritası düzenleyicisinde düzenlenebilen kendi karo haritası vardır. Ancak her ekranı ayrı olarak düzenlemenin başlıca dezavantajı, komşu ekranlarla nasıl birleştiğinin kolayca görülememesidir. Bu bağlantılar, oyun dünyası boyunca süreklilik sağlamanın önemli bir parçasıdır.

Bu nedenle özel bir koleksiyon oluşturulmuştur. Dünyanın test düzenini içeren bu koleksiyonu görmek için "/main/map/test_layout.collection" dosyasını açın:

![](images/rpgmap/test_layout.png)

Bu koleksiyonun tek amacı, geliştirme sırasında bir düzenleme aracı olarak kullanılmaktır. Belirli bir ekranı test düzeni koleksiyonuyla yan yana düzenlemek, üzerinde çalıştığınız ekranın bağlamını görmenizi sağlar ve düzenleme sürecini çok daha rahat hâle getirir:

![](images/rpgmap/side_by_side.png)

Ekranın karo haritasında (burada sağ bölmede) yapılan tüm düzenlemeler, test koleksiyonuna (sol bölmede) anında yansıtılır. Ayrıca test düzeni koleksiyonunun statik hiyerarşiye eklenmediğine, dolayısıyla tüm derlemelerden otomatik olarak çıkarıldığına dikkat edin.

## Özet

Gördüğünüz gibi bu örnek, oyun dünyası ve kahramanın bu dünyada nasıl ilerlediğiyle ilgili belirli kısıtlamalara göre oluşturulmuştur. Oyununuzun gereksinimleri farklıysa muhtemelen farklı bir çözüm bulmanız gerekir. Örneğin oyununuz kameranın dünya haritası üzerinde kesintisiz biçimde hareket etmesini gerektiriyorsa, içeriğinizi parçalara ayırmak için farklı bir yönteme, farklı bir yükleme mekanizmasına ve oyun dünyanızı oluşturmanıza yardımcı olacak farklı araçlara ihtiyacınız vardır.

RPG haritası örneğinin tanıtımı burada sona eriyor. Her zaman olduğu gibi örneğin içeriğini uygun gördüğünüz şekilde kullanmakta özgürsünüz. Defold hakkında daha fazla bilgi edinmek için daha çok örnek, öğretici, kılavuz ve API belgesi bulabileceğiniz [belge sayfalarımıza](https://defold.com/learn) göz atın.

Bir sorunla karşılaşırsanız veya sorularınız varsa [forumumuzu ziyaret edin](https://forum.defold.com/).

Defold ile keyifli çalışmalar!
