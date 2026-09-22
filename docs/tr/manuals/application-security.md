---
title: Uygulama güvenliği kılavuzu
brief: Bu kılavuzda güvenli geliştirme uygulamalarıyla ilgili çeşitli alanlar ele alınır.
---

# Uygulama güvenliği

Uygulama güvenliği, güvenli geliştirme uygulamalarından oyun yayımlandıktan sonra içeriğinin korunmasına kadar pek çok konuyu kapsayan geniş bir alandır. Bu kılavuzda çeşitli alanlar, Defold motoru, araçları ve hizmetleri kullanılırken uygulama güvenliği bağlamında ele alınır:

* Fikrî mülkiyetin korunması
* Hile önleme çözümleri
* Güvenli ağ iletişimi
* Üçüncü taraf yazılımların kullanımı
* Bulut derleme sunucularının kullanımı
* İndirilebilir içerik


## Fikrî mülkiyetinizi hırsızlığa karşı koruma
Çoğu geliştirici, ürettiklerini hırsızlığa karşı nasıl koruyacağını düşünür. Telif hakları, patentler ve ticari markalar, video oyunlarının fikrî mülkiyetinin farklı yönlerini hukuken korumak için kullanılabilir. Telif hakkı, sahibine yaratıcı eseri dağıtma konusunda münhasır hak tanır; patentler buluşları, ticari markalar ise adları, simgeleri ve logoları korur.

Bir oyunu oluşturan yaratıcı çalışmayı korumak için teknik önlemler almak da istenebilir. Ancak oyun oyuncunun eline geçtiğinde varlıkları (asset) çıkarmanın yollarının bulunabileceğini akılda tutmak önemlidir. Bu, oyun uygulamasına ve dosyalarına tersine mühendislik uygulanarak yapılabileceği gibi, dokular ve modeller GPU birimine gönderilirken veya diğer varlıklar belleğe yüklenirken bunları çıkaran araçlar kullanılarak da yapılabilir.

Bu nedenle genel görüşümüz, kullanıcılar bir oyunun varlıklarını çıkarmaya kararlıysa bunu yapabilecekleri yönündedir.

Geliştiriciler kendi koruma önlemlerini ekleyerek varlıkların çıkarılmasını zorlaştırabilir, __ancak imkânsız hâle getiremezler__. Bu genellikle oyun varlıklarını korumak ve gizlemek için çeşitli şifreleme ve karartma (obfuscation) yöntemlerini içerir.

### Kaynak kodunu karartma
Kaynak kodunu karartma, programın çıktısını etkilemeden kaynak kodun insanlar tarafından anlaşılmasını kasıtlı olarak zorlaştıran otomatik bir işlemdir. Amaç genellikle hırsızlığa karşı koruma sağlamak, bunun yanında hile yapmayı da zorlaştırmaktır.

Defold'da kaynak kodunu karartma işlemi, derleme öncesi bir adım olarak veya Defold proje derleme sürecinin bir parçası olarak uygulanabilir. Derleme öncesi karartmada, Defold proje derleme süreci başlatılmadan önce kaynak kod bir karartma aracı kullanılarak karartılır.

Derleme sırasındaki karartma ise bir Lua derleme eklentisi (Lua builder plugin) kullanılarak derleme sürecine dahil edilir. Lua derleme eklentisi, ham kaynak kodu girdi olarak alır ve kaynak kodun karartılmış bir sürümünü çıktı olarak döndürür. Derleme sırasında karartmaya bir örnek, GitHub'da bulunan Prometheus Lua karartıcısını temel alan [Prometheus eklentisinde](https://github.com/defold/extension-prometheus) gösterilmiştir. Aşağıda, bir kod parçasını yoğun biçimde karartmak için Prometheus kullanımının bir örneği verilmiştir (bu tür yoğun karartmanın Lua kodunun çalışma zamanı performansını etkileyeceğini unutmayın):

Örnek:

```
function init(self)
 print("hello")
 test.greet("Bob")
end
```

Karartılmış çıktı:

```
local v={"+qdW","ZK0tEKf=";"XP/IX3+="}for o,J in ipairs({{1;3};{1,1},{2,3}})do while J[1]<J[2]do v[J[1]],v[J[2]],J[1],J[2]=v[J[2]],v[J[1]],J[1]+1,J[2]-1 end end local function J(o)return v[o+45816]end do local o={["/"]=9;["8"]=48;["9"]=1;q=38,o=62;V=33;y=43,d=61,B=50,L=54;v=2;["0"]=21,n=31;p=63;R=5;N=3;i=10;e=35;C=7;l=56;a=47,J=58;m=59;["2"]=36;z=11;M=12;Z=26;O=18;["5"]=20;s=8,["4"]=30,P=55;w=4;U=29;Q=28;r=24,h=41;G=45;c=19;W=34,k=57;T=14,t=44,S=0;f=60;F=42,E=27;u=40;X=25,j=17;["3"]=23,b=13;["1"]=53;Y=32,A=22,K=6,["+"]=16,["6"]=46;["7"]=51;I=37;D=52;H=15,x=49,g=39}local J=type local x=string.sub local d=v local l=string.len local W=string.char local L=table.insert local w=table.concat local h=math.floor for v=1,#d,1 do local X=d[v]if J(X)=="string"then local J=l(X)local H={}local S=1 local k=0 local K=0 while S<=J do local v=x(X,S,S)local d=o[v]if d then k=k+d*64^(3-K)K=K+1 if K==4 then K=0 local o=h(k/65536)local v=h((k%65536)/256)local J=k%256 L(H,W(o,v,J))k=0 end elseif v=="="then L(H,W(h(k/65536)))if S>=J or x(X,S+1,S+1)~="="then L(H,W(h((k%65536)/256)))end break end S=S+1 end d[v]=w(H)end end end local function o(o)test[J(-45815)](o)end function init(v)print(J(-45813))o(J(-45814))end
```

### Kaynakları şifreleme
Defold proje derleme sürecinde oyun kaynakları (resource) işlenir ve Defold motorunun çalışma sırasında kullanımına uygun biçimlere dönüştürülür. Dokular Basis Universal biçimine derlenir; koleksiyonlar (collection), oyun nesneleri (game object) ve bileşenler (component), insanların okuyabildiği metin gösterimlerinden ikili karşılıklarına dönüştürülür; Lua kaynak kodu ise işlenip bayt koduna derlenir. Ses dosyaları gibi diğer varlıklar olduğu gibi kullanılır.

Bu işlem tamamlandığında varlıklar oyun arşivine tek tek eklenir. Oyun arşivi büyük bir ikili dosyadır ve her kaynağın arşiv içindeki konumu bir arşiv dizini dosyasında saklanır. Biçim [burada](https://github.com/defold/defold/blob/dev/engine/docs/ARCHIVE_FORMAT.md) belgelenmiştir.

Lua kaynak dosyaları, arşive eklenmeden önce isteğe bağlı olarak ayrıca şifrelenir. Defold'da sağlanan varsayılan şifreleme, oyun arşivi bir ikili dosya görüntüleme aracıyla incelendiğinde koddaki dizelerin hemen görünmesini önlemek için kullanılan basit bir blok şifrelemedir. Defold kaynak kodu, şifreleme anahtarı da kaynak kodda görülebilecek şekilde GitHub'da bulunduğundan bu şifreleme kriptografik açıdan güvenli kabul edilmemelidir.

Bir kaynak şifreleme eklentisi (Resource encryption plugin) uygulayarak Lua kaynak dosyalarına özel şifreleme eklemek mümkündür. Kaynak şifreleme eklentisi, derleme sürecinin bir parçası olarak kaynakları şifreleyen bir derleme bölümü ile kaynaklar oyun arşivinden okunurken şifrelerini çözen bir çalışma zamanı bölümünden oluşur. Kendi şifreleme çözümünüz için başlangıç noktası olarak kullanabileceğiniz temel bir kaynak şifreleme eklentisi [GitHub'da mevcuttur](https://github.com/defold/extension-resource-encryption).


### Proje yapılandırma değerlerini kodlama
*game.project* dosyası, uygulamanızın dağıtım paketine olduğu gibi eklenir. Bazen hassas nitelikte olan ancak gizli olmayabilecek, herkese açık API erişim anahtarlarını veya benzer değerleri saklamak isteyebilirsiniz. Bu tür değerlerin güvenliğini artırmak için onları *game.project* dosyasında saklamak yerine uygulamanın ikili dosyasına ekleyebilir ve yine de `sys.get_config_string()` gibi Defold API işlevlerinden erişilebilir tutabilirsiniz. Bunun için *game.project* dosyanıza bir yerel kod eklentisi (native extension) ekleyebilir ve `DM_DECLARE_CONFIGFILE_EXTENSION` makrosunu kullanarak Defold API işlevleriyle yapılandırma değerleri alınırken varsayılan davranışı kendi kodunuzla geçersiz kılabilirsiniz. Başlangıç noktası olarak kullanabileceğiniz bir örnek proje [GitHub'da mevcuttur](https://github.com/defold/example-configfile-extension/tree/master).


## Oyununuzu hilecilere karşı koruma
Video oyunlarında hile, oyun sektörü kadar eskidir. Eskiden popüler video oyunu dergilerinde hile kodları paylaşılır, ilk ev bilgisayarları için özel hile kartuşları satılırdı. Sektör ve oyunlar geliştikçe hileciler ve yöntemleri de gelişti. Oyunlarda en yaygın hile yöntemlerinden bazıları şunlardır:

* Özel mantık eklemek için oyun içeriğini yeniden paketleme
* Oyunun normalden daha hızlı veya daha yavaş çalışmasını sağlayan hız hileleri
* Otomatik nişan alma ve botlar için otomasyon ve görsel analiz
* Puanları, canları, cephaneyi vb. değiştirmek için kod ve bellek enjeksiyonu

Hilecilere karşı korunmak zordur, neredeyse imkânsızdır. Oyunların uzak sunucularda çalıştırılıp doğrudan kullanıcının cihazına akışla aktarıldığı bulut oyun hizmetleri bile hilecilerden tamamen arınmış değildir.

Defold, motorda veya araçlarda herhangi bir hile önleme çözümü sağlamaz ve bu tür çalışmaları oyunlar için hile önleme çözümleri sunma konusunda uzmanlaşmış çok sayıdaki şirketten birine bırakır.


## Ağ iletişiminizi güvenli hâle getirme
Defold soket ve HTTP iletişimi, güvenli soket bağlantılarını destekler. Sunucunun kimliğini doğrulamak ve istemciden sunucuya ve ters yönde aktarılırken tüm verilerin gizliliğini ve bütünlüğünü korumak için her türlü sunucu iletişiminde güvenli bağlantılar kullanmanız önerilir. Defold, TLS ve SSL protokollerinin popüler ve yaygın olarak benimsenmiş açık kaynaklı [Mbed TLS](https://github.com/Mbed-TLS/mbedtls) uygulamasını kullanır. Mbed TLS, ARM ve teknoloji ortakları tarafından geliştirilmektedir.

### SSL sertifikası doğrulama
Ağ iletişiminize yönelik ortadaki adam (man in the middle) saldırılarını önlemek için bir sunucuyla bağlantı kurulurken SSL el sıkışması sırasında sertifika zincirini doğrulamak mümkündür. Bunun için Defold'daki ağ istemcisine açık anahtarların bir listesi sağlanabilir. Ağ iletişiminizi güvenli hâle getirme hakkında daha fazla bilgi için [ağ kılavuzundaki](https://defold.com/manuals/networking/#secure-connections) SSL doğrulama bölümünü okuyun.


## Üçüncü taraf yazılımları güvenli kullanma
Bir oyun oluşturmak için üçüncü taraf kütüphaneler veya yerel kod eklentileri kullanmak zorunlu olmasa da geliştirmeyi hızlandırmak için resmî [Asset Portal](https://defold.com/assets/) üzerinden varlık kullanmak geliştiriciler arasında çok yaygın bir uygulama hâline gelmiştir. Asset Portal, üçüncü taraf SDK tümleştirmelerinden ekran yöneticilerine, kullanıcı arayüzü kütüphanelerine, kameralara ve çok daha fazlasına kadar geniş bir varlık yelpazesi içerir.

Asset Portal'daki varlıkların hiçbiri Defold Foundation tarafından incelenmemiştir ve Asset Portal üzerinden edinilen herhangi bir varlığın kullanımı sonucunda bilgisayar sisteminizde veya başka bir cihazınızda meydana gelebilecek hasardan ya da veri kaybından sorumlu değiliz. Ayrıntılı hükümleri [Hüküm ve Koşullarımızda](https://defold.com/terms-and-conditions/#3-no-warranties) okuyabilirsiniz.

Her varlığı kullanmadan önce incelemenizi ve projenizde kullanıma uygun olduğuna karar verdikten sonra siz fark etmeden değişmemesini sağlamak için varlığı çatallamanızı (fork) veya bir kopyasını oluşturmanızı öneririz.


## Bulut derleme sunucularını güvenli kullanma
Defold bulut derleme sunucuları (extender sunucuları olarak da bilinir), geliştiricilerin motorun kendisini yeniden derlemesi gerekmeden Defold motoruna yeni işlevler eklemesine yardımcı olmak için oluşturulmuştur. Yerel kod içeren bir Defold projesi ilk kez derlendiğinde yerel kod ve ilişkili tüm kaynaklar bulut derleme sunucularına gönderilir; burada Defold motorunun özel bir sürümü oluşturulur ve geliştiriciye geri gönderilir. Kullanılmayan bileşenleri motordan çıkarmak için özel bir uygulama bildirimi (application manifest) kullanılarak proje derlendiğinde de aynı süreç uygulanır.

Bulut derleme sunucuları AWS üzerinde barındırılır ve en iyi güvenlik uygulamalarına göre oluşturulmuştur. Ancak Defold Foundation, bulut derleme sunucularının gereksinimlerinizi karşılayacağını, kusur veya virüs içermeyeceğini, güvenli ya da hatasız olacağını veya sunucuları kullanımınızın kesintisiz ya da güvenli olacağını garanti etmez. Ayrıntılı hükümleri [Hüküm ve Koşullarımızda](https://defold.com/terms-and-conditions/#3-no-warranties) okuyabilirsiniz.

Derleme sunucularının güvenliği ve kullanılabilirliği sizin için endişe kaynağıysa kendi özel derleme sunucularınızı kurmanızı öneririz. Kendi sunucunuzu nasıl kuracağınıza ilişkin yönergeler, GitHub'daki extender deposunun [ana readme dosyasında](https://github.com/defold/extender) bulunabilir.


## İndirilebilir içeriğinizi güvenli hâle getirme
Defold Live Update sistemi, geliştiricilerin içeriği daha sonra indirmek ve kullanmak üzere ana oyun dağıtım paketinin dışında bırakmasına olanak tanır. Tipik bir kullanım, oyuncu oyunda ilerledikçe ek bölümlerin, haritaların veya dünyaların indirilmesidir.

Paket dışında bırakılan içerik indirilip oyunda kullanıma hazırlandığında, kullanılmadan önce motor tarafından doğrulanır. Doğrulama, çeşitli kontrollerden oluşur:

* İkili biçim doğru mu?
* İndirilen içerik, o anda çalışan motor sürümü tarafından destekleniyor mu?
* İndirilen içerik tam mı ve tüm dosyalar mevcut mu?

Bu süreç hakkında daha fazla bilgiyi [Live Update kılavuzunda](https://defold.com/manuals/live-update/#content-verification) bulabilirsiniz.
