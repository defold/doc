---
title: Defold projelerinde dosyaları yok sayma
brief: Bu kılavuz, Defold'da dosyaların ve klasörlerin nasıl yok sayılacağını açıklar.
---

# Dosyaları yok sayma

Defold düzenleyicisini ve araçlarını, bir projedeki dosyaları ve klasörleri yok sayacak şekilde yapılandırabilirsiniz. Bu, projede uzantıları Defold'un kullandığı dosya uzantılarıyla çakışan dosyalar varsa yararlı olabilir. Bunun bir örneği, düzenleyicinin oyun nesnesi (game object) dosyaları için kullandığı `.go` uzantısıyla aynı uzantıya sahip olan Go dili dosyalarıdır.

## `.defignore` dosyası
Hariç tutulacak dosyalar ve klasörler, projenin kök dizinindeki `.defignore` adlı dosyada tanımlanır. Bu dosyada, hariç tutulacak dosyalar ve klasörler her satırda bir tane olacak şekilde listelenmelidir. Örnek:

```
/path/to/file.png
/otherpath
```

Bu, `/path/to/file.png` dosyasını ve `/otherpath` yolundaki her şeyi hariç tutar.

## `.defunload` dosyası

Birden çok bağımsız modül içeren bazı büyük projelerde, düzenleyicideki bellek kullanımını ve yükleme sürelerini azaltmak için projenin bazı bölümlerini yükleme dışında tutmak isteyebilirsiniz. Bunu yapmak için yükleme dışında tutulacak yolları proje dizini altındaki bir `.defunload` dosyasında listeleyebilirsiniz.

Basitçe ifade etmek gerekirse, `.defunload` dosyası projenin bazı bölümlerini düzenleyiciden gizlemenizi sağlar; gizlenen kaynaklara (resource) başvurmak derleme hatasına yol açmaz.

`.defunload` içindeki kalıplar, `.defignore` dosyasıyla aynı kuralları kullanır. Yüklenmemiş koleksiyonlar (collection) ve oyun nesneleri, yüklenmiş kaynaklar bunlara başvurduğunda boşmuş gibi davranır. `.defunload` kalıplarıyla eşleşen diğer kaynaklar yüklenmemiş durumda kalır ve düzenleyicide görüntülenemez. Ancak yüklenmiş bir kaynak bunlara bağımlıysa, yüklenmemiş kaynaklar ve bunların bağımlılıkları otomatik olarak yüklenir.

Örneğin, bir sprite bileşeni bir atlastaki görüntülere bağımlıysa atlası yüklememiz gerekir; aksi takdirde eksik görüntü bir hata olarak bildirilir. Bu olursa bir bildirim, kullanıcıyı durum hakkında uyarır ve yüklenmemiş hangi kaynağa nereden başvurulduğu hakkında bilgi verir.

Düzenleyici, kullanıcının yüklenmiş kaynaklardan `.defunloaded` kaynaklara başvuru eklemesini engeller; dolayısıyla bu durum yalnızca kaynaklar diskten okunduğunda ortaya çıkar.

`.defignore` dosyasından farklı olarak, `.defunload` dosyasını düzenledikten sonra değişikliklerin uygulanması için düzenleyiciyi yeniden başlatmanız gerekir.
