---
title: Sürüm kontrolü
brief: Bu kılavuz, Defold projelerinde Git kullanımını ve düzenleyicide yerel değişikliklerin incelenmesini ele alır.
---

# Sürüm kontrolü

Defold projeleri [Git](https://git-scm.com) ile iyi çalışır, ancak eşitleme düzenleyicinin dışında yapılır. Klonlamak (clone), uzak değişiklikleri almak (fetch), değişiklikleri çekmek (pull), değişiklik kaydı oluşturmak (commit), değişiklikleri göndermek (push), dallar oluşturmak ve çakışmaları çözmek için tercih ettiğiniz Git istemcisini veya komut satırını kullanın.

## Değişen dosyalar

Proje dizini, en az bir değişiklik kaydı bulunan bir Git çalışma ağacının (working tree) kök dizini olduğunda Defold, yoksayılmayan ve eklendiği, değiştirildiği, silindiği veya yeniden adlandırıldığı tespit edilen dosyaları düzenleyicinin *Changed Files* bölmesinde listeler. Bu girdileri, diskteki dosyaları doğrudan geçerli değişiklik kaydıyla (`HEAD`) karşılaştırarak belirler; bu nedenle bir değişikliği hazırlama alanına eklemek (staging) listeyi değiştirmez. Birleştirme çakışmalarını harici bir Git istemcisinde çözün.

![değişen dosyalar](images/workflow/changed_files.png)

Değiştirilmiş veya yeniden adlandırılmış dosyalardan tam olarak birini seçin ve metin farkını görüntülemek için <kbd>Diff</kbd> düğmesine tıklayın. Seçilen çalışma ağacı ve indeks (index) değişikliklerini iptal etmek için <kbd>Revert</kbd> düğmesine tıklayın. İzlenen dosyalar `HEAD` durumuna geri yüklenir; `HEAD` içinde bulunmayan dosyalar, ekleme olarak hazırlama alanına alınmış olsalar da olmasalar da silinir; yeniden adlandırmalarda ise yeni yol silinir ve eski yol geri yüklenir. Bu işlem düzenleyicide geri alınamaz; bu nedenle ihtiyaç duyabileceğiniz çalışmalar için değişiklik kaydı oluşturun veya bunları yedekleyin.

## Git

Git, Defold'un metin tabanlı proje dosyalarını verimli biçimde saklar. PSD veya ses prodüksiyonu dosyaları gibi sık değişen büyük ikili varlıklar (binary assets), depo geçmişinin yine de hızla büyümesine neden olabilir. Büyük çalışma dosyaları için Git LFS veya ayrı bir depolama ve yedekleme çözümü kullanmayı değerlendirin.

*Changed Files* bölmesi yalnızca yerel durum, fark görüntüleme ve değişiklikleri geri alma işlemlerini sağlar. Değişiklik kayıtlarının uzak bir depoya gönderilip gönderilmediğini bilmez ve fetch, pull, commit veya push işlemlerini yapmaz. Bu işlemleri harici bir Git istemcisinde veya komut satırından gerçekleştirin. Varsayılan olarak Defold, yeniden odak kazandığında harici değişiklikleri yeniden yükler ve bölmeyi yeniler. *Load External Changes on App Focus* devre dışıysa *File ▸ Load External Changes* seçeneğini seçin.
