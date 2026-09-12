---
title: Defold'un tasarımı
brief: Defold'un tasarımının ardındaki felsefe
---

# Defold'un tasarımı

Defold şu hedeflerle oluşturuldu:

- Oyun ekipleri için eksiksiz, profesyonel ve kullanıma hazır bir üretim platformu olmak.
- Oyun geliştirmede sık karşılaşılan mimari ve iş akışı sorunlarına açık çözümler sunarak sade ve anlaşılır olmak.
- Yinelemeli oyun geliştirme için ideal, son derece hızlı bir geliştirme platformu olmak.
- Çalışma sırasında yüksek performans sunmak.
- Gerçek anlamda birden çok platformu desteklemek.

Düzenleyici ve motorun tasarımı bu hedeflere ulaşmak için özenle hazırlanmıştır. Tasarım kararlarımızdan bazıları, başka platformlarda deneyiminiz varsa alışık olabileceğiniz yaklaşımlardan farklıdır. Örneğin:

- Kaynak ağacının (resource tree) ve tüm adlandırmaların statik olarak bildirilmesini zorunlu tutuyoruz. Bu, başlangıçta biraz çaba göstermenizi gerektirir, ancak uzun vadede geliştirme sürecine büyük katkı sağlar.
- Basit ve kapsüllenmiş birimler arasında ileti aktarımını (message passing) teşvik ediyoruz.
- Nesne yönelimli kalıtım yoktur.
- API'lerimiz eşzamansızdır.
- Görüntü oluşturmayı sağlayan işleme hattı (rendering pipeline) kodla yönetilir ve tamamen özelleştirilebilir.
- Tüm kaynak dosyalarımız basit düz metin biçimlerindedir; hem Git birleştirmeleri hem de harici araçlarla içe aktarma ve işleme için en uygun şekilde yapılandırılmıştır.
- Kaynaklar değiştirilebilir ve oyun çalışırken yeniden yüklenebilir (hot reload); bu da son derece hızlı yineleme ve denemeler yapmayı sağlar.
