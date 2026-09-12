---
title: Kod yazma
brief: Bu kılavuz, Defold'da kodla nasıl çalışılacağını kısaca ele alır.
---

# Kod yazma

Defold, oyun içeriğinizin büyük bir bölümünü karo haritası (tilemap) ve parçacık efekti (particle effect) düzenleyicileri gibi görsel araçlarla oluşturmanıza olanak tanısa da oyun mantığını bir kod düzenleyicisi kullanarak oluşturursunuz. Oyun mantığı [Lua programlama dili](https://www.lua.org/) ile yazılırken motorun kendisine yönelik eklentiler, hedef platformun yerel dili veya dilleri kullanılarak yazılır.

## Lua kodu yazma

Defold, hedef platforma bağlı olarak Lua 5.1 ve LuaJIT kullanır. Oyun mantığını yazarken Lua'nın bu belirli sürümlerinin dil belirtimine uymanız gerekir. Defold'da Lua ile çalışma hakkında daha fazla bilgi için [Defold'da Lua kılavuzumuza](/manuals/lua) bakın.

## Lua'ya dönüştürülen diğer dilleri kullanma

Defold, Lua kodu üreten kaynak kod dönüştürücülerin (transpiler) kullanımını destekler. Kaynak kod dönüştürücü eklentisi yüklüyken, statik olarak denetlenen Lua kodu yazmak için [Teal](https://github.com/defold/extension-teal) gibi alternatif diller kullanabilirsiniz. Bu, kısıtlamaları olan bir önizleme özelliğidir: mevcut kaynak kod dönüştürücü desteği, Defold Lua çalışma zamanı ortamında tanımlı modüller ve işlevler hakkındaki bilgileri sunmaz. Bu nedenle `go.animate` gibi Defold API'lerini kullanmak için harici tanımları kendiniz yazmanız gerekir.

## Yerel kod yazma

Defold, motorun kendisinin sunmadığı platforma özgü işlevlere erişmek için oyun motorunu yerel kodla (native code) genişletmenize olanak tanır. Lua'nın performansı yeterli olmadığında da yerel kod kullanabilirsiniz (yoğun kaynak gerektiren hesaplamalar, görüntü işleme vb.). Daha fazla bilgi için [yerel kod eklentileri kılavuzlarımıza](/manuals/extensions/) bakın.

## Yerleşik kod düzenleyicisini kullanma

Defold'un yerleşik kod düzenleyicisi, Lua dosyalarını (.lua), Defold betik dosyalarını (.script, .gui_script ve .render_script) ve düzenleyicinin doğrudan işlemediği dosya uzantılarına sahip diğer tüm dosyaları açıp düzenlemenize olanak tanır. Ayrıca düzenleyici, Lua ve betik dosyaları için sözdizimi vurgulaması sağlar.

![](/images/editor/code-editor.png)

### Kod tamamlama {#code-completion}

Yerleşik kod düzenleyicisi, kod yazarken işlevler için kod tamamlama önerileri gösterir:

![](/images/editor/codecompletion.png)

<kbd>CTRL</kbd> + <kbd>Space</kbd> tuşlarına bastığınızda işlevler, bağımsız değişkenler ve dönüş değerleri hakkında ek bilgiler gösterilir:

![](/images/editor/apireference.png)

Birlikte gelen Lua dil sunucusu, Defold API'leri için tür açıklamaları (type annotations) içerir. Kod tamamlama, üzerine gelindiğinde gösterilen bilgiler ve tanılama işlevleri; karma değerleri (hash), URL'ler, vektörler ve kuaterniyonlar (quaternion) gibi Defold türlerini, işlev bağımsız değişkenlerini ve dönüş değerlerini tanır. Düzenleyici, oyun betikleri ve `.editor_script` dosyalarında kullanılan `editor.*` API'leri için açıklamalar sağlar. Defold kod düzenleyicisini kullanırken yerleşik API'ler için ayrı bir açıklama kütüphanesine gerek yoktur.

Üçüncü taraf eklenti API'leri kendi açıklamalarına ihtiyaç duyabilir.

### Kodu biçimlendirme {#formatting-code}

Dil sunucusunun biçimlendiricisini çalıştırmak için <kbd>Edit ▸ Format Document/Selection</kbd> seçeneğini seçin veya <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd> tuşlarına basın. Bir seçim varsa düzenleyici seçili satırları, yoksa belgenin tamamını biçimlendirir. Biçimlendirme için ilgili biçimlendirme işlemini destekleyen bir dil sunucusu gerekir.

Değiştirilmiş açık dosyaları kaydederken biçimlendirmek için <kbd>Preferences ▸ Code</kbd> bölümündeki **Format on save** seçeneğini etkinleştirin. Bu tercih varsayılan olarak devre dışıdır ve belge biçimlendirmeyi destekleyen bir dil sunucusu gerektirir. [Kod tercihlerine](/manuals/editor-preferences/#code) bakın.

### Simgeye gitme

Yerleşik kod düzenleyicisi, geçerli kod dosyasındaki işlevler, nesneler ve değişkenler gibi simgelerin aranabilir bir listesini gösterebilir. <kbd>View ▸ Jump to Symbol…</kbd> seçeneğini seçin veya Windows ve Linux'ta <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd>, macOS'te ise <kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>O</kbd> tuşlarına basın.

Simgeler arasında yaklaşık eşleşmeyle arama yapmak için yazmaya başlayın. Sonuçlar arasında ilerlemek ve düzenleyicideki konumlarını önizlemek için ok tuşlarını kullanın, ardından seçili simgeye gitmek için <kbd>Enter</kbd> tuşuna basın. İletişim kutusunu kapatıp önceki imleç ve kaydırma konumuna dönmek için <kbd>Esc</kbd> tuşuna basın.

![](/images/editor/jump-to-symbol.png)

### Statik kod denetimini yapılandırma {#linting-configuration}

Yerleşik kod düzenleyicisi, [Luacheck](https://luacheck.readthedocs.io/en/stable/index.html) ve [Lua dil sunucusunu](https://luals.github.io/wiki/diagnostics/) kullanarak statik kod denetimi (code linting) yapar. Luacheck'i yapılandırmak için projenin kök dizininde bir `.luacheckrc` dosyası oluşturun. Kullanılabilir seçeneklerin listesi için [Luacheck yapılandırma sayfasını](https://luacheck.readthedocs.io/en/stable/config.html) okuyabilirsiniz. Defold, Luacheck yapılandırmasında aşağıdaki varsayılanları kullanır:

```lua
unused_args = false      -- don't warn on unused arguments (common for .script files)
max_line_length = false  -- don't warn on long lines
ignore = {
    "611",               -- line contains only whitespace
    "612",               -- line contains trailing whitespace
    "614"                -- trailing whitespace in a comment
},
```

## Harici bir kod düzenleyicisi kullanma

Defold'un kod düzenleyicisi, kod yazmak için gereken temel işlevleri sağlar. Ancak daha gelişmiş kullanım durumlarında veya tercih ettiği bir kod düzenleyicisi olan ileri düzey kullanıcılar için Defold'un dosyaları harici bir düzenleyiciyle açmasını sağlamak mümkündür. [Preferences penceresinin Code sekmesinde](/manuals/editor-preferences/#code), kod düzenlerken kullanılacak harici bir düzenleyici tanımlayabilirsiniz.

### Visual Studio Code - Defold Kit

Defold Kit, aşağıdaki özellikleri sunan bir Visual Studio Code eklentisidir:

* Önerilen eklentileri yükleme
* Lua vurgulaması, otomatik tamamlama ve statik kod denetimi
* İlgili ayarları çalışma alanına uygulama
* Defold API'si için Lua açıklamaları
* Bağımlılıklar için Lua açıklamaları
* Derleyip başlatma
* Kesme noktalarıyla hata ayıklama
* Tüm platformlar için paketleme
* Bağlı mobil cihazlarda dağıtıma alma

[Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) üzerinden daha fazla bilgi edinin ve Defold Kit'i yükleyin.


## Belge yazılımları

[Dash ve Zeal](https://forum.defold.com/t/defold-docset-for-dash/2417) için topluluk tarafından oluşturulmuş API başvuru belgesi paketleri mevcuttur.
