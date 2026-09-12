---
brief: Defold'a kısa bir giriş. Oyun geliştirme ve Defold maceranıza başlamak için harika bir yer.
github: https://github.com/defold/doc
layout: manual
locale: tr
title: Defold'a giriş
toc:
- Defold'a hoş geldiniz
- Nereden başlamalı?
---

## Defold'a hoş geldiniz

Defold, 2B ve 3B oyun geliştirmek için ücretsiz, hafif ve yüksek performanslı, kullanıma hazır bir çözümdür. Oyun motorunu, düzenleyiciyi ve derleme ekosistemini tek pakette sunarak tasarlamak, geliştirmek ve yayımlamak için ihtiyacınız olan her şeyi sağlar. Desteklenen özelliklerin tam listesini [Ürüne genel bakış](/product) sayfamızda bulabilirsiniz.

Oyun geliştirme sürecinin bazı temel unsurlarını olabildiğince sorunsuz ve zahmetsiz hâle getirmek için çok zaman ve emek harcadık. Bunun Defold'u diğerlerinden ayırdığına inanıyoruz. [Defold'u neden kullanmanız gerektiğini düşündüğümüzü](/why) öğrenin.

## Nereden başlamalı?

[**Öğrenme merkezimiz**](/learn), Defold'a yönelik tüm öğrenme kaynakları için başlangıç noktasıdır. Burada şunları bulabilirsiniz:

- [**Kılavuzlar**](/manuals) (bu kılavuz gibi) - belirli bir konuyu derinlemesine anlamak ve bilginizi genişletmek için
- [**Öğreticiler**](/tutorials) - adım adım yönlendirmeleri izleyerek bir şeyler oluşturmak için
- [**Örnekler**](/examples) - kısa kod parçaları ile basit, küçük, kendi içinde bütünlük taşıyan işlevler ve örnekler
- [**Kurslar**](/courses) - Zenva ve Udemy'deki derslerin yanı sıra topluluğun hazırladığı, daha uzun, kapsamlı ve yapılandırılmış dersler
- [**Videolar**](/videos) - izlemeyi tercih ediyorsanız aralarından seçebileceğiniz çok sayıda video öğretici ve genel bakış videosu
- [**API**](/ref/stable/overview_defoldlua) - güncel ve eksiksiz belgelerimizle sunulan tüm işlevleri ve sabitleri anlamak için
- [**Sık sorulan sorular**](/faq/faq) - en sık sorulan soruların yanıtları; sorununuzun daha önce çözülüp çözülmediğini görmek için arama yapın

Denemeler yapmanızı, öğreticileri izlemenizi, kılavuzlarımızı ve API belgelerimizi okumanızı, soru sormak, diğer kullanıcılardan öğrenmek ve Defold'un gelişimini takip etmek için [topluluk kanallarımıza](/community) katılmanızı öneririz.

Oyun geliştirmeye başlarken veya Defold'u öğrenirken bilmenizde yarar olan bazı noktalar şunlardır:

### Defold düzenleyicisi

[![Düzenleyiciye genel bakış](images/editor/editor_overview.png)](/manuals/editor)

[Düzenleyiciye genel bakış](/manuals/editor/) kılavuzu, düzenleyiciye iyi bir giriş sağlar; arayüzde yolunuzu bulmanıza, görsel araçları kullanmanıza ve kod yazmanıza yardımcı olur. Diğer oyun motorlarının düzenleyicilerine, 3B modelleme programlarına ve programlama için kullanılan tümleşik geliştirme ortamlarına (IDE) aşinaysanız pek fazla sürprizle karşılaşmazsınız. Yine de en sevdiğiniz yazılımdan farklı olan noktalar her zaman olacaktır.

### Defold'un yapı taşları

[![Yapı taşları](images/building_blocks/building_blocks.png)](/manuals/building-blocks)

[Defold'un yapı taşları](/manuals/building-blocks/) kılavuzu, Defold'da oyun geliştirmenin temel kavramlarına harika bir giriş sunar. Defold, oyun geliştirmek için farklı türlerde birden çok bileşen (component) içeren oyun nesneleri (game object) kullanır; bu oyun nesneleri daha sonra koleksiyonlar (collection) hâlinde gruplanır. Daha önce başka motorlar kullandıysanız bunlar size tanıdık gelebilir. Defold'un yapı taşlarını özel kılan bazı mimari tasarım kararları vardır ve bunlarla rahatça çalışmaya alışmak biraz zaman alır. Bu nedenle yapı taşları kılavuzumuz, özellikle sistemin nasıl çalıştığını anlamaya ihtiyaç duyuyorsanız iyi bir başlangıçtır.

### Örnekler

[![Örnekler](images/introduction/examples.png)](/examples)

[Örnekler](/examples/) derlemesi, parçaları bir araya getirerek çalışan bir şey oluşturmayı öğrenmek için iyi bir başlangıçtır. Burada, Defold'da sık karşılaşılan pek çok farklı işlemin nasıl yapılacağını gösteren en küçük örnekleri, kullanabileceğiniz kod parçalarını, yaygın işlevlerin örneklerini ve belirli özellikleri gösteren uygulamaları bulabilirsiniz.

### Öğreticiler

[![Öğreticiler](images/introduction/tutorials.png)](/tutorials)

[Öğreticiler](/tutorials), oyun geliştirmeye başlamak için harikadır. En iyi yaparak öğrendiğinize inanıyoruz. Bu nedenle, çeşitli beceri ve karmaşıklık düzeylerinde bir dizi öğreticiyi doğrudan [düzenleyicide](/manuals/editor/) ve öğrenme merkezimizde sunuyoruz. Düzenleyiciyi başlatın; bir şeyler oluşturmayı ve Defold'un nasıl çalıştığını öğrenmek için adım adım yönergeleri izleyin.

### Lua dili

[![Lua'ya genel bakış](images/introduction/lua.png)](/manuals/lua)

[Lua](/manuals/lua/), Defold'daki tüm mantık denetimi için kullanılan dildir. Motorun iç yapısı C++ ile yazılmış hızlı bir sistemdir, ancak üst düzeyde Lua betikleriyle kontrol edilir. Python, GDScript, GML, JavaScript veya başka bir yüksek düzeyli dilde programlama yaptıysanız Lua'yı oldukça kolay kavrar ve muhtemelen bir öğreticiyi rahatça takip edebilirsiniz. Aksi hâlde Lua kılavuzumuzu okuyarak başlayın ve oradan devam edin.

### Defold forumu

[![Forum](images/introduction/forum.png)](//forum.defold.com/)

[Defold forumu](//forum.defold.com/), çoğu zaman öğrenmenin en iyi yoludur. Başkalarından öğrenebilir, sorunuzun daha önce yanıtlanıp yanıtlanmadığını bulmak için forumda arama yapabilir veya doğrudan sorabilirsiniz. Topluluğumuz çok sıcakkanlı ve yardımseverdir; genel olarak oyun geliştirme, özel olarak da Defold hakkında çok şey bilir. Bir yerde takılırsanız tereddüt etmeyin, yardım almak için foruma gidin!

### Öğrenme merkezi

Defold'u öğrenmek için hangi yolu seçerseniz seçin, başka öğrenme kaynakları bulmak ve Defold'un sunduğu çeşitli özellikler ile kavramlar hakkında derinlemesine açıklamalar içeren kılavuzları okumak için [**Öğrenme merkezimize**](/learn) her zaman dönebileceğinizi unutmayın. Anlamadığınız veya yanlış olduğunu düşündüğünüz noktaları belirtmekten de çekinmeyin. Bu sayfalar sizin için hazırlanıyor ve onları olabildiğince iyi hâle getirmek istiyoruz. Bu nedenle kullanıcıların geri bildirimlerini dikkate alıyor ve öğrenme sürecini mümkün olduğunca sorunsuz kılmak için kaynakları geliştirmeye çalışıyoruz!

Bir sonraki harika oyununuzu Defold'da oluştururken keyif almanızı umuyoruz!
