---
title: Yeniden düzenleme
brief: Bu kılavuz, güçlü yeniden düzenleme desteğiyle projenizin yapısını nasıl kolayca değiştirebileceğinizi açıklar.
---

# Yeniden düzenleme

Yeniden düzenleme (refactoring), mevcut kodun ve varlıkların (asset) yapısını değiştirme sürecidir. Bir proje geliştirilirken öğeleri değiştirme veya taşıma gereksinimi sık sık ortaya çıkar: adlandırma kurallarına uymak ya da daha anlaşılır olmak için adların değiştirilmesi, kod veya varlık dosyalarının ise proje hiyerarşisinde daha mantıklı bir yere taşınması gerekir.

Defold, varlıkların nasıl kullanıldığını izleyerek verimli biçimde yeniden düzenleme yapmanıza yardımcı olur. Yeniden adlandırılan ve/veya taşınan varlıklara yapılan başvuruları otomatik olarak günceller. Bir geliştirici olarak çalışırken kendinizi özgür hissetmelisiniz. Projeniz, her şeyin bozulup dağılmasından korkmadan dilediğiniz gibi değiştirebileceğiniz esnek bir yapıdır.

::: important
Otomatik yeniden düzenleme yalnızca değişiklikler düzenleyici içinden yapılırsa çalışır. Bir dosyayı düzenleyici dışında yeniden adlandırır veya taşırsanız bu dosyaya yapılan başvurular otomatik olarak değiştirilmez.
:::

Ancak, örneğin bir varlığı silerek bir başvuruyu bozarsanız düzenleyici sorunu çözemez, fakat yararlı hata bildirimleri sağlar. Örneğin, bir atlastan bir animasyonu silerseniz ve bu animasyon herhangi bir yerde kullanılıyorsa Defold, oyunu başlatmaya çalıştığınızda bir hata bildirir. Düzenleyici, sorunu hızla bulmanıza yardımcı olmak için hataların oluştuğu yerleri de işaretler:

![Yeniden düzenleme hatası](images/workflow/delete_error.png)

Derleme hataları, düzenleyicinin alt kısmındaki *Build Errors* bölmesinde görünür. Bir hataya <kbd>çift tıkladığınızda</kbd> sorunun bulunduğu yere gidersiniz.
