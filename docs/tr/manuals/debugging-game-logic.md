---
title: Defold'da hata ayıklama
brief: Bu kılavuz, Defold'da bulunan hata ayıklama olanaklarını açıklar.
---

# Oyun mantığında hata ayıklama {#debugging-game-logic}

Defold, inceleme olanağı sunan tümleşik bir Lua hata ayıklayıcısı (debugger) içerir. Yerleşik [profil çıkarma (profiling) araçlarıyla](/manuals/profiling) birlikte, oyun mantığınızdaki hataların nedenini bulmanıza veya performans sorunlarını analiz etmenize yardımcı olabilecek güçlü bir araçtır.

## Yazdırarak ve görsel olarak hata ayıklama {#print-and-visual-debugging}

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

## Hata ayıklayıcıyı çalıştırma {#running-the-debugger}

Lua hata ayıklayıcısı, yerel hata ayıklama ve görüntüsüz (headless) derlemelerde kullanılabilir. Düzenleyiciyle aynı Defold sürümüne ait bir motor kullanın. Yayıma yönelik derlemeler ve Web derlemeleri, hata ayıklayıcı bağlamayı desteklemez.

Hata ayıklayıcıyı çalıştırmak için <kbd>Debug ▸ Start/Attach</kbd> seçeneğini seçin. Bu seçenek, oyunu hata ayıklayıcı bağlı olarak başlatır veya zaten çalışan bir oyuna bağlanır. Hata ayıklama için oyun başlatılırken düzenleyici, etkin kesme noktalarını başlangıç betikleri çalışmadan önce kurar; böylece başlatmadan önce `init()` içine kesme noktası koyabilirsiniz.

Bir cihaza bağlanmak için <kbd>Project ▸ Targets</kbd> altında cihazı seçin, ardından <kbd>Debug ▸ Start/Attach</kbd> seçeneğini seçin. Bağlantı, yürütmeyi bir sonraki Lua satırında duraklatır. Düzenleyici, desteklenen yerel ve uzak hedefler için hata ayıklayıcı bağlantısını otomatik olarak kurar. Bağlantı gereksinimleri için [Uzak hedefler](#remote-targets) bölümüne bakın veya [harici bir hata ayıklayıcıyı bağlama](#native-dap-connections) hakkında bilgi edinin.

![genel bakış](images/debugging/overview.png)

Hata ayıklayıcı bağlanır bağlanmaz konsoldaki hata ayıklayıcı kontrol düğmeleri veya <kbd>Debug</kbd> menüsü aracılığıyla oyunun yürütülmesini kontrol edebilirsiniz:

Break
: ![duraklatma](images/debugging/pause.svg){width=60px .left}
  Lua yürütmesini bir sonraki kaynak satırında duraklatın. Artık oyunun durumunu inceleyebilir, oyunu adım adım ilerletebilir veya bir sonraki kesme noktasına (breakpoint) kadar çalıştırmaya devam edebilirsiniz. Geçerli yürütme noktası kod düzenleyicisinde işaretlenir:

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
Adımlama Lua kaynak satırlarını izler. Örneğin bir döngü yinelendiğinde aynı satıra yeniden gelinebilir; bu nedenle her adım dosyadaki bir sonraki satıra ilerlemez.
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
: Oyun duraklatılmışken *Call Stack* görünümünde bir yığın çerçevesi seçin, konsolun alt kısmına bir Lua ifadesi veya deyimi yazın ve <kbd>Enter</kbd> tuşuna basın. Değerlendirme, seçilen çerçevenin yerel değişkenlerini, üst kapsam değişkenlerini (upvalue) ve genel değişkenlerini kullanır. Tablo sonuçları iç içe içeriklerini de kapsar.

  ![konsol](images/debugging/console.png)

  Atamalar aracılığıyla değerleri de değiştirebilirsiniz; örneğin `self` değişkeninin kullanılabildiği bir çerçevede `self.score = 100` yazabilirsiniz. Değerlendirilen kod, oyun durumunu oyununuzun yürüttüğü kodla aynı şekilde etkiler.

Değişkenleri inceleme
: Yerel değişkenlerini ve üst kapsam değişkenlerini *Variables* görünümünde incelemek için *Call Stack* görünümünde bir çerçeve seçin. Genel değişkenleri incelemek için `_G` öğesini, alanlarını incelemek için tabloları veya `self` öğesini genişletin. Düzenleyici, adımlarken, çerçeve değiştirirken veya değerlendirme sonrasında yenilerken güncel değerleri alır ve genişletilmiş yolları, seçimi ve kaydırma konumunu korur.

Hata ayıklayıcının bağlantısını kesme
: Hata ayıklayıcının oyunla bağlantısını kesmek için <kbd>Debug ▸ Detach Debugger</kbd> seçeneğini seçin. Oyun hemen çalışmaya devam eder. Oyunu yeniden başlatmadan tekrar bağlanmak için <kbd>Debug ▸ Start/Attach</kbd> seçeneğini kullanın.

## Yerel DAP bağlantıları {#native-dap-connections}

Motor, TCP üzerinden yerel bir Debug Adapter Protocol (DAP) sunucusu sağlar. Harici bir DAP istemcisi için dinleyiciyi yerel bir Defold hata ayıklama veya görüntüsüz motorda başlatın, ardından istemciyi motorun adresine ve bağlantı noktasına bağlayın. <kbd>Debug ▸ Start/Attach</kbd> seçeneğini kullandığınızda düzenleyici dinleyiciyi otomatik olarak kurar.

Geçerli düzenleyici yalnızca MobDebug destekleyen eski motorlara bağlanamaz. Geçerli sürümlerde `require "builtins.scripts.mobdebug"` çağrısı gerekli değildir ve kullanılamaz.

### Dinleyiciyi başlatma {#starting-the-listener}

Önce projenizi derleyin. `build/default/game.projectc` dosyasını içeren proje dizininden yerel hata ayıklama motorunu şu [başlangıç yapılandırması geçersiz kılmalarıyla](/manuals/project-settings/#setting-config-values-on-engine-startup) çalıştırın:

```sh
dmengine --config=debugger.enabled=1 \
  --config=debugger.port=8172 --config=debugger.wait=1
```

DAP istemcinizi `127.0.0.1:8172` adresine bağlayın. Motor, başlangıç betiklerini çalıştırmadan önce istemcinin kesme noktalarını yapılandırmasını bekler.

| Ayar | Varsayılan | Amaç |
| --- | --- | --- |
| `debugger.enabled` | `0` | Dinleyiciyi motorun başlangıcında başlatmak için `1` olarak ayarlayın. |
| `debugger.address` | `127.0.0.1` | Dinlenecek IPv4 adresi. Varsayılan değer, aynı bilgisayardan gelen bağlantıları kabul eder. |
| `debugger.port` | `8172` | TCP dinleme bağlantı noktası. Kullanılabilir bir bağlantı noktası seçmek için `0` kullanın. |
| `debugger.wait` | `0` | Başlangıç betiklerini çalıştırmadan önce hata ayıklayıcı istemcisinin yapılandırmasını beklemek için `1` olarak ayarlayın. |

Bu değerleri [game.project dosyasının Debugger bölümüne](/manuals/project-settings/#debugger) de ekleyebilirsiniz. Düzenleyici, <kbd>Debug ▸ Start/Attach</kbd> için dinleyiciyi otomatik olarak yapılandırır; bu nedenle elle yapılandırma yalnızca dinleyiciyi kendiniz başlatırken gerekir.

Motor günlüğü, seçilen adresi ve bağlantı noktasını bildirir. `debugger.wait=0` olduğunda oyun hemen başlar ve daha sonra bağlanabilirsiniz. `debugger.wait=1` olduğunda motor, istemci kesme noktaları dahil oturumu yapılandırmayı bitirene kadar bekler. Yerel hata ayıklama başlatmalarında düzenleyici kullanılabilir bir bağlantı noktasını otomatik olarak seçer.

İstemcinin bağlantısının kesilmesi yürütmeyi sürdürür ve dinleyiciyi başka bir bağlantı için kullanılabilir bırakır. Başlangıç yapılandırması beklenirken bağlantının kesilmesi de motoru serbest bırakır. Dinleyici başlatılamazsa motor hatayı günlüğe yazar ve başlangıç işlemlerine devam eder; kullanılabilir bir bağlantı noktası seçmek için Lua'dan `debugger.start(0)` ile yeniden deneyebilirsiniz.

### Çalışma sırasında dinleyiciyi etkinleştirme {#enabling-the-listener-while-running}

Oyunu yeniden başlatmadan bir betikten dinleyiciyi etkinleştirmek için:

```lua
if debugger then
    local port = debugger.start(0)
    print("DAP listener port:", port)
end
```

`debugger.start([port [, address]])`, dinleme bağlantı noktasını hemen döndürür. İstemci beklemez veya oyunu duraklatmaz. Verilmeyen bağımsız değişkenler için `debugger.port` ve `debugger.address` kullanılır; `0` verilmesi kullanılabilir bir bağlantı noktası seçer. Yinelenen çağrılar mevcut dinleyicinin bağlantı noktasını döndürür ve adresini veya bağlantı noktasını değiştirmez. `debugger` modülünü yerel hata ayıklama ve görüntüsüz motorlar sağlar.

Bağlantı noktası `0` ile `65535` arasında bir tamsayı olmalıdır. Yalnızca adresi geçersiz kılmak için ilk bağımsız değişken olarak `nil` verin. Geçersiz bağımsız değişkenler veya dinleyicinin adrese bağlanamaması bir Lua hatasına yol açar.

### Uzak hedefler {#remote-targets}

Başka bir bilgisayardan doğrudan bağlantı için dinleyiciyi cihazın IPv4 arayüzüne veya `0.0.0.0` adresine (tüm IPv4 arayüzleri) bağlayın. Örneğin `debugger.start(8172, "0.0.0.0")` kullanın veya yukarıdaki başlangıç komutuna `--config=debugger.address=0.0.0.0` ekleyin. İstemciyi cihazın gerçek IP adresine bağlayın ve dinleme bağlantı noktasına TCP erişimine izin verin. `0.0.0.0` bir bağlanma adresidir; istemciye girilecek adres değildir.

Defold düzenleyicisi bu uzak adrese bağlanmayı otomatik olarak ister ve uzak hedefler için `8172 + project.instance_index` bağlantı noktasını kullanır. Dinamik olarak seçilmiş uzak bağlantı noktasını keşfedemez. Uzak dinleyiciyi zaten localhost üzerinde veya farklı bir bağlantı noktasında başlattıysanız düzenleyiciden bağlanmadan önce motoru yeniden başlatın.

Hata ayıklayıcı Lua kodunu değerlendirebilir ve kimlik doğrulaması yapmaz. Uzak erişimi yalnızca güvenilen bir geliştirme ağında etkinleştirin.

### Harici istemciler {#external-clients}

TCP üzerinden doğrudan bir DAP sunucusuna bağlanmayı destekleyen bir istemci kullanın. Kaynak eşlemesini, `game.project` dosyasını içeren klasöre yapılandırın (DAP `localRoot` bağlantı bağımsız değişkeni). Önce motor dinleyicisini başlatın, ardından istemciyi bağlayın.

#### VS Code {#vs-code}

[Lua Debug eklentisini](https://marketplace.visualstudio.com/items?itemName=actboy168.lua-debug) (`actboy168.lua-debug`) yükleyin, `game.project` dosyasını içeren klasörü VS Code'da açın ve `.vscode/launch.json` dosyasına şu yapılandırmayı ekleyin:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Defold Lua",
      "type": "lua",
      "request": "attach",
      "address": "127.0.0.1:8172",
      "debugServer": 8172,
      "localRoot": "${workspaceFolder}",
      "stopOnEntry": false
    }
  ]
}
```

VS Code bir `.script`, `.gui_script` veya `.render_script` dosyasını düz metin olarak açarsa kesme noktalarını ayarlamadan önce durum çubuğundaki dil göstergesinden **Lua** seçeneğini seçin.

Örneğin bir betiğin `init()` işlevinde kesme noktası ayarlayın. [Yukarıdaki başlangıç komutuyla](#starting-the-listener) motoru başlatın, ardından VS Code'un **Run and Debug** görünümünde **Attach to Defold Lua** seçeneğini seçin. `debugger.wait=1` olduğunda motor, istemci kesme noktalarını kurduktan sonra başlangıç betiklerini çalıştırır. Bağlantıdan sonra bir sonraki Lua satırında da duraklamak istiyorsanız `stopOnEntry` değerini `true` olarak ayarlayın.

VS Code'un [`debugServer` ayarı](https://code.visualstudio.com/api/extension-guides/debugger-extension#development-setup-for-mock-debug), motorun yerel TCP dinleyicisine doğrudan bağlanır. Lua Debug eklentisinin bağlantı yapılandırması `address` alanını gerektirir. Dinleyicinin bağlantı noktasını değiştirirseniz her iki alanı da güncelleyin. İstemcinin motorun Lua kaynak adlarını dosyalarınızla eşleyebilmesi için `localRoot` proje klasörünü göstermelidir.

Uzak bir motor için DAP bağlantı noktasını localhost'a yönlendirin ve yönlendirilen bağlantı noktasını her iki alana da yazın veya doğrudan uzak ana bilgisayara bağlanan bir DAP istemcisi kullanın.

## Breakpoints sekmesi {#breakpoints-tab}

  ![Breakpoints sekmesi](images/debugging/breakpoints_tab.png)

  Farklı betiklerde birden çok kesme noktasıyla çalışırken Breakpoints sekmesi, tüm kesme noktalarınızı tek bir yerden yönetebileceğiniz merkezi bir görünüm sunar.

##### Tek bir kesme noktasının kontrolleri {#individual-breakpoint-controls}

  Tek bir kesme noktasıyla çalışmak için:
  - Kesme noktasını kaldırmak için kırmızı çöp kutusu simgesine tıklayın
  - Code View içinde ilgili satıra gitmek için satıra (koşul alanının dışına) çift tıklayın
  - Koşullu kesme noktalarını düzenlemek için koşul hücresine çift tıklayın veya kalem simgesine tıklayın
  - Koşulu temizlemek için imleci koşul hücresinin üzerine getirdiğinizde görünen X temizleme düğmesine tıklayın

##### Toplu işlemler {#batch-operations}

  Ctrl/Cmd+click veya Shift+click kullanarak birden çok kesme noktası seçin, ardından toplu işlemler yapmak için sağ tıklayın. Birden fazla kesme noktasının koşullarını aynı anda düzenleyebilir, etkinlik durumlarını değiştirebilir veya noktaları tamamen kaldırabilirsiniz.

  Araç çubuğundaki düğmeler, tüm kesme noktalarını aynı anda etkinleştirmenizi, devre dışı bırakmanızı veya durumlarını tersine çevirmenizi sağlar. Bu, oyununuzu durmadan çalıştırmak istediğinizde ancak kesme noktalarının konumlarını kaybetmek istemediğinizde yararlıdır. Hata ayıklama oturumunuz bittiğinde tümünü kaldırabilirsiniz.

## Lua hata ayıklama kütüphanesi {#lua-debug-library}

Lua, bazı durumlarda, özellikle Lua ortamınızın iç yapısını incelemeniz gerektiğinde yararlı olan bir hata ayıklama kütüphanesiyle gelir. Bu konuda daha fazla bilgiyi [Lua kılavuzundaki hata ayıklama kütüphanesi bölümünde](http://www.lua.org/pil/contents.html#23) bulabilirsiniz.

## Hata ayıklama kontrol listesi {#debugging-checklist}

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
