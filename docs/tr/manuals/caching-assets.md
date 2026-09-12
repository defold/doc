---
title: Varlıkları önbelleğe alma
brief: Bu kılavuz, proje derlemelerini hızlandırmak için varlık önbelleğinin nasıl kullanılacağını açıklar.
---

# Varlıkları önbelleğe alma

Defold ile oluşturulan oyunlar genellikle saniyeler içinde derlenir, ancak proje büyüdükçe varlıkların (asset) sayısı da artar. Büyük bir projede yazı tiplerini derlemek ve dokuları sıkıştırmak önemli ölçüde zaman alabilir. Varlık önbelleği (asset cache), yalnızca değişen varlıkları yeniden derleyerek ve değişmeyen varlıklar için önbellekteki önceden derlenmiş varlıkları kullanarak proje derlemelerini hızlandırır.

Defold üç katmanlı bir önbellek kullanır:

1. Proje önbelleği
2. Yerel önbellek
3. Uzak önbellek


## Proje önbelleği

Defold varsayılan olarak derlenmiş varlıkları Defold projesinin `build/default` klasöründe önbelleğe alır. Proje önbelleği (project cache), yalnızca değiştirilen varlıkların yeniden derlenmesi gerektiği ve değişmeyen varlıklar proje önbelleğinden kullanıldığı için sonraki proje derlemelerini hızlandırır. Bu önbellek her zaman etkindir ve hem düzenleyici hem de komut satırı araçları tarafından kullanılır.

Proje önbelleğini, `build/default` içindeki dosyaları silerek veya [komut satırı derleme aracı Bob](/manuals/bob) ile `clean` komutunu çalıştırarak elle silebilirsiniz.


## Yerel önbellek

Yerel önbellek (local cache), derlenmiş varlıkların aynı makinede veya bir ağ sürücüsünde, proje dışındaki bir dosya konumunda saklandığı isteğe bağlı ikinci bir önbellektir. Bu dış konum sayesinde proje önbelleği temizlendiğinde yerel önbelleğin içeriği korunur. Ayrıca aynı proje üzerinde çalışan birden fazla geliştirici tarafından paylaşılabilir. Bu önbellek şu anda yalnızca komut satırı araçlarıyla proje derlerken kullanılabilir. `resource-cache-local` seçeneğiyle etkinleştirilir:

```sh
java -jar bob.jar --resource-cache-local /Users/john.doe/defold_local_cache
```

Yerel önbellekteki derlenmiş varlıklara, Defold motorunun sürümünü, kaynak varlıkların adlarını ve içeriklerini, ayrıca proje derleme seçeneklerini dikkate alarak hesaplanan bir sağlama toplamına (checksum) göre erişilir. Bu, önbelleğe alınan varlıkların benzersiz olmasını ve önbelleğin birden fazla Defold sürümü arasında paylaşılabilmesini garanti eder.

::: sidenote
Yerel önbellekteki dosyalar süresiz olarak saklanır. Eski/kullanılmayan dosyaları elle kaldırmak geliştiricinin sorumluluğundadır.
:::


## Uzak önbellek

Uzak önbellek (remote cache), derlenmiş varlıkların bir sunucuda saklandığı ve HTTP istekleriyle erişildiği isteğe bağlı üçüncü bir önbellektir. Bu önbellek şu anda yalnızca komut satırı araçlarıyla proje derlerken kullanılabilir. `resource-cache-remote` seçeneğiyle etkinleştirilir:

```sh
java -jar bob.jar --resource-cache-remote http://192.168.0.100/
```

Yerel önbellekte olduğu gibi, uzak önbellekteki tüm varlıklara hesaplanan bir sağlama toplamına göre erişilir. Önbelleğe alınan varlıklara GET, PUT ve HEAD HTTP istek yöntemleriyle erişilir. Defold uzak önbellek sunucusu sağlamaz. Bunu kurmak her geliştiricinin kendi sorumluluğundadır. [Basit bir Python sunucusu örneğini burada görebilirsiniz](https://github.com/britzl/httpserver-python).
