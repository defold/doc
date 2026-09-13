---
title: Çalışma sırasında yeniden yükleme
brief: Bu kılavuz, Defold'daki çalışma sırasında yeniden yükleme özelliğini açıklar.
---

# Kaynakları çalışma sırasında yeniden yükleme

Defold, kaynakları (resource) çalışma sırasında yeniden yüklemenizi (hot reload) sağlar. Oyun geliştirirken bu özellik belirli görevleri büyük ölçüde hızlandırır. Oyunun kodunu ve içeriğini oyun çalışırken değiştirmenize olanak tanır. Yaygın kullanım alanları şunlardır:

- Lua betiklerinde (script) oynanış parametrelerini ayarlamak.
- Grafik öğelerini (parçacık efektleri veya GUI öğeleri gibi) düzenleyip ayarlamak ve sonuçları uygun bağlamda görmek.
- Gölgelendirici (shader) kodunu düzenleyip ayarlamak ve sonuçları uygun bağlamda görmek.
- Oyunu durdurmadan bölümleri yeniden başlatarak, durumu ayarlayarak ve benzeri işlemlerle oyun testlerini kolaylaştırmak.

## Çalışma sırasında yeniden yükleme nasıl yapılır?

Oyunu düzenleyiciden başlatın (<kbd>Project ▸ Build</kbd>).

Ardından güncellenmiş bir kaynağı yeniden yüklemek için <kbd>File ▸ Hot Reload</kbd> menü öğesini seçmeniz veya klavyede ilgili kısayola basmanız yeterlidir:

![Kaynakları yeniden yükleme](images/hot-reload/menu.png)

## Cihazda çalışma sırasında yeniden yükleme

Çalışma sırasında yeniden yükleme, masaüstünde olduğu gibi cihazda da çalışır. Bu özelliği cihazda kullanmak için mobil cihazınızda oyunun hata ayıklama derlemesini veya [geliştirme uygulamasını](/manuals/dev-app) çalıştırın, ardından düzenleyicide hedef olarak seçin:

![Hedef cihaz](images/hot-reload/target.png)

Artık projeyi derleyip çalıştırdığınızda düzenleyici tüm varlıkları (asset) cihazda çalışan uygulamaya yükler ve oyunu başlatır. Bundan sonra çalışma sırasında yeniden yüklediğiniz her dosya cihazda güncellenir.

Örneğin, telefonunuzda çalışan bir oyunda gösterilen GUI'ye birkaç düğme eklemek için GUI dosyasını açmanız yeterlidir:

![GUI'yi yeniden yükleme](images/hot-reload/gui.png)

Yeni düğmeleri ekleyin, GUI dosyasını kaydedin ve çalışma sırasında yeniden yükleyin. Artık yeni düğmeleri telefon ekranında görebilirsiniz:

![Yeniden yüklenmiş GUI](images/hot-reload/gui-reloaded.png)

Bir dosyayı çalışma sırasında yeniden yüklediğinizde motor, yeniden yüklenen her kaynak dosyasını konsola yazdırır.

## Betikleri yeniden yükleme

Yeniden yüklenen her Lua betik dosyası, çalışan Lua ortamında yeniden yürütülür.

```lua
local my_value = 10

function update(self, dt)
    print(my_value)
end
```

`my_value` değerini 11 olarak değiştirip dosyayı çalışma sırasında yeniden yüklediğinizde değişiklik hemen etkili olur:

```text
...
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
INFO:RESOURCE: /main/hunter.scriptc was successfully reloaded.
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
...
```

Çalışma sırasında yeniden yüklemenin yaşam döngüsü (lifecycle) işlevlerinin yürütülmesini değiştirmediğini unutmayın. Örneğin, çalışma sırasında yeniden yükleme yapıldığında `init()` çağrılmaz. Ancak yaşam döngüsü işlevlerini yeniden tanımlarsanız yeni sürümleri kullanılır.

## Lua modüllerini yeniden yükleme

Bir modül dosyasında değişkenleri genel kapsama (global scope) eklediğiniz sürece, dosyayı yeniden yüklemek bu genel değişkenleri değiştirir:

```lua
--- my_module.lua
my_module = {}
my_module.val = 10
```

```lua
-- user.script
require "my_module"

function update(self, dt)
    print(my_module.val) -- hot reload "my_module.lua" and the new value will print
end
```

Lua modüllerinde yaygın bir yaklaşım, yerel bir tablo oluşturmak, tabloyu doldurmak ve ardından döndürmektir:

```lua
--- my_module.lua
local M = {} -- a new table object is created here
M.val = 10
return M
```

```lua
-- user.script
local mm = require "my_module"

function update(self, dt)
    print(mm.val) -- will print 10 even if you change and hot reload "my_module.lua"
end
```

`my_module.lua` dosyasını değiştirip yeniden yüklemek, `user.script` dosyasının davranışını _değiştirmez_. Bunun nedeni ve bu sorundan nasıl kaçınabileceğiniz hakkında daha fazla bilgi için [Modüller kılavuzuna](/manuals/modules) bakın.

## on_reload() işlevi

Her betik bileşeni (script component) bir `on_reload()` işlevi tanımlayabilir. Bu işlev varsa betik her yeniden yüklendiğinde çağrılır. Bu, verileri incelemek veya değiştirmek, ileti göndermek ve benzeri işlemler için kullanışlıdır:

```lua
function on_reload(self)
    print(self.velocity)

    msg.post("/level#controller", "setup")
end
```

## Gölgelendirici kodunu yeniden yükleme

Köşe gölgelendiricileri (vertex shader) ve parça gölgelendiricileri (fragment shader) yeniden yüklenirken GLSL kodu grafik sürücüsü tarafından yeniden derlenir ve GPU'ya yüklenir. Gölgelendirici kodu bir çökmeye yol açarsa motor da çöker; GLSL çok düşük düzeyde yazıldığı için buna yol açmak kolaydır.
