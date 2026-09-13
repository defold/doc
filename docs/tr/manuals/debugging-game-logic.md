---
title: Defold'da hata ayıklama
brief: Bu kılavuz, Defold'da bulunan hata ayıklama olanaklarını açıklar.
---

# Oyun mantığında hata ayıklama

Defold, inceleme olanağı sunan tümleşik bir Lua hata ayıklayıcısı (debugger) içerir. Yerleşik [profil çıkarma (profiling) araçlarıyla](/manuals/profiling) birlikte, oyun mantığınızdaki hataların nedenini bulmanıza veya performans sorunlarını analiz etmenize yardımcı olabilecek güçlü bir araçtır.

## Yazdırarak ve görsel olarak hata ayıklama

Defold'da oyununuzda hata ayıklamanın en basit yolu, [yazdırarak hata ayıklamayı](http://en.wikipedia.org/wiki/Debugging#Techniques) kullanmaktır. Değişkenleri izlemek veya yürütme akışını göstermek için `print()` ya da [`pprint()`](/ref/builtins#pprint) ifadelerini kullanın. Betiği (script) olmayan bir oyun nesnesi (game object) tuhaf davranıyorsa ona yalnızca hata ayıklama amacı taşıyan bir betik ekleyebilirsiniz. Yazdırma işlevlerinden herhangi birini kullanmak, düzenleyicideki *Console* görünümüne ve [oyun günlüğüne](/manuals/debugging-game-and-system-logs) çıktı yazar.

Motor, yazdırmanın yanı sıra ekrana hata ayıklama metni ve düz çizgiler de çizebilir. Bunun için `@render` soketine (socket) iletiler (message) gönderilir:

```lua
-- Draw value of "my_val" with debug text on the screen
msg.post("@render:", "draw_text", { text = "My value: " .. my_val, position = vmath.vector3(200, 200, 0) })

-- Draw colored text on the screen
local color_green = vmath.vector4(0, 1, 0, 1)
msg.post("@render:", "draw_debug_text", { text = "Custom color", position = vmath.vector3(200, 180, 0), color = color_green })

-- Draw debug line between player and enemy on the screen
local start_p = go.get_position("player")
local end_p = go.get_position("enemy")
local color_red = vmath.vector4(1, 0, 0, 1)
msg.post("@render:", "draw_line", { start_point = start_p, end_point = end_p, color = color_red })
```

Görsel hata ayıklama iletileri, görüntü oluşturan işleme (rendering) hattına veri ekler ve bu veriler normal işleme hattının bir parçası olarak çizilir.

* `"draw_line"`, işleme betiğindeki `render.draw_debug3d()` işleviyle işlenen veriler ekler.
* `"draw_text"`, `/builtins/fonts/debug/always_on_top_font.material` materyalini kullanan `/builtins/fonts/debug/always_on_top.font` yazı tipiyle işlenir.
* `"draw_debug_text"`, `"draw_text"` ile aynıdır, ancak özel bir renkte işlenir.

Bu verileri muhtemelen her karede güncellemek isteyeceğinizi unutmayın; bu nedenle iletileri `update()` işlevinde göndermek iyi bir fikirdir.

## Hata ayıklayıcıyı çalıştırma

Hata ayıklayıcıyı çalıştırmak için <kbd>Debug ▸ Start/Attach</kbd> seçeneğini seçin. Bu seçenek, oyunu hata ayıklayıcı bağlı olarak başlatır veya hata ayıklayıcıyı zaten çalışan bir oyuna bağlar.

![genel bakış](images/debugging/overview.png)

Hata ayıklayıcı bağlanır bağlanmaz konsoldaki hata ayıklayıcı kontrol düğmeleri veya <kbd>Debug</kbd> menüsü aracılığıyla oyunun yürütülmesini kontrol edebilirsiniz:

Break
: ![duraklatma](images/debugging/pause.svg){width=60px .left}
  Oyunun yürütülmesini hemen kesin. Oyun, o anda bulunduğu noktada duraklar. Artık oyunun durumunu inceleyebilir, oyunu adım adım ilerletebilir veya bir sonraki kesme noktasına (breakpoint) kadar çalıştırmaya devam edebilirsiniz. Geçerli yürütme noktası kod düzenleyicisinde işaretlenir:

  ![betik](images/debugging/script.png)

Continue
: ![oynatma](images/debugging/play.svg){width=60px .left}
  Oyunu çalıştırmaya devam edin. Oyun kodu, duraklatma düğmesine basana veya yürütme ayarladığınız bir kesme noktasına ulaşana kadar çalışmaya devam eder. Yürütme, ayarlanmış bir kesme noktasında duraklarsa yürütme noktası kod düzenleyicisinde kesme noktası işaretinin üzerinde gösterilir:

  ![kesme](images/debugging/break.png)

Stop
: ![durdurma](images/debugging/stop.svg){width=60px .left}
  Hata ayıklayıcıyı durdurun. Bu düğmeye basmak, hata ayıklayıcıyı hemen durdurur, oyunla bağlantısını keser ve çalışan oyunu sonlandırır.

Step Over
: ![çağrıyı tamamlayıp ilerleme](images/debugging/step_over.svg){width=60px .left}
  Programın yürütülmesini bir adım ilerletin. Yürütme başka bir Lua işlevinin çalıştırılmasını içeriyorsa yürütme _işlevin içine ilerlemez_; çalışmaya devam eder ve işlev çağrısının altındaki bir sonraki satırda durur. Bu örnekte kullanıcı "step over" düğmesine basarsa hata ayıklayıcı kodu yürütür ve `nextspawn()` işlevinin çağrıldığı satırın altındaki `end` ifadesinde durur:

  ![adım](images/debugging/step.png)

::: sidenote
Bir Lua kodu satırı tek bir ifadeye karşılık gelmez. Hata ayıklayıcıda adımlama, her seferinde bir ifade ilerler; bu nedenle şu anda bir sonraki satıra geçmek için adım düğmesine birden fazla kez basmanız gerekebilir.
:::

Step Into
: ![işlevin içine ilerleme](images/debugging/step_in.svg){width=60px .left}
  Programın yürütülmesini bir adım ilerletin. Yürütme başka bir Lua işlevinin çalıştırılmasını içeriyorsa yürütme _işlevin içine ilerler_. İşlevin çağrılması, çağrı yığınına (call stack) bir kayıt ekler. Giriş noktasını ve o kapanıştaki (closure) tüm değişkenlerin içeriğini görmek için çağrı yığını listesindeki her kayda tıklayabilirsiniz. Burada kullanıcı `nextspawn()` işlevinin içine ilerlemiştir:

  ![işlevin içine ilerleme](images/debugging/step_into.png)

Step Out
: ![geçerli işlevden çıkana kadar ilerleme](images/debugging/step_out.svg){width=60px .left}
  Geçerli işlevden dönene kadar yürütmeye devam edin. Yürütmeyi bir işlevin içine ilerlettiyseniz "step out" düğmesine basmak, işlev dönene kadar yürütmeyi sürdürür.

Kesme noktalarını ayarlama ve temizleme
: Lua kodunuzda istediğiniz sayıda kesme noktası ayarlayabilirsiniz. Oyun, hata ayıklayıcı bağlı olarak çalışırken karşılaştığı bir sonraki kesme noktasında yürütmeyi duraklatır ve sizden yeni bir işlem bekler.

  ![kesme noktası ekleme](images/debugging/add_breakpoint.png)

  Bir kesme noktası ayarlamak veya temizlemek için kod düzenleyicisinde satır numaralarının hemen sağındaki sütuna tıklayın. Menüden <kbd>Edit ▸ Toggle Breakpoint</kbd> seçeneğini de seçebilirsiniz.

Kesme noktalarını devre dışı bırakma ve etkinleştirme
: Kesme noktaları, kaldırılmadan geçici olarak devre dışı bırakılabilir. Devre dışı bırakıldıklarında yürütme sırasında yok sayılırlar, ancak istendiği zaman yeniden etkinleştirilebilirler. Kod düzenleyicisinin kenar boşluğundaki kesme noktasına sağ tıklayın, ardından `Enabled` onay kutusunun durumunu değiştirin. Devre dışı bırakılan kesme noktaları, etkin olmadıklarını göstermek için içleri boş olarak görünür.

  ![kesme noktasını devre dışı bırakma](images/debugging/disable_breakpoint.png)

Koşullu kesme noktalarını ayarlama
: Kesme noktanıza, tetiklenmesi için doğru olarak değerlendirilmesi gereken bir koşul ekleyebilirsiniz. Koşul, kod yürütülürken o satırda kullanılabilen yerel değişkenlere erişebilir.

  ![kesme noktasını düzenleme](images/debugging/edit_breakpoint.png)

  Kesme noktası koşulunu düzenlemek için kod düzenleyicisinde satır numaralarının hemen sağındaki sütuna sağ tıklayın veya menüden <kbd>Edit ▸ Edit Breakpoint</kbd> seçeneğini seçin.

Lua ifadelerini değerlendirme
: Hata ayıklayıcı bağlıyken ve oyun bir kesme noktasında duraklatılmışken geçerli bağlamı içeren bir Lua çalışma zamanı ortamı kullanılabilir. Değerlendirmek için konsolun alt kısmına Lua ifadeleri yazın ve <kbd>Enter</kbd> tuşuna basın:

  ![konsol](images/debugging/console.png)

  Şu anda değerlendirici aracılığıyla değişkenleri değiştirmek mümkün değildir.

Hata ayıklayıcının bağlantısını kesme
: Hata ayıklayıcının oyunla bağlantısını kesmek için <kbd>Debug ▸ Detach Debugger</kbd> seçeneğini seçin. Oyun hemen çalışmaya devam eder.

## Breakpoints sekmesi

  ![Breakpoints sekmesi](images/debugging/breakpoints_tab.png)

  Farklı betiklerde birden çok kesme noktasıyla çalışırken Breakpoints sekmesi, tüm kesme noktalarınızı tek bir yerden yönetebileceğiniz merkezi bir görünüm sunar.

##### Tek bir kesme noktasının kontrolleri

  Tek bir kesme noktasıyla çalışmak için:
  - Kesme noktasını kaldırmak için kırmızı çöp kutusu simgesine tıklayın
  - Code View içinde ilgili satıra gitmek için satıra (koşul alanının dışına) çift tıklayın
  - Koşullu kesme noktalarını düzenlemek için koşul hücresine çift tıklayın veya kalem simgesine tıklayın
  - Koşulu temizlemek için imleci koşul hücresinin üzerine getirdiğinizde görünen X temizleme düğmesine tıklayın

##### Toplu işlemler

  Ctrl/Cmd+click veya Shift+click kullanarak birden çok kesme noktası seçin, ardından toplu işlemler yapmak için sağ tıklayın. Birden fazla kesme noktasının koşullarını aynı anda düzenleyebilir, etkinlik durumlarını değiştirebilir veya noktaları tamamen kaldırabilirsiniz.

  Araç çubuğundaki düğmeler, tüm kesme noktalarını aynı anda etkinleştirmenizi, devre dışı bırakmanızı veya durumlarını tersine çevirmenizi sağlar. Bu, oyununuzu durmadan çalıştırmak istediğinizde ancak kesme noktalarının konumlarını kaybetmek istemediğinizde yararlıdır. Hata ayıklama oturumunuz bittiğinde tümünü kaldırabilirsiniz.

## Lua hata ayıklama kütüphanesi

Lua, bazı durumlarda, özellikle Lua ortamınızın iç yapısını incelemeniz gerektiğinde yararlı olan bir hata ayıklama kütüphanesiyle gelir. Bu konuda daha fazla bilgiyi [Lua kılavuzundaki hata ayıklama kütüphanesi bölümünde](http://www.lua.org/pil/contents.html#23) bulabilirsiniz.

## Hata ayıklama kontrol listesi

Bir hatayla karşılaşırsanız veya oyununuz beklendiği gibi davranmazsa aşağıdaki hata ayıklama kontrol listesini izleyin:

1. Konsol çıktısını kontrol edin ve çalışma zamanı hatası olmadığını doğrulayın.

2. Kodun gerçekten çalıştığını doğrulamak için kodunuza `print` ifadeleri ekleyin.

3. Kod çalışmıyorsa çalışması için düzenleyicide gereken ayarları doğru yaptığınızı kontrol edin. Betik doğru oyun nesnesine eklenmiş mi? Betiğiniz girdi odağını (input focus) almış mı? Girdi tetikleyicileri (input trigger) doğru mu? Gölgelendirici kodu materyale eklenmiş mi? Ve benzeri.

4. Kodunuz değişkenlerin değerlerine bağlıysa (örneğin bir if ifadesinde) bu değerleri kullanıldıkları veya kontrol edildikleri yerde `print` ile yazdırın ya da hata ayıklayıcıyla inceleyin.

Bazen bir hatayı bulmak zor ve zaman alıcı bir süreç olabilir. Bu süreç, kodunuzu parça parça gözden geçirmenizi, her şeyi kontrol etmenizi, hatalı kodun kapsamını daraltmanızı ve hata kaynaklarını elemenizi gerektirir. Bunu en iyi şekilde yapmak için "böl ve yönet" adlı yöntem kullanılır:

1. Kodun hangi yarısının (veya daha küçük bir bölümünün) hatayı içerdiğini belirleyin.
2. Ardından bu yarının hangi yarısının hatayı içerdiğini belirleyin.
3. Hatayı bulana kadar ona neden olan kodun kapsamını daraltmaya devam edin.

İyi avlar!

## Fizik sorunlarında hata ayıklama {#debugging-problems-with-physics}

Fizikle ilgili sorunlar yaşıyorsanız ve çarpışmalar beklendiği gibi çalışmıyorsa fizik hata ayıklamasını etkinleştirmeniz önerilir. *game.project* dosyasının *Physics* bölümündeki *Debug* onay kutusunu işaretleyin:

![fizik hata ayıklama ayarı](images/debugging/physics_debug_setting.png)

Bu onay kutusu etkinleştirildiğinde Defold, tüm çarpışma şekillerini ve çarpışmaların temas noktalarını çizer:

![fizik hata ayıklama görselleştirmesi](images/debugging/physics_debug_visualisation.png)
