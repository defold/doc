---
title: Nasıl yardım alınır
brief: Bu kılavuz, Defold kullanırken bir sorunla karşılaşırsanız nasıl yardım alabileceğinizi açıklar.
---

# Yardım alma {#getting-help}

Defold kullanırken bir sorunla karşılaşırsanız, sorunu düzeltebilmemiz ve/veya geçici bir çözüm bulmanıza yardımcı olabilmemiz için bize bildirmenizi isteriz! Sorunları tartışmanın ve bildirmenin birkaç yolu vardır. Size en uygun seçeneği seçin:

## Forumda sorun bildirme

Bir sorunu tartışmanın ve yardım almanın iyi bir yolu, [forumumuzda](https://forum.defold.com) soru sormaktır. Yaşadığınız sorunun türüne göre [Questions](https://forum.defold.com/c/questions) veya [Bugs](https://forum.defold.com/c/bugs) kategorisinde gönderi oluşturun. Sorununuzun çözümü zaten bulunmuş olabileceğinden, soru sormadan önce sorunuz veya sorununuz hakkında [arama yapmayı](https://forum.defold.com/search) unutmayın.

Birden fazla sorunuz varsa ayrı gönderiler oluşturun. Aynı gönderide birbiriyle ilgisiz sorular sormayın.

### Gerekli bilgiler
Gerekli bilgileri sağlamadığınız sürece destek veremeyiz:

**Başlık**
Kısa ve açıklayıcı bir başlık kullanmaya özen gösterin. "Bir oyun nesnesini (game object) dönük olduğu yönde nasıl hareket ettiririm?" veya "Bir sprite bileşenini nasıl yavaşça görünmez hâle getiririm?" iyi başlık örnekleridir. "Defold kullanırken biraz yardıma ihtiyacım var!" veya "Oyunum çalışmıyor!" ise kötü başlık örnekleridir.

**Hatayı açıklayın (ZORUNLU)**
Hatanın ne olduğunu açık ve öz bir şekilde açıklayın.

**Yeniden oluşturma (ZORUNLU)**
Davranışı yeniden oluşturma adımları:
1. '...' konumuna gidin
2. '....' öğesine tıklayın
3. '....' öğesine kadar aşağı kaydırın
4. Hatayı görün

**Beklenen davranış (ZORUNLU)**
Ne olmasını beklediğinizi açık ve öz bir şekilde açıklayın.

**Defold sürümü (ZORUNLU):**
  - Sürüm [ör. 1.2.155]

**Platformlar (ZORUNLU):**
 - Platformlar: [ör. iOS, Android, Windows, macOS, Linux, HTML5]
 - İşletim sistemi: [ör. iOS8.1, Windows 10, High Sierra]
 - Cihaz: [ör. iPhone6]

**Hatayı yeniden oluşturmak için gereken en küçük proje (İSTEĞE BAĞLI):**
Lütfen hatanın yeniden oluştuğu en küçük projeyi ekleyin. Bu, hatayı incelemeye ve düzeltmeye çalışan kişiye büyük ölçüde yardımcı olacaktır.

**Günlükler (İSTEĞE BAĞLI):**
Lütfen motordan, düzenleyiciden veya derleme sunucusundan ilgili günlükleri sağlayın. Günlüklerin nerede saklandığını [buradan](#log-files) öğrenin.

**Geçici çözüm (İSTEĞE BAĞLI):**
Geçici bir çözüm varsa lütfen burada açıklayın.

**Ekran görüntüleri (İSTEĞE BAĞLI):**
Uygunsa, sorununuzu açıklamaya yardımcı olacak ekran görüntüleri ekleyin.

**Ek bilgiler (İSTEĞE BAĞLI):**
Sorunla ilgili diğer bilgileri buraya ekleyin.


### Kod paylaşma
Kod paylaşırken ekran görüntüsü yerine metin olarak paylaşmanız önerilir. Metin olarak paylaşmak, kodda arama yapmayı, hataları işaretlemeyi, değişiklik önermeyi ve uygulamayı kolaylaştırır. Kodu \`\`\` biçimindeki üç ters tırnak arasına alarak veya 4 boşlukla girintileyerek paylaşın.

Örnek:

\`\`\`
print("Hello code!")
\`\`\`

Sonuç:

```
print("Hello code!")
```


## Düzenleyiciden sorun bildirme {#report-a-problem-from-the-editor}

Düzenleyici, sorun bildirmek için pratik bir yol sunar. Bir sorunu bildirmek için düzenleyicide <kbd>Help->Report Issue</kbd> menü seçeneğini seçin.

![](images/getting_help/report_issue.png)

Bu menü seçeneği sizi GitHub'daki bir sorun takip sistemine götürür. [Günlük dosyalarını](#log-files), işletim sisteminizle ilgili bilgileri, sorunu yeniden oluşturma adımlarını, olası geçici çözümleri vb. sağlayın.

::: sidenote
Bu şekilde hata bildirimi göndermek için bir GitHub hesabına ihtiyacınız vardır.
:::


## Discord'da sorun tartışma

Defold kullanırken bir sorunla karşılaşırsanız soruyu [Discord'da](https://www.defold.com/discord/) sormayı deneyebilirsiniz. Ancak karmaşık soruların ve ayrıntılı tartışmaların forumda paylaşılmasını öneririz. Ayrıca Discord üzerinden gönderilen hata bildirimlerini kabul etmediğimizi unutmayın.


# Günlük dosyaları {#log-files}

Motor, düzenleyici ve derleme sunucusu, yardım isterken ve bir hatayı ayıklarken çok değerli olabilecek günlük bilgileri üretir. Bir sorun bildirirken her zaman günlük dosyalarını sağlayın:

* [Motor günlükleri](/manuals/debugging-game-and-system-logs)
* [Düzenleyici günlükleri](/manuals/editor#editor-logs)
* [Derleme sunucusu günlükleri](/manuals/extensions#build-server-logs)
