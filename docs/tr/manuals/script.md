---
title: Betiklerde oyun mantığı yazma
brief: Bu kılavuz, betik bileşenleri kullanarak oyun mantığının nasıl ekleneceğini açıklar.
---

# Betikler

Betik bileşenleri (script component), [Lua programlama dilini](/manuals/lua) kullanarak oyun mantığı oluşturmanızı sağlar.


## Betik türleri

Defold'da üç tür Lua betiği vardır ve her tür farklı Defold kütüphanelerine erişebilir.

Oyun nesnesi betikleri
: Uzantısı _.script_ şeklindedir. Bu betikler oyun nesnelerine (game object) diğer [bileşenlerle](/manuals/components) aynı şekilde eklenir ve Defold, Lua kodunu motorun yaşam döngüsü (lifecycle) işlevlerinin bir parçası olarak yürütür. Oyun nesnesi betikleri genellikle oyun nesnelerini ve bölüm yükleme, oyun kuralları gibi işlemlerle oyunu bir arada tutan mantığı denetlemek için kullanılır. Oyun nesnesi betikleri [GO](/ref/go) işlevlerine ve [GUI](/ref/gui) ile [Render](/ref/render) işlevleri dışındaki tüm Defold kütüphane işlevlerine erişebilir.


GUI betikleri
: Uzantısı _.gui_script_ şeklindedir. GUI bileşenleri tarafından çalıştırılır ve genellikle oyun içi bilgi göstergeleri, menüler vb. GUI öğelerini görüntülemek için gereken mantığı içerir. Defold, Lua kodunu motorun yaşam döngüsü işlevlerinin bir parçası olarak yürütür. GUI betikleri [GUI](/ref/gui) işlevlerine ve [GO](/ref/go) ile [Render](/ref/render) işlevleri dışındaki tüm Defold kütüphane işlevlerine erişebilir.


İşleme betikleri
: Uzantısı _.render_script_ şeklindedir. İşleme betikleri (render script), işleme hattı (rendering pipeline) tarafından çalıştırılır ve her karede uygulamanın/oyunun tüm grafiklerinden görüntü oluşturmak için gereken mantığı içerir. İşleme betiğinin oyunun yaşam döngüsünde özel bir yeri vardır. Ayrıntıları [uygulama yaşam döngüsü belgelerinde](/manuals/application-lifecycle) bulabilirsiniz. İşleme betikleri [Render](/ref/render) işlevlerine ve [GO](/ref/go) ile [GUI](/ref/gui) işlevleri dışındaki tüm Defold kütüphane işlevlerine erişebilir.


## Betik yürütme, geri çağırımlar ve self

Defold, Lua betiklerini motorun yaşam döngüsünün bir parçası olarak yürütür ve önceden tanımlanmış bir dizi geri çağırım (callback) işleviyle yaşam döngüsüne erişim sağlar. Bir oyun nesnesine betik bileşeni eklediğinizde betik, oyun nesnesinin ve bileşenlerinin yaşam döngüsünün bir parçası olur. Betik yüklendiğinde Lua bağlamında değerlendirilir; ardından motor aşağıdaki işlevleri yürütür ve geçerli betik bileşeni örneğine (instance) bir başvuruyu parametre olarak geçirir. Bileşen örneğinde durum saklamak için bu `self` başvurusunu kullanabilirsiniz.

::: important
`self`, Lua tablosu gibi davranan bir `userdata` nesnesidir; ancak üzerinde `pairs()` veya `ipairs()` ile yineleme yapamaz ve `pprint()` kullanarak içeriğini yazdıramazsınız.
:::

#### `init(self)`
Bileşenin başlangıç işlemleri sırasında çağrılır.

```lua
function init(self)
  -- These variables are available through the lifetime of the component instance
  self.my_var = "something"
  self.age = 0
end
```

#### `final(self)`
Bileşen silindiğinde çağrılır. Temizleme işlemleri için kullanışlıdır; örneğin çalışma sırasında oluşturduğunuz oyun nesnelerinin bileşen silindiğinde silinmesi gerekiyorsa kullanılabilir.

```lua
function final(self)
  if self.my_var == "something" then
      -- do some cleanup
  end
end
```

#### `fixed_update(self, dt)`
Kare hızından bağımsız güncelleme. `dt` parametresi son güncellemeden beri geçen süreyi içerir. Bu işlev, karenin zamanlamasına ve sabit zaman adımlı güncellemenin sıklığına bağlı olarak `0-N` kez çağrılır. Yalnızca *game.project* dosyasında `Physics`-->`Use Fixed Timestep` etkinleştirildiğinde ve `Engine`-->`Fixed Update Frequency` değeri 0'dan büyük olduğunda çağrılır. Kararlı bir fizik simülasyonu elde etmek için fizik nesnelerini düzenli aralıklarla değiştirmek istediğinizde kullanışlıdır.

```lua
function fixed_update(self, dt)
  msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
end
```

#### `update(self, dt)`
Her karede, tüm betiklerin `fixed_update` geri çağırımlarından sonra (Fixed Timestep etkinse) bir kez çağrılır. `dt` parametresi son kareden beri geçen süreyi içerir.

```lua
function update(self, dt)
  self.age = self.age + dt -- increase age with the timestep
end
```

#### `late_update(self, dt)`
Her karede, tüm betiklerin `update` geri çağırımlarından sonra, ancak işlemeden hemen önce bir kez çağrılır. `dt` parametresi son kareden beri geçen süreyi içerir.

```lua
function late_update(self, dt)
  go.set_position("/camera", self.final_camera_position)
end
```

#### on_message(self, message_id, message, sender)
Betik bileşenine [`msg.post()`](/ref/msg#msg.post) aracılığıyla ileti gönderildiğinde motor, alıcı bileşenin bu işlevini çağırır. [İleti aktarımı hakkında daha fazla bilgi edinin](/manuals/message-passing).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("increase_score") then
        self.total_score = self.total_score + message.score
    end
end
```

#### `on_input(self, action_id, action)`
Bu bileşen girdi odağını (input focus) aldıysa (bkz. [`acquire_input_focus`](/ref/go/#acquire_input_focus)) motor, bir girdi algılandığında bu işlevi çağırır. [Girdi işleme hakkında daha fazla bilgi edinin](/manuals/input).

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        print("Touch", action.x, action.y)
    end
end
```

#### `on_reload(self)`
Bu işlev, betik düzenleyicinin çalışma sırasında yeniden yükleme (hot reload) özelliğiyle (<kbd>Edit ▸ Reload Resource</kbd>) yeniden yüklendiğinde çağrılır. Hata ayıklama, test etme ve ince ayar yapma amacıyla çok kullanışlıdır. [Çalışma sırasında yeniden yükleme hakkında daha fazla bilgi edinin](/manuals/hot-reload).

```lua
function on_reload(self)
  print(self.age) -- print the age of this game object
end
```


## Tepkisel mantık

Betik bileşeni olan bir oyun nesnesi belirli bir mantığı uygular. Bu mantık çoğu zaman dış bir etkene bağlıdır. Bir düşmanın yapay zekâsı, oyuncunun kendi çevresindeki belirli bir yarıçaplı alanda bulunmasına tepki verebilir; oyuncunun etkileşimi sonucunda bir kapının kilidi çözülüp kapı açılabilir vb.

`update()` işlevi, her karede çalışan bir durum makinesi (state machine) olarak tanımlanan karmaşık davranışları uygulamanızı sağlar; bazen bu uygun bir yaklaşımdır. Ancak her `update()` çağrısının bir maliyeti vardır. Bu işleve gerçekten ihtiyacınız yoksa silmeniz ve mantığınızı _tepkisel_ (reactive) olarak kurmayı denemeniz önerilir. Bir iletinin tepkiyi tetiklemesini pasif biçimde beklemek, tepki verilecek veriler için oyun dünyasını etkin biçimde sorgulamaktan daha az maliyetlidir. Ayrıca bir tasarım sorununu tepkisel olarak çözmek, çoğu zaman daha temiz ve daha kararlı bir tasarım ve uygulama ortaya çıkarır.

Somut bir örneğe bakalım. Bir betik bileşeninin başlangıç işlemlerinden 2 saniye sonra bir ileti göndermesini istediğinizi varsayalım. Ardından belirli bir yanıt iletisini beklemesi ve yanıtı aldıktan 5 saniye sonra başka bir ileti göndermesi gerekir. Bunun tepkisel olmayan kodu şöyle görünebilir:

```lua
function init(self)
    -- Counter to keep track of time.
    self.counter = 0
    -- We need this to keep track of our state.
    self.state = "first"
end

function update(self, dt)
    self.counter = self.counter + dt
    if self.counter >= 2.0 and self.state == "first" then
        -- send message after 2 seconds
        msg.post("some_object", "some_message")
        self.state = "waiting"
    end
    if self.counter >= 5.0 and self.state == "second" then
        -- send message 5 seconds after we received "response"
        msg.post("another_object", "another_message")
        -- Nil the state so we don’t reach this state block again.
        self.state = nil
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("response") then
        -- “first” state done. enter next
        self.state = "second"
        -- zero the counter
        self.counter = 0
    end
end
```

Bu oldukça basit durumda bile epey karmaşık bir mantık ortaya çıkar. Bir modüldeki eş yordamların (coroutine) yardımıyla bunu iyileştirmek mümkündür (aşağıya bakın); ancak bunun yerine mantığı tepkisel hâle getirmeyi ve yerleşik bir zamanlama mekanizması kullanmayı deneyelim.

```lua
local function send_first()
	msg.post("some_object", "some_message")
end

function init(self)
	-- Wait 2s then call send_first()
	timer.delay(2, false, send_first)
end

local function send_second()
	msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
	if message_id == hash("response") then
		-- Wait 5s then call send_second()
		timer.delay(5, false, send_second)
	end
end
```

Bu daha temizdir ve takibi daha kolaydır. Mantık içindeki değişimlerini izlemenin çoğu zaman zor olduğu ve fark edilmesi güç hatalara yol açabilecek iç durum değişkenlerinden kurtuluruz. Ayrıca `update()` işlevini tamamen kaldırırız. Böylece motor, betiğimiz yalnızca boşta beklerken bile onu saniyede 60 kez çağırmak zorunda kalmaz.


## Ön işleme

Derleme çeşidine bağlı olarak kodu koşullu biçimde dahil etmek için bir Lua ön işlemcisi (preprocessor) ve özel işaretleme kullanabilirsiniz. Örnek:

```lua
-- Use one of the following keywords: RELEASE, DEBUG or HEADLESS
--#IF DEBUG
local lives_num = 999
--#ELSE 
local lives_num = 3
--#ENDIF
```

Ön işlemci bir derleme uzantısı olarak sunulur. Kurulumu ve kullanımı hakkında daha fazla bilgiyi [GitHub'daki uzantı sayfasında](https://github.com/defold/extension-lua-preprocessor) bulabilirsiniz.


## Düzenleyici desteği

Defold düzenleyicisi, sözdizimi renklendirme ve otomatik tamamlama özellikleriyle Lua betiklerini düzenlemeyi destekler. Defold işlev adlarını tamamlamak için *Ctrl+Space* tuşlarına basarak yazdığınız metinle eşleşen işlevlerin listesini açın.

![Otomatik tamamlama](images/script/completion.png)
