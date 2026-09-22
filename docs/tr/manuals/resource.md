---
title: Defold kaynak yönetimi
brief: Bu kılavuz, Defold'un kaynakları otomatik olarak nasıl yönettiğini ve bellekte kaplanan alan ile dağıtım paketi boyutu kısıtlamalarına uymak için kaynakların yüklenmesini elle nasıl yönetebileceğinizi açıklar.
---

# Kaynak yönetimi

Çok küçük bir oyun yapıyorsanız hedef platformun kısıtlamaları (bellekte kaplanan alan, dağıtım paketi boyutu, işlem gücü ve pil tüketimi) hiçbir zaman sorun oluşturmayabilir. Ancak daha büyük oyunlar yaparken, özellikle de elde taşınan cihazlarda, bellek tüketimi büyük olasılıkla en önemli kısıtlamalardan biri olacaktır. Deneyimli bir ekip, platform kısıtlamalarına göre kaynak (resource) bütçelerini özenle belirler. Defold, belleği ve dağıtım paketi boyutunu yönetmeye yardımcı olan çeşitli özellikler sunar. Bu kılavuz, bu özelliklere genel bir bakış sunar.

## Statik kaynak ağacı

Defold'da bir oyunu derlerken kaynak ağacını (resource tree) statik olarak tanımlarsınız. Oyunun her bir parçası, genellikle "main.collection" olarak adlandırılan başlangıç koleksiyonundan (bootstrap collection) başlayarak ağaca bağlanır. Kaynak ağacı her başvuruyu izler ve bu başvurularla ilişkili tüm kaynakları içerir:

- Oyun nesnesi (game object) ve bileşen (component) verileri (atlaslar, sesler vb.).
- Fabrika (factory) bileşeni prototipleri (oyun nesneleri ve koleksiyonlar).
- Koleksiyon vekili (collection proxy) bileşeni başvuruları (koleksiyonlar).
- *game.project* dosyasında tanımlanan [özel kaynaklar](/manuals/project-settings/#custom-resources).

![Kaynak ağacı](images/resource/resource_tree.png)

::: sidenote
Defold'da [dağıtım paketine eklenen kaynaklar](/manuals/project-settings/#bundle-resources) kavramı da vardır. Bu kaynaklar uygulamanın dağıtım paketine dahil edilir, ancak kaynak ağacının bir parçası değildir. Dağıtım paketine eklenen kaynaklar, platforma özgü destek dosyalarından [dosya sisteminden yüklenen](/manuals/file-access/#how-to-access-files-bundled-with-the-application) ve oyununuzun kullandığı harici dosyalara (örneğin FMOD ses bankaları) kadar her tür dosya olabilir.
:::

Oyun *paketlendiğinde* yalnızca kaynak ağacında bulunanlar pakete dahil edilir. Ağaçta başvurulmayan hiçbir şey pakete eklenmez. Dağıtım paketine nelerin dahil edileceğini veya paketten nelerin hariç tutulacağını elle seçmeniz gerekmez.

Oyun *çalıştırıldığında* motor, ağacın başlangıç koleksiyonunun bulunduğu kökünden başlayarak kaynakları belleğe yükler:

- Başvurulan her koleksiyon ve içeriği.
- Oyun nesneleri ve bileşen verileri.
- Fabrika bileşeni prototipleri (oyun nesneleri ve koleksiyonlar).

Ancak motor, başvurulan kaynakların aşağıdaki türlerini çalışma sırasında otomatik olarak yüklemez:

- Koleksiyon vekilleri aracılığıyla başvurulan oyun dünyası koleksiyonları. Oyun dünyaları nispeten büyüktür; bu nedenle bunların yüklenmesini ve bellekten kaldırılmasını kodda elle tetiklemeniz gerekir. Ayrıntılar için [Koleksiyon vekili kılavuzuna](/manuals/collection-proxy) bakın.
- *game.project* dosyasındaki *Custom Resources* ayarıyla eklenen dosyalar. Bu dosyalar, [`sys.load_resource()`](/ref/sys/#sys.load_resource) işleviyle elle yüklenir.

Defold'un kaynakları varsayılan paketleme ve yükleme biçimi, kaynakların belleğe nasıl ve ne zaman yüklendiği üzerinde ayrıntılı denetim sağlamak için değiştirilebilir.

![Kaynak yükleme](images/resource/loading.png)

## Fabrika kaynaklarını dinamik olarak yükleme

Fabrika bileşenlerinin başvurduğu kaynaklar normalde bileşen yüklendiğinde belleğe yüklenir. Böylece kaynaklar, fabrika çalışma zamanı ortamında var olur olmaz oyunda nesne oluşturmak için hazır olur. Varsayılan davranışı değiştirmek ve fabrika kaynaklarının yüklenmesini ertelemek için fabrikanın *Load Dynamically* onay kutusunu işaretlemeniz yeterlidir.

![Dinamik yükleme](images/resource/load_dynamically.png)

Bu kutu işaretliyken motor, başvurulan kaynakları oyunun dağıtım paketine dahil etmeye devam eder, ancak fabrika kaynaklarını otomatik olarak yüklemez. Bunun yerine iki seçeneğiniz vardır:

1. Nesne oluşturmak istediğinizde [`factory.create()`](/ref/factory/#factory.create) veya [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create) işlevini çağırın. Bu işlem, kaynakları eşzamanlı olarak yükler, ardından yeni örnekler oluşturur.
2. Kaynakları eşzamansız olarak yüklemek için [`factory.load()`](/ref/factory/#factory.load) veya [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load) işlevini çağırın. Kaynaklar nesne oluşturmak için hazır olduğunda bir geri çağırım (callback) alınır.

Bunun nasıl çalıştığıyla ilgili ayrıntılar için [Fabrika kılavuzunu](/manuals/factory) ve [Koleksiyon fabrikası (collection factory) kılavuzunu](/manuals/collection-factory) okuyun.

## Dinamik olarak yüklenen kaynakları bellekten kaldırma

Defold, tüm kaynaklar için başvuru sayaçları tutar. Bir kaynağın sayacı sıfıra ulaşırsa bu, artık hiçbir şeyin o kaynağa başvurmadığı anlamına gelir. Kaynak daha sonra otomatik olarak bellekten kaldırılır. Örneğin, bir fabrikanın oluşturduğu tüm nesneleri ve fabrika bileşenini barındıran nesneyi silerseniz fabrikanın daha önce başvurduğu kaynaklar bellekten kaldırılır.

*Load Dynamically* seçeneği işaretli fabrikalar için [`factory.unload()`](/ref/factory/#factory.unload) veya [`collectionfactory.unload()`](/ref/collectionfactory/#collectionfactory.unload) işlevini çağırabilirsiniz. Bu çağrı, fabrika bileşeninin kaynağa olan başvurusunu kaldırır. Kaynağa başka hiçbir şey başvurmuyorsa (örneğin oluşturulan tüm nesneler silinmişse) kaynak bellekten kaldırılır.

## Kaynakları dağıtım paketinden hariç tutma

Koleksiyon vekilleriyle, bileşenin başvurduğu tüm kaynakları paketleme işleminin dışında tutmak mümkündür. Bu, dağıtım paketi boyutunu en düşük düzeyde tutmanız gerektiğinde yararlıdır. Örneğin, oyunları web üzerinde HTML5 olarak çalıştırırken tarayıcı oyunu yürütmeden önce dağıtım paketinin tamamını indirir.

![Hariç tutma](images/resource/exclude.png)

Bir koleksiyon vekilinde *Exclude* seçeneğini işaretlediğinizde başvurulan kaynak oyunun dağıtım paketinin dışında tutulur. Bunun yerine, hariç tutulan koleksiyonları seçtiğiniz bir bulut depolama hizmetinde saklayabilirsiniz. [Live Update kılavuzu](/manuals/live-update/) bu özelliğin nasıl çalıştığını açıklar.
