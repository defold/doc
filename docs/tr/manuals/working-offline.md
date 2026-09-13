---
title: Çevrimdışı çalışma
brief: Bu kılavuz, bağımlılıklar ve özellikle yerel kod eklentileri içeren projelerde çevrimdışı nasıl çalışılacağını açıklar
---

# Çevrimdışı çalışma

Defold çoğu durumda çalışmak için internet bağlantısı gerektirmez. Ancak internet bağlantısının gerektiği birkaç durum vardır:

* Otomatik güncellemeler
* Sorun bildirme
* Bağımlılıkları alma
* Yerel kod eklentilerini derleme


## Otomatik güncellemeler

Defold, yeni güncellemelerin olup olmadığını düzenli aralıklarla denetler. Defold güncelleme denetimleri [resmî indirme sitesi](https://d.defold.com) üzerinden yapılır. Bir güncelleme bulunursa otomatik olarak indirilir.

İnternet bağlantısına yalnızca sınırlı sürelerle erişebiliyorsanız ve otomatik güncellemenin başlamasını beklemek istemiyorsanız, Defold'un yeni sürümlerini [resmî indirme sitesinden](https://d.defold.com) elle indirebilirsiniz.


## Sorun bildirme

Düzenleyicide bir sorun algılanırsa sorunu Defold sorun takip sistemine bildirme seçeneği sunulur. Sorun takip sistemi [GitHub'da barındırıldığından](https://www.github.com/defold/editor2-issues) sorunu bildirmek için internet bağlantısı gerekir.

Çevrimdışıyken bir sorunla karşılaşırsanız, daha sonra düzenleyicinin [Help menüsündeki Report Issue seçeneğini](/manuals/getting-help/#report-a-problem-from-the-editor) kullanarak sorunu elle bildirebilirsiniz.


## Bağımlılıkları alma

Defold, geliştiricilerin [kütüphane projeleri (Library Projects)](/manuals/libraries/) adı verilen bir sistem aracılığıyla kod ve varlık paylaşmasını destekler. Kütüphaneler, internette herhangi bir yerde barındırılabilen zip dosyalarıdır. Defold kütüphane projelerini genellikle GitHub'da ve diğer çevrimiçi kaynak kod depolarında bulabilirsiniz.

Bir projeye, [proje ayarlarında proje bağımlılığı olarak](/manuals/project-settings/#dependencies) bir kütüphane eklenebilir. Bağımlılıklar, proje açıldığında veya *Project* menüsünden *Fetch Libraries* seçeneği seçildiğinde indirilir/güncellenir.

Çevrimdışı olarak birden fazla projede çalışmanız gerekiyorsa, bağımlılıkları önceden indirip yerel bir sunucu aracılığıyla paylaşabilirsiniz. GitHub'daki bağımlılıklar genellikle proje deposunun Releases sekmesinde bulunur:

![GitHub kütüphane URL adresi](images/libraries/libraries_library_url_github.png)

Python kullanarak kolayca yerel bir sunucu oluşturabilirsiniz:

    python -m SimpleHTTPServer

Bu komut, geçerli dizinde `localhost:8000` adresi üzerinden dosya sunan bir sunucu oluşturur. Geçerli dizin indirilmiş bağımlılıklar içeriyorsa, bunları *game.project* dosyanıza ekleyebilirsiniz:

    http://localhost:8000/extension-fbinstant-4.1.1.zip


## Yerel kod eklentilerini derleme

Defold, geliştiricilerin [yerel kod eklentileri (Native Extensions)](/manuals/extensions/) adı verilen bir sistem aracılığıyla motorun işlevlerini genişletmek için yerel kod eklemesini destekler. Defold, bulut tabanlı bir derleme çözümüyle yerel kod eklentilerini hiçbir kurulum gerektirmeden kullanmaya başlamanızı sağlar.

Yerel kod eklentisi içeren bir projeyi ilk kez derlediğinizde, yerel kod Defold derleme sunucularında özel bir Defold oyun motoruna derlenir ve bilgisayarınıza geri gönderilir. Özel motor projenizde önbelleğe alınır ve herhangi bir yerel kod eklentisi eklemediğiniz, kaldırmadığınız veya değiştirmediğiniz ve düzenleyiciyi güncellemediğiniz sürece sonraki derlemelerde yeniden kullanılır.

Çevrimdışı çalışmanız gerekiyorsa ve projeniz yerel kod eklentileri içeriyorsa, projenizin özel motorun önbelleğe alınmış bir kopyasını içermesi için en az bir kez başarıyla derlendiğinden emin olmanız gerekir.
